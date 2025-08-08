Este proyecto implementa una API RESTful desarrollada con FastAPI y MongoDB para gestionar usuarios de manera segura, eficiente y modular.
Permite crear usuarios, autenticarlos mediante tokens JWT, y almacenar los datos de manera persistente utilizando una base de datos NoSQL.

Tecnologías utilizadas

  FastAPI – Framework moderno y rápido para la construcción de APIs con Python.
  MongoDB – Base de datos NoSQL para el almacenamiento de usuarios.
  Pydantic – Validación de datos con expresiones regulares y tipos estrictos.
  bcrypt – Hash seguro de contraseñas.
  Python-Jose – Generación y validación de tokens JWT.
  python-dotenv – Gestión de variables de entorno.
  Docker + Docker Compose – Contenedores para desplegar la API y MongoDB fácilmente.

Funcionalidades principales

Creación de usuarios con validación de datos:
  Validación de formato de correo, nombre y contraseña con expresiones regulares.
  Almacenamiento del usuario en MongoDB si no existe previamente.

Autenticación JWT:
  Generación de tokens JWT al autenticar un usuario con sus credenciales.

Validación de contraseñas:
  Las contraseñas se almacenan en formato hasheado usando bcrypt para evitar exposiciones.

Contenedorización completa:
  Todo el entorno puede desplegarse con docker-compose en cuestión de segundos.

Estructura de carpetas

├── app/
│   ├── main.py  # Punto de entrada de la API
│   ├── database/
│   │   └── database.py # Configuración de conexión a MongoDB
│   ├── autenticacion/
│   │   └── autenticacion.py #configuracion de autenticacion para bearer token en swagger de la API
│   ├── routes/
│   │   ├── registro.py  # Registro de usuarios (Signup)
│   │   ├── login.py  # Login de usuario
│   │   └── deleteuser.py  # Eliminacion de usuario
│   ├── schemas/
│   │   └── account.py   #Modelos Pydantic para validación y serialización (UserCreate, UserOut, LoginRequest, UserResponse)
│   ├── services/
│   ├── seguridad/
│   │   └── seguridad.py   # Funciones de hashing y JWT
│   └── __pycache__/  # cache de python ( No se sube a github)
├── mongo_data/       # Contiene archivos internos de MongoDB
├── docker-compose.yml # Servicio API + MongoDB
├── Dockerfile  # Dockerfile para construir la imagen de la API
├── requirements.txt  #Archivo utilizado para leer las dependencias a instalar
├── .env  #Archivo donde va la clave secreta y sus parametros (ESTE ARCHIVO NO SE COMPARTE EN GITHUB, SE DEBE CREAR INDIVIDUALMENTE)
├── .gitignore #Archivo para denegar la subida de base de datos, variables de entorno y cache de python

Como ejecutar el programa:
Primero se debe tener instalado docker desktop y para iniciar el programa se debe abrir una terminal de powershell, dirigirse a la carpeta que contiene Docker-compose.yml y ejecutar Docker compose up --build
Notas finales
  Este proyecto es ideal para aprender buenas prácticas de desarrollo backend con Python y despliegue con Docker.
  Las contraseñas y claves nunca se almacenan en texto plano.
  El sistema está preparado para escalar y extender funcionalidades fácilmente.
