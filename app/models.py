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


class Nave(models.Model):
    nome = models.CharField(max_length=100)
    velocidade_mineracao = models.FloatField() 
    capacidade_maxima = models.FloatField() 
    status = models.CharField(max_length=50) 

class Mineracao(models.Model):
    asteroide = models.ForeignKey(Asteroide, on_delete=models.CASCADE)
    nave = models.ForeignKey(Nave, on_delete=models.CASCADE)
    total_minerado = models.FloatField()
    valor_ganho = models.FloatField() 
    data = models.DateTimeField(auto_now_add=True)

class HistoricoExtraecoes(models.Model):
    nave = models.CharField(max_length=100)  
    minerio = models.CharField(max_length=50) 
    quantidade = models.FloatField()
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nave} - {self.minerio}"
    

class AlvoRadar(models.Model):
    nome_alvo = models.CharField(max_length=50) 
    quadrante = models.CharField(max_length=20) 
    minerio_disponivel = models.CharField(max_length=50) 
    volume_estimado = models.FloatField() 
    perigo_nivel = models.CharField(max_length=20, default="Baixo") 

    def __str__(self):
        return f"{self.nome_alvo} ({self.minerio_disponivel})"    