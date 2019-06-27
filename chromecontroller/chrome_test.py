import pychrome
import os
import base64
import time
import logging
import json
from heapq import nlargest,nsmallest

def screen_shot():
    data = tab.Page.captureScreenshot()
    with open("%s.png" % time.time(), "wb") as fd:
        fd.write(base64.b64decode(data['data']))

#google-chrome --headless --disable-gpu --remote-debugging-port=9222
# os.system("F:\\software\\Google\\Chrome\\Application\\chrome.exe --headless --disable-gpu --remote-debugging-port=9222")
cc = os.popen("F:\\software\\Google\\Chrome\\Application\\chrome.exe --headless --disable-gpu --remote-debugging-port=9222")

# create a browser instance
browser = pychrome.Browser(url="http://127.0.0.1:9222")
tab = browser.new_tab()
tab.start()
# call method
tab.Network.enable()
tab.Runtime.enable()
tab.DOM.enable()
tab.DOM.getDocument()
# register callback if you want
def request_will_be_sent(**kwargs):
    print("loading: %s" % kwargs.get('request').get('url'))

def responseReceived(**kwargs):
    print(kwargs)
def loadingFinished(**kwargs):
    res = tab.Runtime.evaluate(expression='$(".__emchatrs3_cmfb>div:eq(1)>span").text()',awaitPromise = True)
    print(res)
# tab.Network.requestWillBeSent = request_will_be_sent
# tab.Network.responseReceived = responseReceived
# tab.Network.loadingFinished = loadingFinished
# start the tab

url = "http://quote.eastmoney.com/concept/"
jqf = open("jquery-2.1.4.min.js",encoding='utf-8')
jquery  = ''.join(jqf.readlines())
jqf.close()
result=[]
fs = open("test",encoding='utf-8')
for line in fs.readlines():
    line = line.split("\t")
    print(line)
    quote = 'sh' if line[1] == '1' else 'sz'
    url1 = url+quote+line[2]+".html#chart-k-cyq"
    tab.Page.navigate(url=url1, _timeout=5)
    # tab.wait(0.5)

    tab.Page.addScriptToEvaluateOnNewDocument(source = jquery)
    # temp = tab.Runtime.evaluate(expression = jquery)
    res = {}
    while True:
        if res.__contains__('result') and res['result']['value']!='':
            break
        res = tab.Runtime.evaluate(expression='$(".__emchatrs3_cmfb>div:eq(1)>span").text()',awaitPromise = True)
    print(res)
    print(url1)
    val = res['result']['value'].replace('%',"")
    result.append({'code': line[2], 'value': float(val)})
tab.stop()
    # close tab

browser.close_tab(tab)
nsmall = nsmallest(10,result,key=lambda s:s['value'])
print(nsmall)
# wait for loading
# stop the tab (stop handle events and stop recv message from chrome)






def pychrome_send_click(tab, x, y, button='left'):
    """https://github.com/cyrus-and/chrome-remote-interface/wiki/Trigger-synthetic-click-events"""
    assert isinstance(tab, pychrome.Tab)
    assert isinstance(x, int) and isinstance(y, int)
    # info = tab.Input.dispatchMouseEvent(type='mouseMoved', x=x, y=y, button='left', clickCount=1, modifiers=0)
    info = tab.Input.dispatchMouseEvent(type='mousePressed', x=x, y=y, button=button, clickCount=1, modifiers=0)
    info = tab.Input.dispatchMouseEvent(type='mouseReleased', x=x, y=y, button=button, clickCount=1, modifiers=0)
    return info


def pychrome_send_keys(tab, char):
    assert isinstance(tab, pychrome.Tab)
    # assert isinstance(char, basestring) and len(char) == 1
    info = tab.Input.dispatchKeyEvent(type='rawKeyDown', windowsVirtualKeyCode=ord(char), unmodifiedText=char, text=char)
    info = tab.Input.dispatchKeyEvent(type='char', windowsVirtualKeyCode=ord(char), unmodifiedText=char, text=char)
    info = tab.Input.dispatchKeyEvent(type='keyUp', windowsVirtualKeyCode=ord(char), unmodifiedText=char, text=char)
    return info


def pychrome_call_element_js(tab, query, js):
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


def pychrome_wait_element_appeared(tab, query, timeout, predicate=None):
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
                info = pychrome_call_element_js(tab, query, js_element_getter('outerHTML'))
                if callable(predicate) and not predicate(info['result']):
                    continue
            return True
        except (KeyError, pychrome.CallMethodException) as e:
            logging.info('pychrome_wait_element_appeared(%r, %r) error: %s(%s)', tab, query, type(e), e)
        finally:
            time.sleep(1.0)
            timeout -= 1.0
    return False


def pychrome_get_document_value(tab, expression):
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

def js_element_caller(call):
    return '(function() { this.%s() })' % call

def js_element_getter(name):
    return '(function() { return this.%s })' % name

def js_element_setter(name, value):
    return '(function() { this.%s= "%s" })' % (name, value)

def js_element_position():
    return '(function() {x=this.offsetLeft;y=this.offsetTop;i=this.offsetParent;while(i!==null){x+=i.offsetLeft;y+=i.offsetTop;i=i.offsetParent;}return x+" "+y;})'

def js_document_get_htmls(cssselector):
    return 'JSON.stringify(Array.prototype.slice.call(document.querySelectorAll("%s")).map(function(e){return e.outerHTML}))' % cssselector

def js_document_get_html(cssselector):
    return 'document.querySelector("%s").outerHTML' % cssselector

def js_document_get_tagattr(tag, attr):
    return 'document.getElementsByTagName("%s")[0].attributes["%s"].value' % (tag, attr)

def js_document_get_text(element_id):
    return 'document.getElementById("%s").innerText' % element_id