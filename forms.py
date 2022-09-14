from typing import Text
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField

class NameForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    about = TextAreaField("About User *Not Required")
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message="Passwords Must Match")])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    pfp = FileField("Profile Photo")
    submit = SubmitField("Submit")
    
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    # content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    content = CKEditorField("Content", validators=[DataRequired()], widget=TextArea())
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")