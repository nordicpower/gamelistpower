#!/bin/sh
################################################################################
#                              - GAMELISTPOWER -                               #
#                      - INSTALL PLATEFORME COLLECTIONS -                      #
#------------------------------------------------------------------------------#
# Installation de la plateforme collections                                    #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.10 04/06/2018-30/09/2018 #
################################################################################

#INIT
PATH_DEST_ES_SYSTEMS=/recalbox/share_init/system/.emulationstation/es_systems.cfg
PATH_SRC_ES_SYSTEMS=./ressources/collections/es_systems.cfg
PATH_ROMS_COLLECTIONS=/recalbox/share/roms/collections
PATH_SRC_COLLECTION=./ressources/collections
PATH_ROMS_LINUXTOOLS=/recalbox/share/roms/linuxtools
PATH_SRC_FAVORI=./ressources/favori

mount -o remount,rw /

echo "Deploiement de la plateforme Collections"

################################################################################
#PREPARATION DU DOSSIER COLLECTION
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

if [ -d $PATH_SRC_COLLECTION ];then
	cp $PATH_SRC_COLLECTION/*.png $PATH_ROMS_COLLECTIONS/images
	chmod 777 "$PATH_SRC_COLLECTION/*.sh"
	cp "$PATH_SRC_COLLECTION/*.sh" $PATH_ROMS_COLLECTIONS
	cp $PATH_SRC_COLLECTION/*.txt $PATH_ROMS_COLLECTIONS
	echo "Copie des ressouces images, txt et sh"
fi


################################################################################
#PREPARATION DU DOSSIER LINUXTOOLS POUR LANCER FAVORI / COLLECTION
if [ -d $PATH_ROMS_LINUXTOOLS ];then
	#COLLECTION
	chmod 777 "$PATH_SRC_COLLECTION/*.sh"
	cp "$PATH_SRC_COLLECTION/*.sh" $PATH_ROMS_LINUXTOOLS
	
	#FAVORI
	chmod 777 $PATH_SRC_FAVORI/*.sh
	cp $PATH_SRC_FAVORI/*.sh $PATH_ROMS_LINUXTOOLS
	cp $PATH_SRC_FAVORI/*.jpg $PATH_ROMS_LINUXTOOLS/images
fi


################################################################################
#AJOUT DE LA PLATEFORME COLLECTION
echo "Ajout de la plateforme COLLECTION sous Emulation Station"
python system.py merge -f $PATH_SRC_ES_SYSTEMS


################################################################################
#LANCEMENT DE LA MISE A JOUR COLLECTION
echo "Lancement de la generation des lanceurs COLLECTION"
python gamelistpower.py generate_sh info


################################################################################
echo "Fin"
echo "Merci de rebooter pour prendre en compte la nouvelle plateforme"

