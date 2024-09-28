from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Usuario, Rol
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.is_superuser:
                return redirect('login')
            else:
                rol = Rol.objects.get(nombre='cliente')
                usuario = Usuario(user=user, rol=rol)
                usuario.save()
                return redirect('login')
        else:
            messages.error(request, 'Error al crear el usuario')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['logged_in'] = True
                return redirect('perfil')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Error al autenticar el usuario')
    else:
        if request.session.get('logged_in'):
            return redirect('tienda')
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('shop:product_list')

def perfil(request):
    request.session['logged_in'] = True
    if request.user.is_superuser:
        return redirect('admin:index')
    else:
        return render(request, 'accounts/perfil.html')