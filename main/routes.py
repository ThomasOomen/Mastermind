import flask_login
from flask import render_template, url_for, redirect, flash, request
from main import app, db
from main.Logic.MasterMindGame import GameSetup
from main.Logic.forms import LoginForm, RegForm, InfoForm, GameForm
from main.Model.model import User, UserStats, Game
from flask_login import login_user, current_user
from sqlalchemy import desc


@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('userinfo'))
        else:
            flash('Verkeerde gebruikersnaam', 'danger')
    return render_template('LogIn.html', title="register", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        db.session.query(User).get(1)
        user = User(username=form.username.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account gemaakt met gebruikersnaam: {form.username.data}!', 'success')
        return redirect(url_for("login"))
    return render_template('register.html', title="register", form=form)


@app.route("/info", methods=['GET', 'POST'])
def userinfo():
    form = InfoForm()
    if form.validate_on_submit():
        if form.amount_of_rows.data <= form.amount_of_colors.data or form.double_colors.data == "True":
            active_user = flask_login.current_user.id

            game = Game(amount_of_colors=form.amount_of_colors.data, amount_of_rows=form.amount_of_rows.data,
                        cheat=form.cheat.data, double_colors=form.double_colors.data, user_id=active_user)
            db.session.add(game)
            db.session.commit()
            return redirect(url_for("game"))
        else:
            flash('Alle velden moeten worden ingevuld, aantal velden en kleuren 4 t/m 6. '
                  'Als je meer velden dan kleuren invult moet je dubbele kleuren ook aanzetten', 'danger')
    else:
        flash('Alle velden moeten worden ingevuld, aantal velden en kleuren 4 t/m 6. '
              'Als je meer velden dan kleuren invult moet je dubbele kleuren ook aanzetten')
    return render_template('userInfo.html', title="userInfo", form=form)


@app.route("/game")
def game():
    active_user = flask_login.current_user.id

    info = Game.query.filter_by(user_id=active_user).first()
    gameSetup = GameSetup(info.amount_of_colors, info.amount_of_rows, info.cheat, info.double_colors)
    gameSetup.game_setup(gameSetup.build_usable_colors()) # code die je moet raden.
    choices = gameSetup.get_usable_colors()
    form = GameForm()
    form.input.choices = choices
    # form.makeGameForm(gameSetup.game_setup())
    return render_template("Game.html", form=form, colors=info.amount_of_colors, rows=10)



