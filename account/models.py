from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class Pais(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Departamento(models.Model):
    nombre = models.CharField(max_length=255)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='ciudades')

    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    nombre = models.CharField(max_length=255)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='departamentos+')

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
    email_alternativo = models.EmailField(
        verbose_name='Correo electrónico alternativo',
        max_length=255,
        unique=True,
        null = True,
    )
    nombre = models.CharField(max_length=255, null = False)
    apellido = models.CharField(max_length=255, null = False)
    documento = models.CharField(max_length=10, unique=True, verbose_name='Documento', null= False)  
    telefono = models.CharField(max_length=30, null = False)
    fecha_nacimiento = models.DateField(null=False)
    pais_nacimiento = models.ForeignKey(Pais, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='País Nacimiento')
    departamento_nacimiento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Departamento Nacimiento')
    ciudad_nacimiento = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Ciudad Nacimiento')
    barrio_nacimiento = models.ForeignKey(Barrio, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Barrio Nacimiento')
    tiene_residencia = models.BooleanField(default=False)
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, blank=False, null=False, verbose_name='País')
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, blank=False, null=False, verbose_name='Departamento')
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, blank=False, null=False, verbose_name='Ciudad')
    barrio = models.ForeignKey(Barrio, on_delete=models.SET_NULL, blank=False, null=False, verbose_name='Barrio')
    direccion_particular = models.CharField(max_length=255, null = False)
    sexo = models.CharField(max_length=2, null= True, blank= True)
    cedula_duplicada = models.BooleanField(default=False)
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
