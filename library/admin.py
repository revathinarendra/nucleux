# admin.py
from django.contrib import admin
from .models import LayerA, LayerB, LayerC, LayerD, LayerE

@admin.register(LayerA)
class LayerAAdmin(admin.ModelAdmin):
    list_display = ('layer_a_name', 'slug')
    prepopulated_fields = {'slug': ('layer_a_name',)}

@admin.register(LayerB)
class LayerBAdmin(admin.ModelAdmin):
    list_display = ('layer_a_name', 'layer_b_name', 'slug')
    prepopulated_fields = {'slug': ('layer_b_name',)}

@admin.register(LayerC)
class LayerCAdmin(admin.ModelAdmin):
    list_display = ('layer_b_name', 'layer_c_name', 'slug')
    prepopulated_fields = {'slug': ('layer_c_name',)}

@admin.register(LayerD)
class LayerDAdmin(admin.ModelAdmin):
    list_display = ('layer_c_name', 'layer_d_name', 'slug')
    prepopulated_fields = {'slug': ('layer_d_name',)}

@admin.register(LayerE)
class LayerEAdmin(admin.ModelAdmin):
    list_display = ('layer_d_name', 'layer_e_name')
