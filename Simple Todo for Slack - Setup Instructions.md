# Simple Todo for Slack - Setup Instructions

This Slack bot replicates the functionality of the Simple Todo app from getsimpletodo.com. It allows teams to manage todo lists directly within Slack channels and conversations.

## Deployed Application

The bot is deployed and ready to use at: **https://w5hni7cowkm9.manus.space**

## Features

- **Simple**: Add items as quickly as you can think of them with `/todo [item]`
- **Built In**: Every channel, group, and private conversation has its own todo list
- **Done**: Mark items as complete or clear the entire list

## Available Commands

- `/todo [item]` - Add a new todo item to the current channel/conversation
- `/todo` - Show the current todo list for the channel/conversation
- `/todo done [number]` - Mark a specific todo item as done
- `/todo clear` - Clear all todo items from the current channel/conversation

## Slack App Setup Instructions

### Step 1: Create a New Slack App

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Click "Create New App"
3. Choose "From scratch"
4. Enter app name: "Simple Todo"
5. Select your workspace
6. Click "Create App"

### Step 2: Configure Slash Commands

1. In your app settings, go to "Slash Commands" in the left sidebar
2. Click "Create New Command"
3. Fill in the following details:
   - **Command**: `/todo`
   - **Request URL**: `https://w5hni7cowkm9.manus.space/slack/todo`
   - **Short Description**: `Manage todo items in this channel`
   - **Usage Hint**: `[item] or done [number] or clear`
4. Click "Save"

### Step 3: Configure Interactive Components

1. In your app settings, go to "Interactivity & Shortcuts" in the left sidebar
2. Turn on "Interactivity"
3. Set the **Request URL** to: `https://w5hni7cowkm9.manus.space/slack/interactive`
4. Click "Save Changes"

### Step 4: Set OAuth Permissions

1. Go to "OAuth & Permissions" in the left sidebar
2. Under "Scopes" → "Bot Token Scopes", add the following permissions:
   - `commands` - Add shortcuts and/or slash commands that people can use
   - `chat:write` - Send messages as the app
   - `chat:write.public` - Send messages to channels the app isn't a member of

### Step 5: Install the App

1. Go to "Install App" in the left sidebar
2. Click "Install to Workspace"
3. Review the permissions and click "Allow"

### Step 6: Get Your Signing Secret (Optional)

For production use, you should verify requests from Slack:

1. Go to "Basic Information" in the left sidebar
2. Under "App Credentials", find your "Signing Secret"
3. Set this as an environment variable `SLACK_SIGNING_SECRET` in your deployment

Note: Request verification is currently disabled in the code for easier testing. To enable it, uncomment the verification lines in the `/slack/todo` and `/slack/interactive` endpoints.

## Usage Examples

Once installed, you can use the bot in any channel or direct message:

```
/todo Buy groceries
/todo Review pull request
/todo Schedule team meeting
```

To view your todo list:
```
/todo
```

To mark items as done:
```
/todo done 1
/todo done 2
```

To clear all items:
```
/todo clear
```

## Technical Details

- **Backend**: Flask application with SQLite database
- **Database**: Stores todo items per channel with user attribution
- **Deployment**: Hosted on Manus platform
- **Features**: Interactive buttons for marking items as done

## Troubleshooting

If you encounter issues:

1. Ensure your Slack app has the correct permissions
2. Verify the request URLs are set correctly
3. Check that the app is installed in your workspace
4. Try reinstalling the app if commands don't appear

## Source Code

The complete source code is available in the `/home/ubuntu/slack-todo-bot` directory and includes:

- Flask application with CORS support
- SQLite database models for todo items
- Slack slash command and interactive component handlers
- Web interface showing setup instructions

For support or questions, refer to the Slack API documentation at [https://api.slack.com/](https://api.slack.com/).

