from django.db import models
from django.utils import timezone

class Producto(models.Model):
    codigo_producto = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=100)
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=200, default='default-codigo')  # Valor predeterminado agregado

    def __str__(self):
        return f"Nombre: {self.nombre} - Marca: {self.marca}"

class Precio(models.Model):
    producto = models.ForeignKey(Producto, related_name='precios', on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)  # Utiliza timezone.now como valor por defecto
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto.nombre} - {self.valor} el {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"


    
class Transaccion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) #Una clave foránea que vincula cada transacción con un producto específico. 
    cantidad = models.IntegerField()#La cantidad de productos comprados en esta transacción.
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)#El total pagado en la transacción.

    def __str__(self):
        return f"Transacción {self.id} - {self.fecha}"
