from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
# from .task import Task

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def __init__(self, title: str):
        self.title = title

    def to_dict(self):
        goal_as_dict = {
            "id": self.id,
            "title": self.title,
        }
        return goal_as_dict

    def to_dict_with_tasks(self):
        goal_as_dict = self.to_dict()
        goal_as_dict["tasks"] = [task.to_dict() for task in self.tasks]
        return goal_as_dict

    @classmethod
    def from_dict(cls, goal_data):
        return Goal(title=goal_data["title"])
