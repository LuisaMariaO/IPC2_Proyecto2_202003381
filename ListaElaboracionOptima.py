from ElaboracionOptima import ElaboracionOptima
class ListaElaboracionOptima:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0
    
    def vacia(self):
         return self.primero == None 
    
    def agregar(self, tiempo, linea, accion):
        if self.vacia():
            self.primero = self.ultimo = ElaboracionOptima(tiempo, linea, accion)
        else:
            aux = self.ultimo
            self.ultimo = aux.siguiente = ElaboracionOptima(tiempo, linea, accion)
            self.ultimo.anterior = aux
            