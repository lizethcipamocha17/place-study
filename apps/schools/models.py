from django.core.validators import FileExtensionValidator
from django.db import models


def upload_to_school(instance, filename):
    return 'school/{filename}'.format(filename=filename)


# Create your models here.
class School(models.Model):
    school_id = models.BigAutoField(primary_key=True)
    location = models.ForeignKey('accounts.Location', on_delete=models.CASCADE, verbose_name='ubicación')
    school_name = models.CharField('nombre del colegio', max_length=120)
    photo = models.ImageField('Logo o escudo de un colegio', upload_to=upload_to_school,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
                              )

    class Meta:
        db_table = 'school'
        verbose_name = 'colegio'
        verbose_name_plural = 'colegios'
        ordering = ['school_name']

    def __str__(self):
        return self.school_name
