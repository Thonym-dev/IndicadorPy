from django.db import models

# Create your models here.

class Device(models.Model):
    DEVICE_CHOICES = [
        ('substation', 'Subestação'),
        ('transformer', 'Transformador'),
        ('disconnector', 'Disjuntor'),
        ('fuse_key', 'Chave Fusível'),
        ('recloser', 'Religador Automático'),
        ('bus', 'Barra Elétrica'),
    ]

    device_type = models.CharField(max_length=50, choices=DEVICE_CHOICES)
    device_name = models.CharField(max_length=100)
    interruptions = models.IntegerField()
    resolution_time = models.FloatField()  # Tempo em horas
    connected_clients = models.IntegerField()

    def __str__(self):
        return f"{self.device_name}"
