from django.db import models


# Create your models here.

class Question(models.Model):
    question_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user',
                             verbose_name='Nombre de Usuario')
    text = models.CharField('pregunta', max_length=300)
    type = models.CharField('tema de competencias ciudadanas', max_length=60)
    created_at = models.DateTimeField('fecha de creación', auto_now_add=True)

    class Meta:
        db_table = 'question'
        verbose_name = 'pregunta'
        verbose_name_plural = 'preguntas'


class Answer(models.Model):
    answer_id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField('respuesta', max_length=500)
    created_at = models.DateTimeField('fecha de creación', auto_now_add=True)

    class Meta:
        db_table = 'answer'
        verbose_name = 'respuesta'
        verbose_name_plural = 'respuestas'
