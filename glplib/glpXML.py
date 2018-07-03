#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                              - GAMELISTPOWER -                               #
#                             - MODULE GAMELIST -                              #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.02 31/10/2016-02/07/2018 #
################################################################################

#IMPORT STD---------------------------------------------------------------------
import time
import os
import codecs
import traceback
import re
import io
from xml.dom import minidom
from xml.parsers import expat
from operator import attrgetter, itemgetter

#IMPORT NORDICPOWER-------------------------------------------------------------
from glpDIR import exist_game_rom,predict_encoding
from glpTOOLS import *

#CONSTANTS-----------------------------------------------------------------------
SOURCE_NAME="nordicpower.fr"

NOM_GAMELIST='gamelist'
NOM_GAMELIST_XML=NOM_GAMELIST+'.xml'

#MSG LOCALISATION---------------------------------------------------------------
config=Config()

msg_local={
('MSG_WARN_GLX_EMPTYFILE','FR'):u'Fichier vide : {}',
('MSG_WARN_GLX_EMPTYFILE','EN'):u'Empty file {}',
('MSG_ERROR_GLX_EXCEPTION','FR'):u'{} : {}',
('MSG_ERROR_GLX_EXCEPTION','EN'):u'{} : {}',
('MSG_ERROR_GLX_EXCEPTION_FILE','FR'):u'{} : {} avec le fichier {}',
('MSG_ERROR_GLX_EXCEPTION_FILE','EN'):u'{} : {} with this file {}',
('MSG_DEBUG_GLX_MOVEROM','FR'):u'Modification path ancien={}, nouveau={}',
('MSG_DEBUG_GLX_MOVEROM','EN'):u'Move path old={}, new={}',
('MSG_DEBUG_GLX_UPD_DATE','FR'):u'UpdateDate xml={}, quick={}, refresh={}',
('MSG_DEBUG_GLX_UPD_DATE','EN'):u'UpdateDate xml={}, quick={}, refresh={}',
('MSG_ERROR_XML_LOC','FR'):u'Fichier {} mal form\u00E9 \u00E0 la ligne {} position {}',
('MSG_ERROR_XML_LOC','EN'):u'File {} is not well formed at line {} pos {}',
('MSG_INFO_XML_ADVISE1','FR'):u'Conseil : remplacer {} par {}',
('MSG_INFO_XML_ADVISE1','EN'):u'Advise : replace {} by {}',
('MSG_INFO_XML_ADVISE2','FR'):u'Conseil : v\u00E9rifier la ligne ou les pr\u00E9c\u00E9dents avec les ouvertures (<) ou fermetures de tag (>)',
('MSG_INFO_XML_ADVISE2','EN'):u'Advise : check line or before this line on opening or closing tag',
('MSG_INFO_XML_LINE_SOURCE','FR'):u'Ligne en erreur : {}',
('MSG_INFO_XML_LINE_SOURCE','EN'):u'Error at line {}'
}

#INIT SINGLETON-------------------------------------------------------------------
logger=Logger.logr

#CLASS-GAME----------------------------------------------------------------------
def key_top_game(game):
	"""fonction de tri pour get_top_games"""
	if game.playcount.isdigit():return int(game.playcount)
	return game.playcount


class Game:
	"""POJO Game Class from Class Element of gamelist.xml
		https://github.com/Aloshi/EmulationStation/blob/unstable/GAMELISTS.md"""
	def __init__(self,**kwargs):
		self._path=''
		self._name=''
		self._desc=''
		self._image=''
		self._rating=''
		self._releasedate=''
		self._developer=''
		self._publisher=''
		self._genre=''
		self._players=''
		self._ref_id=''
		self._source=''
		self._playcount=''
		self._lastplayed=''
		self._specific=''
		self._hidden=''
		self._internal_glp_id=''
		self._background=""	#Happigc
		self._screenshot=""	#Happigc
		self._logo=""
		self._textcolor=""	#Happigc
		self._favorite=""
		self._region=""			
		self._thumbnail=''  #Recalbox
		self._emulator="" 	#RecalBox
		self._core="" 			#RecalBox
		self._ratio="" 			#RecalBox
		self._romtype=""    #RecalBox
		
		if kwargs is not None:
			#mise à jour paramètre(s) nommé(s)
			self.__dict__.update(kwargs)

	def __repr__(self):
        	return repr((self.name, self.path, self.image,self.playcount, self.lastplayed))

	def __eq__(self, other):
		""" egalité si le nom des roms sont identiques"""
	        return (self.get_filename_rom() == other.get_filename_rom())

	def __ne__(self, other):
		return not self.__eq__(other)

	#property-------------------------	
	@property
	def path(self):return self._path
	@property
	def name(self):return self._name
	@property
	def desc(self):return self._desc
	@property
	def image(self):return self._image
	@property
	def rating(self):return self._rating
	@property
	def releasedate(self):return self._releasedate
	@property
	def developer(self):return self._developer
	@property
	def publisher(self):return self._publisher
	@property
	def genre(self):return self._genre
	@property
	def players(self):return self._players
	@property
	def ref_id(self):return self._ref_id
	@property
	def source(self):return self._source
	@property
	def playcount(self):return self._playcount
	@property
	def lastplayed(self):return self._lastplayed
	@property
	def specific(self):return self._specific
	@property
	def hidden(self):return self._hidden
	@property
	def internal_glp_id(self):return self._internal_glp_id
	@property
	def background(self):return self._background
	@property
	def screenshot(self):return self._screenshot
	@property
	def logo(self):return self._logo
	@property
	def textcolor(self):return self._textcolor
	@property
	def favorite(self):return self._favorite
	@property
	def region(self):return self._region
	@property
	def emulator(self):return self._emulator
	@property
	def core(self):return self._core
	@property
	def ratio(self):return self._ratio
	@property
	def thumbnail(self):return self._thumbnail
	@property
	def romtype(self):return self._romtype
		
	#setter-------------------------	
	@path.setter
	def path(self,v):self._path=v
	@name.setter
	def name(self,v):self._name=v
	@desc.setter
	def desc(self,v):self._desc=v
	@image.setter
	def image(self,v):self._image=v
	@rating.setter
	def rating(self,v):self._rating=v
	@releasedate.setter
	def releasedate(self,v):self._releasedate=v
	@developer.setter
	def developer(self,v):self._developer=v
	@publisher.setter
	def publisher(self,v):self._publisher=v
	@genre.setter
	def genre(self,v):self._genre=v
	@publisher.setter
	def players(self,v):self._players=v
	@ref_id.setter
	def ref_id(self,v):self._ref_id=v
	@source.setter
	def source(self,v):self._source=v
	@playcount.setter
	def playcount(self,v):self._playcount=v
	@lastplayed.setter
	def lastplayed(self,v):self._lastplayed=v
	@specific.setter
	def specific(self,v):self._specific=v
	@hidden.setter
	def hidden(self,v):self._hidden=v
	@internal_glp_id.setter
	def internal_glp_id(self,v):self._internal_glp_id=v
	@background.setter
	def background(self,v):self._background=v
	@screenshot.setter
	def screenshot(self,v):self._screenshot=v
	@logo.setter
	def logo(self,v):self._logo=v
	@textcolor.setter
	def textcolor(self,v):self._textcolor=v
	@favorite.setter
	def favorite(self,v):self._favorite=v
	@region.setter
	def region(self,v):self._region=v
	@emulator.setter
	def emulator(self,v):self._emulator=v
	@core.setter
	def core(self,v):self._core=v
	@ratio.setter
	def ratio(self,v):self._ratio=v
	@thumbnail.setter
	def thumbnail(self,v):self._thumbnail=v
	@romtype.setter
	def romtype(self,v):self._romtype=v
		
	def get_filename_rom(self):
		"""Extraction du nom de fichiers dans un path"""
		return self.path.replace('\\','/').split('/')[-1]
		
		
	def copy_from_game(self,game_src,preserve_play_values=False):
		"""Copie tous les attributs en dehors du path d'un objet game à un autre"""		
		self.name = game_src.name
		self.desc = game_src.desc
		self.image = game_src.image
		self.rating = game_src.rating
		self.releasedate = game_src.releasedate
		self.developer = game_src.developer
		self.publisher = game_src.publisher
		self.genre = game_src.genre
		self.players = game_src.players
		self.ref_id = game_src.ref_id
		self.source = game_src.source
		if not preserve_play_values:
			self.playcount = game_src.playcount
			self.lastplayed = game_src.lastplayed
		self.specific = game_src.specific
		self.hidden = game_src.hidden
		self.background = game_src.background
		self.screenshot = game_src.screenshot
		self.logo = game_src.logo
		self.textcolor = game_src.textcolor
		self.favorite = game_src.favorite
		self.region = game_src.region
		self.emulator = game_src.emulator
		self.core = game_src.core
		self.ratio = game_src.ratio
		self.thumbnail = game_src.thumbnail
		self.romtype = game_src.romtype
		
		#Id interne non transmis
		self.internal_glp_id = time.strftime('%Y%m%dT%H%M%S',time.localtime())
		
		
#CLASS-FOLDER-------------------------------------------------------------------------
class Folder:
	"""POJO Folder Class from Class Element of gamelist.xml
		https://github.com/Aloshi/EmulationStation/blob/unstable/GAMELISTS.md"""
	def __init__(self,**kwargs):
		self._path=''
		self._name=''
		self._desc=''
		self._image=''
		self._hidden=''
		#self._ref_id=''
		#self._source=''
		self._background=""
		self._screenshot=""
		self._logo=""
		self._textcolor=""
		
		if kwargs is not None:
			#mise à jour paramètre(s) nommé(s)
			self.__dict__.update(kwargs)

	def __repr__(self):
        	return repr((self.name, self.path, self.image))
	
	#property-------------------------	
	@property
	def path(self):return self._path
	@property
	def name(self):return self._name
	@property
	def desc(self):return self._desc
	@property
	def image(self):return self._image
	#@property
	#def ref_id(self):return self._ref_id
	#@property
	#def source(self):return self._source
	@property
	def hidden(self):return self._hidden
	@property
	def background(self):return self._background
	@property
	def screenshot(self):return self._screenshot
	@property
	def logo(self):return self._logo
	@property
	def textcolor(self):return self._textcolor
	
	#setter-------------------------	
	@path.setter
	def path(self,v):self._path=v
	@name.setter
	def name(self,v):self._name=v
	@desc.setter
	def desc(self,v):self._desc=v
	@image.setter
	def image(self,v):self._image=v
	#@ref_id.setter
	#def ref_id(self,v):self._ref_id=v
	#@source.setter
	#def source(self,v):self._source=v
	@hidden.setter
	def hidden(self,v):self._hidden=v
	@background.setter
	def background(self,v):self._background=v
	@screenshot.setter
	def screenshot(self,v):self._screenshot=v
	@logo.setter
	def logo(self,v):self._logo=v
	@textcolor.setter
	def textcolor(self,v):self._textcolor=v
		
	def get_filename_folder(self):
		"""Extraction du nom de dossier dans un path"""
		return self.path.replace('\\','/').split('/')[-1]
		
#CLASS-GAMESLIST-------------------------------------------------------------------------
class GamesList:
	"""Class Gameslist of gamelist.xml"""
	_gameListXmlDom = minidom.getDOMImplementation()
	_CLASS_GAME_NODENAME="game"
	_CLASS_FOLDER_NODENAME="folder"
	_CLASS_GAMELIST_NODENAME="gameList"
	_last_updated_date=""
	_last_quickupdated_date=""
	_empty_file_at_load=False
	_refresh_folders="no"
	
	#property----------------------------------------------------------------	
	@property
	def modified(self):return self._last_updated_date!=''
	@property
	def last_updated_date(self):return self._last_updated_date
	@property
	def last_quickupdated_date(self):return self._last_quickupdated_date
	@property
	def empty_file_at_load(self):return self._empty_file_at_load
	@property
	def refresh_folders(self):return self._refresh_folders
		
		
	def refresh_folders_finished(self):
		"""Positionne l'attribut refresh à no et enregistre info xml"""
		self._refresh_folders="no"
		self.__tag_update()
	
	#file operations----------------------------------------------------------------	
	def create_root_xml(self):
		self._gameListXmlDom = minidom.parseString('<?xml version="1.0" ?><gameList></gameList>')
		self._empty_file_at_load = True
			
	def import_xml_file(self,fullpathname,bStopIfGeneralError=True):
		try:
			self._gameListXmlDom = minidom.parse(fullpathname)
			self.__load_update_dates()
			self.__set_game_internal_glp_id()
			
		except (expat.ExpatError):
			if os.path.getsize(fullpathname)==0:
				logger.warn(msg_local.get(('MSG_WARN_GLX_EMPTYFILE',config.language)).format(fullpathname))
				self.create_root_xml()
			elif predict_encoding(fullpathname)=='Windows-1252':
				with io.open(fullpathname, "r", encoding="cp1252") as my_file:
					xmltext = my_file.read()
					self._gameListXmlDom = minidom.parseString(xmltext.encode("utf-8"))
			else:
				#Gestion des erreurs sur le format XML (>0.6.04)
				trace_message = traceback.format_exc(0).split('\n')[1]
				if 'not well-formed (invalid token)' in trace_message:
					#Erreur entity xml
					trace_data = re.findall(r'\d+', trace_message)
					logger.error(msg_local.get(('MSG_ERROR_XML_LOC',config.language)).format(fullpathname,trace_data[0],trace_data[1]))
					line_xml_error=open(fullpathname).readlines()[int(trace_data[0])-1]
					pos_xml_error=line_xml_error[int(trace_data[1])-1]
					if pos_xml_error=='&':		
						logger.info(msg_local.get(('MSG_INFO_XML_ADVISE1',config.language)).format('&','&amp;'))
					elif pos_xml_error=='<':
						logger.info(msg_local.get(('MSG_INFO_XML_ADVISE1',config.language)).format('<','&lt;'))
					elif pos_xml_error=='>':
						logger.info(msg_local.get(('MSG_INFO_XML_ADVISE1',config.language)).format('>','&gt;'))
					logger.info(msg_local.get(('MSG_INFO_XML_LINE_SOURCE',config.language)).format(line_xml_error))
				elif 'mismatched tag' in trace_message:
					#Erreur de balise 
					trace_data = re.findall(r'\d+', trace_message)
					logger.error(msg_local.get(('MSG_ERROR_XML_LOC',config.language)).format(fullpathname,trace_data[0],trace_data[1]))
					line_xml_error=open(fullpathname).readlines()[int(trace_data[0])-1]
					logger.info(msg_local.get(('MSG_INFO_XML_ADVISE2',config.language)).format(''))
					logger.info(msg_local.get(('MSG_INFO_XML_LINE_SOURCE',config.language)).format(line_xml_error))
				else:
					logger.error(msg_local.get(('MSG_ERROR_GLX_EXCEPTION_FILE',config.language)).format('GamesList.import_xml_file',trace_message,fullpathname))
					
				raise MyError('xml malformed')
				
		except Exception as exception:
			logger.critical(msg_local.get(('MSG_ERROR_GLX_EXCEPTION_FILE',config.language)).format('GamesList.import_xml_file',type(exception).__name__,fullpathname))
			if bStopIfGeneralError:
				sys.exit(1)
	
	def save_xml_file(self,fullpathname,cleaning=True):
		
		self.__unset_game_internal_glp_id()
		
		if cleaning:
			uglyXml = self._gameListXmlDom.toprettyxml()
			#Cleaning maison très bourrin !!
			prettyXml=''
			x = uglyXml.split('\n')
			for xx in x:
				t = xx.strip()
				if len(t) >0:
					prettyXml = prettyXml + t + '\n'
			#Identation a la mano
			prettyXml = prettyXml.replace('<game','  <game')
			prettyXml = prettyXml.replace('  <gameList>','<gameList>') #Patch 0.5.06
			prettyXml = prettyXml.replace('</game>','  </game>')
			prettyXml = prettyXml.replace('<folder','  <folder')
			prettyXml = prettyXml.replace('</folder>','  </folder>')
			prettyXml = prettyXml.replace('<name>','    <name>')
			prettyXml = prettyXml.replace('<desc>','    <desc>')
			prettyXml = prettyXml.replace('<desc/>','    <desc/>')
			prettyXml = prettyXml.replace('<path>','    <path>')
			prettyXml = prettyXml.replace('<image>','    <image>')
			prettyXml = prettyXml.replace('<rating>','    <rating>')
			prettyXml = prettyXml.replace('<rating/>','    <rating/>')
			prettyXml = prettyXml.replace('<releasedate>','    <releasedate>')
			prettyXml = prettyXml.replace('<releasedate/>','    <releasedate/>')
			prettyXml = prettyXml.replace('<developer>','    <developer>')
			prettyXml = prettyXml.replace('<developer/>','    <developer/>')
			prettyXml = prettyXml.replace('<publisher>','    <publisher>')
			prettyXml = prettyXml.replace('<publisher/>','    <publisher/>')
			prettyXml = prettyXml.replace('<genre>','    <genre>')
			prettyXml = prettyXml.replace('<genre/>','    <genre/>')
			prettyXml = prettyXml.replace('<players>','    <players>')
			prettyXml = prettyXml.replace('<players/>','    <players/>')
			prettyXml = prettyXml.replace('<playcount>','    <playcount>')
			prettyXml = prettyXml.replace('<playcount/>','    <playcount/>')
			prettyXml = prettyXml.replace('<lastplayed>','    <lastplayed>')
			prettyXml = prettyXml.replace('<lastplayed/>','    <lastplayed/>')
			prettyXml = prettyXml.replace('<hidden>','    <hidden>')
			prettyXml = prettyXml.replace('<hidden/>','    <hidden/>')
			prettyXml = prettyXml.replace('<background>','    <background>')
			prettyXml = prettyXml.replace('<background/>','    <background/>')
			prettyXml = prettyXml.replace('<screenshot>','    <screenshot>')
			prettyXml = prettyXml.replace('<screenshot/>','    <screenshot/>')
			prettyXml = prettyXml.replace('<logo>','    <logo>')
			prettyXml = prettyXml.replace('<logo/>','    <logo/>')
			prettyXml = prettyXml.replace('<textcolor>','    <textcolor>')
			prettyXml = prettyXml.replace('<textcolor/>','    <textcolor/>')
			prettyXml = prettyXml.replace('<favorite>','    <favorite>')
			prettyXml = prettyXml.replace('<favorite/>','    <favorite/>')
			prettyXml = prettyXml.replace('<region>','    <region>')
			prettyXml = prettyXml.replace('<region/>','    <region/>')
			prettyXml = prettyXml.replace('<emulator>','    <emulator>')
			prettyXml = prettyXml.replace('<emulator/>','    <emulator/>')
			prettyXml = prettyXml.replace('<emulators>','    <emulators>')
			prettyXml = prettyXml.replace('<emulators/>','    <emulators/>')
			prettyXml = prettyXml.replace('<cores>','    <cores>')
			prettyXml = prettyXml.replace('<cores/>','    <cores/>')
			prettyXml = prettyXml.replace('<core>','    <core>')
			prettyXml = prettyXml.replace('<core/>','    <core/>')
			prettyXml = prettyXml.replace('<ratio>','    <ratio>')
			prettyXml = prettyXml.replace('<ratio/>','    <ratio/>')
			prettyXml = prettyXml.replace('<thumbnail/>','    <thumbnail/>')
			prettyXml = prettyXml.replace('<thumbnail/>','    <thumbnail/>')
			prettyXml = prettyXml.replace('<romtype/>','    <romtype/>')
			prettyXml = prettyXml.replace('<romtype/>','    <romtype/>')
			
			#Ecriture sur disque
			f = open(fullpathname,'w')
			f.write(prettyXml.encode("UTF-8"))
			f.close()
			
		else:
			#Ecriture sur disque
			f = open(fullpathname,'w')
			#f.write(self._gameListXmlDom.toxml().encode("UTF-8"))
			f = codecs.lookup("utf-8")[3](f)
			self._gameListXmlDom.writexml(f, encoding="utf-8")
			f.close()
	
	#debug----------------------------------------------------------------	
	def to_xml(self):
		return self._gameListXmlDom.toxml() 

	#private functions----------------------------------------------------------------	
	def __tag_update(self,quick=False):
		"""set modified and update date, quick reserved for quickupdate"""
		self._modified=True
		self._last_updated_date=time.strftime('%Y%m%dT%H%M%S',time.localtime())
		gamelist_element = self._gameListXmlDom.getElementsByTagName(self._CLASS_GAMELIST_NODENAME)
		gamelist_element[0].setAttribute("last_update_date",self._last_updated_date)
		if quick:
			self._refresh_folders="yes"
			self._last_quickupdated_date = self._last_updated_date
			gamelist_element[0].setAttribute("last_quickupdate_date",self._last_quickupdated_date)
		gamelist_element[0].setAttribute("refresh",self._refresh_folders)
		gamelist_element[0].setAttribute("source",SOURCE_NAME)
	
	
	def __load_update_dates(self):
		""" retrieve date from gamelist node"""
		gamelist_element = self._gameListXmlDom.getElementsByTagName(self._CLASS_GAMELIST_NODENAME)
		self._last_updated_date = gamelist_element[0].getAttribute("last_update_date")
		self._last_quickupdate_date = gamelist_element[0].getAttribute("last_quickupdate_date")
		self._refresh_folders = gamelist_element[0].getAttribute("refresh")
		logger.debug(msg_local.get(('MSG_DEBUG_GLX_UPD_DATE',config.language)).format(self._last_updated_date,self._last_quickupdate_date,self._refresh_folders))
		
	def __get_sub_element_value(self,nodegame,elementname):
		"""read value of element return empty if not exist"""
		try:
			return nodegame.getElementsByTagName(elementname)[0].firstChild.nodeValue
		except (AttributeError,IndexError):
			pass
		except Exception as exception:
			#logger.warn('__get_sub_element_value :' +type(exception).__name__)
			logger.warn(msg_local.get(('MSG_ERROR_GLX_EXCEPTION',config.language)).format('GamesList.__get_sub_element_value',type(exception).__name__))
		return ''
	
	def __set_sub_element_value(self,nodegame,elementname,value):
		"""write value of element"""
		try:
			if value=='':
				nodegame.removeChild(nodegame.getElementsByTagName(elementname)[0])
				
			else:
				nodegame.getElementsByTagName(elementname)[0].firstChild.nodeValue=value

		except (AttributeError,IndexError):
			if value !='':
					self.__add_subelement_node(nodegame,elementname,value)
		except Exception as exception:
			#logger.warn('__get_sub_element_value :' +type(exception).__name__)
			logger.warn(msg_local.get(('MSG_ERROR_GLX_EXCEPTION',config.language)).format('GamesList.__set_sub_element_value',type(exception).__name__))
		return ''

	
	def __add_subelement_node(self,node,subnodename,subnodevalue):
		"""add subelement on a node"""
		new_dom_node_subelement = self._gameListXmlDom.createElement(subnodename)
		new_dom_node_subelement_text = self._gameListXmlDom.createTextNode( subnodevalue )
		new_dom_node_subelement.appendChild(new_dom_node_subelement_text)
		node.appendChild(new_dom_node_subelement)


	def __search_node_by_path(self,node_type,search_path):
		"""search node element by path and return objet """
		tag_path = self._gameListXmlDom.getElementsByTagName("path")
		for element in tag_path:
			if element.firstChild.nodeValue == search_path:
				if element.parentNode.nodeName == node_type:
					if element.parentNode.nodeName == self._CLASS_GAME_NODENAME:
						return self.__get_game_from_element(element.parentNode)
					elif element.parentNode.nodeName == self._CLASS_FOLDER_NODENAME:
						return self.__get_folder_from_element(element.parentNode)
					else:
						raise MyError('Unknow node')
				else:
					raise MyError('Not Found1')
		raise MyError('Not Found2')


	def __search_nodes_by_attr(self,node_type,search_attr,search_value):
		"""search nodes element by a value in specific attribut """
		nodes_found =[]
		
		tag_elm = self._gameListXmlDom.getElementsByTagName(search_attr)
		for element in tag_elm:
			try:
				tag_value = element.firstChild.nodeValue
			except:
				#cas des tags vide
				tag_value = ''
			
			#0.7.5 Recherche non sensitive
			if search_value.lower() in tag_value.lower() and tag_value != '':
				if element.parentNode.nodeName == node_type:
					if element.parentNode.nodeName == self._CLASS_GAME_NODENAME:
						nodes_found.append(self.__get_game_from_element(element.parentNode))
					elif element.parentNode.nodeName == self._CLASS_FOLDER_NODENAME:
						nodes_found.append(self.__get_folder_from_element(element.parentNode))
					else:
						raise MyError('Unknow node')
		return nodes_found
		
		
	def __get_nodes_by_type(self,node_type):
		"""search node elements by their node_type return list objet """
		list_element = []
		tag_path = self._gameListXmlDom.getElementsByTagName(node_type)
		for element in tag_path:
			list_element.append(self.__get_game_from_element(element))
		return list_element


	def __set_game_internal_glp_id(self):
		"""tag game node element by internal id """
		tag_game = self._gameListXmlDom.getElementsByTagName(self._CLASS_GAME_NODENAME)
		glp_id_counter=0
		for element in tag_game:
			element.setAttribute("internal_glp_id",time.strftime('%Y%m%dT%H%M%S',time.localtime())+'#'+str(glp_id_counter))
			glp_id_counter=glp_id_counter+1
	
	def __unset_game_internal_glp_id(self):
		"""remove internal id"""
		tag_game = self._gameListXmlDom.getElementsByTagName(self._CLASS_GAME_NODENAME)
		for element in tag_game:
			try:
				element.removeAttribute("internal_glp_id")
			except:
				#noting
				pass
				
	#quick update functions----------------------------------------------------------------	
	def quick_update_game_now_played(self,search_path):
		for element in self._gameListXmlDom.getElementsByTagName("path"):
			if search_path in element.firstChild.nodeValue and element.parentNode.nodeName == self._CLASS_GAME_NODENAME:
				playcount = self.__get_sub_element_value(element.parentNode,"playcount")
				if not playcount.isdigit():
					playcount=1
				else:
					playcount=int(playcount)+1

				self.__set_sub_element_value(element.parentNode,"playcount",str(playcount))
				self.__set_sub_element_value(element.parentNode,"lastplayed",time.strftime('%Y%m%dT%H%M%S',time.localtime()))
				#Update with quickupdate attribute
				self.__tag_update(True)

				
	#game functions----------------------------------------------------------------	
	def __get_game_from_element(self,element):
		"""convert dom element to pojo game"""
		game = Game()
		##Lecture des attributs du noeud game
		game.ref_id=element.getAttribute("id")
		game.source=element.getAttribute("source")
		game.specific=element.getAttribute("specific")
		game.internal_glp_id = element.getAttribute("internal_glp_id")
		##Lecture des noeuds fils
		game.path = self.__get_sub_element_value(element,"path")
		game.name = self.__get_sub_element_value(element,"name")
		game.desc = self.__get_sub_element_value(element,"desc")
		game.image = self.__get_sub_element_value(element,"image")
		game.rating = self.__get_sub_element_value(element,"rating")
		game.releasedate = self.__get_sub_element_value(element,"releasedate")
		game.developer = self.__get_sub_element_value(element,"developer")
		game.publisher = self.__get_sub_element_value(element,"publisher")
		game.genre = self.__get_sub_element_value(element,"genre")
		game.players = self.__get_sub_element_value(element,"players")
		game.playcount = self.__get_sub_element_value(element,"playcount")
		game.lastplayed = self.__get_sub_element_value(element,"lastplayed")
		game.hidden = self.__get_sub_element_value(element,"hidden")
		game.background = self.__get_sub_element_value(element,"background")
		game.screenshot = self.__get_sub_element_value(element,"screenshot")
		game.logo = self.__get_sub_element_value(element,"logo")
		game.textcolor = self.__get_sub_element_value(element,"textcolor")
		game.favorite = self.__get_sub_element_value(element,"favorite")
		game.region = self.__get_sub_element_value(element,"region")
		game.emulator = self.__get_sub_element_value(element,"emulator")
		game.core = self.__get_sub_element_value(element,"core")
		game.ratio = self.__get_sub_element_value(element,"ratio")
		game.thumbnail = self.__get_sub_element_value(element,"thumbnail")
		game.romtype = self.__get_sub_element_value(element,"romtype")
		return game

	
	def search_game_by_path(self,search_path):
		"""search game element by path and return objet """
		try:
			return self.__search_node_by_path(self._CLASS_GAME_NODENAME,search_path)
		except:
			#Cas de Windows sur des fichiers GAMELIST unix (test only)
			return self.__search_node_by_path(self._CLASS_GAME_NODENAME,search_path.replace(os.sep,'/'))


	def search_games(self,search_attr,search_value):
		"""return games which matches critera"""
		return self.__search_nodes_by_attr(self._CLASS_GAME_NODENAME,search_attr,search_value)
		
			
	def get_games(self):
		"""get alls game elements"""
		return self.__get_nodes_by_type(self._CLASS_GAME_NODENAME)


	def get_games_without_roms(self,GameListDirectory):
		"""get alls game elements without rom file"""
		games_XML_not_found = []
		for game_XML in self.__get_nodes_by_type(self._CLASS_GAME_NODENAME):
			if not exist_game_rom(GameListDirectory,game_XML.path):
				games_XML_not_found.append(game_XML)
		return games_XML_not_found
	

	def get_top_games(self,nb_top,exclude_folders):
		"""get top n games"""
		games_XML = [gl for gl in self.get_games() if exclude_folders[0] not in gl.path and exclude_folders[1] not in gl.path and exclude_folders[2] not in gl.path and exclude_folders[3] not in gl.path and gl.playcount<>'']
		if len(games_XML) < int(nb_top) : nb_top = len(games_XML)
		##utilisation fct de tri pour gérer numérique sur playcount
		##return sorted(games_XML,key=attrgetter('playcount','lastplayed','name'),reverse=True)[0:nb_top-1]
		return sorted(games_XML,key=key_top_game,reverse=True)[0:int(nb_top)]

		
	def get_last_games(self,nb_last,exclude_folders):
		"""get last n games"""
		games_XML = [gl for gl in self.get_games() if exclude_folders[0] not in gl.path and exclude_folders[1] not in gl.path and exclude_folders[2] not in gl.path and exclude_folders[3] not in gl.path and gl.lastplayed<>'']
		if len(games_XML) < int(nb_last) : nb_last = len(games_XML)
		return sorted(games_XML,key=attrgetter('lastplayed','playcount','name'),reverse=True)[0:int(nb_last)]


	def get_games_in_folder(self,folder):
		"""get games which rom stored in given folder"""
		return [gl for gl in self.get_games() if folder in gl.path]


	def get_games_in_folder_sorted_by_name(self,folder):
		"""get games which rom stored in given folder sorted by name"""
		games_XML = self.get_games_in_folder(folder)
		return sorted(games_XML,key=attrgetter('name','playcount','lastplayed'),reverse=True)


	def add_game(self,newgame):
		"""add a game in dom"""
		gamelist_element = self._gameListXmlDom.getElementsByTagName(self._CLASS_GAMELIST_NODENAME)
		newdom_game_element = self._gameListXmlDom.createElement(self._CLASS_GAME_NODENAME)
		#Attributs
		newdom_game_element.setAttribute("id",newgame.ref_id)
		if newgame.source=='':newgame.source=SOURCE_NAME
		newdom_game_element.setAttribute("source",newgame.source)
		if newgame.specific != '':
			newdom_game_element.setAttribute("specific",newgame.specific)
		
		newdom_game_element.setAttribute("internal_glp_id",time.strftime('%Y%m%dT%H%M%S',time.localtime()))
		#SubElements	
		self.__add_subelement_node(newdom_game_element,"path",newgame.path)
		if newgame.name!='':
			self.__add_subelement_node(newdom_game_element,"name",newgame.name)
		if newgame.desc!='':
			self.__add_subelement_node(newdom_game_element,"desc",newgame.desc)
		if newgame.image!='':
			self.__add_subelement_node(newdom_game_element,"image",newgame.image)
		if newgame.rating!='':
			self.__add_subelement_node(newdom_game_element,"rating",newgame.rating)
		if newgame.releasedate!='':
			self.__add_subelement_node(newdom_game_element,"releasedate",newgame.releasedate)
		if newgame.developer!='':
			self.__add_subelement_node(newdom_game_element,"developer",newgame.developer)
		if newgame.publisher!='':
			self.__add_subelement_node(newdom_game_element,"publisher",newgame.publisher)
		if newgame.genre!='':
			self.__add_subelement_node(newdom_game_element,"genre",newgame.genre)
		if newgame.players!='':
			self.__add_subelement_node(newdom_game_element,"players",str(newgame.players))
		if newgame.playcount!='':
			self.__add_subelement_node(newdom_game_element,"playcount",str(newgame.playcount))
		if newgame.lastplayed!='':
			self.__add_subelement_node(newdom_game_element,"lastplayed",newgame.lastplayed)
		if newgame.hidden!='':
			self.__add_subelement_node(newdom_game_element,"hidden",newgame.lastplayed)
		if newgame.background!='':
			self.__add_subelement_node(newdom_game_element,"background",newgame.background)
		if newgame.screenshot!='':
			self.__add_subelement_node(newdom_game_element,"screenshot",newgame.screenshot)
		if newgame.logo!='':
			self.__add_subelement_node(newdom_game_element,"logo",newgame.logo)
		if newgame.textcolor!='':
			self.__add_subelement_node(newdom_game_element,"textcolor",newgame.textcolor)
		if newgame.favorite!='':
			self.__add_subelement_node(newdom_game_element,"favorite",newgame.favorite)
		if newgame.region!='':
			self.__add_subelement_node(newdom_game_element,"region",newgame.region)
		if newgame.emulator!='':
			self.__add_subelement_node(newdom_game_element,"emulator",newgame.emulator)
		if newgame.core!='':
			self.__add_subelement_node(newdom_game_element,"core",newgame.core)
		if newgame.ratio!='':
			self.__add_subelement_node(newdom_game_element,"ratio",newgame.ratio)
		if newgame.thumbnail!='':
			self.__add_subelement_node(newdom_game_element,"thumbnail",newgame.thumbnail)
		if newgame.romtype!='':
			self.__add_subelement_node(newdom_game_element,"romtype",newgame.romtype)
		gamelist_element[0].appendChild(newdom_game_element)
		self.__tag_update()

			
	def update_game(self,updgame):
		"""update existing game node in dom"""
		tagpath = self._gameListXmlDom.getElementsByTagName("path")
		for element in tagpath:
			if element.firstChild.nodeValue == updgame.path:
				game_node = element.parentNode
				#Attributs
				game_node.setAttribute("id",updgame.ref_id)
				if updgame.source=='':updgame.source=SOURCE_NAME
				game_node.setAttribute("source",updgame.source)
				if updgame.specific =='':
					if game_node.getAttribute("specific")!='':
						game_node.removeAttribute("specific")
				else:
					game_node.setAttribute("specific",updgame.specific)
				if updgame.internal_glp_id =='':
					if game_node.getAttribute("internal_glp_id")!='':
						game_node.removeAttribute("internal_glp_id")
				else:
					game_node.setAttribute("internal_glp_id",updgame.internal_glp_id)
				#SubElements	
				self.__set_sub_element_value(game_node,"path",updgame.path)
				self.__set_sub_element_value(game_node,"name",updgame.name)
				self.__set_sub_element_value(game_node,"desc",updgame.desc)
				self.__set_sub_element_value(game_node,"image",updgame.image)
				self.__set_sub_element_value(game_node,"rating",updgame.rating)
				self.__set_sub_element_value(game_node,"releasedate",updgame.releasedate)
				self.__set_sub_element_value(game_node,"developer",updgame.developer)
				self.__set_sub_element_value(game_node,"publisher",updgame.publisher)
				self.__set_sub_element_value(game_node,"genre",updgame.genre)
				self.__set_sub_element_value(game_node,"players",updgame.players)
				self.__set_sub_element_value(game_node,"playcount",updgame.playcount)
				self.__set_sub_element_value(game_node,"lastplayed",updgame.lastplayed)
				self.__set_sub_element_value(game_node,"hidden",updgame.hidden)
				self.__set_sub_element_value(game_node,"background",updgame.background)
				self.__set_sub_element_value(game_node,"screenshot",updgame.screenshot)
				self.__set_sub_element_value(game_node,"logo",updgame.logo)
				self.__set_sub_element_value(game_node,"textcolor",updgame.textcolor)
				self.__set_sub_element_value(game_node,"favorite",updgame.favorite)
				self.__set_sub_element_value(game_node,"region",updgame.region)
				self.__set_sub_element_value(game_node,"emulator",updgame.emulator)
				self.__set_sub_element_value(game_node,"core",updgame.core)
				self.__set_sub_element_value(game_node,"ratio",updgame.ratio)
				self.__set_sub_element_value(game_node,"thumbnail",updgame.thumbnail)
				self.__set_sub_element_value(game_node,"romtype",updgame.romtype)
				self.__tag_update()

	
	def move_path_game(self,updgame,new_path):
		"""change path by another"""
		if new_path !=updgame.path:
			
			tagpath = self._gameListXmlDom.getElementsByTagName("path")
			for element in tagpath:
				if element.firstChild.nodeValue == updgame.path:
					game_node = element.parentNode
					game_node.setAttribute("id",updgame.ref_id)
					if updgame.source=='':updgame.source=SOURCE_NAME
					game_node.setAttribute("source",updgame.source)
					self.__set_sub_element_value(game_node,"path",new_path)
					self.__tag_update()
					#logger.debug('Move path old='+updgame.path + ', new='+new_path)
					logger.debug(msg_local.get(('MSG_DEBUG_GLX_MOVEROM',config.language)).format(updgame.path,new_path))
	
	def delete_game(self,delgame):
		"""delete existing folder in dom"""
		tag_path = self._gameListXmlDom.getElementsByTagName("path")
		for element in tag_path:
			if element.firstChild.nodeValue == delgame.path:
				gamelist_element = self._gameListXmlDom.getElementsByTagName(self._CLASS_GAMELIST_NODENAME)
				if element.parentNode.nodeName == self._CLASS_GAME_NODENAME:
					gamelist_element[0].removeChild(element.parentNode)
					self.__tag_update()

	def delete_game_with_glp_id(self,internal_glp_id):
		"""delete existing folder in dom with specific internal id """
		tag_game = self._gameListXmlDom.getElementsByTagName(self._CLASS_GAME_NODENAME)
		for element in tag_game:
			if element.getAttribute("internal_glp_id") == internal_glp_id:
				gamelist_element = self._gameListXmlDom.getElementsByTagName(self._CLASS_GAMELIST_NODENAME)
				gamelist_element[0].removeChild(element)
				self.__tag_update()	


	def top_name(self,pos,name):
		#Nom TOP dans le fichier gamelist.xml
		return "{}. {}".format(pos,name)
		
	def top_name_console(self,pos,name,nb):
		#Nom TOP à l'affichage
		return "{}. ({:>2}) {}".format(pos,nb,name)
		
	def last_name(self,pos,name):
		#Nom LAST dans le fichier gamelist.xml
		return "{}. {}".format(pos,name)

	def last_name_console(self,pos,name,lastplayed):
		#Nom LAST à l'affichage
		last_date=time.strptime(lastplayed,'%Y%m%dT%H%M%S')
		if config.language=='FR':
			last_date_pr=time.strftime('%d/%m/%Y %H:%M:%S',last_date)
		else:
			last_date_pr=time.strftime('%m/%d/%Y %H:%M:%S',last_date)	
		return "{}. {} {}".format(pos,last_date_pr,name)


	#folder functions----------------------------------------------------------------	
	def __get_folder_from_element(self,element):
		"""convert dom element to pojo folder"""
		folder = Folder()
		##Lecture des attributs du noeud game
		#folder.ref_id=element.getAttribute("id")
		#folder.source=element.getAttribute("source")
		##Lecture des noeuds fils
		folder.path = self.__get_sub_element_value(element,"path")
		folder.name = self.__get_sub_element_value(element,"name")
		folder.desc = self.__get_sub_element_value(element,"desc")
		folder.image = self.__get_sub_element_value(element,"image")
		folder.hidden = self.__get_sub_element_value(element,"hidden")
		folder.background = self.__get_sub_element_value(element,"background")
		folder.screenshot = self.__get_sub_element_value(element,"screenshot")
		folder.logo = self.__get_sub_element_value(element,"logo")
		folder.textcolor = self.__get_sub_element_value(element,"textcolor")
		return folder

	
	def search_folder_by_path(self,search_path):
		"""search folder element by path and return objet """
		return self.__search_node_by_path(self._CLASS_FOLDER_NODENAME,search_path)

	
	def get_folders(self):
		"""get alls folder elements"""
		return self.__get_nodes_by_type(self._CLASS_FOLDER_NODENAME)


	def add_folder(self,newfolder):
		"""add a game in dom"""
		gamelist_element = self._gameListXmlDom.getElementsByTagName(self._CLASS_GAMELIST_NODENAME)
		newdom_folder_element = self._gameListXmlDom.createElement(self._CLASS_FOLDER_NODENAME)
		#newdom_folder_element.setAttribute("id",newfolder.ref_id)
		#if newfolder.source=='':newfolder.source=SOURCE_NAME
		#newdom_folder_element.setAttribute("source",newfolder.source)
		self.__add_subelement_node(newdom_folder_element,"path",newfolder.path)
		if newfolder.name!='':
			self.__add_subelement_node(newdom_folder_element,"name",newfolder.name)
		if newfolder.desc!='':
			self.__add_subelement_node(newdom_folder_element,"desc",newfolder.desc)
		if newfolder.image!='':
			self.__add_subelement_node(newdom_folder_element,"image",newfolder.image)
		if newfolder.hidden!='':
			self.__add_subelement_node(newdom_folder_element,"hidden",newfolder.hidden)
		if newfolder.background!='':
			self.__add_subelement_node(newdom_folder_element,"background",newfolder.background)
		if newfolder.screenshot!='':
			self.__add_subelement_node(newdom_folder_element,"screenshot",newfolder.screenshot)
		if newfolder.logo!='':
			self.__add_subelement_node(newdom_folder_element,"logo",newfolder.logo)
		if newfolder.textcolor!='':
			self.__add_subelement_node(newdom_folder_element,"textcolor",newfolder.textcolor)

		gamelist_element[0].appendChild(newdom_folder_element)
		self.__tag_update()

					
	def update_folder(self,updfolder):
		"""update existing game node in dom"""
		tag_path = self._gameListXmlDom.getElementsByTagName("path")
		for element in tag_path:
			if element.firstChild.nodeValue == updfolder.path:
				folder_node = element.parentNode
				#folder_node.setAttribute("id",updfolder.ref_id)
				#if updfolder.source=='':updfolder.source=SOURCE_NAME
				#folder_node.setAttribute("source",updfolder.source)
				self.__set_sub_element_value(folder_node,"path",updfolder.path)
				self.__set_sub_element_value(folder_node,"name",updfolder.name)
				self.__set_sub_element_value(folder_node,"desc",updfolder.desc)
				self.__set_sub_element_value(folder_node,"image",updfolder.image)
				self.__set_sub_element_value(folder_node,"hidden",updfolder.hidden)
				self.__set_sub_element_value(folder_node,"background",updfolder.background)
				self.__set_sub_element_value(folder_node,"screenshot",updfolder.screenshot)
				self.__set_sub_element_value(folder_node,"logo",updfolder.logo)
				self.__set_sub_element_value(folder_node,"textcolor",updfolder.textcolor)
				self.__tag_update()


	def delete_folder(self,delfolder):
		"""delete existing folder in dom"""
		tag_path = self._gameListXmlDom.getElementsByTagName("path")
		for element in tag_path:
			if element.firstChild.nodeValue == delfolder.path:
				gamelist_element = self._gameListXmlDom.getElementsByTagName(self._CLASS_GAMELIST_NODENAME)
				if element.parentNode.nodeName == self._CLASS_FOLDER_NODENAME:
					gamelist_element[0].removeChild(element.parentNode)
					self.__tag_update()


