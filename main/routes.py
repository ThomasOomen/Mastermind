import flask_login
from flask import render_template, url_for, redirect, flash, request, session
from main import app, db
from main.Logic.MasterMindGame import GameSetup, GameLogic
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
    return render_template('LogIn.jinja', title="register", form=form)


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
    return render_template('register.jinja', title="register", form=form)


@app.route("/info", methods=['GET', 'POST'])
def userinfo():
    form = InfoForm()
    active_user = flask_login.current_user.id
    info = UserStats.query.filter_by(user_id=active_user).all()
    if form.validate_on_submit():
        if form.amount_of_rows.data <= form.amount_of_colors.data or form.double_colors.data == "True":
            active_user = flask_login.current_user.id

            game = Game(amount_of_colors=form.amount_of_colors.data, amount_of_rows=form.amount_of_rows.data,
                        cheat=form.cheat.data, double_colors=form.double_colors.data, user_id=active_user)
            db.session.add(game)
            db.session.commit()

            return redirect(url_for("newgame"))
        else:
            flash('Alle velden moeten worden ingevuld, aantal velden en kleuren 4 t/m 6. '
                  'Als je meer velden dan kleuren invult moet je dubbele kleuren ook aanzetten', 'danger')
    else:
        flash('Alle velden moeten worden ingevuld, aantal velden en kleuren 4 t/m 6. '
              'Als je meer velden dan kleuren invult moet je dubbele kleuren ook aanzetten')
    return render_template('userInfo.jinja', title="userInfo", form=form, info=info)


@app.route("/newgame", methods=['POST', 'GET'])
def newgame():
    active_user = flask_login.current_user.id
    info = Game.query.filter_by(user_id=active_user).first()
    gameSetup = GameSetup(info.amount_of_colors, info.amount_of_rows, info.cheat, info.double_colors)
    gameSetup.game_setup(gameSetup.build_usable_colors())
    form = GameForm()
    form.input.choices = gameSetup.get_usable_colors()
    session["code"] = gameSetup.get_code()
    session["usable_colors"] = form.input.choices
    session["active_user"] = active_user
    session["cheat"] = gameSetup.get_cheat()
    session["colors"] = info.amount_of_colors
    session["rows"] = info.amount_of_rows
    session["guessed_colors"] = []
    session["correct_guesses"] = []
    session["guesses_used"] = 0
    return render_template("Game.jinja", form=form, rows=info.amount_of_rows, colors=info.amount_of_colors,
                           code=gameSetup.get_code(), cheat=gameSetup.get_cheat(),
                           guesses_used=session.get("guesses_used"), guessed_colors=[])


@app.route('/game', methods=['POST'])
def game():
    if "gameLogic" in locals():
        return gameLogic.update(request.values.getlist('input'))
    else:
        gameLogic = GameLogic(session.get("code"), session.get("usable_colors"), session.get("active_user"),
                              session.get("cheat"), session.get("colors"), session.get("guessed_colors"),
                              session.get("guesses_used"), session.get("correct_guesses"), session.get("rows"))
        return gameLogic.update(request.values.getlist('input'))