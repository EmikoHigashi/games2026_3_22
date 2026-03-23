import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QColorDialog, QLabel, QGraphicsView, QGraphicsScene, QGraphicsRectItem
)
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import QRectF

CELL_SIZE = 20

class PixelCanvas(QGraphicsView):
    def __init__(self, grid_size):
        super().__init__()
        self.grid_size = grid_size
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.color = QColor("black")
        self.cells = {}

        self.init_grid()

    def init_grid(self):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = QGraphicsRectItem(QRectF(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                rect.setBrush(QBrush(QColor("white")))
                rect.setPen(QColor("gray"))
                rect.setFlag(QGraphicsRectItem.ItemIsSelectable)
                self.scene.addItem(rect)
                self.cells[(x, y)] = rect

    def mousePressEvent(self, event):
        pos = self.mapToScene(event.pos())
        x = int(pos.x() // CELL_SIZE)
        y = int(pos.y() // CELL_SIZE)
        if (x, y) in self.cells:
            self.cells[(x, y)].setBrush(QBrush(self.color))

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("8bit風ペイント - PyQt版")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.size_selector = QComboBox()
        self.size_selector.addItems(["16", "32", "64"])
        self.layout.addWidget(QLabel("キャンバスサイズを選んでね"))
        self.layout.addWidget(self.size_selector)

        self.start_button = QPushButton("スタート！")
        self.start_button.clicked.connect(self.start_painting)
        self.layout.addWidget(self.start_button)

    def start_painting(self):
        size = int(self.size_selector.currentText())
        self.hide()
        self.editor = PaintEditor(size)
        self.editor.show()

class PaintEditor(QWidget):
    def __init__(self, grid_size):
        super().__init__()
        self.setWindowTitle("ドット絵エディタ")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.canvas = PixelCanvas(grid_size)
        self.layout.addWidget(self.canvas)

        color_btn = QPushButton("色を選ぶ")
        color_btn.clicked.connect(self.choose_color)
        self.layout.addWidget(color_btn)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas.color = color

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
