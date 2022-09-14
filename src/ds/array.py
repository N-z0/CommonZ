#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "implements matrices,vectors,quaternions with Numpy arrays for faster calculation"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "1.1.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2022-01"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = ['franco','Mike Day mday@insomniacgames.com']#passed maintainers and any other helpers
__contact__ = "syslog@laposte.net"# current contact address for more info about this file



### external module
import numpy as np          # matrices, vectors & quaternions are numpy arrays



### constants
DEFAULT_TYPE='f' #float

X=0
Y=1
Z=2
#W=3



### VECTORS CREATIONS
### functions returning a vector

### with the W Component 
### if equal 0, the vector is treated as a vector
### when being multiplied by a matrix it will not be translated, only rotated and scaled.
### If the W not equal 0, the vector is treated as a point
### when being multiplied by a matrix. it will be translated, rotated and scaled.

def vector(*iterable):
	"""shortcut to make numpy vector of any iterable(tuple,list...)"""
	return np.asarray( iterable if len(iterable) > 1 else iterable[0] ,dtype=DEFAULT_TYPE)

def normalized_vector(*iterable):
	"""shortcut to make numpy normalized vector of any iterable(tuple,list...)"""
	return normaliz_vector( vector(*iterable) )

def zeros_vector(size):
	"""Returns a vector of zeros"""
	return np.zeros(size,dtype=DEFAULT_TYPE)

def ones_vector(size):
	"""Returns a vector of ones"""
	return  np.ones(size,dtype=DEFAULT_TYPE)

def random_vector(size, mini=-1.0, maxi=1.0):
	"""Return a random vector"""
	dif=maxi-mini
	random_array =np.random.rand(size)*dif+mini
	return vector(random_array)


### VECTORS FUNCTIONS
### functions having at least one vector as parameter
### and returning a vector or anything else than matrix or quaternion

def scalar_product_vectors(vector_a,vector_b):
	"""scalar product of vectors a b ( . dot product)"""
	return np.dot(vector_a,vector_b)

def cross_product_vectors(vector_a,vector_b):
	"""cross product of vectors a b ( x * product)"""
	return np.cross(vector_a,vector_b)

def perpendicular_vector(vector_a,vector_b):
	"""gives a vector perpendicular to the plane formed by two 3Dvectors"""
	return cross_product_vectors(vector_a,vector_b)

def vector_length(vector):
	"""gives the length of the vector"""
	return np.linalg.norm(vector)

def normaliz_vector(vector):
	"""set vector length equal to 1"""
	norm = vector_length(vector)
	return vector / norm

def angle_between_normalized_vectors(vector_normalized_a,vector_normalized_b):
	"""give the 0<=angle<=π between the 2 normalized vectors."""
	### we can use cross product for find angle between 2 vectors
	### But there is an ambiguity problem for obtuse angles, which is why we don't usually use cross-products
	### Using a cross product will be useful only if you know that angles are in the range 0 to 90°
	### If you don't care about the sign of the angle, then we use the dot product
	### dot product give an angle in the range 0 to 180°
	return np.arccos( scalar_product_vectors( vector_normalized_a,vector_normalized_b ) )

def angle_between_vectors(vector_a,vector_b):
	"""give the 0<=angle<=π between the 2 vectors(no matter their length)."""
	return angle_between_normalized_vectors( normaliz_vector(vector_a),normaliz_vector(vector_b) )

def signed_angle_between_vectors(vector_a,vector_b,up):
	"""
	give the -π<=angle<=π between the 2 vectors(no matter their length)
	up can be a value or a vector, if up is positive the angle will be clockwise from 0<angle<=π, if negative -π<=angle<π
	"""
	dot_product= np.dot(vector_a,vector_b)
	cross_product= np.cross(vector_a,vector_b)
	return np.arctan2( np.dot(cross_product,up) , dot_product )

def check_vectors_direction(vector_a,vector_b):
	"""check if the two vectors are in the same direction"""
	return scalar_product_vectors(vector_a,vector_b)==1

def check_vectors_right_angle(vector_a,vector_b):
	"""check if the two vectors forms a right angle(90°)"""
	return scalar_product_vectors(vector_a,vector_b)==0

def check_vectors_opposite_direction(vector_a,vector_b):
	"""check if the two vectors are opposite(angle of 180°)"""
	return  scalar_product_vectors(vector_a,vector_b)==-1

def vector_projection(vector_a,vector_b):
	"""get the result of one vector projected on the other"""
	a=scalar_product_vectors(vector_a,vector_b)
	b=scalar_product_vectors(vector_b,vector_b)
	return a/b*vector_b

def symmetrical_vector(vector,axis):
	"""get the reflect of the given vector, from a symmetry axis"""
	proj=vector_projection(vector,axis)
	result = (proj-vector)*2+vector
	return result

def vector_direction(vector_a,vector_b):
	"""gives the vector from the first point to the second point"""
	return vector_b-vector_a

def vectors_lerp(vector_a, vector_b, fraction):
	"""linear interpolation between two vectors, where fraction is the proportion of vector_b"""
	return vector_a + fraction * vector_direction(vector_a,vector_b)

def scale_range_vector(vector,mini,maxi):
	"""return a vector with values in the interval of mini maxi"""
	scale=maxi-mini
	vmax=max(vector)
	vmin=min(vector)
	delta=vmax-vmin
	return ((vector-vmin)/delta) *scale+mini


### MATRIX CREATIONS
### functions returning a matrix

def identity_matrix():
	""""return a 4x4 identity matrix"""
	return np.identity(4,dtype=DEFAULT_TYPE)

def translate_matrix(x=0.0, y=0.0, z=0.0):
	"""return a matrix 4x4 for translation"""
	a= [1,0,0,x]
	b= [0,1,0,y]
	c= [0,0,1,z]
	d= [0,0,0,1]
	return np.array([a,b,c,d],dtype=DEFAULT_TYPE)

def scale_matrix(x=1.0, y=1.0, z=1.0):
	"""return a homothety 4x4 matrix"""
	a= [x,0,0,0]
	b= [0,y,0,0]
	c= [0,0,z,0]
	d= [0,0,0,1]
	return np.array([a,b,c,d],dtype=DEFAULT_TYPE)

def rotate_matrix(normalized_axis,radian_angle):
	"""return a 4x4 matrix for the axial rotation"""
	x=normalized_axis[X]
	y=normalized_axis[Y]
	z=normalized_axis[Z]
	c=np.cos(radian_angle)
	s=np.sin(radian_angle)
	nc = 1-c
	a= [x*x*nc+c,   x*y*nc-z*s, x*z*nc+y*s, 0]
	b= [y*x*nc+z*s, y*y*nc+c,   y*z*nc-x*s, 0]
	c= [x*z*nc-y*s, y*z*nc+x*s, z*z*nc+c,   0]
	d= [ 0 , 0 , 0 , 1. ]
	return np.array([a,b,c,d],dtype=DEFAULT_TYPE)

def matrix_from_quaternion(q):
	"""create 4x4 rotation matrix from a normalized quaternion"""
	nxx, nyy, nzz = -q[1]*q[1], -q[2]*q[2], -q[3]*q[3]
	qwx, qwy, qwz =  q[0]*q[1],  q[0]*q[2],  q[0]*q[3]
	qxy, qxz, qyz =  q[1]*q[2],  q[1]*q[3],  q[2]*q[3]
	a=[2*(nyy+nzz)+1, 2*(qxy-qwz),   2*(qxz+qwy),   0]
	b=[2*(qxy+qwz),   2*(nxx+nzz)+1, 2*(qyz-qwx),   0]
	c=[2*(qxz-qwy),   2*(qyz+qwx),   2*(nxx+nyy)+1, 0]
	d=[0, 0, 0, 1]
	return np.array([a,b,c,d],dtype=DEFAULT_TYPE)

def perspective_matrix(fov, aspect, near, far):
	"""
	return 4x4 perspective projection matrix,
	use horizontal Field_Of_View in radians
	near < far
	(16:9 screens) have aspect ratio = 1,77
	aspect=2.0 means the viewer's angle is twice as wide in x as it is in y
	"""
	sx = 1.0 / np.tan( fov/2.0 )
	sy = sx  * aspect
	zz = (far+near) / (near-far)
	zw = 2*far*near / (near-far)
	a=[sx, 0,  0,  0]
	b=[0,  sy, 0,  0]
	c=[0,  0, zz, zw]
	d=[0,  0, -1,  0]
	return np.array([a,b,c,d],dtype=DEFAULT_TYPE)

def frustum_matrix(xmin,xmax,ymin,ymax,zmin,zmax):
	"""return 4x4 frustum projection matrix same as glfrustum(l,r,b,t,n,f)"""
	va = (xmax+xmin) / (xmax-xmin)
	vb = (ymax+ymin) / (ymax-ymin)
	vc = -(zmax+zmin) / (zmax-zmin)
	vd = -2*zmax*zmin / (zmax-zmin)
	sx = 2*zmin / (xmax-xmin)
	sy = 2*zmin / (ymax-ymin)
	a=[sx, 0,  va, 0]
	b=[0, sy,  vb, 0]
	c=[0,  0,  vc, vd]
	d=[0,  0, -1, 0]
	return np.array([a,b,c,d],dtype=DEFAULT_TYPE)

def ortho_matrix(left,right,bottom,top,near,far):
	"""return matrix 4x4 same as glortho(l,r,b,t,n,f)"""
	dx= right - left
	dy= top - bottom
	dz= far - near
	rx= -(right+left) / dx
	ry= -(top+bottom) / dy
	rz= -(far+near) / dz
	a=[2/dx, 0,    0,     rx]
	b=[0,    2/dy, 0,     ry]
	c=[0,    0,    -2/dz, rz]
	d=[0,    0,    0,      1]
	return np.array([a,b,c,d],dtype=DEFAULT_TYPE)

def lookat_matrix(eye,target,up):
	"""
	Computes 4x4 view matrix from 3d 'eye' to 'target' vectors,
	with 'up' as normalized vector for orientation
	"""
	view = normaliz_vector(target-eye)
	right = np.cross(view,up)
	up = np.cross(right,view)
	rotation = np.identity(4)
	rotation[:3, :3] = np.vstack([right, up, -view])
	return rotation @ translate_matrix(0-eye[X],0-eye[Y],0-eye[Z])


### MATRIX FUNCTIONS
### functions having at least one matrix as parameter
### and returning a matrix or anything else than quaternion or vector

def translate_matrix_from_matrix(matrix):
	"""Return the position matrix from 4x4 transformation matrix"""
	x=matrix[0][3]
	y=matrix[1][3]
	z=matrix[2][3]
	return translate_matrix(x,y,z)

def scale_matrix_from_matrix(matrix):
	"""
	Return the scale matrix from 4x4 transformation matrix
	Doesn't work for negative scales
	"""
	sxv= vector( matrix[0][0],matrix[1][0],matrix[2][0] )
	syv= vector( matrix[0][1],matrix[1][1],matrix[2][1] )
	szv= vector( matrix[0][2],matrix[1][2],matrix[2][2] )
	return scale_matrix( vector_length(sxv),vector_length(syv),vector_length(szv) )

def rotate_matrix_from_matrix(matrix):
	"""
	Return the orientation matrix from 4x4 transformation matrix.
	The rotation matrix may produce a degenerate quaternion, but this is easy to detect during the conversion,
	"""
	new_matrix= scale_matrix_from_matrix(matrix)
	sv= vector( new_matrix[0][0],new_matrix[1][1],new_matrix[2][2] )
	new_matrix[0][:3]= matrix[0][:3] / sv
	new_matrix[1][:3]= matrix[1][:3] / sv
	new_matrix[2][:3]= matrix[2][:3] / sv
	return new_matrix


### QUATERNION CREATIONS
### functions returning a quaternion

def quaternion(w, x,y,z):
	"""create quaternion"""
	return np.array([w, x,y,z], dtype=DEFAULT_TYPE)

def quaternion_from_yaw(angle):
	"""
	get a quaternion from a pivoting Euler angle( in radians)
	"""
	angle/=2
	x=0
	y=np.sin(angle)
	z=0
	w=np.cos(angle)
	return quaternion(w, x,y,z)

def quaternion_from_roll(angle):
	"""
	get a quaternion from tilting to the side Euler angle( in radians)
	"""
	angle/=2
	x=0
	y=0
	z= np.sin(angle)
	w= np.cos(angle)
	return quaternion(w, x,y,z)

def quaternion_from_pitch(angle):
	"""
	get a quaternion from incline forward or backward Euler angle( in radians)
	"""
	angle/=2
	x=np.sin(angle)
	y=0
	z=0
	w=np.cos(angle)
	return quaternion(w, x,y,z)

def quaternion_from_axis_angle(normalized_axis,angle):
	"""get quaternion from normalized axis vector and radian angle around this axis"""
	angle/=2
	sin_angl = np.sin(angle)
	cos_angl = np.cos(angle)
	axis= normalized_axis*sin_angl
	w= cos_angl
	return quaternion(w, axis[X],axis[Y],axis[Z])

def quaternion_from_matrix(matrix):
	"""Return quaternion orientation from transformation matrix"""
	 ### there are many methods to obtain the quaternion from given rotation matrix
	 ### But they all have to deal with singularities
	if (matrix[2][2] < 0) :
		if matrix[0][0] > matrix[1][1] :
			t = 1 + matrix[0][0] - matrix[1][1] - matrix[2][2]
			q = ( t, matrix[1][0]+matrix[0][1], matrix[0][2]+matrix[2][0], matrix[2][1]-matrix[1][2] )
		else :
			t = 1 - matrix[0][0] + matrix[1][1] - matrix[2][2]
			q = ( matrix[1][0]+matrix[0][1], t, matrix[2][1]+matrix[1][2], matrix[0][2]-matrix[2][0] )
	else :
		if matrix[0][0] < 0-matrix[1][1] :
			t = 1 - matrix[0][0] - matrix[1][1] + matrix[2][2]
			q = ( matrix[0][2]+matrix[2][0], matrix[2][1]+matrix[1][2], t, matrix[1][0]-matrix[0][1] )
		else :
			t = 1 + matrix[0][0] + matrix[1][1] + matrix[2][2]
			q = ( matrix[2][1]-matrix[1][2], matrix[0][2]-matrix[2][0], matrix[1][0]-matrix[0][1], t )
	q= np.array(q,dtype=DEFAULT_TYPE)
	q *= 0.5 / np.sqrt(t)
	return quaternion(q[3],q[0],q[1],q[2])


### QUATERNION FUNCTIONS
### functions having at least one quaternion as parameter
### and returning a quaternion or anything else than matrix or vector

def quaternion_magnitude(q):
	"""gives the magnitude of the quaternion"""
	return np.sqrt( q[0]**2 + q[1]**2 + q[2]**2 + q[3]**2 )

def normalise_quaternion(q):
	"""set quaternion magnitude equal to 1"""
	norm = quaternion_magnitude(q)
	return quaternion( q[0]/norm, q[1]/norm, q[2]/norm, q[3]/norm )

def multiply_quaternions(q1, q2):
	"""compute quaternion from two quaternions"""
	a=[q1[0], -q1[1], -q1[2], -q1[3]]
	b=[q1[1],  q1[0], -q1[3],  q1[2]]
	c=[q1[2],  q1[3],  q1[0], -q1[1]]
	d=[q1[3], -q1[2],  q1[1],  q1[0]]
	m= np.array([a,b,c,d],dtype=DEFAULT_TYPE)
	return np.dot( m, q2 )

def quaternion_slerp(q0, q1, fraction):
	"""spherical interpolation of two normalized quaternions, where fraction is the proportion of q0"""
	dot = np.dot(q0, q1)
	### if negative dot product, the quaternions have opposite handedness
	### And slerp won't take the shorter path.
	### Fix by reversing one quaternion.
	q1, dot = (q1, dot) if dot > 0 else (-q1, -dot)
	theta_0 = np.arccos(np.clip(dot, -1, 1)) # angle between input vectors
	theta = theta_0*fraction                 # angle between q0 and result
	q2 = normaliz_vector(q1-q0*dot)          # {q0, q2} now orthonormal basis
	return q0*np.cos(theta) + q2*np.sin(theta)

def get_axis_angle(q):
	"""return axis as vector and the radian angle from the normalized quaternion"""
	
	### get the angle of rotation
	angle = np.arccos(q[0]) * 2 # * 180 / pi
	
	### get axis normalised
	axis = normalized_vector(q[1],q[2],q[3])
	
	return axis,angle

