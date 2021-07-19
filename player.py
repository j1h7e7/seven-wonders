from card import *

class Player:
    def __init__(self):
        self.board = [] # which board/wonder you have
        self.buildings = [] # cards that have been played
        self.symbols = [] # special symbols
        self.resources = [] # resources
        self.science = [] # science
        self.military = [] # military victories and defeats

        self.cards_by_color = {
            Colors.brown: 0,
            Colors.gray: 0,
            Colors.yellow: 0,
            Colors.red: 0,
            Colors.green: 0,
            Colors.purple: 0,
            Colors.blue: 0
        }

        self.coins = 0
        self.wonder_stages = 0 # stages of wonder built
        self.victory_points = 0

        # references to neighbors
        self.right_neighbor = None
        self.left_neighbor = None

    def _count_players_color(self, players, colors):
        count = 0
        for player in players:
            for color in colors:
                count += player.cards_by_color[color]

        return color

    def calculate_victory_points(self):
        self.victory_points = 0
        self._VP_science()
        self._VP_coins()
        self._VP_symbols()
        self._VP_military()
        self._VP_wonder()

    def _VP_science():
        count = {Science.compass:0, Science.tablet:0, Science.wheel:0}
        
        for sciencetype in self.science:
            count[sciencetype] += 1

        bestscience = max(count, key=lambda x: count[x])

        for x in [symbol for symbol in self.symbols if symbol == Symbols.any_science]:
            count[bestscience]+=1
        
        sciencepoints = sum([count[x]**2 for x in count])
        self.victory_points += sciencepoints

        return sciencepoints

    def _VP_coins():
        coinpoints = int(self.coins/3)
        self.victory_points += coinpoints

        return coinpoints

    def _VP_symbols():
        # TODO: maybe add support for multiple of each symbol?

        symbolpoints = 0

        if Symbols.coins1_VP1_brown_self in self.symbols:
            symbolpoints += self._count_players_color([self.right_neighbor, self.left_neighbor], [Colors.brown])
        if Symbols.coins2_VP2_gray_self in self.symbols:
            symbolpoints += 2*self._count_players_color([self.right_neighbor, self.left_neighbor], [Colors.gray])
        if Symbols.coins1_VP1_yellow_self in self.symbols:
            symbolpoints += self._count_players_color([self.right_neighbor, self.left_neighbor], [Colors.yellow])
        if Symbols.coins3_VP1_red_self in self.symbols:
            symbolpoints += self._count_players_color([self.right_neighbor, self.left_neighbor], [Colors.red])

        if Symbols.VP1_brown_gray_purple_self in self.symbols:
            symbolpoints += self._count_players_color([self], [Colors.brown, Colors.gray, Colors.purple])

        if Symbols.VP1_brown_neighbors in self.symbols:
            symbolpoints += self._count_players_color([self.right_neighbor, self.left_neighbor], [Colors.brown])
        if Symbols.VP1_blue_neighbors in self.symbols:
            symbolpoints += self._count_players_color([self.right_neighbor, self.left_neighbor], [Colors.blue])
        if Symbols.VP1_yellow_neighbors in self.symbols:
            symbolpoints += self._count_players_color([self.right_neighbor, self.left_neighbor], [Colors.yellow])
        if Symbols.VP1_red_neighbors in self.symbols:
            symbolpoints += self._count_players_color([self.right_neighbor, self.left_neighbor], [Colors.red])
        if Symbols.VP1_green_neighbors in self.symbols:
            symbolpoints += self._count_players_color([self.right_neighbor, self.left_neighbor], [Colors.green])
        if Symbols.VP2_gray_neighbors in self.symbols:
            symbolpoints += 2*self._count_players_color([self.right_neighbor, self.left_neighbor], [Colors.gray])

        if Symbols.coins3_VP1_wonder_self in self.symbols:
            symbolpoints += self.wonder_stages
        if Symbols.VP7_wonder_self in self.symbols:
            if self.wonder_stages >= len(self.board): symbolpoints += 7
        if Symbols.VP1_wonder_all in self.symbols:
            symbolpoints += self.wonder_stages + self.right_neighbor.wonder_stages + self.left_neighbor.wonder_stages

        self.victory_points += symbolpoints
        return symbolpoints

    def _VP_military():
        militarypoints = sum(self.military)
        victory_points += militarypoints
        return militarypoints

    def _VP_wonder():
        wonderpoints = 0

        for i in range(self.wonder_stages):
            if "VP" in self.board[i]['reward']: wonderpoints += self.board[i]['reward']["VP"]

        self.victory_points += wonderpoints
        return wonderpoints

