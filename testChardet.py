#!/usr/bin/env python
#-*- coding: utf-8 -*-

#IMPORT STD---------------------------------------------------------------------
import os.path
import shutil
import argparse

from glplib import *

#---------------------------------------------------------------------------------------------------
#---------------------------------------- MAIN -----------------------------------------------------
#---------------------------------------------------------------------------------------------------
def main():

	print('amiga1200/gamelist.xml:'+predict_encoding('/mnt/d/dev-python/roms/amiga1200/gamelist.xml'))
	print('collections/gamelist.xml:'+predict_encoding('/mnt/d/dev-python/roms/collections/gamelist.xml'))
	print('lynx/gamelist.xml:'+predict_encoding('/mnt/d/dev-python/roms/lynx/gamelist.xml'))
	print('metal/gamelist.xml:'+predict_encoding('/mnt/d/dev-python/roms/metal/gamelist.xml'))
	print('nes/gamelist.xml:'+predict_encoding('/mnt/d/dev-python/roms/nes/gamelist.xml'))

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	main()
