# generate pyqt6 window

import json
import sys, os
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QTableWidgetItem, QPushButton, QSpacerItem, \
    QLineEdit, QTableWidget, QLabel
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt


BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

# 状态映射
STATUS_MAPPING = {
    0: "初始化中",
    1: "待执行",
    2: "正在执行",
    3: "完成并提醒",
    10: "异常并停止",
    11: "初始化失败",
}

# main window class
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.resize(1228, 450)

        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)

        # 1 创建布局
        self.layout = QVBoxLayout(self)
        
        self.layout.addLayout(self.init_header())
        self.layout.addLayout(self.init_form())
        self.layout.addLayout(self.init_table())
        self.layout.addLayout(self.init_footer())

        self.show()

    def init_header(self):
        # 2 创建头部布局
        header_layout = QHBoxLayout()
        btn_start = QtWidgets.QPushButton("开始")
        btn_start.show()
        btn_stop = QPushButton("停止")
        header_layout.addWidget(btn_start)
        header_layout.addWidget(btn_stop)
        header_space_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        header_layout.addItem(header_space_item)

        return header_layout
    

    def init_form(self):
        # 3 创建表单布局
        form_layout = QHBoxLayout()
        lineedit = QLineEdit()
        lineedit.setPlaceholderText("请输入商品ID和价格，例如：B0818JJJQQ8=88")
        form_layout.addWidget(lineedit)
        btn_add = QPushButton("添加")
        form_layout.addWidget(btn_add)

        return form_layout
    
    def init_table(self):
         # 4 创建表格布局
        table_layout = QHBoxLayout()
        table_widget = QTableWidget(self)
        
        # 4.1 创建表格
        table_header = [
            {"field": "asin", "text": "ASIN", 'width': 120},
            {"field": "title", "text": "标题", 'width': 150},
            {"field": "url", "text": "URL", 'width': 400},
            {"field": "price", "text": "底价", 'width': 100},
            {"field": "success", "text": "成功次数", 'width': 100},
            {"field": "error", "text": "503次数", 'width': 100},
            {"field": "status", "text": "状态", 'width': 100},
            {"field": "frequency", "text": "频率(N秒/次)", 'width': 100},
        ]
        table_widget.setColumnCount(len(table_header))
        table_widget.setShowGrid(True)
        for idx, info in enumerate(table_header):
            item = QTableWidgetItem()
            item.setText(info['text'])
            table_widget.setHorizontalHeaderItem(idx, item)
            table_widget.setColumnWidth(idx, info['width'])
        table_layout.addWidget(table_widget)

        # 3.2 初始化表格数据
        # 读取数据文件
        file_path = os.path.join(BASE_DIR, "db", "db.json")
        with open(file_path, mode='r', encoding='utf-8') as f:
            data = f.read()
        data_list = json.loads(data)

        # 获取当前表格有多少行
        current_row_count = table_widget.rowCount()
        for row_list in data_list:
            table_widget.insertRow(current_row_count)
            for i, ele in enumerate(row_list):
                ele = STATUS_MAPPING[ele] if i == 6 else ele
                cell = QTableWidgetItem(str(ele))
                if i in [0,4,5,6]:
                    cell.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                table_widget.setItem(current_row_count, i, cell)
            
            

            current_row_count += 1

        return table_layout
    
    def init_footer(self):
        # 5 创建页脚布局
        foot_layout = QHBoxLayout()
        label_status = QLabel()
        label_status.setObjectName("label_status")
        label_status.setText(u"未检测")
        foot_layout.addWidget(label_status)

        foot_space_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        foot_layout.addItem(foot_space_item)

        btn_reinit = QPushButton()
        btn_reinit.setObjectName("btn_reinit")
        btn_reinit.setText(u"重新初始化")
        foot_layout.addWidget(btn_reinit)

        btn_recheck = QPushButton()
        btn_recheck.setObjectName("btn_recheck")
        foot_layout.addWidget(btn_recheck)
        btn_recheck.setText(u"重新检测")

        btn_reset_count = QPushButton()
        btn_reset_count.setObjectName("btn_reset_count")
        foot_layout.addWidget(btn_reset_count)
        btn_reset_count.setText(u"次数清零")

        btn_delete = QPushButton()
        btn_delete.setObjectName("btn_delete")
        foot_layout.addWidget(btn_delete)
        btn_delete.setText(u"删除检测项")

        btn_alert = QPushButton()
        btn_alert.setObjectName("btn_alert")
        foot_layout.addWidget(btn_alert)
        btn_alert.setText(u"SMTP报警配置")

        btn_proxy = QPushButton()
        btn_proxy.setObjectName("btn_proxy")
        foot_layout.addWidget(btn_proxy)
        btn_proxy.setText(u"设置代理")
        return foot_layout
    
# main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
