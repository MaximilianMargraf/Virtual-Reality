#!/usr/bin/python

# import guacamole libraries
import avango
import avango.gua

### import application libraries
from avango.script import field_has_changed
from lib.KeyboardInput import KeyboardInput
from lib.Hinge import Hinge
from lib.Arm import Arm
from lib.Hook import Hook
from lib.Scene import Scene
from lib.ProvenanceInteractionObject import ProvenanceCuboid
from lib.ProvenanceInteractionObject import ProvenancePlane
from lib.ProvenanceInteractionObject import ProvenanceEdge
from lib.ProvenanceInteractionObject import ProvenancePoint


class Crane:

    sf_prov_mode = avango.SFFloat()

    ## constructor
    def __init__(self,
        PARENT_NODE = None,
        TARGET_LIST = [],
        ):

        # resources
        # init base node for whole crane
        self.target_list = TARGET_LIST

        self.input = KeyboardInput()

        self.provenance_object_node = avango.gua.nodes.TransformNode(Name = "provenance_object_node")
        self.provenance_object_node.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
        PARENT_NODE.Children.value.append(self.provenance_object_node)
        #self.provenance_object_node.Tags.value = ["invisible"]

        self.base_node = avango.gua.nodes.TransformNode(Name = "base_node")
        self.base_node.Transform.value = avango.gua.make_trans_mat(0.0, -0.1, 0.0)
        PARENT_NODE.Children.value.append(self.base_node)

        _node = self.get_base_node

        # init internal sub-classes

        self.cuboid1 = ProvenanceCuboid()
        self.cuboid1.my_constructor(
            PARENT_NODE = self.provenance_object_node,
            POSITION = avango.gua.Vec3(0.0,0.1,-0.5),
            DIMENSIONS = avango.gua.Vec3(0.02, 0.02, 0.02),
            ROTATION = avango.gua.Vec4(0.0, 0, 0, 0)
            )

        self.point1 = ProvenancePoint()
        self.point1.my_constructor(
            PARENT_NODE = self.provenance_object_node,
            POSITION = avango.gua.Vec3(0.01, -0.1, -0.02),
            DIAMETER = 0.02
            )


        self.point2 = ProvenancePoint()
        self.point2.my_constructor(
            PARENT_NODE = self.provenance_object_node,
            POSITION = avango.gua.Vec3(0.04, 0.1, -0.02),
            DIAMETER = 0.02
            )

        self.point3 = ProvenancePoint()
        self.point3.my_constructor(
            PARENT_NODE = self.provenance_object_node,
            POSITION = avango.gua.Vec3(-0.04, 0.1, -0.02),
            DIAMETER = 0.02
            )

        self.edge1 = ProvenanceEdge()
        self.edge1.my_constructor(
            PARENT_NODE = self.provenance_object_node,
            NODE_1 = self.point1.get_position_node(),
            NODE_2 = self.point2.get_position_node(),
            EDGE_THICC = 0.005
            )

        self.edge2 = ProvenanceEdge()
        self.edge2.my_constructor(
            PARENT_NODE = self.provenance_object_node,
            NODE_1 = self.point2.get_position_node(),
            NODE_2 = self.point3.get_position_node(),
            EDGE_THICC = 0.005
            )

        self.edge3 = ProvenanceEdge()
        self.edge3.my_constructor(
            PARENT_NODE = self.provenance_object_node,
            NODE_1 = self.point3.get_position_node(),
            NODE_2 = self.point1.get_position_node(),
            EDGE_THICC = 0.005
            )

        self.plane1 = ProvenancePlane()
        self.plane1.my_constructor(
            PARENT_NODE = self.provenance_object_node,
            NODE_1 = self.point1.get_position_node(),
            NODE_2 = self.point2.get_position_node(),
            PLANE_THICC = 0.01
            )

    # Get Base Node for first hinge
    def get_base_node(self):
        return self.base_node

    """
    @field_has_changed(sf_prov_mode)
    def provenance_mode(self):
        print(self.sf_prov_mode.value)
        if self.sf_prov_mode.value == True:
            self.provenance_object_node.Tags.value = []
    
        if self.sf_prov_mode.value == False:
            self.provenance_object_node.Tags.value = ["invisible"]
    """