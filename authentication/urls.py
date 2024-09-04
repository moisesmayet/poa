from django.urls import path
from .views import *

urlpatterns = [
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('account/', Account.as_view(), name="account"),
    path('confirm/<str:activation_key>', Confirm.as_view(), name="confirm"),
    path('recover', Recover.as_view(), name="recover"),
    path('recover_password/<str:activation_key>', RecoverPassword.as_view(), name="recover_password"),
    path('update_password/', UpdatePassword.as_view(), name="update_password"),
]
