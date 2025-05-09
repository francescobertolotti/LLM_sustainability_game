import matplotlib.pyplot as plt
import numpy as np
import os

superfolder = os.path.abspath(os.path.join(os.getcwd(), '..'))
path_pics = os.path.join(superfolder, 'results/pictures')

def plot_individual_ts(mod, path_to_save = ''): # fig1

    fig, ax = plt.subplots(1, 3, figsize=(24, 8), sharex=True)
    for agent in mod.al.original_list:
        ax[0].plot(agent.ts_black, color='black', alpha=0.2)
        ax[1].plot(agent.ts_green, color='lime', alpha=0.2)
        ax[2].plot(agent.ts_red, color='salmon', alpha=0.2)
    
    ax[0].set_title('Black Resources Over Time')
    ax[1].set_title('Green Resources Over Time')
    ax[2].set_title('Red Resources Over Time')
    ax[0].set_ylabel('Resources')
    ax[1].set_ylabel('Resources')
    ax[2].set_ylabel('Resources')

    ax[0].set_xlabel('Time')
    ax[1].set_xlabel('Time')
    ax[2].set_xlabel('Time')

    #path_to_save = os.path.join(path_pics, f'fig1_{mod.id}.png')
    plt.savefig(path_to_save, dpi=300)
    plt.close()



def plot_ts_all(mod, path_to_save = ''): #fig2

    fig, ax = plt.subplots(2, 2, figsize=(12, 12), sharex=True)

    plt.subplot(2,2,1)
    plt.plot(mod.gv.ts_black, label='black', color='black')
    plt.plot(mod.gv.ts_green, label='green', color='lime')
    plt.plot(mod.gv.ts_red, label='red', color='salmon')
    plt.title('Blocks')
    plt.xlabel('turn')
    plt.ylabel('number of blocks')
    plt.legend()

    plt.subplot(2,2,2)
    plt.plot(mod.gv.brown_ts, label='brown', color='brown')
    plt.title('# browns')
    plt.xlabel('turn')
    plt.ylabel('number of brown')
    plt.legend()

    plt.subplot(2,2,3)
    plt.plot(mod.gv.n_players_ts, label='n_players', color='navy')
    plt.title('Number of players')
    plt.xlabel('turn')
    plt.ylabel('number of players')
    plt.legend()

    plt.subplot(2,2,4)
    decisions_ts = []

    for t in range(mod.gv.turn):
        new_decisions = [0] * 7
        for ag in mod.al.original_list:
            if len(ag.ts_decisions_production) < t + 1: continue
            decision_turn_t = ag.ts_decisions_production[t]
            for d in decision_turn_t:
                new_decisions[d[0]] += d[1]
        decisions_ts.append(new_decisions)

    dec1, dec2, dec3, dec4, dec5, dec6, dec7 = [], [], [], [], [], [], []
    for d in decisions_ts:
        dec1.append(d[0])
        dec2.append(d[1])
        dec3.append(d[2])
        dec4.append(d[3])
        dec5.append(d[4])
        dec6.append(d[5])
        dec7.append(d[6])

    plt.plot(dec1, label='k2k', color='black', alpha = 0.5)
    plt.plot(dec2, label='g2k', color='grey', alpha = 0.5)
    plt.plot(dec3, label='k2g', color='green', alpha = 0.5)
    plt.plot(dec4, label='g2g', color='lime', alpha = 0.5)
    plt.plot(dec5, label='k2r', color='red', alpha = 0.5)
    plt.plot(dec6, label='g2r', color='salmon', alpha = 0.5)
    plt.plot(dec7, label='g2b', color='brown', alpha = 0.5)

    plt.legend()
    plt.title('Decisions over time')
    plt.xlabel('turn')
    plt.ylabel('number of blocks')
    
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.2, wspace=0.2)

    #path_to_save = os.path.join(path_pics, f'fig2_{mod.id}.png')
    plt.savefig(path_to_save, dpi=300)
    plt.close()


def plot_ts_all_decisions(mod, path_to_save = ''): # fig3

    n = mod.par.n_players

    # create a figure with subplots grid with 4 columns and the right number of rows 
    n_cols = 4
    n_rows = int(np.ceil(n / n_cols))
    fig, axs = plt.subplots(n_rows, n_cols, figsize=(20, 5 * n_rows), sharex=True)
    axs = axs.flatten()  # flatten the 2D array of axes to 1D for easier indexing

    fig.subplots_adjust(hspace=0.4, wspace=0.4)  # adjust space between subplots

    for i, agent in enumerate(mod.al.original_list):
        ax = axs[i]
        ax.set_title(f'Agent {agent.who} - {agent.strategy_name}')
        ax.set_xlabel('turn')
        ax.set_ylabel('number of blocks')

        # plot the decisions for this agent
        decisions_ts = []
        for t in range(len(agent.ts_decisions_production)):
            new_decisions = [0] * 7
            #if len(agent.ts_decisions_production) < t + 1: continue
            decision_turn_t = agent.ts_decisions_production[t]
            for d in decision_turn_t:
                new_decisions[d[0]] += d[1]
            decisions_ts.append(new_decisions)

        dec1, dec2, dec3, dec4, dec5, dec6, dec7 = [], [], [], [], [], [], []
        for d in decisions_ts:
            dec1.append(d[0])
            dec2.append(d[1])
            dec3.append(d[2])
            dec4.append(d[3])
            dec5.append(d[4])
            dec6.append(d[5])
            dec7.append(d[6])

        ax.plot(dec1, label='k2k', color='black', alpha=0.5)
        ax.plot(dec2, label='g2k', color='grey', alpha=0.5)
        ax.plot(dec3, label='k2g', color='green', alpha=0.5)
        ax.plot(dec4, label='g2g', color='lime', alpha=0.5)
        ax.plot(dec5, label='k2r', color='red', alpha=0.5)
        ax.plot(dec6, label='g2r', color='salmon', alpha=0.5)
        ax.plot(dec7, label='g2b', color='brown', alpha=0.5)

        ax.legend()
    
    # Hide any unused subplots
    for j in range(i + 1, len(axs)):
        fig.delaxes(axs[j])
    
    plt.tight_layout()

    #path_to_save = os.path.join(path_pics, f'fig3_{mod.id}.png')
    plt.savefig(path_to_save, dpi=300)
    plt.close()


