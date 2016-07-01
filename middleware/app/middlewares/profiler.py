"""Profile middleware module."""

import cProfile
import datetime
import os

import config


class ProfileMiddleWare(object):
    """Simple midlleware for profile app."""

    profiler = cProfile.Profile()

    def __init__(self, app):
        """Initialization."""
        self.app = app
        self.profiler.enable()
        self.filepath = self.get_filepath()

    def __call__(self, environ, start_response):
        """Proceed middleware."""
        response_data = self.app(environ, start_response)
        self.dump_profile_data()
        return response_data

    def __del__(self):
        """Flush data."""
        self.dump_profile_data()

    def get_filepath(self):
        """Produce filepath."""
        prof_date = datetime.datetime.now().strftime('%d_%m')
        filename = '{}_{}.prof'.format('app', prof_date)
        filepath = os.path.join(config.BASE_DIR, 'profilers', filename)
        return filepath

    def dump_profile_data(self):
        """Dump profiler stats."""
        self.profiler.dump_stats(self.filepath)
