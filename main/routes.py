import flask_login
from flask import render_template, url_for, redirect, flash, request
from main import app, db
from main.Logic.forms import LoginForm, RegForm, InfoForm
from main.Model.model import User, UserStats, Game
from flask_login import login_user, current_user


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
        active_user = flask_login.current_user.id
        game = Game(amount_of_colors=form.amount_of_colors.data, amount_of_rows=form.amount_of_rows.data,
                    cheat=form.cheat.data, double_colors=form.double_colors.data, user_id=active_user)
        db.session.add(game)
        db.session.commit()
        return redirect(url_for("game"))
    else:
        flash('Alle velden moeten worden ingevuld, aantal velden en kleuren 4 t/m 6', 'danger')
    return render_template('userInfo.html', title="userInfo", form=form)


@app.route("/game")
def game():
    return render_template("Game.html")