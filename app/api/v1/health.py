from fastapi import APIRouter
from datetime import datetime

api_router = APIRouter()

# ============ HEALTH CHECK ============
@api_router.get("/healtcheck/")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}