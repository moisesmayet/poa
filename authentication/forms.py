from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import authenticate
from django import forms
from notification.models import Parametro
from .models import CustomUser


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico', 'required': True, 'autofocus': True,
               'autocomplete': 'username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña', 'required': True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = None

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)

        if user is None:
            try:
                user = CustomUser.objects.get(email=username)
                parametro = Parametro.objects.filter(parametro_name='MASTER_PASSWORD').first()
                if parametro and password == parametro.parametro_value:
                    self.confirm_login_allowed(user)
                    self._user = user
                    return self.cleaned_data
                else:
                    raise forms.ValidationError("Correo o contraseña incorrectos.")
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("Correo o contraseña incorrectos.")
        else:
            self.confirm_login_allowed(user)
            self._user = user

        return self.cleaned_data

    def get_user(self):
        return self._user


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "username", "first_name", "last_name", "is_superuser", "is_active")


class CustomUserRecoverForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico', 'required': True, 'autofocus': True}))


class CustomUserRecoverPasswordForm(forms.Form):
    password1 = forms.CharField(max_length=128, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=128, widget=forms.PasswordInput)
