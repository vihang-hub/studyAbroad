"""
Integration test script to verify all modules are properly wired

Run this script to verify:
1. Configuration loading works
2. Feature flags are properly initialized
3. Database adapter is created correctly
4. Logging is configured
5. Dependencies can be imported
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_configuration():
    """Test configuration loading"""
    print("\n=== Testing Configuration ===")
    try:
        from config.loader import ConfigLoader
        
        config = ConfigLoader.load()
        print(f"✓ Configuration loaded successfully")
        print(f"  - Environment: {config.ENVIRONMENT_MODE}")
        print(f"  - App Version: {config.APP_VERSION}")
        print(f"  - Log Level: {config.LOG_LEVEL}")
        return True
    except Exception as e:
        print(f"✗ Configuration loading failed: {e}")
        return False


def test_feature_flags():
    """Test feature flag initialization"""
    print("\n=== Testing Feature Flags ===")
    try:
        from feature_flags.evaluator import FeatureFlagEvaluator
        from feature_flags.types import Feature
        
        evaluator = FeatureFlagEvaluator()
        flags = evaluator.get_all_flags()
        
        print(f"✓ Feature flags initialized successfully")
        print(f"  - Supabase: {flags.get(Feature.SUPABASE.value)}")
        print(f"  - Payments: {flags.get(Feature.PAYMENTS.value)}")
        print(f"  - Rate Limiting: {flags.get(Feature.RATE_LIMITING.value)}")
        print(f"  - Observability: {flags.get(Feature.OBSERVABILITY.value)}")
        return True
    except Exception as e:
        print(f"✗ Feature flag initialization failed: {e}")
        return False


def test_logging():
    """Test logging configuration"""
    print("\n=== Testing Logging ===")
    try:
        from logging_lib.logger import get_logger
        from logging_lib.correlation import CorrelationContext
        
        logger = get_logger()
        
        with CorrelationContext("test-correlation-id"):
            logger.info("test_log_message", test_field="test_value")
        
        print(f"✓ Logging configured successfully")
        print(f"  - Logger type: {type(logger).__name__}")
        return True
    except Exception as e:
        print(f"✗ Logging configuration failed: {e}")
        return False


def test_database():
    """Test database adapter creation"""
    print("\n=== Testing Database ===")
    try:
        from database.adapters.factory import get_database_adapter
        
        # Don't actually connect, just verify adapter can be created
        adapter = get_database_adapter()
        
        print(f"✓ Database adapter created successfully")
        print(f"  - Adapter type: {type(adapter).__name__}")
        return True
    except Exception as e:
        print(f"✗ Database adapter creation failed: {e}")
        return False


def test_dependencies():
    """Test dependency injection module"""
    print("\n=== Testing Dependencies ===")
    try:
        from dependencies import (
            get_config,
            get_feature_flags,
            get_logger,
        )
        
        config = get_config()
        feature_flags = get_feature_flags()
        logger = get_logger()
        
        print(f"✓ Dependencies module working")
        print(f"  - Config: {type(config).__name__}")
        print(f"  - Feature Flags: {type(feature_flags).__name__}")
        print(f"  - Logger: {type(logger).__name__}")
        return True
    except Exception as e:
        print(f"✗ Dependencies module failed: {e}")
        return False


def test_api_imports():
    """Test that API routes can be imported"""
    print("\n=== Testing API Imports ===")
    try:
        from api.routes import health, reports, webhooks, stream
        
        print(f"✓ API routes imported successfully")
        print(f"  - Health: {health.router.prefix}")
        print(f"  - Reports: {reports.router.prefix}")
        print(f"  - Webhooks: {webhooks.router.prefix}")
        print(f"  - Stream: {stream.router.prefix}")
        return True
    except Exception as e:
        print(f"✗ API imports failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all integration tests"""
    print("=" * 60)
    print("FastAPI Backend Integration Tests")
    print("=" * 60)
    
    results = {
        "Configuration": test_configuration(),
        "Feature Flags": test_feature_flags(),
        "Logging": test_logging(),
        "Database": test_database(),
        "Dependencies": test_dependencies(),
        "API Imports": test_api_imports(),
    }
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:.<40} {status}")
    
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    failed_tests = total_tests - passed_tests
    
    print(f"\nTotal: {total_tests} | Passed: {passed_tests} | Failed: {failed_tests}")
    
    if all(results.values()):
        print("\n🎉 All integration tests passed!")
        return 0
    else:
        print("\n❌ Some integration tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
