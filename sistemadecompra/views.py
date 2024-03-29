## ESTOS ERAN NUESTROS IMPORTS QUE METIMOS AHORA
from django.shortcuts import render
from django.http import HttpResponse
#from .models import Producto
from django.template import loader
from django.db.models import Q
import calendar


###############################################


from django.shortcuts import render, redirect
#from django.views.generic.base import TemplateView
from sistemadecompra.models import Producto, Proveedor, Producto, MetodoDePago, Pedido, Horario, Cliente, Calificacion
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
from sistemadecompra.models import Producto, Proveedor, Producto, MetodoDePago, TipoProducto, Notificacion, EstadoPedido, PedidoProductos
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from operator import itemgetter

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

def mostrar_catalogo_v(request): #Paso un parametro adicional con el valor del indice. (request, indice)
    #print("mostrar catalogo v")

    list_producto_nuevos= Producto.objects.all().order_by('id')[:3]
    print(list_producto_nuevos)

    list_Producto = Producto.objects.all()
    list_TipoProducto = TipoProducto.objects.all()
    list_proveedor =  Proveedor.objects.all()

    #Una lista en la que cada posicion va a ser una lista de 6 posiciones y menos
    # ||<><><><><><>
    # ||<><><><><><>
    # ||<><><><><><>
    # ||<><><><><><>
    # ||<><><><><><>
    # ||<><><><>

    list_producto_paginado= []
    list_paginacion= []
    lista_indice= []
    cont= 1
    for producto in list_Producto:
        lista= []
        for i in range(6):
            if producto is not None:
                lista.append(producto)
        list_paginacion.append(lista)
    


    list_id_users_proveedor= []
    for it in list_proveedor:
        list_id_users_proveedor.append(it.user.id)
        #print ('asdsadasd ', it.user.id)


    # creo el carrito en la session por las dudas
    if 'carrito' not in request.session:
        request.session['carrito'] = []

    
    if 'clasificacion' in request.GET: # AAGREGAR CODIGO DE PAGINACION AQUI TAMBIEN
        tipoElegido = request.GET.get('Tipo') 
        print('tipoElegido: ', tipoElegido)

        #print (type(tipoElegido))
        tipoElegido= int(tipoElegido)
        #print(type(tipoElegido))
        list_Producto = Producto.objects.filter(tipo = tipoElegido)
        #print ('NO 0')
    
    if 'BorrarFiltro' in request.GET:
        list_Producto = Producto.objects.all()


    if (request.method == 'GET'):
        if 'elId' in request.GET:
            dic = request.GET  # devuelve un diccionario
            id = dic['elId']
            #id = int(id)
            #id= int(dic['elId'])

            # print(type(id))
            carritoAux = request.session['carrito']
            # if id not in carritoAux:
            #     carritoAux.append(id)
            
            #ATENCION: SE TUVO QUE HACER ESTA PARTE DEL CODIGO MANUALMENTE POR FALTA DE CONOCIMIENTO

            #busco si ya esta agregado el producto en el carrito
            
            existeElProducto = False
            
            for item in carritoAux:
                print("itreacion")
                if id in item:
                    print("encontro el prod id")
                    item.update({id: item.get(id) + 1})
                    existeElProducto = True
                    break
            
            if (existeElProducto == False):
                 carritoAux.append({id: 1})
            request.session['carrito'] = carritoAux
            
            print("imprimo carrito en consola")
            print(carritoAux)
            return render(request, 'sistemadecompra/mostrar_catalogo.html', {"objproducto": list_Producto, 
                                                                            "list_producto_nuevos":list_producto_nuevos})            


    #tipoProductos = TipoProducto.objects.all()
    # print(tipoProductos)

    #proveedor = Proveedor.objects.all()
    # print(proveedor['Proveedor'])

    return render(request, 'sistemadecompra/mostrar_catalogo.html', {"objproducto": list_Producto, 
                                                                    'list_TipoProducto': list_TipoProducto, 
                                                                    'list_id_users_proveedor':list_id_users_proveedor, 
                                                                    "list_producto_nuevos":list_producto_nuevos})


def detalle_producto_v(request, idProducto):
    producto = Producto.objects.get(id=idProducto)
    
    proveedor = producto.proveedor
    pedidos= Pedido.objects.filter(proveedor= proveedor)
    cantidadCalifacion= 0
    sumaPuntaje= 0
    puntajePromedio= 0
    comentarios= []
    for pedido in pedidos:
        if pedido.calificacion is not None:
            sumaPuntaje= sumaPuntaje + pedido.calificacion.puntaje
            cantidadCalifacion+= 1
            comentarios.append(pedido.calificacion.comentario)
   
    if cantidadCalifacion > 0:
        puntajePromedio= sumaPuntaje / cantidadCalifacion
    
    return render(request, 'sistemadecompra/detalle_producto.html', {
        'producto': producto,
        'carrito': request.session['carrito'],
        'puntajePromedio': puntajePromedio,
        'comentarios': comentarios,
        'cantidadCalifacion':cantidadCalifacion
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
    #traigo todos los productos existentes
    productosQuerySet = Producto.objects.all()

    # inicializo las variables que voy a pasar al template
    productosAgregados = []
    proveedores = []
    total = 0
    horariosProveedor = Horario.objects.all()
    
    # Obtengo las keys que estan en el carrito de la session para tener una lista con los productos ids
    listaProductosIdsFromCarrito = []
    for item in carritoAux:
        idInt = int(next(iter(item.keys())))
        listaProductosIdsFromCarrito.append(idInt)
    
    # guardo los objetos Producto dentro de productosAgregados y extraigo los proveedores
    for producto in productosQuerySet:
        if producto.id in listaProductosIdsFromCarrito:
            prodIdStr = str(producto.id)
            cantAux = 0
            for item in carritoAux:
                if str(producto.id) in item:
                    cantAux = item.get(prodIdStr)
                    break
            
            productosAgregados.append({"producto": producto, "cantidad": cantAux})
            if not(Proveedor.objects.get(id=producto.proveedor.id) in proveedores):
                proveedores.append(Proveedor.objects.get(id=producto.proveedor.id))
            total = total + producto.valor

    
    if (request.method == 'GET'):
        if 'solicitudCheckout' in request.GET:
            # Actualizo las cantidades de los productos del carrito
            for item in carritoAux:
                keyAux = "cantProd" + next(iter(item.keys()))
                dic= request.GET
                item.update({next(iter(item.keys())): int(dic[keyAux])})
            request.session['carrito'] = carritoAux
            
            pedidosParaAlmacenar = []
            for prov in proveedores:
                datosValidados = False
                
                fechaProvId = "fecha" + str(prov.id)
                tiempoProvId = "tiempo" + str(prov.id)
                
                print("fechaprovid")
                print(fechaProvId)
                if fechaProvId in request.GET:
                    dic= request.GET # devuelve un diccionario
                    fecha = dic[fechaProvId]
                    tiempo = dic[tiempoProvId]

                    diaDeLaSemana = datetime.strptime(fecha, '%Y-%m-%d').date().weekday()
                    diaDeLaSemana = diasDeLaSemana.get(diaDeLaSemana)

                    hora = datetime.strptime(tiempo, '%H:%M').time()        
                    print("horarios por prov?")
                    print(prov.horario_set.all().values_list('dia', flat=True))
                    # Compruebo que el dia seleccionado este entre los dias que acepta el prov
                    if diaDeLaSemana in prov.horario_set.all().values_list('dia', flat=True):
                        # Obtengo todos los horarios del proveedor que coincidan con el dia
                        for h in Horario.objects.filter(proveedor = prov, dia = diaDeLaSemana):
                            if(hora >= h.horaInicio) and (hora <= h.horaFinal):
                                pedidosParaAlmacenar.append({
                                    "proveedor": prov.id,
                                    "cliente": request.user.cliente.id,
                                    "hora": tiempo,
                                    "fecha": fecha
                                })
                                datosValidados = True
                                break
            print("datos validados")
            print(datosValidados)
            if datosValidados == True:
                request.session['pedidosParaAlmacenar'] = pedidosParaAlmacenar
                return redirect('proceder_Checkout')
            else:
                print("Datos incorrectos. Vuelva a intentar")
                messages.add_message(request, messages.ERROR, "Ha ingresado una fecha invalida para el proveedor.")
        # if 'borrarItemProducto' in request.GET:
        #     dic= request.GET
        #     id= dic['borrarItemProducto']
        #     id= int(id)
        #     print('EL ID:', id)
        #     carritoAux= request.session['carrito']
        #     print ('CARRITOOO: ',carritoAux)
        #     carritoAux.remove(id)
        #     request.session['carrito']= carritoAux  
        #     return redirect('ver_Carrito')



    
    #le saco los espacios a 
    #for proveedor in proveedores:
    #    proveedor.user.username = proveedor.user.username.replace(" ","")
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

                # Obtengo las keys que estan en el carrito de la session para tener una lista con los productos ids
                listaProductosIdsFromCarrito = []
                for item in carritoAux:
                    idInt = int(next(iter(item.keys())))
                    listaProductosIdsFromCarrito.append(idInt)
                
                
                
                #guardo los objetos Producto dentro de productosAgregados
                for producto in productosQuerySet:
                    if producto.id in listaProductosIdsFromCarrito and producto.proveedor == proveedor:
                        prodIdStr = str(producto.id)
                        cantAux = 0
                        for item in carritoAux:
                            if prodIdStr in item:
                                cantAux = item.get(prodIdStr)
                                break
                        productosAgregados.append({"producto": producto, "cantidad": cantAux})
                        
                #asocio los productos al pedido
                for p in productosAgregados:
                    print("p?")
                    print(p)
                    #pedido.productos(p.get('producto'), through_defaults={'cantidad': p.get('cantidad')})
                    
                    pedidoProducto = PedidoProductos(producto=p.get('producto'), pedido=pedido,
                    cantidad=p.get('cantidad'),)
                    pedidoProducto.save()
                
            request.session['carrito'] = []
            return redirect(reverse_lazy('/'))
        
        #traigo todos los productos existentes
        productosQuerySet = Producto.objects.all()
        
        # inicializo las variables que voy a pasar al template
        productosAgregados = []
        proveedores = []
        totalFinal = 0
        carritoAux = request.session['carrito']
        # Obtengo las keys que estan en el carrito de la session para tener una lista con los productos ids
        listaProductosIdsFromCarrito = []
        for item in carritoAux:
            idInt = int(next(iter(item.keys())))
            listaProductosIdsFromCarrito.append(idInt)
    
        
        # guardo los objetos Producto dentro de productosAgregados y extraigo los proveedores
        for producto in productosQuerySet:
            if producto.id in listaProductosIdsFromCarrito:
                prodIdStr = str(producto.id)
                cantAux = 0
                for item in carritoAux:
                    if str(producto.id) in item:
                        cantAux = item.get(prodIdStr)
                        break
                
                productosAgregados.append({"producto": producto, "cantidad": cantAux, "subTotal": producto.valor * cantAux})
                if not(Proveedor.objects.get(id=producto.proveedor.id) in proveedores):
                    proveedores.append(Proveedor.objects.get(id=producto.proveedor.id))
                totalFinal = totalFinal + producto.valor * cantAux
    return render(request, 'sistemadecompra/checkout.html', {"elCarrito": productosAgregados, "losProveedores": proveedores, 'losPagos': pagos, "totalFinal": totalFinal})

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
            pedido.estado = EstadoPedido.objects.get(nombre="Cancelado")

            user_proveedor= request.user.username
            notificacion_nueva= Notificacion()
            notificacion_nueva.user= pedido.cliente.user
            notificacion_nueva.leido= False
            notificacion_nueva.mensaje= "El proveedor " + user_proveedor + " ha cancelado su compra por falta de stock" 
            notificacion_nueva.save()

            pedido.save()
            #print(pedido)
            ##return render(request, 'registration/perfil_proveedor.html') 
        
        if 'cambioFecha' in request.POST:
            dic=request.POST
            pedido = Pedido.objects.get(id = dic['cambioFecha'])
            user_proveedor= request.user.username

            # Creo la Notificacion
            notificacion_nueva= Notificacion()
            notificacion_nueva.user= pedido.cliente.user
            notificacion_nueva.leido= False
            notificacion_nueva.mensaje= "El proveedor " + user_proveedor + " ha rechazado la fecha. Solicite otra en su menu de pedidos." 
            notificacion_nueva.save()
            

            # Le asigno el estado Cambio Fecha al Pedido
            pedido.estado = EstadoPedido.objects.get(nombre="Cambio Fecha")
            pedido.save()

        return render(request, 'registration/perfil_proveedor.html', {'tab': 'pedidos',})

    for p in pedidos:
        if p.estado.nombre == "Creado":
            listaProd = []
            for producto in p.productos.all():
                pedProd = producto.pedidoproductos_set.get(pedido=p)
                listaProd.append({"producto": pedProd.producto, "cantidad": pedProd.cantidad})
            pedidosSinConfirmar_Producto.append({"pedido": p, "producto_cantidad": listaProd})
        else:
            if p.estado.nombre == "Confirmado":
                listaProd = []
                for producto in p.productos.all():
                    pedProd = producto.pedidoproductos_set.get(pedido=p)
                    listaProd.append({"producto": pedProd.producto, "cantidad": pedProd.cantidad})
                pedidosConfirmado_Producto.append({"pedido": p, "producto_cantidad": listaProd})

    #print(pedidosConfirmado_Producto)
    return render(request, 'sistemadecompra/pedidos.html',{'pedidosSinConfirmar_Producto': pedidosSinConfirmar_Producto, 'pedidosConfirmado_Producto': pedidosConfirmado_Producto})

def verMapa(request):
    estadoConfirmado = EstadoPedido.objects.get(nombre="Confirmado")
    coordenadas=[]
    pedidosQuerySet = Pedido.objects.filter(estado = estadoConfirmado, proveedor = request.user.proveedor)
    print("pedidos:")
    print(pedidosQuerySet)
    for p in pedidosQuerySet:
        latAux = str(p.latitud).replace(',','.')
        lngAux = str(p.longitud).replace(',','.')
        coordenadas.append({'latitud': latAux, 'longitud': lngAux})

    destinoYOrigenLatitud = Proveedor.objects.get(id = request.user.proveedor.id).latitud
    destinoYOrigenLongitud = Proveedor.objects.get(id = request.user.proveedor.id).longitud

    destinoYOrigenLatitud = str(destinoYOrigenLatitud).replace(',','.')
    destinoYOrigenLongitud = str(destinoYOrigenLongitud).replace(',','.')
    print(coordenadas)
    return render(request, 'sistemadecompra/verMapa.html',{'coordenadas': coordenadas, 'destinoYOrigenLatitud': destinoYOrigenLatitud, 'destinoYOrigenLongitud': destinoYOrigenLongitud})

def cambioDeFecha(request, idPedido):
    diasDeLaSemana = {0: 'Lunes', 1: 'Martes', 2: 'Miercoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sabado', 6: 'Domingo'}

    pedido = Pedido.objects.get(id = idPedido)
    proveedor = pedido.proveedor

    if (request.method == 'POST'):
        datosValidados = True

        dic= request.POST
        fecha = dic['fecha']
        tiempo = dic['tiempo']
        
        diaDeLaSemana = datetime.strptime(fecha, '%Y-%m-%d').date().weekday()
        diaDeLaSemana = diasDeLaSemana.get(diaDeLaSemana)

        hora = datetime.strptime(tiempo, '%H:%M').time()

        if diaDeLaSemana in proveedor.horario_set.all().values_list('dia', flat=True):
            for h in Horario.objects.filter(proveedor = proveedor, dia = diaDeLaSemana).values_list('horaInicio', flat=True):
                if(hora >= h):
                    for h in Horario.objects.filter(proveedor = proveedor, dia = diaDeLaSemana).values_list('horaFinal', flat=True):
                        if(hora <= h):
                            pedido.fecha = fecha
                            pedido.hora = tiempo

                            estadoCreado = EstadoPedido.objects.get(nombre="Creado")
                            pedido.estado = estadoCreado

                            pedido.save()

                            return render(request, 'registration/perfil_cliente.html', {'tab': 'pedidos',})


                            datosValidados = datosValidados and True
                        else:
                            datosValidados = datosValidados and False
                else:
                    datosValidados = datosValidados and False
        else:  
            datosValidados = datosValidados and False

        if datosValidados == True:
            print("todo bien")
        else:
            print("Datos incorrectos. Vuelva a intentar")
    return render(request, 'sistemadecompra/cambioDeFecha.html', {'pedido': pedido, 'proveedor': proveedor})

def verHistorialVentas(request):
    #productos = Producto.objects.filter(proveedor = request.user.proveedor)
    estado_entregado= EstadoPedido.objects.get(nombre='Entregado')
    estado_cancelado= EstadoPedido.objects.get(nombre='Cancelado')
    #pedidos = Pedido.objects.filter(proveedor = request.user.proveedor, estado = estado_entregado).order_by('-fecha')

    pedidos = Pedido.objects.filter(proveedor = request.user.proveedor)

    pedidosHistorial = []
    for pedido in pedidos:
        if pedido.estado.nombre == "Entregado" or pedido.estado.nombre == "Cancelado":
            pedidosHistorial.append({"pedido": pedido, "producto": Producto.objects.filter(pedido= pedido)})
            #pedidosHistorial.append({"pedido": pedido, "producto": pedido.productos})
            #print('CALIFICAION:', pedido.calificacion.puntaje)
            #   
    return render(request, 'sistemadecompra/historialVentas.html',{'pedidosHistorial': pedidosHistorial})


def verInformacionProveedor(request):
    proveedor = Proveedor.objects.get(id = request.user.proveedor.id)

    pedidos= Pedido.objects.filter(proveedor= proveedor)
    cantidadCalifacion= 0
    sumaPuntaje= 0
    puntajePromedio= 0
    comentarios= []
    for pedido in pedidos:
        if pedido.calificacion is not None:
            sumaPuntaje= sumaPuntaje + pedido.calificacion.puntaje
            cantidadCalifacion += 1
            #comentarios.append(pedido.calificacion.comentario)
            comentarios.append({'comentario': pedido.calificacion.comentario, 
                                'cliente': pedido.cliente.user.username, 
                                'fecha': pedido.calificacion.fecha,
                                'puntaje': pedido.calificacion.puntaje})

    #print('sumaPuntaje: ', sumaPuntaje)
    #print('cantidadCalifacion: ', cantidadCalifacion) 
    if cantidadCalifacion > 0:
        puntajePromedio= sumaPuntaje / cantidadCalifacion


    return render(request, 'sistemadecompra/informacionProveedor.html',{'proveedor': proveedor,
                                                                        'puntajePromedio':puntajePromedio,
                                                                        'comentarios':comentarios,
                                                                        'cantidadCalifacion':cantidadCalifacion})

def verInformacionCliente(request):
    cliente = Cliente.objects.get(id = request.user.cliente.id)
    #print('asdasd', proveedor.user.email)
    return render(request, 'sistemadecompra/informacionCliente.html',{'cliente': cliente})


def verHistorialCompras(request):
    pedidos = Pedido.objects.filter(cliente = request.user.cliente).order_by('-fecha')

    if (request.method == 'POST'):
        if 'Calificacion' in request.POST:
            dic=request.POST
            #print ('ENTREEE ')
            #print ('calificacion:   ', dic['Calificacion'])
            pedido = Pedido.objects.get(id = dic['Calificacion'])

            #print (dic)
            calificacion_new = Calificacion()
            calificacion_new.puntaje = int(dic['exampleRadios'])
            calificacion_new.comentario = dic['message-text']
            
            calificacion_new.save()
            calificacion = Calificacion.objects.last()

            pedido.calificacion = calificacion
            pedido.save()
        return render(request, 'registration/perfil_cliente.html', {'tab': 'historialCompra',})
    
    pedidosHistorial = []
    for pedido in pedidos:
        if pedido.estado.nombre != "Creado" and pedido.estado.nombre != "Cambio Fecha":
            pedidosHistorial.append({"pedido": pedido, "producto": pedido.productos})
            #print('CALIFICAION:', pedido.calificacion.puntaje)
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
        if pedido.estado.nombre == "Creado" or pedido.estado.nombre == "Cambio Fecha" or pedido.estado.nombre == "Confirmado":
            print ("HORARIOSSSS: ", pedido.proveedor.horario_set.all())
            listaProd = []
            for producto in pedido.productos.all():
                p = producto.pedidoproductos_set.get(pedido=pedido)
                print("productos")
                print(p.producto)
                listaProd.append({"producto": p.producto, "cantidad": p.cantidad})
            misPedidos.append({"pedido": pedido, "producto_cantidad": listaProd})

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

def elimimar_item_carrito(request, idProducto):
    
    producto = Producto.objects.get(id=idProducto)
    carritoAux= request.session['carrito']
    print ('CARRITOOO: ',carritoAux)
    strProdId = str(idProducto)
    for item in carritoAux:
        if strProdId in item:
            item.pop(strProdId)
            break
    
    # Al eliminar el producto (que esta representado por un diccionario), queda un diccionario vacio y rompe todo el sistema.
    # Uso filter para eliminar ese diccionario vacio
    carritoAux = list(filter(None, carritoAux))
    
    # print(type(idProducto))
    # carritoAux.pop(str(idProducto))
    print ('CARRITOOO2: ',carritoAux)
    
    request.session['carrito']= carritoAux  

    return redirect('ver_Carrito')



