import PyChromeDevTools
import time
import pychrome

chrome = PyChromeDevTools.ChromeInterface()
chrome.Network.enable()
chrome.Page.enable()
chrome.Runtime.enable()
start_time=time.time()
# chrome = PyChromeDevTools.ChromeInterface(host="1.1.1.1",port=9222)
chrome.Page.navigate(url="https://github.com/marty90/PyChromeDevTools")
chrome.wait_event("Page.loadEventFired", timeout=60)
res = chrome.Runtime.evaluate(expression="document.querySelectorAll('.commits>a')[0].innerText")
print(chrome.tabs[0]['id'])
chrome.get_tabs()
print(chrome.tabs)
print(res)
end_time=time.time()

print ("Page Loading Time:", end_time-start_time)