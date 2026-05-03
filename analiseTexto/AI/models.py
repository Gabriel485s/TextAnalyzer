from django.db import models

# Create your models here.

class Noticia(models.Model):
    
    conteudo = models.TextField()
    inserido_em = models.DateTimeField(auto_now_add=True)
    sentimento = models.CharField(max_length=20)
    tema = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.tema} ({self.inserido_em.strftime('%d/%m/%Y')})"
    