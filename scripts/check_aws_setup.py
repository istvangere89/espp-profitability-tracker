#!/usr/bin/env python3
"""
AWS Prerequisites Checker
Verifies all requirements are installed before deployment
"""

import subprocess
import sys
import os
from pathlib import Path


def check_command(command, name, install_help):
    """Check if a command is available"""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True
        )
        if result.returncode == 0:
            version = result.stdout.strip().split('\n')[0]
            print(f"✅ {name}: {version}")
            return True
    except Exception:
        pass
    
    print(f"❌ {name}: Not found")
    print(f"   Install: {install_help}")
    return False


def check_aws_credentials():
    """Check if AWS credentials are configured"""
    try:
        result = subprocess.run(
            ["aws", "sts", "get-caller-identity"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            import json
            identity = json.loads(result.stdout)
            print(f"✅ AWS Credentials: Configured (Account: {identity['Account']})")
            return True
    except Exception:
        pass
    
    print("❌ AWS Credentials: Not configured")
    print("   Configure: aws configure")
    return False


def main():
    print("🔍 Checking AWS Deployment Prerequisites")
    print("=" * 60)
    
    checks = []
    
    # Check Python
    checks.append(check_command(
        "python --version",
        "Python",
        "Download from https://python.org"
    ))
    
    # Check Node.js
    checks.append(check_command(
        "node --version",
        "Node.js",
        "Download from https://nodejs.org (required for CDK)"
    ))
    
    # Check npm
    checks.append(check_command(
        "npm --version",
        "npm",
        "Installed with Node.js"
    ))
    
    # Check AWS CLI
    checks.append(check_command(
        "aws --version",
        "AWS CLI",
        "Download from https://aws.amazon.com/cli/"
    ))
    
    # Check AWS CDK
    checks.append(check_command(
        "cdk --version",
        "AWS CDK",
        "npm install -g aws-cdk"
    ))
    
    print("\n" + "=" * 60)
    
    # Check AWS credentials if CLI is installed
    if checks[3]:  # AWS CLI check
        checks.append(check_aws_credentials())
    
    print("\n" + "=" * 60)
    
    # Summary
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"\n✅ All checks passed! ({passed}/{total})")
        print("\n🚀 Ready to deploy! Run: python deploy.py")
        return 0
    else:
        print(f"\n⚠️  {total - passed} check(s) failed ({passed}/{total} passed)")
        print("\n📝 Install missing requirements and run this script again")
        print("   For detailed instructions, see DEPLOYMENT.md")
        return 1


if __name__ == "__main__":
    sys.exit(main())
