import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider, QSizePolicy
)
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QTimer, QRect

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class GridWidget(QWidget):
    def __init__(self, grid, cell_size=10, x_offset=20, y_offset=60):
        super().__init__()
        self.grid = grid
        self.cell_size = cell_size
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.setMinimumWidth(grid.shape[1] * cell_size + x_offset * 2)
        self.setMinimumHeight(grid.shape[0] * cell_size + y_offset + 20)

    def paintEvent(self, event):
        qp = QPainter(self)
        for y in range(self.grid.shape[0]):
            for x in range(self.grid.shape[1]):
                rect_x = x * self.cell_size + self.x_offset
                rect_y = y * self.cell_size + self.y_offset
                color = QColor(0, 0, 0) if self.grid[y][x] == 1 else QColor(255, 255, 255)
                qp.fillRect(QRect(rect_x, rect_y, self.cell_size - 1, self.cell_size - 1), color)


class GameOfLife(QWidget):
    def __init__(self, grid_size=50, cell_size=10):
        super().__init__()
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.grid = (np.random.rand(grid_size, grid_size) < 0.2).astype(int)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_state)
        self.generation = 0
        self.live_history = []

        self.grid_widget = GridWidget(self.grid, cell_size=self.cell_size)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Conway\'s Game of Life')
        self.setMinimumSize(1000, 600)

        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.toggle_timer)

        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.clear_grid)

        self.random_button = QPushButton('Randomize')
        self.random_button.clicked.connect(self.randomize_grid)

        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(10, 1000)
        self.speed_slider.setValue(300)
        self.speed_slider.setTickInterval(10)
        self.speed_slider.valueChanged.connect(self.change_speed)

        controls = QHBoxLayout()
        controls.addWidget(self.start_button)
        controls.addWidget(self.clear_button)
        controls.addWidget(self.random_button)
        controls.addWidget(QLabel('Speed'))
        controls.addWidget(self.speed_slider)

        self.plot_fig = Figure(figsize=(5, 4))
        self.plot_canvas = FigureCanvas(self.plot_fig)
        self.ax = self.plot_fig.add_subplot(111)
        self.ax.set_title("Live Cell Metrics Over Time")
        self.ax.set_xlabel("Generation")
        self.ax.set_ylabel("Metric Value")

        self.metrics_label = QLabel(
            "<b>Metrics:</b><br>"
            "🔵 <b>Live Cells</b>: total live cells per generation<br>"
            "🟠 <b>Occupancy %</b>: percentage of grid filled<br>"
            "🟢 <b>Growth Δ</b>: live cell difference from previous gen"
        )
        self.metrics_label.setWordWrap(True)

        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.plot_canvas)
        plot_layout.addWidget(self.metrics_label)

        main_layout = QVBoxLayout()
        content_layout = QHBoxLayout()
        content_layout.addWidget(self.grid_widget)
        content_layout.addLayout(plot_layout, stretch=1)

        main_layout.addLayout(controls)
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def update_state(self):
        neighbors = sum(np.roll(np.roll(self.grid, i, 0), j, 1)
                        for i in (-1, 0, 1) for j in (-1, 0, 1)
                        if (i != 0 or j != 0))
        new_grid = ((self.grid == 1) & ((neighbors == 2) | (neighbors == 3))) | \
                   ((self.grid == 0) & (neighbors == 3))
        self.grid[:, :] = new_grid.astype(int)
        self.grid_widget.repaint()
        self.update_plot()

    def update_plot(self):
        self.generation += 1
        live_cells = np.sum(self.grid)
        self.live_history.append(live_cells)

        generations = list(range(1, len(self.live_history) + 1))
        occupancy = [(v / (self.grid_size ** 2)) * 100 for v in self.live_history]
        growth = [0] + [self.live_history[i] - self.live_history[i - 1] for i in range(1, len(self.live_history))]

        self.ax.clear()
        self.ax.plot(generations, self.live_history, label="Live Cells", color="blue")
        self.ax.plot(generations, occupancy, label="Occupancy %", color="orange")
        self.ax.plot(generations, growth, label="Growth Δ", color="green")
        self.ax.set_xlabel("Generation")
        self.ax.set_ylabel("Metric Value")
        self.ax.legend()
        self.plot_canvas.draw()

    def toggle_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_button.setText('Start')
        else:
            self.timer.start(self.speed_slider.value())
            self.start_button.setText('Stop')

    def clear_grid(self):
        self.grid[:] = 0
        self.live_history = []
        self.generation = 0
        self.grid_widget.repaint()
        self.update_plot()

    def randomize_grid(self):
        self.grid[:] = (np.random.rand(self.grid_size, self.grid_size) < 0.2).astype(int)
        self.live_history = []
        self.generation = 0
        self.grid_widget.repaint()
        self.update_plot()

    def change_speed(self, value):
        if self.timer.isActive():
            self.timer.setInterval(value)

    def mousePressEvent(self, event):
        x = (event.x() - self.grid_widget.x_offset) // self.cell_size
        y = (event.y() - self.grid_widget.y_offset) // self.cell_size
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            self.grid[y][x] = 1 - self.grid[y][x]
            self.grid_widget.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = GameOfLife(grid_size=50, cell_size=10)
    game.show()
    sys.exit(app.exec_())
