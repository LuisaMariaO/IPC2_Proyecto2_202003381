class Elaboracion():
    def __init__(self,linea,componente):
        self.linea=linea
        self.componente=componente
        self.terminado=False
        self.siguiente = None
        self.anterior = None
       