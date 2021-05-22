from time import timezone
from tkinter import Entry

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone

from apps.schools.models import School


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    location_father = models.ForeignKey('self', on_delete=models.CASCADE,related_name='location', null=True)
    location_name = models.CharField('nombre de la ubicación', max_length=120)
    location_type = models.CharField('Tipo de ubicación', max_length=30)

    class Meta:
        db_table = 'location'
        verbose_name = 'ubicacion'
        verbose_name_plural = 'ubicaciones'

    # def __str__(self):
    #     return self.name_department + "   " + self.name_municipality


class UserManager(BaseUserManager):
    """Custom User Manager"""

    def _create_user(
            self, first_name, last_name, username, birthday_date, email, password, type_user, school_id,
            is_staff, is_superuser, **extra_fields
    ):
        """
        Create a user. This function is called from the console.
        :param extra_fields: Extra fields that are defined in the REQUIRED_FIELDS constant.
        :return: User
        """
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            birthday_date=birthday_date,
            email=self.normalize_email(email),
            password=password,
            type_user=type_user,
            school_id=School.objects.get(pk=school_id),
            is_staff=is_staff,
            is_superuser=is_superuser,
            terms=True,
            **extra_fields
        )
        user.set_password(password)  # Encriptar contraseña
        user.save(using=self.db)
        return user

    def create_user(
            self, first_name, last_name, username, birthday_date, email, password, school_id, **extra_fields
    ):
        """
        Create a user
        :return: User
        """
        return self._create_user(
            first_name, last_name, username, birthday_date, email, password, User.Type.STUDENT, school_id, False,
            False, **extra_fields
        )

    def create_superuser(
            self, first_name, last_name, username, birthday_date, email, password, school_id,
            **extra_fields
    ):
        """
        Create user with administrator permissions
        :return: User
        """
        return self._create_user(
            first_name, last_name, username, birthday_date, email, password, User.Type.ADMIN, school_id, True,
            True, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    class Type(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        TEACHER = 'TCHR', 'Docente'
        STUDENT = 'STDT', 'Estudiante'
        INVITED = 'IVT', 'Invitado'

    user_id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='teacher_user', null=True, blank=True,
        verbose_name='Docente encargado'
    )
    school_id = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='Colegio')
    first_name = models.CharField('Nombres', max_length=60)
    last_name = models.CharField('Apellidos', max_length=60)
    email = models.EmailField('correo del usuario', unique=True, max_length=50)
    contact_email = models.EmailField('correo del padre de familia', blank=True, null=True, max_length=30)
    birthday_date = models.DateField('fecha de nacimiento')
    photo = models.ImageField(upload_to='users/pictures', blank=True, null=True)
    username = models.CharField(
        'usuario',
        max_length=15,
        unique=True,
        help_text='Su usuario debe tener maximo 15 caracteres. Letras, dígitos y @/./+/-/_ solamente.',
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': 'Ya existe un usuario con este nombre de usuario.',
        },
    )
    type_user = models.CharField('tipo de usuario', max_length=10, choices=Type.choices, default=Type.STUDENT)
    is_active = models.BooleanField(
        'activo',
        default=True,
        help_text='Indica que la cuenta del usuario está activa.'
    )
    is_staff = models.BooleanField(
        'login en admin',
        default=False,
        help_text='Designa si este usuario puede acceder al sitio de administración.'
    )
    terms = models.BooleanField('terminos y condiciones')
    date_creation = models.DateTimeField('fecha de registro', auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'birthday_date', 'school_id']

    class Meta:
        db_table = 'user'
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def type_user_teacher(self):
        return self.type_user.find('Docente')

    def is_adult(self):
        """Verificar si el usuario es mayor de 18 años"""
        age = timezone.now() - self.birthday_date
        return True if age >= 18 else False


class Log(models.Model):
    log_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    log_name = models.CharField('nombre del reporte', max_length=30)
    date_conection = models.DateField(auto_now_add=True)  # ultima fecha de conexion

    class Meta:
        db_table = 'log'
        verbose_name = 'iniciar sesion'
        verbose_name_plural = 'iniciar sesion'
