from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.seguridad.seguridad import verify_access_token #importamos la funcion de seguridad que verifica el token
from fastapi import Depends, HTTPException, status
from app.database.database import user_collection #importamos la coleccion de usuarios mongodb
# Usamos HTTPBearer en lugar de OAuth2PasswordBearer
bearer_scheme = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    payload = verify_access_token(token)

    # Validar que se obtuvo payload correctamente
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Token inválido: sin email")

    user = await user_collection.find_one({"email": email})

    if not user or user.get("token") != token or not user.get("isactive", False):
        raise HTTPException(status_code=401, detail="Token inválido o usuario inactivo")

    return user