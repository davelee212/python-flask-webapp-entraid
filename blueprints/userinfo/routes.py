from flask import Blueprint, render_template, session
from flask_session import Session

from blueprints.auth.decorators import login_required

# Defining a blueprint
userinfo = Blueprint(
    'userinfo', __name__,
    template_folder='templates',
    static_folder='static'
)

@userinfo.route('/')   # Focus here
@login_required #**This decorator authenticates the flask route**
def userinfo_index():
    return render_template('userinfo_index.html', user=session.get('user')['name'], preferred_username=session.get('user')['preferred_username'], roles=session.get('user')['roles'])