import os
import requests
from datetime import datetime, timezone
from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from .route_utilities import validate_model
from ..db import db


bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def send_slack_message(task_title):
    slack_token = os.environ.get('SLACK_BOT_TOKEN')
    slack_channel = 'test-slack-api'  # Channel name in Slack
    slack_message = f"Jamie just completed the task {task_title}"

    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json",
    }
    data = {
        "channel": slack_channel,
        "text": slack_message,
    }

    response = requests.post(url, headers=headers, json=data)
    
    if not response.ok:
        print(f"Error sending message to Slack: {response.text}")

@bp.post("")
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
        
    except KeyError as error:
        response = {"details": "Invalid data"}
        abort (make_response(response, 400))
        
    db.session.add(new_task)
    db.session.commit()
    
    return {"task": new_task.to_dict()}, 201

@bp.get("")
def get_all_tasks():
    query = db.select(Task)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))

    sort_param = request.args.get("sort")
    if sort_param == "asc":
        query = query.order_by(Task.title.asc())
    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.title)

    tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return tasks_response

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return {"task": task.to_dict()}

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at", None)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    if isinstance(task, dict):
        return task
    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()

    send_slack_message(task.title)
    
    return make_response("", 204)

@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    if isinstance(task, dict):
        return task
    task.completed_at = None
    db.session.commit()
    return make_response("", 204)