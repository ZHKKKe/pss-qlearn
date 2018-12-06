import numpy as np
from sklearn import mixture
from copy import deepcopy
from third_party.flappybird_qlearning_bot.bot import Bot


class PSSBot(Bot):
    def __init__(self):
        super().__init__()
        self.config = {
            'frames_size': 50000,

            'gmm_comp': 1, 
            'gmm_iter': 100,
            'gmm_type': 'full',
            'gmm_freq': 1000,
            'gmm_threshold': 0.9,
        }

        self.init_frames = [[], []]
        self.is_init = True
        self.great_frames = [[], []]
        self.tmp_frames = [[], []]
        self.frames_size = self.config['frames_size']
        self.clst_idle = None
        self.clst_fly = None
        self.clst = None
        self.gmm = 0

    def act(self, xdif, ydif, vel, is_train=True, inround=True):
        state = self.map_state(xdif, ydif, vel)

        self.moves.append(
            (self.last_state, self.last_action, state)
        )  # Add the experience to the history


        tmp = self.last_state.split('_')
        tmp_val = [int(tmp[0]), int(tmp[1]), int(tmp[2])]
        self.tmp_frames[self.last_action].append(tmp_val)
        
        # add great samples
        if not inround:
        # if not inround and self.gmm == 0:
            for idx in range(0, len(self.great_frames)):
                if self.is_init:
                    self.init_frames[idx] += self.tmp_frames[idx]
                    x = 1 if idx == 0 else 0.2
                    if len(self.init_frames[idx]) > int(self.frames_size * x):
                        self.init_frames[idx] = self.init_frames[idx][-int(self.frames_size * x):]
            self.tmp_frames = [[], []]            
        
        self.last_state = state  # Update the last_state with the current state

        # estimate gmm
        if self.gameCNT % self.config['gmm_freq'] == 0 and not is_train and self.gmm == 0:
            self.action_gmm(self.init_frames)
            self.is_init = False
            self.gmm = 1

        greedy_search = False 
        if is_train:
            if self.clst is not None:
                tmp = state.split('_')
                tmp_val = [[int(tmp[0]), int(tmp[1]), int(tmp[2])]]
                label = self.clst.predict_proba(tmp_val)

                if label[0][0] < self.config['gmm_threshold'] and label[0][1] < self.config['gmm_threshold']:
                    greedy_search = True

        if greedy_search:
            self.last_action = 0 if np.random.rand() < 0.5 else 1
            return self.last_action
        else: 
            if self.qvalues[state][0] >= self.qvalues[state][1]:
                self.last_action = 0
                return 0
            else:
                self.last_action = 1
                return 1

    def action_gmm(self, data):
        print('action estimate')
        print(len(data[0]), len(data[1]))
        if len(data[0]) != 0 or len(data[1]) != 0:
            self.clst = mixture.GaussianMixture(n_components=2, 
                                                    max_iter=self.config['gmm_iter'], 
                                                    covariance_type=self.config['gmm_type'])

            self.clst.fit(np.array(data[0] + data[1]))

