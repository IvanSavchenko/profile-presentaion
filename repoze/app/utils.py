"""Utils should lay here."""

import cProfile
import datetime
import config
import functools
import os

import flask

from database.models import User


def _check_token():
    """Custom user auth by token."""
    request_token_header = getattr(config,
                                   'SECURITY_TOKEN_AUTHENTICATION_HEADER',
                                   'Token')

    token = flask.request.headers.get(request_token_header, None)

    if token is not None:
        user = User.get_user_by_token(token)
        return user if user is not None else False

    return False


def auth_token_required(fn):
    """Decorator that protects endpoints using token authentication.

    The token should be added to the request by the client by using
    a query string variable with a name equal to the configuration value of
    'SECURITY_TOKEN_AUTHENTICATION_KEY` or in a request header named that of
    the configuration value of `SECURITY_TOKEN_AUTHENTICATION_HEADER`

    """
    @functools.wraps(fn)
    def decorated(*args, **kwargs):
        user = _check_token()

        if user is not False:
            # Putting user id into global instance so we can find him easily.
            setattr(flask.g, 'user_id', user.id)
            return fn(*args, **kwargs)
            del flask.g.user_id

        return flask.jsonify(error=403, text='Not authorized'), 403

    return decorated


def profile_this_function(fn):
    """Function profile decorator.

    Creates stats and saves statistic into 'profilers' dir. Use any
    visualizator to check profiler's stats.

    Every profiler file wold be created with next format: function_data.prof.
    Example: app.views.user_get_28_06.prof
    """
    @functools.wraps(fn)
    def profiling(*args, **kwargs):
        # Ebable profiler.
        profiler = cProfile.Profile()
        profiler.enable()

        # Calling function.
        response_data = fn(*args, **kwargs)

        # Gatther profile stats.
        profiler.disable()

        if not os.path.isdir(os.path.join(config.BASE_DIR, 'profilers')):
            os.mkdir(os.path.join(config.BASE_DIR, 'profilers'))

        # Make file name and set file path.
        prof_date = datetime.datetime.now().strftime('%d_%m')
        filename = '{}_{}_{}.prof'.format(fn.__module__, fn.__name__,
                                          prof_date)
        filepath = os.path.join(config.BASE_DIR, 'profilers', filename)

        # Save data.
        profiler.dump_stats(filepath)

        return response_data
    return profiling
