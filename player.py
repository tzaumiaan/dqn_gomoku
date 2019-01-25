import random

class player():
  def __init__(self, pid):
    self.pid = pid
  
  def get_pid(self):
    return self.pid

  def evaluate(self, game):
    pass
  
  def act(self, game):
    # randomly pick from valid moves
    move = random.choice(game.get_valid_moves())
    return (move[0], move[1])

