import json

class Bot(object):
    '''
        This class implements a bot that applies the reinforced-learning algorithm to the Flappy Bird game.
        After each iteration (defined as a game that ends when the bird dies), it wil update the Q-values.
        After each DUMPING_N interations, it will dump the Q-values into the local JSON file as a state-save thing.
    '''
    def __init__(self):
        self.gameCNT = 0 # Game count of current run, +1 after each death
        self.DUMPING_N = 25 # Iterations after which to dump the Q-values into the JSON.
        self.discount = 1.0
        self.r = {0:1 , 1:-1000} # Reward function - +1 for not dying, -1000 for dying. Extreme prejudice to life.
        self.lr = 0.7
        self.load_qvalues()
        self.last_state = "420_240_0"
        self.last_action = 0
        self.moves = []
    
    def load_qvalues(self):
        '''
            load Q-values from a JSON file
        '''
        self.qvalues = {}
        try:
            json_file = open('qvalues.json','r')
        except IOError:
            return
        self.qvalues = json.load(json_file)
        json_file.close()

    def act(self,xdif,ydif,vel):
        '''
            Choose the best action to do wrt the current state - chooses to not flap for tiebreak
        '''
        state = self.map_state(xdif,ydif,vel)
            #Add the experience to personal history
        self.moves.append( [self.last_state, self.last_action, state] ) 
            #Update last_state with curent state
        self.last_state = state 

        if self.qvalues[state][0] >= self.qvalues[state][1]:
            self.last_action = 0 
            return 0
        else:
            self.last_action = 1
            return 1
        
    def get_last_state(self):
        return self.last_state
    
    def update_scores(self):
        '''
            Updates Q-values by iterating over experiences
        '''
        history = list(reversed(self.moves))

            #Flag if the bird died in the top pipe
        high_death_flag = True if int(history[0][2].split('_')[1]) > 120 else False

            #Q-learning score updates
        t = 1
        for exp in history:
            state = exp[0]
            act=  exp[1]
            res_state = exp[2]

            #Select reward
            if t == 1 or t == 2:
                cur_reward = self.r[1]
            elif high_death_flag and act:
                cur_reward = self.r[1]
                high_death_flag = False
            else:
                cur_reward = self.r[0]
            
            #Now, update them.
            self.qvalues[state][act] = (1-self.lr)*(self.qvalues[state][act]) + self.lr*(cur_reward + self.discount*max(self.qvalues[res_state]))
            t += 1

        self.gameCNT += 1   #Game has obviously ended by this point, so increase counter
        self.dump_qvalues() #Also dump q-values data while we're at it
        self.moves = [] #Clear up moves for next gen - we've already updated the strategy while dumping

    def map_state(self,xdif,ydif,vel):
        '''
            Map the tuple (xdif,ydif,vel) into the state, wrt the grid.
            The state is a string, defined as "xdif_ydif_vel".
            Here,

            x => [-40,-30, ... , 120] U [140,210, ... ,420]
            y => [-300,-290, ... , 160] U [180,240, ... , 420]
        '''
        if xdif < 140:
            xdif = int(xdif) - (int(xdif) % 10)
        else:
            xdif = int(xdif) - (int(xdif) % 70)
            
        if ydif < 180:
            ydif = int(ydif) - (int(ydif) % 10)
        else:
            ydif = int(ydif) - (int(ydif) % 60)

        #Return the values
        return str(int(xdif)) + '_' + str(int(ydif)) + '_' + str(vel)

    def dump_qvalues(self):
        '''
            Dump the Q-values to a local JSON file.
        '''

        if self.gameCNT % self.DUMPING_N == 0:
            infile = open('qvalues.json','w')
            json.dump(self.qvalues,infile)
            infile.close()
            print("Q-Values updated on the local file.")
        