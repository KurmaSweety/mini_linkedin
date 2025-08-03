from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange
from flask_wtf.file import FileAllowed


class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    headline = StringField('Headline', validators=[Optional(), Length(max=150)])
    current_title = StringField('Current Title', validators=[Optional(), Length(max=100)])
    company = StringField('Company', validators=[Optional(), Length(max=100)])
    location = StringField('Location', validators=[Optional(), Length(max=100)])
    skills = TextAreaField('Skills (comma-separated)', validators=[Optional()])
    education = StringField('Education', validators=[Optional(), Length(max=200)])
    experience_years = IntegerField('Years of Experience', validators=[Optional(), NumberRange(min=0)])
    profile_pic = FileField('Upload Profile Picture', validators=[
        Optional(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Register')


class EditProfileForm(FlaskForm):
    headline = StringField('Headline', validators=[Optional(), Length(max=150)])
    current_title = StringField('Current Title', validators=[Optional(), Length(max=100)])
    company = StringField('Company', validators=[Optional(), Length(max=100)])
    location = StringField('Location', validators=[Optional(), Length(max=100)])
    skills = StringField('Skills (comma-separated)', validators=[Optional()])
    education = StringField('Education', validators=[Optional(), Length(max=200)])
    experience_years = IntegerField('Years of Experience', validators=[Optional()])

    profile_pic = FileField('Update Profile Picture', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])

    submit = SubmitField('Save Changes')


class PostForm(FlaskForm):
    content = TextAreaField('What do you want to share?', validators=[DataRequired()])
    submit = SubmitField('Post')

