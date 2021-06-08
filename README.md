# FlaskApp Motor de Búsqueda
Aplicación Flask para desarrollar el motor de busqueda 

# Installation

### Clonar Repositorio
`git clone git@github.com:TrabajoGradoMotorBusqueda/FlaskApp.git`

### Creación Virtual ENV
Instalar **Python 3.7**
(Debian/Ubuntu)
`sudo apt install python3.7`

Instalar **pip3**
`sudo apt install -y python3-pip`

Instalar **virtualenv**
`pip install virtualenv`

Crear Ambiente Virtual
`virtualenv <nombre-ambiente>`

Activar Ambiente Virtual
`source <nombre-ambiente>/bin/activate`

### Instalar Requirements para el Ambiente
Instalar dependecias y paquetes
`pip install -r requirements.txt`

### Creación de Base de Datos

**TODO**

### Solicitar Carpeta Config
### Crear Carpeta Modelos

### URL DATABASE en archivo config 
`SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://<username>:<password>@<url>:<port>/<database_name>'

### Exportar Variables del archivo .env
Ejemplo:

`export FLASK_ENV=development`

### Migración de base de datos
Identificar STAMP HEAD
`flask db stamp head`

Migración Local
`flask db migrate -m 'Nombre Desarrollador'`

Actualizaer Base de Datos
`flask db upgrade` 

### Correr Aplicación
`flask run`
