import sys
import pandas as pd
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QBrush, QColor, QPainter, QFont
from PySide6.QtWidgets import (QApplication, QWidget,
                               QLabel, QVBoxLayout,
                               QHBoxLayout, QPushButton,
                               QColorDialog, QFrame)

class Board:
    def __init__(self, size = 8):
        self.size = size
        self.grid = pd.DataFrame(None, range(size), columns=range(size))
        for i, row in self.grid.iterrows():
            for j in range(len(row)):
                self.grid.iloc[i, j] = SquareWidget(i, j)

    def display_grid(self):
        msg = ""
        for row in range(self.size):
            for col in range(self.size):
                c = self.grid.iloc[row, col].hit_char
                msg += c + " "
            msg += "\n"
        return(msg)

class SquareWidget(QWidget):
    def __init__(self, row, col, size = 50):
        super().__init__()
        self.row = row
        self.col = col
        self.square_size = size
        self.hit = False
        self.default_color = QBrush(QColor(255, 0, 0))
        self.hit_color = QBrush(QColor(0, 0, 255))

    @property
    def rect_colour(self):
        if self.hit:
            return self.hit_color
        return self.default_color

    def __str__(self):
        return f"({self.row}, {self.col}): {self.hit_char}"

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        square_rect = QRect(self.square_y, self.square_x, self.square_size, self.square_size)
        painter.fillRect(square_rect, self.rect_colour)

    @property
    def square_x(self):
        return self.row * self.square_size

    @property
    def square_y(self):
        return self.col * self.square_size

    @property
    def hit_char(self):
        if self.hit:
            return "x"
        return "0"

class LogMove(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Log the Square")
        self.setGeometry(parent.x() + parent.width(),
                         parent.y(), 200, 3000)
        self.setFixedSize(200, 300)
        self.layout = QVBoxLayout()
        self.txtBox = QLabel("")
        self.txtBox.setWordWrap(False)
        self.txtBox.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.txtBox)
        self.setLayout(self.layout)
        font = QFont()
        font.setFamily("Courier")
        font.setPointSize(12)
        font.setBold(True)
        self.txtBox.setFont(font)
        
class GameBoard(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Move the Square")
        self.setGeometry(100, 100, 410, 410)
        self.setFixedSize(410, 410)
        self.square_size = 50
        self.picked_colour = QBrush(QColor(255, 0, 0))
        self.board = Board()
        self.logger = LogMove(self)
        self.parent = parent

        self.row = 1
        self.old_row = 0
        self.col = 1
        self.old_col = 0
        self.move_type = 0
        self.update_board()

    def keyPressEvent(self, event):
        key = event.key()
        self.old_row = self.row
        self.old_col = self.col
        
        if key == Qt.Key_Up and self.row > 1:
            self.row -= 1
            self.move_type = 1
        elif key == Qt.Key_Down and self.row < self.board.size:
            self.row += 1
            self.move_type = 1
        elif key == Qt.Key_Left and self.col > 1:
            self.col -= 1
            self.move_type = 1
        elif key == Qt.Key_Right and self.col < self.board.size:
            self.col += 1
            self.move_type = 1
        elif key == Qt.Key_Space:
            self.move_type = 2

        self.update_board()

    def update_board(self):
        sq = self.board.grid.iloc[self.row - 1, self.col - 1]
        txt = self.logger.txtBox

        if self.move_type == 1:
            old_sq = self.board.grid.iloc[self.old_row - 1, self.old_col - 1]
            if not old_sq.hit:
                old_sq.setParent(None)

        if self.move_type == 2:
            if sq.hit:
                sq.hit = False
                sq.setParent(None)
            else:
                sq.hit = True
                sq.hit_color = self.parent.picked_color
            txt.setText(self.board.display_grid())

        sq.setParent(self)
        sq.show()

        self.logger.update()
        self.logger.show()
  
        self.setFocus()
        self.update()
        self.show()

        self.move_type = 0

            
class MainApp(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Game")
        layout = QHBoxLayout()
        self.picked_color = QBrush(QColor(255, 0, 0))
        self.game = GameBoard(self)
        button = QPushButton("Quit")
        col_button = QPushButton("Select Colour")
        button.clicked.connect(QApplication.quit)
        col_button.clicked.connect(self.select_colour)
        self.create_rectangle()
        layout.addWidget(self.game)
        layout.addWidget(self.game.logger)
        self.game.logger.layout.addWidget(button)
        self.game.logger.layout.addWidget(self.rectangle_frame)
        self.game.logger.layout.addWidget(col_button)
        self.setLayout(layout)
        self.game.setFocus()

    def create_rectangle(self):
        self.rectangle_frame = QFrame()
        self.rectangle_frame.setFrameShape(QFrame.Box)  # Set the frame shape to a box (rectangle)
        self.rectangle_frame.setFrameShadow(QFrame.Plain)  # Set the frame shadow
        
        # Set the size and position of the rectangle within its layout
        self.rectangle_frame.setFixedSize(50, 50)  # Set the size of the rectangle
        self.rectangle_frame.setGeometry(QRect(0, 0, 50, 50))  # Set the position of the rectangle

    def select_colour(self):
        color_dialog = QColorDialog(self)
        color = color_dialog.getColor()
        
        if color.isValid():
            # Do something with the selected color (here, just print the RGB values)
            self.rectangle_frame.setStyleSheet(
                f"background-color: rgb({color.red()}, {color.green()}, {color.blue()});")
            self.picked_color = QBrush(QColor(color.red(),
                                              color.green(), color.blue()))
        self.game.setFocus()
                  
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()