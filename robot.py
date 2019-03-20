"""
The Robot module handles behaviors for each
robot

@author: Dillon O'Leary
"""
import threading
import random
import json
from queue import Queue
from typing import Dict, Any
from abc import ABC, abstractmethod
from utils import Bcolors, convert_to_sec, update_interface
from main import NUM_TASKS

# Globals
to_do = {}  # the remaining tasks
notifications = []  # the notifications
busy_robots = {}  # the robots doing tasks
free_robots: Dict[Any, Any] = {}  # the robots available to work
prompt = ""  # the input prompt
bot_threads = []  # all the threads running
# active_threads_lock = threading.Lock()
list_lock = threading.Lock()

# Set up all the hard coded values
with open('config.json', 'r') as json_file:
    json = json.load(json_file)
    adverbs = json["adverbs"]
    robot_types = json["robot_types"]
    tasks = json["tasks"]
    start_verbs = json["start_verbs"]


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
        # for automatic task assignment
        self.queued_tasks = Queue()  # used for auto task assignment
        self.attempted_task_id = -1  # counter for attempted task id

    def get_available_task(self):
        """
        Iterate through all the tasks in
        the to do list. This is done in case
        there are tasks that a robot cannot
        complete. When the attempted task is
        beyond the ids in the to do list, the
        robot is no longer useful and taken off
        of free_robots
        :return: a task id
        """
        self.attempted_task_id += 1
        while self.attempted_task_id not in to_do:
            self.attempted_task_id += 1
            if self.attempted_task_id > NUM_TASKS:
                free_robots.pop(self.id)
                return -1
        return self.attempted_task_id

    def get_task_from_queue(self):
        """
        Return the first task from the queue if possible
        otherwise just choose one from the to_do
        :return:
        """
        if not self.queued_tasks.empty():
            task_id = self.queued_tasks.get()
        else:
            task_id = self.get_available_task()
        return task_id

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

    @abstractmethod
    def screen_task(self, desc):
        """
        Check to see if the task is
        specially handled by this type of robot
        :param desc: task description
        :return:
        """
        pass

    def complete_task(self, desc):
        """
        Run once eta has passed
        :param desc: task description
        """
        notifications.append(Bcolors.OKGREEN +
                             '{} the {} completed: {}\n'.format(self.name, self.robo_type, desc)
                             + Bcolors.ENDC)
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
        bot_threads.append(activity)  # append to threads that have run
        notifications.append(Bcolors.OKBLUE +
                             '{} {} {} to {}.\n'.format(self.name,
                                                        self.get_task_adverb(),
                                                        start_verbs[
                                                            random.randint(0, len(start_verbs) - 1)],
                                                        to_do[task_id]["description"])
                             + Bcolors.ENDC)
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
    notifications.append(Bcolors.WARNING +
                         "A {} cannot {}, {}!\n".format(robot_type, desc, excuse) +
                         Bcolors.ENDC)
    raise ActionExecutionError


class Unipedal(Robot):
    def screen_task(self, desc):
        problem_task = "mow the lawn"
        excuse = "all the walking tires it out"
        if desc == problem_task:
            handle_problem_task(self.robo_type, desc, excuse)


class Bipedal(Robot):
    def screen_task(self, desc):
        problem_task = "bake some cookies"
        excuse = "it never learned to cook"
        if desc == problem_task:
            handle_problem_task(self.robo_type, desc, excuse)


class Quadrupedal(Robot):
    def screen_task(self, desc):
        problem_task = "do the dishes"
        excuse = "it's clumsy and the dishes will break"
        if desc == problem_task:
            handle_problem_task(self.robo_type, desc, excuse)


class Arachnid(Robot):
    def screen_task(self, desc):
        problem_task = "give the dog a bath"
        excuse = "all the legs freak out the dog"
        if desc == problem_task:
            handle_problem_task(self.robo_type, desc, excuse)


class Radial(Robot):
    def screen_task(self, desc):
        problem_task = "do the laundry"
        excuse = "it always gets wrapped up in the blankets"
        if desc == problem_task:
            handle_problem_task(self.robo_type, desc, excuse)


class Aeronautical(Robot):
    def screen_task(self, desc):
        problem_task = "rake the leaves"
        excuse = "they blow away"
        if desc == problem_task:
            handle_problem_task(self.robo_type, desc, excuse)
