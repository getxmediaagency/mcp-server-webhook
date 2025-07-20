"""
Minimal server for Render
"""

import os
from aiohttp import web
import asyncio

async def health_check(request):
    return web.json_response({"status": "healthy"})

async def get_client_data(request):
    data = await request.json()
    return web.json_response({
        "client_id": data.get("client_id", "unknown"),
        "status": "success"
    })

async def main():
    app = web.Application()
    
    # Add routes
    app.router.add_get('/health', health_check)
    app.router.add_post('/api/action/get_client_data', get_client_data)
    
    # Get port from environment
    port = int(os.getenv('PORT', 8000))
    
    print(f"Starting server on port {port}")
    
    # Start server
    web.run_app(app, host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()
