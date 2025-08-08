from fastapi import FastAPI
from app.routes import registro
from app.routes import login
from app.routes import deleteuser

app = FastAPI()

#Rutas de la aplicacion
app.include_router(registro.router, prefix="/user", tags=["Registro"])

app.include_router(login.router, prefix="/user", tags=["login"])

app.include_router(deleteuser.router, prefix="/user", tags=["delete_user"])