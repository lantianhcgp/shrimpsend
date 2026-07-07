"""
ShrimpSend AI Client - Main client class
"""

import os
import json
from typing import Optional, Dict, Any, List
from pathlib import Path

from .auth import AuthManager
from .device import DeviceManager
from .transfer import TransferManager


class ShrimpSendClient:
    """
    Main client for AI agents to interact with ShrimpSend.
    
    Usage:
        client = ShrimpSendClient(
            server="https://xiachuan.net",
            token="jwt_token_here"
        )
        
        # Register as device
        device = client.register_device(
            name="Omnibot AI Agent",
            type="AI_AGENT"
        )
        
        # Send text
        client.send_text(
            target_device="My Phone",
            text="Hello from AI!"
        )
        
        # Send file
        client.send_file(
            target_device="My Laptop",
            file_path="/path/to/document.pdf"
        )
    """
    
    def __init__(
        self,
        server: str,
        token: Optional[str] = None,
        config_dir: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize ShrimpSend client.
        
        Args:
            server: ShrimpSend server URL (e.g., "https://xiachuan.net")
            token: JWT authentication token
            config_dir: Directory to store configuration
            timeout: Request timeout in seconds
        """
        self.server = server.rstrip('/')
        self.timeout = timeout
        
        # Setup config directory
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = Path.home() / ".shrimpsend-ai"
        
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize managers
        self.auth = AuthManager(
            server=self.server,
            config_dir=self.config_dir,
            timeout=self.timeout
        )
        
        self.device = DeviceManager(
            server=self.server,
            auth=self.auth,
            timeout=self.timeout
        )
        
        self.transfer = TransferManager(
            server=self.server,
            auth=self.auth,
            device=self.device,
            timeout=self.timeout
        )
        
        # Set token if provided
        if token:
            self.auth.set_token(token)
    
    def login(self, email: str, password: str) -> bool:
        """
        Login to ShrimpSend.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            True if login successful
        """
        return self.auth.login(email, password)
    
    def register_device(
        self,
        name: str = "Omnibot AI Agent",
        device_type: str = "AI_AGENT",
        platform: str = "Linux/Alpine",
        capabilities: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Register AI agent as a device.
        
        Args:
            name: Device name
            device_type: Device type
            platform: Platform name
            capabilities: List of capabilities
            
        Returns:
            Device information
        """
        if capabilities is None:
            capabilities = ["text", "file_transfer"]
        
        return self.device.register(
            name=name,
            device_type=device_type,
            platform=platform,
            capabilities=capabilities
        )
    
    def list_devices(self) -> List[Dict[str, Any]]:
        """
        List all devices.
        
        Returns:
            List of device information
        """
        return self.device.list()
    
    def send_text(
        self,
        target_device: str,
        text: str,
        thread_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send text to a target device.
        
        Args:
            target_device: Target device name or ID
            text: Text content to send
            thread_id: Optional thread ID for conversation
            
        Returns:
            Transfer information
        """
        return self.transfer.send_text(
            target_device=target_device,
            text=text,
            thread_id=thread_id
        )
    
    def send_file(
        self,
        target_device: str,
        file_path: str,
        thread_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send file to a target device.
        
        Args:
            target_device: Target device name or ID
            file_path: Path to file to send
            thread_id: Optional thread ID for conversation
            
        Returns:
            Transfer information
        """
        return self.transfer.send_file(
            target_device=target_device,
            file_path=file_path,
            thread_id=thread_id
        )
    
    def send_clipboard(
        self,
        target_device: str,
        content: str,
        content_type: str = "text/plain",
        thread_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send clipboard content to a target device.
        
        Args:
            target_device: Target device name or ID
            content: Clipboard content
            content_type: MIME type of content
            thread_id: Optional thread ID for conversation
            
        Returns:
            Transfer information
        """
        return self.transfer.send_clipboard(
            target_device=target_device,
            content=content,
            content_type=content_type,
            thread_id=thread_id
        )
    
    def get_device_info(self, device_id: str) -> Dict[str, Any]:
        """
        Get device information.
        
        Args:
            device_id: Device ID
            
        Returns:
            Device information
        """
        return self.device.get_info(device_id)
    
    def update_device_presence(
        self,
        device_id: str,
        is_online: bool = True,
        ip_address: Optional[str] = None,
        port: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Update device presence.
        
        Args:
            device_id: Device ID
            is_online: Whether device is online
            ip_address: Device IP address
            port: Device port
            
        Returns:
            Updated device information
        """
        return self.device.update_presence(
            device_id=device_id,
            is_online=is_online,
            ip_address=ip_address,
            port=port
        )
    
    def save_config(self, config: Dict[str, Any]) -> None:
        """
        Save configuration to file.
        
        Args:
            config: Configuration dictionary
        """
        config_file = self.config_dir / "config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Returns:
            Configuration dictionary
        """
        config_file = self.config_dir / "config.json"
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        return {}
    
    @classmethod
    def from_config(cls, config_path: Optional[str] = None) -> 'ShrimpSendClient':
        """
        Create client from configuration file.
        
        Args:
            config_path: Path to config file
            
        Returns:
            Configured client instance
        """
        if config_path:
            config_file = Path(config_path)
        else:
            config_file = Path.home() / ".shrimpsend-ai" / "config.json"
        
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        return cls(
            server=config['server'],
            token=config.get('token'),
            config_dir=str(config_file.parent)
        )