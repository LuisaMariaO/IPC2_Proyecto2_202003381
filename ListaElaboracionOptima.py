from ElaboracionOptima import ElaboracionOptima
class ListaElaboracionOptima:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0
    
    def vacia(self):
         return self.primero == None 
    
    def agregar(self, linea,accion):
        if self.vacia():
            self.primero = self.ultimo = ElaboracionOptima(linea,accion)
        else:
            aux = self.ultimo
            self.ultimo = aux.siguiente = ElaboracionOptima(linea,accion)
            self.ultimo.anterior = aux

    def imprimir(self):
        aux = self.primero
        while aux:
            print("Linea ",aux.linea," ", aux.accion)
            aux = aux.siguiente
            