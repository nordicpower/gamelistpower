#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                     - EMULATIONSTATION GAMELIST PATCH -                      #
#                                - CHECK XML -                                 #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.1 14/05/2017-14/01/2019  #
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
ARG_MODE_EMPTY_ATTR='empty'
ARG_MODE_LIST_ATTR='list'
ARG_MODE_LIST_SI_ATTR='list_single'
ARG_MODE_LIST_FAVORITE='list_favorite'
ARG_MODE_LIST_HIDDEN='list_hidden'
ARG_MODE_COUNT_ATTR='count'
ARG_MODE_HASH='list_hash_multiple'
ARG_FILE='file'
ARG_ATTR='--attribute'

#---------------------------------------------------------------------------------------------------
def get_args():
	parser = argparse.ArgumentParser(description='file checker of gamelist.xml',epilog='(C) NORDIC POWER')
	parser.add_argument(ARG_MODE,choices=[ARG_MODE_LOAD_ONLY,ARG_MODE_EMPTY_ATTR,ARG_MODE_LIST_ATTR,ARG_MODE_LIST_SI_ATTR,ARG_MODE_COUNT_ATTR,ARG_MODE_HASH,ARG_MODE_LIST_FAVORITE,ARG_MODE_LIST_HIDDEN], default=ARG_MODE_LOAD_ONLY, help='mode')
	parser.add_argument(ARG_FILE)
	parser.add_argument(ARG_ATTR)
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
	
	if not os.path.isfile(args.file):
		print('file not existing !')
		sys.exit(1)

	if args.attribute==None:
		args.attribute='name'
	if args.mode==ARG_MODE_HASH:
		args.attribute='hash'
	if args.mode in [ARG_MODE_EMPTY_ATTR,ARG_MODE_LIST_ATTR,ARG_MODE_LIST_SI_ATTR,ARG_MODE_COUNT_ATTR] and args.attribute not in GamesList().getGameXMLAttributeName():
		print('attribute '+args.attribute+' not supported !')
		sys.exit(1)
	if args.attribute=='hash':
		args.attribute='hashtag'
	
	
	if args.mode==ARG_MODE_LOAD_ONLY:
		#Lecture charset
		print('charset:'+predict_encoding(args.file))
	
	gamesList = GamesList()
	try:
		gamesList.import_xml_file(args.file)
	except MyError:
		#cas fichier gamelist.xml mal formé, on passe au dossier de roms suivant
		print 'error while loading file !'
		sys.exit(1)
	
	#List des games par attribut vide
	if args.mode==ARG_MODE_LOAD_ONLY:
		print('file loading OK')
		
		bGameFound=False
		for game_src in gamesList.get_games():
			if game_src.path=="":
				print('game '+game_src.name+' without path !')
				bGameFound=True
		if bGameFound==False:
			print('check games ok')
		sys.exit(0)
	
	#List des games par attribut vide
	if args.mode==ARG_MODE_EMPTY_ATTR:
		bGameFound=False
		for game_src in gamesList.get_games():
			if game_src.__dict__[args.attribute]=="":
				print('game '+game_src.name+' without '+args.attribute)
				bGameFound=True
		if bGameFound==False:
			print('no game found!')
		sys.exit(0)	
		
	#List simple
	if args.mode==ARG_MODE_LIST_ATTR:
		for game_src in sorted(gamesList.get_games(),key=attrgetter(args.attribute,"name")):
			print(game_src.__dict__[args.attribute])
		sys.exit(0)	
	
	#Listage avec count occurence
	if args.mode in[ARG_MODE_COUNT_ATTR,ARG_MODE_LIST_SI_ATTR]:
		dico_count={}
		for game_src in gamesList.get_games():
			if game_src.__dict__[args.attribute] not in dico_count.keys():
				dico_count[game_src.__dict__[args.attribute]]=1
			else:
				dico_count[game_src.__dict__[args.attribute]]=dico_count[game_src.__dict__[args.attribute]]+1
			
		if args.mode in[ARG_MODE_COUNT_ATTR]:
			for key, value in sorted(dico_count.iteritems(), key=lambda (k,v): (v,k), reverse=True):
				print "%-40s: %3s" % (key, value)
				
		if args.mode in[ARG_MODE_LIST_SI_ATTR]:
			for key in sorted(dico_count.keys()):
				print "%s" % (key)
		
		sys.exit(0)	
		
	#Listage avec filtre
	if args.mode in [ARG_MODE_LIST_FAVORITE,ARG_MODE_LIST_HIDDEN]:
		result_filtered=[]
		search_value="true"
		if args.mode in [ARG_MODE_LIST_FAVORITE]:
			args.attribute="favorite"
		if args.mode in [ARG_MODE_LIST_HIDDEN]:
			args.attribute="hidden"
			
		for game_src in gamesList.get_games():
			if game_src.__dict__[args.attribute]==search_value:
				result_filtered.append(game_src.name)
		
		for name in sorted(result_filtered):
			print "%s" % (name)
		
		sys.exit(0)	
		
	if args.mode==ARG_MODE_HASH:
		for game_src in gamesList.get_games():
			if " " in game_src.hashtag:
				print('game '+game_src.name+' with multiple files')
		
		sys.exit(0)
	#Fin
	sys.exit(0)

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	main()
