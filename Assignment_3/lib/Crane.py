#!/usr/bin/python

# import guacamole libraries
import avango
import avango.gua


### import application libraries
from lib.KeyboardInput import KeyboardInput
from lib.Hinge import Hinge
from lib.Arm import Arm
from lib.Hook import Hook
from lib.Scene import Scene


class Crane:
  
    ## constructor
    def __init__(self,
        PARENT_NODE = None,
        TARGET_LIST = [],
        ):

        ### resources ###
        ## init base node for whole crane
        self.target_list = TARGET_LIST
       
        self.base_node = avango.gua.nodes.TransformNode(Name = "base_node")
        self.base_node.Transform.value = avango.gua.make_trans_mat(0.0,-0.1,0.0)
        PARENT_NODE.Children.value.append(self.base_node)

        _node = self.get_base_node

        ## init internal sub-classes
        self.input = KeyboardInput()


        ## ToDo: init first hinge && connect rotation input
        # default constructor is empty -> first construct, then fill with function
        self.hinge1 = Hinge()

        self.hinge1.my_constructor(
            PARENT_NODE = self.base_node,
            DIAMETER = 0.1, #in meter
            HEIGHT = 0.01, #in meter
            ROT_OFFSET_MAT = avango.gua.make_identity_mat(), # the rotation offset relative to the parent coordinate system
            ROT_AXIS = avango.gua.Vec3(0,1,0), # the axis to rotate arround with the rotation input (default is head axis)        
            )

        # here it is directly the constructor
        self.arm1 = Arm(
            PARENT_NODE = self.hinge1.get_hinge_position_node(),
            DIAMETER = 0.01, 
            LENGTH = 0.1, 
            ROT_OFFSET_MAT = avango.gua.make_identity_mat(),
            )

        ## ToDo: init second hinge && connect rotation input 
        self.hinge2 = Hinge()

        self.hinge2.my_constructor(
            PARENT_NODE = self.arm1.get_arm_top_position_node(),
            DIAMETER = 0.02, 
            HEIGHT = 0.01, 
            ROT_OFFSET_MAT = avango.gua.make_rot_mat(90.0, 1.0, 0.0, 0.0),
            ROT_AXIS = avango.gua.Vec3(0,0,1),        
            )

        ## ToDo: init second arm-segment
        self.arm2 = Arm(
            PARENT_NODE = self.hinge2.get_hinge_position_node(),
            DIAMETER = 0.01, 
            LENGTH = 0.07,
            )

        ## ToDo: init third hinge && connect rotation input 
        self.hinge3 = Hinge()

        self.hinge3.my_constructor(
            PARENT_NODE = self.arm2.get_arm_top_position_node(),
            DIAMETER = 0.02,
            HEIGHT = 0.01,
            ROT_OFFSET_MAT = avango.gua.make_rot_mat(90.0, 1.0, 0.0, 0.0),
            ROT_AXIS = avango.gua.Vec3(0,0,1),       
            )

        ## ToDo: init third arm-segment
        self.arm3 = Arm(
            PARENT_NODE = self.hinge3.get_hinge_position_node(),
            DIAMETER = 0.01,
            LENGTH = 0.07,
            ROT_OFFSET_MAT = avango.gua.make_identity_mat(),
            )

        ## ToDo: init hook
        self.hook = Hook()

        self.hook.my_constructor(
            PARENT_NODE = self.arm3.get_arm_top_position_node(),
            SIZE = 0.02,
            TARGET_LIST = self.target_list
            )

                     
    def get_base_node(self):
        return self.base_node
