"""Local config file."""

DEBUG = True

DATABASE_HOST = 'localhost'
DATABASE_NAME = 'posts'
USER = 'postuser'
PASSWORD = 'bestpassword'


SQLALCHEMY_DATABASE_URI = "postgresql://{user}:{password}@{host}/{db}".format(
        user=USER, password=PASSWORD, host=DATABASE_HOST, db=DATABASE_NAME)

SQLALCHEMY_TRACK_MODIFICATIONS = True
