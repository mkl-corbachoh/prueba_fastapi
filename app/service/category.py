from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.schemas import CategoryCreate

# ============ CATEGORÍAS ============


def get_categories(db: Session):
    """Obtiene todas las categorías"""
    return db.query(Category).all()


def get_category_by_id(db: Session, category_id: int):
    """Obtiene una categoría por ID"""
    return db.query(Category).filter(Category.id == category_id).first()


def create_category(db: Session, category: CategoryCreate):
    """Crea una nueva categoría"""
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    """Elimina una categoría por ID"""
    db_category = db.query(Category).filter(Category.id == category_id).first()

    if db_category:
        db.delete(db_category)
        db.commit()

    return db_category
