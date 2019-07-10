from flask import Blueprint,render_template,session, request, flash,current_app
from werkzeug.security import generate_password_hash
from datetime import timedelta
import asyncio
import threading
# manage = Blueprint('manage',__name__, template_folder='templates',static_folder='static')
tasks = Blueprint('tasks', __name__)
loop = asyncio.get_event_loop()

@tasks.route("/")
def hello():
    return "hello"
@tasks.route("/add")
def add_task():
    print("create tasks")
    task = loop.create_task(worker(1))
    task = asyncio.ensure_future(worker(1),loop=loop)
    # TODO it doesn't work
    # asyncio.run_coroutine_threadsafe(worker(1),loop)
    # loop.call_soon(worker1,1)
    # loop.call_soon_threadsafe(worker1,1)
    return "ok"

async def worker(delay):
    await asyncio.sleep(delay)
    print("worker")
def worker1(delay):
    print("worker1")
@tasks.route("/stop")
def stop():
    loop.stop()
    return "loop stop"
@tasks.route("/start")
def start():
    print("run loop forever")
    thread = threading.Thread(target=loop.run_forever)
    thread.start()
    # thread.setDaemon(True)
    return "ok run loop forever"

def restart():
    global loop
    if loop.is_running():
        loop.close()
    else:loop = asyncio.new_event_loop()
    thread = threading.Thread(target=loop.run_forever)
    thread.start()
    # loop.run_forever()