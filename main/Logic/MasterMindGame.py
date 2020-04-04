import random


class GameSetup:
    def __init__(self, amount_of_colors, amount_of_rows, cheat, double_colors):
        self.amount_of_colors = amount_of_colors
        self.amount_of_rows = amount_of_rows
        self.cheat = cheat
        self.double_colors = double_colors
        self.all_colors = [(0, 'Groen'), (1, 'Geel'), (2, 'Rood'),
                           (3, 'Blauw'), (4, 'Paars'), (5, 'Zwart')]
        self.usable_colors = []

    def print(self):
        print(self.amount_of_colors)
        print(self.amount_of_rows)
        print(self.cheat)
        print(self.double_colors)

    def game_setup(self, usable_colors):
        return self.generate_code(self.amount_of_colors, self.double_colors, self.usable_colors)

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
            return code
        elif double_colors == "True":
            code = []
            for amount in range(amount_of_colors):
                code.append(random.choice(usable_colors))
            print(code)
            return code

    def set_usable_colors(self, usable_colors):
        self.usable_colors = usable_colors

    def get_usable_colors(self):
        return self.usable_colors
