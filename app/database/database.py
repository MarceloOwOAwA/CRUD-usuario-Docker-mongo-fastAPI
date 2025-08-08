from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

# URL de conexión 
MONGO_URI = config("MONGO_URI", default="mongodb://localhost:27017")

# Cliente y base de datos
client = AsyncIOMotorClient(MONGO_URI)
db = client["usuarios_db"]

# Colección de usuarios
user_collection = db["users"]  # definimos la colección de usuarios

# Función para usar como dependencia en FastAPI
async def get_mongo_db():
    return db
