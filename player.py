from dqn import dqn

import random

class player():
  def __init__(self, pid, board_size, brain=None):
    self.pid = pid
    if brain is not None:
      self.brain = brain(board_size, 'p{}'.format(pid))
  
  def get_pid(self):
    return self.pid

  def evaluate(self, game):
    pass
  
  def act(self, game):
    # randomly pick from valid moves
    move = random.choice(game.get_valid_moves())
    return (move[0], move[1])

