# Slack Task Assignment Bot

A powerful Slack bot for creating, assigning, and tracking tasks within your team. Built with Flask and SQLAlchemy.

## 🚀 Features

- **Task Creation**: Create tasks with `/addtask [description]`
- **Team Assignment**: Assign tasks to team members (David, Emma, Nora, Eric, Kenny)
- **Status Tracking**: Track task status (Done ✅, In Progress 🔄, Not Done ❌)
- **Interactive Buttons**: Easy status updates with clickable buttons
- **Security**: HMAC signature verification for all Slack requests
- **Database Storage**: Persistent task storage with SQLite

## 📋 Available Commands

### `/addtask [task description]`
Creates a new task and shows team member selection buttons.

### `/showlist`
Displays all tasks with date, assignee, and status controls.

## 👥 Team Members
- David
- Emma  
- Nora
- Eric
- Kenny

## 📊 Status Options
- **Done** ✅ - Task completed
- **In Progress** 🔄 - Task being worked on
- **Not Done** ❌ - Task not started/incomplete

## 🛠️ Local Development Setup

### Prerequisites
- Python 3.11+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd slack-task-bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your Slack credentials
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

The bot will be available at `http://localhost:5000`

## 🌐 Deployment Options

### Option 1: Railway (Recommended)

1. **Fork this repository** to your GitHub account

2. **Go to [Railway](https://railway.app/)**
   - Sign up with GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your forked repository

3. **Configure Environment Variables**
   In Railway dashboard, add these variables:
   ```
   SLACK_SIGNING_SECRET=e178377b1931850482d86a6920d7ef00
   SLACK_BOT_TOKEN=xoxb-9153598789972-9163840334662-quLu21epAVWYaDdAN11M3gOx
   SLACK_APP_TOKEN=xapp-1-A094Z78RBN0-9180856017889-be5c3d466513ada2fbba58c60366f952527a4224aefa6bcd2be99e5bd71893dc
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///tasks.db
   ```

4. **Deploy**
   - Railway will automatically deploy your app
   - Get your deployment URL (e.g., `https://your-app.railway.app`)

### Option 2: Heroku

1. **Install Heroku CLI**
   ```bash
   # Follow instructions at https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku app**
   ```bash
   heroku create your-slack-bot-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set SLACK_SIGNING_SECRET=e178377b1931850482d86a6920d7ef00
   heroku config:set SLACK_BOT_TOKEN=xoxb-9153598789972-9163840334662-quLu21epAVWYaDdAN11M3gOx
   heroku config:set SLACK_APP_TOKEN=xapp-1-A094Z78RBN0-9180856017889-be5c3d466513ada2fbba58c60366f952527a4224aefa6bcd2be99e5bd71893dc
   heroku config:set SECRET_KEY=your-secret-key-here
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

### Option 3: Render

1. **Go to [Render](https://render.com/)**
   - Sign up with GitHub
   - Click "New Web Service"
   - Connect your GitHub repository

2. **Configure the service**
   - **Name**: `slack-task-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

3. **Add Environment Variables**
   ```
   SLACK_SIGNING_SECRET=e178377b1931850482d86a6920d7ef00
   SLACK_BOT_TOKEN=xoxb-9153598789972-9163840334662-quLu21epAVWYaDdAN11M3gOx
   SLACK_APP_TOKEN=xapp-1-A094Z78RBN0-9180856017889-be5c3d466513ada2fbba58c60366f952527a4224aefa6bcd2be99e5bd71893dc
   SECRET_KEY=your-secret-key-here
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy your app

## 🔧 Slack App Configuration

### Step 1: Create/Update Your Slack App

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Select your existing app or create a new one
3. Enter app name: "Task Assignment Bot"

### Step 2: Configure Slash Commands

Add these two slash commands in your app settings:

**Command 1:**
- **Command**: `/addtask`
- **Request URL**: `https://your-deployment-url.com/slack/addtask`
- **Short Description**: `Create and assign a new task`
- **Usage Hint**: `[task description]`

**Command 2:**
- **Command**: `/showlist`
- **Request URL**: `https://your-deployment-url.com/slack/showlist`
- **Short Description**: `Display all tasks with status controls`
- **Usage Hint**: `(no parameters needed)`

### Step 3: Configure Interactive Components

1. Go to "Interactivity & Shortcuts" in your app settings
2. Turn on "Interactivity"
3. Set **Request URL**: `https://your-deployment-url.com/slack/interactive`
4. Click "Save Changes"

### Step 4: Set OAuth Permissions

Add these bot token scopes:
- `commands` - Add shortcuts and/or slash commands
- `chat:write` - Send messages as the app
- `chat:write.public` - Send messages to channels the app isn't a member of

### Step 5: Verify Signing Secret

1. Go to "Basic Information" → "App Credentials"
2. Confirm your **Signing Secret** matches: `e178377b1931850482d86a6920d7ef00`
3. If different, update the secret in your app settings

### Step 6: Install/Reinstall the App

1. Go to "Install App" in the left sidebar
2. Click "Reinstall to Workspace" (if previously installed)
3. Review permissions and click "Allow"

## 🔒 Security Features

- **Slack Request Verification**: All requests are verified using your signing secret
- **Timestamp Validation**: Requests older than 5 minutes are rejected
- **HMAC Signature Verification**: Ensures requests are genuinely from Slack
- **Unauthorized Access Protection**: Invalid requests return 401 Unauthorized

## 📱 Usage Examples

### Creating Tasks
```
/addtask Review quarterly budget report
```
→ Shows buttons: [David] [Emma] [Nora] [Eric] [Kenny]

### Viewing Tasks
```
/showlist
```
→ Shows all tasks with interactive status buttons

### Task List Format
```
❌ 2025-07-08 22:45 | Review budget report | Assigned to: David | Status: no
🔄 2025-07-08 22:30 | Update documentation | Assigned to: Emma | Status: in progress  
✅ 2025-07-08 22:15 | Fix login bug | Assigned to: Nora | Status: done
```

## 🛠️ Technical Details

- **Framework**: Flask with CORS support
- **Database**: SQLite with SQLAlchemy ORM
- **Security**: HMAC-SHA256 signature verification
- **Deployment**: Supports Railway, Heroku, Render, and other platforms
- **Request Validation**: 5-minute timestamp window

## 🔧 Troubleshooting

### Common Issues

1. **"Unauthorized" errors**
   - Verify your Slack app's signing secret matches exactly
   - Ensure all endpoint URLs are updated in Slack app settings
   - Try reinstalling the app to your workspace

2. **Commands not working**
   - Check that your deployment URL is accessible
   - Verify slash commands are properly configured in Slack app
   - Ensure the bot is installed to your workspace

3. **Database issues**
   - For SQLite: Ensure the app has write permissions
   - For PostgreSQL: Check DATABASE_URL format

### Health Check

Test if your bot is running by visiting:
```
https://your-deployment-url.com/health
```

Should return: `{"status": "healthy"}`

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify your Slack app configuration
3. Test the health endpoint
4. Check deployment logs for errors 