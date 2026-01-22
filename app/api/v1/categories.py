
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.service.category as crud
from app.deps.deps import get_db
from app.schemas import schemas

api_router = APIRouter()

# ============ CATEGORIAS ============
@api_router.get("/categories/", response_model=list[schemas.CategoryResponse])
async def read_categories(db: Session = Depends(get_db)):
    categories = crud.get_categories(db)
    return categories


@api_router.post("/categories/", response_model=schemas.CategoryResponse)
async def create_category(
    category: schemas.CategoryCreate, db: Session = Depends(get_db)
):
    created_category = crud.create_category(db, category)
    return created_category


# ⚠️ SIN response_model
@api_router.delete("/categories/{category_id}")
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    deleted_category = crud.delete_category(db, category_id)
    if not deleted_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully", "category": deleted_category}
