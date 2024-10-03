from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil

class AuthenticationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario', 'class': 'form-control'})
    )
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'form-control'})
    )


class RegistroForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}))
    nombre_completo = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Nombre completo'}))
    telefono = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Número de teléfono'}))
    fecha_nacimiento = forms.DateField(required=False, widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    direccion = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Dirección'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirma tu contraseña'}))


    class Meta:
        model = User
        fields = ('username', 'email', 'nombre_completo', 'telefono', 'fecha_nacimiento', 'direccion', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            user.save()  # Guarda el usuario
            perfil = Perfil(
                user=user,
                nombre_completo=self.cleaned_data['nombre_completo'],
                telefono=self.cleaned_data['telefono'],
                fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
                direccion=self.cleaned_data['direccion']
            )
            perfil.save()  # Guarda el perfil
        return user
    
    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        self.fields['nombre_completo'].widget.attrs.update({'class': 'mi-clase'})

class EditarPerfilForm(forms.ModelForm):
    username = forms.CharField(max_length=150)

    class Meta:
        model = Perfil
        fields = ('nombre_completo', 'telefono', 'fecha_nacimiento', 'direccion')

    def __init__(self, *args, **kwargs):
        super(EditarPerfilForm, self).__init__(*args, **kwargs)
        self.fields['username'].initial = self.instance.user.username

    def save(self, commit=True):
        user = self.instance.user
        user.username = self.cleaned_data['username']
        user.save()
        return super(EditarPerfilForm, self).save(commit)