Title: Plan9 from whichever space
Date: 2013-09-09 11:17
Author: Wxcafe
Category: OSes
Slug: plan-9-from-whichever-space

[__Plan 9 from Outer Space__](http://en.wikipedia.org/wiki/Plan_9_from_Outer_Space) est un film de série Z, produit en 1959 par Edward D. 
Wood. Il est assez connu comme étant l'un des pires films jamais sortis. Rempli
d'erreur de montage, d'effets spéciaux au rabais, et ayant même connu la mort
d'un acteur, il a ainsi atteint le statut de film culte grâce a sa médiocrité.

[__Plan 9 from Bell Labs__](http://plan9.bell-labs.com/plan9/) est un OS venant de Bell Labs (comme son nom l'indique),
et qui a été pensé comme le successeur d'Unix. Il est conçu comme une poursuite
des concepts unixiens jusqu'à leur but naturel. Ainsi, c'est Plan9 qui a
introduit le concept d'UnionFS, le protocole 9P qui permet d'acceder a des
ressources appartenant a d'autres ordinateurs a distance, un support de
l'unicode par défaut et sur tout le système (a l'inverse d'Unix, qui fonctionne
a la base en ASCII), un support de ProcFS amélioré, une interface graphique par
défaut, et d'autres améliorations sur les thèmes de base que propose Unix. 

Cependant, Plan9 n'a jamais été véritablement utilisé pour quoi que ce soit
d'autre que la recherche en systèmes, et c'est dommage, parce que Plan9 a
quelque chose de très intéressant à proposer. En effet, en ces jours d'intérêt
grandissant pour le klaoude et la délocalisation a la fois du processing et des
données, et bien que Plan9 ait été créé bien avant que le terme "cloud
computing" n'apparaisse pour la première fois, il semble que ce système ait été
conçu pour apporter cette délocalisation tant rêvée.

En effet, même si l'on considère que les nouveautés qu'il apporte par rapport a 
Unix ne sont pas extraordinaires en soit (alors qu'elles sont déjà
conséquentes), lorsqu'on les prend ensemble, elles font de Plan9 le système
d'exploitation ultime en terme de partage de ressources et de données. 
Ainsi, le fait que 9P permette de considérer toutes les ressources d'un système
distant comme n'étant qu'une poignée de fichiers permet de le monter comme
n'importe quel système de fichier. Le fait que chaque utilisateur puisse accéder
a plusieurs namespaces de façon transparente (et donc de démarrer, arrêter et 
gérer des processus sur chacun de ces namespaces) et que chaque namespace puisse
interagir avec les autres, même s'ils sont hétérogènes (c'est a dire provenant
de machines différentes), permet d'utiliser les ressources d'une machine
distante comme si elle était présente localement. Le mécanisme d'UnionFS permet
de rendre tout ça utilisable, en montant plusieurs systèmes de fichiers sur le
même point de montage, en même temps, et de pouvoir ainsi accéder aux fichiers
de plusieurs machines a la fois (ce qui permet une délocalisation des données
bien plus poussée que Dropbox ou Google Drive, et ce en kernelspace).

Le réseau fait donc partie intégrante de Plan9, et il devient plus difficile de
parler d'ordinateur lorsque le concept même du système est d'être composé de 
clusters eux mêmes composés de machines hétérogènes. Le système de fichier
virtuel /net fourni par le kernel de Plan9 permet d'implémenter très facilement
différents concepts réseaux : en montant le /net d'un ordinateur du réseau local
sur celui servant de gateway vers l'internet, on crée un NAT vers cet ordinateur
du réseau local. En montant le /net d'un ordinateur distant sur un ordinateur
local via le protocole 9P sécurisé, on crée un VPN : les connections locales se
font en utilisant l'accès de l'ordinateur distant, et les connections entre les
deux sont chiffrées. 

Bref, bien avant les clusters de Raspberry Pi qui utilisent une api python pour
partager leur "puissance" de calcul en userspace, des superordinateurs pour
lesquels le noyau Linux s'est doté du support de jusqu'à 4096 CPUs, des OS tels
JoliOS qui promettent une integration du klaoude alors qu'ils ne sont en fait
que des navigateurs web a peine améliorés et des services de stockage en ligne
qui promettent un accès universel a toutes nos données alors qu'ils ne proposent
que de les garder a disposition par le web, Plan9 promettait une technologie de 
partage des ressources système et de données, une intégration du réseau dans le
système particulièrement poussée, un environnement graphique supporté par le
basesystem et non greffé par dessus comme l'a été X11, et de nombreuses autres 
améliorations sur Unix.

Malheureusement, il n'a jamais été adopté de façon véritablement significative,
et ce pour une raison très Unixiènne : "worse is better". En effet, le parc de
machines Unix déjà installées était suffisamment performant et fonctionnel pour
que des solutions soient développées au dessus du système pour remplir les 
mêmes fonctions que remplit Plan9 *via* son kernel, tels le nouveau ProcFS de
Linux, FUSE, etc...
