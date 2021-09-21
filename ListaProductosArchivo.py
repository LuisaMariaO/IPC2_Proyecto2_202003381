from ProductoArchivo import ProductoArchivo
class ListaProductosArchivo:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0

    def vacia(self):
         return self.primero == None 
    
    def agregar(self, nombre):
        if self.vacia():
            self.primero = self.ultimo = ProductoArchivo(nombre)
        else:
            aux = self.ultimo
            self.ultimo = aux.siguiente = ProductoArchivo(nombre)
        self.size+=1

    def imprimir(self):
        aux = self.primero
        while aux:
            print("Producto= "+aux.nombre)
            aux = aux.siguiente