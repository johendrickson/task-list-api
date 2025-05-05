import os
import requests
from flask import Blueprint, abort, make_response, request, Response
from app.models.goal import Goal
from .route_utilities import validate_model
from ..db import db

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

from flask import Blueprint, request, abort, make_response, Response
from app.models.goal import Goal
from .route_utilities import validate_model
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

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}

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
