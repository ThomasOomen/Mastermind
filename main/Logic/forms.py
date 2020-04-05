import flask_login
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from main.Model.model import User, UserStats, Game
from flask_login import login_user


class RegForm(FlaskForm):
    username = StringField("Gebruikersnaam", validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Gebruikersnaam bestaat al")


class LoginForm(FlaskForm):
    username = StringField("Gebruikersnaam", validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField("Login")


class InfoForm(FlaskForm):
    amount_of_colors = IntegerField("Aantal kleuren", validators=[NumberRange(min=4, max=6, message='Invalid length'),
                                                                  DataRequired()])
    amount_of_rows = IntegerField("Aantal velden", validators=[NumberRange(min=4, max=6, message='Invalid length'),
                                                               DataRequired()])
    cheat = RadioField('Cheat mode', choices=[('True', u'Ja'), ('False', u'Nee'),], default='False',
                       validators=[DataRequired()])
    double_colors = RadioField('Dubbele kleuren', choices=[('True', u'Ja'),('False', u'Nee')], default='False',
                               validators=[DataRequired()])
    play = SubmitField("play")


class GameForm(FlaskForm):
    input = SelectField("Kleuren", choices=[('groen', 'Groen'), ('geel', 'Geel'), ('rood', 'Rood'),
                                 ('blauw', 'Blauw'), ('paars', 'Paars'), ('zwart', 'Zwart')])
    submit = SubmitField("Check")

