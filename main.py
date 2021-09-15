import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QAction, QMessageBox, QDialog
from Interfaz import MainWindow
import xml.etree.ElementTree as ET
from Maquina import Maquina
import re


class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=MainWindow()
        self.ui.setupUi(self)
        self.ui.action_config_maquina.triggered.connect(self.config)

        #self.pushButton.clicked.connect(self.hola)
    def config(self):
        
        archivo=QFileDialog.getOpenFileName(self, 'Abrir archivo', 'C:\\','Archivos xml (*.xml)')
        #try:
        #Tomo la posición 0 de la ruta, pues QFileDialog retorna una tupla compuesta por la ruta y el tipo de archivo
        tree = ET.parse(archivo[0])
        root = tree.getroot()  
        for Ma in root:
            for l in Ma.iter('CantidadLineasProduccion'):
                lineas=l.text
                lineas=int(lineas)
                
            #Creación de objeto máquina
            maquina=Maquina(lineas)
            
            #Busco las lineas de producción
            for listado in Ma.iter('ListadoLineasProduccion'):
                for linea in listado.iter('LineaProduccion'):
                    for numero in linea.iter('Numero'):
                        number=int(numero.text)
                    for componentes in linea.iter('CantidadComponentes'):
                        components=int(componentes.text)
                    for tiempo in linea.iter('TiempoEnsamblaje'):
                        time=int(tiempo.text)
                    maquina.lineas.agregar(number,components,time)
            for productos in Ma.iter('ListadoProductos'):
                for producto in productos.iter('Producto'):
                    for nombre in producto.iter('nombre'):
                        name=nombre.text
                        name=name.replace('\t','')
                        name=name.replace('\n','')
                    maquina.productos.agregar(name)
                    for elaboracion in producto.iter('elaboracion'):
                        item=maquina.productos.getProducto(name)
                        patronElaboracion=re.compile('L[0-9]+pC[0-9]+')
                        patron=patronElaboracion.findall(elaboracion.text)
                        patronLinea=re.compile('L[0-9]+') #Encuentra la linea
                        patronComponente=re.compile('C[0-9]+') #Encuentra el componente
                        
                        for el in patron:
                            #Toma la linea
                            line=patronLinea.search(el)
                            line=line.group()
                            #Toma el componente
                            component=patronComponente.search(el)
                            component=component.group()
                            #Agrega a la cola de elaboracion
                            item.elaboracion.encolar(line,component)
                        
                        
            
            
                        
                        



                
        #except:
            #QMessageBox.about(self, "Advertencia", "No es posible abrir el archivo")





if __name__=='__main__':
    app=QApplication(sys.argv)
    GUI=Ventana()
    GUI.show()
    sys.exit(app.exec_())