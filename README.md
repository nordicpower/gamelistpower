EMULATIONSTATION GAMELISTPOWER
==============================
# Readme / lisez-moi
***Par Nordicpower***
*amiga15@outlook.fr / https://twitter.com/nordicpower*
***Juin 2018***

Gamelistpower est une série de scripts en python afin d'améliorer Recalbox.

La version 0.9 de Gamelistpower installe une nouvelle plateforme dénommée **collections** dans RecalBox *(avec le thème favori)* . Celle-ci permet de lancer des jeux sur plusieurs plateformes différentes au sein d'une seule et de les regrouper par dossier.

Ces dossiers de jeux multi-plateformes sont alimentés par une recherche de vos roms à travers les fichiers **gamelist.xml** et d'alimenter cette nouvelle plateforme collections.

##  Comment installer ?
Procédure testé sous Windows10
 1. A partir de l'adresse du site https://github.com/nordicpower/gamelistpower, choisir download puis Download ZIP
 2. Ouvrir le partage \\recalbox\share
 3. Créer un dossier \\recalbox\share\nordicpower
 4. Copier le fichier gamelistpower-master.zip \\recalbox\share\nordicpower
 5. Bouton droit sur le fichier gamelistpower-master.zip, Menu extraire tout et Bouton OK
 6. 
 7. Ouvrir une session ssh<br />
`mount -o remount,rw /`<br />
`cd /recalbox/share/nordicpower/gamelistpower-master`<br />
`cp -r gamelistpower-master /recalbox/scripts/gamelistpower`<br />
`cd /recalbox/scripts/gamelistpower`<br />
`chmod 777 *.sh`<br />
`./install.sh`<br />
 8. Une recherche sera lancée, la nouvelle plateforme sera prise en compte après un reboot de recalbox

## Comment configurer ?

Dans le fichier **rules_gensh.xml**, le fichier contient des règles de recherche permettant d'alimenter la plateforme collections, un exemple :
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
Editeur MD : https://stackedit.io/app#
