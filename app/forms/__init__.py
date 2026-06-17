from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (StringField, PasswordField, BooleanField, TextAreaField,
                     SelectField, SubmitField, IntegerField, FloatField)
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError


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


class MatricResultForm(FlaskForm):
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=2000, max=2100)])
    candidates = IntegerField('Candidates', validators=[DataRequired(), NumberRange(min=1)])
    pass_rate = FloatField('Pass Rate (%)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    bachelor_passes = IntegerField('Bachelor Passes', validators=[DataRequired(), NumberRange(min=0)])
    diploma_passes = IntegerField('Diploma Passes', validators=[DataRequired(), NumberRange(min=0)])
    higher_cert_passes = IntegerField('Higher Certificate Passes', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Save Result')


_GRADES = [('', '— Select —'), ('Grade 7', 'Grade 7'), ('Grade 8', 'Grade 8'),
           ('Grade 9', 'Grade 9'), ('Grade 10', 'Grade 10'), ('Grade 11', 'Grade 11'),
           ('Grade 12', 'Grade 12'), ('Other', 'Other')]

_APPLYING_GRADES = [('', '— Select —'), ('Grade 8', 'Grade 8'), ('Grade 9', 'Grade 9'),
                    ('Grade 10', 'Grade 10'), ('Grade 11', 'Grade 11'), ('Grade 12', 'Grade 12')]


class ApplicationRequestForm(FlaskForm):
    parent_name = StringField('Parent / Guardian Full Name', validators=[DataRequired(), Length(1, 100)])
    parent_email = StringField('Parent / Guardian Email', validators=[DataRequired(), Email(), Length(1, 120)])
    parent_phone = StringField('Parent / Guardian Phone', validators=[DataRequired(), Length(1, 20)])
    learner_first_name = StringField('Learner First Name', validators=[DataRequired(), Length(1, 50)])
    learner_last_name = StringField('Learner Surname', validators=[DataRequired(), Length(1, 50)])
    current_grade = SelectField('Current Grade', choices=_GRADES, validators=[DataRequired()])
    grade_applying = SelectField('Grade Applying For', choices=_APPLYING_GRADES, validators=[DataRequired()])
    popia_consent = BooleanField('I consent to the collection and processing of this information', validators=[DataRequired()])
    submit = SubmitField('Submit Application Request')

    def validate_popia_consent(self, field):
        if not field.data:
            raise ValidationError('You must accept the POPIA consent to submit.')


class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(1, 100)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(1, 120)])
    message = TextAreaField('Your Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')
