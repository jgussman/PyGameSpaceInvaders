import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras.layers.convolutional import Conv2D
from tensorflow.python.keras.layers.core import Activation


class QLearningNet:
    def __init__(self, name='QLearningNet'):
        self.state_size = [500,700,4]
        self.action_size = 3
        self.learning_rate = 0.00025
        self.predict_model = tf.keras.Sequential([
          tf.keras.layers.Conv2D(8,(7,7),input_shape = (500,700,1),
                                  strides = (4,4)),
          tf.keras.layers.Conv2D(64,(7,7),activation= 'relu',strides = (4,4)),
          tf.keras.layers.MaxPooling2D(pool_size = (10,10)),
          tf.keras.layers.Dropout(0.25),
          tf.keras.layers.Flatten(),
          tf.keras.layers.Dense(3,activation = 'relu')
        ])
        print(self.predict_model.summary())
        self.target_model = tf.keras.models.clone_model(self.predict_model)

        self.predict_model.compile(optimizer='adam',loss = 'mean_squared_error')
        self.target_model.compile(optimizer= 'adam')

    def feedForward(self,frameStack):
      possible_actions = [1,2,3]
      Qs = self.predict_model.predict(frameStack)
      choice = tf.reduce_sum(Qs,0)
      choice = tf.argmax(choice)
      return possible_actions[choice]

    def train(self,batch):
      """
      Takes in batch (64 length list with [(reward,action,state),...()])
      returns VOID trains the model
      """

      #init decay rate
      decay_step = 0
      for point in batch:
        reward,action,stack_state = point
        

          # Feed forward in predict net


          # Feed forward in target net
          #this should just be self.target_Q. This is from above 


          # add reward to target net values

          # Find the loss 
          # Loss = (Q_target - Predicted_Q)^2

          # update weights in predict
        

        # Copy predict weights to target

    def store_weights(self):
      """
      Stores the weights in some way to call again
      """
      

        
