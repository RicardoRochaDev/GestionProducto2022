from django.urls import path
#from .views import *
from django.conf import settings
from django.conf.urls.static import static 
from . import views

urlpatterns = [
    path('login/', views.iniciar_sesion_v, name='login'),
    #path('login/', views.LoginView.as_view(), name= 'inicio_login'),
    path('logout/', views.logout_View, name='logout'),

    path('RegistrarProveedor/', views.registrar_usuario_proveedor_v, name='registrar_Proveedor'),
    path('RegistrarCliente/', views.registrar_usuario_cliente_v, name='registrar_Cliente'),
    
    
    path('ModificarProveedor/<int:pk>/', views.ProveedorUpdate.as_view(), name='modificar_Proveedor'),
    path('ModificarCliente/<int:pk>/', views.ClienteUpdate.as_view(), name='modificar_Cliente'),

    path('creacionProducto/', views.ProductoCreate.as_view(), name='crear_Producto'),
    path('modificarProducto/<int:pk>/', views.ProductoUpdate.as_view(), name='modificar_Producto'),
    path('eliminarProducto/<int:pk>/', views.ProductoDelete.as_view(), name='eliminar_Producto'),
    
    path('listaProductos/', views.ver_productos_proveedor, name='ver_Produto_Proveedor'),

    path('listaHorarios/', views.ver_horarios_proveedor, name='ver_Horario_Proveedor'),
    #path('creacionHorario/', views.HorarioCreate.as_view(), name='crear_Horario'),

    path('registrarHorario/', views.registrar_horario, name='registrar_Horario'),
    path('eliminarHorario/<int:pk>/', views.HorarioDelete.as_view(), name='eliminar_Horario'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
