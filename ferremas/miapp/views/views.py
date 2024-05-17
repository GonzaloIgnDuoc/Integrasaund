from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from miapp.serializer import ProductoSerializer,PrecioSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from miapp.models import Producto, Precio
import json

def index(request):
    return render(request, 'index.html')

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        producto_data = request.data
        precios_data = producto_data.pop('precios', [])

        producto_serializer = self.get_serializer(data=producto_data)
        producto_serializer.is_valid(raise_exception=True)
        producto = producto_serializer.save()

        for precio_data in precios_data:
            Precio.objects.create(producto=producto, **precio_data)

        headers = self.get_success_headers(producto_serializer.data)
        return Response(producto_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PrecioViewSet(viewsets.ModelViewSet):
    queryset = Precio.objects.all()
    serializer_class = PrecioSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        precio_data = request.data
        producto_id = precio_data.get('producto_id')

        if not producto_id:
            return Response({'error': 'producto_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        producto = Producto.objects.get(id=producto_id)
        precio_data['producto'] = producto

        precio_serializer = self.get_serializer(data=precio_data)
        precio_serializer.is_valid(raise_exception=True)
        precio = precio_serializer.save()

        headers = self.get_success_headers(precio_serializer.data)
        return Response(precio_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# Create your views here.

def productos_list(request):
    if request.method == 'GET':
        productos = Producto.objects.all()
        productos_list = []
        for producto in productos:
            precios = list(producto.precios.values('fecha', 'valor'))
            productos_list.append({
                'id': producto.id,
                'codigo_producto': producto.codigo_producto,
                'marca': producto.marca,
                'nombre': producto.nombre,
                'codigo': producto.codigo,
                'precios': precios
            })
        return JsonResponse(productos_list, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        producto = Producto.objects.create(
            codigo_producto=data['codigo_producto'],
            marca=data['marca'],
            nombre=data['nombre'],
            codigo=data['codigo']
        )
        for precio_data in data['precios']:
            Precio.objects.create(
                producto=producto,
                fecha=precio_data['fecha'],
                valor=precio_data['valor']
            )
        return JsonResponse({'id': producto.id, 'mensaje': 'Producto agregado con éxito!'})

@csrf_exempt
def producto_detail(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'DELETE':
        producto.delete()
        return JsonResponse({'mensaje': 'Producto eliminado con éxito!'})
    elif request.method == 'PUT' or request.method == 'PATCH':
        data = json.loads(request.body)
        producto.codigo_producto = data.get('codigo_producto', producto.codigo_producto)
        producto.marca = data.get('marca', producto.marca)
        producto.nombre = data.get('nombre', producto.nombre)
        producto.codigo = data.get('codigo', producto.codigo)
        producto.save()
        # Actualiza los precios
        producto.precios.all().delete()  # Elimina los precios antiguos
        for precio_data in data['precios']:
            Precio.objects.create(
                producto=producto,
                fecha=precio_data['fecha'],
                valor=precio_data['valor']
            )
        return JsonResponse({'mensaje': 'Producto actualizado con éxito!'})
#Pruebas
def lista_productos(request):
    productos = Producto.objects.all()
    print(request)
    return render(request, 'index.html', {'productos': productos})

