"""
Webhook Integration Actions

This module handles webhook integrations with external services like Make.com.
It provides actions for processing webhook data and integrating with external APIs.

Based on the Make.com scenario: "GPT - Get Client Knowledge Graph"
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
import json
import uuid
from datetime import datetime
import aiohttp

from ..core.action_registry import action_handler


@action_handler(
    description="Process webhook data from Make.com ChatGPT-Clients integration",
    requires_approval=False
)
async def process_webhook_data(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process webhook data from the Make.com ChatGPT-Clients integration.
    
    This action handles the webhook payload from the Make.com scenario
    "GPT - Get Client Knowledge Graph" and extracts relevant client information.
    
    Args:
        params: Dictionary containing webhook data
            - webhook_data: Raw webhook payload from Make.com
            - client_id: Optional client identifier
            - action_id: Optional action identifier from webhook
            
    Returns:
        Dictionary containing processed webhook data and client information
        
    Raises:
        ValueError: If invalid webhook data is provided
        KeyError: If required fields are missing from webhook
    """
    logger = logging.getLogger('process_webhook_data')
    
    # Extract parameters
    webhook_data = params.get('webhook_data', {})
    client_id = params.get('client_id')
    action_id = params.get('action_id')
    
    logger.info(f"Processing webhook data for client_id: {client_id}")
    
    # Validate webhook data
    if not isinstance(webhook_data, dict):
        raise ValueError("webhook_data must be a dictionary")
    
    # Extract client_id from webhook if not provided
    if not client_id:
        client_id = webhook_data.get('client_id')
        if not client_id:
            raise KeyError("client_id not found in webhook data or parameters")
    
    # Extract action_id from webhook if not provided
    if not action_id:
        action_id = webhook_data.get('action_id')
    
    # Process webhook data based on Make.com scenario structure
    processed_data = {
        'webhook_id': str(uuid.uuid4()),
        'client_id': client_id,
        'action_id': action_id,
        'timestamp': datetime.utcnow().isoformat(),
        'source': 'make.com_chatgpt_clients',
        'webhook_data': webhook_data,
        'status': 'processed'
    }
    
    # Extract additional data from webhook payload
    if 'task' in webhook_data:
        processed_data['task_data'] = webhook_data['task']
    
    if 'custom_fields' in webhook_data:
        processed_data['custom_fields'] = webhook_data['custom_fields']
    
    # Add metadata about the webhook processing
    processed_data['metadata'] = {
        'webhook_version': '1.0',
        'integration_type': 'make.com_chatgpt_clients',
        'processing_time': datetime.utcnow().isoformat(),
        'webhook_size': len(json.dumps(webhook_data))
    }
    
    logger.info(f"Successfully processed webhook data for client: {client_id}")
    
    return processed_data


@action_handler(
    description="Extract client knowledge graph data from webhook",
    requires_approval=False
)
async def extract_client_knowledge_graph(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract and structure client knowledge graph data from webhook payload.
    
    This action specifically handles the "GPT - Get Client Knowledge Graph"
    Make.com scenario and extracts structured knowledge graph data.
    
    Args:
        params: Dictionary containing webhook parameters
            - webhook_data: Raw webhook payload
            - client_id: Client identifier
            - include_task_details: Whether to include full task details
            
    Returns:
        Dictionary containing structured knowledge graph data
        
    Raises:
        ValueError: If invalid parameters are provided
    """
    logger = logging.getLogger('extract_client_knowledge_graph')
    
    # Extract parameters
    webhook_data = params.get('webhook_data', {})
    client_id = params.get('client_id')
    include_task_details = params.get('include_task_details', True)
    
    logger.info(f"Extracting knowledge graph for client: {client_id}")
    
    # Validate parameters
    if not client_id:
        raise ValueError("client_id is required")
    
    if not isinstance(webhook_data, dict):
        raise ValueError("webhook_data must be a dictionary")
    
    # Initialize knowledge graph structure
    knowledge_graph = {
        'client_id': client_id,
        'extraction_id': str(uuid.uuid4()),
        'timestamp': datetime.utcnow().isoformat(),
        'knowledge_nodes': [],
        'relationships': [],
        'metadata': {}
    }
    
    # Extract task data if available
    task_data = webhook_data.get('task', {})
    if task_data:
        # Create knowledge nodes from task data
        knowledge_graph['knowledge_nodes'].append({
            'node_id': f"task_{task_data.get('id', 'unknown')}",
            'node_type': 'task',
            'properties': {
                'name': task_data.get('name', ''),
                'description': task_data.get('description', ''),
                'status': task_data.get('status', {}).get('status', ''),
                'priority': task_data.get('priority', {}).get('priority', ''),
                'due_date': task_data.get('due_date'),
                'created_date': task_data.get('date_created'),
                'updated_date': task_data.get('date_updated')
            }
        })
        
        # Extract assignees as knowledge nodes
        assignees = task_data.get('assignees', [])
        for assignee in assignees:
            knowledge_graph['knowledge_nodes'].append({
                'node_id': f"user_{assignee.get('id', 'unknown')}",
                'node_type': 'user',
                'properties': {
                    'username': assignee.get('username', ''),
                    'email': assignee.get('email', ''),
                    'initials': assignee.get('initials', ''),
                    'profile_picture': assignee.get('profilePicture', '')
                }
            })
            
            # Create relationship between task and assignee
            knowledge_graph['relationships'].append({
                'relationship_id': f"assigns_{task_data.get('id')}_{assignee.get('id')}",
                'source_node': f"task_{task_data.get('id')}",
                'target_node': f"user_{assignee.get('id')}",
                'relationship_type': 'assigned_to',
                'properties': {
                    'assigned_date': task_data.get('date_created')
                }
            })
        
        # Extract custom fields as knowledge nodes
        custom_fields = task_data.get('custom_fields', [])
        for field in custom_fields:
            if field.get('value'):
                knowledge_graph['knowledge_nodes'].append({
                    'node_id': f"field_{field.get('id', 'unknown')}",
                    'node_type': 'custom_field',
                    'properties': {
                        'name': field.get('name', ''),
                        'type': field.get('type', ''),
                        'value': field.get('value', ''),
                        'required': field.get('required', False)
                    }
                })
                
                # Create relationship between task and custom field
                knowledge_graph['relationships'].append({
                    'relationship_id': f"has_field_{task_data.get('id')}_{field.get('id')}",
                    'source_node': f"task_{task_data.get('id')}",
                    'target_node': f"field_{field.get('id')}",
                    'relationship_type': 'has_custom_field',
                    'properties': {}
                })
    
    # Add metadata about the extraction
    knowledge_graph['metadata'] = {
        'total_nodes': len(knowledge_graph['knowledge_nodes']),
        'total_relationships': len(knowledge_graph['relationships']),
        'extraction_method': 'make.com_webhook',
        'webhook_source': 'chatgpt_clients_integration'
    }
    
    logger.info(f"Successfully extracted knowledge graph with {len(knowledge_graph['knowledge_nodes'])} nodes")
    
    return knowledge_graph


@action_handler(
    description="Send webhook response back to Make.com",
    requires_approval=True  # Requires approval for external API calls
)
async def send_webhook_response(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send a response back to Make.com webhook endpoint.
    
    This action allows sending structured responses back to the Make.com
    scenario that triggered the webhook.
    
    Args:
        params: Dictionary containing response parameters
            - response_url: URL to send response to
            - response_data: Data to send in response
            - response_type: Type of response (success, error, etc.)
            - client_id: Client identifier for tracking
            
    Returns:
        Dictionary containing response status and details
        
    Raises:
        ValueError: If invalid parameters are provided
        aiohttp.ClientError: If HTTP request fails
    """
    logger = logging.getLogger('send_webhook_response')
    
    # Extract parameters
    response_url = params.get('response_url')
    response_data = params.get('response_data', {})
    response_type = params.get('response_type', 'success')
    client_id = params.get('client_id')
    
    logger.info(f"Sending webhook response for client: {client_id}")
    
    # Validate parameters
    if not response_url:
        raise ValueError("response_url is required")
    
    if not isinstance(response_data, dict):
        raise ValueError("response_data must be a dictionary")
    
    # Prepare response payload
    response_payload = {
        'status': response_type,
        'client_id': client_id,
        'timestamp': datetime.utcnow().isoformat(),
        'response_id': str(uuid.uuid4()),
        'data': response_data
    }
    
    try:
        # Send HTTP POST request to response URL
        async with aiohttp.ClientSession() as session:
            async with session.post(
                response_url,
                json=response_payload,
                headers={'Content-Type': 'application/json'}
            ) as response:
                response_status = response.status
                response_text = await response.text()
                
                logger.info(f"Webhook response sent successfully: {response_status}")
                
                return {
                    'response_id': response_payload['response_id'],
                    'status': 'sent',
                    'response_status': response_status,
                    'response_text': response_text,
                    'client_id': client_id,
                    'timestamp': datetime.utcnow().isoformat()
                }
                
    except aiohttp.ClientError as e:
        logger.error(f"Failed to send webhook response: {str(e)}")
        raise aiohttp.ClientError(f"Webhook response failed: {str(e)}")


@action_handler(
    description="Validate webhook signature and authenticity",
    requires_approval=False
)
async def validate_webhook_signature(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate webhook signature to ensure authenticity.
    
    This action validates webhook signatures to prevent unauthorized
    webhook calls and ensure data integrity.
    
    Args:
        params: Dictionary containing validation parameters
            - webhook_data: Raw webhook payload
            - signature: Webhook signature to validate
            - secret_key: Secret key for signature validation
            - client_id: Client identifier
            
    Returns:
        Dictionary containing validation result
        
    Raises:
        ValueError: If invalid parameters are provided
    """
    logger = logging.getLogger('validate_webhook_signature')
    
    # Extract parameters
    webhook_data = params.get('webhook_data', {})
    signature = params.get('signature')
    secret_key = params.get('secret_key')
    client_id = params.get('client_id')
    
    logger.info(f"Validating webhook signature for client: {client_id}")
    
    # Validate parameters
    if not signature:
        raise ValueError("signature is required")
    
    if not secret_key:
        raise ValueError("secret_key is required")
    
    # In a real implementation, you would validate the signature
    # For now, we'll simulate validation
    import hashlib
    import hmac
    
    # Create expected signature
    payload_string = json.dumps(webhook_data, sort_keys=True)
    expected_signature = hmac.new(
        secret_key.encode('utf-8'),
        payload_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Compare signatures
    is_valid = hmac.compare_digest(signature, expected_signature)
    
    validation_result = {
        'validation_id': str(uuid.uuid4()),
        'client_id': client_id,
        'is_valid': is_valid,
        'timestamp': datetime.utcnow().isoformat(),
        'signature_provided': signature,
        'signature_expected': expected_signature,
        'validation_method': 'hmac_sha256'
    }
    
    if is_valid:
        logger.info(f"Webhook signature validated successfully for client: {client_id}")
    else:
        logger.warning(f"Webhook signature validation failed for client: {client_id}")
    
    return validation_result
