#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                     - EMULATIONSTATION GAMELIST PATCH -                      #
#                                - CHECK XML -                                 #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.07 14/05/2017-09/09/2018 #
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
ARG_MODE_LOAD_ONLY='load'
ARG_MODE_NOIMAGE_ATTR='noimage_attribute'
ARG_MODE_NOGENRE_ATTR='nogenre_attribute'
ARG_MODE_NOREGION_ATTR='noregion_attribute'
ARG_MODE_HASH_MULTIPLE='hash_multiple'
ARG_FILE='file'

#---------------------------------------------------------------------------------------------------
def get_args():
	parser = argparse.ArgumentParser(description='file checker of gamelist.xml',epilog='(C) NORDIC POWER')
	parser.add_argument(ARG_MODE,choices=[ARG_MODE_LOAD_ONLY,ARG_MODE_NOIMAGE_ATTR,ARG_MODE_NOGENRE_ATTR,ARG_MODE_NOREGION_ATTR,ARG_MODE_HASH_MULTIPLE], default=ARG_MODE_LOAD_ONLY, help='mode')
	parser.add_argument(ARG_FILE)
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
	
	if os.path.getsize(args.file)==0:
		print('file not existing !')
		sys.exit(1)
	
	if args.mode==ARG_MODE_LOAD_ONLY:
		#Lecture charset
		print('charset:'+predict_encoding(args.file))
	
	gamesList = GamesList()
	try:
		gamesList.import_xml_file(args.file)
		if args.mode==ARG_MODE_LOAD_ONLY:
			print('file loading OK')
			sys.exit(0)
	except MyError:
		#cas fichier gamelist.xml mal formé, on passe au dossier de roms suivant
		print 'error while loading file !'
		sys.exit(1)
	
	bGameFound=False
	
	if args.mode==ARG_MODE_NOIMAGE_ATTR:
		for game_src in gamesList.get_games():
			if game_src.image=='':
				print('game '+game_src.name+' without image')
				bGameFound=True
		if bGameFound==False:
			print('no game found!')
		sys.exit(0)	
	
	if args.mode==ARG_MODE_NOGENRE_ATTR:
		for game_src in gamesList.get_games():
			if game_src.genre=='':
				print('game '+game_src.name+' without genre')
				bGameFound=True
		if bGameFound==False:
			print('no game found!')
		sys.exit(0)
	
	if args.mode==ARG_MODE_NOREGION_ATTR:
		for game_src in gamesList.get_games():
			if game_src.region=='':
				print('game '+game_src.name+' without region')
				bGameFound=True
		if bGameFound==False:
			print('no game found!')
		sys.exit(0)
	
	if args.mode==ARG_MODE_HASH_MULTIPLE:
		for game_src in gamesList.get_games():
			if " " in game_src.hashtag:
				print('game '+game_src.name+' with multiple files')
		
		sys.exit(0)
	#Fin
	sys.exit(0)

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	main()
