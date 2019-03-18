"""
The Robot module handles behaviors for each
robot
"""
import threading
import random
import json
from typing import Dict, Any
from abc import ABC, abstractmethod
from utils import Bcolors, update_interface, convert_to_sec

# Globals
to_do = {}  # the remaining tasks
notifications = []  # the notifications
busy_robots = {}  # the robots doing tasks
free_robots: Dict[Any, Any] = {}  # the robots available to work
prompt = ""

# Set up all the hard coded values
with open('config.json', 'r') as json_file:
    json = json.load(json_file)
    adverbs = json["adverbs"]
    robot_types = json["robot_types"]
    tasks = json["tasks"]
    start_verbs = json["start_verbs"]
list_lock = threading.Lock()


class Robot(ABC):
    """
    Abstract class with behavior shared by all robots
    """
    # used for ids
    num_robots = 0

    def __init__(self, name, robo_type):
        """
        This initialized a robot of a certain type
        :param name: The name of the robot
        :param robo_type: the type of robot
        """
        self.name = name
        self.id = Robot.num_robots
        Robot.num_robots += 1
        self.robo_type = robo_type

    def get_task_adverb(self):
        """
        Acquire an ambitious alliteration adverb
        :return: adjective corresponding with robot
        name
        """
        first_letter = self.name[0].lower()
        if first_letter not in adverbs:
            return ""
        letter_adverbs = adverbs[first_letter]  # adverbs associated with that letter
        return letter_adverbs[random.randint(0, len(letter_adverbs) - 1)]

    def screen_task(self, desc):
        """
        Check to see if the task is
        specially handled by this type of robot
        :param desc: task description
        :return:
        """
        pass

    # @abstractmethod
    def complete_task(self, desc):
        """
        Run once eta has passed
        :param desc: task description
        """
        notifications.append(Bcolors.OKGREEN + '{} the {} completed: {}\n'.format(self.name,
                                                                                  self.robo_type, desc) + Bcolors.ENDC)
        list_lock.acquire()
        del busy_robots[self.id]
        free_robots[self.id] = self
        list_lock.release()
        update_interface(to_do, free_robots, notifications)
        print(prompt)

    def begin_task(self, task_id):
        """
        This method will create a thread
        to complete the task provided
        :param task_id: the task assigned
        :return:
        """
        self.screen_task(to_do[task_id]["description"])  # only preforms action if task is a special case
        list_lock.acquire()
        del free_robots[self.id]
        busy_robots[self.id] = self
        list_lock.release()
        activity = threading.Timer(convert_to_sec(to_do[task_id]["eta"]),
                                   self.complete_task, [to_do[task_id]["description"]])
        activity.start()
        notifications.append(Bcolors.OKBLUE + '{} {} {} to {}.\n'.format(self.name,
                                                                         self.get_task_adverb(),
                                                                         start_verbs[
                                                                             random.randint(0, len(start_verbs) - 1)],
                                                                         to_do[task_id]["description"]) + Bcolors.ENDC)
        del to_do[task_id]


class ActionExecutionError(Exception):
    """
    Raise when the action cannot be
    executed by the robot
    """
    pass


def handle_problem_task(robot_type, desc, excuse):
    """
    Each robot has a task it cannot complete
    :param robot_type: the type of robot
    :param desc: the description of the task
    :param excuse: the reason it cannot be completed
    :return:
    """
    notifications.append(Bcolors.HEADER +
                         "{} cannot {}, {}!\n".format(robot_type, desc, excuse) +
                         Bcolors.ENDC)
    raise ActionExecutionError


class Unipedal(Robot):
    # def __init__(self, name, robot_type):
    #     super().__init__(name, robot_type)

    def screen_task(self, desc):
        problem_task = "mow the lawn"
        excuse = "all the walking tires him out"
        if desc == problem_task:
            handle_problem_task(self.robo_type, desc, excuse)


class Bipedal(Robot):
    # def __init__(self, name, robot_type):
    #     super().__init__(name, robot_type)

    def screen_task(self, desc):
        problem_task = "bake some cookies"
        excuse = "she never learned to cook"
        if desc == problem_task:
            handle_problem_task(self.robo_type, desc, excuse)


class Quadrupedal(Robot):
    # def __init__(self, name, robot_type):
    #     super().__init__(name, robot_type)

    def screen_task(self, desc):
        problem_task = "do the dishes"
        excuse = "it's clumsy and the dishes always break"
        if desc == problem_task:
            handle_problem_task(self.robo_type, desc, excuse)


class Arachnid(Robot):
    # def __init__(self, name, robot_type):
    #     super().__init__(name, robot_type)

    def screen_task(self, desc):
        problem_task = "give the dog a bath"
        excuse = "all the legs freak out the dog"
        if desc == problem_task:
            handle_problem_task(self.robo_type, desc, excuse)


class Radial(Robot):
    # def __init__(self, name, robot_type):
    #     super().__init__(name, robot_type)

    def screen_task(self, desc):
        problem_task = "do the laundry"
        excuse = "it gets wrapped up in the blankets"
        if desc == problem_task:
            handle_problem_task(self.robo_type, desc, excuse)


class Aeronautical(Robot):
    # def __init__(self, name, robot_type):
    #     super().__init__(name, robot_type)

    def screen_task(self, desc):
        problem_task = "rake the leaves"
        excuse = "they blow away"
        if desc == problem_task:
            handle_problem_task(self.robo_type, desc, excuse)
