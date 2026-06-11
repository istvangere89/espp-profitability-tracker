#!/usr/bin/env python3
"""
AWS CDK App for EPAM Stock Tracker
Deploys static website with Lambda CORS proxy
"""

import os
import aws_cdk as cdk
from stacks.stock_tracker_stack import StockTrackerStack

app = cdk.App()

# Get region from context, environment variable, or default to eu-central-1
region = (
    app.node.try_get_context("region") 
    or os.environ.get("AWS_REGION") 
    or os.environ.get("AWS_DEFAULT_REGION")
    or "eu-central-1"
)

StockTrackerStack(
    app, 
    "EpamStockTrackerStack",
    description="EPAM Stock Tracker with S3, CloudFront, Lambda CORS Proxy",
    env=cdk.Environment(
        account=app.node.try_get_context("account") or os.environ.get("CDK_DEFAULT_ACCOUNT"),
        region=region
    )
)

app.synth()
