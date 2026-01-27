from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.service.cart import get_cart_by_user, add_item_to_cart, delete_item_from_cart
from app.deps.deps import get_db, get_current_user

api_router = APIRouter()

@api_router.get("/", summary="Get current user's cart")
def get_cart(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    cart = get_cart_by_user(db, current_user.id)
    return cart

@api_router.post("/add/{item_id}", summary="Add item to cart")
def add_item(item_id: int, quantity: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    cart = get_cart_by_user(db, current_user.id)
    try:
        cart_item = add_item_to_cart(db, cart.id, item_id, quantity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Item added to cart", "item": cart_item}

@api_router.delete("/delete/{item_id}", summary="Delete item from cart")
def delete_item(item_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # cart = get_cart_by_user(db, current_user.id)
    cart_item = delete_item_from_cart(db, item_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    return {"message": "Item deleted from cart", "item": cart_item}
