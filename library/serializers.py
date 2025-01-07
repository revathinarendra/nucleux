from rest_framework import serializers
from .models import LayerA, LayerB, LayerC, LayerD, LayerE, LayerF  
import json


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


# class LayerFSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LayerF
#         fields = ['id', 'layer_e_name', 'layer_f_name','layer_f_note']



class LayerFSerializer(serializers.ModelSerializer):
    layer_f_note = serializers.JSONField(required=False)

    class Meta:
        model = LayerF
        fields = ['id', 'layer_e_name', 'layer_f_name', 'layer_f_note']

    # def to_representation(self, instance):
    #     """Convert the JSON string back to a dictionary for output."""
    #     representation = super().to_representation(instance)
    #     try:
    #         representation['layer_f_note'] = instance.get_layer_f_note_json()
    #     except json.JSONDecodeError:
    #         representation['layer_f_note'] = None
    #     return representation

    # def update(self, instance, validated_data):
    #     """Handle JSON serialization during update."""
    #     layer_f_note = validated_data.pop('layer_f_note', None)
    #     if layer_f_note is not None:
    #         instance.set_layer_f_note_json(layer_f_note)
    #     return super().update(instance, validated_data)

    # def create(self, validated_data):
    #     """Handle JSON serialization during creation."""
    #     layer_f_note = validated_data.pop('layer_f_note', None)
    #     instance = super().create(validated_data)
    #     if layer_f_note is not None:
    #         instance.set_layer_f_note_json(layer_f_note)
    #         instance.save()
    #     return instance
