"""
Health Check Endpoint for Render Deployment

This script adds a health check endpoint to verify the server is running.
"""

from aiohttp import web
import json

async def health_check(request):
    """Health check endpoint for Render."""
    return web.json_response({
        "status": "healthy",
        "service": "mcp-server",
        "version": "1.0.0",
        "endpoints": [
            "/api/action/get_client_data",
            "/api/action/process_webhook_data",
            "/webhook/make.com_chatgpt_clients"
        ]
    })

# Add this to your server routes
# app.router.add_get('/health', health_check)
