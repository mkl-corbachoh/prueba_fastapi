from sqlalchemy.orm import Session
from app.models.orders import Cart, CartItem, Order, OrderDetail

def get_cart_by_user(db: Session, user_id: int):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart: # Si noy carrito creamos uno nuevo
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

def add_item_to_cart(db: Session, cart_id: int, product_id: int, quantity: int = 1):
    # Si el producto esta se añade a la cantidad si no se crea un nuevo item
    cart_item = db.query(CartItem).filter(CartItem.cart_id == cart_id, CartItem.product_id == product_id).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    
    return cart_item

def delete_item_from_cart(db: Session, item_id: int):
    item = db.query(CartItem).get(item_id)
    if item:
        db.delete(item)
        db.commit()

    db.refresh(item)
    return item