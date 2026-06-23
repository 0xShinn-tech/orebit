from rest_framework import serializers
from .models import Asteroide, Nave, Mineracao

# Serializer do Asteroide
class AsteroideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asteroide
        fields = '__all__'

# Serializer da Mineracao
class MineracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mineracao
        fields = '__all__'