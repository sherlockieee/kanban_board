import os
import sqlite3
from flask import (
    Flask,
    request,
    g,
    abort,
    flash,
    jsonify,
)
import json

app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file


# Load default config and override config from an environment variable
app.config.update(
    dict(
        DATABASE=os.path.join(app.root_path, "kanban.db"),
        SECRET_KEY="development key",
    )
)
app.config.from_envvar("FLASKR_SETTINGS", silent=True)


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config["DATABASE"])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()
    with app.open_resource("schema.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command("initdb")
def initdb_command():
    """Initializes the database."""
    init_db()
    print("Initialized the database.")


@app.route("/")
def hello_world():
    return "Server is running"


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    db = get_db()
    cur = db.execute("select id, name, description, type from tasks order by id desc")
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
    db = get_db()
    db.execute(
        "insert into tasks (name, description, type) values (?, ?, ?)",
        [new_task["name"], new_task["description"], new_task["type"]],
    )
    db.commit()
    flash("New entry was successfully posted")
    return jsonify({"message": "Task added successfully"}), 201


@app.route("/api/tasks/<task_id>", methods=["DELETE", "PUT"])
def task_function(task_id):
    if request.method == "DELETE":
        return delete_task(task_id)
    elif request.method == "PUT":
        return update_task(task_id)


def delete_task(task_id):
    db = get_db()
    db.execute(
        "DELETE FROM tasks WHERE id=?",
        task_id,
    )
    db.commit()
    flash("Task deleted")
    return jsonify({"message": "Task deleted successfully"}), 201


def update_task(task_id):
    db = get_db()
    task = {
        "id": task_id,
        "name": request.json["name"],
        "description": request.json["description"],
        "type": request.json["type"],
    }
    db.execute(
        "UPDATE tasks SET name=?, description=?,type=? WHERE id=?",
        (task["name"], task["description"], task["type"], task["id"]),
    )
    db.commit()
    flash("Task updated")
    return jsonify({"message": "Task updated successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)
