"""
Simple Render-compatible server
"""

import os
import asyncio
from aiohttp import web
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def health_check(request):
    """Health check endpoint."""
    return web.json_response({
        "status": "healthy",
        "service": "mcp-server",
        "version": "1.0.0"
    })

async def get_client_data(request):
    """Get client data endpoint."""
    try:
        data = await request.json()
        client_id = data.get('client_id', 'unknown')
        
        return web.json_response({
            "client_id": client_id,
            "status": "success",
            "message": f"Client data retrieved for {client_id}",
            "timestamp": "2024-01-01T00:00:00Z"
        })
    except Exception as e:
        return web.json_response({
            "error": str(e)
        }, status=400)

async def process_webhook_data(request):
    """Process webhook data endpoint."""
    try:
        data = await request.json()
        
        return web.json_response({
            "status": "success",
            "message": "Webhook data processed",
            "webhook_data": data
        })
    except Exception as e:
        return web.json_response({
            "error": str(e)
        }, status=400)

async def init_app():
    """Initialize the application."""
    app = web.Application()
    
    # Add routes
    app.router.add_get('/health', health_check)
    app.router.add_post('/api/action/get_client_data', get_client_data)
    app.router.add_post('/api/action/process_webhook_data', process_webhook_data)
    app.router.add_post('/webhook/make.com_chatgpt_clients', process_webhook_data)
    
    return app

async def main():
    """Main function."""
    # Get port from environment
    port = int(os.getenv('PORT', 8000))
    host = '0.0.0.0'
    
    logger.info(f"Starting server on {host}:{port}")
    
    app = await init_app()
    
    # Start the server
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, host, port)
    await site.start()
    
    logger.info(f"Server started successfully on {host}:{port}")
    logger.info(f"Health check: http://{host}:{port}/health")
    
    # Keep server running
    try:
        await asyncio.Future()  # Run forever
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        await runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
