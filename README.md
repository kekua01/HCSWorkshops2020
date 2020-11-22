# hcs-f20-ml
Workshop 3 - Machine Learning

See code is in connectfour.py
Note that the same strategy as in tictactoe is used – train the Agent with a number training games, with a set percentage of exploratory moves. However, there a HUGE number of variations for connect4, so it it harder to train the bot. I ran it multiple times with an increasing number of training games. The most I had patience for was 100k, which took a while (several minutes), which resulted in a about 40 percent win rate against a bot that simply makes winning moves if it can, and blocks winning moves if it can. 

That's still not pretty high, but a lot better than <1 percent, which is what you get without training. Extrapolating my data, training a million games would result in the Agent winning every tme. 
