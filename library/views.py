from rest_framework import generics
from .models import LayerA, LayerB, LayerC, LayerD, LayerE
from .serializers import LayerASerializer, LayerBSerializer, LayerCSerializer, LayerDSerializer, LayerESerializer

class LayerAListView(generics.ListAPIView):
    queryset = LayerA.objects.all()
    serializer_class = LayerASerializer

class LayerBListView(generics.ListAPIView):
    queryset = LayerB.objects.all()
    serializer_class = LayerBSerializer

class LayerCListView(generics.ListAPIView):
    queryset = LayerC.objects.all()
    serializer_class = LayerCSerializer

class LayerDListView(generics.ListAPIView):
    queryset = LayerD.objects.all()
    serializer_class = LayerDSerializer

class LayerEListView(generics.ListAPIView):
    queryset = LayerE.objects.all()
    serializer_class = LayerESerializer
