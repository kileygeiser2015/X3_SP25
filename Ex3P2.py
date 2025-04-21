import sys  # Allows interaction with the Python interpreter and command line arguments
import xml.etree.ElementTree as ET  # XML parser to process the custom circuit description file
from PyQt5.QtWidgets import (  # Import widgets used for building the GUI
    QApplication, QWidget, QGraphicsScene,
    QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem
)
from PyQt5.QtGui import QPen, QBrush, QColor  # Import classes for drawing and styling graphics
from P2py import Ui_P2  # Import the auto-generated PyQt5 UI file from Qt Designer

# Define a class for the circuit viewer GUI, inheriting from QWidget
class CircuitViewer(QWidget):
    def __init__(self):  # Constructor method
        super().__init__()  # Call the parent QWidget constructor
        self.ui = Ui_P2()  # Create instance of the UI layout class
        self.ui.setupUi(self)  # Set up the layout for this widget using the generated UI

        self.scene = QGraphicsScene()  # Create a scene to draw the circuit graphics
        self.ui.graphicsView.setScene(self.scene)  # Attach the scene to the graphics view widget

        self.nodes = {}  # Dictionary to store node names and positions
        self.components = []  # List to store circuit components (resistors, capacitors, etc.)

        self.ui.btn_load_circuit.clicked.connect(self.load_circuit)  # Connect button click to the function

        # self.load_circuit()  # Optional: You can auto-load the file here if uncommented

    def load_circuit(self):  # Function to load and parse the circuit from a file
        file_path = "circuit_description.txt"  # Name of the circuit description file
        try:
            with open(file_path, 'r') as file:  # Try to open the file in read mode
                self.nodes.clear()  # Clear old nodes before loading new ones
                self.components.clear()  # Clear old components as well

                wrapped = "<root>\n" + file.read() + "\n</root>"  # Wrap contents in a root tag for XML parsing
                root = ET.fromstring(wrapped)  # Parse the XML string into an ElementTree object

                for element in root:  # Iterate over each element in the XML
                    tag = element.tag.lower()  # Convert the tag name to lowercase

                    if tag == "node":  # Handle node elements separately
                        name = element.attrib["name"]  # Get node name
                        x = int(element.attrib["x"])  # Get x position as integer
                        y = int(element.attrib["y"])  # Get y position as integer
                        self.nodes[name] = (x, y)  # Store node in the dictionary
                    else:  # Handle all other elements (components)
                        name = element.attrib["name"]  # Get component label/name
                        n1 = element.attrib["n1"]  # Starting node
                        n2 = element.attrib["n2"]  # Ending node
                        self.components.append((tag.upper(), name, n1, n2))  # Store component in list

                self.draw_circuit()  # After loading, draw everything on the scene

        except FileNotFoundError:  # If the file is missing
            print("ERROR: circuit_description.txt not found.")  # Show error message
        except ET.ParseError as e:  # If XML is malformed
            print(f"XML Parsing Error: {e}")  # Print the XML parsing error

    def draw_circuit(self):  # Function to render the circuit on the canvas
        self.scene.clear()  # Clear any previous drawings in the scene

        for name, (x, y) in self.nodes.items():  # Iterate through all nodes
            dot = QGraphicsEllipseItem(x - 4, y - 4, 8, 8)  # Create a small circle to represent a node
            dot.setPen(QPen())  # Use default pen outline
            dot.setBrush(QBrush(QColor("black")))  # Fill node with black color
            self.scene.addItem(dot)  # Add node circle to the scene

            label = QGraphicsTextItem(name)  # Create text label for the node
            label.setPos(x + 6, y - 6)  # Position the label next to the node
            self.scene.addItem(label)  # Add the label to the scene

        for comp_type, label, n1, n2 in self.components:  # Loop over all circuit components
            if n1 not in self.nodes or n2 not in self.nodes:  # Skip if nodes don't exist
                continue

            x1, y1 = self.nodes[n1]  # Get start node coordinates
            x2, y2 = self.nodes[n2]  # Get end node coordinates
            mid_x = (x1 + x2) / 2  # Midpoint x-coordinate for label
            mid_y = (y1 + y2) / 2  # Midpoint y-coordinate for label

            if comp_type == "RESISTOR":  # If component is a resistor
                segments = 4  # Number of zigzag segments
                dx = (x2 - x1) / (segments * 2)  # Segment width
                dy = (y2 - y1) / (segments * 2)  # Segment height

                for i in range(segments):  # Draw zigzag pattern
                    x_start = x1 + ((-1) ** i) * 5
                    y_start = y1 + i * 2 * dy
                    x_end = x1 + ((-1) ** (i + 1)) * 5
                    y_end = y1 + (i * 2 + 1) * dy
                    line = QGraphicsLineItem(x_start, y_start, x_end, y_end)  # Create zigzag line
                    self.scene.addItem(line)  # Add to the scene

                text = QGraphicsTextItem(label)  # Add component label
                text.setPos(mid_x + 10, mid_y - 10)  # Position label
                self.scene.addItem(text)

            elif comp_type == "CAPACITOR":  # If component is a capacitor
                dx = (x2 - x1)  # Difference in x
                dy = (y2 - y1)  # Difference in y
                length = (dx ** 2 + dy ** 2) ** 0.5  # Distance between nodes
                unit_dx = dx / length  # Normalize dx
                unit_dy = dy / length  # Normalize dy

                offset = 10  # Distance from center for terminals
                px1 = mid_x - unit_dx * offset
                py1 = mid_y - unit_dy * offset
                px2 = mid_x + unit_dx * offset
                py2 = mid_y + unit_dy * offset

                self.scene.addItem(QGraphicsLineItem(x1, y1, px1, py1))  # Wire to first plate
                self.scene.addItem(QGraphicsLineItem(x2, y2, px2, py2))  # Wire to second plate

                plate_dx = -unit_dy * 10  # Plate offset perpendicular to wire
                plate_dy = unit_dx * 10
                plate1 = QGraphicsLineItem(px1 - plate_dx, py1 - plate_dy, px1 + plate_dx, py1 + plate_dy)
                plate2 = QGraphicsLineItem(px2 - plate_dx, py2 - plate_dy, px2 + plate_dx, py2 + plate_dy)
                self.scene.addItem(plate1)  # Draw first plate
                self.scene.addItem(plate2)  # Draw second plate

                text = QGraphicsTextItem(label)  # Add label for capacitor
                text.setPos(mid_x + 8, mid_y - 8)  # Position the label
                self.scene.addItem(text)

            elif comp_type == "INDUCTOR":  # If component is an inductor
                num_loops = 4  # Number of loops
                total_length = x2 - x1  # Horizontal span
                loop_width = total_length / num_loops  # Width of one loop
                loop_radius = loop_width / 2  # Radius of each loop

                for i in range(num_loops):  # Draw each loop as a half-circle
                    cx = x1 + i * loop_width + loop_radius  # Center x of loop
                    cy = (y1 + y2) / 2  # Center y of loop
                    arc = QGraphicsEllipseItem(cx - loop_radius, cy - loop_radius, 2 * loop_radius, 2 * loop_radius)
                    arc.setStartAngle(0 * 16)  # Start at 0 degrees
                    arc.setSpanAngle(180 * 16)  # Span 180 degrees (half circle)
                    self.scene.addItem(arc)

                text = QGraphicsTextItem(label)  # Add label for inductor
                text.setPos(mid_x - 10, mid_y - 15)  # Position label
                self.scene.addItem(text)

            elif comp_type == "VOLTAGE":  # If component is a voltage source
                is_horizontal = (y1 == y2)  # Determine orientation
                line = QGraphicsLineItem(x1, y1, x2, y2)  # Draw connecting wire
                self.scene.addItem(line)

                radius = 10  # Radius of voltage source symbol
                circle = QGraphicsEllipseItem(mid_x - radius, mid_y - radius, 2 * radius, 2 * radius)
                self.scene.addItem(circle)  # Draw the voltage source circle

                plus = QGraphicsTextItem("+")  # Add "+" for polarity
                if is_horizontal:  # Position "+" depending on orientation
                    plus.setPos(mid_x - 4, mid_y - 18)
                else:
                    plus.setPos(mid_x - 4, mid_y - 10)
                self.scene.addItem(plus)

                text = QGraphicsTextItem(label)  # Voltage label
                text.setPos(mid_x + 12, mid_y - 6)  # Position the label
                self.scene.addItem(text)

            elif comp_type == "WIRE":  # If component is a wire
                line = QGraphicsLineItem(x1, y1, x2, y2)  # Draw simple wire between nodes
                self.scene.addItem(line)  # Add to scene

# Entry point of the program
if __name__ == "__main__":  # Ensure this runs only when executed directly (not imported)
    app = QApplication(sys.argv)  # Create the Qt application instance
    window = CircuitViewer()  # Create the main GUI window
    window.show()  # Show the window on screen
    sys.exit(app.exec_())  # Start the application's event loop and exit when done
