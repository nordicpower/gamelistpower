#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                              - GAMELISTPOWER -                               #
#                              - MODULE RULES -                                #
#------------------------------------------------------------------------------#
# Manipulation du fichier de regle pour le module GAMEGEN                      #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.12 28/05/2018-16/03/2019 #
################################################################################

#IMPORT STD---------------------------------------------------------------------
from xml.dom import minidom
from xml.parsers import expat
from operator import attrgetter, itemgetter
import traceback
import re
import os

#IMPORT NORDICPOWER-------------------------------------------------------------
from glpTOOLS import *
from glpXML import * 

#MSG LOCALISATION---------------------------------------------------------------
config=Config()

msg_local={
('MSG_WARN_RUL_SOURCE_NOT_SUPPORTED','FR'):u'Source {} non support\u00E9 dans la r\u00E8gle: {}',
('MSG_WARN_RUL_SOURCE_NOT_SUPPORTED','EN'):u'Source {} not supported in this rule: {}',
('MSG_WARN_RUL_FOLDER_CREATION','FR'):u'Cr\u00E9 du dossier : {}',
('MSG_WARN_RUL_FOLDER_CREATION','EN'):u'Folder created: {}',
('MSG_INFO_RUL_GAMELIST_LOADED','FR'):u'R\u00E8gle {}: le fichier {} a \u00E9t\u00E9 charg\u00E9',
('MSG_INFO_RUL_GAMELIST_LOADED','EN'):u'Rule {}: File {} is successfully loaded',
('MSG_ERROR_RUL_EXCEPTION','FR'):u'{} : {}',
('MSG_ERROR_RUL_EXCEPTION','EN'):u'{} : {}'
}

#CONSTANTS----------------------------------------------------------------------
SOURCE_ATTR_PATH      ='path'
SOURCE_ATTR_GENRE     ='genre'
SOURCE_ATTR_NAME      ='name'
SOURCE_ATTR_DEVELOPER ='developer'
SOURCE_ATTR_PUBLISHER ='publisher'
SOURCE_ATTR_PLAYERS   ='players'

TYPE_RULE_GENSH  = 'gensh'
TYPE_RULE_ROMCPY = 'romcpy'

#INIT SINGLETON-----------------------------------------------------------------
logger=Logger.logr

#CLASS-RULE---------------------------------------------------------------------
class Rule:
	"""POJO Stockage d'une règle"""
	def __init__(self,**kwargs):
		self._name=''
		self._type=''
		self._source=''
		self._search=''
		self._dest_path=''
		self._dest_path_name=''
		self._exclusion_files=[]
		self._image_background=''
		self._image_screenshot=''
		self._image_logo=''
		self._textcolor=''
		self._preserveFavorite=''
		self._gamelistInfoFile=''
		self._gamelistInfo = GamesList()
		self._gamelistLoaded = False
		
		if kwargs is not None:
			#mise à jour paramètre(s) nommé(s)
			self.__dict__.update(kwargs)

	def __repr__(self):
		return repr((self.name, self.source, self.search,self.dest_path,'|'.join(map(str, self.exclusion_files))))
        	
	#property-------------------------	
	@property
	def name(self):return self._name
	@property
	def type(self):return self._type
	@property
	def source(self):return self._source
	@property
	def search(self):return self._search
	@property
	def dest_path(self):return self._dest_path
	@property
	def dest_path_name(self):return self._dest_path_name
	@property
	def exclusion_files(self):return self._exclusion_files
	@property
	def image_background(self):return self._image_background
	@property
	def image_screenshot(self):return self._image_screenshot
	@property
	def image_logo(self):return self._image_logo
	@property
	def textcolor(self):return self._textcolor
	@property
	def preserveFavorite(self):return self._preserveFavorite
	@property
	def gamelistInfoFile(self):return self._gamelistInfoFile
	@property
	def gamelistInfo(self):return self._gamelistInfo
	@property
	def gamelistLoaded(self):return self._gamelistLoaded
	
	#setter-------------------------	
	@name.setter
	def name(self,v):self._name=v
	@type.setter
	def type(self,v):self._name=v
	@source.setter
	def source(self,v):self._source=v
	@search.setter
	def search(self,v):self._search=v
	@dest_path.setter
	def dest_path(self,v):self._dest_path=v
	@dest_path_name.setter
	def dest_path_name(self,v):self._dest_path_name=v
	@dest_path.setter
	def exclusion_files(self,v):self._exclusion_files=v
	@dest_path.setter
	def image_background(self,v):self._image_background=v
	@dest_path.setter
	def image_screenshot(self,v):self._image_screenshot=v
	@dest_path.setter
	def image_logo(self,v):self._image_logo=v
	@textcolor.setter
	def textcolor(self,v):self._textcolor=v
	@preserveFavorite.setter
	def preserveFavorite(self,v):self._preserveFavorite=v
	
	@gamelistInfoFile.setter
	def gamelistInfoFile(self,v):self._gamelistInfoFile=v
	@gamelistInfo.setter
	def gamelistInfo(self,v):self._gamelistInfo=v
		
#CLASS-RULEEXCEPTION---------------------------------------------------------
class RuleException:
	"""Classe POJO GameGenRuleException du tag <exclusion>"""
		
	def __init__(self,**kwargs):
		self._filename=''
		
		if kwargs is not None:
			#mise à jour paramètre(s) nommé(s)
			self.__dict__.update(kwargs)
	
	def __repr__(self):
		return repr((self.filename))
	
	#property-------------------------	
	@property
	def filename(self):return self._filename
	
	#setter-------------------------	
	@filename.setter
	def filename(self,v):self._filename=v

#CLASS-DecodeXMLRules----------------------------------------------------------------
class DecodeXMLRules:
	"""Classe DecodeXMLRules du tag <rules> + fonctions de manipulation"""
	
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
			logger.error(msg_local.get(('MSG_ERROR_RUL_EXCEPTION',config.language)).format('DecodeXMLRules.import_xml_file',trace_message))		
			raise MyError('xml malformed')
				
		except Exception as exception:
			logger.error(msg_local.get(('MSG_ERROR_RUL_EXCEPTION',config.language)).format('DecodeXMLRules.import_xml_file',type(exception).__name__))
			raise MyError('tech exception')

	#- base XML manipulation ---------------------------------------------------------------------------
	def __get_sub_element_value(self,node,elementname):
		"""read value of element return empty if not exist"""
		try:
			return node.getElementsByTagName(elementname)[0].firstChild.nodeValue
		except (AttributeError,IndexError):
			pass
		except Exception as exception:
			logger.warn(msg_local.get(('MSG_ERROR_RUL_EXCEPTION',config.language)).format('DecodeXMLRules.__get_sub_element_value',type(exception).__name__))
		return ''

	#- recherche et lecture XML --------------------------------------------------

	def __search_node_by_name_eq(self,search_name):
		"""search node element by name and return objet """
		tag_name = self._XmlDom.getElementsByTagName("name")
		for element in tag_name:
			if element.firstChild.nodeValue == search_name:
				
				if element.parentNode.nodeName == 'rule':
					return self.__get_system_from_element(element.parentNode)
				else:
					raise MyError('Unknow node')
					
		###Fin
		raise MyError('Not Found2')
	
			
	def __get_nodes_by_type(self,node_type):
		"""search node elements by their node_type return list objet """
		list_element = []
		tag_path = self._XmlDom.getElementsByTagName(node_type)
		for element in tag_path:
			list_element.append(self.__get_rule_from_element(element))
		return list_element

		
	def __get_rule_from_element(self,element):
		"""convert dom element to pojo game"""
		gameGenRule = Rule()
		
		##Lecture des noeuds fils
		gameGenRule.name = self.__get_sub_element_value(element,"name")
		gameGenRule.source = self.__get_sub_element_value(element,"searchAttribute")
		gameGenRule.search = self.__get_sub_element_value(element,"searchValue")
		gameGenRule.dest_path = self.__get_sub_element_value(element,"destination")
		gameGenRule.dest_path_name = self.__get_sub_element_value(element,"destinationName")
		gameGenRule.image_background = self.__get_sub_element_value(element,"imageBackground")
		gameGenRule.image_screenshot = self.__get_sub_element_value(element,"imageScreenshoot")
		gameGenRule.image_logo = self.__get_sub_element_value(element,"imageLogo")
		gameGenRule.textColor = self.__get_sub_element_value(element,"textColor")
		gameGenRule.preserveFavorite = self.__get_sub_element_value(element,"preserveFavorite")
		gameGenRule.gamelistInfoFile = self.__get_sub_element_value(element,"gamelistInfoFile")
		
		#Lecture des noeuds exceptions/exception
		exclusion_files = []
		try:
			nodeExclusions = element.getElementsByTagName("exclusions")[0]
			for nodeExclusion in nodeExclusions.getElementsByTagName("exclusion"):
				exclusion_files.append(nodeExclusion.firstChild.nodeValue)
		except (AttributeError,IndexError): #si aucun noeud <exceptions> ou <exception>
			pass
		gameGenRule.exclusion_files = exclusion_files
		
		#Lecture gamelist
		if gameGenRule.gamelistInfoFile!='':
			if os.path.isfile(gameGenRule.gamelistInfoFile):
				try:
					gameGenRule.gamelistInfo.import_xml_file(gameGenRule.gamelistInfoFile,False)
					gameGenRule.gamelistLoaded=True
					for game in gameGenRule.gamelistInfo.get_games():
						#suppression des paths et extension pour simplifier recherche
						new_path = game.get_filename_rom()
						new_path = ('.').join(new_path.split('.')[:-1])
						gameGenRule.gamelistInfo.move_path_game(game,new_path)
						
					logger.info(msg_local.get(('MSG_INFO_RUL_GAMELIST_LOADED',config.language)).format(gameGenRule.name,gameGenRule.gamelistInfoFile))	
					
				except MyError:
					#cas fichier gamelist.xml mal formé, on passe au dossier de roms suivant		
					trace_message = traceback.format_exc(0).split('\n')[1]
					logger.error(msg_local.get(('MSG_ERROR_RUL_EXCEPTION',config.language)).format('load '+gameGenRule.gamelistInfoFile+' KO-1',trace_message))		
					pass
				except Exception as exception:
					#fichier inexistant, on passe au dossier de roms suivant
					trace_message = traceback.format_exc(0).split('\n')[1]
					logger.error(msg_local.get(('MSG_ERROR_RUL_EXCEPTION',config.language)).format('load '+gameGenRule.gamelistInfoFile+' KO-2',trace_message))		
					pass
		
		
		#print('EXC: '+'|'.join(map(str, gameGenRule.exclusion_files)))
		return gameGenRule

		
	def search_rule_by_name(self,search_name):
		"""search system element by path and return objet """
		return self.__search_node_by_name_eq(search_name)
	
	def get_rules(self):
		"""get alls system elements"""
		return self.__get_nodes_by_type("rule")		

	def get_plateform(self):
		target_path = ''
		for element in self._XmlDom.getElementsByTagName("options"):
			target_path=self.__get_sub_element_value(element,"path")
		return target_path

	def get_title_format(self):
		title_format = ''
		for element in self._XmlDom.getElementsByTagName("options"):
			title_format=self.__get_sub_element_value(element,"titleformat")
		if title_format == '':
			title_format="%%NAME%% (%%PLATEFORM%%)"
		return title_format
		
		
#LOAD DESTINATION (XML)---------------------------------------------------------
def get_plateform_from_xml_config(fullpathname):
	decodeXMLRules = DecodeXMLRules()
	decodeXMLRules.import_xml_file(fullpathname)
	return decodeXMLRules.get_plateform()

#LOAD FORMAT TITRE (XML)--------------------------------------------------------
def get_title_format_from_xml_config(fullpathname):
	decodeXMLRules = DecodeXMLRules()
	decodeXMLRules.import_xml_file(fullpathname)
	return decodeXMLRules.get_title_format()

#LOAD RULES (XML)---------------------------------------------------------------
def load_rules_from_xml_config(fullpathname, type_rule=TYPE_RULE_ROMCPY):
	decodeXMLRules = DecodeXMLRules()
	decodeXMLRules.import_xml_file(fullpathname)
	rules = decodeXMLRules.get_rules()
	for rule in rules:
		rule.type=type_rule
		if type_rule==TYPE_RULE_ROMCPY:
			rule.exclusion_files.append(".sh")
	return rules

#LOAD RULES (INI)---------------------------------------------------------------
def load_rules_from_ini_config(config_rules):
	"""decodage des lignes de configuration des rêgles"""
	rules=[]
	try:
		for config_rule_key in config_rules.keys():
			rule = Rule(name=config_rule_key)
			elms_rule = config_rules[config_rule_key].split(',')
			rule.exclusion_files=[]
			rule.source=elms_rule[0]
			if rule.source not in [SOURCE_ATTR_GENRE,SOURCE_ATTR_NAME,SOURCE_ATTR_DEVELOPER,SOURCE_ATTR_PUBLISHER,SOURCE_ATTR_PATH,SOURCE_ATTR_PLAYERS]:
				logger.warn(msg_local.get(('MSG_WARN_RUL_SOURCE_NOT_SUPPORTED',config.language)).format(rule.source,rule.name))
				next
			rule.type=TYPE_RULE_ROMCPY
			rule.search=elms_rule[1]
			rule.dest_path=elms_rule[2]
			if len(elms_rule)>3:
				rule.exclusion_files=elms_rule[3].split('|')
			if len(elms_rule)>4:
				rule.image_background=elms_rule[4]
			if len(elms_rule)>5:
				rule.image_screenshot=elms_rule[5]
			if len(elms_rule)>6:
				rule.image_logo=elms_rule[6]
			if len(elms_rule)>7:
				rule.textcolor=elms_rule[7]
			if len(elms_rule)>8:
				rule.preserveFavorite=elms_rule[8]
				
			if os.path.isdir(rule.dest_path):
				rules.append(rule)
			
		return rules
	except Exception as exception:
		logger.warn(msg_local.get(('MSG_ERROR_RUL_EXCEPTION',config.language)).format('load_rules_from_ini_config',type(exception).__name__))
		return []

#BASIC RULES---------------------------------------------------------------------
def generate_rules():	
	return [
	Rule(name='Flipper1',source=SOURCE_ATTR_GENRE,search='pinball',dest_path='/home/pi/happi/divers/multi/flipper'),
	Rule(name='Flipper2',source=SOURCE_ATTR_GENRE,search='flipper',dest_path='/home/pi/happi/divers/multi/flipper'),
	Rule(name='OutRun',source=SOURCE_ATTR_NAME,search='outrun',dest_path='/home/pi/happi/divers/multi/outrun')
	]


#BASIC RULES---------------------------------------------------------------------
def create_destination_rules(rules):
	"""creation du dossier dans les regles si inexistant"""
	for rule in rules:
		if not os.path.exists(rule.dest_path):
			os.makedirs(rule.dest_path)
			logger.warn(msg_local.get(('MSG_WARN_RUL_FOLDER_CREATION',config.language)).format(rule.dest_path))


#---------------------------------------------------------------------------------------------------
#---------------------------------------- MAIN -----------------------------------------------------
#---------------------------------------------------------------------------------------------------
def main():
	
	#Init Log
	logger=Logger.logr

	#Generation rules
	#rules = generate_rules()

	#Lecture Configuration INI
	#config.load_from_file()
	#rules = load_rules_from_ini_config(config.generation_rules)

	#Lecture Configuration XML
	print('load rules')
	rules = load_rules_from_xml_config('../rules.xml')
	
	print('rules')
	print rules
	
#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	main()
