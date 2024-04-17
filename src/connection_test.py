from task import *
import time
import math

# doc sphinx

def get_robot_state(robot="localhost"):
    #"""Get the state of the robot.
    
    #:param robot: The hostname or IP address of the robot, defaults to "localhost"
    #:type robot: str, optional
    #:return: The overall status of the robot, which is set to 'Idle' in this case.
    #:rtype: Any (replace with the actual type)
    #"""
    """Get the state of the robot.

    This function retrieves the overall status of the specified robot by calling a method 
    using the `call_method` function.

    :param robot: The hostname or IP address of the robot. Defaults to "localhost".
    :type robot: str, optional

    :return: A dictionary containing information about the robot's state.
             The keys in the dictionary represent different aspects of the robot's state.
             - 'O_T_EE': Transformation matrix or pose of the end effector.
             - 'current_task': The current task the robot is performing (e.g., 'IdleTask').
             - 'error_message': Any error message related to the robot's state (currently an empty string).
             - 'grasped_object': The object currently grasped by the robot ('NullObject' if none).
             - 'gripper_width': The width of the gripper.
             - 'q': Joint positions or angles of the robot.
             - 'result': The result of the state retrieval operation (True).
             - 'status': The status of the robot (e.g., 'UserStopped').
    :rtype: dict
    """
   
    
    return call_method(robot, 12000, "get_state")


def get_EE_pose(robot="localhost"):
    
    """Get the pose of the end effector of the robot.

    This function retrieves the transformation matrix or pose of the end effector
    from the robot's state information.

    :param robot: The hostname or IP address of the robot. Defaults to "localhost".
    :type robot: str, optional

    :return: The transformation matrix or pose of the end effector.
    :rtype: list
    """
    robot_state = get_robot_state(robot)
    
    # Extract the end effector pose from the robot state
    ee_pose = robot_state.get('result', {}).get('O_T_EE', [])

    return ee_pose

    
def get_joint_state(robot="localhost"):
    """Get the joint state of the robot.

    This function retrieves the joint positions or angles from the robot's state information.

    :param robot: The hostname or IP address of the robot. Defaults to "localhost".
    :type robot: str, optional

    :return: The joint positions 
    :rtype: list
    """
    robot_state = get_robot_state(robot)
    
    # Extract the joint positions or angles from the robot state
    joint_state = robot_state.get('result', {}).get('q', [])

    return joint_state

def lock_robot(robot="localhost"):
    """Lock the robot_gripper.

    :param robot: The hostname or IP address of the robot, defaults to "localhost"
    :type robot: str, optional
    :return: The result of the lock operation
    :rtype: Any (replace with the actual type)
    """
    return call_method(robot, 12000, "lock_brakes")

def unlock_robot(robot="localhost"):
    """Unlock the robot_gripper.

    :param robot: The hostname or IP address of the robot, defaults to "localhost"
    :type robot: str, optional
    :return: The result of the unlock operation
    :rtype: Any (replace with the actual type)
    """
    return call_method(robot, 12000, "unlock_brakes")