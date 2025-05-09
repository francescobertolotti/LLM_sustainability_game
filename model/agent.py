#import libraries
import numpy as np
import random
import networkx as nx
from openai import OpenAI
import os
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor

openai_api_key="ADD YOUR APIKEY HERE! THANKS FOR CHECKING MY CODE BUT I DO NOT WANT TO PAY FOR YOUR EXPERIMENTS :)"
os.environ["OPENAI_API_KEY"] = openai_api_key

client = OpenAI()

class LLM_output_production(BaseModel):
    value: str
    explanation: str

class LLM_output_attack(BaseModel):
    value: str
    explanation: str


class agent:
    def __init__(self, par, who):
        self.who = who #number of the agent

        self.black = par.init_black
        self.green = par.init_green
        self.red = par.init_red

        self.free_black = 0
        self.free_green = 0

        self.distroyed_black = 0
        self.distroyed_green = 0

        self.survived = 1
        self.winner = 0

        self.ts_black = [par.init_black]
        self.ts_green = [par.init_green]
        self.ts_red = [par.init_red]
        self.ts_attacks_made = []
        self.ts_attacks_received = []

        self.ts_decisions_production = []
        self.ts_decisions_attack = []

        self.neighbors = []
        self.last_defeated_by = None

        # memory
        self.length_forecast = par.length_forecast
        self.length_memory = par.length_memory

        # strategy
        self.strategy = ""
        self.strategy_name = ""

        self.targets = []
        self.last_decision = []
        
    def initialize_strategy(self, strategies, strategies_names):

        # prompt = f"""You are an agent in the game and you have to decide your strategy. These are the rules.
        # ["{par.rules}"]
        # Decide your purpose and your strategy in the game, and return it in max 5 rows."""
        # messages = [{"role": "user", "content": prompt}]
        # completion = client.chat.completions.create(model="gpt-4o-mini",messages=messages,temperature=1.5, max_tokens=400)
        # self.strategy = completion.choices[0].message.content

        self.strategy = random.choice(strategies)
        self.strategy_name = strategies_names[strategies.index(self.strategy)]





    def decision_resource(self, par, gv, al):

        self.free_black, self.free_green = self.black, self.green

        decision_random = False

        if decision_random:
            #decide the action to do
            available_actions = [0,1,2,3,4,5,6]
            decisions_type = random.choice(available_actions)
            decisions_size = random.randint(1, par.max_blocks)
            decisions = [(decisions_type, decisions_size)]
        else:
            # decide the action to do

            system_prompt = par.rules

            if par.strategy: system_prompt = system_prompt + "\n\n YOUR STRATEGY IS: [" + self.strategy + "]"
            if par.prediction_brown: system_prompt = system_prompt + f"\n\n With the current trend of biosphere consumption, in {par.length_forecast} turns, the brown blocks will be {gv.brown_prediction}."
            if par.information_neighbors: system_prompt = system_prompt + f"\n\nThe mean of your neighbors is: black={np.mean([ag.black for ag in self.neighbors]):.1f}, red={np.mean([ag.red for ag in self.neighbors]):.1f}, green={np.mean([ag.green for ag in self.neighbors]):.1f}."

            system_prompt = system_prompt + "\n\n" + par.prompt_production
            system_prompt += f"Your current dotation of blocks is black={self.black}, red={self.red}, green={self.green}.\n"

            if par.explanation_production: system_prompt = system_prompt + "\n\n The explanation of your decision can be maximum 1 sentence."
            content = f"Agent {self.who}: black={self.black}, red={self.red}, green={self.green}\n"

            messages = [{"role": "system", "content": system_prompt},{"role": "user", "content": content}]
            if par.explanation_production:
                completion = client.beta.chat.completions.parse(model="gpt-4o-mini",messages=messages,temperature=0.7, response_format=LLM_output_production)
                answer = completion.choices[0].message.parsed.value
                print(completion.choices[0].message.parsed.explanation)
            else:
                completion = client.chat.completions.create(model="gpt-4o-mini",messages=messages,temperature=0.7)
                answer = completion.choices[0].message.content
            # print(self.who, answer)
            self.last_decisions = eval(completion.choices[0].message.content)
        
        self.ts_decisions_production.append(self.last_decisions)
            

    def implement_decision_resource(self, par, gv, al):

        for decision in self.last_decisions:

            decision_type = decision[0]
            decision_size = decision[1]
            
            init_black, init_green = self.black, self.green
            
            # 0: k --> k
            tot_blocks = self.black + self.green + self.red
            if decision_type == 0: 
                new_black = int(min(decision_size, self.free_black) / par.ip[0])
                new_black = min(new_black, max(par.max_blocks - tot_blocks, 0))
                self.black += new_black
                self.free_black -= int(min(decision_size, self.free_black)) # effective consumption of bl
            
            # 1: g --> k
            if decision_type == 1: 
                converted_blocks = int(min(decision_size, init_green) / par.ip[1])
                self.black += converted_blocks
                self.green -= converted_blocks
                
            # 2: k --> g
            if decision_type == 2:
                converted_blocks = int(min(decision_size, init_black) / par.ip[2])
                self.green += converted_blocks
                self.black -= converted_blocks

            # 3: g --> g
            if decision_type == 3: 
                new_green = int(min(decision_size, self.free_green) / par.ip[3])
                new_green = min(new_green, max(par.max_blocks - tot_blocks, 0))
                self.green += new_green
                self.free_green -= int(min(decision_size, self.free_green)) # effective consumption of greens used to generate, without efficiency par.ip[3]

            # 4: k --> r
            if decision_type == 4:
                new_red = int(min(decision_size, self.free_black) / par.ip[4])
                new_red = min(new_red, max(par.max_blocks - tot_blocks, 0))
                self.red += new_red
                self.free_black -= int(min(decision_size, self.black)) # effective consumption

            # 5: g --> r
            if decision_type == 5: 
                new_red = int(min(decision_size, self.free_green) / par.ip[5])
                new_red = min(new_red, max(par.max_blocks - tot_blocks, 0))
                self.red += new_red
                self.free_green -= int(min(decision_size, self.green)) # effective consumption
            
            # 6: g --> b
            if decision_type == 6: 
                gv.brown += int(min(decision_size, self.green) / par.ip[6])
                self.free_green -= int(min(decision_size, self.green)) # effective consumption

        self.last_decisions = []


    def decision_attack(self, par, gv, al):

        def make_decision(par):

            system_prompt = par.rules 
            if par.strategy: system_prompt = system_prompt + "\n\n YOUR STRATEGY IS: [" + self.strategy + "]"
            system_prompt = system_prompt + "\n\n" + par.prompt_attack
            content = ""
            for a in self.neighbors:
                content += f"Agent {a.who}: black={a.black}, red={a.red}, green={a.green}\n"

            messages = [{"role": "system", "content": system_prompt},{"role": "user", "content": content}]
        
            completion = client.chat.completions.create(model="gpt-4o-mini",messages=messages,temperature=0.7)
            answer = completion.choices[0].message.content
            # print(self.who, answer)
            return eval(completion.choices[0].message.content)

        random_decision = False

        if self.red == 0: # if no red blocks, no attack
            targets = []
        elif random_decision: # random decision for testing
            prob_attack = [np.random.uniform() for _ in range(len(self.neighbors))]
            prob_attack = [p / sum(prob_attack) for p in prob_attack]
            other_players = [ag.who for ag in self.neighbors]
            targets = random.choices(other_players, weights = prob_attack, k = 1)
        else:
            targets = make_decision(par)

        self.targets = [ag for ag in self.neighbors if ag.who in targets]
             

    def perform_attack(self, par, gv, al):

        def implement_decision_attack(winner, loser):

            loser.last_defeated_by = winner

            winner.red -= loser.red
            loser.red = 0

            #take first black, than green
            temp_red = winner.red
            
            if temp_red <= loser.black:
                winner.black += temp_red
                loser.black -= temp_red
            else: 
                winner.black += loser.black 
                loser.black = 0
                temp_red -= loser.black 

                #then, if there are still reds that can conquest, take the green
                green_taken = min(loser.green, temp_red)
                winner.green += green_taken
                loser.green -= green_taken

        for target in self.targets:
            # update the memory 
            self.ts_attacks_made.append({'turn': gv.turn, 'target': target.who, 'self_red': self.red, 'target_red': target.red})
            target.ts_attacks_received.append({'turn': gv.turn, 'aggressor': self.who, 'self_red': target.red, 'aggressor_red': self.red})

            if self.red >= target.red:
                implement_decision_attack(self, target)
            else:
                implement_decision_attack(target, self)

        self.ts_decisions_attack.append([t.who for t in self.targets])
        self.targets = [] # reset the targets for the next turn



    def update_dec_making(self, par, gv, al):

        self.ts_black.append(self.black)
        self.ts_green.append(self.green)
        self.ts_red.append(self.red)
        





def create_networks(par, gv, al):

    # assign neighbors to each agent
    for i, agent in enumerate(al.original_list):
        # create a list of neighbors different from the agent itself and that are not already neighbors
        possible_neighbors = [ag for ag in al.original_list if ag != agent and agent.who not in ag.neighbors] 
        
        if len(possible_neighbors) == 0: continue # if there are no possible neighbors, skip the agent
       
        current_neighbors = len(agent.neighbors)  # count the current number of neighbors

        # assign the neighbors to the agent
        if current_neighbors < par.n_connections:
            # if the agent has less than n_connections neighbors, assign random neighbors
            try:
                new_neighbors = random.sample(possible_neighbors, par.n_connections - current_neighbors)
            except: # no more new neightbors
                new_neighbors = []
            agent.neighbors = agent.neighbors + new_neighbors
            # remove duplicates from agent.neighbors
            agent.neighbors = list(set(agent.neighbors))

        # check if the neighbors of the agents has the agent in their list
        for neighbor in agent.neighbors:
            if agent not in neighbor.neighbors:
                neighbor.neighbors.append(agent) # if the agent is not in the neighbors list of the neighbor, add it

    # remove theirself from the neighbors list in case
    for agent in al.original_list:
        if agent in agent.neighbors:
            agent.neighbors.remove(agent)



        
    



