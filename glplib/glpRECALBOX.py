#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                              - GAMELISTPOWER -                               #
#                             - MODULE RECALBOX -                              #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.00 10/10/2018-10/06/2018 #
################################################################################

#IMPORT NORDICPOWER-------------------------------------------------------------
from glpTOOLS import *

#INIT SINGLETON-----------------------------------------------------------------
logger=Logger.logr

#CLASS-EMULATOR-----------------------------------------------------------------
class Emulator():

	def __init__(self,**kwargs):
	  self._name = ''
	  self._emulator = ''
	  self._core = ''
	  
	  if kwargs is not None:
			#mise à jour paramètre(s) nommé(s)
			self.__dict__.update(kwargs)

	#property-------------------------	
	@property
	def name(self):return self._name
	@property
	def emulator(self):return self._emulator
	@property
	def core(self):return self._core
		
	#setter-------------------------	
	@name.setter
	def name(self,v):self._name=v
	@emulator.setter
	def emulator(self,v):self._emulator=v
	@core.setter
	def core(self,v):self._core=v

#------------------------------------------------------------------------------
def getRecalBoxEmulators():
	# Extrait du fichier /usr/lib/python2.7/site-packages/configgen/emulatorlauncher.py
	# 20/04/2018 - 18.04.20
	
	# START
	# List emulators with their cores rest mupen64, scummvm
	emulators = dict()
	# Nintendo
	emulators["snes"] = Emulator(name='snes', emulator='libretro', core='pocketsnes')
	emulators["nes"] = Emulator(name='nes', emulator='libretro', core='fceunext')
	emulators["n64"] = Emulator(name='n64', emulator='mupen64plus', core='gliden64')
	emulators["gba"] = Emulator(name='gba', emulator='libretro', core='gpsp')
	emulators["gb"] = Emulator(name='gb', emulator='libretro', core='gambatte')
	emulators["gbc"] = Emulator(name='gbc', emulator='libretro', core='gambatte')
	emulators["fds"] = Emulator(name='fds', emulator='libretro', core='nestopia')
	emulators["virtualboy"] = Emulator(name='virtualboy', emulator='libretro', core='vb')
	emulators["gamecube"] = Emulator(name='gamecube', emulator='dolphin')
	emulators["wii"] = Emulator(name='wii', emulator='dolphin')
	emulators["nds"] = Emulator(name='nds', emulator='libretro', core='desmume')
	# Sega
	emulators["sg1000"] = Emulator(name='sg1000', emulator='libretro', core='genesisplusgx')
	emulators["mastersystem"] = Emulator(name='mastersystem', emulator='libretro', core='picodrive')
	emulators["megadrive"] = Emulator(name='megadrive', emulator='libretro', core='picodrive')
	emulators["gamegear"] = Emulator(name='gamegear', emulator='libretro', core='genesisplusgx')
	emulators["sega32x"] = Emulator(name='sega32x', emulator='libretro', core='picodrive')
	emulators["segacd"] = Emulator(name='segacd', emulator='libretro', core='picodrive')
	emulators["dreamcast"] = Emulator(name='dreamcast', emulator='reicast')
	# Arcade
	emulators["neogeo"] = Emulator(name='neogeo', emulator='fba2x')
	emulators["mame"] = Emulator(name='mame', emulator='libretro', core='mame078')
	emulators["fba"] = Emulator(name='fba', emulator='fba2x')
	emulators["fba_libretro"] = Emulator(name='fba_libretro', emulator='libretro', core='fba')
	emulators["advancemame"] = Emulator(name='advancemame', emulator='advmame')
	# Computers
	emulators["msx"] = Emulator(name='msx', emulator='libretro', core='bluemsx')
	emulators["msx1"] = Emulator(name='msx1', emulator='libretro', core='bluemsx')
	emulators["msx2"] = Emulator(name='msx2', emulator='libretro', core='bluemsx')
	emulators["amiga"] = Emulator(name='amiga', emulator='libretro', core='puae')
	emulators["amstradcpc"] = Emulator(name='amstradcpc', emulator='libretro', core='cap32')
	emulators["apple2"] = Emulator(name='apple2', emulator='linapple', videomode='default')
	emulators["atarist"] = Emulator(name='atarist', emulator='libretro', core='hatari')
	emulators["zxspectrum"] = Emulator(name='zxspectrum', emulator='libretro', core='fuse')
	emulators["o2em"] = Emulator(name='odyssey2', emulator='libretro', core='o2em')
	emulators["zx81"] = Emulator(name='zx81', emulator='libretro', core='81')
	emulators["dos"] = Emulator(name='dos', emulator='dosbox', videomode='default')
	emulators["c64"] = Emulator(name='c64', emulator='libretro', core='vice_x64')
	emulators["x68000"] = Emulator(name='x68000', emulator='libretro', core='px68k')
	#
	emulators["ngp"] = Emulator(name='ngp', emulator='libretro', core='mednafen_ngp')
	emulators["ngpc"] = Emulator(name='ngpc', emulator='libretro', core='mednafen_ngp')
	emulators["gw"] = Emulator(name='gw', emulator='libretro', core='gw')
	emulators["vectrex"] = Emulator(name='vectrex', emulator='libretro', core='vecx')
	emulators["lynx"] = Emulator(name='lynx', emulator='libretro', core='handy')
	emulators["lutro"] = Emulator(name='lutro', emulator='libretro', core='lutro')
	emulators["wswan"] = Emulator(name='wswan', emulator='libretro', core='mednafen_wswan', ratio='16/10')
	emulators["wswanc"] = Emulator(name='wswanc', emulator='libretro', core='mednafen_wswan', ratio='16/10')
	emulators["pcengine"] = Emulator(name='pcengine', emulator='libretro', core='mednafen_supergrafx')
	emulators["pcenginecd"] = Emulator(name='pcenginecd', emulator='libretro', core='mednafen_supergrafx')
	emulators["supergrafx"] = Emulator(name='supergrafx', emulator='libretro', core='mednafen_supergrafx')
	emulators["atari2600"] = Emulator(name='atari2600', emulator='libretro', core='stella')
	emulators["atari7800"] = Emulator(name='atari7800', emulator='libretro', core='prosystem')
	emulators["prboom"] = Emulator(name='prboom', emulator='libretro', core='prboom')
	emulators["psx"] = Emulator(name='psx', emulator='libretro', core='pcsx_rearmed')
	emulators["cavestory"] = Emulator(name='cavestory', emulator='libretro', core='nxengine')
	emulators["imageviewer"] = Emulator(name='imageviewer', emulator='libretro', core='imageviewer')
	emulators["scummvm"] = Emulator(name='scummvm', emulator='scummvm', videomode='default')
	emulators["colecovision"] = Emulator(name='colecovision', emulator='libretro', core='bluemsx')
	emulators["3do"] = Emulator(name='3do', emulator='libretro', core='4do')
	emulators["amiga600"] = Emulator(name='amiga600', emulator='amiberry')
	emulators["amiga1200"] = Emulator(name='amiga1200', emulator='amiberry')
	emulators["amigacd32"] = Emulator(name='amigacd32', emulator='amiberry')
	
	emulators["kodi"] = Emulator(name='kodi', emulator='kodi', videomode='default')
	emulators["moonlight"] = Emulator(name='moonlight', emulator='moonlight')
	emulators["psp"] = Emulator(name='psp', emulator='ppsspp')
	#STOP
	
	return emulators