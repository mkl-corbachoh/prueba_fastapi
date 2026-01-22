from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.service.product as crud
from app.deps.deps import get_db, reqires_admin
from app.schemas import ProductCreate, ProductResponse


api_router = APIRouter()

# ============ PRODUCTOS ============
@api_router.get("/products/", response_model=list[ProductResponse])
async def read_products(db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return products


@api_router.post(
    "/products/",
    response_model=ProductResponse,
    dependencies=[Depends(reqires_admin)],
)  # Protege la ruta para que solo admins puedan crear productos
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    created_product = crud.create_product(db, product)
    return created_product


@api_router.put(
    "/products/{product_id}",
    response_model=ProductResponse,
    dependencies=[
        Depends(reqires_admin)
    ],  # Protege la ruta para que solo admins puedan actualizar productos
)
async def update_product(
    product_id: int,
    updated_product: ProductCreate,
    db: Session = Depends(get_db),
):
    updated_product = crud.update_product(db, product_id, updated_product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@api_router.delete(
    "/products/{product_id}",
    dependencies=[Depends(reqires_admin)],
)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):  # Protege la ruta para que solo admins puedan eliminar productos
    deleted_product = crud.delete_product(db, product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully", "product": deleted_product}
