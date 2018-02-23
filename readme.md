![data visualization samples](https://github.com/Ardibid/AnkiLearning/blob/master/Media/00.png)

Anki Learn is a project aimed to add a custom object detection to Cozmo's Anki robots. It is based on project [CozmoPedia](https://github.com/touretzkyds/cozmopedia/wiki) developed by prof. Dave Touretzky and used in [Cognitive Robotics](http://www.cs.cmu.edu/afs/cs/academic/class/15494-s17) course at Carnegie Mellon University.

## Project Architecture
![Project Architecture](https://github.com/Ardibid/AnkiLearning/blob/master/Media/01.png)

## Image Classification
For the image classification, I used transfer lerning to over Inception model to train the model with images taken from the Cozmo's onboard caemra. 
![Image Classification](https://github.com/Ardibid/AnkiLearning/blob/master/Media/02-1.png)
![Image Classification Results](https://github.com/Ardibid/AnkiLearning/blob/master/Media/03.png)


## Image Detection and Turning towards the object
For image detection, I used slicing technique to divide the image into vertical slices and find the object in them. The processed data would be used by the state machine to direct the robot.
![Image Detection](https://github.com/Ardibid/AnkiLearning/blob/master/Media/02-2.png)

The overall architecture is illustrated here:
![Image Detection](https://github.com/Ardibid/AnkiLearning/blob/master/Media/02-0.png)

You can find more info in this [slideshow](https://github.com/Ardibid/AnkiLearning/blob/master/Media/AnkiWhere.gslides). 






