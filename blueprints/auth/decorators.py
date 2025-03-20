import flask
from datetime import datetime, timedelta
from functools import wraps
#from application import appsettings as config
from flask import current_app

def login_required(f):
    """
    Decorator for flask endpoints, ensuring that the user is authenticated and redirecting to log-in page if not.
    Example:
    ```
        from flask import current_app as app
        @login_required
        @app.route("/")
        def index():
            return 'route protected'
    ```
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #if not config.REQUIRE_AUTHENTICATION:
            # Disable authentication, for use in dev/test only!
            #if config.HTTPS_SCHEME == 'https':
                #raise ValueError('Not supported: Cant turn off authentication for https endpoints')

            #current_app.logger.error('Authentication is disabled! For dev/test only!')
            #flask.session['user'] = {'name': 'auth disabled'}
            #return f(*args, **kwargs)

        if not flask.session.get("user"):
            print ("User not authenticated, redirecting to auth")
            return flask.redirect(flask.url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function
