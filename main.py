import sys
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction, QPainter
from PySide6.QtWidgets import (QApplication, QHeaderView, QMainWindow, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
from PySide6.QtCharts import QChartView, QPieSeries, QChart

class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.items = 0
        #Dummy Data
        self._data = {"Water": 24, "Rent": 1000, "Coffee": 30, "Grocery": 300, "Phone": 45, "Internet": 70}
        
        #Left Widget
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Description", "Expense"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.stretch)
        
        #Chart View
        self.chart_view = QTableWidget()
        self.chart_view.setRenderHint(QPainter.Antiliasing)
        
        #QWidget Layout
        self.layout = QHBoxLayout()
        
        #Adding widget for left side (Table)
        self.layout.addWidget(self.table)
        
        #Adding layout for right side (buttons, chart, etc)
        self.layout.addLayout(self.right)
        
        #Set the layout to the widget
        self.setLayout(self.layout)
        
        #Right Widget
        self.description = QLineEdit()
        self.expense = QLineEdit()
        self.add = QPushButton("Add")
        self.clear = QPushButton("Clear")
        self.quit = QPushButton("Quit")
        self.plot = QPushButton("Plot")
        
        self.right = QVBoxLayout()
        self.addWidget(QLabel("Description"))
        self.right.addWidget(self.description)
        self.addWidget(QLabel("($)Expense"))
        self.right.addWidget(self.expense)
        self.widget.addWidget(self.add)
        self.widget.addWidget(self.plot)
        self.right.addWidget(self.chart_view)
        self.right.addWidget(self.clear)
        self.right.addWidget(self.quit)
        
        # Signals and Slots
        self.add.clicked.connect(self.add_element)
        self.add.clicked.connect(self.quit_application)
        self.plot.clicked.connect(self.plot_data)
        self.plot.clicked.connect(self.clear_table)
        self.description.textChanged[str].connect(self.check_disable)
        self.price.textChanged[str].connect(self.check_disable)
        
        
        #Add Element to the table
    def add_element(self):
        des = self.description.text()
        expense = self.expense.text()
        try:
            expense_item = QTableWidgetItem(f"{float(expense):.2f}")
            expense_item.setTextAlignment(Qt.AlignRight)
            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, QTableWidgetItem(desc))
            self.table.setItem(self.items, 1, QTableWidgetItem(str(exp)))

            self.description.setText("")
            self.expense.setText("")
            self.items += 1
            
        except ValueError:
            print("That is wrong input: ", price, " Please enter a number!")
        
    @Slot()
    def check_disable(self, x):
        if not self.description.text() or not self.expense.text():
            self.add.setEnabled(False)
        else:
            self.add.setEnabled(True)
    
    
    @Slot()
    def plot_data():
        #Get table information
        series = QPieSeries()
        for i in range(self.table.rowCount()):
            text = self.table.item(i, 0).text()
            number = float(self.table.item(i, 1).text())
            series.append(text, number)
        chart = QChart()
        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignLeft)
        self.chart_view.setChart(chart)
            
        
    @Slot()
    def quit_application(self):
        QApplication.quit()    
        
        
    def fill_table(self, data=None):
        data = self._data if not data else data
        for desc, exp in data.items():
            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, QTableWidgetItem(desc))
            self.table.setItem(self.items, 1, QTableWidgetItem(str(exp)))
            self.items += 1
            
    @Slot()
    def clear_table(self):
        self.table.setRowCount(0)
        self.items = 0
        

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Expense Tracker")

        #Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        
        #Exit the QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)
        self.file_menu.addAction(exit_action)
        
    @Slot()
    def exit_app(self, checked):
        QApplication.quit()



if __name__ == "__main__":
    
    #Qt Application
    app = QApplication(sys.argv)
    #QWidget
    widget = QWidget()
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    
    #Execite Application
    sys.exit(app.exec())