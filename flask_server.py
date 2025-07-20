"""
Flask server for Render (more reliable)
"""

import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "mcp-server",
        "port": os.getenv('PORT', '8000')
    })

@app.route('/api/action/get_client_data', methods=['POST'])
def get_client_data():
    data = request.get_json()
    client_id = data.get('client_id', 'unknown') if data else 'unknown'
    
    return jsonify({
        "client_id": client_id,
        "status": "success",
        "message": f"Client data retrieved for {client_id}"
    })

@app.route('/api/action/process_webhook_data', methods=['POST'])
def process_webhook_data():
    data = request.get_json()
    
    return jsonify({
        "status": "success",
        "message": "Webhook data processed",
        "webhook_data": data
    })

@app.route('/webhook/make.com_chatgpt_clients', methods=['POST'])
def webhook_handler():
    data = request.get_json()
    
    return jsonify({
        "status": "success",
        "message": "Webhook received",
        "data": data
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    print(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
