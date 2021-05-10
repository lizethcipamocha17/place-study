from django.db import models


# Create your models here.
class School(models.Model):
    id_school = models.AutoField(primary_key=True)
    code_dane = models.CharField('codigo dane del colegio', max_length=30)
    location = models.ForeignKey('accounts.Location', on_delete=models.CASCADE)
    name_school = models.CharField('nombre del colegio', max_length=120)
    name_calendar = models.CharField('tipo calendario', null=True, max_length=20)
    address = models.CharField('dirección del colegio', null=True, max_length=120)

    class Meta:
        db_table = 'school'
        verbose_name = 'colegio'
        verbose_name_plural = 'colegios'

    # def __str__(self):
    #     return self.name_school


class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name_category = models.CharField('nombre categoria', max_length=50)
    description = models.CharField('descripcion', max_length=60)

    class Meta:
        db_table = 'category'
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'


class Content(models.Model):
    id_content = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name_content = models.CharField('Nombre de la Publicación', max_length=60)
    description = models.CharField('Descripción de la publicación', max_length=150)
    image = models.ImageField('Imagen de la publicación', upload_to='content/image', blank=True)

    class Meta:
        db_table = 'content'
        verbose_name = 'contenido'
        verbose_name_plural = 'contenidos'
