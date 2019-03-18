"""
Utilities for the program.
Includes printing, conversion, and coloring text
"""


def convert_to_sec(milli):
    """
    Convert from milliseconds to seconds
    :param milli: time in milliseconds
    :return: time in seconds
    """
    return milli / 1000


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
    else:
        notif_list = list(reversed(notif_list))
        notif_list = list(notif_list)

    for elem in notif_list:
        ret_str += elem
    return ret_str


def update_interface(to_do, free_robots, notifications):
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


class Bcolors:
    """
    Used to color text
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
