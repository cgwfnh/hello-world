# generate pyqt6 window

import json
import sys, os
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QTableWidgetItem, QPushButton, QSpacerItem, \
    QLineEdit, QTableWidget, QLabel, QMessageBox, QMenu
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

# 状态管理
RUNNING = 1
STOPPING = 2
STOP = 3

# main window class
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.switch = STOP
        self.setWindowTitle("My App")
        self.resize(1228, 450)

        # 表单输入控件，收集ASIN
        self.txt_asin = None

        # 表格对象
        self.table_widget = None

        self.label_status = None

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
        btn_start.clicked.connect(self.event_start_click)
        btn_stop = QPushButton("停止")
        btn_stop.clicked.connect(self.event_stop_click)
        header_layout.addWidget(btn_start)
        header_layout.addWidget(btn_stop)
        header_space_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        header_layout.addItem(header_space_item)

        return header_layout
    

    def init_form(self):
        # 3 创建表单布局
        form_layout = QHBoxLayout()
        txt_asin = QLineEdit()
        txt_asin.setText("B07YN82X3B=29")
        txt_asin.setPlaceholderText("请输入商品ID和价格，例如：B0818JJJQQ8=88")
        self.txt_asin = txt_asin
        form_layout.addWidget(txt_asin)
        btn_add = QPushButton("添加")
        btn_add.clicked.connect(self.event_add_click)
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
        self.table_widget = table_widget

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

        # 开启右键设置
        table_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        table_widget.customContextMenuRequested.connect(self.table_right_menu)
        return table_layout

    # 表格开启右键菜单设置。
    def table_right_menu(self, pos):
        # 只有选中一行时，才支持右键
        selected_item_list = self.table_widget.selectedItems()
        if len(selected_item_list) != 1:
            return

        menu = QMenu()
        item_copy = menu.addAction("复制")
        item_view_log = menu.addAction("查看日志")
        item_clear_log = menu.addAction("清除日志")
        # 选中了哪个
        action = menu.exec(self.table_widget.mapToGlobal(pos))
        if action == item_copy:
            # 复制当前ASIN
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_item_list[0].text())
        elif action == item_view_log:
            # 查看日志，在对话框中显示 日志信息。
            from utils.dialog import LogDialog
            dialog = LogDialog(selected_item_list[0].text())
            dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
            dialog.exec()
        elif action == item_clear_log:
            # 清除日志
            file_path = os.path.join(BASE_DIR, "log", selected_item_list[0].text() + ".log")
            if os.path.exists(file_path):
                os.remove(file_path)
    def init_footer(self):
        # 5 创建页脚布局
        foot_layout = QHBoxLayout()
        self.label_status = label_status = QLabel()
        label_status.setObjectName("label_status")
        label_status.setText(u"未检测")
        foot_layout.addWidget(label_status)

        foot_space_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        foot_layout.addItem(foot_space_item)

        btn_reinit = QPushButton()
        btn_reinit.setObjectName("btn_reinit")
        btn_reinit.setText(u"重新初始化")
        btn_reinit.clicked.connect(self.event_reinit_click)
        foot_layout.addWidget(btn_reinit)

        btn_recheck = QPushButton()
        btn_recheck.setObjectName("btn_recheck")
        foot_layout.addWidget(btn_recheck)
        btn_recheck.setText(u"重新检测")

        btn_reset_count = QPushButton()
        btn_reset_count.setObjectName("btn_reset_count")
        foot_layout.addWidget(btn_reset_count)
        btn_reset_count.clicked.connect(self.event_reset_count_click)
        btn_reset_count.setText(u"次数清零")

        btn_delete = QPushButton()
        btn_delete.setObjectName("btn_delete")
        btn_delete.clicked.connect(self.event_delete_click)
        foot_layout.addWidget(btn_delete)
        btn_delete.setText(u"删除检测项")

        btn_alert = QPushButton()
        btn_alert.setObjectName("btn_alert")
        btn_alert.clicked.connect(self.event_alert_click)
        foot_layout.addWidget(btn_alert)
        btn_alert.setText(u"SMTP报警配置")

        btn_proxy = QPushButton()
        btn_proxy.setObjectName("btn_proxy")
        foot_layout.addWidget(btn_proxy)
        btn_proxy.clicked.connect(self.event_proxy_click)
        btn_proxy.setText(u"设置代理")
        return foot_layout
    
    # 点击添加按钮的函数处理
    def event_add_click(self):
        # 1. 获取输入框中的内容
        # text = self.txt_asin.text().strip()

        text = self.txt_asin.text()
        if not text:
            QMessageBox.warning(self, "错误", "商品的ASIN输入错误")
            return
        asin, price = text.split("=")
        price = float(price)
        # 2. 添加到表格中
        new_row_list = [asin, "", "", price, 0, 0, 0, 5]
        current_row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(current_row_count)
        for i, ele in enumerate(new_row_list):
            ele = STATUS_MAPPING[ele] if i == 6 else ele
            cell = QTableWidgetItem(str(ele))
            if i in [0, 4, 5, 6]:
                cell.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            self.table_widget.setItem(current_row_count, i, cell)
        # 3. 发送请求获取数据
        # 注意：不能在主线程中进行爬虫的事情，创建一个线程去做爬虫，获取 数据后，再更新到窗体中（信号）
        from utils.threads import NewTaskThread
        thread = NewTaskThread(current_row_count, asin)
        thread.success_signal.connect(self.init_task_success_callback)
        thread.error_signal.connect(self.init_task_error_callback)
        thread.start()

    # 点击重新初始化
    def event_reinit_click(self):
        # 1. 获取已选中的行，
        row_list = self.table_widget.selectionModel().selectedRows()
        if not row_list:
            QMessageBox.warning(self, "错误", "请选择要重新初始化的行")
            return
        # 2. 获取每一行进行重新初始化
        for row_object in row_list:
            row_index = row_object.row()
            print("选中的行", row_index)
            # 获取ASIN
            asin = self.table_widget.item(row_index, 0).text()

            # 更新状态列
            cell_status = QTableWidgetItem(STATUS_MAPPING[0])
            cell_status.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            self.table_widget.setItem(row_index, 6, cell_status)

            # 创建线程去进行初始化动作
            from utils.threads import NewTaskThread
            thread = NewTaskThread(row_index, asin)
            thread.success_signal.connect(self.init_task_success_callback)
            thread.error_signal.connect(self.init_task_error_callback)
            thread.start()

    # 点击数量清零
    def event_reset_count_click(self):
        row_list = self.table_widget.selectionModel().selectedRows()

        if not row_list:
            QMessageBox.warning(self, "错误", "请选择要清除次数的行")
            return

        for row_object in row_list:
            row_index = row_object.row()
            cell_status = QTableWidgetItem(str(0))
            cell_status.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            self.table_widget.setItem(row_index, 4, cell_status)
            # self.table_widget.setItem(row_index, 5, cell_status)  # 注意虽然从代码来看，是想一起设置4、5两列的数据，但代码执行情况来看，需要设置下述代码才可以更改第5列。
            cell_status = QTableWidgetItem(str(0))
            cell_status.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            self.table_widget.setItem(row_index, 5, cell_status)

    # 删除按钮的功能实现
    def event_delete_click(self):
        # 1. 获取已选中的行
        row_list = self.table_widget.selectionModel().selectedRows()

        if not row_list:
            QMessageBox.warning(self, "错误", "请选择要操作的行")
            return
        # 2. 倒序删除选择的行。
        # 翻转一下行的顺序
        row_list.reverse()
        for row_object in row_list:
            index = row_object.row()
            self.table_widget.removeRow(index)

    # 发送SMTP邮件的功能。
    def event_alert_click(self):
        # 创建一个弹窗，并在弹窗中进行设置
        from utils.dialog import AlertDialog
        dialog = AlertDialog()
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.exec()

    # 点击代理设置
    def event_proxy_click(self):
        from utils.dialog import ProxyDialog
        dialog = ProxyDialog()
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.exec()


    # 初始化任务成功回调函数
    def init_task_success_callback(self, row_index, asin, title, url):
        # 更新窗体显示的数据
        # 更新标题列
        cell_title = QTableWidgetItem(title)
        self.table_widget.setItem(row_index, 1, cell_title)

        # 更新URL
        cell_url = QTableWidgetItem(url)
        self.table_widget.setItem(row_index, 2, cell_url)

        # 更新状态列
        cell_status = QTableWidgetItem(STATUS_MAPPING[1])
        cell_status.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        self.table_widget.setItem(row_index, 6, cell_status)

        # 输入框清空
        self.txt_asin.clear()

    def init_task_error_callback(self, row_index, asin, title, url):
        # 更新标题列
        cell_title = QTableWidgetItem(title)
        self.table_widget.setItem(row_index, 1, cell_title)

        # 更新URL
        cell_url = QTableWidgetItem(url)
        self.table_widget.setItem(row_index, 2, cell_url)

        # 更新状态列
        cell_status = QTableWidgetItem(STATUS_MAPPING[11])
        cell_status.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        self.table_widget.setItem(row_index, 6, cell_status)

    # 点击开始
    def event_start_click(self):
        # 状态管理
        if self.switch != STOP:
            QMessageBox.warning(self, "错误", "正在执行获取终止中，请勿执行操作")
        self.switch = RUNNING
        # 1. 为每一行开启一个线程去执行，并记录下来
        from utils.scheduler import SCHEDULER
        SCHEDULER.start(BASE_DIR, self, self.task_start_callback, self.task_stop_callback, self.task_counter_callback, self.task_error_counter_callback)
        # 2. 执行中
        # 检测状态修改为执行中
        self.update_status_message("执行中")

    # 点击停止
    def event_stop_click(self):
        # 状态管理
        if self.switch != RUNNING:
            QMessageBox.warning(self, "错误", "已停止或者正在停止，请勿执行操作")
            return
        self.switch = STOPPING
        # 1. 执行中的线程要逐一终止
        from utils.scheduler import SCHEDULER
        SCHEDULER.stop()
        # 2. 终止后更新状态

    # 点击开始按键后，生成的线程执行的回调函数
    def task_start_callback(self, row_index):
        # 对表格中的数据状态进行更新
        cell_status = QTableWidgetItem(STATUS_MAPPING[2])
        cell_status.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        self.table_widget.setItem(row_index, 6, cell_status)

    # 执行次数的更新。
    def task_counter_callback(self, row_index):
        # 原有个数 + 1
        old_count = self.table_widget.item(row_index, 4).text().strip()
        new_count = int(old_count) + 1
        cell_status = QTableWidgetItem(str(new_count))
        cell_status.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        self.table_widget.setItem(row_index, 4, cell_status)

    # 错误记数
    def task_error_counter_callback(self, row_index):
        # 原有个数 + 1
        old_count = self.table_widget.item(row_index, 5).text().strip()
        new_count = int(old_count) + 1
        cell_status = QTableWidgetItem(str(new_count))
        cell_status.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        self.table_widget.setItem(row_index, 5, cell_status)

    # 停止按钮的信号
    def task_stop_callback(self, row_index):
        cell_status = QTableWidgetItem(STATUS_MAPPING[1])
        cell_status.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        self.table_widget.setItem(row_index, 6, cell_status)

    # 更新状态栏中标签的状态
    def update_status_message(self,message):
        if message == "已终止":
            self.switch = STOP
        self.label_status.setText(message)
        self.label_status.repaint()


# main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
