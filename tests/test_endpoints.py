import pytest



def create_user(client, *, username, email, password, is_admin=False):
    payload = {
        "username": username,
        "email": email,
        "password": password,
        "is_admin": is_admin,
    }
    response = client.post("/api/v1/auth/users/", json=payload)
    return response


def login_user(client, *, username, password):
    data = {"username": username, "password": password}
    response = client.post("/api/v1/auth/login/", data=data)
    return response


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def create_category(client, name="Category A"):
    return client.post("/api/v1/categories/categories/", json={"name": name})


def create_product(client, *, name="Product A", price=12.5, in_stock=True, category_id=None):
    payload = {
        "name": name,
        "price": price,
        "in_stock": in_stock,
        "category_id": category_id,
    }
    return client.post("/api/v1/products/products/", json=payload)



def test_health_check(client):
    response = client.get("/api/v1/health/healtcheck/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_categories_crud(client):
    create_response = create_category(client, name="Tools")
    assert create_response.status_code == 200
    category_id = create_response.json()["id"]

    list_response = client.get("/api/v1/categories/categories/")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    delete_response = client.delete(f"/api/v1/categories/categories/{category_id}")
    assert delete_response.status_code == 200


def test_products_crud(client):
    # Crear un usuario admin
    admin_response = create_user(
        client,
        username="admin",
        email="admin@example.com",
        password="adminpass",
        is_admin=True,
    )
    assert admin_response.status_code == 201
    
    # Login como admin
    login_response = login_user(client, username="admin@example.com", password="adminpass")
    assert login_response.status_code == 200
    admin_token = login_response.json()["access_token"]
    admin_headers = auth_header(admin_token)
    
    # Crear categoría
    category = create_category(client, name="Hardware").json()

    # Crear producto como admin
    create_response = client.post(
        "/api/v1/products/products/",
        json={"name": "Hammer", "price": 25.0, "in_stock": True, "category_id": category["id"]},
        headers=admin_headers
    )
    assert create_response.status_code == 200
    product_id = create_response.json()["id"]

    list_response = client.get("/api/v1/products/products/")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_payload = {
        "name": "Hammer Pro",
        "price": 30.0,
        "in_stock": False,
        "category_id": category["id"],
    }
    update_response = client.put(f"/api/v1/products/products/{product_id}", json=update_payload, headers=admin_headers)
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Hammer Pro"

    delete_response = client.delete(f"/api/v1/products/products/{product_id}", headers=admin_headers)
    assert delete_response.status_code == 200


def test_user_login_me(client):
    create_response = create_user(
        client,
        username="mikel",
        email="mikel@example.com",
        password="secret",
        is_admin=False,
    )
    assert create_response.status_code == 201

    login_response = login_user(client, username="mikel@example.com", password="secret")
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    me_response = client.get("/api/v1/auth/users/me/", headers=auth_header(token))
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "mikel@example.com"


def test_admin_ping_validation_error(client):
    create_response = create_user(
        client,
        username="admin",
        email="admin@example.com",
        password="adminpass",
        is_admin=True,
    )
    assert create_response.status_code == 201

    login_response = login_user(client, username="admin@example.com", password="adminpass")
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    ping_response = client.get("/api/v1/auth/admin/ping", headers=auth_header(token))
    assert ping_response.status_code == 500
