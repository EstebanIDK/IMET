from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('productos/', views.productos, name="productos"),
    path('nuevo_producto/', views.nuevo_producto, name="nuevo_producto"),
    path('categorias/', views.categorias, name='categorias'),
    path('nueva_categoria/', views.nueva_categoria, name="nueva_categoria")
]