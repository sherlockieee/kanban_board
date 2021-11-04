from flask import json


def test_initialize_server(client):
    """test that server is running"""
    rv = client.get("/")
    assert rv.data == b"Server is running"


def test_get_all_tasks(client):
    """test that all data we insert in data.sql is in the database, in ascending order by id"""
    rv = client.get("/api/tasks")
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert data == [
        {"id": 3, "name": "task 3", "description": "Description 3", "type": "done"},
        {"id": 2, "name": "task 2", "description": "Description 2", "type": "doing"},
        {"id": 1, "name": "task 1", "description": "Description 1", "type": "to-do"},
    ]


def test_get_one_task(client):
    """test that we can get a specific task with id 1"""
    rv = client.get("/api/tasks/1")
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert data == {
        "id": 1,
        "name": "task 1",
        "description": "Description 1",
        "type": "to-do",
    }


def test_get_one_task_that_does_not_exist(client):
    """test that if we try to get a task that doesn't exist, it will return an error"""
    rv = client.get("/api/tasks/5")
    assert rv.status_code == 400


def test_create_task(client):
    """test that we can create a new task"""
    rv = client.post(
        "/api/tasks",
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


def test_create_wrong_task(client):
    """test that if the json is of the wrong format or doesn't exist, it will return a 400 error"""
    rv = client.post(
        "/api/tasks",
        json={
            "id": 4,
            "name": "task 4",
            "description": "Description 4",
            "type": "to-do",
        },
    )
    assert rv.status_code == 400
    rv = client.post("/api/tasks", json={})
    assert rv.status_code == 400


def test_update_task(client):
    """test that we can update a new task"""
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
    assert "task 1 - edited" in str(rv.data)
    assert "Description 1" not in str(rv.data)


def test_delete_task(client):
    """test that we can delete a new task"""
    rv = client.delete("/api/tasks/2")
    assert rv.status_code == 201
    assert "Task 2 deleted successfully" in str(rv.data)
