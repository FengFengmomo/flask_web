from flask import Blueprint,render_template,session,redirect,url_for,request,send_from_directory, current_app
from werkzeug.utils import secure_filename

tools = Blueprint('tools',__name__)
@tools.route('/')
def hello_world(name=None,age=None):
    name = 'zyf'
    age = 23
    ids = [1,2,3,4]
    boxes =['box1','box2','box3']
    return render_template('include_list.html',age = age,name=name,ids = ids,boxes = boxes)

@tools.before_request
def auth():
    logined = session.get("userid")
    # print(request.host_url)
    # print(request.host)
    # print(request.path)
    # print(request.full_path)
    print('userid' in session)
    if 'userid' not in session and request.path != "/manage/loginpage" and request.path != "/manage/login":
        print('redirect')
        # return redirect(url_for("manage.login_page"))

@tools.before_request
def security():
    logined = session.get("userid")
    if not logined:
        pass
        # redirect()


@tools.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save(secure_filename(f.filename))

@tools.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename)

@tools.route("/logger")
def upload():
    current_app.logger.debug('123')
    current_app.logger.warning('123')
    current_app.logger.error('123')
    return redirect(url_for("login"))


@tools.route("/hello/<name>")
def hello(name):
    print(request.args.get('name', ''))
    return "hello everyone  {} profile".format(name)

@tools.route("/login1/<int:post_id>")
def login1(post_id):
    return "post_id %d" % post_id

@tools.route("/uuid/<uuid:post_id>")
def uuid(post_id):
    return "uuid %d" % post_id

@tools.route("/path/<path:subpath>")
def path(subpath):
    return "subpath %d" % subpath



