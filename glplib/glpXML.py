#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                              - GAMELISTPOWER -                               #
#                             - MODULE GAMELIST -                              #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.15 31/10/2016-23/04/2020 #
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
		self._hashtag="" 		#RecalBox 18.06.27
		self._video=""      #RecalBox 6.1 (gamelistpower 0.9.14)
		self._md5=""        #Arrm (gamelistpower 0.9.14)
		self._marquee=""    #Arrm/BATOCERA (gamelistpower 0.9.15)
		
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
	@property
	def hashtag(self):return self._hashtag
	@property
	def video(self):return self._video
	@property
	def md5(self):return self._md5
	@property
	def marquee(self):return self._marquee
		
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
	@hashtag.setter
	def hashtag(self,v):self._hashtag=v
	@video.setter
	def video(self,v):self._video=v
	@md5.setter
	def md5(self,v):self._md5=v
	@marquee.setter
	def marquee(self,v):self._marquee=v
	
		
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
		self.hashtag = game_src.hashtag
		self.video = game_src.video
		self.md5 = game_src.md5
		self.marquee = game_src.marquee
		
		#Id interne non transmis
		self.internal_glp_id = time.strftime('%Y%m%dT%H%M%S',time.localtime())
		
	def smartCopy_from_game(self,game_src):
		"""Copie tous les attributs (en dehors du path) d'un objet game à un autre avec des contrôle de cohérence"""		
		self.name = game_src.name
		if game_src.desc!='':
			self.desc = game_src.desc
		if game_src.image!='' and os.path.isfile(game_src.image):
			self.image = game_src.image
		if game_src.rating!='':
			self.rating = game_src.rating
		if self.releasedate=='' or self.releasedate < game_src.releasedate:
			self.releasedate = game_src.releasedate
		if game_src.developer!='':
			self.developer = game_src.developer
		if game_src.publisher!='':
			self.publisher = game_src.publisher
		if game_src.genre!='':
			self.genre = game_src.genre
		if game_src.players!='':
			self.players = game_src.players
		if game_src.ref_id!='':
			self.ref_id = game_src.ref_id
		if game_src.source!='':
			self.source = game_src.source
		if game_src.playcount!='':
			self.playcount = game_src.playcount
		if self.lastplayed=='' or self.lastplayed < game_src.lastplayed:
			self.lastplayed = game_src.lastplayed
		if game_src.specific!='':
			self.specific = game_src.specific
		if game_src.hidden!='':
			self.hidden = game_src.hidden
		if game_src.background!='':
			self.background = game_src.background
		if game_src.screenshot!='':
			self.screenshot = game_src.screenshot
		if game_src.logo!='':
			self.logo = game_src.logo
		if game_src.textcolor!='':
			self.textcolor = game_src.textcolor
		if game_src.favorite!='':
			self.favorite = game_src.favorite
		if game_src.region!='':
			self.region = game_src.region
		if game_src.emulator!='':
			self.emulator = game_src.emulator
		self.core = game_src.core
		if game_src.ratio!='':
			self.ratio = game_src.ratio
		if game_src.thumbnail!='':
			self.thumbnail = game_src.thumbnail
		if game_src.romtype!='':
			self.romtype = game_src.romtype
		if game_src.hashtag!='':
			self.hashtag = game_src.hashtag
		if game_src.video!='':
			self.video = game_src.video
		if game_src.md5!='':
			self.md5 = game_src.md5
		if game_src.marquee!='':
			self.marquee = game_src.marquee
			
		#Id interne non transmis
		self.internal_glp_id = time.strftime('%Y%m%dT%H%M%S',time.localtime())
		
		#Cleaning des dates
		self.releasedate=self.cleaningDate(self.releasedate)
		self.lastplayed=self.cleaningDate(self.lastplayed)

	def cleaningDate(self,oldDate):
		if oldDate=='01010101T000000':
			return ''
		else:
			return oldDate
			
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
	
	_last_updated_date=""
	_last_quickupdated_date=""
	_empty_file_at_load=False
	_refresh_folders="no"
	
	
	#XML definition----------------------------------------------------------------	
	_CLASS_GAME_NODENAME="game"
	_CLASS_FOLDER_NODENAME="folder"
	_CLASS_GAMELIST_NODENAME="gameList"
	
	
	def getGameXMLAttributeName_Standard(self):
		return ['path','name','desc','image','rating','releasedate','developer','publisher','genre','region','players','playcount','lastplayed','hidden','favorite','md5','marquee']
	
	def getGameXMLAttributeName_Recalbox(self):
		return ['emulator','emulators','cores','core','ratio','romtype','thumbnail','hash','video']
	
	def getGameXMLAttributeName_Happigc(self):
		return ['background','screenshot','logo','textcolor']
	
	def getGameXMLAttributeName_TextType(self):
		return ['name','desc','developer','publisher','genre','region','md5']
	
	def getGameXMLAttributeName_PathType(self):
		return ['path','image','thumbnail','background','screenshot','logo','video','marquee']
	
	def getGameXMLAttributeName_DateType(self):
		return ['releasedate','lastplayed']
	
	def getGameXMLAttributeName_Default(self):
		return ['path','name','desc','image','releasedate','developer','publisher','genre','region','players','video']
	
	def getGameXMLAttributeName(self):
		standard = self.getGameXMLAttributeName_Standard()
		standard.extend(self.getGameXMLAttributeName_Recalbox())
		standard.extend(self.getGameXMLAttributeName_Happigc())
		
		return standard
		
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
			for TagXML in self.getGameXMLAttributeName():
				prettyXml = prettyXml.replace('<'+TagXML+'>','    <'+TagXML+'>')
				prettyXml = prettyXml.replace('<'+TagXML+'/>','    <'+TagXML+'/>')
			
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
	
	
	def sort(self,sortkey1='name',sortkey2='name',descending=False):
		"""Tri des noeuds XML selon deux clés"""
		gamesList_sorted = GamesList()
		gamesList_sorted.create_root_xml()
		
		for folder_sorted in sorted(self.get_folders(),key=attrgetter(sortkey1,sortkey2),reverse=descending):
			gamesList_sorted.add_folder(folder_sorted)
	
		for game_sorted in sorted(self.get_games(),key=attrgetter(sortkey1,sortkey2),reverse=descending):
			gamesList_sorted.add_game(game_sorted)
			
		return gamesList_sorted
		
	
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
	
	def __set_sub_element_value(self,nodegame,elementname,value,deleteEmptyTag=True):
		"""write value of element"""
		try:
			if value=='':
				nodegame.removeChild(nodegame.getElementsByTagName(elementname)[0])
				
				if not deleteEmptyTag and elementname in self.getGameXMLAttributeName_Default():
					self.__add_subelement_node(nodegame,elementname,value)
				
			else:
				nodegame.getElementsByTagName(elementname)[0].firstChild.nodeValue=value

		except (AttributeError,IndexError):
			if value !='':
				self.__add_subelement_node(nodegame,elementname,value)
			elif not deleteEmptyTag and elementname in self.getGameXMLAttributeName_Default():
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
		game.hashtag = self.__get_sub_element_value(element,"hash")
		game.video = self.__get_sub_element_value(element,"video")
		game.md5 = self.__get_sub_element_value(element,"md5")
		game.marquee = self.__get_sub_element_value(element,"marquee")
		
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
		#print (search_attr,search_value)
	
		if search_attr=='ref_id':		
			return filter(lambda x: x.ref_id == search_value , self.__get_nodes_by_type(self._CLASS_GAME_NODENAME))
		else:
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
		if newgame.video!='':
			self.__add_subelement_node(newdom_game_element,"video",newgame.video)
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
			self.__add_subelement_node(newdom_game_element,"hidden",newgame.hidden)
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
		if newgame.hashtag!='':
			self.__add_subelement_node(newdom_game_element,"hash",newgame.hashtag)
		if newgame.md5!='':
			self.__add_subelement_node(newdom_game_element,"md5",newgame.md5)
		if newgame.marquee!='':
			self.__add_subelement_node(newdom_game_element,"marquee",newgame.marquee)
		
		gamelist_element[0].appendChild(newdom_game_element)
		self.__tag_update()

			
	def update_game(self,updgame,deleteEmptyTag=True):
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
				self.__set_sub_element_value(game_node,"path",updgame.path,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"name",updgame.name,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"desc",updgame.desc,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"image",updgame.image,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"rating",updgame.rating,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"releasedate",updgame.releasedate,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"developer",updgame.developer,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"publisher",updgame.publisher,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"genre",updgame.genre,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"players",updgame.players,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"playcount",updgame.playcount,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"lastplayed",updgame.lastplayed,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"hidden",updgame.hidden,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"background",updgame.background,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"screenshot",updgame.screenshot,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"logo",updgame.logo,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"textcolor",updgame.textcolor,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"favorite",updgame.favorite,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"region",updgame.region,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"emulator",updgame.emulator,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"core",updgame.core,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"ratio",updgame.ratio,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"thumbnail",updgame.thumbnail,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"romtype",updgame.romtype,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"hash",updgame.hashtag,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"video",updgame.video,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"md5",updgame.md5,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"marquee",updgame.marquee,deleteEmptyTag)
				
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




#CLASS-GAME-EXPORT---------------------------------------------------------------
class GameExport:
	
	def __init__(self,**kwargs):
		self._plateform=''
		self._plateformPath=''
		self._path=''
		self._name=''
		self._hashtag="" 		#RecalBox 18.06.27
		self._favorite=""
		self._playcount=''
		self._lastplayed=''
		self._hidden=''
		self._specific=''
				
		if kwargs is not None:
			#mise à jour paramètre(s) nommé(s)
			self.__dict__.update(kwargs)

	def __repr__(self):
        	return repr((self.name, self.path, self.favorite, self.playcount, self.lastplayed, self.hidden))

	#property-------------------------
	@property
	def plateform(self):return self._plateform
	@property
	def plateformPath(self):return self._plateformPath
	@property
	def path(self):return self._path
	@property
	def name(self):return self._name
	@property
	def hashtag(self):return self._hashtag
	@property
	def favorite(self):return self._favorite
	@property
	def hidden(self):return self._hidden		
	@property
	def playcount(self):return self._playcount
	@property
	def lastplayed(self):return self._lastplayed
	@property
	def specific(self):return self._specific
	
	#setter-------------------------	
	@plateform.setter
	def plateform(self,v):self._plateform=v
	@plateformPath.setter
	def plateformPath(self,v):self._plateformPath=v
	@path.setter
	def path(self,v):self._path=v
	@name.setter
	def name(self,v):self._name=v
	@hashtag.setter
	def hashtag(self,v):self._hashtag=v
	@favorite.setter
	def favorite(self,v):self._favorite=v
	@hidden.setter
	def hidden(self,v):self._hidden=v
	@playcount.setter
	def playcount(self,v):self._playcount=v
	@lastplayed.setter
	def lastplayed(self,v):self._lastplayed=v
	@specific.setter
	def specific(self,v):self._specific=v
			
	def get_filename_rom(self):
		"""Extraction du nom de fichiers dans un path"""
		return self.path.replace('\\','/').split('/')[-1]
		
		
	def import_from_game(self,plateform,plateform_path,game_src,addPlayInfo=True,addHidden=True):
		"""Copie les attributs d'un object game vers GameExport"""		
		
		self.plateform = plateform
		self.plateformPath = plateform_path
		self.path = game_src.path
		self.name = game_src.name
		self.hashtag = game_src.hashtag
		self.favorite = game_src.favorite
		if addPlayInfo:
			self.playcount = game_src.playcount
			self.lastplayed = game_src.lastplayed
		if addHidden:
			self.hidden = game_src.hidden
		
	def export_to_game(self,game_dest,addPlayInfo=True,addHidden=True):
		"""Copie les attributs de l'objet vers un object game"""		
		
		game_dest.favorite = self.favorite
		if addPlayInfo:
			game_dest.playcount = self.playcount
			game_dest.lastplayed = self.lastplayed
		if addHidden:
			game_dest.hidden = self.hidden
	
		return game_dest
		
		
#CLASS-GAMESLIST-EXPORT------------------------------------------------------------------
class GamesListExport:
	"""Class Gameslist of gamelist.xml"""
	_gameListXmlDom = minidom.getDOMImplementation()
	_last_updated_date=""
	_empty_file_at_load=False
	
	#XML definition----------------------------------------------------------------	
	_CLASS_GAME_NODENAME_EXPORT="gameExport"
	_CLASS_GAMELIST_NODENAME_EXPORT="gameListExport"
			
	def getGameXMLAttributeName(self):
		return ['path','name','hash','favorite','playcount','lastplayed','hidden','plateform','plateformPath']


	#property----------------------------------------------------------------	
	@property
	def modified(self):return self._last_updated_date!=''
	@property
	def last_updated_date(self):return self._last_updated_date	
	@property
	def empty_file_at_load(self):return self._empty_file_at_load

	#file operations----------------------------------------------------------------	
	def create_root_xml(self):
		self._gameListXmlDom = minidom.parseString('<?xml version="1.0" ?><'+self._CLASS_GAMELIST_NODENAME_EXPORT+'></'+self._CLASS_GAMELIST_NODENAME_EXPORT+'>')
		self._empty_file_at_load = True
		
	def import_xml_file(self,fullpathname,bStopIfGeneralError=True):
		try:
			self._gameListXmlDom = minidom.parse(fullpathname)
			self.__load_update_dates()
			
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
			prettyXml = prettyXml.replace('<'+self._CLASS_GAME_NODENAME_EXPORT,'  <'+self._CLASS_GAME_NODENAME_EXPORT)
			prettyXml = prettyXml.replace('  <'+self._CLASS_GAMELIST_NODENAME_EXPORT+'>','<'+self._CLASS_GAMELIST_NODENAME_EXPORT+'>') #Patch 0.5.06
			prettyXml = prettyXml.replace('</'+self._CLASS_GAME_NODENAME_EXPORT+'>','  </'+self._CLASS_GAME_NODENAME_EXPORT+'>')
			for TagXML in self.getGameXMLAttributeName():
				prettyXml = prettyXml.replace('<'+TagXML+'>','    <'+TagXML+'>')
				prettyXml = prettyXml.replace('<'+TagXML+'/>','    <'+TagXML+'/>')
			
			#Ecriture sur disque
			f = open(fullpathname,'w')
			f.write(prettyXml.encode("UTF-8"))
			f.close()
			
		else:
			#Ecriture sur disque
			f = open(fullpathname,'w')
			f = codecs.lookup("utf-8")[3](f)
			self._gameListXmlDom.writexml(f, encoding="utf-8")
			f.close()
	
	
	def sort(self,sortkey1='name',sortkey2='name',descending=False):
		"""Tri des noeuds XML selon deux clés"""
		gamesList_sorted = GamesListExport()
		gamesList_sorted.create_root_xml()
		
		for game_sorted in sorted(self.get_games(),key=attrgetter(sortkey1,sortkey2),reverse=descending):
			gamesList_sorted.add_game(game_sorted)
			
		return gamesList_sorted
		
	
	#debug----------------------------------------------------------------	
	def to_xml(self):
		return self._gameListXmlDom.toxml() 

	#private functions----------------------------------------------------------------	
	def __tag_update(self):
		"""set modified and update date, quick reserved for quickupdate"""
		self._modified=True
		self._last_updated_date=time.strftime('%Y%m%dT%H%M%S',time.localtime())
		gamelist_element = self._gameListXmlDom.getElementsByTagName(self._CLASS_GAMELIST_NODENAME_EXPORT)
		gamelist_element[0].setAttribute("last_update_date",self._last_updated_date)
		gamelist_element[0].setAttribute("source",SOURCE_NAME)
	
	
	def __load_update_dates(self):
		""" retrieve date from gamelist node"""
		gamelist_element = self._gameListXmlDom.getElementsByTagName(self._CLASS_GAMELIST_NODENAME_EXPORT)
		self._last_updated_date = gamelist_element[0].getAttribute("last_update_date")
		logger.debug(msg_local.get(('MSG_DEBUG_GLX_UPD_DATE',config.language)).format(self._last_updated_date,self._last_updated_date,self._last_updated_date))
		
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
	
	def __set_sub_element_value(self,nodegame,elementname,value,deleteEmptyTag=True):
		"""write value of element"""
		try:
			if value=='':
				nodegame.removeChild(nodegame.getElementsByTagName(elementname)[0])
				
				if not deleteEmptyTag and elementname in self.getGameXMLAttributeName_Default():
					self.__add_subelement_node(nodegame,elementname,value)
				
			else:
				nodegame.getElementsByTagName(elementname)[0].firstChild.nodeValue=value

		except (AttributeError,IndexError):
			if value !='':
				self.__add_subelement_node(nodegame,elementname,value)
			elif not deleteEmptyTag and elementname in self.getGameXMLAttributeName_Default():
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
					if element.parentNode.nodeName == self._CLASS_GAME_NODENAME_EXPORT:
						return self.__get_game_from_element(element.parentNode)
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
					if element.parentNode.nodeName == self._CLASS_GAME_NODENAME_EXPORT:
						nodes_found.append(self.__get_game_from_element(element.parentNode))
					elif element.parentNode.nodeName == self._CLASS_FOLDER_NODENAME:
						nodes_found.append(self.__get_folder_from_element(element.parentNode))
					else:
						raise MyError('Unknow node')
		return nodes_found
				
	#game functions----------------------------------------------------------------	
	def __get_game_from_element(self,element):
		"""convert dom element to pojo game"""
		game = GameExport()
		##Lecture des noeuds fils
		game.path = self.__get_sub_element_value(element,"path")
		game.name = self.__get_sub_element_value(element,"name")
		game.plateform = self.__get_sub_element_value(element,"plateform")
		game.playcount = self.__get_sub_element_value(element,"playcount")
		game.lastplayed = self.__get_sub_element_value(element,"lastplayed")
		game.hidden = self.__get_sub_element_value(element,"hidden")
		game.favorite = self.__get_sub_element_value(element,"favorite")
		game.hashtag = self.__get_sub_element_value(element,"hash")
		return game

	def search_game_by_path(self,search_path):
		"""search game element by path and return objet """
		try:
			return self.__search_node_by_path(self._CLASS_GAME_NODENAME_EXPORT,search_path)
		except:
			#Cas de Windows sur des fichiers GAMELIST unix (test only)
			return self.__search_node_by_path(self._CLASS_GAME_NODENAME_EXPORT,search_path.replace(os.sep,'/'))
			
	def search_games(self,search_attr,search_value):
		"""return games which matches critera"""

		return self.__search_nodes_by_attr(self._CLASS_GAME_NODENAME_EXPORT,search_attr,search_value)
		
	def get_games(self):
		"""get alls game elements"""
		return self.__get_nodes_by_type(self._CLASS_GAME_NODENAME_EXPORT)

	def get_games_by_plateformPath(self,seach_plateform):
		"""get alls game on a specific plateform"""
		return self.__search_nodes_by_attr(self._CLASS_GAME_NODENAME_EXPORT,'plateformPath',seach_plateform)

	def add_game(self,newgame):
		"""add a game in dom"""
		gamelist_element = self._gameListXmlDom.getElementsByTagName(self._CLASS_GAMELIST_NODENAME_EXPORT)
		newdom_game_element = self._gameListXmlDom.createElement(self._CLASS_GAME_NODENAME_EXPORT)
		
		#SubElements	
		self.__add_subelement_node(newdom_game_element,"path",newgame.path)
		if newgame.plateform!='':
			self.__add_subelement_node(newdom_game_element,"plateform",newgame.plateform)
		if newgame.plateformPath!='':
			self.__add_subelement_node(newdom_game_element,"plateformPath",newgame.plateformPath)
		if newgame.name!='':
			self.__add_subelement_node(newdom_game_element,"name",newgame.name)
		if newgame.playcount!='':
			self.__add_subelement_node(newdom_game_element,"playcount",str(newgame.playcount))
		if newgame.lastplayed!='':
			self.__add_subelement_node(newdom_game_element,"lastplayed",newgame.lastplayed)
		if newgame.hidden!='':
			self.__add_subelement_node(newdom_game_element,"hidden",newgame.hidden)
		if newgame.favorite!='':
			self.__add_subelement_node(newdom_game_element,"favorite",newgame.favorite)
		if newgame.hashtag!='':
			self.__add_subelement_node(newdom_game_element,"hash",newgame.hashtag)
		
		gamelist_element[0].appendChild(newdom_game_element)
		self.__tag_update()

			
	def update_game(self,updgame,deleteEmptyTag=True):
		"""update existing game node in dom"""
		tagpath = self._gameListXmlDom.getElementsByTagName("path")
		for element in tagpath:
			if element.firstChild.nodeValue == updgame.path:
				game_node = element.parentNode
				#SubElements	
				self.__set_sub_element_value(game_node,"path",updgame.path,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"plateformPath",updgame.plateformPath,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"name",updgame.name,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"plateform",updgame.plateform,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"playcount",updgame.playcount,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"lastplayed",updgame.lastplayed,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"hidden",updgame.hidden,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"favorite",updgame.favorite,deleteEmptyTag)
				self.__set_sub_element_value(game_node,"hash",updgame.hashtag,deleteEmptyTag)
				self.__tag_update()

		
	def delete_game(self,delgame):
		"""delete existing folder in dom"""
		tag_path = self._gameListXmlDom.getElementsByTagName("path")
		for element in tag_path:
			if element.firstChild.nodeValue == delgame.path:
				gamelist_element = self._gameListXmlDom.getElementsByTagName(self._CLASS_GAMELIST_NODENAME_EXPORT)
				if element.parentNode.nodeName == self._CLASS_GAME_NODENAME_EXPORT:
					gamelist_element[0].removeChild(element.parentNode)
					self.__tag_update()
