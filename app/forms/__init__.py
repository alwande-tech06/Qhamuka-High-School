from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (StringField, PasswordField, BooleanField, TextAreaField,
                     SelectField, SubmitField)
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Sign In')


class AnnouncementForm(FlaskForm):
    title = StringField('Announcement Title', validators=[DataRequired(), Length(1, 100)])
    content = TextAreaField('Content Body', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('General', 'General Notice'),
        ('Academic', 'Academic Update'),
        ('Sports', 'Sports & Culture'),
        ('Admissions', 'Admissions Notice'),
    ], validators=[DataRequired()])
    is_published = BooleanField('Publish Immediately', default=True)
    submit = SubmitField('Save Announcement')


class GalleryUploadForm(FlaskForm):
    image = FileField('Select Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images Only!'),
    ])
    caption = StringField('Caption/Description', validators=[Length(0, 200)])
    event_name = SelectField('School Event Category', choices=[
        ('Events', 'School Events'),
        ('Sports', 'Sports Activities'),
        ('Cultural', 'Cultural Exhibitions'),
        ('Academic', 'Academic Milestones'),
    ], validators=[DataRequired()])
    submit = SubmitField('Upload to Gallery')


class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(1, 100)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(1, 120)])
    message = TextAreaField('Your Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')
