"""Main view for common things."""

import flask
import flask.views


main = flask.Blueprint('main', 'main')


class IndexView(flask.views.MethodView):
    """Some view. For now just for test."""

    methods = ('GET',)

    def get(self):
        """Hello world."""
        return '<h1>Hello World</h1>'


main.add_url_rule('/', view_func=IndexView.as_view('index'))
