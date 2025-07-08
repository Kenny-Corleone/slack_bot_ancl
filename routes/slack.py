from flask import Blueprint, request, jsonify
from models.task import Task
from app import db
import json
import hmac
import hashlib
import time
import os

slack_bp = Blueprint("slack", __name__)

# Slack credentials
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET", "e178377b1931850482d86a6920d7ef00")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "xoxb-9153598789972-9163840334662-quLu21epAVWYaDdAN11M3gOx")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN", "xapp-1-A094Z78RBN0-9180856017889-be5c3d466513ada2fbba58c60366f952527a4224aefa6bcd2be99e5bd71893dc")

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
        "response_type": "in_channel",
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

@slack_bp.route("/test", methods=["GET"])
def test_endpoint():
    """Test endpoint to verify the bot is running"""
    return jsonify({
        "status": "success",
        "message": "Slack Task Assignment Bot is running",
        "team_members": TEAM_MEMBERS,
        "status_options": STATUS_OPTIONS
    }) 