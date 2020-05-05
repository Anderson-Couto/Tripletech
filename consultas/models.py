from django.db import models


# Create your models here.
class Agenda(models.Model):
    objects = models.Manager()
    numero_pessoas = models.IntegerField()
    ids_pessoas = models.CharField(max_length=200)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()

    class Meta:
        db_table = "agenda"