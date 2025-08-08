from fastapi import APIRouter,Depends
from app.autenticacion.autenticacion import get_current_user
from app.schemas.account import AccountData

router = APIRouter()

@router.get("/admin", response_model=AccountData)
async def read_current_user(user= Depends(get_current_user)):
    return user