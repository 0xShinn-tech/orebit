from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import AlvoRadar, Asteroide, Nave, Mineracao ,HistoricoExtraecoes
from .serializers import AlvoRadarSerializer, AsteroideSerializer, NaveSerializer, MineracaoSerializer, HistoricoSerializer


class AsteroideViewSet(viewsets.ModelViewSet):
    queryset = Asteroide.objects.all() 
    serializer_class = AsteroideSerializer

class NaveViewSet(viewsets.ModelViewSet):
    queryset = Nave.objects.all() 
    serializer_class = NaveSerializer


class MineracaoViewSet(viewsets.ModelViewSet):
    queryset = Mineracao.objects.all() 
    serializer_class = MineracaoSerializer

class HistoricoViewSet(viewsets.ModelViewSet):
    queryset = HistoricoExtraecoes.objects.all().order_by('-data') 
    serializer_class = HistoricoSerializer
    permission_classes = [AllowAny]  

class AlvoRadarViewSet(viewsets.ModelViewSet):
    queryset = AlvoRadar.objects.all()
    serializer_class = AlvoRadarSerializer
    permission_classes = [AllowAny]    