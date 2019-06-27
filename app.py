from werkzeug.serving import run_simple
from util import create_app

# application = DispatcherMiddleware(app,{'/front': fr.create_app(), '/back': qs.app })
app = create_app(None)

if __name__ == '__main__':
    run_simple('localhost',5000,app,use_reloader=True,use_debugger=True,use_evalex=True)