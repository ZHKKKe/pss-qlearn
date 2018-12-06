from third_party.flappybird_qlearning_bot.learn import *
from third_party.flappybird_qlearning_bot.bot import Bot
from pssbot import PSSBot

if __name__ == '__main__':
    learner(PSSBot, init=True, iter=10000, verbose=True)
    # learner(Bot, init=True, iter=10000, verbose=True)