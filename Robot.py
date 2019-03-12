"""
This abstract class defines the behavior that
each type of robot must implement
"""
import threading
import random
import json


def convert_to_sec(milli):
    """
    Convert from milliseconds to seconds
    :param milli: time in milliseconds
    :return: time in seconds
    """
    return milli / 1000


class Robot:
    def __init__(self, name, robo_type):
        """
        This initialized a robot of a certain type
        :param name: The name of the robot
        :param robo_type: the type of robot
        """
        self.name = name
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

    def complete_task(self, task_desc):
        """
        Run once eta has passed
        :param task_desc: a description of the task
        """
        # TODO print to a certain output
        print('{} completed: {}'.format(self.name, task_desc))

    def begin_task(self, task_desc, eta):
        """
        This method will create a thread
        to complete the task provided
        :param task_desc:
        :param eta:
        :return:
        """
        activity = threading.Timer(convert_to_sec(eta), self.complete_task, [task_desc])
        activity.start()
        print('{} {} begins to {}.'.format(self.name, self.get_task_adverb(), task_desc))


# TODO put in JSON
with open('adverbs.json', 'r') as json_file:
    adverbs = json.load(json_file)

if __name__ == "__main__":
    robo_1 = Robot("Allen", "quad")
    robo_2 = Robot("Beth", "uno")
    robo_1.begin_task("mow the lawn", 5000)
    robo_2.begin_task("do dishes", 3000)
