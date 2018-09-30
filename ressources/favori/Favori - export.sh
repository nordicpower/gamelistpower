#!/bin/bash
################################################################################
#                              - GAMELISTPOWER -                               #
#------------------------------------------------------------------------------#
# EXPORT DES INFORMATIONS JEUX FAVORI / PLAYINFO / HIDDEN                      #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.10 28/09/2018-28/09/2018 #
################################################################################

#Suppression des 3 derniers arguments
set -- "${@:1:$#-1}"

END_IMG="/recalbox/share/roms/linuxtools/images/Favori-Export-Okay.jpg"

################################################################################
#EXPORT
cd /recalbox/scripts/gamelistpower
python gamelist_favori.py export --hidden --playinfo
cd -

################################################################################
#AFFICHAGE IMAGE FIN
python /usr/lib/python2.7/site-packages/configgen/emulatorlauncher.pyc "$@" -system imageviewer -rom "$END_IMG" -emulator default -core default -ratio auto
echo fin
