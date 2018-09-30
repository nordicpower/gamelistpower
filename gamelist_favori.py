#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                     - EMULATIONSTATION GAMELIST PATCH -                      #
#                     - IMPORT / EXPORT FAVORI/PLAY INFO -                     #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.10 23/10/2018-27/10/2018 #
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
ARG_MODE_IMPORT='import'
ARG_MODE_EXPORT='export'
ARG_VERBOSE='--verbose'
ARG_PLAYINFO='--playinfo'
ARG_HIDDEN='--hidden'
ARG_FILENAME='--filename'

#---------------------------------------------------------------------------------------------------
def get_args():
	parser = argparse.ArgumentParser(description='file checker of gamelist.xml',epilog='(C) NORDIC POWER')
	parser.add_argument(ARG_MODE,choices=[ARG_MODE_IMPORT,ARG_MODE_EXPORT], default=ARG_MODE_EXPORT, help='mode')
	parser.add_argument(ARG_VERBOSE,action="store_true")
	parser.add_argument(ARG_PLAYINFO,action="store_true")
	parser.add_argument(ARG_HIDDEN,action="store_true")
	parser.add_argument(ARG_FILENAME)
	return parser.parse_args()

#---------------------------------------------------------------------------------------------------
#---------------------------------------- MAIN -----------------------------------------------------
#---------------------------------------------------------------------------------------------------
def main():
	
	#Test Arg
	args=get_args()
	if args.filename is None:
		args.filename='gamelistexport.xml'
	
	#Init Log
	logger=Logger.logr
	Logger.setLevel(logging.DEBUG)
	Logger.add_handler_console()
	
	#Lecture Configuration
	config.load_from_file()
	
	#Gestion des GameExport
	gamesListExport = GamesListExport()
	filename = os.path.join(config.rootPath,args.filename)
	if args.mode==ARG_MODE_IMPORT:
		if not os.path.isfile(filename):
			print('File '+ filename +' not existing !')
			sys.exit(1)
		try:
			gamesListExport.import_xml_file(filename)
		except MyError:
			print 'error while loading '+filename+' !'
			sys.exit(1)
	else:
		gamesListExport.create_root_xml()	
	
	#Chargement du fichier es_systems.cfg (configuration EmulationStation)
	try:
		configs_ES = ESSystemList()
		configs_ES.import_xml_file(config.emulation_station_systems)
	except Exception as exception:
		print('Error while loading es_systems.cfg...')
		sys.exit(1)
	
	#Boucle sur les plateformes
	for plateform in sorted(configs_ES.get_systems(),key=attrgetter('name')):
		
		#Chargement
		loaded=False		
		gamesList_IE = GamesList()
		filename_IE = os.path.join(plateform.path,'gamelist.xml')
		try:
			print('Loading '+filename_IE+' ...')
			if os.path.isfile(filename_IE):
				gamesList_IE.import_xml_file(filename_IE)
				loaded=True
		
		except MyError:
			#cas fichier gamelist.xml mal formé, on passe au dossier de roms suivant
			print 'error while loading '+plateform.name+' !'
		
		if not loaded:
			continue
		
		if args.mode==ARG_MODE_EXPORT:
			#Recherche
			print('Searching...')
			for game in gamesList_IE.get_games():
				if game.favorite=='true' or (args.hidden and game.hidden=='true') or (args.playinfo and (game.lastplayed!="" or game.playcount!="")):
					favori = GameExport()
					favori.import_from_game(plateform.name,plateform.path,game,True,True)
					gamesListExport.add_game(favori)
		
		if args.mode==ARG_MODE_IMPORT:
			#Recherche
			search_attrs=['hash','path','name']
			print('Searching in '+plateform.name + ' ('+plateform.path+')')
			bUpdateGameList=False
			
			for gameExport in gamesListExport.get_games_by_plateformPath(plateform.path):
				
				bRomFound = False
				games_dst = Game()
				for search_attr in search_attrs:
					try:
						if search_attr=='path':
							games_dst = gamesList_IE.search_game_by_path(gameExport.path)
							bRomFound=True
							pass
						elif search_attr=='hash':
							if gameExport.__dict__['hashtag']!="":
								games_dst = gamesList_IE.search_games(search_attr,gameExport.__dict__['hashtag'])
								if len(games_dst)>0:
									bRomFound=True
									games_dst = games_dst[0]
						elif search_attr=='name':
							games_dst = gamesList_IE.search_games(search_attr,gameExport.__dict__[search_attr])
							if len(games_dst)>0:
								bRomFound=True
								games_dst = games_dst[0]
				
					except MyError:
						#not found, next search
						pass
			
				if bRomFound:		
					if gameExport.favorite=='true' or (args.hidden and gameExport.hidden=='true') or (args.playinfo and (gameExport.lastplayed!="" or gameExport.playcount!="")):
						gameExport.export_to_game(games_dst,args.playinfo,args.hidden)
						gamesList_IE.update_game(games_dst)
						bUpdateGameList=True
						if gameExport.hidden=='true':
							print(gameExport.name+ ' (hidden)')
						else:
							print(gameExport.name)
							
			if bUpdateGameList:
				print ("Saving to "+filename_IE+" ...")
				gamesList_IE.save_xml_file(filename_IE)
				
	if args.mode==ARG_MODE_EXPORT:
		#Sauvegarde	
		print ("Saving to "+filename)
		gamesListExport.save_xml_file(filename)
	
	#Fin
	sys.exit(0)

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	main()
