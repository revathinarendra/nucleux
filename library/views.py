from rest_framework import generics
from .models import LayerA, LayerB, LayerC, LayerD, LayerE
from .serializers import LayerASerializer, LayerBSerializer, LayerCSerializer, LayerDSerializer, LayerESerializer
from .models import LayerF
from .serializers import LayerFSerializer


class LayerAListView(generics.ListAPIView):
     queryset = LayerA.objects.all().prefetch_related(
         'layer_bs__layer_cs__layer_ds__layer_es'  # Use prefetch_related for reverse relationships
     )
     serializer_class = LayerASerializer


# class LayerAListView(generics.ListAPIView):
#     queryset = LayerA.objects.all()
#     serializer_class = LayerASerializer

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


class LayerFListCreateView(generics.ListCreateAPIView):
    queryset = LayerF.objects.all()
    serializer_class = LayerFSerializer

class LayerFDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LayerF.objects.all()
    serializer_class = LayerFSerializer
