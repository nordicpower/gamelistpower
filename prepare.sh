#!/bin/sh
################################################################################
#                              - GAMELISTPOWER -                               #
#                      - INSTALL PLATEFORME COLLECTIONS -                      #
#------------------------------------------------------------------------------#
# Preparation de l'installation de la plateforme collections                   #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.00 16/06/2018-16/06/2018 #
################################################################################

echo ---------------------------------------------------------------------------
echo CREATION DU TAR
echo ---------------------------------------------------------------------------

#CUR_VERSION=$(basename $(pwd))
CUR_VERSION=09
CUR_DATE=$(date +%Y%m%d)

rm *.log

echo $CUR_DATE
tar czvf ../gamelistpower_${CUR_VERSION}_${CUR_DATE}.tar.gz ../gamelistpower

echo OK