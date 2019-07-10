import pychrome
import os
import base64
import time
import logging
import json
from heapq import nlargest,nsmallest
import asyncio


class ChromeDataGet():

    def __init__(self):
        # google-chrome --headless --disable-gpu --remote-debugging-port=9222
        # os.system("F:\\software\\Google\\Chrome\\Application\\chrome.exe --headless --disable-gpu --remote-debugging-port=9222")
        # cc = os.popen("F:\\software\\Google\\Chrome\\Application\\chrome.exe --headless --disable-gpu --remote-debugging-port=9222")

        # create a browser instance
        self.browser = pychrome.Browser(url="http://127.0.0.1:9222")
        self.loop = asyncio.get_event_loop()
        # self.loop.set_debug(True)
        asyncio.Semaphore(500)
        jqf = open("jquery-2.1.4.min.js", encoding='utf-8')
        self.jquery = ''.join(jqf.readlines())
        jqf.close()
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
        # print("get tab: "+tab.id)
        return tab

    def close_tab(self,tab):
        tab.stop()
        # print("close tab: "+tab.id)
        self.browser.close_tab(tab_id=tab.id, timeout=3)

    def worker(self):
        fs = open("test", encoding='utf-8')
        tasks = []
        for line in fs.readlines():
            line = line.split("\t")
            quote = 'sh' if line[1] == '1' else 'sz'
            url1 = self.url + quote + line[2] + ".html#chart-k-cyq"
            # temp = tab.Runtime.evaluate(expression = jquery)
            print(line)
            # await self.loading_data(url1, None, line[2])
            # task = asyncio.gather(self.loading_data(url1, None,line[2]),self.loop)
            # task = self.loop.create_task(self.loading_data(url1, None,line[2]))
            # task = loop.run_in_executor(None,self.loading_data(url1, None,line[2]))
            # val =await task
            tasks.append(self.loading_data(url1, None,line[2]))
            # await self.loading_data(url1, tab,line[2])
        return tasks
        # print(results)
        # self.print_data()

    def proxy(self):
        tasks = self.worker()
        self.loop.run_until_complete(asyncio.gather(*tasks))
        for tab in self.browser.list_tab():
            self.browser.close_tab(tab_id=tab.id)
        self.print_data()

    def print_data(self):
        while True:
            print(len(self.result))
            asyncio.sleep(1)
            if len(self.result) == 30:
                print(len(self.result))
                break
        nsmall = nsmallest(10, self.result, key=lambda s: s['value'])
        print(nsmall)

    async def screen_shot(self,tab):
        data = tab.Page.captureScreenshot()
        with open("%s.png" % time.time(), "wb") as fd:
            fd.write(base64.b64decode(data['data']))

    def tab_setting(self,tab):
        tab.start()
        # call method
        tab.Network.enable()
        tab.Runtime.enable()
        tab.DOM.enable()
        tab.DOM.getDocument()
        # tab.Network.requestWillBeSent = self.request_will_be_sent
        # tab.Network.responseReceived = self.responseReceived
        # tab.Network.loadingFinished = self.loadingFinished
        # start the tab

    async def loading_data(self,url,tab,code):
        # print("loading_data------------")
        tab = self.get_new_tab()
        tab.Page.navigate(url=url, _timeout=3)
        tab.Page.addScriptToEvaluateOnNewDocument(source=self.jquery)
        res = {}
        while True:
            await asyncio.sleep(0.1)
            if res.__contains__('result') and res['result'].get('value', "") != '':
                break
            res = tab.Runtime.evaluate(expression='$(".__emchatrs3_cmfb>div:eq(1)>span").text()', awaitPromise=True)
        print(res)
        # print(url)
        val = res['result']['value'].replace('%', "")
        self.result.append({'code': code, 'value': float(val)})
        self.close_tab(tab)
        return val

    def request_will_be_sent(self, **kwargs):
        print("loading: %s" % kwargs.get('request').get('url'))

    def responseReceived(self, **kwargs):
        print(kwargs)

    def loadingFinished(self, **kwargs):
        print(kwargs)

    def pychrome_send_click(self, tab, x, y, button='left'):
        """https://github.com/cyrus-and/chrome-remote-interface/wiki/Trigger-synthetic-click-events"""
        assert isinstance(tab, pychrome.Tab)
        assert isinstance(x, int) and isinstance(y, int)
        # info = tab.Input.dispatchMouseEvent(type='mouseMoved', x=x, y=y, button='left', clickCount=1, modifiers=0)
        info = tab.Input.dispatchMouseEvent(type='mousePressed', x=x, y=y, button=button, clickCount=1, modifiers=0)
        info = tab.Input.dispatchMouseEvent(type='mouseReleased', x=x, y=y, button=button, clickCount=1, modifiers=0)
        return info


    def pychrome_send_keys(self, tab, char):
        assert isinstance(tab, pychrome.Tab)
        # assert isinstance(char, basestring) and len(char) == 1
        info = tab.Input.dispatchKeyEvent(type='rawKeyDown', windowsVirtualKeyCode=ord(char), unmodifiedText=char, text=char)
        info = tab.Input.dispatchKeyEvent(type='char', windowsVirtualKeyCode=ord(char), unmodifiedText=char, text=char)
        info = tab.Input.dispatchKeyEvent(type='keyUp', windowsVirtualKeyCode=ord(char), unmodifiedText=char, text=char)
        return info


    def pychrome_call_element_js(self, tab, query, js):
        assert isinstance(tab, pychrome.Tab)
        # assert isinstance(query, basestring) and isinstance(js, basestring)
        tab.DOM.enable()
        tab.DOM.getDocument()
        info = tab.DOM.performSearch(query=query, includeUserAgentShadowDOM=True)
        logging.info('pychrome_call: %r DOM.performSearch(%r) return %s', tab, query, info)
        info = tab.DOM.getSearchResults(searchId=info['searchId'], fromIndex=0, toIndex=info['resultCount'])
        info = tab.DOM.resolveNode(nodeId=info['nodeIds'][0])
        info = tab.Runtime.callFunctionOn(objectId=info['object']['objectId'], functionDeclaration=js)
        logging.info('pychrome_call: %r callFunctionOn(%r) return %s', tab, js[:128], info)
        return info


    def pychrome_wait_element_appeared(self, tab, query, timeout, predicate=None):
        assert isinstance(tab, pychrome.Tab)
        # assert isinstance(query, basestring) and isinstance(timeout, (int, float))
        while timeout > 0:
            try:
                if query.startswith('document.'):
                    info = tab.Runtime.evaluate(expression=query)
                    logging.info('pychrome_wait_element_appeared: tab.Runtime.evaluate(%s) return: %s', query, info)
                    if callable(predicate) and not predicate(info['result']):
                        continue
                else:
                    info = self.pychrome_call_element_js(tab, query, self.js_element_getter('outerHTML'))
                    if callable(predicate) and not predicate(info['result']):
                        continue
                return True
            except (KeyError, pychrome.CallMethodException) as e:
                logging.info('pychrome_wait_element_appeared(%r, %r) error: %s(%s)', tab, query, type(e), e)
            finally:
                time.sleep(1.0)
                timeout -= 1.0
        return False


    def pychrome_get_document_value(self, tab, expression):
        assert isinstance(tab, pychrome.Tab)
        # assert isinstance(expression, basestring)
        tab.DOM.enable()
        tab.DOM.getDocument()
        info = tab.Runtime.evaluate(expression=expression)
        logging.info('pychrome_get_elements_html: %r tab.Runtime.evaluate(%r) return %s', tab, expression, info)
        value = info['result']['value']
        if expression.startswith('JSON.stringify('):
            value = json.loads(value)
        return value

    def js_element_caller(self, call):
        return '(function() { this.%s() })' % call

    def js_element_getter(self, name):
        return '(function() { return this.%s })' % name

    def js_element_setter(self, name, value):
        return '(function() { this.%s= "%s" })' % (name, value)

    def js_element_position(self):
        return '(function() {x=this.offsetLeft;y=this.offsetTop;i=this.offsetParent;while(i!==null){x+=i.offsetLeft;y+=i.offsetTop;i=i.offsetParent;}return x+" "+y;})'

    def js_document_get_htmls(self, cssselector):
        return 'JSON.stringify(Array.prototype.slice.call(document.querySelectorAll("%s")).map(function(e){return e.outerHTML}))' % cssselector

    def js_document_get_html(self, cssselector):
        return 'document.querySelector("%s").outerHTML' % cssselector

    def js_document_get_tagattr(self, tag, attr):
        return 'document.getElementsByTagName("%s")[0].attributes["%s"].value' % (tag, attr)

    def js_document_get_text(self,element_id):
        return 'document.getElementById("%s").innerText' % element_id

if __name__ == '__main__':
    chrome = ChromeDataGet()
    # loop = asyncio.get_event_loop()
    # loop.set_debug(True)
    # task = loop.create_task(chrome.proxy())
    # loop.run_until_complete(chrome.worker())
    from datetime import datetime
    print(datetime.now())
    chrome.proxy()
    print(datetime.now())
    # chrome.print_data()