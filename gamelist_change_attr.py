#!/usr/bin/env python
#-*- coding: utf-8 -*-
################################################################################
#                     - EMULATIONSTATION GAMELIST PATCH -                      #
#                          --- CHANGE ATTRIBUT -----                           #
#------------------------------------------------------------------------------#
# NORDIC POWER amiga15@outlook.fr                 0.9.14 09/09/2018-03/09/2019 #
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
ARG_MODE_COPY_REGION_FROM_DEVELOPER='copy_region_from_developer'
ARG_MODE_COPY_EMPTY_REGION_FROM_PATH='copy_empty_region_from_path'
ARG_MODE_COPY_EMPTY_REGION_FROM_NAME='copy_empty_region_from_name'
ARG_MODE_COPY_DEV2PUBLISHER='copy_empty_publisher_from_developer'
ARG_MODE_COPY_PUBLISHER2DEV='copy_empty_developer_from_publisher'
ARG_MODE_COPY_GENRE_FROM_DESC='copy_genre_from_desc'

ARG_MODE_UPPER='upper'
ARG_MODE_UPPER_ALL='upper_all'

ARG_MODE_ADD_EMPTY_TAG='add_emptytag'
ARG_MODE_ADD_REGION_TITLE='add_region_title'

ARG_MODE_REMOVE='remove'
ARG_MODE_REMOVE_PLAYINFO='remove_playinfo'
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
ARG_MODE_CLEAN_FAVORITE='clean_favorite'
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
dico_region["Angleterre"]="ANGLETERRE"
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
dico_region["UK"]="ANGLETERRE"
dico_region["USA,Europe"]="USA, EUROPE"
dico_region["USA, Europe"]="USA, EUROPE"
##Moins récurrents
dico_region["Asia"]="ASIE"
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

#FBA/MAME
dico_region_dev = {}
dico_region_dev["ADK CORPORATION"]="JAPON" #ADK
dico_region_dev["ALPHA DENSHI"]="JAPON" #ADK
dico_region_dev["ALPHA DENSHI CO."]="JAPON" #ADK
dico_region_dev["AFEGA"]=u"COR\u00C9E DU SUD"
dico_region_dev["AICOM CORPORATION"]="JAPON"
dico_region_dev["ALLUMER LTD."]="JAPON"
dico_region_dev["AMENIP CORPORATION"]="CANADA"
dico_region_dev["AMERICAN SAMMY CORPORATION"]="USA"
dico_region_dev["AMSTAR ELECTRONICS"]="USA"
dico_region_dev["AMUSE WORLD"]=u"COR\u00C9E DU SUD"
dico_region_dev["ANDAMIRO ENTERTAINMENT CO.,LTD"]="TAÏWAN"
dico_region_dev["ANDAMIRO"]=u"COR\u00C9E DU SUD"
dico_region_dev["ARIKA CO., LTD."]="JAPON"
dico_region_dev["ART & MAGIC"]="BELGIQUE"
dico_region_dev["ATARI"]="USA"
dico_region_dev["ATARI, INC."]="USA" #1972-1984 
dico_region_dev["ATARI GAMES"]="USA"
dico_region_dev["ATARI GAMES CORP."]="USA" #1984-2000
dico_region_dev["ATARI GAMES CORPORATION"]="USA"
dico_region_dev["ATHENA"]="JAPON"
dico_region_dev["ATLUS"]="JAPON"
dico_region_dev["BALLY MIDWAY"]="USA"
dico_region_dev["BALLY MIDWAY MFG. CO."]="USA" 
dico_region_dev["BALLY SENTE INC."]="USA" 
dico_region_dev["BANPRESTO CO., LTD."]="JAPON"
dico_region_dev["BARKO CORP."]=u"COR\u00C9E DU SUD"
dico_region_dev["BOOTLEG"]="JAPON"
dico_region_dev["C.P. BRAIN"]="JAPON"
dico_region_dev["CALL ELECTRONICS"]=u"COR\u00C9E DU SUD"
dico_region_dev["CAPCOM"]="USA"
dico_region_dev["CAVE"]="JAPON"
dico_region_dev["CENTURI"]="USA"
dico_region_dev["CENTURY ELECTRONICS LTD."]="ANGLETERRE" #CVS
dico_region_dev["CINEMATRONICS"]="USA"
dico_region_dev["CINEMATRONICS, INC."]="USA"
dico_region_dev["CIDELSA"]="ESPAGNE" #ELECTRÓNICA FUNCIONAL OPERATIVA SA
dico_region_dev["CENTRO INDUSTRIAL DE DESARROLLOS ELECTRÓNICOS, S.A."]="ESPAGNE" #CIDELSA
dico_region_dev["COMAD INDUSTRY COMPANY, LIMITED."]=u"COR\u00C9E DU SUD"
dico_region_dev["COMAD"]=u"COR\u00C9E DU SUD"
dico_region_dev["CORELAND"]="JAPON"
dico_region_dev["COSMO ELECTRONICS CORPORATION"]="JAPON"
dico_region_dev["COASTAL AMUSEMENTS INC."]="USA"
dico_region_dev["CRUX"]="JAPON"
dico_region_dev["CVS"]="ANGLETERRE"
dico_region_dev["D-GATE"]=u"COR\u00C9E DU SUD"
dico_region_dev["DAEHYUN ELECTRONICS"]=u"COR\u00C9E DU SUD"
dico_region_dev["DAEJIN"]=u"COR\u00C9E DU SUD"
dico_region_dev["DATA EAST CORPORATION"]="USA"
dico_region_dev["DATA EAST DECO CASSETTE SYSTEM"]="USA"
dico_region_dev["DATA EAST USA"]="USA"
dico_region_dev["DATA EAST USA, INC."]="USA"
dico_region_dev["DENIAM CORP"]="ALLEMAGNE"
dico_region_dev["DENIAM"]=u"COR\u00C9E DU SUD"
dico_region_dev["DGPIX ENTERTAINMENT"]=u"COR\u00C9E DU SUD"
dico_region_dev["DIGITAL SILKROAD"]=u"COR\u00C9E DU SUD"
dico_region_dev["DONGSEO COMPUTOPIA"]=u"COR\u00C9E DU SUD"
dico_region_dev["DONGSUNG JOYCOM"]=u"COR\u00C9E DU SUD"
dico_region_dev["DONGYANG A.M."]=u"COR\u00C9E DU SUD"
dico_region_dev["DOOYONG"]=u"COR\u00C9E DU SUD"
dico_region_dev["E.G. FELACO"]="ITALIE"
dico_region_dev["EAST COAST COIN CO."]="AUSTRALIE"
dico_region_dev["EIGHTING"]="JAPON"
dico_region_dev["EIGHTING CO., LTD."]="JAPON"
dico_region_dev["EIM"]="JAPON"
dico_region_dev["ELECTRO SPORT INC."]="USA"
dico_region_dev["ELECTRO DESIGN CO.,LTD."]="JAPON"
dico_region_dev["ELECTRONIC DEVICES ITALY"]="ITALIE"
dico_region_dev["ELECTRÓNICA FUNCIONAL OPERATIVA, S.A."]="ESPAGNE"
dico_region_dev["ELETTRONOLO"]="ITALIE"
dico_region_dev["ELECTRONIC ARTS, INC."]="USA"
dico_region_dev["EM TECH"]=u"COR\u00C9E DU SUD"
dico_region_dev["ENTER-TECH"]="USA"
dico_region_dev["EOLITH"]=u"COR\u00C9E DU SUD"
dico_region_dev["EPOS CORPORATION"]="JAPON"
dico_region_dev["ESD"]=u"COR\u00C9E DU SUD"
dico_region_dev["ESOFNET"]=u"COR\u00C9E DU SUD"
dico_region_dev["EASTERN MICRO ELECTRONICS, INC."]="USA"
dico_region_dev["ENERDYNE TECHNOLOGIES INC."]="JAPON"
dico_region_dev["ENTER-TECH, LTD."]="USA"
dico_region_dev["EUMJEONG SYSCOM"]=u"COR\u00C9E DU SUD"
dico_region_dev["EXCELLENT SYSTEMS"]="JAPON"
dico_region_dev["EXPOTATO"]=u"COR\u00C9E DU SUD"
dico_region_dev["EXIDY"]="USA"
dico_region_dev["EXIDY, INC."]="USA"
dico_region_dev["F2 SYSTEM"]=u"COR\u00C9E DU SUD"
dico_region_dev["FACE"]="JAPON"
dico_region_dev["FORTE II GAMES"]="BR\u00C9SIL"
dico_region_dev["FUJITEK"]="JAPON"
dico_region_dev["FUUKI"]="JAPON"
dico_region_dev["FUUKI CO. LTD."]="JAPON"
dico_region_dev["GAELCO"]="ESPAGNE"
dico_region_dev["GAELCO, S.A."]="ESPAGNE"
dico_region_dev["GAME IQ"]=u"COR\u00C9E DU SUD"
dico_region_dev["GAME KOREA"]=u"COR\u00C9E DU SUD"
dico_region_dev["GAME PLUS"]=u"COR\u00C9E DU SUD"
dico_region_dev["GAME STUDIO"]=u"COR\u00C9E DU SUD"
dico_region_dev["GAMETECH"]=u"COR\u00C9E DU SUD"
dico_region_dev["GAMEPLAN INC."]=u"USA"
dico_region_dev["GC TECH"]=u"COR\u00C9E DU SUD"
dico_region_dev["GISEONG"]=u"COR\u00C9E DU SUD"
dico_region_dev["GLOBAL CORPORATION"]="USA"
dico_region_dev["GOTTLIEB"]="USA"
dico_region_dev["HANAHO GAMES"]="USA"
dico_region_dev["HANARO"]=u"COR\u00C9E DU SUD"
dico_region_dev["HANIL JEONJA"]=u"COR\u00C9E DU SUD"
dico_region_dev["HICOM / ESOFNET"]=u"COR\u00C9E DU SUD"
dico_region_dev["HOEI CORPORATION"]="JAPON"
dico_region_dev["HOME DATA"]="JAPON" #MAGICAL COMPANY
dico_region_dev["HOME DATA INC."]="JAPON"
dico_region_dev["HOME DATA CORP."]="JAPON"
dico_region_dev["HOT-B CO., LTD."]="JAPON"
dico_region_dev["HUDSON SOFT COMPANY, LIMITED"]="JAPON"
dico_region_dev["HUMAN ENTERTAINMENT"]="JAPON"
dico_region_dev["ICE OF AMERICA"]="USA"
dico_region_dev["IDSA"]="ESPAGNE"
dico_region_dev["IGS"]="TAÏWAN" 
dico_region_dev["INCREDIBLE TECHNOLOGIES"]="USA"
dico_region_dev["INTERZONE 21"]=u"COR\u00C9E DU SUD"
dico_region_dev["IPM CORP."]="JAPON" #IREM
dico_region_dev["ITISA ELECTRONICS"]="ESPAGNE"
dico_region_dev["IREM"]="JAPON"
dico_region_dev["ITCHELL CORPORATION"]="JAPON"
dico_region_dev["JALECO"]="JAPON"
dico_region_dev["JALECO LTD."]="JAPON"
dico_region_dev["JAMP"]="JAPON"
dico_region_dev["JCC SOFT"]=u"COR\u00C9E DU SUD"
dico_region_dev["JETSOFT"]="USA"
dico_region_dev["JOOYOUN"]=u"COR\u00C9E DU SUD"
dico_region_dev["JUNGWON"]=u"COR\u00C9E DU SUD"
dico_region_dev["KANEKO CO.,LTD."]="JAPON" #KANEKO
dico_region_dev["KANEKO SEISAKUSHO CO.,LTD."]="JAPON" #KANEKO
dico_region_dev["KARAM"]=u"COR\u00C9E DU SUD"
dico_region_dev["KEE GAMES"]="USA" #ATARI
dico_region_dev["KONAMI"]="JAPON"
dico_region_dev["KONAMI INDUSTRY CO. LTD."]="JAPON"
dico_region_dev["KOUYOUSHA LTD"]="JAPON"
dico_region_dev["KUMKANG"]=u"COR\u00C9E DU SUD"
dico_region_dev["KUMYUNG"]=u"COR\u00C9E DU SUD"
dico_region_dev["LAI GAMES"]="AUSTRALIE"
dico_region_dev["LELAND"]="USA"
dico_region_dev["LELAND CORP."]="USA"
dico_region_dev["LELAND CORPORATION"]="USA"
dico_region_dev["MAGICAL COMPANY"]="JAPON" #HOME DATA
dico_region_dev["METRO"]="JAPON"
dico_region_dev["MIDAS ENGINEERING"]=u"COR\u00C9E DU SUD"
dico_region_dev["MIDCOIN"]="ITALIE"
dico_region_dev["MIDWAY"]="USA"
dico_region_dev["MIDWAY MANUFACTURING COMPANY"]="USA"
dico_region_dev["MIDWAY MFG. CO."]="USA"
dico_region_dev["MIJIN COMPUTER"]=u"COR\u00C9E DU SUD"
dico_region_dev["MIJIN"]="JAPON"
dico_region_dev["MIN CORPORATION"]=u"COR\u00C9E DU SUD"
dico_region_dev["MITCHELL CORPORATION"]="JAPON"
dico_region_dev["MIZI PRODUCTION"]=u"COR\u00C9E DU SUD"
dico_region_dev["MONDIAL GAMES"]="ITALIE"
dico_region_dev["MONOLITH"]="JAPON"
dico_region_dev["MOSS CO.,LTD."]="JAPON"
dico_region_dev["MULTIMEDIA CONTENT"]=u"COR\u00C9E DU SUD"
dico_region_dev["MYLSTAR ELECTRONICS"]="USA"
dico_region_dev["NAMCO"]="JAPON"
dico_region_dev["NAMCO LIMITED"]="JAPON"
dico_region_dev["NASCO"]="JAPON"
dico_region_dev["NAXAT SOFT"]="JAPON"
dico_region_dev["NGF DEV"]="FRANCE"
dico_region_dev["NICHIBUTSU"]="JAPON" ##Nom usuel de NIHON BUSSAN
dico_region_dev["NICS"]=u"COR\u00C9E DU SUD"
dico_region_dev["NIEMER"]="ESPAGNE"
dico_region_dev["NIHON BUSSAN CO., LTD."]="JAPON"
dico_region_dev["NIHON SYSTEM INC"]="JAPON"
dico_region_dev["NINTENDO"]="JAPON"
dico_region_dev["NINTENDO CO., LTD."]="JAPON"
dico_region_dev["NIPPON AMUSE CO-LTD"]="JAPON"
dico_region_dev["NMK"]="JAPON"
dico_region_dev["NMK CO. LTD."]="JAPON"
dico_region_dev["NPLEX"]=u"COR\u00C9E DU SUD"
dico_region_dev["OCEAN OF AMERICA, INC."]="USA"
dico_region_dev["OCEAN SOFTWARE"]="USA"
dico_region_dev["OMORI ELECTRIC CO., LTD."]="JAPON" #OEC
dico_region_dev["OKSAN"]=u"COR\u00C9E DU SUD"
dico_region_dev["OMORI ELECTRIC CO., LTD."]="JAPON"
dico_region_dev["ORCA CORPORATION"]="JAPON"
dico_region_dev["PACIFIC NOVELTY"]="USA"
dico_region_dev["PARA ENTERPRISE"]=u"COR\u00C9E DU SUD"
dico_region_dev["PARA"]=u"COR\u00C9E DU SUD"
dico_region_dev["PENI SOFT"]="JAPON"
dico_region_dev["PENTAVISION"]=u"COR\u00C9E DU SUD"
dico_region_dev["PHILKO CORPORATION"]=u"COR\u00C9E DU SUD"
dico_region_dev["PLAYMARK"]="ITALIE"
dico_region_dev["PLAYWORKS"]=u"COR\u00C9E DU SUD"
dico_region_dev["PROMAT"]=u"COR\u00C9E DU SUD"
dico_region_dev["PROMAT CO., LTD."]=u"COR\u00C9E DU SUD"
dico_region_dev["PSIKYO"]="JAPON"
dico_region_dev["PURSEONE"]=u"COR\u00C9E DU SUD"
dico_region_dev["RAIZING"]="JAPON"
dico_region_dev["RAIZING CO., LTD."]="JAPON"
dico_region_dev["RAMTEK"]="USA"
dico_region_dev["RARE"]="ANGLETERRE"
dico_region_dev["RARE LTD."]="ANGLETERRE"
dico_region_dev["ROMSTAR INC."]="USA"
dico_region_dev["SABA VIDEOPLAY"]="JAPON"
dico_region_dev["SAMMY"]="JAPON"
dico_region_dev["SAMMY CORPORATION"]="JAPON"
dico_region_dev["SAMMY USA CORPORATION"]="USA"
dico_region_dev["SAMWON"]=u"COR\u00C9E DU SUD"
dico_region_dev["SANRITSU DENKI"]="JAPON"
dico_region_dev["SANRITSU ELECTRONICS CO., LTD."]="JAPON"
dico_region_dev["SEGA"]="JAPON"
dico_region_dev["SEGA ENTERPRISES LTD."]="JAPON"
dico_region_dev["SEGO ENTERTAINMENT"]=u"COR\u00C9E DU SUD"
dico_region_dev["SEIBU DENSHI"]="JAPON"
dico_region_dev["SEIBU KAIHATSU"]="JAPON"
dico_region_dev["SEMICOM"]=u"COR\u00C9E DU SUD"
dico_region_dev["SEOUL COIN CORP."]=u"COR\u00C9E DU SUD"
dico_region_dev["SEOUL COIN"]=u"COR\u00C9E DU SUD"
dico_region_dev["SERGI"]="JAPON"
dico_region_dev["SESAME JAPAN"]="JAPON"
dico_region_dev["SETA CORPORATION"]="JAPON"
dico_region_dev["SETA"]="JAPON"
dico_region_dev["SEUNGYEON"]=u"COR\u00C9E DU SUD"
dico_region_dev["SHARP TRAVEL SERVICE"]=u"COR\u00C9E DU SUD"
dico_region_dev["SHINKAI INC."]="JAPON"
dico_region_dev["SHOEISHA CO., LTD."]="JAPON"
dico_region_dev["SIGMA ENTERPRISES"]="JAPON"
dico_region_dev["SIGMA ENTERPRISES INC."]="JAPON"
dico_region_dev["SIGMA"]="JAPON"
dico_region_dev["SIGNATRON USA"]="USA"
dico_region_dev["SKONEC ENTERTAINMENT"]=u"COR\u00C9E DU SUD"
dico_region_dev["SNK"]="JAPON"
dico_region_dev["SOFT ART"]=u"COR\u00C9E DU SUD"
dico_region_dev["SOFT ART CO."]=u"COR\u00C9E DU SUD"
dico_region_dev["STERN ELECTRONICS, INC."]="USA"
dico_region_dev["SUBSINO"]="JAPON"
dico_region_dev["SUCCESS"]=u"COR\u00C9E DU SUD"
dico_region_dev["SUNA"]=u"COR\u00C9E DU SUD"
dico_region_dev["SUN ELECTRONICS"]="JAPON" #SUN
dico_region_dev["SUNSOFT"]="JAPON" #SUN
dico_region_dev["TAD CORPORATION"]="JAPON"
dico_region_dev["TAEGEUK MUYEOK"]=u"COR\u00C9E DU SUD"
dico_region_dev["TAEJIN MEDIA"]=u"COR\u00C9E DU SUD"
dico_region_dev["TAGO ELECTRONICS"]="USA"
dico_region_dev["TAITO AMERICA"]="USA"
dico_region_dev["TAITO CORPORATION"]="JAPON"
dico_region_dev["TAITO DO BRASIL"]="BRÉSIL"
dico_region_dev["TAIYO SYSTEM"]="JAPON"
dico_region_dev["TAKUMI CORPORATION"]="JAPON"
dico_region_dev["TAKARA"]="JAPON"
dico_region_dev["TAMTEX"]="JAPON"
dico_region_dev["TATSUMI"]="JAPON"
dico_region_dev["TATSUMI ELECTRONICS CO., LTD."]="JAPON"
dico_region_dev["TCH SA"]="ESPAGNE"
dico_region_dev["TECFRI"]="USA"
dico_region_dev["TECMO"]="JAPON"
dico_region_dev["TECMO, LTD."]="JAPON"
dico_region_dev["TEHKAN LTD."]="JAPON" #TECMO LTD.
dico_region_dev["TECHNOS JAPAN CORP."]="JAPON"
dico_region_dev["TERMINAL REALITY"]="RUSSIE"
dico_region_dev["THE GAME ROOM"]="USA"
dico_region_dev["TOAPLAN CO., LTD."]="JAPON"
dico_region_dev["TOSE CO., LTD."]="JAPON"
dico_region_dev["TRIVISION"]=u"COR\u00C9E DU SUD"
dico_region_dev["TRUST"]=u"COR\u00C9E DU SUD"
dico_region_dev["U.S. GAMES"]="USA"
dico_region_dev["UNIANA"]=u"COR\u00C9E DU SUD"
dico_region_dev["UNICO"]=u"COR\u00C9E DU SUD"
dico_region_dev["UNICO ELECTRONICS CO., LTD."]=u"COR\u00C9E DU SUD"
dico_region_dev["UNIVERSAL ENTERTAINMENT CORPORATION"]="JAPON"
dico_region_dev["UNIVERSAL CO., LTD."]="JAPON"
dico_region_dev["UPL CO., LTD"]="JAPON"
dico_region_dev["V-SYSTEM CO."]="JAPON"
dico_region_dev["VALADON AUTOMATION"]="FRANCE"
dico_region_dev["VEB POLYTECHNIK KARL-MARX-STAD"]="ALLEMAGNE"
dico_region_dev["VENTURE LINE"]="USA"
dico_region_dev["VENTURE LINE INC."]="USA"
dico_region_dev["VICCOM"]=u"COR\u00C9E DU SUD"
dico_region_dev["VIDEO SYSTEM CO., LTD."]="JAPON"
dico_region_dev["VID KIDZ"]="USA"
dico_region_dev["VIDEO GAMES GMBH"]="ALLEMAGNE"
dico_region_dev["VISCO GAMES"]="JAPON"
dico_region_dev["VISION"]=u"COR\u00C9E DU SUD"
dico_region_dev["WECOM"]=u"COR\u00C9E DU SUD"
dico_region_dev["WHITEBOARD"]="JAPON"
dico_region_dev["WILLIAMS ELECTRONICS INC."]="USA"
dico_region_dev["WINDEAL"]=u"COR\u00C9E DU SUD"
dico_region_dev["WING CO."]="USA"
dico_region_dev["WINKY SOFT"]="JAPON"
dico_region_dev["YACHIYO ELECTRONICS"]="JAPON"
dico_region_dev["YUGA"]="JAPON"
dico_region_dev["YUMYEONG JEONJA"]=u"COR\u00C9E DU SUD"
dico_region_dev["YUN SUNG"]=u"COR\u00C9E DU SUD"
dico_region_dev["YUWON TECH"]=u"COR\u00C9E DU SUD"
dico_region_dev["ZACCARIA"]="ITALIE"
dico_region_dev["ZEUS SOFTWARE"]="ESPAGNE"
dico_region_dev["ZILEC ELECTRONICS"]="ANGLETERRE"

#NEOGEO
dico_region_dev["AICOM"]="JAPON"
dico_region_dev["BREZZASOFT"]="JAPON"
dico_region_dev["NAZCA CORPORATION"]="JAPON"
dico_region_dev["NOISE FACTORY"]="JAPON"
dico_region_dev["SAURUS"]="JAPON"
dico_region_dev["WAVE CORP"]="JAPON"
dico_region_dev["YUKI ENTERPRISE"]="JAPON"
dico_region_dev["YUMEKOBO"]="JAPON" #anciennement AICOM


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
	parser.add_argument(ARG_MODE,choices=[
		ARG_MODE_UPPER,ARG_MODE_UPPER_ALL,
		
		ARG_MODE_COPY_REGION_FROM_PATH,ARG_MODE_COPY_EMPTY_REGION_FROM_PATH,ARG_MODE_COPY_EMPTY_REGION_FROM_NAME,
		ARG_MODE_COPY_GENRE_FROM_DESC,ARG_MODE_REMOVE_ID,ARG_MODE_CLEAN_GENRE,ARG_MODE_COPY_REGION_FROM_DEVELOPER,
		
		ARG_MODE_REMOVE,ARG_MODE_REMOVE_PLAYINFO,ARG_MODE_ADD_EMPTY_TAG,
		ARG_MODE_REMOVE_EMPTY_TAG,ARG_MODE_COPY_DEV2PUBLISHER,ARG_MODE_COPY_PUBLISHER2DEV,
		
		ARG_MODE_ADD_REGION_TITLE,ARG_MODE_REMOVE_REGION_TITLE,
		
		ARG_MODE_CLEAN_DEVELOPER,ARG_MODE_CLEAN_PUBLISHER,ARG_MODE_CLEAN_FAVORITE,
		ARG_MODE_CLEAN_PLAYERS,ARG_MODE_CLEAN_DESC,ARG_MODE_CLEAN_ALL,ARG_MODE_CLEAN_NAME,ARG_MODE_CLEAN_DATE
		], 
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
	
	if args.mode in [ARG_MODE_COPY_REGION_FROM_DEVELOPER]:
		for game in gamesList.get_games():
			if game.region=="":
				try:
					new_region=dico_region_dev[game.developer]
					print('Update region '+new_region+' to '+game.name)
					game.region=new_region
					gamesList.update_game(game)
					bChanged=True
				except:
					print('Unknow region from '+ game.developer)
						
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
	
	if args.mode in [ARG_MODE_CLEAN_DEVELOPER,ARG_MODE_CLEAN_ALL]:
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
	
	if args.mode in [ARG_MODE_CLEAN_PUBLISHER,ARG_MODE_CLEAN_ALL]:
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
	
	if args.mode in [ARG_MODE_CLEAN_FAVORITE,ARG_MODE_CLEAN_ALL]:
		for game in gamesList.get_games():
			if game.favorite !='':
				if game.favorite in ['Y','YES','Yes','yes']:
					print('Update favorite '+game.favorite+' to True to '+game.name+')')
					game.favorite=True
					gamesList.update_game(game,False)
					bChanged=True
				if game.favorite in ['N','NO','No','no']:
					print('Update favorite '+game.favorite+' to False to '+game.name+')')
					game.favorite=False
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
