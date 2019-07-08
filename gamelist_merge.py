#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                     - EMULATIONSTATION GAMELIST PATCH -                      #
#                           - MERGE GAMELIST.XML -                             #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.14 21/08/2018-08/07/2019 #
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
ARG_MODE_MERGE_ATTR_ONLY='merge_attr'
ARG_MODE_MERGE_FULL='merge_full'
ARG_FILE_SRC='file_source'
ARG_FILE_DST='file_destination'
ARG_METHOD='--method'
ARG_ATTR='--attribute'

#---------------------------------------------------------------------------------------------------
def get_args():
	parser = argparse.ArgumentParser(description='merge two files gamelist.xml',epilog='(C) NORDIC POWER')
	parser.add_argument(ARG_MODE,choices=[ARG_MODE_MERGE_NAME_ONLY,ARG_MODE_MERGE_ATTR_ONLY,ARG_MODE_MERGE_FULL], default=ARG_MODE_MERGE_NAME_ONLY, help='mode')
	parser.add_argument(ARG_FILE_SRC)
	parser.add_argument(ARG_FILE_DST)
	parser.add_argument(ARG_METHOD)
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
	
	if os.path.getsize(args.file_source)==0:
		print('source file not existing !')
		sys.exit(1)
	
	if os.path.getsize(args.file_destination)==0:
		print('destination file not existing !')
		sys.exit(1)
	
	#arguments
	if args.method!='':
		if args.method not in ['path','name','id']:
			print('method not supported !')
			sys.exit(1)
	else:
		args.method='path'
	
	if args.mode in [ARG_MODE_MERGE_ATTR_ONLY] and args.attribute not in GamesList().getGameXMLAttributeName():
		print('attribute '+args.attribute+' not supported !')
		sys.exit(1)
	if args.attribute=='hash':
		args.attribute='hashtag'
	if args.attribute=='':
		args.attribute='name'
	
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
	
	
	#MERGE GAME--------------------------------------------------------------------
	for game_src in gamesList_src.get_games():
		
		try:
			#Recherche
			if args.method=='path':
				game_dst = gamesList_dst.search_game_by_path(game_src.path)
			if args.method=='id':
				if game_src.ref_id!="" and game_src.ref_id!="0":
					game_dst_liste = gamesList_dst.search_games('ref_id',game_src.__dict__['ref_id'])
					if len(game_dst_liste)>0:
						game_dst = game_dst_liste[0]
					else:
						continue
				else:
					continue
			if args.method=='name':
				game_dst_liste = gamesList_dst.search_games('name',game_src.name)
				if len(game_dst_liste)>0:
					game_dst = game_dst_liste[0]
				else:
					continue
			
			#Mise à jour metadata game
			if args.mode==ARG_MODE_MERGE_NAME_ONLY:
				if game_dst.name != game_src.name:
					print (game_src.name+' applied to ' + game_dst.name)
					game_dst.name = game_src.name
					gamesList_dst.update_game(game_dst)
				else:
					print (game_src.name+' not changed')
				
			if args.mode==ARG_MODE_MERGE_ATTR_ONLY:
				if args.attribute=='id':
					if game_dst.__dict__['ref_id'] != game_src.__dict__['ref_id']:
						print (game_dst.name+' new id !')
						game_dst.__dict__['ref_id'] = game_src.__dict__['ref_id']
						gamesList_dst.update_game(game_dst)
					else:
						print (game_dst.name+' id not changed')
				else:
					if game_dst.__dict__[args.attribute] != game_src.__dict__[args.attribute]:
						print (game_dst.name+' new '+args.attribute+' !')
						game_dst.__dict__[args.attribute] = game_src.__dict__[args.attribute]
						gamesList_dst.update_game(game_dst)
					else:
						print (game_dst.name+' '+args.attribute+' not changed')
					
			if args.mode==ARG_MODE_MERGE_FULL:
				#game_dst.path = game_src.path
				if game_src.name!='':game_dst.name = game_src.name
				if game_src.desc!='':game_dst.desc = game_src.desc
				if game_src.image!='':game_dst.image = game_src.image		
				if game_src.rating!='':game_dst.rating = game_src.rating
				if game_src.releasedate!='':game_dst.releasedate = game_src.releasedate
				if game_src.developer!='':game_dst.developer = game_src.developer
				if game_src.publisher!='':game_dst.publisher = game_src.publisher
				if game_src.genre!='':game_dst.genre = game_src.genre
				if game_src.players!='':game_dst.players = game_src.players
				if game_src.ref_id!='':game_dst.ref_id = game_src.ref_id
				if game_src.source!='':game_dst.source = game_src.source
				if game_src.playcount!='':game_dst.playcount = game_src.playcount
				if game_src.lastplayed!='':game_dst.lastplayed = game_src.lastplayed
				gamesList_dst.update_game(game_dst)
				print (game_dst.name+' changed')
			
		except MyError:
			
			if args.mode in[ARG_MODE_MERGE_DESC_ONLY,ARG_MODE_MERGE_NAME_ONLY]:
				print (game_src.name+' not found')
			
			if args.mode == ARG_MODE_MERGE_FULL:
				game_dst = Game()
				game_dst.path = game_src.path
				game_dst.copy_from_game(game_src)
				gamesList_dst.add_game(game_dst)
			
			pass
	
	#MERGE FOLDER--------------------------------------------------------------------
	for folder_XML_src in gamesList_src.get_folders():
	
		try:
			folder_XML_dest = gamesList_dst.search_folder_by_path(folder_XML_src.path)
			
			#folder trouvé, la source écrase les infos de la destination
			folder_XML_dest.path = folder_XML_src.path
			if args.mode in[ARG_MODE_MERGE_NAME_ONLY,ARG_MODE_MERGE_FULL]:
				if folder_XML_src.name!='':folder_XML_dest.name = folder_XML_src.name
			if args.mode in[ARG_MODE_MERGE_DESC_ONLY,ARG_MODE_MERGE_FULL]:
				if folder_XML_src.desc!='':folder_XML_dest.desc = folder_XML_src.desc
			if args.mode in[ARG_MODE_MERGE_FULL]:
				if folder_XML_src.image!='':folder_XML_dest.image = folder_XML_src.image
				if folder_XML_src.hidden!='':folder_XML_dest.hidden = folder_XML_src.hidden
			gamesList_dst.update_folder(folder_XML_dest)
			
		except MyError:
			#folder non trouvé, simple recopie
			folder_XML_dest = Folder()
			folder_XML_dest.path = folder_XML_src.path
			folder_XML_dest.name = folder_XML_src.name
			folder_XML_dest.desc = folder_XML_src.desc
			folder_XML_dest.image = folder_XML_src.image
			folder_XML_dest.hidden = folder_XML_src.hidden
			gamesList_dst.add_folder(folder_XML_dest)
	
	#Sauvegarde destination
	print ("Saving...")
	gamesList_dst.save_xml_file(args.file_destination)
	print ("End")
	
	#Fin
	sys.exit(0)

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	main()
