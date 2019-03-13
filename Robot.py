"""
The Robot module handles behaviors for each
robot
"""
import threading
import random
import json
from queue import Queue


class Robot:
    # used for ids
    num_robots = 0

    # def __str__(self):
    # return "id:{} name:{} type:{}".format(self.id,
    #                                       self.name,
    #                                       self.robo_type)

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

    def complete_task(self, desc):
        """
        Run once eta has passed
        :param desc: task description
        """
        # TODO print to a certain output
        notifications.put('{} the {} completed: {}\n'.format(self.name,
                                                                self.robo_type, desc))
        list_lock.acquire()
        del busy_robots[self.id]
        free_robots[self.id] = self
        list_lock.release()
        update_interface()

    def begin_task(self, task_id):
        """
        This method will create a thread
        to complete the task provided
        :param task_id: the task assigned
        :param eta: the time to completion
        :return:
        """
        list_lock.acquire()
        del free_robots[self.id]
        busy_robots[self.id] = self
        list_lock.release()
        activity = threading.Timer(convert_to_sec(to_do[task_id]["eta"]),
                                   self.complete_task, [to_do[task_id]["description"]])
        activity.start()
        notifications.put('{} {} {} to {}.\n'.format(self.name,
                                                        self.get_task_adverb(),
                                                        start_verbs[random.randint(0, len(start_verbs) - 1)],
                                                        to_do[task_id]["description"]))
        del to_do[task_id]
        update_interface()


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
    ret_str = "\n"
    for key, val in task_list.items():
        ret_str += "{}: {}, eta {}\n".format(key,
                                             val["description"],
                                             val["eta"])
    return ret_str


def print_robots(robots):
    """
    Proper print of robot list
    :param robots: the list of robots
    :return:
    """
    ret_str = ""
    for index in robots:
        ret_str += "{}: {} {}\n".format(robots[index].id,
                                        robots[index].name,
                                        robots[index].robo_type)
    return ret_str


def print_notifications(q):
    """
    Print out recent notifications
    :param q: all queued notifications
    :return:
    """
    ret_str = ""
    if not q.empty:
        ret_str += q[-1]
    return ret_str


def update_interface():
    """
    Call whenever there is a change to
    the interface
    :return:
    """
    print(print_tasks(to_do))
    print(print_robots(free_robots))
    print(print_notifications(notifications))
    print(prompt)


if __name__ == "__main__":
    to_do = {}
    notifications = Queue()
    prompt = ""
    for i in range(10):
        to_do[i] = (tasks[random.randint(0, len(tasks) - 1)])

    free_robots = {0: Robot("Rllen", robot_types[0]),
                   1: Robot("Yeth", robot_types[4])}
    busy_robots = {}
    while len(to_do) > 0:
        valid_input = False
        robot_id = -1
        assignment_id = -1
        while not valid_input:
            update_interface()
            prompt = "Choose a robot by id: "
            update_interface()
            robot_id = input()
            if not robot_id.isdigit():
                # notifications.put("Input must be a digit, try again\n")
                print("Input must be a digit, try again")
                continue
            robot_id = int(robot_id)
            if robot_id in free_robots:
                prompt = "Choose a task by id: "
                update_interface()
                assignment_id = input()
                if not assignment_id.isdigit():
                    # notifications.put("Input must be a digit, try again\n")
                    print("Input must be a digit, try again")
                    continue
                assignment_id = int(assignment_id)
                if assignment_id in to_do:
                    valid_input = True
                    break
            # notifications.put("Input '{}' out of range, try again\n".format(robot_id))
            print("Input '{}' out of range, try again".format(robot_id))
        free_robots[robot_id].begin_task(assignment_id)

