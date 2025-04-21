from Otto_GUI import Ui_Form  # Import the GUI class that was auto-generated from Qt Designer
from PyQt5 import QtWidgets as qtw  # Import PyQt5 widgets and alias as qtw for shorter access
import sys  # Gives access to command-line arguments and system exit
from Otto import CycleController  # Import the controller logic for the Otto (and Diesel) cycle

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg  # Canvas class to embed matplotlib plots in Qt
from matplotlib.figure import Figure  # Used to create a matplotlib Figure object

# Define the main window class, inheriting from QWidget and the Ui_Form from Qt Designer
class MainWindow(qtw.QWidget, Ui_Form):
    def __init__(self):  # Constructor for MainWindow
        super().__init__()  # Initialize the parent classes
        self.setupUi(self)  # Set up the UI layout from the Qt Designer `.ui` file
        self.radio_otto.setChecked(True)  # Set the Otto cycle radio button as the default selected

        self.figure = Figure(figsize=(8, 8))  # Create a new matplotlib Figure with size 8x8
        self.canvas = FigureCanvasQTAgg(self.figure)  # Create a canvas widget to display the Figure
        self.ax = self.figure.add_subplot()  # Add a subplot (axes) to the figure for plotting
        self.main_VerticalLayout.addWidget(self.canvas)  # Add the canvas to the main layout in the UI

        self.controller = CycleController(ax=self.ax)  # Create an instance of the controller, passing the axes
        self.controller.setWidgets([  # Link all necessary widgets from the GUI to the controller
            self.lbl_THigh, self.lbl_TLow, self.lbl_P0, self.lbl_V0, self.lbl_CR,  # Labels for input parameters
            self.le_THigh, self.le_TLow, self.le_P0, self.le_V0, self.le_CR,  # Line edits for input values
            self.le_T1, self.le_T2, self.le_T3, self.le_T4,  # Line edits for state temperatures
            self.lbl_T1Units, self.lbl_T2Units, self.lbl_T3Units, self.lbl_T4Units,  # Labels for units of state temps
            self.le_PowerStroke, self.le_CompressionStroke, self.le_HeatAdded, self.le_Efficiency,  # Outputs
            self.lbl_PowerStrokeUnits, self.lbl_CompressionStrokeUnits, self.lbl_HeatInUnits,  # Output units
            self.rdo_Metric, self.cmb_Abcissa, self.cmb_Ordinate,  # Unit selection + axes selectors
            self.chk_LogAbcissa, self.chk_LogOrdinate, self.ax, self.canvas  # Log scale toggles + plot objects
        ])

        self.btn_Calculate.clicked.connect(self.calcOtto)  # When "Calculate" button is clicked, call `calcOtto`
        self.radio_otto.toggled.connect(self.setUnits)  # When Otto radio is toggled, update unit labels
        self.radio_diesel.toggled.connect(self.setUnits)  # Same for Diesel radio button
        self.cmb_Abcissa.currentIndexChanged.connect(self.plot)  # When x-axis dropdown changes, update plot
        self.cmb_Ordinate.currentIndexChanged.connect(self.plot)  # When y-axis dropdown changes, update plot
        self.chk_LogAbcissa.stateChanged.connect(self.plot)  # Re-plot if log x-axis is toggled
        self.chk_LogOrdinate.stateChanged.connect(self.plot)  # Re-plot if log y-axis is toggled

        self.show()  # Show the main window to the user

    def calcOtto(self):  # Function called when Calculate button is clicked
        self.controller.calc()  # Ask the controller to compute the cycle and update results

    def plot(self):  # Function to update the plot
        self.controller.plot_cycle_XY()  # Ask the controller to redraw the cycle plot

    def setUnits(self):  # Function to refresh unit labels and conversions
        self.controller.updateView()  # Ask the controller to update labels and units

# Start of the program if this file is run directly
if __name__ == "__main__":  # Standard Python check for script execution
    app = qtw.QApplication(sys.argv)  # Create the Qt Application, passing command-line args
    window = MainWindow()  # Create an instance of your main window class
    window.setWindowTitle("Thermodynamic Cycle Simulator")  # Set the window title
    sys.exit(app.exec())  # Start the Qt event loop and exit when the window is closed


