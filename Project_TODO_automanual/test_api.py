import requests

BASE_URL = "http://127.0.0.1:5000"

def test_get_tasks_empty():
    resp = requests.get(f"{BASE_URL}/tasks")
    assert resp.status_code == 200
    assert resp.json() == []

def test_create_task_and_get_by_id():
    
    data = {"title": "Test task", "description": "Test description"}
    resp = requests.post(f"{BASE_URL}/tasks", json=data)
    assert resp.status_code == 201
    task = resp.json()
    assert task["title"] == data["title"]
    task_id = task["id"]

   
    resp2 = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert resp2.status_code == 200
    assert resp2.json()["id"] == task_id

def test_update_task():
  
    data = {"title": "Update test"}
    resp = requests.post(f"{BASE_URL}/tasks", json=data)
    task_id = resp.json()["id"]

    update_data = {"status": "completed"}
    resp2 = requests.put(f"{BASE_URL}/tasks/{task_id}", json=update_data)
    assert resp2.status_code == 200
    assert resp2.json()["status"] == update_data["status"]

def test_delete_task():
   
    data = {"title": "Delete test"}
    resp = requests.post(f"{BASE_URL}/tasks", json=data)
    task_id = resp.json()["id"]

    resp2 = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    assert resp2.status_code == 200
    assert resp2.json()["message"] == "Task deleted"

    resp3 = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert resp3.status_code == 404
