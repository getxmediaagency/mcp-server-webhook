"""
Main Entry Point for Modular MCP Server

This script starts the MCP server with all registered actions and
human-in-the-loop collaboration features.
"""

import asyncio
import logging
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


async def main():
    """
    Main function to start the MCP server.
    
    This function:
    1. Creates and configures the MCP server
    2. Registers all available actions
    3. Configures webhook integrations
    4. Starts the server and keeps it running
    """
    # Configure basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger('main')
    logger.info("Starting Modular MCP Server with Webhook Integration")
    
    try:
        # Create MCP server instance
        server = MCPServer(
            host="localhost",
            port=8000,
            debug=True  # Enable debug mode for development
        )
        
        # Register actions
        logger.info("Registering actions...")
        
        # Register client data actions
        server.register_action(
            name="get_client_data",
            handler=get_client_data,
            requires_approval=False
        )
        
        server.register_action(
            name="update_client_session",
            handler=update_client_session,
            requires_approval=True
        )
        
        # Register webhook integration actions
        server.register_action(
            name="process_webhook_data",
            handler=process_webhook_data,
            requires_approval=False
        )
        
        server.register_action(
            name="extract_client_knowledge_graph",
            handler=extract_client_knowledge_graph,
            requires_approval=False
        )
        
        server.register_action(
            name="send_webhook_response",
            handler=send_webhook_response,
            requires_approval=True  # Requires approval for external API calls
        )
        
        server.register_action(
            name="validate_webhook_signature",
            handler=validate_webhook_signature,
            requires_approval=False
        )
        
        # Configure webhook integrations
        logger.info("Configuring webhook integrations...")
        
        # Register webhook secrets (in production, these would come from environment variables)
        server.register_webhook_secret("make.com", "your_make_com_secret_here")
        server.register_webhook_secret("zapier", "your_zapier_secret_here")
        
        # Register webhook routes
        server.register_webhook_route("make.com_chatgpt_clients", "process_webhook_data")
        server.register_webhook_route("zapier_generic", "process_webhook_data")
        
        logger.info("All actions and webhook integrations registered successfully")
        
        # Start the server
        logger.info("Starting server...")
        await server.start()
        
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())
