"""
Main Entry Point for Modular MCP Server (Deployment Version)

This script starts the MCP server with all registered actions and
human-in-the-loop collaboration features, optimized for cloud deployment.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from mcp_server.core.server import MCPServer
from mcp_server.actions.client_data import get_client_data, update_client_session
from mcp_server.actions.webhook_integration import (
    process_webhook_data,
    extract_client_knowledge_graph,
    send_webhook_response,
    validate_webhook_signature
)
from health_check import health_check

# Configure logging for deployment
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main server startup function."""
    try:
        # Get port from environment (Render sets PORT env var)
        port = int(os.getenv('PORT', 8000))
        host = os.getenv('HOST', '0.0.0.0')  # Bind to all interfaces for cloud
        
        logger.info(f"Starting MCP Server on {host}:{port}")
        
        # Initialize server with deployment settings
        server = MCPServer(
            host=host,
            port=port,
            enable_cors=True,  # Enable CORS for web access
            cors_origins=["*"]  # Allow all origins for ChatGPT
        )
        
        # Add health check route
        server.app.router.add_get('/health', health_check)
        
        # Register all actions
        logger.info("Registering actions...")
        
        # Client data actions
        server.register_action("get_client_data", get_client_data)
        server.register_action("update_client_session", update_client_session)
        
        # Webhook integration actions
        server.register_action("process_webhook_data", process_webhook_data)
        server.register_action("extract_client_knowledge_graph", extract_client_knowledge_graph)
        server.register_action("send_webhook_response", send_webhook_response)
        server.register_action("validate_webhook_signature", validate_webhook_signature)
        
        # Register webhook routes
        server.register_webhook_route("make.com_chatgpt_clients", "process_webhook_data")
        server.register_webhook_route("zapier_generic", "process_webhook_data")
        
        logger.info("All actions and webhook integrations registered successfully")
        
        # Start the server
        logger.info(f"Server starting on {host}:{port}")
        await server.start()
        
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())
