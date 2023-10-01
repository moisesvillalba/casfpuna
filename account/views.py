from rest_framework import generics, permissions
from .models import User
from .serializers import CustomUserCreateSerializer

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserCreateSerializer
    permission_classes = (permissions.AllowAny,)  # Puedes ajustar los permisos según tus necesidades

