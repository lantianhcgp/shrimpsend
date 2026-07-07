#!/usr/bin/env python3
"""
Demo script for ShrimpSend AI Client
"""

import sys
import os
import json
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shrimpsend_ai import ShrimpSendClient


def demo_basic_usage():
    """Demonstrate basic usage of ShrimpSend AI Client."""
    print("ShrimpSend AI Client - Demo")
    print("=" * 40)
    
    # Create client with temporary config directory
    with tempfile.TemporaryDirectory() as temp_dir:
        config_dir = Path(temp_dir) / ".shrimpsend-ai"
        
        client = ShrimpSendClient(
            server="https://xiachuan.net",
            config_dir=str(config_dir)
        )
        
        print("1. Client created successfully")
        print(f"   Server: {client.server}")
        print(f"   Config dir: {config_dir}")
        
        # Test token management
        print("\n2. Testing token management...")
        test_token = "demo_jwt_token_12345"
        client.auth.set_token(test_token)
        
        if client.auth.is_authenticated():
            print("   ✓ Token set and authenticated")
        
        # Test configuration save/load
        print("\n3. Testing configuration save/load...")
        demo_config = {
            "server": "https://xiachuan.net",
            "device_id": "ai-demo-123",
            "capabilities": ["text", "file_transfer"],
            "created": "2026-07-07"
        }
        
        client.save_config(demo_config)
        loaded_config = client.load_config()
        
        if loaded_config == demo_config:
            print("   ✓ Configuration saved and loaded correctly")
        
        # Test file operations
        print("\n4. Testing file operations...")
        with tempfile.TemporaryDirectory() as file_temp:
            # Create sample file
            sample_file = Path(file_temp) / "demo.txt"
            content = "Hello from ShrimpSend AI Client Demo!\n"
            content += "This is a sample file for demonstration.\n"
            
            with open(sample_file, 'w') as f:
                f.write(content)
            
            # Verify file
            with open(sample_file, 'r') as f:
                read_content = f.read()
            
            if read_content == content:
                print("   ✓ File creation and read successful")
        
        print("\n" + "=" * 40)
        print("Demo completed successfully!")
        print("=" * 40)


def demo_cli_usage():
    """Demonstrate CLI usage."""
    print("\nCLI Usage Examples:")
    print("-" * 40)
    
    examples = [
        "# Login to ShrimpSend",
        "python -m shrimpsend_ai.cli login --server https://xiachuan.net --email user@example.com --password password",
        "",
        "# Register as AI device",
        "python -m shrimpsend_ai.cli register --name 'Omnibot AI Agent' --type AI_AGENT",
        "",
        "# List available devices",
        "python -m shrimpsend_ai.cli list-devices",
        "",
        "# Send text to device",
        "python -m shrimpsend_ai.cli send-text --device 'My Phone' --text 'Hello from AI!'",
        "",
        "# Send file to device",
        "python -m shrimpsend_ai.cli send-file --device 'My Laptop' --file /path/to/document.pdf",
        "",
        "# Send clipboard content",
        "python -m shrimpsend_ai.cli send-clipboard --device 'My Phone' --content 'Text from AI'",
        "",
        "# Logout",
        "python -m shrimpsend_ai.cli logout"
    ]
    
    for line in examples:
        print(line)


def demo_python_api():
    """Demonstrate Python API usage."""
    print("\nPython API Examples:")
    print("-" * 40)
    
    code_examples = [
        "# Basic client usage",
        "from shrimpsend_ai import ShrimpSendClient",
        "",
        "# Create client",
        "client = ShrimpSendClient(",
        "    server='https://xiachuan.net',",
        "    config_dir='/path/to/config'",
        ")",
        "",
        "# Login",
        "client.login('user@example.com', 'password')",
        "",
        "# Register as device",
        "device = client.register_device(",
        "    name='Omnibot AI Agent',",
        "    device_type='AI_AGENT'",
        ")",
        "",
        "# Send text",
        "client.send_text(",
        "    target_device='My Phone',",
        "    text='Hello from AI!'",
        ")",
        "",
        "# Send file",
        "client.send_file(",
        "    target_device='My Laptop',",
        "    file_path='/path/to/document.pdf'",
        ")",
        "",
        "# Send clipboard",
        "client.send_clipboard(",
        "    target_device='My Phone',",
        "    content='Text from AI',",
        "    content_type='text/plain'",
        ")"
    ]
    
    for line in code_examples:
        print(line)


def main():
    """Run demo."""
    demo_basic_usage()
    demo_cli_usage()
    demo_python_api()
    
    print("\n" + "=" * 40)
    print("Next Steps:")
    print("1. Get a ShrimpSend account at https://xiachuan.net")
    print("2. Login using the CLI command above")
    print("3. Register your AI agent as a device")
    print("4. Start sending files and text to your devices!")
    print("=" * 40)


if __name__ == "__main__":
    main()