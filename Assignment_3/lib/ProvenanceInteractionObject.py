# ProvenanceObjekteUberklasse
import avango
import avango.gua
import math

# VERSION 1
import lib.Utilities
# lib.Utilities.get_ray_transform_between()

from lib.KeyboardInput import KeyboardInput

# VERSION 2
# from lib.Utilities import *
# get_ray_transform_between()

class ProvenanceInteractionObject(avango.script.Script):
	# init class
	def __init__(self):
		self.super(ProvenanceInteractionObject).__init__()
		self.evaluate()

	# constructor
	def my_constructor(self,
		PARENT_NODE = None,
		POSITION = avango.gua.Vec3(0.0, 0.0, 0.0),
		PROVENANCE_MODE = False
		):

		# parameters
		self._parent_node = PARENT_NODE
		self._position = POSITION

	# functions:
	# get ProvenanceInteractionObject´s position
	def get_position_node(self):
		raise NotImplementedError("Must be implemented by a subclass")


class ProvenanceCuboid(ProvenanceInteractionObject): # Viereck
	# init class
	def __init__(self):
		self.super(ProvenanceCuboid).__init__()

		self.evaluate()

	def my_constructor(self,
		PARENT_NODE = None,
		POSITION = avango.gua.Vec3(0.0, 0.0, 0.0),
		DIMENSIONS = avango.gua.Vec3(0.01, 0.01, 0.01),
		ROTATION = avango.gua.Vec4(0.0, 0, 0, 0)
		):

		# call base class constructor
		ProvenanceInteractionObject.my_constructor(self, PARENT_NODE, POSITION) 
		
		# parameters
		self._dimensions = DIMENSIONS
		self._rotation = ROTATION

		# init nodes & geometry
		self.cuboid_position_node = avango.gua.nodes.TransformNode(Name = "prov_cuboid_node")
		self.cuboid_position_node.Transform.value = \
			avango.gua.make_trans_mat(self._position)
		PARENT_NODE.Children.value.append(self.cuboid_position_node)

		_loader = avango.gua.nodes.TriMeshLoader()
		self.provenance_cuboid_geometry = _loader.create_geometry_from_file("prov_cub_geometry", "data/objects/cube.obj", avango.gua.LoaderFlags.DEFAULTS)
		self.provenance_cuboid_geometry.Transform.value = \
			avango.gua.make_rot_mat(self._rotation) * \
			avango.gua.make_scale_mat(self._dimensions)
		self.provenance_cuboid_geometry.Material.value.set_uniform("Color", avango.gua.Vec4(1.0, 0.0, 0.0, 0.7))
		self.cuboid_position_node.Children.value.append(self.provenance_cuboid_geometry)

    # functions
	def get_position_node(self):
		ProvenanceInteractionObject.get_position_node(self)

		return self.cuboid_position_node


class ProvenancePlane(ProvenanceInteractionObject): # Fläche
	# init class
	def __init__(self):
		self.super(ProvenancePlane).__init__()

		self.evaluate()

	def my_constructor(self,
		PARENT_NODE = None,
		NODE_1 = None,
		NODE_2 = None,
		PLANE_THICC = 0.001
		):

		# call base class constructor
		ProvenanceInteractionObject.my_constructor(self, PARENT_NODE)

		# parameters
		self._node_mat1 = NODE_1.WorldTransform.value
		self._node_mat2 = NODE_2.WorldTransform.value
		self._thickness = PLANE_THICC

		# init geometry
		_loader = avango.gua.nodes.TriMeshLoader()

		self.provenance_plane_geometry = _loader.create_geometry_from_file("prov_plane_geometry", "data/objects/plane.obj", avango.gua.LoaderFlags.DEFAULTS)
		self.provenance_plane_geometry.Transform.value = \
			lib.Utilities.get_ray_transform_between_plane(self._node_mat2, self._node_mat1, self._thickness) * \
			avango.gua.make_rot_mat(90, 1, 0, 0)
		self.provenance_plane_geometry.Material.value.set_uniform("Color", avango.gua.Vec4(1.0, 0.0, 0.0, 0.7))
		PARENT_NODE.Children.value.append(self.provenance_plane_geometry)

    # functions
	def provenance_mode(self, BOOL):
		raise NotImplementedError("Must be implemented by a subclass")

	def get_position_node(self):
		return self.plane_position_node


class ProvenanceEdge(ProvenanceInteractionObject): # Kante
	# init class
	def __init__(self):
		self.super(ProvenanceEdge).__init__()

		self.evaluate()

	#Constructor using two Nodes
	def my_constructor(self,
		PARENT_NODE = None,
		NODE_1 = None,
		NODE_2 = None,
		EDGE_THICC = 0.001
		):

		# call base class constructor
		ProvenanceInteractionObject.my_constructor(self, PARENT_NODE)

		# parameters
		self._node_mat1 = NODE_1.WorldTransform.value
		self._node_mat2 = NODE_2.WorldTransform.value
		self._thickness = EDGE_THICC

		# loader = avango.gua.nodes.LineStripLoader()
        # line_strip_geode = loader.create_empty_geometry("line_strip_model_1", "empty_name_1.lob")
		# line_strip_geode.ScreenSpaceLineWidth.value = 1.0
		# line_strip_geode.push_vertex(vertex_x, vertex_y, vertex_z, col_r, col_g, col_b, thickness)
		# line_strip_geode.clear_vertices()

		# init geometry
		_loader = avango.gua.nodes.TriMeshLoader()

		self.provenance_edge_geometry = _loader.create_geometry_from_file("prov_edge_geometry", "data/objects/cylinder.obj", avango.gua.LoaderFlags.DEFAULTS)
		self.provenance_edge_geometry.Transform.value = \
			lib.Utilities.get_ray_transform_between(self._node_mat2, self._node_mat1, self._thickness) * \
			avango.gua.make_rot_mat(90, 1, 0, 0)
		self.provenance_edge_geometry.Material.value.set_uniform("Color", avango.gua.Vec4(1.0, 0.0, 0.0, 0.7))
		PARENT_NODE.Children.value.append(self.provenance_edge_geometry)

		print(self.provenance_edge_geometry.WorldTransform.value.get_translate())

	# functions
	def provenance_mode(self, BOOL):
		raise NotImplementedError("Must be implemented by a subclass")

	def get_position_node(self):
		return self.edge_position_node


class ProvenancePoint(ProvenanceInteractionObject): # Punkt
	# init class
	def __init__(self):
		self.super(ProvenancePoint).__init__()

		self.evaluate()

	def my_constructor(self,
		PARENT_NODE = None,
		POSITION = avango.gua.Vec3(0.0, 0.0, 0.0),
		DIAMETER = 0.02
		):

		# call base class constructor
		ProvenanceInteractionObject.my_constructor(self, PARENT_NODE, POSITION)

		# parameters
		self._diameter = DIAMETER
		self._selected = 0
	
		# init nodes & geometry
		self.point_position_node = avango.gua.nodes.TransformNode(Name = "prov_point_node")
		self.point_position_node.Transform.value = \
			avango.gua.make_trans_mat(self._position)
		PARENT_NODE.Children.value.append(self.point_position_node)

		_loader = avango.gua.nodes.TriMeshLoader()

		self.provenance_point_geometry = _loader.create_geometry_from_file("prov_point_geometry", "data/objects/sphere.obj", avango.gua.LoaderFlags.DEFAULTS)
		self.provenance_point_geometry.Transform.value = \
			avango.gua.make_scale_mat(self._diameter)
		self.provenance_point_geometry.Material.value.set_uniform("Color", avango.gua.Vec4(1.0, 0.0, 1.0, 0.7))
		self.point_position_node.Children.value.append(self.provenance_point_geometry)

    # functions
	def provenance_mode(self, BOOL):
		raise NotImplementedError("Must be implemented by a subclass")

	def get_position_node(self):
		return self.point_position_node