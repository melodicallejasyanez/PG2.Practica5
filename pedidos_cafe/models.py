from django.db import models
from django.core.exceptions import ValidationError

INGREDIENTES_VALIDOS = ["leche", "azúcar", "canela", "chocolate", "vainilla"]

# Create your models here.
class PedidoCafe(models.Model):
    cliente = models.CharField(max_length=100)
    tipo_base = models.CharField(
        max_length=20,
        choices=[
            ("espresso", "Espresso"),
            ("americano", "Americano"),
            ("latte", "Latte"),
        ],
    )
    ingredientes = models.JSONField(default=list)
    tamanio = models.CharField(
        max_length=10,
        choices=[
            ("pequeño", "Pequeño"),
            ("mediano", "Mediano"),
            ("grande", "Grande"),
        ],
    )
    fecha = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Validar que los ingredientes sean válidos
        for ingrediente in self.ingredientes:
            if ingrediente not in INGREDIENTES_VALIDOS:
                raise ValidationError(f"Ingrediente no válido: {ingrediente}")