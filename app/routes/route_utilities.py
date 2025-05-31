from flask import abort, make_response
from ..db import db
from sqlalchemy.orm import Session

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
    model = db.session.get(cls, model_id)
    if model is None:
        abort(404, description=f"{cls.__name__} not found")
    return model

def send_slack_message_to_channel(message: str, channel: str):
    slack_token = os.environ.get('SLACK_BOT_TOKEN')
    if not slack_token:
        print("Slack token not found in environment variables.")
        return

    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json",
    }
    data = {
        "channel": channel,
        "text": message,
    }

    response = requests.post(url, headers=headers, json=data)
    if not response.ok:
        print(f"Error sending message to Slack: {response.text}")

def notify_task_completion(task):
    message = task.slack_completion_message()
    channel = "test-slack-api"
    send_slack_message_to_channel(message, channel)