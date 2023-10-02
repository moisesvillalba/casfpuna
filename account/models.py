from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class Pais(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    nombre = models.CharField(max_length=255)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='ciudades')

    def __str__(self):
        return self.nombre

class Barrio(models.Model):
    nombre = models.CharField(max_length=255)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, related_name='barrios')

    def __str__(self):
        return self.nombre

# Gestor de usuarios personalizado
class UserManager(BaseUserManager):
    def create_user(self, email, nombre, documento, ciudad=None, pais=None, barrio=None, is_admin=False, password=None):
        if not email:
            raise ValueError('El usuario debe tener una dirección de correo electrónico')
        user = self.model(
            email=self.normalize_email(email),
            nombre=nombre,
            documento=documento,
            ciudad=ciudad,
            pais=pais,
            barrio=barrio,
            is_admin=is_admin
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, nombre, documento, ciudad=None, pais=None, barrio=None, is_admin=True, password=None):
        user = self.create_user(
            email=email,
            password=password,
            nombre=nombre,
            documento=documento,
            ciudad=ciudad,
            pais=pais,
            barrio=barrio,
            is_admin=is_admin
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Modelo de usuario personalizado
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Correo electrónico',
        max_length=255,
        unique=True,
    )
    nombre = models.CharField(max_length=255)
    documento = models.CharField(max_length=10, unique=True, verbose_name='Documento', default='')  
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Ciudad')
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='País')
    barrio = models.ForeignKey(Barrio, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Barrio')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'documento'
    REQUIRED_FIELDS = ['email', 'nombre', 'is_admin']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.nombre

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
