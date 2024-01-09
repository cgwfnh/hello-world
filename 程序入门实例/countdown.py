
import sys

from PyQt6 import QtGui
from PyQt6.QtCore import QTimer, Qt, QTime
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QApplication, QMessageBox,QMainWindow


class CountdownTimer1():
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Countdown Timer")
        self.setFixedSize(300, 150)

        self.countdown_label = QLabel("00:00")
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 30px;")

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_timer)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_timer)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_timer)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)

        self.minutes = 10
        self.seconds = 00

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.countdown_label)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.reset_button)
        self.setLayout(self.layout)

    def start_timer(self):
        self.timer.start()

    def stop_timer(self):
        self.timer.stop()

    def reset_timer(self):
        self.timer.stop()
        self.minutes = 0
        self.seconds = 0
        self.countdown_label.setText("00:00")

    def update_timer(self):
        if self.seconds == 0:
            if self.minutes == 0:
                self.timer.stop()
            else:
                self.minutes -= 1
                self.seconds = 59
        else:
            self.seconds -= 1

        self.countdown_label.setText(f"{self.minutes:02d}:{self.seconds:02d}")


class CountdownTimer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Countdown Timer")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.resize(300, 200)

        self.label = QLabel(self)
        self.label.setText("00:00:00")
        self.label.setFont(QtGui.QFont("Arial", 36))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.start_button = QPushButton(self)
        self.start_button.setText("Start")
        self.start_button.clicked.connect(self.start_timer)

        self.pause_button = QPushButton(self)
        self.pause_button.setText("Pause")
        self.pause_button.clicked.connect(self.pause_timer)

        self.stop_button = QPushButton(self)
        self.stop_button.setText("Stop")
        self.stop_button.clicked.connect(self.stop_timer)

        self.reset_button = QPushButton(self)
        self.reset_button.setText("Reset")
        self.reset_button.clicked.connect(self.reset_timer)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.pause_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.reset_button)

        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.setInterval(1000)  # 1 second
        self.timer.timeout.connect(self.update_timer)

        self.time_remaining = 0

    def start_timer(self):
        if self.time_remaining == 0:
            self.time_remaining = 60 * 60  # 1 hour

        self.timer.start()
        self.start_button.setDisabled(True)

    def pause_timer(self):
        self.timer.stop()

    def stop_timer(self):
        self.timer.stop()
        self.time_remaining = 0

    def reset_timer(self):
        self.timer.stop()
        self.time_remaining = 0
        self.label.setText("00:00:00")

    def update_timer(self):
        self.time_remaining -= 1

        hours = self.time_remaining // 3600
        minutes = (self.time_remaining % 3600) // 60
        seconds = self.time_remaining % 60

        self.label.setText("{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds))

        if self.time_remaining == 0:
            self.timer.stop()
            QMessageBox.information(self, "Timer", "Time's up!")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Countdown Timer")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)

        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setFont(QFont("Arial", 24))

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_timer)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_timer)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_timer)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.time_label)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.reset_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.start_time = QTime()
        self.end_time = QTime()

    def start_timer(self):
        self.start_time = QTime.currentTime()
        self.timer.start()

    def stop_timer(self):
        self.timer.stop()
        self.end_time = QTime.currentTime()

    def reset_timer(self):
        self.start_time = QTime()
        self.end_time = QTime()
        self.update_timer()

    def update_timer(self):
        current_time = QTime.currentTime()
        remaining_time = self.end_time.secsTo(current_time) - self.start_time.secsTo(current_time)
        if remaining_time < 0:
            remaining_time = 0
        self.time_label.setText(remaining_time)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    timer = CountdownTimer()
    timer.show()
    sys.exit(app.exec())