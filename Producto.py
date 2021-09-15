from Cola import Cola
class Producto():
    def __init__(self,nombre):
        self.nombre=nombre
        self.elaboracion=Cola()
        self.siguiente = None
        self.anterior = None
       