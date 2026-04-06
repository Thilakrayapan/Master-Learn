"""PeakPulse — Database Models"""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):
    """A productivity task with deadline tracking."""

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending | completed | missed
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime, nullable=True)
    punishment = db.Column(db.Text, nullable=True)

    # Relationship
    study_sessions = db.relationship("StudySession", backref="task", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "punishment": self.punishment,
        }


class StudySession(db.Model):
    """A timed study session, optionally linked to a task."""

    __tablename__ = "study_sessions"

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=True)
    duration = db.Column(db.Integer, nullable=False)  # seconds
    date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date())
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "duration": self.duration,
            "date": self.date.isoformat() if self.date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


def check_deadlines():
    """Scan all pending tasks — mark overdue ones as missed and assign punishments."""
    from punishments import get_punishment

    now = datetime.now(timezone.utc)
    overdue = Task.query.filter(Task.status == "pending", Task.deadline < now).all()

    if overdue:
        # Count total missed (existing + new)
        existing_missed = Task.query.filter(Task.status == "missed").count()
        for i, task in enumerate(overdue):
            task.status = "missed"
            task.punishment = get_punishment(existing_missed + i + 1)
        db.session.commit()

    return len(overdue)
