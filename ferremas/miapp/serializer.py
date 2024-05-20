from rest_framework import serializers
from .models import Transaccion,Producto,Precio


class PrecioSerializer(serializers.ModelSerializer):
    producto_id = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all(), source='producto', write_only=True)
    #PrimaryKeyRelatedField: Este campo dice que producto_id es una referencia a otro modelo, en este caso Producto.
#queryset=Producto.objects.all(): Esto define que los valores válidos para producto_id son todos los productos en la base de datos.
#source='producto': Esto mapea el campo producto_id al campo producto en el modelo Precio.
#write_only=True: Esto significa que este campo solo se usará al escribir (crear o actualizar) datos, no al leer (mostrar) datos.
    class Meta:
        model = Precio
        fields = ['id', 'producto_id', 'fecha', 'valor']

class ProductoSerializer(serializers.ModelSerializer):
    precios = PrecioSerializer(many=True, required=False)

    class Meta:
        model = Producto
        fields = ['codigo_producto', 'marca', 'codigo', 'nombre', 'precios']

    def create(self, validated_data):
        precios_data = validated_data.pop('precios', [])
        producto = Producto.objects.create(**validated_data)
        for precio_data in precios_data:
            Precio.objects.create(producto=producto, **precio_data)
        return producto
    #Este método define cómo crear un nuevo producto y, al mismo tiempo, cómo crear sus precios asociados:
    #validated_data.pop('precios', []): Extrae los datos de los precios de los datos validados, y si no hay precios, usa una lista vacía.
    #Producto.objects.create(**validated_data): Crea un nuevo producto con los datos validados restantes.
    #for precio_data in precios_data: Para cada precio en los datos de precios:
    #Precio.objects.create(producto=producto, **precio_data): Crea un nuevo precio y lo asocia con el producto recién creado.
    #return producto: Devuelve el producto creado.