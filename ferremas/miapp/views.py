from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializer import ProductoSerializer,PrecioSerializer
from django.http import JsonResponse,HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Producto, Precio
import json
import datetime as dt
from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys
import random



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

@csrf_exempt
def webpay_plus_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            amount = data.get('amount')

            buy_order = str(random.randrange(1000000, 99999999))
            session_id = str(random.randrange(1000000, 99999999))
            return_url = request.build_absolute_uri('commit-pay/')

            tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY))
            response = tx.create(buy_order, session_id, amount, return_url)
            print('Response from Webpay:', response)

            if 'url' in response and 'token' in response:
                return JsonResponse({'url': response['token'], 'token': response['url']})
            else:
                return JsonResponse({'error': 'La respuesta de Webpay no contiene los atributos esperados.'}, status=500)
        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt 
def commit_pay(request):
    print("aaRequest method:", request.method)
    print('commitpay', commit_pay    )
    print('request: ', request.POST)
    token = request.GET.get('token_ws')
    TBK_TOKEN = request.POST.get('TBK_TOKEN')
    TBK_ID_SESSION = request.POST.get('TBK_ID_SESSION')
    TBK_ORDEN_COMPRA = request.POST.get('TBK_ORDEN_COMPRA')
    
    #TRANSACCIÓN REALIZADA
    if TBK_TOKEN is None and TBK_ID_SESSION is None  and TBK_ORDEN_COMPRA is None and token is not None:
        #APROBAR TRANSACCION
        tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY))
        response = tx.commit(token)
        status = response.get('status')
        buy_order = response.get('buy_order')
        session_id = response.get('session_id')

        print('status: ', status)
        response_code = response.get('response_code')
        print('response_code: ', response_code)
        #TRANSACCIÓN APROBADA
        if status == 'AUTHORIZED' and response_code == 0:
            state = ''
            if response.get('status') == 'AUTHORIZED':
                state = 'Aceptado'
            pay_type = ''
            if response.get('payment_type_code') == 'VD':
                pay_type = 'Tarjeta de Débito'
            amount = int(response.get('amount'))
            amount = f'{amount:,.0f}'.replace(',', '.')
            transaction_date = dt.datetime.strptime(response.get('transaction_date'), '%Y-%m-%dT%H:%M:%S.%fZ')
            transaction_date = '{:%d-%m-%Y %H%M:%S}'.format(transaction_date)
            transaction_detail = {
                'card_number': response.get('card_detail').get('card_number'),
                'transaction_date': transaction_date,
                'state': state,
                'pay_type': pay_type,
                'amount': amount,
                'authorization_code': response.get('authorization_code'),
                'buy_order': response.get('buy_order')
            }
            return render(request, 'commitpay.html', {'transaction_detail': transaction_detail})
        else:
            return HttpResponse('ERROR EN LA TRANSACCIÓN, SE RECHAZA LA TRANSACCIÓN')
    else:                             
        return HttpResponse('ERROR EN LA TRANSACCIÓN, SE CANCELO EL PAGO')