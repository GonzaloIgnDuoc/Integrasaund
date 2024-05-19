"""
URL configuration for ferremas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from miapp.views.views import ProductoViewSet,PrecioViewSet, index, producto_detail
from miapp.views import transbank, views


router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'precios', PrecioViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('index', index, name='index'),
    path('productos/<int:id>/', producto_detail, name='producto_detail'),
    path('webpay-plus-create/', transbank.webpay_plus_create),
    path('webpay-plus-create/commitpay/', transbank.commit_pay, name='commit-pay'),
    path('get_dolar_data/', views.get_dolar_data, name='get_dolar_data'), 
]