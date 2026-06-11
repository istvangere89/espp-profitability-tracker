#!/usr/bin/env python3
"""
Deployment script for EPAM Stock Tracker
Updates api.js with the API Gateway URL before deploying
"""

import json
import subprocess
import sys
import re


def get_api_endpoint():
    """Get the API Gateway endpoint from CDK outputs"""
    try:
        result = subprocess.run(
            ["cdk", "output", "ApiUrlForConfig", "--json"],
            cwd="infrastructure/cdk",
            capture_output=True,
            text=True,
            check=True
        )
        outputs = json.loads(result.stdout)
        return outputs.get("EpamStockTrackerStack", {}).get("ApiUrlForConfig")
    except Exception as e:
        print(f"Warning: Could not get API endpoint: {e}")
        return None


def update_api_js(api_endpoint):
    """Update api.js to use the deployed API Gateway endpoint"""
    if not api_endpoint:
        print("Skipping api.js update - no API endpoint available")
        return
    
    print(f"Updating api.js with API endpoint: {api_endpoint}")
    
    with open("src/js/api.js", "r") as f:
        content = f.read()
    
    # Replace localhost:8080 with API Gateway endpoint
    updated_content = re.sub(
        r'http://localhost:8080\?url=',
        api_endpoint,
        content
    )
    
    with open("src/js/api.js", "w") as f:
        f.write(updated_content)
    
    print("✅ api.js updated successfully")


def main():
    print("🚀 Starting EPAM Stock Tracker deployment...")
    
    # Check if CDK is installed
    try:
        subprocess.run(["cdk", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ AWS CDK not found. Install it with: npm install -g aws-cdk")
        sys.exit(1)
    
    # Install CDK dependencies
    print("\n📦 Installing CDK dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "infrastructure/cdk/requirements.txt"], check=True)
    
    # Bootstrap CDK (if not already done)
    print("\n🔧 Bootstrapping CDK (if needed)...")
    subprocess.run(["cdk", "bootstrap"], cwd="infrastructure/cdk")
    
    # Deploy the stack
    print("\n☁️  Deploying to AWS...")
    result = subprocess.run(["cdk", "deploy", "--require-approval", "never"], cwd="infrastructure/cdk")
    
    if result.returncode != 0:
        print("❌ Deployment failed")
        sys.exit(1)
    
    # Get and update API endpoint
    print("\n🔄 Updating API configuration...")
    api_endpoint = get_api_endpoint()
    if api_endpoint:
        update_api_js(api_endpoint)
        
        # Redeploy to update the files
        print("\n📤 Redeploying with updated configuration...")
        subprocess.run(["cdk", "deploy", "--require-approval", "never"], cwd="infrastructure/cdk")
    
    # Show outputs
    print("\n✅ Deployment complete!")
    print("\n📊 Stack outputs:")
    subprocess.run(["cdk", "output"], cwd="infrastructure/cdk")
    
    print("\n🎉 Your EPAM Stock Tracker is now live!")
    print("\nNext steps:")
    print("  1. Open the WebsiteURL in your browser")
    print("  2. Your data is stored locally in the browser")
    print("  3. To destroy the stack: cd infrastructure/cdk && cdk destroy")


if __name__ == "__main__":
    main()
