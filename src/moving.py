#!/usr/bin/python3 -u
from task import *
from ws_client import *
import numpy as np


def teach_location(robot: str, location: str):
    #TODO: @zewei write a small testing function which consists of teach_location & move_to_location
    """

    :param robot: The robot object that will be taught the location.
    :type robot: str
    :param location: The name or identifier of the location to be taught.
    :type location: str
    """
    call_method(robot, 12000, "teach_object", {"object": location})

def move_to_joint(robot: str, q_g: list):
    # TODO: @zewei
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
    #TODO:
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