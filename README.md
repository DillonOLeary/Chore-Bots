# BOT-O-MAT
Welcome to bot-o-mat. You've got work to do!!

In this game, you will try to complete all your chores before mom gets home. User input, except robot names, is done through selecting the index of the option you want.

There are two game modes: manual and automatic.
- manual: you assign the robots tasks as the game runs
- automatic: robots are automatically assigned tasks, starting with a queue of 5 tasks

There are two phases of the game:
1. Setup: naming robots and setting their type, selecting a game mode
2. Doing Chores: Either manually assigning the robots chores or allowing the robots to automatically take on their own chores

The game concludes when either the time runs out or all the chores are completed. Keep in mind there are tasks that each robot cannot complete!


## Running the Program
to run, just enter in your terminal
```
python main.py
```

## Files
main.py - the main execution handling
utils.py - utils used by other modules
robot.py - defines the behavior of each robot
data.json - hard coded data, such as task names and adverbs

## Authors
- Scott Hoffman <https://github.com/scottshane>  (program idea)
- Olivia Osby <https://github.com/oosby> (program idea)
- Dillon O'Leary <https://github.com/dillonoleary>
