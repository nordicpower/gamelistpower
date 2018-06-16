#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                     - EMULATIONSTATION GAMELIST PATCH -                      #
#                                - MERGE XML -                                 #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.2.0  15/05/2017-02/07/2017 #
#------------------------------------------------------------------------------#
#0.2.0 - 02/07/2017 - Support des folders                                      #
################################################################################

#IMPORT STD---------------------------------------------------------------------
import os.path
import sys
import time
import shutil
import traceback
import argparse
from os.path import basename, splitext

#IMPORT NORDICPOWER--------------------------------------------------------------
from GameListXml import *
from GameListDir import *
from GameListTools import *
from GameListPatch import *

#CONSTANTS-----------------------------------------------------------------------
VERSION='0.2.0 BETA'

#CONSTANTS ARGUMENTS LANCEMENT---------------------------------------------------
ARG_FILE_SRC='file_src'
ARG_FILE_DEST='file_dest'

#MSG LOCALISATION----------------------------------------------------------------
config=Config()

msg_local={
('MSG_ERROR_MX_EXCEPTION','FR'):u'{} : {}',
('MSG_ERROR_MX_EXCEPTION','EN'):u'{} : {}',
('MSG_ERROR_MX_GAMEXML_SRC_NOT_FOUND','FR'):u'Fichier {} non trouv\u00E9 !',
('MSG_ERROR_MX_GAMEXML_SRC_NOT_FOUND','EN'):u'file {} not found !',
('MSG_INFO_MX_GAMEXML_DEST_NOT_FOUND','FR'):u'Fichier dest {} non trouv\u00E9, copie du fichier source',
('MSG_INFO_MX_GAMEXML_DEST_NOT_FOUND','EN'):u'destination file {} not found, make a simple copy',
('MSG_ERROR_MX_GAMEXML_DEST_COPY','FR'):u'Erreur dans la copie',
('MSG_ERROR_MX_GAMEXML_DEST_COPY','EN'):u'error during the copy',
('MSG_ERROR_MX_LOADING_GAMEXML','FR'):u'Erreur dans le fichier xml {}',
('MSG_ERROR_MX_LOADING_GAMEXML','EN'):u'xml error in {}',
('MSG_INFO_MX_PRG_END','FR'):u'Fusion termin\u00E9',
('MSG_INFO_MX_PRG_END','EN'):u'Merge end'
}

#---------------------------------------------------------------------------------------------------
def get_args():
	parser = argparse.ArgumentParser(description='fusion de fichiers gamelist.xml',epilog='(C) NORDIC POWER')
	parser.add_argument(ARG_FILE_SRC)
	parser.add_argument(ARG_FILE_DEST)
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
	
	logger.info('mergexml - NordicPower - Version '+VERSION)
	#Lecture Configuration
	config.load_from_file()
	
	if not os.path.isfile(args.file_src):
		logger.error(msg_local.get(('MSG_ERROR_MX_GAMEXML_SRC_NOT_FOUND',config.language)).format(args.file_src))
		sys.exit(1)
	
	#Chargement du fichier source
	gamesList_src  = GamesList()
	try:
		gamesList_src.import_xml_file(args.file_src)
	except MyError:
		logger.error(msg_local.get(('MSG_ERROR_MX_LOADING_GAMEXML',config.language)).format(args.file_src))
		sys.exit(1)
		
	#Pas de fichier destination, réalisation d'une simple copie de fichiers
	if not os.path.isfile(args.file_dest):
		try:
			shutil.copyfile(args.file_src, args.file_dest)
			logger.error(msg_local.get(('MSG_INFO_MX_GAMEXML_DEST_NOT_FOUND',config.language)).format(args.file_dest))
		except:
			pass
		sys.exit(0)

	#Chargement du fichier destination
	gamesList_dest = GamesList()
	try:
		gamesList_dest.import_xml_file(args.file_dest)
	except MyError:
		logger.error(msg_local.get(('MSG_ERROR_MX_LOADING_GAMEXML',config.language)).format(args.file_dest))
		sys.exit(1)
	
	#Fusion des XML
	for game_XML_src in gamesList_src.get_games():
	
		try:
			game_XML_dest = gamesList_dest.search_game_by_path(game_XML_src.path)
			
			#Game trouvé, la source écrase les infos de la destination
			game_XML_dest.path = game_XML_src.path
			if game_XML_src.name!='':game_XML_dest.name = game_XML_src.name
			if game_XML_src.desc!='':game_XML_dest.desc = game_XML_src.desc
			if game_XML_src.image!='':game_XML_dest.image = game_XML_src.image		
			if game_XML_src.rating!='':game_XML_dest.rating = game_XML_src.rating
			if game_XML_src.releasedate!='':game_XML_dest.releasedate = game_XML_src.releasedate
			if game_XML_src.developer!='':game_XML_dest.developer = game_XML_src.developer
			if game_XML_src.publisher!='':game_XML_dest.publisher = game_XML_src.publisher
			if game_XML_src.genre!='':game_XML_dest.genre = game_XML_src.genre
			if game_XML_src.players!='':game_XML_dest.players = game_XML_src.players
			if game_XML_src.ref_id!='':game_XML_dest.ref_id = game_XML_src.ref_id
			if game_XML_src.source!='':game_XML_dest.source = game_XML_src.source
			if game_XML_src.playcount!='':game_XML_dest.playcount = game_XML_src.playcount
			if game_XML_src.lastplayed!='':game_XML_dest.lastplayed = game_XML_src.lastplayed
			
			gamesList_dest.update_game(game_XML_dest)
			
		except MyError:
			#Game non trouvé, simple recopie
			game_XML_dest = Game()
			game_XML_dest.path = game_XML_src.path
			game_XML_dest.copy_from_game(game_XML_src)
			
			gamesList_dest.add_game(game_XML_dest)
	
	#Fusion des XML
	for folder_XML_src in gamesList_src.get_folders():
	
		try:
			folder_XML_dest = gamesList_dest.search_folder_by_path(folder_XML_src.path)
			
			#folder trouvé, la source écrase les infos de la destination
			folder_XML_dest.path = folder_XML_src.path
			if folder_XML_src.name!='':folder_XML_dest.name = folder_XML_src.name
			if folder_XML_src.desc!='':folder_XML_dest.desc = folder_XML_src.desc
			if folder_XML_src.image!='':folder_XML_dest.image = folder_XML_src.image
			if folder_XML_src.hidden!='':folder_XML_dest.hidden = folder_XML_src.hidden
			
			
			gamesList_dest.update_folder(folder_XML_dest)
			
		except MyError:
			#folder non trouvé, simple recopie
			folder_XML_dest = Folder()
			folder_XML_dest.path = folder_XML_src.path
			folder_XML_dest.name = folder_XML_src.name
			folder_XML_dest.desc = folder_XML_src.desc
			folder_XML_dest.image = folder_XML_src.image
			folder_XML_dest.hidden = folder_XML_src.hidden
			gamesList_dest.add_folder(folder_XML_dest)
			
	
	#STEP END - Sauvegarde si intervention sur le fichier--------------------------------------------
	if gamesList_dest.modified:
		
		if len(gamesList_dest.get_games())>SEUIL_SAUVEGARDE_BIGROM:
			#logger.debug(msg_local.get(('MSG_INFO_GLP_PRG_SAVE_BIGROM',config.language)).format(args.file_dest))
			gamesList_dest.save_xml_file(args.file_dest,False)
		else:
			#logger.debug(msg_local.get(('MSG_INFO_GLP_PRG_SAVE',config.language)).format(args.file_dest))
			gamesList_dest.save_xml_file(args.file_dest)

	logger.info(msg_local.get(('MSG_INFO_MX_PRG_END',config.language)))
	
	#Fin
	sys.exit(0)

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	main()
