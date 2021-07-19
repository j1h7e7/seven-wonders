from enum import Enum

class Resource(Enum):
    wood =  1
    ore =   2
    brick = 3
    stone = 4

    cloth = 11
    glass = 12
    paper = 13

class ChainIcon(Enum):
    hammer = 1
    water = 2
    altar = 3
    theater = 4
    camel = 5
    lighthouse = 6
    post = 7
    barrel = 8
    horse = 9
    mortar = 10
    bolt = 11
    torch = 12
    target = 13
    lamp = 14
    saw = 15
    planet = 16
    scale = 17
    book = 18
    senate = 19
    scroll = 20
    harp = 21
    feather = 22
    wall = 23
    soldier = 24

class Science(Enum):
    compass = 1
    wheel   = 2
    tablet  = 3

class Colors(Enum):
    brown = 1
    gray = 2
    yellow = 3
    green = 4
    red = 5
    blue = 6
    purple = 7

class Symbols(Enum):
    basic_trade_left = 1
    basic_trade_right = 2
    adv_trade_both = 3

    coins1_brown_all = 4
    coins2_gray_all = 5

    VP1_brown_neighbors = 6
    VP2_gray_neighbors = 7
    VP1_blue_neighbors = 8
    VP1_yellow_neighbors = 9
    VP1_red_neighbors = 10
    VP1_green_neighbors = 11

    VP1_brown_gray_purple_self = 12

    coins1_VP1_brown_self = 13
    coins2_VP2_gray_self = 14
    coins1_VP1_yellow_self = 15
    coins3_VP1_red_self = 16

    coins3_VP1_wonder_self = 17
    VP1_wonder_all = 18
    VP7_wonder_self = 19

    play_last_2 = 20
    play_discard_free = 21
    first_color_free = 22
    first_age_free = 23
    last_age_free = 24

    any_science = 25



class Card:
    def __init__(self, name, color, cost, benefit, chain = []):
        self.name = name
        self.color = color
        self.cost = cost
        self.benefit = benefit
        self.chain = chain

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        return self.name < other.name

    @classmethod
    def card_by_name(self, name):
        # basic resources
        if name == 'Lumber Yard':       return self.base_single_resource(name, Resource.wood)
        if name == 'Ore Vein':          return self.base_single_resource(name, Resource.ore)
        if name == 'Clay Pool':         return self.base_single_resource(name, Resource.brick)
        if name == 'Stone Pit':         return self.base_single_resource(name, Resource.stone)

        # dual resources
        if name == 'Timber Yard':       return self.base_choice_resource(name, [Resource.wood, Resource.stone])
        if name == 'Clay Pit':          return self.base_choice_resource(name, [Resource.brick, Resource.ore])
        if name == 'Excavation':        return self.base_choice_resource(name, [Resource.brick, Resource.stone])
        if name == 'Forest Cave':       return self.base_choice_resource(name, [Resource.wood, Resource.ore])
        if name == 'Tree Farm':         return self.base_choice_resource(name, [Resource.wood, Resource.brick])
        if name == 'Mine':              return self.base_choice_resource(name, [Resource.ore, Resource.stone])

        # double resources
        if name == 'Sawmill':           return self.base_double_resource(name, Resource.wood)
        if name == 'Foundry':           return self.base_double_resource(name, Resource.ore)
        if name == 'Brickyard':         return self.base_double_resource(name, Resource.brick)
        if name == 'Quarry':            return self.base_double_resource(name, Resource.stone)

        # tier 2 resources
        if name == 'Loom':              return self.base_advanced_resource(name, Resource.cloth)
        if name == 'Glassworks':        return self.base_advanced_resource(name, Resource.glass)
        if name == 'Press':             return self.base_advanced_resource(name, Resource.paper)

        # age 1 reds
        if name == 'Stockade':          return self.base_red_card(name, 1, [[Resource.wood]])
        if name == 'Barracks':          return self.base_red_card(name, 1, [[Resource.ore]])
        if name == 'Guard Tower':       return self.base_red_card(name, 1, [[Resource.brick]])

        # age 2 reds
        if name == 'Stables':           return self.base_red_card(name, 2, [[Resource.wood,Resource.brick,Resource.ore], [ChainIcon.horse]])
        if name == 'Archery Range':     return self.base_red_card(name, 2, [[Resource.wood]*2+[Resource.ore], [ChainIcon.target]])
        if name == 'Walls':             return self.base_red_card(name, 2, [[Resource.stone]*3], chain=[ChainIcon.wall])
        if name == 'Training Ground':   return self.base_red_card(name, 2, [[Resource.ore,Resource.ore,Resource.wood]], chain=[ChainIcon.soldier])

        # age 3 reds
        if name == 'Castrum':           return self.base_red_card(name, 3, [[Resource.brick]*2+[Resource.wood,Resource.paper]])
        if name == 'Siege Workshop':    return self.base_red_card(name, 3, [[Resource.brick]*3+[Resource.wood], [ChainIcon.saw]])
        if name == 'Fortifications':    return self.base_red_card(name, 3, [[Resource.ore]*3+[Resource.brick], [ChainIcon.wall]])
        if name == 'Arsenal':           return self.base_red_card(name, 3, [[Resource.ore]*2+[Resource.wood,Resource.cloth]])
        if name == 'Circus':            return self.base_red_card(name, 3, [[Resource.stone]*3+[Resource.ore], [ChainIcon.soldier]])

        # blues
        if name == 'Altar':             return self.base_blue_card(name, 3, [], chain=[ChainIcon.altar])
        if name == 'Baths':             return self.base_blue_card(name, 3, [Resource.stone], chain=[ChainIcon.water])
        if name == 'Theater':           return self.base_blue_card(name, 3, [], chain=[ChainIcon.theater])
        if name == 'Well':              return self.base_blue_card(name, 3, [], chain=[ChainIcon.hammer]) # not sure

        if name == 'Statue':            return self.base_blue_card(name, 4, [[Resource.ore]*2+[Resource.wood], [ChainIcon.hammer]])
        if name == 'Aqueduct':          return self.base_blue_card(name, 5, [[Resource.stone]*3, [ChainIcon.water]])
        if name == 'Courthouse':        return self.base_blue_card(name, 4, [[Resource.brick]*2+[Resource.cloth], [ChainIcon.scale]])
        if name == 'Temple':            return self.base_blue_card(name, 4, [[Resource.wood,Resource.brick,Resource.glass]])

        if name == 'Pantheon':          return self.base_blue_card(name, 7, [[Resource.brick]*2+[Resource.ore,Resource.glass,Resource.paper,Resource.cloth], [ChainIcon.altar]])
        if name == 'Gardens':           return self.base_blue_card(name, 5, [[Resource.brick]*2+[Resource.wood], [ChainIcon.theater]])
        if name == 'Town Hall':         return self.base_blue_card(name, 6, [[Resource.stone]*2+[Resource.ore,Resource.glass]])
        if name == 'Palace':            return self.base_blue_card(name, 8, [[Resource.brick,Resource.stone,Resource.wood,Resource.ore,Resource.paper,Resource.glass,Resource.cloth]])
        if name == 'Senate':            return self.base_blue_card(name, 6, [[Resource.wood]*2+[Resource.stone,Resource.ore], [ChainIcon.senate]])

        # greens
        if name == 'Apothecary':        return self.base_green_card(name, Science.compass, [[Resource.cloth]], chain=[ChainIcon.horse,ChainIcon.mortar])
        if name == 'Workshop':          return self.base_green_card(name, Science.wheel,   [[Resource.glass]], chain=[ChainIcon.target,ChainIcon.lamp])
        if name == 'Scriptorium':       return self.base_green_card(name, Science.tablet,  [[Resource.paper]], chain=[ChainIcon.scale,ChainIcon.book])

        if name == 'Dispensary':        return self.base_green_card(name, Science.compass, [[Resource.ore]*2+[Resource.glass], [ChainIcon.mortar]], chain=[ChainIcon.bolt,ChainIcon.torch])
        if name == 'Laboratory':        return self.base_green_card(name, Science.wheel, [[Resource.brick]*2+[Resource.paper], [ChainIcon.lamp]], chain=[ChainIcon.saw,ChainIcon.planet])
        if name == 'Library':           return self.base_green_card(name, Science.tablet, [[Resource.stone]*2+[Resource.cloth], [ChainIcon.book]], chain=[ChainIcon.senate,ChainIcon.scroll])
        if name == 'School':            return self.base_green_card(name, Science.tablet, [[Resource.wood,Resource.paper]], chain=[ChainIcon.harp,ChainIcon.feather])

        if name == 'Lodge':             return self.base_green_card(name, Science.compass, [[Resource.brick]*2+[Resource.cloth,Resource.paper], [ChainIcon.torch]])
        if name == 'Academy':           return self.base_green_card(name, Science.compass, [[Resource.stone]*3+[Resource.glass], [ChainIcon]])
        if name == 'Observatory':       return self.base_green_card(name, Science.wheel, [[Resource.ore]*2+[Resource.glass,Resource.cloth], [ChainIcon.planet]])
        if name == 'Study':             return self.base_green_card(name, Science.wheel, [[Resource.wood,Resource.paper,Resource.cloth], [ChainIcon.feather]])
        if name == 'University':        return self.base_green_card(name, Science.tablet, [[Resource.wood]*2+[Resource.paper,Resource.glass], [ChainIcon.harp]])

        # yellows
        if name == 'Tavern':            return self(name, Colors.yellow, [], {'coins': 5})

        if name == 'East Trading Post': return self(name, Colors.yellow, [], {'symbol': Symbols.basic_trade_right}, chain=[ChainIcon.post])
        if name == 'West Trading Post': return self(name, Colors.yellow, [], {'symbol': Symbols.basic_trade_left}, chain=[ChainIcon.post])
        if name == 'Marketplace':       return self(name, Colors.yellow, [], {'symbol': Symbols.adv_trade_both}, chain=[ChainIcon.camel])

        if name == 'Vineyard':          return self(name, Colors.yellow, [], {'symbol': Symbols.coins1_brown_all})
        if name == 'Bazar':             return self(name, Colors.yellow, [], {'symbol': Symbols.coins2_gray_all})

        if name == 'Caravansery':       return self(name, Colors.yellow, [[Resource.wood]*2, [ChainIcon.camel]], {'resource': [[Resource.wood,Resource.stone,Resource.brick,Resource.ore]]}, chain=[ChainIcon.lighthouse])
        if name == 'Forum':             return self(name, Colors.yellow, [[Resource.brick]*2, [ChainIcon.post]], {'resource': [[Resource.glass,Resource.paper,Resource.cloth]]}, chain=[ChainIcon.barrel])

        if name == 'Arena':             return self(name, Colors.yellow, [[Resource.stone]*2+[Resource.ore], [ChainIcon.bolt]], {'symbol': Symbols.coins3_VP1_wonder_self})
        if name == 'Lighthouse':        return self(name, Colors.yellow, [[Resource.stone,Resource.glass], [ChainIcon.lighthouse]], {'symbol': Symbols.coins1_VP1_yellow_self})
        if name == 'Haven':             return self(name, Colors.yellow, [[Resource.wood,Resource.ore,Resource.cloth], [ChainIcon.barrel]], {'symbol': Symbols.coins1_VP1_yellow_self})
        if name == 'Chamber of Commerce': return self(name,Colors.yellow,[[Resource.brick]*2+[Resource.cloth]], {'symbol': Symbols.coins2_VP2_gray_self})
        if name == 'Ludus':             return self(name, Colors.yellow, [[Resource.stone,Resource.ore]], {'symbol': Symbols.coins3_VP1_red_self})

        # purples
        if name == 'Workers Guild':      return self.base_purple_card(name, Symbols.VP1_brown_neighbors, [Resource.ore]*2+[Resource.brick,Resource.stone,Resource.wood])
        if name == 'Craftsmens Guild':   return self.base_purple_card(name, Symbols.VP2_gray_neighbors, [Resource.ore,Resource.stone]*2)
        if name == 'Shipowners Guild':   return self.base_purple_card(name, Symbols.VP1_brown_gray_purple_self, [Resource.wood]*3+[Resource.glass,Resource.paper])
        if name == 'Traders Guild':      return self.base_purple_card(name, Symbols.VP1_yellow_neighbors, [Resource.glass,Resource.cloth,Resource.paper])
        if name == 'Magistrates Guild':  return self.base_purple_card(name, Symbols.VP1_blue_neighbors, [Resource.wood]*3+[Resource.stone,Resource.cloth])
        if name == 'Builders Guild':     return self.base_purple_card(name, Symbols.VP1_wonder_all, [Resource.stone]*3+[Resource.wood]*2+[Resource.glass])
        if name == 'Philosophers Guild': return self.base_purple_card(name, Symbols.VP1_green_neighbors, [Resource.brick]*3+[Resource.cloth,Resource.paper])
        if name == 'Scientists Guild':   return self.base_purple_card(name, Symbols.any_science, [Resource.wood,Resource.ore]*2+[Resource.paper])
        if name == 'Spies Guild':        return self.base_purple_card(name, Symbols.VP1_red_neighbors, [Resource.brick]*2+[Resource.glass])
        if name == 'Decorators Guild':   return self.base_purple_card(name, Symbols.VP7_wonder_self, [Resource.ore]*2+[Resource.stone,Resource.cloth])

        #raise KeyError('No card with name "'+name+'" was found.')
        print(name)


    @classmethod
    def base_single_resource(self, name, resource):
        return self(name, Colors.brown, [], {'resource': [[resource]]})

    @classmethod
    def base_choice_resource(self, name, resources):
        return self(name, Colors.brown, [{'coins':1}], {'resource': [resources]})

    @classmethod
    def base_double_resource(self, name, resource):
        return self(name, Colors.brown, [{'coins':1}], {'resource': [[resource],[resource]]})
    
    @classmethod
    def base_advanced_resource(self, name, resource):
        return self(name, Colors.gray, [], {'resource': [[resource]]})

    @classmethod
    def base_red_card(self, name, swords, requirements, chain = []):
        return self(name, Colors.red, requirements, {'swords': swords}, chain)

    @classmethod
    def base_green_card(self, name, sciencetype, requirements, chain = []):
        return self(name, Colors.green, requirements, {'science': sciencetype}, chain)

    @classmethod
    def base_blue_card(self, name, points, requirements, chain = []):
        return self(name, Colors.blue, requirements, {'points': points}, chain)

    @classmethod
    def base_purple_card(self, name, symbol, cost):
        return self(name, Colors.purple, [cost], {'symbol': symbol})



class Deck:
    def __init__(self):
        self.cards_3_age1 = [
            'Lumber Yard','Stone Pit','Clay Pool','Ore Vein','Clay Pit','Timber Yard','Glassworks','Press','Loom','Baths','Altar','Theater',
            'Marketplace','West Trading Post','East Trading Post','Stockade','Barracks','Guard Tower','Apothecary','Workshop','Scriptorium'
        ]
        self.cards_4_age1 = ['Lumber Yard','Ore Vein','Excavation','Well','Tavern','Guard Tower','Scriptorium']
        self.cards_5_age1 = ['Stone Pit','Clay Pool','Forest Cave','Altar','Tavern','Barracks','Apothecary']
        self.cards_6_age1 = ['Tree Farm','Mine','Glassworks','Press','Loom','Theater','Marketplace']
        self.cards_7_age1 = ['Well','Baths','Tavern','West Trading Post','East Trading Post','Stockade','Workshop']

        self.cards_3_age2 = [
            'Sawmill','Quarry','Brickyard','Foundry','Glassworks','Press','Loom','Statue','Aqueduct','Temple','Courthouse','Caravansery',
            'Forum','Vineyard','Stables','Archery Range','Walls','Dispensary','Laboratory','Library','School'
        ]
        self.cards_4_age2 = ['Sawmill','Quarry','Brickyard','Foundry','Bazar','Training Ground','Dispensary']
        self.cards_5_age2 = ['Glassworks','Press','Loom','Courthouse','Caravansery','Stables','Laboratory']
        self.cards_6_age2 = ['Temple','Caravansery','Forum','Vineyard','Archery Range','Training Ground','Library']
        self.cards_7_age2 = ['Statue','Aqueduct','Forum','Bazar','Walls','Training Ground','School']

        self.cards_3_age3 = [
            'Pantheon','Gardens','Town Hall','Palace','Senate','Lighthouse','Haven','Arena','Fortifications','Arsenal','Siege Workshop','Lodge',
            'Academy','Observatory','Study','University','Workers Guild','Craftsmens Guild','Magistrates Guild','Traders Guild','Builders Guild',
            'Spies Guild','Philosophers Guild','Decorators Guild','Scientists Guild','Shipowners Guild'
        ]
        self.cards_4_age3 = ['Gardens','Haven','Chamber of Commerce','Castrum','Circus','University']
        self.cards_5_age3 = ['Senate','Ludus','Arena','Arsenal','Siege Workshop','Study']
        self.cards_6_age3 = ['Pantheon','Town Hall','Lighthouse','Chamber of Commerce','Circus','Lodge']
        self.cards_7_age3 = ['Palace','Ludus','Castrum','Fortifications','Academy','Observatory']

    def get_deck(self, players, age):
        deck = []

        if age is 1:
            if players >= 3: deck.extend([Card.card_by_name(cardname) for cardname in self.cards_3_age1])
            if players >= 4: deck.extend([Card.card_by_name(cardname) for cardname in self.cards_4_age1])
            if players >= 5: deck.extend([Card.card_by_name(cardname) for cardname in self.cards_5_age1])
            if players >= 6: deck.extend([Card.card_by_name(cardname) for cardname in self.cards_6_age1])
            if players >= 7: deck.extend([Card.card_by_name(cardname) for cardname in self.cards_7_age1])

        if age is 2:
            if players >= 3: deck.extend([Card.card_by_name(cardname) for cardname in self.cards_3_age2])
            if players >= 4: deck.extend([Card.card_by_name(cardname) for cardname in self.cards_4_age2])
            if players >= 5: deck.extend([Card.card_by_name(cardname) for cardname in self.cards_5_age2])
            if players >= 6: deck.extend([Card.card_by_name(cardname) for cardname in self.cards_6_age2])
            if players >= 7: deck.extend([Card.card_by_name(cardname) for cardname in self.cards_7_age2])

        if age is 3:
            if players >= 3: deck.extend([Card.card_by_name(cardname) for cardname in self.cards_3_age3])
            if players >= 4: deck.extend([Card.card_by_name(cardname) for cardname in self.cards_4_age3])
            if players >= 5: deck.extend([Card.card_by_name(cardname) for cardname in self.cards_5_age3])
            if players >= 6: deck.extend([Card.card_by_name(cardname) for cardname in self.cards_6_age3])
            if players >= 7: deck.extend([Card.card_by_name(cardname) for cardname in self.cards_7_age3])

        return sorted(deck)


class Boards:
    def __init__(self):
        self.base_board = {'starting': Resource.wood, 'wonder': [
            {'cost': [Resource.stone]*2, 'reward': {'VP':3}},
            {'cost': [Resource.brick]*3, 'reward': {'VP':5}},
            {'cost': [Resource.ore]*4, 'reward': {'VP':7}}
        ]}

        self.example_board = {'starting': Resource.paper, 'wonder': [
            {'cost': [Resource.wood,Resource.brick], 'reward': {'VP':1,'coins':3}},
            {'cost': [Resource.glass,Resource.stone,Resource.ore], 'reward': {'symbol':Symbols.play_discard_free}},
            {'cost': [Resource.cloth]*3, 'reward': {'swords':3}}
        ]}


if __name__ == "__main__":
    dealer = Deck()

    for age in [1,2,3]:
        print('Age',age)
        for players in [3,4,5,6,7]:
            deck = dealer.get_deck(players, age)
            print('Players:',players,'| Expected:',players*7,'| Actual:',len(deck),'| Error:',players*7-len(deck))