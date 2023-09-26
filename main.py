import sys
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction, QPainter
from PySide6.QtWidgets import (QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit, QMainWindow, 
                               QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
from PySide6.QtCharts import QChartView, QPieSeries, QChart

class ExpenseTracker(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.expense_count = 0
        
        #self.expense_data = {"Rent": 1200, "Internet": 170, "Grocery": 500, "Phone": 175, "Gas": 400, "Car": 450}

        # Left Side
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Description", "Expense in $"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Total Label and Value
        self.total_label = QLabel("Total:")
        self.total_value = QLabel("0.00")
        self.total_value.setAlignment(Qt.AlignRight)

        # Chart
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # Right Widget
        self.description = QLineEdit()
        self.price = QLineEdit()
        self.add = QPushButton("Add")
        self.clear = QPushButton("Clear")
        self.quit = QPushButton("Quit")
        self.plot = QPushButton("Plot")

        # Disabling 'Add' button
        self.add.setEnabled(False)

        self.right = QVBoxLayout()
        self.right.addWidget(QLabel("Description"))
        self.right.addWidget(self.description)
        self.right.addWidget(QLabel("Price"))
        self.right.addWidget(self.price)
        self.right.addWidget(self.add)
        self.right.addWidget(self.plot)
        self.right.addWidget(self.chart_view)
        self.right.addWidget(self.total_label)
        self.right.addWidget(self.total_value)
        self.right.addWidget(self.clear)
        self.right.addWidget(self.quit)

        # QWidget Layout
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.right)

        # Set the layout to the QWidget
        self.setLayout(self.layout)

        # Signals and Slots
        self.add.clicked.connect(self.add_expense)
        self.quit.clicked.connect(self.quit_application)
        self.plot.clicked.connect(self.plot_expenses)
        self.clear.clicked.connect(self.clear_table)
        self.description.textChanged[str].connect(self.check_disable)
        self.price.textChanged[str].connect(self.check_disable)

    @Slot()
    def add_expense(self):
        description = self.description.text()
        price = self.price.text()

        try:
            # Remove the "$" sign if it exists
            price = price.replace('$', '')

            price_item = QTableWidgetItem(f"{float(price):.2f}")
            price_item.setTextAlignment(Qt.AlignRight)

            self.table.insertRow(self.expense_count)
            description_item = QTableWidgetItem(description)

            self.table.setItem(self.expense_count, 0, description_item)
            self.table.setItem(self.expense_count, 1, price_item)

            self.description.setText("")
            self.price.setText("")

            self.expense_count += 1

            # Update the total
            self.update_total()
        except ValueError:
            print("Invalid input for price:", price, "Make sure to enter a valid price!")

    @Slot()
    def check_disable(self, x):
        if not self.description.text() or not self.price.text():
            self.add.setEnabled(False)
        else:
            self.add.setEnabled(True)

    @Slot()
    def plot_expenses(self):
        # Get table information
        series = QPieSeries()
        for i in range(self.table.rowCount()):
            text = self.table.item(i, 0).text()
            number = float(self.table.item(i, 1).text())
            series.append(text, number)

        chart = QChart()
        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignLeft)
        self.chart_view.setChart(chart)

        # Update the total after plotting
        total = self.calculate_total()
        self.total_value.setText(f"${total:.2f}")

    @Slot()
    def quit_application(self):
        QApplication.quit()

    @Slot()
    def clear_table(self):
        self.table.setRowCount(0)
        self.expense_count = 0

    def update_total(self):
        total = self.calculate_total()
        self.total_value.setText(f"${total:.2f}")

    def calculate_total(self):
        total = 0.0
        for row in range(self.table.rowCount()):
            try:
                price = float(self.table.item(row, 1).text())
                total += price
            except ValueError:
                pass
        return total

class ExpenseTrackerApp(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Expense Tracker App")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        self.file_menu.addAction(exit_action)
        self.setCentralWidget(widget)

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()

if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    # QWidget
    widget = ExpenseTracker()
    # QMainWindow using QWidget as the central widget
    window = ExpenseTrackerApp(widget)
    window.resize(800, 600)
    window.show()

    # Execute the application
    sys.exit(app.exec())
