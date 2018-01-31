#!/usr/bin/python

## @file
# Contains helper methods for various tasks.

### import avango-guacamole libraries
import avango
import avango.gua

### import python libraries
import math

import xml.etree.ElementTree as ET



## Converts a rotation matrix to the Euler angles yaw, pitch and roll.
# @param MATRIX The rotation matrix to be converted.
def get_euler_angles(MATRIX):

    quat = MATRIX.get_rotate()
    qx = quat.x
    qy = quat.y
    qz = quat.z
    qw = quat.w

    sqx = qx * qx
    sqy = qy * qy
    sqz = qz * qz
    sqw = qw * qw
    
    unit = sqx + sqy + sqz + sqw # if normalised is one, otherwise is correction factor
    test = (qx * qy) + (qz * qw)

    if test > 1:
        yaw = 0.0
        roll = 0.0
        pitch = 0.0

    if test > (0.49999 * unit): # singularity at north pole
        yaw = 2.0 * math.atan2(qx,qw)
        roll = math.pi/2.0
        pitch = 0.0
    elif test < (-0.49999 * unit): # singularity at south pole
        yaw = -2.0 * math.atan2(qx,qw)
        roll = math.pi/-2.0
        pitch = 0.0
    else:
        #print("euler", 2.0 * test)
        yaw = math.atan2(2.0 * qy * qw - 2.0 * qx * qz, 1.0 - 2.0 * sqy - 2.0 * sqz)
        roll = math.asin(2.0 * test)
        pitch = math.atan2(2.0 * qx * qw - 2.0 * qy * qz, 1.0 - 2.0 * sqx - 2.0 * sqz)

    if yaw < 0.0:
        yaw += 2.0 * math.pi

    if pitch < 0:
        pitch += 2 * math.pi
    
    if roll < 0:
        roll += 2 * math.pi

    return yaw, pitch, roll


## Extracts the yaw (head) rotation from a rotation matrix.
# @param MATRIX The rotation matrix to extract the angle from.
def get_yaw(MATRIX):

    try:
        _yaw, _pitch, _roll = get_euler_angles(MATRIX)
        return _yaw
    except:
        return 0


## Returns the rotation matrix of the rotation between two input vectors.
# @param VEC1 First vector.
# @param VEC2 Second vector.
def get_rotation_between_vectors(VEC1, VEC2, FLIP = False):

  tmp_vec1 = avango.gua.Vec3(VEC1.x,VEC1.y,VEC1.z)
  tmp_vec2 = avango.gua.Vec3(VEC2.x,VEC2.y,VEC2.z)

  if tmp_vec1.length() == 0.0 or tmp_vec2.length() == 0.0:
    return avango.gua.make_identity_mat()
  
  if abs(tmp_vec1.x) == abs(tmp_vec2.x) and abs(tmp_vec1.y) == abs(tmp_vec2.y) and abs(tmp_vec1.z) == abs(tmp_vec2.z): # identical vectors
    return avango.gua.make_identity_mat()

    
  tmp_vec1.normalize()
  tmp_vec2.normalize()

  _angle = math.degrees(math.acos(min(max(tmp_vec1.dot(tmp_vec2), -1.0), 1.0)))
  if FLIP:
    _angle = _angle * -1


  _axis = tmp_vec1.cross(tmp_vec2)
  _axis = avango.gua.Vec3(_axis.x,_axis.y,_axis.z)

  return avango.gua.make_rot_mat(_angle, _axis)

def get_ray_transform_between(MAT_FROM, MAT_TO, SCALE):
  f_pos = MAT_FROM.get_translate()
  t_pos = MAT_TO.get_translate()

  v = t_pos - f_pos
  v_norm = norm(v)

  midpoint = f_pos + (v * 0.5)

  return  avango.gua.make_trans_mat(midpoint[0],midpoint[1],midpoint[2]) * \
          get_rotation_between_vectors(avango.gua.Vec3(0.0,0.0,-1.0),v_norm) * \
          avango.gua.make_scale_mat(SCALE, SCALE, get_vector_length(v))

def get_ray_transform_between_plane(MAT_FROM, MAT_TO, SCALE):
  f_pos = MAT_FROM.get_translate()
  t_pos = MAT_TO.get_translate()

  v = t_pos - f_pos
  v_norm = norm(v)

  midpoint = f_pos + (v * 0.5)

  return  avango.gua.make_trans_mat(midpoint[0],midpoint[1],midpoint[2]) * \
          get_rotation_between_vectors(avango.gua.Vec3(0.0,0.0,-1.0),v_norm) * \
          avango.gua.make_scale_mat(get_vector_length(v), get_vector_length(v), SCALE)

def get_angle_between_vectors(VEC1, VEC2):

  if VEC1.length() == 0.0 or VEC2.length() == 0.0:
    return 0.0
  
  if abs(VEC1.x) == abs(VEC2.x) and abs(VEC1.y) == abs(VEC2.y) and abs(VEC1.z) == abs(VEC2.z): # identical vectors
    return 0.0

  VEC1.normalize()
  VEC2.normalize()

  return math.degrees(math.acos(min(max(VEC1.dot(VEC2), -1.0), 1.0)))

  '''
  _epsilon = 0.000001
  if abs(VEC1.x - VEC2.x) < _epsilon and abs(VEC1.y - VEC2.y) < _epsilon and abs(VEC1.z - VEC2.z) < _epsilon:
    return 0.0

  else:
    VEC1.normalize()
    VEC2.normalize()

    return math.degrees(math.acos(VEC1.dot(VEC2)))
  '''

def get_axis_between_vectors(VEC1, VEC2):

  if VEC1.length() == 0.0 or VEC2.length() == 0.0:
    return avango.gua.Vec3()

  if abs(VEC1.x) == abs(VEC2.x) and abs(VEC1.y) == abs(VEC2.y) and abs(VEC1.z) == abs(VEC2.z): # identical vectors
    return avango.gua.Vec3()

  else:
    VEC1.normalize()
    VEC2.normalize()

    return VEC1.cross(VEC2)

def norm(VEC):
    if not get_vector_length == 0:
        return VEC/get_vector_length(VEC)
    else:   
        return None

def get_vector_length(VEC):
    return math.sqrt(VEC[0]*VEC[0] + VEC[1]*VEC[1] + VEC[2]*VEC[2])

def cross(VEC1 , VEC2):
    return avango.gua.Vec3( VEC1[1]*VEC2[2]-VEC1[2]*VEC2[1],
                            VEC1[2]*VEC2[0]-VEC1[0]*VEC2[2],
                            VEC1[0]*VEC2[1]-VEC1[1]*VEC2[0])

def scalar(VEC1 , VEC2):
    tmp_vec1 = norm(VEC1)
    tmp_vec2 = norm(VEC2)
    return tmp_vec1[0]*tmp_vec2[0] + tmp_vec1[1]*tmp_vec2[1] + tmp_vec1[2]*tmp_vec2[2]




## Returns the Euclidean distance between two points.
# @param POINT1 Starting point.
# @param POINT2 End point.
def euclidean_distance(POINT1, POINT2):
    _diff_x = POINT2.x - POINT1.x
    _diff_y = POINT2.y - POINT1.y
    _diff_z = POINT2.z - POINT1.z

    return math.sqrt(math.pow(_diff_x, 2) + math.pow(_diff_y, 2) + math.pow(_diff_z, 2))

## Computes the distance between a Point and a 3D-line.
# @param POINT_TO_CHECK The point to compute the distance for.
# @param LINE_POINT_1 One point lying on the line.
# @param LINE_VEC Direction vector of the line.
def compute_point_to_line_distance(POINT_TO_CHECK, LINE_POINT_1, LINE_VEC):

    _point_line_vec = avango.gua.Vec3(LINE_POINT_1.x - POINT_TO_CHECK.x, LINE_POINT_1.y - POINT_TO_CHECK.y, LINE_POINT_1.z - POINT_TO_CHECK.z)

    _dist = (_point_line_vec.cross(LINE_VEC)).length() / LINE_VEC.length()

    return _dist


## Gets the world transformation of the handled scenegraph node.
def get_world_transform(NODE):
    _world_mat = NODE.Transform.value
    _parent_node = NODE.Parent.value

    while True:
        if _parent_node is not None:
            _world_mat = _parent_node.Transform.value * _world_mat
            _parent_node = _parent_node.Parent.value

        else:
            break
    return _world_mat


def load_matrix_from_xml(PATH):
    xml = ET.parse(PATH).getroot()

    trans = xml.find("Transformation")
    position = parse_vec3(trans.find("Position").text, faktor=0.001)
    rot_x = parse_vec3(trans.find("Direction").find("X").text)
    rot_y = parse_vec3(trans.find("Direction").find("Y").text)
    rot_z = parse_vec3(trans.find("Direction").find("Z").text)

    pxl = xml.find("Image").find("Pixel")
    pxl_size = float(pxl.find("Size").text)

    pxl_x = float(pxl.find("Width").text)
    pxl_y = float(pxl.find("Height").text)

    scale_x = pxl_x * pxl_size
    scale_y = pxl_y * pxl_size

    depth = float(xml.find("Depth").find("Range").text)

    transform =\
        build_matrix(position, rot_x, rot_y, rot_z) *\
        avango.gua.make_scale_mat(scale_x, scale_y, depth)

    return transform
   

def parse_vec3(text, faktor=1.0):
    text = text[1:-1]
    texts = text.split('/')
    floats = list(map(float, texts))
    return avango.gua.Vec3(floats[0], floats[1], floats[2]) * faktor


def build_matrix(p, x, y, z):
    lst = [
        x[0], x[1], x[2], 0.0,
        y[0], y[1], y[2], 0.0,
        z[0], z[1], z[2], 0.0,
        p[0], p[1], p[2], 1.0,
    ]
    return avango.gua.from_list(lst)
    
def get_lookat_matrix(DIR, UP = avango.gua.Vec3(0.0,1.0,0.0), FLIP = False):
  tmp_vec1 = DIR
  tmp_vec2 = UP
  tmp_vec2.normalize()
  tmp_vec1.normalize()
  if FLIP is True:
    _f = avango.gua.Vec3(-tmp_vec1.x, -tmp_vec1.y, -tmp_vec1.z) #flipped lookat direction
  else:
    _f = avango.gua.Vec3(tmp_vec1.x, tmp_vec1.y, tmp_vec1.z) #lookat direction
  _s = _f.cross(tmp_vec2) #lookat tangent relative to up vector
  _u = _s.cross(_f) #lookat binormal
  _s.normalize()
  _u.normalize()

  return avango.gua.from_list([ _s.x,  _s.y,  _s.z, 0.0
                              , _u.x,  _u.y,  _u.z, 0.0
                              ,-_f.x, -_f.y, -_f.z, 0.0
                              ,  0.0,   0.0,   0.0, 1.0])

def get_rotate_scale_corrected(MAT4):
  _scale_mat = avango.gua.make_scale_mat(MAT4.get_scale())
  _scale_independent_mat = MAT4 * avango.gua.make_inverse_mat(_scale_mat)

  return _scale_independent_mat.get_rotate()


def print_graph(root_node):
  stack = [(root_node, 0)]
  while stack:
    node, level = stack.pop()
    print("|   " * level + "|---{0} <{1}>".format(node.Name.value, node.__class__.__name__))
    stack.extend([(child, level + 1) for child in reversed(node.Children.value)])

def set_visibility(NODE, BOOL):

  if BOOL:
    if "invisible" in NODE.Tags.value:
      NODE.Tags.value.remove("invisible")
  else:
    if "invisible" not in NODE.Tags.value:
      NODE.Tags.value.append("invisible")


import builtins

def get_color_by_id(ID):
  return builtins.COLOR_LIST[ID % len(builtins.COLOR_LIST)]


# RED   = "\033[1;31m"  
# BLUE  = "\033[1;34m"
# CYAN  = "\033[1;36m"
# GREEN = "\033[0;32m"
# RESET = "\033[0;0m"
# BOLD    = "\033[;1m"
# REVERSE = "\033[;7m"
def colorize_string(STRING, ID):

  color = get_color_by_id(ID)

  if color.r == 1.0 and color.g == 0.0 and color.b == 0.0: #red
    return '\033[91m' + STRING + '\033[0m'
  if color.r == 0.0 and color.g == 1.0 and color.b == 0.0: #green
    return '\033[1;32m' + STRING + '\033[0m'
  if color.r == 1.0 and color.g == 0.0 and color.b == 0.0: #blue
    return '\033[1;34m' + STRING + '\033[0m'

  return STRING