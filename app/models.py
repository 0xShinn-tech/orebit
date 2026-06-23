from django.db import models


class Asteroide(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100) 
    tamanho = models.FloatField() 
    distancia = models.FloatField()
    ferro = models.FloatField()
    niquel = models.FloatField()
    platina = models.FloatField()
    agua = models.FloatField()

    def __str__(self):
        return self.nome

class Mineracao(models.Model):
    asteroide = models.ForeignKey(Asteroide, on_delete=models.CASCADE)
    total_minerado = models.FloatField()
    valor_ganho = models.FloatField() 
    data = models.CharField(max_length=20) 