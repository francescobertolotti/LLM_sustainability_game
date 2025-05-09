# import libraries

class parameters:
    def __init__(self):

        self.max_turn = 100
        self.n_players = 100

        self.strategy = True
        self.memory_attack = False
        self.prediction_brown = True
        self.information_neighbors = True

        #init parameters
        self.init_black = 5
        self.init_green = 5
        self.init_red = 0
        self.init_brown = 2000

        #network parameters
        self.n_connections = 5

        #investment parameters
        self.ip = [1,2,2,2,1,1,2]
        self.max_blocks = 500 
        self.max_brown = self.init_brown


        #brown consumption parameters
        self.brown_per_black = 1
        self.brown_per_red = 1

        #memory parameters
        self.pref_ud_rate = 0.05 # preference update rate
        self.length_forecast = 5
        self.length_memory = 5

        # prompts
        self.rules = """Each agent has with non-polluting industrial capability (green blocks), polluting industrial capability (black blocks), and military capability (red blocks). 
        All share a biosphere (brown blocks). If the brown blocks are depleted, you have lost.
        On each turn, agents decide what to produce and whether to attack. 
        Green and black blocks can be used to produce more blocks. Red blocks are used to attack. 
        If you have no red blocks, you cannot attack and can not defend from others' attacks.
        Attacks transfer resources if successful, and can eliminate neighbors. 
        Brown blocks are depleted by owning red or black blocks, unless sustained by green ones. 
        The game ends when: one agent remains, biosphere is exhausted, or max turns are reached."""

        self.prompt_attack = """You are an agent in the game and you have to decide whether to attack or not.
        You can decide to not attack or to attack one or more of your neighbors. You have information to decide your actions.
        Return a list of targets (neighbors) to attack. If you do not want to attack, return an empty list [].
        Do not return any extra comment, only the list of the entities (only number!) you want to attack."""

        self.prompt_production = f"""You are an agent in the game and you have to decide how to produce. 
        You can take one of these decisions: 
        - decision 0: employ black produce new black (ratio {self.ip[0]}:1)
        - decision 1: destroy green to produce new black (ratio {self.ip[1]}:1)
        - decision 2: destroy black to produce new green (ratio {self.ip[2]}:1)
        - decision 3: employ green to produce new green (ratio {self.ip[3]}:1)
        - decision 4: employ black to produce new red (ratio {self.ip[4]}:1) 
        - decision 5: employ green to produce new red (ratio {self.ip[5]}:1)
        - decision 6: employ green to produce new brown (ratio {self.ip[6]}:1)
        You can take one of these decisions. You can not have more than {self.max_blocks} in total.
        You can convert black to green and vice versa. It can make sense especially when the brown is low, to avoid depleting the biosphere and lose.
        If the prediction of brown block is below 0, you should convert black in green and produce brown blocks to avoid losing the game.
        Return a list with the decision you want to take and the amount of blocks you want to use.
        Do not return any extra comment, only the list of the decision you want to take and the amount of blocks you want to use.
        The list should be in this format: [(decision_type, decision_size)], or you can [(d1, s1), (d2, s2), ...] if you want to take more than one decision."""

        self.explanation_attack = False
        self.explanation_production = False

        self.debug_LLM = False

