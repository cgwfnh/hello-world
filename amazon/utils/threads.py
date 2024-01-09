import time

import bs4
import lxml
import requests
from PyQt6.QtCore import QThread, pyqtSignal

HOST = "https://www.amazon.com/"
HOST_ASIN_TPL = "{}{}".format(HOST, "gp/product/")
HOST_TASK_LIST_TPL = "{}{}".format(HOST, "gp/offer-listing")

# FILTERS = quote('{"all": true, "new":true}')
# TPL = "https://www.amazon.com/gp/aod/ajax/ref=aod_f_new?qty=1&asin={}&pc=dp&pageno=1&filters={}"
class NewTaskThread(QThread):
    # 触发信号，
    success_signal = pyqtSignal(int, str, str, str)
    error_signal = pyqtSignal(int, str, str, str)

    def __init__(self, row_index, asin, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row_index = row_index
        self.asin = asin

    def run(self):
        '''
        具体要做的
        :return:
        '''
        try:
            # url = "{}{}/".format(HOST_ASIN_TPL, self.asin)
            url = "https://www.amazon.com/gp/product/{}/".format(self.asin)
            print(url)
            proxies = {
                'http': 'http://127.0.0.1:7890',
                'https': 'http://127.0.0.1:7890',
            }
            res = requests.get(
                url = url,
                headers= {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "pragma": "no-cache",
                    "upgrade-insecure-requests": "1",
                    "cache-control": "no-cache",
                    "accept-language": "zh-CN, zh; q= 0.9",
                    "accept-encoding": "gzip, deflate, br",
                    "accept": "*/*"
                },
                proxies = proxies
            )
            if res.status_code != 200:
                raise Exception("初始化失败")

            soup = bs4.BeautifulSoup(res.text, lxml)
            title = soup.find(id="productTitle").text.strip()
            tpl = "https://www.amazon.com/gp/product/ajax/ref=dp_aod_ALL_mbc?asin={}&m=&qid=&smid=&lsourcecustomerorglistid=&sourcecustomerorglistitemed=&sr=&pc=dp&experienceId=aodAjaxMain"
            # url = "{}/{}/ref=dp_olp_all_mbc?ie=UTF8&condition=new".format(HOST_TASK_LIST_TPL, self.asin)
            url = tpl.format(self.asin)

            # 获取到title和url， 将这个信息填写到表格上 & 写入文件中。
            self.success_signal.emit(self.row_index, self.asin, title, url)
        except Exception as e:
            print(e)
            title = "监控项 {} 添加失败".format(self.asin)
            self.error_signal.emit(self.row_index, self.asin, title, str(e))


class TaskThread(QThread):
    start_signal = pyqtSignal(int)
    stop_signal = pyqtSignal(int)
    counter_signal = pyqtSignal(int)
    error_counter_signal = pyqtSignal(int)

    def __init__(self, scheduler, log_file_path, row_index, asin, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scheduler = scheduler
        self.log_file_path = log_file_path
        self.row_index = row_index
        self.asin = asin

    def run(self):
        # 触发信号
        self.start_signal.emit(self.row_index)

        import time
        import random
        while True:
            # 停止信号
            if self.scheduler.terminate:
                self.stop_signal.emit(self.row_index)
                # 自己的线程在thread_list中移除自己
                self.scheduler.destory_thread(self)
                return
            try:
                # 触发信号
                time.sleep(random.randint(1, 3))
                self.counter_signal.emit(self.row_index)

                # 写日志
                with open(self.log_file_path, "a", encoding="utf-8") as f:
                    f.write("日志\n")

                # 监控动作
                # 根据ASIN，去访问每一个连接，通过bs4获取数据，
                # 获取到数据，价格是否小于预期
                # 发送报警（邮件）
            except Exception as e:
                self.error_counter_signal.emit(self.row_index)



# 停止线程
class StopThread(QThread):
    updated_signal = pyqtSignal(str)

    def __init__(self, scheduler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scheduler = scheduler

    def run(self):
        # 1. 监控线程总的数量
        # total_count = len(self.scheduler.thread_list)
        while True:
            running_count = len(self.scheduler.thread_list)
            self.updated_signal.emit("正在终止({})".format(running_count))
            # 更新至窗体中
            if running_count == 0:
                break
            time.sleep(1)
        self.updated_signal.emit("已终止")
