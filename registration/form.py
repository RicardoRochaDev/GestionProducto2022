from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from sistemadecompra.models import Horario, Proveedor, Cliente,Producto


class UserForm (UserCreationForm):
    first_name = forms.CharField(label='Nombre', max_length=140, required=True)
    last_name = forms.CharField(label='Apellido', max_length=140, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ProveedorUserForm(ModelForm):
    class Meta:
        model = Proveedor # ME VIVO AUTO CAGANDOOOOOO
        exclude = ['user', 'longitud', 'latitud', 'calificacion']
    
    def __init__(self, *args, **kwargs):
        super(ProveedorUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ClienteUserForm(ModelForm):
    class Meta:
        model = Cliente # ME VIVO AUTO CAGANDOOOOOO
        exclude = ['user', 'latitud', 'longitud']
    
    def __init__(self, *args, **kwargs):
        super(ClienteUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
#no sirve
class ProveedorForm(forms.Form):
    nombre= forms.CharField(label='Nombre', required=True, widget= forms.TextInput(
        attrs={'placeholder':'Escribe tu nombre'}
    ))
    apellido= forms.CharField(label='Apellido', required=True)
    direccion= forms.CharField(label='Direccion', required=True)
    telefono= forms.IntegerField(label='Telefono', required=True)
    email= forms.EmailField(label='Email', required=True)
    nombreUsuario= forms.CharField(label='Nombre de usuario', required=True)
    #contrasenia= forms.PasswordInput(label='Contrasenia', required=True)
    descripcionNegocio= forms.CharField(label='Descripcion de negocio', required=True, widget=forms.Textarea)


#NUEVO AGREGADO
class UserSesionForm(forms.Form):
    username= forms.CharField(label='Nombre de Usuario', required=True)
    #password= forms.CharField(label='Contraseña', required=True)
    #password= forms.PasswordInput(label='pass')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
    
    def __init__(self, *args, **kwargs):
        super(UserSesionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


DIAS = [

    ('Lunes', 'Lunes'),
    ('Martes', 'Martes'),
    ('Miercoles', 'Miercoles'),
    ('Jueves', 'Jueves'),
    ('Viernes', 'Viernes'),
    ('Sabado', 'Sabado'),
    ('Domingo', 'Domingo'),
]

class HorarioForm(forms.Form):
    horaInicio = forms.TimeField (label='Hora Inicio', required=True, widget=forms.TimeInput(attrs={'type': 'time'}))
    horaFinal = forms.TimeField (label='Hora Final', required=True, widget=forms.TimeInput(attrs={'type': 'time'}))
    dia= forms.CharField(widget=forms.Select(choices=DIAS))

    class Meta:
        model = Horario
        fields = ['horaInicio','horaFinal','dia']
    
    def __init__(self, *args, **kwargs):
        super(HorarioForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

# class ProveedorUserForm(ModelForm):
#     class Meta:
#         model = Horario # ME VIVO AUTO CAGANDOOOOOO
#         exclude = ['user', 'longitud', 'latitud', 'calificacion']


class ProductoForm(ModelForm):
    descripcion = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Producto
        fields = ['nombre','marca','tipo','descripcion','valor']
    
    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'