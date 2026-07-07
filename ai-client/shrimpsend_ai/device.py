"""
ShrimpSend AI Client - Device Manager
"""

import uuid
from typing import Optional, Dict, Any, List

import requests

from .auth import AuthManager


class DeviceManager:
    """
    Manages device registration and management.
    """
    
    def __init__(
        self,
        server: str,
        auth: AuthManager,
        timeout: int = 30
    ):
        """
        Initialize device manager.
        
        Args:
            server: ShrimpSend server URL
            auth: Authentication manager
            timeout: Request timeout
        """
        self.server = server
        self.auth = auth
        self.timeout = timeout
    
    def _get_headers(self) -> Dict[str, str]:
        """Get authentication headers."""
        return self.auth.get_auth_headers()
    
    def register(
        self,
        name: str = "Omnibot AI Agent",
        device_type: str = "AI_AGENT",
        platform: str = "Linux/Alpine",
        capabilities: Optional[List[str]] = None,
        device_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Register AI agent as a device.
        
        Args:
            name: Device name
            device_type: Device type
            platform: Platform name
            capabilities: List of capabilities
            device_id: Optional device ID (generated if not provided)
            
        Returns:
            Device information
            
        Raises:
            requests.RequestException: If request fails
        """
        if not self.auth.is_authenticated():
            raise ValueError("Not authenticated")
        
        if device_id is None:
            device_id = f"ai-{uuid.uuid4().hex[:12]}"
        
        if capabilities is None:
            capabilities = ["text", "file_transfer"]
        
        url = f"{self.server}/api/devices"
        payload = {
            'deviceId': device_id,
            'name': name,
            'type': device_type,
            'platform': platform,
            'capabilities': capabilities
        }
        
        response = requests.post(
            url,
            json=payload,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        
        if response.status_code == 200:
            return response.json()
        
        raise requests.RequestException(
            f"Device registration failed: {response.status_code}"
        )
    
    def list(self) -> List[Dict[str, Any]]:
        """
        List all devices.
        
        Returns:
            List of device information
            
        Raises:
            requests.RequestException: If request fails
        """
        if not self.auth.is_authenticated():
            raise ValueError("Not authenticated")
        
        url = f"{self.server}/api/devices"
        
        response = requests.get(
            url,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        
        if response.status_code == 200:
            return response.json()
        
        raise requests.RequestException(
            f"Failed to list devices: {response.status_code}"
        )
    
    def get_info(self, device_id: str) -> Dict[str, Any]:
        """
        Get device information.
        
        Args:
            device_id: Device ID
            
        Returns:
            Device information
            
        Raises:
            requests.RequestException: If request fails
        """
        if not self.auth.is_authenticated():
            raise ValueError("Not authenticated")
        
        url = f"{self.server}/api/devices/{device_id}"
        
        response = requests.get(
            url,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        
        if response.status_code == 200:
            return response.json()
        
        raise requests.RequestException(
            f"Failed to get device info: {response.status_code}"
        )
    
    def update(
        self,
        device_id: str,
        name: Optional[str] = None,
        platform: Optional[str] = None,
        capabilities: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Update device information.
        
        Args:
            device_id: Device ID
            name: New device name
            platform: New platform
            capabilities: New capabilities
            
        Returns:
            Updated device information
            
        Raises:
            requests.RequestException: If request fails
        """
        if not self.auth.is_authenticated():
            raise ValueError("Not authenticated")
        
        url = f"{self.server}/api/devices/{device_id}"
        
        payload = {}
        if name is not None:
            payload['name'] = name
        if platform is not None:
            payload['platform'] = platform
        if capabilities is not None:
            payload['capabilities'] = capabilities
        
        response = requests.patch(
            url,
            json=payload,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        
        if response.status_code == 200:
            return response.json()
        
        raise requests.RequestException(
            f"Failed to update device: {response.status_code}"
        )
    
    def update_presence(
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
            
        Raises:
            requests.RequestException: If request fails
        """
        if not self.auth.is_authenticated():
            raise ValueError("Not authenticated")
        
        url = f"{self.server}/api/devices/{device_id}/presence"
        
        payload = {
            'isOnline': is_online
        }
        
        if ip_address is not None:
            payload['ipAddress'] = ip_address
        if port is not None:
            payload['port'] = port
        
        response = requests.post(
            url,
            json=payload,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        
        if response.status_code == 200:
            return response.json()
        
        raise requests.RequestException(
            f"Failed to update presence: {response.status_code}"
        )
    
    def unregister(self, device_id: str) -> bool:
        """
        Unregister device.
        
        Args:
            device_id: Device ID
            
        Returns:
            True if successful
            
        Raises:
            requests.RequestException: If request fails
        """
        if not self.auth.is_authenticated():
            raise ValueError("Not authenticated")
        
        url = f"{self.server}/api/devices/{device_id}"
        
        response = requests.delete(
            url,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        
        return response.status_code == 204
    
    def find_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Find device by name.
        
        Args:
            name: Device name
            
        Returns:
            Device information or None
        """
        devices = self.list()
        for device in devices:
            if device.get('name') == name:
                return device
        return None
    
    def find_by_type(self, device_type: str) -> List[Dict[str, Any]]:
        """
        Find devices by type.
        
        Args:
            device_type: Device type
            
        Returns:
            List of matching devices
        """
        devices = self.list()
        return [d for d in devices if d.get('type') == device_type]
    
    def get_ai_devices(self) -> List[Dict[str, Any]]:
        """
        Get all AI agent devices.
        
        Returns:
            List of AI devices
        """
        return self.find_by_type("AI_AGENT")