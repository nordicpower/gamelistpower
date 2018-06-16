#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                     - EMULATIONSTATION GAMELIST PATCH -                      #
#                                   - THEME -                                  #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.1.03 29/06/2017-21/09/2017 #
#------------------------------------------------------------------------------#

#IMPORT STD---------------------------------------------------------------------
import os.path
import shutil
import argparse

#IMPORT NORDICPOWER--------------------------------------------------------------
from GameListXml import *
from GameListTools import *
from GameListEsSystem import *

#CONSTANTS-----------------------------------------------------------------------
VERSION='0.1.03 BETA'

#CONSTANTS ARGUMENTS LANCEMENT---------------------------------------------------
ARG_MODE='mode'
ARG_MODE_REFRESH='refresh'
ARG_MODE_CHANGE='change'
ARG_MODE_CHANGE_THEME='theme'
ARG_MODE_CURRENT='current'
ARG_MODE_CHECK='check'
ARG_MODE_CHECK_KO='check_ko'
ARG_LANG='language'
ARG_LANG_FR="fr_FR"
ARG_LANG_EN="en_GB"

#MSG LOCALISATION----------------------------------------------------------------
config=Config()

msg_local={
('MSG_ERROR_THE_EXCEPTION','FR'):u'{} : {}',
('MSG_ERROR_THE_EXCEPTION','EN'):u'{} : {}',
('MSG_ERROR_THE_ARGUMENT_ERROR','FR'):u'Argument {} manquant',
('MSG_ERROR_THE_ARGUMENT_ERROR','EN'):u'Arg {} missing',
('MSG_ERROR_THE_ARGUMENT_ERROR','FR'):u'Theme {} inexistant',
('MSG_ERROR_THE_ARGUMENT_ERROR','EN'):u'Theme {} not found',
('MSG_INFO_THE_SET_THEME','FR'):u'Theme {} appliqu\u00E9',
('MSG_INFO_THE_SET_THEME','EN'):u'Theme {} is changed',
('MSG_INFO_THE_CURRENT_THEME','FR'):u'Theme actif {}',
('MSG_INFO_THE_CURRENT_THEME','EN'):u'Current theme is {}',
('MSG_INFO_THE_INFO_PLATEFORME_THEME','FR'):u'Plateforme {} Theme {} : {}',
('MSG_INFO_THE_INFO_PLATEFORME_THEME','EN'):u'Plateform {} Theme {} : {}',
('MSG_INFO_THE_INFO_PLATEFORME_THEME_COUNT','FR'):u'Total Plateforme {}/{} OK',
('MSG_INFO_THE_INFO_PLATEFORME_THEME_COUNT','EN'):u'Total Plateform {}/{} OK',
('MSG_INFO_THE_GEN_LAUNCHER','FR'):u'G\u00E9n\u00E9ration du laucher: {}',
('MSG_INFO_THE_GEN_LAUNCHER','EN'):u'Generate launcher: {}',
('MSG_CRITICAL_THE_ESSYSTEM_LOAD_ERROR','FR'):u'Erreur de chargement du fichier es_systems.cfg',
('MSG_CRITICAL_THE_ESSYSTEM_LOAD_ERROR','EN'):u'Error while loading es_systems.cfg'
}

#---------------------------------------------------------------------------------------------------
def get_args():
	parser = argparse.ArgumentParser(description='gestion du fichier es_configs.cfg',epilog='(C) NORDIC POWER')
	parser.add_argument(ARG_MODE,choices=[ARG_MODE_REFRESH,ARG_MODE_CHANGE,ARG_MODE_CURRENT,ARG_MODE_CHECK,ARG_MODE_CHECK_KO], default=ARG_MODE_REFRESH, help='mode')
	parser.add_argument(ARG_LANG,choices=[ARG_LANG_FR,ARG_LANG_EN], default=ARG_LANG_FR, help='language')
	parser.add_argument('-t',dest=ARG_MODE_CHANGE_THEME,nargs='*')
	return parser.parse_args()

#---------------------------------------------------------------------------------------------------
#---------------------------------------- MAIN -----------------------------------------------------
#---------------------------------------------------------------------------------------------------
def main():
	
	#Test Arg
	args=get_args()
	
	#Init Log
	logger=Logger.logr
	Logger.setLevel(logging.DEBUG)
	Logger.add_handler_console()
	
	logger.info('theme - NordicPower - Version '+VERSION)
	#Lecture Configuration
	config.load_from_file()
	#print config.emulation_station_settings
	
	#Chargement de la configuration
	es_Settings=ESSettings()
	es_Settings.import_es_settings(config.emulation_station_settings)
	
	#Regeneration des themes disponibles
	fileDirThemes=FileDirThemes(config.emulation_station_themes)
	fileDirThemes.read_themes()
		
	if args.mode in [ARG_MODE_REFRESH]:		
		#Suppression des sh de lancement
		suppr_name_wildcard = config.theme_sh_name.replace("{","").replace("}","*")
		os.system("rm -rf {}".format(os.path.join(config.theme_menu_sh_folder, suppr_name_wildcard )))
		#Regeneration des sh
		for dir_theme in sorted(fileDirThemes.theme_dict):
			#Definition du sh
			command = config.theme_sh_launch.format(dir_theme)
			name_file_launcher = config.theme_sh_name.format(dir_theme)
			fullpath_launcher = os.path.expanduser(config.theme_menu_sh_folder + os.sep + name_file_launcher)
			#Enregistrement
			try:
				launcher = open(fullpath_launcher,'w')
				launcher.write("#!/bin/bash -e")
				launcher.write("\n")
				launcher.write(command)
				launcher.close
				os.chmod(fullpath_launcher,0o777)
				logger.info(msg_local.get(('MSG_INFO_THE_GEN_LAUNCHER',config.language)).format(name_file_launcher))
			except Exception as exception:
				logger.warn(msg_local.get(('MSG_ERROR_THE_EXCEPTION',config.language)).format('refresh sh',type(exception).__name__))
		
		#Regeneration du menu--------
		gamesList = GamesList()
		try:
			gameListName=config.theme_menu_file_configxml.format(args.language)
			gamesList.import_xml_file(gameListName)
		except MyError:
			#cas fichier gamelist.xml mal formé, on passe au dossier de roms suivant
			gamelist_load_errors.append(GameListDirectory + os.sep + NOM_GAMELIST_XML)
			logger.error(msg_local.get(('MSG_ERROR_THE_EXCEPTION',config.language)).format('load config',type(exception).__name__))
			sys.exit(1)
		except Exception as exception:
			logger.error(msg_local.get(('MSG_ERROR_THE_EXCEPTION',config.language)).format('load config',type(exception).__name__))
			sys.exit(1)
			
		for dir_theme in sorted(fileDirThemes.theme_dict):
			#Mise à jour des noeuds game
			try:
				name_file_launcher = config.theme_sh_name.format(dir_theme)
				fullpath_launcher = '.' + os.sep + "themes" + os.sep + name_file_launcher
				game_XML = gamesList.search_game_by_path(fullpath_launcher)
				game_XML.name = "Theme " + fileDirThemes.theme_dict[dir_theme]
				game_XML.image=fileDirThemes.theme_img[dir_theme]
				gamesList.update_game(game_XML)
				
			except MyError:		
				#Pas de noeud game trouvé
				game_XML = Game()
				game_XML.path = fullpath_launcher
				#Ajout de l'entrée
				game_XML.name = "Theme " + fileDirThemes.theme_dict[dir_theme]
				game_XML.image=fileDirThemes.theme_img[dir_theme]
				gamesList.add_game(game_XML)
		
		#Sauvegarde		
		gamesList.save_xml_file(gameListName)
	
	elif args.mode in [ARG_MODE_CHANGE]:
		
		try:
			iter(args.theme)
		except:
			logger.error(msg_local.get(('MSG_ERROR_THE_ARGUMENT_ERROR',config.language)).format('-t'))
			sys.exit(1)
			
		#Changement du theme actif (1ière argument
		theme_found=False
		for dir_theme in sorted(fileDirThemes.theme_dict):
			
			if args.theme[0] in dir_theme:
				theme_found=True
				break
		if theme_found:
			es_Settings.conf_dict[("string","ThemeSet")]=args.theme[0]
			es_Settings.save_es_settings(config.emulation_station_settings)
			logger.info(msg_local.get(('MSG_INFO_THE_SET_THEME',config.language)).format(args.theme[0]))

		else:
			logger.error(msg_local.get(('MSG_ERROR_THE_ARGUMENT_ERROR',config.language)).format(args.theme[0]))
			sys.exit(1)

	elif args.mode in [ARG_MODE_CURRENT]:
		logger.info(msg_local.get(('MSG_INFO_THE_CURRENT_THEME',config.language)).format(es_Settings.conf_dict[("string","ThemeSet")]))

	elif args.mode in [ARG_MODE_CHECK,ARG_MODE_CHECK_KO]:
		logger.info(msg_local.get(('MSG_INFO_THE_CURRENT_THEME',config.language)).format(es_Settings.conf_dict[("string","ThemeSet")]))
		
		#Chargement du fichier es_systems.cfg (configuration EmulationStation)
		try:
			configs_ES = ESSystemList()		
			configs_ES.import_xml_file(config.emulation_station_systems)
		except Exception as exception:
			logger.critical(msg_local.get(('MSG_CRITICAL_THE_ESSYSTEM_LOAD_ERROR',config.language)).format(type(exception).__name__))
			sys.exit(1)
		
		count_system=0
		count_system_ok=0
		
		for system in configs_ES.get_systems():
			count_system+=1
			path_theme = config.emulation_station_themes + os.sep + es_Settings.conf_dict[("string","ThemeSet")] + os.sep + system.theme
			if os.path.isdir(path_theme):
				count_system_ok+=1
				if args.mode in [ARG_MODE_CHECK]:
					logger.info(msg_local.get(('MSG_INFO_THE_INFO_PLATEFORME_THEME',config.language)).format(system.name, system.theme,'OK'))
			else:
				logger.info(msg_local.get(('MSG_INFO_THE_INFO_PLATEFORME_THEME',config.language)).format(system.name, system.theme,'KO'))
		
		logger.info(msg_local.get(('MSG_INFO_THE_INFO_PLATEFORME_THEME_COUNT',config.language)).format(count_system_ok, count_system))
			
	#Fin
	sys.exit(0)

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	main()
