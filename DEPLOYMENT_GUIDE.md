# 🚀 Render Deployment Guide

## Overview
This guide will help you deploy your MCP server to Render and connect it to ChatGPT as a Custom GPT Action.

## 📋 Prerequisites
- [x] Render account (free tier available)
- [x] GitHub account
- [x] Your MCP server code (this project)

## 🔧 Step 1: Prepare Your Code

### Files Created for Deployment:
- `render.yaml` - Render configuration
- `Dockerfile` - Container configuration  
- `main_deploy.py` - Deployment-optimized server
- `requirements.txt` - Python dependencies

### Key Changes for Deployment:
- ✅ CORS enabled for web access
- ✅ Environment variable support
- ✅ Port configuration for Render
- ✅ Proper logging for cloud deployment

## 📤 Step 2: Push to GitHub

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit for Render deployment"

# Create GitHub repository
# Go to github.com and create a new repository

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## 🌐 Step 3: Deploy to Render

### Option A: Using render.yaml (Recommended)
1. Go to [render.com](https://render.com)
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Click "Apply" to deploy

### Option B: Manual Setup
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `mcp-server`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main_deploy.py`
   - **Port**: `8000`

## 🔐 Step 4: Environment Variables

In Render dashboard, add these environment variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `PORT` | `8000` | Server port |
| `WEBHOOK_SECRET` | `your-secret-here` | Webhook security |
| `MAKE_API_KEY` | `YOUR_MAKE_API_KEY` | Make.com API key |

## 🌍 Step 5: Get Your Public URL

After deployment, Render will provide:
- **URL**: `https://your-app-name.onrender.com`
- **Status**: Should show "Live"

## 🤖 Step 6: Configure ChatGPT Action

### Create Custom GPT Action:
1. Go to ChatGPT → Create GPT
2. Click "Configure" → "Actions" tab
3. Click "Add action" → "Import from URL"
4. Use this OpenAPI spec:

```yaml
openapi: 3.0.0
info:
  title: Client Knowledge Graph API
  description: Access client data and knowledge graphs
  version: 1.0.0
servers:
  - url: https://your-app-name.onrender.com
    description: MCP Server
paths:
  /api/action/get_client_data:
    post:
      summary: Get client data
      operationId: getClientData
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                client_id:
                  type: string
                  example: "86drqmpje"
              required: [client_id]
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
```

## 🧪 Step 7: Test Your Deployment

### Test the API:
```bash
curl -X POST https://your-app-name.onrender.com/api/action/get_client_data \
  -H "Content-Type: application/json" \
  -d '{"client_id": "86drqmpje"}'
```

### Test in ChatGPT:
- "Get client data for 86drqmpje"
- "What services does this client offer?"
- "Show me the contact information"

## 🔄 Step 8: Update Webhook URLs

Update your Make.com scenario webhook URL to:
`https://your-app-name.onrender.com/webhook/make.com_chatgpt_clients`

## 📊 Monitoring

- **Render Dashboard**: Monitor logs and performance
- **Health Check**: `https://your-app-name.onrender.com/health`
- **Status Page**: Render provides uptime monitoring

## 🚨 Troubleshooting

### Common Issues:
1. **Build fails**: Check `requirements.txt` and Python version
2. **Port issues**: Ensure `PORT` env var is set
3. **CORS errors**: Verify CORS is enabled in server
4. **Webhook timeouts**: Check Render's timeout limits

### Debug Commands:
```bash
# Check logs in Render dashboard
# Test locally first
python main_deploy.py
```

## 🎯 Next Steps

After deployment:
1. ✅ Test webhook integration
2. ✅ Verify ChatGPT Action works
3. ✅ Monitor performance
4. ✅ Set up alerts for downtime

## 📞 Support

- Render Documentation: [docs.render.com](https://docs.render.com)
- Render Community: [community.render.com](https://community.render.com)
