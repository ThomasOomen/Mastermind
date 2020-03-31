from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from main.Model.model import User, UserStats


class RegForm(FlaskForm):
    username = StringField("Gebruikersnaam", validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Deze gebruikersnaam bestaat al")


class LoginForm(FlaskForm):
    username = StringField("Gebruikersnaam", validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField("Login")


class InfoForm(FlaskForm):
    playNormal = SubmitField("normalGame")
    playCheat = SubmitField("cheatGame")