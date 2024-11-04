#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 00:51:34 2024

@author: johnnynienstedt
"""

#
# Championship Odds for 6- and 8-team playoffs
#
# Johnny Nienstedt 10/31/24
#

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


# sim wild card series
def wc_series_sim(wins, current_format):
    
    a = wins
    
    if current_format:
        if a > 90:
            b = 88
        else:
            b = 90
    else:
        b = 93 - (a-93)
    
    home_field = a > b
    
    a = a/162 - (a/162 - 0.5)/29
    b = b/162 - (b/162 - 0.5)/29
    
    p = a*(1-b)/((a*(1-b))+(b*(1-a)))
    
    if home_field:
        p = p + 0.035
    else:
        p = p - 0.035
        
    a_win = 0
    for n in range(1,3):
        a_win += math.comb(n,1) * p * (1-p)**(n-1)
    a_win = p*a_win
    
    return a_win
    
# sim 5 and 7 game series
def long_series_sim(wins, current_format, n_games):

    a = wins
            
    if n_games == 5:
        if current_format:
            b = 95
        else:
            b = 95 - (a-95)/1.5
            
    if n_games == 7:
        b = 96
        
    a = a/162 - (a/162 - 0.5)/29
    b = b/162 - (b/162 - 0.5)/29
        
    p = a*(1-b)/((a*(1-b))+(b*(1-a)))
    
    a_win = 0
    k = math.floor(n_games/2)
    for n in range(k,n_games):
        a_win += math.comb(n,k) * p**k * (1-p)**(n-k)
    a_win = p*a_win
    
    return a_win
    
# get odds
def playoff_sim(wins, current_format, verbose):
    
    if current_format:
        playoff_dict = {81: 0.05,
                        82: 0.075,
                        83: 0.125,
                        84: 0.2,
                        85: 0.275,
                        86: 0.442,
                        87: 0.65,
                        88: 0.725,
                        89: 0.791,
                        90: 0.875,
                        91: 0.925,
                        92: 0.95,
                        93: 0.975}
        
        if wins < 94:
            p_odds = playoff_dict[wins]
        else: p_odds = 1
    
    else:
        playoff_dict = {81: 0.467,
                        82: 0.633,
                        83: 0.766,
                        84: 0.867,
                        85: 0.95,
                        86: 0.975}
        
        if wins < 87:
            p_odds = playoff_dict[wins]
        else: p_odds = 1
    
    bye_dict = {90: 0.025,
                91: 0.05,
                92: 0.125,
                93: 0.225,
                94: 0.3,
                95: 0.45,
                96: 0.575,
                97: 0.65,
                98: 0.7,
                99: 0.725,
                100: 0.775,
                101: 0.85,
                102: 0.9,
                103: 0.95}
    
    if current_format:
        
        if wins > 103:
            bye = 1
        elif wins < 90:
            bye = 0
        else:
            bye = bye_dict[wins]
            
    else:
        bye = 0
    
    round_odds = [None]*4
    round_odds[0] = wc_series_sim(wins, current_format)
    round_odds[1] = long_series_sim(wins, current_format, 5)
    round_odds[2] = long_series_sim(wins, current_format, 7)
    round_odds[3] = long_series_sim(wins, current_format, 7)    

    cgb = math.prod(round_odds[1:])
    cnb = math.prod(round_odds)

    if bye == 1:
        round_odds[0] = 1
    if bye < 1:
        round_odds[0] = bye + (1-bye)*round_odds[0]
            
    ws_odds = math.prod(round_odds)
    championship_odds = p_odds*ws_odds
    
    if verbose:
        if p_odds < 1 and current_format:
            print(f"\nA {wins}-win team has a {100*p_odds:.1f}% chance of reaching the playoffs under the current format.")
            print(f"\nIf they reach the playoffs, they have a {100*bye:.1f}% chance of recieving a bye.")
            print(f"If they do receive a bye, they have a {100*cgb:.1f}% chance to win the World Series, {100*cnb:.1f}% if not.")
            print(f"\nTherefore, their overall championship odds are {100*championship_odds:.1f}%.")
            
        if p_odds == 1 and current_format:
            print(f"\nA {wins}-win team will very likely make the playoffs, with a {100*bye:.1f}% chance to receive a bye.")
            print(f"If they do receive a bye, they have a {100*cgb:.1f}% chance to win the World Series, {100*cnb:.1f}% if not.")
            print(f"\nTherefore, their overall championship odds are {100*championship_odds:.1f}%.")
            
        if p_odds < 1 and not current_format:
            print(f"\nA {wins}-win team has a {100*p_odds:.1f}% chance of reaching the playoffs under the new format.")
            print(f"\nIf they reach the playoffs, they have a {100*ws_odds:.1f}% chance to win the world series,")
            print(f"meaning their overall championship odds are {100*championship_odds:.1f}%.")
            
        if p_odds == 1 and not current_format:
            print(f"\nA {wins}-win team will very likely make the playoffs under the new format.")
            print(f"\nTheir championship odds are {100*championship_odds:.1f}%.")
        
    return championship_odds

# current format vs potential 8-team no byes format
current = []
proposed = []
for w in range(81,106):
    current.append(playoff_sim(w, True, verbose = False))
    proposed.append(playoff_sim(w, False, verbose = False))


# plot results
fig, ax = plt.subplots()
plt.plot(np.arange(81,106), current, label='Current Format')
plt.plot(np.arange(81,106), proposed, label='Proposed Format')

ax.set_title('World Series Odds by Regular Season Wins')
ax.set_xlabel('Regular Season Wins')
ax.set_ylabel('Calculated Championship Odds')
ax.set_xticks(np.arange(81,106,2))
ax.legend(fontsize = 12, loc='upper left', bbox_to_anchor=(0.05,0.9))
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{100*y:.0f}%'))

plt.tight_layout()
plt.show()