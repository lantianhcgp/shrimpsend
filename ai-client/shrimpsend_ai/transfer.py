"""
ShrimpSend AI Client - Transfer Manager
"""

import os
import hashlib
import uuid
from pathlib import Path
from typing import Optional, Dict, Any, BinaryIO
import mimetypes

import requests

from .auth import AuthManager
from .device import DeviceManager


class TransferManager:
    """
    Manages file and content transfers.
    """
    
    def __init__(
        self,
        server: str,
        auth: AuthManager,
        device: DeviceManager,
        timeout: int = 30
    ):
        """
        Initialize transfer manager.
        
        Args:
            server: ShrimpSend server URL
            auth: Authentication manager
            device: Device manager
            timeout: Request timeout
        """
        self.server = server
        self.auth = auth
        self.device = device
        self.timeout = timeout
    
    def _get_headers(self) -> Dict[str, str]:
        """Get authentication headers."""
        return self.auth.get_auth_headers()
    
    def _calculate_hash(self, file_path: str) -> str:
        """
        Calculate SHA-256 hash of file.
        
        Args:
            file_path: Path to file
            
        Returns:
            SHA-256 hash
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def _generate_file_id(self, file_path: str, file_size: int) -> str:
        """
        Generate file ID.
        
        Args:
            file_path: Path to file
            file_size: File size
            
        Returns:
            File ID
        """
        # According to protocol: hash(fileName)_fileSize
        file_name = os.path.basename(file_path)
        file_hash = hashlib.md5(file_name.encode()).hexdigest()
        return f"{file_hash}_{file_size}"
    
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
            thread_id: Optional thread ID
            
        Returns:
            Transfer information
        """
        if not self.auth.is_authenticated():
            raise ValueError("Not authenticated")
        
        # Find target device
        device_info = self.device.find_by_name(target_device)
        if not device_info:
            device_info = self.device.get_info(target_device)
        
        target_device_id = device_info.get('deviceId')
        
        # Create transfer request
        url = f"{self.server}/api/transfer/text"
        payload = {
            'targetDeviceId': target_device_id,
            'content': text,
            'contentType': 'text/plain'
        }
        
        if thread_id:
            payload['threadId'] = thread_id
        
        response = requests.post(
            url,
            json=payload,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        
        if response.status_code == 200:
            return response.json()
        
        raise requests.RequestException(
            f"Failed to send text: {response.status_code}"
        )
    
    def send_file(
        self,
        target_device: str,
        file_path: str,
        thread_id: Optional[str] = None,
        chunk_size: int = 1024 * 1024  # 1MB chunks
    ) -> Dict[str, Any]:
        """
        Send file to a target device.
        
        Args:
            target_device: Target device name or ID
            file_path: Path to file to send
            thread_id: Optional thread ID
            chunk_size: Chunk size for upload
            
        Returns:
            Transfer information
        """
        if not self.auth.is_authenticated():
            raise ValueError("Not authenticated")
        
        # Check file exists
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_size = path.stat().st_size
        file_hash = self._calculate_hash(file_path)
        file_id = self._generate_file_id(file_path, file_size)
        
        # Find target device
        device_info = self.device.find_by_name(target_device)
        if not device_info:
            device_info = self.device.get_info(target_device)
        
        target_device_id = device_info.get('deviceId')
        target_ip = device_info.get('ipAddress')
        target_port = device_info.get('port', 9000)
        
        # Try HTTP direct push first
        if target_ip:
            try:
                return self._send_file_direct(
                    target_ip=target_ip,
                    target_port=target_port,
                    file_path=file_path,
                    file_size=file_size,
                    file_hash=file_hash,
                    file_id=file_id,
                    thread_id=thread_id,
                    chunk_size=chunk_size
                )
            except Exception as e:
                # Fall back to S3 relay
                pass
        
        # Use S3 relay as fallback
        return self._send_file_relay(
            target_device_id=target_device_id,
            file_path=file_path,
            file_size=file_size,
            file_hash=file_hash,
            file_id=file_id,
            thread_id=thread_id,
            chunk_size=chunk_size
        )
    
    def _send_file_direct(
        self,
        target_ip: str,
        target_port: int,
        file_path: str,
        file_size: int,
        file_hash: str,
        file_id: str,
        thread_id: Optional[str],
        chunk_size: int
    ) -> Dict[str, Any]:
        """
        Send file via HTTP direct push.
        
        Args:
            target_ip: Target device IP
            target_port: Target device port
            file_path: Path to file
            file_size: File size
            file_hash: File hash
            file_id: File ID
            thread_id: Thread ID
            chunk_size: Chunk size
            
        Returns:
            Transfer information
        """
        url = f"http://{target_ip}:{target_port}/transfer"
        
        headers = {
            'X-File-Name': os.path.basename(file_path),
            'X-File-Size': str(file_size),
            'X-File-Hash': file_hash,
            'X-File-Id': file_id,
            'Content-Type': 'application/octet-stream'
        }
        
        if thread_id:
            headers['X-Thread-Id'] = thread_id
        
        # Send file
        with open(file_path, 'rb') as f:
            response = requests.post(
                url,
                data=f,
                headers=headers,
                timeout=self.timeout
            )
        
        if response.status_code == 200:
            return {
                'transferId': file_id,
                'method': 'direct',
                'status': 'completed',
                'fileSize': file_size,
                'fileHash': file_hash
            }
        
        raise requests.RequestException(
            f"Direct transfer failed: {response.status_code}"
        )
    
    def _send_file_relay(
        self,
        target_device_id: str,
        file_path: str,
        file_size: int,
        file_hash: str,
        file_id: str,
        thread_id: Optional[str],
        chunk_size: int
    ) -> Dict[str, Any]:
        """
        Send file via S3 relay.
        
        Args:
            target_device_id: Target device ID
            file_path: Path to file
            file_size: File size
            file_hash: File hash
            file_id: File ID
            thread_id: Thread ID
            chunk_size: Chunk size
            
        Returns:
            Transfer information
        """
        # Get presigned upload URL
        url = f"{self.server}/api/s3/presign-upload"
        payload = {
            'fileId': file_id,
            'fileName': os.path.basename(file_path),
            'fileSize': file_size,
            'fileHash': file_hash,
            'targetDeviceId': target_device_id
        }
        
        if thread_id:
            payload['threadId'] = thread_id
        
        response = requests.post(
            url,
            json=payload,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        
        if response.status_code != 200:
            raise requests.RequestException(
                f"Failed to get presigned URL: {response.status_code}"
            )
        
        data = response.json()
        upload_url = data.get('uploadUrl')
        
        if not upload_url:
            raise ValueError("No upload URL provided")
        
        # Upload file to S3
        with open(file_path, 'rb') as f:
            upload_response = requests.put(
                upload_url,
                data=f,
                headers={'Content-Type': 'application/octet-stream'},
                timeout=self.timeout
            )
        
        if upload_response.status_code not in (200, 201):
            raise requests.RequestException(
                f"File upload failed: {upload_response.status_code}"
            )
        
        # Notify server of completion
        notify_url = f"{self.server}/api/transfer/complete"
        notify_payload = {
            'fileId': file_id,
            'transferId': data.get('transferId')
        }
        
        notify_response = requests.post(
            notify_url,
            json=notify_payload,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        
        return {
            'transferId': data.get('transferId'),
            'method': 'relay',
            'status': 'completed',
            'fileSize': file_size,
            'fileHash': file_hash
        }
    
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
            content_type: MIME type
            thread_id: Thread ID
            
        Returns:
            Transfer information
        """
        if not self.auth.is_authenticated():
            raise ValueError("Not authenticated")
        
        # Find target device
        device_info = self.device.find_by_name(target_device)
        if not device_info:
            device_info = self.device.get_info(target_device)
        
        target_device_id = device_info.get('deviceId')
        
        # Create transfer request
        url = f"{self.server}/api/transfer/clipboard"
        payload = {
            'targetDeviceId': target_device_id,
            'content': content,
            'contentType': content_type
        }
        
        if thread_id:
            payload['threadId'] = thread_id
        
        response = requests.post(
            url,
            json=payload,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        
        if response.status_code == 200:
            return response.json()
        
        raise requests.RequestException(
            f"Failed to send clipboard: {response.status_code}"
        )
    
    def get_transfer_status(self, transfer_id: str) -> Dict[str, Any]:
        """
        Get transfer status.
        
        Args:
            transfer_id: Transfer ID
            
        Returns:
            Transfer status
        """
        if not self.auth.is_authenticated():
            raise ValueError("Not authenticated")
        
        url = f"{self.server}/api/transfer/status/{transfer_id}"
        
        response = requests.get(
            url,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        
        if response.status_code == 200:
            return response.json()
        
        raise requests.RequestException(
            f"Failed to get transfer status: {response.status_code}"
        )
    
    def cancel_transfer(self, transfer_id: str) -> bool:
        """
        Cancel transfer.
        
        Args:
            transfer_id: Transfer ID
            
        Returns:
            True if successful
        """
        if not self.auth.is_authenticated():
            raise ValueError("Not authenticated")
        
        url = f"{self.server}/api/transfer/cancel/{transfer_id}"
        
        response = requests.post(
            url,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        
        return response.status_code == 200