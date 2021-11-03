from flask import json, jsonify


def test_initialize_database(client):
    rv = client.get("/")
    assert rv.data == b"Server is running"


def test_get_all_tasks(client):
    rv = client.get("/api/tasks")
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert data == [
        {"id": 3, "name": "task 3", "description": "Description 3", "type": "done"},
        {"id": 2, "name": "task 2", "description": "Description 2", "type": "doing"},
        {"id": 1, "name": "task 1", "description": "Description 1", "type": "to-do"},
    ]


def test_get_one_task(client):
    rv = client.get("/api/tasks/1")
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert data == {
        "id": 1,
        "name": "task 1",
        "description": "Description 1",
        "type": "to-do",
    }


def test_create_task(client):
    rv = client.post(
        "/api/tasks/add",
        json={
            "task": {
                "id": 4,
                "name": "task 4",
                "description": "Description 4",
                "type": "to-do",
            }
        },
    )
    assert rv.status_code == 201
    assert "Task added successfully" in str(rv.data)


def test_update_task(client):
    rv = client.put(
        "/api/tasks/1",
        json={
            "id": 1,
            "name": "task 1 - edited",
            "description": "a new description",
            "type": "to-do",
        },
    )
    assert rv.status_code == 201
    assert "task 1 - edited" in rv.data
    assert "Description 1" not in rv.data


def test_delete_task(client):
    rv = client.delete("/api/tasks/2")
    assert rv.status_code == 201
    assert "task 2" not in rv.data
    assert "description 2" not in rv.data
