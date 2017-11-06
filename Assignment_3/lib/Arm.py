#!/usr/bin/python

# import guacamole libraries
import avango
import avango.gua


class Arm:

    ### class variables ###

    # Number of Arm instances that have already been created.
    number_of_instances = 0
    
  
    ## constructor
    def __init__(self,
        PARENT_NODE = None,
        DIAMETER = 0.1, # in meter
        LENGTH = 0.1, # in meter
        ROT_OFFSET_MAT = avango.gua.make_identity_mat(), # the rotation offset relative to the parent coordinate system
        ):

        ## get unique id for this instance
        self.id = Arm.number_of_instances
        Arm.number_of_instances += 1

        ### variables ###
        self.diameter = DIAMETER
        self.length = LENGTH

        ### resources ###
        _loader = avango.gua.nodes.TriMeshLoader() # get trimesh loader to load external tri-meshes
        
        ### init Geometry ###
        self.object_geometry = _loader.create_geometry_from_file("arm_geometry", "data/objects/cylinder.obj", avango.gua.LoaderFlags.DEFAULTS)
        #self.object_geometry.Transform.value = avango.gua.make_trans_mat(0.0, self.length * 50, 0.0)        
        self.object_geometry.Transform.value = avango.gua.make_scale_mat(self.diameter, self.length, self.diameter)


        #### init hinge nodes ###
        self.arm_position_node = avango.gua.nodes.TransformNode(Name = "arm_center_position_node")
        self.arm_position_node.Children.value = [self.object_geometry]
        self.arm_position_node.Transform.value *= avango.gua.make_trans_mat(0.0, self.length/2, 0.0 )
        PARENT_NODE.Children.value.append(self.arm_position_node)

        self.arm_top_position_node = avango.gua.nodes.TransformNode(Name = "arm_top_position_node")
        self.arm_top_position_node.Transform.value = avango.gua.make_trans_mat(0.0, self.length, 0.0)
        self.arm_top_position_node.Transform.value *= ROT_OFFSET_MAT

        PARENT_NODE.Children.value.append(self.arm_top_position_node)

    def get_arm_top_position_node(self):
        return self.arm_top_position_node