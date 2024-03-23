from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Gestor de usuarios personalizado
class UserManager(BaseUserManager):
    def create_user(self, email, nombre, apellido, documento, telefono, fecha_nacimiento, ciudad_nacimiento=None, pais_nacimiento=None, barrio_nacimiento=None, is_admin=False, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener una dirección de correo electrónico')
        user = self.model(
            email=self.normalize_email(email),
            nombre=nombre,
            apellido=apellido,
            documento=documento,
            telefono=telefono,
            fecha_nacimiento=fecha_nacimiento,
            ciudad_nacimiento=ciudad_nacimiento,
            pais_nacimiento=pais_nacimiento,
            barrio_nacimiento=barrio_nacimiento,
            is_admin=is_admin,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, nombre, apellido, documento, telefono, fecha_nacimiento, ciudad_nacimiento=None, pais_nacimiento=None, barrio_nacimiento=None, is_admin=True, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        return self.create_user(email, nombre, apellido, documento, telefono, fecha_nacimiento, ciudad_nacimiento, pais_nacimiento, barrio_nacimiento, is_admin=True, password=password, **extra_fields)

# Modelo de usuario personalizado
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Correo electrónico',
        max_length=255,
        unique=True,
    )
    email_alternativo = models.EmailField(
        verbose_name='Correo electrónico alternativo',
        max_length=255,
        unique=True,
        null=True,
    )
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    documento = models.CharField(max_length=10, unique=True, verbose_name='Documento')
    telefono = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField()
    direccion_particular = models.CharField(max_length=255)
    sexo = models.CharField(max_length=2, null=True, blank=True)
    cedula_duplicada = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edad = models.IntegerField(default=0)  # Agregar el campo 'edad'

    objects = UserManager()

    USERNAME_FIELD = 'documento'
    REQUIRED_FIELDS = ['email', 'nombre', 'apellido']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.nombre} {self.apellido}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
