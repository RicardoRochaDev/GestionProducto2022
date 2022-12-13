from sistemadecompra.models import Notificacion
from datetime import datetime, timezone, timedelta

def notificaciones(request):
    list_notificacion_user_actual= []
    list_notificacion= Notificacion.objects.all()
    contador_mensajes_no_leidos= 0 
    cantidad_items_carrito = 0
    fechaHoy = datetime.now(timezone.utc)
    #print("calle: ", request.user.cliente.calle)

    #type(i)
    if request.user.is_authenticated:
        #print(hasattr(request.user, 'cliente'))
        if hasattr(request.user, 'cliente'): 
            #list_notificacion= Notificacion.objects.filter(pedido.cliente.id = request.user.cliente.id)
            for n in list_notificacion:
                #print("AQUI ESTOY: ", n.pedido.cliente.id)
                #print("que hay aqui? ", request.user.id)

                #print(mostrarTiempoDesde(fechaHoy - n.fecha))
                if request.user.id == n.user.id:
                    if n.leido == False:
                        ##list_notificacion_user_actual.append(n)
                        list_notificacion_user_actual.append({'notificacionObjeto': n, 'fechaCalculada': mostrarTiempoDesde(fechaHoy - n.fecha)})
                        contador_mensajes_no_leidos+= 1

            
            carrito_session = request.session.get('carrito', [])
            cantidad_items_carrito = 0
            
            # solo por las dudas, filtro la lista de diccionarios para sacar los diccionarios vacios (pueden llegar a quedar diccionarios vacios a veces)
            carrito_session = list(filter(None, carrito_session))
            request.session['carrito']= carrito_session 
            
            for item in carrito_session:
                print("item")
                print(item)
                cantidad_items_carrito += next(iter(item.values()))
    
                          
        if hasattr(request.user, 'proveedor'):
            for n in list_notificacion:
                #print(mostrarTiempoDesde(fechaHoy - n.fecha))

                if request.user.id == n.user.id:
                    if n.leido == False:
                        #list_notificacion_user_actual.append(n)
                        list_notificacion_user_actual.append({'notificacionObjeto': n, 'fechaCalculada': mostrarTiempoDesde(fechaHoy - n.fecha)})
                        contador_mensajes_no_leidos+= 1 
    
    #print(list_notificacion_user_actual)
    contexto= {'list_notificacion_user_actual':list_notificacion_user_actual,
                'contadorNotificacion':contador_mensajes_no_leidos,
                'cantidad_items_carrito':cantidad_items_carrito}
    return contexto  

def mostrarTiempoDesde(tiempo):
    if (tiempo < timedelta(minutes=1)):
        return "hace un momento"
    elif (tiempo < timedelta(minutes=60)):
        return "hace " + str((tiempo.seconds // 60) % 60) + "m"
    elif (tiempo < timedelta(hours=24)):
        return "hace " + str(tiempo.seconds // 3600) + "h"
    else:
        return "hace " + str(tiempo.days) + "d"
    