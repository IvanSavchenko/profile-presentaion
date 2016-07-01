"""User's manager."""

import flask.ext.login
import werkzeug.security


class UserManager(flask.ext.login.UserMixin):
    """Manager for perform secure password set and get by working with hash."""

    def check_password(self, password):
        """Check if hashed password is the same as inputed.

        :param password: checked password.

        """
        return werkzeug.security.check_password_hash(self._password, password)

    @classmethod
    def get_user_by_token(cls, token):
        """Get user by token."""
        return cls.query.filter_by(token=token).first()

    def get_auth_token(self):
        """Return auth token for user."""
        token = werkzeug.sercurity.make_secure_token(str(self.id))
        return token
