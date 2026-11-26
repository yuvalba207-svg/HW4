import sys

from About import AboutWindow
import numpy as np
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT,
)
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class IceCreamWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.temperatures = []
        self.revenues = []

        self.setWindowTitle("Ice Cream Revenue Analysis")

        self.load_button = QPushButton("Load Ice Cream CSV")
        self.load_button.clicked.connect(self.load_file)

        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.show_about)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.ax = self.figure.add_subplot(111)

        top_bar = QHBoxLayout()
        top_bar.addWidget(self.load_button)
        top_bar.addWidget(self.about_button)

        layout = QVBoxLayout()
        layout.addLayout(top_bar)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.draw_graph()

    def load_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select Ice Cream File", "", "CSV Files (*.csv);;All Files (*)"
        )
        if filename:
            self.temperatures = []
            self.revenues = []

            with open(filename, "r") as f:
                next(f)
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) >= 2:
                        self.temperatures.append(float(parts[0]))
                        self.revenues.append(float(parts[1]))

            self.draw_graph()

    def draw_graph(self):
        self.ax.clear()

        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)

        if self.temperatures and self.revenues:
            self.ax.scatter(self.temperatures, self.revenues, s=1, label="Daily Data")

            # Linear trendline
            x_arr = np.array(self.temperatures)
            y_arr = np.array(self.revenues)
            m, b = np.polyfit(x_arr, y_arr, 1)

            x_line = np.linspace(x_arr.min(), x_arr.max(), 100)
            y_line = m * x_line + b
            equation_text = f"y = {m:.2f}x + {b:.2f}"
            self.ax.plot(
                x_line,
                y_line,
                color="red",
                linewidth=1.5,
                label=f"Trendline: {equation_text}",
            )
            self.ax.legend()

        self.ax.set_title("Ice Cream Revenue vs. Outside Temperature")
        self.ax.set_xlabel("Temperature [°C / °F]")
        self.ax.set_ylabel("Revenue [$]")
        self.canvas.draw()

    def show_about(self):
        self.about_window = AboutWindow()
        self.about_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QMainWindow {
            background-color: #f8f9fa;
        }
        QPushButton {
            background-color: #0078d4;
            color: white;
            border-radius: 6px;
            padding: 8px 18px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #005a9e;
        }
    """)

    window = IceCreamWindow()
    window.resize(850, 650)
    window.show()
    sys.exit(app.exec())