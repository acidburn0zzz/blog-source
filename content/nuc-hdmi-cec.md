Title: les NUCs et le HDMI-CEC
Date: 2015-08-22 02:43
Author: Wxcafe
Category: Note
Slug: nuc-hdmi-cec

J'ai récemment récupéré une télé. Ce post ne se centrant pas sur cette télé,
passons rapidement sur ce qui y est lié : ne souhaitant pas "profiter" du
paysage audiovisuel français (ou PAF), et ayant nombre de films et séries acquis
tout a fait légalement (hmm hmm) stockés sur mon serveur local, je souhaitais
brancher sur ma télévision un système me permettant de regarder ces films et
séries, et possiblement quelques sources de vidéos en ligne (Youtube, Netflix,
etc...) simplement.

Ayant un [Raspberry Pi 1](https://www.raspberrypi.org/) qui trainait, j'ai
décidé d'installer [OpenELEC](http://openelec.tv/) dessus et de voir ce que ça
donnait. Le résultat n'étant pas satisfaisant (a cause des difficultés du RPi
a faire fonctionner tout ça), j'ai décidé d'upgrader le système.

J'ai donc acquis un [NUC D34010WYK](http://www.amazon.fr/gp/product/B00GPJ83EU)
(attention, les nouveaux modèles ne fonctionnent pas pour ce qui suit), un 
[adaptateur HDMI-CEC](http://www.amazon.fr/dp/B00WU5F8MS/) pour celui-ci, et un
[SSD mSATA](http://www.amazon.fr/gp/product/B00INTR4ZE), en me disant que je
pourrais sans trop de problème faire tourner [Kodi](http://kodi.tv/) sur un
debian, avec en plus Steam pour faire du streaming depuis mon desktop. L'autre
avantage de tourner sur du Intel, c'est de pouvoir mater Netflix (puisque le
plugin kodi approprié utilise chrome, et ne fonctionne (a ma connaissance) que
sur x86).

J'ai donc reçu après un certain temps le matériel sus cité, que j'ai avidement
monté, avant de me rendre compte que le manuel de l'adaptateur Pulse-Eight était
\[PDF\][assez médiocre](https://www.pulse-eight.com/Download/Get/30). J'ai donc
cherché plusieurs heures, avant de trouver \[DE\][ce 
post](http://www.technikaffe.de/anleitung-293-pulse_eight_intel_nuc_hdmi_cec_adapter_im_test)
expliquant comment brancher l'adaptateur. Je vais donc résumer ici le processus,
ce qui devrait rendre la tache a la fois plus simple pour les autres personnes
cherchant l'information, et pour moi si je dois remonter ce système.

Pour faire simple, le NUC présente trois headers séparés : un dual-USB, un dit
"Front Panel", et un appelé "Custom Solution Header". Les trois sont utilisés
ici. La première chose a faire est de brancher les fiches grises et rouges sur
le Custom Solution Header: le branchement doit être fait ainsi :

	Custom Solution
	  ┌─┬─┬─┬─┬─┐
	  │g│ │·│r│·│
	  ├─┼─┼─┼─┼─┤
	  │·│·│·│·│·│
	  └─┴─┴─┴─┴─┘
	
	  g ➔ fiche grise
	  r ➔ fiche rouge
	  · ➔ pin inutilisé
	    ➔ espace vide (sans pin)

Une fois cela fait, il faut brancher le Front Panel. Heureusement, c'est plus
facile, puisqu'il n'y a qu'une seule fiche a brancher ici : la orange.


	  Front Panel
	  ┌─┬─┬─┬─┬─┐
	  │·│·│·│·│·│
	  ├─┼─┼─┼─┼─┤
	  │ │·│o│·│·│
	  └─┴─┴─┴─┴─┘
	
	  o ➔ fiche orange
	  · ➔ pin inutilisé
	    ➔ espace vide (sans pin)

Enfin, il faut encore brancher les fiches restantes sur le header dual-USB.
Étant donné que ce header contient deux fois les pins nécessaires a un
branchement USB, il est possible de brancher les cables de plusieurs façons. 


	   Dual-USB
	  ┌─┬─┬─┬─┬─┐
	  │b│B│v│n│·│
	  ├─┼─┼─┼─┼─┤
	  │·│·│·│·│ │
	  └─┴─┴─┴─┴─┘
	
	  b ➔ fiche bleue
	  B ➔ fiche Blanche
	  v ➔ fiche verte
	  n ➔ fiche noire
	  · ➔ pin inutilisé
	    ➔ espace vide (sans pin)

Tous les branchements étant effectués, il faut maintenant remonter la bête
(attention a ne pas déranger les branchements avec les antennes Wifi, par
exemple), la brancher, et vérifier que tout démarre bien. Il faut aussi changer
un paramètre dans le BIOS intel : dans Power➔Secondary Power Settings, il faut
que "Deep S4/S5" soit *dés*activé. Ceci permettant a la connection HDMI-CEC de
démarrer et le NUC.

Ne reste plus ensuite qu'a installer un système digne de ce nom dessus!
