from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

# Carrito
class Cart(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete") # una vez se elimina un carrito, se eliminan sus items


# Item del carrito
class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")

# Pedido
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now)
    total = Column(Float, default=0.0)
    status = Column(String, default="pending")
    details = relationship("OrderDetail", back_populates="order", cascade="all, delete")

# Detalle del pedido
class OrderDetail(Base):
    __tablename__ = "order_details"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    subtotal = Column(Float, default=0.0)
    order = relationship("Order", back_populates="details")
    product = relationship("Product")
