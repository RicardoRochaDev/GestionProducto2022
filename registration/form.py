from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from sistemadecompra.models import Proveedor, Cliente


class UserForm (UserCreationForm):
    first_name = forms.CharField(max_length=140, required=True)
    last_name = forms.CharField(max_length=140, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']


class ProveedorUserForm(ModelForm):
    class Meta:
        model = Proveedor # ME VIVO AUTO CAGANDOOOOOO
        exclude = ['user', 'longitud', 'latitud', 'calificacion']

class ClienteUserForm(ModelForm):
    class Meta:
        model = Cliente # ME VIVO AUTO CAGANDOOOOOO
        exclude = ['user', 'latitud', 'longitud']
    
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