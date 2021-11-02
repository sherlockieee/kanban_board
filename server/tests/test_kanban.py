
def test_initialize_database(client):
    rv = client.get("/")
    assert rv.data == b"Server is running"

def test_get_all_tasks(client):
    rv = client.get("/api/tasks")
    assert rv.status_code == 200
    assert rv.json == [{"id": 1, "title": "task 1", "description": "Description 1", "type": "to-do"},
    {"id": 2, "title": "task 2", "description": "Description 2", "type": "doing"}, 
    {"id": 3, "title": "task 3", "description": "Description 3", "type": "done"}]

def test_get_one_task(client):
    rv = client.get("/api/tasks/1")
    assert rv.status_code == 200
    assert rv.json == {"id": 1, "title": "task 1", "description": "Description 1", "type": "to-do"}

def test_create_task(client):
    rv = client.post('/api/tasks/add', json = {
        "id": 4,
        "title": "task 4",
        "description": "Description 4", 
        "type": "to-do"
    })
    assert "task 4" in rv.data and "Description 4" in rv.data

def test_update_task(client):
    rv = client.put('/api/tasks/1', json = {
        "id": 1,
        "title": "task 1 - edited",
        "description": "a new description",
        "type": "to-do"
    })
    assert "task 1 - edited" in rv.data
    assert "Description 1" not in rv.data

def test_delete_task(client):
    rv = client.delete('/api/tasks/2')
    assert "task 2" not in rv.data
    assert "description 2" not in rv.data


