#!/usr/bin/python

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
from lib.Scene import Scene


class Hook(avango.script.Script):

    ## internal fields
    sf_mat = avango.gua.SFMatrix4()
 
    # constructor
    def __init__(self):
        self.super(Hook).__init__()


    def my_constructor(self,
        PARENT_NODE = None,
        SIZE = 0.1,
        TARGET_LIST = [],
        ):

        ### external references ##

        ### variable
        self.size = SIZE
        self.target_list = TARGET_LIST


        ### resources ###
        _loader = avango.gua.nodes.TriMeshLoader()


        #Init Geometry
        self.object_geometry = _loader.create_geometry_from_file("hook_geometry", "data/objects/sphere.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.object_geometry.Transform.value *= avango.gua.make_scale_mat(self.size)
        self.object_geometry.Material.value.set_uniform("Color", avango.gua.Vec4(1, 185/255, 15/255, 1))

        ##Init Hook Nodes
        self.hook_position_node = avango.gua.nodes.TransformNode(Name = "hook_position_node")
        self.hook_position_node.Children.value = [self.object_geometry]
        PARENT_NODE.Children.value.append(self.hook_position_node)

        self.always_evaluate(True)
        print(self.object_geometry.Transform.value)
        print(self.hook_position_node.Transform.value)


        #Use wolrd tranform to get the hook_position in the world coordinate system
        self.sf_mat.connect_from(self.hook_position_node.WorldTransform)


    ### callback functions ###
    @field_has_changed(sf_mat)
    def sf_mat_changed(self):
        _pos = self.sf_mat.value.get_translate() # world position of hook
        
        for _node in self.target_list: # iterate over all target nodes
            _bb = _node.BoundingBox.value # get bounding box of a node
            #print(_node.Name.value, _bb.contains(_pos))
            
            if _bb.contains(_pos) == True: # hook inside bounding box of this node
                _node.Material.value.set_uniform("Color", avango.gua.Vec4(1.0,0.0,0.0,0.85)) # highlight color
            else:
                _node.Material.value.set_uniform("Color", avango.gua.Vec4(1.0,1.0,1.0,1.0)) # default color
       
