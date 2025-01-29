
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app import db


class Employee(db.Model):
    id: Mapped[int] = mapped_column(
        unique=True, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(40))
    email: Mapped[str] = mapped_column(String(40), unique=True)
    salary:  Mapped[int]

    def __repr__(self):
        return f"<Employee {self.name}>"
