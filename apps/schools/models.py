from django.core.validators import FileExtensionValidator
from django.db import models


def upload_to(instance ,filename):
    return 'content/{filename}'.format(filename=filename)


# Create your models here.
class School(models.Model):
    school_id = models.BigAutoField(primary_key=True)
    location = models.ForeignKey('accounts.Location', on_delete=models.CASCADE, related_name='School',
                                 verbose_name='Departamento')
    school_name = models.CharField('nombre del colegio', max_length=120)

    class Meta:
        db_table = 'school'
        verbose_name = 'colegio'
        verbose_name_plural = 'colegios'
        ordering = ['school_name']

    # def __str__(self):
    #     return self.school_name


class Content(models.Model):
    content_id = models.BigAutoField(primary_key=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='Nombre del Colegio')
    name = models.CharField('Nombre de la Publicación', max_length=60)
    description = models.CharField('Descripción de la publicación', max_length=100)
    image = models.ImageField(
        'Imagen de la publicación', upload_to=upload_to,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    created_at = models.DateTimeField('fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('fecha de actualización', auto_now=True)

    class Meta:
        db_table = 'content'
        verbose_name = 'contenido'
        verbose_name_plural = 'contenidos'

    def __str__(self):
        return self.name


class Comment(models.Model):
    comment_id = models.BigAutoField(primary_key=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE,
                             verbose_name=' Nombre de usuario')
    text = models.CharField('comentario', max_length=100)
    created_at = models.DateTimeField('fecha de creación', auto_now_add=True)

    class Meta:
        db_table = 'comment'
        verbose_name = 'comentario'
        verbose_name_plural = 'comentarios'


class Like(models.Model):
    like_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE,
                             verbose_name='like')
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    like = models.BooleanField('Me gusta')

    class Meta:
        db_table = 'like'
        verbose_name = 'Me gusta'
        verbose_name_plural = 'Me gustas'
