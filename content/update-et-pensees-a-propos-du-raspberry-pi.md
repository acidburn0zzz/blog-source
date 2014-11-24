Title: Update et pensées a propos du Raspberry Pi
Date: 2013-01-27 01:55
Author: Wxcafe
Category: Ranting 
Slug: update-et-pensees-a-propos-du-raspberry-pi

Bon.  
J'ai annoncé il y a environ 20 jours que j'avais pour projet de faire
une Piratebox basée sur un Raspberry Pi, <del>astucieusement</del> nommée
PiRatBox. Il se trouve qu'après de nombreux essais, un problème
récurrent apparait: le Raspberry Pi n'est pas capable de fournir assez
de courant par défaut pour faire fonctionner a la fois un disque dur et
une antenne WiFi.  
Alors, autant il me semble évident qu'avec une
alimentation provenant d'un port USB a 2A (max), je n'avais pas
énormément de chances d'avoir 2A sur chacun des ports host du Raspi,
autant avoir moins de 250 mA sur chacun de ces ports me semble un tout
petit peu exagéré en terme de rentabilité.  

De même, le fait de ne pas pouvoir désactiver le port Ethernet (ne me
servant a rien) (vous savez, celui qui est monté en USB...), qui
consomme énormément, est assez louche. Il devrait toujours être possible
de désactiver une device USB, me semble-t-il, au niveau logiciel. La,
bien qu'il soit surement possible de la désactiver au niveau du kernel,
il n'est pas **simplement** possible de la "débrancher". Ce qui est bien
chiant, étant donné le besoin évident de puissance électrique dans
lequel on se retrouve.  

Bon, je dois avouer n'avoir pas testé de lancer les différents services
composant le système des piratebox sous arch, pour la simple <del>et
bonne</del> raison qu'arch utilise systemd et qu'il n'existe pas de wrapper
systemd pour les daemons piratebox, et que j'ai la flemme d'en faire,
parce que systemd est une horreur a utiliser avec les scripts init. Donc
non, j'utiliserai debian. Le problème d'utiliser debian dans ce cas
précis est que apt/dpkg a une gestion des dépendances dans un sens mais
pas dans l'autre, en ce sens que si on installe un package "haut", c'est
a dire dépendant de plusieurs autres packages, apt/dpkg se charge
efficacement d'installer toutes les dépendances nécessaires, tandis que
si on désinstalle un package "bas", c'est a dire sur lequel de nombreux
autres packages dépendent, apt/dpkg ne désinstalle pas ces packages
"hauts", ce qui pose un vrai problème quand on se retrouve sur un
Raspberry Pi, puisqu'il n'y a pas de moyen "facile" de choisir ce qui
sera installé sur le système avant l'installation proprement dite
(puisque le moyen "universel" d'installation sur Raspberry Pi est le dd
vers la SD qui sert de disque système.)

Il y a **énormément** d'autres critiques que l'ont pourrait faire
concernant le Raspberry Pi. Son système de démarrage a s'arracher les
cheveux, par exemple. En effet, plutôt que de faire comme tout pc
normalement constitué ou la partie calcul démarre, lance le bootloader,
cherche le kernel de l'OS qui lui même se lance, initialise le hardware,
etc..., a un système bâtard du au fait que la puce au centre de la carte
est a la base une puce graphique a laquelle on a greffé un cœur de
calcul (probablement au fond d'une cour d'immeuble, dans les quartiers
pauvres de Bratislava, vu la propreté de la greffe...), et le moyen le
plus efficace qu'aient trouvé les personnes ayant implémenté cette
atrocité de gérer le boot est donc de faire démarrer le cœur graphique
en premier, ce dernier exécute un code propriétaire pour démarrer le
cœur de calcul, qui a son tour lance le bootloader qui cherche le kernel
etc...  

Ce qui non seulement complique énormément le boot, non seulement ajoute
du code propriétaire a un projet se disant libre, mais en plus n'est
**visiblement** pas fait pour être utilisé de cette manière. Le hack,
oui, mais uniquement quand c'est bien réalisé, sinon je dis non.  

Enfin, le projet que j'avais est toujours en cours de réalisation. Je
le terminerai dès que j'aurai récupéré les outils nécessaires pour
monter mon alimentation personnalisée pour le Raspberry Pi. Et une fois
que cela sera fait, ce Raspi restera une Piratebox pour le reste de sa
vie. Les problèmes qu'il m'a posé, qu'il n'aurait pas du me poser, m'ont
trop agacé pour que j'aie envie de le sortir et de jouer avec une fois
sa mission remplie.  

Dommage.
