from rest_framework import serializers
from .models import LayerA, LayerB, LayerC, LayerD, LayerE

# class LayerESerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LayerE
#         fields = ['id', 'layer_e_name']

# class LayerDSerializer(serializers.ModelSerializer):
#     layer_es = LayerESerializer(many=True, read_only=True)

#     class Meta:
#         model = LayerD
#         fields = ['id', 'layer_d_name', 'slug', 'layer_es']

# class LayerCSerializer(serializers.ModelSerializer):
#     layer_ds = LayerDSerializer(many=True, read_only=True)

#     class Meta:
#         model = LayerC
#         fields = ['id', 'layer_c_name', 'slug', 'layer_ds']

# class LayerBSerializer(serializers.ModelSerializer):
#     layer_cs = LayerCSerializer(many=True, read_only=True)

#     class Meta:
#         model = LayerB
#         fields = ['id', 'layer_b_name', 'slug', 'layer_cs']

# class LayerASerializer(serializers.ModelSerializer):
#     layer_bs = LayerBSerializer(many=True, read_only=True)

#     class Meta:
#         model = LayerA
#         fields = ['id', 'layer_a_name', 'slug', 'layer_bs']


# class LayerESerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LayerE
#         fields = ['id', 'layer_e_name']  # Include only the necessary fields

# class LayerDSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = LayerD
#         fields = ['id', 'layer_d_name', 'slug']  # Include only the necessary fields

# class LayerCSerializer(serializers.ModelSerializer):
    

#     class Meta:
#         model = LayerC
#         fields = ['id', 'layer_c_name', 'slug']  # Include only the necessary fields

# class LayerBSerializer(serializers.ModelSerializer):
   

#     class Meta:
#         model = LayerB
#         fields = ['id', 'layer_b_name', 'slug']  # Include only the necessary fields

# class LayerASerializer(serializers.ModelSerializer):
    

#     class Meta:
#         model = LayerA
#         fields = ['id', 'layer_a_name', 'slug']  # Include only the necessary fi
from rest_framework.response import Response
from .models import LayerA, LayerB, LayerC, LayerD, LayerE

# Serializers
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



