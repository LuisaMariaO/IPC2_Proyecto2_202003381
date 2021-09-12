from ElaboracionOptima import ElaboracionOptima
class ProductoSimulado():
    def __init__(self,nombre,tiempoTotal):
        self.nombre=nombre
        self.tiempoTotal=tiempoTotal
        self.elaboracionOptima=ElaboracionOptima()
        self.siguiente = None
        self.anterior = None