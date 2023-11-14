import sys
from PySide6.QtWidgets import (QMainWindow,
                               QApplication, QFileDialog)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from squares import MainApp as MainWindow

class MainApp(QMainWindow):

    def __init__(self):
        super().__init__()
        # Create a File menu
        self.gen_menubar()
        self.gen_mainview()


    def gen_menubar(self):
        file_menu = self.menuBar().addMenu('File')

        # Add a Save action to the File menu
        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_image)
        file_menu.addAction(save_action)

    def gen_mainview(self):
        self.window = MainWindow()
        self.setCentralWidget(self.window)
        self.window.game.setFocus()      

    def save_image(self):
        capture = self.window.grab()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png)")

        if file_name:
            capture.save(file_name, "PNG")
            print(f"Screenshot saved as {file_name}")

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
