from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, widgets, RadioField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
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
    amount_of_colors = IntegerField("Aantal kleuren", validators=[NumberRange(min=4, max=6, message='Invalid length'),
                                                                  DataRequired()])
    amount_of_rows = IntegerField("Aantal velden", validators=[NumberRange(min=4, max=6, message='Invalid length'),
                                                               DataRequired()])
    cheat = RadioField('Cheat mode', choices=[('1', u'Ja'), ('2', u'Nee'),], default='2',
                       validators=[DataRequired()])
    double_colors = RadioField('Dubbele kleuren', choices=[('1', u'Ja'),('2', u'Nee')], default='2',
                               validators=[DataRequired()])
    play = SubmitField("play")

