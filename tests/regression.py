"""Tests de non-régression minimalistes pour l'application Todo."""

import logging

from flask.testing import FlaskClient

from app import Todo, db

logger = logging.getLogger(__name__)


def test_health_endpoint_format_regression(client: FlaskClient) -> None:
    """RÉGRESSION: Format de réponse du health check (pour monitoring/CI)."""
    logger.info("Testing health endpoint format for regression")
    response = client.get("/health")
    logger.info(f"Health endpoint returned status: {response.status_code}")
    assert response.status_code == 200
    assert response.is_json
    assert "status" in response.json
    assert response.json["status"] == "healthy"
    logger.info("✓ Health endpoint format regression test passed")


def test_app_serves_html_content(client: FlaskClient) -> None:
    """RÉGRESSION: L'app sert bien du contenu HTML (pas JSON par erreur)."""
    logger.info("Testing app serves HTML content regression")
    response = client.get("/")
    logger.info(
        f"Home route returned status: {response.status_code}, "
        f"content-type: {response.content_type}"
    )
    assert response.status_code == 200
    assert "text/html" in response.content_type
    assert b"<html" in response.data or b"<!DOCTYPE" in response.data
    logger.info("✓ App serves HTML content regression test passed")


def test_database_schema_compatibility(client: FlaskClient) -> None:
    """RÉGRESSION: La structure de la DB reste compatible."""
    logger.info("Testing database schema compatibility regression")
    with client.application.app_context():
        # Vérifier que les colonnes essentielles existent
        logger.info("Executing schema validation query")
        result = db.session.execute(
            db.text("SELECT id, title, complete FROM todos LIMIT 0")
        )
        # Si cette requête passe, le schéma est OK
        logger.info("Schema validation query executed successfully")
        assert result is not None
        logger.info("✓ Database schema compatibility regression test passed")


def test_todo_workflow_end_to_end(client: FlaskClient) -> None:
    """RÉGRESSION: Workflow complet en une seule transaction."""
    logger.info("Testing end-to-end todo workflow regression")
    # Test rapide du workflow complet pour détecter les régressions d'intégration
    logger.info("Creating todo for E2E test")
    client.post("/add", data={"title": "E2E Test"})

    with client.application.app_context():
        todo = Todo.query.filter_by(title="E2E Test").first()
        todo_id = todo.id
        logger.info(f"Created todo with ID: {todo_id}")

    # Update puis delete en chaîne
    logger.info(f"Updating todo {todo_id}")
    client.get(f"/update/{todo_id}")
    logger.info(f"Deleting todo {todo_id}")
    client.get(f"/delete/{todo_id}")

    # Vérifier que tout est nettoyé
    with client.application.app_context():
        deleted_todo = db.session.get(Todo, todo_id)
        logger.info(f"Todo {todo_id} after E2E workflow: {deleted_todo}")
        assert deleted_todo is None
        logger.info("✓ End-to-end workflow regression test passed")


def test_empty_title_edge_case(client: FlaskClient) -> None:
    """RÉGRESSION: Gestion des titres vides/espaces."""
    logger.info("Testing empty title edge case regression")
    initial_count = Todo.query.count() if hasattr(Todo, "query") else 0
    logger.info(f"Initial todo count: {initial_count}")

    # Tester différents cas de titres vides
    empty_titles = ["", "   ", "\t", "\n"]
    logger.info(f"Testing {len(empty_titles)} empty title variations")
    for empty_title in empty_titles:
        client.post("/add", data={"title": empty_title})

    with client.application.app_context():
        final_count = Todo.query.count()
        logger.info(f"Final todo count after empty title tests: {final_count}")
        # Aucun todo vide ne devrait être créé
        assert final_count == initial_count
        logger.info("✓ Empty title edge case regression test passed")
