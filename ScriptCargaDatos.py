import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GestionProducto2022.settings')
django.setup()

from sistemadecompra.models.Producto import Producto
from sistemadecompra.models.TipoProducto import TipoProducto
from sistemadecompra.models.Proveedor import Proveedor
from sistemadecompra.models.EstadoPedido import EstadoPedido
from django.contrib.auth.models import User

from urllib.request import urlopen

with open('datos/TipoProducto.json', 'r') as archivoTipoProducto:
    tipoProducto = archivoTipoProducto.read()
listaTipoProducto = json.loads(tipoProducto) #devuelve una lista de TipoProducto

with open('datos/EstadoPedido.json', 'r') as archivoEstadoPedido:
    estadoPedido = archivoEstadoPedido.read()
listaEstadoPedido = json.loads(estadoPedido) #devuelve una lista de TipoProducto

with open('datos/Proveedor.json', 'r') as archivoProveedor:
    proveedor = archivoProveedor.read()
listaProveedor = json.loads(proveedor) #devuelve una lista de Proveedor


with open('datos/Producto.json', 'r') as archivoProducto:
    producto = archivoProducto.read()
objetoProducto = json.loads(producto) #devuelve una lista de Producto


#print (listaTipoProducto)

super_usuario = User.objects.create_superuser(
                                            username="admin", 
                                            email="rocha_095@hotmail.com", 
                                            password="admin", 
                                            is_active=True, 
                                            is_staff=True)

for tipo_producto in listaTipoProducto:
    tipo_producto_new = TipoProducto()
    tipo_producto_new.nombre = tipo_producto['Nombre']
    tipo_producto_new.save()

for estado_pedido in listaEstadoPedido:
    estado_pedido_new = EstadoPedido()
    estado_pedido_new.nombre = estado_pedido['Nombre']
    estado_pedido_new.save()

for proveedor in listaProveedor:
    
    user_new = User.objects.create_user(proveedor['NombreUsuario'], proveedor['Email'], proveedor['Contrasenia'])
    user_new.first_name = proveedor['Nombre']
    user_new.last_name = proveedor['Apellido']
    user_new.save()
    user_new = User.objects.last()

    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + proveedor['Numero'] + "+" + calleNombreAux + "&key=AIzaSyAgnETqEf92aH6sMfZ8TT3oXpR1ZWubs0Y"
    json_url = urlopen(url)
    data = json.loads(json_url.read())

    proveedor_new = Proveedor()
    proveedor_new.calle = proveedor['Calle']
    proveedor_new.numero = proveedor['Numero']
    proveedor_new.latitud = data['results'][0]['geometry']['location']['lat']
    proveedor_new.longitud = data['results'][0]['geometry']['location']['lng']
    proveedor_new.telefono = proveedor['Telefono']
    proveedor_new.descripcionNegocio = proveedor['DescripcionNegocio']
    proveedor_new.save()

# dicTipo= TipoProducto.objects.all()
# pro= Proveedor.objects.all()

# for it in objetoProducto:
#     p = Producto()
#     p.nombre = it['Nombre']
#     p.marca = it['Marca']
    
#     for tp in dicTipo:
#         if it['Tipo'] == tp.nombre:
#             p.tipo= tp 
        
#     p.descripcion = it['Descripcion']
#     p.valor = it['Valor']

#     for pr in pro:
#         if it['Proveedor'] == pr.nombre:
#             p.proveedor= pr
#     p.save()


print('TERMINADO')
