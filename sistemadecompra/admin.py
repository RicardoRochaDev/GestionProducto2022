from django.contrib import admin

from .models import Producto
from .models import Proveedor
from .models import TipoProducto


admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(TipoProducto)