from flask import Blueprint, request, jsonify
from models.task import Task
import json
import hmac
import hashlib
import time
import os
import requests

from database import db

slack_bp = Blueprint("slack", __name__)

# Slack credentials
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET", "e178377b1931850482d86a6920d7ef00")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "xoxb-9153598789972-9163840334662-quLu21epAVWYaDdAN11M3gOx")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN", "xapp-1-A094Z78RBN0-9180856017889-be5c3d466513ada2fbba58c60366f952527a4224aefa6bcd2be99e5bd71893dc")

# Slack API endpoints
SLACK_API_BASE = "https://slack.com/api"

# Team members for task assignment
TEAM_MEMBERS = ["David", "Emma", "Nora", "Eric", "Kenny"]
STATUS_OPTIONS = ["done", "no", "in progress"]

def verify_slack_request(request):
    """Verify that the request is from Slack"""
    timestamp = request.headers.get("X-Slack-Request-Timestamp")
    if not timestamp:
        return False
    
    # Check if request is too old (more than 5 minutes)
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False
    
    # Create signature
    sig_basestring = f"v0:{timestamp}:{request.get_data(as_text=True)}"
    my_signature = "v0=" + hmac.new(
        SLACK_SIGNING_SECRET.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()
    
    slack_signature = request.headers.get("X-Slack-Signature")
    return hmac.compare_digest(my_signature, slack_signature or "")

@slack_bp.route("/addtask", methods=["POST"])
def handle_addtask_command():
    """Handle /addtask slash command"""
    if not verify_slack_request(request):
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.form
    text = data.get("text", "").strip()
    channel_id = data.get("channel_id")
    user_id = data.get("user_id")
    
    if not text:
        return jsonify({
            "response_type": "ephemeral",
            "text": "Please provide a task description. Usage: `/addtask [task description]`"
        })
    
    # Show team member selection buttons
    attachments = [{
        "text": f"Task: {text}\nSelect team member to assign this task to:",
        "callback_id": f"assign_task",
        "actions": []
    }]
    
    # Add buttons for each team member
    for member in TEAM_MEMBERS:
        attachments[0]["actions"].append({
            "name": "assign",
            "text": member,
            "type": "button",
            "value": json.dumps({
                "task": text,
                "member": member,
                "channel_id": channel_id,
                "dispatcher_id": user_id
            })
        })
    
    return jsonify({
        "response_type": "ephemeral",
        "text": "Choose team member for task assignment:",
        "attachments": attachments
    })

@slack_bp.route("/showlist", methods=["POST"])
def handle_showlist_command():
    """Handle /showlist slash command"""
    if not verify_slack_request(request):
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.form
    channel_id = data.get("channel_id")
    user_id = data.get("user_id")
    
    # Get all tasks for this channel
    tasks = Task.query.filter_by(channel_id=channel_id).order_by(Task.created_at.desc()).all()
    
    if not tasks:
        return jsonify({
            "response_type": "in_channel",
            "text": "No tasks found. Create one with `/addtask [task description]`"
        })
    
    # Format task list
    task_list = []
    attachments = []
    
    for task in tasks:
        status_emoji = {
            "done": "✅",
            "no": "❌", 
            "in progress": "🔄"
        }.get(task.status, "❓")
        
        task_text = f"{status_emoji} *{task.created_at.strftime('%Y-%m-%d %H:%M')}* | {task.task_description} | Assigned to: *{task.assigned_to}* | Status: *{task.status}*"
        task_list.append(task_text)
        
        # Add status change buttons for each task
        attachments.append({
            "text": f"Task #{task.id}: {task.task_description} (Assigned to: {task.assigned_to})",
            "callback_id": f"change_status_{task.id}",
            "actions": [
                {
                    "name": "status",
                    "text": "Done",
                    "type": "button",
                    "value": json.dumps({"task_id": task.id, "status": "done"}),
                    "style": "primary" if task.status != "done" else "default"
                },
                {
                    "name": "status",
                    "text": "In Progress",
                    "type": "button", 
                    "value": json.dumps({"task_id": task.id, "status": "in progress"}),
                    "style": "primary" if task.status != "in progress" else "default"
                },
                {
                    "name": "status",
                    "text": "Not Done",
                    "type": "button",
                    "value": json.dumps({"task_id": task.id, "status": "no"}),
                    "style": "danger" if task.status != "no" else "default"
                }
            ]
        })
    
    response_text = "*Task List:*\n" + "\n".join(task_list)
    
    return jsonify({
        "response_type": "ephemeral",
        "text": response_text,
        "attachments": attachments
    })

@slack_bp.route("/interactive", methods=["POST"])
def handle_interactive():
    """Handle interactive button clicks"""
    if not verify_slack_request(request):
        return jsonify({"error": "Unauthorized"}), 401
    
    payload = json.loads(request.form.get("payload"))
    user_id = payload["user"]["id"]
    
    # Handle home tab interactions
    if payload.get("type") == "view_submission":
        return handle_view_submission(payload)
    
    # Handle button clicks from home tab
    if payload.get("type") == "block_actions":
        return handle_block_actions(payload)
    
    # Handle legacy interactive components
    if payload.get("type") == "interactive_message":
        return handle_legacy_interactive(payload)
    
    # Handle task assignment
    if payload["callback_id"] == "assign_task":
        action = payload["actions"][0]
        task_data = json.loads(action["value"])
        
        # Create new task
        new_task = Task(
            task_description=task_data["task"],
            assigned_to=task_data["member"],
            channel_id=task_data["channel_id"],
            dispatcher_id=task_data["dispatcher_id"]
        )
        db.session.add(new_task)
        db.session.commit()
        
        return jsonify({
            "response_type": "in_channel",
            "text": f"✅ Task assigned to *{task_data['member']}*: {task_data['task']}",
            "replace_original": True
        })
    
    # Handle status changes
    elif payload["callback_id"].startswith("change_status_"):
        task_id = int(payload["callback_id"].split("_")[-1])
        action = payload["actions"][0]
        status_data = json.loads(action["value"])
        
        task = Task.query.get(task_id)
        if task:
            old_status = task.status
            task.status = status_data["status"]
            db.session.commit()
            
            status_emoji = {
                "done": "✅",
                "no": "❌",
                "in progress": "🔄"
            }.get(task.status, "❓")
            
            return jsonify({
                "response_type": "in_channel",
                "text": f"{status_emoji} <@{user_id}> changed task status: \"{task.task_description}\" → *{task.status}*",
                "replace_original": False
            })
    
            return jsonify({"text": "Action completed"})

def handle_view_submission(payload):
    """Handle view submission from home tab"""
    try:
        user_id = payload["user"]["id"]
        view = payload["view"]
        
        if view["callback_id"] == "create_task_modal":
            # Handle task creation from modal
            values = view["state"]["values"]
            task_description = values["task_description"]["task_input"]["value"]
            assigned_to = values["assigned_to"]["assignee_select"]["selected_option"]["value"]
            
            # Create new task
            new_task = Task(
                task_description=task_description,
                assigned_to=assigned_to,
                channel_id="home_tab",  # Special identifier for home tab tasks
                dispatcher_id=user_id
            )
            db.session.add(new_task)
            db.session.commit()
            
            # Update home tab
            update_home_tab(user_id)
            
            return jsonify({"response_action": "clear"})
        
        return jsonify({"response_action": "clear"})
    except Exception as e:
        print(f"Error handling view submission: {e}")
        return jsonify({"response_action": "clear"})

def handle_block_actions(payload):
    """Handle block actions from home tab"""
    try:
        user_id = payload["user"]["id"]
        actions = payload["actions"]
        
        for action in actions:
            action_id = action["action_id"]
            
            if action_id == "create_task":
                # Open task creation modal
                return open_task_creation_modal(user_id)
            
            elif action_id == "refresh_tasks":
                # Refresh home tab
                update_home_tab(user_id)
                return jsonify({"text": "Tasks refreshed!"})
            
            elif action_id.startswith("change_status_"):
                # Handle status change
                task_id = int(action_id.split("_")[-1])
                value = json.loads(action["value"])
                
                task = Task.query.get(task_id)
                if task:
                    task.status = value.get("status", "done")
                    db.session.commit()
                    update_home_tab(user_id)
                
                return jsonify({"text": "Status updated!"})
        
        return jsonify({"text": "Action completed"})
    except Exception as e:
        print(f"Error handling block actions: {e}")
        return jsonify({"text": "Error occurred"})

def handle_legacy_interactive(payload):
    """Handle legacy interactive components"""
    user_id = payload["user"]["id"]
    
    # Handle task assignment
    if payload["callback_id"] == "assign_task":
        action = payload["actions"][0]
        task_data = json.loads(action["value"])
        
        # Create new task
        new_task = Task(
            task_description=task_data["task"],
            assigned_to=task_data["member"],
            channel_id=task_data["channel_id"],
            dispatcher_id=task_data["dispatcher_id"]
        )
        db.session.add(new_task)
        db.session.commit()
        
        # Update home tab for the assigned user
        update_home_tab(task_data["member"])
        
        return jsonify({
            "response_type": "in_channel",
            "text": f"✅ Task assigned to *{task_data['member']}*: {task_data['task']}",
            "replace_original": True
        })
    
    # Handle status changes
    elif payload["callback_id"].startswith("change_status_"):
        task_id = int(payload["callback_id"].split("_")[-1])
        action = payload["actions"][0]
        status_data = json.loads(action["value"])
        
        task = Task.query.get(task_id)
        if task:
            old_status = task.status
            task.status = status_data["status"]
            db.session.commit()
            
            status_emoji = {
                "done": "✅",
                "no": "❌",
                "in progress": "🔄"
            }.get(task.status, "❓")
            
            return jsonify({
                "response_type": "in_channel",
                "text": f"{status_emoji} <@{user_id}> changed task status: \"{task.task_description}\" → *{task.status}*",
                "replace_original": False
            })
    
    return jsonify({"text": "Action completed"})

def open_task_creation_modal(user_id):
    """Open modal for task creation"""
    try:
        modal_view = {
            "type": "modal",
            "callback_id": "create_task_modal",
            "title": {
                "type": "plain_text",
                "text": "Создать задачу",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Создать",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Отмена",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "input",
                    "block_id": "task_description",
                    "label": {
                        "type": "plain_text",
                        "text": "Описание задачи",
                        "emoji": True
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "task_input",
                        "multiline": True,
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Опишите задачу..."
                        }
                    }
                },
                {
                    "type": "input",
                    "block_id": "assigned_to",
                    "label": {
                        "type": "plain_text",
                        "text": "Назначить на",
                        "emoji": True
                    },
                    "element": {
                        "type": "static_select",
                        "action_id": "assignee_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Выберите участника",
                            "emoji": True
                        },
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": member,
                                    "emoji": True
                                },
                                "value": member
                            } for member in TEAM_MEMBERS
                        ]
                    }
                }
            ]
        }
        
        response = requests.post(
            f"{SLACK_API_BASE}/views.open",
            headers={
                "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "trigger_id": user_id,  # This should be the actual trigger_id
                "view": modal_view
            }
        )
        
        return response.json()
    except Exception as e:
        print(f"Error opening modal: {e}")
        return jsonify({"text": "Error opening modal"})

def update_home_tab(user_id, channel_id=None):
    """Update the home tab for a user with their tasks"""
    try:
        # Get tasks for the user
        if channel_id:
            tasks = Task.query.filter_by(channel_id=channel_id).order_by(Task.created_at.desc()).all()
        else:
            # Get all tasks assigned to this user
            tasks = Task.query.filter_by(assigned_to=user_id).order_by(Task.created_at.desc()).all()
        
        # Create blocks for the home tab
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📋 Task Manager",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Управляйте задачами прямо здесь!"
                }
            },
            {
                "type": "divider"
            }
        ]
        
        if tasks:
            for task in tasks:
                status_emoji = {
                    "done": "✅",
                    "no": "❌", 
                    "in progress": "🔄"
                }.get(task.status, "❓")
                
                task_block = {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{status_emoji} *{task.task_description}*\n"
                               f"📅 {task.created_at.strftime('%Y-%m-%d %H:%M')}\n"
                               f"👤 Назначено: {task.assigned_to}\n"
                               f"📊 Статус: {task.status}"
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Изменить статус",
                            "emoji": True
                        },
                        "value": json.dumps({"task_id": task.id, "action": "change_status"}),
                        "action_id": f"change_status_{task.id}"
                    }
                }
                blocks.append(task_block)
                blocks.append({"type": "divider"})
        else:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "🎉 У вас пока нет задач! Используйте `/addtask` для создания новой задачи."
                }
            })
        
        # Add action buttons
        blocks.extend([
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Создать задачу",
                            "emoji": True
                        },
                        "style": "primary",
                        "action_id": "create_task"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Обновить",
                            "emoji": True
                        },
                        "action_id": "refresh_tasks"
                    }
                ]
            }
        ])
        
        # Update the home tab
        response = requests.post(
            f"{SLACK_API_BASE}/views.publish",
            headers={
                "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "user_id": user_id,
                "view": {
                    "type": "home",
                    "blocks": blocks
                }
            }
        )
        
        return response.json()
    except Exception as e:
        print(f"Error updating home tab: {e}")
        return None

@slack_bp.route("/createtaskchannel", methods=["POST"])
def handle_createtaskchannel_command():
    """Handle /createtaskchannel slash command - creates a dedicated task channel"""
    if not verify_slack_request(request):
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.form
    user_id = data.get("user_id")
    channel_id = data.get("channel_id")
    
    # This would require additional Slack API calls to create a channel
    # For now, we'll provide instructions
    return jsonify({
        "response_type": "ephemeral",
        "text": "📋 *Создание канала для задач:*\n\n1. Создайте новый канал с названием `#tasks` или `#задачи`\n2. Добавьте туда всех участников команды\n3. Используйте команды `/addtask` и `/showlist` в этом канале\n\n*Преимущества:*\n• Все задачи в одном месте\n• Нет путаницы в общих чатах\n• Легко отслеживать прогресс"
    })

@slack_bp.route("/home", methods=["GET", "POST"])
def handle_home_tab():
    """Handle home tab events"""
    if request.method == "GET":
        return jsonify({"status": "ok", "message": "Home tab endpoint is working"})
    
    # For URL verification, we don't need to verify the request
    try:
        payload = json.loads(request.get_data(as_text=True))
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON"}), 400
    
    if payload["type"] == "url_verification":
        return jsonify({"challenge": payload["challenge"]})
    
    # For actual events, verify the request
    if not verify_slack_request(request):
        return jsonify({"error": "Unauthorized"}), 401
    
    if payload["type"] == "event_callback":
        event = payload["event"]
        
        if event["type"] == "app_home_opened":
            user_id = event["user"]
            update_home_tab(user_id)
    
    return jsonify({"status": "ok"})

@slack_bp.route("/test", methods=["GET"])
def test_endpoint():
    """Test endpoint to verify the bot is running"""
    return jsonify({
        "status": "success",
        "message": "Slack Task Assignment Bot is running",
        "team_members": TEAM_MEMBERS,
        "status_options": STATUS_OPTIONS
    })

@slack_bp.route("/events", methods=["GET", "POST"])
def handle_events():
    """Handle Slack events and URL verification"""
    if request.method == "GET":
        return jsonify({"status": "ok", "message": "Events endpoint is working"})
    
    # For URL verification, we don't need to verify the request
    try:
        payload = json.loads(request.get_data(as_text=True))
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON"}), 400
    
    if payload["type"] == "url_verification":
        return jsonify({"challenge": payload["challenge"]})
    
    # For actual events, verify the request
    if not verify_slack_request(request):
        return jsonify({"error": "Unauthorized"}), 401
    
    if payload["type"] == "event_callback":
        event = payload["event"]
        
        if event["type"] == "app_home_opened":
            user_id = event["user"]
            update_home_tab(user_id)
    
    return jsonify({"status": "ok"}) 