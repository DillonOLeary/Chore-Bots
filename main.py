"""
This module handles the main functionality
of the program
"""
import os
import Robot
from time import *


def setup():
    """
    Instantiate the robots and create the
    tasks
    """
    for i in range(5):
        Robot.to_do[i] = (Robot.tasks[Robot.random.randint(0, len(Robot.tasks) - 1)])
    Robot.free_robots = {0: Robot.Robot("Rllen", Robot.robot_types[0]),
                         1: Robot.Robot("Yeth", Robot.robot_types[4])}


def get_input_id(prompt):
    """
    Get an id from the user
    :param prompt:
    :return: the id
    """
    Robot.prompt = prompt
    robot_id = input(prompt)
    while not robot_id.isdigit():
        robot_id = input(prompt)
        print("Input must be a digit, try again")
    return int(robot_id)


def get_task_assignment():
    """
    Get the robot assignment
    :return: the robot that should do work
    :return: the task that should be done
    """
    valid_input = False
    robot_id = -1
    assignment_id = -1
    Robot.update_interface()
    while not valid_input:
        robot_id = get_input_id("Choose a robot by id: ")
        if robot_id in Robot.free_robots:
            assignment_id = get_input_id("Choose a task by id "
                                         "for {}: ".format(Robot.free_robots[robot_id].name))
            if assignment_id in Robot.to_do:
                Robot.valid_input = True
                Robot.prompt = ""
                break
        print("Input '{}' out of range, try again".format(robot_id))
    return robot_id, assignment_id


def introduce_program():
    """
    Output the strings that introduce the
    program to the user
    :return:
    """
    print("Oh no! Mom's gonna be home in two minutes and you "
          "haven't done any of your chores!")
    print("Luckily you have your secret army of "
          "chore robots. ")
    print("Complete all the tasks by before mom arrives"
          "to avoid a stern talking to\n")
    input("Press Enter to continue...")


def failure():
    """
    User doesn't complete chores in time
    """
    print("\n\nMom arrived and you didn't finish!")
    print("She does NOT look happy...")


def success():
    """
    User completes chores in time
    """
    print("Mom arrives home, impressed you did all that work!")


def run():
    """
    Main loop of the program. Ends when the user
    has completed all the tasks or when the time
    runs out
    """
    start_time = time()

    while len(Robot.to_do) > 0 and time() < start_time + MAX_TIME:
        robot_id, assignment_id = get_task_assignment()
        Robot.free_robots[robot_id].begin_task(assignment_id)
    if len(Robot.to_do) > 0 or len(Robot.busy_robots) > 0:
        failure()
    else:
        success()
    # FIXME this works but I don't think it is the best way to
    # FIXME exit all threads
    os._exit(1)


if __name__ == "__main__":
    # how much time until program stops
    MAX_TIME = 120
    setup()
    introduce_program()
    run()
