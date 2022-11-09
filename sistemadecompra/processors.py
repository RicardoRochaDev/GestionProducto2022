
from sistemadecompra.models import Notificacion

def notificaciones(request):
    list_notificacion=  Notificacion.objects.all()
    contexto= {'list_notificacion':list_notificacion}
    return contexto  