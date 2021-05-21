from django.db import models


# Create your models here.

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    text = models.CharField('pregunta', max_length=300)
    type = models.CharField('tema de competencias ciudadanas', max_length=60)

    class Meta:
        db_table = 'question'
        verbose_name = 'pregunta'
        verbose_name_plural = 'preguntas'


class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField('respuesta', max_length=500)

    class Meta:
        db_table = 'answer'
        verbose_name = 'respuesta'
        verbose_name_plural = 'respuestas'
