from fastapi import FastAPI
from app.routes import registro
from app.routes import login
from app.routes import autenticacion
from app.autenticacion.autenticacion import get_current_user

app = FastAPI()

#Rutas de la aplicacion
app.include_router(registro.router, prefix="/user", tags=["Registro"])

app.include_router(login.router, prefix="/user", tags=["login"])

app.include_router(autenticacion.router, prefix="/user", tags=["admin"])