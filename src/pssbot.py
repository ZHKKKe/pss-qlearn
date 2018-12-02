from third_party.flappybird_qlearning_bot.bot import Bot


class PSSBot(Bot):
    def __init__(self):
        super().__init__()
        self.right_samples = []

    