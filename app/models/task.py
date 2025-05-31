from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from .goal import Goal

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    completed_at: Mapped[Optional[datetime]] = mapped_column()
    goal_id: Mapped[Optional[int]] = mapped_column(db.ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def is_complete(self):
        return self.completed_at is not None

    def slack_completion_message(self):
        return f"Jamie just completed the task: {self.title}"

    def to_dict(self):
        task_as_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete()
        }

        if self.goal_id is not None:
            task_as_dict["goal_id"] = self.goal_id

        return task_as_dict

    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data.get("completed_at"),
            goal_id=task_data.get("goal_id")
        )
        return new_task