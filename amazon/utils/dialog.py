import os
import json

from PyQt6.QtCore import Qt
# send email dialog
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QLineEdit, \
    QTextEdit


class AlertDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filed_dict = {}
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("报警邮件SMTP配置")
        self.resize(300, 270)

        layout = QVBoxLayout()

        form_data_list = [
            {"title": "SMTP服务器", "filed": "smtp"},
            {"title": "发件箱", "filed": "from"},
            {"title": "密码", "filed": "pwd"},
            {"title": "收件人（多个用逗号分割）", "filed": "to"},
        ]

        # 读取文件中的配置
        old_data_dict = {}
        # 1. 判断文件是否存在
        alert_file_path = os.path.join("db", "alert.json")
        if os.path.exists(alert_file_path):
            with open(alert_file_path, "r") as f:
                old_data_dict = json.load(f)

        # 初始化对话框界面
        for item in form_data_list:
            lbl = QLabel()
            lbl.setText(item['title'])
            layout.addWidget(lbl)

            txt = QLineEdit()
            layout.addWidget(txt)
            filed = item['filed']
            if old_data_dict and filed in old_data_dict:
                txt.setText(old_data_dict[filed])
            self.filed_dict[item['filed']] = txt

        btn_save = QPushButton()
        btn_save.setText("保存")
        btn_save.clicked.connect(self.event_save_click)
        layout.addWidget(btn_save, 0, Qt.AlignmentFlag.AlignRight)
        layout.addStretch(1)
        self.setLayout(layout)

    def event_save_click(self):
        data_dict = {}
        for key, field in self.field_dict.items():
            value = field.text().strip()
            if not value:
                QMessageBox.warning(self, "错误", "邮件报警项不能为空")
                return
            data_dict[key] = value
        #  save to config.json in db directory

        file_object = open(os.path.join("db", 'alert.json'), mode='w', encoding='utf-8')
        json.dump(data_dict, file_object)
        file_object.close()
        self.close()

class ProxyDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("代理配置")
        self.resize(500, 400)

        layout = QVBoxLayout()
        # 输入框
        text_edit = QTextEdit()
        layout.addWidget(text_edit)
        text_edit.setPlaceholderText("可用换行来设置多个代理IP，每个代理IP设置格式为：xx.xx.xx.xx:1234")
        file_path = os.path.join("db", "proxy.txt")
        all_proxy = ""
        if os.path.exists(file_path):
            with open(os.path.join("db", "proxy.txt"), "r", encoding="utf-8") as f:
                all_proxy = f.read()
        text_edit.setText(all_proxy)
        self.text_edit = text_edit

        footer_config = QHBoxLayout()
        btn_save = QPushButton()
        btn_save.setText("重置")
        btn_save.clicked.connect(self.event_save_click)
        footer_config.addWidget(btn_save, 0, Qt.AlignmentFlag.AlignRight)
        layout.addLayout(footer_config)
        self.setLayout(layout)

    def event_save_click(self):
        text = self.text_edit.toPlainText()
        # 写入到代理文件中、
        file_object = open(os.path.join("db", 'proxy.txt'), mode='w', encoding='utf-8')
        file_object.write(text)
        file_object.close()
        self.close()

class LogDialog(QDialog):
    def __init__(self, asin, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.asin = asin
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("查看日志")
        self.resize(500, 400)

        layout = QVBoxLayout()
        text_edit = QTextEdit()
        layout.addWidget(text_edit)
        text_edit.setText("")

        self.setLayout(layout)

        # 读取日志展示出来
        file_path = os.path.join("log", "{}.log".format(self.asin))
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                text_edit.setText(f.read())