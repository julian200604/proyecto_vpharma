from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib import messages
from .models import Usuario, Rol, Perfil
from django.urls import reverse
from .forms import RegistroForm, EditarPerfilForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse

# Registro de usuario cliente
def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            rol, created = Rol.objects.get_or_create(nombre='cliente')
            Usuario.objects.create(user=user, rol=rol)

            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
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
                if user.is_superuser:
                    return redirect('admin:index')
                else:
                    return redirect('perfil')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Error al autenticar el usuario')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def perfil(request):
    if request.user.is_superuser:
        return redirect('admin:index')
    
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        perfil = Perfil.objects.create(user=request.user)

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = EditarPerfilForm(instance=perfil)

    return render(request, 'accounts/perfil.html', {'form': form, 'perfil': perfil})

@login_required
def editar_perfil(request):
    perfil = request.user.perfil
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = EditarPerfilForm(instance=perfil)

    return render(request, 'accounts/editar_perfil.html', {'form': form})

# Cerrar sesión correctamente
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('shop:product_list')

# Recuperación de contraseña
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = Usuario.objects.filter(user__email=data)
            if associated_users.exists():
                print(f"Usuarios asociados encontrados: {associated_users}")  # Depuración
                for user in associated_users:
                    subject = "Petición de restablecimiento de contraseña"
                    email_template_name = "accounts/password_reset_email.txt"
                    c = {
                        "email": user.user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Mi proyecto local',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        print(f"Enviando correo a: {user.user.email}")  # Depuración antes de enviar
                        send_mail(subject, email, 'julianurrea2006@gmail.com', [user.user.email], fail_silently=False)
                        print(f"Correo enviado a: {user.user.email}")  # Depuración
                    except BadHeaderError:
                        print('Invalid header found.')  # Depuración
                    except Exception as e:
                        print(f"Error al enviar correo: {e}")  # Captura de cualquier otro error

                # Redireccionar después de enviar el correo
                return redirect("password_reset_done")  # Usa el nombre de la URL
            else:
                print(f"No se encontraron usuarios asociados para el correo: {data}")  # Depuración
                # Considera agregar un mensaje de error para el usuario
    else:
        password_reset_form = PasswordResetForm()

    return render(request, "accounts/password_reset.html", {"password_reset_form": password_reset_form})

def password_reset_done(request):
    return render(request, 'accounts/password_reset_done.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Usuario.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
        else:
            form = SetPasswordForm(user)
        return render(request, 'accounts/password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'accounts/password_reset_invalid.html')

def password_reset_complete(request):
    return render(request, 'accounts/password_reset_complete.html')