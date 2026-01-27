from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.deps.deps import get_db, get_current_user
from app.service.order import create_order

api_router = APIRouter()

@api_router.post("/confirm", summary="Confirm order sales")
def confirm_order(db: Session =  Depends(get_db), user = Depends(get_current_user)):
    try:
        order = create_order(db, user)
        return {"message": "Order generate", "order_id": order.id, "total": order.total}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))