from config import LEARNING_RATE

import tensorflow as tf
from tensorflow.contrib import slim

def fully_connected_model(
    state_vec, 
    action_dim=None,
    l2_scale=0.0,
    scope='fc_model'):
  # dict for components to be monitored
  end_points = {}
  
  # model build-up
  with tf.variable_scope(scope, 'fc_model', [state_vec]):
    with slim.arg_scope(
        [slim.fully_connected],
        weights_regularizer=slim.l2_regularizer(scale=l2_scale),
        weights_initializer=tf.truncated_normal_initializer(stddev=0.1),
        activation_fn=tf.nn.relu):
      
      net = end_points['fc1'] = slim.fully_connected(state_vec, 64, scope='fc1')
      if not action_dim:
        # without final layer, can be used for transfer learning
        return net, end_points
      logits = end_points['logits'] = slim.fully_connected(
          net, action_dim, activation_fn=None, scope='fc2')
  return logits, end_points

class dqn():
  def __init__(self, board_size, scope='dqn'):
    self.scope = scope
    self.replay_buffer = []
    self.state_dim = board_size**2 + 1
    self.action_dim = board_size**2
    self.create_network()
    self.create_trainer()
    self.session = tf.InteractiveSession()
    self.session.run(tf.global_variables_initializer())
    self.transfer_weights_to_target()

  def create_network(self):
    # placeholder for input
    self.state_input = tf.placeholder('float', [None, self.state_dim])
    # network for q learning
    scope = self.scope+'_q_learning'
    self.q_learning, _ = fully_connected_model(self.state_input, self.action_dim, scope=scope)
    self.q_learning_weights = [v for v in tf.trainable_variables() if v.name.startswith(scope)]
    # network for q target
    scope = self.scope+'_q_target'
    self.q_target, _ = fully_connected_model(self.state_input, self.action_dim, scope=scope)
    self.q_target_weights = [v for v in tf.trainable_variables() if v.name.startswith(scope)]

  def create_trainer(self):
    # placeholder for input
    self.action_input = tf.placeholder("float", [None,self.action_dim]) # one-hot
    self.q_input = tf.placeholder("float", [None])
    # get the q value from one-hot action input
    q_action = tf.reduce_sum(tf.multiply(self.q_learning, self.action_input), reduction_indices=1)
    # loss definition
    loss = tf.reduce_mean(tf.square(self.q_input - q_action))
    # add histograms for trainable variables
    for var_ in tf.trainable_variables():
      tf.summary.histogram(var_.op.name, var_)
    # specify optimizer
    opt = tf.train.GradientDescentOptimizer(LEARNING_RATE)
    # compute gradients and apply
    # note: with batch norm layers we have to use update_ops
    #       to get hidden variables into the list needed
    #       to be trained
    update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
    with tf.control_dependencies(update_ops): 
      grads = opt.compute_gradients(loss)
      # add histograms for gradients
      for grad_, var_ in grads:
        if grad_ is not None:
          tf.summary.histogram(var_.op.name + '/gradients', grad_)
      # train op
      self.train_op = opt.apply_gradients(grads)
  
  def transfer_weights_to_target(self):
    for learning_w, target_w in zip(self.q_learning_weights, self.q_target_weights):
      self.session.run(tf.assign(target_w, learning_w))
	
  def perceive(self, state, action ,reward, next_state, done):
    pass 
 
  def train(self):
    pass
 
  def action(self, state, egreedy=False):
    pass

