#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                     - EMULATIONSTATION GAMELIST PATCH -                      #
#                          --- CHANGE ATTRIBUT -----                           #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.14 09/09/2018-28/07/2019 #
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
ARG_MODE_COPY_EMPTY_REGION_FROM_NAME='copy_empty_region_from_name'
ARG_MODE_COPY_DEV2PUBLISHER='copy_empty_publisher_from_developer'
ARG_MODE_COPY_PUBLISHER2DEV='copy_empty_developer_from_publisher'
ARG_MODE_COPY_GENRE_FROM_DESC='copy_genre_from_desc'
ARG_MODE_UPPER='upper'
ARG_MODE_UPPER_ALL='upper_all'
ARG_MODE_REMOVE='remove'
ARG_MODE_REMOVE_PLAYINFO='remove_playinfo'
ARG_MODE_ADD_EMPTY_TAG='add_emptytag'
ARG_MODE_ADD_REGION_TITLE='add_region_title'
ARG_MODE_REMOVE_EMPTY_TAG='remove_emptytag'
ARG_MODE_REMOVE_REGION_TITLE='remove_region_title'
ARG_MODE_REMOVE_ID='remove_id'
ARG_MODE_CLEAN_PLAYERS='clean_players'
ARG_MODE_CLEAN_DESC='clean_desc'
ARG_MODE_CLEAN_NAME='clean_name'
ARG_MODE_CLEAN_DATE='clean_date'
ARG_MODE_CLEAN_GENRE='clean_genre'
ARG_MODE_CLEAN_DEVELOPER='clean_developer'
ARG_MODE_CLEAN_PUBLISHER='clean_publisher'
ARG_MODE_CLEAN_ALL='clean_all'
ARG_FILE='file'
ARG_OVERWRITE='--overwrite'
ARG_ATTR='--attribute'

#DICTIONNAIRES-------------------------------------------------------------------
dico_region = {}
##Plus récurrents
dico_region["USA"]="USA"
dico_region["U"]="USA"
dico_region["E"]="EUROPE"
dico_region["Eu"]="EUROPE"
dico_region["Europe"]="EUROPE"
dico_region["F"]="FRANCE"
dico_region["Fr"]="FRANCE"
dico_region["France"]="FRANCE"
dico_region["De"]="ALLEMAGNE"
dico_region["Germany"]="ALLEMAGNE"
dico_region["J"]="JAPON"
dico_region["Japan"]="JAPON"
dico_region["Japon"]="JAPON"
dico_region["World"]="WORLD"
dico_region["USA,Europe"]="USA, EUROPE"
dico_region["USA, Europe"]="USA, EUROPE"
##Moins récurrents
dico_region["Australia"]="AUSTRALIE"
dico_region["Europe, Australia"]="EUROPE, AUSTRALIE"
dico_region["Brazil"]=u"BR\u00C9SIL"
dico_region["Canada"]="CANADA"
dico_region["China"]="CHINE"
dico_region["Japan,Europe"]="JAPON, EUROPE"
dico_region["Japan, Europe"]="JAPON, EUROPE"
dico_region["Japan,Korea"]=u"JAPON, COR\u00C9E"
dico_region["Japan, Korea"]=u"JAPON, COR\u00C9E"
dico_region["Japan, USA"]="JAPON, USA"
dico_region["Japan,USA"]="JAPON, USA"
dico_region["Korea"]=u"COR\u00C9E"
dico_region["Russie"]="RUSSIE"
dico_region["Taiwan"]="TAIWAN"
dico_region["USA, Australia"]="USA, AUSTRALIE"
dico_region["USA,Australia"]="USA, AUSTRALIE"
dico_region["USA, Korea"]=u"USA, COR\u00C9E"
dico_region["USA,Korea"]=u"USA, COR\u00C9E"
dico_region["Sweden"]="SUEDE"

dico_upper = {}
dico_upper["&AMP;"]="&amp;"
dico_upper["&NBSP;"]="&nbsp;"

dico_genre = {}
##Plus récurrents
dico_genre["JEU D'ACTION HORRIFIQUE"]="ACTION, HORREUR"
dico_genre["JEU D'ACTION ET DE CONDUITE"]="ACTION, CONDUITE"

dico_genre["JEU DE TIR"]="TIR"
dico_genre["UN BEAT'EM ALL"]="TIR"
dico_genre["JEU D'ACTION/TIR"]="TIR"

dico_genre["JEU DE PLATES-FORMES"]="PLATEFORME"
dico_genre["JEU DE PLATEFORME"]="PLATEFORME"
dico_genre["JEU DE PLATE-FORME"]="PLATEFORME"
dico_genre["JEU DE PLATE FORME"]="PLATEFORME"
dico_genre["JEU D'ACTION ET DE PLATES-FORMES"]="PLATEFORME"
dico_genre["JEU D'ACTION/PLATE-FORME"]="PLATEFORME"
dico_genre["JEU D'ACTION PLATE-FORME"]="PLATEFORME"
dico_genre["JEU D'ACTION/PLATES-FORMES"]="PLATEFORME"
dico_genre["JEU D'ACTION PLATES-FORMES"]="PLATEFORME"
dico_genre["PLATFORM GAME"]="PLATEFORME"
dico_genre["PLATFORM ACTION GAME"]="PLATEFORME"
dico_genre["PLATFORM VIDEO GAME"]="PLATEFORME"
dico_genre[u"JEU VID\u00C9O DE PLATES-FORMES"]="PLATEFORME"

dico_genre["JEU D'ACTION-SIMULATION"]="SIMULATION"
dico_genre["JEU D'ACTION/SIMULATION"]="SIMULATION"
dico_genre["JEU D'ACTION SIMULATION"]="SIMULATION"

dico_genre["JEU D'ACTION-AVENTURE"]="AVENTURE"
dico_genre["JEU D'ACTION/AVENTURE"]="AVENTURE"
dico_genre["JEU D'ACTION AVENTURE"]="AVENTURE"
dico_genre["JEU D'ACTION ET D'AVENTURE"]="AVENTURE"

dico_genre["JEU D'ACTION/COURSE"]="COURSE"

dico_genre[u"JEU D'ACTION REFLEXION"]=u"ACTION, R\u00C9FLEXION"
dico_genre[u"JEU D'ACTION-REFLEXION"]=u"ACTION, R\u00C9FLEXION"
dico_genre[u"JEU D'ACTION/REFLEXION"]=u"ACTION, R\u00C9FLEXION"
dico_genre[u"JEU D'ACTION R\u00C9FLEXION"]=u"ACTION, R\u00C9FLEXION"
dico_genre[u"JEU D'ACTION-R\u00C9FLEXION"]=u"ACTION, R\u00C9FLEXION"
dico_genre[u"JEU D'ACTION/R\u00C9FLEXION"]=u"ACTION, R\u00C9FLEXION"
dico_genre[u"JEU DE ACTION/R\u00C9FLEXION"]=u"ACTION, R\u00C9FLEXION"

dico_genre[u"JEU DE R\u00C9FLEXION"]=u"R\u00C9FLEXION"

dico_genre[u"JEU D'ACTION-STRATEGIE"]=u"ACTION, STRAT\u00C9GIE"
dico_genre[u"JEU D'ACTION/STRATEGIE"]=u"ACTION, STRAT\u00C9GIE"
dico_genre[u"JEU D'ACTION-STRATEGIE"]=u"ACTION, STRAT\u00C9GIE"
dico_genre[u"JEU D'ACTION-STRAT\u00C9GIE"]=u"ACTION, STRAT\u00C9GIE"
dico_genre[u"JEU D'ACTION/STRAT\u00C9GIE"]=u"ACTION, STRAT\u00C9GIE"
dico_genre[u"JEU D'ACTION STRAT\u00C9GIE"]=u"ACTION, STRAT\u00C9GIE"

dico_genre[u"JEU DE STRAT\u00C9GIE"]=u"STRAT\u00C9GIE"

dico_genre[u"JEU DE ROLE ORIENT\u00C9 ACTION"]=u"ACTION, JEU DE R\u00D4LES"
dico_genre[u"JEU DE R\u00D4LE ORIENT\u00C9 ACTION"]=u"ACTION, JEU DE R\u00D4LES"
dico_genre[u"ACTION/JEU DE ROLE"]=u"ACTION, JEU DE R\u00D4LES"
dico_genre[u"ACTION/JEU DE R\u00D4LE"]=u"ACTION, JEU DE R\u00D4LES"
dico_genre["RPG/ACTION GAME"]=u"ACTION, JEU DE R\u00D4LES"
dico_genre["JEU D'ACTION/RPG"]=u"ACTION, JEU DE R\u00D4LES"
dico_genre[u"JEU DE ROLE"]=u"JEU DE R\u00D4LES"
dico_genre[u"JEU DE R\u00D4LE"]=u"JEU DE R\u00D4LES"
dico_genre[u"ROLE-PLAYING GAME"]=u"JEU DE R\u00D4LES"

dico_genre["JEU ACTION/COMBAT"]="ACTION, COMBAT"
dico_genre["JEU MIXANT ACTION ET COMBAT"]="ACTION, COMBAT"

dico_genre[u"JEU DE COMBAT"]=u"COMBAT"

dico_genre[u"LUDO-EDUCATIF"]=u"LUDO-\u00C9DUCATIF"
dico_genre[u"LUDO-\u00C9DUCATIF"]=u"LUDO-\u00C9DUCATIF"

dico_genre[u"JEU D'ACTION / PUZZLE"]=u"ACTION, PUZZLE-GAME"

dico_genre[u"JEU DE PUZZLE-GAME"]=u"PUZZLE-GAME"
dico_genre[u"IS A PUZZLE GAME"]=u"PUZZLE-GAME"

dico_genre[u"JEU DE BEAT'EM ALL"]=u"BEAT'EM ALL"

dico_genre[u"JEU DE SHOOT'EM UP"]=u"SHOOT'EM UP"
dico_genre[u"JEU DE SHOOT 'EM UP"]=u"SHOOT'EM UP"

dico_genre[u"JEU DE CASSE-BRIQUE"]=u"CASSE-BRIQUES"
dico_genre[u"JEU DE CASSE BRIQUE"]=u"CASSE-BRIQUES"
dico_genre[u"JEU VID\u00C9O DE CASSE-BRIQUES"]=u"CASSE-BRIQUES"

dico_genre[u"JEU DE MOTO"]=u"CONDUITE, MOTO"

dico_genre[u"JEU VIDÉO DE BASEBALL"]=u"SPORT, BASEBALL"
dico_genre[u"JEU DE BASE-BALL"]=u"SPORT, BASEBALL"
dico_genre[u"JEU DE BASEBALL"]=u"SPORT, BASEBALL"
dico_genre[u"BASKETBALL GAME"]=u"SPORT, BASKET"
dico_genre[u"POOL SIMULATION"]=u"SPORT, BILLARD"
dico_genre[u"BOWLING GAME"]=u"SPORT, BOWLING"
dico_genre[u"BOXING GAME"]=u"SPORT, BOXE"
dico_genre[u"PRO WRESTLING GAME"]=u"SPORT, CATCH"
dico_genre[u"JEU DE CATCH"]=u"SPORT, CATCH"
dico_genre[u"SOCCER GAME"]=u"SPORT, FOOTBALL"
dico_genre[u"JEU DE FOOTBALL"]=u"SPORT, FOOTBALL"
dico_genre[u"ICE HOCKEY GAME"]=u"SPORT, HOCKEY SUR GLACE"
dico_genre[u"GOLF SIMULATOR"]=u"SPORT, GOLF"
dico_genre[u"GOLF GAME"]=u"SPORT, GOLF"
dico_genre[u"JEU DE GOLF"]=u"SPORT, GOLF"
dico_genre[u"RUGBY GAME"]=u"SPORT, RUGBY"

dico_genre[u"SHOOT'EM UP"]=u"SHOOT'EM UP"

#en bas car moins priorité et permet de capter les chaines plus longues
#dico_genre["JEU D'ACTION "]="ACTION" #pose problème
dico_genre["JEU D'ARCADE"]="ACTION"
dico_genre["ACTION GAME"]="ACTION"

#-------------------------------------------------------------------------------
def get_args():
	parser = argparse.ArgumentParser(description='change attribut of gamelist.xml',epilog='(C) NORDIC POWER')
	parser.add_argument(ARG_MODE,choices=[ARG_MODE_UPPER,ARG_MODE_UPPER_ALL,
		ARG_MODE_COPY_REGION_FROM_PATH,ARG_MODE_COPY_EMPTY_REGION_FROM_PATH,ARG_MODE_COPY_EMPTY_REGION_FROM_NAME,
		ARG_MODE_COPY_GENRE_FROM_DESC,ARG_MODE_REMOVE_ID,ARG_MODE_CLEAN_GENRE,
		ARG_MODE_CLEAN_DEVELOPER,ARG_MODE_CLEAN_PUBLISHER,
		ARG_MODE_REMOVE,ARG_MODE_REMOVE_PLAYINFO,ARG_MODE_ADD_EMPTY_TAG,
		ARG_MODE_REMOVE_EMPTY_TAG,ARG_MODE_COPY_DEV2PUBLISHER,ARG_MODE_COPY_PUBLISHER2DEV,
		ARG_MODE_ADD_REGION_TITLE,ARG_MODE_REMOVE_REGION_TITLE,
		ARG_MODE_CLEAN_PLAYERS,ARG_MODE_CLEAN_DESC,ARG_MODE_CLEAN_ALL,ARG_MODE_CLEAN_NAME,ARG_MODE_CLEAN_DATE], 
		default=ARG_MODE_COPY_REGION_FROM_PATH, help='mode')
	parser.add_argument(ARG_FILE)
	parser.add_argument(ARG_OVERWRITE,action="store_true")
	parser.add_argument(ARG_ATTR)
	return parser.parse_args()

def upper_html(input_string):

	if 'HTTPS:' in input_string or 'https:' in input_string :
		return input_string.lower()
	if 'HTTP:' in input_string or 'http:' in input_string :
		return input_string.lower()
		
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
	
	if args.mode in [ARG_MODE_REMOVE_ID]:
		for game in gamesList.get_games():
			if game.ref_id in game.path and game.source=="nordicpower.fr":
				game.ref_id=""
				print('Remove id to '+game.name)
				gamesList.update_game(game)
				bChanged=True
	
	if args.mode in [ARG_MODE_COPY_REGION_FROM_PATH,ARG_MODE_COPY_EMPTY_REGION_FROM_PATH]:
		for game in gamesList.get_games():
			if ((game.region=="" and args.mode==ARG_MODE_COPY_EMPTY_REGION_FROM_PATH) or (args.mode==ARG_MODE_COPY_REGION_FROM_PATH)):
				for cle in dico_region.keys():
					if "("+cle.upper()+")" in game.path.upper() and game.region=='':
						if args.mode==ARG_MODE_COPY_EMPTY_REGION_FROM_PATH:
							print('Add region '+dico_region[cle]+' to '+game.name)
						else:
							print('Update region '+dico_region[cle]+' to '+game.name)
						game.region=dico_region[cle]
						gamesList.update_game(game)
						bChanged=True
						break
	
	if args.mode in [ARG_MODE_COPY_GENRE_FROM_DESC]:
		for game in gamesList.get_games():
			for cle in dico_genre.keys():
				try:
					if cle.upper() in game.desc.upper():
						if game.genre==dico_genre[cle]:
							#si 1ière occurence trouvé et identique au genre, plus d'autres recherche à faire
							break
						else:
							print('Update genre '+dico_genre[cle]+' to '+game.name)
							game.genre=dico_genre[cle]
							gamesList.update_game(game)
							bChanged=True
							break
				except:
					print('Exception sur '+cle.upper())
					break
	
	if args.mode in [ARG_MODE_COPY_EMPTY_REGION_FROM_NAME]:
		for game in gamesList.get_games():
			if game.region=="":
				for cle in dico_region.keys():
					if ("("+cle.upper()+")" in game.name.upper() or "["+cle.upper()+"]" in game.name.upper() ) and game.region=='':
						print('Add region '+dico_region[cle]+' to '+game.name)
						game.region=dico_region[cle]
						gamesList.update_game(game)
						bChanged=True
	
	if args.mode in [ARG_MODE_COPY_PUBLISHER2DEV]:
		for game in gamesList.get_games():
			if (game.developer=="" and game.publisher!=""):
				game.developer=game.publisher
				print('Update developer '+game.developer+' to '+game.name)
				gamesList.update_game(game)
				bChanged=True
	
	if args.mode in [ARG_MODE_CLEAN_DEVELOPER]:
		for game in gamesList.get_games():
			if ' - ' in game.developer:
				game.developer = game.developer.replace(' - ',', ')
				print('Update developer '+game.developer+' to '+game.name)
				gamesList.update_game(game,False)
				bChanged=True
	
	if args.mode in [ARG_MODE_COPY_DEV2PUBLISHER]:
		for game in gamesList.get_games():
			if (game.publisher=="" and game.developer!=""):
				game.publisher=game.developer
				print('Update publisher '+game.publisher+' to '+game.name)
				gamesList.update_game(game)
				bChanged=True
	
	if args.mode in [ARG_MODE_CLEAN_PUBLISHER]:
		for game in gamesList.get_games():
			if ' - ' in game.publisher:
				game.publisher = game.publisher.replace(' - ',', ')
				print('Update publisher '+game.publisher+' to '+game.name)
				gamesList.update_game(game,False)
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
	
	if args.mode in [ARG_MODE_CLEAN_DATE,ARG_MODE_CLEAN_ALL]:
		for game in gamesList.get_games():
			if len(game.releasedate) < 17:
				if len(game.releasedate) == 4 and game.releasedate[0:2] in ['19','20']:
					game.releasedate=game.releasedate+'0101'+'T000000'
					print('Update date '+game.releasedate+' to '+game.name)
					gamesList.update_game(game,False)
					bChanged=True
	
				if len(game.releasedate) == 8:
					game.releasedate=game.releasedate+'T000000'
					print('Update date '+game.releasedate+' to '+game.name)
					gamesList.update_game(game,False)
					bChanged=True
	
	if args.mode in [ARG_MODE_CLEAN_PLAYERS,ARG_MODE_CLEAN_ALL]:
		for game in gamesList.get_games():
			if '-' in game.players:
				game.players = game.players.split('-')[1]
				print('Update players '+game.players+' to '+game.name)
				gamesList.update_game(game,False)
				bChanged=True

	if args.mode in [ARG_MODE_CLEAN_DESC,ARG_MODE_CLEAN_ALL]:
		for game in gamesList.get_games():
			if game.desc[-1:]=='.' and game.desc[-3:]!='...':
				game.desc = game.desc[:-1]
				gamesList.update_game(game,False)
				bChanged=True

	if args.mode in [ARG_MODE_CLEAN_NAME,ARG_MODE_CLEAN_ALL]:
		for game in gamesList.get_games():
			if ' - ' in game.name:
				game.name = game.name.replace(' - ',': ')
				print('Update name '+game.name)
				gamesList.update_game(game,False)
				bChanged=True
			if ', THE' in game.name:
				game.name = 'THE '+game.name.replace(', THE','')
				print('Update name '+game.name)
				gamesList.update_game(game,False)
				bChanged=True


	if args.mode in [ARG_MODE_CLEAN_GENRE,ARG_MODE_CLEAN_ALL]:
		for game in gamesList.get_games():
			if ' / ' in game.genre:
				game.genre = game.genre.replace(' / ',', ')
				print('Update genre '+game.genre+' to '+game.name)
				gamesList.update_game(game,False)
				bChanged=True
			if ', VERTICAL' in game.genre:
				game.genre = game.genre.replace(', VERTICAL','')
				print('Update genre '+game.genre+' to '+game.name)
				gamesList.update_game(game,False)
				bChanged=True
				
	if args.mode in [ARG_MODE_ADD_REGION_TITLE]:
		for game in gamesList.get_games():
			if '[' not in game.name and game.region !='':
				game.name = game.name + ' ['+game.region+']'
				print('Update name to '+game.name)
				gamesList.update_game(game,False)
				bChanged=True
	
	if args.mode in [ARG_MODE_REMOVE_REGION_TITLE]:
		for game in gamesList.get_games():
			if '[' in game.name:
				game.name = game.name.split(' [')[0]
				print('Update name to '+game.name)
				gamesList.update_game(game,False)
				bChanged=True
				
			if '(' in game.name:
				game.name = game.name.split(' (')[0]
				print('Update name to '+game.name)
				gamesList.update_game(game,False)
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
