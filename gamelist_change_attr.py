#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                     - EMULATIONSTATION GAMELIST PATCH -                      #
#                          --- CHANGE ATTRIBUT -----                           #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.10 09/09/2018-28/09/2018 #
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
ARG_MODE_COPY_REGION_FROM_PATH='copy_region_from_path'
ARG_MODE_COPY_EMPTY_REGION_FROM_PATH='copy_empty_region_from_path'
ARG_MODE_UPPER='upper'
ARG_MODE_UPPER_ALL='upper_all'
ARG_MODE_REMOVE='remove'
ARG_MODE_REMOVE_PLAYINFO='remove_playinfo'
ARG_MODE_ADD_EMPTY_TAG='add_emptytag'
ARG_MODE_REMOVE_EMPTY_TAG='remove_emptytag'
ARG_FILE='file'
ARG_OVERWRITE='--overwrite'
ARG_ATTR='--attribute'

#DICTIONNAIRES-------------------------------------------------------------------
dico_region = {}
##Plus récurrents
dico_region["USA"]="USA"
dico_region["Europe"]="EUROPE"
dico_region["France"]="FRANCE"
dico_region["Japan"]="JAPON"
dico_region["World"]="WORLD"
dico_region["USA, Europe"]="USA, EUROPE"
##Moins récurrents
dico_region["Australia"]="AUSTRALIE"
dico_region["Brazil"]="BRESIL"
dico_region["Japan,Europe"]="JAPON, EUROPE"
dico_region["Japan,Korea"]="JAPON, COREE"
dico_region["Korea"]="COREE"
dico_region["Russie"]="RUSSIE"
dico_region["Taiwan"]="TAIWAN"
dico_region["USA, Australia"]="USA, AUSTRALIE"
dico_region["USA, Korea"]="USA, COREE"


dico_upper = {}
dico_upper["&AMP;"]="&amp;"

#-------------------------------------------------------------------------------
def get_args():
	parser = argparse.ArgumentParser(description='change attribut of gamelist.xml',epilog='(C) NORDIC POWER')
	parser.add_argument(ARG_MODE,choices=[ARG_MODE_COPY_REGION_FROM_PATH,ARG_MODE_COPY_EMPTY_REGION_FROM_PATH,
		ARG_MODE_UPPER,ARG_MODE_UPPER_ALL,ARG_MODE_REMOVE,ARG_MODE_REMOVE_PLAYINFO,ARG_MODE_ADD_EMPTY_TAG,
		ARG_MODE_REMOVE_EMPTY_TAG], default=ARG_MODE_COPY_REGION_FROM_PATH, help='mode')
	parser.add_argument(ARG_FILE)
	parser.add_argument(ARG_OVERWRITE,action="store_true")
	parser.add_argument(ARG_ATTR)
	return parser.parse_args()

def upper_html(input_string):

	input_string=input_string.upper()
	
	for keyUpper in dico_upper.keys():
		input_string.replace(keyUpper,dico_upper[keyUpper])
	
	return input_string

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
	
	#Argument
	if args.attribute==None:
		args.attribute='name'
	if args.mode in [ARG_MODE_UPPER] and args.attribute not in GamesList().getGameXMLAttributeName():
		print('attribute '+args.attribute+' not supported !')
		sys.exit(1)
	if args.attribute=='hash':
		args.attribute='hashtag'
	
	if not os.path.isfile(args.file):
		print('File not existing !')
		sys.exit(1)
	
	#Chargement du fichier
	gamesList = GamesList()
	try:
		gamesList.import_xml_file(args.file)
	except MyError:
		#cas fichier gamelist.xml mal formé, on passe au dossier de roms suivant
		print 'Error while loading file !'
		sys.exit(1)
	
	bChanged=False
	if args.mode in [ARG_MODE_COPY_REGION_FROM_PATH,ARG_MODE_COPY_EMPTY_REGION_FROM_PATH]:
		for game in gamesList.get_games():
			if ((game.region=="" and args.mode==ARG_MODE_COPY_EMPTY_REGION_FROM_PATH) or (args.mode==ARG_MODE_COPY_REGION_FROM_PATH)):
				for cle in dico_region.keys():
					if "("+cle+")" in game.path and game.region=='':
						if args.mode==ARG_MODE_COPY_EMPTY_REGION_FROM_PATH:
							print('Add region '+dico_region[cle]+' to '+game.name)
						else:
							print('Update region '+dico_region[cle]+' to '+game.name)
						game.region=dico_region[cle]
						gamesList.update_game(game)
						bChanged=True
		
	if args.mode in [ARG_MODE_UPPER]:
		for game in gamesList.get_games():
			game.__dict__[args.attribute]=upper_html(game.__dict__[args.attribute])
			gamesList.update_game(game)
		bChanged=True
	
	if args.mode in [ARG_MODE_UPPER_ALL]:
		for game in gamesList.get_games():
			for xml_attr in gamesList.getGameXMLAttributeName_TextType():
				game.__dict__[xml_attr]=upper_html(game.__dict__[xml_attr])
			gamesList.update_game(game)
		bChanged=True
	
	if args.mode in [ARG_MODE_REMOVE]:
		for game in gamesList.get_games():
			game.__dict__[args.attribute]=""
			gamesList.update_game(game)
		bChanged=True
	
	if args.mode in [ARG_MODE_REMOVE_PLAYINFO]:
		for game in gamesList.get_games():
			for xml_attr in gamesList.getGameXMLAttributeName_TextType():
				game.playcount=""
				game.lastplayed=""
			gamesList.update_game(game)
		bChanged=True
	
	if args.mode in [ARG_MODE_ADD_EMPTY_TAG]:
		for game in gamesList.get_games():
			gamesList.update_game(game,False)
		bChanged=True
		
	if args.mode in [ARG_MODE_REMOVE_EMPTY_TAG]:
		for game in gamesList.get_games():
			gamesList.update_game(game)
		bChanged=True
	
	if bChanged:
		newfilemame = args.file.replace('.xml','_new.xml')
		if args.overwrite:
			newfilemame = args.file
		gamesList.save_xml_file(newfilemame,True)
	else:
		print 'No change !'
		
	#Fin
	sys.exit(0)

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	main()
