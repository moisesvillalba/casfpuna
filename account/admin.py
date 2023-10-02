from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from .models import User, Pais, Ciudad, Barrio

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class UserModelAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'nombre', 'is_active', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('Credenciales de usuario', {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('nombre',)}),
        ('Permisos', {'fields': ('is_admin', 'is_active')}),
        ('Ubicación', {'fields': ('pais', 'ciudad', 'barrio')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'password1', 'password2', 'is_admin', 'is_active', 'pais', 'ciudad', 'barrio'),
        }),
    )
    search_fields = ('documento',)
    ordering = ('email', 'id')
    filter_horizontal = ()
    form = UserAdminForm
    raw_id_fields = ('pais', 'ciudad', 'barrio')

# Registrar el nuevo UserModelAdmin
admin.site.register(User, UserModelAdmin)
admin.site.register(Pais)
admin.site.register(Ciudad)
admin.site.register(Barrio)
