"""Tests d'intégration minimalistes pour la base de données Neon."""

import logging
import os
import sys

# Configure logging for integration tests
logger = logging.getLogger(__name__)

# Vérifier que DATABASE_URL est définie
if not os.environ.get("DATABASE_URL"):
    raise ValueError(
        "DATABASE_URL environment variable must be set to run integration tests"
    )

# Import the app directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from app import Todo, app, db


def test_neon_connection():
    """Test de connexion à la base de données Neon."""
    logger.info("Testing Neon database connection")
    with app.app_context():
        logger.info("Executing SELECT 1 query on Neon database")
        result = db.session.execute(db.text("SELECT 1")).scalar()
        logger.info(f"Query result: {result}")
        assert result == 1
        logger.info("✓ Neon database connection test passed")


def test_neon_crud_operations():
    """Test CRUD basique sur Neon PostgreSQL."""
    logger.info("Starting CRUD operations test on Neon PostgreSQL")
    with app.app_context():
        # Create
        logger.info("Creating new todo in Neon database")
        todo = Todo(title="Test Neon Integration")
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id
        logger.info(f"Todo created with ID: {todo_id}")

        # Read
        logger.info(f"Reading todo {todo_id} from Neon database")
        found = db.session.get(Todo, todo_id)
        logger.info(f"Found todo: '{found.title}', complete: {found.complete}")
        assert found.title == "Test Neon Integration"
        assert found.complete is False

        # Update
        logger.info(f"Updating todo {todo_id} to complete")
        found.complete = True
        db.session.commit()

        updated = db.session.get(Todo, todo_id)
        logger.info(f"Updated todo complete status: {updated.complete}")
        assert updated.complete is True

        # Delete
        logger.info(f"Deleting todo {todo_id} from Neon database")
        db.session.delete(updated)
        db.session.commit()

        deleted = db.session.get(Todo, todo_id)
        logger.info(f"Todo after deletion: {deleted}")
        assert deleted is None
        logger.info("✓ CRUD operations test completed successfully")
