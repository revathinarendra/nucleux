from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
import json

class LayerA(models.Model):
    layer_a_name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True,max_length=200)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.layer_a_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.layer_a_name

class LayerB(models.Model):
    layer_a_name = models.ForeignKey(LayerA, on_delete=models.CASCADE, related_name='layer_bs')
    layer_b_name = models.TextField()
    slug = models.SlugField(unique=True, blank=True,max_length=200)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.layer_b_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.layer_b_name

class LayerC(models.Model):
    layer_b_name = models.ForeignKey(LayerB, on_delete=models.CASCADE, related_name='layer_cs')
    layer_c_name = models.TextField()
    slug = models.SlugField(unique=True, blank=True,max_length=300)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.layer_c_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.layer_c_name

class LayerD(models.Model):
    layer_c_name = models.ForeignKey(LayerC, on_delete=models.CASCADE, related_name='layer_ds')
    layer_d_name = models.TextField()
    slug = models.SlugField(unique=True, blank=True, max_length=200)

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.layer_d_name)
    #     super().save(*args, **kwargs)
    def save(self, *args, **kwargs):
        if not self.slug:
            full_slug = slugify(self.layer_d_name)
            # Ensure the slug fits within the 50-character limit, including '...'
            self.slug = full_slug[:47] + '...' if len(full_slug) > 50 else full_slug
        super().save(*args, **kwargs)


    def __str__(self):
        return self.layer_d_name

class LayerE(models.Model):
    layer_d_name = models.ForeignKey(LayerD, on_delete=models.CASCADE, related_name='layer_es')
    layer_e_name = models.TextField()

    def __str__(self):
        return self.layer_e_name

class LayerF(models.Model):
    layer_e_name = models.ForeignKey(LayerE, on_delete=models.CASCADE, related_name='layer_es')
    layer_f_name = RichTextField()
    layer_f_note = models.TextField(blank=True)

    def set_layer_f_note_json(self, data):
        """Save JSON data to layer_f_note."""
        self.layer_f_note = json.dumps(data)

    def get_layer_f_note_json(self):
        """Retrieve JSON data from layer_f_note."""
        if self.layer_f_note:
            return json.loads(self.layer_f_note)
        return None

    def __str__(self):
        return self.layer_f_name