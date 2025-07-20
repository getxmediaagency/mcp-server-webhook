# Webhook Integration Guide

This document describes how to integrate the MCP server with external webhook services, specifically Make.com.

## Overview

The MCP server now includes comprehensive webhook integration capabilities that allow it to:
- Receive webhooks from external services
- Process webhook data automatically
- Extract structured knowledge graphs
- Send responses back to webhook sources
- Validate webhook signatures for security

## Make.com Integration

### Webhook Endpoint

The server provides a dedicated endpoint for Make.com webhooks:

```
POST /api/webhook/make.com/chatgpt-clients
```

### Expected Payload

Based on the Make.com scenario "GPT - Get Client Knowledge Graph", the webhook expects:

```json
{
  "client_id": "client-123",
  "action_id": "get_client_data",
  "task": {
    "id": "task_123",
    "name": "Client Task Name",
    "description": "Task description",
    "status": {
      "status": "in progress",
      "color": "#ff6b6b"
    },
    "custom_fields": [
      {
        "id": "field_1",
        "name": "Client ID",
        "type": "text",
        "value": "client-123"
      }
    ],
    "assignees": [
      {
        "id": 1,
        "username": "user1",
        "email": "user1@example.com",
        "initials": "U1"
      }
    ]
  }
}
```

### Response Format

The server responds with:

```json
{
  "webhook_id": "uuid-123",
  "status": "processed",
  "client_id": "client-123",
  "result": {
    "webhook_id": "uuid-123",
    "client_id": "client-123",
    "action_id": "get_client_data",
    "timestamp": "2024-01-01T12:00:00Z",
    "source": "make.com_chatgpt_clients",
    "knowledge_graph": {
      "client_id": "client-123",
      "extraction_id": "uuid-456",
      "knowledge_nodes": [...],
      "relationships": [...],
      "metadata": {...}
    }
  }
}
```

## Available Actions

### 1. process_webhook_data
Processes raw webhook data and extracts basic information.

**Parameters:**
- `webhook_data`: Raw webhook payload
- `client_id`: Client identifier
- `action_id`: Action identifier

**Returns:** Processed webhook data with metadata

### 2. extract_client_knowledge_graph
Extracts structured knowledge graph data from webhook payload.

**Parameters:**
- `webhook_data`: Raw webhook payload
- `client_id`: Client identifier
- `include_task_details`: Whether to include full task details

**Returns:** Structured knowledge graph with nodes and relationships

### 3. send_webhook_response
Sends a response back to the webhook source (requires approval).

**Parameters:**
- `response_url`: URL to send response to
- `response_data`: Data to send in response
- `response_type`: Type of response
- `client_id`: Client identifier

**Returns:** Response status and details

### 4. validate_webhook_signature
Validates webhook signature for security.

**Parameters:**
- `webhook_data`: Raw webhook payload
- `signature`: Webhook signature
- `secret_key`: Secret key for validation
- `client_id`: Client identifier

**Returns:** Validation result

## Configuration

### Environment Variables

Set these environment variables for webhook configuration:

```bash
# Make.com webhook secret
MAKE_COM_WEBHOOK_SECRET=your_secret_here

# Make.com webhook endpoint (optional)
MAKE_COM_WEBHOOK_ENDPOINT=https://your-endpoint.com

# Webhook validation (default: true)
WEBHOOK_VALIDATION_ENABLED=true

# Webhook timeout in seconds (default: 30)
WEBHOOK_TIMEOUT_SECONDS=30
```

### Programmatic Configuration

```python
from mcp_server.core.server import MCPServer

server = MCPServer()

# Register webhook secrets
server.register_webhook_secret("make.com", "your_secret_here")

# Register webhook routes
server.register_webhook_route("make.com_chatgpt_clients", "process_webhook_data")
```

## Testing

### Test Webhook Integration

Run the webhook integration test:

```bash
python test_webhook_integration.py
```

### Manual Testing

Test the webhook endpoint manually:

```bash
curl -X POST http://localhost:8000/api/webhook/make.com/chatgpt-clients \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "test-client",
    "action_id": "get_client_data",
    "task": {
      "id": "task_123",
      "name": "Test Task",
      "description": "Test description"
    }
  }'
```

## Security

### Signature Validation

The server supports HMAC-SHA256 signature validation for webhooks:

1. **Register Secret**: Add your webhook secret to the server
2. **Validate Signature**: The server automatically validates incoming webhooks
3. **Reject Invalid**: Webhooks with invalid signatures are rejected

### Approval Workflow

Sensitive webhook actions (like sending responses) require human approval:

1. **Action Triggered**: Webhook action is triggered
2. **Approval Request**: Server creates approval request
3. **Human Review**: Human reviews and approves/rejects
4. **Execution**: Approved actions are executed

## Error Handling

The webhook integration includes comprehensive error handling:

- **Invalid Payload**: Returns 400 with error details
- **Missing Fields**: Returns 400 with field requirements
- **Processing Errors**: Returns 500 with error information
- **Timeout Errors**: Returns 408 for long-running operations

## Monitoring

### Logging

All webhook operations are logged with unique IDs:

```
2024-01-01 12:00:00 - webhook_handler - INFO - Processing Make.com webhook: uuid-123
2024-01-01 12:00:01 - process_webhook_data - INFO - Successfully processed webhook data for client: client-123
```

### Status Endpoint

Check webhook status:

```bash
curl http://localhost:8000/api/status
```

## Troubleshooting

### Common Issues

1. **Webhook Not Received**
   - Check server is running on correct port
   - Verify webhook URL is correct
   - Check firewall settings

2. **Signature Validation Fails**
   - Verify secret key is correct
   - Check signature format
   - Ensure payload hasn't been modified

3. **Processing Errors**
   - Check webhook payload format
   - Verify required fields are present
   - Review server logs for details

### Debug Mode

Enable debug mode for detailed logging:

```python
server = MCPServer(debug=True)
```

## Extending

### Adding New Webhook Types

1. **Create Handler**: Add new webhook handler method
2. **Register Route**: Add route in server setup
3. **Add Actions**: Create actions for processing
4. **Test**: Test with sample webhook data

### Custom Processing

Extend webhook processing by:

1. **Adding Actions**: Create new actions for specific processing
2. **Modifying Handlers**: Update webhook handlers for custom logic
3. **Adding Validation**: Implement custom validation rules
4. **Enhancing Security**: Add additional security measures
