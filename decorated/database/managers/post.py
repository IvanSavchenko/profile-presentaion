"""Manager for Post model."""


class PostsManager(object):
    """Post manager.

    Insert basic methods to work with post model here.

    """

    @classmethod
    def get_posts_by_user_id(cls, user_id):
        """Return all posts created by choosen user.

        :param user_id: id of chosen user.

        """
        posts = cls.query.filter_by(creator_id=user_id).all()
        return posts
