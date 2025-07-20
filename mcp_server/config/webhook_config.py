"""
Webhook Configuration for MCP Server

This module contains configuration settings for webhook integrations
with external services like Make.com, Zapier, etc.
"""

import os
from typing import Dict, Any, Optional


class WebhookConfig:
    """
    Configuration manager for webhook integrations.
    
    Features:
    - Environment-based configuration
    - Secret management
    - Webhook endpoint configuration
    - Validation settings
    """
    
    def __init__(self):
        """Initialize webhook configuration."""
        self.webhook_secrets: Dict[str, str] = {}
        self.webhook_endpoints: Dict[str, str] = {}
        self.validation_enabled: bool = True
        self.timeout_seconds: int = 30
        
        # Load configuration from environment
        self._load_environment_config()
    
    def _load_environment_config(self):
        """Load configuration from environment variables."""
        # Make.com configuration
        make_com_secret = os.getenv('MAKE_COM_WEBHOOK_SECRET')
        if make_com_secret:
            self.webhook_secrets['make.com'] = make_com_secret
        
        # Zapier configuration
        zapier_secret = os.getenv('ZAPIER_WEBHOOK_SECRET')
        if zapier_secret:
            self.webhook_secrets['zapier'] = zapier_secret
        
        # Webhook endpoints
        make_com_endpoint = os.getenv('MAKE_COM_WEBHOOK_ENDPOINT')
        if make_com_endpoint:
            self.webhook_endpoints['make.com'] = make_com_endpoint
        
        zapier_endpoint = os.getenv('ZAPIER_WEBHOOK_ENDPOINT')
        if zapier_endpoint:
            self.webhook_endpoints['zapier'] = zapier_endpoint
        
        # Validation settings
        validation_enabled = os.getenv('WEBHOOK_VALIDATION_ENABLED', 'true').lower()
        self.validation_enabled = validation_enabled == 'true'
        
        # Timeout settings
        timeout = os.getenv('WEBHOOK_TIMEOUT_SECONDS', '30')
        try:
            self.timeout_seconds = int(timeout)
        except ValueError:
            self.timeout_seconds = 30
    
    def get_webhook_secret(self, webhook_type: str) -> Optional[str]:
        """
        Get secret for webhook type.
        
        Args:
            webhook_type: Type of webhook
            
        Returns:
            Secret key or None if not found
        """
        return self.webhook_secrets.get(webhook_type)
    
    def get_webhook_endpoint(self, webhook_type: str) -> Optional[str]:
        """
        Get endpoint URL for webhook type.
        
        Args:
            webhook_type: Type of webhook
            
        Returns:
            Endpoint URL or None if not found
        """
        return self.webhook_endpoints.get(webhook_type)
    
    def is_validation_enabled(self) -> bool:
        """Check if webhook validation is enabled."""
        return self.validation_enabled
    
    def get_timeout(self) -> int:
        """Get webhook timeout in seconds."""
        return self.timeout_seconds
    
    def add_webhook_secret(self, webhook_type: str, secret: str):
        """
        Add a webhook secret.
        
        Args:
            webhook_type: Type of webhook
            secret: Secret key
        """
        self.webhook_secrets[webhook_type] = secret
    
    def add_webhook_endpoint(self, webhook_type: str, endpoint: str):
        """
        Add a webhook endpoint.
        
        Args:
            webhook_type: Type of webhook
            endpoint: Endpoint URL
        """
        self.webhook_endpoints[webhook_type] = endpoint
    
    def get_config_summary(self) -> Dict[str, Any]:
        """
        Get configuration summary for debugging.
        
        Returns:
            Dictionary with configuration summary
        """
        return {
            'webhook_types_configured': list(self.webhook_secrets.keys()),
            'endpoints_configured': list(self.webhook_endpoints.keys()),
            'validation_enabled': self.validation_enabled,
            'timeout_seconds': self.timeout_seconds,
            'environment_loaded': True
        }


# Global configuration instance
webhook_config = WebhookConfig()
