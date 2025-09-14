"""Tests unitaires pour l'application Flask Todo."""

import logging

from flask import Flask
from flask.testing import FlaskClient

from app import Todo, db

# Configure logging for tests
logger = logging.getLogger(__name__)


def test_home_route(client: FlaskClient) -> None:
    """Test the home route returns 200."""
    logger.info("Testing home route accessibility")
    response = client.get("/")
    logger.info(f"Home route returned status code: {response.status_code}")
    assert response.status_code == 200
    logger.info("✓ Home route test passed")


def test_add_todo(client: FlaskClient) -> None:
    """Test adding a new todo."""
    logger.info("Testing todo addition functionality")
    response = client.post("/add", data={"title": "Test Todo"})
    logger.info(f"Add todo POST request returned status: {response.status_code}")
    assert response.status_code == 302  # Redirect after POST

    # Verify todo was added
    with client.application.app_context():
        todo = Todo.query.filter_by(title="Test Todo").first()
        logger.info(f"Retrieved todo from database: {todo.title if todo else 'None'}")
        assert todo is not None
        assert todo.complete is False
        logger.info(f"✓ Todo '{todo.title}' successfully added with ID: {todo.id}")


def test_update_todo(client: FlaskClient) -> None:
    """Test updating a todo's completion status."""
    logger.info("Testing todo update functionality")
    # First add a todo
    with client.application.app_context():
        todo = Todo(title="Test Todo", complete=False)
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id
        logger.info(f"Created test todo with ID: {todo_id}")

    # Update the todo
    logger.info(f"Attempting to update todo {todo_id}")
    response = client.get(f"/update/{todo_id}")
    logger.info(f"Update request returned status: {response.status_code}")
    assert response.status_code == 302

    # Verify todo was updated
    with client.application.app_context():
        updated_todo = db.session.get(Todo, todo_id)
        assert updated_todo is not None
        assert updated_todo.complete is True
        logger.info(
            f"✓ Todo {todo_id} successfully updated to complete: "
            f"{updated_todo.complete}"
        )


def test_delete_todo(client: FlaskClient) -> None:
    """Test deleting a todo."""
    logger.info("Testing todo deletion functionality")
    # First add a todo
    with client.application.app_context():
        todo = Todo(title="Test Todo", complete=False)
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id
        logger.info(f"Created test todo with ID: {todo_id} for deletion test")

    # Delete the todo
    logger.info(f"Attempting to delete todo {todo_id}")
    response = client.get(f"/delete/{todo_id}")
    logger.info(f"Delete request returned status: {response.status_code}")
    assert response.status_code == 302

    # Verify todo was deleted
    with client.application.app_context():
        deleted_todo = db.session.get(Todo, todo_id)
        logger.info(f"Todo {todo_id} after deletion: {deleted_todo}")
        assert deleted_todo is None
        logger.info(f"✓ Todo {todo_id} successfully deleted")


def test_todo_model(app_context: Flask) -> None:
    """Test the Todo model."""
    logger.info("Testing Todo model functionality")
    todo = Todo(title="Test Model", complete=False)
    logger.info(f"Created todo model: '{todo.title}'")
    db.session.add(todo)
    db.session.commit()
    logger.info(f"Todo model saved with ID: {todo.id}")

    assert todo.id is not None
    assert todo.title == "Test Model"
    assert todo.complete is False
    logger.info("✓ Todo model test passed - all attributes verified")
