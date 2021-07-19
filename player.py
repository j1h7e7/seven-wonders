from card import *
import itertools, copy
from collections import Counter

def issubset(x, y): # is x a subset of y
    return not Counter(x)-Counter(y)

class Player:
    def __init__(self):
        self.board = [] # which board/wonder you have
        self.buildings = [] # cards that have been played
        self.symbols = [] # special symbols
        self.resources = [] # resources
        self.chains = [] # chain icons
        self.science = [] # science
        self.military = [] # military victories and defeats
        self.blues = [] # blue card points

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
        self.swords = 0 # number of swords (on red cards)
        self.wonder_stages = 0 # stages of wonder built
        self.victory_points = 0

        # references to neighbors
        self.right_neighbor = None
        self.left_neighbor = None

        # card stuff for resolution
        self.effect_to_resolve = None

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
        self._VP_blues()
        return self.victory_points

    def _VP_science(self):
        count = {Science.compass:0, Science.tablet:0, Science.wheel:0}
        
        for sciencetype in self.science:
            count[sciencetype] += 1

        bestscience = max(count, key=lambda x: count[x])

        for x in [symbol for symbol in self.symbols if symbol == Symbols.any_science]:
            count[bestscience]+=1
        
        sciencepoints = sum([count[x]**2 for x in count])
        self.victory_points += sciencepoints

        return sciencepoints

    def _VP_coins(self):
        coinpoints = int(self.coins/3)
        self.victory_points += coinpoints

        return coinpoints

    def _VP_symbols(self):
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

    def _VP_military(self):
        militarypoints = sum(self.military)
        victory_points += militarypoints
        return militarypoints

    def _VP_wonder(self):
        wonderpoints = 0

        for i in range(self.wonder_stages):
            if "VP" in self.board[i]['reward']: wonderpoints += self.board[i]['reward']["VP"]

        self.victory_points += wonderpoints
        return wonderpoints

    def _VP_blues(self):
        bluepoints = sum(self.blues)
        self.victory_points += bluepoints
        return bluepoints


    def can_play_free(self, cost):  # can we play it without buying from other players
        costoptions = copy.deepcopy(cost) # duplicates so we can fiddle with it
        if len(costoptions) == 0: return True

        for option in costoptions:
            # first check coins:
            if "coins" in option:
                if self.coins >= option['coins']: return True
                else: continue

            # then check chains
            if isinstance(option[0], ChainIcon):
                if option[0] in self.chains: return True
                else: continue

            resourcesleft = [x for x in self.resources]
            # first removes the things we can do 1:1
            for ingredient in [x for x in option]: # have to make a copy so we can delete elements
                if [ingredient] in resourcesleft:
                    resourcesleft.remove([ingredient])
                    option.remove(ingredient)

            if len(option) == 0: return True # if we easily satisfied everything

            if len(option) > len(resourcesleft): return False # easy fast check

            choiceresources = [x for x in resourcesleft if len(x)>1] # choice stuff
            permutations = [x for x in itertools.product(*choiceresources)] # for some reason need to generate this out

            if any(map(lambda x: issubset(option,x), permutations)): return True # wonky subset stuff

            # no idea how to do this for buying stuff lol
            # maybe either minimizing the ingredients left or minimizing the cost

        return False

    def can_play_help(self, cost):  # can we play it with help from neighbors
        # assume that we have already checked if we can play it for free
        if self.can_play_free(cost): return [0,0]

        costoptions = copy.deepcopy(cost) # duplicates so we can fiddle with it

        mincost = 100
        price = [0,0]   # amount to left, right neighbor

        for option in costoptions:
            # ignore if coins/chain:
            if "coins" in option: continue
            if isinstance(option[0], ChainIcon): continue

            resourcesleft = [x for x in self.resources]
            # first removes the things we can do 1:1
            for ingredient in [x for x in option]: # have to make a copy so we can delete elements
                if [ingredient] in resourcesleft:
                    resourcesleft.remove([ingredient])
                    option.remove(ingredient)

            choiceresources = [x for x in resourcesleft if len(x)>1] # choice stuff
            leftresources = [x+[None] for x in self.left_neighbor.resources]
            rightresources = [x+[None] for x in self.right_neighbor.resources]

            selfpermutations = [x for x in itertools.product(*choiceresources)] # for some reason need to generate this out
            leftpermutations = [x for x in itertools.product(*leftresources)]
            rightpermutations = [x for x in itertools.product(*rightresources)]

            for allocation1 in selfpermutations:
                for allocation2 in leftpermutations:
                    for allocation3 in rightpermutations:
                        if not issubset(option, allocation1+allocation2+allocation3): continue # doesn't meet requirements

                        L_T1 = len([x for x in allocation2 if x in Resources_T1])
                        L_T2 = len([x for x in allocation2 if x in Resources_T2])
                        R_T1 = len([x for x in allocation3 if x in Resources_T1])
                        R_T2 = len([x for x in allocation3 if x in Resources_T2])

                        leftprice = L_T1 * (1 if Symbols.basic_trade_left in self.symbols else 2) + \
                                    L_T2 * (1 if Symbols.adv_trade_both in self.symbols else 2)
                        rightprice = R_T1 * (1 if Symbols.basic_trade_right in self.symbols else 2) + \
                                     R_T2 * (1 if Symbols.adv_trade_both in self.symbols else 2)

                        if leftprice+rightprice < mincost:
                            mincost = leftprice+rightprice
                            price = [leftprice, rightprice]

                     
        if mincost < 100: return price

        return False
            

    def play_card(self, card):
        self.buildings.append(card.name)
        self.cards_by_color[card.color] += 1
        self.chains.extend(card.chain)

        self.effect_to_resolve = card.benefit

    def resolve_effect(self):
        effect = self.effect_to_resolve

        if 'resource' in effect:
            self.resources.extend(effect['resource'])
        if 'science' in effect:
            self.science[effect['science']] += 1
        if 'swords' in effect:
            self.swords += effect['swords']
        if 'points' in effect:
            self.blues.append(effect['points'])
        if 'coins' in effect:
            self.coins += effect['coins']
        if 'VP' in effect:
            pass # wonder VP, counted at the end
        
        symbol = ""
        if 'symbol' in effect:
            symbol = effect['symbol']
            self.symbols.append(symbol)

        if symbol == Symbols.coins1_brown_all:
            self.coins += self._count_players_color([self,self.right_neighbor,self.left_neighbor], Colors.brown)
        if symbol == Symbols.coins2_gray_all:
            self.coins += 2*self._count_players_color([self,self.right_neighbor,self.left_neighbor], Colors.gray)

        if symbol == Symbols.coins1_VP1_brown_self:
            self.coins += self._count_players_color([self], Colors.brown)
        if symbol == Symbols.coins1_VP1_yellow_self:
            self.coins += self._count_players_color([self], Colors.yellow)
        if symbol == Symbol.coins2_VP2_gray_self:
            self.coins += 2*self._count_players_color([self], Colors.gray)
        if symbol == Symbol.coins3_VP1_red_self:
            self.coins += 3*self._count_players_color([self], Colors.red)
        if symbol == Symbol.coins3_VP1_wonder_self:
            self.coins += 3*self.wonder_stages

        # TODO: all this stuff:
        if symbol == Symbols.play_discard_free:
            print('NYI sorry')
        

def solo_tests():
    print("Starting solo tests")
    player = Player()
    
    # test 1
    player.resources = [[Resource.stone],[Resource.wood]]
    assert player.can_play_free([[Resource.stone,Resource.wood]]) == True
    assert player.can_play_free([[Resource.stone,Resource.wood]]) == True
    assert player.can_play_free([[Resource.stone]]) == True
    assert player.can_play_free([[Resource.stone,Resource.stone]]) == False
    assert player.can_play_free([[Resource.ore]]) == False
    assert player.can_play_free([[Resource.ore],[Resource.wood]]) == True
    print("Basic tests passed")

    # test 2
    player.resources = [[Resource.stone,Resource.wood],[Resource.wood,Resource.ore]]
    assert player.can_play_free([[Resource.stone,Resource.ore]]) == True
    assert player.can_play_free([[Resource.stone,Resource.wood]]) == True
    assert player.can_play_free([[Resource.wood,Resource.ore]]) == True
    assert player.can_play_free([[Resource.stone,Resource.stone]]) == False
    print("Choice tests passed")

    # test 3
    player.resources = []
    player.coins = 1
    player.chains = [ChainIcon.camel]
    assert player.can_play_free([{"coins":1}]) == True
    assert player.can_play_free([{"coins":1},[Resource.wood]]) == True
    assert player.can_play_free([{"coins":2}]) == False
    assert player.can_play_free([[ChainIcon.camel]]) == True
    assert player.can_play_free([[ChainIcon.torch]]) == False
    print("Special tests passed")

    print("All solo tests passed")

def multiplayer_tests():
    print("Starting multiplayer tests")
    player = Player()
    left = Player()
    right = Player()
    player.left_neighbor = left
    player.right_neighbor = right

    # test 1
    player.resources = []
    left.resources = [[Resource.stone]]
    right.resources = [[Resource.wood]]
    assert player.can_play_help([[Resource.stone]]) == [2,0]
    assert player.can_play_help([[Resource.wood]]) == [0,2]
    assert player.can_play_help([[Resource.stone,Resource.wood]]) == [2,2]
    assert player.can_play_help([[Resource.ore]]) == False
    print("Basic tests passed")

    # test 2
    player.resources = []
    left.resources = [[Resource.stone]]
    right.resources = [[Resource.stone,Resource.wood]]
    player.symbols = [Symbols.basic_trade_left]
    assert player.can_play_help([[Resource.stone]]) == [1,0]
    assert player.can_play_help([[Resource.stone,Resource.stone]]) == [1,2]
    assert player.can_play_help([[Resource.wood]]) == [0,2]
    print("Cost tests passed")

    print("All multiplayer tests passed")

if __name__ == "__main__":
    solo_tests()
    print()
    multiplayer_tests()


