import random
from main.Logic.forms import GameForm
from flask import render_template
from main.Model.model import UserStats, Game
from datetime import datetime
from main import db

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
        for color in range(amount_of_colors):
            colors.append(usable_colors[color][1])

        if double_colors == "False":
            code = random.sample(colors, amount_of_colors)
            self.set_code(code)
            return code
        elif double_colors == "True":
            code = []
            for amount in range(amount_of_colors):
                code.append(random.choice(usable_colors))
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
    def __init__(self, code, usable_colors, active_user, cheat, colors):
        self.mystery_code = code
        self.usable_colors = usable_colors
        self.won = False
        self.cheat = cheat
        self.active_user = active_user
        self.guesses = 10
        self.colors_info = colors
        form = GameForm()
        form.input.choices = self.usable_colors
        self.form = form
        print("weeee")


    def check(self, inputs):
        guesses_correct = []
        temp_code = self.mystery_code.copy()
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

        if len(guesses_correct) == 4 and all(number is 1 for number in guesses_correct):
            self.won = True
        else:
            print("hier moet ie een keer de hoeveelheid guesses ophogen :), maar dat doet ie nog niet")
            # self.update_amount_of_guesses()
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
            return render_template("Game.jinja", form=self.form, colors=self.colors_info,
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
        print(info)
        db.session.delete(info)
        db.session.commit()