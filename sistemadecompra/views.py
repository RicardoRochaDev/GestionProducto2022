## ESTOS ERAN NUESTROS IMPORTS QUE METIMOS AHORA
from django.shortcuts import render
from django.http import HttpResponse
#from .models import Producto
from django.template import loader
from django.db.models import Q


###############################################


from django.shortcuts import render, redirect
#from django.views.generic.base import TemplateView
from sistemadecompra.models import Producto, Proveedor, Producto, MetodoDePago, Pedido, Horario, Cliente
#from .form import ProveedorForm
from datetime import datetime
import calendar
from urllib.request import urlopen
import json
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from sistemadecompra.models import Producto, Proveedor, Producto, MetodoDePago, TipoProducto, Notificacion, EstadoPedido
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User

# Create your views here.
## ESTAS DOS VISTAS LAS CREAMOS NOSOTROS AHORA

def catalogo(request): #NO ESTA EN USO.
    lista_productos = Producto.objects.all()

    template = loader.get_template('sistemadecompra/catalogo.html')
    context = {
        'lista_productos': lista_productos
    }

    if (request.method == 'GET'):
        if 'productoId' in request.GET:
            diccionario = request.GET  # devuelve un diccionario
            id = diccionario['productoId']
            id = int(id)
   
            carritoAux = request.session.get('carrito', [])
            if id not in carritoAux:
                carritoAux.append(id)
            request.session['carrito'] = carritoAux
            return render(request, 'sistemadecompra/catalogo.html', context)  

    return render(request, 'sistemadecompra/catalogo.html', context)


def carrito(request):

    itemsCarrito = []
    carritoSession = request.session.get('carrito', [])

    if carritoSession:
        itemsCarrito = Producto.objects.filter(id__in=carritoSession)
    
    context = {
        'itemsCarrito': itemsCarrito
    }
    return render(request, 'sistemadecompra/carrito.html', context)

## FIN ESTAS DOS VISTAS LAS CREAMOS NOSOTROS AHORA

def mostrar_catalogo_v(request):
    #print("mostrar catalogo v")

    list_producto_nuevos= Producto.objects.all().order_by('id')[:3]
    print(list_producto_nuevos)

    list_Producto = Producto.objects.all()
    list_TipoProducto = TipoProducto.objects.all()
    list_proveedor =  Proveedor.objects.all()

    list_id_users_proveedor= []
    for it in list_proveedor:
        list_id_users_proveedor.append(it.user.id)
        #print ('asdsadasd ', it.user.id)

    if 'carrito' not in request.session:
        request.session['carrito'] = []

    
    if 'clasificacion' in request.GET:
        tipoElegido = request.GET.get('clasificacion') 
        print('tipoElegido: ', tipoElegido)

        if (tipoElegido != 'Seleccione...'):
            #print (type(tipoElegido))
            tipoElegido= int(tipoElegido)
            #print(type(tipoElegido))
            list_Producto = Producto.objects.filter(tipo = tipoElegido)
            #print ('NO 0')

    if (request.method == 'GET'):
        if 'elId' in request.GET:
            dic = request.GET  # devuelve un diccionario
            id = dic['elId']
            id = int(id)
            #id= int(dic['elId'])

            # print(type(id))
            carritoAux = request.session['carrito']
            if id not in carritoAux:
                carritoAux.append(id)
            request.session['carrito'] = carritoAux
        # if 'clasificacion' in request.GET:
        #     dic = request.GET
        #     if dic['clasificacion'] == "1":
        #         p = Producto.objects.get(id=1)
            return render(request, 'sistemadecompra/mostrar_catalogo.html', {"objproducto": list_Producto, "list_producto_nuevos":list_producto_nuevos})            


    #tipoProductos = TipoProducto.objects.all()
    # print(tipoProductos)

    #proveedor = Proveedor.objects.all()
    # print(proveedor['Proveedor'])

    return render(request, 'sistemadecompra/mostrar_catalogo.html', {"objproducto": list_Producto, 'list_TipoProducto': list_TipoProducto, 'list_id_users_proveedor':list_id_users_proveedor, "list_producto_nuevos":list_producto_nuevos})


def detalle_producto_v(request, idProducto):
    producto = Producto.objects.get(id=idProducto)
    #producto= Producto.objects.filter(id=id)

    return render(request, 'sistemadecompra/detalle_producto.html', {
        'producto': producto,
        'carrito': request.session['carrito']
    })

def mostrar_perfil_proveedor_v(request):
    
    return render(request, 'registration/perfil_proveedor.html')
 
def mostrar_perfil_cliente_v(request):
    
    return render(request, 'registration/perfil_cliente.html')
    

##################################################################################################

def verCarrito(request):
    now = datetime.now()
    fechaActual= str(now.year) + "-" + str(now.month) + "-" + str(now.day)
    diasDeLaSemana = {0: 'Lunes', 1: 'Martes', 2: 'Miercoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sabado', 6: 'Domingo'}

    #me aseguro que el carrito exista en la session, por las dudas
    if 'carrito' not in request.session:
        request.session['carrito'] = []

    carritoAux = request.session['carrito']
    #carritoAux.append(1)
    #carritoAux.append(2)
    #traigo todos los productos existentes
    productosQuerySet = Producto.objects.all()

    # inicializo las variables que voy a pasar al template
    productosAgregados = []
    proveedores = []
    total = 0
    horariosProveedor = Horario.objects.all()

    # guardo los objetos Producto dentro de productosAgregados y extraigo los proveedores
    for producto in productosQuerySet:
        if producto.id in carritoAux:
            productosAgregados.append(producto)
            if not(Proveedor.objects.get(id=producto.proveedor.id) in proveedores):
                proveedores.append(Proveedor.objects.get(id=producto.proveedor.id))
            total = total + producto.valor

    if (request.method == 'GET'):
        if 'solicitudCheckout' in request.GET:
            datosValidados = True
            pedidosParaAlmacenar = []
            for prov in proveedores:
                fechaProvId = "fecha" + str(prov.id)
                tiempoProvId = "tiempo" + str(prov.id)
                
                if fechaProvId in request.GET:
                    dic= request.GET # devuelve un diccionario
                    fecha = dic[fechaProvId]
                    tiempo = dic[tiempoProvId]

                    diaDeLaSemana = datetime.strptime(fecha, '%Y-%m-%d').date().weekday()
                    diaDeLaSemana = diasDeLaSemana.get(diaDeLaSemana)

                    hora = datetime.strptime(tiempo, '%H:%M').time()

                    if diaDeLaSemana in Horario.objects.filter(proveedor = prov).values_list('dia', flat=True):
                        for h in Horario.objects.filter(proveedor = prov, dia = diaDeLaSemana).values_list('horaInicio', flat=True):
                            if(hora >= h):
                                for h in Horario.objects.filter(proveedor = prov, dia = diaDeLaSemana).values_list('horaFinal', flat=True):
                                    if(hora <= h):
                                        #Si entra en este if, la fecha y hora esta validada
                                        pedidosParaAlmacenar.append({
                                            "proveedor": prov.id,
                                            "cliente": request.user.cliente.id,
                                            "hora": tiempo,
                                            "fecha": fecha

                                        })
                                        datosValidados = datosValidados and True
                                    else:
                                        datosValidados = datosValidados and False
                            else:
                                datosValidados = datosValidados and False
                    else:  
                        datosValidados = datosValidados and False
            if datosValidados == True:
                request.session['pedidosParaAlmacenar'] = pedidosParaAlmacenar 
                return redirect('proceder_Checkout')
            else:
                print("Datos incorrectos. Vuelva a intentar")
        if 'borrarItemProducto' in request.GET:
            dic= request.GET
            id= dic['borrarItemProducto']
            id= int(id)
            print('EL ID:', id)
            carritoAux= request.session['carrito']
            print ('CARRITOOO: ',carritoAux)
            carritoAux.remove(id)
            request.session['carrito']= carritoAux  
            return redirect('ver_Carrito')

    print(proveedores)
    return render(request, "sistemadecompra/verCarrito.html", {"elCarrito": productosAgregados, "losProveedores": proveedores, "total": total, "horarios": horariosProveedor, 'fechaActual': fechaActual})

def verCheckout(request):
    pagos = MetodoDePago.objects.all().values()

    if (request.method == 'GET'):
        if 'solicitudRealizarPedido' in request.GET:
            dic= request.GET # devuelve un diccionario
            pedidosParaAlmacenar = request.session['pedidosParaAlmacenar']
            for p in pedidosParaAlmacenar:
                cliente = Cliente.objects.get(id= p['cliente'])
                proveedor = Proveedor.objects.get(id= p['proveedor'])
                if dic['elegirDir'] == 'propia':                  
                    calleNombre = Cliente.objects.get(id= p['cliente']).calle
                    calleNumero = Cliente.objects.get(id= p['cliente']).numero
                    latitud = Cliente.objects.get(id= p['cliente']).latitud
                    longitud = Cliente.objects.get(id= p['cliente']).longitud
                else:
                    calleNombre = dic['nuevaCalle'].replace(" ","+")
                    calleNumero = dic['nuevaCalleNumero']
                    #Se envia una direccion por la url y se recibe un json con varios datos, entre ellos la latitud y longitud
                    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + calleNumero + "+" + calleNombre + "&key=AIzaSyAgnETqEf92aH6sMfZ8TT3oXpR1ZWubs0Y"
                    json_url = urlopen(url)
                    data = json.loads(json_url.read())
                    latitud = data['results'][0]['geometry']['location']['lat']
                    longitud = data['results'][0]['geometry']['location']['lng']
                    
                    calleNombre = dic['nuevaCalle'].replace("+"," ")
                
                estadoCreado = EstadoPedido.objects.get(nombre="Creado")
                print(estadoCreado)
                pedido = Pedido(
                    fecha= p['fecha'],
                    hora= p['hora'], 
                    calle= calleNombre, 
                    numero=calleNumero, 
                    latitud= latitud, 
                    longitud = longitud,
                    cliente= cliente, 
                    proveedor= proveedor,
                    estado = estadoCreado
                )
                
                notificacion_nueva= Notificacion()
                notificacion_nueva.user = pedido.proveedor.user
                notificacion_nueva.leido= False
                notificacion_nueva.mensaje= "El cliente " + request.user.username + " le ha realizado un pedido" 
                notificacion_nueva.save()  
                pedido.save()
                
                print("Se creo bien el pedido")

                #Comienza a asociar los productos con el pedido
                carritoAux = request.session['carrito']

                #traigo todos los productos existentes
                productosQuerySet = Producto.objects.all()
                productosAgregados = []

                #guardo los objetos Producto dentro de productosAgregados
                for producto in productosQuerySet:
                    if producto.id in carritoAux:
                        productosAgregados.append(producto)
                for p in productosAgregados:
                    pedido.productos.add(p)
                
                request.session['carrito'] = []
                return redirect(reverse_lazy('/'))
    return render(request, 'sistemadecompra/checkout.html', {'losPagos': pagos})

def verPedidos(request):

    pedidos = Pedido.objects.filter(proveedor = request.user.proveedor)
    productos = Producto.objects.filter(proveedor = request.user.proveedor) # Se usa?
    
    pedidosSinConfirmar_Producto = []
    pedidosConfirmado_Producto = []

    if (request.method == 'POST'):
        if 'confirmar' in request.POST:
            dic=request.POST

            pedido = Pedido.objects.get(id = dic['confirmar'])
            user_proveedor= request.user.username

            # Creo la Notificacion
            notificacion_nueva= Notificacion()
            notificacion_nueva.user= pedido.cliente.user
            notificacion_nueva.leido= False
            notificacion_nueva.mensaje= "El proveedor " + user_proveedor + " le ha confirmado su compra" 
            notificacion_nueva.save()

            # Le asigno el estado Confirmado al Pedido
            estadoConfirmado = EstadoPedido.objects.get(nombre="Confirmado")
            pedido.estado = estadoConfirmado

            pedido.save()

        # Cuando se clickea en Confirmar Entrega se cambia de estado a Entregado
        if 'confirmarEntrega' in request.POST:

            dic=request.POST
            pedido = Pedido.objects.get(id = dic['confirmarEntrega'])

            # Le asigno el estado Entregado al Pedido
            pedido.estado = EstadoPedido.objects.get(nombre="Entregado")

            pedido.save()

        if 'cancelar' in request.POST:
            dic=request.POST
            pedido = Pedido.objects.get(id = dic['cancelar'])

            user_proveedor= request.user.username
            notificacion_nueva= Notificacion()
            notificacion_nueva.user= pedido.cliente.user
            notificacion_nueva.leido= False
            notificacion_nueva.mensaje= "El proveedor " + user_proveedor + " ha cancelado su compra" 
            notificacion_nueva.save()

            pedido.delete()
            print(pedido)
            ##return render(request, 'registration/perfil_proveedor.html') 
        
        if 'cambioFecha' in request.POST:
            dic=request.POST
            pedido = Pedido.objects.get(id = dic['cambioFecha'])
            user_proveedor= request.user.username

            # Creo la Notificacion
            notificacion_nueva= Notificacion()
            notificacion_nueva.user= pedido.cliente.user
            notificacion_nueva.leido= False
            notificacion_nueva.mensaje= "El proveedor " + user_proveedor + " ha rechazado el fecha. Solicite otra en su menu de pedidos." 
            notificacion_nueva.save()
            

            # Le asigno el estado Cambio Fecha al Pedido
            pedido.estado = EstadoPedido.objects.get(nombre="Cambio Fecha")
            pedido.save()

        return render(request, 'registration/perfil_proveedor.html', {'tab': 'pedidos',})

    for p in pedidos:
        if p.estado.nombre == "Creado":
            pedidosSinConfirmar_Producto.append({"pedido": p, "producto": Producto.objects.filter(pedido= p)})
        else:
            if p.estado.nombre == "Confirmado":
                pedidosConfirmado_Producto.append({"pedido": p, "producto": Producto.objects.filter(pedido= p)})

    #print(pedidosConfirmado_Producto)
    return render(request, 'sistemadecompra/pedidos.html',{'pedidosSinConfirmar_Producto': pedidosSinConfirmar_Producto, 'pedidosConfirmado_Producto': pedidosConfirmado_Producto})

def verMapa(request):
    estadoConfirmado = EstadoPedido.objects.get(nombre="Confirmado")
    coordenadas=[]
    pedidosQuerySet = Pedido.objects.filter(estado = estadoConfirmado)
    for p in pedidosQuerySet:
        latAux = str(p.latitud).replace(',','.')
        lngAux = str(p.longitud).replace(',','.')
        coordenadas.append({'latitud': latAux, 'longitud': lngAux})

    destinoYOrigenLatitud = Proveedor.objects.get(id = request.user.proveedor.id).latitud
    destinoYOrigenLongitud = Proveedor.objects.get(id = request.user.proveedor.id).longitud

    destinoYOrigenLatitud = str(destinoYOrigenLatitud).replace(',','.')
    destinoYOrigenLongitud = str(destinoYOrigenLongitud).replace(',','.')
    
    return render(request, 'sistemadecompra/verMapa.html',{'coordenadas': coordenadas, 'destinoYOrigenLatitud': destinoYOrigenLatitud, 'destinoYOrigenLongitud': destinoYOrigenLongitud})


def verHistorialVentas(request):
    productos = Producto.objects.filter(proveedor = request.user.proveedor)
    pedidos = Pedido.objects.filter(proveedor = request.user.proveedor, entregado = 1).order_by('-fecha')

    pedidosHistorial = []
    for p in pedidos:
        pedidosHistorial.append({"pedido": p, "producto": Producto.objects.filter(pedido= p)})
    return render(request, 'sistemadecompra/historialVentas.html',{'pedidosHistorial': pedidosHistorial})


def verInformacionProveedor(request):
    proveedor = Proveedor.objects.get(id = request.user.proveedor.id)
    print('asdasd', proveedor.user.email)
    return render(request, 'sistemadecompra/informacionProveedor.html',{'proveedor': proveedor})

def verInformacionCliente(request):
    cliente = Cliente.objects.get(id = request.user.cliente.id)
    #print('asdasd', proveedor.user.email)
    return render(request, 'sistemadecompra/informacionCliente.html',{'cliente': cliente})


def verHistorialCompras(request):
    pedidos = Pedido.objects.filter(cliente = request.user.cliente).order_by('-fecha')

    pedidosHistorial = []
    for pedido in pedidos:
        if pedido.estado.nombre != "Creado" and pedido.estado.nombre != "Cambio Fecha":
            pedidosHistorial.append({"pedido": pedido, "producto": pedido.productos})
    return render(request, 'sistemadecompra/historialCompras.html',{'pedidosHistorial': pedidosHistorial})
    
def verComprasPendientes(request):
    pedidos = Pedido.objects.filter(cliente = request.user.cliente, entregado = 0).order_by('-fecha')

    pedidosHistorial = []
    for pedido in pedidos:
        pedidosHistorial.append({"pedido": pedido, "producto": pedido.productos})
    return render(request, 'sistemadecompra/comprasPendientes.html',{'pedidosHistorial': pedidosHistorial})

def verPedidosCliente(request):

    #misPedidosSinConfirmar_Producto = []
    #pedidosConfirmado_Producto = []
    auxPedidos= Pedido.objects.filter(cliente = request.user.cliente)
    misPedidos= []
    
    for pedido in auxPedidos:
        if pedido.estado.nombre == "Creado" or pedido.estado.nombre == "Cambio Fecha":
            print ("HORARIOSSSS: ", pedido.proveedor.horario_set.all())
            
            misPedidos.append({"pedido": pedido, "producto": Producto.objects.filter(pedido= pedido)})

    #print(pedidosSinConfirmar_Producto[0].productos)
    #print(pedidosConfirmado_Producto)
    return render(request, 'sistemadecompra/pedidosCliente.html',{'misPedidos': misPedidos})

def actualizar_mensaje_leido(request):
    #list_notificacion= Notificacion.objects.all()

    #PROBANDOOO

    list_notificacion= Notificacion.objects.filter(user = request.user.id)
    for n in list_notificacion:
        if request.user.id == n.user.id:
            n.leido = True
            n.save() 
    return HttpResponse(request)

