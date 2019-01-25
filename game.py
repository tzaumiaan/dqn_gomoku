import numpy as np

class gomoku():
  def __init__(self, board_size, win_size):
    self.board_size = board_size
    self.win_size = win_size
    self.board = np.zeros([board_size, board_size]).astype(np.uint)
    self.history = []
    self.winner = 0

  def vis_board(self):
    for i in range(self.board_size):
      for j in range(self.board_size):
        print(self.board[i,j], end='')
      print()
  
  def replay(self, upto=None):
    # backup self.board and self.winner
    bak_board, bak_winnder = self.board, self.winner
    
    # start to replay
    self.board = np.zeros(bak_board.shape).astype(np.uint)
    self.winner = 0
    for i, (pid, move) in enumerate(self.history):
      if upto is not None:
        if i >= upto:
          break
      print('replay step={}, pid={} move={}'.format(i, pid, move))
      self.step(pid, move, replay_mode=True)
      self.vis_board() 
      win = self.evaluate_move(pid, move)
      print('replay step={}, pid={} wins? {}'.format(i, pid, win))
    
    # keep the data as original
    self.board, self.winner = bak_board, bak_winnder
    print('replay ends')

  def step(self, pid, pos, replay_mode=False):
    assert self.board[pos]==0, 'step: invalid move'
    self.board[pos] = pid
    if replay_mode==False:
      self.history.append((pid, pos))
  
  def get_history(self):
    return self.history

  def get_valid_moves(self):
    return np.argwhere(self.board == 0)
  
  def evaluate_move(self, pid, pos):
    assert self.board[pos]==pid, 'evaluate_move: invalid request'
    assert self.winner==0, 'evaluate_move: already game over'
    pad_size = self.win_size - 1
    pad_board = np.pad(self.board, pad_size, 'constant', constant_values=0)
    patch = pad_board[pos[0]:pos[0]+2*self.win_size-1, pos[1]:pos[1]+2*self.win_size-1]
    vecs = [patch[:,self.win_size-1], # horizontal line
            patch[self.win_size-1,:], # vertical line
            np.diag(patch), # diagonal line
            np.diag(np.fliplr(patch))] # anti-diagonal line
    target = (np.ones(self.win_size) * pid).astype(np.uint) 
    for v in vecs:
      for i in range(self.win_size):
        if(np.array_equal(v[i:i+self.win_size], target)):
          self.winner = pid
          break
    return (self.winner==pid)

