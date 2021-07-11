from app import app
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)


class PostSerializer(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'date')
