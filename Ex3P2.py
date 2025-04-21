import sys
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGraphicsScene,
    QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem
)
from PyQt5.QtGui import QPen, QBrush, QColor
from P2py import Ui_P2


class CircuitViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_P2()
        self.ui.setupUi(self)

        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

        self.nodes = {}
        self.components = []

        self.ui.btn_load_circuit.clicked.connect(self.load_circuit)
        # self.load_circuit()  # Removed to wait for button press

    def load_circuit(self):
        file_path = "circuit_description.txt"
        try:
            with open(file_path, 'r') as file:
                self.nodes.clear()
                self.components.clear()

                wrapped = "<root>\n" + file.read() + "\n</root>"
                root = ET.fromstring(wrapped)

                for element in root:
                    tag = element.tag.lower()

                    if tag == "node":
                        name = element.attrib["name"]
                        x = int(element.attrib["x"])
                        y = int(element.attrib["y"])
                        self.nodes[name] = (x, y)
                    else:
                        name = element.attrib["name"]
                        n1 = element.attrib["n1"]
                        n2 = element.attrib["n2"]
                        self.components.append((tag.upper(), name, n1, n2))

                self.draw_circuit()

        except FileNotFoundError:
            print("ERROR: circuit_description.txt not found.")
        except ET.ParseError as e:
            print(f"XML Parsing Error: {e}")

    def draw_circuit(self):
        self.scene.clear()

        for name, (x, y) in self.nodes.items():
            dot = QGraphicsEllipseItem(x - 4, y - 4, 8, 8)
            dot.setPen(QPen())
            dot.setBrush(QBrush(QColor("black")))
            self.scene.addItem(dot)

            label = QGraphicsTextItem(name)
            label.setPos(x + 6, y - 6)
            self.scene.addItem(label)

        for comp_type, label, n1, n2 in self.components:
            if n1 not in self.nodes or n2 not in self.nodes:
                continue

            x1, y1 = self.nodes[n1]
            x2, y2 = self.nodes[n2]
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2

            if comp_type == "RESISTOR":
                segments = 4
                dx = (x2 - x1) / (segments * 2)
                dy = (y2 - y1) / (segments * 2)

                for i in range(segments):
                    x_start = x1 + ((-1) ** i) * 5
                    y_start = y1 + i * 2 * dy
                    x_end = x1 + ((-1) ** (i + 1)) * 5
                    y_end = y1 + (i * 2 + 1) * dy
                    line = QGraphicsLineItem(x_start, y_start, x_end, y_end)
                    self.scene.addItem(line)

                text = QGraphicsTextItem(label)
                text.setPos(mid_x + 10, mid_y - 10)
                self.scene.addItem(text)

            elif comp_type == "CAPACITOR":
                dx = (x2 - x1)
                dy = (y2 - y1)
                length = (dx ** 2 + dy ** 2) ** 0.5
                unit_dx = dx / length
                unit_dy = dy / length

                offset = 10
                px1 = mid_x - unit_dx * offset
                py1 = mid_y - unit_dy * offset
                px2 = mid_x + unit_dx * offset
                py2 = mid_y + unit_dy * offset

                self.scene.addItem(QGraphicsLineItem(x1, y1, px1, py1))
                self.scene.addItem(QGraphicsLineItem(x2, y2, px2, py2))

                plate_dx = -unit_dy * 10
                plate_dy = unit_dx * 10
                plate1 = QGraphicsLineItem(px1 - plate_dx, py1 - plate_dy, px1 + plate_dx, py1 + plate_dy)
                plate2 = QGraphicsLineItem(px2 - plate_dx, py2 - plate_dy, px2 + plate_dx, py2 + plate_dy)
                self.scene.addItem(plate1)
                self.scene.addItem(plate2)

                text = QGraphicsTextItem(label)
                text.setPos(mid_x + 8, mid_y - 8)
                self.scene.addItem(text)

            elif comp_type == "INDUCTOR":
                num_loops = 4
                total_length = x2 - x1
                loop_width = total_length / num_loops
                loop_radius = loop_width / 2

                for i in range(num_loops):
                    cx = x1 + i * loop_width + loop_radius
                    cy = (y1 + y2) / 2
                    arc = QGraphicsEllipseItem(cx - loop_radius, cy - loop_radius, 2 * loop_radius, 2 * loop_radius)
                    arc.setStartAngle(0 * 16)
                    arc.setSpanAngle(180 * 16)
                    self.scene.addItem(arc)

                text = QGraphicsTextItem(label)
                text.setPos(mid_x - 10, mid_y - 15)
                self.scene.addItem(text)

            elif comp_type == "VOLTAGE":
                is_horizontal = (y1 == y2)
                line = QGraphicsLineItem(x1, y1, x2, y2)
                self.scene.addItem(line)

                radius = 10
                circle = QGraphicsEllipseItem(mid_x - radius, mid_y - radius, 2 * radius, 2 * radius)
                self.scene.addItem(circle)

                plus = QGraphicsTextItem("+")
                if is_horizontal:
                    plus.setPos(mid_x - 4, mid_y - 18)
                else:
                    plus.setPos(mid_x - 4, mid_y - 10)
                self.scene.addItem(plus)

                text = QGraphicsTextItem(label)
                text.setPos(mid_x + 12, mid_y - 6)
                self.scene.addItem(text)

            elif comp_type == "WIRE":
                line = QGraphicsLineItem(x1, y1, x2, y2)
                self.scene.addItem(line)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CircuitViewer()
    window.show()
    sys.exit(app.exec_())