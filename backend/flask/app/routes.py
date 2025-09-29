from datetime import datetime
from typing import Any, Dict
from flask import Blueprint, request, jsonify, abort
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from .db import SessionLocal
from .models import Task, Priority

api_bp = Blueprint("api", __name__)

def task_to_dict(t: Task) -> Dict[str, Any]:
    return {
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "due_date": t.due_date.isoformat() if t.due_date else None,
        "completed": t.completed,
        "priority": {"id": t.priority.id, "name": t.priority.name, "rank": t.priority.rank} if t.priority else None,
        "created_at": t.created_at.isoformat(),
        "updated_at": t.updated_at.isoformat(),
    }

@api_bp.get("/priorities")
def get_priorities():
    db = SessionLocal()
    try:
        rows = db.execute(select(Priority).order_by(Priority.rank)).scalars().all()
        return jsonify([{"id": p.id, "name": p.name, "rank": p.rank} for p in rows])
    finally:
        db.close()

@api_bp.get("/tasks")
def list_tasks():
    db = SessionLocal()
    try:
        q = select(Task).options(joinedload(Task.priority))
        search = request.args.get("search")
        priority_id = request.args.get("priority")
        completed = request.args.get("completed")
        page = int(request.args.get("page", "1"))
        page_size = min(100, int(request.args.get("page_size", "20")))
        if search:
            like = f"%{search}%"
            q = q.where(func.lower(Task.title).like(func.lower(like)))
        if priority_id:
            try:
                pid = int(priority_id)
                q = q.where(Task.priority_id == pid)
            except ValueError:
                pass
        if completed is not None:
            if completed.lower() in ("true", "1"):
                q = q.where(Task.completed.is_(True))
            if completed.lower() in ("false", "0"):
                q = q.where(Task.completed.is_(False))
        total = db.execute(q.with_only_columns(func.count())).scalar_one()
        q = q.order_by(Task.completed.asc(), Task.due_date.is_(True), Task.due_date.asc().nulls_last(), Task.created_at.desc())
        items = db.execute(q.limit(page_size).offset((page - 1) * page_size)).scalars().all()
        return jsonify({
            "items": [task_to_dict(t) for t in items],
            "page": page,
            "page_size": page_size,
            "total": total,
        })
    finally:
        db.close()

@api_bp.post("/tasks")
def create_task():
    data = request.get_json(force=True, silent=True) or {}
    title = data.get("title")
    if not title or not isinstance(title, str):
        abort(400, description="title is required")
    db = SessionLocal()
    try:
        t = Task(
            title=title.strip(),
            description=data.get("description"),
            due_date=datetime.fromisoformat(data["due_date"]).date() if data.get("due_date") else None,
            completed=bool(data.get("completed", False)),
            priority_id=int(data["priority_id"]) if data.get("priority_id") else None,
        )
        db.add(t)
        db.commit()
        db.refresh(t)
        return jsonify(task_to_dict(t)), 201
    finally:
        db.close()

@api_bp.patch("/tasks/<int:task_id>")
def update_task(task_id: int):
    data = request.get_json(force=True, silent=True) or {}
    db = SessionLocal()
    try:
        t = db.get(Task, task_id)
        if not t:
            abort(404)
        if "title" in data and isinstance(data["title"], str):
            t.title = data["title"].strip()
        if "description" in data:
            t.description = data["description"]
        if "due_date" in data:
            t.due_date = datetime.fromisoformat(data["due_date"]).date() if data["due_date"] else None
        if "completed" in data:
            t.completed = bool(data["completed"])
        if "priority_id" in data:
            t.priority_id = int(data["priority_id"]) if data["priority_id"] else None
        db.commit()
        db.refresh(t)
        return jsonify(task_to_dict(t))
    finally:
        db.close()

@api_bp.delete("/tasks/<int:task_id>")
def delete_task(task_id: int):
    db = SessionLocal()
    try:
        t = db.get(Task, task_id)
        if not t:
            abort(404)
        db.delete(t)
        db.commit()
        return "", 204
    finally:
        db.close()
