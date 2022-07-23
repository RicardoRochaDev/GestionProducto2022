from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .form import ProveedorUserForm, ClienteUserForm, UserForm
from django.contrib.auth.forms import UserCreationForm
from sistemadecompra.models import Proveedor, Cliente, Producto
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from urllib.request import urlopen
import json


def registrar_usuario_proveedor_v(request):
    print("vista: registrar usuario proveedor v")

    context={}
    if request.method == 'POST':
        print('ENTRE AL IF')
        form_user = UserForm(request.POST)
        form_user_proveedor = ProveedorUserForm(request.POST)
        print('LLEGA ACA')
        print(form_user.is_valid())
        print(form_user_proveedor.is_valid())

        if form_user.is_valid() and form_user_proveedor.is_valid():

            #username= form_user.cleaned_data['username']
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            calle = request.POST.get('calle')
            numero = request.POST.get('numero')
            telefono = request.POST.get('telefono')
            descripcionNegocio = request.POST.get('descripcionNegocio')
            calificacion = request.POST.get('calificacion')

            user = User.objects.create_user(username, email, password1)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            user = User.objects.last()
            user_proveedor = Proveedor()
            user_proveedor.user = user
            user_proveedor.calle = calle
            user_proveedor.numero = numero

            calleNombreAux = calle.replace(" ","+")
            calleNumero = numero
            #Se envia una direccion por la url y se recibe un json con varios datos, entre ellos la latitud y longitud
            url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + calleNumero + "+" + calleNombreAux + "&key=AIzaSyAgnETqEf92aH6sMfZ8TT3oXpR1ZWubs0Y"
            json_url = urlopen(url)
            data = json.loads(json_url.read())
            user_proveedor.latitud = data['results'][0]['geometry']['location']['lat']
            user_proveedor.longitud = data['results'][0]['geometry']['location']['lng']

            user_proveedor.telefono = telefono
            user_proveedor.descripcionNegocio = descripcionNegocio
            user_proveedor.calificacion = 0
            user_proveedor.save()
            print('USUARIO Y PROVEEDOR CREADO')
            login(request, user)
            # return render(request, 'maxproductos/mostrar_Catalogo.html')
            return redirect(reverse_lazy('/'))
    else:
        print('ENTRE AL ELSE')
        form_user = UserForm()
        form_user_proveedor = ProveedorUserForm()
        context = {'form_user': form_user,
                   'form_user_proveedor': form_user_proveedor}

    # print(form_user)
    return render(request, 'registration/registrar_usuario_proveedor.html', context)


def registrar_usuario_cliente_v(request):
    context={}
    if request.method == 'POST':
        form_user = UserForm(request.POST)
        form_user_cliente = ClienteUserForm(request.POST)
        print(form_user.is_valid())
        print(form_user_cliente.is_valid())
        if form_user.is_valid() and form_user_cliente.is_valid():
            print(request.POST)
            print("entrad")

            #username= form_user.cleaned_data['username']
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            calle = request.POST.get('calle')
            numero = request.POST.get('numero')
            
            telefono = request.POST.get('telefono')

            user = User.objects.create_user(username, email, password1)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            user = User.objects.last()
            user_cliente = Cliente()
            user_cliente.user = user
            user_cliente.calle = calle
            user_cliente.numero = numero

            calleNombreAux = calle.replace(" ","+")
            calleNumero = numero
            #Se envia una direccion por la url y se recibe un json con varios datos, entre ellos la latitud y longitud
            url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + calleNumero + "+" + calleNombreAux + "&key=AIzaSyAgnETqEf92aH6sMfZ8TT3oXpR1ZWubs0Y"
            json_url = urlopen(url)
            data = json.loads(json_url.read())
            user_cliente.latitud = data['results'][0]['geometry']['location']['lat']
            user_cliente.longitud = data['results'][0]['geometry']['location']['lng']
 
            user_cliente.telefono = telefono
            user_cliente.save()
            login(request, user)
            return redirect(reverse_lazy('/'))
            
    else:
        form_user = UserForm()
        form_user_cliente = ClienteUserForm()
        context = {'form_user': form_user,
                   'form_user_cliente': form_user_cliente}

    return render(request, 'registration/registrar_usuario_cliente.html', context)

def mostrar_perfil_proveedor_v(request):
    
    return render(request, 'registration/perfil_proveedor.html')

def ver_productos_proveedor(request):
    lista_producto_proveedor = Producto.objects.filter(
        proveedor=request.user.proveedor)
    context = {'lista_producto_proveedor': lista_producto_proveedor}
    return render(request, 'registration/producto_proveedor.html', context)


class ProductoCreate(CreateView):
    # nombre del template = (todo minuscula) nombreModelo_form

    # hace una busqueda mal('registration/templates/maxproductos/producto_form.html', nada que ver) sino agrego este atributo.
    template_name = 'registration/producto_form.html'
    model = Producto
    fields = ['nombre', 'marca', 'tipo', 'descripcion', 'valor', 'proveedor']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('login'))
        # print(request.user)
        return super(ProductoCreate, self).dispatch(request, *args, **kwargs)

    success_url = reverse_lazy('mostrar_Perfil_Proveedor')


class ProductoUpdate(UpdateView):
    model = Producto
    fields = ['nombre', 'marca', 'tipo', 'descripcion', 'valor']
    #template_name_suffix = '_update_form'

    # lo mismo que ProductoUpdate
    template_name = 'registration/producto_update_form.html'

    def get_success_url(self):
        return reverse_lazy('ver_Produto_Proveedor')

class ProductoDelete(DeleteView):
    model = Producto
    # lo mismo que ProductoUpdate
    template_name = 'registration/producto_confirm_delete.html'
    success_url = reverse_lazy('ver_Produto_Proveedor')

class ClienteUpdate(UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    #template_name_suffix = '_update_form'

    # lo mismo que ProductoUpdate
    template_name = 'registration/cliente_update_form.html'

    def get_success_url(self):
        return reverse_lazy('ver_Produto_Proveedor')


# class RegistrarUsuario(CreateView):
#     model = User
#     template_name= 'registration/regitrar_usuario.html'
#     form_class = ProveedorUserForm
#     success_url = reverse_lazy('/')
