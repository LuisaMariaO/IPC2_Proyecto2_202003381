# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Interfaz.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1166, 624)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Imagenes/icono.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(170, 140, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(50, 550, 541, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label_progreso = QtWidgets.QLabel(self.centralwidget)
        self.label_progreso.setGeometry(QtCore.QRect(290, 510, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_progreso.setFont(font)
        self.label_progreso.setObjectName("label_progreso")
        self.list_componentes = QtWidgets.QListView(self.centralwidget)
        self.list_componentes.setGeometry(QtCore.QRect(90, 230, 331, 251))
        self.list_componentes.setObjectName("list_componentes")
        self.label_componentes = QtWidgets.QLabel(self.centralwidget)
        self.label_componentes.setGeometry(QtCore.QRect(150, 200, 211, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_componentes.setFont(font)
        self.label_componentes.setObjectName("label_componentes")
        self.temporizador = QtWidgets.QLCDNumber(self.centralwidget)
        self.temporizador.setGeometry(QtCore.QRect(940, 520, 71, 31))
        self.temporizador.setObjectName("temporizador")
        self.label_segundos = QtWidgets.QLabel(self.centralwidget)
        self.label_segundos.setGeometry(QtCore.QRect(1020, 530, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_segundos.setFont(font)
        self.label_segundos.setObjectName("label_segundos")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(210, 120, 81, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalScrollBar = QtWidgets.QScrollBar(self.centralwidget)
        self.verticalScrollBar.setGeometry(QtCore.QRect(1070, 90, 20, 411))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.B_play = QtWidgets.QPushButton(self.centralwidget)
        self.B_play.setGeometry(QtCore.QRect(570, 90, 61, 41))
        self.B_play.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Imagenes/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.B_play.setIcon(icon1)
        self.B_play.setObjectName("B_play")
        self.B_siguiente = QtWidgets.QPushButton(self.centralwidget)
        self.B_siguiente.setEnabled(False)
        self.B_siguiente.setGeometry(QtCore.QRect(640, 50, 75, 23))
        self.B_siguiente.setObjectName("B_siguiente")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(640, 80, 491, 431))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 489, 429))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.table = QtWidgets.QTableView(self.scrollAreaWidgetContents)
        self.table.setGeometry(QtCore.QRect(0, 0, 491, 431))
        self.table.setObjectName("table")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1166, 21))
        self.menubar.setObjectName("menubar")
        self.menuArchivo = QtWidgets.QMenu(self.menubar)
        self.menuArchivo.setObjectName("menuArchivo")
        self.menuReportes = QtWidgets.QMenu(self.menubar)
        self.menuReportes.setObjectName("menuReportes")
        self.menuAyuda = QtWidgets.QMenu(self.menubar)
        self.menuAyuda.setObjectName("menuAyuda")
        self.menuReiniciar = QtWidgets.QMenu(self.menubar)
        self.menuReiniciar.setObjectName("menuReiniciar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_config_maquina = QtWidgets.QAction(MainWindow)
        self.action_config_maquina.setObjectName("action_config_maquina")
        self.action_simulacion = QtWidgets.QAction(MainWindow)
        self.action_simulacion.setObjectName("action_simulacion")
        self.action_reporte_simulacion = QtWidgets.QAction(MainWindow)
        self.action_reporte_simulacion.setObjectName("action_reporte_simulacion")
        self.action_reporte_cola = QtWidgets.QAction(MainWindow)
        self.action_reporte_cola.setObjectName("action_reporte_cola")
        self.action_acerca_de = QtWidgets.QAction(MainWindow)
        self.action_acerca_de.setObjectName("action_acerca_de")
        self.action_my_info = QtWidgets.QAction(MainWindow)
        self.action_my_info.setObjectName("action_my_info")
        self.action_borrar = QtWidgets.QAction(MainWindow)
        self.action_borrar.setObjectName("action_borrar")
        self.menuArchivo.addAction(self.action_config_maquina)
        self.menuArchivo.addAction(self.action_simulacion)
        self.menuReportes.addAction(self.action_reporte_simulacion)
        self.menuReportes.addAction(self.action_reporte_cola)
        self.menuAyuda.addAction(self.action_acerca_de)
        self.menuAyuda.addSeparator()
        self.menuAyuda.addAction(self.action_my_info)
        self.menuReiniciar.addAction(self.action_borrar)
        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuReportes.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())
        self.menubar.addAction(self.menuReiniciar.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Digital Intelligence S.A."))
        self.comboBox.setItemText(0, _translate("MainWindow", "Seleccionar"))
        self.label_progreso.setText(_translate("MainWindow", "Progreso"))
        self.label_componentes.setText(_translate("MainWindow", "Componentes necesarios"))
        self.label_segundos.setText(_translate("MainWindow", "segundos"))
        self.label.setText(_translate("MainWindow", "Producto"))
        self.B_siguiente.setText(_translate("MainWindow", "Siguiente"))
        self.menuArchivo.setTitle(_translate("MainWindow", "Archivo"))
        self.menuReportes.setTitle(_translate("MainWindow", "Reportes"))
        self.menuAyuda.setTitle(_translate("MainWindow", "Ayuda"))
        self.menuReiniciar.setTitle(_translate("MainWindow", "Máquina"))
        self.action_config_maquina.setText(_translate("MainWindow", "Cargar configuración de máquina"))
        self.action_simulacion.setText(_translate("MainWindow", "Cargar archivo de simulación"))
        self.action_reporte_simulacion.setText(_translate("MainWindow", "Reporte de simulación"))
        self.action_reporte_cola.setText(_translate("MainWindow", "Reporte de cola de secuencia"))
        self.action_acerca_de.setText(_translate("MainWindow", "Acerca de la aplicación"))
        self.action_my_info.setText(_translate("MainWindow", "Acerca del programador"))
        self.action_borrar.setText(_translate("MainWindow", "Borrar configuración de máquina"))
