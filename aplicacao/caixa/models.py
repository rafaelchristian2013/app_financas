from django.db import models
from datetime import datetime

class Transacao(models.Model):
    nome_transacao = models.CharField(max_length=200, blank=True)
    valor_transacao = models.DecimalField(max_digits=10, decimal_places=2)
    data_transacao = models.DateField(default=datetime.now)
    tipo_transacao = models.CharField(max_length=200)
