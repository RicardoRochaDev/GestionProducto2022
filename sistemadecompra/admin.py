from django.contrib import admin

from .models import Producto
from .models import Proveedor
from .models import TipoProducto
from .models import Cliente
from .models import Horario
from .models import Pedido
from .models import MetodoDePago
from .models import Notificacion
from .models import Calificacion
from .models import EstadoPedido


admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(TipoProducto)
admin.site.register(Cliente)
admin.site.register(Horario)
admin.site.register(Pedido)
admin.site.register(MetodoDePago)
admin.site.register(Notificacion)
admin.site.register(Calificacion)
admin.site.register(EstadoPedido)
