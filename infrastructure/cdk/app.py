#!/usr/bin/env python3
"""
AWS CDK App for EPAM Stock Tracker
Deploys static website with Lambda CORS proxy
"""

import aws_cdk as cdk
from stacks.stock_tracker_stack import StockTrackerStack

app = cdk.App()

StockTrackerStack(
    app, 
    "EpamStockTrackerStack",
    description="EPAM Stock Tracker with S3, CloudFront, Lambda CORS Proxy",
    env=cdk.Environment(
        account=app.node.try_get_context("account"),
        region=app.node.try_get_context("region") or "us-east-1"
    )
)

app.synth()
