#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                              - GAMELISTPOWER -                               #
#                               - MODULE TOOLS -                               #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.00 31/10/2016-21/05/2018 #
#------------------------------------------------------------------------------#

#IMPORT STD---------------------------------------------------------------------
import logging
import ConfigParser
import os.path
import sys
import logging
from logging.handlers import RotatingFileHandler
import StringIO
import codecs

#CONSTANTS----------------------------------------------------------------------
DEFAULT_EXTENSIONS_IMAGE=['jpg','JPG','png','PNG']
DEFAULT_PATH_INI='/home/pi/happi/script/maconfig'
#MSG LOCALISATION---------------------------------------------------------------
#config=Config()

msg_local={
('MSG_ERROR_GLT_EXCEPTION','FR'):u'{} : {}',
('MSG_ERROR_GLT_EXCEPTION','EN'):u'{} : {}',
('MSG_GLT_ERROR_FINDENTRY','FR'):u'Impossible de trouver l''entr\u00E9e {}= ou la section {} dans {}',
('MSG_GLT_ERROR_FINDENTRY','EN'):u'Can''t find {}= entry, section {} in {}',
('MSG_DEBUG_GLT_FINDENTRY','FR'):u'Impossible de trouver l''entr\u00E9e {}= ou la section {} dans {}',
('MSG_DEBUG_GLT_FINDENTRY','EN'):u'Can''t find {}= entry, section {} in {}',
('MSG_ERROR_GLT_LAN_NOT_SUPPORTED','FR'):u'Language={} non support\u00E9 !',
('MSG_ERROR_GLT_LAN_NOT_SUPPORTED','EN'):u'Language={} not supported !',
('MSG_DEBUG_GLT_EXC_DIR_NOT_EXIST','FR'):u'le chemin exclusion_directories {} n''existe pas',
('MSG_DEBUG_GLT_EXC_DIR_NOT_EXIST','EN'):u'Exclusion_directories not exist {} !',
('MSG_WARN_GLT_GAME_NOT_PICT_DEF','FR'):u'Le chemin de l''image par d\u00E9faut {} n''existe pas',
('MSG_WARN_GLT_GAME_NOT_PICT_DEF','EN'):u'File default for game not exist {} !',
('MSG_ERROR_GLT_CONF_FILE_NOT_FOUND','FR'):u'Fichier {} non trouv\u00E9 !',
('MSG_ERROR_GLT_CONF_FILE_NOT_FOUND','EN'):u'Can''t find {} !',
('MSG_DEBUG_GLT_CONF_FILE_LOAD','FR'):u'Fichier de configuration {}',
('MSG_DEBUG_GLT_CONF_FILE_LOAD','EN'):u'Configuration file {}',
('MSG_ERROR_GLT_NO_NAME_XML','FR'):u'Aucun nom trouv\u00E9 {}_name_xml, utilisation de {} \u00E0 la place dans {}',
('MSG_ERROR_GLT_NO_NAME_XML','EN'):u'No name in {}_name_xml, use {} as name in {}',
('MSG_ERROR_GLT_NO_DEF_PICT','FR'):u'Image par d\u00E9faut de {} manquante dans {}, D\u00E9sactivation de la fonctionnalit\u00E9',
('MSG_ERROR_GLT_NO_DEF_PICT','EN'):u'{}_default_image is missing in {}, default picture for this folder is disabled !'
}


#CLASS-SINGLETON----------------------------------------------------------------
def singleton(cls):
    instances = {}
    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance()

#CLASS-EXCEPTION----------------------------------------------------------------
class MyError(Exception):
	"""my own raise exception"""
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

#CLASS-OBJECTWITHEVENTS-------------------------------------------------------------------
class ObjectWithEvents(object):
	"""gestion d'appel inter-objets"""
	callbacks = None
	
	def on(self, event_name, callback):
		if self.callbacks is None:
			self.callbacks = {}
	
		if event_name not in self.callbacks:
			self.callbacks[event_name] = [callback]
		else:
			self.callbacks[event_name].append(callback)
	
	def trigger(self, event_name):
		if self.callbacks is not None and event_name in self.callbacks:
			for callback in self.callbacks[event_name]:
				callback(self)


#CLASS-LOGGER-------------------------------------------------------------------
class loggerEvent(logging.getLoggerClass(),ObjectWithEvents):
	"""logger couplé des events pour affichage graphique"""
	
	def __init__(self,name,**kwargs):
		self._MessageValue=''
		self._ActivateEvents=False
		self._name = name
		
		logging.getLoggerClass().__init__(self,name)
		
		if kwargs is not None:
			#mise à jour paramètre(s) nommé(s)
			self.__dict__.update(kwargs)
	
	#property-------------------------	
	@property
	def ActivateEvents(self):return self._ActivateEvents
	#setter-------------------------	
	@ActivateEvents.setter
	def ActivateEvents(self,v):self._ActivateEvents=v
	
	#Récriture des appels de logging
	def debug(self, message):
		self.root.debug(message)
		#if self._ActivateEvents:
		#	self._MessageValue=message+'\n'
		#	self.trigger('NewMessage')
		
	def info(self, message):
		self.root.info(message)
		if self._ActivateEvents:
			self._MessageValue=message+'\n'
			self.trigger('NewMessage')
    
	def warn(self, message):
		self.root.warn(message)
		if self._ActivateEvents:
			self._MessageValue=message+'\n'
			self.trigger('NewMessage')
		
	def error(self, message):
		self.root.error(message)
		if self._ActivateEvents:
			self._MessageValue=message+'\n'
			self.trigger('NewMessage')
		
	def critical(self, message):
		self.root.critical(message)
		if self._ActivateEvents:
			self._MessageValue=message+'\n'
			self.trigger('NewMessage')
	
	def addHandler(self, hdlr):
		self.root.addHandler(hdlr)
		
	def setLevel(self, level):
		self.root.setLevel(level)
		

	#Event, récupération du message en cours
	def __str__(self):
		return self._MessageValue
		

@singleton
class Logger():
	
	_stream_buffer = StringIO.StringIO()
	
	def __init__(self):
		#Init Logger
		#self.logr = logging.getLogger()
		self.logr = loggerEvent('glp')
		self.logr.setLevel(logging.DEBUG)
		#Logger 1:fichier rotate en niveau debug, 1M, 1 sauvegarde.
		formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
		if os.path.exists('/recalbox'):
			file_handler = RotatingFileHandler(filename='/recalbox/share/system/logs/gamelistpower.log', mode='a', maxBytes=2000000, backupCount=1)
		else:
			file_handler = RotatingFileHandler(filename='gamelistpower.log', mode='a', maxBytes=2000000, backupCount=1)
		
		file_handler.setLevel(logging.DEBUG)
		file_handler.setFormatter(formatter)
		self.logr.addHandler(file_handler)
		
	def __del__(self):
		self._stream_buffer.close()
	
	def add_handler_console(self):
		stream_handler_stdout = logging.StreamHandler()
		stream_handler_stdout.setLevel(logging.INFO)
		self.logr.addHandler(stream_handler_stdout)
	
	def add_handler_StringIO(self):
		"""déprécié, ne permet pas d'utiliser des échanges avec des caractères avec accent"""
		stream_buffer_buffer = logging.StreamHandler(self._stream_buffer)
		stream_buffer_buffer.setLevel(logging.INFO)
		self.logr.addHandler(stream_buffer_buffer)
	
	def add_handler_GUI(self):
		self.logr.ActivateEvents=True
	
	def setLevel(self, level):
		self.logr.setLevel(level)
		for h in self.logr.handlers:
			h.SetLevel(level)
			
	def read_buffer(self):
		return self._stream_buffer.getvalue()
		
	def truncate_buffer(self):
		return self._stream_buffer.truncate(0)




		
				 
#CLASS-CONFIG-------------------------------------------------------------------
class Config:
	"""Configuration of the batch"""
	def __init__(self):
		self._rootpath=''
		self._rootpath_usb=''
		#self._inifilename=__file__[0:-3] + '.ini'
		self._inifilename='gamelistpower.ini'
		self._configParser=ConfigParser.ConfigParser(allow_no_value=True)
		
		self._language='FR'		
		self._option_save_origin=True
		self._option_save_backup=True
		
		self._emulation_station_systems=''
		self._emulation_station_systems_usb=''
		self._emulation_station_settings=''
		self._emulation_station_themes=''
		
		self._theme_menu_file_configxml=''
		self._theme_menu_sh_folder=''
		self._theme_sh_name=''
		self._theme_sh_launch=''
		
		self._hint_use_refresh_tag=False
		self._hint_use_os_stat=False
		
		self._images_extension=[]
		self._images_folder=[]
		
		self._game_name_exclusion=[]
		self._game_name_hidden=[]
		self._game_extension_exclusion=[]
		self._game_delete_option='D' #Désactivé

		self._default_game_picture=''
		self._default_game_picture_mode=''

		self._folder_name_exclusion=[]
		self._folder_name_hidden=[]
		
		self._folder_default_picture=''
		self._folder_default_picture_mode=''
		
		self._folder_ko_picture=''
		self._folder_ko_picture_mode=''
		self._folder_ko_dir=''
		self._folder_ko_xml=''
		
		self._folder_top_dir=''
		self._folder_top_xml=''
		self._folder_top_nb=5
		self._folder_top_picture=''
		self._folder_top_picture_mode=''
		
		self._folder_last_dir=''
		self._folder_last_xml=''
		self._folder_last_nb=5
		self._folder_last_picture=''
		self._folder_last_picture_mode=''
	
		self._folder_best_dir=''
		self._folder_best_xml=''
		self._folder_best_nb=5
		self._folder_best_picture=''
		self._folder_best_picture_mode=''
		
		self._generation_rules=[]
		
		self._folder_multi=''
	
	
	#properties-------------------------------------------------------------------------------------------	
	#SCAN
	@property
	def rootPath(self):return self._rootpath
	@property
	def rootPathUsb(self):return self._rootpath_usb
	@property
	def images_extension(self):return self._images_extension
	@property
	def images_folder(self):return self._images_folder
		
	@property
	def game_name_exclusion(self):return self._game_name_exclusion
	@property
	def game_name_hidden(self):return self._game_name_hidden
	@property
	def game_extension_exclusion(self):return self._game_extension_exclusion
	
	@property
	def folder_name_exclusion(self):return self._folder_name_exclusion
	@property
	def folder_name_hidden(self):return self._folder_name_hidden
	@property
	def folder_path_multi(self):return self._folder_multi
		
	#GAME
	@property
	def default_game_picture(self):return self._default_game_picture	
	@property
	def is_default_game_picture_mode_append(self):return self._default_game_picture_mode[0].upper() == "A"
	@property
	def is_default_game_picture_mode_delete(self):return self._default_game_picture_mode[0].upper() == "S"
	@property
	def is_delete_game_everywhere(self):return self._game_delete_option[0].upper() == 'T'
	def is_delete_game_in_ko_only(self):return self._game_delete_option[0].upper() == 'R'		
	def is_delete_game_none(self):return (self._game_delete_option[0].upper() != 'T'	and self._game_delete_option[0].upper() != 'R')
		
	#SAVE
	@property
	def option_save_origin(self):return self._option_save_origin
	@property
	def option_save_backup(self):return self._option_save_backup
	
	#HINTS
	@property
	def hint_use_refresh_tag(self):return self._hint_use_refresh_tag
	@property
	def hint_use_os_stat(self):return self._hint_use_os_stat
	
	#EMULATION STATION
	@property
	def emulation_station_systems(self):return self._emulation_station_systems
	@property
	def emulation_station_systems_usb(self):return self._emulation_station_systems_usb
	@property
	def emulation_station_settings(self):return self._emulation_station_settings
	@property
	def emulation_station_themes(self):return self._emulation_station_themes
	
	
	#THEME
	@property
	def theme_menu_file_configxml(self):return self._theme_menu_file_configxml
	@property
	def theme_menu_sh_folder(self):return self._theme_menu_sh_folder
	@property
	def theme_sh_name(self):return self._theme_sh_name
	@property
	def theme_sh_launch(self):return self._theme_sh_launch
		
	
	#MISC	
	@property
	def language(self):return self._language
	@property
	def generation_rules(self):return self._generation_rules
	
	#FOLDER DEFAULT
	@property
	def default_folder_picture_path(self):return self._folder_default_picture
	@property
	def is_folder_default_picture_mode_append(self):return self._folder_default_picture_mode[0].upper() == "A"
	@property
	def is_folder_default_picture_mode_delete(self):return self._folder_default_picture_mode[0].upper() == "S"
	
	#FOLDER KO
	@property
	def ko_folder_name_dir(self):return self._folder_ko_dir
	@property
	def ko_folder_name_xml(self):return self._folder_ko_xml
	@property
	def ko_folder_picture_path(self):return self._folder_ko_picture
	@property
	def is_folder_ko_picture_mode_append(self):return self._folder_ko_picture_mode[0].upper() == "A"
	@property
	def is_folder_ko_picture_mode_delete(self):return self._folder_ko_picture_mode[0].upper() == "S"
	
	#FOLDER TOP
	@property
	def top_folder_name_dir(self):return self._folder_top_dir
	@property
	def top_folder_name_xml(self):return self._folder_top_xml
	@property
	def top_folder_nb(self):return self._folder_top_nb	
	@property
	def folder_top_picture(self):return self._folder_top_picture	
	@property
	def is_folder_top_picture_mode_append(self):return self._folder_top_picture_mode[0].upper() == "A"
	@property
	def is_folder_top_picture_mode_delete(self):return self._folder_top_picture_mode[0].upper() == "S"
	
	#FOLDER LAST
	@property
	def last_folder_name_dir(self):return self._folder_last_dir
	@property
	def last_folder_name_xml(self):return self._folder_last_xml
	@property
	def last_folder_nb(self):return self._folder_last_nb	
	@property
	def folder_last_picture(self):return self._folder_last_picture	
	@property
	def is_folder_last_picture_mode_append(self):return self._folder_last_picture_mode[0].upper() == "A"
	@property
	def is_folder_last_picture_mode_delete(self):return self._folder_last_picture_mode[0].upper() == "S"
		
	#FOLDER BEST
	@property
	def best_folder_name_dir(self):return self._folder_best_dir
	@property
	def best_folder_name_xml(self):return self._folder_best_xml
	@property
	def best_folder_nb(self):return self._folder_best_nb	
	@property
	def folder_best_picture(self):return self._folder_best_picture	
	@property
	def is_folder_best_picture_mode_append(self):return self._folder_best_picture_mode[0].upper() == "A"
	@property
	def is_folder_best_picture_mode_delete(self):return self._folder_best_picture_mode[0].upper() == "S"
	
	
	#internal functions-----------------------------------------------------------------------------------
	def __ConfigSectionMap(self,section):
		dict1 = {}
		options = self._configParser.options(section)
		for option in options:
			try:
				dict1[option] = self._configParser.get(section, option)
				if dict1[option] == -1:
					logger.debug("skip: %s" % option)
			except:
				logger.error("exception on %s!" % option)
				dict1[option] = None
		return dict1


	def __debug_folder(self, prefix, folder_dir, folder_xml, folder_nb, folder_picture_mode, folder_picture):
		"""put folder options into logger"""
		
		if config.language=='FR':
			if prefix!='default':
				logger.debug('Configuration - Dossier ' + prefix.upper() + ' Nom = '+ folder_dir)
				logger.debug('Configuration - Dossier ' + prefix.upper() + ' Nom XML = ' + folder_xml)
			if prefix!='default' and prefix!='ko' and prefix!='best':
				logger.debug('Configuration - Dossier ' + prefix.upper() + ' NB   = ' + folder_nb)
			logger.debug('Configuration - Dossier ' + prefix.upper() + ' Image = ' + folder_picture_mode)
			logger.debug('Configuration - Dossier ' + prefix.upper() + ' Mode Image = ' + folder_picture)
			
		else:
			if prefix!='default':
				logger.debug('Config - Folder ' + prefix.upper() + ' Name = '+ folder_dir)
				logger.debug('Config - Folder ' + prefix.upper() + ' Name XML = ' + folder_xml)
			if prefix!='default' and prefix!='ko' and prefix!='best':
				logger.debug('Config - Folder ' + prefix.upper() + ' NB   = ' + folder_nb)
			logger.debug('Config - Folder ' + prefix.upper() + ' Picture = ' + folder_picture_mode)
			logger.debug('Config - Folder ' + prefix.upper() + ' Picture Mode = ' + folder_picture)
			
  #public functions----------------------------------------------------------------------------------------------------------------
	def debug(self):
		"""put all options into logger"""
		if config.language=='FR':
			logger.debug(u'Configuration - Dossier des ROMS = ' + self._rootpath)
			logger.debug(u'Configuration - Dossier des ROMS USB = ' + self._rootpath_usb)
			logger.debug(u'Configuration - Extension fichier des images = ' + ','.join(self._images_extension))
			#logger.debug(u'Configuration - Exclusion dossier = ' + ','.join(self._folder_name_exclusion))
			for dir in sorted(self._folder_name_exclusion):
				logger.debug(u'Configuration - Exclusion dossier = ' + dir)
		
		else:
			logger.debug(u'Config - Read roms = ' + self._rootpath)
			logger.debug(u'Config - Read roms from USB = ' + self._rootpath_usb)
			logger.debug(u'Config - Image Extensions = ' + ','.join(self._images_extension))
			#logger.debug(u'Config - Folder Exclusion = ' + ','.join(self._folder_name_exclusion))
			for dir in sorted(self._folder_name_exclusion):
				logger.debug(u'Config - Folder Exclusion = ' + dir)
		
		self.__debug_folder('default', self._folder_default_dir, self._folder_default_xml, '0', self._folder_default_picture, self._folder_default_picture_mode)
		self.__debug_folder('ko', self._folder_ko_dir, self._folder_ko_xml, '0', self._folder_ko_picture, self._folder_ko_picture_mode)
		self.__debug_folder('top', self._folder_top_dir, self._folder_top_xml, str(self._folder_top_nb),self._folder_top_picture, self._folder_top_picture_mode)
		self.__debug_folder('last', self._folder_last_dir, self._folder_last_xml, str(self._folder_last_nb),self._folder_last_picture, self._folder_last_picture_mode)
		self.__debug_folder('best', self._folder_best_dir, self._folder_best_xml, str(self._folder_best_nb),self._folder_best_picture, self._folder_best_picture_mode)
		
		if config.language=='FR':
			logger.debug(u'Configuration - Jeux - Exclusion noms = ' + ','.join(self._game_name_exclusion))
			logger.debug(u'Configuration - Jeux - Roms cach\u00E9es = ' + ','.join(self._game_name_hidden))
			logger.debug(u'Configuration - Jeux - Exclusion extensions= ' + ','.join(self._game_extension_exclusion))
			logger.debug(u'Configuration - Jeux - Image par d\u00E9faut = ' + self._default_game_picture)
			logger.debug(u'Configuration - Jeux - Mode Image par d\u00E9faut = ' + self._default_game_picture_mode)
			logger.debug(u'Configuration - Jeux - Mode suppression des jeux = ' + self._game_delete_option)
			logger.debug(u'Configuration - Images - Extension fichiers = ' + ','.join(self._images_extension))
			logger.debug(u'Configuration - Images - Dossiers = ' + ','.join(self._images_folder))
			logger.debug(u'Configuration - Dossier - Dossiers cach\u00E9s = ' + ','.join(self._folder_name_hidden))
			logger.debug(u'Configuration - Dossier - Dossier multi-\u00E9mulateurs =' +self._folder_multi)
			logger.debug(u'Configuration - Gamelist - Sauvegarde 1er ex\u00E9cution = ' + str(self._option_save_origin))
			logger.debug(u'Configuration - Gamelist - Sauvegarde \u00E0 chaque ex\u00E9cution = ' + str(self._option_save_backup))
			logger.debug(u'Configuration - EmulationStation - es_systems.cfg = ' + self._emulation_station_systems)
			logger.debug(u'Configuration - EmulationStation - es_systems_usb.cfg = ' + self._emulation_station_systems_usb)
			logger.debug(u'Configuration - EmulationStation - es_settings.cfg = ' + self._emulation_station_settings)
			logger.debug(u'Configuration - EmulationStation - theme = ' + self._emulation_station_themes)
			logger.debug(u'Configuration - Config/Theme - config.xml = ' + self._theme_menu_file_configxml)
			logger.debug(u'Configuration - Config/Theme - folder = ' + self._theme_menu_sh_folder)
			logger.debug(u'Configuration - Config/Theme - sh_name = ' + self._theme_sh_name)
			logger.debug(u'Configuration - Config/Theme - sh_launch = ' + self._theme_sh_launch)
			logger.debug(u'Configuration - Optimisation attribut refresh  = ' + str(self._hint_use_refresh_tag))
			logger.debug(u'Configuration - Optimisation os.stat  = ' + str(self._hint_use_os_stat))
			for config_rule in self._generation_rules:
				logger.debug(u'Configuration - R\u00e8gle de g\u00E9n\u00E9ration [ '+ config_rule +' ]')
		else:
			logger.debug(u'Config - Game - Name Exclusion = ' + ','.join(self._game_name_exclusion))
			logger.debug(u'Config - Game - Name Hidden = ' + ','.join(self._game_name_hidden))
			logger.debug(u'Config - Game - Extension Exclusion = ' + ','.join(self._game_extension_exclusion))
			logger.debug(u'Config - Game - Default Picture = ' + self._default_game_picture)
			logger.debug(u'Config - Game - Default Picture Mode = ' + self._default_game_picture_mode)
			logger.debug(u'Config - Game - Delete Mode = ' + self._game_delete_option)
			logger.debug(u'Config - Picture - File Extension  = ' + ','.join(self._images_extension))
			logger.debug(u'Config - Picture - Folder = ' + ','.join(self._images_folder))
			logger.debug(u'Config - Folder - Name Hidden = ' + ','.join(self._folder_name_hidden))
			logger.debug(u'Config - Folder - Folder multi-emulators =' +_folder_multi)
			logger.debug(u'Config - Gamelist - SaveOrigin = ' + str(self._option_save_origin))
			logger.debug(u'Config - Gamelist - SaveBackup = ' + str(self._option_save_backup))
			logger.debug(u'Config - EmulationStation - es_systems.cfg = ' + self._emulation_station_systems)
			logger.debug(u'Config - EmulationStation - es_systems_usb.cfg = ' + self._emulation_station_systems_usb)
			logger.debug(u'Config - EmulationStation - es_settings.cfg = ' + self._emulation_station_settings)
			logger.debug(u'Config - EmulationStation - theme = ' + self._emulation_station_themes)
			logger.debug(u'Configuration - Config/Theme - config.xml = ' + self._theme_menu_file_configxml)
			logger.debug(u'Configuration - Config/Theme - folder = ' + self._theme_menu_sh_folder)
			logger.debug(u'Configuration - Config/Theme - sh_name = ' + self._theme_sh_name)
			logger.debug(u'Configuration - Config/Theme - sh_launch = ' + self._theme_sh_launch)
			logger.debug(u'Config - Hint refresh attribut = ' + str(self._hint_use_refresh_tag))
			logger.debug(u'Config - Hint os.stat  = ' + str(self._hint_use_os_stat))
			for config_rule in self._generation_rules:
				logger.debug(u'Config - Generation rule [ '+ config_rule +' ]')


	def load_from_file(self):
		"""read config from GameListParch.ini"""
		#0.7.06 - Chargement prioritaire à partir de /home/pi/happi/script/maconfig sur linux
		if os.name=='posix':
			if os.path.isfile(os.path.join(DEFAULT_PATH_INI,self._inifilename)):
				self._inifilename=os.path.join(DEFAULT_PATH_INI,self._inifilename)
				
		if os.path.isfile(self._inifilename):
			logger.debug(msg_local.get(('MSG_DEBUG_GLT_CONF_FILE_LOAD','EN')).format(self._inifilename))
			self._configParser.read(self._inifilename)
			
			#LANGUAGE----------------------------------------------------------------------------------
			try:
				self._language = self.__ConfigSectionMap('localisation')['language']
				self._language = self._language.upper()
				if not (self._language == 'EN' or self._language == 'FR'):
					#logger.error('Language='+self._language+' not supported')
					logger.error(msg_local.get(('MSG_ERROR_GLT_LAN_NOT_SUPPORTED','EN')).format(self._language))
					
					sys.exit(1)
			except:
				#logger.error('Can''t find language= entry, section [localisation] in '+self._inifilename)
				logger.error(msg_local.get(('MSG_ERROR_GLT_FINDENTRY','EN')).format('language','localisation',self._inifilename))
				
				sys.exit(1)
				
			
			#----- Section directories -----------------------------------------------
			#Répertoire des ROMS
			try:
				self._rootpath = self.__ConfigSectionMap('directories')['rom']
			except:
				#logger.error('Can''t find rom= entry, section [directories] in '+self._inifilename)
				logger.error(msg_local.get(('MSG_ERROR_GLT_FINDENTRY',config.language)).format('rom','directories',self._inifilename))
				sys.exit(1)
			if self._rootpath =='':
				#logger.error('Can''t find rom= entry, section [directories] in '+self._inifilename)
				logger.error(msg_local.get(('MSG_ERROR_GLT_FINDENTRY',config.language)).format('rom','directories',self._inifilename))
				sys.exit(1)
			
			#Répertoire des ROMS sur USB, optionnel
			try:
				self._rootpath_usb = self.__ConfigSectionMap('directories')['rom_usb']
			except:
				self._rootpath_usb = ''
			
			#Extensions des images (ajout des majuscules en auto)
			try:
				opt_image_extension = self.__ConfigSectionMap('directories')['image_extension']
				opt_image_extension = opt_image_extension + ',' + opt_image_extension.upper()
				self._images_extension = opt_image_extension.split(',')
			except:
				self._images_extension = DEFAULT_EXTENSIONS_IMAGE
			
			#Folder des images (ajout des majuscules en auto)
			try:
				opt_image_folder = self.__ConfigSectionMap('directories')['image_folder']
				self._images_folder = opt_image_folder.split(',')
			except:
				self._images_folder = 'images,downloaded_images'.split(',')
			
			#Exclusion de folder
			try:
				self._folder_name_exclusion=[]
				exclusion_directories = self.__ConfigSectionMap('directories')['exclusion_directories']
				if exclusion_directories!='':
					exc_folders=exclusion_directories.split(',')
					for exc_folder in exc_folders:
						if not os.path.isdir(exc_folder):
							logger.debug(msg_local.get(('MSG_DEBUG_GLT_EXC_DIR_NOT_EXIST',config.language)).format(exc_folder))
						else:
							self._folder_name_exclusion.append(exc_folder)
							#0.5.18 Ajout des sous dossiers d'exclusion
							for path, dirs, files in os.walk(exc_folder):
								for dir in dirs:
									self._folder_name_exclusion.append(os.path.join(path,dir))
									
				#else: Gestion du cas où il existe au moins un élément d'exclusion qui est invalide
				if len(self._folder_name_exclusion)==0:
					self._folder_name_exclusion.append('')
					
			except:
				self._folder_name_exclusion =['']
			
			#nom de dossier hidden
			try:
				self._folder_name_hidden = self.__ConfigSectionMap('directories')['hidden_name'].split(',')
			except:
				self._folder_name_hidden =''
			
			#option optimisation via tag xml refresh
			try:
				self._hint_use_refresh_tag = self.__ConfigSectionMap('directories')['hint_use_refresh_tag']
				if self._hint_use_refresh_tag=='1':
					self._hint_use_refresh_tag = True
				else:
					self._hint_use_refresh_tag = False
			except:
				self._hint_use_refresh_tag = False
			
			#option optimisation via os.stats
			try:
				self._hint_use_os_stat = self.__ConfigSectionMap('directories')['hint_use_os_stat']
				if self._hint_use_os_stat=='1':
					self._hint_use_os_stat = True
				else:
					self._hint_use_os_stat = False
			except:
				self._hint_use_os_stat = False
			
			#Dossier multi-émulateur
			try:
				self._folder_multi = self.__ConfigSectionMap('directories')['folder_multi']
			except:
				self._folder_multi =''
			
			
			#----- Section game ------------------------------------------------------
			#Exclusion de nom de fichiers
			try:
				self._game_name_exclusion = self.__ConfigSectionMap('game')['exclusion_name'].split(',')
			except:
				self._game_name_exclusion =''
			
			#nom de fichiers hidden
			try:
				self._game_name_hidden = self.__ConfigSectionMap('game')['hidden_name'].split(',')
			except:
				self._game_name_hidden =''
				
			#Exclusion d'extension de fichiers
			try:
				opt_excl_extension = self.__ConfigSectionMap('game')['exclusion_extension']
				opt_excl_extension = opt_excl_extension + ',' + opt_excl_extension.upper()
				self._game_extension_exclusion = opt_excl_extension.split(',')
			except:
				self._game_extension_exclusion =''
			
			#Mode de suppression game
			try:
				self._game_delete_option = self.__ConfigSectionMap('game')['mode_delete']
			except:
				self._game_delete_option =''
			
		
			#----- Section folder ----------------------------------------------------
			#FOLDERS DEFAULT, KO, TOP, LAST, BEST-------------------------------------
			self._folder_default_dir, self._folder_default_xml, self._folder_default_nb, self._folder_default_picture_mode, self._folder_default_picture = self.__load_config_folder('default')
			self._folder_ko_dir, self._folder_ko_xml, self._folder_ko_nb, self._folder_ko_picture_mode, self._folder_ko_picture = self.__load_config_folder('ko')
			self._folder_top_dir, self._folder_top_xml, self._folder_top_nb, self._folder_top_picture_mode, self._folder_top_picture = self.__load_config_folder('top')
			self._folder_last_dir, self._folder_last_xml, self._folder_last_nb, self._folder_last_picture_mode, self._folder_last_picture = self.__load_config_folder('last')
			self._folder_best_dir, self._folder_best_xml, self._folder_best_nb, self._folder_best_picture_mode, self._folder_best_picture = self.__load_config_folder('best')

			#GAME IMAGE PAR DEFAUT----------------------------------------------------
			#Image par défaut des jeux (non bloquant)
			try:
				self._default_game_picture = self.__ConfigSectionMap('game')['default_image']
				if not os.path.isfile(os.path.expanduser(self._folder_default_picture)):
					logger.warn(msg_local.get(('MSG_WARN_GLT_GAME_NOT_PICT_DEF',config.language)).format(self._default_game_picture))
					
					self._folder_default_picture =''
			except:
				logger.debug(msg_local.get(('MSG_DEBUG_GLT_FINDENTRY',config.language)).format('default_image','game',self._inifilename))
				
			#Mode de l'image par défaut des jeux (non bloquant)
			try:
				self._default_game_picture_mode = self.__ConfigSectionMap('game')['mode_image']
				self._default_game_picture_mode = self._default_game_picture_mode[0].upper()
			except:
				logger.debug(msg_local.get(('MSG_DEBUG_GLT_FINDENTRY',config.language)).format('mode_image','game',self._inifilename))
		

			#----- Section save ------------------------------------------------------
			#Option de sauvegarde origin
			try:
				self._option_save_origin = self._configParser.getboolean('save', 'origin')
			except:
				#logger.debug('Config.load_from_file : Section [save] or option origin= not found')
				logger.debug(msg_local.get(('MSG_DEBUG_GLT_FINDENTRY',config.language)).format('origin','save',self._inifilename))
				
			#Option de sauvegarde backup
			try:
				self._option_save_backup = self._configParser.getboolean('save', 'backup')
			except:
				#logger.debug('Config.load_from_file : Section [save] or option backup= not found')
				logger.debug(msg_local.get(('MSG_DEBUG_GLT_FINDENTRY',config.language)).format('backup','save',self._inifilename))


			#----- Section emulation_station -----------------------------------------
			#Configuration emulation station
			try:
				self._emulation_station_systems = self.__ConfigSectionMap('emulation_station')['es_systems']
			except:
				pass

			try:
				self._emulation_station_systems_usb = self.__ConfigSectionMap('emulation_station')['es_systems_sub']
			except:
				pass

			try:
				self._emulation_station_settings = self.__ConfigSectionMap('emulation_station')['es_settings']
			except:
				pass
				
			try:
				self._emulation_station_themes = self.__ConfigSectionMap('emulation_station')['es_themes']
			except:
				pass
			
			#----- Section config_themes -----------------------------------------
			try:
				self._theme_menu_file_configxml = self.__ConfigSectionMap('config_themes')['config_xml']
			except:
				pass
				
			try:
				self._theme_menu_sh_folder = self.__ConfigSectionMap('config_themes')['sh_folder']
			except:
				pass

			try:
				self._theme_sh_name = self.__ConfigSectionMap('config_themes')['sh_name']
			except:
				pass
			
			try:
				self._theme_sh_launch = self.__ConfigSectionMap('config_themes')['sh_launch']
			except:
				pass
					
			
			#----- Rules -------------------------------------------------------------
			#Règles de génération
			try:
				self._generation_rules = self.__ConfigSectionMap('rules')
			except:
				pass
				
		else:
			#logger.error('Can''t find '+self._inifilename)
			logger.error(msg_local.get(('MSG_ERROR_GLT_CONF_FILE_NOT_FOUND',config.language)).format(self._inifilename))
			sys.exit(1)



	def __load_config_folder(self, prefix):
		"""load all option for a folder config"""
		folder_dir=''
		folder_xml=''
		folder_nb=''
		folder_picture_mode=''
		folder_picture=''
		
		#Nom du répertoire dans le filesystem
		if prefix!='default':
			try:
				folder_dir = self.__ConfigSectionMap('folder')[prefix + '_name_directory']
			except:
				#logger.debug('Config.load_from_file : Section [folder] or option '+ prefix + '_name_directory= not found')
				logger.debug(msg_local.get(('MSG_DEBUG_GLT_FINDENTRY',config.language)).format(prefix + '_name_directory','folder',self._inifilename))
				
			#Nom du répertoire dans le gamelist.xml
			try:
				folder_xml = self.__ConfigSectionMap('folder')[prefix + '_name_xml']
				folder_xml = folder_xml.replace("&nbsp;"," ")
				if folder_xml=='' and folder_dir!='':	
					folder_xml = folder_dir
					#logger.debug('Config.load_from_file : no name in '+ prefix + '_name_xml, use '+ folder_dir +' as name in '+NOM_GAMELIST_XML)
					logger.debug(msg_local.get(('MSG_ERROR_GLT_NO_NAME_XML',config.language)).format(prefix + '_name_xml',folder_dir,self._inifilename))
					
			except:
				#logger.debug('Config.load_from_file : Section [folder] or option '+ prefix + '_name_xml= not found')
				logger.debug(msg_local.get(('MSG_DEBUG_GLT_FINDENTRY',config.language)).format(prefix + '_name_xml','folder',self._inifilename))
			if folder_xml=='': folder_xml=folder_dir
		
		if prefix!='default' and prefix!='ko':
			#Nb entrées
			try:
				folder_nb = self.__ConfigSectionMap('folder')[prefix + '_number']
			except:
				#logger.debug('Config.load_from_file : Section [folder] or option '+ prefix + '_number= not found')
				logger.debug(msg_local.get(('MSG_DEBUG_GLT_FINDENTRY',config.language)).format(prefix + '_number','folder',self._inifilename))
		
		#Mode de l'image 
		try:
			folder_picture_mode = self.__ConfigSectionMap('folder')[prefix + '_mode_image']
			folder_picture_mode = folder_picture_mode[0].upper()
		except:
			#logger.debug('Config.load_from_file : Section [folder] or option '+ prefix + '_mode_image= not found')
			logger.debug(msg_local.get(('MSG_DEBUG_GLT_FINDENTRY',config.language)).format(prefix + '_mode_image','folder',self._inifilename))
		
		#Image du dossier 
		try:
			folder_picture = self.__ConfigSectionMap('folder')[prefix + '_image']
			#os.path.expanduser => gestion du tild
			if not os.path.isfile(os.path.expanduser(folder_picture)):
				logger.warn('Config.load_from_file : '+ prefix + ' default picture not exist '+ folder_picture)
				folder_picture =''
		except:
			#logger.debug('Config.load_from_file : Section [folder] or option '+ prefix + '_image= not found')
			logger.debug(msg_local.get(('MSG_DEBUG_GLT_FINDENTRY',config.language)).format(prefix + '_image','folder',self._inifilename))
			
		#Vérification cohérence
		if folder_dir!='' and folder_picture=='':
			folder_dir==''
			#logger.debug('Config.load_from_file : '+ prefix +'default_image missing, defaut picture for this folder is disabled')
			logger.debug(msg_local.get(('MSG_ERROR_GLT_NO_DEF_PICT',config.language)).format(prefix,self._inifilename))
			
		#Retour des valeurs
		return folder_dir, folder_xml, folder_nb, folder_picture_mode, folder_picture


#INIT LOGGER--------------------------------------------------------------------
logger=Logger.logr

#MSG LOCALISATION---------------------------------------------------------------
config=Config()
