"""Flask extensions.

If you need to use one of this extensions, you need to import them from
this module. It will prevent circular imports in Flask app.
"""

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.script import Manager


db = SQLAlchemy()
migrate = Migrate()
manager = Manager()

# Script manager.
batch = Manager()
