# IMPLEMENTATO IN 4 - 1 - la rete quando muore un agente si "rimargina" e crea un nuovo link fra due che non sono collegati, se possibile. SI prende il nuovo vicino fra i vicini di qeullo morto
# 2 - nel processo decisionale, la scelta di fare rossi dipende anche dal numero di rossi degli avversari
# 3 - potrei dover implementare delle decisioni 7 e 8 in cui si dismettono i rossi e si trasformano in neri o verdi
# FATTO 4 - quando un agente muore, la sua rete di vicini è ereditata dall'agente che l'ha sconfitto per ultimo, e allo stesso modo gli agenti che lo avevano vicino sostituiscono come vicino quello che l'ha sconfitto (a meno che non ci sia già)

from parameters import *
from global_vars import *
from agent import * 
from setup import *
from go import *
import os
from visualize import *

import numpy as np
import random
import pandas as pd
import datetime
import time

class model():
    def __init__(self, my_seed):
        
        random.seed(my_seed)
        np.random.seed(seed=my_seed)

        self.al = agents_list()
        self.par = parameters()
        self.gv = glob_vars(self.par)
        self.id = f"{np.random.randint(0,99999999)}_seed_{my_seed}"
        self.seed = my_seed

    def run(self, my_seed):
        
        random.seed(my_seed)
        np.random.seed(seed=my_seed)

        if self.par.debug_LLM: print("SETUP")
        setup(self.par, self.gv, self.al)

        if self.par.debug_LLM: print("GO")
        while(self.gv.end_flag):
            if self.par.debug_LLM: print(f"turn {self.gv.turn} - brown {self.gv.brown} - n_players {len(self.al.agents_list)} - brown_pred {self.gv.brown_prediction}")
            go(self.par, self.gv, self.al)


        return self.gv



class experiment():

    def __init__(self, n_sim):

        self.n_sim = n_sim
        self.mod = None
        self.path_results = os.path.join(os.path.abspath(os.path.join(os.getcwd(), '..')), 'results')
        self.id_experiment = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        self.dict_res = {
                         # inputs 
                         'seed': [],
                         'n_connections': [],
                         'n_players': [],
                         'init_brown': [], 
                         'length_forecast': [],
                         'length_memory': [],

                         # outputs
                         'final_turn': [],
                         'n_players_final': [],
                         'blacks':[],
                         'greens':[],
                         'reds':[],
                         'browns':[]
                         }
        
    def initialize_experiment(self):

        # create a subfolder to self.path_results called with the id of the experiment
        os.makedirs(os.path.join(self.path_results, self.id_experiment), exist_ok=True)
        # create in the subfolder two others subfolders, one called figures and the other agents_data
        os.makedirs(os.path.join(self.path_results, self.id_experiment, 'figures'), exist_ok=True)
        os.makedirs(os.path.join(self.path_results, self.id_experiment, 'agents_data'), exist_ok=True)



    def generate_inputs(self,mod):
        
        self.mod.par.n_connections = random.choice([1,3,5])
        self.mod.par.n_players = random.choice([5,10,15,20,25,30])
        self.mod.par.init_brown = 2000
        self.mod.par.length_forecast = np.random.randint(1,10)
        self.mod.par.length_memory = 5

    def run_experiment(self):

        self.initialize_experiment()
        
        errors = 0
        for i in range(self.n_sim): 

            print('Sim #' + str(i) + ' of ' + str(self.n_sim))

            try:
                my_seed = random.randint(0,1000000)
                self.mod = model(my_seed)
                self.generate_inputs(self.mod)
                self.mod.run(my_seed)
                self.collect_results(my_seed)
                time.sleep(30)
            except Exception as e:
                errors += 1
                print('     Error in sim ' + str(i) + ': ' + str(e) + 'Waiting 60 seconds before retrying...')
                time.sleep(60)
                continue

            if i % 10 == 0:
                df_results_temp = pd.DataFrame(self.dict_res)
                df_results_temp.to_csv(os.path.join(self.path_results, self.id_experiment, 'results_' + str(np.random.randint(0,99999999)) + '.csv'), index = False)


        self.dict_res = pd.DataFrame(self.dict_res)
        self.dict_res.to_csv(os.path.join(self.path_results, self.id_experiment, 'results_' + str(np.random.randint(0,99999999)) + '.csv'), index = False)
        print("Experiment completed! There were " + str(errors) + " errors: as always, your code is not perfect...but it works most of the time!")

    def collect_results(self, my_seed):

        self.dict_res['seed'].append(my_seed)
        self.dict_res['n_connections'].append(self.mod.par.n_connections)
        self.dict_res['n_players'].append(self.mod.par.n_players)
        self.dict_res['init_brown'].append(self.mod.par.init_brown)
        self.dict_res['length_forecast'].append(self.mod.par.length_forecast)
        self.dict_res['length_memory'].append(self.mod.par.length_memory)

        self.dict_res['final_turn'].append(self.mod.gv.turn)
        self.dict_res['blacks'].append(self.mod.gv.ts_black[len(self.mod.gv.ts_black) - 1])
        self.dict_res['greens'].append(self.mod.gv.ts_green[len(self.mod.gv.ts_green) - 1])
        self.dict_res['reds'].append(self.mod.gv.ts_red[len(self.mod.gv.ts_red) - 1])
        self.dict_res['browns'].append(self.mod.gv.brown_ts[len(self.mod.gv.brown_ts) - 1])

        ag_survived = [ag for ag in self.mod.al.agents_list]
        ag_death = [ag for ag in self.mod.al.original_list if ag.survived == 0]
        
        self.dict_res['n_players_final'].append(len(ag_survived))

        path_figures = os.path.join(self.path_results, self.id_experiment, 'figures')
        plot_individual_ts(self.mod, path_figures + f"/fig1_{self.mod.id}")
        plot_ts_all(self.mod, path_figures + f"/fig2_{self.mod.id}")
        plot_ts_all_decisions(self.mod, path_figures + f"/fig3_{self.mod.id}")

        # store time series of all the properties of the agents
        dict_single_agent = {
            'who': [],
            'strategy': [],
            'ts_black': [],
            'ts_green': [],
            'ts_red': [],
            'ts_attacks_made': [],
            'ts_attacks_received': [],
            'ts_decisions_production': [],
            'ts_decisions_attack': []
        }

        for ag in self.mod.al.original_list:
            dict_single_agent['who'].append(ag.who)
            dict_single_agent['strategy'].append(ag.strategy)
            dict_single_agent['ts_black'].append(ag.ts_black)
            dict_single_agent['ts_green'].append(ag.ts_green)
            dict_single_agent['ts_red'].append(ag.ts_red)
            dict_single_agent['ts_attacks_made'].append(ag.ts_attacks_made)
            dict_single_agent['ts_attacks_received'].append(ag.ts_attacks_received)
            dict_single_agent['ts_decisions_production'].append(ag.ts_decisions_production)
            dict_single_agent['ts_decisions_attack'].append(ag.ts_decisions_attack)
        dict_single_agent = pd.DataFrame(dict_single_agent)
        dict_single_agent.to_csv(os.path.join(self.path_results, self.id_experiment, 'agents_data', 'agents_data_' + self.mod.id + '.csv'), index = False)