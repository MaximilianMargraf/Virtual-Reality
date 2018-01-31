import avango
import avango.gua
import math


class ProvenanceData(avango.script.Script):

	# init class
    def __init__(self):
        self.super(ProvenanceData).__init__()

        self.evaluate()

    # constructor
	def my_constructor(self,
		PARENT_NODE = None,
		OFFSET = avango.gua.Vec3(0.0, 0.0, 0.0),
		ROTATION = avango.gua.Vec4(0.0, 0, 0, 0)
		):

	# parameters
	self._offset = OFFSET
	self._rotation = ROTATION

	# if provenanceData is pick_result but not selected, change transparence to 1 for better visibility 
	def highlighted
		raise NotImplementedError("Must be implemented by a subclass")

	# if ProvenanceData is selected with click, show data
	def show(self):
		raise NotImplementedError("Must be implemented by a subclass")


class ProvenanceAudio(ProvenanceData):

	# init class
    def __init__(self):
        self.super(ProvenanceAudio).__init__()

        self.evaluate()

    # constructor
	def my_constructor(self,
		PARENT_NODE = None,
		POSITION = avango.gua.Vec3(0.0, 0.0, 0.0)
		):

	ProvenanceData.my_constructor(PARENT_NODE, POSITION)
	# own code


class ProvenanceText(ProvenanceData):

	# init class
    def __init__(self):
        self.super(ProvenanceText).__init__()

        self.evaluate()

    # constructor
	def my_constructor(self,
		PARENT_NODE = None,
		POSITION = avango.gua.Vec3(0.0, 0.0, 0.0)
		):

	# parameters
	self._position = POSITION


class ProvenanceImage(ProvenanceData):

	# init class
    def __init__(self):
        self.super(ProvenanceImage).__init__()

        self.evaluate()

    # constructor
	def my_constructor(self,
		PARENT_NODE = None,
		POSITION = avango.gua.Vec3(0.0, 0.0, 0.0)
		):

	# parameters
	self._position = POSITION