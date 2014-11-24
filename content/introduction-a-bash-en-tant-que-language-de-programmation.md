Title: Introduction a bash en tant que language de programmation.
Date: 2012-09-08 18:15
Author: Wxcafe
Category: Programmation 
Slug: introduction-a-bash-en-tant-que-language-de-programmation

L’interpréteur de commandes bash (Bourne Again SHell)
est possiblement le shell le plus connu, notamment grâce a son
intégration en tant que shell par défaut dans les distributions Linux
les plus répandues (Debian - Ubuntu, Fedora, OpenSUSE, Mandriva -
Mageia, etc...).

Cependant, il n'est souvent connu qu'en tant qu’interpréteur de
commande. Alors qu'en réalité, le bash est un langage de programmation
(presque) complet! Ainsi, il intègre les structures de contrôle
habituelles ( pour mémoire, les structures de contrôle comprennent les
conditions (les ifs), les boucles (les while), et les choix (les case),
entre autres.), et est donc ce que l'on pourrait appeler un langage de
script, interprété, de la même façon que python, a la difference près
qu'il contient un prompt (un système d'entrée de commande interactif)
bien plus complet et développé que python.  

Cependant, les programmes en bash ne sont executables que dans un
environnement de type UNIX, et donc pas sous Windows (cygwin
(cygwin.com) propose ceci dit un système permettant d'utiliser bash sous
windows. Il faut malgré tout convenir que cet environnement est bien
plus compliqué a manipuler, et globalement ne permet pas d'acceder a des
portages de qualité satisfaisante.)

Ainsi, il est possible de créer des fichiers .sh, contenant des
instructions bash mises a la suite (de la même façon qu'un script BATCH
Windows .bat), et faisant appel autant aux commandes internes de bash,
aussi bien que les commandes externes mises en place par les programmes
installés sur le système, exactement comme dans une invite de commande.
Ainsi, pour appeller firefox, la commande 'firefox' lancera le petit
panda roux directement dans la boite magique, tandis qu'un if
[condition] suivi d'un then (quelque chose) lancera le fameux quelque
chose suscité si la condition est vérifiée. Un peu comme en C, quoi.  

De cette façon, et avec quelques informations et connaissances, il est
facile de comprendre le fonctionnement de la programmation en bash.
Quelques exemples commentés:

	#!/bin/bash 
	# La ligne du dessus est très importante, c'est elle qui dit a bash quel doit être 
	# l'interpreteur des commandes écrites dans ce script. Ici, on dit a bash d'interpréter 
	# lui même les commandes comprises dans ce script. On aurait tout de fois pu lui faire 
	# executer du python, par exemple, en mettant #!/usr/bin/python a la place.
	echo "this is a test of bash as a simple script manager" # echo est une commande d'affichage de message.
	echo "what's your name, user?" 
	read your_name # la commande read permet de demander a l'utilisateur de donner une 
	# information, stockée dans la variable en paramètre. 
	echo $your_name "is your name" # echo permet aussi d'afficher la valeur de variables. 
	# Ici, on renvoie la variable remplie précédemment, suivie d'un message. 
	exit # cet appel a exit n'est pas obligatoire, mais donne un aspect plus 
	# propre au code. Il ne quittera pas la session de terminal, cependant.

Voila. Ce script bash ne sert pas a grand chose, mais il a le mérite
d'être clair quand aux capacités et a la simplicité du bash en tant que
language de programmation. Alors en effet, nous n'avons ici absolument
pas utilisé les capacités de bash en lui même, et n'avons fait que le
renvoyer a des programmes externes (sauf read, il est vrai). Voyons
maintenant la syntaxe de bash quand il s'agit d'utiliser les structures
de contrôle:

    #!/bin/bash 
    echo "welcome to this second bash program. would you please kindly enter the name of the machine you're running this on?" 
    read host_name 
    if [ $host_name == $HOSTNAME ] ## voici la syntaxe du if. Attention a bien penser a mettre les espaces avant la première variable, et après la seconde. La variable $HOSTNAME ici utilisée est une variable présente par défaut sur le système. 
    then echo "you told the truth!" 
    fi ## le fi est la commande fermant le if, tout comme le EndIf en basic. C'est un peu vieillot, mais important en bash. 
    if [ $host_name != $HOSTNAME ] ## l'opérateur != est l'inverse de ==, il vérifie donc si les deux variables ne sont pas les mêmes. 
    then echo "you lied!" 
    fi 
    exit

Voila un petit programme permettant d'apprendre la syntaxe du if en
bash. comme vous pouvez le voir, le language est plutôt lite, et la
structure if n'est pas très difficile a prendre en main.

Passons maintenant au while:

    #!/bin/bash
    echo "what is your name?"
    read name
    while [ 1 < 10 ]    ## le while se présente sous la forme while (truc); do (machin); done. Les [] sont en fait des programmes differents, inclus dans bash.
    do echo "i love" $name
    done
    exit

Ce petit programme permet d'observer les bases de while (qui est la
boucle de base en bash).

Le troisième opérateur de bash est case. Voyons:

    #!/bin/bash
    echo "please enter a number between one and five"
    read number
    case $number in 
    1)
    echo "the choosen number was one"
    ;;
    2)
    echo "the choosen number was two"
    ;;
    3)
    echo "the choosen number was three"
    ;;
    4)
    echo "the choosen number was four"
    ;;
    5)
    echo "the choosen number was five"
    ;;
    *)
    echo "this number is not correct"
    ;; 
    esac
    exit

case est un opérateur plus complexe a utiliser a bon escient, et sert a
faire des ifs multiples sans avoir a taper des dizaines de lignes de
code.  
(pour ceux qui auraient du mal avec cet opérateur, il faut comprendre
que le code vérifie chacune des conditions : le 1) est validé si la
valeur de \$number est 1, le 2) est validé si cette valeur est 2, etc..
le \*) désigne toutes les valeurs, et est donc validé si aucune autre
valeur n'a précédemment acceptée.

Quelques notions manquent ici:  
- les nombres aléatoires sont générés par un appel a la variable
\$RANDOM, qui renvoie un nombre aléatoire entre 0 et 32767 (un entier a
16 bits donc). il est possible de faire des invocations a des nombres
aléatoires plus grands, mais les méthodes permettant de faire cela sont
plus complexes, et je ne les aborderai donc pas ici.  
- comme vous avez pu le constater, les variables sont désignées en tant
que telles par l'utilisation d'un symbole \$ au début de leur nom.
Ainsi, echo number renverra "number", tandis que echo \$number renverra
le résultat de la variable \$number.  
être utilisées dans un programme bash.  
- comme vous avez pu le constater, les commandes doivent tenir en
théorie en une ligne. Cependant, le caractère \\ permet de retourner a
la ligne en faisant considérer a bash qu'il s'agit de la même ligne.

Globalement, il faut admettre que bash n'a pas vocation a être un
langage de programmation extrêmement développé. Sans framework
graphique, avec peu de manières d'utiliser de grandes variables, ou
encore une gestion de la mémoire risible, bash n'a rien d'un langage de
développement professionnel.  
Cependant, le simple fait qu'il soit considéré comme un langage de
programmation a part entière font de lui un langage de script d'une
puissance incontestable, et sa simplicité et sa grande popularité font
de lui un langage de choix pour apprendre la programmation simplement et
sans trop se prendre la tête.

J'espère que cet article aura été utile a certain-e-s, et je vous
souhaite bonne chance dans votre découverte de la programmation (n'allez
pas voir ceux qui font de l'orienté objet, c'est des méchants :3)
