from card import *
from game import *
from player import Player
import numpy

actions = ['sell', 'build', 'Arsenal', 'Craftsmens Guild', 'Altar', 'Sawmill', 'Glassworks', 'East Trading Post', 'Well', 'Traders Guild', 'Marketplace', 'Mine', 'Press', 'Scientists Guild', 'School', 'Lodge', 'Dispensary', 'Fortifications', 'Baths', 'Caravansery', 'Foundry', 'Ludus', 'Decorators Guild', 'Barracks', 'Statue', 'Lighthouse', 'Clay Pool', 'Brickyard', 'Stockade', 'Walls', 'Scriptorium', 'Forum', 'Clay Pit', 'Library', 'Excavation', 'Stables', 'Archery Range', 'Philosophers Guild', 'Siege Workshop', 'Palace', 'Ore Vein', 'Chamber of Commerce', 'Workshop', 'Lumber Yard', 'Guard Tower', 'Spies Guild', 'Arena', 'Study', 'Training Ground', 'Pantheon', 'Builders Guild', 'Forest Cave', 'Courthouse', 'Academy', 'Theater', 'Magistrates Guild', 'Workers Guild', 'Shipowners Guild', 'University', 'Tavern', 'Observatory', 'Tree Farm', 'Circus', 'Vineyard', 'Aqueduct', 'Temple', 'Town Hall', 'Bazar', 'Haven', 'Laboratory', 'Stone Pit', 'Senate', 'Gardens', 'Apothecary', 'Loom', 'Quarry', 'Castrum', 'Timber Yard', 'West Trading Post']


class Game():
    """
    Game wrapper.
    """

    def __init__(self, seed=None):
        self.env = Seven_Wonders(seed)

    def step(self, action):
        """
        Apply action to the game.
        Args:
            action : action of the action_space to take.
        Returns:
            The new observation, the reward and a boolean if the game has ended.
        """
        observation, reward, done = self.env.step(action)
        return observation, reward, done

    def to_play(self):
        """
        Return the current player.
        Returns:
            The current player, it should be an element of the players list in the config.
        """
        return self.env.to_play()

    def legal_actions(self):
        """
        Should return the legal actions at each turn, if it is not available, it can return
        the whole action space. At each turn, the game have to be able to handle one of returned actions.
        For complex game where calculating legal moves is too long, the idea is to define the legal actions
        equal to the action space but to return a negative reward if the action is illegal.
        Returns:
            An array of integers, subset of the action space.
        """
        return self.env.legal_actions()

    def reset(self):
        """
        Reset the game for a new game.
        Returns:
            Initial observation of the game.
        """
        return self.env.reset()

    def render(self):
        """
        Display the game observation.
        """
        self.env.render()
        input("Press enter to take a step ")

    def human_to_action(self):
        """
        For multiplayer games, ask the user for a legal action
        and return the corresponding action number.
        Returns:
            An integer from the action space.
        """
        choice = input(
            f"Enter an action for player: {self.to_play()}: "
        )
        while choice not in [str(action) for action in self.legal_actions()]:
            choice = input("Enter an action: ")
        return int(choice)

    def action_to_string(self, action_number):
        """
        Convert an action number to a string representing the action.
        Args:
            action_number: an integer from the action space.
        Returns:
            String representing the action.
        """
        return f"{action_number}. {actions[action_number]}"

    def expert_agent(self):
        """
        Hard coded agent that MuZero faces to assess his progress in multiplayer games.
        It doesn't influence training
        Returns:
            Action as an integer to take in the current game state
        """
        return self.env.random_action()

##############################################################################################################
# TODO: make function that takes array of card names and returns equivalent array of the number representation of the cards and vise versa

def cards_to_actions(cards):
    actions = []
    for card in cards:
        actions.append(cards.index(card.name))
    return actions

class Seven_Wonders:
    def __init__(self, seed):
        self.random = numpy.random.RandomState(seed)
        self.current_player = 0
        self.num_players = 7
        self.dealer = Deck()
        self.boards = Boards()
        self.hands = []
        self.players = []
        self.current_age = 1
        self.direction = -1
        self.turn_num = 0
        for i in range(self.num_players):
            self.players.append(Player())

        # assign neighbors
        for i in range(self.num_players):
            self.players[i].left_neighbor =  self.players[(i-1) % self.num_players]
            self.players[i].right_neighbor = self.players[(i+1) % self.num_players]

        # assign boards
        # for now we just give everyone the boring board
        for player in self.players:
            player.board = self.boards.base_board['wonder']
            player.resources = [[self.boards.base_board['starting']]]

    def step(self, action):
        observation = []
        reward = 0

        # setup action queue
        action_queue = {}
        for i in range(self.num_players):
            action_queue[i] = []

        # puts action into queue

        # either selling or building
        if action == 0 or action == 1:
            card_played = actions[action]
        else:
            for card in self.get_player_hand(self.current_player):
                if card.name == actions[action]:
                    card_played = card
        action_queue[self.current_player] = card_played

        # swap players
        # if at the end of the players, play the turn
        self.current_player += 1
        if self.current_player > self.num_players:
            self.current_player = 0
            self.play_turn(action_queue)
        
        # see if end of age
        self.turn_num += 1
        if self.turn_num == 6:
            done = self.new_age()
            if done:
                reward = self.players[self.current_player].calculate_victory_points()

        # do observation space
        observation = self.do_observation()

        """
        Apply action to the game.
        Args:
            action : action of the action_space to take.
        Returns:
            The new observation, the reward and a boolean if the game has ended.
        """

        # put the action into a queue
        # swap players
        # if at the end of the players, do all actions in action queue
        # see if end of age
        # if end of age, do military stuff, deal new hands, ect
        # if end of game, calc wins
        
        observation, reward, done = self.env.step(action)
        return observation, reward, done

    # obersvation: [
        # [other board, coins]
        # [other board, coins]
        # [other board, coins]
        # [other board, coins]
        # [other board, coins]
        # [other board, coins]
        # [your hand]
        # [your board, coins]
    # ]
    def do_observation(self):
        observation = []
        your_hand = []
        your_board = []
        for i in range(self.num_players):
            to_append = []
            # for other players
            if not i == self.current_player:
                to_append.append(cards_to_actions(self.get_player_hand(i)))
                to_append.append(self.players[i].coins)
            # for you
            else:
                your_hand = self.get_player_hand(i)
                your_board.append(cards_to_actions(self.players[i].buildings))
                your_board.append(self.players[i].coins)
        observation.append(your_hand)
        observation.append(your_board)
        return observation

    def get_player_hand(self, index):
        return self.hands[(index+self.turnnum*self.direction) % self.numplayers]

    def do_military(self, agenum):
        for i in range(self.numplayers):
            for direction in [-1,+1]:
                if self.players[i].swords < self.players[(i+direction) % self.numplayers].swords:
                    self.players[i].military.append(-1)
                if self.players[i].swords > self.players[(i+direction) % self.numplayers].swords:
                    self.players[i].military.append(agenum*2-1)

    def play_turn(self, action_queue):
        for i in range(self.numplayers):
            # if chose to sell or build, deal with that
            if action_queue[i] == "sell" or action_queue[i] == "build":
                card = self.random.choice(self.get_player_hand(i))
                if action_queue[i] == "sell":
                    self.players[i].sell_card(card)
                elif action_queue[i] == "build":
                    self.players[i].build_wonder(card)
                action_queue[i] = card
            # call play_card if that
            else:
                self.players[i].play_card(action_queue[i])
            # delete card from hand
            self.get_player_hand(i).remove(action_queue[i])

        for player in self.players:
            player.resolve_effect()

    # returns true of game is ended
    def new_age(self, agenum):
        deck = self.dealer.get_deck(self.numplayers, agenum)
        self.hands = [[] for _ in range(self.numplayers)]
        self.random.shuffle(deck)

        for hand in self.hands:
            for i in range(7): hand.append(deck.pop())

        self.direction = (1 if agenum == 2 else -1)

        if not agenum == 1:
            self.do_military(agenum)

        agenum += 1
        return agenum == 4

    def to_play(self):
        """
        Return the current player.
        Returns:
            The current player, it should be an element of the players list in the config.
        """
        return self.current_player

    def legal_actions(self):
        """
        Should return the legal actions at each turn, if it is not available, it can return
        the whole action space. At each turn, the game have to be able to handle one of returned actions.
        For complex game where calculating legal moves is too long, the idea is to define the legal actions
        equal to the action space but to return a negative reward if the action is illegal.
        Returns:
            An array of integers, subset of the action space.
        """
        # look at current player's hand
        # call can_play on all of the cards
        # put all cards (number representations) in which true is returned into an array and return it
        # sell card
        # can build wonder
        legalactions = [0]
        for card in self.get_player_hand(self.current_player):
            if self.players[self.current_player].can_play_card(card):
                legalactions.append(actions.index(card.name))
        if self.players[self.current_player].can_upgrade_wonder():
            legalactions.append(1)

        return legalactions

    def reset(self):
        """
        Reset the game for a new game.
        Returns:
            Initial observation of the game.
        """
        self.__init__()
        return self.do_observation()