Title: Archlinux made simple
Date: 2012-10-05 14:48
Author: Wxcafe
Category: OSes 
Slug: archlinux-made-simple

Archlinux est réputée être une distribution Linux très complexe a
installer et a maintenir.

Je vais tenter ici de vous convaincre que ce n'est pas le cas, et
qu'elle peut se monter très intéressante et très instructive a installer
tout autant qu'a utiliser.

Il convient tout d'abord de rappeler a quels principes obéit Arch:

1. Le KISS : Keep It Simple and Stupid, Archlinux tente de faire des
	programmes simples et utilisables par tous. Avec comme base de
	simplicité les utilisateurs de LFS... Mais il n'empêche qu'avec un peu
	de bonne volonté, la configuration n'est pas si compliquée!

2. La philosophie UNIX : chaque programme est prévu pour ne remplir
	qu'une seule tâche. Bien entendu, cela ne concerne que les programmes
	conçus pour s’insérer dans la philosophie UNIX, et les installations de
	dépendances avec le gestionnaire de paquet d'Arch fonctionnent
	superbement bien.

De plus, posons les bases d'Arch : le gestionnaire de paquets s'appelle
pacman, et les commandes de base sont :

- recherche d'un paquet :

		pacman -Ss paquet

- installation d'un paquet :

		sudo pacman -S paquet

- désinstallation d'un paquet :

		sudo pacman -R paquet

- mise a jour de tous les paquets installés :

		sudo pacman -Syu paquet

Archlinux est une distribution dite "rolling release", ce qui signifie
qu'il n'y a pas de version a proprement dites, et que les paquets se
mettent a jour en permanence, sans jamais changer la "version" d'Arch.
Il n'y a d'ailleurs qu'une seule version de l'installeur sur le site,
puisqu'une version plus ancienne n'aurait aucun sens.

Arch n'offre pas d'interface graphique par défaut : après avoir installé
le système, vous n'aurez qu'une invite de commande. Heureusement, je
vais ici vous guider a travers l'installation d'une interface graphique
(mate, le fork de gnome 2)

L'installation d'Arch se fait par le réseau, veillez a avoir une
connection WiFi ou filaire a proximité avant de suivre ce guide.

Ce guide utilise SystemV, alors qu'Arch va prochainement passer sous
systemd. N'ayant pas encore eu le temps d’expérimenter assez avec ce
dernier, je ferais un tutoriel pour passer votre Arch a systemd bientôt.

Bon, passons a l'explication de l'installation proprement dite :

Tout d'abord, téléchargeons l'iso d'arch la plus récente :

	wget http://mir.archlinux.fr/iso/2012.09.07/archlinux-2012.09.07-dual.iso

Ensuite, gravons cette image sur un disque USB :

	dd if=archlinux-2012.09.07-dual.iso of=/dev/sdX

Après reboot de la machine sur l'iso en question et choix de
l'architecture, nous sommes accueillis par un shell root.

La première chose a faire est de paramétrer le clavier :

	loadkeys fr

Puis nous pouvons passer a l'installation proprement dite.
Partitionnement :

	cfdisk # cfdisk est suffisamment clair pour ne pas nécessiter d'explications

formatage des partitions :

	mkfs.ext4 /dev/sda1 # partition root

	pacman -Syu btrfs-progs && mkfs.btrfs /dev/sda2 # partition home

	mkswap /dev/sda3 && swapon /dev/sda3 # partition de swap

Montons les partitions nouvellement créées, puis installons le système :

	mount /dev/sda1 /mnt

	mkdir /mnt/home && mount /dev/sda2 /mnt/home 

	dhclient eth0 # si vous utilisez une connection filaire, sinon voire http://wiki.archlinux.fr/Wifi#Configuration

	pacstrap /mnt base base-devel

	genfstab -p /mnt > /mnt/etc/fstab

Allons prendre un café le temps que ça charge, puis installons les
quelques paquets nécessaires a notre installation et au premier
démarrage:

	pacstrap /mnt syslinux btrfs-progs wireless_tools dhclient

Maintenant, passons sur notre install toute fraîche d'Arch :

	arch-chroot /mnt bash

configurons les bases :

	echo HOSTNAME > /etc/hostname

	ln -s /usr/share/zoneinfo/Europe/Paris /etc/localtime

	date MMJJhhmmAAAA

	hwclock --systohc

	vim /etc/locale.gen # Décommentez les lignes correspondant au français : fr_FR.UTF-8 et fr_FR.ISO-8859-1

	echo  'LANG="fr_FR.UTF-8"' > /etc/locale.conf

	locale-gen

	mkinitcpio -p linux

Enfin, vérifions que syslinux est correctement configuré :

    vim /boot/syslinux/syslinux.cfg # il devrait y avoir "append root=/dev/sda1"

Si tout est correct, installons syslinux, et paramétrons un mot de passe
root :

    syslinux-install_update /dev/sda -mia

    passwd root

Et voila, l'installation est terminée! Plus qu'a quitter la session et a
redémarrer l'ordinateur!

     exit
    umount /mnt/home 
    umount /mnt
    reboot

Fini!

Prenons une petite pause. La partie suivante de ce tutoriel consister en
un paramétrage des principaux services nécessaires a l'utilisation d'un
OS, disons, moyen :

- Installation de MATE, le gestionnaire de bureau (voir
[http://mate-desktop.org/][])

- Installation de sudo et de networkmanager pour faire fonctionner les
composants essentiels du système sans avoir a tout activer a la main a
chaque démarrage

- Installation de SLiM comme gestionnaire de login graphique, pour
présenter une interface plus accueillante que la console, et
configuration de celui-ci

- Installation des principaux logiciels utiles non inclus dans mate ni
base (yaourt, chromium, thunderbird, etc...).

Ce guide est bien sur optionnel, si vous souhaitez utiliser Arch avec un
gestionnaire de bureau autre que mate, ou sans, vous pouvez vous arrêter
ici.

Bon, reprenons.

Nous sommes donc sur une demande de mot de passe. Entrez donc le mot de
passe paramétré plus haut pour le root, puis retapez la commande
utilisée plus tôt pour vous connecter a internet.

Il convient d'ajouter le dépôt de MATE pour installer ce dernier, puis
d'effectuer l'action en question :

    vim /etc/pacman.conf

Ici, ajoutez les lignes suivantes :

    [mate]
    Server = http://repo.mate-desktop.org/archlinux/$arch

Installons maintenant les paquets :

    pacman -Syu mate mate-extras dbus dbus-core alsa networkmanager sudo

Ajoutons un compte utilisateur pour utiliser les composants du système
sans tout crasher a chaque fois :

    useradd -g users -G wheel,audio,optical,lp,scanner,log,power,floppy,storage,games,video -m -s /bin/bash *votrenom*
    passwd *votrenom*
    su *votrenom*

Il faut maintenant éditer le fichier \~/.xinitrc pour préciser a X.org
ce que l'on veut utiliser :

    echo "exec ck-launch-session mate-session" > ~/.xinitrc

Profitons en pour ajouter les démons système au lancement :

    vim /etc/rc.conf

Ajoutez donc `dbus, alsa. hwclock` et `networkmanager` dans la section
DAEMONS (entre les parenthèses, après crond normalement)

    DAEMONS=(syslog-ng network crond dbus alsa hwclock networkmanager)

Pour éviter un reboot, il est ici possible de faire un

    su

Puis un

     /etc/rc.d/dbus start && /etc/rc.d/alsa start && /etc/rc.d/networkmanager start

Sinon, il est possible de juste redémarrer.  
Une fois cela fait, profitez de ce moment pour vous autoriser vous même
a utiliser sudo. Loggez vous en root, et :

     vim /etc/sudoers

Décommentez la ligne qui commence par \# %wheel ALL=(ALL)  
Sauvegardez le fichier, puis, après un `su *votrenom*`, tentez de faire
un sudo ls /  
Normalement, vous devriez avoir un listing du dossier /  
Bon, maintenant, pourquoi ne pas tenter de lancer MATE?  
C'est simple comme bonjour :

     startx

Et PAF! Voila un MATE desktop flambant neuf a configurer!  
Avant de faire ça, retournez sur un TTY (CTRL+ALT+Fx), loggez vous,
puis installez SLiM (`sudo pacman -Syu slim`).  
Configurons le:

    echo "exec dbus-launch mate-session" > ~/.xinitrc && vim /etc/slim.conf

Éditez la ligne
"`sessions            xfce4,icewm-session,wmaker,blackbox`" de facon a
ce qu'elle ressemble a "`sessions            mate-session`"  
Puis ajoutez slim dans /etc/rc.conf, dans la section DAEMONS.  
Normalement, tout devrait fonctionner!  
Ah oui, et pour installer thunderbird, firefox, chromium, etc...

    sudo pacman -Syu chromium thunderbird xchat firefox rhythmbox pidgin transmission-gtk vlc

Voila! Et comme dirait [@Spartition][], c'est sale, mais qu'est-ce que c'est
bon!  
A plus~

  [@Spartition]: https://twitter.com/spartition
  [http://mate-desktop.org/]: http://mate-desktop.org/
