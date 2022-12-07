from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.models import User

#from sistemadecompra.models.Horario import Horario
from .form import ProductoForm, ProveedorForm, ProveedorUserForm, ClienteUserForm, UserForm, UserSesionForm, HorarioForm
from django.contrib.auth.forms import UserCreationForm
from sistemadecompra.models import Proveedor, Cliente, Producto, Horario
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, logout, authenticate
from urllib.request import urlopen
import json
from django.contrib import messages


from django.views.generic.base import TemplateView

#from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.INFO: ' USUARIO CREADO CON EXITO',
    50: 'critical',
}

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
            print("callenombreaux")
            print(calleNombreAux)
            print("callenumero")
            print(calleNumero)
            #Se envia una direccion por la url y se recibe un json con varios datos, entre ellos la latitud y longitud
            url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + calleNumero + "+" + calleNombreAux + "&key=AIzaSyAgnETqEf92aH6sMfZ8TT3oXpR1ZWubs0Y"
            json_url = urlopen(url)
            print("json_url")
            print(json_url)
            print("data")
            data = json.loads(json_url.read())
            print(data)
            user_proveedor.latitud = data['results'][0]['geometry']['location']['lat']
            user_proveedor.longitud = data['results'][0]['geometry']['location']['lng']

            user_proveedor.telefono = telefono
            user_proveedor.descripcionNegocio = descripcionNegocio
            user_proveedor.calificacion = 0
            user_proveedor.save()
            print('USUARIO Y PROVEEDOR CREADO')
            login(request, user)
            # return render(request, 'maxproductos/mostrar_Catalogo.html')
            messages.add_message(request, messages.INFO,"Usuario creado con exito")
            return redirect(reverse_lazy('/'))
        else:
            messages.add_message(request, messages.ERROR, form_user.errors.as_data())
            form_user = UserForm()
            form_user_proveedor = ProveedorUserForm()
            context = {'form_user': form_user,
                   'form_user_proveedor': form_user_proveedor}        
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
        # print(' user validado? ',form_user.is_valid())
        # print(' cliente validado? ', form_user_cliente.is_valid())
        if form_user.is_valid() and form_user_cliente.is_valid():
            
            # Asignamos los datos propios del USUARIO
            #username= form_user.cleaned_data['username']
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            # Obtenemos la latidud y longitud en base a la dirección
            calle = request.POST.get('calle')
            numero = request.POST.get('numero')
            
            calleNombreAux = calle.replace(" ","+")
            calleNumero = numero
            latitudDesdeJSON = ""
            longitudDesdeJSON = ""

            #Se envia una direccion por la url y se recibe un json con varios datos, entre ellos la latitud y longitud
            url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + calleNumero + "+" + calleNombreAux + "&key=AIzaSyAgnETqEf92aH6sMfZ8TT3oXpR1ZWubs0Y"
            json_url = urlopen(url)
            data = json.loads(json_url.read())
            
            # Si hay datos en la lista "results" continua. Si no hay datos devuelve un error
            if data['results']:
                latitudDesdeJSON = data['results'][0]['geometry']['location']['lat']
                longitudDesdeJSON = data['results'][0]['geometry']['location']['lng']

                telefono = request.POST.get('telefono')

                # Creamos el objecto User con sus datos y lo guardamos en la base de datos
                user = User.objects.create_user(username, email, password1)
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                # Una vez creado el usuario, volvemos a obtenerlo, lo asociamos a un obtejo Cliente
                # y lo guardamos en la base de datos
                user = User.objects.last()
                user_cliente = Cliente()
                user_cliente.user = user
                user_cliente.calle = calle
                user_cliente.numero = numero
                user_cliente.latitud = latitudDesdeJSON
                user_cliente.longitud = longitudDesdeJSON
                user_cliente.telefono = telefono
                user_cliente.save()

                # Una vez finalizado el proceso redirijo al Inicio
                login(request, user)
                return redirect(reverse_lazy('/'))
            else:
                messages.add_message(request, messages.ERROR, "La dirección ingresada no existe.")
                form_user = UserForm()
                form_user_cliente = ClienteUserForm()
                context = {'form_user': form_user,
                    'form_user_proveedor': form_user_cliente}
        else:
            # Muestro los errores de los formularios si no pudieron ser validados
            messages.add_message(request, messages.ERROR, form_user.errors.as_data())
            messages.add_message(request, messages.ERROR, form_user_cliente.errors.as_data())
            form_user = UserForm()
            form_user_cliente = ClienteUserForm()
            context = {'form_user': form_user,
                'form_user_proveedor': form_user_cliente}
    else: 
        # Si es GET envio un formulario User y ClienteUser vacios al template
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

def ver_horarios_proveedor(request):
    lista_horario_proveedor = Horario.objects.filter(
        proveedor=request.user.proveedor)
    context = {'lista_horario_proveedor': lista_horario_proveedor}
    return render(request, 'registration/horario_proveedor.html', context)


class ProductoCreate(CreateView):
    # nombre del template = (todo minuscula) nombreModelo_form

    # hace una busqueda mal('registration/templates/maxproductos/producto_form.html', nada que ver) sino agrego este atributo.
    template_name = 'registration/producto_form.html'
    model = Producto
    form_class = ProductoForm
    ##fields = ['nombre', 'marca', 'tipo', 'descripcion', 'valor']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('login'))
        # print(request.user)
        return super(ProductoCreate, self).dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        form.instance.proveedor = self.request.user.proveedor
        return super().form_valid(form)

    success_url = reverse_lazy('mostrar_Perfil_Proveedor')
    #success_url = render('registration/perfil_proveedor.html', {'tab': 'pedidos'})


class ProductoUpdate(UpdateView):
    model = Producto
    fields = ['nombre', 'marca', 'tipo', 'descripcion', 'valor','imagenUrl']
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
        return reverse_lazy('mostrar_Perfil_Cliente')

class ProveedorUpdate(UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    #template_name_suffix = '_update_form'

    # lo mismo que ProductoUpdate
    template_name = 'registration/proveedor_update_form.html'

    def get_success_url(self):
        return reverse_lazy('mostrar_Perfil_Proveedor')



# class RegistrarUsuario(CreateView):
#     model = User
#     template_name= 'registration/regitrar_usuario.html'
#     form_class = ProveedorUserForm
#     success_url = reverse_lazy('/')

#def iniciar_sesion_v(request):
#    return render(request, 'registration/iniciar_sesion.html')

def iniciar_sesion_v(request):
    context={}
    if request.method == 'POST':
        form_user_sesion = UserSesionForm(request.POST)
        if form_user_sesion.is_valid():
            #username= form_user.cleaned_data['username']
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('/'))
            else:
                messages.add_message(request, messages.ERROR, "No se encuentra el usuario y/o la contraseña")
        else:
            messages.add_message(request, messages.ERROR, form_user_sesion.errors.as_data())
    
    form_user_sesion = UserSesionForm()
    context = {'form_user_sesion': form_user_sesion}

    return render(request, 'registration/login.html', context)

class InicioSesionView(TemplateView):
    template_name = "sistemadecompra/iniciar_sesion.html"

#adsasd
def registrar_usuario_v(request):
    formulario_proveedor = ProveedorForm()
    # print(request.POST)
    return render(request, 'sistemadecompra/registrar_usuario.html', {'formulario_proveedor': formulario_proveedor})

# Desloguea al usuario actual.
def logout_View(request):
    logout(request)
    #return render(request, 'sistemadecompra/mostrar_Catalogo.html')
    return redirect(reverse_lazy('/'))
    #return reverse_lazy('mostrar_catalogo_v')

#region Horario

class HorarioCreate(CreateView):
    # hace una busqueda mal('registration/templates/maxproductos/producto_form.html', nada que ver) sino agrego este atributo.
    template_name = 'registration/horario_form.html'
    model = Horario
    form_class = HorarioForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('login'))
        # print(request.user)
        return super(HorarioCreate, self).dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        form.instance.proveedor = self.request.user.proveedor
        return super().form_valid(form)

    success_url = reverse_lazy('mostrar_Perfil_Proveedor')

#endregion Horario

# def registrar_usuario_proveedor_v(request):
#     print("vista: registrar usuario proveedor v")

#     context={}
#     if request.method == 'POST':
#         print('ENTRE AL IF')
#         form_user = UserForm(request.POST)
#         form_user_proveedor = ProveedorUserForm(request.POST)
#         form_user_horarios 
#         print('LLEGA ACA')
#         print(form_user.is_valid())
#         print(form_user_proveedor.is_valid())

#         if form_user.is_valid() and form_user_proveedor.is_valid():
#             #username= form_user.cleaned_data['username']
#             username = request.POST.get('username')
#             first_name = request.POST.get('first_name')
#             last_name = request.POST.get('last_name')
#             email = request.POST.get('email')
#             password1 = request.POST.get('password1')
#             password2 = request.POST.get('password2')

#             calle = request.POST.get('calle')
#             numero = request.POST.get('numero')
#             telefono = request.POST.get('telefono')
#             descripcionNegocio = request.POST.get('descripcionNegocio')
#             calificacion = request.POST.get('calificacion')

#             user = User.objects.create_user(username, email, password1)
#             user.first_name = first_name
#             user.last_name = last_name
#             user.save()

#             user = User.objects.last()
#             user_proveedor = Proveedor()
#             user_proveedor.user = user
#             user_proveedor.calle = calle
#             user_proveedor.numero = numero

#             calleNombreAux = calle.replace(" ","+")
#             calleNumero = numero
#             #Se envia una direccion por la url y se recibe un json con varios datos, entre ellos la latitud y longitud
#             url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + calleNumero + "+" + calleNombreAux + "&key=AIzaSyAgnETqEf92aH6sMfZ8TT3oXpR1ZWubs0Y"
#             json_url = urlopen(url)
#             data = json.loads(json_url.read())
#             user_proveedor.latitud = data['results'][0]['geometry']['location']['lat']
#             user_proveedor.longitud = data['results'][0]['geometry']['location']['lng']

#             user_proveedor.telefono = telefono
#             user_proveedor.descripcionNegocio = descripcionNegocio
#             user_proveedor.calificacion = 0
#             user_proveedor.save()
#             print('USUARIO Y PROVEEDOR CREADO')
#             login(request, user)
#             # return render(request, 'maxproductos/mostrar_Catalogo.html')
#             return redirect(reverse_lazy('/'))
#         else:
#             messages.add_message(request, messages.ERROR, form_user.errors.as_data())
#             form_user = UserForm()
#             form_user_proveedor = ProveedorUserForm()
#             context = {'form_user': form_user,
#                    'form_user_proveedor': form_user_proveedor}        
#     else:
#         print('ENTRE AL ELSE')
        
#         form_user = UserForm()
#         form_user_proveedor = ProveedorUserForm()
#         form_horario = HorarioForm()
#         context = {'form_user': form_user,
#                    'form_user_proveedor': form_user_proveedor}

#     # print(form_user)
#     return render(request, 'registration/registrar_usuario_proveedor.html', context)


def registrar_horario(request):
    context={}
    if request.method == 'POST':
        form_horario = HorarioForm(request.POST)
        # print(' user validado? ',form_user.is_valid())
        if form_horario.is_valid():
            
            # Asignamos los datos propios del USUARIO
            #username= form_user.cleaned_data['username']
            hora_Inicio = request.POST.get('horaInicio')
            hora_Fin = request.POST.get('horaFinal')
            dia = request.POST.get('dia')  

            horario = Horario()
            horario.horaInicio = hora_Inicio
            horario.horaFinal = hora_Fin
            horario.dia = dia
            horario.proveedor = request.user.proveedor
            horario.save()

            #return redirect(reverse_lazy('mostrar_perfil_proveedor_v'))
            return render(request, 'registration/perfil_proveedor.html')
        else:
            # Muestro los errores de los formularios si no pudieron ser validados
            messages.add_message(request, messages.ERROR, form_horario.errors.as_data())
            form_horario = HorarioForm()
            context = {'form_horario': form_horario}
    else: 
        # Si es GET envio un formulario Horario vacio al template
        form_horario = HorarioForm()
        context = {'form_horario': form_horario}

    return render(request, 'registration/registrar_horario.html', context)

class HorarioDelete(DeleteView):
    model = Horario
    # lo mismo que ProductoUpdate
    template_name = 'registration/horario_confirm_delete.html'
    success_url = reverse_lazy('mostrar_Perfil_Proveedor')