import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GestionProducto2022.settings')
django.setup()
django.core.management.execute_from_command_line(['manage.py', 'makemigrations', 'sistemadecompra']) #Ejecuta el comando: py makemigrations sistemadecompra
django.core.management.execute_from_command_line(['manage.py', 'migrate']) #Ejecuta el comando: py manage.py migrate


from sistemadecompra.models.Producto import Producto
from sistemadecompra.models.TipoProducto import TipoProducto
from sistemadecompra.models.Proveedor import Proveedor
from sistemadecompra.models.EstadoPedido import EstadoPedido
from sistemadecompra.models.Cliente import Cliente
from sistemadecompra.models.Horario import Horario
from django.contrib.auth.models import User

from urllib.request import urlopen
#from django.db import migrations


with open('datos/TipoProducto.json', 'r') as archivoTipoProducto:
    tipoProducto = archivoTipoProducto.read()
listaTipoProducto = json.loads(tipoProducto) #devuelve una lista de TipoProducto

with open('datos/EstadoPedido.json', 'r') as archivoEstadoPedido:
    estadoPedido = archivoEstadoPedido.read()
listaEstadoPedido = json.loads(estadoPedido) #devuelve una lista de EstadoPedido

with open('datos/Proveedor.json', 'r') as archivoProveedor:
    proveedor = archivoProveedor.read()
listaProveedor = json.loads(proveedor) #devuelve una lista de Proveedor

with open('datos/Producto.json', 'r') as archivoProducto:
    producto = archivoProducto.read()
listaProducto = json.loads(producto) #devuelve una lista de Producto

with open('datos/Horario.json', 'r') as archivoHorario:
    horario = archivoHorario.read()
listaHorario = json.loads(horario) #devuelve una lista de Horarios

with open('datos/Cliente.json', 'r') as archivoCliente:
    cliente = archivoCliente.read()
listaCliente = json.loads(cliente) #devuelve una lista de Producto



#print (listaTipoProducto)

#Creo un superusuario
super_usuario = User.objects.create_superuser(
                                            username="admin", 
                                            email="rocha_095@hotmail.com", 
                                            password="admin", 
                                            is_active=True, 
                                            is_staff=True)

#Creo los tipos de producto
for tipo_producto in listaTipoProducto:
    tipo_producto_new = TipoProducto()
    tipo_producto_new.nombre = tipo_producto['Nombre']
    tipo_producto_new.save()

#Creo los estados de pedido
for estado_pedido in listaEstadoPedido:
    estado_pedido_new = EstadoPedido()
    estado_pedido_new.nombre = estado_pedido['Nombre']
    estado_pedido_new.save()

#Creo los proveedores
for proveedor in listaProveedor:
    #Creo el usuario(Instancia User)
    user_new = User.objects.create_user(proveedor['NombreUsuario'], proveedor['Email'], proveedor['Contrasenia'])
    user_new.first_name = proveedor['Nombre']
    user_new.last_name = proveedor['Apellido']
    user_new.save()
    user_new = User.objects.last()

    #Obtengo coordenadas de la direccion pasada por json
    #print("CALLEEE")
    calle = proveedor['Calle'].replace(" ","+") #Reemplaza los espacios por "+"
    #print(calle)
    numero = proveedor['Numero']
    #print("NUMEROOOOOO")
    numero = str(numero)
    #print(numero)
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + numero + "+" + calle + "&key=AIzaSyAgnETqEf92aH6sMfZ8TT3oXpR1ZWubs0Y"
    json_url = urlopen(url)
    #print("JSON_URL:")
    #print(json_url)
    #print("DATAAAAAA")
    data = json.loads(json_url.read())
    #print(data)

    #Creo la instancia Proveedor y lo relaciono con user.
    proveedor_new = Proveedor()
    proveedor_new.user = user_new
    proveedor_new.calle = proveedor['Calle']
    proveedor_new.numero = proveedor['Numero']
    proveedor_new.latitud = data['results'][0]['geometry']['location']['lat']
    proveedor_new.longitud = data['results'][0]['geometry']['location']['lng']
    proveedor_new.telefono = proveedor['Telefono']
    proveedor_new.descripcionNegocio = proveedor['DescripcionNegocio']
    proveedor_new.save()

#Creo los productos y lo relaciono con un proveedor y un tipo
for producto in listaProducto:
    producto_new = Producto()
    producto_new.nombre = producto['Nombre']
    producto_new.marca = producto['Marca']
    producto_new.tipo = TipoProducto.objects.get(nombre= producto['Tipo'])
    producto_new.descripcion = producto['Descripcion']
    producto_new.valor = producto['Valor']
    producto_new.imagenUrl = producto['imagenUrl'] 

    user= User.objects.get(username= producto['Proveedor'])
    producto_new.proveedor = user.proveedor
    #producto_new.proveedor = Proveedor.objects.get(calle= producto['Proveedor'])
    producto_new.save()

#Creo los clientes
for cliente in listaCliente:
    #Creo el usuario(Instancia User)
    user_new = User.objects.create_user(cliente['NombreUsuario'], cliente['Email'], cliente['Contrasenia'])
    user_new.first_name = cliente['Nombre']
    user_new.last_name = cliente['Apellido']
    user_new.save()
    user_new = User.objects.last()

    #Obtengo coordenadas de la direccion pasada por json
    calle = cliente['Calle'].replace(" ","+") #Reemplaza los espacios por "+"
    numero = cliente['Numero']
    numero = str(numero)
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + numero + "+" + calle + "&key=AIzaSyAgnETqEf92aH6sMfZ8TT3oXpR1ZWubs0Y"
    json_url = urlopen(url)
    data = json.loads(json_url.read())

    #Creo la instancia Cliente y lo relaciono con user.
    cliente_new = Cliente()
    cliente_new.user = user_new
    cliente_new.calle = cliente['Calle']
    cliente_new.numero = cliente['Numero']
    cliente_new.latitud = data['results'][0]['geometry']['location']['lat']
    cliente_new.longitud = data['results'][0]['geometry']['location']['lng']
    cliente_new.telefono = cliente['Telefono']
    cliente_new.save()

print('TERMINADO')

#from django.core.management import call_command
#from django.core.wsgi import get_wsgi_application 
#application = get_wsgi_application()
#call_command('runserver',  '127.0.0.1:8000')

#django.core.management.execute_from_command_line(['manage.py', 'runserver']) #Ejecuta el comando: py manage.py migrate
