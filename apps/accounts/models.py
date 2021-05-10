from time import timezone

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone

from apps.schools.models import School


class Location(models.Model):
    id_location = models.AutoField(primary_key=True)
    code_department = models.IntegerField('codigo departamento')
    code_municipality = models.IntegerField('codigo municipio')
    name_department = models.CharField('nombre departamento', max_length=60)
    name_municipality = models.CharField('nombre municipio', max_length=60)

    class Meta:
        db_table = 'location'
        verbose_name = 'ubicacion'
        verbose_name_plural = 'ubicaciones'

    # def __str__(self):
    #     return self.name_department, self.name_municipality


class UserManager(BaseUserManager):
    """Custom User Manager"""

    def _create_user(
            self, first_name, last_name, username, date_of_birth, email, password, type_user, location, school,
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
            date_of_birth=date_of_birth,
            email=self.normalize_email(email),
            password=password,
            type_user=type_user,
            location=Location.objects.get(pk=location),
            school=School.objects.get(pk=school),
            is_staff=is_staff,
            is_superuser=is_superuser,
            terms=True,
            **extra_fields
        )
        user.set_password(password)  # Encriptar contraseña
        user.save(using=self.db)
        return user

    def create_user(
            self, first_name, last_name, username, date_of_birth, email, password, location, school, **extra_fields
    ):
        """
        Create a user
        :return: User
        """
        return self._create_user(
            first_name, last_name, username, date_of_birth, email, password, User.Type.STUDENT, location, school, False,
            False, **extra_fields
        )

    def create_superuser(
            self, first_name, last_name, username, date_of_birth, email, password, location, school, **extra_fields
    ):
        """
        Create user with administrator permissions
        :return: User
        """
        return self._create_user(
            first_name, last_name, username, date_of_birth, email, password, User.Type.ADMIN, location, school, True,
            True,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    class Type(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        STUDENT = 'STDT', 'Estudiante'
        INVITED = 'IVT', 'Invitado'

    id_user = models.AutoField(primary_key=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    first_name = models.CharField('Nombres del usuario', max_length=60)
    last_name = models.CharField('Apellidos del usuario', max_length=60)
    email = models.EmailField('correo del usuario', unique=True, max_length=60)
    contact_email = models.EmailField('correo del padre de familia', blank=True, null=True, max_length=60)
    date_of_birth = models.DateField('fecha de nacimiento')
    photo = models.ImageField(upload_to='users/pictures', blank=True)
    username = models.CharField(
        'usuario',
        max_length=60,
        unique=True,
        help_text='Su usuario debe tener maximo 60 caracteres. Letras, dígitos y @/./+/-/_ solamente.',
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': 'Ya existe un usuario con este nombre de usuario.',
        },
    )
    type_user = models.CharField('tipo de usuario', max_length=8, choices=Type.choices, default=Type.STUDENT)
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
    created_at = models.DateTimeField('fecha de registro', auto_now_add=True)
    updated_at = models.DateTimeField('fecha de modificación de la cuenta', auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'date_of_birth', 'location', 'school']

    class Meta:
        db_table = 'user'
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def is_adult(self):
        """Verificar si el usuario es mayor de 18 años"""
        age = timezone.now() - self.date_of_birth
        return True if age >= 18 else False


class Report(models.Model):
    id_report = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('nombre del reporte', max_length=60)
    type = models.CharField('tipo de reporte', max_length=60)
    date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'report'
        verbose_name = 'reporte'
        verbose_name_plural = 'reportes'
