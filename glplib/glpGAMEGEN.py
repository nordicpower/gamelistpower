#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                              - GAMELISTPOWER -                               #
#                           - GENERATE COLLECTION -                            #
#------------------------------------------------------------------------------#
# Generation d'un fichier gamelist "collection" selon criteres de recherche    #
# dans les autres gamelist.xml                                                 #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.07 17/04/2017-06/09/2018 #
################################################################################

#IMPORT STD---------------------------------------------------------------------
import json
import os
import shutil

#IMPORT NORDICPOWER-------------------------------------------------------------
from glpES import *
from glpDIR import *
from glpTOOLS import *
from glpXML import *
from glpRULES import *
from gamelistpower import SEUIL_SAUVEGARDE_BIGROM

#MSG LOCALISATION---------------------------------------------------------------
config=Config()

msg_local={
('MSG_ERROR_GLG_EXCEPTION','FR'):u'{} : {}',
('MSG_ERROR_GLG_EXCEPTION','EN'):u'{} : {}',
('MSG_WARN_GLG_SOURCE_NOT_SUPPORTED','FR'):u'Source {} non support\u00E9 dans la r\u00E8gle: {}',
('MSG_WARN_GLG_SOURCE_NOT_SUPPORTED','EN'):u'Source {} not supported in this rule: {}',
('MSG_DEBUG_GLG_MATCH_GAME','FR'):u'Rom {} sur plateforme {} correspond \u00E0 la r\u00E8gle: {}',
('MSG_DEBUG_GLG_MATCH_GAME','EN'):u'Rom {} on plateform {} match with this rule: {}',
('MSG_INFO_GLG_GEN_LAUNCHER','FR'):u'G\u00E9n\u00E9ration du laucher: {}',
('MSG_INFO_GLG_GEN_LAUNCHER','EN'):u'Generate launcher: {}',
('MSG_WARN_GLG_ROM_NOT_FOUND','FR'):u'Rom non trouv\u00E9: {}',
('MSG_WARN_GLG_ROM_NOT_FOUND','EN'):u'Rom not found: {}',
('MSG_INFO_GLG_ROM_ADDED','FR'):u'Ajout de la rom : {}',
('MSG_INFO_GLG_ROM_ADDED','EN'):u'Rom added: {}',
('MSG_WARN_GLG_EMULATOR_NOT_SUPPORTED','FR'):u'Emulateur non support\u00E9: {} pour la rom {}',
('MSG_WARN_GLG_EMULATOR_NOT_SUPPORTED','EN'):u'Emulator not supported: {} with this rom {}',
('MSG_DEBUG_GLG_USE_EXTERNAL_GAMELIST','FR'):u'Utilisation Gamelist externe avec la rom {}',
('MSG_DEBUG_GLG_USE_EXTERNAL_GAMELIST','EN'):u'Use external Gamelist with this rom {}',
('MSG_INFO_GLG_GEN_EXCLUDE','FR'):u'Exclusion du fichier: {}',
('MSG_INFO_GLG_GEN_EXCLUDE','EN'):u'Exclude file: {}'
}

#INIT SINGLETON-----------------------------------------------------------------
logger=Logger.logr

#CLASS-RESULT---------------------------------------------------------------------
class Result:
	"""POJO Stockage d'un résultat"""
	def __init__(self,**kwargs):
		self._name=''
		self._type=''
		self._plateform=''
		self._command=''
		self._dest_path=''
		self._game=Game()
		#Happigc
		self._image_background=''
		self._image_screenshot=''
		self._image_logo=''
		self._textcolor=''
		#RecalBox
		self._system='' 
		self._emulator='' 
		self._core=''
		self._ratio=''
		self._preserveFavorite=''
		
		if kwargs is not None:
			#mise à jour paramètre(s) nommé(s)
			self.__dict__.update(kwargs)
			
	#property-------------------------	
	@property
	def name(self):return self._name
	@property
	def type(self):return self._type
	@property
	def plateform(self):return self._plateform
	@property
	def command(self):return self._command
	@property
	def game(self):return self._game
	@property
	def dest_path(self):return self._dest_path
	@property
	def image_background(self):return self._image_background
	@property
	def image_screenshot(self):return self._image_screenshot
	@property
	def image_logo(self):return self._image_logo
	@property
	def textcolor(self):return self._textcolor
	@property
	def system(self):return self._system
	@property
	def emulator(self):return self._emulator
	@property
	def core(self):return self._core
	@property
	def ratio(self):return self._ratio
	@property
	def preserveFavorite(self):return self._preserveFavorite
		
	#setter-------------------------	
	@name.setter
	def name(self,v):self._name=v
	@type.setter
	def type(self,v):self._name=v
	@plateform.setter
	def plateform(self,v):self._plateform=v
	@command.setter
	def command(self,v):self._command=v
	@game.setter
	def game(self,v):self._game=v
	@dest_path.setter
	def dest_path(self,v):self._dest_path=v
	@image_background.setter
	def image_background(self,v):self._image_background=v
	@image_screenshot.setter
	def image_screenshot(self,v):self._image_screenshot=v
	@image_logo.setter
	def image_logo(self,v):self._image_logo=v
	@textcolor.setter
	def textcolor(self,v):self._textcolor=v
	@system.setter
	def system(self,v):self._system=v
	@emulator.setter
	def emulator(self,v):self._emulator=v
	@core.setter
	def core(self,v):self._core=v
	@ratio.setter
	def ratio(self,v):self._ratio=v
	@preserveFavorite.setter
	def preserveFavorite(self,v):self._preserveFavorite=v
	
	def __repr__(self):
		return repr((self.name, self.plateform, self.command,self.game.name,self.game.path))
		
	
def delete_commands_for_multi(rules):
	"""suppression de tous les sh existants"""
	for rule in rules:
		os.system("rm -rf {}".format(os.path.join(rule.dest_path, "*" )))

def search_games_for_multi(GameListDirectory,gamesList,plateform,es_system_name,es_config_command,es_config_default_emulator,es_config_default_core,rules,exclude_folders,default_game_picture):
	"""génération des configurations multi-émulateurs selon critère"""
	
	Match_results_rules = []
	
	for rule in rules:
			#recherche sur un attribut
			if rule.source in [SOURCE_ATTR_GENRE,SOURCE_ATTR_NAME,SOURCE_ATTR_DEVELOPER,SOURCE_ATTR_PUBLISHER]:
				for result_game in gamesList.search_games(rule.source,rule.search):
					
					rom_to_exclude=False
					#exclusion par fichier ini
					for exclude_folder in exclude_folders:
						if exclude_folder in result_game.path:
							rom_to_exclude = True
					#exclusion par rule
					gameFullPathName=os.path.join(GameListDirectory,result_game.path.replace('.'+os.sep,''))
					for exclusion_file in rule.exclusion_files:
						if len(exclusion_file)>0 and exclusion_file in gameFullPathName:
							logger.info(msg_local.get(('MSG_INFO_GLG_GEN_EXCLUDE',config.language)).format(gameFullPathName))
							rom_to_exclude = True
								
					#exclusion par attribut cache gamelist.xml
					if result_game.hidden=='true':
						rom_to_exclude = True
					#recherche doublon sur la même chemin cible et nom de rom
					if rom_to_exclude == False:
						for match_results_rule in Match_results_rules:
							if match_results_rule.game == result_game and match_results_rule.dest_path == rule.dest_path :
								rom_to_exclude = True
					
					#Ajout du resultat
					if rom_to_exclude==False:
						result_game.path = result_game.path.replace('.'+os.sep,GameListDirectory+os.sep)
						if result_game.image != default_game_picture and result_game.image !='':
							result_game.image = result_game.image.replace('.'+os.sep,GameListDirectory+os.sep)
						local_emulator = result_game.emulator
						if local_emulator=='':
							local_emulator = es_config_default_emulator
						local_core = result_game.core
						if local_core=='':
							local_core = es_config_default_core
						local_ratio = result_game.ratio
						if local_ratio=='':
							local_ratio = 'auto'
						
						#Enrichissement de l'objet Game par un gamelist externe
						if rule.gamelistLoaded==True:
							game_search_name = result_game.get_filename_rom()
							game_search_name = ('.').join(game_search_name.split('.')[:-1])
							try:
								game_XML = rule.gamelistInfo.search_game_by_path(game_search_name)
								logger.debug(msg_local.get(('MSG_DEBUG_GLG_USE_EXTERNAL_GAMELIST',config.language)).format(game_search_name))
								result_game.smartCopy_from_game(game_XML)
								
							except MyError:
								#Non trouvé
								pass
						
						#Création du résultat
						result = Result(name=rule.name,plateform=plateform,system=es_system_name,command=es_config_command,emulator=local_emulator,core=local_core,ratio=local_ratio,game=result_game,dest_path=rule.dest_path,
						image_background=rule.image_background,image_screenshot=rule.image_screenshot,image_logo=rule.image_logo,textcolor=rule.textcolor,preserveFavorite=rule.preserveFavorite,type=rule.type)
						Match_results_rules.append(result)
						logger.debug(msg_local.get(('MSG_DEBUG_GLG_MATCH_GAME',config.language)).format(result.game.name,get_last_folder_plateform(plateform),rule.name))
					
			elif rule.source in [SOURCE_ATTR_PATH]:
				for result_game in gamesList.search_games(rule.source,rule.search):
					result_game.path = result_game.path.replace('.'+os.sep,GameListDirectory+os.sep)
					if result_game.image != default_game_picture and result_game.image !='':
						result_game.image = result_game.image.replace('.'+os.sep,GameListDirectory+os.sep)
					local_emulator = result_game.emulator
					if local_emulator=='':
						local_emulator = es_config_default_emulator
					local_core = result_game.emulator
					if local_core=='':
						local_core = es_config_default_core
					local_ratio = result_game.ratio
					if local_ratio=='':
							local_ratio = 'auto'
					
					#Enrichissement de l'objet Game par un gamelist externe
					if rule.gamelistLoaded==True:
						game_search_name = result_game.get_filename_rom()
						game_search_name = ('.').join(game_search_name.split('.')[:-1])
						try:
							game_XML = rule.gamelistInfo.search_game_by_path(game_search_name)
							logger.debug(msg_local.get(('MSG_DEBUG_GLG_USE_EXTERNAL_GAMELIST',config.language)).format(game_search_name))
							result_game.smartCopy_from_game(game_XML)
							
						except MyError:
							#Non trouvé
							pass
					
					#Création du résultat
					result = Result(name=rule.name,plateform=plateform,system=es_system_name,command=es_config_command,emulator=local_emulator,core=local_core,ratio=local_ratio,game=result_game,dest_path=rule.dest_path,
					image_background=rule.image_background,image_screenshot=rule.image_screenshot,image_logo=rule.image_logo,textcolor=rule.textcolor,preserveFavorite=rule.preserveFavorite,type=rule.type)
					Match_results_rules.append(result)
					logger.debug(msg_local.get(('MSG_DEBUG_GLG_MATCH_GAME',config.language)).format(result.game.name,get_last_folder_plateform(plateform),rule.name))
				
			else:
				logger.warn(msg_local.get(('MSG_WARN_GLG_SOURCE_NOT_SUPPORTED',config.language)).format(rule.source,rule.name))
	
	return Match_results_rules
	

def update_folders_attributes(rules,gamesList):
	"""ajout info sur folder"""
	
	#Parcourir des rules pour les dossiers
	for rule in rules:
		try:
				
			name_entry=rule.dest_path.replace('\\','/').split('/')[-1]
			folder_XML = gamesList.search_folder_by_path('.'+os.sep+name_entry)
			
			#entrée XML trouvé
			if rule.dest_path_name !='':
				folder_XML.name = rule.dest_path_name
				
			#mise à jour
			gamesList.update_folder(folder_XML)
			
		except MyError:
			#Folder non trouvé
			pass
		except Exception as exception:		
			logger.warn(msg_local.get(('MSG_ERROR_GLG_EXCEPTION',config.language)).format('update_folders_attributes',type(exception).__name__))
			pass
			
def generate_launcher_for_multi(config,plateform_collection,match_results_rules,format_titre="%%NAME%% (%%PLATEFORM%%)",bNetPlayInCommandCollection=False):
	"""generation des launchers"""
	
	#Chargement XML avec MiniDom :-<
	gamesList_loaded=False
	gamesList_multi = GamesList()
	
	if os.path.isfile(config.folder_path_multi + os.sep + NOM_GAMELIST_XML):
		try:	
			gamesList_multi.import_xml_file(plateform_collection + os.sep + NOM_GAMELIST_XML,False)
			gamesList_loaded=True
		except Exception as exception:
			gamesList_loaded=False
	else:
		gamesList_loaded=False
		
	#TYPE_RULE_GENSH--------------------------------------------------------------
	for match_results_rule in [x for x in match_results_rules if x.type==TYPE_RULE_GENSH]:
		#Si fichier rom n'existe pas, on passe au suivant
		if not os.path.isfile(match_results_rule.game.path) and not os.path.isdir(match_results_rule.game.path):
			logger.warn(msg_local.get(('MSG_WARN_GLG_ROM_NOT_FOUND',config.language)).format(match_results_rule.game.path))
			continue
		
		#Bug Recalbox PSP
		if match_results_rule.system=="psp":
			match_results_rule.emulator="default" #PPSPP entraine une erreur
		
		#Generation du launcher happigc/recalbox
		command = match_results_rule.command.replace('%ROM%',escape_path(match_results_rule.game.path))
		#Generation du launcher happigc
		command = command.replace('%USERMODE%','$1')
		#Generation du launcher recalbox
		command = '#!/bin/sh\nRATIO=${@:$#}\nset -- "${@:1:$#-1}"\n' + command
		command = command.replace('%CONTROLLERSCONFIG%','"$@"')
		command = command.replace('%SYSTEM%',match_results_rule.system)
		command = command.replace('%EMULATOR%',match_results_rule.emulator)
		command = command.replace('%CORE%',match_results_rule.core)
		command = command.replace('%RATIO%',match_results_rule.ratio)
		#Suppr variable NETPLAY si absent de la commande de lancement
		if bNetPlayInCommandCollection==False:
			command = command.replace(' %NETPLAY%','')
		#Nom du fichier
		#BUG Nom avec des . [:-1]
		name_file_launcher = match_results_rule.name + '_' + get_last_folder_plateform(match_results_rule.plateform) + '_' + os.path.splitext(match_results_rule.game.get_filename_rom())[0].strip() + '.sh'
		fullpath_launcher = os.path.expanduser(match_results_rule.dest_path + os.sep + name_file_launcher)
		try:
			launcher = open(fullpath_launcher,'w')
			launcher.write(command)
			launcher.close
			os.chmod(fullpath_launcher,0o777)
			logger.info(msg_local.get(('MSG_INFO_GLG_GEN_LAUNCHER',config.language)).format(name_file_launcher))
		except Exception as exception:
			logger.warn(msg_local.get(('MSG_ERROR_GLG_EXCEPTION',config.language)).format('generate_launcher_for_multi',type(exception).__name__))
			
		#Calcul du path
		local_path = get_last_folder_plateform(match_results_rule.dest_path)
		if local_path=='':
			#A la racine
			local_path='.'+os.sep+name_file_launcher
		else:
			#Dans un sous-répertoire
			local_path='.'+os.sep+ local_path + os.sep + name_file_launcher
		
		#Mise à jour du gamelist.xml
		if gamesList_loaded==True:
			
			name_formated = format_titre
			name_formated = name_formated.replace('%%NAME%%',match_results_rule.game.name.upper())
			name_formated = name_formated.replace('%%PLATEFORM%%',get_last_folder_plateform(match_results_rule.plateform).upper())
			name_formated = name_formated.replace('%%REGION%%',match_results_rule.game.region.upper())
			name_formated = name_formated.replace('%%name%%',match_results_rule.game.name)
			name_formated = name_formated.replace('%%plateform%%',get_last_folder_plateform(match_results_rule.plateform))
			name_formated = name_formated.replace('%%region%%',match_results_rule.game.region)
			
			try:
				#MAJ du noeud existant
				game_XML = gamesList_multi.search_game_by_path(local_path)
				game_XML.smartCopy_from_game(match_results_rule.game)
				game_XML.name=name_formated
				#game_XML.name=match_results_rule.game.name + ' (' + get_last_folder_plateform(match_results_rule.plateform) + ')'
				game_XML.background = match_results_rule.image_background
				game_XML.screenshot = match_results_rule.image_screenshot
				game_XML.logo = match_results_rule.image_logo
				game_XML.textcolor = match_results_rule.textcolor
				if get_last_folder_plateform(match_results_rule.plateform)=='amiga' and game_XML.name[0:4]=='ADF ': 
					game_XML.name = game_XML.name[4:]
				if not match_results_rule.preserveFavorite in ['true','True','Vrai','vrai']:
					game_XML.favorite='false'
				gamesList_multi.update_game(game_XML)
			except MyError:
				#Pas de noeud game trouvé
				game_XML = Game()
				game_XML.smartCopy_from_game(match_results_rule.game)
				game_XML.path=local_path
				game_XML.name=format_titre
				game_XML.name=name_formated
				game_XML.background = match_results_rule.image_background
				game_XML.screenshot = match_results_rule.image_screenshot
				game_XML.logo = match_results_rule.image_logo
				game_XML.textcolor = match_results_rule.textcolor
				if get_last_folder_plateform(match_results_rule.plateform)=='amiga' and game_XML.name[0:4]=='ADF ': 
					game_XML.name = game_XML.name[4:]
				if not match_results_rule.preserveFavorite in ['true','True','Vrai','vrai']:
					game_XML.favorite='false'
					
				#Ajout de l'entrée
				gamesList_multi.add_game(game_XML)
			
			logger.info(msg_local.get(('MSG_INFO_GLG_ROM_ADDED',config.language)).format(name_formated))
		#fin for
	
	#TYPE_RULE_ROMCPY--------------------------------------------------------------
	for match_results_rule in [x for x in match_results_rules if x.type==TYPE_RULE_ROMCPY]:
		
		#Systeme non supporte
		if match_results_rule.emulator in ['amiberry','dosbox','scummvm']:
			logger.warn(msg_local.get(('MSG_WARN_GLG_EMULATOR_NOT_SUPPORTED',config.language)).format(match_results_rule.emulator,match_results_rule.game.path))
			continue
			
		#Si fichier rom n'existe pas, on passe au suivant
		if not os.path.isfile(match_results_rule.game.path) and not os.path.isdir(match_results_rule.game.path):
			logger.warn(msg_local.get(('MSG_WARN_GLG_ROM_NOT_FOUND',config.language)).format(match_results_rule.game.path))
			continue
		
		#Copie de la rom a la cible	
		shutil.copy(match_results_rule.game.path, match_results_rule.dest_path)
		
		#Calcul du path
		local_path = get_last_folder_plateform(match_results_rule.dest_path)
		if local_path=='':
			#A la racine
			local_path='.'+os.sep+name_file_launcher
		else:
			#Dans un sous-répertoire
			local_path='.'+os.sep+ local_path + os.sep + match_results_rule.game.get_filename_rom()
			
		#Mise à jour du gamelist.xml
		if gamesList_loaded==True:
			
			name_formated = format_titre
			name_formated = name_formated.replace('%%NAME%%',match_results_rule.game.name.upper())
			name_formated = name_formated.replace('%%PLATEFORM%%',get_last_folder_plateform(match_results_rule.plateform).upper())
			name_formated = name_formated.replace('%%REGION%%',match_results_rule.game.region.upper())
			name_formated = name_formated.replace('%%name%%',match_results_rule.game.name)
			name_formated = name_formated.replace('%%plateform%%',get_last_folder_plateform(match_results_rule.plateform))
			name_formated = name_formated.replace('%%region%%',match_results_rule.game.region)
			
			try:
				#MAJ du noeud existant
				game_XML = gamesList_multi.search_game_by_path(local_path)
				game_XML.copy_from_game(match_results_rule.game)
				game_XML.emulator=match_results_rule.emulator
				game_XML.core = match_results_rule.core
				if not match_results_rule.preserveFavorite in ['true','True','Vrai','vrai']:
					game_XML.favorite='false'
				game_XML.name=name_formated
				gamesList_multi.update_game(game_XML)
			except MyError:
				#Pas de noeud game trouvé
				game_XML = Game()
				game_XML.copy_from_game(match_results_rule.game)
				game_XML.path = local_path
				game_XML.emulator=match_results_rule.emulator
				game_XML.core = match_results_rule.core
				if not match_results_rule.preserveFavorite in ['true','True','Vrai','vrai']:
					game_XML.favorite='false'
				game_XML.name=name_formated
				#Ajout de l'entrée
				gamesList_multi.add_game(game_XML)
				
			logger.info(msg_local.get(('MSG_INFO_GLG_ROM_ADDED',config.language)).format(name_formated))
		#fin for
		
	if gamesList_loaded==True and gamesList_multi.modified:
		gamesList_multi.refresh_folders_finished()	
		if len(gamesList_multi.get_games())>SEUIL_SAUVEGARDE_BIGROM:
			#logger.debug(msg_local.get(('MSG_INFO_GLP_PRG_SAVE_BIGROM',config.language)).format(NOM_GAMELIST_XML))
			gamesList_multi.save_xml_file(os.path.join(plateform_collection,NOM_GAMELIST_XML),False)
		else:
			#logger.debug(msg_local.get(('MSG_INFO_GLP_PRG_SAVE',config.language)).format(NOM_GAMELIST_XML))
			gamesList_multi.save_xml_file(os.path.join(plateform_collection,NOM_GAMELIST_XML))

def escape_path(rom_path):
	"""Gestion escape similaire à ES"""
	
	for e in '\ "!$^&*(){}[]?;<>\'':
		if rom_path.find(e)>0:
			rom_path=rom_path.replace(e, '\\'+e)
	
	return rom_path
			
#---------------------------------------------------------------------------------------------------
#---------------------------------------- MAIN -----------------------------------------------------
#---------------------------------------------------------------------------------------------------
def main():
	
	#Init Log
	logger=Logger.logr
	
	#Lecture Configuration
	config.load_from_file()
	
	#Lecture Configuration
	#rules = generate_rules()
	rules = load_rules_from_ini_config(config.generation_rules)
	
	print rules
	
#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	main()
