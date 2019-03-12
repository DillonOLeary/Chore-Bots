"""
The Robot module handles behaviors for each
robot
"""
import threading
import random
import json


class Robot:
    # used for ids
    num_robots = 0

    def __str__(self):
        return "id:{} name:{} type:{}".format(self.id,
                                              self.name,
                                              self.robo_type)

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
        :param task_id: the task assigned
        :param desc: task description
        """
        # TODO print to a certain output
        print('{} the {} completed: {}'.format(self.name,
                                               self.robo_type, desc))
        list_lock.acquire()
        del busy_robots[self.id]
        list_lock.release()
        free_robots[self.id] = self

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
        print('{} {} {} to {}.'.format(self.name,
                                              self.get_task_adverb(),
                                              start_verbs[random.randint(0, len(start_verbs) - 1)],
                                              to_do[task_id]["description"]))
        del to_do[task_id]


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
        ret_str += "{}: {} {}\n".format(key,
                                        val["description"],
                                        val["eta"])
    print(ret_str)

def print_robots(robots):
    """
    Proper print of robot list
    :param robots: the list of robots
    :return:
    """
    ret_str = ""
    for i in robots:
        ret_str += "{}: {} {}\n".format(robots[i].id,
                                        robots[i].name,
                                        robots[i].robo_type)
    print(ret_str)

if __name__ == "__main__":
    to_do = {}
    for i in range(10):
        to_do[i] = (tasks[random.randint(0, len(tasks) - 1)])

    free_robots = {0:Robot("Rllen", robot_types[0]),
              1:Robot("Yeth", robot_types[4])}
    busy_robots = {}
    while len(to_do) > 0:
        valid_input = False
        robot_id = -1
        assignment_id = -1
        while not valid_input:
            print_robots(free_robots)
            robot_id = input("Choose a robot by id: ")
            if not robot_id.isdigit():
                print("Improper input, try again")
                continue
            robot_id = int(robot_id)
            if robot_id in free_robots:
                print_tasks(to_do)
                assignment_id = input("Choose a task by id: ")
                if not assignment_id.isdigit():
                    print("Improper input, try again")
                    continue
                assignment_id = int(assignment_id)
                if assignment_id in to_do:
                    valid_input = True
                    break
            print("Improper input, try again")
        free_robots[robot_id].begin_task(assignment_id)

