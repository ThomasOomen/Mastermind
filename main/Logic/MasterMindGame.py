import random
from main.Logic.forms import GameForm
from flask import render_template, session
from main.Model.model import UserStats, Game
from datetime import datetime
from main import db
from operator import itemgetter

class GameSetup:
    def __init__(self, amount_of_colors, amount_of_rows, cheat, double_colors):
        self.amount_of_colors = amount_of_colors
        self.amount_of_rows = amount_of_rows
        self.cheat = cheat
        self.double_colors = double_colors
        self.all_colors = [(0, 'Groen'), (1, 'Geel'), (2, 'Rood'),
                           (3, 'Blauw'), (4, 'Paars'), (5, 'Zwart')]
        self.usable_colors = []
        self.code = []

    def get_cheat(self):
        return self.cheat

    def game_setup(self, usable_colors):
        code = self.generate_code(self.amount_of_colors, self.double_colors, self.usable_colors)
        return code

    def build_usable_colors(self):
        usable_colors = self.generate_usable_colors_tuple(self.amount_of_colors, self.all_colors, self.usable_colors)
        self.set_usable_colors(usable_colors)
        return usable_colors

    def generate_usable_colors_tuple(self, amount_of_colors, all_colors, usable_colors):
        for color in range(amount_of_colors):
            if any(color in colors for colors in all_colors):
                usable_colors.append(all_colors[color])
        return usable_colors

    def generate_code(self, amount_of_colors, double_colors, usable_colors):
        colors = []
        for color in range(int(self.amount_of_rows)):
            colors.append(usable_colors[color][1])

        if double_colors == "False":
            code = random.sample(colors, self.amount_of_rows)
            self.set_code(code)
            return code
        elif double_colors == "True":
            code = []
            for amount in range(self.amount_of_rows):
                code.append(random.choice(usable_colors))
            print("code na append", code)
            code = list(map(itemgetter(1), code))
            self.set_code(code)
            return code

    def set_usable_colors(self, usable_colors):
        self.usable_colors = usable_colors

    def get_usable_colors(self):
        return self.usable_colors

    def set_code(self, code):
        self.code = code

    def get_code(self):
        return self.code


class GameLogic:
    def __init__(self, code, usable_colors, active_user, cheat, colors, guesses, rows):
        self.mystery_code = code
        self.usable_colors = usable_colors
        self.rows = rows
        self.won = False
        self.cheat = cheat
        self.active_user = active_user
        if guesses is None:
            self.guesses = 1
        else:
            self.guesses = guesses
        self.colors_info = colors
        form = GameForm()
        form.input.choices = self.usable_colors
        self.form = form

    def print(self):
        print(self.usable_colors)
        print(self.rows)

    def check(self, inputs):
        guesses_correct = []
        temp_code = self.mystery_code.copy()
        print("temp code ", temp_code)
        list = []
        for guess in inputs:
            x = self.usable_colors[int(guess)][1]
            list.append(x)

        for color in range(len(list)):
            if temp_code[color] is not None:
                if list[color] == temp_code[color]:
                    temp_code[color] = None
                    guesses_correct.append(1)

        for color in range(len(list)):
            if list[color] in temp_code:
                temp_code[temp_code.index(list[color])] = None
                guesses_correct.append(2)
        print(guesses_correct)
        if len(guesses_correct) == self.rows and all(number is 1 for number in guesses_correct):
            self.won = True
        else:
            self.set_guesses()
            session["guesses"] = self.get_guesses()
        return guesses_correct

    def update(self, inputs):
        self.check(inputs)
        if self.won is True:
            self.updateDb(win=True)
            return render_template('victory.jinja')
        elif self.guesses == 10:
            self.updateDb(win=False)
            return render_template('lose.jinja')
        else:
            return render_template("Game.jinja", form=self.form, rows=self.rows,
                                    code=self.mystery_code, cheat=self.cheat)

    def updateDb(self, win):
        if self.cheat == "False":
            self.cheat = False
        else:
            self.cheat = True
        userstats = UserStats(date_played=datetime.now(), win=win, cheat=self.cheat,
                    amount_of_guesses=self.guesses, user_id=self.active_user)
        db.session.add(userstats)
        db.session.commit()

        info = Game.query.filter_by(user_id=self.active_user).first()
        db.session.delete(info)
        db.session.commit()
       # self.guesses = 0

    def set_guesses(self):
        self.guesses += 1

    def get_guesses(self):
        return self.guesses