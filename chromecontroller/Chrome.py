import pychrome
import os
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
# create a browser instance
browser = pychrome.Browser(url="http://127.0.0.1:9222")

# create a tab
def gettab():
    try:
        tab = browser.new_tab()
    except Exception as e:
        # os.popen(".\\Application\\chrome.exe --headless --disable-gpu --remote-debugging-port=9222")
        os.popen(".\\Application\\chrome.exe  --remote-debugging-port=9222")
        tab = browser.new_tab()
        pass
    return tab


# register callback if you want
def request_will_be_sent(**kwargs):
    print("loading: %s" % kwargs.get('request').get('url'))


def loading(code):

    tab = gettab()
    tab.start()
    tab.Network.enable()
    tab.Page.enable()
    tab.Runtime.enable()
    # tab.Page.navigate(url="https://github.com/fate0/pychrome", _timeout=5)
    tab.Page.navigate(url="http://quote.eastmoney.com/concept/sh{}.html#chart-k-cyq".format(code), _timeout=10)
    tab.wait(3)
    res = tab.Runtime.evaluate(expression="document.querySelectorAll('.__emchatrs3_cmfb>div')[1].innerText")
    while res and res["result"] and res["result"]["value"] =="":
        tab.wait(0.5)
        res = tab.Runtime.evaluate(expression="document.querySelectorAll('.__emchatrs3_cmfb>div')[1].innerText")
    print(res)
    # stop the tab (stop handle events and stop recv message from chrome)
    tab.stop()

    # close tab
    browser.close_tab(tab_id=tab.id)
    return res
if __name__ == '__main__':
    from multiprocessing import Pool,freeze_support
    pool = ProcessPoolExecutor(max_workers=3)
    # pool = ThreadPoolExecutor(max_workers=3)
    # freeze_support()
    # pool = Pool()
    codes = ["600063","601236","600860","601698","600888"]
    # for code in codes:
    pool.map(loading,codes)
    # result=pool.map(loading,codes)
    # result = pool.map(loading,codes)
    # print(result)


