from fastapi import APIRouter,Depends,HTTPException,status
from app.schemas.account import UserData
from app.schemas.account import LoginRequest
from app.database.database import get_mongo_db, user_collection
from app.seguridad.seguridad import verify_password, create_access_token
from datetime import datetime, timezone



router = APIRouter()

@router.post("/login", response_model=UserData)
async def login_user(login_data: LoginRequest,db=Depends(get_mongo_db)):
    #Buscar usuario por email usando user_collection de la base de datos
    user = await user_collection.find_one({"email": login_data.email})
    if not user:
        #utilizacion de HTTPException para manejar errores y status codes
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    #Verificar contraseña
    if not verify_password(login_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    token = create_access_token(data={"email": user["email"]})
    now = datetime.now(timezone.utc)
    #Actualizamos campos en MongoDB
    await user_collection.update_one(
        {"id": user["_id"]},
        {"$set": {
            "last_login": now,
            "modified": now,
            "token": token
        }}
    )
    #devolver usuario actualizado
    user["last_login"] = now
    user["modified"] = now 
    user["token"] = token
    user["id"] = str(user["_id"])
    user["Phones"] = user.get("phones", [])
    return UserData(**user)
