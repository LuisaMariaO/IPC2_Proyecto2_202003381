from Segundo import Segundo
class ListaSegundos:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0
    
    def vacia(self):
         return self.primero == None 
    
    def agregar(self, segundo):
        if self.vacia():
            self.primero = self.ultimo = Segundo(segundo)
        else:
            aux = self.ultimo
            self.ultimo = aux.siguiente = Segundo(segundo)
            self.ultimo.anterior = aux

    def getSegundo(self,segundo):
     
        aux = self.primero
        while aux:
            if segundo==aux.segundo:
      
                return aux
            aux = aux.siguiente
        return None

    def imprimir(self):
        aux = self.primero
        while aux:
            print("Segundo= ",aux.segundo)
            aux = aux.siguiente
            