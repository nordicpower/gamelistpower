EMULATIONSTATION GAMELISTPOWER
==============================
# Readme / lisez-moi
***Par Nordicpower***
*amiga15@outlook.fr / https://twitter.com/nordicpower*
***Mai 2018***

L'objectif de GameListPatch est d'améliorer les fichiers **gamelist.xml** de EmulationStation http://emulationstation.org/
en ajoutant des nouvelles fonctionnalités en créant automatiquement des nouvelles entrées, par exemple :
- Les derniers jeux joués
- Les Top des jeux joués
- L'organisation sous-forme de dossiers
- Des images par défaut pour les jeux
---

Le projet est né à cause du scrapper par défaut d'EmulationStation. Celui-ci ne permet pas de gérer les dossiers, alors 
que EmulationStation les supporte. Je créé initialement ceux-ci donc à la main dans le fichier gamelist.xml 
mais ils étaient perdus à chaque exécution du scrapper, idem pour les images de jeux que j'ajoutais. 
J'ai donc décidé d'automatiser tout cela dans l'objectif de me faire la main sur le langage python.

Les développements ont été réalisés avec :
* Python
* Pygame pour la partie graphique, disponible en standard sur RaspberryPi
* Interphase (http://gatc.ca/projects/interphase) pour l'affichage de la texte box avec des boutons

Je remercie JBAM pour avoir créer happigc et happiga, quel plaisir de jouer sur nos anciennes plateformes
à travers le RasberryPi. http://www.bpj-studio.fr/_happi/fr-telechargement.html
Et c'est français !!


## Fonctions au niveau des roms :
* Ajout des roms non présentes dans le gamelist.xml (avec gestion exclusion de noms et extensions)
* Ajout des images de roms non présentes dans le gamelist.xml (on ajoute une image avec le bon nom et on lance)
* Gestion des déplacements de roms au sein du dossier de l'émulateur (pratique lors du déplacement de roms)

Le script permet de gérer 3 sources d'images distinctes :

 1. en se basant sur le nom de la rom, il recherche son image dans ./images/nom_rom+'-image.'+extension image
 2. idem si la rom se trouve dans un sous dossier, il recherche dans ./sousdossier/images/nom_rom+'-image.'+extension image
 3. sinon, il positionne l'image du dossier par défaut

## Fonctions au niveau des dossiers :
* Gestion d'un dossier TOP pour les jeux les plus joués
* Gestion d'un dossier LAST pour les jeux dernièrement joués
* Gestion d'un dossier BEST pour les meilleurs jeux
* Gestion d'un dossier ROMS KO pour archiver les jeux qui ne fonctionnent pas
* Ajout des dossiers dans Gamelist.xml avec une image
* Suppression des dossiers inexistants
	
Le script permet de gérer 4 sources d'images distinctes :
 1. en se basant sur le nom du dossier, il recherche son image dans ./images/nom_dossier+'-image.'+extension image
 2. en se basant sur le nom du dossier, il recherche dans ./nom_dossier/images/nom_dossier+'-image.'+extension image
 3. si le nom est identifié comme celui des roms KO, il positionne l'image dédié (voir fichier de configuration)
 4. sinon, il positionne l'image du dossier par défaut


## Deux astuces pour les images par défaut :
- si l'image du dossier par défaut ne convient pas, créer une image avec le bon nom selon la règle :
  nom_dossier/rom+'-image.'+extension image, elle sera automatiquement remplacée lors de l'exécution suivante
- si on souhaite remplacer l'image par défaut, il faut positionner le mode suppression, exécuter le script, changer le nom de l'image et positionner le mode ajout

## Quelques trucs à dire :
- La détection d'un dossier à traiter est effectuée par la présence d'un fichier gamelist.xml, même vide
- Cas de neogeo, il faut positionner le fichier rom dans tous les sous-répertoires pour l'émulateur
- EmulationStation n'aime pas le GIF :-< et les liens symboliques
- Le code python est surement optimisable ...

-------

#Installation

les fichiers suivants sont nécessaires pour installer le patch

a) Dossier existant /home/pi/happi/config/scraper

CALCULER TOP.sh									: lancement mise à jour des dossiers TOP, LAST et BEST
CORRIGER METADONNEES (DEBUG).sh : lancement correction gamelist avec log au niveau debug
CORRIGER METADONNEES.sh        	: lancement correction gamelist
LISTER ROMS SANS IMAGE.sh       : lancement liste des roms sans image associée

Attention à positionner l'attribut d'exécution sur ces fichiers.


b) Dossier /home/pi/happi/config/scraper/gamelistpatch 

- interphase/*												: module interphase pour la gestion graphique (24 fichiers)
- checkxml.py													: permet de tester la validité d'un fichier gamelist.xml
- CHANGELOG.md												: détails des modifications apportées	
- folder-bestgames-image.png					: l'image par défaut du dossier des meilleurs jeux
- folder-default-image.png						: l'image par défaut des dossiers sans image
- folder-KO-image.png									: l'image par défaut du dossier des ROM KO
- folder-lastgames-image.png					: l'image par défaut du dossier des jeux joués récemment
- folder-topgames-image.png						: l'image par défaut du dossier des jeux les plus joués
- game-default-image.png							: l'image par défaut des roms de jeu
- GameListDir.py											: module python dédié aux accès disque
- GameListEsSystem.py									: module python dédié à l'accès à la configuration de emulation Station
- GameListGen.py											: module python dédié à la gestion des launchers (multi-émulateurs)
- GameListPatch.ini										: les paramètres du patch
- GameListPatch.png                   : l'image de fond de la version graphique
- GameListPatch.mp3										: musique pour la version graphique (non fournie)
- GameListPatch.py										: Moteur du patch et lancement en mode console
- GameListPatchG.py										: Lancement en mode graphique
- GameListTools.py										: module python dédié aux fonctions diverses
- GameListXml.py											: module python dédié à la manipulation du XML
- mergexml.py													: script permettant de merger un fichier gamelist.xml dans un autre
- plateform.py												: script permettant d'ajouter/modifier/activer/desactiver une plateforme
- quickupdate.py											: script maj attribut d'un jeu lors du lancement de celui-ci
- README.md														: ce fichier

c) dossier /home/pi/.happi/script

- es_launch.sh												: nouveau script de lancement des roms définis dans /etc/emulationstation/es_system.cfg

d) dossier /home/pi/.happi/script

- es_systems.cfg											: nouveau paramétrage de emulationstation (appel de es_launch)


#Configuration

La configuration est disponible dans le fichier GameListPatch.ini	

[directories]
;Définition du dossier racine où se trouve les roms
rom=/home/pi/happi/roms
;Définition d'une seconde liste (Optionnel)
rom_usb=/home/pi/happi/roms_usb/rom

;Liste de dossiers à exclure (à séparer par des virgules)  
exclusion_directories=/home/pi/happi/roms/arcade/fba/downloaded_images,/home/pi/happi/roms/console/psp/PPSSPP

;Liste des extensions des fichiers images supportés par le script
;celui recherche des images sous la forme nomrom + "-images." + extension_image
image_extension=jpg,png

;liste des folders avec des images
image_folder=images,downloaded_images

;liste des entrées folder à cocher (balise <hidden>)
hidden_name=downloaded_images

;activation de l'attribut refresh pour calculer TOP/LAST si changement entre deux exécutions (modification par quickupdate.py)
hint_use_refresh_tag=1
;activation de os.stat pour calculer les images données disque et réaliser vérification roms/images que si changement
hint_use_os_stat=1

;dossier multi-émulateurs
folder_multi=/home/pi/happi/divers/multi

[game]
;Exclusion des fichiers
;liste d'exclusion d'extensions dans la recherche des roms
exclusion_extension=txt,nv
;liste d'exclusion par une liste de noms dans la recherche des roms
exclusion_name=MAME  -0.78-JBAM.zip,MAME - Bios Pack.zip,lynxboot.img,disksys.rom,gba_bios.bin,eu_mcd1_9210.bin,jp_mcd1_9112.bin,us_scd1_9210.bin,SCPH1001.BIN,panafz10.bin,syscard3.pce,neogeo.zip,pgm.zip,o2rom.bin,DISK.ROM,MSX2P.ROM,MSX2PEXT.ROM
;liste des entrées game à cocher (balise <hidden>)
hidden_name=neogeo.zip

;Mode de gestion de l'image par défaut (si aucune image trouvée selon le modèle nomrom + "-images." + extension_image pour les roms)
;chemin de l'image
default_image=~/happi/config/scraper/gamelistpatch/game-default-image.png
;Le mode (A)jout permet d'ajouter
;Le mode (S)uppression permet de supprimer
mode_image=A

;Mode de suppression des noeuds game
; Le mode (R) pour le dossier ROMS KO
; Le mode (D) pour désactiver
; Le mode (T) pour tous les dossiers
mode_delete=T


[folder]

;Dossier par defaut
;Le mode (A)jout permet d'ajouter l'image par défaut des dossiers
;Le mode (S)uppression permet les images par défaut des dossiers
default_mode_image=A
;Image par défaut si aucune image trouvée selon le modèle nomrom + "-images." + extension_image pour les dossiers
default_image=~/happi/config/scraper/gamelistpatch/folder-default-image.png

;Dossier KO
;Nom du dossier KO sur le disque
ko_name_directory=ROMS_KO
;Le mode (A)jout permet d'ajouter l'image par défaut des dossiers KO
;Le mode (S)uppression permet les images par défaut des dossiers KO
ko_mode_image=A
;Nom du dossier affiché dans le gamelist et à l'écran
;(&nbsp; est remplacé par un espace)
ko_name_xml=&nbsp;KO GAMES
;Image par défaut des dossiers stockants les ROMS KO de chaque émulateur
ko_image=~/happi/config/scraper/gamelistpatch/folder-KO-image.png


;Dossier TOP
top_name_directory=TOP
top_number=9
top_mode_image=A
top_name_xml=&nbsp;TOP GAMES
top_image=~/happi/config/scraper/gamelistpatch/folder-topgames-image.png


;Dossier LAST
last_name_directory=LAST
last_number=9
last_mode_image=A
last_name_xml=&nbsp;LAST GAMES
last_image=~/happi/config/scraper/gamelistpatch/folder-lastgames-image.png


;Dossier BEST
best_name_directory=BEST
best_number=9
best_mode_image=A
best_name_xml=&nbsp;BEST GAMES
best_image=~/happi/config/scraper/gamelistpatch/folder-bestgames-image.png


[save]
;Sauvegarde du fichier gamelist.xml à la première exécution
origin=True

;Sauvegarde d'un backup à chaque éxecution
backup=True

[emulation_station]
;fichier de paramétrage de emulation station
es_systems=/etc/emulationstation/es_systems.cfg

[localisation]
;Langues FR,EN supportées
language=FR

[rules]
;règles de génération de lanceur
flipper1=genre,pinball,/home/pi/happi/divers/multi/pinball
flipper2=genre,flipper,/home/pi/happi/divers/multi/pinball
outrun=name,outrun,/home/pi/happi/divers/multi/outrun
best=path,/BEST/,/home/pi/happi/divers/multi/BEST

#Log
Un fichier de log est généré dans **/home/pi/happi/config/scraper/gamelistpatch/GameListPatch.log** 

#Divers
Un fichier /home/pi/happi/config/scraper/gamelistpatch/gamelist.hash est généré afin de conserver un hash des images des dossiers
Cela permet de ne pas lancer la vérification des roms ou images si aucun changement entre deux exécutions

----------
Editeur MD : https://stackedit.io/editor

