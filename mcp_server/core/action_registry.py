"""
Action Registry for Modular MCP Server

This module provides a plugin-ready action management system that allows:
- Dynamic action registration and execution
- Action metadata and documentation
- Error handling and validation
- Performance monitoring and logging
"""

import asyncio
import logging
from typing import Dict, Any, Callable, Optional, List
from functools import wraps
import time
import uuid


def action_handler(description: str = "", requires_approval: bool = False):
    """
    Decorator for registering action handlers with metadata.
    
    Args:
        description: Human-readable description of the action
        requires_approval: Whether this action requires human approval
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate unique execution ID for tracking
            execution_id = str(uuid.uuid4())
            
            # Log execution start
            logging.getLogger('action_registry').info(
                f"Executing action {func.__name__} with ID: {execution_id}"
            )
            
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                logging.getLogger('action_registry').info(
                    f"Action {func.__name__} completed in {execution_time:.2f}s"
                )
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                logging.getLogger('action_registry').error(
                    f"Action {func.__name__} failed after {execution_time:.2f}s: {str(e)}"
                )
                raise
        
        # Store metadata on the function
        wrapper.action_metadata = {
            'description': description,
            'requires_approval': requires_approval,
            'name': func.__name__
        }
        
        return wrapper
    return decorator


class ActionRegistry:
    """
    Registry for managing and executing MCP server actions.
    
    Features:
    - Dynamic action registration
    - Metadata tracking
    - Performance monitoring
    - Error handling and logging
    - Plugin-ready architecture
    """
    
    def __init__(self):
        """Initialize the action registry."""
        self.actions: Dict[str, Callable] = {}
        self.metadata: Dict[str, Dict[str, Any]] = {}
        self.logger = logging.getLogger('action_registry')
        
        # Performance tracking
        self.execution_stats: Dict[str, Dict[str, Any]] = {}
        
        self.logger.info("Action registry initialized")
    
    def register_action(self, name: str, handler: Callable, metadata: Optional[Dict[str, Any]] = None):
        """
        Register a new action with the registry.
        
        Args:
            name: Unique action name
            handler: Async function to handle the action
            metadata: Optional metadata about the action
        """
        if name in self.actions:
            self.logger.warning(f"Overwriting existing action: {name}")
        
        self.actions[name] = handler
        
        # Store metadata
        action_metadata = {
            'description': getattr(handler, 'action_metadata', {}).get('description', ''),
            'requires_approval': getattr(handler, 'action_metadata', {}).get('requires_approval', False),
            'registered_at': time.time(),
            'execution_count': 0,
            'total_execution_time': 0.0,
            'last_execution': None
        }
        
        if metadata:
            action_metadata.update(metadata)
        
        self.metadata[name] = action_metadata
        
        self.logger.info(f"Registered action: {name} - {action_metadata['description']}")
    
    async def execute_action(self, name: str, params: Dict[str, Any]) -> Any:
        """
        Execute an action with the given parameters.
        
        Args:
            name: Action name to execute
            params: Parameters to pass to the action
            
        Returns:
            Action execution result
            
        Raises:
            KeyError: If action is not registered
            Exception: If action execution fails
        """
        if name not in self.actions:
            raise KeyError(f"Action '{name}' is not registered")
        
        handler = self.actions[name]
        execution_id = str(uuid.uuid4())
        
        self.logger.info(f"Executing action '{name}' with ID: {execution_id}")
        
        # Update metadata
        self.metadata[name]['execution_count'] += 1
        self.metadata[name]['last_execution'] = time.time()
        
        start_time = time.time()
        
        try:
            # Execute the action
            result = await handler(params)
            
            execution_time = time.time() - start_time
            self.metadata[name]['total_execution_time'] += execution_time
            
            self.logger.info(f"Action '{name}' completed successfully in {execution_time:.2f}s")
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error(f"Action '{name}' failed after {execution_time:.2f}s: {str(e)}")
            raise
    
    def list_actions(self) -> List[Dict[str, Any]]:
        """
        Get list of all registered actions with metadata.
        
        Returns:
            List of action information dictionaries
        """
        actions = []
        
        for name, metadata in self.metadata.items():
            action_info = {
                'name': name,
                'description': metadata['description'],
                'requires_approval': metadata['requires_approval'],
                'execution_count': metadata['execution_count'],
                'total_execution_time': metadata['total_execution_time'],
                'average_execution_time': (
                    metadata['total_execution_time'] / metadata['execution_count']
                    if metadata['execution_count'] > 0 else 0
                ),
                'last_execution': metadata['last_execution']
            }
            actions.append(action_info)
        
        return actions
    
    def get_action_metadata(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a specific action.
        
        Args:
            name: Action name
            
        Returns:
            Action metadata or None if not found
        """
        return self.metadata.get(name)
    
    def unregister_action(self, name: str) -> bool:
        """
        Unregister an action from the registry.
        
        Args:
            name: Action name to unregister
            
        Returns:
            True if action was unregistered, False if not found
        """
        if name in self.actions:
            del self.actions[name]
            del self.metadata[name]
            self.logger.info(f"Unregistered action: {name}")
            return True
        
        return False
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """
        Get overall execution statistics.
        
        Returns:
            Dictionary with execution statistics
        """
        total_actions = len(self.actions)
        total_executions = sum(meta['execution_count'] for meta in self.metadata.values())
        total_time = sum(meta['total_execution_time'] for meta in self.metadata.values())
        
        return {
            'total_actions': total_actions,
            'total_executions': total_executions,
            'total_execution_time': total_time,
            'average_execution_time': total_time / total_executions if total_executions > 0 else 0
        }
