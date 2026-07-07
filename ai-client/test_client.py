#!/usr/bin/env python3
"""
Test script for ShrimpSend AI Client
"""

import sys
import os
import json
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shrimpsend_ai import ShrimpSendClient


def test_config_directory():
    """Test configuration directory setup."""
    print("1. Testing configuration directory setup...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_dir = Path(temp_dir) / ".shrimpsend-ai"
        
        client = ShrimpSendClient(
            server="https://xiachuan.net",
            config_dir=str(config_dir)
        )
        
        assert config_dir.exists(), "Config directory should be created"
        print("✓ Configuration directory created successfully")
        return client


def test_auth_manager(client):
    """Test authentication manager."""
    print("\n2. Testing authentication manager...")
    
    # Test token management
    test_token = "test_jwt_token_12345"
    client.auth.set_token(test_token)
    
    assert client.auth.get_token() == test_token, "Token should be set"
    assert client.auth.is_authenticated(), "Should be authenticated with token"
    
    # Test logout
    client.auth.logout()
    assert not client.auth.is_authenticated(), "Should not be authenticated after logout"
    
    print("✓ Authentication manager works correctly")
    return True


def test_device_manager(client):
    """Test device manager (mock)."""
    print("\n3. Testing device manager...")
    
    # Note: This would require a real server for actual testing
    # For now, we'll just test the manager initialization
    
    assert client.device is not None, "Device manager should be initialized"
    assert client.device.server == client.server, "Server should match"
    
    print("✓ Device manager initialized correctly")
    return True


def test_transfer_manager(client):
    """Test transfer manager (mock)."""
    print("\n4. Testing transfer manager...")
    
    assert client.transfer is not None, "Transfer manager should be initialized"
    assert client.transfer.server == client.server, "Server should match"
    
    print("✓ Transfer manager initialized correctly")
    return True


def test_config_save_load(client):
    """Test configuration save and load."""
    print("\n5. Testing configuration save/load...")
    
    # Save config
    test_config = {
        "server": "https://test.example.com",
        "device_id": "ai-test-123",
        "last_used": "2026-07-07"
    }
    
    client.save_config(test_config)
    
    # Load config
    loaded_config = client.load_config()
    
    assert loaded_config == test_config, "Loaded config should match saved config"
    
    print("✓ Configuration save/load works correctly")
    return True


def test_cli_help():
    """Test CLI help."""
    print("\n6. Testing CLI help...")
    
    # Import CLI module
    from shrimpsend_ai.cli import main
    
    # Test help (should not exit with error)
    try:
        # This will print help and exit
        main(['--help'])
    except SystemExit as e:
        # --help causes SystemExit(0), which is expected
        assert e.code == 0, "Help should exit with code 0"
    
    print("✓ CLI help works correctly")
    return True


def test_file_operations():
    """Test file operations."""
    print("\n7. Testing file operations...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test file
        test_file = Path(temp_dir) / "test.txt"
        test_content = "Hello from ShrimpSend AI Client!\n"
        
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        # Verify file exists
        assert test_file.exists(), "Test file should exist"
        
        # Read file
        with open(test_file, 'r') as f:
            content = f.read()
        
        assert content == test_content, "File content should match"
        
        print("✓ File operations work correctly")
        return True


def main():
    """Run all tests."""
    print("ShrimpSend AI Client - Test Suite")
    print("=" * 40)
    
    try:
        # Run tests
        client = test_config_directory()
        test_auth_manager(client)
        test_device_manager(client)
        test_transfer_manager(client)
        test_config_save_load(client)
        test_cli_help()
        test_file_operations()
        
        print("\n" + "=" * 40)
        print("All tests passed! ✓")
        print("=" * 40)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())