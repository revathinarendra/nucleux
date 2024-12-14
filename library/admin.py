from django.contrib import admin
from .models import LayerA, LayerB, LayerC, LayerD, LayerE, LayerF
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from .models import LayerF
from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget

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


class LayerFAdminForm(forms.ModelForm):
    layer_f_name = forms.CharField(widget=CKEditorUploadingWidget())  

    class Meta:
        model = LayerF
        fields = '__all__'  


class LayerFAdmin(admin.ModelAdmin):
    form = LayerFAdminForm
    list_display = ('get_layer_e_name', 'layer_f_name')

    def get_layer_e_name(self, obj):
        return obj.layer_e_name.layer_e_name 
    get_layer_e_name.short_description = 'Layer E Name'

admin.site.register(LayerF, LayerFAdmin)


