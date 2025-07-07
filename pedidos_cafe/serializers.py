from rest_framework import serializers
from pedidos_cafe.models import PedidoCafe
from pedidos_cafe.factory import CafeFactory
from pedidos_cafe.builder import CafePersonalizadoBuilder, CafeDirector
from api_patrones.logger import Logger

INGREDIENTES_VALIDOS = ["leche", "azúcar", "canela", "chocolate", "vainilla"]

class PedidoCafeSerializer(serializers.ModelSerializer):
    precio_total = serializers.SerializerMethodField()
    ingredientes_finales = serializers.SerializerMethodField()
    ingredientes = serializers.ListField(
        child=serializers.CharField(), allow_empty=True
    )
    class Meta:
        model = PedidoCafe
        fields = [
            "id",
            "cliente",
            "tipo_base",
            "ingredientes",
            "tamanio",
            "fecha",
            "precio_total",
            "ingredientes_finales",
        ]
    
    def validate_ingredientes(self, value):
        for ingrediente in value:
            if ingrediente not in INGREDIENTES_VALIDOS:
                raise serializers.ValidationError(f"Ingrediente no válido: {ingrediente}")
        return value    

    def get_precio_total(self, obj):
        # Patron Factory
        cafe = CafeFactory.obtener_base(obj.tipo_base)
        # Patron Builder
        builder = CafePersonalizadoBuilder(cafe)
        director = CafeDirector(builder)
        director.construir(obj.ingredientes, obj.tamanio)
        # Patron Singleton
        Logger().registrar(f"Se registró el calculo del precio para el pedido {obj.id}")
        print(Logger().obtener_logs())
        return builder.obtener_precio()

    def get_ingredientes_finales(self, obj):
        # Patron Factory
        cafe = CafeFactory.obtener_base(obj.tipo_base)
        # Patron Builder
        builder = CafePersonalizadoBuilder(cafe)
        director = CafeDirector(builder)
        director.construir(obj.ingredientes, obj.tamanio)
        # Patron Singleton
        Logger().registrar(
            f"Se registró la obtención de ingredientes finales para el pedido {obj.id}"
        )
        print(Logger().obtener_logs())
        return builder.obtener_ingredientes_finales()