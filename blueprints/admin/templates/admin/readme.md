As of Flask 0.8, blueprints add the specified template_folder to the app's searchpath, rather than treating each of the directories as separate entities. This means that if you have two templates with the same filename, the first one found in the searchpath is the one used. 

To ensure that there is no ambiguity over which template is used, the "templates" folder at this level has a subfolder that matches the name of the blueprint.  So any routes in this blueprint that return a rendered page will reference the template file as admin/filename.html.

To ensure that we