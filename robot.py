"""
The Robot module handles behaviors for each
robot
"""
import threading
import random
import json
from typing import Dict, Any
from abc import ABC, abstractmethod
from bcolors import Bcolors

# FIXME how should I store the global variables?
# Globals
to_do = {}  # the remaining tasks
notifications = []  # the notifications
busy_robots = {}  # the robots doing tasks
free_robots: Dict[Any, Any] = {}  # the robots available to work
prompt = ""


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

    def screen_task(self):
        """
        Check to see if the task is
        specially handled by this type of robot
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
        update_interface()
        print(prompt)

    # @abstractmethod
    def begin_task(self, task_id):
        """
        This method will create a thread
        to complete the task provided
        :param task_id: the task assigned
        :return:
        """

        self.screen_task()


        list_lock.acquire()
        del free_robots[self.id]
        busy_robots[self.id] = self
        list_lock.release()
        activity = threading.Timer(convert_to_sec(to_do[task_id]["eta"]),
                                   self.complete_task, [to_do[task_id]["description"]])
        activity.start()
        notifications.append(Bcolors.OKBLUE + '{} {} {} to {}.\n'.format(self.name,
                                                        self.get_task_adverb(),
                                                        start_verbs[random.randint(0, len(start_verbs) - 1)],
                                                        to_do[task_id]["description"]) + Bcolors.ENDC)
        del to_do[task_id]


class Unipedal(Robot):
    def __init__(self, name, type):
        super().__init__(name, type)

    def screen_task(self):
        notifications.append(Bcolors.HEADER + "TESTTT\n" + Bcolors.ENDC)






def convert_to_sec(milli):
    """
    Convert from milliseconds to seconds
    :param milli: time in milliseconds
    :return: time in seconds
    """
    return milli / 1000


# Set up all the hard coded values
with open('config.json', 'r') as json_file:
    json = json.load(json_file)
    adverbs = json["adverbs"]
    robot_types = json["robot_types"]
    tasks = json["tasks"]
    start_verbs = json["start_verbs"]

list_lock = threading.Lock()


def print_tasks(task_list):
    """
    Proper print of tasks
    :param task_list: list of tasks
    :return:
    """
    ret_str = Bcolors.BOLD + "\nTasks Left To Do:\n" + Bcolors.ENDC
    for key, val in task_list.items():
        ret_str += "{}: {}, eta {} seconds\n".format(key,
                                                     val["description"],
                                                     convert_to_sec(val["eta"]))
    return ret_str


def print_robots(robots):
    """
    Proper print of robot list
    :param robots: the list of robots
    :return:
    """
    ret_str = Bcolors.BOLD + "Robots Available:\n" + Bcolors.ENDC
    for index in robots:
        ret_str += "{}: {} {}\n".format(robots[index].id,
                                        robots[index].name,
                                        robots[index].robo_type)
    return ret_str


def print_notifications(notif_list):
    """
    Print out recent notifications
    :param notif_list: list of notifications
    :return:
    """
    ret_str = Bcolors.BOLD + "Notifications:\n" + Bcolors.ENDC
    if len(notif_list) > 4:
        notif_list = list(reversed(notif_list))[:3]
        notif_list = list(notif_list)
        notif_list.append("...\n")

    for elem in notif_list:
        ret_str += elem
    return ret_str


def update_interface():
    """
    Call whenever there is a change to
    the interface
    :return:
    """
    for x in range(20):
        print("\n")
    print(print_tasks(to_do))
    print(print_robots(free_robots))
    print(print_notifications(notifications))
