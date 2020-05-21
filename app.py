from flask import Flask, render_template,request, jsonify,session
from flask_session.__init__ import Session
from flask_uploads import configure_uploads, IMAGES, UploadSet
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import FileField,StringField
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://icmwuvgxqphskl:29518807a50b98eff4637464f45393efd41a9e80b3dff925af7c55e28e967b28@ec2-54-210-128-153.compute-1.amazonaws.com:5432/d9u7e52sn8k5ti'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOADED_IMAGES_DEST']= "static/"
images = UploadSet('images',IMAGES)
configure_uploads(app,images)
db = SQLAlchemy(app)
Session(app)

class Photo(FlaskForm):
   image = FileField('image')    
class Users(db.Model):
    __tablename__ = "user_profiles"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80))
    password = db.Column(db.String(120))
    email = db.Column(db.String(120))
    location = db.Column(db.String(120))
    biography = db.Column(db.String(255))
    profile_photo = db.Column(db.String(255))
    joined_on = db.Column(db.String(255))
    def __init__(self, first_name, last_name,username,password, gender, email, location,
                 biography, photo):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email
        self.location = location
        self.biography = biography
        self.profile_photo = photo
        self.joined_on = format_date_joined()
class Posts(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    photo = db.Column(db.String(255))
    caption = db.Column(db.String(255))
    created_on = db.Column(db.String(255))
    def __init__(self,id,user_id,photo,caption,created_on):
        self.user_id=user_id
        self.photo=photo
        self.caption=caption
        self.created_on= format_date_joined()
class Likes(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)
    def __init__(self,id,user_id,post_id):
        self.user_id=user_id
        self.post_id=post_id
class Follows(db.Model):
    __tablename__ = "follows"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    follower_id = db.Column(db.Integer)
    def __init__(self,id,user_id,follower_id):
        self.follower_id=follower_id
        self.user_id=user_id
        def __repr__(self):
            return self.id
            
db.create_all()

@app.route('/test', methods=['GET']) 
def api_test():
    return jsonify({"username":session['username'],"password":session['password']})

@app.route('/api/users/register', methods=['POST']) 
def api_register():
    content=request.json
    data=Users(content['first_name'], content['last_name'],content['username'],content['password'],"Male", content['email'], content['location'],content['biography'],"photo")
    db.session.add(data)
    db.session.flush()
    db.session.commit()
    return jsonify({"message:":"User successfully registered"})
    
@app.route('/api/users/addphoto/<string:uname>', methods=['POST']) 
def api_photo(uname):
    PhotoForm=Photo()
    filename = images.save(PhotoForm.image.data)
    user = Users.query.filter_by(username=uname).first()
    user.photo= filename 
    db.session.flush()
    db.session.commit()
    return jsonify({"message:":"Photo Added"})

    
@app.route('/api/auth/login', methods=['POST']) 
def api_login():
    content=request.json
    users = Users.query.all()
    for user in users:
        if user.username==content['username'] and user.password==content['password'] :
            session['id']=user.id
            return jsonify({"message:":"User successfully logged in"})
    return jsonify({"message":"User login failed"})
    
@app.route('/api/session', methods=['GET']) 
def api_session():
    try:
        return jsonify({"message":session['id']})
    except KeyError as err:
        return jsonify({"message":0})
    return 0
@app.route('/api/auth/logout', methods=['GET']) 
def api_logout():
    session.pop('id', None)
    return jsonify({"message:":"User successfully logged out"})

@app.route('/api/users', methods=['GET']) 
def api_users():
    dataJson = []
    users = Users.query.all()
    for user in users:
        dataJson.append({
        'id': user.id,    
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'password': user.password,
        'email': user.email,
        'location': user.location,
        'biography': user.biography,
         'photo': user.profile_photo,
        })            
    return jsonify(dataJson)
    
@app.route('/api/user/<int:id>', methods=['GET']) 
def api_user(id):
    if id ==0:
        id=session['id'] 
    users = Users.query.all()
    for user in users:
        if user.id == id:
            return jsonify({
            'id': user.id,    
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'password': user.password,
            'email': user.email,
            'location': user.location,
            'biography': user.biography,
            'photo': user.profile_photo,
        })            
    return jsonify({"message:":"User not found"})


@app.route('/api/users/<string:id>/posts', methods=['POST','GET']) 
def api_posts(id):
    dataJson = []
    if id ==0:
        id=session['id'] 
    posts = Posts.query.all()
    if request.method == "POST":
            content=request.json
            data=Posts(0,id,content['photo'],content['caption'],format_date_joined())
            db.session.add(data)
            db.session.flush()
            db.session.commit()
            return jsonify({"message:":"Post successfully added"})

    if request.method == "GET":
        for post in posts:
            if post.user_id==int(id):
                dataJson.append({
                'id': post.id,
                'user_id': post.user_id,
                'photo': post.photo,
                'caption': post.caption,
                'created_on': post.created_on,
            })            
        return jsonify(dataJson)
        

@app.route('/api/users/<string:id>/follow', methods=['POST']) 
def api_follow(id):
    content=request.json
    data=Follows(0,content['user_id'],content['follower_id'])
    db.session.add(data)
    db.session.flush()
    db.session.commit()    
    return jsonify({"message:":"successfully followed user"})
    
@app.route('/api/posts', methods=['GET']) 
def api_all_posts():
    dataJson = []
    posts = Posts.query.all()
    for post in posts:
        dataJson.append({
        'id': post.id,
        'user_id': post.user_id,
        'photo': post.photo,
        'caption': post.caption,
        'created_on': post.created_on,
        })            
    return jsonify(dataJson)
    
@app.route('/api/posts/<string:id>/like', methods=['POST']) 
def api_like(id):
   content=request.json
   data=Likes(0,content['user_id'],content['post_id'])
   db.session.add(data)
   db.session.flush()
   db.session.commit()    
   return jsonify({"message:":"successfully followed user"})
    
def format_date_joined():
    import datetime
    now = datetime.datetime.now()  # today's date
    date_joined = now  # a specific date
    return date_joined.strftime("%B %V, %Y")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """
    Because we use HTML5 history mode in vue-router we need to configure our
    web server to redirect all routes to index.html. Hence the additional route
    "/<path:path".
    Also we will render the initial webpage and then let VueJS take control.
    """
    try:
        
        return render_template('index.html',curent=session['id'])
    except KeyError as err:
        return render_template('index.html',current=0)
@app.errorhandler(404)
def page_not_found(error):

    """Custom 404 page."""

    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)