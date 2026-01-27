from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.orders import Order, OrderDetail, Cart

def create_order(db: Session, user_id: int):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart or not cart.items:
        raise ValueError("Cart is empty")

    total = 0.0
    order = Order(user_id=user_id, total=0)
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart.items:
        product = db.get(Product, item.product_id)
        if not product or product.in_stock is False or product.price <= 0:
            continue
        if item.quantity <= 0:
            continue

        subtotal = product.price * item.quantity
        detail = OrderDetail(
            order_id=order.id, product_id=product.id, quantity=item.quantity, subtotal=subtotal
        )
        db.add(detail)
        total += subtotal
    
    order.total = total
    db.commit()
    db.refresh(order)
    for item in cart.items:
        db.delete(item)
    db.commit()
    return order
