#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                     - EMULATIONSTATION GAMELIST PATCH -                      #
#                           - DIFF  GAMELIST.XML -                             #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.11 20/09/2018-11/01/2019 #
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
ARG_MODE_DIFF_XML='diff_xml'
ARG_MODE_DIFF_TXT='diff_txt'
ARG_FILE_SRC='file_source'
ARG_FILE_DST='file_destination'
ARG_VERBOSE='--verbose'
ARG_NOTUSEID='--notuseid'

#---------------------------------------------------------------------------------------------------
def get_args():
	parser = argparse.ArgumentParser(description='diff two files gamelist.xml',epilog='(C) NORDIC POWER')
	parser.add_argument(ARG_MODE,choices=[ARG_MODE_DIFF_XML,ARG_MODE_DIFF_TXT], default=ARG_MODE_DIFF_XML, help='mode')
	parser.add_argument(ARG_FILE_SRC)
	parser.add_argument(ARG_FILE_DST)
	parser.add_argument(ARG_VERBOSE,action="store_true")
	parser.add_argument(ARG_NOTUSEID,action="store_true")
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
	
	if not os.path.isfile(args.file_source):
		print('source file not existing !')
		sys.exit(1)
	
	if not os.path.isfile(args.file_destination):
		print('destination file not existing !')
		sys.exit(1)
	
	
	gamesList_src = GamesList()
	try:
		gamesList_src.import_xml_file(args.file_source)
		print('source file loading OK')
		
	except MyError:
		#cas fichier gamelist.xml mal formé, on passe au dossier de roms suivant
		print 'error while loading source file !'
		sys.exit(1)
	
	gamesList_dst = GamesList()
	try:
		gamesList_dst.import_xml_file(args.file_destination)
		print('destination file loading OK')
		
	except MyError:
		#cas fichier gamelist.xml mal formé, on passe au dossier de roms suivant
		print 'error while loading destination file !'
		sys.exit(1)
	
	print ("Search...")
	#DIFF GAME--------------------------------------------------------------------
	search_attrs=['hash','path','name']
	if not args.notuseid:
		search_attrs.append('id')
		
	nb_in_dest={}
	for search_attr in search_attrs:
		nb_in_dest[search_attr]=0
	
	
	gamesList_notfound=GamesList()
	gamesList_notfound.create_root_xml()
	
	for game_src in gamesList_src.get_games():
		
		bRomFound=False
		
		#Recherche par + méthodes
		for search_attr in search_attrs:
			try:
				if search_attr=='path':
					games_dst = gamesList_dst.search_game_by_path(game_src.path)
					bRomFound=True
					pass
				elif search_attr=='hash':
					if game_src.__dict__['hashtag']!="":
						games_dst = gamesList_dst.search_games(search_attr,game_src.__dict__['hashtag'])
						bRomFound=len(games_dst)>0
				elif search_attr in ['name']:
					games_dst = gamesList_dst.search_games(search_attr,game_src.__dict__[search_attr])
					bRomFound=len(games_dst)>0
				elif search_attr in ['id']:
					if game_src.ref_id!="" and game_src.ref_id!="0":
						games_dst = gamesList_dst.search_games('ref_id',game_src.__dict__['ref_id'])
						bRomFound=len(games_dst)>0
					
				if bRomFound:
					game_src.specific='FOUND'
					nb_in_dest[search_attr]=nb_in_dest[search_attr]+1
					if args.verbose :
						print(game_src.name+' found in destination by '+search_attr)
					break
			except MyError:
				#not found, next search
				pass
			
		#Roms non trouvés
		if not bRomFound:
			gamesList_notfound.add_game(game_src)
	
	#AFFICHAGE GAME--------------------------------------------------------------------
	if args.mode==ARG_MODE_DIFF_TXT:
		for game_not_found in gamesList_notfound.get_games():
			print(game_not_found.name+' not found (hash='+game_not_found.hashtag+')')
		
	if args.mode==ARG_MODE_DIFF_XML:
		newfilemame = args.file_source.replace('.xml','_diff.xml')
		print ("Saving to ..." + newfilemame)
		gamesList_notfound.save_xml_file(newfilemame)
	
	print('')
	print('Game in source: '+str(len(gamesList_src.get_games())))
	print('Game in dest  : '+str(len(gamesList_dst.get_games())))
	nb_total=0
	for search_attr in search_attrs:
		nb_total+=nb_in_dest[search_attr]
		print ('Find in two files by '+search_attr+' : '+str(nb_in_dest[search_attr]))
	print('Total Find in two files : '+str(nb_total)+' '+str(100*nb_total/len(gamesList_src.get_games()))+'%')
	print('Total Not find :'+str(len(gamesList_notfound.get_games())))
	print('End')
	
	#Fin
	sys.exit(0)

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	main()
