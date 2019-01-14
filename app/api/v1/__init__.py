"""
Register Resource endpoints for Api V1
"""

from flask import Blueprint
from flask_restful import Api
from .views.user_view import Index, Register, Login, Logout, RefreshToken
from .views.question_view import Question, QuestionUpvote, QuestionDownvote, QuestionList
from .views.meetup_view import Meetup, Meetups, MeetupsUpcoming, MeetupRsvp
from .views.comment_view import Comment

version_1 = Blueprint('version_one', __name__, url_prefix='/api/v1')

api = Api(version_1)

api.add_resource(Index, '/')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(RefreshToken, '/refresh-token')
api.add_resource(Question, '/questions')
api.add_resource(QuestionUpvote, '/questions/<int:question_id>/upvote')
api.add_resource(QuestionDownvote, '/questions/<int:question_id>/downvote')
api.add_resource(QuestionList, '/meetups/<int:meetup_id>/questions')
api.add_resource(Meetup, '/meetups/<int:meetup_id>')
api.add_resource(Meetups, '/meetups')
api.add_resource(MeetupsUpcoming, '/meetups/upcoming')
api.add_resource(MeetupRsvp, '/meetups/<int:meetup_id>/<string:rsvp>')
api.add_resource(Comment, '/questions/<int:question_id>/comments')
