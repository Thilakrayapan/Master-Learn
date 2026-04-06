"""PeakPulse — Flask Application Entry Point"""

import os
from datetime import datetime, timezone, date, timedelta
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from models import db, Task, StudySession, check_deadlines
from punishments import get_punishment, get_all_punishments, get_level_for_count


# ─── App Factory ────────────────────────────────────────────────────
app = Flask(__name__)
app.config["SECRET_KEY"] = "peakpulse-secret-2026"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///peakpulse.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# ─── Context Processor ─────────────────────────────────────────────
@app.context_processor
def inject_now():
    return {"now": datetime.now(timezone.utc)}


# ─── Page Routes ────────────────────────────────────────────────────
@app.route("/")
def index():
    """Home page — task list."""
    check_deadlines()
    tasks = Task.query.order_by(Task.deadline.asc()).all()
    return render_template("index.html", tasks=tasks)


@app.route("/timer")
def timer():
    """Study timer page."""
    pending_tasks = Task.query.filter_by(status="pending").order_by(Task.deadline.asc()).all()
    today = date.today()
    today_sessions = StudySession.query.filter_by(date=today).all()
    total_today = sum(s.duration for s in today_sessions)
    return render_template("timer.html", tasks=pending_tasks, total_today=total_today)


@app.route("/dashboard")
def dashboard():
    """Dashboard page."""
    check_deadlines()
    return render_template("dashboard.html")


# ─── Task CRUD ──────────────────────────────────────────────────────
@app.route("/add", methods=["POST"])
def add_task():
    """Add a new task."""
    title = request.form.get("title", "").strip()
    deadline_str = request.form.get("deadline", "")

    if not title or not deadline_str:
        flash("Please fill in both the task title and deadline.", "error")
        return redirect(url_for("index"))

    try:
        deadline = datetime.fromisoformat(deadline_str).replace(tzinfo=timezone.utc)
    except ValueError:
        flash("Invalid deadline format.", "error")
        return redirect(url_for("index"))

    task = Task(title=title, deadline=deadline)
    db.session.add(task)
    db.session.commit()
    flash(f"Task '{title}' added! 🎯", "success")
    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    """Mark a task as completed."""
    task = Task.query.get_or_404(task_id)
    task.status = "completed"
    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()
    flash(f"Task '{task.title}' completed! 🎉", "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    """Delete a task."""
    task = Task.query.get_or_404(task_id)
    title = task.title
    db.session.delete(task)
    db.session.commit()
    flash(f"Task '{title}' deleted.", "info")
    return redirect(url_for("index"))


# ─── API Endpoints ──────────────────────────────────────────────────
@app.route("/api/tasks")
def api_tasks():
    """JSON list of all tasks."""
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks])


@app.route("/api/stats")
def api_stats():
    """Dashboard statistics."""
    check_deadlines()
    total = Task.query.count()
    completed = Task.query.filter_by(status="completed").count()
    missed = Task.query.filter_by(status="missed").count()
    pending = Task.query.filter_by(status="pending").count()
    rate = round((completed / total * 100), 1) if total > 0 else 0

    # Study data for the last 7 days
    today = date.today()
    study_data = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        sessions = StudySession.query.filter_by(date=d).all()
        total_mins = sum(s.duration for s in sessions) / 60
        study_data.append({"date": d.strftime("%a"), "minutes": round(total_mins, 1)})

    # Tasks completed per day (last 7 days)
    completion_data = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        d_start = datetime(d.year, d.month, d.day, tzinfo=timezone.utc)
        d_end = d_start + timedelta(days=1)
        count = Task.query.filter(
            Task.status == "completed",
            Task.completed_at >= d_start,
            Task.completed_at < d_end,
        ).count()
        completion_data.append({"date": d.strftime("%a"), "count": count})

    # Recent punishments
    punished = Task.query.filter(Task.punishment.isnot(None)).order_by(Task.id.desc()).limit(5).all()
    punishment_list = [{"title": t.title, "punishment": t.punishment} for t in punished]

    return jsonify({
        "total": total,
        "completed": completed,
        "missed": missed,
        "pending": pending,
        "rate": rate,
        "study_data": study_data,
        "completion_data": completion_data,
        "punishments": punishment_list,
        "missed_level": get_level_for_count(missed),
    })


@app.route("/api/timer/save", methods=["POST"])
def save_timer():
    """Save a study session from the timer."""
    data = request.get_json()
    if not data or "duration" not in data:
        return jsonify({"error": "Duration is required"}), 400

    duration = int(data["duration"])
    if duration < 1:
        return jsonify({"error": "Duration must be at least 1 second"}), 400

    task_id = data.get("task_id")
    if task_id == "" or task_id == "null" or task_id is None:
        task_id = None
    else:
        task_id = int(task_id)

    session = StudySession(
        task_id=task_id,
        duration=duration,
        date=date.today(),
    )
    db.session.add(session)
    db.session.commit()

    return jsonify({"success": True, "session": session.to_dict()})


# ─── Run ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
