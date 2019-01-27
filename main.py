from game import gomoku
from player import player
from dqn import dqn
from config import BOARD_SIZE, WIN_SIZE

def main():
  g = gomoku(board_size=BOARD_SIZE, win_size=WIN_SIZE)
  g.vis_board()
  
  p1 = player(pid=1, board_size=BOARD_SIZE, brain=dqn)
  p2 = player(pid=2, board_size=BOARD_SIZE)
  turn = p1.get_pid()
  
  i = 0
  while True:
    if len(g.get_valid_moves()) == 0:
      print('game draw')
      break

    if turn==p1.get_pid():
      move = p1.act(g)
    elif turn==p2.get_pid():
      move = p2.act(g)
    
    g.step(turn, move)
    win = g.evaluate_move(turn, move)
    print('game step={}, pid={} move={} wins? {}'.format(i, turn, move, win))
    g.vis_board() 

    if win:
      print('game ends, winner={}'.format(turn))
      break
    elif turn==p1.get_pid():
      turn = p2.get_pid()
    elif turn==p2.get_pid():
      turn = p1.get_pid()
    
    i += 1
  
if __name__=='__main__':
  main()
