"""
Simple Webhook Receiver for Testing

This creates a simple webhook endpoint that you can use
to test your Make.com scenario and see the real data.
"""

import asyncio
import aiohttp
import json
from datetime import datetime
from aiohttp import web
from aiohttp.web import Request, Response

class SimpleWebhookReceiver:
    """Simple webhook receiver for testing Make.com scenarios."""
    
    def __init__(self, port=8006):
        self.port = port
        self.app = web.Application()
        self.app.router.add_post('/webhook', self.handle_webhook)
        self.app.router.add_get('/', self.root)
        self.received_data = []
        
    async def handle_webhook(self, request: Request) -> Response:
        """Handle incoming webhook data."""
        try:
            # Get the raw data
            data = await request.json()
            
            print("\n" + "="*60)
            print("🔔 WEBHOOK DATA RECEIVED!")
            print("="*60)
            print(f"📅 Timestamp: {datetime.now().isoformat()}")
            print(f"📊 Data Structure:")
            print(json.dumps(data, indent=2))
            print("="*60)
            
            # Store the data
            self.received_data.append({
                'timestamp': datetime.now().isoformat(),
                'data': data
            })
            
            # Return success
            return web.json_response({
                'status': 'success',
                'message': 'Data received and logged',
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return web.json_response({
                'status': 'error',
                'error': str(e)
            }, status=500)
    
    async def root(self, request: Request) -> Response:
        """Root endpoint with instructions."""
        instructions = f"""
        <html>
        <head><title>Webhook Test Receiver</title></head>
        <body>
        <h1>Webhook Test Receiver</h1>
        <p>Webhook URL: <code>http://localhost:{self.port}/webhook</code></p>
        <p>Method: POST</p>
        <p>Content-Type: application/json</p>
        <br>
        <h2>Instructions:</h2>
        <ol>
        <li>Update your Make.com Webhook Respond URL to: <code>http://localhost:{self.port}/webhook</code></li>
        <li>Test your Make.com scenario with client_id: 86drqmpje</li>
        <li>Check the console output for the received data</li>
        </ol>
        <br>
        <h2>Received Data Count: {len(self.received_data)}</h2>
        </body>
        </html>
        """
        return web.Response(text=instructions, content_type='text/html')
    
    async def start(self):
        """Start the webhook receiver."""
        runner = web.AppRunner(self.app)
        await runner.setup()
        
        site = web.TCPSite(runner, 'localhost', self.port)
        await site.start()
        
        print(f"🚀 Webhook receiver started!")
        print(f"📡 URL: http://localhost:{self.port}/webhook")
        print(f"🌐 Instructions: http://localhost:{self.port}/")
        print()
        print("📋 Next Steps:")
        print("1. Update your Make.com Webhook Respond URL to:")
        print(f"   http://localhost:{self.port}/webhook")
        print("2. Test your Make.com scenario")
        print("3. Watch this console for the received data")
        print()
        print("⏳ Waiting for webhook data...")
        print("   Press Ctrl+C to stop")
        
        try:
            await asyncio.Future()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            await runner.cleanup()

if __name__ == "__main__":
    asyncio.run(SimpleWebhookReceiver().start())
