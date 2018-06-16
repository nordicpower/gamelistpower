#!/bin/sh
################################################################################
#                              - GAMELISTPOWER -                               #
#                      - INSTALL PLATEFORME COLLECTIONS -                      #
#------------------------------------------------------------------------------#
# Installation de la plateforme collections                                    #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.00 04/06/2018-16/06/2018 #
################################################################################

#INIT
PATH_DEST_ES_SYSTEMS=/recalbox/share_init/system/.emulationstation/es_systems.cfg
PATH_ROMS_COLLECTIONS=/recalbox/share/roms/collections
PATH_SRC_IMAGES=./ressources/collections
PATH_SRC_ES_SYSTEMS=./ressources/collections/es_systems.cfg

mount -o remount,rw /

echo "Deploiement de la plateforme Collections"

################################################################################
#PREPARATION DU DOSSIER
echo "Gestion des dossiers"

if [ ! -d $PATH_ROMS_COLLECTIONS ];then
	mkdir $PATH_ROMS_COLLECTIONS
	chmod 777 $PATH_ROMS_COLLECTIONS
	echo "Creation du dossier $PATH_ROMS_COLLECTIONS"
	touch $PATH_ROMS_COLLECTIONS/gamelist.xml
fi

if [ ! -d $PATH_ROMS_COLLECTIONS/images ];then
	mkdir $PATH_ROMS_COLLECTIONS/images
	chmod 777 $PATH_ROMS_COLLECTIONS/images
	echo "Creation du dossier $PATH_ROMS_COLLECTIONS/images"
fi

if [ -d $PATH_SRC_IMAGES ];then
	cp $PATH_SRC_IMAGES/*.png $PATH_ROMS_COLLECTIONS/images
	chmod 777 $PATH_SRC_IMAGES/*.sh
	cp $PATH_SRC_IMAGES/*.sh $PATH_ROMS_COLLECTIONS
	echo "Copie des images et sh"
fi

################################################################################
#AJOUT DE LA PLATEFORME
echo "Gestion de la plateforme sous Emulation Station"

python system.py merge -f $PATH_SRC_ES_SYSTEMS


################################################################################
#LANCEMENT DE LA MISE A JOUR
echo "Lancement de la generation"

python gamelistpower.py generate_sh info

################################################################################
echo "Fin"
echo "Merci de rebooter pour prendre en compte la nouvelle plateforme"
