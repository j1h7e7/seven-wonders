from card import *
from game import *
from player import Player
import numpy
import datetime
import os
import numpy
import torch
from .abstract_game import AbstractGame
import random

actions = ['sell', 'build', 'Arsenal', 'Craftsmens Guild', 'Altar', 'Sawmill', 'Glassworks', 'East Trading Post', 'Well', 'Traders Guild', 'Marketplace', 'Mine', 'Press', 'Scientists Guild', 'School', 'Lodge', 'Dispensary', 'Fortifications', 'Baths', 'Caravansery', 'Foundry', 'Ludus', 'Decorators Guild', 'Barracks', 'Statue', 'Lighthouse', 'Clay Pool', 'Brickyard', 'Stockade', 'Walls', 'Scriptorium', 'Forum', 'Clay Pit', 'Library', 'Excavation', 'Stables', 'Archery Range', 'Philosophers Guild', 'Siege Workshop', 'Palace', 'Ore Vein', 'Chamber of Commerce', 'Workshop', 'Lumber Yard', 'Guard Tower', 'Spies Guild', 'Arena', 'Study', 'Training Ground', 'Pantheon', 'Builders Guild', 'Forest Cave', 'Courthouse', 'Academy', 'Theater', 'Magistrates Guild', 'Workers Guild', 'Shipowners Guild', 'University', 'Tavern', 'Observatory', 'Tree Farm', 'Circus', 'Vineyard', 'Aqueduct', 'Temple', 'Town Hall', 'Bazar', 'Haven', 'Laboratory', 'Stone Pit', 'Senate', 'Gardens', 'Apothecary', 'Loom', 'Quarry', 'Castrum', 'Timber Yard', 'West Trading Post']

class MuZeroConfig:
    def __init__(self):
        # More information is available here: https://github.com/werner-duvaud/muzero-general/wiki/Hyperparameter-Optimization

        self.seed = 0  # Seed for numpy, torch and the game
        self.max_num_gpus = None  # Fix the maximum number of GPUs to use. It's usually faster to use a single GPU (set it to 1) if it has enough memory. None will use every GPUs available

        ### Game
        self.observation_shape = (1, 5, len(actions)+1)  # Dimensions of the game observation, must be 3D (channel, height, width). For a 1D array, please reshape it to (1, 1, length of array)
        self.action_space = list(range(len(actions)))  # Fixed list of all possible actions. You should only edit the length
        self.players = list(range(2))  # List of players. You should only edit the length
        self.stacked_observations = 0  # Number of previous observations and previous actions to add to the current observation

        # Evaluate
        self.muzero_player = 0  # Turn Muzero begins to play (0: MuZero plays first, 1: MuZero plays second)
        self.opponent = 'random'  # Hard coded agent that MuZero faces to assess his progress in multiplayer games. It doesn't influence training. None, "random" or "expert" if implemented in the Game class

        ### Self-Play
        self.num_workers = 2  # Number of simultaneous threads/workers self-playing to feed the replay buffer
        self.selfplay_on_gpu = False
        self.max_moves = 500  # Maximum number of moves if game is not finished before
        self.num_simulations = 40  # Number of future moves self-simulated
        self.discount = 0.9746306992907622  # Chronological discount of the reward
        self.temperature_threshold = None  # Number of moves before dropping the temperature given by visit_softmax_temperature_fn to 0 (ie selecting the best action). If None, visit_softmax_temperature_fn is used every time

        # Root prior exploration noise
        self.root_dirichlet_alpha = 0.3
        self.root_exploration_fraction = 0.25

        # UCB formula
        self.pb_c_base = 19652
        self.pb_c_init = 1.25

        ### Network
        self.network = "resnet"  # "resnet" / "fullyconnected"
        self.support_size = 10  # Value and reward are scaled (with almost sqrt) and encoded on a vector with a range of -support_size to support_size. Choose it so that support_size <= sqrt(max(abs(discounted reward)))

        # Residual Network
        self.downsample = False  # Downsample observations before representation network, False / "CNN" (lighter) / "resnet" (See paper appendix Network Architecture)
        self.blocks = 2  # Number of blocks in the ResNet
        self.channels = 32  # Number of channels in the ResNet
        self.reduced_channels_reward = 32  # Number of channels in reward head
        self.reduced_channels_value = 32  # Number of channels in value head
        self.reduced_channels_policy = 32  # Number of channels in policy head
        self.resnet_fc_reward_layers = [16]  # Define the hidden layers in the reward head of the dynamic network
        self.resnet_fc_value_layers = [16]  # Define the hidden layers in the value head of the prediction network
        self.resnet_fc_policy_layers = [16]  # Define the hidden layers in the policy head of the prediction network

        # Fully Connected Network
        self.encoding_size = 32
        self.fc_representation_layers = [16]  # Define the hidden layers in the representation network
        self.fc_dynamics_layers = [16]  # Define the hidden layers in the dynamics network
        self.fc_reward_layers = [16]  # Define the hidden layers in the reward network
        self.fc_value_layers = [16]  # Define the hidden layers in the value network
        self.fc_policy_layers = [16]  # Define the hidden layers in the policy network

        ### Training
        self.results_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../results",
                                         os.path.basename(__file__)[:-3], datetime.datetime.now().strftime(
                "%Y-%m-%d--%H-%M-%S"))  # Path to store the model weights and TensorBoard logs
        self.save_model = True  # Save the checkpoint in results_path as model.checkpoint
        self.training_steps = 100000  # Total number of training steps (ie weights update according to a batch)
        self.batch_size = 5  # Number of parts of games to train on at each training step
        self.checkpoint_interval = 50  # Number of training steps before using the model for self-playing
        self.value_loss_weight = 1  # Scale the value loss to avoid overfitting of the value function, paper recommends 0.25 (See paper appendix Reanalyze)
        self.train_on_gpu = True if torch.cuda.is_available() else False  # Train on GPU if available

        self.optimizer = "Adam"  # "Adam" or "SGD". Paper uses SGD
        self.weight_decay = 1e-4  # L2 weights regularization
        self.momentum = 0.9  # Used only if optimizer is SGD

        # Exponential learning rate schedule
        self.lr_init = 0.0031622776601683772  # Initial learning rate
        self.lr_decay_rate = 0.9  # Set it to 1 to use a constant learning rate
        self.lr_decay_steps = 10000

        ### Replay Buffer
        self.replay_buffer_size = 1000  # Number of self-play games to keep in the replay buffer
        self.num_unroll_steps = 121  # Number of game moves to keep for every batch element
        self.td_steps = 121  # Number of steps in the future to take into account for calculating the target value
        self.PER = True  # Prioritized Replay (See paper appendix Training), select in priority the elements in the replay buffer which are unexpected for the network
        self.PER_alpha = 0.5  # How much prioritization is used, 0 corresponding to the uniform case, paper suggests 1

        # Reanalyze (See paper appendix Reanalyse)
        self.use_last_model_value = False  # Use the last model to provide a fresher, stable n-step value (See paper appendix Reanalyze)
        self.reanalyse_device = "cpu"  # "cpu" / "cuda"
        self.reanalyse_num_gpus = 0  # Number of GPUs to use for the reanalyse, it can be fractional, don't fortget to take the train worker and the selfplay workers into account

        # Reanalyze (See paper appendix Reanalyse)
        self.use_last_model_value = True  # Use the last model to provide a fresher, stable n-step value (See paper appendix Reanalyze)
        self.reanalyse_on_gpu = False

        ### Adjust the self play / training ratio to avoid over/underfitting
        self.self_play_delay = 0  # Number of seconds to wait after each played game
        self.training_delay = 0  # Number of seconds to wait after each training step
        self.ratio = 1  # Desired training steps per self played step ratio. Equivalent to a synchronous version, training can take much longer. Set it to None to disable it

    def visit_softmax_temperature_fn(self, trained_steps):
        """
        Parameter to alter the visit count distribution to ensure that the action selection becomes greedier as training progresses.
        The smaller it is, the more likely the best action (ie with the highest visit count) is chosen.
        Returns:
            Positive float.
        """
        if trained_steps < 0.5 * self.training_steps:
            return 1.0
        elif trained_steps < 0.75 * self.training_steps:
            return 0.5
        else:
            return 0.25


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
            f"Enter an action for player: {self.to_play()}; their possible actions are: {actions_to_card_names(self.legal_actions)}, which are represented as: {self.legal_actions}"
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

def actions_to_card_names(actions_given):
    cards = []
    for action in actions_given:
        cards.append(actions[action])
    return cards

def names_of_cards_to_actions(cards):
    possilbe_actions = []
    for card in cards:
        possilbe_actions.append(actions.index(card))
    return possilbe_actions

def create_observation_space(buildings):
    observation = numpy.zeros(len(actions))
    for i in range(len(buildings)):
        observation[i] = buildings[i]
    return numpy.ndarray.tolist(observation)

class Seven_Wonders:
    def __init__(self, seed):
        self.seed = seed
        self.random = numpy.random.RandomState(seed)
        self.current_player = 0
        self.num_players = 5
        self.dealer = Deck()
        self.boards = Boards()
        self.hands = []
        self.players = []
        self.current_age = 0
        self.setting_up = True
        self.direction = -1
        self.turn_num = 0
        self.action_queue = {}
        self.done = False
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

        deck = self.dealer.get_deck(self.num_players, self.current_age)
        self.hands = [[] for _ in range(self.num_players)]
        self.random.shuffle(deck)

        self.new_age()

    def step(self, action):
        observation = []
        reward = 0
        done = False

        if self.done:
            self.current_player = 1
            self.turn_num = 6
            done = True
        else:
            # puts action into queue
            self.action_queue[self.current_player] = self.get_card_from_action(action)

            # swap players
            # if at the end of the players, play the turn
            # play for other non-muzero players
            self.current_player += 1
            while not self.current_player == 0 and not self.current_player == 1:
                # puts random action in queue for that player
                self.action_queue[self.current_player] = self.get_card_from_action(self.random.choice(self.legal_actions()))
                self.current_player += 1
                if self.current_player >= self.num_players:
                    self.current_player = 0
                    self.play_turn(self.action_queue)
                    self.turn_num += 1
                    break

        # see if end of age
        if self.turn_num == 6:
            self.turn_num = 0
            if self.done or self.new_age():
                total_points = 0
                for i in range(self.num_players):
                    if not i == self.current_player:
                        total_points += self.players[i].calculate_victory_points()
                reward = self.players[self.current_player].calculate_victory_points() - (total_points / (self.num_players-1))
                self.done = True

        # do observation space
        observation = self.get_observation()

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
        
        return observation, reward, done

    # obersvation: [
        # [other board, coins]
        # [other board, coins]
        # [other board, coins]
        # [other board, coins]
        # [other board, coins]
        # [other board, coins]
        # [your board, coins]
    # ]
    def get_observation(self):
        observation = []
        your_board = []
        for i in range(self.num_players):
            to_append = []
            # for other players
            if not i == self.current_player:
                to_append = create_observation_space(names_of_cards_to_actions(self.players[i].buildings))
                to_append.append(self.players[i].coins)
                observation.append(to_append)
            # for you
            else:
                your_board = create_observation_space(names_of_cards_to_actions(self.players[i].buildings))
                your_board.append(self.players[i].coins)
        observation.append(your_board)
        return [observation]

    def get_card_from_action(self, action):
        # either selling or building
        if action == 0 or action == 1:
            card_played = actions[action]
        # normal playing
        else:
            for card in self.get_player_hand(self.current_player):
                if card.name == actions[action]:
                    card_played = card
        return card_played

    def get_player_hand(self, index):
        return self.hands[(index+self.turn_num*self.direction) % self.num_players]

    def do_military(self, agenum):
        for i in range(self.num_players):
            for direction in [-1,+1]:
                if self.players[i].swords < self.players[(i+direction) % self.num_players].swords:
                    self.players[i].military.append(-1)
                if self.players[i].swords > self.players[(i+direction) % self.num_players].swords:
                    self.players[i].military.append(agenum*2-1)

    def play_turn(self, action_queue):
        for i in range(self.num_players):
            # if chose to sell or build, deal with that
            if action_queue[i] == "sell" or action_queue[i] == "build":
                card = self.random.choice(self.get_player_hand(i))
                if action_queue[i] == "sell":
                    self.players[i].sell_card(card)
                elif action_queue[i] == "build":
                    self.players[i].build_wonder()
                action_queue[i] = card
            # call play_card if that
            else:
                self.players[i].play_card(action_queue[i])
            # delete card from hand
            self.get_player_hand(i).remove(action_queue[i])

        self.action_queue = {}

        for player in self.players:
            player.resolve_effect()

    # returns true if game is ended
    def new_age(self):
        self.current_age += 1

        if self.current_age == 4:
            return True

        deck = self.dealer.get_deck(self.num_players, self.current_age)
        self.hands = [[] for _ in range(self.num_players)]
        self.random.shuffle(deck)

        for hand in self.hands:
            for i in range(7): hand.append(deck.pop())

        if not self.setting_up:
            self.do_military(self.current_age)
        self.setting_up = False

        self.direction = (1 if self.current_age == 2 else -1)

        return False

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
        legalactions = []
        for card in self.get_player_hand(self.current_player):
            if self.players[self.current_player].can_play_card(card):
                legalactions.append(actions.index(card.name))
        if self.players[self.current_player].can_upgrade_wonder():
            legalactions.append(1)
        if len(legalactions) == 0:
            legalactions = [0]

        return legalactions

    def reset(self):
        """
        Reset the game for a new game.
        Returns:
            Initial observation of the game.
        """
        self.__init__(self.seed)
        return self.get_observation()

    def render(self):
        for i in range(self.num_players):
            print(f"player {str(i)} has {self.players[i].coins} coins and their board is:")
            print(self.players[i].buildings)
            print("and their hand is: ")
            print(self.get_player_hand(i))
            print(f"and they have: {self.players[i].calculate_victory_points()} victory point(s)")

    def close(self):
        pass