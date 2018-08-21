#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                     - EMULATIONSTATION GAMELIST PATCH -                      #
#                           - MERGE GAMELIST.XML -                             #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.06 21/08/2018-21/08/2018 #
#------------------------------------------------------------------------------#

#IMPORT STD---------------------------------------------------------------------
import os.path
import sys
import time
import shutil
import argparse
from os.path import basename, splitext

#IMPORT NORDICPOWER--------------------------------------------------------------
from glplib import *


#CONSTANTS ARGUMENTS LANCEMENT---------------------------------------------------
ARG_MODE='mode'
ARG_MODE_MERGE_NAME_ONLY='merge_name'
ARG_MODE_MERGE_DESC_ONLY='merge_desc'
ARG_FILE_SRC='file_source'
ARG_FILE_DST='file_destination'

#---------------------------------------------------------------------------------------------------
def get_args():
	parser = argparse.ArgumentParser(description='merge deux fichiers gamelist.xml',epilog='(C) NORDIC POWER')
	parser.add_argument(ARG_MODE,choices=[ARG_MODE_MERGE_NAME_ONLY,ARG_MODE_MERGE_DESC_ONLY], default=ARG_MODE_MERGE_NAME_ONLY, help='mode')
	parser.add_argument(ARG_FILE_SRC)
	parser.add_argument(ARG_FILE_DST)
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
	
	#Lecture Configuration
	config.load_from_file()
	
	if os.path.getsize(args.file_source)==0:
		print('Fichier source inexistant')
		sys.exit(1)
	
	if os.path.getsize(args.file_destination)==0:
		print('Fichier destination inexistant')
		sys.exit(1)
	
	
	gamesList_src = GamesList()
	try:
		gamesList_src.import_xml_file(args.file_source)
		print('Chargement Source OK')
		
	except MyError:
		#cas fichier gamelist.xml mal formé, on passe au dossier de roms suivant
		print 'Erreur de chargement Source !'
		sys.exit(1)
	
	gamesList_dst = GamesList()
	try:
		gamesList_dst.import_xml_file(args.file_destination)
		print('Chargement Destination OK')
		
	except MyError:
		#cas fichier gamelist.xml mal formé, on passe au dossier de roms suivant
		print 'Erreur de chargement Destination !'
		sys.exit(1)
	
	
	#Start Copy
	for game_src in gamesList_src.get_games():
		
		try:
			#Mise à jour metadata game	
			game_dst = gamesList_dst.search_game_by_path(game_src.path)
			if args.mode=='merge_name':
				if game_dst.name != game_src.name:
					print (game_src.name+' applied to ' + game_dst.name)
					game_dst.name = game_src.name
					gamesList_dst.update_game(game_dst)
				else:
					print (game_src.name+' not changed')
				
			if args.mode=='merge_desc':
				if game_dst.desc != game_src.desc:
					print (game_dst.name+' new description !')
					game_dst.desc = game_src.desc
					gamesList_dst.update_game(game_dst)
				else:
					print (game_dst.name+' description not changed')
					
		except MyError:
			#TODO : Ajout metadata game
			print (game_src.name+' not found')
			pass
	
	#Sauvegarde destination
	print ("Sauvegarde...")
	gamesList_dst.save_xml_file(args.file_destination)
	print ("ok")
	
	#Fin
	sys.exit(0)

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	main()
