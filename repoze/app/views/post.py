"""View for posts."""

import flask
import flask.views

from database.models import Post
from database.models import User

from app.utils import auth_token_required

post = flask.Blueprint('post', 'post')


class PostsView(flask.views.MethodView):
    """Class view for post logic.

    Methods: get, post.
    GET: Returns all posts. (paginated in future)
    POST: Save the post to db with current user.
    """

    methods = ('GET', 'POST')

    def get(self):
        """Return list of all posts."""
        posts = Post.query.all()

        avoid_fields = ('modified_at',)
        list_of_posts = [post.instance_to_dict(avoid_fields) for post in posts]

        return flask.jsonify(posts=list_of_posts)

    @auth_token_required
    def post(self):
        """Save post into database."""
        post_data = flask.request.json
        creator = User.query.get(flask.g.user_id)

        new_post = Post.create(creator=creator, **post_data)
        new_post.commit()

        avoid_fields = ('modified_at',)
        return flask.jsonify(new_post.instance_to_dict(avoid_fields))


class UsersPostsView(flask.views.MethodView):
    """View for return posts made by current user."""

    methods = ('GET',)

    @auth_token_required
    def get(self):
        """Return list of posts by current user."""
        user = User.query.get(flask.g.user_id)

        avoid_fields = ('modified_at',)
        posts = Post.query.filter_by(creator=user).all()
        list_of_posts = [post.instance_to_dict(avoid_fields) for post in posts]

        return flask.jsonify(posts=list_of_posts)


post.add_url_rule('/', view_func=PostsView.as_view('posts'))
post.add_url_rule('/user', view_func=UsersPostsView.as_view('user'))
