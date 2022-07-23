from django import forms


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
