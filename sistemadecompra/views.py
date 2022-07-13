from django.shortcuts import render
from django.http import HttpResponse
from .models import Producto
from django.template import loader


# Create your views here.

def catalogo(request):
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
