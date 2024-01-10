from task import *
import time
import math

# doc sphinx

def get_robot_state(robot="localhost"):
    """Get the state of the robot.
    
    :param robot: The hostname or IP address of the robot, defaults to "localhost"
    :type robot: str, optional
    :return: The overall status of the robot, which is set to 'Idle' in this case.
    :rtype: Any (replace with the actual type)
    """
    
    # TODO: add desciption for the return state, the keys in the return dict
    
    return call_method(robot, 12000, "get_state")


def get_EE_pose():
    # TODO
    pass
    
def get_joint_state():
    # TODO
    pass

def lock_robot(robot="localhost"):
    """Lock the robot.

    :param robot: The hostname or IP address of the robot, defaults to "localhost"
    :type robot: str, optional
    :return: The result of the lock operation
    :rtype: Any (replace with the actual type)
    """
    return call_method(robot, 12000, "lock")

def unlock_robot(robot="localhost"):
    """Unlock the robot.

    :param robot: The hostname or IP address of the robot, defaults to "localhost"
    :type robot: str, optional
    :return: The result of the unlock operation
    :rtype: Any (replace with the actual type)
    """
    return call_method(robot, 12000, "unlock")