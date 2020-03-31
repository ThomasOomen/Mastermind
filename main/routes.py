from flask import render_template, url_for, redirect, flash, request
from main import app, db
from main.Logic.forms import LoginForm, RegForm, InfoForm
from main.Model.model import User, UserStats
from flask_login import login_user


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
        user = User(username=form.username.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account gemaakt met gebruikersnaam: {form.username.data}!', 'success')
        return redirect(url_for("login"))
    return render_template('register.html', title="register", form=form)


@app.route("/info" , methods=['GET', 'POST'])
def userinfo():
    form = InfoForm()
    return render_template('userInfo.html', title="userInfo", form=form)


@app.route("/normalgame")
def normalgame():
    return render_template("userInfo.html")