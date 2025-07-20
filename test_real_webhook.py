"""
Real Webhook Test for Make.com Integration

This script creates a test webhook endpoint that will receive
real data from your Make.com scenario and display the structure.
"""

import asyncio
import aiohttp
import json
import logging
from datetime import datetime
from aiohttp import web
from aiohttp.web import Request, Response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('test_webhook')

class TestWebhookServer:
    """Test webhook server to receive real data from Make.com."""
    
    def __init__(self, port=8005):
        self.port = port
        self.app = web.Application()
        self.app.router.add_post('/test-webhook', self.handle_webhook)
        self.app.router.add_get('/health', self.health_check)
        self.received_data = []
        
    async def handle_webhook(self, request: Request) -> Response:
        """Handle incoming webhook data from Make.com."""
        try:
            # Parse the incoming data
            data = await request.json()
            
            # Log the received data
            logger.info("🔔 Received webhook data!")
            logger.info(f"📊 Data structure: {json.dumps(data, indent=2)}")
            
            # Store the data for analysis
            self.received_data.append({
                'timestamp': datetime.now().isoformat(),
                'data': data
            })
            
            # Return success response
            response_data = {
                'status': 'success',
                'message': 'Webhook data received and logged',
                'timestamp': datetime.now().isoformat(),
                'data_received': True
            }
            
            return web.json_response(response_data)
            
        except Exception as e:
            logger.error(f"❌ Error processing webhook: {str(e)}")
            return web.json_response({
                'status': 'error',
                'error': str(e)
            }, status=500)
    
    async def health_check(self, request: Request) -> Response:
        """Health check endpoint."""
        return web.json_response({
            'status': 'healthy',
            'webhook_endpoint': f'http://localhost:{self.port}/test-webhook',
            'received_data_count': len(self.received_data)
        })
    
    async def start(self):
        """Start the test webhook server."""
        runner = web.AppRunner(self.app)
        await runner.setup()
        
        site = web.TCPSite(runner, 'localhost', self.port)
        await site.start()
        
        logger.info(f"🚀 Test webhook server started on port {self.port}")
        logger.info(f"📡 Webhook URL: http://localhost:{self.port}/test-webhook")
        logger.info(f"🏥 Health check: http://localhost:{self.port}/health")
        
        # Keep server running
        try:
            await asyncio.Future()
        except KeyboardInterrupt:
            logger.info("🛑 Shutting down test webhook server...")
            await runner.cleanup()

async def main():
    """Main function to start the test webhook server."""
    print("🧪 Real Webhook Test Server")
    print("=" * 50)
    print()
    print("📋 Instructions:")
    print("1. This server will receive webhook data from your Make.com scenario")
    print("2. Update your Make.com Webhook Respond URL to:")
    print("   http://localhost:8005/test-webhook")
    print("3. Test with client_id: 86drqmpje")
    print("4. Check the server logs for the real data structure")
    print()
    
    # Create and start the test server
    server = TestWebhookServer(port=8005)
    
    print("🌐 Test Webhook Server Ready!")
    print(f"   URL: http://localhost:8005/test-webhook")
    print(f"   Method: POST")
    print(f"   Content-Type: application/json")
    print()
    print("📝 Make.com Webhook Respond Configuration:")
    print("   URL: http://localhost:8005/test-webhook")
    print("   Method: POST")
    print("   Body: Use your current custom_fields response")
    print()
    print("⏳ Waiting for webhook data...")
    print("   Press Ctrl+C to stop the server")
    
    await server.start()

if __name__ == "__main__":
    asyncio.run(main())
