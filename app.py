# import modules
from flask import Flask, render_template, session
from flask_session import Session
import json

from werkzeug.middleware.proxy_fix import ProxyFix
from blueprints.auth.decorators import login_required



def create_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__)
    
    # Load Config Option 1: Hard code the App Settings.  This is bad, don't do this.  Maybe OK for testing, but not prod
    # app.config["SESSION_TYPE"] = "filesystem"
    # app.config["MSAL_TENANT"] = "<GUID>"
    # app.config["MSAL_CLIENT_ID"] = "<GUID>"
    # app.config["MSAL_CLIENT_SECRET"] = "<SECRET>"
    # app.config["MSAL_HTTPS_SCHEME"] = "http"

    # Load Config Option 2: Load App Settings from a file
    app.config.from_file('appsettings.development.json', load=json.load)

    # Load Option 3: Load App Settings from environment variables
    # This will load in any environment variables that start with "FLASK_" into app.config.  So if you have a env var called "FLASK_MSAL_TENANT" it will 
    # be loaded into app.config["MSAL_TENANT"]
    # app.config.from_prefixed_env()

    Session(app)

    with app.app_context():

        # Register blueprint for auth
        from blueprints import auth
        app.register_blueprint(auth.construct_blueprint(
                {
                    "TENANT": app.config["MSAL_TENANT"],
                    "CLIENT_ID": app.config["MSAL_CLIENT_ID"],
                    "CLIENT_SECRET": app.config["MSAL_CLIENT_SECRET"],
                    "HTTPS_SCHEME": app.config["MSAL_HTTPS_SCHEME"] 
                }
            ), url_prefix='/auth')

        # Fix "flask.url_for" when deployed to an azure container web app
        # See https://github.com/Azure-Samples/ms-identity-python-webapp/issues/18#issuecomment-604744997
        app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
        
        # Register route for root of the web app
        @app.route("/")
        # Without the @login_required decorator, users can see the page without authenticating
        def index():
            return render_template('root_index.html')

        @app.route("/protected")
        @login_required
        def protected():
            return render_template('root_protected.html', user=session['name'], preferred_username=session.get('user')['preferred_username'])           

        # Import and Register Admin blueprint
        from blueprints.admin.routes import admin
        app.register_blueprint(admin, url_prefix='/admin')

        # Import and Register Admin blueprint
        from blueprints.userinfo.routes import userinfo
        app.register_blueprint(userinfo, url_prefix='/userinfo')

    return app