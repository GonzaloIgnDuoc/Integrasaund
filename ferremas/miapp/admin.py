from django.contrib import admin
from .models import Producto,Transaccion,Precio
# Register your models here.

admin.site.register(Producto)
admin.site.register(Transaccion)
admin.site.register(Precio)