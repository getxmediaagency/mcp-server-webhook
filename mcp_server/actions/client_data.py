"""
Client Data Actions

This module contains actions related to client data management:
- get_client_data: Retrieve client information and metadata
- Additional client-related actions can be added here
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

from ..core.action_registry import action_handler


@action_handler(
    description="Retrieve client data and metadata for the current session",
    requires_approval=False
)
async def get_client_data(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get client data and metadata for the current session.
    
    This action retrieves comprehensive client information including:
    - Client session details
    - System information
    - Request metadata
    - Performance metrics
    
    Args:
        params: Dictionary containing request parameters
            - client_id: Optional client identifier
            - include_metrics: Whether to include performance metrics
            - include_system_info: Whether to include system information
            
    Returns:
        Dictionary containing client data and metadata
        
    Raises:
        ValueError: If invalid parameters are provided
    """
    logger = logging.getLogger('get_client_data')
    
    # Extract parameters with defaults
    client_id = params.get('client_id', str(uuid.uuid4()))
    include_metrics = params.get('include_metrics', True)
    include_system_info = params.get('include_system_info', True)
    
    logger.info(f"Retrieving client data for client_id: {client_id}")
    
    # Validate parameters
    if not isinstance(client_id, str):
        raise ValueError("client_id must be a string")
    
    if not isinstance(include_metrics, bool):
        raise ValueError("include_metrics must be a boolean")
    
    if not isinstance(include_system_info, bool):
        raise ValueError("include_system_info must be a boolean")
    
    # Build response data
    client_data = {
        'client_id': client_id,
        'timestamp': datetime.utcnow().isoformat(),
        'session_id': str(uuid.uuid4()),
        'status': 'active',
        'request_id': params.get('request_id', str(uuid.uuid4()))
    }
    
    # Add system information if requested
    if include_system_info:
        client_data['system_info'] = {
            'platform': 'darwin',  # macOS
            'python_version': '3.x',
            'server_time': datetime.utcnow().isoformat(),
            'timezone': 'UTC'
        }
    
    # Add performance metrics if requested
    if include_metrics:
        client_data['metrics'] = {
            'request_count': 1,  # This would be tracked in a real implementation
            'average_response_time': 0.0,  # This would be calculated from history
            'last_request_time': datetime.utcnow().isoformat(),
            'session_duration': 0  # This would be calculated from session start
        }
    
    # Add client capabilities
    client_data['capabilities'] = {
        'supports_async': True,
        'supports_human_loop': True,
        'supports_metrics': include_metrics,
        'supports_system_info': include_system_info
    }
    
    # Add request metadata
    client_data['request_metadata'] = {
        'user_agent': params.get('user_agent', 'MCP-Client/1.0'),
        'request_source': params.get('request_source', 'api'),
        'request_method': 'POST',
        'content_type': 'application/json'
    }
    
    logger.info(f"Successfully retrieved client data for {client_id}")
    
    return client_data


@action_handler(
    description="Update client session information",
    requires_approval=True  # This action requires human approval
)
async def update_client_session(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update client session information.
    
    This action allows updating client session data and requires
    human approval for security reasons.
    
    Args:
        params: Dictionary containing update parameters
            - client_id: Client identifier to update
            - session_data: New session data to set
            - update_reason: Reason for the update
            
    Returns:
        Dictionary containing update confirmation
        
    Raises:
        ValueError: If invalid parameters are provided
    """
    logger = logging.getLogger('update_client_session')
    
    # Extract and validate parameters
    client_id = params.get('client_id')
    session_data = params.get('session_data', {})
    update_reason = params.get('update_reason', 'No reason provided')
    
    if not client_id:
        raise ValueError("client_id is required")
    
    if not isinstance(session_data, dict):
        raise ValueError("session_data must be a dictionary")
    
    logger.info(f"Updating client session for {client_id}: {update_reason}")
    
    # In a real implementation, this would update the actual session data
    # For now, we return a confirmation
    return {
        'client_id': client_id,
        'status': 'updated',
        'update_reason': update_reason,
        'session_data': session_data,
        'timestamp': datetime.utcnow().isoformat(),
        'updated_by': 'human_approval'
    }
