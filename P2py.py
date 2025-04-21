# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'P2.ui'
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_P2(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 500)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_title = QtWidgets.QLabel(Form)
        self.lbl_title.setObjectName("lbl_title")
        self.verticalLayout.addWidget(self.lbl_title)
        self.btn_load_circuit = QtWidgets.QPushButton(Form)
        self.btn_load_circuit.setObjectName("btn_load_circuit")
        self.verticalLayout.addWidget(self.btn_load_circuit)
        self.graphicsView = QtWidgets.QGraphicsView(Form)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Circuit Viewer"))
        self.lbl_title.setText(_translate("Form", "Circuit Viewer"))
        self.btn_load_circuit.setText(_translate("Form", "Load Circuit"))