from django.db import models
from django.contrib.auth.models import  BaseUserManager,AbstractBaseUser, PermissionsMixin
from django.db.models.deletion import CASCADE




class UsuarioAdmin(BaseUserManager):
    def _create_user(self,username,email,nombres,password,is_staff,is_superuser,**extra_fields):
        usuario = self.model(
            username = username,
            email = email,
            nombres = nombres,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        usuario.set_password(password)
        usuario.save(using=self.db)
        return usuario
    def create_user(self,username, email, nombres, password=None,**extra_fields):
        return self._create_user(username,email,nombres,password,True, False,**extra_fields)

    def create_superuser(self,username,email,nombres,password=None,**extra_fields):
        return self._create_user(username,email,nombres,password,True, True,**extra_fields)
      

class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Nombre de usuario', unique=True, max_length=50)
    #Agrgar RFC
    #Gestion de usuario con diferentes roles, diferenciar.
    email = models.CharField('Correo Electrónico', unique=True, max_length=254)
    nombres = models.CharField('Nombres', max_length=200, blank=True, null=True)
    apellidos = models.CharField('Apellidos', max_length=200, blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UsuarioAdmin()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [ 'email','nombres']

    def __str__(self):
        return f'{self.username}'