#!/usr/bin/python

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed


class Hinge(avango.script.Script):

    ## input fields
    sf_rot_value = avango.SFFloat()

    ### class variables ###

    # Number of Hinge instances that have already been created.
    number_of_instances = 0
   

    ## constructor
    def __init__(self):
        self.super(Hinge).__init__()

        ## get unique id for this instance
        self.id = Hinge.number_of_instances
        Hinge.number_of_instances += 1
        

    def my_constructor(self,
        PARENT_NODE = None,
        DIAMETER = 0.1, # in meter
        HEIGHT = 0.1, # in meter
        ROT_OFFSET_MAT = avango.gua.make_identity_mat(), # the rotation offset relative to the parent coordinate system
        ROT_AXIS = avango.gua.Vec3(0,1,0), # the axis to rotate arround with the rotation input (default is head axis)        
        SF_ROT_INPUT_MAT = None
        ):


        ### parameters ###
        self.rot_axis = ROT_AXIS        


        ### variables ###
        self.diameter = DIAMETER
        self.height = HEIGHT

        ### resources ###
        _loader = avango.gua.nodes.TriMeshLoader() # get trimesh loader to load external tri-meshes

        ### init Geometry ###
        self.object_geometry = _loader.create_geometry_from_file("hinge_geometry", "data/objects/cylinder.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.object_geometry.Transform.value = avango.gua.make_scale_mat(self.diameter, self.height, self.diameter)

        #### init hinge nodes ###
        self.hinge_position_node = avango.gua.nodes.TransformNode(Name = "hinge_position_node")
        self.hinge_position_node.Children.value = [self.object_geometry]
        self.hinge_position_node.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
        PARENT_NODE.Children.value.append(self.hinge_position_node)

        ## ToDo: connect input fields
        # ...


        
    ### callback functions ###
    
    @field_has_changed(sf_rot_value)
    def sf_rot_value_changed(self):
        pass
        ## ToDo: accumulate input to hinge node && consider rotation contraints of this hinge
        # ...

    def get_hinge_position_node(self):
        return self.hinge_position_node