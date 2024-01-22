#!/usr/bin/python3 -u
from task import *
from ws_client import *
import numpy as np


def teach_location(robot: str, location: str):
    
    """

    :param robot: The robot object that will be taught the location.
    :type robot: str
    :param location: The name or identifier of the location to be taught.
    :type location: str
    """
    call_method(robot, 12000, "teach_object", {"object": location})

def move_to_joint(robot: str, q_g: list):
    
    """Move the robot to a specified joint configuration.

    Parameters:
    - robot (str): The identifier or name of the robot.
    - q_g (list): The target joint configuration.

    Returns:
    The result of the movement operation.
    """
    parameters = {
        "parameters": {
        "pose": "NoneObject",
        "q_g": q_g,
        "speed": 0.5,
        "acc": 0.7,        
        }       
    }
    return start_task_and_wait(robot, "MoveToJointPose", parameters, False)

def move_to_location(robot: str, location: str):
    
    """

    :param robot: The robot object that will perform the movement.
    :type robot: str
    :param location: The name or identifier of the target location.
    :type location: str
    """
    context = {
        "skill": {
            "p0":{
                "dX_d": [0.1, 0.5],
                "ddX_d": [0.5, 1],
                "K_x": [1500, 1500, 1500, 150, 150, 150],

            },
            "objects": {
                    "GoalPose": location
                }
        },
        "control": {
            "control_mode": 2
        }
    }
    t = Task(robot)
    t.add_skill("move", "TaxMove", context)
    t.start()
    result = t.wait()
    print("Result: " + str(result))


def move_to_cart(robot, R, T):
    #Here R is a 3x3 rotation matrix, T is a 3x1 translation vector
    call_method(robot, 12000, "teach_object", {"object": "tmp"})
    print(R)
    payload = {
        "object": "tmp",
        "data": {
            "x": T[0],
            "y": T[1],
            "z": T[2],
            "R": np.reshape(R, (-1,)).tolist(),
        },
    }
    call_method(robot, 12000, "set_partial_object_data", payload)
    move_to_location(robot, "tmp")

def test_move_to_cart():
    goal = np.array([0.8806477623571686,
   -0.2836747863438268,
   -0.379432314318779,
   0.0,
   -0.3086662673892797,
   -0.9511455266573038,
   -0.00529805596215621,
   0.0,
   -0.3593993430914907,
   0.12178602207388385,
   -0.9252028302014778,
   0.0,
   0.3533251717402699,
   -0.10562543811627921,
   0.22412871727639294,
   1.0])
    goal = np.reshape(goal, (4,4))
    
    move_to_cart("localhost", goal[:3,:3], goal[3,:3])


#def test_robot_movement():
    #robot_object = "Robot1"  # Replace with the actual robot object or identifier

    # Teach a location
    #location_to_teach = "Kitchen"  # Replace with the location you want to teach
    #teach_location(robot_object, location_to_teach)

    # Move to the taught location
    #target_location = "Kitchen"  # Replace with the location you want to move to
    #move_to_location(robot_object, target_location)

# Call the testing function
#test_robot_movement()
    
#def test_robot_movement(robot: str, location1: str, location2: str):
    # Teach a location1
    #teach_location(robot, location1)
    #call_method(robot, 12000, "teach_object", {"object": location2})

    # Teach a location2
    #teach_location(robot, location2)
    #call_method(robot, 12000, "teach_object", {"object": location2})
    # Move to the taught location
    #move_to_location(robot, location1)
    #move_to_location(robot, location2)

def teach_location_with_pause(robot: str, location: str):
    # Display a message and wait for user input
    input("Please move the robot and press Enter to continue...")

    # Execute the operation to teach the robot location
    teach_location(robot, location)  # Placeholder for the teach_location function



def test_robot_movement(robot: str, location1: str, location2: str):
    # Teach the robot location1 with a pause
    teach_location_with_pause(robot, location1)

    # Display a message and wait for user input (e.g., to press the lock button)
    #input("Please press the lock button or perform any necessary actions, and then press Enter to continue...")

    # Teach the robot location2 with a pause
    teach_location_with_pause(robot, location2)

    # Display a message and wait for user input (e.g., to press the lock button)
    input("Please release the external activation device and then press Enter to continue...")

    # Move to the taught locations
    move_to_location(robot, location1)
    move_to_location(robot, location2)

