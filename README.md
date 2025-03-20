# Scaffold for Python Web App with Entra ID Authentication

This project is a Python web application that demonstrates Entra ID authentication, including the ability to see the App Roles assigned to the user. It also showcases the use of protected and unprotected pages.  It follows the Application Factory/Blueprints method.  It demonstrates setting app config from files, environment variables or directly into app.config itself.

## Why

I'll start by saying, I'm not a software developer... but I did a fair bit of application support and development early on in my career and I do like writing code.

Very early on in my career, I used to like knocking up internal use admin portals in "classic" Active Service Pages (ok, they weren't "classic" back then, but this was before ASP.NET).  I wanted to be able to do something similar but with a more modern language/framework/approach.

I've had a look at Blazor in the past, given I thought it would be the obvious choice being sort of like ASP I was used to - but I've never really got my head around Dot Net, so something else was required.

So, Python/Flask it is :D


## Blueprints

Blueprints are a pattern for modularising Flask web apps.  They are described in detail here: https://flask.palletsprojects.com/en/stable/blueprints/

The TLDR version

- A blueprint is a folder that contains the python code, template HTML files and static content that comprise a piece of functionality or a feature in an application.
- Separating functions into different blueprints, over having all code in a single python file, helps with scalability and code organisation.
- Each blueprint contains:
   - a routes.py file that contains the available URIs for that application and the code that runs when the URI is requested
   - the template HTML files that are used when the render_template is used
   - any static files
- Each blueprint is "registered" to the application as defined in the app.py file in the root of the application.  This  provides a mapping to the URI (routes) defined within that blueprint.


## Templates

### How templates work in Blueprints

As of Flask 0.8, blueprints add the specified template_folder to the app's searchpath, rather than treating each of the directories as separate entities. This means that if you have two templates with the same filename, the first one found in the searchpath is the one used.

To ensure that there is no ambiguity over which template is used, the files in "templates" folder for each blueprint have the blueprint name as a prefix.  So any routes in this blueprint (called "userinfo") that return a rendered page will reference the template file as userinfo_filename.html.

This also has the advantage of allowing you to reference templates from other blueprints just by using the filename.  Where this is really useful is if you have template header, footer or base files in the root of the application.  These can easily be referenced in blueprint template files without providing a specific path.


### The templates in this sample app

The templates and static folders at the root of this project contain the files that are used at the root of the app and a "root_base.html" file which is referenced by all other HTML files.  root_base.html contains the styling and navbar (implemented using out-the-box Bootstrap 5) is used by all blueprints.  The HTML files in the blueprints define the content that is loaded into the framework defined in root_base.html.


## Microsoft Entra ID Integration

Microsoft Authentication Library for Python provides the integration with Entra ID.  There is documentation on it here: https://learn.microsoft.com/en-us/entra/msal/python/

There is an example Flask project that includes Entra ID authentication here: https://github.com/AzureAD/microsoft-authentication-library-for-python  Although very easy to get started with, I found it difficult to figure out how to retrieve the list of AppRoles the user is assigned to, which would be key to RBAC in a webapp.

I found the following blog post from Andrew Sprague on [Flask Blueprint for Microsoft Azure AAD Authentication](https://andysprague.com/2020/11/11/flask-blueprint-for-microsoft-azure-aad-authentication-oauth-2-0/).  I needed to make a few modifications to make it work in my app.  Some of that may well be due to my inexperience with Flask and Blueprints at the time, but it's largely implemented as described in Andrew's blog post.



## Quickstart

1. Clone the repo
2. Change to your local version
3. Create a python virtual environment  ```python venv -m venv```
4. Activate the venv (assuming your in a PowerShell prompt):  ```./venv/scripts/activate.ps1```
5. Install prerequisite modules:  ```pip install -r requirements.txt```
6. Configure your Entra ID 
   - Setup the Application Registration for your app to use: See the Register an Application Section here: https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app?tabs=certificate%2Cexpose-a-web-api#register-an-application
   - Setup at least one AppRole with the value ReadAccess and add your Entra ID user to it:  https://learn.microsoft.com/en-us/entra/identity-platform/howto-add-app-roles-in-apps
7. Set the app/reg details in the appsettings.development.json file
6. Run the app locally, e.g.: ```python -m flask run --debug --host=localhost --port=5000```

