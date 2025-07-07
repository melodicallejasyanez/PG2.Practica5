# API de Pedidos de Café

Esta API permite gestionar pedidos personalizados de café, permitiendo a los usuarios seleccionar el tipo de café base, tamaño y una lista de ingredientes extra válidos. El sistema calcula automáticamente el precio total y los ingredientes finales del pedido, aplicando reglas de negocio y validaciones tanto en la API como en el panel de administración de Django. El proyecto está desarrollado con Django y Django REST Framework, y utiliza patrones de diseño para organizar y escalar la lógica de negocio.

## Pasos seguidos para el desarrollo

1. **Inicialización del proyecto Django** y creación de la app `pedidos_cafe`.
2. **Definición del modelo `PedidoCafe`** en `models.py`, incluyendo validaciones de ingredientes.
3. **Configuración del panel de administración** en `admin.py` para gestionar pedidos desde el admin de Django.
4. **Creación de serializers** en `serializers.py` para exponer y validar los datos de la API.
5. **Implementación de patrones de diseño** (Factory, Builder, Singleton) en archivos separados para organizar la lógica de creación y personalización de cafés.
6. **Configuración de rutas y vistas** usando Django REST Framework.
7. **Pruebas de la API** desde el navegador.

## Patrones de diseño utilizados

### 1. Factory
 
Este patron de diseño se encuentra en `pedidos_cafe/factory.py`.  
Se utiliza el patrón Factory para encapsular la creación de objetos de café base (`Espresso`, `Americano`, `Latte`). Esto permite centralizar la lógica de instanciación y facilita la fabricacion a nuevos tipos de café en el futuro.

**Código ejemplo:**

````python
# filepath: pedidos_cafe/factory.py
from pedidos_cafe.base import Espresso, Americano, Latte

class CafeFactory:
    @staticmethod
    def obtener_base(tipo):
        if tipo == "espresso":
            cafe = Espresso()
        elif tipo == "americano":
            cafe = Americano()
        elif tipo == "latte":
            cafe = Latte()
        else:
            raise ValueError("Tipo de café no válido")
        cafe.inicializar()
        return cafe


---

### 2. Builder

Este patron de diseño se encuentra en `pedidos_cafe/builder.py`.  
El patrón Builder se usa para construir cafés personalizados paso a paso, agregando ingredientes y ajustando el tamaño. Esto separa la lógica de construcción de la lógica de representación del café, haciendo el código más mantenible y flexible.

````python
# filepath: pedidos_cafe/builder.py
class CafePersonalizadoBuilder:
    def __init__(self, cafe_base):
        self.cafe = cafe_base

    def agregar_ingredientes(self, ingredientes):
        for ingrediente in ingredientes:
            self.cafe.agregar_ingrediente(ingrediente)

    def set_tamanio(self, tamanio):
        self.cafe.tamanio = tamanio

    def obtener_precio(self):
        return self.cafe.calcular_precio()

    def obtener_ingredientes_finales(self):
        return self.cafe.ingredientes

class CafeDirector:
    def __init__(self, builder):
        self.builder = builder

    def construir(self, ingredientes, tamanio):
        self.builder.agregar_ingredientes(ingredientes)
        self.builder.set_tamanio(tamanio)

---

### 3. Singleton
  
Este patron de diseño se encuentra en `api_patrones/logger.py`. 
El patrón Singleton se implementa en la clase `Logger` para asegurar que solo exista una instancia de registro de logs en toda la aplicación. Esto es útil para centralizar el registro de eventos importantes, como el cálculo de precios o la obtención de ingredientes finales.


````python
# filepath: api_patrones/logger.py
class Logger:
    _instancia = None
    _logs = []

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def registrar(self, mensaje):
        self._logs.append(mensaje)

    def obtener_logs(self):
        return self._logs
---

## Uso de la API

- **Panel de administración:**  
  Accede a `/admin` para gestionar pedidos (requiere superusuario).
- **API REST:**  
  Accede a `/api/pedidos_cafe/` para crear, listar y consultar pedidos de café personalizados.
- **Validación:**  
  Solo se permiten ingredientes válidos definidos en el sistema, tanto desde la API como desde el admin.

---