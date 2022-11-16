from sistemadecompra.models import Notificacion

def notificaciones(request):
    list_notificacion_user_actual= []
    list_notificacion= Notificacion.objects.all()
    contador_mensajes_no_leidos= 0 
    cantidad_items_carrito = 0
    #print("calle: ", request.user.cliente.calle)

    #type(i)
    if request.user.is_authenticated:
        #print(hasattr(request.user, 'cliente'))
        if hasattr(request.user, 'cliente'): 
            #list_notificacion= Notificacion.objects.filter(pedido.cliente.id = request.user.cliente.id)
            for n in list_notificacion:
                #print("AQUI ESTOY: ", n.pedido.cliente.id)
                #print("que hay aqui? ", request.user.id)
                if request.user.id == n.user.id:
                    if n.leido == False:
                        list_notificacion_user_actual.append(n)
                        contador_mensajes_no_leidos+= 1
            
            
            carrito_session = request.session.get('carrito', [])
            cantidad_items_carrito = len( carrito_session)
    
                          
        if hasattr(request.user, 'proveedor'):
            for n in list_notificacion:
                if request.user.id == n.user.id:
                    if n.leido == False:
                        list_notificacion_user_actual.append(n)
                        contador_mensajes_no_leidos+= 1 
    
    
    contexto= {'list_notificacion_user_actual':list_notificacion_user_actual,
                'contadorNotificacion':contador_mensajes_no_leidos,
                'cantidad_items_carrito':cantidad_items_carrito}
    return contexto  