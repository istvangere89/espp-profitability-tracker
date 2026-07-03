"""
Integration tests for CDK infrastructure
Tests for common deployment issues encountered during development
"""

import os
import sys
import json
import re
import unittest
from pathlib import Path

# Add paths for imports
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root / 'infrastructure' / 'lambda' / 'cors_proxy'))
sys.path.insert(0, str(repo_root / 'infrastructure' / 'cdk'))

from index import handler


class TestLambdaPathResolution(unittest.TestCase):
    """Test that Lambda handler can be imported from any directory"""
    
    def test_lambda_import_works(self):
        """Lambda handler should be importable"""
        self.assertIsNotNone(handler)
        self.assertTrue(callable(handler))
    
    def test_lambda_handler_responds(self):
        """Lambda handler should respond to valid requests"""
        event = {
            'queryStringParameters': {
                'url': 'https://api.exchangerate-api.com/v4/latest/USD'
            }
        }
        response = handler(event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Cache-Control', response['headers'])
        self.assertEqual(response['headers']['Cache-Control'], 'public, max-age=3600')


class TestCDKAssetPaths(unittest.TestCase):
    """Test that CDK asset paths are correct relative to infrastructure/cdk/"""
    
    def setUp(self):
        self.cdk_dir = repo_root / 'infrastructure' / 'cdk'
    
    def test_lambda_asset_path_exists(self):
        """Lambda code path should exist relative to CDK directory"""
        # Path used in stock_tracker_stack.py: ../lambda/cors_proxy
        lambda_path = (self.cdk_dir / '..' / 'lambda' / 'cors_proxy').resolve()
        self.assertTrue(lambda_path.exists(), f"Lambda path not found: {lambda_path}")
        self.assertTrue((lambda_path / 'index.py').exists(), 
                       f"Lambda index.py not found in {lambda_path}")
    
    def test_src_asset_path_exists(self):
        """Frontend source path should exist relative to CDK directory"""
        # Path used in stock_tracker_stack.py: ../../src
        src_path = (self.cdk_dir / '..' / '..' / 'src').resolve()
        self.assertTrue(src_path.exists(), f"Source path not found: {src_path}")
        self.assertTrue((src_path / 'index.html').exists(),
                       f"index.html not found in {src_path}")


class TestPythonSyntax(unittest.TestCase):
    """Test Python files for syntax errors"""
    
    def test_all_python_files_compile(self):
        """All Python files should compile without syntax errors"""
        python_files = [
            'scripts/deploy.py',
            'scripts/check_aws_setup.py',
            'scripts/test_lambda.py',
            'dev/proxy_server.py',
            'infrastructure/cdk/app.py',
            'infrastructure/cdk/stacks/__init__.py',
            'infrastructure/cdk/stacks/stock_tracker_stack.py',
            'infrastructure/lambda/cors_proxy/index.py'
        ]
        
        for file_path in python_files:
            full_path = repo_root / file_path
            with self.subTest(file=file_path):
                self.assertTrue(full_path.exists(), f"File not found: {file_path}")
                
                # Try to compile
                with open(full_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                try:
                    compile(code, file_path, 'exec')
                except SyntaxError as e:
                    self.fail(f"Syntax error in {file_path}: {e}")


class TestAPIGatewayConfiguration(unittest.TestCase):
    """Test API Gateway configuration"""
    
    def test_cloudwatch_role_exists(self):
        """API Gateway should have CloudWatch Logs role configured"""
        stack_path = repo_root / 'infrastructure' / 'cdk' / 'stacks' / 'stock_tracker_stack.py'
        with open(stack_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for CloudWatch role creation
        self.assertIn('ApiGatewayCloudWatchRole', content,
                     "API Gateway CloudWatch role should be created")
        
        # Check for CfnAccount resource
        self.assertIn('CfnAccount', content,
                     "CfnAccount should be used to set CloudWatch role")
        
        # Check for the managed policy
        self.assertIn('AmazonAPIGatewayPushToCloudWatchLogs', content,
                     "Should use AmazonAPIGatewayPushToCloudWatchLogs policy")


class TestWorkflowConfiguration(unittest.TestCase):
    """Test GitHub Actions workflow configuration"""
    
    def test_workflow_uses_node_24(self):
        """Workflow should use Node.js 24 (not outdated versions)"""
        workflow_path = repo_root / '.github' / 'workflows' / 'deploy.yml'
        with open(workflow_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check NODE_VERSION
        node_version_match = re.search(r"NODE_VERSION:\s*['\"](\d+)['\"]", content)
        self.assertIsNotNone(node_version_match, "NODE_VERSION not found in workflow")
        
        node_version = int(node_version_match.group(1))
        self.assertGreaterEqual(node_version, 24, 
                               f"Node.js version {node_version} is outdated, should be 24+")
    
    def test_workflow_uses_github_variable(self):
        """Workflow should use vars.AWS_GITHUB_ROLE_ARN (not secrets)"""
        workflow_path = repo_root / '.github' / 'workflows' / 'deploy.yml'
        with open(workflow_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for correct variable reference
        self.assertIn('vars.AWS_GITHUB_ROLE_ARN', content,
                     "Workflow should use vars.AWS_GITHUB_ROLE_ARN")
        
        # Should not use secrets for role ARN
        if 'AWS_GITHUB_ROLE_ARN' in content:
            self.assertNotIn('secrets.AWS_GITHUB_ROLE_ARN', content,
                           "Workflow should use vars not secrets for role ARN")
    
    def test_workflow_deploys_stack(self):
        """Workflow should deploy the main stack"""
        workflow_path = repo_root / '.github' / 'workflows' / 'deploy.yml'
        with open(workflow_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for deploy command
        self.assertIn('cdk deploy', content,
                     "Workflow should use 'cdk deploy' to deploy the stack")


def run_tests():
    """Run all tests and return results"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
