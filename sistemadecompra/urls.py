from django.urls import path
from . import views

urlpatterns = [
    path('', views.mostrar_catalogo_v, name='/'),
    path('iniciarSesion/', views.iniciar_sesion_v, name='iniciar_Sesion'),
    path('detalleProducto/<int:idProducto>/', views.detalle_producto_v, name='detalle_Producto'),
    path('verCarrito/', views.verCarrito, name='ver_Carrito'),
    path('procederACheckout/', views.verCheckout, name='proceder_Checkout'),
    path('pedidos/', views.verPedidos, name='ver_Pedidos'),
    path('verMapa/', views.verMapa, name='ver_Mapa'),
    path('historialVentas/', views.verHistorialVentas, name='ver_Historial_Ventas'),

    path('perfilProveedor/', views.mostrar_perfil_proveedor_v, name='mostrar_Perfil_Proveedor'),
    path('perfilCliente/', views.mostrar_perfil_cliente_v, name='mostrar_Perfil_Cliente'),
    
    #path('perfilProveedor/<int:idProveedor>/', views.mostrar_perfil_proveedor_v, name='mostrar_Perfil_Proveedor'),
    
    
    #path('iniciarSesion/', views.InicioSesionView.as_view(), name='ini'),


    # parece ser que debe terminar el nombre(no name) de la url con / para que
    # funcione el {% url %} en el template

    # el nombre de la variable del parametro del path tiene que ser igual al parametro del la funcion 
    # de la vista


]
