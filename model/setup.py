# import libraries
from agent import * 
from global_vars import *
import pandas as pd
import os

def setup(par, gv, al):

    # with pandas, read strategy.csv not from the same folder but from the superfolder
    superfolder = os.path.abspath(os.path.join(os.getcwd(), '..'))
    path = os.path.join(superfolder, 'strategies.xlsx')
    df = pd.read_excel(path)
    strategies = df['description'].values.tolist()
    strategies_names = df['strategy'].values.tolist()


    #create agents
    for _ in range(par.n_players):
        if par.debug_LLM: print(f"Creating agent {_ + 1} out of {par.n_players}         ", end = "\r")
        new_agent = agent(par, _)
        new_agent.initialize_strategy(strategies, strategies_names)
        al.agents_list.append(new_agent)
        al.original_list.append(new_agent)

    # create network
    create_networks(par, gv, al)
    #for a in al.agents_list: a.neighbors = [ag for ag in al.agents_list if ag != a]

    #adjust globals
    adjust_globals(par, gv, al)




        






