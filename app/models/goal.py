from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def to_dict(self):
        goal_as_dict = {
            "id": self.id,
            "title": self.title,
        }
        return goal_as_dict

    @classmethod
    def from_dict(cls, goal_data):
        return Goal(title=goal_data["title"])
