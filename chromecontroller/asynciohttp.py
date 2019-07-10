import pychrome
import os
import base64
import time
import logging
import json
from heapq import nlargest,nsmallest
import asyncio
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor


class ChromeDataGet:

    def __init__(self):
        # google-chrome --headless --disable-gpu --remote-debugging-port=9222
        # os.system("F:\\software\\Google\\Chrome\\Application\\chrome.exe --headless --disable-gpu --remote-debugging-port=9222")
        # cc = os.popen("F:\\software\\Google\\Chrome\\Application\\chrome.exe --headless --disable-gpu --remote-debugging-port=9222")

        # create a browser instance
        self.browser = pychrome.Browser(url="http://127.0.0.1:9222")
        self.url = "http://quote.eastmoney.com/concept/"
        self.result = []

    def get_new_tab(self):
        try:
            tab = self.browser.new_tab()
        except Exception as e:
            cc = os.popen(
                "F:\\software\\Google\\Chrome\\Application\\chrome.exe --headless  --remote-debugging-port=9222")
            tab = self.browser.new_tab()
        self.tab_setting(tab=tab)
        return tab

    def close_tab(self,tab):
        tab.stop()
        # print("close tab: "+tab.id)
        self.browser.close_tab(tab_id=tab.id, timeout=5)
    def close_alltab(self):
        for tab in self.browser.list_tab():
            self.browser.close_tab(tab_id=tab.id)
    def worker(self):
        fs = open("test", encoding='utf-8')
        # tasks = []
        # pool = ThreadPoolExecutor()
        pool = ProcessPoolExecutor()
        # results = pool.map(self.loading_data, fs.readlines())
        for data in pool.map(self.loading_data,fs.readlines()):
            print(data)

        print("finished")
        # print(results)
        # return results

    def proxy(self):
        tasks = self.worker()
        self.print_data()

    def print_data(self):
        nsmall = nsmallest(10, self.result, key=lambda s: s['value'])
        print(nsmall)

    def screen_shot(self,tab):
        data = tab.Page.captureScreenshot()
        with open("%s.png" % time.time(), "wb") as fd:
            fd.write(base64.b64decode(data['data']))

    def tab_setting(self,tab):
        tab.start()
        tab.Network.enable()
        tab.Runtime.enable()
        # tab.DOM.enable()
        # tab.DOM.getDocument()
        # tab.Network.requestWillBeSent = self.request_will_be_sent
        # tab.Network.responseReceived = self.responseReceived
        # tab.Network.loadingFinished = self.loadingFinished
        # start the tab

    def loading_data(self,line):
        # print("loading_data------------")
        line = line.split("\t")
        quote = 'sh' if line[1] == '1' else 'sz'
        url = self.url + quote + line[2] + ".html#chart-k-cyq"
        code = line[2]
        tab = self.get_new_tab()
        print(code+" naving")
        tab.Page.navigate(url=url, _timeout=6)
        print(code+" nav end")
        res = {}
        tab.wait(6)
        print(code+" wait end")
        # tab.wait(5)
        res = tab.Runtime.evaluate(expression='document.querySelectorAll(".__emchatrs3_cmfb>div")[1].innerText', awaitPromise=True)
        print(res)
        # print(url)
        try:
            val = res['result']['value'].replace('%', "").replace("获取比例:","").replace("：","")
        except Exception as e:
            print(e)
            val =-1.0

        self.result.append({'code': code, 'value': float(val)})
        self.close_tab(tab)
        return True


if __name__ == '__main__':
    chrome = ChromeDataGet()
    from datetime import datetime
    print(datetime.now())
    chrome.proxy()
    # chrome.close_alltab()
    print(datetime.now())