from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms

from .models import CustomUser


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico', 'required': True, 'autofocus': True, 'autocomplete': 'username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña', 'required': True}))


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
