from ListaProductosSimulados import ListaProductosSimulados
class Simulacion():
    def __init__(self,nombre):
        self.nombre=nombre
        self.productos_simulados=ListaProductosSimulados()
        self.siguiente = None
        self.anterior = None