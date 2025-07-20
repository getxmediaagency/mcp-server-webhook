# Read the server.py file
with open('mcp_server/core/server.py', 'r') as f:
    content = f.read()

# Add webhook routes after the status endpoint
content = content.replace(
    "        # Status endpoint for debugging\n        self.app.router.add_get('/api/status', self._status)",
    """        # Status endpoint for debugging
        self.app.router.add_get('/api/status', self._status)
        
        # Webhook endpoints
        self.app.router.add_post('/api/webhook/make.com/chatgpt-clients', self._handle_make_com_webhook)
        self.app.router.add_post('/api/webhook/{webhook_type}', self._handle_generic_webhook)"""
)

# Write back to file
with open('mcp_server/core/server.py', 'w') as f:
    f.write(content)

print("Added webhook routes to server")
