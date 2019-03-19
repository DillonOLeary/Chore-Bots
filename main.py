"""
This module handles the main functionality
of the program
"""
import multiprocessing
import os
import robot
from time import *


def get_input_id(prompt):
    """
    Get an id from the user
    :param prompt:
    :return: the id
    """
    robot.prompt = prompt
    robot_id = input(prompt)
    while not robot_id.isdigit():
        robot_id = input(prompt)
        print("Input must be a digit, try again")
    return int(robot_id)


def get_robot_name():
    """
    Get the name of the robot
    :return: the name of the robot
    """
    return input("Enter a robot name: ")


def get_robot_type():
    """
    Get the type of the robot
    indexing
    :return:
    """
    for i, elem in enumerate(robot.robot_types):
        print("{}: {}".format(i, elem))
    type_id = -1
    while type_id >= len(robot.robot_types) or type_id < 0:
        type_id = get_input_id("Select a type by index: ")
    return robot.robot_types[type_id]


def create_robot():
    """
    Create a robot of the correct type
    :return:
    """
    print("")  # Blank line
    name = get_robot_name()
    robo_type = get_robot_type()
    # Create a robot of the given type
    if robo_type == 'Unipedal':
        robo = robot.Unipedal(name, robo_type)
    elif robo_type == 'Bipedal':
        robo = robot.Bipedal(name, robo_type)
    elif robo_type == 'Quadrupedal':
        robo = robot.Quadrupedal(name, robo_type)
    elif robo_type == 'Arachnid':
        robo = robot.Arachnid(name, robo_type)
    elif robo_type == 'Radial':
        robo = robot.Radial(name, robo_type)
    elif robo_type == 'Aeronautical':
        robo = robot.Aeronautical(name, robo_type)
    else:
        raise RuntimeError("Robot type is not one that is available")
    print("{} the {} has been activated".format(name, robo_type))
    return robo


def get_robots():
    ret_bots = {}  # Robot dictionary
    for num in range(NUM_ROBOTS):
        ret_bots[num] = create_robot()

    return ret_bots


def setup():
    """
    Create the tasks
    """
    for i in range(NUM_TASKS):
        robot.to_do[i] = (robot.tasks[robot.random.randint(0, len(robot.tasks) - 1)])


def get_task_assignment():
    """
    Get the robot assignment
    :return: the robot that should do work
    :return: the task that should be done
    """
    valid_input = False
    robot_id = -1
    assignment_id = -1
    robot.update_interface(robot.to_do, robot.free_robots, robot.notifications)
    while not valid_input:
        robot_id = get_input_id("Choose a robot by id: ")
        if robot_id in robot.free_robots:
            assignment_id = get_input_id("Choose a task by id "
                                         "for {}: ".format(robot.free_robots[robot_id].name))
            if assignment_id in robot.to_do:
                robot.valid_input = True
                robot.prompt = ""
                break
        print("Input '{}' out of range, try again".format(robot_id))
    return robot_id, assignment_id


def introduce_program():
    """
    Output the strings that introduce the
    program to the user and create the robots
    :return:
    """
    print("Oh no! Mom's gonna be home in two minutes and you "
          "haven't done any of your chores!")
    print("Luckily you have your secret army of "
          "chore robots. ")
    print("Complete all the tasks by before mom arrives"
          "to avoid a stern talking to\n")
    print("First, assemble your forces")
    robot.free_robots = get_robots()
    input("Press Enter to get to work!!...")


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
    # start_time = time()

    # FIXME you cannot win with this conditional

    while len(robot.to_do) > 0:
        robot_id, assignment_id = get_task_assignment()
        try:
            robot.free_robots[robot_id].begin_task(assignment_id)
        except robot.ActionExecutionError:
            continue

if __name__ == "__main__":
    # how much time until program stops
    MAX_TIME = 120
    NUM_ROBOTS = 2  # How many robots
    NUM_TASKS = 10  # How many tasks to complete
    setup()
    introduce_program()

    # Create a thread which just sends a signal back to main when
    # the time is up. This signal is handled by main by halting all program
    # execution, ending the threads, and finishing the program

    # TODO have the two robots randomly complete 5 tasks each
    # TODO instead of user input, it just takes input from two queues
    # User create queues before execution? Maybe during execution
    # if all robots cannot do task end the program
    # if a task is unacomplishable by the robot, reassign it
    # Start foo as a process
    p = multiprocessing.Process(target=run, name="Run")
    p.start()

    # Wait 10 seconds for foo
    sleep(10)

    # Terminate foo
    # Terminate all bot threads, whether or not they have already been terminated
    p.terminate()

    # Cleanup
    p.join()
    # run()
    if len(robot.to_do) > 0 or len(robot.busy_robots) > 0:
        failure()
    else:
        success()
    # FIXME this works but I don't think it is the best way to
    # FIXME exit all threads
    os._exit(1)

#