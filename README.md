# B351-Final-Project

Repository that serves to host Space Invaders AI project for Intro to AI course at IU.

## Main usage

To see how well the current model plays simply run the spaceinvaders.py file in the terminal 
and a pygame window will appear. If you are using this project and wish to further train the model then uncomment the code in the main section of spaceinvaders.py and uncomment the "TO TRAIN MODEL FURTHER SECTION" and comment out the "TO SEE RESULTS" section.

## Storing models

It may be of interest to save several iterations of the model. This can be done by suplying a filepath argument to the ```.store_weights()``` method in teh training section. An easy usage would be to use model[i] where i represents the iteration of the for loop.

## Retrieving models

If you wish to retrain a model from a certain point, potentially to attempt a different training method then you can supply the optional filepath argument to be the location of the h5 file for which you would like to use.

## Dependencies

This project was built using the following packages
- Tensorflow V2.3.1
- Numpy V1.17.3
- Pygame V2.0.0
- keras V2.4.0

All these dependencies are in the requirements.txt file and can be installed with pip. Please note that running ``` pip -r requirements.txt ``` will install the latest versions of all packages. We are not liable for new versions of software breaking the code. If version errors emmerage please use the specified versions listed above as those are guranteed to work.  

### Side note on Python versions:
This was written in Python 3.8.0 but any version after 3.6 should be fine, although the dependency test has not been conducted so I can not make promises. The other requirement is that a 64 bit version of python should be used as 32 bits is not compatabile with Tensorflow.

## Performance and machine limitions

The most expensive part of the program is fetching the pixel arrays from pygame. Currently the only option is to copy all the values into an array. This 120X100 array is then fed into the CNN which will produce the Q-values and give the appropiate move. This event occurs every second or so, which means the program can be quite hard on software. Some frame drops and stutter occurred on my laptop that has an Intel I5 processor and 8GB of RAM. However no stuttering occurred on an Intel I7 processor and 16 GB of RAM. If stuttering is occuring due to inadequate CPU power, consider using GPU Tensorflow if a GPU is available.
