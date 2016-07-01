"""Basic app compile file."""
import flask
import flask_migrate

import app.batch
import app.extensions
import app.views
import app.middlewares

# init app
application = flask.Flask(__name__, template_folder='./templates',
                          static_folder='./static')

application.config.from_object('config')

# init database
FlaskDB = app.extensions.db
FlaskDB.init_app(application)

# init migrate
FlaskMigrateScript = app.extensions.migrate
FlaskMigrateScript.init_app(application, FlaskDB)

# script managers
FlaskManager = app.extensions.manager
FlaskManager.app = application
FlaskManager.add_command('db', flask_migrate.MigrateCommand)
FlaskManager.add_command('script', app.batch.batch)

# register blueprints
application.register_blueprint(app.views.main)
application.register_blueprint(app.views.user, url_prefix='/user')
application.register_blueprint(app.views.post, url_prefix='/posts')

# register middlewares
if application.config.get('PROFILER_ENABLE', False) is True:
    application.wsgi_app = \
        app.middlewares.ProfileMiddleWare(application.wsgi_app)
