'''
使用PyQt6, 设计一个可以伸缩的窗口，当鼠标右键选择设置时，展开当前窗口，显示字体、窗口透明度等设置，并可以自动把设置的内容保存到文件中。

'''
import sys
import os

from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QFont, QCursor, QFontDatabase
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpinBox, QComboBox, \
    QSlider, QFileDialog, QGridLayout


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Expandable Settings Window")
        self.resize(300, 200)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.button_settings = QPushButton("Settings")
        self.button_settings.clicked.connect(self.show_settings_window)
        self.main_layout.addWidget(self.button_settings)

        self.settings_window = QWidget()
        self.settings_window.setWindowTitle("Settings")
        self.settings_window.resize(400, 300)
        self.settings_window.hide()

        self.settings_layout = QGridLayout()
        self.settings_window.setLayout(self.settings_layout)

        self.font_label = QLabel("Font:")
        self.settings_layout.addWidget(self.font_label, 0, 0)

        self.font_combo_box = QComboBox()
        self.font_combo_box.addItems(QFontDatabase.families())
        self.font_combo_box.currentIndexChanged.connect(self.update_font)
        self.settings_layout.addWidget(self.font_combo_box, 0, 1)

        self.font_size_label = QLabel("Font Size:")
        self.settings_layout.addWidget(self.font_size_label, 1, 0)

        self.font_size_spin_box = QSpinBox()
        self.font_size_spin_box.setRange(1, 50)
        self.font_size_spin_box.valueChanged.connect(self.update_font)
        self.settings_layout.addWidget(self.font_size_spin_box, 1, 1)

        self.transparency_label = QLabel("Transparency:")
        self.settings_layout.addWidget(self.transparency_label, 2, 0)

        self.transparency_slider = QSlider(Qt.Orientation.Horizontal)
        self.transparency_slider.setRange(0, 100)
        self.transparency_slider.valueChanged.connect(self.update_transparency)
        self.settings_layout.addWidget(self.transparency_slider, 2, 1)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.settings_layout.addWidget(self.save_button, 3, 1)

        self.load_settings()

    def show_settings_window(self):
        if self.settings_window.isVisible():
            self.settings_window.hide()
        else:
            self.settings_window.show()

    def update_font(self):
        font = QFont(self.font_combo_box.currentText(), self.font_size_spin_box.value())
        self.setFont(font)

    def update_transparency(self):
        transparency = self.transparency_slider.value()
        self.setWindowOpacity(transparency / 100)

    def save_settings(self):
        settings = QSettings("My Company", "My Application")

        settings.setValue("font_family", self.font_combo_box.currentText())
        settings.setValue("font_size", self.font_size_spin_box.value())
        settings.setValue("transparency", self.transparency_slider.value())

        self.settings_window.hide()

    def load_settings(self):
        settings = QSettings("My Company", "My Application")

        font_family = settings.value("font_family", "Arial")
        font_size = settings.value("font_size", 12)
        transparency = settings.value("transparency", 100)

        self.font_combo_box.setCurrentText(font_family)
        self.font_size_spin_box.setValue(font_size)
        self.transparency_slider.setValue(transparency)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
