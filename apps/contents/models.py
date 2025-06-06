import os.path

from django.db import models
from django.core.validators import FileExtensionValidator


# Create your models here.
from apps.accounts.models import User


def upload_to(instance, filename):
    return 'content/{filename}'.format(filename=filename)


def upload_to_document(instance, filename):
    return 'content/documents/{filename}'.format(filename=filename)


class Content(models.Model):
    content_id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Nombre del autor del contenido')
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


class DocumentContent(models.Model):
    """Document Content model"""

    class FileType(models.TextChoices):
        PDF = 'PDF', 'Archivo PDF'
        WORD = 'WORD', 'Archivo WORD'
        PPTX = 'POWER_POINT', 'Archivo POWER POINT'
        URL = 'URL', 'Enlace del archivo'

    content = models.ForeignKey(
        Content, verbose_name='contenido', related_name='documents', on_delete=models.CASCADE
    )
    file = models.FileField('archivo', upload_to=upload_to_document, null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['docx', 'pdf', 'pptx'])
    ])
    url = models.URLField('enlace del documento', null=True, blank=True)
    file_type = models.CharField('tipo de archivo', max_length=11, choices=FileType.choices)

    class Meta:
        db_table = 'document_content'
        verbose_name = 'documento extra por publicación'
        verbose_name_plural = 'documentos extra por publicación'

    def _str_(self):
        return self.file.name

    @property
    def file_name(self):
        return os.path.basename(self.file.name)


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
