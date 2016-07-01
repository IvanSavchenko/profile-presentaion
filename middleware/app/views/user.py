"""View for procceed all manipulations with user."""

import flask
import flask.views

import app.utils

from database.models import User

user = flask.Blueprint('user', 'user')


class UserView(flask.views.MethodView):
    """View which provides get, patch and post methods.

    Methods (in plan):
        GET - receive information about user.
        POST - login user in and return token.
        PATCH - edit user information.
    """

    methods = ('GET', 'PATCH', 'POST')

    @app.utils.auth_token_required
    def get(self):
        """Retrieve user's information by token provided in request header."""
        user = User.query.get(flask.g.user_id)

        avoid_fields = ('_password',)
        user_data = user.instance_to_dict(avoid_fields)

        return flask.jsonify(**user_data)

    def post(self):
        """Login user in and (if success) return token for user."""
        login_data = flask.request.json

        validation = self._check_login_data(login_data)

        if validation is False:
            return flask.jsonify({'Message': 'Wrong login data.'})

        return flask.jsonify({'token': validation.token})

    def _check_login_data(register_data):
        """Check if user provided correct login data."""
        password = register_data.get('password', None)
        username = register_data.get('username', None)

        # Should i do more output messages?
        if username is not None:
            user = User.query.filter_by(username).first()

            if password is not None:
                password_checked = user.check_password(password)

        if password_checked is True:
            return user

        return False


class UserRegistration(flask.views.MethodView):
    """View for user registration.

    Required:
        :param username: auth username.
        :param password: auth paasword.

    Not required:
        :param email: email address.
        :param first_name: users first name.
        :param last_name: users last name.
        :param bio: users bio.
        :param mobile_number: mobile number.

    """

    methods = ('POST',)

    def post(self):
        """Register method."""
        register_data = flask.request.json

        data_checked = self._check_register_data(register_data)

        if data_checked is True:
            user = User.create(**register_data)
            user.commit()
            return flask.jsonify({'token': user.token})

        return flask.jsonify({'message': 'Wrong register data. {}'
                             .format(data_checked)})

    def _check_register_data(self, register_data):
        """Validation of register data."""
        username = register_data.get('username', None)
        password = register_data.get('password', None)

        if username is not None:
            user = User.query.filter_by(username=username).first()

            if user is not None:
                return 'User allready exists.'

            if len(password) < 6:
                return ("""Password is too small.
                        Provide password more then 6 character.""")

            return True

        return False


user.add_url_rule('/', view_func=UserView.as_view('get_user'))
user.add_url_rule('/register/',
                  view_func=UserRegistration.as_view('register_user'))
