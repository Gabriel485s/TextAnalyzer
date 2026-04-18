from django.db import models

# Create your models here.

class IaModel(models.Model):
    
    texto = models.TextField(null=False, blank=False)
