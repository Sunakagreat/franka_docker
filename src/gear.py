from task import *
from moving import *
import time
import math

# robot = "10.157.175.17"
robot = "localhost"
   
initJ =  [1.6805736406158316,
   -0.7780998814026686,
   -0.18556492468223312,
   -2.4818779002068383,
   -0.1630406865146425,
   1.9203671494023304,
   0.7846937289967224]
   
appJ = [1.046577663283599,
   0.5408990772481549,
   -0.15745039685756726,
   -1.8918086455997665,
   -0.024037218966209112,
   2.4770484238137676,
   0.6262800398601426]
   
pickJ = [1.62521114151198,
   -0.17855889359949387,
   0.5047374598854466,
   -2.33690645769903,
   0.18616158796681298,
   2.207514072974523,
   0.7601201489350046]

#[0.999932578298823, -0.010526316515627295, -0.0021868741366545754, 0.0, -0.010513086326297987, -0.9999172533717611, 0.0059756444487183286, 0.0, -0.00224963801754845, -0.005952365365499018, -0.9999797540327232, 0.0, 0.43604286088473987, 0.37174356696230537, 0.014075713047352658, 1.0], 'error_message': '', 'grasped_object': 'NullObject', 'q': [0.8744786531329155, 0.6354851113625126, -0.15135975750376113, -2.084133865470237, 0.20442904366387257, 2.700332147236262, 1.3624367617699833] 4/24

def grasp(width, force = 0.1):

    """
    Control the robot to perform a grasping operation.

    Parameters:
    - width: The width at which the gripper should open.
    - force: The force to be applied during the grasping operation.

    Returns:
    The result of the grasping operation.

    libranka description:
    This function controls the robot to execute a grasping operation by calling the grasp method from libranka.
    The gripper opens to the specified width and applies the specified force during the grasping process.
    The parameters epsilon_inner and epsilon_outer define the precision of the grasping operation.
    """
    payload = {
        "width": width,
        "speed": 0.05,
        "force": force,
        "epsilon_inner": 1,
        "epsilon_outer": 1, 

    }
    return call_method(robot, 12000, "grasp", payload)

def move_gripper(width):

    """
    Control the robot to move the gripper to a specified width.

    Parameters:
    - width: The target width for the gripper.

    Returns:
    The result of the gripper movement.

    libranka description:
    This function utilizes libranka to control the robot's gripper, moving it to the specified width.
    The movement speed is set to 0.05 to ensure a controlled and gradual gripper motion.
    """
    payload = {
        "width": width,
        "speed": 0.05,
    }
    return call_method(robot, 12000, "move_gripper", payload)

def pick():
    #move_to_location(robot, "pre0")
    moveJ(initJ)
    move_gripper(0.0015)
    moveJ(pickJ)

    #
    moveJ(pickJ)
    move_to_location(robot, "pre1")
    move_to_location(robot, "pre2")
    grasp(0.005)
    call_method(robot, 12000, "set_grasped_object", {"object": "ring"})
    call_method(robot, 12000, "set_grasped_object", {"object": "ring"})
    time.sleep(0.2)
    
    move_to_location(robot, "pre1")
    #move_to_location(robot, "pre0")
    moveJ(initJ)
    moveJ([0.9007378674889246,   0.4424676128353988,   -0.20733402558702654,   -2.1164788800130077,   0.17233900280558392,   2.543009564002355,   1.3696695665589578])
    #move_to_location(robot, "app1")
    
    # time.sleep(3)
    # move_gripper(0.004)

def modify_taught_pose(x, y, z, name:str):
    
    """
    :param x: X-coordinate for the object's position.
    :param y: Y-coordinate for the object's position.
    :param z: Z-coordinate for the object's position.
    :param name: A string representing the object's name.
    
    :return: The result of the modify_taught_pose operation.
    
    """
    payload = {
        "object": name,
        "data": {
            "x": x,
            "y": y,
            "z": z,
            #"R": [0, 1, 0, 1, 0, 0, 0, 0, -1],
            "R": [1, 0, 0, 0, -1, 0, 0, 0, -1],
        #[1, 0, 0, 0, 1, 0, 0, 0, 1]
        },
    }
    return call_method(robot, 12000, "set_partial_object_data", payload)
    
def moveJ(q_g):     
         
        """
        Move the robot to a specified joint pose.

        Args:
        q_g (list): Joint pose.
        robot: The robot object.

        Returns:
        The result of the movement task.
        
        
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


def insertion():
    print(call_method(robot, 12000, "get_state"))
    call_method(robot, 12000, "set_grasped_object", {"object": "obj1"})
    content = {
        "skill": {
            "objects": {
                # "Container": "hole",
                # "Approach": "app1",
                # "Insertable": "hex1"
                "Container": "container",
                "Approach": "approach",
                "Insertable": "obj1"                
            },
            "time_max": 10,
            "p0": {
                "dX_d": [0.1, 0.5],
                "ddX_d": [0.5, 1],
                "DeltaX": [0, 0, 0, 0, 0, 0],
                "K_x": [1500, 1500, 1500, 100, 100, 100]
            },
            "p1": {
                "dX_d": [0.02, 0.05],
                "ddX_d": [0.5, 0.1],
                "K_x": [500, 500, 500, 100, 100, 100]
            },
            "p2": {
                "search_a": [4, 6, 15, 0, 0, 0],
                # "search_a": [5, 5, 0, 2, 2, 0],
                "search_f": [1.2, 1.2, 0, 1.2, 1, 0],
                # "search_a": [0, 0, 0, 0, 0, 0],
                # "search_f": [0, 0, 0, 0, 0, 0],
                "search_phi": [0, math.pi/2, 0, 0, 0, 0],
                "K_x": [1000, 1000, 1000, 100, 100, 100],
                "f_push": [0, 0, 15, 0, 0, 0],
                "dX_d": [0.1, 0.5],
                "ddX_d": [0.5, 1]
            },
            "p3": {
                "dX_d": [0.1, 0.5],
                "ddX_d": [0.5, 1],
                "f_push": 10,
                "K_x": [500, 500, 0, 800, 800, 800]
            }
        },
        "control": {
            "control_mode": 0
        },
        "user": {
            "env_X": [0.01, 0.01, 0.002, 0.05, 0.05, 0.05],
            "env_dX": [0.001, 0.001, 0.001, 0.005, 0.005, 0.005],
            "F_ext_contact": [2.0, 1.0]
        }
    }
    t = Task(robot)
    t.add_skill("insertion", "TaxInsertion", content)
    t.start()
    time.sleep(0.5)
    result = t.wait()
    print("Result: " + str(result))
    return result
    
    # move_to_location(robot, "app2")

    #call_method(robot, 12000, "teach_object", {"object": ring, "teach_width":True})

#  0.417140386890134,
#  0.4047956531460382,
#  0.015098423457252558,


def modify_app1(x = 0.417140386890134, y = 0.4047956531460382):
    print([x,y])
    return modify_taught_pose(x, y,0.04859681927176112, "app1")

def modify_housing(x = 0.417140386890134, y = 0.4047956531460382):
    return modify_taught_pose(x, y, 0.015098423457252558, "housing")

def extract():
    move_gripper(0.002)
    time.sleep(0.5)
    gripper(0.0005)
    teach_location(robot, "above")
    a = call_method(robot, 12000, "get_state")
    x = a["result"]['O_T_EE'][-4]
    y = a["result"]['O_T_EE'][-3]
    z = a["result"]['O_T_EE'][-2] + 0.05
    modify_taught_pose(x,y,z,"above")
    print('Housing pose:', [x,y])
    move_to_location(robot, "above")

def tilt_back_wall():
    teach_location(robot, "xxx")
    a = call_method(robot, 12000, "get_state")
    x = a["result"]['O_T_EE'][-4]
    y = a["result"]['O_T_EE'][-3]
    z = a["result"]['O_T_EE'][-2] 
    payload = {
        "object": 'xxx',
        "data": {
            "x": x,
            "y": y,
            "z": z,
            #"R": [0, 1, 0, 0, 0, 1, 1, 0, 0],
            "R": [0, 0, 1, 1, 0, 0, 0, 1, 0],
        },
    }
    # call_method(robot, 12000, "set_partial_object_data", payload)
    
    # move_to_location(robot, "xxx")
    
  
    

def pick_and_insert():
    time.sleep(3)
    pick()
    insertion()
    time.sleep(1)
    extract()
    moveJ(initJ)

def end():
    extract()
    moveJ(initJ)

def in_100():
    for i in range(100):
        insertion()
        time.sleep(0.5)
        print("------------------------- ", i, " ---------------------")
        
def extract_skill():
    extraction_context = {
        "skill": {
            "objects": {
                "Container": "hole",
                "ExtractTo": "app1",
                "Extractable": "hex1"
            },
            "time_max": 10,
            "p0": {
                "search_a": [0, 0, 0, 0, 0, 0],
                "search_f": [0, 0, 0, 0, 0, 0],
                "K_x": [1500, 1500, 1500, 150, 150, 150],
                "dX_d": [0.1, 0.5],
                "ddX_d": [0.5, 1]
            },
            "p1": {
                "dX_d": [0.1, 0.5],
                "ddX_d": [0.5, 1],
                "K_x": [1000, 1000, 1500, 100, 100, 100]
            }
        },
        "control": {
            "control_mode": 0
        },
        "user": {
            "env_X": [0.005, 0.01, 0.01, 0.05, 0.05, 0.05],
            "env_dX": [0.001, 0.001, 0.001, 0.005, 0.005, 0.005]
        }
    }
    
    t = Task(robot)
    t.add_skill("extraction", "TaxExtraction", extraction_context)
    t.start()
    time.sleep(0.1)
    result = t.wait()
    print("Result: " + str(result))
    
