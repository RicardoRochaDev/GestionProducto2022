from django.urls import path
from . import views

urlpatterns = [
    path('', views.mostrar_catalogo_v, name='/'),
    path('detalleProducto/<int:idProducto>/', views.detalle_producto_v, name='detalle_Producto'),
    path('verCarrito/', views.verCarrito, name='ver_Carrito'),
    path('procederACheckout/', views.verCheckout, name='proceder_Checkout'),
    path('pedidos/', views.verPedidos, name='ver_Pedidos'),
    path('pedidosCliente/', views.verPedidosCliente, name='ver_Pedidos_Cliente'),
    path('verMapa/', views.verMapa, name='ver_Mapa'),
    path('historialVentas/', views.verHistorialVentas, name='ver_Historial_Ventas'),
    path('historialCompras/', views.verHistorialCompras, name='ver_Historial_Compras'),
    path('comprasPendientes/', views.verComprasPendientes, name='ver_Compras_Pendientes'),
    path('cambioDeFecha/<int:idPedido>', views.cambioDeFecha, name='cambio_De_Fecha'),

    path('informacionProveedor/', views.verInformacionProveedor, name='ver_Informacion_Proveedor'),
    path('informacionCliente/', views.verInformacionCliente, name='ver_Informacion_Cliente'),



    path('perfilProveedor/', views.mostrar_perfil_proveedor_v, name='mostrar_Perfil_Proveedor'),
    path('perfilCliente/', views.mostrar_perfil_cliente_v, name='mostrar_Perfil_Cliente'),

    path('actualizarMensajeLeido/', views.actualizar_mensaje_leido, name='actualizar_mensaje_leido'),
    
    
    #path('perfilProveedor/<int:idProveedor>/', views.mostrar_perfil_proveedor_v, name='mostrar_Perfil_Proveedor'),
    
    #path('iniciarSesion/', views.InicioSesionView.as_view(), name='ini'),


    # parece ser que debe terminar el nombre(no name) de la url con / para que
    # funcione el {% url %} en el template

    # el nombre de la variable del parametro del path tiene que ser igual al parametro del la funcion 
    # de la vista


]
