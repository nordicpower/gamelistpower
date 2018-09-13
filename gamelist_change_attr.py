#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                     - EMULATIONSTATION GAMELIST PATCH -                      #
#                          --- CHANGE ATTRIBUT -----                           #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.08 09/09/2018-11/09/2018 #
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
ARG_FILE='file'*
ARG_OVERWRITE='--overwrite'

#DICTIONNAIRE--------------------------------------------------------------------
dico_region = {}
dico_region["Europe"]="EUROPE"
dico_region["USA"]="USA"
dico_region["Japan"]="JAPON"
dico_region["USA, Europe"]="USA, EUROPE"
dico_region["France"]="FRANCE"
dico_region["World"]="WORLD"
dico_region["Japan,Europe"]="JAPON, EUROPE"
dico_region["Japan,Korea"]="JAPON, COREE"
dico_region["Russie"]="RUSSIE"

#---------------------------------------------------------------------------------------------------
def get_args():
	parser = argparse.ArgumentParser(description='change attribut of gamelist.xml',epilog='(C) NORDIC POWER')
	parser.add_argument(ARG_MODE,choices=[ARG_MODE_COPY_REGION_FROM_PATH,ARG_MODE_COPY_EMPTY_REGION_FROM_PATH], default=ARG_MODE_COPY_REGION_FROM_PATH, help='mode')
	parser.add_argument(ARG_FILE)
	parser.add_argument(ARG_OVERWRITE,action="store_true")
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
	
	#Chargement du fichier
	gamesList = GamesList()
	try:
		gamesList.import_xml_file(args.file)
	except MyError:
		#cas fichier gamelist.xml mal formé, on passe au dossier de roms suivant
		print 'error while loading file !'
		sys.exit(1)
	
	bChanged=False
	if args.mode in [ARG_MODE_COPY_REGION_FROM_PATH,ARG_MODE_COPY_EMPTY_REGION_FROM_PATH]:
		for game in gamesList.get_games():
			if ((game.region=="" and args.mode==ARG_MODE_COPY_EMPTY_REGION_FROM_PATH) or (args.mode==ARG_MODE_COPY_REGION_FROM_PATH)):
				for cle in dico_region.keys():
					if "("+cle+")" in game.path and game.region=='':
						if args.mode==ARG_MODE_COPY_EMPTY_REGION_FROM_PATH:
							print('Add region '+dico_region[cle]+' to '+game.name)
						else
							print('Update region '+dico_region[cle]+' to '+game.name)
						game.region=dico_region[cle]
						gamesList.update_game(game)
						bChanged=True
		
	if bChanged:
		print 'Saving'
		newfilemame = args.file.replace('.xml','_sorted.xml')
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
