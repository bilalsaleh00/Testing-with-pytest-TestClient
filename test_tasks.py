def test_create_task(client):
    task_data = {"title": "Write tests"}

    response = client.post("/tasks/", json=task_data)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Write tests"
    assert data["completed"] is False
    assert "id" in data


def test_list_tasks(client):
    response = client.get("/tasks/")

    assert response.status_code == 200
    assert response.json() == []


def test_get_task_by_id(client):
    created = client.post("/tasks/", json={"title": "Read a book"})
    assert created.status_code == 201

    task_id = created.json()["id"]
    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Read a book"


def test_get_nonexistent_task_returns_404(client):
    response = client.get("/tasks/9999")

    assert response.status_code == 404


def test_patch_task(client):
    created = client.post("/tasks/", json={"title": "Write tests"})
    assert created.status_code == 201

    task_id = created.json()["id"]
    response = client.patch(
        f"/tasks/{task_id}",
        json={"completed": True},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True
    assert data["title"] == "Write tests"


def test_delete_task(client):
    created = client.post("/tasks/", json={"title": "Delete me"})
    assert created.status_code == 201

    task_id = created.json()["id"]
    delete_response = client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 200
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_create_task_invalid_data_returns_422(client):
    response = client.post("/tasks/", json={"title": ""})

    assert response.status_code == 422


def test_duplicate_task_title_returns_409(client):
    first = client.post("/tasks/", json={"title": "Unique task"})
    assert first.status_code == 201

    second = client.post("/tasks/", json={"title": "Unique task"})

    assert second.status_code == 409
