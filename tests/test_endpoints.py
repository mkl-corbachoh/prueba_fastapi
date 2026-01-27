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


def create_admin_and_token(client):
    admin_response = create_user(
        client,
        username="admin",
        email="admin@example.com",
        password="adminpass",
        is_admin=True,
    )
    assert admin_response.status_code == 201
    login_response = login_user(client, username="admin@example.com", password="adminpass")
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    return auth_header(token)


def create_user_and_token(client, *, username, email, password):
    create_response = create_user(
        client,
        username=username,
        email=email,
        password=password,
        is_admin=False,
    )
    assert create_response.status_code == 201
    login_response = login_user(client, username=email, password=password)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    return auth_header(token)


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
    admin_headers = create_admin_and_token(client)

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
    admin_headers = create_admin_and_token(client)
    ping_response = client.get("/api/v1/auth/admin/ping", headers=admin_headers)
    assert ping_response.status_code == 200
    assert ping_response.json()["role"] == "admin"


def test_admin_ping_forbidden(client):
    user_headers = create_user_and_token(
        client, username="user1", email="user1@example.com", password="secret"
    )
    ping_response = client.get("/api/v1/auth/admin/ping", headers=user_headers)
    assert ping_response.status_code == 403


def test_login_invalid_credentials(client):
    create_user(
        client,
        username="maria",
        email="maria@example.com",
        password="secret",
        is_admin=False,
    )
    login_response = login_user(client, username="maria@example.com", password="wrongpass")
    assert login_response.status_code == 401


def test_cart_and_order_flow(client):
    admin_headers = create_admin_and_token(client)
    category = create_category(client, name="Gadgets").json()
    product_response = client.post(
        "/api/v1/products/products/",
        json={"name": "Mouse", "price": 20.0, "in_stock": True, "category_id": category["id"]},
        headers=admin_headers,
    )
    assert product_response.status_code == 200
    product_id = product_response.json()["id"]

    user_headers = create_user_and_token(
        client, username="buyer", email="buyer@example.com", password="secret"
    )

    get_cart_response = client.get("/api/v1/cart/", headers=user_headers)
    assert get_cart_response.status_code == 200

    add_response = client.post(
        f"/api/v1/cart/add/{product_id}?quantity=2", headers=user_headers
    )
    assert add_response.status_code == 200
    item_id = add_response.json()["item"]["id"]
    assert add_response.json()["item"]["quantity"] == 2

    order_response = client.post("/api/v1/order/confirm", headers=user_headers)
    assert order_response.status_code == 200
    data = order_response.json()
    assert "order_id" in data
    assert data["total"] == 40.0

    delete_response = client.delete(
        f"/api/v1/cart/delete/{item_id}", headers=user_headers
    )
    assert delete_response.status_code == 404


def test_order_confirm_empty_cart(client):
    user_headers = create_user_and_token(
        client, username="empty", email="empty@example.com", password="secret"
    )
    response = client.post("/api/v1/order/confirm", headers=user_headers)
    assert response.status_code == 400
