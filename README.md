Nuestra aplicación fue creada con django, django-restframework y MySql.

Los primeros pasos:
Remover entorno
  - Remove-Item -Recurse -Force env

Crear entorno
  - python -m venv env

Instalar dependencias
- pip install django
- pip install django-cors-headers
- pip install djangorestframework
- pip install mysql
- pip install transbank-sdk
- pip install request

** Se encuentran en requirements.txt

En el código, deberá ingresar las credenciales de Mysql
Estás deberán ser ingresadas en: ferremas/ferremas/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'schema', --nombre de esquema
        'USER': '-', 
        'PASSWORD': '-',
        'HOST': 'localhost',  # O una URL de servidor remoto
        'PORT': '3306'
    }
}

En Mysql se deberá crear un schema "ferremas"
**Tablas para importar se adjuntara en zip
En MySql-> Server-> Import -> seleccionar "/ferremas.sql" -> Start import

Al iniciar nuestro proyecto con 
py manage.py runserver

*En caso de necesitar migrar
python manage.py makemigrations
python manage.py migrate


Nuestros avances se centran en backend, en donde se logra una correcta conexión con base de datos. Usted podrá agregar un producto en la que se agregará a la base de datos y entrega información mediante la API, 
que podrá ser consumida por otros vendedores en caso de tener consultas especificas. Trabajando con una estructura de api en base a lo solicitado con el precio en un arreglo que se uniría a 
producto en base a sus ID. 
Mediante Serializers, funciones de django. Los serializers manejan la conversion entre los modelos django(bd) y los formatos de api (json).
También se consume valor del dolar y se hara presente en las cards que representarían a los productos registrados, en los que se listará y podrán ser comprados a través de webpay.
