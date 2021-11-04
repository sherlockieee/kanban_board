import os
from flask import Flask, request, abort, flash, jsonify, json
from kanban.db import init_app, get_db


def create_app(cfg=None):
    app = Flask(__name__)  # create the application instance :)
    app.config.from_mapping(
        DEBUG=True,
        DEVELOPMENT=True,
        SECRET_KEY="development key",
        DATABASE=os.path.join(app.root_path, "kanban.db"),
    )  # load config
    if cfg:
        app.config.update(cfg)  # update config as necessary

    init_app(app)

    @app.route("/")
    def hello_world():
        """Initialize server"""
        return "Server is running"

    @app.route("/api/tasks", methods=["GET"])
    def get_tasks():
        """get all tasks"""
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

    @app.route("/api/tasks", methods=["POST"])
    def add_task():
        """add a single task"""
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

    @app.route("/api/tasks/<task_id>", methods=["GET"])
    def get_task(task_id):
        """get a single task from task ID"""
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

    @app.route("/api/tasks/<task_id>", methods=["DELETE"])
    def delete_task(task_id):
        """delete task of task id from database"""
        database = get_db()
        database.execute(
            "DELETE FROM tasks WHERE id=?",
            task_id,
        )
        database.commit()
        flash("Task deleted")
        return jsonify({"message": f"Task {task_id} deleted successfully"}), 201

    @app.route("/api/tasks/<task_id>", methods=["PUT"])
    def update_task(task_id):
        """update task with new data"""
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


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
