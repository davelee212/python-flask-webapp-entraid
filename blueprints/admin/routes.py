from flask import Blueprint, render_template, session
from flask_session import Session

from blueprints.auth.decorators import login_required

# Defining a blueprint
admin = Blueprint(
    'admin', __name__,
    template_folder='templates',
    static_folder='static'
)

@admin.route('/')   # Focus here
@login_required #**This decorator authenticates the flask route**
def adminindex():
    return "Admin Index Page"

@admin.route('/hello')   # Focus here
@login_required #**This decorator authenticates the flask route**
def adminhello():
    test = "this is a test string"
    return render_template('admin/hello.html')
    