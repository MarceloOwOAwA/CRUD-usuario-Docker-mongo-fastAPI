from app.schemas.account import DeleteUserRequest
from app.database.database import user_collection
from app.seguridad.seguridad import verify_access_token, verify_password
from fastapi import HTTPException, status, APIRouter
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/borrar_usuario", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_user(delete_request: DeleteUserRequest):
    """
    Elimina un usuario de la base de datos.
    
    - Verifica que el correo exista.
    - Valida el token de autenticación.
    - Comprueba la contraseña.
    - Elimina el usuario si todas las validaciones pasan.
    """

    # Verificar token
    payload = verify_access_token(delete_request.token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token inválido o expirado."
        )

    # Opcional: verificar que el email del token coincida
    if "email" in payload and payload["email"] != delete_request.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este usuario."
        )

    # Buscar usuario
    existing_user = await user_collection.find_one({"email": delete_request.email})
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El correo electrónico no está registrado."
        )

    # Verificar contraseña
    if not verify_password(delete_request.password, existing_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta."
        )

    # Eliminar usuario
    result = await user_collection.delete_one({"email": delete_request.email})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo eliminar el usuario."
        )

    # Log de auditoría
    logger.info(f"Usuario eliminado: {delete_request.email} por {payload.get('email', 'desconocido')}")

    return {"message": "Usuario eliminado correctamente."}
