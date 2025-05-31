from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from .task import Task

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def __init__(self, title: str):
        self.title = title

    def to_dict(self):
        goal_as_dict = {
            "id": self.id,
            "title": self.title,
        }
        return goal_as_dict

    @classmethod
    def from_dict(cls, goal_data):
        return Goal(title=goal_data["title"])
