#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                     - EMULATIONSTATION GAMELIST PATCH -                      #
#                                 - SORT XML -                                 #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.07 06/09/2018-09/09/2018 #
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
ARG_MODE_SORT_BY_PATH='path'
ARG_MODE_SORT_BY_NAME='name'
ARG_MODE_SORT_BY_REGION='region'
ARG_MODE_SORT_BY_DEVELOPER='developer'
ARG_MODE_SORT_BY_PUBLISHER='publisher'
ARG_MODE_SORT_BY_RELEASEDATE='releasedate'

ARG_FILE='file'

#---------------------------------------------------------------------------------------------------
def get_args():
	parser = argparse.ArgumentParser(description='tri de fichier gamelist.xml',epilog='(C) NORDIC POWER')
	parser.add_argument(ARG_MODE,choices=[ARG_MODE_SORT_BY_PATH,ARG_MODE_SORT_BY_NAME,ARG_MODE_SORT_BY_REGION,ARG_MODE_SORT_BY_DEVELOPER,ARG_MODE_SORT_BY_PUBLISHER,ARG_MODE_SORT_BY_RELEASEDATE], default=ARG_MODE_SORT_BY_PATH, help='mode')
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
		print('Fichier inexistant')
		sys.exit(1)
	
	#Chargement
	gamesList = GamesList()
	try:
		gamesList.import_xml_file(args.file)
		print('Loading file')
	except MyError:
		#cas fichier gamelist.xml mal formé, on passe au dossier de roms suivant
		print 'Error while loading !'
		sys.exit(1)
	
	#Tri
	if args.mode not in ['path','name','desc','image','rating','releasedate','developer','publisher','genre','players','playcount','lastplayed','region','hash']:
		print 'Error, unknow attribut '+args.mode+' !'
		sys.exit(1)
	
	print 'Sorting xml by ' + args.mode
	gamesList_sorted = GamesList()
	gamesList_sorted = gamesList.sort(args.mode)
	
	print 'Saving'
	newfilemame = args.file.replace('.xml','_sorted.xml')
	gamesList_sorted.save_xml_file(newfilemame,True)
	
	print 'New file available on '+newfilemame
	print 'End'
	
	#Fin
	sys.exit(0)

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	main()
