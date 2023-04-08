import re
import os
import time
from lxml import etree
import requests
from urllib.parse import quote
from threading import Thread
from PySide2.QtWidgets import QApplication, QLineEdit, QPlainTextEdit
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Signal, QObject
from PySide2.QtGui import QIcon

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
}


# 自定义信号源对象类型，一定要继承自 QObject
class MySignals(QObject):
    # 定义一种信号，一个参数 类型是：字符串
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    update_line_info = Signal(QLineEdit, str)
    update_content_info = Signal(QPlainTextEdit, str)


# 实例化
global_ms = MySignals()


class GetNovel:
    def __init__(self):
        # 动态导入UI文件
        self.ui = QUiLoader().load('ui/Novel_Download.ui')
        # 点击事件
        self.ui.downbutton.clicked.connect(self.handleCalc)
        # 自定义信号的处理函数
        global_ms.update_line_info.connect(self.update_line)
        global_ms.update_content_info.connect(self.update_content)

    def update_line(self, line, text):
        line.setText(text)

    def update_content(self, content, text):
        content.appendPlainText(text)

    def get_url_1(self, title):
        title_truth = quote(title)
        url = "https://www.aixdzs.com/novel/" + title_truth
        resp = requests.get(url=url, headers=header)
        if resp.status_code != 200:
            return None
        else:
            return url

    def get_novel_1(self, url, title):
        time.sleep(3)
        urlBase = "https://www.aixdzs.com"  # 主url
        obj_contentBase = re.compile(r'目录(?P<contentBase>.*?)关于我们', re.S)
        obj_url = re.compile(r'<li class="chapter"><a href="(?P<url>.*?)" title="字数:.*?">(?P<title>.*?)</a></li>', re.S)
        obj_content = re.compile(r'<div class="content">(?P<content>.*?)</div>', re.S)
        resultUrl = obj_contentBase.findall(requests.get(url=url, headers=header).text)
        resultUrl = resultUrl[0]
        result_url = obj_url.finditer(resultUrl)
        with open(f'{title}.txt', "a+", encoding='utf-8') as f:
            for i in result_url:
                urlContent = urlBase + i.group('url')
                resultContent = obj_content.findall(requests.get(url=urlContent, headers=header).text)[0]
                content = i.group('title') + '\n' + resultContent.replace("<p>", "　　").replace("</p>", "\n")
                f.write(content)
                global_ms.update_content_info.emit(self.ui.content, i.group('title') + "完成！")
                print(i.group('title') + "完成！")
                time.sleep(3)
        global_ms.update_content_info.emit(self.ui.content, "Over!")

    def get_url_2(self, title):
        title_true = title
        title = quote(title)
        url = f'https://www.xbiquge.la/modules/article/waps.php?searchkey={title}'
        obj4 = re.compile(rf'<td class="even"><a href="(?P<url>.*?)" target="_blank">{title_true}</a></td>', re.S)
        resp = requests.get(url=url, headers=header)
        result = obj4.finditer(resp.text.encode('iso-8859-1').decode('utf-8'))
        for i in result:
            if i is not None:
                url = i.group("url")
                return url
            else:
                return None

    def get_novel_2(self, url, title):
        resp1 = requests.get(url=url, headers=header)
        url1 = 'https://www.xbiquge.la'  # 原始url
        obj_5 = re.compile(r"<dd><a href='(?P<url>.*?)' >(?P<title>.*?)</a></dd>", re.S)
        result1 = obj_5.finditer(resp1.text.encode('iso-8859-1').decode('utf-8'))
        with open(f'{title}.txt', "a+", encoding='utf-8') as f:
            for i in result1:
                url2 = url1 + i.group('url')  # 拼接分url
                resp2 = requests.get(url=url2, headers=header)
                resp_html = etree.HTML(resp2.text.encode('iso-8859-1').decode('utf-8'))
                result0 = resp_html.xpath('//*[@id="content"]/text()')
                result = str(result0)
                content = i.group('title') + "\n" + result.replace("[", '').replace(']', '').replace(',', '').replace(
                    '\xa0\xa0\xa0\xa0', '').replace("'", "").replace(r"\xa0\xa0\xa0\xa0", "　　").replace(r"\r \r ",
                                                                                                        "\n") + "\n"
                f.write(content)
                global_ms.update_content_info.emit(self.ui.content, i.group('title') + "完成！")
                time.sleep(3)
        global_ms.update_content_info.emit(self.ui.content, "Over!")

    def get_url_3(self, title):
        title_truth = title
        title = quote(title)
        url = f'https://www.bige3.com/s?q={title}'
        resp = requests.get(url=url, headers=header, verify=False)
        obj3 = re.compile(
            r'</a></div><div class="bookinfo"><h4 class="bookname"><a href="(?P<url>.*?)">(?P<title>.*?)</a>',
            re.S)
        result = obj3.finditer(resp.text)
        for i in result:
            if i is not None and i.group("title") == title_truth:
                url = f'https://www.bige3.com{i.group("url")}'
                return url
            else:
                return None

    def get_novel_3(self, url, title):
        url1 = url  # 主url
        url0 = url1.split('/book')[0]  # 拼接url作准备
        resp1 = requests.get(url=url1, headers=header, verify=False)  # 获取主页内容(为拼接分url准备)
        # print(resp1.content.decode('utf-8'))  # 查看内容是否正确
        obj1 = re.compile(r'<dd><a href ="(?P<url>.*?)">', re.S)
        obj2 = re.compile(
            r'<h1 class="wap_none">(?P<title>.*?)</h1>.*?class="Readarea ReadAjax_content">(?P<content>.*?)'
            r'<p class="readinline">',
            re.S)
        result1 = obj1.finditer(resp1.text)  # 第一次匹配
        f = open(f'{title}.txt', 'a+', encoding='utf-8')  # 打开文件
        for i in result1:
            url2 = url0 + i.group('url')  # 拼接分url
            resp2 = requests.get(url=url2, headers=header)  # 获取分url内容
            result2 = obj2.finditer(resp2.text)  # 第二次匹配
            for ii in result2:
                content = ii.group('title') + '\n' + ii.group('content').replace('<br /><br />', '\n')  # 内容查询与凭借
                f.write(content)  # 写入内容
                global_ms.update_content_info.emit(self.ui.content, i.group('title') + "完成！")  # 打印写入信息
            time.sleep(3)
        f.close()  # 关闭文件
        global_ms.update_content_info.emit(self.ui.content, "Over!")

    def handleCalc(self):
        def threadFunc():
            title = self.ui.name.text()
            downroad = self.ui.downroad.currentText()
            print(downroad)
            print(downroad == "使用路径二下载")
            print((url1 := self.get_url_1(title)) is not None)
            if downroad == "使用路径一下载" and (url1 := self.get_url_1(title)) is not None:  # url = "https://www.aixdzs.com/"
                print("使用路径一下载！")
                global_ms.update_line_info.emit(self.ui.savepath, str(os.getcwd()) + f'\{title}.txt')
                print(str(os.getcwd()) + f'\{title}.txt')
                self.get_novel_1(url1, title)
            elif downroad == "使用路径二下载" and (url2 := self.get_url_2(title)) is not None:  # url = "https://www.xbiquge.la/"
                print("使用路径二下载！")
                global_ms.update_line_info.emit(self.ui.savepath, str(os.getcwd()) + f'\{title}.txt')
                print(str(os.getcwd()) + f'\{title}.txt')
                self.get_novel_2(url2, title)
            elif downroad == "使用路径三下载" and (url3 := self.get_url_3(title)) is not None:  # url = "http://www.bige3.com/"
                print("使用路径三下载！")
                global_ms.update_line_info.emit(self.ui.savepath, str(os.getcwd()) + f'\{title}.txt')
                print(str(os.getcwd()) + f'\{title}.txt')
                self.get_novel_3(url3, title)
            else:
                global_ms.update_content_info.emit(self.ui.content, "未找到相关内容，请选择其他路径或重新输入！")

        thread = Thread(target=threadFunc)
        thread.start()


if __name__ == '__main__':
    app = QApplication([])
    # 加载 icon
    app.setWindowIcon(QIcon('./Icon/DrizzleDrop.jpg'))
    getNovel = GetNovel()
    getNovel.ui.show()
    app.exec_()
