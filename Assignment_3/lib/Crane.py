#!/usr/bin/python

# import guacamole libraries
import avango
import avango.gua


### import application libraries
from lib.KeyboardInput import KeyboardInput
from lib.Hinge import Hinge
from lib.Arm import Arm
from lib.Hook import Hook


class Crane:
  
    ## constructor
    def __init__(self,
        PARENT_NODE = None,
        TARGET_LIST = [],
        ):


        ### resources ###

        ## init base node for whole crane
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
            DIAMETER = 0.1, # in meter
            HEIGHT = 0.01, # in meter
            ROT_OFFSET_MAT = avango.gua.make_identity_mat(), # the rotation offset relative to the parent coordinate system
            ROT_AXIS = avango.gua.Vec3(0,1,0), # the axis to rotate arround with the rotation input (default is head axis)        
            #SF_ROT_INPUT_MAT = 0.0
            )

        # here it is directly the constructor
        self.arm1 = Arm(
            PARENT_NODE = self.hinge1.get_hinge_position_node(),
            DIAMETER = 0.01, # in meter
            LENGTH = 0.1, # in meter
            ROT_OFFSET_MAT = avango.gua.make_identity_mat(),
            )



        ## ToDo: init second hinge && connect rotation input 
        # ...

        ## ToDo: init second arm-segment
        # ...
        

        ## ToDo: init third hinge && connect rotation input 
        # ...

        ## ToDo: init third arm-segment
        # ...


        ## ToDo: init hook
        # ...
                     
    def get_base_node(self):
        return self.base_node
