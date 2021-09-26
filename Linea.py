
class Linea():
    def __init__(self,numero,no_componentes,tiempo):
        self.numero=numero
        self.no_componentes=no_componentes
        self.tiempo=tiempo
       
     
        self.ensamblando=False

        self.componente_actual=0
        self.componente_siguiente=None
        self.disponible=True
        self.siguiente = None
        self.anterior = None
       