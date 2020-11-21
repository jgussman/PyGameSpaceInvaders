import tensorflow as tf
from tensorflow import keras
from random import randint
import os

class QLearningNet:
    def __init__(self, name='QLearningNet',previousModel = False,randomActions = False,filepath = "spaceinvaders/models/model.h5"):
        self.state_size = [120,140,4]
        self.action_size = 3
        self.learning_rate = 0.000025
        self.gamma = .99
        self.randomMode = False
        self.randomModeCounter = 30
        self.lastmoves = []
        self.loss = keras.losses.Huber()
        self.optimizer = keras.optimizers.Adam(self.learning_rate,clipnorm = 1.0)
        if not previousModel:
          self.predict_model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(16,(5,5),input_shape = (120,100,1),padding='valid'),
            tf.keras.layers.Conv2D(64,(3,3),activation= 'relu',padding = 'valid'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(3,activation = 'relu')
          ])
          self.target_model = tf.keras.models.clone_model(self.predict_model)
          self.predict_model.compile(optimizer='adam',loss = 'mean_squared_error')
          self.target_model.compile(optimizer= 'adam')
        else:
          self.predict_model = tf.keras.models.load_model(filepath)
          self.target_model = tf.keras.models.clone_model(self.predict_model)
          self.target_model.compile(optimizer='adam')
        self.random_actions = randomActions
          


    def feedForward(self,frameStack):
      possible_actions = [1,2,3]
      Qs = self.predict_model.predict(frameStack)
      choice = tf.reduce_sum(Qs,0)
      max_choice = tf.argmax(choice)
      move = None
      if self.random_actions or all([i==0 for i in choice]):
        move = randint(1,3)
      else:
        move = possible_actions[max_choice]
      if sum([i == move for i in self.lastmoves]) > 30 and not self.randomMode:
        self.randomMode = True
      if self.randomModeCounter == 0:
        self.randomMode = False
        self.randomModeCounter = 30
        self.lastmoves = []
      if self.randomMode:
        move = randint(1,3)
        self.randomModeCounter -= 1
      self.lastmoves.append(move)
      if randint(1,20) == 10:
        print(self.randomMode)
      return move


    def train(self,batch,target_update):
      """
      Takes in batch (64 length list with [(reward,action,state),...()])
      returns VOID trains the model
      """

      #init decay rate
      for point in batch:
        reward,state = point
        
        # Feed forward in target net
        Q_target = self.target_model.predict(state)
        # add reward to target net values
        Q_update = reward + self.gamma * Q_target
        with tf.GradientTape() as tape:
          q_values = self.predict_model(state)
          # Find the loss 
          loss = self.loss(max(Q_update),max(q_values))
        # update weights in predict using backpropogation
        if loss > 0:
          grads = tape.gradient(loss,self.predict_model.trainable_variables)
          self.optimizer.apply_gradients(zip(grads,self.predict_model.trainable_variables))

      # Copy predict weights to target
      if target_update == True:
        print('updates weights')
        self.target_model.set_weights(self.predict_model.get_weights())

    def store_weights(self,filepath = "spaceinvaders/models/model.h5"):
      """
      Stores the weights in some way to call again
      """
      self.predict_model.save(filepath)
      

class RandomPlayer:


  def __init__(self):
    """
    No instance variables
    """

  def feedForward(self,inputVector):
    return randint(1,3)  

