#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "3D obj file loader"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "3.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
__date__ = "2010"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



MAT_LIB='mtllib'
USEMAT='usemat'
USEMTL='usemtl'
SMOOTH='s'
FACE='f'
GROUP='g'
OBJECTS='o'
V='v'
VT='vt'
VN='vn'
VP='vp'



def load_obj_file(filepath):
	"""read 3D obj file and return data"""
	#obj_file_list=[]
	objet={}
	objet[V]=[]
	objet[VT]=[]
	objet[VN]=[]
	objet[OBJECTS]={}
	with open(filepath, 'r') as data_file:
		for line in data_file.readlines() :
			if line.startswith('#'):
				continue
			data=line.split()
			if not len(data)==0 :
				signal=data[0]
				if signal==V :
					objet[V].append( tuple(map(float, data[1:4])) )
				elif signal==VT :
					objet[VT].append( tuple(map(float, data[1:3]))  )
				elif signal==VN:
					objet[VN].append( tuple(map(float, data[1:4])) )
				elif signal==VP:
					### Parameter space vertices not currently supported
					pass
				elif signal==SMOOTH:
					### smoothing-group not currently supported
					pass
				elif signal==FACE :
					face=[]
					for d in data[1:] :
						face.append( tuple(map(int,d.split('/'))) )
					face_list.append( tuple(face) )
				elif signal in (USEMTL,USEMAT) :
					material_name=data[1]
					if not mat_lib_name in materials :
						materials[mat_lib_name]={}
					mat_lib=materials[mat_lib_name]
					if not material_name in mat_lib :
						mat_lib[material_name]=[]
					face_list=mat_lib[material_name]
				elif signal==GROUP :
					materials={}
					groups[data[1]]=materials
				elif signal==OBJECTS :
					groups={}
					objet[OBJECTS][data[1]]=groups
				elif signal==MAT_LIB :
					mat_lib_name=data[1]
				else :
					#print("signal unknow: "+signal)
					pass
	return objet


