from fastapi import APIRouter
from app.api.v1 import auth, cart, products, categories, health, order

# Define the API router para instanciar las rutas
api_router = APIRouter()

api_router.include_router(auth.api_router, prefix="/auth", tags=["auth"]) # tag es para docuementacion
api_router.include_router(products.api_router, prefix="/products", tags=["products"])
api_router.include_router(categories.api_router, prefix="/categories", tags=["categories"])
api_router.include_router(health.api_router, prefix="/health", tags=["health"])
api_router.include_router(cart.api_router, prefix="/cart", tags=["carts"])
api_router.include_router(order.api_router, prefix="/order", tags=["orders"])