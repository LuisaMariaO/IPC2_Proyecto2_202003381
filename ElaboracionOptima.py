class ElaboracionOptima():
    def __init__(self,tiempo,linea,accion):
        self.tiempo=tiempo
        self.linea=linea
        self.accion=accion()
        self.siguiente = None
        self.anterior = None