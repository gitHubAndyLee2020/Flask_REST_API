from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
# create a database at relative path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
db.create_all()

class VideoModel(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  # nullable=False means that the column cannot be null
  name = db.Column(db.String(100), nullable=False)
  views = db.Column(db.Integer, nullable=False)
  likes = db.Column(db.Integer, nullable=False)
  
  def __repr__(self):
    return f'Video(name = {name}, views = {views}, likes = {likes})'

# run this code to create the database
# db.create_all()

# validates the request arguments
# if the argument is not present, it will automatically add them with the value None
video_put_args = reqparse.RequestParser()
video_put_args.add_argument('name', type=str, help='Name of the video', required=True)
video_put_args.add_argument('views', type=int, help='Views of the video', required=True)
video_put_args.add_argument('likes', type=int, help='Likes of the video', required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument('name', type=str, help='Name of the video')
video_update_args.add_argument('views', type=int, help='Views of the video')
video_update_args.add_argument('likes', type=int, help='Likes of the video')


# defines how to DB instance should be serialized
resource_fields = {
  'id': fields.Integer,
  'name': fields.String,
  'views': fields.Integer,
  'likes': fields.Integer
}

class Video(Resource):
  # this sepcifies that the returning value should be serialized with the resource_fields
  @marshal_with(resource_fields)
  def get(self, video_id):
    # add() to fetch all the instances with id=video_id
    result = VideoModel.query.filter_by(id=video_id).first()
    # checks if the video exists
    if not result: 
      abort(404, message='Could not find video with that id')
    return result
  
  @marshal_with(resource_fields)
  def put(self, video_id):
    args = video_put_args.parse_args()
    # checks if the video already exists
    result = VideoModel.query.filter_by(id=video_id).first()
    if result:
      abort(409, message='Videp id taken...')

    video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
    db.session.add(video)
    db.session.commit()
    return video, 201

  @marshal_with(resource_fields)
  def patch(self, video_id):
    args = video_update_args.parse_args()
    result = VideoModel.query.filter_by(id=video_id).first()
    if not result:
      abort(404, message='Video doesn\'t exist, cannot update') 

    if args['name']:
      result.name = args['name']
    if args['views']:
      result.views = args['views']
    if args['likes']:
      result.likes = args['likes']

    db.session.commit()

    return result, 200

  @marshal_with(resource_fields)
  def delete(self, video_id):
    result = VideoModel.query.filter_by(id=video_id).first()
    if not result:
      abort(404, message='Video doesn\'t exist, cannot delete')
    
    db.session.delete(result)
    db.session.commit()

    return {}, 204

api.add_resource(Video, '/video/<int:video_id>')

# remove debug=True at deployment
if __name__ == '__main__':
  app.run(debug=True)