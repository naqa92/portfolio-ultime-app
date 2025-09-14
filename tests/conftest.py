"""Fixtures pour tester l'application Flask."""

import os
import sys

import pytest

# Import the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from app import app as flask_app
from app import db as _db


@pytest.fixture(scope="session")
def app():
    """Create application for the tests."""
    # Use the test database URL from environment or fallback to in-memory SQLite
    test_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

    # Configure the app for testing
    flask_app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": test_DATABASE_URL,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "WTF_CSRF_ENABLED": False,  # Disable CSRF for testing
        }
    )

    # Create application context
    ctx = flask_app.app_context()
    ctx.push()

    yield flask_app

    ctx.pop()


@pytest.fixture(scope="session")
def db(app):
    """Create database for the tests."""
    _db.app = app

    # Create all tables
    _db.create_all()

    yield _db

    # Clean up
    _db.drop_all()


@pytest.fixture(scope="function")
def session(db):
    """Create a database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    # Create a scoped session tied to the connection
    from sqlalchemy.orm import scoped_session, sessionmaker

    session_factory = sessionmaker(bind=connection)
    session = scoped_session(session_factory)

    # Replace the db session with our test session
    db.session = session

    yield session

    # Clean up
    session.remove()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(app, session):
    """Create a test client for the Flask application."""
    return app.test_client()


@pytest.fixture(scope="function")
def app_context(app, session):
    """Provide application context for tests that need it."""
    with app.app_context():
        yield app
