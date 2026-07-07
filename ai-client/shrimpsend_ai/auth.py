"""
ShrimpSend AI Client - Authentication Manager
"""

import json
import time
from typing import Optional, Dict, Any
from pathlib import Path

import requests


class AuthManager:
    """
    Handles authentication with ShrimpSend server.
    """
    
    def __init__(
        self,
        server: str,
        config_dir: Path,
        timeout: int = 30
    ):
        """
        Initialize authentication manager.
        
        Args:
            server: ShrimpSend server URL
            config_dir: Configuration directory
            timeout: Request timeout
        """
        self.server = server
        self.config_dir = config_dir
        self.timeout = timeout
        
        # Token storage
        self._token: Optional[str] = None
        self._token_expiry: Optional[float] = None
        
        # Load token from config if available
        self._load_token()
    
    def _load_token(self) -> None:
        """Load token from config file."""
        token_file = self.config_dir / "auth.json"
        if token_file.exists():
            try:
                with open(token_file, 'r') as f:
                    data = json.load(f)
                    self._token = data.get('token')
                    self._token_expiry = data.get('expiry')
                    
                    # Check if token is expired
                    if self._token_expiry and time.time() > self._token_expiry:
                        self._token = None
                        self._token_expiry = None
            except (json.JSONDecodeError, KeyError):
                pass
    
    def _save_token(self) -> None:
        """Save token to config file."""
        token_file = self.config_dir / "auth.json"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        data = {
            'token': self._token,
            'expiry': self._token_expiry
        }
        with open(token_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def set_token(self, token: str, expiry: Optional[float] = None) -> None:
        """
        Set authentication token.
        
        Args:
            token: JWT token
            expiry: Token expiry timestamp
        """
        self._token = token
        self._token_expiry = expiry
        self._save_token()
    
    def get_token(self) -> Optional[str]:
        """
        Get current authentication token.
        
        Returns:
            JWT token or None
        """
        return self._token
    
    def is_authenticated(self) -> bool:
        """
        Check if user is authenticated.
        
        Returns:
            True if authenticated
        """
        if not self._token:
            return False
        
        # Check if token is expired
        if self._token_expiry and time.time() > self._token_expiry:
            self._token = None
            self._token_expiry = None
            self._save_token()
            return False
        
        return True
    
    def login(self, email: str, password: str) -> bool:
        """
        Login to ShrimpSend.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            True if login successful
            
        Raises:
            requests.RequestException: If request fails
        """
        url = f"{self.server}/api/auth/login"
        payload = {
            'email': email,
            'password': password
        }
        
        response = requests.post(
            url,
            json=payload,
            timeout=self.timeout
        )
        
        if response.status_code == 200:
            data = response.json()
            self._token = data.get('token')
            
            # Parse token expiry (if provided)
            expires_in = data.get('expiresIn')
            if expires_in:
                self._token_expiry = time.time() + expires_in
            else:
                # Default to 24 hours
                self._token_expiry = time.time() + 86400
            
            self._save_token()
            return True
        
        return False
    
    def register(
        self,
        email: str,
        password: str,
        name: Optional[str] = None
    ) -> bool:
        """
        Register new user.
        
        Args:
            email: User email
            password: User password
            name: User name
            
        Returns:
            True if registration successful
            
        Raises:
            requests.RequestException: If request fails
        """
        url = f"{self.server}/api/auth/register"
        payload = {
            'email': email,
            'password': password
        }
        
        if name:
            payload['name'] = name
        
        response = requests.post(
            url,
            json=payload,
            timeout=self.timeout
        )
        
        if response.status_code == 200:
            data = response.json()
            self._token = data.get('token')
            
            # Parse token expiry
            expires_in = data.get('expiresIn')
            if expires_in:
                self._token_expiry = time.time() + expires_in
            else:
                self._token_expiry = time.time() + 86400
            
            self._save_token()
            return True
        
        return False
    
    def refresh_token(self) -> bool:
        """
        Refresh authentication token.
        
        Returns:
            True if refresh successful
        """
        if not self._token:
            return False
        
        url = f"{self.server}/api/auth/refresh"
        headers = self.get_auth_headers()
        
        response = requests.post(
            url,
            headers=headers,
            timeout=self.timeout
        )
        
        if response.status_code == 200:
            data = response.json()
            self._token = data.get('token')
            
            expires_in = data.get('expiresIn')
            if expires_in:
                self._token_expiry = time.time() + expires_in
            
            self._save_token()
            return True
        
        return False
    
    def logout(self) -> None:
        """Logout and clear token."""
        self._token = None
        self._token_expiry = None
        self._save_token()
    
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers.
        
        Returns:
            Headers dictionary
        """
        headers = {
            'Content-Type': 'application/json'
        }
        
        if self._token:
            headers['Authorization'] = f'Bearer {self._token}'
        
        return headers
    
    def validate_token(self) -> bool:
        """
        Validate current token with server.
        
        Returns:
            True if token is valid
        """
        if not self._token:
            return False
        
        url = f"{self.server}/api/auth/validate"
        headers = self.get_auth_headers()
        
        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=self.timeout
            )
            return response.status_code == 200
        except requests.RequestException:
            return False