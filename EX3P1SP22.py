#Region Imports
from PyQt5.QtWidgets import QApplication, QWidget
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from Problem1 import Ui_Form
import sys
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

#
class main_window(Ui_Form, QWidget):
    def __init__(self):
        super().__init__()  # Initialize the QWidget + Ui_Form superclass
        self.setupUi(self)  # Set up all widgets from the .ui layout
        self.setupImageLabel()  # Load and display the circuit image

        #Connect the Simulate button to a function (event handler)
        self.btn_sim.clicked.connect(self.handle_simulate)
        self.show()  # Show the GUI window

    def handle_simulate(self):
        """Triggered when the Simulate button is clicked."""
        #Prompt user for input values
        R = float(self.le_R.text())  # Get resistance (Ohms) from input field
        L = float(self.le_L.text())  # Get inductance (Henries) from input field
        C = float(self.le_C.text())  # Get capacitance (Farads) from input field
        V0 = float(self.le_V0.text())  # Get voltage amplitude (Volts) from input field
        f = float(self.le_f.text())  # Get frequency (Hz) from input field
        phi = float(self.le_phi.text())  # Get phase angle (degrees) from input field

        #print values from user input
        print(f"R = {R} Ohms")  # Print resistance value to terminal
        print(f"L = {L} H")  # Print inductance value to terminal
        print(f"C = {C} F")  # Print capacitance value to terminal
        print(f"V0 = {V0} V")  # Print voltage amplitude to terminal
        print(f"f = {f} Hz")  # Print frequency to terminal
        print(f"phi = {phi} degrees")  # Print phase angle to terminal

        #ODE Simulation
        omega = 2 * np.pi * f  # Convert frequency to angular frequency (rad/s)
        phi_rad = np.deg2rad(phi)  # Convert phase angle to radians

        def V_in(t):  # Define input voltage as a cosine function of time
            return V0 * np.cos(omega * t + phi_rad)

        def dVdt(t):  # Define derivative of voltage function (needed for ODE)
            return -V0 * omega * np.sin(omega * t + phi_rad)

        def model(y, t):  # Define second-order differential equation model
            i, di_dt = y  # y[0] = i(t), y[1] = di/dt
            d2i_dt2 = (dVdt(t) - R * di_dt - i / C) / L  # Second derivative using RLC equation
            return [di_dt, d2i_dt2]  # Return the two first-order ODEs as a list

        #simulation setup
        t = np.linspace(0, 0.1, 1000)  # Create a time vector from 0 to 0.1 seconds
        y0 = [0, 0]  # Initial conditions: i(0) = 0 A, di/dt(0) = 0 A/s
        sol = odeint(model, y0, t)  # Solve the system of ODEs using scipy's odeint
        i = sol[:, 0]  # Extract current i(t) from solution

        #plot results
        plt.figure()  # Create a new plot window
        plt.plot(t, i, label="Current i(t)")  # Plot current vs. time
        plt.xlabel("Time (s)")  # Label x-axis
        plt.ylabel("Current (A)")  # Label y-axis
        plt.title("Transient Response of Series RLC Circuit")  # Title of the plot
        plt.grid(True)  # Add grid lines to the plot
        plt.legend()  # Show legend for the plot
        plt.show()  # Display the plot

    def setupImageLabel(self):
        # region setup a label to display the image of the circuit
        self.pixMap = qtg.QPixmap()  # Create a QPixmap object to hold the image
        self.pixMap.load("Circuit1.png")  # Load the image file named "Circuit1.png"
        self.image_label = qtw.QLabel()  # Create a QLabel widget to display the image
        self.image_label.setPixmap(self.pixMap)  # Set the loaded pixmap onto the QLabel
        self.layout_GridInput.addWidget(self.image_label)  # Add the QLabel into the input layout on the GUI
        # endregion
#endregion

if __name__ == "__main__":
    app = QApplication.instance()  # Check if a QApplication instance already exists (prevents duplicates)
    if not app:  # If no instance exists,
        app = QApplication(sys.argv)  # Create a new QApplication to manage the GUI event loop
    app.aboutToQuit.connect(app.deleteLater)  # Ensure proper cleanup when the app is closed
    main_win = main_window()  # Create an instance of the main window (your GUI)
    sys.exit(app.exec_())  # Start the event loop and exit the program when the GUI is closed