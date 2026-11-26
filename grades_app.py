import os
import subprocess
import sys

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class GradesWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ""
        self.header_line = "ID,Grade\n"

        self.setWindowTitle("Grades Updater")

        self.load_button = QPushButton("Load Grades File")
        self.load_button.clicked.connect(self.load_file)

        self.bonus_label = QLabel("Bonus Points:")
        self.bonus_input = QSpinBox()
        self.bonus_input.setRange(-100, 100)
        self.bonus_input.editingFinished.connect(self.apply_bonus)

        self.update_button = QPushButton("Update File")
        self.update_button.clicked.connect(self.update_file)

        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.show_about)

        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Original Grades", "Corrected Grades"]
        )
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.load_button)
        top_layout.addWidget(self.bonus_label)
        top_layout.addWidget(self.bonus_input)
        top_layout.addWidget(self.update_button)
        top_layout.addWidget(self.about_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select Grades File", "", "CSV Files (*.csv);;All Files (*)"
        )
        if filename:
            self.selected_file = filename
            self.student_ids = []
            self.original_grades = []
            self.corrected_grades = []

            with open(filename, "r") as f:
                self.header_line = next(f)
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) >= 2:
                        student_id = parts[0]
                        grade = int(float(parts[1]))
                        self.student_ids.append(student_id)
                        self.original_grades.append(grade)
                        self.corrected_grades.append(grade)

            self.fill_table()

    def fill_table(self):
        self.table.setRowCount(max(50, len(self.student_ids)))
        for row, (s_id, orig, corr) in enumerate(
            zip(self.student_ids, self.original_grades, self.corrected_grades)
        ):
            self.table.setItem(row, 0, QTableWidgetItem(str(s_id)))
            self.table.setItem(row, 1, QTableWidgetItem(str(orig)))
            self.table.setItem(row, 2, QTableWidgetItem(str(corr)))

    def apply_bonus(self):
        bonus = self.bonus_input.value()
        self.corrected_grades = []
        for orig in self.original_grades:
            new_grade = orig + bonus
            if new_grade > 100:
                new_grade = 100
            elif new_grade < 0:
                new_grade = 0
            self.corrected_grades.append(new_grade)

        self.fill_table()

    def update_file(self):
        if not self.selected_file:
            return

        with open(self.selected_file, "w") as f:
            f.write(self.header_line)
            for s_id, corr in zip(self.student_ids, self.corrected_grades):
                f.write(f"{s_id},{corr}\n")

        # Open updated file according to OS
        if sys.platform.startswith("win"):
            os.startfile(self.selected_file)
        elif sys.platform == "darwin":
            subprocess.call(["open", self.selected_file])
        else:
            subprocess.call(["xdg-open", self.selected_file])

    def show_about(self):
        QMessageBox.information(
            self,
            "About",
            "Grades Updater App\n"
            "Created by: Yuval Barkai\n"
            "GitHub: https://github.com/YOUR_USERNAME/YOUR_REPO",
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QMainWindow {
            background-color: #f4f6f9;
        }
        QPushButton {
            background-color: #2b579a;
            color: white;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #1e3f73;
        }
        QSpinBox {
            padding: 6px;
            border: 1px solid #cccccc;
            border-radius: 4px;
            font-size: 14px;
            background-color: white;
        }
        QTableWidget {
            background-color: white;
            gridline-color: #e0e0e0;
            font-size: 13px;
        }
        QHeaderView::section {
            background-color: #e9eef5;
            padding: 6px;
            border: 1px solid #d0d7de;
            font-weight: bold;
        }
    """)

    window = GradesWindow()
    window.resize(750, 600)
    window.show()
    sys.exit(app.exec())