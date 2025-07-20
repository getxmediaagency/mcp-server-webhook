"""
Main MCP Server Implementation

This module contains the core MCPServer class that handles:
- HTTP request/response processing with aiohttp
- Action routing and execution
- Human-in-the-loop workflow integration
- Comprehensive logging and debugging
"""

import asyncio
import logging
from typing import Dict, Any, Optional, Callable
from aiohttp import web, ClientSession
from aiohttp.web import Request, Response
import json
import uuid

from .action_registry import ActionRegistry
from .human_loop import HumanLoopManager
from .webhook_handler import WebhookHandler


class MCPServer:
    """
    Main MCP Server class with modular action execution and human-in-the-loop support.
    
    Features:
    - Async HTTP server using aiohttp
    - Plugin-ready action registry
    - Human approval workflow integration
    - Comprehensive logging and debugging
    - Unique ID tracking for all operations
    """
    
    def __init__(self, host: str = "localhost", port: int = 8000, debug: bool = False):
        """
        Initialize the MCP server with configuration.
        
        Args:
            host: Server host address
            port: Server port number
            debug: Enable debug logging and features
        """
        self.host = host
        self.port = port
        self.debug = debug
        self.server_id = str(uuid.uuid4())  # Unique server instance ID
        
        # Initialize core components
        self.action_registry = ActionRegistry()
        self.human_loop = HumanLoopManager()
        self.webhook_handler = WebhookHandler(self.action_registry)
        
        # Setup logging with unique server ID
        self._setup_logging()
        
        # Create aiohttp application
        self.app = web.Application()
        self._setup_routes()
        
        # Store active sessions and requests
        self.active_requests: Dict[str, Dict[str, Any]] = {}
        
        self.logger.info(f"MCP Server initialized with ID: {self.server_id}")
    
    def _setup_logging(self):
        """Configure comprehensive logging with unique server identification."""
        log_level = logging.DEBUG if self.debug else logging.INFO
        
        # Create custom formatter with server ID
        formatter = logging.Formatter(
            f'%(asctime)s - MCP-Server-{self.server_id[:8]} - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Setup console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Setup file handler for persistent logging
        file_handler = logging.FileHandler(f'mcp_server_{self.server_id[:8]}.log')
        file_handler.setFormatter(formatter)
        
        # Configure root logger
        self.logger = logging.getLogger(f'mcp_server_{self.server_id[:8]}')
        self.logger.setLevel(log_level)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        self.logger.info("Logging system initialized")
    
    def _setup_routes(self):
        """Configure HTTP routes for the MCP server."""
        
        # Main action execution endpoint
        self.app.router.add_post('/api/action/{action_name}', self._handle_action_request)
        
        # Health check endpoint
        self.app.router.add_get('/health', self._health_check)
        
        # Action discovery endpoint
        self.app.router.add_get('/api/actions', self._actions_list)
        
        # Human approval endpoint
        self.app.router.add_post('/api/approval/{request_id}', self._human_approval)
        
        # Status endpoint for debugging
        self.app.router.add_get('/api/status', self._status)
        
        # Webhook endpoints
        self.app.router.add_post('/api/webhook/make.com/chatgpt-clients', self._handle_make_com_webhook)
        self.app.router.add_post('/api/webhook/{webhook_type}', self._handle_generic_webhook)
        
        self.logger.info("HTTP routes configured")
    
    async def _handle_action_request(self, request: Request) -> Response:
        """
        Handle action execution requests with human-in-the-loop support.
        
        Args:
            request: aiohttp Request object
            
        Returns:
            Response with action result or approval request
        """
        request_id = str(uuid.uuid4())
        action_name = request.match_info['action_name']
        
        self.logger.info(f"Processing action request {request_id} for action: {action_name}")
        
        try:
            # Parse request body
            body = await request.json()
            params = body.get('params', {})
            
            # Store request context for debugging
            self.active_requests[request_id] = {
                'action': action_name,
                'params': params,
                'timestamp': asyncio.get_event_loop().time(),
                'status': 'processing'
            }
            
            # Check if action requires human approval
            if self.human_loop.requires_approval(action_name):
                approval_request = await self.human_loop.create_approval_request(
                    request_id=request_id,
                    action_name=action_name,
                    params=params
                )
                
                self.active_requests[request_id]['status'] = 'awaiting_approval'
                
                return web.json_response({
                    'request_id': request_id,
                    'status': 'awaiting_approval',
                    'approval_url': f'/api/approval/{request_id}',
                    'message': 'Action requires human approval'
                })
            
            # Execute action directly
            result = await self.action_registry.execute_action(action_name, params)
            
            self.active_requests[request_id]['status'] = 'completed'
            
            return web.json_response({
                'request_id': request_id,
                'status': 'completed',
                'result': result
            })
            
        except Exception as e:
            self.logger.error(f"Error processing request {request_id}: {str(e)}")
            self.active_requests[request_id]['status'] = 'error'
            
            return web.json_response({
                'request_id': request_id,
                'status': 'error',
                'error': str(e)
            }, status=500)
    
    async def _health_check(self, request: Request) -> Response:
        """Handle health check requests."""
        return web.json_response({
            'status': 'healthy',
            'server_id': self.server_id,
            'active_requests': len(self.active_requests)
        })
    
    async def _actions_list(self, request: Request) -> Response:
        """Return list of available actions."""
        actions = self.action_registry.list_actions()
        return web.json_response({
            'actions': actions,
            'total': len(actions)
        })
    
    async def _human_approval(self, request: Request) -> Response:
        """Handle human approval responses."""
        request_id = request.match_info['request_id']
        
        try:
            body = await request.json()
            approved = body.get('approved', False)
            comments = body.get('comments', '')
            
            result = await self.human_loop.process_approval(
                request_id=request_id,
                approved=approved,
                comments=comments
            )
            
            return web.json_response({
                'request_id': request_id,
                'status': 'approved' if approved else 'rejected',
                'result': result
            })
            
        except Exception as e:
            return web.json_response({
                'request_id': request_id,
                'status': 'error',
                'error': str(e)
            }, status=500)
    
    async def _status(self, request: Request) -> Response:
        """Return detailed server status for debugging."""
        return web.json_response({
            'server_id': self.server_id,
            'active_requests': self.active_requests,
            'registered_actions': len(self.action_registry.list_actions()),
            'pending_approvals': len(self.human_loop.pending_approvals)
        })
    
    async def start(self):
        """Start the MCP server."""
        self.logger.info(f"Starting MCP Server on {self.host}:{self.port}")
        
        runner = web.AppRunner(self.app)
        await runner.setup()
        
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        
        self.logger.info(f"MCP Server started successfully")
        
        # Keep server running
        try:
            await asyncio.Future()  # Run forever
        except KeyboardInterrupt:
            self.logger.info("Shutting down MCP Server")
            await runner.cleanup()
    
    def register_action(self, name: str, handler: Callable, requires_approval: bool = False):
        """
        Register a new action with the server.
        
        Args:
            name: Action name
            handler: Async function to handle the action
            requires_approval: Whether this action requires human approval
        """
        self.action_registry.register_action(name, handler)
        
        if requires_approval:
            self.human_loop.add_approval_requirement(name)
        
        self.logger.info(f"Registered action: {name} (approval required: {requires_approval})")

    async def _handle_make_com_webhook(self, request: Request) -> Response:
        """Handle Make.com webhook requests."""
        return await self.webhook_handler.handle_make_com_webhook(request)
    
    async def _handle_generic_webhook(self, request: Request) -> Response:
        """Handle generic webhook requests."""
        webhook_type = request.match_info['webhook_type']
        return await self.webhook_handler.handle_generic_webhook(request, webhook_type)
    
    def register_webhook_secret(self, webhook_type: str, secret: str):
        """Register a secret for webhook signature validation."""
        self.webhook_handler.register_webhook_secret(webhook_type, secret)
    
    def register_webhook_route(self, webhook_type: str, action_name: str):
        """Register a route for webhook type to action mapping."""
        self.webhook_handler.register_webhook_route(webhook_type, action_name)

    async def _handle_make_com_webhook(self, request: Request) -> Response:
        """Handle Make.com webhook requests."""
        return await self.webhook_handler.handle_make_com_webhook(request)
    
    async def _handle_generic_webhook(self, request: Request) -> Response:
        """Handle generic webhook requests."""
        webhook_type = request.match_info['webhook_type']
        return await self.webhook_handler.handle_generic_webhook(request, webhook_type)
    
    def register_webhook_secret(self, webhook_type: str, secret: str):
        """Register a secret for webhook signature validation."""
        self.webhook_handler.register_webhook_secret(webhook_type, secret)
    
    def register_webhook_route(self, webhook_type: str, action_name: str):
        """Register a route for webhook type to action mapping."""
        self.webhook_handler.register_webhook_route(webhook_type, action_name)
