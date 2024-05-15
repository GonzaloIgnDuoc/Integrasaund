from rest_framework import serializers
from .models import Transaccion,Producto,Precio



class PrecioSerializer(serializers.ModelSerializer):
    producto_id = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all(), source='producto', write_only=True)

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