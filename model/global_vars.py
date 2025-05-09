# import libraries+
import numpy as np

class glob_vars:
    
    def __init__(self, par):

        #self.t = 0 #time step of the simulation

        self.brown = par.init_brown 
        self.brown_ts = []
        self.brown_prediction = [par.init_brown for x in range(par.length_forecast)]
        self.n_players_ts = []
    
        self.ts_black = [par.init_black]
        self.ts_green = [par.init_green]
        self.ts_red = [par.init_red]

        self.end_flag = True
        self.turn = 0

        



    def compute_globals(self, al, par):

        def brown_prediction():
            self.brown_ts.append(self.brown)
            if self.turn == 0: 
                self.brown_prediction = self.brown
                return

            brown_ts_infer = self.brown_ts
            if self.turn > par.length_memory:
                brown_ts_infer = self.brown_ts[-par.length_memory:]
            

            trend_brown = np.polyfit(range(len(brown_ts_infer)), brown_ts_infer, 1)
            self.brown_prediction = []
            for i in range(par.length_forecast):
                self.brown_prediction.append(self.brown + i * trend_brown[0])
            #print(self.brown_prediction)
            self.brown_prediction = self.brown_prediction[-1]

        def compute_time_series():
            self.n_players_ts.append(len(al.agents_list))
            self.turn += 1

            new_black, new_green, new_red = 0,0,0
            for a in al.agents_list:
                new_green += a.green
                new_black += a.black
                new_red += a.red

            self.ts_black.append(new_black / len(al.agents_list))
            self.ts_green.append(new_green / len(al.agents_list))
            self.ts_red.append(new_red / len(al.agents_list))

        brown_prediction()
        compute_time_series()
        if self.turn == par.max_turn: self.end_flag = False



    
    def brown_computing(self, par, gv, al):

        remove_browns_black = par.brown_per_black * sum([ag.black for ag in al.agents_list])
        remove_browns_red = par.brown_per_red * sum([ag.red for ag in al.agents_list])
            
        self.brown -= ( remove_browns_black + remove_browns_red)
        if self.brown <= 0: 
            self.end_flag = False
            self.brown = 0 #for plots

        



def agent_death(par, gv, al):
      
    ag_death = [ag for ag in al.agents_list if ag.green + ag.black == 0]
    if any(ag_death):
        for ag in ag_death: 
            al.agents_list.remove(ag)
            ag.survived = 0
            for n in ag.neighbors: 
                # remove dying agent from the network of the neighbor
                n.neighbors.remove(ag)

                def_agent = ag.last_defeated_by
                # if not present, add defeating agent in the network of the neighbor
                if def_agent not in n.neighbors:
                    n.neighbors.append(ag.last_defeated_by)
                # if not present, add neighbor in the network of the defeated agent
                if n not in def_agent.neighbors:
                    def_agent.neighbors.append(n)
        
        # if population of a single agent, finish the simulation
        if len(al.agents_list) < 2: gv.end_flag = False

def adjust_globals(par, gv, al):
    
    gv.brown = par.init_brown 
    par.max_brown = 2 * par.init_brown




class agents_list:
    def __init__(self):

        self.agents_list = []
        self.original_list = []
        #insert list initialized with []



            