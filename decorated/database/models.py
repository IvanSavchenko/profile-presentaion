"""Application models."""
from __future__ import unicode_literals

import uuid

import werkzeug.security

import database.managers

from app.extensions import db


class BaseModel(database.managers.BasicManager, db.Model):
    """Base abstract class for all models."""

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp()
                            )


class User(database.managers.UserManager, BaseModel, db.Model):
    """Model User."""

    __tablename__ = 'user'

    username = db.Column(db.String(length=50), unique=True)
    _password = db.Column(db.String(length=150))
    first_name = db.Column(db.String(length=50))
    last_name = db.Column(db.String(length=50))
    email = db.Column(db.String(length=50))
    mobile_number = db.Column(db.String(length=13))
    bio = db.Column(db.UnicodeText())
    token = db.Column(db.String(length=80))

    # Social credentials
    facebook_id = db.Column(db.String(length=30))
    twitter_id = db.Column(db.String(length=30))
    google_id = db.Column(db.String(length=30))
    github_id = db.Column(db.String(length=30))
    linkedin_id = db.Column(db.String(length=30))

    def __init__(self, *args, **kwargs):
        """Creating token for each user."""
        self.token = str(uuid.uuid4())
        super(User, self).__init__(*args, **kwargs)

    def __str__(self):
        """Simple representation of model."""
        return '{id} - {username}'.format(id=self.id, username=self.username)

    @property
    def password(self):
        """Password getter."""
        return self._password

    @password.setter
    def password(self, password):
        """Password setter."""
        self._password = werkzeug.security.generate_password_hash(password)

    @property
    def full_name(self):
        """Return full name of user."""
        return '{0} {1}'.format(self.first_name, self.last_name)


class Post(database.managers.PostsManager, BaseModel, db.Model):
    """Model Post.

    Relations:
        User: one-to-many.
    """

    __tablename__ = 'post'

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship('User', uselist=False,
                              foreign_keys='Post.creator_id')

    title = db.Column(db.String(length=150))
    text = db.Column(db.UnicodeText())

    __mapper_args__ = {
        'order_by': id
    }

    def __str__(self):
        """Simple representation of model."""
        return '{creator} - {title}'.format(
            creator=self.creator.username,
            title=self.title
        )
