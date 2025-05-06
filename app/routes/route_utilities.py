from flask import abort, make_response
from ..db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"message": f"Invalid request: invalid {cls.__name__} id"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)
    
    if not model:
        response = {"message": f"{cls.__name__} not found"}
        abort(make_response(response, 404))
    
    return model

def get_model_by_id(cls, model_id):
    model = cls.query.get(model_id)
    if model is None:
        abort(404, description=f"{cls.__name__} with id {model_id} not found")
    return model