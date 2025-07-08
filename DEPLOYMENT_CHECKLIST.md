# 🚀 Deployment Checklist - Slack Task Assignment Bot

Use this checklist to ensure your bot is properly deployed and configured.

## 📁 Files to Upload to GitHub

### ✅ Core Application Files
- [ ] `app.py` - Main Flask application
- [ ] `requirements.txt` - Python dependencies
- [ ] `Procfile` - For Heroku/Railway deployment
- [ ] `runtime.txt` - Python version specification
- [ ] `Dockerfile` - For containerized deployment
- [ ] `docker-compose.yml` - For local development
- [ ] `deploy.sh` - Local deployment script

### ✅ Configuration Files
- [ ] `.gitignore` - Git ignore rules
- [ ] `env.example` - Environment variables template
- [ ] `README.md` - Project documentation
- [ ] `SETUP_GUIDE.md` - Detailed setup instructions

### ✅ Application Structure
- [ ] `models/__init__.py` - Models package
- [ ] `models/task.py` - Task database model
- [ ] `routes/__init__.py` - Routes package
- [ ] `routes/slack.py` - Slack bot routes

## 🌐 Deployment Platform Setup

### Railway (Recommended)
- [ ] Created Railway account
- [ ] Connected GitHub repository
- [ ] Created new project from GitHub repo
- [ ] Set environment variables:
  - [ ] `SLACK_SIGNING_SECRET=e178377b1931850482d86a6920d7ef00`
  - [ ] `SLACK_BOT_TOKEN=xoxb-9153598789972-9163840334662-quLu21epAVWYaDdAN11M3gOx`
  - [ ] `SLACK_APP_TOKEN=xapp-1-A094Z78RBN0-9180856017889-be5c3d466513ada2fbba58c60366f952527a4224aefa6bcd2be99e5bd71893dc`
  - [ ] `SECRET_KEY=your-super-secret-key-change-this`
  - [ ] `DATABASE_URL=sqlite:///tasks.db`
- [ ] Deployment successful
- [ ] Got deployment URL: `https://your-app-name.railway.app`

### Alternative: Heroku
- [ ] Installed Heroku CLI
- [ ] Created Heroku app
- [ ] Set environment variables
- [ ] Deployed with `git push heroku main`

### Alternative: Render
- [ ] Created Render account
- [ ] Connected GitHub repository
- [ ] Created web service
- [ ] Set environment variables
- [ ] Deployment successful

## 🔧 Slack App Configuration

### Basic Information
- [ ] App name: "Task Assignment Bot"
- [ ] App created in your workspace
- [ ] Signing Secret verified: `e178377b1931850482d86a6920d7ef00`

### Slash Commands
- [ ] `/addtask` command created
  - [ ] Request URL: `https://your-deployment-url.com/slack/addtask`
  - [ ] Description: "Create and assign a new task"
  - [ ] Usage Hint: `[task description]`
- [ ] `/showlist` command created
  - [ ] Request URL: `https://your-deployment-url.com/slack/showlist`
  - [ ] Description: "Display all tasks with status controls"
  - [ ] Usage Hint: `(no parameters needed)`

### Interactive Components
- [ ] Interactivity enabled
- [ ] Request URL: `https://your-deployment-url.com/slack/interactive`
- [ ] Changes saved

### OAuth & Permissions
- [ ] Bot token scopes added:
  - [ ] `commands`
  - [ ] `chat:write`
  - [ ] `chat:write.public`
- [ ] App installed to workspace
- [ ] Permissions granted

## 🧪 Testing Checklist

### Health Check
- [ ] Visit: `https://your-deployment-url.com/health`
- [ ] Response: `{"status": "healthy"}`

### Slack Commands
- [ ] `/addtask Test task` works
- [ ] Shows team member buttons: [David] [Emma] [Nora] [Eric] [Kenny]
- [ ] Clicking a team member creates the task
- [ ] `/showlist` shows all tasks
- [ ] Status buttons work (Done, In Progress, Not Done)

### Security
- [ ] Invalid requests return 401 Unauthorized
- [ ] HMAC signature verification working
- [ ] Timestamp validation working

## 🔒 Security Verification

### Environment Variables
- [ ] All sensitive data in environment variables
- [ ] No hardcoded secrets in code
- [ ] `.env` file in `.gitignore`

### Request Verification
- [ ] Slack signing secret matches exactly
- [ ] HMAC signature verification enabled
- [ ] Timestamp validation (5-minute window)
- [ ] Unauthorized requests blocked

## 📱 Bot Features

### Team Members
- [ ] David
- [ ] Emma
- [ ] Nora
- [ ] Eric
- [ ] Kenny

### Task Status Options
- [ ] Done ✅
- [ ] In Progress 🔄
- [ ] Not Done ❌

### Commands
- [ ] `/addtask [description]` - Create and assign tasks
- [ ] `/showlist` - View all tasks with status controls

## 🚨 Troubleshooting

### If Commands Don't Work
- [ ] Check deployment URL is accessible
- [ ] Verify all URLs in Slack app settings
- [ ] Test health endpoint
- [ ] Check deployment logs
- [ ] Ensure app is installed to workspace

### If Getting "Unauthorized" Errors
- [ ] Verify signing secret matches exactly
- [ ] Check request timestamps
- [ ] Ensure all environment variables are set
- [ ] Test with curl: `curl https://your-url.com/health`

### If Database Issues
- [ ] Check DATABASE_URL format
- [ ] Verify write permissions
- [ ] Check deployment logs for database errors

## 🎉 Success Criteria

Your bot is successfully deployed when:
- [ ] Health endpoint returns `{"status": "healthy"}`
- [ ] `/addtask` command works and shows team member buttons
- [ ] `/showlist` command shows tasks with status buttons
- [ ] Status buttons update task status correctly
- [ ] All team members can use the bot
- [ ] Tasks persist between bot restarts

## 📞 Final Steps

- [ ] Share bot usage instructions with your team
- [ ] Test with real tasks
- [ ] Monitor deployment logs for any issues
- [ ] Set up monitoring/alerting if needed

## 🚀 Deployment Complete!

Once all items are checked:
1. ✅ Your bot is live and secure
2. ✅ Team can create and track tasks
3. ✅ All features are working
4. ✅ Ready for production use

**Your Slack Task Assignment Bot is now ready! 🎉** 