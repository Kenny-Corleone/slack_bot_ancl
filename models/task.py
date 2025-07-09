from datetime import datetime
from database import db

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    task_description = db.Column(db.String(500), nullable=False)
    assigned_to = db.Column(db.String(100), nullable=False)
    channel_id = db.Column(db.String(100), nullable=False)
    dispatcher_id = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='no')  # 'done', 'no', 'in progress'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Task {self.id}: {self.task_description} assigned to {self.assigned_to}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'task_description': self.task_description,
            'assigned_to': self.assigned_to,
            'channel_id': self.channel_id,
            'dispatcher_id': self.dispatcher_id,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 