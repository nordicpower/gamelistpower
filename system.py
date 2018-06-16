#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                              - GAMELISTPOWER -                               #
#                         - SYSTEM EMULATIONSTATION -                          #
#------------------------------------------------------------------------------#
# Operations en ligne de commande sur le fichier es_systems.cfg                #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.00 10/06/2017-15/05/2018 #
################################################################################

#IMPORT STD---------------------------------------------------------------------
import os.path
import sys
import time
import shutil
import traceback
import argparse
from os.path import basename, splitext

#IMPORT NORDICPOWER--------------------------------------------------------------
from glplib import *

#CONSTANTS-----------------------------------------------------------------------
VERSION='0.9.0 BETA'

#CONSTANTS ARGUMENTS LANCEMENT---------------------------------------------------
ARG_MODE='mode'
ARG_MODE_MERGE='merge'
ARG_MODE_ENABLED='enabled'
ARG_MODE_DISABLED='disabled'
ARG_MODE_IS_ENABLED='is_enabled'
ARG_MODE_IS_DISABLED='is_disabled'
ARG_MODE_STATUS='status'
ARG_MODE_LIST='list'
ARG_MODE_TEST_ADD='test_add'
ARG_MODE_TEST_UPD='test_upd'
ARG_ACTIVATION_PLATEFORMS='plateforms'
ARG_MERGE_FILES='files'

#MSG LOCALISATION----------------------------------------------------------------
config=Config()

msg_local={
('MSG_ERROR_PLA_EXCEPTION','FR'):u'{} : {}',
('MSG_ERROR_PLA_EXCEPTION','EN'):u'{} : {}',
('MSG_ERROR_PLA_ARGUMENT_ERROR','FR'):u'Argument {} manquant',
('MSG_ERROR_PLA_ARGUMENT_ERROR','EN'):u'Arg {} missing',
('MSG_ERROR_PLA_SRC_NOT_FOUND','FR'):u'Fichier {} non trouv\u00E9 !',
('MSG_ERROR_PLA_SRC_NOT_FOUND','EN'):u'file {} not found !',
('MSG_INFO_PLA_PLATEFORM_ADD','FR'):u'Ajout de la plateforme {}',
('MSG_INFO_PLA_PLATEFORM_ADD','EN'):u'Plateform {} is added {}',
('MSG_INFO_PLA_PLATEFORM_UPDATE','FR'):u'Mise \u00E0 jour de la plateforme {}',
('MSG_INFO_PLA_PLATEFORM_UPDATE','EN'):u'Plateform {} is updated {}',
('MSG_INFO_PLA_PLATEFORM_ACTIVATE','FR'):u'Activation de la plateforme {}',
('MSG_INFO_PLA_PLATEFORM_ACTIVATE','EN'):u'Plateform {} is enabled {}',
('MSG_INFO_PLA_PLATEFORM_DEACTIVATE','FR'):u'D\u00E9sactivation de la platerforme {}',
('MSG_INFO_PLA_PLATEFORM_DEACTIVATE','EN'):u'Plateform {} is disabled',
('MSG_CRITICAL_PLA_ESSYSTEM_LOAD_ERROR','FR'):u'Erreur de chargement du fichier es_systems.cfg: {}',
('MSG_CRITICAL_PLA_ESSYSTEM_LOAD_ERROR','EN'):u'Error while loading es_systems.cfg: {}',
('MSG_CRITICAL_PLA_ESSYSTEM_LOAD_ERROR2','FR'):u'Erreur de chargement du fichier {}',
('MSG_CRITICAL_PLA_ESSYSTEM_LOAD_ERROR2','EN'):u'Error while loading  {}',
('MSG_DEBUG_PLA_ESSYSTEM_UNKNOW_PLATEFORM','FR'):u'Pas d\x27information es_systems.cfg',
('MSG_DEBUG_PLA_ESSYSTEM_UNKNOW_PLATEFORM','EN'):u'No information in es_systems.cfg'
}

#---------------------------------------------------------------------------------------------------
def get_args():
	parser = argparse.ArgumentParser(description='gestion du fichier es_system.cfg',epilog='(C) NORDIC POWER')
	parser.add_argument(ARG_MODE,choices=[ARG_MODE_MERGE,ARG_MODE_ENABLED,ARG_MODE_DISABLED,ARG_MODE_STATUS,ARG_MODE_IS_ENABLED,ARG_MODE_IS_DISABLED,ARG_MODE_LIST,ARG_MODE_TEST_ADD,ARG_MODE_TEST_UPD], default=ARG_MODE_ENABLED, help='mode')
	parser.add_argument('-p',dest=ARG_ACTIVATION_PLATEFORMS,nargs='*')
	parser.add_argument('-f',dest=ARG_MERGE_FILES,nargs='*')
	return parser.parse_args()

def print_system(system):
	#logger.info('def: '+system.getDefaultEmulatorCore())
	loginfo='<system><fullname>'+system.fullname+'</fullname><name>'+system.name+'</name><path>'+system.path+'</path><extension>'+system.extension+'</extension><command>'+system.command+'</command><platform>'+system.platform+'</platform><theme>'+system.theme+'</theme>'
	if not system.emulators == []:
		loginfo=loginfo+'<emulators>'
		for emulator in system.emulators:
			loginfo=loginfo+'<emulator name="'+emulator.name+'">'
			if not emulator.cores == []:
				loginfo=loginfo+'<cores>'
				for core in emulator.cores:
					loginfo=loginfo+'<core>'+core+'</core>'
				loginfo=loginfo+'</cores>'
			loginfo=loginfo+'</emulator>'
		loginfo=loginfo+'</emulators>'
		
	#Itération sur <emulators>/<emulator> puis <cores>/<core>
	loginfo=loginfo+'</system>'
	logger.info(loginfo)

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
	
	logger.info('plateform - NordicPower - Version '+VERSION)
	#Lecture Configuration
	config.load_from_file()

	#Chargement du fichier es_systems.cfg (configuration EmulationStation)
	try:
		configs_ES = ESSystemList()		
		configs_ES.import_xml_file(config.emulation_station_systems)
	except Exception as exception:
		logger.critical(msg_local.get(('MSG_CRITICAL_PLA_ESSYSTEM_LOAD_ERROR',config.language)).format(type(exception).__name__))
		sys.exit(1)

	#Activation / Désactivation d'une plateforme par modification du path
	if args.mode in [ARG_MODE_ENABLED,ARG_MODE_DISABLED,ARG_MODE_STATUS,ARG_MODE_IS_ENABLED,ARG_MODE_IS_DISABLED]:	
		
		try:
			iter(args.plateforms)
		except:
			logger.error(msg_local.get(('MSG_ERROR_PLA_ARGUMENT_ERROR',config.language)).format('-p'))
			sys.exit(1)
	
		for path_plateform in args.plateforms:
			try:
				plateform = configs_ES.search_system_by_short_path(path_plateform)
				if args.mode==ARG_MODE_ENABLED:
					configs_ES.activate_system(plateform)
					logger.info(msg_local.get(('MSG_INFO_PLA_PLATEFORM_ACTIVATE',config.language)).format(plateform.name))
				if args.mode==ARG_MODE_DISABLED:
					configs_ES.deactivate_system(plateform)
					logger.info(msg_local.get(('MSG_INFO_PLA_PLATEFORM_DEACTIVATE',config.language)).format(plateform.name))
				if args.mode in [ARG_MODE_STATUS,ARG_MODE_IS_ENABLED,ARG_MODE_IS_DISABLED]:
					if plateform.path_desac=='':
						print plateform.name + ' est actif'
						if args.mode in [ARG_MODE_IS_ENABLED]:
							sys.exit(0)
						else:
							sys.exit(1)
					else:
						print plateform.name + ' est inactif'
						if args.mode in [ARG_MODE_IS_DISABLED]:
							sys.exit(0)
						else:
							sys.exit(1)
					
			except MyError:
				logger.error(msg_local.get(('MSG_DEBUG_PLA_ESSYSTEM_UNKNOW_PLATEFORM',config.language)).format(path_plateform))
					
			except Exception as exception:
				logger.error(msg_local.get(('MSG_ERROR_PLA_EXCEPTION',config.language)).format('platform.py',type(exception).__name__))
	
	#Fusion de configuration de plateforme------------------------------------------------------------------------
	elif args.mode in [ARG_MODE_MERGE]:
		
		try:
			iter(args.files)
		except:
			logger.error(msg_local.get(('MSG_ERROR_PLA_ARGUMENT_ERROR',config.language)).format('-f'))
			sys.exit(1)
		
		for files_src in args.files:
			
			if not os.path.isfile(files_src):
				logger.error(msg_local.get(('MSG_ERROR_PLA_SRC_NOT_FOUND',config.language)).format(files_src))
				sys.exit(1)
			
			#try:
			configs_ES_src = ESSystemList()	
			configs_ES_src.import_xml_file(files_src)
			#except Exception as exception:
				
			#	logger.critical(msg_local.get(('MSG_CRITICAL_PLA_ESSYSTEM_LOAD_ERROR2',config.language)).format(files_src))
			#	sys.exit(1)

			for system_src in configs_ES_src.get_systems():				
				try:
					system_dest = configs_ES.search_system_by_short_path(system_src.path)
					#plateforme trouvé, on écrase avec la source
					configs_ES.update_system(system_src)
					logger.info(msg_local.get(('MSG_INFO_PLA_PLATEFORM_UPDATE',config.language)).format(system_src.name))

				except MyError:
					#plateforme non trouvé, on ajoute
					configs_ES.add_system(system_src)
					logger.info(msg_local.get(('MSG_INFO_PLA_PLATEFORM_ADD',config.language)).format(system_src.name))
	
	#Print : lecture et affichage de l'ensemble des systemes du fichier es_systems-------------------------------------------
	elif args.mode in [ARG_MODE_LIST]:
		for system in configs_ES.get_systems():
			print_system(system)
		sys.exit(0)
	
	#test_add : test unitaire d'ajout d'un systeme---------------------------------------------------------------------------
	elif args.mode in [ARG_MODE_TEST_ADD]:
		system = ESSystem(name='test_name',fullname='test_fullname',desc='test_desc',
		path='test_path',path_desac='test_path_desac',extension='test extension',
		command='test command',platform='test plateform',theme='test theme',usermode='test usermode')
		emulator = ESSystemEmulator(name='test emulator')
		emulator.cores.append('test core 1-1')
		emulator.cores.append('test core 1-2')
		system.emulators.append(emulator)
		print_system(system)
		configs_ES.add_system(system)
	
	#test_upd : test unitaire de mise a jour d'un systeme--------------------------------------------------------------------
	elif args.mode in [ARG_MODE_TEST_UPD]:
		try:
			system_upd=configs_ES.search_system_by_path('test_path')
			system_upd.desc='test_desc_upd1'
			#system_upd.emulators=[]
			#system_upd.emulators[0].name='test emulator1'
			emulator = ESSystemEmulator(name='test emulator 2')
			emulator.cores.append('test core 2-1')
			system_upd.emulators.append(emulator)
			print_system(system_upd)
			configs_ES.update_system(system_upd)
		except Exception as exception:
			logger.error(msg_local.get(('MSG_ERROR_PLA_EXCEPTION',config.language)).format('platform.py',type(exception).__name__))
		
	#Sauvegarde
	configs_ES.save_xml_file(config.emulation_station_systems)
	
	#Fin
	sys.exit(0)

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	main()
