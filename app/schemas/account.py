from pydantic import BaseModel, Field, field_validator
import re
from datetime import datetime

class Phone(BaseModel): #Modelo para los números de teléfono
    number: str = Field(..., example="12345678")
    devicecode: str = Field(..., example="9")
    countrycode: str = Field(..., example="56")
    @field_validator('number')
    def number_must_be_digits(cls, v):
        pattern = r'^\d{8}$'
        if not re.match(pattern, v):
            raise ValueError("El número de teléfono debe contener solo dígitos y tener 8 caracteres")
        return v
    @field_validator('devicecode')
    def devicecode_must_be_digits(cls, v):
        pattern = r'^\d{1,2}$'
        if not re.match(pattern, v):
            raise ValueError("El código de ciudad debe contener solo dígitos y tener entre 1 y 2 caracteres")
        return v
    @field_validator('countrycode')
    def countrycode_must_be_digits(cls, v):
        pattern = r'^\d{1,2}$'
        if not re.match(pattern, v):
            raise ValueError("El código de país debe contener solo dígitos y tener entre 1 y 2 caracteres")
        return v

class AccountCreate(BaseModel):#Modelo para crear un usuario, en este se validaran los datos del correo y contraseña
    name: str = Field(..., example="Marcelo Ordenes")
    email: str = Field(..., example="marceloordenesalbornoz@gmail.com")
    password: str = Field(..., min_length=6, example="Password123")
    phones: list[Phone]
    is_admin: bool = Field(..., example=False)
    @field_validator('email')
    def email_must_be_valid(cls, v):
        v = v.lower()
        pattern = r'^[\w\.-]+@[\w\.-]+\.(cl|com)$'
        if not re.match(pattern, v):
            raise ValueError("El correo debe tener un formato válido y terminar en '.cl'o '.com'")
        return v
    @field_validator('password')
    def password_must_be_complex(cls, v):
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=(?:.*\d){2,}).{6,}$'
        if not re.match(pattern, v):
            raise ValueError(
                "La contraseña debe tener al menos una mayúscula, letras minúsculas y dos números"
            )
        return v
class UserData(BaseModel): #Respuesta que se le enviará al cliente al hacer login
    id: str
    name: str
    email: str
    phones: list[Phone]
    last_login: datetime
    modified: datetime
    created: datetime
    token: str

    model_config = {
        "from_attributes": True,
    }
    

class AccountData(BaseModel): #Respuesta que se le enviara al administrador al crear un usuario
    id:str
    name: str
    email: str
    phones: list[Phone]
    is_admin: bool
    created: datetime
    modified: datetime
    last_login: datetime
    token: str

    model_config = {
        "from_attributes": True,
    }

#Modelo para login
class LoginRequest(BaseModel):
    email: str = Field(..., example="marceloordenesalbornoz@gmail.com")
    @field_validator('email')
    def email_to_lower(cls,v):
        return v.lower()
    password: str = Field(..., example="Password123")

#Modelo para eliminar usuario
class DeleteUserRequest(BaseModel):
    email: str = Field(..., example="email@email.com")
    password: str = Field(..., example="Password123")
    token : str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
