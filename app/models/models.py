"""Database models for the Todo application."""

from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()


class Todo(db.Model):
    """Todo model for storing todo items."""

    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        """String representation of Todo object."""
        return f"<Todo {self.id}: {self.title}>"