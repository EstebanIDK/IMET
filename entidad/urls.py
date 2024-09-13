from django.urls import path
from . import views


urlpatterns = [
    path('productos/', views.productos, name="productos"),
    path('nuevo_producto/', views.nuevo_producto, name="nuevo_producto")
]