from task import *
from moving import *
from connection_test import *
import time
import math



robot = "localhost"
   

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

container = teach_location("localhost", "container")
approach = teach_location("localhost", "approach")
obj1 = teach_location("localhost", "obj1")
time_max = 10  

def insertion(container, approach, obj1, time_max):
    """
    Executes an insertion task with the robot.

    This function performs an insertion task with the robot. It sets the grasped object of the robot to "obj1",
    defines parameters for the insertion task, creates a Task object, adds the insertion skill to it, starts the task,
    waits for its completion, and returns the result.

    Returns:
        Any: The result of the insertion task execution.

        1.First Output (printed inside the function):
        It displays the current state of the robot, including the end-effector's pose, the current task status, etc.

        2.Second Output (printed inside the function):
        It shows the parameter configuration for the insertion task, including skill parameters, control parameters, and user-defined environmental parameters.

        3.Third Output (printed outside the function):
        It indicates the time taken for task execution, where 7.084 seconds were spent on executing the insertion task.

        4.Final Output (the return result of the function):
        -It is a dictionary containing the results of task execution.
        -Under the 'result' key is a sub-dictionary containing detailed task execution results.
        -The 'error' key indicates whether there were any errors during execution, which is empty here, indicating no errors.
        -Under the 'task_result' key are detailed results of the task.
        -The 'success' key indicates whether the task was successfully completed, which is True here, indicating successful completion.
        -Under the 'skill_results' key is a sub-dictionary containing the execution results of each skill.
        -Under 'insertion' key is the execution result of the insertion skill.
        -The 'cost' key holds a sub-dictionary with the cost assessment results of the insertion task, such as contact forces, desired force, and pose deviation.
        -The 'heuristic' key indicates the heuristic evaluation result of the insertion task.

    Raises:
        Any: Any exceptions raised during task execution.
    """

    container = "container"
    approach = "approach"
    obj1 = "obj1"
    print(call_method(robot, 12000, "get_state"))
    call_method(robot, 12000, "set_grasped_object", {"object": obj1})
    content = {
        "skill": {
            "objects": {
          
                "Container": container,
                "Approach": approach,
                "Insertable": obj1                
            },
            
            "time_max": time_max,
            

            # p0: the first mp, indicating the move_to_pose "Approach"
            "p0": {
                "dX_d": [0.1, 0.5], # This is a list of length 2, indicating the target translation velocities of the robot end-effector in the X and Y directions during the insertion action. In this example, dX_d is [0.1, 0.5], indicating a target velocity of 0.1 meters per second in the X direction and 0.5 meters per second in the Y direction.
                "ddX_d": [0.5, 1], # This is a list of length 2, indicating the target accelerations of the robot end-effector in the X and Y directions during the insertion action. In this example, ddX_d is [0.5, 1], indicating a target acceleration of 0.5 meters per second squared in the X direction and 1 meter per second squared in the Y direction.
                "DeltaX": [0, 0, 0, 0, 0, 0], # This is a list of length 6, representing the corresponding displacement increments during the insertion action. In this example, DeltaX is [0, 0, 0, 0, 0, 0], indicating no displacement in the X, Y, and Z directions.
                "K_x": [1500, 1500, 1500, 100, 100, 100] # This is a list of length 6, representing the control gains during the insertion action. In this example, K_x is [1500, 1500, 1500, 100, 100, 100], indicating control gains of 1500 in the X, Y, and Z directions and 100 in rotation directions. These gains are used to adjust the stability and accuracy of the robot during the insertion action.
            },
            # p1: the second mp, indicating the move_to_contact, along the direction "Approach" -> "Container"
            "p1": {
                "dX_d": [0.02, 0.05], # This is a list of length 2, indicating the target translation velocities of the robot end-effector in the X and Y directions during the insertion action. Here, dX_d is [0.02, 0.05], meaning a target velocity of 0.02 meters per second in the X direction and 0.05 meters per second in the Y direction.
                "ddX_d": [0.5, 0.1], # This is a list of length 2, indicating the target accelerations of the robot end-effector in the X and Y directions during the insertion action. In this example, ddX_d is [0.5, 0.1], indicating a target acceleration of 0.5 meters per second squared in the X direction and 0.1 meters per second squared in the Y direction.
                "K_x": [500, 500, 500, 100, 100, 100] # This is a list of length 6, representing the control gains during the insertion action. Here, K_x is [500, 500, 500, 100, 100, 100], indicating control gains of 500 in the X, Y, and Z directions and 100 in rotation directions. These gains are used to adjust the stability and accuracy of the robot during the insertion action.
            },
            # p2: the third mp, indicating the insertion
            "p2": {
                "search_a": [4, 6, 15, 0, 0, 0], # This is a list of length 6, representing the search amplitudes during the insertion action. It determines the range of motion or deviation allowed during the insertion process. For example, [4, 6, 15, 0, 0, 0] implies that there's a search amplitude of 4 in the X direction, 6 in the Y direction, and 15 in the Z direction, while no search amplitude is specified for rotation.
                # "search_a": [5, 5, 0, 2, 2, 0],
                "search_f": [1.2, 1.2, 0, 1.2, 1, 0], # This is a list of length 6, indicating the search frequencies during the insertion action. It determines how rapidly the system explores the search space. For instance, [1.2, 1.2, 0, 1.2, 1, 0] suggests a search frequency of 1.2 Hz in the X, Y, and Z directions, and 1 Hz for rotation, except for no search frequency specified in the Z rotation.
                # "search_a": [0, 0, 0, 0, 0, 0],
                # "search_f": [0, 0, 0, 0, 0, 0],
                "search_phi": [0, math.pi/2, 0, 0, 0, 0], # This is a list of length 6, representing the search phases during the insertion action. It determines the starting phase of the search motion. Here, [0, math.pi/2, 0, 0, 0, 0] indicates that the search starts from 0 radians in the X direction and π/2 radians (90 degrees) in the Y direction, while no phase shift is applied to other directions.
                "K_x": [1000, 1000, 1000, 100, 100, 100], # This is a list of length 6, representing the control gains during the insertion action, similar to previous instances. It adjusts the stability and accuracy of the robot during insertion.
                "f_push": [0, 0, 15, 0, 0, 0], # This is a list of length 6, specifying the pushing forces during the insertion action. It defines the magnitude of the force applied to the object being inserted. For example, [0, 0, 15, 0, 0, 0] indicates a force of 15 Newtons along the Z direction.
                "dX_d": [0.1, 0.5], # This is a list of length 2, similar to previous instances, indicating the target translation velocities of the robot end-effector in the X and Y directions during the insertion action.
                "ddX_d": [0.5, 1] # This is a list of length 2, similar to previous instances, indicating the target accelerations of the robot end-effector in the X and Y directions during the insertion action.
            },
            # p3: not used
            "p3": {
                "dX_d": [0.1, 0.5], # This is a list of length 2, indicating the target translation velocities of the robot end-effector in the X and Y directions during the insertion action. It specifies the desired linear velocity for the insertion task. Here, [0.1, 0.5] suggests a target velocity of 0.1 meters per second in the X direction and 0.5 meters per second in the Y direction.
                "ddX_d": [0.5, 1], # This is a list of length 2, indicating the target accelerations of the robot end-effector in the X and Y directions during the insertion action. It specifies the desired linear acceleration for the insertion task. For instance, [0.5, 1] implies a target acceleration of 0.5 meters per second squared in the X direction and 1 meter per second squared in the Y direction.
                "f_push": 10, # This parameter indicates the pushing force during the insertion action. It defines the magnitude of the force applied by the robot end-effector while inserting the object. Here, f_push is set to 10, indicating a pushing force of 10 Newtons.
                "K_x": [500, 500, 0, 800, 800, 800] # This is a list of length 6, representing the control gains during the insertion action. It adjusts the stability and accuracy of the robot during the insertion process. The values specified here affect the control behavior of the robot's end-effector. For example, [500, 500, 0, 800, 800, 800] suggests control gains of 500 in the X and Y directions, no gain in the Z direction, and 800 in rotation.
            }
        },
        "control": {
            "control_mode": 0
        },
        # user: Limited conditions to determine whether the Insertion execution is successful, such as position and velocity tolerances, and maximum contact forces
        "user": {
            "env_X": [0.01, 0.01, 0.002, 0.05, 0.05, 0.05], # This parameter is a list of length 6, representing the environmental conditions related to position in the X, Y, and Z directions. It specifies the position tolerances or variations allowed in the environment. For example, [0.01, 0.01, 0.002, 0.05, 0.05, 0.05] indicates tolerance values of 0.01 meters in the X and Y directions, 0.002 meters in the Z direction, and 0.05 meters for rotation.
            "env_dX": [0.001, 0.001, 0.001, 0.005, 0.005, 0.005], # This parameter is a list of length 6, similar to env_X, but it represents the environmental conditions related to velocity. It specifies the allowed velocity variations or tolerances in the environment. For instance, [0.001, 0.001, 0.001, 0.005, 0.005, 0.005] suggests velocity tolerance values of 0.001 meters per second in the X, Y, and Z directions, and 0.005 meters per second for rotation.
            "F_ext_contact": [2.0, 1.0] # This parameter is a list of length 2, representing the external contact forces. It specifies the maximum forces allowed to be exerted on the objects or surfaces in contact with the robot during the insertion task. Here, [2.0, 1.0] indicates maximum contact forces of 2.0 Newtons in the X, Y, and Z directions and 1.0 Newtons for rotation.
        }
    }
    t = Task(robot)
    t.add_skill("insertion", "TaxInsertion", content)
    t.start()
    time.sleep(0.5)
    result = t.wait()
    print("Result: " + str(result))
    return result






def extract():
    move_gripper(0.002)
    time.sleep(0.5)
    move_gripper(0.0005)
    teach_location(robot, "above")
    a = call_method(robot, 12000, "get_state")
    x = a["result"]['O_T_EE'][-4]
    y = a["result"]['O_T_EE'][-3]
    z = a["result"]['O_T_EE'][-2] + 0.05
    modify_taught_pose(x,y,z,"above")
    print('Housing pose:', [x,y])
    move_to_location(robot, "above")




def extract_skill(container, approach, obj1, time_max):
    container = "container"
    approach = "approach"
    obj1 = "obj1"
   
    extraction_context = {
        "skill": {
            "objects": {
                "Container": container,
                "ExtractTo": approach,
                "Extractable": obj1
            },
            "time_max": time_max,
            "p0": {
                "search_a": [4, 6, 15, 0, 0, 0],
                "search_f": [1.2, 1.2, 0, 1.2, 1, 0],
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



class Insertion:
    #a = None

    def __init__(self, robot, object_id="obj1"):
      self.robot = robot
      self.object_id = object_id
      self.time_max = 10  
        
      self.search_a = [4, 6, 15, 0, 0, 0]
      self.search_f =  [1.2, 1.2, 0, 1.2, 1, 0]
      self.search_phi = [0, math.pi/2, 0, 0, 0, 0]
      self.K_x = [1000, 1000, 1000, 100, 100, 100]
      self.f_push = [0, 0, 15, 0, 0, 0]
      self.env_X = [0.01, 0.01, 0.002, 0.05, 0.05, 0.05]
      self.F_ext_contact = [2.0, 1.0]
      self.prepared = False  # New attribute to track whether prepare has been executed
    #   self.content = s

  
    #First run the prepare function to set the initial state of the robot
    def prepare(self,robot: str, obj1: str, approach: str,container: str):

        obj1 = input("Enter your taught pose name for obj1: ")
        input("Please move the robot to the object position and press Enter to continue...")
        teach_location("localhost", obj1)

        approach = input("Enter your taught pose name for approach: ")
        input("Please move the robot to the approach position and press Enter to continue...")
        teach_location("localhost", approach)
        
        
        container = input("Enter your taught pose name for container: ")
        input("Please move the robot to the container position and press Enter to continue...")
        teach_location("localhost", container)

        self.prepared = True
        print("Prepare method has been executed.")

    def modify_time(self, time_max):
        self.time_max = time_max
    
    
    def modify_search_amplitudes(self,search_a):
        self.search_a = search_a
    
    def modify_F_ext_contact(self,F_ext_contact):
        self.F_ext_contact = F_ext_contact
    
    #def modify_search_phi(self,search_phi):
     #   self.search_phi= search_phi
    
    #def modify_K_x(self,K_x):
     #   self.K_x= K_x

    def modify_f_push(self,f_push):
        self.f_pushx = f_push    

    def modify_lissajous(self,search_phi):
        self.search_phi = search_phi

    def modify_succ_condition(self,env_X):
        self.env_X = env_X

    def modify_stiffness(self,K_x):
        self.K_x = K_x
    
    def modify_stiffness(self,K_x):
        self.K_x = K_x

    def save_to_json(self, file_path):
        data = {
            "robot": self.robot,
            "object_id": self.object_id,
            "time_max": self.time_max,
            "search_a": self.search_a,
            "search_f": self.search_f,
            "search_phi": self.search_phi,
            "K_x": self.K_x,
            "f_push": self.f_push,
            "env_X": self.env_X,
            "F_ext_contact": self.F_ext_contact,
            #"prepared": self.prepared
        }
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file)
        print(f"Data saved to {file_path}")

    def load_from_json(self, file_path):
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            self.robot = data["robot"]
            self.object_id = data["object_id"]
            self.time_max = data["time_max"]
            self.search_a = data["search_a"]
            self.search_f = data["search_f"]
            self.search_phi = data["search_phi"]
            self.K_x = data["K_x"]
            self.f_push = data["f_push"]
            self.env_X = data["env_X"]
            self.F_ext_contact = data["F_ext_contact"]
            #self.prepared = data["prepared"]
        print(f"Data loaded from {file_path}")


    def execute(self):
        # Check if prepare has been executed before proceeding with any other logic
        if not self.prepared:
            print("Error: Please execute the prepare method before executing.")
            return
        # Content of the original execute method
        print("Executing the task...")
        print(call_method(self.robot, 12000, "get_state"))
        call_method(self.robot, 12000, "set_grasped_object", {"object": self.object_id})
        content = {
            "skill": {
                "objects": {
                    "Container": "container",
                    "Approach": "approach",
                    "Insertable": self.object_id                
                },
                "time_max": self.time_max, 
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
                     "search_a": self.search_a,
                # "search_a": [5, 5, 0, 2, 2, 0],
                "search_f": self.search_f,
                # "search_a": [0, 0, 0, 0, 0, 0],
                # "search_f": [0, 0, 0, 0, 0, 0],
                "search_phi": self.search_phi,
                "K_x": self.K_x,
                "f_push": self.f_push,
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
            "user": {"env_X": self.env_X,
            "env_dX": [0.001, 0.001, 0.001, 0.005, 0.005, 0.005],
            "F_ext_contact": self.F_ext_contact
                
            }
        }
        t = Task(self.robot)
        t.add_skill("insertion", "TaxInsertion", content)
        t.start()
        time.sleep(0.5)
        result = t.wait()
        print("Result：", str(result))
        return result
    


