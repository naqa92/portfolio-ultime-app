import logging
import os

from flask import (
    Flask,
    Response,
    jsonify,
    render_template,
    request,
)

from models.models import db, Todo

# Create Flask app
app = Flask(__name__)

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///todos.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database with the app
db.init_app(app)

# Create tables if they don't exist (SQLite only - PostgreSQL uses Atlas migrations)
if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
    with app.app_context():
        db.create_all()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
app.logger.info("Using database: %s", app.config["SQLALCHEMY_DATABASE_URI"])


# Define routes
@app.route("/health", methods=["GET"]) # Endpoint pour les Probes
def health() -> Response:
    """Liveness and Readiness probe endpoints."""
    return jsonify({"status": "healthy"}), 200

@app.route("/", methods=["GET"])
def home() -> str:
    """Home page displaying all todos."""
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add() -> str:
    """Add a new todo item."""
    title = request.form.get("title", "").strip()  # Strip whitespace
    if title:
        new_todo = Todo(title=title)
        db.session.add(new_todo)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.error("Error committing to DB: %s", e)
            db.session.rollback()
    
    todo_list = Todo.query.all()
    return render_template("todo_list.html", todo_list=todo_list)


@app.route("/update/<int:todo_id>", methods=["PUT"])
def update(todo_id: int) -> str:
    """Update a todo item's completion status."""
    todo = db.get_or_404(Todo, todo_id)
    todo.complete = not todo.complete
    try:
        db.session.commit()
    except Exception as e:
        app.logger.error("Error committing to DB: %s", e)
        db.session.rollback()
    
    todo_list = Todo.query.all()
    return render_template("todo_list.html", todo_list=todo_list)


@app.route("/delete/<int:todo_id>", methods=["DELETE"])
def delete(todo_id: int) -> str:
    """Delete a todo item."""
    todo = db.get_or_404(Todo, todo_id)
    db.session.delete(todo)
    try:
        db.session.commit()
    except Exception as e:
        app.logger.error("Error committing to DB: %s", e)
        db.session.rollback()
    
    todo_list = Todo.query.all()
    return render_template("todo_list.html", todo_list=todo_list)


# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0")
