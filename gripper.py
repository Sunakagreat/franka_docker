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
# TODO: add descriotion from libranka
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
    # TODO, move release
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
