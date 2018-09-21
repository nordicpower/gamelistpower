#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                     - EMULATIONSTATION GAMELIST PATCH -                      #
#                            - VERSION CONSOLE -                               #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.09 20/09/2016-20/09/2018 #
#------------------------------------------------------------------------------#
#Création des entrées folder des nouveaux dossiers                             #
#Suppression des entrées folder inexistantes dans les dossiers                 #
#Gestion des déplacements des roms                                             #
#Gestion des images des roms                                                   #
#Création des entrées game des nouvelles roms + attribut hidden                #
#Gestion des dossiers TOP, LAST, BEST par hard link                            #
#------------------------------------------------------------------------------#

#IMPORT STD---------------------------------------------------------------------
import os.path
import sys
import time
import shutil
import argparse
from os.path import basename, splitext
from threading import Thread

#IMPORT NORDICPOWER--------------------------------------------------------------
from glplib import *
	
#CONSTANTS-----------------------------------------------------------------------
VERSION='0.9.09 BETA 20/09/2018'
SOURCE_NAME='NordicPower'
SEUIL_AFFICHAGE_CHECKPICTURES=1
SEUIL_SAUVEGARDE_BIGROM=50 #20

NOM_GAMELIST='gamelist'
NOM_GAMELIST_XML       =NOM_GAMELIST+'.xml'
NOM_GAMELIST_XML_NEW   =NOM_GAMELIST+'.new.xml'
NOM_GAMELIST_XML_SAV   =NOM_GAMELIST+'.sav.xml'
NOM_GAMELIST_XML_CACHE =NOM_GAMELIST+'.cache.xml'
NOM_GAMELIST_XML_ORIGIN=NOM_GAMELIST+'.origin.xml'

#CONSTANTS ARGUMENTS LANCEMENT---------------------------------------------------
ARG_MODE='mode'
ARG_MODE_PATCH_FULL='update'
ARG_MODE_PATCH_FORCE='updateforce'
ARG_MODE_CORRECT_ONLY='correct'
ARG_MODE_TOP_ONLY='top'
ARG_MODE_STATS_ONLY='stats'
ARG_MODE_NOIMAGE_ONLY='noimage'
ARG_MODE_GENERATE_SH='generate_sh'
ARG_MODE_GENERATE_ROMCPY='generate_romcpy'

ARG_LOG='log'
ARG_LOG_DEBUG='debug'
ARG_LOG_INFO='info'
ARG_LOG_ERROR='error'

#MSG LOCALISATION----------------------------------------------------------------
config=Config()

msg_local={
('MSG_ERROR_GLP_EXCEPTION','FR'):u'{} : {}',
('MSG_ERROR_GLP_EXCEPTION','EN'):u'{} : {}',
('MSG_INFO_GLP_START_BESTGAMES','FR'):u'MEILLEURS JEUX',
('MSG_INFO_GLP_START_BESTGAMES','EN'):u'BEST GAMES',
('MSG_INFO_GLP_START_TOPGAMES','FR'):u'JEUX LES + JOUES',
('MSG_INFO_GLP_START_TOPGAMES','EN'):u'TOP GAMES',
('MSG_INFO_GLP_START_LASTGAMES','FR'):u'DERNIERS JEUX JOUES',
('MSG_INFO_GLP_START_LASTGAMES','EN'):u'LAST GAMES',
('MSG_INFO_GLP_START_CHECKPICTURES','FR'):u'VERIFICATION IMAGES DES ROMS',
('MSG_INFO_GLP_START_CHECKPICTURES','EN'):u'CHECK ROMS PICTURES',
('MSG_DEBUG_GLP_UPD_GAME_SRC','FR'):u'{} : Mise \u00E0 jour du jeu {} avec cette source {}',
('MSG_DEBUG_GLP_UPD_GAME_SRC','EN'):u'{} : update game {} with this source {}',
('MSG_DEBUG_GLP_GAMEXML_NOT_FOUND','FR'):u'{} : Jeu {} non trouv\u00E9 !',
('MSG_DEBUG_GLP_GAMEXML_NOT_FOUND','EN'):u'{} : game {} not found !',
('MSG_DEBUG_GLP_PATH_NOT_EXIST','FR'):u'{} : Pas de fichier trouv\u00E9 {} !',
('MSG_DEBUG_GLP_PATH_NOT_EXIST','EN'):u'{} : No file found {}!',
('MSG_DEBUG_GLP_FILE_EXCL_FOUND','FR'):u'{} : Fichier {} dans la liste exclusion',
('MSG_DEBUG_GLP_FILE_EXCL_FOUND','EN'):u'{} : File {} in exclusion list',
('MSG_DEBUG_GLP_ASS_FOLDER_TYPE','FR'):u'{} : Association du dossier {} avec l\x27image {}',
('MSG_DEBUG_GLP_ASS_FOLDER_TYPE','EN'):u'{} : Associed this folder {} with {} image',
('MSG_DEBUG_GLP_FOLDER_NO_IMAGE','FR'):u'{} : Dossier {} sans image',
('MSG_DEBUG_GLP_FOLDER_NO_IMAGE','EN'):u'{} : Found folder {} without image',
('MSG_DEBUG_GLP_FOLDER_FOUND_IMAGE','FR'):u'{} : Dossier {} avec image {}',
('MSG_DEBUG_GLP_FOLDER_FOUND_IMAGE','EN'):u'{} : Found folder {} with image {}',
('MSG_DEBUG_GLP_FOLDER_REFRESH_NAME','FR'):u'{} : MAJ Dossier {} avec nom {}',
('MSG_DEBUG_GLP_FOLDER_REFRESH_NAME','EN'):u'{} : Refresh folder {} with name {}',
('MSG_INFO_GLP_FOLDER_UPD_DEL_IMAGE','FR'):u'{} : MAJ Dossier {} suppression image',
('MSG_INFO_GLP_FOLDER_UPD_DEL_IMAGE','EN'):u'{} : Refresh folder {} delete image',
('MSG_INFO_GLP_FOLDER_UPD_UPD_IMAGE','FR'):u'{} : MAJ Dossier {} avec image {}',
('MSG_INFO_GLP_FOLDER_UPD_UPD_IMAGE','EN'):u'{} : Refresh folder {} with this image {}',
('MSG_DEBUG_GLP_FOLDER_UPD_ALREADY_IMAGE','FR'):u'{} : MAJ Dossier {} d\u00E9j\u00E0 \u00E0 jour',
('MSG_DEBUG_GLP_FOLDER_UPD_ALREADY_IMAGE','EN'):u'{} : Folder {} is up-to-date',
('MSG_INFO_GLP_FOLDER_ADD','FR'):u'{} : Ajout du dossier {} avec image {}',
('MSG_INFO_GLP_FOLDER_ADD','EN'):u'{} : Add New Folder Entry {} with this image {}',
('MSG_DEBUG_GLP_FOLDER_NOSUB_FOLDER','FR'):u'Pas de sous dossier',
('MSG_DEBUG_GLP_FOLDER_NOSUB_FOLDER','EN'):u'Skip no sub directory',
('MSG_INFO_GLP_FOLDER_DIR_NOT_FOUND','FR'):u'Dossier {} non trouv\u00E9, suppression de l\x27entr\u00E9e XML ',
('MSG_INFO_GLP_FOLDER_DIR_NOT_FOUND','EN'):u'Folder {} not found, delete it',
('MSG_DEBUG_GLP_FUNCTION_START','FR'):u'{} : D\u00E9but',
('MSG_DEBUG_GLP_FUNCTION_START','EN'):u'{} : Start',
('MSG_DEBUG_GLP_FUNCTION_REFRESH','FR'):u'{} : Mise \u00E0 jour {}',
('MSG_DEBUG_GLP_FUNCTION_REFRESH','EN'):u'{} : Update {}',
('MSG_DEBUG_GLP_FUNCTION_NOREFRESH','FR'):u'{} : Pas besoin mise \u00E0 jour {}',
('MSG_DEBUG_GLP_FUNCTION_NOREFRESH','EN'):u'{} : No need to update {}',
('MSG_INFO_GLP_CURRENT_FOLDER','FR'):u'DOSSIER {}',
('MSG_INFO_GLP_CURRENT_FOLDER','EN'):u'FOLDER {}',
('MSG_INFO_GLP_PRG_SAVE','FR'):u'Sauvegarde de {}',
('MSG_INFO_GLP_PRG_SAVE','EN'):u'Save {}',
('MSG_INFO_GLP_PRG_SAVE_BIGROM','FR'):u'Sauvegarde de {}',
('MSG_INFO_GLP_PRG_SAVE_BIGROM','EN'):u'Save {}',
('MSG_DEBUG_GLP_PRG_INIT','FR'):u'Initialisation mise \u00E0 jour',
('MSG_DEBUG_GLP_PRG_INIT','EN'):u'Preparing',
('MSG_DEBUG_GLP_PRG_START','FR'):u'D\u00E9but de la mise \u00E0 jour',
('MSG_DEBUG_GLP_PRG_START','EN'):u'Start Updating',
('MSG_INFO_GLP_PRG_END','FR'):u'Fin',
('MSG_INFO_GLP_PRG_END','EN'):u'End',
('MSG_DEBUG_GLP_FOLDER_SUB','FR'):u'{} : Sous-Dossier : {}',
('MSG_DEBUG_GLP_FOLDER_SUB','EN'):u'{} : Sub Directory : {}',
('MSG_INFO_GLP_GAME_ADD','FR'):u'Ajout d\x27un nouveau jeu {}',
('MSG_INFO_GLP_GAME_ADD','EN'):u'Add New Game Entry : {}',
('MSG_INFO_GLP_GAME_UPD_IMAGE','FR'):u'MAJ Jeu {} avec l\x27image {}',
('MSG_INFO_GLP_GAME_UPD_IMAGE','EN'):u'Update Game Entry {} with this image {}',
('MSG_INFO_GLP_GAME_UPD_IMAGE_DEF','FR'):u'MAJ Jeu [{}] avec image par d\u00E9faut',
('MSG_INFO_GLP_GAME_UPD_IMAGE_DEF','EN'):u'Update Game Entry [{}] with default image',
('MSG_INFO_GLP_GAME_DEL_IMAGE_DEF','FR'):u'MAJ Jeu {} avec suppression image par d\u00E9faut',
('MSG_INFO_GLP_GAME_DEL_IMAGE_DEF','EN'):u'Update Game Entry {} delete default image',
('MSG_INFO_GLP_GAME_UPD_IMAGE_NONE','FR'):u'{} : Pas image pour le jeu : {}',
('MSG_INFO_GLP_GAME_UPD_IMAGE_NONE','EN'):u'{} : No image for {}',
('MSG_INFO_GLP_GAME_UPD_HIDDEN','FR'):u'{} : MAJ Attribut Hidden : {}',
('MSG_INFO_GLP_GAME_UPD_HIDDEN','EN'):u'{} : Set Hidden value {}',
('MSG_DEBUG_GLP_GAME_NOT_FOUND','FR'):u'{} : Aucun jeu',
('MSG_DEBUG_GLP_GAME_NOT_FOUND','EN'):u'{} : No Game Found',
('MSG_INFO_GLP_GAME_IMAGE_NOT_FOUND','FR'):u'Image du jeu {} non trouv\u00E9e : {}',
('MSG_INFO_GLP_GAME_IMAGE_NOT_FOUND','EN'):u'Game {} picture {} not found',
('MSG_INFO_GLP_GAME_NO_IMAGE','FR'):u'Jeu sans image : {}',
('MSG_INFO_GLP_GAME_NO_IMAGE','EN'):u'No image for {}',
('MSG_INFO_GLP_GAME_DEL','FR'):u'Suppression du jeu {}',
('MSG_INFO_GLP_GAME_DEL','EN'):u'Delete Game {}',
('MSG_INFO_GLP_GAME_WITHOUT_ROM','FR'):u'Jeu {} sans rom {}',
('MSG_INFO_GLP_GAME_WITHOUT_ROM','EN'):u'Game {} without rom {}',
('MSG_INFO_GLP_GAME_FOUND_ROM','FR'):u'Jeu {} la rom trouv\u00E9e dans {}',
('MSG_INFO_GLP_GAME_FOUND_ROM','EN'):u'Game {} found this rom in {}',
('MSG_DEBUG_GLP_GAME_FOUND','FR'):u'Jeu : Rom [{}] Nom [{}] => {}',
('MSG_DEBUG_GLP_GAME_FOUND','EN'):u'Game : Rom [{}] Name [{}] => {}',
('MSG_INFO_GLP_GAME_DOUBLE','FR'):u'Suppression Jeu en doublon : Rom [{}] Nom [{}]',
('MSG_INFO_GLP_GAME_DOUBLE','EN'):u'Delete duplicate entrie : Rom [{}] Name [{}]',
('MSG_DEBUG_GLP_FOLDER_HASH_REFRESH','FR'):u'Calcul du hash {}',
('MSG_DEBUG_GLP_FOLDER_HASH_REFRESH','EN'):u'refresh hash {}',
('MSG_DEBUG_GLP_FOLDER_HASH_NOCHANGE','FR'):u'Pas de changement de hash d\u00E9tect\u00E9 : {}',
('MSG_DEBUG_GLP_FOLDER_HASH_NOCHANGE','EN'):u'No hash changed detected {}',
('MSG_INFO_GLP_GAMELIST_ERROR','FR'):u'Attention, {} gamelist.xml en erreur ! V\u00E9rifier les messages pr\u00E9c\u00E9dents',
('MSG_INFO_GLP_GAMELIST_ERROR','EN'):u'Warning, {} gamelist.xml in error ! Check log previous messages',
('MSG_INFO_GLP_GAMELIST_ERROR_DET','FR'):u'- {}',
('MSG_INFO_GLP_GAMELIST_ERROR_DET','EN'):u'- {}',
('MSG_CRITICAL_GLP_ESSYSTEM_LOAD_ERROR','FR'):u'Erreur de chargement du fichier es_systems.cfg',
('MSG_CRITICAL_GLP_ESSYSTEM_LOAD_ERROR','EN'):u'Error while loading es_systems.cfg',
('MSG_DEBUG_GLP_ESSYSTEM_CONFIG_PLATEFORM','FR'):u'Param\u00E9trage es_systems.cfg command={},extension={}',
('MSG_DEBUG_GLP_ESSYSTEM_CONFIG_PLATEFORM','EN'):u'Parameters es_systems.cfg command={},extension={}',
('MSG_DEBUG_GLP_ESSYSTEM_UNKNOW_PLATEFORM','FR'):u'Pas d\x27information es_systems.cfg',
('MSG_DEBUG_GLP_ESSYSTEM_UNKNOW_PLATEFORM','EN'):u'No information in es_systems.cfg',
('MSG_CRITICAL_GLP_RULE_NOT_EXIST','FR'):u'{} : Pas de fichier trouv\u00E9 {} !',
('MSG_CRITICAL_GLP_RULE_NOT_EXIST','EN'):u'{} : No file found {}!',
('MSG_DEBUG_GLP_LAUNCH_ARG_MODE','FR'):u'Mode de lancement {}',
('MSG_DEBUG_GLP_LAUNCH_ARG_MODE','EN'):u'Run with mode {}'
}
msg_local_arg={
('MSG_ARG_PRG_DESCRIPTION','FR'):u'GameListPatch permet de corriger et d\x27ajouter des fonctionnalit\u00E9s dans le fichier gamelist.xml',
('MSG_ARG_PRG_DESCRIPTION','EN'):u'GameListPatch permits to patch and add enhanced functions in gamelist.xml file',
('MSG_ARG_MODE_HELP','FR'):u'mode de traitement: update pour lancer les options correct et top,updateforce idem update sans tenir compte optimisation refresh, correct pour corriger les fichiers gamelist.xml vs dossiers roms, top pour calculer les dossiers top et last, stats pour le tableau final uniquement, noimage pour lister rom sans image et generate pour la g\u00E9n\u00E9ration de lanceurs dans le dossier multi',
('MSG_ARG_MODE_HELP','EN'):u'run mode : update for launch correct et top options, updateforce same as update but ignore all refresh tips, correct to correct gamelist.xml vs roms folders, top to refresh top and last folders, stats for final report, noimage to get all roms without picture and generate to add or refresh game launcher in folder multi',
('MSG_ARG_LOG_HELP','FR'):u'niveau de log',
('MSG_ARG_LOG_HELP','EN'):u'log level'
}


#CLASS-GAME STATS--------------------------------------------------------------
class GameStats(Game):
	def __init__(self,**kwargs):
		self._plateform=''
		Game.__init__(self, **kwargs)

		if kwargs is not None:
			#mise à jour paramètre(s) nommé(s)
			self.__dict__.update(kwargs)

	def __repr__(self):
		return repr((self.plateform, self.name, self.path))

	#property-------------------------	
	@property
	def plateform(self):return self._plateform
		
		
#CLASS-GAMES STATS--------------------------------------------------------------
class GamesStats():
	
	def __init__(self,v_config,**kwargs):
		self._config = v_config
		self._list_roms = []		
		self._list_plateforms = []
				
		if kwargs is not None:
			#mise à jour paramètre(s) nommé(s)
			self.__dict__.update(kwargs)
			
	#add public functions-------------------------	
	def add_plateform(self,v_plateform):
		self._list_plateforms.append(get_last_folder_plateform(v_plateform))
		
	def add_rom(self,v_plateform,v_game):
		game_Stats = GameStats(plateform=get_last_folder_plateform(v_plateform))
		game_Stats.copy_from_game(v_game)
		game_Stats.path = v_game.path
		self._list_roms.append(game_Stats)

	#Count public functions------------------------
	def total_plateforms(self):
		return len(self._list_plateforms)
	
	def total_roms(self):
		return len(self._list_roms)
	
	def total_uniq_roms(self):
		return len(self.list_uniq_roms())
		
	def total_roms_ko(self):
		return len(self.list_all_roms_ko())
		
	def total_roms_without_picture(self):
		return len(self.list_all_roms_without_picture())
	
	def total_roms_played(self):
		return len ([gl for gl in self.list_all_roms() 
		if self._config.top_folder_name_dir not in gl.path and 
		self._config.last_folder_name_dir not in gl.path and 
		self._config.best_folder_name_dir not in gl.path and 
		gl.playcount<>'' and gl.playcount<>'0'])
					
	#list public functions-------------------------	
	def list_all_plateforms(self):
		return sorted(self._list_plateforms)

	def list_all_roms(self):
		return sorted(self._list_roms,key=attrgetter('plateform','name'),reverse=False)

	def list_all_roms_on_plateform(self,v_plateform):
		local_list = [gl for gl in self.list_all_roms() if gl.plateform == v_plateform]
		return sorted(local_list,key=attrgetter('name'),reverse=False)

	def list_all_roms_on_plateform_in_path(self,v_plateform, v_path):
		local_list = [gl for gl in self.list_all_roms() if gl.plateform == v_plateform and v_path in gl.path]
		return sorted(local_list,key=attrgetter('name'),reverse=False)
	
	def list_all_roms_in_path(self, v_path):
		local_list = [gl for gl in self.list_all_roms() if v_path in gl.path]
		return sorted(local_list,key=attrgetter('name'),reverse=False)
	
	def list_all_roms_ko(self):
		return self.list_all_roms_in_path(self._config.ko_folder_name_dir)
		
	def list_all_roms_on_plateform_ko(self,v_plateform):
		return self.list_all_roms_on_plateform_in_path(v_plateform,self._config.ko_folder_name_dir)
		
	def list_uniq_roms(self):
		"""Exclusion de TOP, BEST et LAST"""
		local_list = [gl for gl in self.list_all_roms() if 
		self._config.last_folder_name_dir not in gl.path and 
		self._config.top_folder_name_dir not in gl.path and 
		self._config.best_folder_name_dir not in gl.path]
		return sorted(local_list,key=attrgetter('plateform','name'),reverse=False)
	
	def list_uniq_roms_on_plateform(self,v_plateform):
		"""Exclusion de TOP, BEST et LAST"""
		local_list = [gl for gl in self.list_all_roms() if 
		self._config.last_folder_name_dir not in gl.path and 
		self._config.top_folder_name_dir not in gl.path and 
		self._config.best_folder_name_dir not in gl.path and 
		gl.plateform == v_plateform]
		return sorted(local_list,key=attrgetter('name'),reverse=False)
		
	def list_all_roms_without_picture(self):
		#BUG : ne fonctionne plus avec config ~
		local_list = [gl for gl in self.list_all_roms() if gl.image =='' or gl.image == self._config.default_game_picture]
		return sorted(local_list,key=attrgetter('name'),reverse=False)
	
	def list_all_roms_on_plateform_without_picture(self,v_plateform):
		#BUG : ne fonctionne plus avec config ~
		local_list = [gl for gl in self.list_all_roms() if gl.image =='' or gl.image == self._config.default_game_picture and gl.plateform == v_plateform]
		return sorted(local_list,key=attrgetter('name'),reverse=False)
		
	def list_top_played(self):
		games_XML = [gl for gl in self.list_all_roms() 
		if self._config.top_folder_name_dir not in gl.path and 
		self._config.last_folder_name_dir not in gl.path and 
		self._config.best_folder_name_dir not in gl.path and gl.playcount<>'']
		
		nb_top = int(self._config.top_folder_nb)
		if len(games_XML) < int(nb_top): nb_top = len(games_XML)
		return sorted(games_XML,key=key_top_game,reverse=True)[0:nb_top]	
	
	def list_last_played(self):
		games_XML = [gl for gl in self.list_all_roms() 
		if self._config.top_folder_name_dir not in gl.path and 
		self._config.last_folder_name_dir not in gl.path and 
		self._config.best_folder_name_dir not in gl.path and gl.lastplayed<>'']
		
		nb_last = int(self._config.last_folder_nb)
		if len(games_XML) < int(nb_last): nb_last = len(games_XML)
		return sorted(games_XML,key=attrgetter('lastplayed','playcount','name'),reverse=True)[0:nb_last]
			
	
	def _format_left(self,texte,total_car_max):
		if len(texte)>total_car_max: return texte[0:total_car_max]
		nb_spaces = total_car_max - len(texte)
		return texte + ' '*nb_spaces
	
	def _format_right(self,texte,total_car_max):
		nb_spaces = total_car_max - len(texte)
		return ' '*nb_spaces + texte
		
	def log_stats(self):
				
		msg_stats={
		('MSG_STATS_MAIN','FR'):u'STATISTIQUES',
		('MSG_STATS_MAIN','EN'):u'STATS',
		('MSG_STATS_BORDER1','FR'):u'+------------------+---------+--------+-----------+-------------------+',
		('MSG_STATS_TITLE1','FR'): '| Plateforme       |  TOTAL  | UNIQUE |  ROMS_KO  |       SANS IMAGE  |',
		('MSG_STATS_TITLE1','EN'): '| Plateform Name   |  TOTAL  |  UNIQ  |  ROMS_KO  |  WITHOUT PICTURE  |',
		('MSG_STATS_BORDER1','EN'):u'+------------------+---------+--------+-----------+-------------------+',
		('MSG_STATS_BORDER2','FR'):u'+------------------+--------------------------------------------+-----+',
		('MSG_STATS_TOT_PLA','FR'):u'| LES + JOUES      |                      TOTAL ROMS DISTINCTES :{} |',
		('MSG_STATS_TOT_PLA','EN'):u'| TOP PLAYED       |                      TOTAL DISTINCT PLAYED :{} |',
		('MSG_STATS_BORDER2','EN'):u'+------------------+--------------------------------------------+-----+',
		('MSG_STATS_BORDER3','FR'):u'+------------------+---------------------------------------+----------+',
		('MSG_STATS_LAS_PLA','FR'):u'| DERNIERS JOUES   |                                                  |',
		('MSG_STATS_LAS_PLA','EN'):u'| LAST PLAYED      |                                                  |',
		('MSG_STATS_BORDER3','EN'):u'+------------------+---------------------------------------+----------+'
		}
		
		logger.info(msg_stats.get(('MSG_STATS_MAIN',config.language)))
		logger.info(msg_stats.get(('MSG_STATS_BORDER1',config.language)))
		logger.info(msg_stats.get(('MSG_STATS_TITLE1',config.language)))
		logger.info(msg_stats.get(('MSG_STATS_BORDER1',config.language)))
		for plateform_name in self.list_all_plateforms():
			logger.info('| '+self._format_left(plateform_name,17) + '|' + 
			self._format_right(str(len(self.list_all_roms_on_plateform(plateform_name))),8) + ' |'+
			self._format_right(str(len(self.list_uniq_roms_on_plateform(plateform_name))),7) + ' |'+
			self._format_right(str(len(self.list_all_roms_on_plateform_ko(plateform_name))),10) + ' |'+
			self._format_right(str(len(self.list_all_roms_on_plateform_without_picture(plateform_name))),18) + ' |'
			)
		logger.info(msg_stats.get(('MSG_STATS_BORDER1',config.language)))
		logger.info('| TOTAL '+ self._format_right(str(self.total_plateforms()),10) + ' |' +
		self._format_right(str(self.total_roms()),8)+ ' |' +
		self._format_right(str(self.total_uniq_roms()),7)+ ' |'+
		self._format_right(str(self.total_roms_ko()),10)+ ' |'+
		self._format_right(str(self.total_roms_without_picture()),18)+ ' |'
		)
		logger.info(msg_stats.get(('MSG_STATS_BORDER1',config.language)))
		#logger.info('| TOP PLAYED       |                      TOTAL DISTINCT PLAYED :'+self._format_right(str(self.total_roms_played()),4)+' |')
		logger.info(msg_stats.get(('MSG_STATS_TOT_PLA',config.language)).format(self._format_right(str(self.total_roms_played()),4)))
		logger.info(msg_stats.get(('MSG_STATS_BORDER2',config.language)))
		for game_top in self.list_top_played():
			logger.info('| '+ self._format_left(game_top.plateform,17) + '|' + self._format_left(game_top.name,44)+'|'+ self._format_right(game_top.playcount,4)+' |')
		logger.info(msg_stats.get(('MSG_STATS_BORDER2',config.language)))
		#logger.info('| LAST PLAYED      |                                                  |')
		logger.info(msg_stats.get(('MSG_STATS_LAS_PLA',config.language)))
		logger.info(msg_stats.get(('MSG_STATS_BORDER3',config.language)))
		for game_last in self.list_last_played():
			#logger.info('| '+ self._format_left(game_last.plateform,17) + '|' + self._format_left(game_last.name,50)+'|')
			last_date=time.strptime(game_last.lastplayed,'%Y%m%dT%H%M%S')
			if config.language=='FR':
				last_date_pr=time.strftime('%d/%m/%Y',last_date)
			else:
				last_date_pr=time.strftime('%m/%d/%Y',last_date)
			logger.info('| '+ self._format_left(game_last.plateform,17) + '|' + self._format_left(game_last.name,39)+'|'+last_date_pr+'|')
		logger.info(msg_stats.get(('MSG_STATS_BORDER3',config.language)))
		
	
	def log_roms_without_picture(self):
		
		msg_stats={
		('MSG_STATS_MAIN','FR'):u'ROMS SANS IMAGE',
		('MSG_STATS_MAIN','EN'):u'ROMS WITHOUT PICTURE',
		('MSG_STATS_BORDER1','FR'):u'+------------+--------------------------+-----------------------------+',
		('MSG_STATS_TITLE1','FR'): '| Plateforme | NOM                      | CHEMIN                      |',
		('MSG_STATS_TITLE1','EN'): '| Plateform  | NAME                     | PATH                        |',
		('MSG_STATS_BORDER1','EN'):u'+------------+--------------------------+-----------------------------+'
		}
		
		logger.info(msg_stats.get(('MSG_STATS_MAIN',config.language)))
		logger.info(msg_stats.get(('MSG_STATS_BORDER1',config.language)))
		logger.info(msg_stats.get(('MSG_STATS_TITLE1',config.language)))
		logger.info(msg_stats.get(('MSG_STATS_BORDER1',config.language)))
		for game in self.list_all_roms_without_picture():
			logger.info('| '+self._format_left(game.plateform,11) + '|' + self._format_left(game.name,26) + '|' + self._format_left(game.path,29) + '|')
		logger.info(msg_stats.get(('MSG_STATS_BORDER1',config.language)))


#Class Patchs---------------------------------------------------------------------------
class GameListPatcher(Thread,ObjectWithEvents):
	"""All Patches for Gamelist.xml"""
	
	#Indicateur de fin pour le Thread
	running=False
	#Event, récupération du répertoire en cours
	GameListDirectory_Event=''
	
	def __init__(self,v_config,v_affichage,v_mode):
		Thread.__init__(self)
		self._config = v_config
		self._affichage = v_affichage
		self._mode = v_mode
		self._gamesStats=GamesStats(v_config)
		self._folders_Hash=Folders_Hash(NOM_GAMELIST+'.hash',v_config)
		self._local_image_folder='images'
		self.running = False
	
	@property
	def gamesStats(self):return self._gamesStats
		
	
	#Event, récupération du répertoire en cours
	def __str__(self):
		return self.GameListDirectory_Event

	#---------------------------------------------------------------------------------------------------
	
	def Patch_Game_Doublons(self,GameListDirectory,gamesList):
		"""Suppression des doublons"""
		logger.debug(msg_local.get(('MSG_DEBUG_GLP_FUNCTION_START',config.language)).format('Patch_Game_Doublons'))
		games_XML = gamesList.get_games()
		
		#Recherche de doublons
		for pos_orig in xrange(0,len(games_XML)):
			if not games_XML[pos_orig].specific=='DOUBLONS':
				for pos_search in xrange(pos_orig+1,len(games_XML)):
					if games_XML[pos_orig].path == games_XML[pos_search].path:
						games_XML[pos_search].specific='DOUBLONS'
						
		#Purge doublons
		for game_XML in games_XML:
			if game_XML.specific=='DOUBLONS':
				logger.info(msg_local.get(('MSG_INFO_GLP_GAME_DOUBLE',config.language)).format(game_XML.path,game_XML.name))
				gamesList.delete_game_with_glp_id(game_XML.internal_glp_id)
	
	#---------------------------------------------------------------------------------------------------
		
	def Patch_Best_Games(self,GameListDirectory,gamesList,es_config_extension):
		"""Gestion des folders BEST afin de recopier les informations entre le noeud game d'orgine et celui dans best"""
		
		pos=1
		#logger.info('BEST GAMES')
		logger.debug(msg_local.get(('MSG_DEBUG_GLP_FUNCTION_START',config.language)).format('Patch_Best_Games'))
		logger.info(msg_local.get(('MSG_INFO_GLP_START_BESTGAMES',config.language)))
		
		for game_best in gamesList.get_games_in_folder_sorted_by_name(self._config.best_folder_name_dir):
			logger.info(gamesList.last_name(pos,game_best.name))
			#si existance origine, mise à jour
			try:
				game_origin = gamesList.search_game_by_path ('.'+ os.sep + game_best.get_filename_rom())
				game_best.copy_from_game(game_origin)
				gamesList.update_game(game_best)
				
				#logger.debug('Patch_Best_Games : update game ' + game_best.path + ' with this source ' + game_origin.path)
				logger.debug(msg_local.get(('MSG_DEBUG_GLP_UPD_GAME_SRC',config.language)).format('Patch_Best_Games',game_best.path,game_origin.path))
			except MyError:
				#logger.debug('Patch_Best_Games : game orgin for ' + game_best.get_filename_rom() + ' not found')
				logger.debug(msg_local.get(('MSG_DEBUG_GLP_GAMEXML_NOT_FOUND',config.language)).format('Patch_Best_Games',game_best.get_filename_rom()))
			pos+=1
	
	#---------------------------------------------------------------------------------------------------
		
	def Patch_Top_Games(self,GameListDirectory,gamesList,es_config_extension):
		"""Gestion des folders TOP basés sur l'attribut playcount"""
		
		#Gestion du nouveau top
		pos=1
		#logger.info('TOP GAMES')
		logger.debug(msg_local.get(('MSG_DEBUG_GLP_FUNCTION_START',config.language)).format('Patch_Top_Games'))
		logger.info(msg_local.get(('MSG_INFO_GLP_START_TOPGAMES',config.language)))
		
		#Test sur le refresh : si refresh = 'no' et que le dossier TOP est pas vide
		if gamesList.refresh_folders=='no' and self._config.hint_use_refresh_tag==True:
			game_files = list_sub_files(os.path.join(GameListDirectory,self._config.top_folder_name_dir),self._config.folder_name_exclusion,self._config.game_name_exclusion,self._config.images_extension + self._config.game_extension_exclusion,es_config_extension)
			if len(game_files)>0:
				#Pas besoin, simple listing
				logger.debug(msg_local.get(('MSG_DEBUG_GLP_FUNCTION_NOREFRESH',config.language)).format('Patch_Top_Games','TOP'))
				for game_newtop in gamesList.get_top_games(self._config.top_folder_nb,[self._config.top_folder_name_dir,self._config.last_folder_name_dir,self._config.ko_folder_name_dir,self._config.best_folder_name_dir]):
					logger.info(gamesList.top_name_console(pos,game_newtop.name,game_newtop.playcount))
					pos+=1
				return
					
		#Mise à jour du Top
		logger.debug(msg_local.get(('MSG_DEBUG_GLP_FUNCTION_REFRESH',config.language)).format('Patch_Top_Games','TOP'))
		for game_newtop in gamesList.get_top_games(self._config.top_folder_nb,[self._config.top_folder_name_dir,self._config.last_folder_name_dir,self._config.ko_folder_name_dir,self._config.best_folder_name_dir]):
			game_found=False
			logger.info(gamesList.top_name_console(pos,game_newtop.name,game_newtop.playcount))
			#Recherche existance ancien top		
			for game_lasttop in gamesList.get_games_in_folder(self._config.top_folder_name_dir):
				if game_lasttop == game_newtop:
					game_lasttop.specific='TOP'
					game_lasttop.name = gamesList.top_name(pos,game_newtop.name)
					gamesList.update_game(game_lasttop)
					game_found=True
					break
			if not game_found:
				oldpath=os.path.join(GameListDirectory,os.path.expanduser(get_path_without_current(game_newtop.path)))
				newpath=os.path.join(GameListDirectory,self._config.top_folder_name_dir,game_newtop.get_filename_rom())
				if os.path.isfile(oldpath):
					if not os.path.isfile(newpath):
						if os.name=='posix':
							#création hardlink sous linux
							os.link(oldpath,newpath)
						else:
							shutil.copyfile(oldpath,newpath)
						
					game_newtop.path = '.' + os.sep + self._config.top_folder_name_dir + os.sep + game_newtop.get_filename_rom()
					game_newtop.specific='TOP'
					game_newtop.name = gamesList.top_name(pos,game_newtop.name)
					gamesList.add_game(game_newtop)
				else:
					#logger.debug('Patch_Top_Games : no file in source '+oldpath + ' for new top')
					logger.debug(msg_local.get(('MSG_DEBUG_GLP_PATH_NOT_EXIST',config.language)).format('Patch_Top_Games',oldpath))
			pos+=1
			
		#Purge des anciens entrées TOP et suppression attribut specific
		for game_lasttop in gamesList.get_games_in_folder(self._config.top_folder_name_dir):
			if game_lasttop.specific=='TOP':
				game_lasttop.specific=''
				gamesList.update_game(game_lasttop)
			else:
				#test des exclusions pour conserver les ROMs (cas de neogeo)
				if is_not_exclusion_file('.' + os.sep + self._config.top_folder_name_dir,game_lasttop.get_filename_rom(),self._config.game_name_exclusion,self._config.images_extension + self._config.game_extension_exclusion):
					gamesList.delete_game(game_lasttop)
					if os.path.isfile(os.path.join(GameListDirectory,os.path.expanduser(get_path_without_current(game_lasttop.path)))):
						os.remove(os.path.join(GameListDirectory,get_path_without_current(game_lasttop.path)))
					else:
						#logger.debug('Patch_Top_Games : no file to delete ('+game_lasttop.path+')')
						logger.debug(msg_local.get(('MSG_DEBUG_GLP_PATH_NOT_EXIST',config.language)).format('Patch_Top_Games',game_lasttop.path))
				else:
					#logger.debug('Patch_Top_Games : exclusion file ('+game_lasttop.get_filename_rom()+')')
					logger.debug(msg_local.get(('MSG_DEBUG_GLP_FILE_EXCL_FOUND',config.language)).format('Patch_Top_Games',game_lasttop.get_filename_rom()))
	
	
	#---------------------------------------------------------------------------------------------------
	def Patch_Last_Games(self,GameListDirectory,gamesList,es_config_extension):
		"""Gestion des folders LAST basés sur l'attribut lastplayed"""
		
		#Gestion du nouveau LAST
		pos=1
		#logger.info('LAST GAMES')
		logger.debug(msg_local.get(('MSG_DEBUG_GLP_FUNCTION_START',config.language)).format('Patch_Last_Games'))
		logger.info(msg_local.get(('MSG_INFO_GLP_START_LASTGAMES',config.language)))
		
		#Test sur le refresh : si refresh = 'no' et que le dossier LAST est pas vide
		if gamesList.refresh_folders=='no' and self._config.hint_use_refresh_tag==True:
			game_files = list_sub_files(os.path.join(GameListDirectory,self._config.last_folder_name_dir),self._config.folder_name_exclusion,self._config.game_name_exclusion,self._config.images_extension + self._config.game_extension_exclusion,es_config_extension)
			if len(game_files)>0:
				#Pas besoin, simple listing
				logger.debug(msg_local.get(('MSG_DEBUG_GLP_FUNCTION_NOREFRESH',config.language)).format('Patch_Last_Games','LAST'))
				for game_newlast in gamesList.get_last_games(self._config.last_folder_nb,[self._config.top_folder_name_dir,self._config.last_folder_name_dir,self._config.ko_folder_name_dir,self._config.best_folder_name_dir]):
					logger.info(gamesList.last_name_console(pos,game_newlast.name,game_newlast.lastplayed))
					pos+=1
				return
		
		#Mise à jour du LAST
		logger.debug(msg_local.get(('MSG_DEBUG_GLP_FUNCTION_REFRESH',config.language)).format('Patch_Last_Games','LAST'))
		for game_newlast in gamesList.get_last_games(self._config.last_folder_nb,[self._config.top_folder_name_dir,self._config.last_folder_name_dir,self._config.ko_folder_name_dir,self._config.best_folder_name_dir]):
			game_found=False
			logger.info(gamesList.last_name_console(pos,game_newlast.name,game_newlast.lastplayed))
			#Recherche existance ancien last	
			for game_lastlast in gamesList.get_games_in_folder(self._config.last_folder_name_dir):
				if game_lastlast == game_newlast:
					game_lastlast.specific='LAST'
					game_lastlast.name = gamesList.last_name(pos,game_newlast.name)
					gamesList.update_game(game_lastlast)
					game_found=True
					break
			if not game_found:
				oldpath=os.path.join(GameListDirectory,os.path.expanduser(get_path_without_current(game_newlast.path)))
				newpath=os.path.join(GameListDirectory,self._config.last_folder_name_dir,game_newlast.get_filename_rom())
				if os.path.isfile(oldpath):
					if not os.path.isfile(newpath):
						if os.name=='posix':
							#création hardlink sous linux
							os.link(oldpath,newpath)
						else:
							shutil.copyfile(oldpath,newpath)
					
					game_newlast.path = '.' + os.sep + self._config.last_folder_name_dir + os.sep + game_newlast.get_filename_rom()
					game_newlast.specific='LAST'
					game_newlast.name = gamesList.last_name(pos,game_newlast.name)
					gamesList.add_game(game_newlast)
				else:
					#logger.debug('Patch_Last_Games : no file in source '+oldpath + ' for new last')
					logger.debug(msg_local.get(('MSG_DEBUG_GLP_PATH_NOT_EXIST',config.language)).format('Patch_Last_Games',oldpath))
			pos+=1
			
		#Purge des anciens entrées LAST et suppression attribut specific
		for game_lastlast in gamesList.get_games_in_folder(self._config.last_folder_name_dir):
			if game_lastlast.specific=='LAST':
				game_lastlast.specific=''
				gamesList.update_game(game_lastlast)
			else:
				#test des exclusions pour conserver les ROMs (cas de neogeo)
				if is_not_exclusion_file('.' + os.sep + self._config.last_folder_name_dir,game_lastlast.get_filename_rom(),self._config.game_name_exclusion,self._config.images_extension + self._config.game_extension_exclusion):
					gamesList.delete_game(game_lastlast)
					if os.path.isfile(os.path.join(GameListDirectory,os.path.expanduser(get_path_without_current(game_lastlast.path)))):
						os.remove(os.path.join(GameListDirectory,get_path_without_current(game_lastlast.path)))
					else:
						#logger.debug('Patch_Last_Games : no file to delete ('+game_lastlast.path+')')
						logger.debug(msg_local.get(('MSG_DEBUG_GLP_PATH_NOT_EXIST',config.language)).format('Patch_Last_Games',game_lastlast.path))
				else:
					#logger.debug('Patch_Last_Games : exclusion file ('+game_lastlast.get_filename_rom()+')')
					logger.debug(msg_local.get(('MSG_DEBUG_GLP_FILE_EXCL_FOUND',config.language)).format('Patch_Last_Games',game_lastlast.get_filename_rom()))
					
					
	#---------------------------------------------------------------------------------------------------
	def Patch_Folder_Picture(self,GameListDirectory,gamesList):
		"""Gestion des images pour les noeuds folder"""
		logger.debug(msg_local.get(('MSG_DEBUG_GLP_FUNCTION_START',config.language)).format('Patch_Folder_Picture'))
		
		#Recherche des sous-dossiers
		subDirectories = list_sub_directories(GameListDirectory,self._config.images_folder,self._config.folder_name_exclusion)
		if len(subDirectories)>0:
			for SubDirectory in subDirectories:
				force_refresh_xml = False
				is_folder_rom_ko = False
				is_folder_top = False
				is_folder_last = False
				is_folder_best = False
				
				#Recherche de l'image d'un sous-dossier sur le système de fichiers
				#logger.debug('SubDirectory='+SubDirectory)
				logger.debug(msg_local.get(('MSG_DEBUG_GLP_FOLDER_SUB',config.language)).format('Patch_Folder_Picture',SubDirectory))
				
				pictureFile = get_associed_image_from_file(GameListDirectory,SubDirectory,self._config.images_extension,self._config.images_folder)
				#Gestion Folder par défaut
				if pictureFile=='':
					if self._config.default_folder_picture_path =='':
						pathPicture =''
						#logger.debug ('found folder '+SubDirectory + ' without image')	
						logger.debug(msg_local.get(('MSG_DEBUG_GLP_FOLDER_NO_IMAGE',config.language)).format('Patch_Folder_Picture',SubDirectory))
						
					else:
						if self._config.ko_folder_name_dir in SubDirectory:
							#FOLDER KO ROMS
							is_folder_rom_ko = True
							if self._config.is_folder_ko_picture_mode_append:
								pathPicture = self._config.ko_folder_picture_path
								#logger.debug ('found folder '+SubDirectory + ' use ko image')
								logger.debug(msg_local.get(('MSG_DEBUG_GLP_ASS_FOLDER_TYPE',config.language)).format('Patch_Folder_Picture',SubDirectory,'KO'))
							else:
								pathPicture=''
								force_refresh_xml = True
								
						elif self._config.top_folder_name_dir in SubDirectory:
							#FOLDER TOP
							is_folder_top=True
							if self._config.is_folder_top_picture_mode_append:
								pathPicture = self._config.folder_top_picture
								
								#logger.debug ('found folder '+SubDirectory + ' use top image')
								logger.debug(msg_local.get(('MSG_DEBUG_GLP_ASS_FOLDER_TYPE',config.language)).format('Patch_Folder_Picture',SubDirectory,'TOP'))
								
							else:
								pathPicture=''
								force_refresh_xml = True
						
						elif self._config.last_folder_name_dir in SubDirectory:
							#FOLDER LAST
							is_folder_last=True
							if self._config.is_folder_last_picture_mode_append:
								pathPicture = self._config.folder_last_picture
								#logger.debug ('found folder '+SubDirectory + ' use last image')
								logger.debug(msg_local.get(('MSG_DEBUG_GLP_ASS_FOLDER_TYPE',config.language)).format('Patch_Folder_Picture',SubDirectory,'LAST'))
							else:
								pathPicture=''
								force_refresh_xml = True
						
						elif self._config.best_folder_name_dir in SubDirectory:
							#FOLDER BEST
							is_folder_best=True
							if self._config.is_folder_best_picture_mode_append:
								pathPicture = self._config.folder_best_picture
								#logger.debug ('found folder '+SubDirectory + ' use best image')
								logger.debug(msg_local.get(('MSG_DEBUG_GLP_ASS_FOLDER_TYPE',config.language)).format('Patch_Folder_Picture',SubDirectory,'BEST'))
							else:
								pathPicture=''
								force_refresh_xml = True
								
						elif self._config.is_folder_default_picture_mode_append:
							#FOLDER DEFAULT
							#logger.debug ('found folder '+SubDirectory + ' use default image')
							logger.debug(msg_local.get(('MSG_DEBUG_GLP_ASS_FOLDER_TYPE',config.language)).format('Patch_Folder_Picture',SubDirectory,'DEFAULT'))
							pathPicture = self._config.default_folder_picture_path
						else:
							pathPicture = ''
							force_refresh_xml = True
							
				else:
					if self._local_image_folder + os.sep in pictureFile:
						#cas d'une image dans un sous-répertoire (chemin complet)
						pathPicture = '.' +os.sep + pictureFile
					else:
						#cas d'une image dans le répertoire image au même niveau que gamelist.xml (nom du fichier)
						pathPicture = '.' +os.sep + self._local_image_folder + os.sep + pictureFile
						#logger.debug ('found folder in DIR : .' +os.sep + SubDirectory + ' image='+ pathPicture)
				

				#Mise à jour XML
				if pathPicture!='' or force_refresh_xml:
					try:
						folder_XML = gamesList.search_folder_by_path('.'+os.sep+SubDirectory)
						#logger.debug ('found folder in XML : '+ folder_XML.path + ' image=' +folder_XML.image)
						logger.debug(msg_local.get(('MSG_DEBUG_GLP_FOLDER_FOUND_IMAGE',config.language)).format('Patch_Folder_Picture',folder_XML.path,folder_XML.image))
						
						#Cas du changement de nom KO
						if is_folder_rom_ko and folder_XML.name!=self._config.ko_folder_name_xml:
							folder_XML.name=self._config.ko_folder_name_xml
							force_refresh_xml = True
							#logger.info ('found folder '+SubDirectory + ' refresh name ko')
							logger.debug(msg_local.get(('MSG_DEBUG_GLP_FOLDER_REFRESH_NAME',config.language)).format('Patch_Folder_Picture',SubDirectory,'KO'))
						
						#Cas du changement de nom TOP
						if is_folder_top and folder_XML.name!=self._config.top_folder_name_xml:
							folder_XML.name=self._config.top_folder_name_xml
							force_refresh_xml = True
							#logger.info ('found folder '+SubDirectory + ' refresh name top')
							logger.debug(msg_local.get(('MSG_DEBUG_GLP_FOLDER_REFRESH_NAME',config.language)).format('Patch_Folder_Picture',SubDirectory,'TOP'))
						
						#Cas du changement de nom LAST
						if is_folder_last and folder_XML.name!=self._config.last_folder_name_xml:
							folder_XML.name=self._config.last_folder_name_xml
							force_refresh_xml = True
							#logger.info ('found folder '+SubDirectory + ' refresh name last')
							logger.debug(msg_local.get(('MSG_DEBUG_GLP_FOLDER_REFRESH_NAME',config.language)).format('Patch_Folder_Picture',SubDirectory,'LAST'))
						
						#Cas du changement de nom BEST
						if is_folder_best and folder_XML.name!=self._config.best_folder_name_xml:
							folder_XML.name=self._config.best_folder_name_xml
							force_refresh_xml = True
							#logger.info ('found folder '+SubDirectory + ' refresh name best')
							logger.debug(msg_local.get(('MSG_DEBUG_GLP_FOLDER_REFRESH_NAME',config.language)).format('Patch_Folder_Picture',SubDirectory,'BEST'))
							
						#Mise à jour
						#if pathPicture != folder_XML.image or folder_XML.ref_id=='' or folder_XML.source=='' or force_refresh_xml:
						if pathPicture != folder_XML.image or force_refresh_xml:
							#folder_XML.ref_id=SubDirectory
							folder_XML.image=pathPicture
							gamesList.update_folder(folder_XML)
							if pathPicture=='' and force_refresh_xml:
								#logger.info ('Update Folder '+SubDirectory+' delete image')
								logger.info(msg_local.get(('MSG_INFO_GLP_FOLDER_UPD_DEL_IMAGE',config.language)).format('Patch_Folder_Picture',SubDirectory))
							else:
								#logger.info ('Update Folder '+SubDirectory+' with this image '+pathPicture)
								logger.info(msg_local.get(('MSG_INFO_GLP_FOLDER_UPD_UPD_IMAGE',config.language)).format('Patch_Folder_Picture',SubDirectory,pathPicture))
						else:
							#logger.debug ('Folder '+SubDirectory+' is up-to-date')
							logger.debug(msg_local.get(('MSG_DEBUG_GLP_FOLDER_UPD_ALREADY_IMAGE',config.language)).format('Patch_Folder_Picture',SubDirectory))
							
							
					except MyError:
						#Pas de noeud folder trouvé
						folder_XML=Folder()
						folder_XML.path='.'+os.sep+SubDirectory
						#Définition du nom
						if self._config.ko_folder_name_dir in SubDirectory:
							folder_XML.name=self._config.ko_folder_name_xml
						elif self._config.top_folder_name_dir in SubDirectory:
							folder_XML.name=self._config.top_folder_name_xml
						elif self._config.last_folder_name_dir in SubDirectory:
							folder_XML.name=self._config.last_folder_name_xml
						elif os.sep in SubDirectory:
							folder_XML.name=SubDirectory.split(os.sep)[-1]
						else:
							folder_XML.name=SubDirectory
						#La suite...
						folder_XML.image=pathPicture
						#0.5.06
						#folder_XML.ref_id=SubDirectory.replace(os.sep,'_')
						gamesList.add_folder(folder_XML)
						#logger.info ('Add New Folder Entry '+SubDirectory+' with this image '+pathPicture)
						logger.info(msg_local.get(('MSG_INFO_GLP_FOLDER_ADD',config.language)).format('Patch_Folder_Picture',SubDirectory,pathPicture))
					
					except Exception as exception:
						#logger.warn('Patch_Folder_Picture :' +type(exception).__name__)
						logger.warn(msg_local.get(('MSG_ERROR_GLP_EXCEPTION',config.language)).format('Patch_Folder_Picture',type(exception).__name__))
						sys.exit(1)
	
	
					#Gestion de l'attribut hidden
					bHidden = ( folder_XML.get_filename_folder() in self._config.folder_name_hidden )
					if bHidden and not folder_XML.hidden=='true':
						folder_XML.hidden='true'
						gamesList.update_folder(folder_XML)
						logger.debug(msg_local.get(('MSG_INFO_GLP_GAME_UPD_HIDDEN',config.language)).format('Patch_Folder_Picture','True'))
					if not bHidden and folder_XML.hidden=='true':
						folder_XML.hidden='false'
						gamesList.update_folder(folder_XML)
						logger.debug(msg_local.get(('MSG_INFO_GLP_GAME_UPD_HIDDEN',config.language)).format('Patch_Folder_Picture','False'))
	
	
		else:
			#logger.debug ('Skip no sub directory')
			logger.debug(msg_local.get(('MSG_DEBUG_GLP_FOLDER_NOSUB_FOLDER',config.language)).format('Patch_Folder_Picture'))
		
	
	#---------------------------------------------------------------------------------------------------
	
	def Patch_Folder_NotExist(self,GameListDirectory,gamesList):
		"""suppression des noeuds folder non existant dans le système de fichiers"""
		logger.debug(msg_local.get(('MSG_DEBUG_GLP_FUNCTION_START',config.language)).format('Patch_Folder_NotExist'))
		
		for folder_XML in gamesList.get_folders():
			folder_to_check = get_path_without_current(folder_XML.path)
			if not os.path.isdir(os.path.join(GameListDirectory,folder_to_check)):
				#suppression du noeud
				gamesList.delete_folder(folder_XML)
				#logger.info('Folder ' + folder_to_check + ' not found, delete it')
				logger.info(msg_local.get(('MSG_INFO_GLP_FOLDER_DIR_NOT_FOUND',config.language)).format(folder_to_check))
				
			else:
				if self._config.is_folder_default_picture_mode_delete and folder_XML.image == self._config.default_folder_picture_path or \
				self._config.is_folder_ko_picture_mode_delete and folder_XML.image == self._config.ko_folder_picture_path or \
				self._config.is_folder_last_picture_mode_delete and folder_XML.image == self._config.last_folder_picture_path or \
				self._config.is_folder_top_picture_mode_delete and folder_XML.image == self._config.top_folder_picture_path or \
				self._config.is_folder_best_picture_mode_delete and folder_XML.image == self._config.best_folder_picture_path:
					#suppression image par défaut
					folder_XML.image=''
					gamesList.update_folder(folder_XML)
					#logger.info('Folder ' + folder_to_check + ' delete default image')
					logger.info(msg_local.get(('MSG_INFO_GLP_FOLDER_UPD_DEL_IMAGE',config.language)).format(folder_to_check))
	
	
	#---------------------------------------------------------------------------------------------------
	
	def Patch_Game_NotExist(self,GameListDirectory,gamesList):
		"""recherche de déplacements des roms si la rom dans gamelist.xml n'existe plus"""
		logger.debug(msg_local.get(('MSG_DEBUG_GLP_FUNCTION_START',config.language)).format('Patch_Game_NotExist'))
		
		#Le dossier root rom est prioritaire
		#subDirectories = list_sub_directories(GameListDirectory,self._config.folder_name_exclusion)
		#subDirectories.append('.') #ajoute une chaine en + pour le répertoire courant
		subDirectories=['.']
		subDirectories.extend(list_sub_directories(GameListDirectory,self._config.images_folder,self._config.folder_name_exclusion))
		
		for game_XML in gamesList.get_games_without_roms(GameListDirectory):
			#logger.info('Game ' + game_XML.name + ' without rom ' + game_XML.path)
			logger.info(msg_local.get(('MSG_INFO_GLP_GAME_WITHOUT_ROM',config.language)).format(game_XML.name,game_XML.path))
			
			game_name = game_XML.name
			rom_found=False
			
			#0.6.0-0.6.3 Recherche de la rom sauf si dans les dossiers LAST, TOP et BEST => suppression directe
			if game_XML.path.find(self._config.last_folder_name_dir)==-1 and game_XML.path.find(self._config.top_folder_name_dir)==-1 and game_XML.path.find(self._config.best_folder_name_dir)==-1:
				
				#Recherche des sous-dossiers
				for SubDirectory in subDirectories:
					game_name = game_XML.get_filename_rom()
					
					if SubDirectory=='.':
						SubDirectory_search = GameListDirectory
					else:
						SubDirectory_search = GameListDirectory + os.sep + SubDirectory

					if exist_game_rom(SubDirectory_search, game_name):
						#Rom trouvé dans un autre répertoire
						#logger.info('Game ' + game_name + ' found this rom in ' + SubDirectory)
						logger.info(msg_local.get(('MSG_INFO_GLP_GAME_FOUND_ROM',config.language)).format(game_name,SubDirectory))
						
						rom_found=True
						if SubDirectory_search == GameListDirectory:
							game_XML.ref_id=game_name
							gamesList.move_path_game(game_XML,"."+os.sep+game_name)
						else:
							game_XML.ref_id=(SubDirectory+os.sep+game_name).replace(os.sep,'_')
							gamesList.move_path_game(game_XML,"."+os.sep+SubDirectory+os.sep+game_name)
						break
	
			if not rom_found and (self._config.is_delete_game_everywhere or self._config.is_delete_game_in_ko_only and self._config.ko_folder_name_dir in game_XML.path):
				#suppression du noeud
				gamesList.delete_game(game_XML)
				#logger.info('Delete Game ' + game_name)
				logger.info(msg_local.get(('MSG_INFO_GLP_GAME_DEL',config.language)).format(game_name))
	
	#---------------------------------------------------------------------------------------------------
	
	def Patch_Game_Picture(self,GameListDirectory,gamesList):
		"""Gestion des images pour les noeuds game"""
		logger.debug(msg_local.get(('MSG_DEBUG_GLP_FUNCTION_START',config.language)).format('Patch_Game_Picture'))
		
		#0.6.2 - Message si volume important
		games_XML = gamesList.get_games()
		if len(games_XML)>=SEUIL_AFFICHAGE_CHECKPICTURES:
			logger.info(msg_local.get(('MSG_INFO_GLP_START_CHECKPICTURES',config.language)).format(''))
		
		for game_XML in games_XML:
			force_refresh_xml = False
			default_image_first_time=True
			
			if game_XML.image=='':
				#logger.info('Game ' + game_XML.name + ' without picture')
				logger.info(msg_local.get(('MSG_INFO_GLP_GAME_NO_IMAGE',config.language)).format(game_XML.name))
				
			else:
				#Test existence fichier image issue du fichier XML
				game_picture_to_check = get_path_without_current(game_XML.image)
				
				if game_XML.image==self._config.default_game_picture:
					#on reinit pour chercher si existence image
					default_image_first_time=False
					game_XML.image=''
					force_refresh_xml = self._config.is_default_game_picture_mode_delete
				else:
					#Correction 0.5.16 sur gestion /home et ~
					#if not os.path.isfile(os.path.expanduser(os.path.join(GameListDirectory,game_picture_to_check))):
					if not os.path.isfile(os.path.join(GameListDirectory,os.path.expanduser(game_picture_to_check))):
						#logger.info('Game ' + game_XML.name + ' picture ' + game_picture_to_check + ' not found')
						logger.info(msg_local.get(('MSG_INFO_GLP_GAME_IMAGE_NOT_FOUND',config.language)).format(game_XML.name,game_picture_to_check))
						game_XML.image=''
			
			#Gestion de l'image
			if game_XML.image=='':
				#Correction 0.5.13 pour extraction des noms fichiers avec .
				#picture_name = get_associed_image_from_file(GameListDirectory,game_XML.path[2:len(game_XML.path)].split('.')[0],self._config.images_extension)
				picture_name = get_associed_image_from_file(GameListDirectory,('.').join(game_XML.path[2:len(game_XML.path)].split('.')[:-1]),self._config.images_extension,self._config.images_folder)
	
				if picture_name!='':
					if os.sep in picture_name:
						#cas d'une image niveau >1
						game_XML.image = '.' +os.sep + picture_name
					else:
						game_XML.image = '.' +os.sep + self._local_image_folder + os.sep + picture_name
					gamesList.update_game(game_XML)
					#logger.info('Update Game Entry '+game_XML.name+' with this image ' + picture_name)
					logger.info(msg_local.get(('MSG_INFO_GLP_GAME_UPD_IMAGE',config.language)).format(game_XML.name,picture_name))
				elif self._config.is_default_game_picture_mode_append:
					game_XML.image = self._config.default_game_picture
					gamesList.update_game(game_XML)
					if default_image_first_time:
						#logger.info('Update Game Entry '+game_XML.name+' with default image')
						logger.info(msg_local.get(('MSG_INFO_GLP_GAME_UPD_IMAGE_DEF',config.language)).format(game_XML.name))
					else:
						#logger.debug('Update Game Entry '+game_XML.name+' with default image')
						logger.debug(msg_local.get(('MSG_INFO_GLP_GAME_UPD_IMAGE_DEF',config.language)).format(game_XML.name))
				elif force_refresh_xml:
					game_XML.image=''
					gamesList.update_game(game_XML)
					#logger.info('Update Game Entry '+game_XML.name+' delete default image')
					logger.info(msg_local.get(('MSG_INFO_GLP_GAME_DEL_IMAGE_DEF',config.language)).format(game_XML.name))
			
			#Gestion de l'attribut hidden
			bHidden = ( game_XML.get_filename_rom() in self._config.game_name_hidden )
			if bHidden and not game_XML.hidden=='True':
				game_XML.hidden='True'
				gamesList.update_game(game_XML)
				logger.debug(msg_local.get(('MSG_INFO_GLP_GAME_UPD_HIDDEN',config.language)).format('Patch_Game_Picture','True'))
			if not bHidden and game_XML.hidden=='True':
				game_XML.hidden='False'
				gamesList.update_game(game_XML)
				logger.debug(msg_local.get(('MSG_INFO_GLP_GAME_UPD_HIDDEN',config.language)).format('Patch_Game_Picture','False'))
					
			#Stats
			#self._gamesStats.add_rom(GameListDirectory,game_XML)
	
	#---------------------------------------------------------------------------------------------------
	
	def Patch_Game_Directory(self,GameListDirectory,gamesList,es_config_extension):
		"""Ajout des fichiers rom non présents dans gamelist.xml"""
		logger.debug(msg_local.get(('MSG_DEBUG_GLP_FUNCTION_START',config.language)).format('Patch_Game_Directory'))
		
		game_files = list_sub_files(GameListDirectory,self._config.folder_name_exclusion,self._config.game_name_exclusion,self._config.images_extension + self._config.game_extension_exclusion,es_config_extension)
		if len(game_files)>0:
			for game_file in game_files:
				#Recherche de l'entrée XML
				try:
					#logging.debug (game_file)
					game_XML = gamesList.search_game_by_path('.'+os.sep+game_file)
				except MyError:
					
					#Pas de noeud game trouvé
					game_XML = Game()
					game_XML.path='.'+os.sep+game_file
					
					#Correction 0.5.13 pour extraction des noms fichiers avec .
					#game_XML.name=game_file.split('.')[0]
					game_XML.name=('.').join(game_file.split('.')[:-1])
					#
					
					if os.sep in game_XML.name:
						game_XML.name = game_XML.name.split(os.sep)[-1]
						
					#Correction 0.5.13 pour extraction des noms fichiers avec .
					#game_XML.ref_id=game_file.split('.')[0].replace(os.sep,'_')
					game_XML.ref_id = game_XML.name.replace(os.sep,'_')
					#
					
					#Ajout de l'entrée
					gamesList.add_game(game_XML)
					#self._gamesStats.add_rom(GameListDirectory,game_XML)
					#logger.info ('Add New Game Entry : '+ game_file)
					logger.info(msg_local.get(('MSG_INFO_GLP_GAME_ADD',config.language)).format(game_XML.name))
				except Exception as exception:
						#logger.warn('main step2 :' +type(exception).__name__)
						logger.warn(msg_local.get(('MSG_ERROR_GLP_EXCEPTION',config.language)).format('Patch_Game_Directory',type(exception).__name__))
	
				#logger.debug ('Game found : '+ game_file + ' = ' + game_XML.name + ' => ' + game_XML.image)
				logger.debug(msg_local.get(('MSG_DEBUG_GLP_GAME_FOUND',config.language)).format(game_file,game_XML.name,game_XML.image))
				
				if game_XML.image=='':
					
					#Correction 0.5.13 pour extraction des noms fichiers avec .
					#picture_name = get_associed_image_from_file(GameListDirectory,game_XML.path[2:len(game_XML.path)].split('.')[0],self._config.images_extension)
					picture_name = get_associed_image_from_file(GameListDirectory,('.').join(game_XML.path[2:len(game_XML.path)].split('.')[:-1]),self._config.images_extension,self._config.images_folder)
					
					if picture_name!='':
						if os.sep in picture_name:
							#cas d'une image niveau >1
							game_XML.image = '.' +os.sep + picture_name
						else:
							game_XML.image = '.' +os.sep + self._local_image_folder + os.sep + picture_name
						gamesList.update_game(game_XML)
						#logger.info('Update Game Entry '+game_XML.name+' with this image ' + picture_name)
						logger.info(msg_local.get(('MSG_INFO_GLP_GAME_UPD_IMAGE',config.language)).format(game_XML.name,picture_name))
					elif self._config.is_default_game_picture_mode_append:
						game_XML.image = self._config.default_game_picture
						gamesList.update_game(game_XML)
						#logger.info('Update Game Entry '+game_XML.name+' with default image')
						logger.info(msg_local.get(('MSG_INFO_GLP_GAME_UPD_IMAGE_DEF',config.language)).format(game_XML.name))
					elif force_refresh_xml:
						game_XML.image=''
						gamesList.update_game(game_XML)
						#logger.info('Update Game Entry '+game_XML.name+' delete default image')
						logger.info(msg_local.get(('MSG_INFO_GLP_GAME_DEL_IMAGE_DEF',config.language)).format(game_XML.name))
					else:
						#logger.debug('no image for ' + game_XML.name)
						logger.debug(msg_local.get(('MSG_DEBUG_GLP_GAME_NOT_FOUND',config.language)).format('Patch_Game_Directory',game_XML.name))
		else:
			#logger.debug ('No game found')
			logger.debug(msg_local.get(('MSG_DEBUG_GLP_GAME_NOT_FOUND',config.language)).format('Patch_Game_Directory'))
					
	#---------------------------------------------------------------------------------------------------

	def Compute_Game_Stats(self,GameListDirectory,gamesList):
		"""Calcul des statistiques post-exec"""
		self._gamesStats.add_plateform(GameListDirectory)
		for game_XML in gamesList.get_games():
			self._gamesStats.add_rom(GameListDirectory,game_XML)
	
	#---------------------------------------------------------------------------------------------------
	
	
			
	#---------------------------------------------------------------------------------------------------
	
	def run(self):

		
		gamelist_load_errors=[]   		#Liste des gamelist.xml en erreur de chargement
		es_config_command=''      		#Commande de lancement des roms pour une configuration (RecalBox/Happigc)
		es_config_system_name=''      #Nom du systeme a passer dans la commande (RecalBox)
		es_config_default_emulator=''	#Emulateur par defaut du system a passer dans la commande (RecalBox)
		es_config_default_core=''			#Coeur par defaut de l'emulateur du system a passer dans la commande (RecalBox)
		es_config_extension=[]    		#Liste des extensions des roms pour une configuration
		plateform_collection=''       #Path de plateforme cible collection
		format_titre="%%NAME%% (%%PLATEFORM%%)" #Format par defaut du titre
		bNetPlayInCommandCollection=False			  #Support de %NETPLAY% dans ligne de commande de collection
		
		self.running=True
		if self._affichage == 'console':logger.info('#'*79) 
		else:logger.info('#'*71)
		logger.info('GameListPower - NordicPower - Version '+VERSION)
		if self._affichage == 'console':logger.info('#'*79) 
		else:logger.info('#'*71)
		self._config.debug()
		logger.debug(msg_local.get(('MSG_DEBUG_GLP_LAUNCH_ARG_MODE',config.language)).format(self._mode))
		logger.debug(msg_local.get(('MSG_DEBUG_GLP_PRG_INIT',config.language)))
		
		GameListDirectories = list_gamelist_directories(self._config.rootPath,self._config.folder_name_exclusion,self._config.images_folder)
		
		#Ajout des roms USB si existant
		if self._config.rootPathUsb !='':
			#Recherche des dossiers roms USB
			GameListDirectories_usb = list_gamelist_directories(self._config.rootPathUsb,self._config.folder_name_exclusion,self._config.images_folder)
			#Ajout à la liste principale
			GameListDirectories.extend(GameListDirectories_usb)
		
		#Event Start avec nb répertoire
		self.GameListDirectory_Event = str(len(GameListDirectories))
		self.trigger('GameListDirectoryStart')
		
		#Chargement des hashs
		self._folders_Hash.load()
		
		#Chargement du fichier es_systems.cfg (configuration EmulationStation)
		try:
			configs_ES = ESSystemList()
			configs_ES.import_xml_file(self._config.emulation_station_systems)
		except Exception as exception:
			logger.critical(msg_local.get(('MSG_CRITICAL_GLP_ESSYSTEM_LOAD_ERROR',config.language)).format(type(exception).__name__))
			sys.exit(1)
		
		#Tri des dossiers par ordre alphabetique
		GameListDirectories = sorted(GameListDirectories)
		
		#Initialisation du mode multi
		if self._mode in [ARG_MODE_GENERATE_SH]:
			#Chargement des règles de génération gensh
			if os.path.isfile('rules_gensh.xml'):
				rules = load_rules_from_xml_config('rules_gensh.xml',TYPE_RULE_GENSH)
				plateform_collection=get_plateform_from_xml_config('rules_gensh.xml')
				format_titre=get_title_format_from_xml_config('rules_gensh.xml')
			else:
				rules = load_rules_from_ini_config(config.generation_rules)
				plateform_collection = config.folder_path_multi
		
		if self._mode in [ARG_MODE_GENERATE_ROMCPY]:
			#Chargement des règles de génération romcpy
			if os.path.isfile('rules_romcpy.xml'):
				rules = load_rules_from_xml_config('rules_romcpy.xml',TYPE_RULE_ROMCPY)
				plateform_collection=get_plateform_from_xml_config('rules_romcpy.xml')
				format_titre=get_title_format_from_xml_config('rules_romcpy.xml')
				
			else:
				logger.critical(msg_local.get(('MSG_CRITICAL_GLP_RULE_NOT_EXIST',config.language)).format('rules_romcpy.xml'))
				sys.exit(1)
		
		
		if self._mode in [ARG_MODE_GENERATE_SH,ARG_MODE_GENERATE_ROMCPY]:
			#Cas particulier collection sans gamelist.xml cible 
			if self._mode in [ARG_MODE_GENERATE_SH,ARG_MODE_GENERATE_ROMCPY]:
				if not os.path.isfile(os.path.join(plateform_collection,NOM_GAMELIST_XML)):
					gamesList = GamesList()
					gamesList.create_root_xml()
					gamesList.save_xml_file(os.path.join(plateform_collection,NOM_GAMELIST_XML))
			#Recherche de la commande pour vérifier le support NETPLAY (
			if configs_ES.search_system_by_short_path(get_short_path_from_root(config.rootPath,plateform_collection)).command in '%NETPLAY%':
				bNetPlayInCommandCollection=True
			#Suppression de l'ensemble des fichiers sh, ils sont regénérés ensuite (suppression des sh obsolètes)
			delete_commands_for_multi(rules)
			#Creation des dossiers destinations
			create_destination_rules(rules)
			#Dossier Multi à la fin du traitement
			try:
				GameListDirectories.remove(plateform_collection)
			except:
				pass
			if plateform_collection!='':
				GameListDirectories.append(plateform_collection)
    
		logger.debug(msg_local.get(('MSG_DEBUG_GLP_PRG_START',config.language)))
    
		#Recherche des répertoires de jeu et lancement des patchs
		for GameListDirectory in GameListDirectories:
			
			#Event & log
			self.GameListDirectory_Event = get_short_path_from_root(config.rootPath,GameListDirectory)
			self.trigger('GameListDirectoryRun')
			logger.info(msg_local.get(('MSG_INFO_GLP_CURRENT_FOLDER',config.language)).format(self.GameListDirectory_Event))
			
			#Recherche du dossier image de réference
			self._local_image_folder='images'
			for image_folder in config.images_folder:
				if os.path.exists(os.path.join(GameListDirectory,image_folder)):
					self._local_image_folder = image_folder
					break
			
			#Chargement configuration EmulationStation
			try:
				config_ES = configs_ES.search_system_by_short_path(get_short_path_from_root(config.rootPath,GameListDirectory))
				es_config_system_name=config_ES.name
				es_config_command=config_ES.command
				es_config_default_emulator=config_ES.getDefaultEmulator()
				es_config_default_core=config_ES.getDefaultEmulatorCore()
				es_config_extension=config_ES.extension.replace('.','').split(' ')
				logger.debug(msg_local.get(('MSG_DEBUG_GLP_ESSYSTEM_CONFIG_PLATEFORM',config.language)).format(es_config_command,config_ES.extension))
			except:
				es_config_command=''
				es_config_system_name=''
				es_config_default_emulator=''
				es_config_default_core=''
				es_config_extension=[]
				logger.debug(msg_local.get(('MSG_DEBUG_GLP_ESSYSTEM_UNKNOW_PLATEFORM',config.language)).format(config_ES.name))

			if self._config.rootPathUsb !='' and es_config_command =='':
				try:
					config_ES = configs_ES.search_system_by_short_path(get_short_path_from_root(config.rootPathUsb,GameListDirectory))
					es_config_system_name=config_ES.name
					es_config_command=config_ES.command
					es_config_default_emulator=config_ES.getDefaultEmulator()
					es_config_default_core=config_ES.getDefaultEmulatorCore()
					es_config_extension=config_ES.extension.replace('.','').split(' ')
					logger.debug(msg_local.get(('MSG_DEBUG_GLP_ESSYSTEM_CONFIG_PLATEFORM',config.language)).format(es_config_command,config_ES.extension))
				except:
					es_config_system_name=''
					es_config_command=''
					es_config_default_emulator=''
					es_config_default_core=''
					es_config_extension=[]
					logger.debug(msg_local.get(('MSG_DEBUG_GLP_ESSYSTEM_UNKNOW_PLATEFORM',config.language)).format(''))
			
			#Chargement XML avec MiniDom :-<
			gamesList = GamesList()
			try:
				gamesList.import_xml_file(GameListDirectory + os.sep + NOM_GAMELIST_XML,True)
			except MyError:
				#cas fichier gamelist.xml mal formé, on passe au dossier de roms suivant
				gamelist_load_errors.append(GameListDirectory + os.sep + NOM_GAMELIST_XML)
				continue
			except Exception as exception:
				#fichier inexistant, on passe au dossier de roms suivant
				gamelist_load_errors.append(GameListDirectory + os.sep + NOM_GAMELIST_XML)
				continue
				
			#[ARG_MODE_PATCH_FULL,ARG_MODE_PATCH_FORCE,ARG_MODE_CORRECT_ONLY,ARG_MODE_TOP_ONLY,ARG_MODE_STATS_ONLY,ARG_MODE_NOIMAGE_ONLY,ARG_MODE_GENERATE_SH,ARG_MODE_GENERATE_ROMCPY]
			if self._mode in [ARG_MODE_PATCH_FULL,ARG_MODE_PATCH_FORCE,ARG_MODE_CORRECT_ONLY]:
				#STEP 0 - Calcul du Hash et comparaison version précédente
				folder_change_since_last_exec = self._folders_Hash.changed(GameListDirectory)
				if not folder_change_since_last_exec:
					logger.debug(msg_local.get(('MSG_DEBUG_GLP_FOLDER_HASH_NOCHANGE',config.language)).format(self._folders_Hash.dictionary[GameListDirectory]))
			
				#EXEC si modification détectée ou desactivation de la fonctionnalité
				if folder_change_since_last_exec or not self._config.hint_use_os_stat or self._mode==ARG_MODE_PATCH_FORCE:
					#STEP 1 - Parcours des répertoires et correction du gamelist.xml---------------------------------
					self.Patch_Folder_Picture(GameListDirectory,gamesList)
					#STEP 2 - Parcours des noeuds folder du gamelist.xml---------------------------------------------
					self.Patch_Folder_NotExist(GameListDirectory,gamesList)
					#STEP 3 - Suppression des doublons game----------------------------------------------------------
					self.Patch_Game_Doublons(GameListDirectory,gamesList)
					#STEP 4 - Parcours des noeuds game pour les roms du gamelist.xml---------------------------------
					self.Patch_Game_NotExist(GameListDirectory,gamesList)
					#STEP 5 - Parcours des noeuds game pour les images du gamelist.xml-------------------------------
					self.Patch_Game_Picture(GameListDirectory,gamesList)
					#STEP 6 - Parcours des roms et correction du gamelist.xml----------------------------------------
					self.Patch_Game_Directory(GameListDirectory,gamesList,es_config_extension)

			#[ARG_MODE_PATCH_FULL,ARG_MODE_PATCH_FORCE,ARG_MODE_CORRECT_ONLY,ARG_MODE_TOP_ONLY,ARG_MODE_STATS_ONLY,ARG_MODE_NOIMAGE_ONLY,ARG_MODE_GENERATE_SH,ARG_MODE_GENERATE_ROMCPY]
			if self._mode in [ARG_MODE_GENERATE_SH,ARG_MODE_GENERATE_ROMCPY] and GameListDirectory in [plateform_collection]:
				#STEP 1 - Parcours des répertoires et correction du gamelist.xml---------------------------------
				self.Patch_Folder_Picture(GameListDirectory,gamesList)
				#STEP 2 - Parcours des noeuds folder du gamelist.xml---------------------------------------------
				self.Patch_Folder_NotExist(GameListDirectory,gamesList)
				#STEP 4 - Parcours des noeuds game pour les roms du gamelist.xml---------------------------------
				self.Patch_Game_NotExist(GameListDirectory,gamesList)
			
			#[ARG_MODE_PATCH_FULL,ARG_MODE_PATCH_FORCE,ARG_MODE_CORRECT_ONLY,ARG_MODE_TOP_ONLY,ARG_MODE_STATS_ONLY,ARG_MODE_NOIMAGE_ONLY,ARG_MODE_GENERATE_SH,ARG_MODE_GENERATE_ROMCPY]
			if self._mode in [ARG_MODE_PATCH_FULL,ARG_MODE_PATCH_FORCE,ARG_MODE_TOP_ONLY]:

				#STEP 7 - Gestion du TOP-------------------------------------------------------------------------
				if self._config.top_folder_name_dir!='':
					if os.path.isdir(os.path.join(GameListDirectory,self._config.top_folder_name_dir)):
						self.Patch_Top_Games(GameListDirectory,gamesList,es_config_extension)
				
				#STEP 8 - Gestion du LAST-------------------------------------------------------------------------
				if self._config.last_folder_name_dir!='':
					if os.path.isdir(os.path.join(GameListDirectory,self._config.last_folder_name_dir)):
						self.Patch_Last_Games(GameListDirectory,gamesList,es_config_extension)
				
				#STEP 9 - Gestion du BEST-----------------------------------------------------------------------
				if self._config.best_folder_name_dir!='':
						if os.path.isdir(os.path.join(GameListDirectory,self._config.best_folder_name_dir)):
							self.Patch_Best_Games(GameListDirectory,gamesList,es_config_extension)
			
			#[ARG_MODE_PATCH_FULL,ARG_MODE_PATCH_FORCE,ARG_MODE_CORRECT_ONLY,ARG_MODE_TOP_ONLY,ARG_MODE_STATS_ONLY,ARG_MODE_NOIMAGE_ONLY,ARG_MODE_GENERATE_SH,ARG_MODE_GENERATE_ROMCPY]
			if self._mode in [ARG_MODE_GENERATE_SH,ARG_MODE_GENERATE_ROMCPY] and GameListDirectory not in [plateform_collection]:
				#Ne pas sauvegarder car lecture uniquement sauf si cible
				gamesList.modified=False
				
			#[ARG_MODE_PATCH_FULL,ARG_MODE_PATCH_FORCE,ARG_MODE_CORRECT_ONLY,ARG_MODE_TOP_ONLY,ARG_MODE_STATS_ONLY,ARG_MODE_NOIMAGE_ONLY,ARG_MODE_GENERATE_SH,ARG_MODE_GENERATE_ROMCPY]
			if self._mode in [ARG_MODE_GENERATE_SH,ARG_MODE_GENERATE_ROMCPY] and es_config_command !='' and GameListDirectory in [plateform_collection] :
				#Mise à jour attribut dossier
				update_folders_attributes(rules,gamesList)
				
			#STEP END - Sauvegarde si intervention sur le fichier--------------------------------------------
			if gamesList.modified:
				
				#folders à jour
				gamesList.refresh_folders_finished()
				
				if not gamesList.empty_file_at_load:
					#Création d'une sauvegarde origin uniq 1ier modification du fichier
					if not os.path.isfile(os.path.join(GameListDirectory,os.path.expanduser(NOM_GAMELIST_XML_ORIGIN))) and self._config.option_save_origin:
						#logger.debug('SAVE '+ NOM_GAMELIST_XML_ORIGIN)
						logger.debug(msg_local.get(('MSG_INFO_GLP_PRG_SAVE',config.language)).format(NOM_GAMELIST_XML_ORIGIN))
						shutil.copyfile(os.path.join(GameListDirectory,NOM_GAMELIST_XML),(os.path.join(GameListDirectory,NOM_GAMELIST_XML_ORIGIN)))
					#Création d'une sauvegarde
					if self._config.option_save_backup:
						shutil.copyfile(os.path.join(GameListDirectory,NOM_GAMELIST_XML),(os.path.join(GameListDirectory,NOM_GAMELIST_XML_SAV)))
						#logger.debug('SAVE '+ NOM_GAMELIST_XML_SAV)
						logger.debug(msg_local.get(('MSG_INFO_GLP_PRG_SAVE',config.language)).format(NOM_GAMELIST_XML_SAV))
		
				#Patch 0.5.17
				#if self.GameListDirectory_Event in ['roms/arcade/fba','roms/arcade/mame']:
				if len(gamesList.get_games())>SEUIL_SAUVEGARDE_BIGROM:
					logger.debug(msg_local.get(('MSG_INFO_GLP_PRG_SAVE_BIGROM',config.language)).format(NOM_GAMELIST_XML))
					gamesList.save_xml_file(os.path.join(GameListDirectory,NOM_GAMELIST_XML),False)
				else:
					logger.debug(msg_local.get(('MSG_INFO_GLP_PRG_SAVE',config.language)).format(NOM_GAMELIST_XML))
					gamesList.save_xml_file(os.path.join(GameListDirectory,NOM_GAMELIST_XML))

			#[ARG_MODE_PATCH_FULL,ARG_MODE_PATCH_FORCE,ARG_MODE_CORRECT_ONLY,ARG_MODE_TOP_ONLY,ARG_MODE_STATS_ONLY,ARG_MODE_NOIMAGE_ONLY,ARG_MODE_GENERATE_SH,ARG_MODE_GENERATE_ROMCPY]
			if self._mode in [ARG_MODE_PATCH_FULL,ARG_MODE_PATCH_FORCE,ARG_MODE_CORRECT_ONLY,ARG_MODE_TOP_ONLY,ARG_MODE_STATS_ONLY,ARG_MODE_NOIMAGE_ONLY]:
				#Calcul des statistiques
				self.Compute_Game_Stats(GameListDirectory,gamesList)
			
			#[ARG_MODE_PATCH_FULL,ARG_MODE_PATCH_FORCE,ARG_MODE_CORRECT_ONLY,ARG_MODE_TOP_ONLY,ARG_MODE_STATS_ONLY,ARG_MODE_NOIMAGE_ONLY,ARG_MODE_GENERATE_SH,ARG_MODE_GENERATE_ROMCPY]
			if self._mode in [ARG_MODE_PATCH_FULL,ARG_MODE_PATCH_FORCE,ARG_MODE_CORRECT_ONLY]:
				#Calcul du hash
				self._folders_Hash.set_hash(GameListDirectory)
				logger.debug(msg_local.get(('MSG_DEBUG_GLP_FOLDER_HASH_REFRESH',config.language)).format(self._folders_Hash.dictionary[GameListDirectory]))
						
			#[ARG_MODE_PATCH_FULL,ARG_MODE_PATCH_FORCE,ARG_MODE_CORRECT_ONLY,ARG_MODE_TOP_ONLY,ARG_MODE_STATS_ONLY,ARG_MODE_NOIMAGE_ONLY,ARG_MODE_GENERATE_SH,ARG_MODE_GENERATE_ROMCPY]
			if self._mode in [ARG_MODE_GENERATE_SH,ARG_MODE_GENERATE_ROMCPY] and es_config_command !='' and GameListDirectory not in [plateform_collection] :
				#Generation sh et noeud game
				local_match_results_rules = search_games_for_multi(GameListDirectory,gamesList,self.GameListDirectory_Event,
				es_config_system_name,es_config_command,es_config_default_emulator,es_config_default_core,rules,
				[self._config.top_folder_name_dir,self._config.last_folder_name_dir,self._config.best_folder_name_dir,self._config.ko_folder_name_dir],
				self._config.default_game_picture)
				if len(local_match_results_rules)>0:
					generate_launcher_for_multi(config,plateform_collection,local_match_results_rules,format_titre,bNetPlayInCommandCollection)
				
			#Ligne de séparation
			if self._affichage == 'console':logger.info('-'*79) 
			else: logger.info('-'*71) 
			
			#Fin boucle répertoire


		#[ARG_MODE_PATCH_FULL,ARG_MODE_PATCH_FORCE,ARG_MODE_CORRECT_ONLY,ARG_MODE_TOP_ONLY,ARG_MODE_STATS_ONLY,ARG_MODE_NOIMAGE_ONLY,ARG_MODE_GENERATE_SH,ARG_MODE_GENERATE_ROMCPY]
		if self._mode in [ARG_MODE_PATCH_FULL,ARG_MODE_PATCH_FORCE,ARG_MODE_CORRECT_ONLY]:
			#Enregistrement des hashs
			self._folders_Hash.save()
		
		#[ARG_MODE_PATCH_FULL,ARG_MODE_PATCH_FORCE,ARG_MODE_CORRECT_ONLY,ARG_MODE_TOP_ONLY,ARG_MODE_STATS_ONLY,ARG_MODE_NOIMAGE_ONLY,ARG_MODE_GENERATE_SH,ARG_MODE_GENERATE_ROMCPY]
		if self._mode in [ARG_MODE_PATCH_FULL,ARG_MODE_PATCH_FORCE,ARG_MODE_CORRECT_ONLY,ARG_MODE_TOP_ONLY,ARG_MODE_STATS_ONLY]:
			#Tableau des statistiques
			self._gamesStats.log_stats()
		if self._mode in [ARG_MODE_NOIMAGE_ONLY]:
			#Liste des roms sans image
			self.gamesStats.log_roms_without_picture()
			
		#Event
		self.GameListDirectory_Event = ''
		self.trigger('GameListDirectoryEnd')

		#Message erreur fin
		if len(gamelist_load_errors)>0:
			logger.info(msg_local.get(('MSG_INFO_GLP_GAMELIST_ERROR',config.language)).format(len(gamelist_load_errors)))
			for gamelist_load_error in gamelist_load_errors:
				logger.info(msg_local.get(('MSG_INFO_GLP_GAMELIST_ERROR_DET',config.language)).format(gamelist_load_error))
		
		#logger.info('End')
		logger.info(msg_local.get(('MSG_INFO_GLP_PRG_END',config.language)))
		self.running=False

#---------------------------------------------------------------------------------------------------
def get_args():
	parser = argparse.ArgumentParser(description=msg_local_arg.get(('MSG_ARG_PRG_DESCRIPTION',config.language)),epilog='(C) '+SOURCE_NAME+' '+VERSION)
	#Version Happigc
	#parser.add_argument(ARG_MODE,choices=[ARG_MODE_PATCH_FULL,ARG_MODE_PATCH_FORCE,ARG_MODE_CORRECT_ONLY,ARG_MODE_TOP_ONLY,ARG_MODE_STATS_ONLY,ARG_MODE_NOIMAGE_ONLY,ARG_MODE_GENERATE_SH,ARG_MODE_GENERATE_ROMCPY], default=ARG_MODE_PATCH_FULL, help=msg_local_arg.get(('MSG_ARG_MODE_HELP',config.language)))
	#Version Recalbox
	parser.add_argument(ARG_MODE,choices=[ARG_MODE_GENERATE_SH,ARG_MODE_GENERATE_ROMCPY], default=ARG_MODE_GENERATE_SH, help=msg_local_arg.get(('MSG_ARG_MODE_HELP',config.language)))
	parser.add_argument(ARG_LOG,choices=[ARG_LOG_DEBUG,ARG_LOG_INFO,ARG_LOG_ERROR], default=ARG_LOG_DEBUG, help=msg_local_arg.get(('MSG_ARG_LOG_HELP',config.language)))
	return parser.parse_args()

#---------------------------------------------------------------------------------------------------
#---------------------------------------- MAIN -----------------------------------------------------
#---------------------------------------------------------------------------------------------------
def main():
	
	#Test Arg
	args=get_args()
	
	#Init Log
	logger=Logger.logr
	if args.log==ARG_LOG_DEBUG:
		Logger.setLevel(logging.DEBUG)
	elif args.log==ARG_LOG_INFO:
		Logger.setLevel(logging.INFO)
	elif args.log==ARG_LOG_ERROR:
		Logger.setLevel(logging.ERROR)
	Logger.add_handler_console()
	
	#Lecture Configuration
	config.load_from_file()
	
	#Execution des patchs
	gameListPatch = GameListPatcher(config,'console',args.mode)
	gameListPatch.start()
	gameListPatch.join()
	
	#Fin
	sys.exit(0)

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	main()
