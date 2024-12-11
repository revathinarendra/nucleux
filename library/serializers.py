from rest_framework import serializers
from .models import LayerA, LayerB, LayerC, LayerD, LayerE

class LayerESerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerE
        fields = ['id', 'layer_e_name']

class LayerDSerializer(serializers.ModelSerializer):
    layer_es = LayerESerializer(many=True, read_only=True)

    class Meta:
        model = LayerD
        fields = ['id', 'layer_d_name', 'slug', 'layer_es']

class LayerCSerializer(serializers.ModelSerializer):
    layer_ds = LayerDSerializer(many=True, read_only=True)

    class Meta:
        model = LayerC
        fields = ['id', 'layer_c_name', 'slug', 'layer_ds']

class LayerBSerializer(serializers.ModelSerializer):
    layer_cs = LayerCSerializer(many=True, read_only=True)

    class Meta:
        model = LayerB
        fields = ['id', 'layer_b_name', 'slug', 'layer_cs']

class LayerASerializer(serializers.ModelSerializer):
    layer_bs = LayerBSerializer(many=True, read_only=True)

    class Meta:
        model = LayerA
        fields = ['id', 'layer_a_name', 'slug', 'layer_bs']
