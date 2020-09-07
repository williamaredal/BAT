############ Forms ############
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

############ Signup ############
class SignupForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=6, message='Username must be longer than 6 characters.')
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8, message='Select a stronger password.')
        ]
    )

    confirm = PasswordField(
        'Confirm your password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ]
    )

    submit = SubmitField('Register')


############ Authentication ############
class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired()]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )

    submit = SubmitField('Authenticate')


############ Beam Terminal ############
class TerminalForm(FlaskForm):
    terminal = StringField(
        'Terminal',
        validators=[DataRequired()]
    )


############ Make ############
class MakeForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired()]
    )

    protocol = TextAreaField(
        'Protocol',
        validators=[DataRequired()]
    )

    poi = TextAreaField(
        'Persons of interest',
        validators=[DataRequired()]
    )

    attachment = TextAreaField(
        'Dossier attachments',
        validators=[DataRequired()]
    )
    
    submit = SubmitField('Make')


############ Update ############
class UpdateForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired()]
    )

    protocol = TextAreaField(
        'Protocol',
        validators=[DataRequired()]
    )

    poi = TextAreaField(
        'Persons of interest',
        validators=[DataRequired()]
    )

    attachment = TextAreaField(
        'Dossier attachments',
        validators=[DataRequired()]
    )

    submit = SubmitField('Update')
