from Otto_GUI import Ui_Form
from PyQt5 import QtWidgets as qtw
import sys
from Otto import CycleController

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MainWindow(qtw.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.radio_otto.setChecked(True)

        self.figure = Figure(figsize=(8, 8))
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot()
        self.main_VerticalLayout.addWidget(self.canvas)

        self.controller = CycleController(ax=self.ax)
        self.controller.setWidgets([
            self.lbl_THigh, self.lbl_TLow, self.lbl_P0, self.lbl_V0, self.lbl_CR,
            self.le_THigh, self.le_TLow, self.le_P0, self.le_V0, self.le_CR,
            self.le_T1, self.le_T2, self.le_T3, self.le_T4,
            self.lbl_T1Units, self.lbl_T2Units, self.lbl_T3Units, self.lbl_T4Units,
            self.le_PowerStroke, self.le_CompressionStroke, self.le_HeatAdded, self.le_Efficiency,
            self.lbl_PowerStrokeUnits, self.lbl_CompressionStrokeUnits, self.lbl_HeatInUnits,
            self.rdo_Metric, self.cmb_Abcissa, self.cmb_Ordinate,
            self.chk_LogAbcissa, self.chk_LogOrdinate, self.ax, self.canvas
        ])

        self.btn_Calculate.clicked.connect(self.calcOtto)
        self.radio_otto.toggled.connect(self.setUnits)
        self.radio_diesel.toggled.connect(self.setUnits)
        self.cmb_Abcissa.currentIndexChanged.connect(self.plot)
        self.cmb_Ordinate.currentIndexChanged.connect(self.plot)
        self.chk_LogAbcissa.stateChanged.connect(self.plot)
        self.chk_LogOrdinate.stateChanged.connect(self.plot)

        self.show()

    def calcOtto(self):
        self.controller.calc()

    def plot(self):
        self.controller.plot_cycle_XY()

    def setUnits(self):
        self.controller.updateView()

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Thermodynamic Cycle Simulator")
    sys.exit(app.exec())

