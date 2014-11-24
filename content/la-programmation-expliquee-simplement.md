Title: La programmation expliquée simplement
Date: 2012-08-27 00:22
Author: Wxcafe
Category: Teaching 
Slug: la-programmation-expliquee-simplement

Salut!  
Tout d'abord, je tiens a m'excuser de ne pas avoir eu le temps d'écrire
récement, mais j'ai eu la chance d'avoir un PC a monter, donc j'ai passé
pas mal de temps assez occupé.  

Enfin, après un certain temps a farfouiller au millieu des connecteurs
SATA et a apprendre que, oui, l'alimentation sert aussi pour les disques
durs, je suis de retour pour un court article.  
Du coup, je m'étais dit que j'allais reprendre sur le thème de
l'informatique expliquée au grand public, en tentant d'aller un peu plus
loin que la dernière fois sur le thème de la programmation  
Ce qu'il faut comprendre, c'est la facon dont fonctionne un ordinateur.
Si a peu près tout le monde sait que "les ordinateurs, ils ne
comprennent que les 1 et les 0!", peu de gens savent comment cela
fonctionne en détail.  

Si vous êtes sur ce blog, il y a pas mal de chance que vous ayez déjà
des notions de base en informatique. Ainsi, vous savez surement que les
ordinateurs fonctionnent avec des programmes, qui sont composés de
code.  
Ainsi, il faut comprendre que le code (source) est "compilé" en un
fichier "binaire". Un fichier binaire est un fichier comprenant les
instructions telles qu’exécutées par le processeur, et donc absolument
illisible pour un humain.  

La compilation est le processus qui transforme le code source en
binaire executable. Les binaires ont, sous Windows, l'extension .exe,
tandis que sous les systèmes UNIX-like, ils n'ont pas d'extension
particulière.  
Ceci étant dit, il faut comprendre que certains langages sont plus
proches que d'autres du langage processeur, les langages les plus
proches sont dits de "bas niveau". Les langages les plus éloignés sont
donc dits de haut niveau.  

Par exemple, l'assembleur est l'un des languages de plus bas niveau,
tandis que python par exemple est un langage de plus haut niveau. Les
langages de haut niveau sont souvent bien plus simples a comprendre et a
apprendre que les langages de bas niveau  

Ainsi, en C, un langage de niveau relativement bas, pour afficher
"hello world" sur l'écran, le code nécessaire est :

    #include 
    void main() {
    printf("hello world");
    return 0;
    }

le même programme en python s'écrit :

    print "hello world"

et n'a pas besoin d'être compilé , puisqu'il peut être intepreté
directement.  

Python utilise en effet un système similaire a Java en ayant un
interpréteur dit "runtime" ou "temps réel", qui interprète le programme
sans le compiler. Java utilise un système légèrement différent, puisque
le code a besoin d'être compilé, mais est interpreté par un interpréteur
et non par le processeur.  

Cette méthode permet le fameux "code once, run everywhere", ce qui
signifie que le même code est exécutable sur quasiment tous les systèmes
d'exploitation (en fait, tous ceux sur lesquels l’interpréteur est
disponible.)

Voila, je vous laisse sur le fonctionnement de Java et de Python, et je
vais me coucher.  
A bientôt!
