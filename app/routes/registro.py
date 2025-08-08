from fastapi import APIRouter, status, HTTPException
from app.schemas.account import AccountCreate, AccountData
from app.database.database import user_collection #Importamos la coleccion de usuarios de nuestra base de datos
from uuid import uuid4
from pymongo.errors import DuplicateKeyError
from app.seguridad.seguridad import get_password_hash, create_access_token
from datetime import datetime, timezone

router = APIRouter()

@router.post("/registro",response_model=AccountData, status_code=status.HTTP_201_CREATED)
async def register_user(user: AccountCreate):
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )
    # Hasheamos la contraseña antes de guardarla
    hashed_password = get_password_hash(user.password)
    #Creamos el token JWT sujeto al email del usuario
    token = create_access_token({"email": user.email})
    #Ponemos la fecha actual en UTC
    now = datetime.now(timezone.utc)
    #Preparamos los datos del usuario para guardarlos en la base de datos
    user_dict ={
        "id": str(uuid4()),
        "name": user.name,
        "email": user.email,    
        "password": hashed_password,
        "phones": [phone.dict() for phone in user.phones],
        "is_admin": user.is_admin,
        "created": now,
        "modified": now,
        "last_login": now,
        "token": token
    }
    try:
        await user_collection.insert_one(user_dict)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe."
        )

    # Retorna la info usando el modelo UserOut (sin password)
    user_dict.pop("password")
    return AccountData(**user_dict)
