# <h1>PROJECT_IPS</h1>

# Configuración del Proyecto para Colaboradores

Si eres un colaborador del proyecto, sigue estos pasos para configurar el entorno de desarrollo en tu máquina local:

## 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/PROJECT_IPS.git
cd PROJECT_IPS
```

## 2. Crear y Activar un Entorno Virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
```

## 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

## 4. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto (donde se encuentra manage.py) y añade las siguientes variables:

```
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=True
DATABASE_URL=tu_url_de_base_de_datos_aqui
```

Asegúrate de reemplazar los valores con los apropiados para tu entorno local.

## 5. Aplicar Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

## 6. Crear un Superusuario (opcional)

```bash
python manage.py createsuperuser
```

## 7. Ejecutar el Servidor de Desarrollo

```bash
python manage.py runserver
```

Visita http://127.0.0.1:8000/ en tu navegador para ver la aplicación en funcionamiento.

## Notas Importantes

- Asegúrate de no compartir tu archivo `.env` en el repositorio.
- Si encuentras algún problema durante la configuración, revisa el archivo `requirements.txt` para asegurarte de tener todas las dependencias necesarias instaladas.
- Para cualquier duda o problema, contacta al administrador del proyecto.

# Proceso de Creación de un Proyecto Django

## 1. Preparación del Entorno

### 1.1 Instalar Python
Asegúrate de tener Python instalado en tu sistema. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).

### 1.2 Crear un Entorno Virtual
```bash
python -m venv env
source env/bin/activate
En Windows: env\Scripts\activate
```

### 1.3 Instalar Django
```bash
pip install django
```

## 2. Crear el Proyecto Django

### 2.1 Iniciar el Proyecto
```bash
django-admin startproject project
cd project
```

### 2.2 Crear una Aplicación
```bash
python manage.py startapp tienda
```

### 2.3 Configurar la Aplicación
Añade 'tienda' a INSTALLED_APPS en project/settings.py:
```python
INSTALLED_APPS = [
    ...
    'tienda',
]
```

## 3. Configurar Claves Seguras

### 3.1 Crear archivo .env
Crea un archivo llamado `.env` en la raíz de tu proyecto:
```bash
touch .env
```

### 3.2 Añadir claves seguras al .env
Edita el archivo `.env` y añade tus claves seguras:
```
DB_NAME=nombre_de_tu_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=tu_secreto_de_django
DEBUG=True
```

### 3.3 Instalar django-environ
```bash
pip install django-environ
```

### 3.4 Configurar settings.py para usar .env
Añade y agrega lo siguiente al inicio de tu archivo `settings.py`:
```python
import environ

env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
DATABASES = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
}
```

### 3.5 Añadir .env a .gitignore
Asegúrate de añadir `.env` a tu archivo `.gitignore` para no compartir tus claves secretas:
```
echo ".env" >> .gitignore
```

## 4. Configurar la Base de Datos

### 4.1 Configurar la Base de Datos en settings.py
La configuración de la base de datos ya está hecha en el paso 3.4 usando django-environ.

### 4.2 Realizar Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### EJEMPLO

## 5. Crear Modelos

### 5.1 Definir Modelos en myapp/models.py
```python
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
```

### 5.2 Crear y Aplicar Migraciones
```bash
python manage.py makemigrations myapp
python manage.py migrate
```

## 6. Crear Vistas

### 6.1 Definir Vistas en myapp/views.py
```python
from django.shortcuts import render
from .models import MyModel

def home(request):
    items = MyModel.objects.all()
    return render(request, 'home.html', {'items': items})
```

## 7. Configurar URLs

### 7.1 Crear myapp/urls.py
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
```

### 7.2 Actualizar myproject/urls.py
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]
```

## 8. Crear Plantillas HTML

### 8.1 Crear el Directorio de Plantillas
```bash
mkdir -p myapp/templates
```

### 8.2 Crear home.html en myapp/templates
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Django App</title>
</head>
<body>
    <h1>Welcome to My Django App</h1>
    <ul>
    {% for item in items %}
        <li>{{ item.name }}: {{ item.description }}</li>
    {% endfor %}
    </ul>
</body>
</html>
```

## 9. Ejecutar el Servidor de Desarrollo
```bash
python manage.py runserver
```

Visita http://127.0.0.1:8000/ en tu navegador para ver tu aplicación en funcionamiento.
