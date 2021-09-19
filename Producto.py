from Cola import Cola
from ListaElaboracionOptima import ListaElaboracionOptima
class Producto():
    def __init__(self,nombre):
        self.nombre=nombre
        self.elaboracion=Cola()
        self.elaboracionOptima=ListaElaboracionOptima()
        self.siguiente = None
        self.anterior = None
       