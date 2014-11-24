Title: Pourquoi je vais quitter linux pour passer a FreeBSD.
Date: 2013-02-04 17:41
Author: Wxcafe
Category: Ranting
Slug: pourquoi-je-vais-quitter-linux-pour-passer-a-freebsd

*This is subject to debate, and as most of the actors in this field are
not French-speaker, there is an English version of this text [here][]*

Bon, voila. J'ai passé le cap. Je suis sous GNU/Linux depuis un certain
temps, maintenant, et depuis un certain temps je remarque des
changements malvenus. Bien entendu, au début, je n'avais pas les
connaissances nécessaires pour comprendre ne serait-ce que ces
modifications existaient. Et puis certaines sont arrivées avant que je
n'ai même idée que quelque chose dans mon système d'exploitation avait
cette fonction la. Par exemple, udev, ou policykit/consolekit/. A
l'époque, je n'avais aucune idée de la façon dont les disques étaient
montés sur mon système. Le premier système non-Windows que j'ai utilisé
fut Ubuntu 9.10 Karmic Koala, et il était encore trop tôt pour que je
cherche a démonter le système pour comprendre comment il fonctionnait en
profondeur. Cependant, avec le temps, les connaissances s'accumulant et
mon niveau de compréhension du système s'améliorant, j'ai commencé a
remarquer que certain bouts de l'OS ne collaient pas exactement avec les
autres. Bien sur, je ne saurais dire si cette réalisation s'est faite a
cause de la recrudescence de ces bouts d'OS, ou bien juste a cause de ma
compréhension plus poussée. Toujours est-il que ces petits bouts d'OS ne
s’adaptant pas au reste du système se faisaient de plus en plus visible.
Et puis, un jour, j'en ai eu marre de voir unity sur ma machine, et j'ai
choisi de passer a Archlinux. C'était avant le passage a systemd. Ce
système me convenait bien. Si je n'installais pas Gnome, ce que je ne
comptais pas faire, il ne me forçait pas a installer un *kit
quelconque, ni dbus. Oui, udev était toujours la, mais c'était le moins
envahissant de ceux la.

Mais Archlinux est passé a systemd. Attention hein, je ne critique ici
ni systemd, ni udev, ni même les *kit, et surtout pas Archlinux. Les
premiers sont probablement très efficaces dans leur domaine, et le
second n'a pas **vraiment** eu le choix, rapport a la philosophie de la
distribution d'avoir au plus vite les dernières versions de tout.
Cependant, systemd, tout comme udev et les *kits (bien que ce ne soient
pas les seuls a faire ça...) ont un problème très précis, qui n'importe
pas a tout le monde, mais qui est très gênant pour ceux a qui il
importe, et ce problème est que ces systèmes ne respectent absolument
pas la philosophie UNIX. La philosophie UNIX, pour rappel, se résume en
ces 9 principes :

1.  Ce qui est petit est beau
2.  Faites en sorte que chaque programme fasse une chose, bien.
3.  Faites un prototype aussi vite que possible
4.  Choisissez la portabilité plutôt que l'efficacité
5.  Stockez les données dans des fichiers textes.
6.  Utilisez ce qui existe déjà a votre avantage. [**1**]
7.  Utilisez des scripts shells pour faciliter la portabilité et la
    réutilisation.
8.  Évitez les UI qui "capturent" l'utilisateur.
9.  Faites de chaque programme un filtre.

Alors bien entendu, un système d'exploitation est fait pour évoluer, et
on pourrait penser qu'UNIX a fait son temps. Cependant, ce n'est pas
exactement la façon dont l'informatique fonctionne. Effectivement, les
standards, les systèmes d'exploitation, les logiciels, tout doit évoluer
- ou mourir - et UNIX ne fait pas exception a la règle. Mais ce n'est
pas d'UNIX que nous parlons ici. C'est de la *philosophie* UNIX. Et
celle-ci n'a pas fait son temps, **elle a fait ses preuves.** La
philosophie UNIX, en plus d'être efficace sur le papier, a aussi 44 ans
de tests derrière elle, et fonctionne aussi bien qu'au premier jour.  
La philosophie UNIX est aussi et surtout une garantie d'utilisabilité
et de simplicité pour les administrateurs systèmes, pour les
développeurs, bref pour tous ceux qui font de l'informatique
*sérieusement* (je ne dis pas que les autres métiers de l'informatique
ne sont pas sérieux, je prend juste ceux-ci comme exemples parce que ce
sont ceux qui sont les plus proches du système).

Tous OS se doit d'avoir un système standardisé pour faire communiquer
les programmes entre eux. UNIX a un système de pipes, des sortes de
fichiers spéciaux permettant d'échanger des informations. C'est
efficace, ça respecte le "tout est fichier", c'est standard, c'est
simple a comprendre, bref, ça fonctionne parfaitement. Dbus vient
remplacer ça, avec une interface qui n'est explicitement pas faite pour
être utilisée a la ligne de commande mais a l'aide d'APIs, et un
programme monolithique qui effectue sa tache d'une façon complètement
obscure pour l'utilisateur. Alors bien sur, il l'effectue d'une façon
efficace, cette tache. Oui, ça va plus vite qu'avant. Oui, c'est plus
"rangé", ça fait moins "fouillis". Mais c'est moins efficace. C'est
*beaucoup* moins utilisable pour l'utilisateur final. C'est
horriblement chiant pour les sysadmins, parce qu'ils ne peuvent plus
lire facilement les échanges entre programmes. C'est peu pratique, en
fin de compte. Et ça ne respecte pas du tout la philosophie UNIX.  
Systemd prend le même parti de créer une interface unifiée, accessible
via des appels a des APIs uniquement, complètement obscure, extrêmement
abstraite, bien entendu monolithique, et très peu ouverte a la
modification par l'utilisateur final. Alors oui, il parait que ça
augmente la vitesse de boot. Eh bien, au risque d'en choquer quelques
uns, je préfère avoir un système qui boote *légèrement* plus lentement
et que je puisse modifier facilement, et qui soit ouvert, compréhensible
et distribué. C'est presque comme si les projets freedesktop.org avaient
pour but de remplacer la base UNIX de linux en créant un système
concurrent, bâtard, bâti sur le kernel Linux mais n'employant plus les
systèmes basiques d'UNIX.

Le problème est qu'il est facilement visible que la direction prise par
la communauté Linux n'est pas celle du retour sur les systèmes UNIX ni
celle du développement de solutions respectant la philosophie UNIX, mais
remises au gout du jour (?), mais est bien d'accepter et de pousser les
changements apportés par les projets freedesktop.org directement dans le
cœur du système lui même. Ainsi, Fedora (très près de Red Hat, dont font
partie de nombreux développeurs de ces projets), a déjà adopté tous ces
changements (archlinux aussi, mais pour d'autres raisons...), et on peut
compter sur le fait que les autres distributions l'adopteront un jour ou
l'autre.

Bon, maintenant que nous avons, si ce n'est démontré la nocivité de ces
systèmes, tout du moins exprimé les raisons qui font qu'ils me
déplaisent, on pourrait penser qu'il suffit de passer a une distribution
n'incluant pas systemd, voire a une distribution n'incluant pas du tout
de contenus freedesktop.org, et de vivre avec le fait de ne pas être sur
archlinux. Cependant, avec un peu de réflexion, on voit que si des
distributions comme archlinux et Fedora ont adopté systemd (et
qu'OpenSUSE est en train de l’intégrer), il est probable que cela
devienne un standard au fil des années, et que seuls survivent systemd
et upstart, le gestionnaire de démarrage d'ubuntu, qui ne changera
probablement pas (je les vois mal revenir en arrière sur ce point.)
Toujours est-il que l'init héritée du System V semble condamnée a mourir
sous Linux. Il pourrait être judicieux de passer sous debian squeeze,
qui ne recevra probablement jamais la mise a jour, ou a wheezy, qui ne
la recevra probablement que dans 2/3 ans. Cependant, cette période est
toujours trop courte, et met sur mon système d'exploitation une date
d'expiration, chose qui ne me plait que moyennement. Non, la solution
est de passer sous un système autre, qui ait son propre système d'init
(ou qui ne risque pas de passer sous systemd). Dans ce cas, deux options
principales s'ouvrent a moi: OpenSolaris et *BSD. Minix n'est pas
vraiment un choix, vu le peu de programmes qu'il permet de faire
fonctionner et le fait qu'il ne soit disponible que sur i386, ce qui
n'est pas vraiment avantageux au vu de mon système en x86\_64. Haiku
n'est pas un choix non plus, puisque le but est de rester dans une
optique UNIX.

OpenSolaris est un système d'exploitation tout a fait valable. Je n'ai
en théorie aucun problème sur cet OS, sauf que certains choix de design
ne correspondent pas du tout a l'idée que j'ai d'un OS. En effet,
OpenSolaris ressemble assez a Debian dans sa vision du fonctionnement de
ses outils, avec des paquets modifiés pour les rendre plus simples a
utiliser (fichiers de configuration fournis par défaut, par exemple, et
autres patchs "release-only"), et une tendance a faire des scripts et
des outils installés par défaut pour tout et n'importe quoi. Bref, cela
n'est pas le sujet. Il convient aussi de voir qu'avec la récente
acquisition de Sun par Oracle, il est possible que le projet OpenSolaris
n'ait pas de très beaux jours devant lui (la [page d’accueil][] du
projet affiche d'ailleurs un ÉNORME logo Oracle, du meilleur gout.)

Il reste donc *BSD. Pourquoi choisir FreeBSD plutôt qu'OpenBSD, NetBSD
ou DragonFlyBSD (pour ne citer que les plus connus) ? Et bien c'est
simple : pour aucune raison particulière. OpenBSD et NetBSD ont pour
réputation d'être orientées sécurité, et d'après ce que j'ai pu en voir
DFBSD ressemble aussi au système de l'assistance a l'user a outrance
décris plus haut. Mais la vérité est que je n'ai pas fait suffisamment
de recherches et que FreeBSD ne va me voir arriver que par hasard, parce
qu'entre toutes les BSD ca me semble la plus sympa et la plus agréable a
utiliser, plus le fait que le système de ports me convient bien (j'aime
pouvoir configurer mes logiciels de façon assez profonde.)

Voila, c'est mon avis sur ce "problème" actuel du monde de Linux. Bien
entendu, je continuerai a utiliser Linux, et je ne peux qu’espérer que
les systèmes tels que systemd ou dbus ne disparaissent, ou tout du moins
n'apparaissent jamais chez certaines distributions, créant de ce fait un
choix pour les utilisateurs.  
[1]: Je n'ai pas trouvé de traduction satisfaisante a "software leveraging", mais l'idée est la...*
  
  [here]: http://data.wxcafe.net/archives/126
  [page d’accueil]: http://hub.opensolaris.org/bin/view/Main/
