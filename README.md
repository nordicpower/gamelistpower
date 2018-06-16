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

 1. A partir de l'adresse du site https://github.com/nordicpower/gamelistpower, choisir download puis Download ZIP
 2. Ouvrir le partage \\recalbox\share
 3. Créer un dossier \\recalbox\share\nordicpower
 4. Créer un dossier \\recalbox\share\nordicpower\gamelistpower
 5. Dézipper le fichier gamelistpower-master.zip \\recalbox\share\nordicpower\gamelistpower
 6. Ouvrir une session ssh
`mount -o remount,rw /`
`cd /recalbox/share/nordicpower`
`cp -r gamelistpower /recalbox/scripts`
`cd /recalbox/scripts/gamelistpower`
`chmod 777 *.sh`
`./install.sh`
 7. Une recherche sera lancée, la nouvelle plateforme sera prise en compte après un reboot de recalbox

## Comment configurer ?

Dans le fichier **rules_gensh.xml**, le fichier contient des règles de recherche permettant d'alimenter la plateforme collections, un exemple :
`<rule>`
	`<name>mario</name>`
	`<searchAttribute>name</searchAttribute>`
	`<searchValue>mario</searchValue>`
	`<destination>/recalbox/share/roms/collections/mario</destination>`	`<preserveFavorite>false</preserveFavorite>`
`</rule>`
Cette règle permettra de rechercher tous les jeux dont le nom contient mario et de copier le résultat dans le dossier /recalbox/share/roms/collections/mario. L'attribut favori ne sera pas conservé.

## Configuration par défaut
La configuration par défaut permet de rechercher et de classer des roms sur les thématiques suivantes : Giana Sisters, Magic Drop, Mario, Metal Slug, Outrun, Pang, Pinball, Puyo Puto, Rick Dangerous, Street Fighter, Tetris. Les images des dossiers sont fournies à l'installation. 

## Configuration avancée

### Exclusion de dossiers ou de roms
Il est possible d'exclure au sein d'une règle des roms ou des dossiers, il suffit d'indiquer le nom ou le chemin concerné
`<exclusions>`
    	`<exclusion>Mario Lemieux Hockey.zip</exclusion>`
    	`<exclusion>/recalbox/share/roms/mario</exclusion>`
`</exclusions>`

### Modifier le titre des roms
`<options>`
		`<titleformat>%%NAME%% (%%PLATEFORM%%)</titleformat>`
		`<path>/recalbox/share/roms/collections</path>`
	`</options>`
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
