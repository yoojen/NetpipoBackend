
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id: Mapped[int] = mapped_column(
        autoincrement=True, primary_key=True, unique=True)
    email: Mapped[str] = mapped_column(String(40), unique=True)
    password: Mapped[str] = mapped_column(String(256))

    def create_user_pass_hash(self):
        self.password = generate_password_hash(password=self.password)

    def check_user_pass_hash(self, plain_password):
        return check_password_hash(self.password, plain_password)

    @staticmethod
    def find_existing_email(email):
        return db.session.query(User).filter_by(email=email).first()

    @staticmethod
    def find_user(id):
        """Helper to find user in the db"""
        user = db.session.query(User).filter_by(id=id).first()
        return user


class Employee(db.Model):
    id: Mapped[int] = mapped_column(
        unique=True, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(40))
    email: Mapped[str] = mapped_column(String(40), unique=True)
    salary:  Mapped[int]

    def __repr__(self):
        return f"<Employee {self.name}>"

    @staticmethod
    def find_existing_email(email):
        """Helper to find user in the db"""
        employee = db.session.query(Employee).filter_by(email=email).first()
        return employee

    @staticmethod
    def find_employee(id):
        """Helper to find user in the db"""
        employee = db.session.get(Employee, id)
        return employee
