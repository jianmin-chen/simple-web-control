`simple-web-controls` is just the Gradio sliders but not the actual connection to robot, `ardupilot` takes care of the actual connection + sending data to robot.

turn `dance_template.py` into full fledged thing

* donuts
* crabs
* going straight
* encapsulate into oop? or avoid oop
* force_disarm, can't tell if gradio ui error or what
* fun: write parser to take instructions like `forward`, `right`, `down`, `up` (like a freakin turtle) so we can abstract it

[set of config]
forward 50
right 

what is important in a config?

* size of pool, which matters for max speed at given time (bc u don't want it to crash into a wall, the first step to minimizing that risk is to make it slower imho)
* but what if i want to add machine learning? basically you forgot about the 15 billion other sensors that also matter (maybe that's what makes the robot so expensive lol) 
