# <h1>PROJECT_IPS</h1>

# Proceso de Creación de un Proyecto Django

## 1. Preparación del Entorno

### 1.1 Instalar Python
Asegúrate de tener Python instalado en tu sistema. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).

### 1.2 Crear un Entorno Virtual
```bash
python -m venv myenv
source myenv/bin/activate  # En Windows: myenv\Scripts\activate
```

### 1.3 Instalar Django
```bash
pip install django
```

## 2. Crear el Proyecto Django

### 2.1 Iniciar el Proyecto
```bash
django-admin startproject myproject
cd myproject
```

### 2.2 Crear una Aplicación
```bash
python manage.py startapp myapp
```

### 2.3 Configurar la Aplicación
Añade 'myapp' a INSTALLED_APPS en myproject/settings.py:
```python
INSTALLED_APPS = [
    ...
    'myapp',
]
```

## 3. Configurar la Base de Datos

### 3.1 Configurar la Base de Datos en settings.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 3.2 Realizar Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

## 4. Crear Modelos

### 4.1 Definir Modelos en myapp/models.py
```python
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
```

### 4.2 Crear y Aplicar Migraciones
```bash
python manage.py makemigrations myapp
python manage.py migrate
```

## 5. Crear Vistas

### 5.1 Definir Vistas en myapp/views.py
```python
from django.shortcuts import render
from .models import MyModel

def home(request):
    items = MyModel.objects.all()
    return render(request, 'home.html', {'items': items})
```

## 6. Configurar URLs

### 6.1 Crear myapp/urls.py
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
```

### 6.2 Actualizar myproject/urls.py
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]
```

## 7. Crear Plantillas HTML

### 7.1 Crear el Directorio de Plantillas
```bash
mkdir -p myapp/templates
```

### 7.2 Crear home.html en myapp/templates
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

## 8. Ejecutar el Servidor de Desarrollo
```bash
python manage.py runserver
```

Visita http://127.0.0.1:8000/ en tu navegador para ver tu aplicación en funcionamiento.
```

¿Necesitas alguna modificación adicional en este contenido Markdown?
