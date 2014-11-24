Title: Sed Basics
Date: 2013-08-18 22:57
Author: Wxcafe
Category: Tutoriel
Slug: sed-basics

`sed` est un outil Unix très largement utilisé et très pratique pour manipuler
le texte (ce qui se montre relativement indispensable dans un environnement
Unix, puisque ce système est assez porté sur le texte). Cependant, il assez peu
connu en détail, et la plupart du temps une seule fonction est utilisée : le
remplacement de texte.  
Or `sed` a bien plus de possibilités que ça, comme nous allons le voir.

Tout d'abord, rappelons les bases : `sed` est un programme Unix de base, mais
aussi un langage de manipulation de texte dérivé de `ed`, l'éditeur original.
`ed` est un éditeur de ligne, conçu a l'époque ou les ordinateurs n'étaient pas
personnels et étaient utilisés avec des [téléscripteurs](http://fr.wikipedia.org/wiki/telescripteur), c'est a dire des
machines dépourvues d'écrans et ne permettant donc pas l'utilisation d'éditeurs
dits "visuels", tels que vim, emacs, et globalement tous les éditeurs ayant un
curseur et affichant plusieurs lignes. `sed` est donc une évolution de `ed`, le
s signifiant stream, `sed` est un éditeur de flux, prenant donc avantage du
concept Unixien de flux de données (voir [Flux standards](http://fr.wikipedia.org/wiki/Flux_standard)) pour éditer plus d'une ligne a la fois.
En pratique, `sed` est principalement utilisé sur des fichiers.

`sed` a quelques options pratique, notamment `-s` qui permet d'empêcher
l'affichage systématique des lignes traitées, ou bien `-i` (pour GNU sed) qui
permet de rediriger l'output dans le fichier d'input. Cela dit, l'intérêt unique
du programme est son langage de manipulation de texte.

`ed`, et donc `sed`, utilise un langage basé sur les séparations (en général des
/). Ainsi, la commande de base dans `sed` est 

	/[regex]/

qui permet de ne sélectionner que les lignes qui matchent \[regex\] (et donc de 
n'exécuter les commandes qui suivent que sur ces lignes.)  

<br/>
La commande `sed` la plus utilisée est bien entendu le **s**, qui s'utilise de
la façon suivante : 

	s/[old text]/[new text]/[options]

qui se propose donc de remplacer (substitute) \[old text\] (qui peut être une
regex) par \[new text\] (qui doit être un texte fixe, avec quelques
exceptions), en appliquant \[options\], la plus connue des options étant `g`, 
qui permet d'appliquer la commande affectée a toutes les occurrences du texte
matché sur la/les lignes concernée-s.  
Les exceptions a la "fixité" de \[new text\] sont particulièrement
intéressantes. En effet, `sed` utilise un langage de regex plutôt standard,
excepté le fait qu'il permet jusqu'à 9 "holding spaces", qui sont délimités par
\\( et \\), et qui sont représentées dans le texte de remplacement par \\1 à
\\9.

Par exemple, la commande 

	sed 's/\(hello world\) world/\1/'

sur le texte "hello world world" renverrait comme résultat

	hello world

De la même façon, le symbole `&` dans le texte de remplacement représente le
texte original. Ainsi, la commande 

	sed 's/hello world/& world/'

sur le texte "hello world" renverrait comme résultat

	hello world world

<br/>

Une autre commande utile est **p**, qui sert a afficher le texte présent dans
l'espace courant :

	/[regex]/p

`sed` stocke en effet la ligne sur laquelle il travaille dans un espace mémoire
dédié, que j'appelle l'espace courant (pattern space en anglais). La commande
`p` affiche (print) ce qui ce trouve dans cet espace. La /\[regex\]/ réduit
le pattern space de façon a ce qu'il ne contienne que les lignes matchant, et le 
**p** affiche donc ce dernier.


Un autre exemple de commande sont **c**, **i** et **a**, qui s'utilisent ainsi :

	c \
	[text]

De la même façon, pour le i : 

	i \
	[text]

Et de même pour a. 

Ces trois commandes s'utilisent de la même façon pour la bonne raison qu'elles
sont très proches. **i** sert a insérer du texte *avant* le pattern space. **a**
sert a insérer du texte *après* le pattern space, et enfin **c** sert a
remplacer *tout* le pattern space. Les trois utilisent \[text\] comme
remplacement ou insert.
Attention, les insertions se font sur la ligne précédant ou suivant le pattern
space, et non sur la ligne en question.

Enfin, dernière commande ne fonctionnant que ligne par ligne, **d** :
	/[regex]/d
**d** (delete) supprime les contenus du pattern space.

`sed` est un outil puissant, mais complexe. Dans un prochain article, je
parlerai des commandes multilignes et des labels.

