"""
The Robot module handles behaviors for each
robot
"""
import threading
import random
import json


class Robot:
    def __init__(self, name, robo_type):
        """
        This initialized a robot of a certain type
        :param name: The name of the robot
        :param robo_type: the type of robot
        """
        self.name = name
        self.robo_type = robo_type
        self.busy = False  # if the robot is busy

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

    def complete_task(self, task_desc):
        """
        Run once eta has passed
        :param task_desc: a description of the task
        """
        # TODO print to a certain output
        print('{} the {} completed: {}'.format(self.name,
                                               self.robo_type, task_desc))
        self.busy = False

    def begin_task(self, task_desc, eta):
        """
        This method will create a thread
        to complete the task provided
        :param task_desc: the task assigned
        :param eta: the time to completion
        :return:
        """
        activity = threading.Timer(convert_to_sec(eta), self.complete_task, [task_desc])
        self.busy = True
        activity.start()
        print('{} the {} {} {} to {}.'.format(self.name, self.robo_type,
                                              self.get_task_adverb(),
                                              start_verbs[random.randint(0, len(start_verbs) - 1)],
                                              task_desc))


with open('config.json', 'r') as json_file:
    json = json.load(json_file)
    adverbs = json["adverbs"]
    robot_types = json["robot_types"]
    tasks = json["tasks"]
    start_verbs = json["start_verbs"]


def convert_to_sec(milli):
    """
    Convert from milliseconds to seconds
    :param milli: time in milliseconds
    :return: time in seconds
    """
    return milli / 1000


if __name__ == "__main__":
    to_do = []
    for i in range(10):
        to_do.append(tasks[random.randint(0, len(tasks) - 1)])
    print(to_do)
    robots = [Robot("Zllen", robot_types[0]),
              Robot("Geth", robot_types[4])]
    while len(to_do) > 0:

    robo_1.begin_task("mow the lawn", 5000)
    robo_2.begin_task("do dishes", 3000)
