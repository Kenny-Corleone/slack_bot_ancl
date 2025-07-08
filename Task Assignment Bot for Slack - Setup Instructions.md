# Task Assignment Bot for Slack - Setup Instructions

This Slack bot has been updated to implement a task assignment system with specific team members and status tracking as requested. It allows dispatchers to assign tasks to team members and track their progress.

## Deployed Application

The updated bot is deployed and ready to use at: **https://nghki1c83wll.manus.space**

## Key Features

✅ **Task Assignment System** - Assign tasks to specific team members  
✅ **Team Member Selection** - Choose from David, Emma, Nora, Eric, Kenny  
✅ **Status Tracking** - Three status levels: Done, In Progress, Not Done  
✅ **Dispatcher Control** - Only dispatchers can change task status  
✅ **Date Tracking** - Shows creation date and time for each task  
✅ **Interactive Interface** - Click buttons to assign and update tasks  

## Available Commands

### `/addtask [task description]`
Creates a new task and shows team member selection buttons.

**Example:**
```
/addtask Review project proposal
```
This will show buttons for David, Emma, Nora, Eric, and Kenny to assign the task.

### `/showlist`
Displays all tasks for the current channel with:
- Date and time of task creation
- Task description
- Assigned team member
- Current status (with emoji indicators)
- Interactive buttons to change status

**Example Output:**
```
Task List:
❌ 2025-07-08 22:27 | Review project proposal | Assigned to: David | Status: no
🔄 2025-07-08 22:30 | Update documentation | Assigned to: Emma | Status: in progress
✅ 2025-07-08 22:25 | Fix login bug | Assigned to: Nora | Status: done
```

## Team Members

Tasks can be assigned to the following team members:
- **David**
- **Emma** 
- **Nora**
- **Eric**
- **Kenny**

## Status Options

Each task can have one of three status levels:
- **Done** ✅ - Task completed
- **In Progress** 🔄 - Task being worked on
- **Not Done** ❌ - Task not started or incomplete

## Workflow

1. **Create Task**: Use `/addtask [description]` to create a new task
2. **Assign Member**: Click on a team member button to assign the task
3. **View Tasks**: Use `/showlist` to see all tasks with dates and status
4. **Update Status**: Click status buttons to change task progress (dispatcher control)

## Slack App Setup Instructions

### Step 1: Create a New Slack App

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Click "Create New App"
3. Choose "From scratch"
4. Enter app name: "Task Assignment Bot"
5. Select your workspace
6. Click "Create App"

### Step 2: Configure Slash Commands

1. In your app settings, go to "Slash Commands" in the left sidebar
2. Click "Create New Command" for each command:

**Command 1:**
- **Command**: `/addtask`
- **Request URL**: `https://nghki1c83wll.manus.space/slack/addtask`
- **Short Description**: `Create and assign a new task`
- **Usage Hint**: `[task description]`

**Command 2:**
- **Command**: `/showlist`
- **Request URL**: `https://nghki1c83wll.manus.space/slack/showlist`
- **Short Description**: `Display all tasks with status controls`
- **Usage Hint**: `(no parameters needed)`

3. Click "Save" for each command

### Step 3: Configure Interactive Components

1. In your app settings, go to "Interactivity & Shortcuts" in the left sidebar
2. Turn on "Interactivity"
3. Set the **Request URL** to: `https://nghki1c83wll.manus.space/slack/interactive`
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

Note: Request verification is currently disabled in the code for easier testing. To enable it, uncomment the verification lines in the endpoints.

## Usage Examples

### Creating and Assigning Tasks

```
/addtask Review quarterly budget report
```
→ Shows buttons: [David] [Emma] [Nora] [Eric] [Kenny]
→ Click "Emma" to assign the task

### Viewing Task List

```
/showlist
```
→ Shows all tasks with status buttons for each task

### Updating Task Status

When viewing the task list, click the status buttons:
- **Done** - Mark task as completed
- **In Progress** - Mark task as being worked on  
- **Not Done** - Mark task as not started/incomplete

## Technical Details

- **Backend**: Flask application with SQLite database
- **Database**: Stores tasks with assignment and status tracking
- **Deployment**: Hosted on Manus platform
- **Features**: Interactive buttons for assignment and status updates
- **Team Members**: Hardcoded list of 5 team members
- **Status Tracking**: Three-level status system with emoji indicators

## Database Schema

The Task model includes:
- `id` - Unique task identifier
- `task_description` - Task description text
- `assigned_to` - Team member name (David, Emma, Nora, Eric, Kenny)
- `status` - Current status (done, no, in progress)
- `channel_id` - Slack channel where task was created
- `dispatcher_id` - User who created the task
- `created_at` - Timestamp of task creation

## Troubleshooting

If you encounter issues:

1. Ensure your Slack app has the correct permissions
2. Verify both slash command URLs are set correctly
3. Check that the interactive components URL is configured
4. Ensure the app is installed in your workspace
5. Try reinstalling the app if commands don't appear

## Source Code

The complete source code is available in the `/home/ubuntu/slack-todo-bot` directory and includes:

- Updated Flask application with task assignment logic
- SQLite database models for task tracking
- Interactive components for team member selection and status updates
- Web interface showing the new functionality

For support or questions, refer to the Slack API documentation at [https://api.slack.com/](https://api.slack.com/).

