import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from app.models import task
from app.models.task import Task
from app.db import db
import pytest


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_mark_complete_on_incomplete_task(client, one_task):
    # Arrange
    """
    The future Wave 4 adds special functionality to this route,
    so for this test, we need to set-up "mocking."

    Mocking will help our tests work in isolation, which is a
    good thing!

    We need to mock any POST requests that may occur during this
    test (due to Wave 4).

    There is no action needed here, the tests should work as-is.
    """
    with patch("requests.post") as mock_get:
        mock_get.return_value.status_code = 200

        # Act
        response = client.patch("/tasks/1/mark_complete")

    # Assert
    assert response.status_code == 204

    query = db.select(Task).where(Task.id == one_task.id)
    assert db.session.scalar(query).completed_at


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_mark_incomplete_on_complete_task(client, completed_task):
    task_id = completed_task.id

    # Act
    response = client.patch("/tasks/1/mark_incomplete")


    # Assert
    assert response.status_code == 204

    query = db.select(Task).where(Task.id == task_id)
    task_in_db = db.session.scalar(query)
    assert task_in_db.completed_at is None


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_mark_complete_on_completed_task(client, completed_task):
    # Arrange
    """
    The future Wave 4 adds special functionality to this route,
    so for this test, we need to set-up "mocking."

    Mocking will help our tests work in isolation, which is a
    good thing!

    We need to mock any POST requests that may occur during this
    test (due to Wave 4).

    There is no action needed here, the tests should work as-is.
    """
    with patch("requests.post") as mock_get:
        mock_get.return_value.status_code = 200

        # Act
        response = client.patch("/tasks/1/mark_complete")

    # Assert
    assert response.status_code == 204

    query = db.select(Task).where(Task.id == completed_task.id)
    assert db.session.scalar(query).completed_at is not None

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_mark_incomplete_on_incomplete_task(client, one_task):
    task_id = one_task.id

    # Act
    response = client.patch("/tasks/1/mark_incomplete")

    # Assert
    assert response.status_code == 204

    query = db.select(Task).where(Task.id == task_id)
    task_in_db = db.session.scalar(query)
    assert task_in_db.completed_at is None


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_mark_complete_missing_task(client):
    # Act
    response = client.patch("/tasks/1/mark_complete")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {'message': 'Task not found'}


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_mark_incomplete_missing_task(client):
    # Act
    response = client.patch("/tasks/1/mark_incomplete")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {'message': 'Task not found'}