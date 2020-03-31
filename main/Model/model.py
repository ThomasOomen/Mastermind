from datetime import datetime
from main import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    Games = db.relationship('UserStats', backref="username", lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}')"

class UserStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_played = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    win = db.Column(db.Boolean, nullable=False)
    cheat = db.Column(db.Boolean, nullable=False)
    amount_of_guesses = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.date_played}', '{self.win}', '{self.cheat}', '{self.amount_of_guesses}', '{self.user_id}')"