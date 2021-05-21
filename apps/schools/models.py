from django.db import models


# Create your models here.
class School(models.Model):
    school_id = models.AutoField(primary_key=True)
    location_id = models.ForeignKey('accounts.Location', on_delete=models.CASCADE, verbose_name='Departamento')
    school_name = models.CharField('nombre del colegio', max_length=120)

    class Meta:
        db_table = 'school'
        verbose_name = 'colegio'
        verbose_name_plural = 'colegios'
        ordering = ['school_name']

    def __str__(self):
        return self.school_name


class Content(models.Model):
    content_id = models.AutoField(primary_key=True)
    school_id = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField('Nombre de la Publicación', max_length=60)
    description = models.CharField('Descripción de la publicación', max_length=60)
    image = models.ImageField('Imagen de la publicación', upload_to='content/image')

    class Meta:
        db_table = 'content'
        verbose_name = 'contenido'
        verbose_name_plural = 'contenidos'


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    content_id = models.ForeignKey(Content, on_delete=models.CASCADE)
    user_id = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    text = models.CharField('comentario', max_length=100)
    like = models.BooleanField('Me gusta')

    class Meta:
        db_table = 'comment'
        verbose_name = 'comentario'
        verbose_name_plural = 'comentarios'
