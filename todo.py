from src.models.user import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_description = db.Column(db.Text, nullable=False)
    assigned_to = db.Column(db.String(50), nullable=False)  # David, Emma, Nora, Eric, Kenny
    status = db.Column(db.String(20), default='no', nullable=False)  # done, no, in progress
    channel_id = db.Column(db.String(100), nullable=False)
    dispatcher_id = db.Column(db.String(100), nullable=False)  # User who created the task
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Task {self.id}: {self.task_description[:50]} -> {self.assigned_to}>'

    def to_dict(self):
        return {
            'id': self.id,
            'task_description': self.task_description,
            'assigned_to': self.assigned_to,
            'status': self.status,
            'channel_id': self.channel_id,
            'dispatcher_id': self.dispatcher_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }

