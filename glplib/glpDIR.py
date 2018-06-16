#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                              - GAMELISTPOWER -                               #
#                            - MODULE DIRECTORY -                              #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.00 01/11/2016-16/05/2018 #
#------------------------------------------------------------------------------#

#IMPORT STD---------------------------------------------------------------------
import os.path
import sys
import time
import shutil
from os.path import basename, splitext
import hashlib
import json

#IMPORT NORDICPOWER-------------------------------------------------------------
from glpTOOLS import *

#IMPORT COMPOSANT TIERS---------------------------------------------------------
import chardet as chardet

#MSG LOCALISATION---------------------------------------------------------------
#config=Config()

msg_local={
('MSG_GLD_APPPATH','FR'):u'{} : Ajout du chemin : {}',
('MSG_GLD_APPPATH','EN'):u'{} : Add path : {}',
('MSG_GLD_EXCPATH','FR'):u'{} : Exclusion du chemin : {}',
('MSG_GLD_EXCPATH','EN'):u'{} : Exclude path : {}',
('MSG_GLD_EXCFILE','FR'):u'{} : Exclusion du fichier : {}',
('MSG_GLD_EXCFILE','EN'):u'{} : Exclude file : {}',
('MSG_GLD_ADDGLFILE','FR'):u'{} : Ajout du fichier : {}',
('MSG_GLD_ADDGLFILE','EN'):u'{} : Add file : {}',
('MSG_GLD_TEST_FILE','FR'):u'{} : Test du fichier : {}',
('MSG_GLD_TEST_FILE','EN'):u'{} : Test file : {}',
('MSG_GLD_ADDGLFOLDER','FR'):u'{} : Ajout du dossier : {}',
('MSG_GLD_ADDGLFOLDER','EN'):u'{} : Add folder : {}'
}

#INIT LOGGER -------------------------------------------------------------------
logger=Logger.logr

#CONSTANTS----------------------------------------------------------------------
NOM_GAMELIST='gamelist'
NOM_GAMELIST_XML=NOM_GAMELIST+'.xml'
NOM_DIR_IMAGES3='folders'

#PUBLIC FUNCTIONS FICHIERS------------------------------------------------------
def list_gamelist_directories(rom_path,folder_name_exclusion,images_folder):
	"""Search directory which a gamelist.xml file inside"""
	
	#Recherche sans exclusion
	if folder_name_exclusion[0]=='': return list_gamelist_directories_simple(rom_path)
	
	gamelistDirectories=[]
	#Recherche avec exclusion	
	for path, dirs, files in os.walk(rom_path):
		path_added=False
		for checked_path in folder_name_exclusion:
			if path[0:len(checked_path)] != checked_path and not path_added:
				for file in files:
					#Ajout du répertoire du crawler
					if file == NOM_GAMELIST_XML:
						#logger.debug(msg_local.get(('MSG_GLD_APPPATH',config.language)).format('list_gamelist_directories',path))
						gamelistDirectories.append(path)
						path_added=True
		
		#Cas d'un répertoire vide => création Gamelist.xml vide pour la suite (0.6.00)
		if path_added==False:
			base_rom = path[len(rom_path)-len(path)+1:]
			base_rom_decompose = base_rom.split(os.sep)
			#recherche d'un répertoire de deuxième niveau uniquement sous les 3 racines
			if base_rom_decompose[0] in ['arcade','console','ordinateur'] and len(base_rom_decompose)==2:
				#création d'un fichier vide
				#logger.debug(msg_local.get(('MSG_GLD_ADDGLFILE',config.language)).format('list_gamelist_directories',os.path.join(path,NOM_GAMELIST_XML)))
				open(os.path.join(path,NOM_GAMELIST_XML),'a').close()
				#création d'un répertoire images (avec le 1er nom de dossier images)
				dossier_image = os.path.join(path,images_folder[0])
				if not os.path.exists(dossier_image):
					#logger.debug(msg_local.get(('MSG_GLD_ADDGLFOLDER',config.language)).format('list_gamelist_directories',dossier_image))
					os.makedirs(dossier_image)
				#Ajout du répertoire du crawler
				#logger.debug(msg_local.get(('MSG_GLD_APPPATH',config.language)).format('list_gamelist_directories',path))
				gamelistDirectories.append(path)
				path_added=True
			
	return gamelistDirectories


def list_gamelist_directories_simple(rom_path):
	"""Search directory which a gamelist.xml file inside without exclusion patch"""
	gamelistDirectories=[]
	
	for path, dirs, files in os.walk(rom_path):
			for file in files:
				if file == NOM_GAMELIST_XML:
					#logger.debug(msg_local.get(('MSG_GLD_APPPATH',config.language)).format('list_gamelist_directories_simple',path))
					gamelistDirectories.append(path)
					
	return gamelistDirectories
	

def list_sub_directories(root_path,folder_name_exclusion,images_folder,exclude_dir_images=True ):
	"""Search Sub Directories, excluding images directory"""
	subDirectories=[]
	
	#Exclusion via le root
	if root_path in folder_name_exclusion:
		return subDirectories
	
	for path, dirs, files in os.walk(root_path):
		
		#0.5.18 - Filtrage des dossiers interdits
		if path not in folder_name_exclusion:
			
			dirs_filtered = [tempdir for tempdir in dirs if os.path.join(path,tempdir) not in folder_name_exclusion]
			for dir in dirs_filtered:
				
				#if dir != NOM_DIR_IMAGES or exclude_dir_images == False:
				if dir not in images_folder or exclude_dir_images == False:
					#logger.debug('dir='+dir+' relpath='+path[len(root_path)+1:999])
					
					if path[len(root_path)+1:999]=='':
						#sous-répertoire niveau 1
						subDirectories.append(dir)
						
					else:
						#sous-répertoire niveau >1
						subDirectories.append(path[len(root_path)+1:]+os.sep+dir)
					
	return subDirectories


def is_not_exclusion_file(game_path,game_file,game_name_exclusion,game_ext_exclusion):
	"""return true if 1) not in excluded file name 2) file exist"""
	#test sur nom en dur
	if '-image.' in game_file or NOM_GAMELIST in game_file:
		return False
	
	#test sur les noms réservés
	for name_exc in game_name_exclusion:
		if name_exc in game_file : return False
		
	#test sur les extensions fichiers
	for ext in game_ext_exclusion:
		if '.'+ext in game_file:
			return False
	
	#test existence fichier pas nécessaire
	#return os.path.isfile(os.path.expanduser(os.path.join(game_path,game_file)))
	return True



def is_inclusion_file(game_path,game_file,game_name_exclusion,game_ext_inclusion):
	"""return true if 1) not in excluded file name 2) accepted extension """
	#test sur nom en dur
	if '-image.' in game_file or NOM_GAMELIST in game_file:
		return False
	
	#test sur les noms réservés
	for name_exc in game_name_exclusion:
		if name_exc in game_file : return False
		
	#test sur les extensions fichiers
	for ext in game_ext_inclusion:
		if '.'+ext in game_file:
			return True
	
	#test existence fichier
	return False
	

def list_sub_files(root_path,folder_name_exclusion,game_name_exclusion,game_ext_exclusion,game_ext_inclusion):
	"""Search files, excluding gamelist files"""
	search_files=[]
	
	for path, dirs, files in os.walk(root_path):
	
		#TODO 0.5.18 Exclusion des fichiers dans certains répertoires !!
		if path in folder_name_exclusion:
			return search_files
		
		for file in files:
			
			if len(game_ext_inclusion)==0:
				#fonctionnement par exclusion
				#exclusion des fichiers gamelist*, image et non existant
				file_accepted = is_not_exclusion_file(path,file,game_name_exclusion,game_ext_exclusion)
			else:
				#fonctionnement par inclusion (es_systems.cfg)
				file_accepted = is_inclusion_file(path,file,game_name_exclusion,game_ext_inclusion)
				
			#if is_not_exclusion_file(path,file,game_name_exclusion,game_ext_exclusion):
			if file_accepted:
				if path[len(root_path)+1:]=='':
					#fichier jeu au niveau 1
					search_files.append(file)
				else:
					#fichier jeu au niveau >1
					search_files.append(path[len(root_path)+1:999]+os.sep+file)				
				
	return search_files

	
def get_associed_image_from_file(gameListDir,entry,images_extension,images_folder):
	"""
	Search associed picture file of an entry with name format entry + '-image.' + extension
	Return empty if not found
	"""
	testFile=''
	#recherche du nom, même dans un sous répertoire
	name_entry=entry.replace('\\','/').split('/')[-1]
	
	for extension in images_extension:
		
		for folder_name in images_folder:
			
			#Test n°1 (./images/<rom>-image.*)
			testFile = folder_name + os.sep + name_entry + '-image.' + extension
			if os.path.isfile(os.path.expanduser(gameListDir + os.sep + testFile)): return testFile
	
			#Test n°2 (./images/<rom>.*)
			testFile = folder_name + os.sep + name_entry + '.' + extension			
			if os.path.isfile(os.path.expanduser(gameListDir + os.sep + testFile)): return testFile

			#Test n°3 dans le répertoire images d'un sous-répertoire du répertoire de gamelist.xml
			testFile = entry + os.sep + folder_name + os.sep + name_entry + '-image.' + extension
			if os.path.isfile(os.path.expanduser(gameListDir + os.sep + testFile)): return testFile
		
			#Test n°4 dans le répertoire images d'un sous-répertoire du répertoire de gamelist.xml (sans -image)
			testFile = entry + os.sep + folder_name + os.sep + name_entry + '.' + extension
			if os.path.isfile(os.path.expanduser(gameListDir + os.sep + testFile)): return testFile	
	
			#Test n°5/6 dans le répertoire images d'un sous-répertoire du répertoire de gamelist.xml
			if os.sep in entry:
				last_folder=entry.split(os.sep)[-1]
				testFile = entry[0:len(entry)-len(last_folder)] + folder_name + os.sep + name_entry +'-image.'+extension
				if os.path.isfile(os.path.expanduser(gameListDir + os.sep + testFile)): return testFile
					
				testFile = entry[0:len(entry)-len(last_folder)] + folder_name + os.sep + name_entry +'.'+extension
				if os.path.isfile(os.path.expanduser(gameListDir + os.sep + testFile)): return testFile
	
	return ''


def get_path_without_current(path):
		"""Suppression du point qui désigne folder courant"""
		if path.replace('\\','/')[0:2]=="./":
			return path[2:]
		else:
			return path

def get_last_folder_plateform(folder):
		"""return name of plateform"""
		return folder.replace('\\','/').replace('/atari/launcher','/atari').replace('/amiga/config','/amiga').split('/')[-1]

def exist_game_rom(GameListDirectory, path_rom):
		"""return true if rom exist in folder"""
		return os.path.isfile(os.path.expanduser(os.path.join(GameListDirectory,get_path_without_current(path_rom))))

def get_short_path_from_root(rootPath,path):
	"""retourne une contraction du path root"""
	return path[len(rootPath)-len(os.path.basename(rootPath)):]


#CLASS-GAMES os_stats--------------------------------------------------------------
class OsStatModify():
	"""Objet conteneur des appels os.stat"""
	def __init__(self,v_path,v_config,v_size=0,v_mtime=0,v_ctime=0,**kwargs):
		self._path = v_path
		self._config = v_config
		self._size = v_size
		self._mtime = v_mtime 
		self._ctime = v_ctime
		self._condansa_filenames = 0
		
		if kwargs is not None:
			#mise à jour paramètre(s) nommé(s)
			self.__dict__.update(kwargs)
	
	def __repr__(self):
        	return repr((self.path, self.size, self.mtime, self.ctime, self.condansa_filenames))
        		
	#property-------------------------	
	@property
	def path(self):return self._path
	@property
	def mtime(self):return self._mtime
	@property
	def ctime(self):return self._ctime
	@property
	def size(self):return self._size
	@property
	def condansa_filenames(self):return self._condansa_filenames
		
	#setter-------------------------	
	@path.setter
	def path(self,v):self._path=v
	@mtime.setter
	def name(self,v):self._mtime=v
	@ctime.setter
	def name(self,v):self._ctime=v
	@size.setter
	def name(self,v):self._size=v
	@condansa_filenames.setter
	def name(self,v):self._condansa_filenames=v
	
	def setStats(self):
		stats = os.stat(self._path)
		self._size = stats.st_size #size of file, in bytes
		self._mtime = stats.st_mtime #time of most recent content modification
		self._ctime = stats.st_ctime #platform dependent; time of most recent metadata change on Unix, or the time of creation on Windows)
			

def get_hash_from_path(path_directory,config):
	"""Calcul d'un condensat contenant les informations de modifications du dossier et de ses dossiers
	ainsi que la liste des fichiers. Ne détecte pas les modifications de taille"""
	m = hashlib.sha256()
	os_stats_alldir = []
	
	osStatModify = OsStatModify(path_directory,config)
	osStatModify.setStats()
	#Liste des fichiers (sans tenir compte es_systems.cfg)
	files = list_sub_files(path_directory,config.folder_name_exclusion,config.game_name_exclusion,config.game_extension_exclusion,'')
	text_to_hash=''.join(files)
	m.update(text_to_hash)
	osStatModify.condansa_filenames=m.hexdigest()
	os_stats_alldir.append(osStatModify)
	
	#Liste sur les dossiers et ses fichiers
	subDirectories = list_sub_directories(path_directory,config.folder_name_exclusion,config.images_folder,False)
	if len(subDirectories)>0:
		for SubDirectory in subDirectories:
			osStatModify = OsStatModify(os.path.join(path_directory,SubDirectory),config)
			osStatModify.setStats()
			#Liste des fichiers (sans tenir compte es_systems.cfg)
			files = list_sub_files(osStatModify.path,config.folder_name_exclusion,config.game_name_exclusion,config.game_extension_exclusion,'')
			text_to_hash=''.join(files)
			m.update(text_to_hash)
			osStatModify.condansa_filenames=m.hexdigest()
			os_stats_alldir.append(osStatModify)
	
	text_to_hash=''
	for os_stats in os_stats_alldir:
		text_to_hash = text_to_hash + str(os_stats)
	m.update(text_to_hash)
	
	return m.hexdigest()


#Detection encoding ----------------------------------------------------------------
def predict_encoding(file_path, n_lines=50):
	'''Predict a file's encoding using chardet'''

	# Open the file as binary data
	with open(file_path, 'rb') as f:
		# Join binary lines for specified number of lines
		rawdata = b''.join([f.readline() for _ in range(n_lines)])

	return chardet.detect(rawdata)['encoding']  
	

#CLASS-GAMES os_folderhash--------------------------------------------------------------
class Folders_Hash():
	"""gestion des hash"""
	def __init__(self,v_path,v_config,**kwargs):
		self._path = v_path
		self._config = v_config
		self._hash_dictionary={}
		
		if kwargs is not None:
			#mise à jour paramètre(s) nommé(s)
			self.__dict__.update(kwargs)

	#property-------------------------	
	@property
	def dictionary(self):return self._hash_dictionary
		
	#setter-------------------------	
	@dictionary.setter
	def dictionary(self,v):self._hash_dictionary=v
	
	def set_hash(self,folder):
		self._hash_dictionary[folder]= get_hash_from_path(folder,self._config)
	
	def save(self):
		with open(self._path, 'w') as f:
			json.dump(self._hash_dictionary, f)
			
	def load(self):
		try:
			with open(self._path) as f:
				self._hash_dictionary = json.load(f)
		except:
			self._hash_dictionary = {}
				
	def changed(self,folder):
		test_new_hash = get_hash_from_path(folder,self._config)	
		if self._hash_dictionary.has_key(folder):
			if test_new_hash == self._hash_dictionary[folder]:
				return False
			else:
				return True
		else:
			#pas d'entrée, forcage du changement
			return True
			