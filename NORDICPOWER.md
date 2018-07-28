EMULATIONSTATION GAMELISTPOWER
================================
# Change Log
***NORDIC POWER amiga15@outlook.fr***

# [0.9.05] 2018-07-11 (Version public)
###GameGen
* Ajout d'un nouveau noeud <destinationName> permettant de modifier le nom du 
  dossier dans le gamelist.xml
* Ajout d'un nouveau noued <gamelistInfoFile> permettant de remplacer les 
  informations des noeuds <game> trouvés par des informations de ce gamelist
#rules_gensh.xml
* Ajout d'une nouvelle règle pour les jeux Turiccan
* Réactualisation des règles avec des exclusions

# [0.9.02] 2018-07-11 (Version public)
###Gamelist.xml
* Support de l'attribut <hash>

# [0.9.02] 2018-06-11 (Version public)
###GameGen
* Création automatique du fichier gamelist.xml si inexistant
* Support de RecalBox 18.06.27

# [0.9.00] 2018-06-11 (Version public)
###GameGen
* Support de la chaine de commande de recalbox
* Gestion de l'attribut hidden en exclusion de la recherche
* Suppression des doublons si deux règles renvoient la même rom
* Ajout de l'option <preserveFavorite> afin de conserver ou non l'attribut favorite dans le gamelist cible
* Support fichier rules_gensh.xml au lieu des règles dans gamelistpower.ini
* Création du dossier destination si inexistant
* Ajout des exclusions par path
* Préservation des comptages lancement/date dans gamelist.xml destination
* Support fichier rules_romcpy.xml pour generer une plateforme par recopie de roms
* Exclusion auto *.sh pour le mode romcpy
* Skip des entrees gamelist.xml ou la rom n'existe pas
* Support d'un format personalisé pour les titres des roms
* Amiberry, dosbox et scummvm non supporté en mode romcpy
###Gamelist.xml
* Support des attributs emulator, core et ratio au niveau des opérations XML + recherche
* Support du Charset Windows-1252
* Support des attributs recalbox thumbnail, romtype
###Plateform
* Lecture/Ecriture de la structure emulators/emulator/cores/core dans es_systems.cfg de recalbox
###Divers
* Arrêt de GameListPatch (Happigc) et lancement de GameListPower (Recalbox)
* Renommage des fichiers modules en glp*.py et position dans le dossier glplib
* Ajout de chardet https://pypi.org/project/chardet/ (LGPL)
* Log dans /recalbox/share/system/logs/gamelistpower.log
* Ini dans gamelistpower.ini
* Ajout de fichier "X - Refresh.sh" dans le dossier collections pour lancer le script à travers recalbox

#-----------------------------------------------------------------------------------------

# [0.8.08] 2018-02-11 (Version privée)
###Divers
* Gestion d'une seconde liste de source de roms, entree [directories] rom_usb

# [0.8.07] 2017-09-22 (Version privée)
###SH
* Regénération des deux langues sur "RAFRAICHIR THEMES.sh"

# [0.8.06] 2017-09-18 (Version privée)
###Gamelist.xml
* support des attributs favorite et region au niveau des opérations XML
###SH
* Passage des arguments USERMODE et LANGUAGE aux scripts suivants :
  - CALCULER TOP.sh
  - CORRIGER METADONNEES.sh
  - GENERER MENU MULTI.sh
  - LISTER ROMS SANS IMAGE.sh
  Permet d'activer le niveau de log debug si USERMODE=developpeur sinon info
  
# [0.8.05] 2017-09-03 (Version privée)
###Paramétrage GameListPatch.ini
* correction de la règle pang
 
# [0.8.04] 2017-09-03 (Version alpha)
###Themes
* correction bug si plusieurs retours chariot dans es_settings.cfg
###Gamelist.xml
* support des attributs background, screenshot et logo au niveau des opérations XML
###Generation multi
* correction bug sur exclusion des roms dans règle
* ajout des attributs background, screenshot et logo dans la configuration des règles
* modification du fichier de paramétrage pour les générations
* ajout de 2 règles pour street fighter
###ESSystem
* ajout de l'attribut usermode

# [0.8.03] 2017-07-11 (Version public)
###Themes
* ajout de l'option current pour afficher le theme actif
* ajout de l'option check et check_ko permettant de vérifier si pour chaque système (es_system.cfg), le theme existe

# [0.8.02] 2017-07-09 (Version public)
###Divers
* nouvelle image folder-KO-image.png (dossier rouge style outlaw)
* nouvelle image folder-default-image.png (dossier jaune style outlaw)

# [0.8.01] 2017-07-08 (Version public)
###Divers
* exclusion dans GameListPatch.ini du dossier /home/pi/happi/roms/console/vectrex/overlays
* exclusion dans GameListPatch.ini du dossier /home/pi/happi/roms/divers/pcdos/SC2000/VESA
* exclusion dans GameListPatch.ini du dossier /home/pi/happi/roms/divers/pcdos/SC2000/SOUND
* exclusion dans GameListPatch.ini du dossier /home/pi/happi/roms/divers/pcdos/SC2000/SCENARIO
* correction gamelist pour multi sur giana et xrick (lien image)
* integration des images dossier outlaw pour multi

# [0.8.00] 2017-07-02 (Version privée)
###Themes
* lecture des dossiers présents dans les themes
* modification du paramétrage theme courant dans es_configs.cfg
* creation de la rubrique themes dans le menu config
* génération automatique de la liste des themes disponibles
* menu de refresh de la liste

###Merge 0.2.0
* support des folders

# [0.7.11] 2017-06-18 (Version public)
###Multi
* suppression des anciens sh puis regénération complète : plus de lanceur orphelin (cas des changements de règles)
* ajout de l'analyse des dossiers dans le mode génération

### Corrections BUG
* correction de l'évolution de la 0.7.09 sur les chemins des images

###Divers
* séparation de l'installation entre gamelistpatch et le fichier es_launch.sh
* nouveau kit d'installation revue vs 3.9.0.2
* ajout des règles multi giana et rick


# [0.7.10] 2017-06-18 (Version public)
###Divers
* nouvelles images folder-bestgames-image.png, folder-lastgames-image.png et folder-topgames-image.png de Outlaw
* es_systems.cfg : intégration wonderswam + vectrex vertical et C64 de MisterJam
* es_systems.cfg : intégration pcdos de NordicPower
* es_launch.sh : intégration lancement sh dans dosbox pour intégration doom/quake...
* es_launch.sh : définition d'un script player.sh pour lancer vidéo au lieu appel direct omxplayer (non fourni)
* ajout du theme pcdos + patch du theme atari

# [0.7.09] 2017-06-11 (Version public)
###Divers
* ajout de l'ajout et de la modification d'une plateforme
* ajout de l'activation et de la désactivation d'une plateforme
* ajout du script python plateform pour appel fusion/activation/désactivation plateforme
* ajout d'un nouveau paramètre pour les chemins d'images par défaut

### Corrections BUG
* correction appel quickupdate.py dans es_launch.sh
  -> si le nom de la rom contient un espace, pas d'affichage du nom et pas de sauvegarde info

# [0.7.08] 2017-05-26 (Version public)
###Divers
* ajout du launcher ATARI ST + Slide
* ajout du script checkxml.py pour tester un fichier gamelist.xml, v0.1 => chargement uniquement
* ajout du script mergexml.py pour fusion un fichier gamelist.xml source vers un fichier gamelist.xml destination

### Corrections BUG 
* les noms des fichiers sh issus de la génération multi ne prennaient pas en compte les noms de roms avec des . en dehors de l'extension
* si le dossier d'exclusion n'existe pas, génération d'une exception. contournement <0.7.8 mettre en commentaire

# [0.7.07] 2017-05-07 (Version public)
### Corrections BUG
* correction de l'installeur

# [0.7.06] 2017-05-06 (Version public)
###Divers
* recherche du fichier de configuration GameListPatch.ini sur /home/pi/happi/script/maconfig puis sur dossier courant
  permettant ainsi de l'éditer à travers le partage SAMBA
### Fonctionnalités multi-émulateurs
* critère optionel d'exclusion de roms avec une liste exclusion avec pipe
  ex : mario=name,mario,/home/pi/happi/roms/divers/multi/mario,Mario Lemieux Hockey.zip => exclusion de la rom Mario Lemieux Hockey.zip de la recherche mario
### Lancement des roms comme nouveau point d'entrée emulationStation
* support de dosbox avec des fichiers BAT

# [0.7.05] 2017-04-31 (Version public)
### Fonctionnalités multi-émulateurs
* comparaison sans tenir compte de la casse
### Fonctionnalités sur les options au lancement du script
* ajout du mode updateforce permettant de ne pas tenir compte des optimisations de refresh

# [0.7.04] 2017-04-18 (Version privée)
### Fonctionnalités sur les Roms
* intégration lecture configuration de emulationstation (es_systems.cfg) et extraction command et extension
* utilisation des extensions de chaque plateforme de es_systems.cfg pour référencer les roms
### Fonctionnalités multi-émulateurs
* ajout d'une section [rules] dans GameListPatch.ini pour définir des règles de recherche de roms
  ->règle  BEST    : tous les dossiers des roms BEST de chaque plateforme sont les sources pour le dossier BEST multi-émulateur
  ->règles flipper : tous les genres (xml) contenant pinball ou flipper sont les sources pour le dossier pinball multi-émulateur
  ->règle  outrun  : tous les noms (xml) contenant outrun sont les sources pour le dossier outrun multi-émulateur
* ajout d'une entrée folder_multi pour définir le dossier de lancement multi-émulateurs (/home/pi/happi/divers/multi)
* ajout d'un moteur de recherche des roms
* ajout d'un générateur de fichiers de lancement sh afin de lancer les roms à partir du dossier/sous-dossier multi
* mise à jour du fichier gamelist.xml du dossier multi avec données sources des roms (+image)
### Fonctionnalités sur les options au lancement du script
* ajout d'un argument au lancement sur le mode de fonctionnement : update, verify, top, stats, noimage et generate :
* - update pour lancer les options correct et top
* - correct pour corriger les fichiers gamelist.xml vs dossiers roms
* - top pour calculer les dossiers top et last
* - stats pour le tableau final uniquement
* - noimage pour lister rom sans image
* - generate pour la génération de lanceurs dans le dossier multi
* ajout d'un argument au lancement sur le niveau de log : debug, info ou error

# [0.6.04] 2017-03-31 (Version public)
### Fonctionnalités sur les Roms
* détection des fichiers mal formés et annulation du traitement du dossier, sans écraser celui-ci

# [0.6.03] 2017-03-21 (Version privée)
### Fonctionnalités sur le lancement des emulateurs
* nouveau script es_launch.sh configuré dans es_system.cfg pour remplacer les longues lignes de commande de <path>
* déplacement automatique des roms dans dossier ROMS_KO si l'emulateur retourne une erreur lors de son exec
* gestion des overlays directement en bash au lieu de python (+ rapide)
* inclusion des scripts AmigaArg.sh, AmigaArgcd32.sh au sein de es_launch.sh
* capacité à désactiver quickupdate.py par la variable USE_GAMELIST_PATCH

### Corrections BUG
* Test Game XML sans rom existante, suppression (et recréation des info) au lieu simple recherche de la rom (cas déplacement . vers .\ROMS_KO)

# [0.6.02] 2017-03-11 (Version public)
### Fonctionnalités sur les Roms
* Calcul d'un hash sur la photo du contenu de chaque dossier de rom et enregistrement sur le fichier gamelist.hash
* Exploitation des hash pour décider si besoin de vérifier contenu d'un dossier rom dans les séquences de patch => gain de temps et en io
* Ajout de la gestion du dossier downloaded_images en plus de dossier images
* Ajout du cas downloaded_images/folders 

### Divers
* Suppression des exclusions obsolètes dans ini : MAME  -0.78-JBAM.zip,MAME - Bios Pack.zip
* Suppression des exclusions roms dans ini : pgm.zip, neogeo.zip (pour faire apparaitre image rom)
* Ajout du message "VERIFICATION IMAGES"
* Ajout des options ini hint_use_refresh_tag et hint_use_os_stat
### Corrections BUG
* Correction des statistiques dans le cas des ajouts

# [0.6.01] 2017-02-19 (Version privée)
### Fonctionnalités sur les Roms
* Optimisation gestion TOP/LAST en fonction attribut refresh

### Corrections BUG
* cas bizarre de XML invalide avec MAME, 1ière passage avec <?xml version="1.0" encoding="iso-8859-1" ?> obligatoire

# [0.6.00] 2017-02-18 (Version public)
### Fonctionnalités sur les Roms
* Remplacement de la copie d'une rom par un hardlink (plus rapide, pas de consommation de place)
* Tri sur la recherche des dossiers à analyser
* Création automatique des fichiers gamelist.xml et dossiers images dans les dossiers arcade,console,ordinateurs
* Suppression des noeuds game en doublons
* Modification affichage TOP/LAST dans la liste

### Corrections BUG
* Correction de la gestion des exclusions dans les sous-dossiers
* Correction bug doublon object game XML suite suppression rom dans les dossiers BEST, LAST, TOP, ROMS_KO
* Ajout de ...psp\PPSSPP comme dossier d'exclusion

# [0.5.16] 2017-02-05 (Version public)
### Corrections Bug
* Correction de la gestion du ~ => plus de freeze à la fin du deuxième lancement
* Gestion des caractères dans la description des roms pour le mode console
* Correction documentation du fichier ini dans README.md


# [0.5.15] 2017-01-26 (Version public)
### Fonctionnalités sur les Roms
* Prise en charge de l'attribut hidden par la configuration hidden_name roms/folders

### Corrections Bug
* Correction régression sur gestion des accents sur quickupdate

# [0.5.14] 2017-01-20 (Version public)
* Gain sur la sauvegarde de quickupdate 50s->2s

# [0.5.13] 2017-01-20 (Version public)
### Corrections Bug
* Gestion des roms dont le nom contient des . (ex: rom 1.2.gg)
* Ajout quit explicit sur pygame
* Exclusion des fichiers configuration.backup et Thumbs.db
* Correction problème aléatoire avec les tildes

# [0.5.12] 2017-01-15 (Version public)
### Fonctionnalités sur les Roms
* Changement des messages console sur quickupdate.py

### Corrections Bug
* Affichage du texte en remplacement du log exécution au lieu à la suite sur les touches F2/F3
* Exclusion répertoire BEST dans la recherche des derniers jeux lancés
* Support des caractères accentués dans le fichier gamelist.xml
* Format date de l'attribut lastupdatedate incorrect

# [0.5.11] 2017-01-08 (Version privée)
### Fonctionnalités sur les Roms
* Recherche des images basées sur le nom : nom_rom + '.' + extension image
### Corrections Bug
* Gestion des extensions de rom à 2 caractères (les gg de gamegear)
* Les statistiques du nb roms incluent maintenant les roms ajoutés durant la session d'exec

# [0.5.10] 2017-01-07 (Version public)
### Corrections Bug
* Gestion des accents dans les messages en français
* Gestion des ' dans les messages en français

# [0.5.08] 2016-12-06 (Version public)
### Fonctionnalités Graphique
* Ajout d'une interface style Amiga Workbench 1.3 constituée :
	- d'une zone d'affichage avec deux boutons de défilement texte
  - d'une jauge d'avancement
  - de zones de click complémentaire : fermeture fenetre et défilement vertical
	- d'un message en bas d'écran du dossier en cours de scan
	- touche F1 pour l'aide
	- touche F2 pour lister les jeux sans ROMS
	- touche F3 pour voir les statistiques
	- touche F4 pour revoir log initial
	- touche ESC pour quitter
	- touche Home/End/Up/Down pour le défilement du texte
* Gestion des messages en français et anglais
* Musique
  - Lancement musique si existance d'un fichier GameListPatch.mp3
  - touche F5 pour mettre en pause ou supprimer pause
  - touche F6 pour augmenter le volume
  - touche SHIFT F6 pour diminuer le volume

### Fonctionnalités Statistiques
* Par plateforme : nb roms, nb roms unique, nb sans image, nb dans répertoire ROMS_KO
* Total de l'ensemble des plateformes	
* Nombre total de jeux distinct joués
* Top des jeux joués sur l'ensemble des plateformes
* Derniers jeux joués sur l'ensemble des plateformes

### Refactoring
* Fusion des modules dans GameListTools
* Renommage gamelist.py en GameListXml.py
* Renommage gamelistdir.py en GameListDir.py

### Corrections Bug
* Gestion ~ dans le chemin des images


# [0.4.18] 2016-11-12
### Fonctionnalités sur les dossiers
* Gestion d'un répertoire TOP x où sont présents les rom les plus jouées (automatique)
* Gestion d'un répertoire LAST x où sont présents les dernières roms jouées (automatique)
* Gestion d'un répertoire BEST avec maintient des informations de la localisation originale
* Suppression des noeuds game sans rom (gestion par option)

### Refactoring
* Modification des noms des entrées [folder] dans GameListPatch.ini
* Création du fichier gamelist.py pour toutes les opérations XML/objets sur le fichier gamelist.xml
* Création du fichier gamelistdir.py pour toutes les opérations disque sur les répertoires de rom
* Création du fichier mylog.py pour le logging sur l'ensemble des modules
* Création du fichier myconfig.py pour la configuration
* Création du fichier myexcept.py pour les exceptions
* Création du fichier quickupdate.py pour mise à jour attribut d'un jeu
* Passage en sous-fonction pour alléger le fonction main()
* Test des répertoires d'exclusion

### Corrections Bug
* si l'entrée exclusion_directories vide, le programme ne fonctionne pas
=======
>>>>>>> a1d49e40e71329102d13dd5ebc806db0495d8b3d


# [0.4.11] 2016-10-16

### Fonctionnalités sur les dossiers
* Ajout d'une image par défaut si aucune image trouvée. Option [folder] default_image=
* Ajout d'une image dédiée pour les dossiers stockant des ROMs KO. Option [folder] ko_image=
* Suppression des nœuds xml folder si le dossier n'existe plus
* Gestion des images dans le répertoire images de la racine ou dans les sous-répertoires
* Ajout exclusion de dossiers lors du scan de dossiers, Option [directories] exclusion_directories
* Mode image permettant d'ajouter ou de supprimer l'image par défaut. A utiliser par exemple pour remplacer une image par défaut par une autre
### Fonctionnalités sur les Roms
* Ajout d'une image par défaut si aucune image trouvée. Option [game] default_image=
* Gestion des images dans le répertoire images de la racine ou dans les sous-répertoires
* Exclusion de roms lors du scan par des extensions et des noms spécifiques, Option [game] exclusion_extension/exclusion_name
* Si le nœud xml game ne contient plus un lien vers un fichier rom, recherche de celui-ci à travers le dossier racine de la console émulée ou ses sous-répertoire. Très utile par exemple lors du déplacement d'un jeu dans le répertoire des ROMs KO.
* Mode image permettant d'ajouter ou de supprimer l'image par défaut. A utiliser par exemple pour remplacer une image par défaut par une autre
### Autres fonctionnalités
* Si le fichier Gamelist.xml est vide (ex: commande touch), création du nœud xml principal
* Deux sauvegardes de fichiers Gamelist.xml : gamelist.origin.xml pour la 1ière exécution et gamelist.sav.xml à chaque exécution. Option disponible dans le fichier de configuration [save] origin/backup
### Corrections Bug
* Conflit python avec les classes avec une propriété id (mot clé réservé)


# [0.3.4] 2016-10-02
### Fonctionnalités sur les Roms
* Recherche des images de rom selon le pattern "./images/" + nom_rom + "-images." + extension images et affectation au jeu si trouvé.
### Fonctionnalités sur les dossiers
* Les dossiers sont maintenant gérés dans des nœuds folder et non game en XML 
### Autres fonctionnalités
* Ajout d'un logger, voir le fichier GameListPatch.log
* Ajout d'un attribut source et last_change_date sur le nœud gamelist XML
### Corrections Bug
* Ajout des éléments xml ***desc, playcount*** et ***lastplayed*** du nœud game xml

#[0.2.5] 2016-09-25
### Fonctionnalités sur les dossiers
* Ajout des nœuds folder à partir du scan des dossiers
### Autres fonctionnalités
* Ajout d'un fichier de configuration


----------
Editeur MD : https://stackedit.io/editor
