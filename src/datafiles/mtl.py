#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "3D mtl file loader"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "3.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
__date__ = "2010"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### standard parameters
NEW_MTL='newmtl'
KA='Ka'
KD='Kd'
KS='Ks'
NS='Ns'
TF='Tf'
D='d'
TR='Tr'
ILLUM='illum'
SHARPNESS='sharpness'
NI='Ni'
### added parameters for extended format
KE='Ke'
PR='Pr'
PM='Pm'
PS='Ps'
PC= 'Pc'
PCR= 'Pcr'
ANISO='aniso'
ANISOR='anisor'



def get_values(data):
	"""return the formatted values from data"""
	if data[0]=="spectral" :
		if len(data[1:])==2 :
			values = ( data[1], float(data[2]) )
		else :
			values = ( data[1], 1.0 )
	elif data[0]=="xyz" :
		values = tuple(map(float, data[1:]))
	else :
		values = tuple(map(float,data))
	return values


def load_mtl_file(filepath):
	"""read 3D mtl file and return the data"""
	mat_lib={}
	with open(filepath, 'r') as data_file:
		for line in data_file.readlines() :
			if line.startswith('#'):
				continue
			data=line.split()
			if not len(data)==0 :
				signal=data[0]
				
				if signal==NEW_MTL :
					### specify material name
					name=data[1]
					material={}
					mat_lib[name]=material
					
				elif signal==KA :
					### specify the ambient reflectivity colors
					material[KA]=get_values(data[1:])
					
				elif signal==KD :
					### specify the diffuse reflectivity colors
					material[KD]=get_values(data[1:])
					
				elif signal==KS :
					### specify the specular reflectivity colors
					material[KS]=get_values(data[1:])
					
				elif signal==NS :
					### Specifies the specular exponent
					### This defines the focus of the specular highlight.
	 				### A high exponent results in a tight, concentrated highlight.
	 				### Ns values normally range from 0 to 1000.
					material[NS]=float(data[1])
					
				elif signal==TF :
					### specify the transmission filter of the current material
					### Any light passing through the object is filtered by the transmission filter,
					### which only allows the specifiec colors to pass through.
					### For example, Tf 0 1 0 allows all the green to pass through and filters out all the red and blue.
					material[TF]=get_values(data[1:])
					
				elif signal==D :
					### Specifies the dissolve factor for the current material.
	 				### the amount this material dissolves into the background.
	 				### A factor of 1.0 is fully opaque.
	 				### A factor of 0.0 is fully dissolved (completely transparent).
	 				### Unlike a real transparent material, the dissolve does not depend upon material thickness
					### if data[1]=="-halo" the dissolve factor is dependent on the surface orientation relative to the viewer.
					### For example, a sphere with "d -halo 0.0", is fully dissolved at its center and appear gradually more opaque toward its edge
					if data[1]=="-halo" :
						material[D]=( True , float(data[2]) )
					else :
						material[D]=( False , float(data[1]) )
					
				elif signal==TR :
					### inverted d
					### Tr = 1 - d
					material[TR]= float(data[1])
					
				elif signal==ILLUM :
					### specifies the illumination model
					### Illumination models are mathematical equations that represent various material lighting and shading effects.
	 				### "illum_#" can be a number from 0 to 10.
					### 0		Color on and Ambient off
					### 1		Color on and Ambient on
					### 2		Highlight on
					### 3		Reflection on and Ray trace on
					### 4		Transparency: Glass on
					### 		Reflection: Ray trace on
					### 5		Reflection: Fresnel on and Ray trace on
					### 6		Transparency: Refraction on
					### 		Reflection: Fresnel off and Ray trace on
					### 7		Transparency: Refraction on
					### 		Reflection: Fresnel on and Ray trace on
					### 8		Reflection on and Ray trace off
					### 9		Transparency: Glass on
					### 		Reflection: Ray trace off
					### 10		Casts shadows onto invisible surfaces
					material[ILLUM]=float(data[1])
					
				elif signal==SHARPNESS :
					### Specifies the sharpness of the reflections from the local reflection map.
					###  can be a number from 0 to 1000.  The default is 60.
					### A high value results in a clear reflection of objects in the reflection map.
					### If a material does not have a local reflection map defined in its material definition, sharpness will apply to the global reflection map defined in PreView.
					material[SHARPNESS]=float(data[1])
					
				elif signal==NI :
					### Specifies the optical density for the surface.
					### This is also known as index of refraction.
					### The values can range from 0.001 to 10. 
					### A value of 1.0 means that light does not bend as it passes through an object.
					### Increasing the optical_density increases the amount of bending.
					### Glass has an index of refraction of about 1.5.
					### Values of less than 1.0 produce bizarre results and are not recommended.
					material[NI]=float(data[1])
				
				elif signal in ('map_Ka','map_Kd','map_Ks','map_Ns','map_d','disp','decal','bump') :
					### maps are ignored 
					### because materials must be independent of mesh
					### but if a texture map is not specific to a mesh the applied result is distorted 
					pass
				
				
				### The creators of the online 3D editing and modeling tool Clara.io proposed extending the MTL format
				### the added parameters represent physically-based rendering parameters
				
				elif signal==KE:
					### specify the the color of emitted light.
					### to simulate surfaces such as neons, etc.
					material[KE]= tuple(map(float, data[1:]))
					
				elif signal==PR:
					### specify the roughness
					material[PR]= float(data[1])
					
				elif signal==PM:
					### specify the metallic
					material[PM]= float(data[1])
					
				elif signal==PS:
					### specify the sheen
					### Stimulating the effect of microscopic fibers or fuzz on surface.
					material[PS]= float(data[1])
					
				elif signal==PC:
					### specify clearcoat thickness
					### is a way to simulate the coating you can find in automotive car paint.
					### It usually is a transparent layer of paint that can be used to cover the colored coat.
					material[PC]= float(data[1])
					
				elif signal==PCR:
					### specify clearcoat roughness
					### is a way to simulate the coating you can find in automotive car paint.
					### It usually is a transparent layer of paint that can be used to cover the colored coat.
					material[PCR]= float(data[1])
				
				elif signal==ANISO:
					### anisotropy
					### By default materials are isotropic.
					### This means the shape of the reflection is identical in every direction.
					### Nevertheless, in real life some materials shows really elongated highlights.
					### For instance, looking an old vinyl disc, you can see the specular lighting being spread from the center to the border
					### or brushed metals
					material[ANISO]= float(data[1])
				
				elif signal==ANISOR:
					### anisotropy rotation
					### By default materials are isotropic.
					### This means the shape of the reflection is identical in every direction.
					### Nevertheless, in real life some materials shows really elongated highlights.
					### For instance, looking an old vinyl disc, you can see the specular lighting being spread from the center to the border
					### or brushed metals
					material[ANISOR]= float(data[1])
					
				elif signal in ('map_Pr','map_Pm','map_Ps','map_Ke','norm') :
					### maps are ignored 
					### because materials must be independent of mesh
					### but if a texture map is not specific to a mesh the applied result is distorted 
					pass
				
				else :
					#print("signal unknow: "+signal)
					pass
	
	return mat_lib
