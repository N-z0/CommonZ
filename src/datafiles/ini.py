#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "INI File Reading and Writing."#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "2.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
__date__ = "2021"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



class Parser:
	def __init__(self,pathname):
		"""
		This ini parser is able to write back the data with comments
		also can handle different characters signs for comment and keys value
		"""
		
		self.pathname = pathname
		
		self.parse=[]
		### read and store the data from the given ini file
		with open(self.pathname,'r') as f:
			### A file is already an iterable full of lines.
			### And it's a smart iterable, reading lines as you need them, with some clever buffering under the covers.
			### .readlines() reads all the file into memory before starting to loop
			for line in f :
				### seperate data and comments
				hash_index=line.find("#")
				semicolon_index=line.find(";")
				if hash_index>semicolon_index :
					line=line.split("#",1)
					comment="#"+line[1]
					data=line[0]
				elif hash_index<semicolon_index :
					line=line.split(";",1)
					comment=";"+line[1]
					data=line[0]
				else :
					comment=''
					data=line
				### 
				data=data.strip()
				comment=comment.strip()
				equal_index=data.find("=")
				colon_index=data.find(":")
				if data.startswith('[') and data.endswith(']') :
					section = data.strip("[]")
					self.parse.append(["[]",section,comment])
				elif equal_index<colon_index :
					pair = data.split(":",1)
					key = pair[0].strip()
					value = pair[1].strip()
					self.parse.append([":",key,value,comment])
				elif equal_index>colon_index :
					pair = data.split("=",1)
					key = pair[0].strip()
					value = pair[1].strip()
					self.parse.append(["=",key,value,comment])
				elif data=='' :
					self.parse.append(['','',comment])
				else :
					print(line)
					raise EOFError
	
	
	def get_sections(self):
		"""get the list of all sections names"""
		return [data[1] for data in self.parse if data[0]=="[]"]
	
	
	def get_keys(self,section):
		"""get the list of keys found under specified section"""
		keys_list=[]
		collect=False
		for data in self.parse :
			if data[0]=="[]" :
				if data[1]==section :
					collect=True
				elif collect :
					break
				else:
					pass
			elif collect and (data[0]==":" or data[0]=="=") :
				keys_list.append(data[1])
			else :
				pass
		return keys_list
	
	
	def get_valu(self,section,key):
		"""get the valu for the specified section and key"""
		collect=False
		for data in self.parse :
			if data[0]=="[]" :
				if data[1]==section :
					collect=True
				elif collect :
					return None
				else:
					pass
			elif collect and (data[0]==":" or data[0]=="=") and data[1]==key :
				return data[2]
			else :
				pass
	
	
	def set_valu(self,section,key,valu):
		"""set the valu for the specified section and key"""
		collect=False
		for data_index in range(len(self.parse)) :
			data=self.parse[data_index]
			if data[0]=="[]" :
				if data[1]==section :
					collect=True
				elif collect :
					break
				else:
					pass
			elif collect and (data[0]==":" or data[0]=="=") and data[1]==key :
				self.parse[data_index][2]=valu
			else :
				pass
	
	
	def get_dictionary(self):
		"""return a dictionary containing all section keys value"""
		dico={}
		for data in self.parse :
			if data[0]=="[]" :
				section=data[1]
				dico[section]={}
			elif data[0]==":" or data[0]=="=" :
				key=data[1]
				valu=data[2]
				dico[section].update({key:valu})
			else :
				pass
		return dico
	
	
	def write_file(self,pathname=None):
		"""write the ini file"""
		if not pathname :
			pathname=self.pathname
		with open(pathname,'w') as f:
			for data in self.parse :
				if data[0]=='[]' :
					section=data[1]
					comment=data[2]
					f.write( '[{}] {}\n'.format(section,comment) )
				elif data[0]==':' or data[0]=='=' :
					separator=data[0]
					key=data[1]
					valu=data[2]
					comment=data[3]
					f.write( '{} {} {} {}\n'.format(key,separator,valu,comment) )
				elif data[2] :
					comment=data[2]
					f.write( '{}\n'.format(comment) )
				else :
					f.write( '\n')
				f.write( '\n' )
