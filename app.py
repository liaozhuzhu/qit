from cgi import parse_multipart
from email.policy import default
from inspect import Attribute
from re import S
from sre_constants import SUCCESS
from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
import os
from forms import NameForm, UserForm, PostForm, LoginForm, SearchForm, CommentForm
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
import uuid as uuid

# ===== Starter Code ===== 
app = Flask(__name__)
ckeditor = CKEditor(app)
SECRET_KEY = os.environ.get("SECRET_KEY")
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://xpnsmhccilpvqs:5abd2b2b4fae4b6ee3ad0b8fa43c133f09016292dd8d1b6bac7768abf00eaf52@ec2-34-200-205-45.compute-1.amazonaws.com:5432/d8kqv7b2k9q5ga"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:#LzHawkeye21@localhost/users"

UPLOAD_FOLDER = "static/images/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get((user_id))

# ===== Routes =====
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, username=form.username.data, email=form.email.data, about=form.about.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ""
        form.username.data = ""
        form.email.data = ""
        form.about.data = ""
        form.password_hash.data = ""
        login_user(user, remember=True)
        flash("User Added!", category="success")
        return render_template("profile.html")
    
    our_users = Users.query.order_by(Users.date_added)
    return render_template("sign_up.html", name=name, our_users=our_users, form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password_hash.data):
                login_user(user, remember=True)
                return redirect(url_for("home"))
            else:
                flash("Wrong Password, Try Again", category="error")
        else:
            flash("No User Found", category="error")
            
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    return render_template("profile.html")

@app.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id):   
    user_to_update = Users.query.get_or_404(id)
    form = UserForm()
    # if form.validate_on_submit():
    #     user_to_update.name = form.name.data
    #     user_to_update.username = form.username.data
    #     user_to_update.email = form.email.data
        # user_to_update.about = form.about.data
    if request.method == "POST":
        user_to_update.name = request.form["name"]
        user_to_update.username = request.form["username"]
        user_to_update.email = request.form["email"]
        user_to_update.about = request.form["about"]
        
        if request.files["pfp"]:
            user_to_update.pfp = request.files["pfp"]
            pfp_filename = secure_filename(user_to_update.pfp.filename)
            pfp_name = str(uuid.uuid1()) + "_" + pfp_filename
            
            saver = request.files["pfp"]
            user_to_update.pfp = pfp_name     
    
            try:
                db.session.commit()
                saver.save(os.path.join(app.config["UPLOAD_FOLDER"], pfp_name))
                flash("User Updated Successfully", category="success")
                return render_template("profile.html")
            except:
                flash("User Could Not Be Updated", category="error")
                return render_template("update.html", form=form, user_to_update=user_to_update)
        else:
            db.session.commit()
            flash("User Updated Successfully", category="success")
            return render_template("profile.html")
        
    else:
        return render_template("update.html", form=form, user_to_update=user_to_update)

@app.route("/delete/<int:id>")
def delete(id):
    name = None
    form = UserForm()
    user_to_delete = Users.query.get_or_404(id)
    if user_to_delete.id == current_user.id or current_user.id == 1:
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User Deleted", category="success")
            # our_users = Users.query.order_by(Users.date_added)
            # return render_template("sign_up.html", name=name, our_users=our_users, form=form)
            return redirect(url_for('home'))
        
        except:
            flash("Problem Deleting User", category="error")
            return redirect(url_for('profile'))
    else:
        flash("Access Denied", category="error")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("sign_up.html", name=name, our_users=our_users, form=form)
    
@app.route("/add-post", methods=["GET", "POST"])
@login_required
def add_post():
    form = PostForm()
    
    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(title=form.title.data, content=form.content.data, poster_id=poster, slug=form.slug.data)
        form.title.data = ""
        form.content.data = ""
        form.slug.data = ""
        db.session.add(post)
        db.session.commit()
        flash("Post Uploaded!", category="success")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)
        
    return render_template("add_post.html", form=form)    

@app.route("/posts", methods=["GET", "POST"])
def posts():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)

@app.route("/posts/<int:id>", methods=["GET", "POST"])
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template("post.html", post=post)

@app.route("/posts/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = form.slug.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        flash("Post Updated", category="success")
        return redirect(url_for("post", id=post.id))
    
    if current_user.id == post.poster.id:
        form.title.data = post.title
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template("edit_post.html", form=form, id=post.id)
    else:
        flash("Access Denied", category="error")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)

@app.route("/posts/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    if current_user.id == post_to_delete.poster.id or current_user.id == 1:
        try: 
            db.session.delete(post_to_delete)
            db.session.commit()
            flash("Post Deleted", category="success")
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html", posts=posts)
        
        except:
            flash("There Was a Problem Deleting Post", category="error")
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html", posts=posts)
    else:
        flash("Access Denied", category="error")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)
    
#pass search to search bar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)
    
@app.route("/search", methods=["POST"])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        post.searched = form.searched.data
        posts = posts.filter(Posts.content.like("%" + post.searched + "%"))
        posts = posts.order_by(Posts.title).all()
        return render_template("search.html", form=form, searched=post.searched, posts=posts)
    
    else:
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)
    
@app.route("/admin")
@login_required
def admin():
    if current_user.id == 1:
        return render_template("admin.html")        
    else:
        flash("Access Denied", category="error")
        return redirect(url_for("profile"))
    
@app.route("/like/<int:id>", methods=["POST"])
def like(id):
    post_to_like = Posts.query.filter_by(id=id).first()
    like = Likes.query.filter_by(liker=current_user.id, post_id=id).first()
    if not post_to_like:
        # flash("Post Does Not Exist", category="error")
        return jsonify({"error":"Post Does Not Exist"}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Likes(liker=current_user.id, post_id=id)
        db.session.add(like)
        db.session.commit()
        
    # return redirect(url_for("posts"))       
    return jsonify({"likes":len(post_to_like.likes), "liked":current_user.id in map(lambda x: x.liker, post_to_like.likes)})

@app.route("/create-comment/<int:id>", methods=["POST"])
@login_required
def create_comment(id):
    text = request.form.get("text")
    form = CommentForm()
    
    if not text:
        flash("Comment Cannot be Empty", category="error")
        
    else:
        post = Posts.query.filter_by(id=id)
        
        if post:
            comment = Comments(text=text, commentor_id=current_user.id, post_id=id)
            db.session.add(comment)
            db.session.commit()
            
        else:
            flash("Post Does Not Exist", category="error")
    
    form.text.data = ""
        
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts, form=form)

@app.route('/delete-comment/<int:id>', methods=["GET"])
@login_required
def delete_comment(id):
    form = CommentForm()
    comment = Comments.query.filter_by(id=id).first()
    if not comment:
        flash("Comment Does Not Exist", category="error")
        # return jsonify({"error":"Comment Does Not Exist"}, 400)
    elif current_user.id != comment.commentor.id and current_user.id != comment.post.poster_id:
        flash("Access Denied", category="error")
    else:
        db.session.delete(comment)
        db.session.commit()
        
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts, form=form)
    # return jsonify({})
# ===== Models =====
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    poster_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    likes = db.relationship("Likes", backref="post")
    comments = db.relationship("Comments", backref="post")

class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    liker = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    date_commented = db.Column(db.DateTime, default=datetime.utcnow)
    commentor_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(200))
    about = db.Column(db.Text(), nullable=True)
    pfp = db.Column(db.String(200), nullable=True)
    posts = db.relationship("Posts", backref="poster")
    comments = db.relationship("Comments", backref="commentor")
    
    @property
    def password(self):
        raise AttributeError("Password is Not a Readable Attribute")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return "<Name %r>" % self.name