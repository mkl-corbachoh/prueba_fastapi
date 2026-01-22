from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.schemas import ProductCreate

# ============ PRODUCTOS ============

def get_products(db: Session):
    """
    Obtiene todos los productos de la base de datos.
    
    Args:
        db: Sesión de SQLAlchemy
    
    Returns:
        Lista de todos los productos
    """
    return db.query(Product).all()


def get_product_by_id(db: Session, product_id: int):
    """
    Obtiene un producto específico por su ID.
    
    Args:
        db: Sesión de SQLAlchemy
        product_id: ID del producto a buscar
    
    Returns:
        El producto si existe, None si no
    """
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, product: ProductCreate):
    """
    Crea un nuevo producto en la base de datos.
    
    Args:
        db: Sesión de SQLAlchemy
        product: Esquema con los datos del producto a crear
    
    Returns:
        El producto creado
    """
    # Crear una instancia del modelo Product con los datos del esquema
    db_product = Product(
        name=product.name,
        price=product.price,
        in_stock=product.in_stock,
        category_id=product.category_id
    )
    # Agregar a la sesión
    db.add(db_product)
    # Confirmar los cambios en la base de datos
    db.commit()
    # Refrescar para obtener el ID generado
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, updated_product: ProductCreate):
    """
    Actualiza un producto existente en la base de datos.
    
    Args:
        db: Sesión de SQLAlchemy
        product_id: ID del producto a actualizar
        updated_product: Esquema con los nuevos datos
    
    Returns:
        El producto actualizado si existe, None si no existe
    """
    # Buscar el producto por ID
    db_product = db.query(Product).filter(Product.id == product_id).first()
    
    if db_product:
        # Actualizar solo los campos proporcionados
        db_product.name = updated_product.name
        db_product.price = updated_product.price
        db_product.in_stock = updated_product.in_stock
        db_product.category_id = updated_product.category_id
        # Confirmar cambios
        db.commit()
        # Refrescar para obtener datos actualizados
        db.refresh(db_product)
    
    return db_product


def delete_product(db: Session, product_id: int):
    # Buscar el producto por ID
    db_product = db.query(Product).filter(Product.id == product_id).first()
    
    if db_product:
        # Eliminar el producto
        db.delete(db_product)
        # Confirmar cambios
        db.commit()
        return db_product
    
    return None  
