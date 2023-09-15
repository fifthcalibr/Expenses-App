from PySide6.QtCore import Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        
        #Dummy Data
        self._data = {"Water": 24, "Rent": 1000, "Coffee": 30, "Grocery": 300, "Phone": 45, "Internet": 70}
        
        #Left Widget
        self.table = QTableWidget()
        self.table.setColumnCount(2)

class MainWindom(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Expense Tracker")

        #Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        
        #Exit the QAction
        exit_action = QAction("Exit", self)
        exit_action.setshortcut("Ctrl+Q")
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