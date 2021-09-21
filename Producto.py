from Cola import Cola
from ListaSegundos import ListaSegundos
class Producto():
    def __init__(self,nombre):
        self.nombre=nombre
        self.elaboracion=Cola()
        self.segundos=ListaSegundos()
        self.siguiente = None
        self.anterior = None
        self.simulado=False
       