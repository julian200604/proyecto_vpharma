from django.http import HttpResponseNotFound
from django.template import loader
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import resolve

class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            template = loader.get_template('404.html')
            return HttpResponseNotFound(template.render())
        return response

class SessionVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_url = resolve(request.path_info).url_name
            if current_url not in ['login', 'logout']:  # Agrega aquí otras URLs que quieras excluir
                if not request.session.get('is_valid', False):
                    logout(request)
                    return redirect('login')
        response = self.get_response(request)
        return response
