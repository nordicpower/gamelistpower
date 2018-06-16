#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                              - GAMELISTPOWER -                               #
#                             - MODULE ES_SYSTEM -                             #
#------------------------------------------------------------------------------#
# Manipulation des fichiers de configuration es_systems.cfg + es_settings.cfg  #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.00 03/04/2017-10/06/2018 #
################################################################################

#IMPORT STD---------------------------------------------------------------------
from xml.dom import minidom
from xml.parsers import expat
from operator import attrgetter, itemgetter
import traceback
import re

#IMPORT NORDICPOWER-------------------------------------------------------------
from glpTOOLS import *
from glpRECALBOX import *

#CONSTANTS----------------------------------------------------------------------
EMPTY_FOLDER='/home/pi/vide'

#MSG LOCALISATION---------------------------------------------------------------
config=Config()

msg_local={
('MSG_ERROR_GLE_EXCEPTION','FR'):u'{} : {}',
('MSG_ERROR_GLE_EXCEPTION','EN'):u'{} : {}'
}

#INIT SINGLETON-----------------------------------------------------------------
logger=Logger.logr

#CLASS-ESSYSTEM-----------------------------------------------------------------
class ESSystem:
	"""Classe POJO ESSystemEmulator du tag <system>"""
		
	def __init__(self,**kwargs):
		self._fullname=''
		self._name=''
		self._desc=''
		self._path=''
		self._path_desac='' #Happigc
		self._extension=''
		self._command=''
		self._platform=''
		self._theme=''
		self._usermode=''   #Happigc
		self._emulators=[]  #Recalbox
		
		if kwargs is not None:
			#mise à jour paramètre(s) nommé(s)
			self.__dict__.update(kwargs)
	
	def __repr__(self):
		return repr((self.name))
	
	#property-------------------------	
	@property
	def fullname(self):return self._fullname
	@property
	def name(self):return self._name
	@property
	def desc(self):return self._desc
	@property
	def path(self):return self._path
	@property
	def path_desac(self):return self._path_desac
	@property
	def extension(self):return self._extension
	@property
	def command(self):return self._command
	@property
	def platform(self):return self._platform
	@property
	def theme(self):return self._theme
	@property
	def usermode(self):return self._usermode
	@property
	def emulators(self):return self._emulators
	
	#enhanced property-------------------------	
	def getDefaultEmulator(self):
		if self.emulators == []:
			RecalBoxEmulators = getRecalBoxEmulators()
			if self.name in RecalBoxEmulators:
				#Valeur dans emulatorlauncher.py
				return RecalBoxEmulators[self.name].emulator
			else:
				#Nouveau systeme ?
				return 'default'
		else:
			#Valeur dans es_system.cfg
			return self.emulators[0].name
	
	def getDefaultEmulatorCore(self):
		if self.emulators == []:
			return 'default'
		else:
			if self.emulators[0].cores == []:
				return 'default'
			else:
				return self.emulators[0].cores[0]
	
	#setter-------------------------	
	@fullname.setter
	def fullname(self,v):self._fullname=v
	@name.setter
	def name(self,v):self._name=v
	@desc.setter
	def desc(self,v):self._desc=v		
	@path.setter
	def path(self,v):self._path=v
	@path_desac.setter
	def path_desac(self):return self._path_desac
	@extension.setter
	def extension(self,v):self._extension=v
	@command.setter
	def command(self,v):self._command=v
	@platform.setter
	def platform(self,v):self._platform=v
	@theme.setter
	def theme(self,v):self._theme=v
	@usermode.setter
	def usermode(self,v):self._usermode=v
	@emulators.setter
	def emulators(self,v):self._emulators=v

	

#CLASS-ESSYSTEMEMULATOR---------------------------------------------------------
class ESSystemEmulator:
	"""Classe POJO ESSystemEmulator du tag <emulator>"""
		
	def __init__(self,**kwargs):
		self._name=''
		self._cores=[]
		
		if kwargs is not None:
			#mise à jour paramètre(s) nommé(s)
			self.__dict__.update(kwargs)
	
	def __repr__(self):
		return repr((self.name))
	
	#property-------------------------	
	@property
	def name(self):return self._name
	@property
	def cores(self):return self._cores
	
	#setter-------------------------	
	@name.setter
	def name(self,v):self._name=v
	@cores.setter
	def cores(self,v):self._cores=v		

#CLASS-ESSYSTEMS----------------------------------------------------------------
class ESSystemList:
	"""Classe ESSystemList du tag <systemList> + fonctions de manipulation"""
	
	_CLASS_SYSTEM_NODENAME="system"
	_CLASS_SYSTEMLIST_NODENAME="systemList"
	_CLASS_EMULATORS_NODENAME='emulators'
	_CLASS_EMULATOR_NODENAME='emulator'
	_CLASS_CORES_NODENAME='cores'
	_CLASS_CORE_NODENAME='core'
	
	def __init__(self,**kwargs):		
		self._XmlDom = minidom.getDOMImplementation()
		if kwargs is not None:
			#mise à jour paramètre(s) nommé(s)
			self.__dict__.update(kwargs)
	
	
	#- I/O ---------------------------------------------------------------------------
	
	def import_xml_file(self,fullpathname):
		try:
			self._XmlDom = minidom.parse(fullpathname)
			
		except (expat.ExpatError):
			trace_message = traceback.format_exc(0).split('\n')[1]
			logger.error(msg_local.get(('MSG_ERROR_GLE_EXCEPTION',config.language)).format('ESSystemList.import_xml_file',trace_message))		
			raise MyError('xml malformed')
				
		except Exception as exception:
			logger.error(msg_local.get(('MSG_ERROR_GLE_EXCEPTION',config.language)).format('ESSystemList.import_xml_file',type(exception).__name__))
			raise MyError('tech exception')

	def save_xml_file(self,fullpathname):
		#Ecriture sur disque
		f = open(fullpathname,'w')
		f = codecs.lookup("utf-8")[3](f)
		self._XmlDom.writexml(f, encoding="utf-8")
		f.close()

	#- base XML manipulation ---------------------------------------------------------------------------
	
	def __get_sub_element_value(self,node,elementname):
		"""read value of element return empty if not exist"""
		try:
			return node.getElementsByTagName(elementname)[0].firstChild.nodeValue
		except (AttributeError,IndexError):
			pass
		except Exception as exception:
			logger.warn(msg_local.get(('MSG_ERROR_GLE_EXCEPTION',config.language)).format('ESSystemList.__get_sub_element_value',type(exception).__name__))
		return ''
		
	def __set_sub_element_value(self,node,elementname,value):
		"""write value of element"""
		try:
			if value=='':
				node.removeChild(node.getElementsByTagName(elementname)[0])
				
			else:
				node.getElementsByTagName(elementname)[0].firstChild.nodeValue=value

		except (AttributeError,IndexError):
			if value !='':
					self.__add_subelement_node_text(node,elementname,value)
		except Exception as exception:
			logger.warn(msg_local.get(('MSG_ERROR_GLE_EXCEPTION',config.language)).format('GamesList.__set_sub_element_value',type(exception).__name__))
		return ''

	def __add_subelement_node_text(self,node,subnodename,subnodevalue):
		"""ajouter un nouveau noeud avec du texte"""
		new_dom_node_subelement = self._XmlDom.createElement(subnodename)
		new_dom_node_subelement_text = self._XmlDom.createTextNode( subnodevalue )
		new_dom_node_subelement.appendChild(new_dom_node_subelement_text)
		node.appendChild(new_dom_node_subelement)

	#- recherche et lecture XML --------------------------------------------------

	def __search_node_by_path_eq(self,node_type,search_path):
		"""search node element by path and return objet """
		###recherche classique
		tag_path = self._XmlDom.getElementsByTagName("path")
		for element in tag_path:
			if element.firstChild.nodeValue == search_path:
				if element.parentNode.nodeName == node_type:
					if element.parentNode.nodeName == self._CLASS_SYSTEM_NODENAME:
						return self.__get_system_from_element(element.parentNode)
					else:
						raise MyError('Unknow node')
				else:
					raise MyError('Not Found1')
		
		###recherche sur une plateforme désactivee
		tag_path = self._XmlDom.getElementsByTagName("path-desac")
		for element in tag_path:
			if element.firstChild.nodeValue == search_path:
				if element.parentNode.nodeName == node_type:
					if element.parentNode.nodeName == self._CLASS_SYSTEM_NODENAME:
						return self.__get_system_from_element(element.parentNode)
					else:
						raise MyError('Unknow node')
				else:
					raise MyError('Not Found1')
		
		###Fin
		raise MyError('Not Found2')


	def __search_node_by_path_in(self,node_type,search_path):
		"""search node element by contains value in path and return objet """
		###recherche classique
		tag_path = self._XmlDom.getElementsByTagName("path")
		for element in tag_path:
			if search_path in element.firstChild.nodeValue:
				if element.parentNode.nodeName == node_type:
					if element.parentNode.nodeName == self._CLASS_SYSTEM_NODENAME:
						return self.__get_system_from_element(element.parentNode)
					else:
						raise MyError('Unknow node')
				else:
					raise MyError('Not Found1')
					
		###recherche sur une plateforme désactivee
		tag_path = self._XmlDom.getElementsByTagName("path-desac")
		for element in tag_path:
			if element.firstChild.nodeValue == search_path:
				if element.parentNode.nodeName == node_type:
					if element.parentNode.nodeName == self._CLASS_SYSTEM_NODENAME:
						return self.__get_system_from_element(element.parentNode)
					else:
						raise MyError('Unknow node')
				else:
					raise MyError('Not Found1')
		
		###Fin
		raise MyError('Not Found2')
		
			
	def __get_nodes_by_type(self,node_type):
		"""search node elements by their node_type return list objet """
		list_element = []
		tag_path = self._XmlDom.getElementsByTagName(node_type)
		for element in tag_path:
			list_element.append(self.__get_system_from_element(element))
		return list_element

		
	def __get_system_from_element(self,element):
		"""convert dom element to pojo game"""
		esSystem = ESSystem()
		##Lecture des noeuds fils
		esSystem.fullname = self.__get_sub_element_value(element,"fullname")
		esSystem.name = self.__get_sub_element_value(element,"name")
		esSystem.desc = self.__get_sub_element_value(element,"desc")
		esSystem.path = self.__get_sub_element_value(element,"path")
		esSystem.path_desac = self.__get_sub_element_value(element,"path-desac")
		esSystem.extension = self.__get_sub_element_value(element,"extension")
		esSystem.command = self.__get_sub_element_value(element,"command")
		esSystem.platform = self.__get_sub_element_value(element,"platform")
		esSystem.theme = self.__get_sub_element_value(element,"theme")
		esSystem.usermode = self.__get_sub_element_value(element,"usermode")
		
		#Lecture des noeuds emulators/emulator/cores/core
		eSSystemEmulators = []
		try:
			nodeEmulators = element.getElementsByTagName("emulators")[0]
			for nodeEmulator in nodeEmulators.getElementsByTagName("emulator"):
				eSSystemEmulator=ESSystemEmulator(name=nodeEmulator.getAttribute("name"))
				try:
					nodeCores = nodeEmulator.getElementsByTagName("cores")[0]
					eSSystemEmulator.cores=[]
					for nodeCore in nodeCores.getElementsByTagName("core"):
						eSSystemEmulator.cores.append(nodeCore.firstChild.nodeValue)
				except (AttributeError,IndexError): #si aucun noeud <cores>
					pass
				#print 'emulator:'+eSSystemEmulator.name
				#for core in eSSystemEmulator.cores:
				#	print 'core:'+core
				eSSystemEmulators.append(eSSystemEmulator)
		except (AttributeError,IndexError): #si aucun noeud <emulators> ou <emulator>
			pass
		esSystem.emulators = eSSystemEmulators
		
		return esSystem

		
	def search_system_by_path(self,search_path):
		"""search system element by path and return objet """
		return self.__search_node_by_path_eq(self._CLASS_SYSTEM_NODENAME,search_path)
	
	def search_system_by_short_path(self,search_path):
		"""search system element by path and return objet """
		if os.name=='posix':
			return self.__search_node_by_path_in(self._CLASS_SYSTEM_NODENAME,search_path)
		else:
			#Pour besoin test sous Windows
			return self.__search_node_by_path_in(self._CLASS_SYSTEM_NODENAME,search_path.replace(os.path.sep,'/'))

	def get_systems(self):
		"""get alls system elements"""
		return self.__get_nodes_by_type(self._CLASS_SYSTEM_NODENAME)		
	
	
	#- mise à jour XML ---------------------------------------------------------------------------
	def add_system(self,addsys):
		systemlist_element = self._XmlDom.getElementsByTagName(self._CLASS_SYSTEMLIST_NODENAME)
		newdom_system_element = self._XmlDom.createElement(self._CLASS_SYSTEM_NODENAME)
		if addsys.fullname!='':
			self.__add_subelement_node_text(newdom_system_element,"fullname",addsys.fullname)
		if addsys.name!='':
			self.__add_subelement_node_text(newdom_system_element,"name",addsys.name)
		if addsys.desc!='':
			self.__add_subelement_node_text(newdom_system_element,"desc",addsys.desc)
		if addsys.path!='':
			self.__add_subelement_node_text(newdom_system_element,"path",addsys.path)
		if addsys.path_desac!='':
			self.__add_subelement_node_text(newdom_system_element,"path-desac",addsys.path_desac)
		if addsys.extension!='':
			self.__add_subelement_node_text(newdom_system_element,"extension",addsys.extension)
		if addsys.command!='':
			self.__add_subelement_node_text(newdom_system_element,"command",addsys.command)
		if addsys.platform!='':
			self.__add_subelement_node_text(newdom_system_element,"platform",addsys.platform)
		if addsys.theme!='':
			self.__add_subelement_node_text(newdom_system_element,"theme",addsys.theme)
		if addsys.usermode!='':
			self.__add_subelement_node_text(newdom_system_element,"usermode",addsys.usermode)
		
		#Ecriture des noeuds emulators/emulator/cores/core
		if not addsys.emulators == []:
			new_dom_emulators_element = self._XmlDom.createElement(self._CLASS_EMULATORS_NODENAME)
			for emulator in addsys.emulators:
				new_dom_emulator_element = self._XmlDom.createElement(self._CLASS_EMULATOR_NODENAME)
				new_dom_emulator_element.setAttribute("name",emulator.name)
				if not emulator.cores == []:
					new_dom_cores_element = self._XmlDom.createElement(self._CLASS_CORES_NODENAME)
					for core in emulator.cores:
						new_dom_core_element = self._XmlDom.createElement(self._CLASS_CORE_NODENAME)
						new_dom_core_element_text = self._XmlDom.createTextNode(core)
						new_dom_core_element.appendChild(new_dom_core_element_text)
						new_dom_cores_element.appendChild(new_dom_core_element)
					new_dom_emulator_element.appendChild(new_dom_cores_element)
				new_dom_emulators_element.appendChild(new_dom_emulator_element)
			newdom_system_element.appendChild(new_dom_emulators_element)
		
		#Ajout du noeud system à l'arbre existant
		systemlist_element[0].appendChild(newdom_system_element)
		
	def update_system(self,updsys):
		"""update existing system node in dom"""
		#tagpath = self._XmlDom.getElementsByTagName("path")
		tagpath = self._XmlDom.getElementsByTagName("name")
		
		for element in tagpath:
			
			if element.firstChild.nodeValue == updsys.name:
				systemp_node = element.parentNode
				#Sous-Elements du noeud system
				self.__set_sub_element_value(systemp_node,"fullname",updsys.fullname)
				self.__set_sub_element_value(systemp_node,"name",updsys.name)
				self.__set_sub_element_value(systemp_node,"desc",updsys.desc)
				self.__set_sub_element_value(systemp_node,"path",updsys.path)
				self.__set_sub_element_value(systemp_node,"path-desac",updsys.path_desac)
				self.__set_sub_element_value(systemp_node,"extension",updsys.extension)
				self.__set_sub_element_value(systemp_node,"command",updsys.command)
				self.__set_sub_element_value(systemp_node,"platform",updsys.platform)
				self.__set_sub_element_value(systemp_node,"theme",updsys.theme)
				self.__set_sub_element_value(systemp_node,"usermode",updsys.usermode)
				
				#Ecriture des noeuds emulators/emulator/cores/core
				try:
					systemp_node.removeChild(systemp_node.getElementsByTagName(self._CLASS_EMULATORS_NODENAME)[0])
				except (AttributeError,IndexError):
					pass
						
				if not updsys.emulators == []:
					new_dom_emulators_element = self._XmlDom.createElement(self._CLASS_EMULATORS_NODENAME)
					for emulator in updsys.emulators:
						new_dom_emulator_element = self._XmlDom.createElement(self._CLASS_EMULATOR_NODENAME)
						new_dom_emulator_element.setAttribute("name",emulator.name)
						if not emulator.cores == []:
							new_dom_cores_element = self._XmlDom.createElement(self._CLASS_CORES_NODENAME)
							for core in emulator.cores:
								new_dom_core_element = self._XmlDom.createElement(self._CLASS_CORE_NODENAME)
								new_dom_core_element_text = self._XmlDom.createTextNode(core)
								new_dom_core_element.appendChild(new_dom_core_element_text)
								new_dom_cores_element.appendChild(new_dom_core_element)
							new_dom_emulator_element.appendChild(new_dom_cores_element)
						new_dom_emulators_element.appendChild(new_dom_emulator_element)
					systemp_node.appendChild(new_dom_emulators_element)

				
				
	#- activation / desactivation ---------------------------------------------------------------------------
	
	def deactivate_system(self,disabled_sys):
		"""Disabled a system by change his path"""
		if disabled_sys.path != EMPTY_FOLDER:
			disabled_sys.path_desac = disabled_sys.path
			disabled_sys.path = EMPTY_FOLDER
			self.update_system(disabled_sys)
		
	def activate_system(self,enabled_sys):
		"""Disabled a system by change his path"""
		if enabled_sys.path_desac!="":
			enabled_sys.path = enabled_sys.path_desac
		enabled_sys.path_desac =''
		self.update_system(enabled_sys)

#CLASS-ESconfig-----------------------------------------------------------------
class ESSettings:
	"""ESconfig Class to load or save es_settings.cfg"""

	def __init__(self,**kwargs):

		self._conf_dict = dict()
		
		if kwargs is not None:
			#mise à jour paramètre(s) nommé(s)
			self.__dict__.update(kwargs)
	
	#property-------------------------	
	@property
	def conf_dict(self):return self._conf_dict	
		
	#- I/O ---------------------------------------------------------------------------
	def import_es_settings(self,fullpathname):
		try:
			f = open(fullpathname).readlines()
			firstLine = f.pop(0)
			for line in f:
				line=line.replace('\n','')
				if (line==""):
					break
				decoding=re.findall("""\w+="[^"]*"|\w+='[^']*'|\w+=\w+|\w+""", line)
				name=decoding[1].replace('"',"")
				name=name.replace("name=","")
				value=decoding[2].replace('"',"")
				value=value.replace('=',"")
				value=value.replace("value","")
				
				self._conf_dict[decoding[0],name]=value
				
		except Exception as exception:
			logger.error(msg_local.get(('MSG_ERROR_GLE_EXCEPTION',config.language)).format('ESSystemList.import_es_settings',type(exception).__name__))
			raise MyError('tech exception')

	def save_es_settings(self,fullpathname):
		#Ecriture sur disque
		f = open(fullpathname,"w")
		format_write='\n<{} name=\"{}\" value=\"{}\" />'
		f.write("<?xml version=\"1.0\"?>")
		
		for key_config in sorted(self._conf_dict):
			value_config=self._conf_dict[key_config]
			f.write(format_write.format(key_config[0],key_config[1],value_config))
		f.close
		

	
class FileDirThemes:
	"""load all themes directory in a dict"""	
	def __init__(self,v_root,**kwargs):
		self._root=v_root
		self._theme_dict=dict()
		self._theme_img=dict()
		
	#property-------------------------	
	@property
	def theme_dict(self):return self._theme_dict
	@property
	def theme_img(self):return self._theme_img
	
	def read_themes(self):
	
		for themedir in os.listdir(self._root):
		
			#Lecture commentaire du theme
			fullpath_theme_xml=os.path.join(self._root,themedir,themedir.lower()+".xml")
			if os.path.isfile(fullpath_theme_xml):
			
				theme_name=''
				theme_version=''
				theme_author=''
				
				with open(fullpath_theme_xml,"r") as f:
					while True:
						line=f.readline()
						if not line: break
						if "-->" in line :break
						if "<!--" in line:continue
						line = line.replace('\n','')
						if "theme name" in line:
							theme_name = line.replace("theme name:","").replace("\"","").strip()
						if "version" in line:
							theme_version = line.replace("version:","").strip()
						if "author" in line:
							theme_author = line.replace("author:","").strip()
							
				f.close
				
				self._theme_dict[themedir] = theme_name+' '+theme_version+' de '+theme_author
			
			#Gestion de l'image preview
			if os.path.isfile(os.path.join(self._root,themedir,"preview.png")):
				self._theme_img[themedir]	= os.path.join(self._root,themedir,"preview.png")
			else:
				self._theme_img[themedir]	= ""
			