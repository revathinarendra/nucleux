from django.urls import path
from .views import LayerAListView, LayerBListView, LayerCListView, LayerDListView, LayerEListView

urlpatterns = [
    path('layera/', LayerAListView.as_view(), name='layera-list'),
    path('layerb/', LayerBListView.as_view(), name='layerb-list'),
    path('layerc/', LayerCListView.as_view(), name='layerc-list'),
    path('layerd/', LayerDListView.as_view(), name='layerd-list'),
    path('layere/', LayerEListView.as_view(), name='layere-list'),
]
