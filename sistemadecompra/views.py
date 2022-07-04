from django.shortcuts import render
from django.http import HttpResponse
from .models import Producto
from django.template import loader


# Create your views here.

def catalogo(request):
    lista_productos = Producto.objects.all()

    template = loader.get_template('sistemadecompra/catalogo.html')
    context = {
        'lista_productos': lista_productos,
    }
    return render(request, 'sistemadecompra/catalogo.html', context)
