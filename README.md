EMULATIONSTATION GAMELISTPOWER
==============================
# Readme / lisez-moi
***Par Nordicpower***
*amiga15@outlook.fr / https://twitter.com/nordicpower*
***Juin 2018***

Gamelistpower est une série de scripts en python afin d'améliorer Recalbox sur Pi3.

La version 0.9 de Gamelistpower installe une nouvelle plateforme dénommée **collections** dans RecalBox *(avec le thème favori)*. Celle-ci permet de lancer des jeux sur plusieurs plateformes différentes au sein d'une seule et de les regrouper par dossier, Tout-ceci sans recopier les roms, préservant ainsi l'espace disponible sur votre SD ou HDD!!

Ces dossiers de jeux multi-plateformes sont issus par des recherche des métadonnées des roms (fichiers **gamelist.xml**), chaque rom trouvé possède alors un script de lancement (sh) et ces métadonnées sont recopiées dans le gamelist de la plateforme collections

Un guide des 1er pas est fourni dans le Wiki !(https://github.com/nordicpower/gamelistpower/wiki)

##  Copies d'écran du résultat
Le dossier Outrun
![Alt text](/screenshots/Outrun-folder.png?raw=true "Outrun-folder")
![Alt text](/screenshots/Outrun-inside.png?raw=true "Outrun-inside")

Le dossier Street-Fighter
![Alt text](/screenshots/StreetFighter-folder.png?raw=true "StreetFighter-folder")
![Alt text](/screenshots/StreetFighter-inside.png?raw=true "StreetFighter-inside")

##  Comment installer ?

 1. Ouvrir une session ssh<br />
`mount -o remount,rw /`<br />
`cd /recalbox/share`<br />
`wget https://github.com/nordicpower/gamelistpower/archive/master.tar.gz`<br />
`tar xzvf master.tar.gz`<br />
`cp -r /recalbox/share/gamelistpower-master /recalbox/scripts/gamelistpower`<br />
`cd /recalbox/scripts/gamelistpower`<br />
`chmod 777 *.sh`<br />
`./install.sh`<br />
2. Une recherche sera lancée, la nouvelle plateforme sera prise en compte après un reboot de recalbox

## Comment configurer ?

Dans le fichier **rules_gensh.xml** (dans /recalbox/scripts/gamelistpower), le fichier contient des règles de recherche permettant d'alimenter la plateforme collections, un exemple :
<br />`<rule>`<br />
	`<name>mario</name>`<br />
	`<searchAttribute>name</searchAttribute>`<br />
	`<searchValue>mario</searchValue>`<br />
	`<destination>/recalbox/share/roms/collections/mario</destination>`<br />
	`<preserveFavorite>false</preserveFavorite>`<br />
`</rule>`<br />

Cette règle permettra de rechercher tous les jeux dont le nom contient mario et de copier le résultat dans le dossier /recalbox/share/roms/collections/mario. L'attribut favori ne sera pas conservé.

## Configuration par défaut
La configuration par défaut permet de rechercher et de classer des roms sur les thématiques suivantes : Giana Sisters, Magic Drop, Mario, Metal Slug, Outrun, Pang, Pinball, Puyo Puto, Rick Dangerous, Street Fighter, Tetris. Les images des dossiers sont fournies à l'installation. 

## Configuration avancée

### Exclusion de dossiers ou de roms
Il est possible d'exclure au sein d'une règle des roms ou des dossiers, il suffit d'indiquer le nom ou le chemin concerné
`<exclusions>`<br />
    	`<exclusion>Mario Lemieux Hockey.zip</exclusion>`<br />
    	`<exclusion>/recalbox/share/roms/mario</exclusion>`<br />
`</exclusions>`<br />

### Modifier le titre des roms
`<options>`<br />
		`<titleformat>%%NAME%% (%%PLATEFORM%%)</titleformat>`<br />
		`<path>/recalbox/share/roms/collections</path>`<br />
	`</options>`<br />
La balise **titleformat** permet de personnaliser le titre de la rom dans la plateforme collection. La configuration par défaut utilise le nom de la rom et en parenthèse le nom de la plateforme source. Les variables disponibles sont %%NAME%% (la balise name), %%PLATEFORM%% (le nom de la plateforme) et %%REGION%% (la balise region). Il est possible d'avoir le résultat en majuscule ou minuscule par l'utilisation de la variable en majuscule ou minuscule (%%NAME ou %%name%%)

### Image des dossiers
Les images de dossiers doivent être stockées dans le dossier /recalbox/share/roms/collections/images. Le script recherche une image du même nom que le dossier de destination de la règle (avec une extension png ou jpg) et créer l'entrée nécessaire. 

## Comment rafraîchir la plateforme ?
Deux méthodes sont disponibles :
 - Directement à travers emulationstation, une entrée "Z-Refresh" permet de lancer la mise à jour et de relancer Recalbox une fois terminée
- Via la commande SSH :
*cd /recalbox/share/scripts/gamelistpower*
*python gamelistpower.py generate_sh info*
Il sera nécessaire de relancer RecalBox pour prendre en compte les nouvelles roms identifiées.

---------------------------------------------
Mon éditeur MD en ligne : https://stackedit.io/app#
