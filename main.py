import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QAction, QMessageBox, QDialog
from Interfaz import MainWindow
import xml.etree.ElementTree as ET


class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=MainWindow()
        self.ui.setupUi(self)
        self.ui.action_config_maquina.triggered.connect(self.config)

        #self.pushButton.clicked.connect(self.hola)
    def config(self):
        archivo=QFileDialog.getOpenFileName(self, 'Abrir archivo', 'C:\\','Archivos xml (*.xml)')
        try:
        
            tree = ET.parse(archivo[0])
            root = tree.getroot()   
        except:
            QMessageBox.about(self, "Advertencia", "No es posible abrir el archivo")





if __name__=='__main__':
    app=QApplication(sys.argv)
    GUI=Ventana()
    GUI.show()
    sys.exit(app.exec_())