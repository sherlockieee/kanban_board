import os
from flask import Flask, request, g, abort, flash, jsonify, current_app
from flask.cli import with_appcontext
import json
import sqlite3
import click


def create_app(cfg=None):
    app = Flask(__name__)  # create the application instance :)
    app.config.from_mapping(
        DEBUG=True,
        DEVELOPMENT=True,
        SECRET_KEY="development key",
        DATABASE=os.path.join(app.root_path, "kanban.db"),
    )  # load config from this file
    if cfg:
        app.config.update(cfg)

    init_app(app)

    @app.route("/")
    def hello_world():
        return "Server is running"

    @app.route("/api/tasks", methods=["GET"])
    def get_tasks():
        database = get_db()
        cur = database.execute(
            "SELECT id, name, description, type FROM tasks ORDER BY id DESC"
        )
        tasks = cur.fetchall()
        result = []
        for task_id, name, description, type in tasks:
            task_obj = {
                "id": task_id,
                "name": name,
                "description": description,
                "type": type,
            }
            result.append(task_obj)
        return json.dumps(result)

    @app.route("/api/tasks/add", methods=["POST"])
    def add_task():
        if not request.json or not "task" in request.json:
            abort(400)
        new_task = request.json["task"]
        database = get_db()
        database.execute(
            "insert into tasks (name, description, type) values (?, ?, ?)",
            [new_task["name"], new_task["description"], new_task["type"]],
        )
        database.commit()
        flash("New entry was successfully posted")
        return jsonify({"message": "Task added successfully", "task": new_task}), 201

    @app.route("/api/tasks/<task_id>", methods=["GET", "DELETE", "PUT"])
    def task_function(task_id):
        if request.method == "GET":
            return get_task(task_id)
        elif request.method == "DELETE":
            return delete_task(task_id)
        elif request.method == "PUT":
            return update_task(task_id)

    def get_task(task_id):
        database = get_db()
        task = database.execute("SELECT * FROM tasks WHERE id =?", (task_id)).fetchone()
        if not task:
            abort(400)
        task_obj = {
            "id": task["id"],
            "name": task["name"],
            "description": task["description"],
            "type": task["type"],
        }
        return json.dumps(task_obj)

    def delete_task(task_id):
        database = get_db()
        database.execute(
            "DELETE FROM tasks WHERE id=?",
            task_id,
        )
        database.commit()
        flash("Task deleted")
        return jsonify({"message": f"Task {task_id} deleted successfully"}), 201

    def update_task(task_id):
        database = get_db()
        task = {
            "id": task_id,
            "name": request.json["name"],
            "description": request.json["description"],
            "type": request.json["type"],
        }
        database.execute(
            "UPDATE tasks SET name=?, description=?,type=? WHERE id=?",
            (task["name"], task["description"], task["type"], task["id"]),
        )
        database.commit()
        flash("Task updated")
        return (
            jsonify({"message": f"Task {task_id} updated successfully", "task": task}),
            201,
        )

    return app


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.sqlite_db.row_factory = sqlite3.Row

    return g.sqlite_db


def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()


@click.command("initdb")
@with_appcontext
def initdb_command():
    """Initializes the database."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(initdb_command)


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
