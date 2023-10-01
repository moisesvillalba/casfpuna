from django.urls import path, include
from .views import CreateUserView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
        # Ruta para la vista de creación de usuarios
    path('api/register/', CreateUserView.as_view(), name='register'),

    # Ruta para obtener tokens de autenticación (si se utiliza)
    path('api/token/', obtain_auth_token, name='token'),
]
