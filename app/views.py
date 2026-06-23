from django.shortcuts import render
from rest_framework import viewsets
from .models import Asteroide, Nave, Mineracao
from .serializers import AsteroideSerializer, NaveSerializer, MineracaoSerializer

# API de Asteroides
class AsteroideViewSet(viewsets.ModelViewSet):
    queryset = Asteroide.objects.all() 
    serializer_class = AsteroideSerializer

# API de Mineracoes
class MineracaoViewSet(viewsets.ModelViewSet):
    queryset = Mineracao.objects.all() 
    serializer_class = MineracaoSerializer