# import libraries
from global_vars import *
from agent import * 
import random
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import time

def go(par, gv, al):

    # 1 - agent turn

    for ag in al.agents_list: ag.update_dec_making(par, gv, al)
    time.sleep(0.2)
    
    with ThreadPoolExecutor(max_workers=len(al.agents_list)) as executor:
        futures = [executor.submit(ag.decision_resource, par, gv, al) for ag in al.agents_list]
        for future in futures:
            future.result()
    
    #time.sleep(5)

    for ag in al.agents_list:
        ag.implement_decision_resource(par, gv, al)

    with ThreadPoolExecutor(max_workers=len(al.agents_list)) as executor:
        futures = [executor.submit(ag.decision_attack, par, gv, al) for ag in al.agents_list]
        for future in futures:
            future.result()

    # for ag in al.agents_list:
    #     ag.decision_attack(par, gv, al)

    for ag in al.agents_list:
        ag.perform_attack(par, gv, al)

    # 2 - blocks computing
    gv.brown_computing(par, gv, al)


    # 3 - death of agents
    agent_death(par, gv, al)


    # N - compute globals
    gv.compute_globals(al, par)




