"""
Webhook Handler for MCP Server

This module provides specialized webhook handling for external integrations
like Make.com, with proper validation and processing.
"""

import asyncio
import logging
from typing import Dict, Any, Optional
import json
import uuid
from datetime import datetime
from aiohttp import web
from aiohttp.web import Request, Response

from .action_registry import ActionRegistry


class WebhookHandler:
    """
    Specialized handler for webhook integrations with external services.
    
    Features:
    - Webhook signature validation
    - Automatic action routing based on webhook type
    - Integration with human-in-the-loop workflow
    - Comprehensive logging and debugging
    """
    
    def __init__(self, action_registry: ActionRegistry):
        """
        Initialize the webhook handler.
        
        Args:
            action_registry: Action registry for executing webhook actions
        """
        self.action_registry = action_registry
        self.logger = logging.getLogger('webhook_handler')
        
        # Webhook configuration
        self.webhook_secrets: Dict[str, str] = {}
        self.webhook_routes: Dict[str, str] = {}
        
        self.logger.info("Webhook handler initialized")
    
    def register_webhook_secret(self, webhook_type: str, secret: str):
        """
        Register a secret for webhook signature validation.
        
        Args:
            webhook_type: Type of webhook (e.g., 'make.com', 'zapier')
            secret: Secret key for signature validation
        """
        self.webhook_secrets[webhook_type] = secret
        self.logger.info(f"Registered secret for webhook type: {webhook_type}")
    
    def register_webhook_route(self, webhook_type: str, action_name: str):
        """
        Register a route for webhook type to action mapping.
        
        Args:
            webhook_type: Type of webhook
            action_name: Action to execute for this webhook type
        """
        self.webhook_routes[webhook_type] = action_name
        self.logger.info(f"Registered route: {webhook_type} -> {action_name}")
    
    async def handle_make_com_webhook(self, request: Request) -> Response:
        """
        Handle webhooks from Make.com integrations.
        
        This handler specifically processes webhooks from the Make.com
        "GPT - Get Client Knowledge Graph" scenario.
        
        Args:
            request: aiohttp Request object containing webhook data
            
        Returns:
            Response with processing result
        """
        webhook_id = str(uuid.uuid4())
        
        self.logger.info(f"Processing Make.com webhook: {webhook_id}")
        
        try:
            # Parse webhook data
            webhook_data = await request.json()
            
            # Extract client_id from webhook payload
            client_id = webhook_data.get('client_id')
            if not client_id:
                # Try to extract from nested structure
                if 'task' in webhook_data and 'custom_fields' in webhook_data['task']:
                    # Look for client_id in custom fields
                    custom_fields = webhook_data['task']['custom_fields']
                    for field in custom_fields:
                        if field.get('name', '').lower() == 'client_id':
                            client_id = field.get('value')
                            break
            
            # If still no client_id, generate one
            if not client_id:
                client_id = f"webhook_client_{webhook_id[:8]}"
            
            # Prepare action parameters
            action_params = {
                'webhook_data': webhook_data,
                'client_id': client_id,
                'webhook_id': webhook_id,
                'webhook_type': 'make.com_chatgpt_clients',
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Execute webhook processing action
            result = await self.action_registry.execute_action(
                'process_webhook_data',
                action_params
            )
            
            # Extract knowledge graph if task data is present
            if 'task' in webhook_data:
                knowledge_graph_result = await self.action_registry.execute_action(
                    'extract_client_knowledge_graph',
                    {
                        'webhook_data': webhook_data,
                        'client_id': client_id,
                        'include_task_details': True
                    }
                )
                result['knowledge_graph'] = knowledge_graph_result
            
            self.logger.info(f"Successfully processed Make.com webhook: {webhook_id}")
            
            return web.json_response({
                'webhook_id': webhook_id,
                'status': 'processed',
                'client_id': client_id,
                'result': result,
                'timestamp': datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            self.logger.error(f"Error processing Make.com webhook {webhook_id}: {str(e)}")
            
            return web.json_response({
                'webhook_id': webhook_id,
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }, status=500)
    
    async def handle_generic_webhook(self, request: Request, webhook_type: str) -> Response:
        """
        Handle generic webhooks with automatic routing.
        
        Args:
            request: aiohttp Request object
            webhook_type: Type of webhook for routing
            
        Returns:
            Response with processing result
        """
        webhook_id = str(uuid.uuid4())
        
        self.logger.info(f"Processing generic webhook {webhook_type}: {webhook_id}")
        
        try:
            # Parse webhook data
            webhook_data = await request.json()
            
            # Determine action to execute
            action_name = self.webhook_routes.get(webhook_type, 'process_webhook_data')
            
            # Prepare action parameters
            action_params = {
                'webhook_data': webhook_data,
                'webhook_id': webhook_id,
                'webhook_type': webhook_type,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Execute action
            result = await self.action_registry.execute_action(action_name, action_params)
            
            self.logger.info(f"Successfully processed webhook {webhook_type}: {webhook_id}")
            
            return web.json_response({
                'webhook_id': webhook_id,
                'status': 'processed',
                'webhook_type': webhook_type,
                'result': result,
                'timestamp': datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            self.logger.error(f"Error processing webhook {webhook_type} {webhook_id}: {str(e)}")
            
            return web.json_response({
                'webhook_id': webhook_id,
                'status': 'error',
                'error': str(e),
                'webhook_type': webhook_type,
                'timestamp': datetime.utcnow().isoformat()
            }, status=500)
    
    def validate_webhook_signature(self, webhook_data: Dict[str, Any], 
                                 signature: str, webhook_type: str) -> bool:
        """
        Validate webhook signature for security.
        
        Args:
            webhook_data: Webhook payload
            signature: Signature to validate
            webhook_type: Type of webhook
            
        Returns:
            True if signature is valid, False otherwise
        """
        if webhook_type not in self.webhook_secrets:
            self.logger.warning(f"No secret registered for webhook type: {webhook_type}")
            return False
        
        secret = self.webhook_secrets[webhook_type]
        
        # In a real implementation, you would validate the signature
        # For now, we'll simulate validation
        import hashlib
        import hmac
        
        payload_string = json.dumps(webhook_data, sort_keys=True)
        expected_signature = hmac.new(
            secret.encode('utf-8'),
            payload_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
