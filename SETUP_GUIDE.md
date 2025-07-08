# 🚀 Slack Task Assignment Bot - Complete Setup Guide

This guide will walk you through setting up and deploying your Slack Task Assignment Bot step by step.

## 📋 Prerequisites

- GitHub account
- Python 3.11+ installed
- Slack workspace with admin permissions

## 🎯 Quick Start (5 minutes)

### Step 1: Upload to GitHub

1. **Create a new repository** on GitHub
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name it: `slack-task-bot`
   - Make it **Public** (for free deployment)
   - Don't initialize with README

2. **Upload all files** to your repository:
   ```
   app.py
   requirements.txt
   Procfile
   runtime.txt
   Dockerfile
   docker-compose.yml
   deploy.sh
   README.md
   .gitignore
   env.example
   models/
   ├── __init__.py
   └── task.py
   routes/
   ├── __init__.py
   └── slack.py
   ```

### Step 2: Deploy to Railway (Recommended)

1. **Go to [Railway](https://railway.app/)**
   - Sign up with GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `slack-task-bot` repository

2. **Configure Environment Variables**
   In Railway dashboard → Variables tab, add:
   ```
   SLACK_SIGNING_SECRET=e178377b1931850482d86a6920d7ef00
   SLACK_BOT_TOKEN=xoxb-9153598789972-9163840334662-quLu21epAVWYaDdAN11M3gOx
   SLACK_APP_TOKEN=xapp-1-A094Z78RBN0-9180856017889-be5c3d466513ada2fbba58c60366f952527a4224aefa6bcd2be99e5bd71893dc
   SECRET_KEY=your-super-secret-key-change-this
   DATABASE_URL=sqlite:///tasks.db
   ```

3. **Deploy**
   - Railway will automatically deploy
   - Get your URL: `https://your-app-name.railway.app`

### Step 3: Configure Slack App

1. **Go to [Slack API Apps](https://api.slack.com/apps)**
   - Click "Create New App"
   - Choose "From scratch"
   - App name: `Task Assignment Bot`
   - Select your workspace

2. **Configure Slash Commands**
   - Go to "Slash Commands" → "Create New Command"
   
   **Command 1:**
   - Command: `/addtask`
   - Request URL: `https://your-app-name.railway.app/slack/addtask`
   - Short Description: `Create and assign a new task`
   - Usage Hint: `[task description]`
   
   **Command 2:**
   - Command: `/showlist`
   - Request URL: `https://your-app-name.railway.app/slack/showlist`
   - Short Description: `Display all tasks with status controls`
   - Usage Hint: `(no parameters needed)`

3. **Configure Interactive Components**
   - Go to "Interactivity & Shortcuts"
   - Turn on "Interactivity"
   - Request URL: `https://your-app-name.railway.app/slack/interactive`
   - Save Changes

4. **Set OAuth Permissions**
   - Go to "OAuth & Permissions"
   - Add these scopes:
     - `commands`
     - `chat:write`
     - `chat:write.public`

5. **Install App**
   - Go to "Install App"
   - Click "Install to Workspace"
   - Allow permissions

## 🔧 Alternative Deployment Options

### Option A: Heroku

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Deploy**
   ```bash
   heroku create your-slack-bot-name
   heroku config:set SLACK_SIGNING_SECRET=e178377b1931850482d86a6920d7ef00
   heroku config:set SLACK_BOT_TOKEN=xoxb-9153598789972-9163840334662-quLu21epAVWYaDdAN11M3gOx
   heroku config:set SLACK_APP_TOKEN=xapp-1-A094Z78RBN0-9180856017889-be5c3d466513ada2fbba58c60366f952527a4224aefa6bcd2be99e5bd71893dc
   heroku config:set SECRET_KEY=your-secret-key
   git push heroku main
   ```

### Option B: Render

1. **Go to [Render](https://render.com/)**
   - Sign up with GitHub
   - "New Web Service"
   - Connect your repository

2. **Configure**
   - Name: `slack-task-bot`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

3. **Add Environment Variables**
   ```
   SLACK_SIGNING_SECRET=e178377b1931850482d86a6920d7ef00
   SLACK_BOT_TOKEN=xoxb-9153598789972-9163840334662-quLu21epAVWYaDdAN11M3gOx
   SLACK_APP_TOKEN=xapp-1-A094Z78RBN0-9180856017889-be5c3d466513ada2fbba58c60366f952527a4224aefa6bcd2be99e5bd71893dc
   SECRET_KEY=your-secret-key
   ```

### Option C: Local Development

1. **Clone and setup**
   ```bash
   git clone <your-repo-url>
   cd slack-task-bot
   chmod +x deploy.sh
   ./deploy.sh
   ```

2. **Use ngrok for local testing**
   ```bash
   # Install ngrok
   # Download from https://ngrok.com/
   
   # Start tunnel
   ngrok http 5000
   
   # Use the ngrok URL in your Slack app configuration
   ```

## 🧪 Testing Your Bot

### 1. Health Check
Visit: `https://your-deployment-url.com/health`
Should return: `{"status": "healthy"}`

### 2. Test Commands in Slack
```
/addtask Test task creation
/showlist
```

### 3. Expected Behavior
- `/addtask` should show team member buttons
- Clicking a team member should create the task
- `/showlist` should show all tasks with status buttons
- Status buttons should update task status

## 🔒 Security Verification

Your bot includes these security features:
- ✅ HMAC signature verification
- ✅ Timestamp validation (5-minute window)
- ✅ Request origin verification
- ✅ Unauthorized access protection

## 🚨 Troubleshooting

### Common Issues

1. **"Unauthorized" errors**
   - Check your signing secret matches exactly
   - Verify all URLs in Slack app settings
   - Ensure app is installed to workspace

2. **Commands not working**
   - Test health endpoint first
   - Check deployment logs
   - Verify slash command URLs

3. **Database errors**
   - For SQLite: Check write permissions
   - For PostgreSQL: Verify DATABASE_URL format

### Debug Steps

1. **Check deployment logs**
   - Railway: Project → Deployments → View logs
   - Heroku: `heroku logs --tail`
   - Render: Service → Logs

2. **Test endpoints manually**
   ```bash
   curl https://your-app-url.com/health
   curl https://your-app-url.com/slack/test
   ```

3. **Verify Slack app settings**
   - All URLs are correct
   - App is installed
   - Permissions are set

## 📱 Bot Usage

### Creating Tasks
```
/addtask Review quarterly budget report
```
→ Shows: [David] [Emma] [Nora] [Eric] [Kenny]

### Viewing Tasks
```
/showlist
```
→ Shows all tasks with status buttons

### Task Status
- ✅ Done
- 🔄 In Progress  
- ❌ Not Done

## 🎉 Success!

Once everything is working:
1. ✅ Your bot is deployed and running
2. ✅ Slack app is configured
3. ✅ Commands are working
4. ✅ Team can create and track tasks

## 📞 Support

If you need help:
1. Check the troubleshooting section
2. Verify all configuration steps
3. Test the health endpoint
4. Review deployment logs

Your Slack Task Assignment Bot is now ready for production use! 🚀 