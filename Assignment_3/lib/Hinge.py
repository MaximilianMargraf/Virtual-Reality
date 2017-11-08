#!/usr/bin/python

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
from lib.KeyboardInput import KeyboardInput


class Hinge(avango.script.Script):

    ## input fields
    sf_rot_value = avango.SFFloat()
    sf_rot_frame = avango.SFFloat()

    ### class variables ###

    # Number of Hinge instances that have already been created.
    number_of_instances = 0
    

    ## constructor
    def __init__(self):
        self.super(Hinge).__init__()

        ## get unique id for this instance
        self.id = Hinge.number_of_instances
        Hinge.number_of_instances += 1
        self.evaluate()
        

    def my_constructor(self,
        PARENT_NODE = None,
        DIAMETER = 0.1, # in meter
        HEIGHT = 0.1, # in meter
        ROT_CONSTRAINTS = avango.gua.Vec2(90, -90),
        ROT_OFFSET_MAT = avango.gua.make_identity_mat(), # the rotation offset relative to the parent coordinate system
        ROT_AXIS = avango.gua.Vec3(0,1,0), # the axis to rotate arround with the rotation input (default is head axis)        
        SF_ROT_INPUT_MAT = None
        ):


        #Access to KeyboardInput
        self.input = KeyboardInput()


        ### parameters ###
        self.rot_axis = ROT_AXIS
        self.sf_rot_value
        self.rot_constraints = ROT_CONSTRAINTS 
        self.diameter = DIAMETER
        self.height = HEIGHT
        self.allcounter = 0


        ### resources ###
        _loader = avango.gua.nodes.TriMeshLoader() # get trimesh loader to load external tri-meshes


        ### init Geometry ###
        self.object_geometry = _loader.create_geometry_from_file("hinge_geometry", "data/objects/cylinder.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.object_geometry.Transform.value *= ROT_OFFSET_MAT
        self.object_geometry.Transform.value *= avango.gua.make_scale_mat(self.diameter, self.height, self.diameter)
        self.object_geometry.Material.value.set_uniform("Color", avango.gua.Vec4(1.0 , 0, 0, 1))


        #### init hinge nodes ###
        self.hinge_position_node = avango.gua.nodes.TransformNode(Name = "hinge_position_node")
        self.hinge_position_node.Children.value = [self.object_geometry]
        PARENT_NODE.Children.value.append(self.hinge_position_node)


        ### connect input fields ###
        if self.id == 0:
            self.sf_rot_value.connect_from(self.input.sf_rot_input0)

        elif self.id == 1:
            self.sf_rot_value.connect_from(self.input.sf_rot_input1)

        elif self.id == 2:
            self.sf_rot_value.connect_from(self.input.sf_rot_input2)

        
    ### callback functions ###
    @field_has_changed(sf_rot_value)
    def sf_rot_value_changed(self):
        pass
        #Get time in between frames from keyboardinputs, to compute scaling factor for rotation
        self.sf_rot_frame.connect_from(self.input.sf_rot_frame)


        #Is not pretty
        #Negative Constraints
        if self.allcounter <= self.rot_constraints[1] and self.sf_rot_value.value < 0:
            self.allcounter = self.rot_constraints[1]

        elif self.allcounter <= self.rot_constraints[1] and self.sf_rot_value.value > 0:
            self.allcounter += self.sf_rot_value.value
            self.hinge_position_node.Transform.value *= avango.gua.make_rot_mat(self.sf_rot_value.value, self.rot_axis)

        #Positive Constraints
        elif self.allcounter >= self.rot_constraints[0] and self.sf_rot_value.value < 0:
            self.allcounter += self.sf_rot_value.value
            self.hinge_position_node.Transform.value *= avango.gua.make_rot_mat(self.sf_rot_value.value, self.rot_axis)

        elif self.allcounter >= self.rot_constraints[0] and self.sf_rot_value.value > 0:
            self.allcounter = self.rot_constraints[0]

        #In Between
        elif self.allcounter < self.rot_constraints[0] and self.allcounter > self.rot_constraints[1]:
            self.allcounter += self.sf_rot_value.value
            self.hinge_position_node.Transform.value *= avango.gua.make_rot_mat(self.sf_rot_value.value, self.rot_axis)

        print(self.allcounter)

    def get_hinge_position_node(self):
        return self.hinge_position_node

