from django.contrib import admin

from .models import Producto
from .models import Proveedor

admin.site.register(Producto)
admin.site.register(Proveedor)