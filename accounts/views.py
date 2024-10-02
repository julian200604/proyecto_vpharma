from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Usuario, Rol
from django.urls import reverse
from .forms import RegistroForm
from django.http import HttpResponseRedirect

def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Guarda el usuario
            user = form.save()
            # Obtiene o crea el rol
            rol, created = Rol.objects.get_or_create(nombre='cliente')
            # Crea el objeto Usuario relacionado
            Usuario.objects.create(user=user, rol=rol)

            # Autentica al usuario
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)

            # Mensaje de éxito
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return HttpResponseRedirect(reverse('shop:product_list'))
        else:
            # Mensaje de error con detalles de los errores del formulario
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            messages.error(request, 'Error al registrar el usuario. Revisa los datos ingresados.')
    else:
        form = RegistroForm()
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
                return HttpResponseRedirect(reverse('shop:product_list'))
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Error al autenticar el usuario')
    else:
        if request.session.get('logged_in'):
            return HttpResponseRedirect(reverse('shop:product_list'))
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('shop:product_list')

def perfil(request):
    if request.user.is_authenticated:
        perfil = request.user.perfil
        if request.method == 'POST':
            form = RegistroForm(request.POST, instance=perfil)
            if form.is_valid():
                form.save()
                messages.success(request, 'Perfil actualizado correctamente')
                return redirect('perfil')
        else:
            form = RegistroForm(instance=perfil)
        return render(request, 'accounts/perfil.html', {'form': form})
    else:
        return redirect('login')