from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Required, Email, Regexp, EqualTo
from wtforms import ValidationError
from .models import User

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me', default=False)
    submit = SubmitField('Log in')

class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username', validators=[Required(), Length(1, 20), Regexp('^[a-zA-Z][a-zA-Z0-9._]*$', 0, 'Username must only have letters, numbers, dots, and underscores')])
    password1 = PasswordField('Password', validators=[Required(), Length(1, 20)])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already in use')

    def validate_user(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')

class PostForm(Form):
    body = TextAreaField('What\'s on your mind', validators=[Required()])
