from fastapi import APIRouter, Depends
from app.utils.deps import get_current_user

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/me")
def get_me(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello {current_user}"}