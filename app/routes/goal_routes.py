from flask import Blueprint, abort, make_response, request, Response
from app.models.goal import Goal
from .route_utilities import validate_model, get_model_by_id
from ..db import db

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@bp.post("")
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"}, 400)

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201

@bp.get("")
def get_all_goals():
    query = db.select(Goal)
    goals = db.session.scalars(query).all()

    goals_response = [goal.to_dict() for goal in goals]
    return goals_response

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = get_model_by_id(Goal, goal_id)
    return {"goal": goal.to_dict_with_tasks()}

@bp.post("/<goal_id>/tasks")
def assign_tasks_to_goal(goal_id):
    from app.models.task import Task

    goal = get_model_by_id(Goal, goal_id)

    request_data = request.get_json()
    task_ids = request_data.get("task_ids")

    if not task_ids or not isinstance(task_ids, list):
        return make_response({"details": "task_ids must be a list of integers."}, 400)

    tasks = [get_model_by_id(Task, task_id) for task_id in task_ids]

    goal.tasks = tasks
    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": [task.id for task in tasks]
    }, 200

@bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = get_model_by_id(Goal, goal_id)
    return goal.to_dict_with_tasks(), 200