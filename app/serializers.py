from rest_framework import serializers
from .models import AlvoRadar, Asteroide, Nave, Mineracao

class AsteroideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asteroide
        fields = '__all__'

class NaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nave
        fields = '__all__'

class MineracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mineracao
        fields = '__all__'
from rest_framework import serializers
from .models import HistoricoExtraecoes

class HistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoExtraecoes
        fields = '__all__' 




class AlvoRadarSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlvoRadar
        fields = '__all__'

