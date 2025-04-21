# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Problem1.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")  # Give the main window an internal name
        Form.resize(400, 300)  # Set the window size (width x height)

        # Create main vertical layout for the form
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")

        # Create a group box labeled "Input"
        self.gb_Input = QtWidgets.QGroupBox(Form)
        self.gb_Input.setObjectName("gb_Input")

        # Add a vertical layout inside the group box
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.gb_Input)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # Create a grid layout for input widgets (label + field pairs)
        self.layout_GridInput = QtWidgets.QGridLayout()
        self.layout_GridInput.setObjectName("layout_GridInput")

        # Add the grid layout to the vertical layout inside the group box
        self.verticalLayout_2.addLayout(self.layout_GridInput)

        # Add the group box to the main form layout
        self.verticalLayout.addWidget(self.gb_Input)

        # Resistance R input
        self.label_R = QtWidgets.QLabel("R (Ohms):")  # Create label for resistance
        self.le_R = QtWidgets.QLineEdit()  # Create input box for resistance
        self.layout_GridInput.addWidget(self.label_R, 0, 0)  # Place label in grid row 0, col 0
        self.layout_GridInput.addWidget(self.le_R, 0, 1)  # Place input in grid row 0, col 1

        # Inductance L input
        self.label_L = QtWidgets.QLabel("L (Henries):")  # Create label for inductance
        self.le_L = QtWidgets.QLineEdit()  # Create input box for inductance
        self.layout_GridInput.addWidget(self.label_L, 1, 0)  # Place label in grid row 1, col 0
        self.layout_GridInput.addWidget(self.le_L, 1, 1)  # Place input in grid row 1, col 1

        # Capacitance C input
        self.label_C = QtWidgets.QLabel("C (Farads):")  # Create label for capacitance
        self.le_C = QtWidgets.QLineEdit()  # Create input box for capacitance
        self.layout_GridInput.addWidget(self.label_C, 2, 0)  # Place label in grid row 2, col 0
        self.layout_GridInput.addWidget(self.le_C, 2, 1)  # Place input in grid row 2, col 1

        # Voltage V₀ input
        self.label_V0 = QtWidgets.QLabel("V₀ (Volts):")  # Create label for source voltage
        self.le_V0 = QtWidgets.QLineEdit()  # Create input box for voltage amplitude
        self.layout_GridInput.addWidget(self.label_V0, 3, 0)  # Place label in grid row 3, col 0
        self.layout_GridInput.addWidget(self.le_V0, 3, 1)  # Place input in grid row 3, col 1

        # Frequency f input
        self.label_f = QtWidgets.QLabel("f (Hz):")  # Create label for frequency
        self.le_f = QtWidgets.QLineEdit()  # Create input box for frequency
        self.layout_GridInput.addWidget(self.label_f, 4, 0)  # Place label in grid row 4, col 0
        self.layout_GridInput.addWidget(self.le_f, 4, 1)  # Place input in grid row 4, col 1

        # Phase φ input
        self.label_phi = QtWidgets.QLabel("φ (degrees):")  # Create label for phase angle
        self.le_phi = QtWidgets.QLineEdit()  # Create input box for phase angle
        self.layout_GridInput.addWidget(self.label_phi, 5, 0)  # Place label in grid row 5, col 0
        self.layout_GridInput.addWidget(self.le_phi, 5, 1)  # Place input in grid row 5, col 1

        # Simulate Button
        self.btn_sim = QtWidgets.QPushButton("Simulate")  # Create simulate button
        self.layout_GridInput.addWidget(self.btn_sim, 6, 0, 1, 2)  # Span the button across both columns in row 6

        # Apply translations and connect widgets by name
        self.retranslateUi(Form)  # Set the display text for widgets
        QtCore.QMetaObject.connectSlotsByName(Form)  # Auto-connect signals if using Qt Designer slots

    #Setting widget texts (used for localization)
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))  # Set the window title
        self.gb_Input.setTitle(_translate("Form", "Input"))  # Set the title of the group box

