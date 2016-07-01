"""Basic managers for models."""

import flask_sqlalchemy
import werkzeug.exceptions

from app.extensions import db


class BasicManager(object):
    """Basic manager for models includes commont methods."""

    @classmethod
    def create(cls, **arguments):
        """Perform faster instance create.

        Just paste (**dict_with_args) to this method
        to perform init instance creation.

        """
        new_instance = cls()

        for column in arguments:
            setattr(new_instance, column, arguments[column])

        return new_instance

    @classmethod
    def get_table_columns(cls):
        """Return all columns for table except id."""
        return [col.name for col in flask_sqlalchemy.inspect(cls).c
                if col.name not in ['id', ]]

    @classmethod
    def get_or_404(cls, instance_id):
        """Basic Django shortcut on Flask."""
        instance = cls.query.get(instance_id)

        if instance is None:
            werkzeug.exceptions.abort(404)

        return instance

    def instance_to_dict(self, avoid_fields=[]):
        """Convert instance to dictionary."""
        columns = self.get_table_columns()

        columns = set(columns) - set(avoid_fields)

        result_dict = {column: getattr(self, column) for column in columns}

        return result_dict

    def commit(self):
        """Performing fast commit."""
        db.session.add(self)
        db.session.commit()

        return self

    def delete(self):
        """Performing fast delete."""
        db.session.delete(self)
        db.session.commit()

        return True
