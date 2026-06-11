#!/usr/bin/env python3
"""
AWS CDK App for EPAM Stock Tracker
Deploys static website with Lambda CORS proxy
Uses two stacks:
- WafStack in us-east-1 (CloudFront WAF requirement)
- StockTrackerStack in eu-central-1 (main application)
"""

import os
import aws_cdk as cdk
from stacks.waf_stack import WafStack
from stacks.stock_tracker_stack import StockTrackerStack

app = cdk.App()

# Get region from context, environment variable, or default to eu-central-1
region = (
    app.node.try_get_context("region") 
    or os.environ.get("AWS_REGION") 
    or os.environ.get("AWS_DEFAULT_REGION")
    or "eu-central-1"
)

account = app.node.try_get_context("account") or os.environ.get("CDK_DEFAULT_ACCOUNT")

# Create WAF stack in us-east-1 (required for CloudFront)
waf_stack = WafStack(
    app,
    "EpamStockTrackerWafStack",
    description="WAF WebACL for EPAM Stock Tracker CloudFront (us-east-1)",
    cross_region_references=True,  # Enable cross-region references
    env=cdk.Environment(
        account=account,
        region="us-east-1"  # Must be us-east-1 for CloudFront WAF
    )
)

# Create main application stack in specified region
main_stack = StockTrackerStack(
    app, 
    "EpamStockTrackerStack",
    description="EPAM Stock Tracker with S3, CloudFront, Lambda CORS Proxy",
    waf_acl_arn=waf_stack.waf_web_acl.attr_arn,  # Cross-region reference
    cross_region_references=True,  # Enable cross-region references
    env=cdk.Environment(
        account=account,
        region=region
    )
)

# Main stack depends on WAF stack
main_stack.add_dependency(waf_stack)

app.synth()
