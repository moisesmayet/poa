
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from google.oauth2 import id_token
from google.auth.transport import requests
from config.settings import GOOGLE_OAUTH_CLIENT_ID
from poa.models import POA
from poa.views import RegistrarLog
from uapa.models import Colaborador, Estamento
from .forms import *
from notification.views import SendMail, GetURL


class AuthReceiver(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        token = request.POST.get('credential')
        if not token:
            return HttpResponse(status=400)

        try:
            user_data = id_token.verify_oauth2_token(
                token, requests.Request(), GOOGLE_OAUTH_CLIENT_ID
            )
        except ValueError:
            return HttpResponse(status=403)

        email = user_data.get('email')
        if not email:
            messages.error(request, "Error al obtener el correo electrónico de Google.")
            return redirect("login")
        elif user_data.get('hd') != "uapa.edu.do":
            messages.error(request, "Solo se permiten correos de la UAPA(uapa.edu.do)")
            return redirect("login")

        user = CustomUser.objects.filter(email=email).first()
        if not user:
            messages.error(request, f"Usuario({email}) no está registrado en el PopIn")
            return redirect("login")

        if user.is_active:
            try:
                login(request, user)
                if user.activation_key != '':
                    user.activation_key = ''
                    user.save()
                return redirect("home")
            except Exception as e:
                messages.error(request, f"Error al iniciar sesión: {str(e)}")
        else:
            messages.error(request, "Usuario suspendido. Póngase en contacto con el administrador.")

        return redirect("login")


class Login(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            form = CustomAuthenticationForm()
            return render(request, F"login.html", {"form": form})

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                if user.is_active:
                    request.session.modified = True
                    try:
                        login(request, user)
                        if user.activation_key != '':
                            user.activation_key = ''
                            user.save()
                    except Exception as e:
                        raise Exception(str(e))
                    RegistrarLog(0, 0, user, 'Login', 'Inicio de sección')
                    colaboradores_ids = Colaborador.objects.filter(colaborador_user=user).values_list(
                        'colaborador_estamento', flat=True
                    )

                    # Inicializar con los poas sin incluir los subs
                    estamentos_main = Estamento.objects.filter(estamento_user=user, estamento_has_poa=True)
                    estamentos_colaboradores = Estamento.objects.filter(id__in=colaboradores_ids)
                    estamentos = estamentos_main.union(estamentos_colaboradores, all=True)
                    estamentos_ids = [estamento.id for estamento in estamentos]
                    POA.objects.filter(poa_estamento_id__in=estamentos_ids).update(poa_include_subs=False)
                    return redirect("home")
                else:
                    messages.error(request, F"Usuario suspendido. Póngase en contacto con el administrador")
            else:
                messages.error(request, F"Correo o contraseña incorrecta")
        else:
            messages.error(request, F"Los datos son incorrectos")

        form = CustomAuthenticationForm()
        return render(request, F"login.html", {"form": form})


class Account(View):
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            usuario = CustomUser.objects.get(email=user.email)
            return render(request, "account.html", {"usuario": usuario})
        return redirect("home")

    # noinspection PyMethodMayBeStatic
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user_id = request.POST.get('id', '')
            custon_user = CustomUser.objects.get(id=user_id)

            custon_user.email = request.POST.get('email', '').strip()
            custon_user.username = request.POST.get('first_name', '').upper().strip()
            custon_user.first_name = request.POST.get('first_name', '').upper().strip()
            custon_user.last_name = request.POST.get('last_name', '').upper().strip()

            custon_user.save()
            messages.success(request, F"Datos guardados")

            return redirect("account")

        return redirect("home")


class Confirm(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        activation_key = request.POST.get('activation_key', '')

        # Verifica que el usuario ya está logeado
        if not request.user.is_authenticated and activation_key != '':
            user = CustomUser.objects.filter(activation_key=activation_key).first()
            if user is not None:
                user.activation_key = ''
                user.is_active = True
                user.save()

                login(request, user)
                messages.success(request, F"Hola " + user.username + ", tu usuario fue activado correctamente")
            else:
                messages.error(request,
                               F"Código de activación caducado o incorrecto. Puede usar la opción de recupar contraseña si lo necesita")

        return redirect("home")


class Recover(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        if not request.user.is_authenticated:
            form = CustomUserRecoverForm()
            return render(request, "recover.html", {"form": form})

        return redirect("home")

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        if not request.user.is_authenticated:
            form = CustomUserRecoverForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get("email")
                user = CustomUser.objects.filter(email=email).first()
                if user is not None:
                    activation_key = get_random_string(length=40)
                    user.activation_key = activation_key
                    user.save()

                    # Enviar un email de confirmación
                    domain = "http://" + request.META['HTTP_HOST']
                    subject = 'Confirmación de registro'
                    template = 'basic_email.html'
                    message = "Se ha solicitado una recuperación de contraseña. Para recuerar su contraseña haga clíck en el siguiente enlace: " + domain + "/accounts/recover_password/" + activation_key

                    firma = GetURL(request) + "static/images/logo/popin_firma.png"
                    SendMail(user.username, email, subject, template, message, "", firma)

                    messages.success(request, F"Se envió un enlace a su correo para cambiar la contraseña")
                    return redirect("login")
                else:
                    messages.error(request, "No existe usuario con el correo proporcionado")
                    form = CustomUserRecoverForm(initial={"email": email})
            else:
                messages.error(request, "Los datos son incorrectos")
                form = CustomUserRecoverForm()

            return render(request, "recover.html", {"form": form})

        return redirect("home")


class RecoverPassword(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request, activation_key):
        if activation_key != '':
            user = CustomUser.objects.filter(activation_key=activation_key).first()
            if user is not None:
                form = CustomUserRecoverPasswordForm()
                return render(request, F"recover_password.html", {"form": form})

        messages.error(request, F"Código de activación caducado")
        return redirect("home")

    # noinspection PyMethodMayBeStatic
    def post(self, request, activation_key):
        if request.method == "POST":
            form = CustomUserRecoverPasswordForm(request.POST)
            if form.is_valid() and activation_key != '':
                user = CustomUser.objects.filter(activation_key=activation_key).first()
                if user is not None:
                    user.password = make_password(str(form.cleaned_data.get("password1")))
                    user.activation_key = ''
                    user.save()

                    messages.success(request, F"Su contraseña se ha cambiado correctamente")
                    return redirect("login")
                else:
                    messages.error(request, F"Código de activación caducado")
            else:
                messages.error(request, F"Las contraseñas no coinciden y/o están vacías")

            form = CustomUserRecoverPasswordForm()
            return render(request, F"recover_password.html", {"form": form})


class UpdatePassword(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        if request.user is not None:
            form = CustomUserRecoverPasswordForm()
            return render(request, F"recover_password.html", {"form": form})

        return redirect("home")

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        if request.method == "POST":
            form = CustomUserRecoverPasswordForm(request.POST)
            if form.is_valid():
                user = request.user
                if user is not None:
                    user.password = make_password(str(form.cleaned_data.get("password1")))
                    user.activation_key = ''
                    user.save()

                    messages.success(request, F"Su contraseña se ha cambiado correctamente")
                    return redirect("home")
                else:
                    messages.error(request, F"Código de activación caducado")
            else:
                messages.error(request, F"Las contraseñas no coinciden o están vacías")

            form = CustomUserRecoverPasswordForm()
            return render(request, F"recover_password.html", {"form": form})


class Logout(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        logout(request)
        messages.success(request, F"Tu sesión se ha cerrado correctamente")
        return redirect("home")
