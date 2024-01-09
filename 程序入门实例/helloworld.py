from PyQt6.QtWidgets import QApplication, QWidget
import sys

app = QApplication(sys.argv)
# print(sys.argv)

window = QWidget()
window.show()
window.setWindowTitle("学习Python")
window.resize(400,300)

sys.exit(app.exec())