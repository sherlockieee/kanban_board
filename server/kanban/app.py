import os
from flask import (
    Flask,
    request,
    g,
    abort,
    flash,
    jsonify,
)
import json
import db

def create_app(cfg = None):

    app = Flask(__name__)  # create the application instance :)
    app.config.from_mapping(
        DEBUG = True,
        DEVELOPMENT = True,
        SECRET_KEY = "development key",
        DATABASE=os.path.join(app.root_path, "kanban.db")
    )  # load config from this file
    if cfg:
        app.config.update(cfg)

    db.init_app(app)


    @app.route("/")
    def hello_world():
        return "Server is running"


    @app.route("/api/tasks", methods=["GET"])
    def get_tasks():
        database = db.get_db()
        cur = database.execute("SELECT id, name, description, type FROM tasks ORDER BY id DESC")
        tasks = cur.fetchall()
        result = []
        for task_id, name, description, type in tasks:
            task_obj = {
                "id": task_id,
                "name": name,
                "description": description,
                "type": type  
            }
            result.append(task_obj)
        return json.dumps(result)


    @app.route("/api/tasks/add", methods=["POST"])
    def add_task():
        if not request.json or not "task" in request.json:
            abort(400)
        new_task = request.json["task"]
        database = db.get_db()
        database.execute(
            "insert into tasks (name, description, type) values (?, ?, ?)",
            [new_task["name"], new_task["description"], new_task["type"]],
        )
        database.commit()
        flash("New entry was successfully posted")
        return jsonify({"message": "Task added successfully"}), 201


    @app.route("/api/tasks/<task_id>", methods=["GET", "DELETE", "PUT"])
    def task_function(task_id):
        if request.method == "GET":
            return get_task(task_id)
        elif request.method == "DELETE":
            return delete_task(task_id)
        elif request.method == "PUT":
            return update_task(task_id)

    def get_task(task_id):
        database = db.get_db()
        task = database.execute("SELECT * FROM tasks WHERE id =?", (task_id)).fetchone()
        if not task:
            abort(400)
        print(task["name"])
        task_obj = {
            "id": task["id"],
            "name": task["name"],
            "description": task["description"],
            "type": task["type"]  
        }
        return json.dumps(task_obj)

    def delete_task(task_id):
        database = db.get_db()
        database.execute(
            "DELETE FROM tasks WHERE id=?",
            task_id,
        )
        database.commit()
        flash("Task deleted")
        return jsonify({"message": "Task deleted successfully"}), 201


    def update_task(task_id):
        database = db.get_db()
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
        return jsonify({"message": "Task updated successfully"}), 201

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
