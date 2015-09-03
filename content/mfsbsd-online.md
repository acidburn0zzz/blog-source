Title: Installer FreeBSD sur un serveur Online avec MfsBSD
Date: 2014-08-28 12:16
Author: Wxcafe
Category: Tutoriel
Slug: freebsd-online-mfsbsd

J'ai récemment eu l'occasion de louer un serveur chez Online.net (filiale de Illiad)
Voulant depuis pas mal de temps gérer un serveur sous FreeBSD (et tester [bhyve](http://bhyve.org/))
et n'ayant pour différentes raisons pas eu l'occasion de le faire sur mon 
[serveur auto-hebergé](http://home.wxcafe.net) ni sur [ce serveur ci](http://wxcafe.net), 
j'ai commencé a chercher comment le faire sur ce serveur.

Étant donné que Online ne propose pas directement d'image FreeBSD sur ses serveurs, il m'a fallu
chercher un peu plus loin. Il se trouve que [ce post](http://forum.online.net/index.php?/topic/3557-installation-de-freebsd-91-amd64-sur-une-dedibox-lt15k-2013/) sur les forums
d'online explique une procédure, mais celle-ci ne fonctionnait pas pour mon serveur en particulier. 

J'ai donc cherché un peu sur internet, puis demandé sur irc (#freebsd-fr@freenode),
ou l'on m'a dirigé vers [mfsbsd](http://mfsbsd.vx.sk/), un projet d'installeur
alternatif, minimaliste et simplifié pour FreeBSD.

Pour installer FreeBSD sur votre serveur, donc, il vous faudra accéder a une
console KVM (dans mon cas personnel, iLO). Cela doit être faisable depuis le
panel Online. Une fois cela fait, lancez une console, puis téléchargez l'image
mfsbsd. Dans la console iLO, choisissez de booter sur une image CD/DVD, puis
choisissez l'image mfsbsd. Ensuite, rebootez le serveur. Choisissez de booter
sur l'image CD/DVD (F11 puis 1). Une fois ceci fait, un FreeBSD a l'air tout
a fait classique va démarrer. Une fois ceci fait, la partie importante arrive:
mfsbsd contient un script d'installation root-on-zfs, nommé logiquement
zfsinstall, qui va se charger de tout le travail pour nous.

Utilisez donc ce script ainsi : 

	::bash
	# tout d'abord, wipons le MBR :
	dd < /dev/zero > /dev/da0 count=1
	# maintenant, installons le système
	zfsinstall -g da0 -u ftp://ftp.freebsd.org/pub/FreeBSD/releases/amd64/10.0-RELEASE/ -s 2G -p root -c

Avec `-g da0` votre disque dur principal, `-s 2G` la quantité de swap désirée,
`-p root` le nom du zpool, et `-c` pour activer la compression. D'autres options
sont disponibles, je vous invite a faire un `zfsinstall -h` si mon setup ne vous
convient pas.

Une fois ceci fait, faites un chroot dans /mnt (ou doit se trouver le nouveau
système) et éditez /etc/rc.conf :

	::python
	zfs_load="YES"
	sshd_load="YES
	hostname="whatever"
	ifconfig_igb0="DHCP"

Remplacez whatever par votre hostname, et igb0 par le nom de votre interface
physique connectée a internet. Quittez le chroot, rebootez, et voila, vous avez
maintenant un système FreeBSD tout propre installé sur zfs a découvrir et
utiliser!

Voila, c'est la fin de ce tutoriel.
(Cela dit, bon courage pour tester bhyve, vu que l'IPv6 chez online est... peu 
crédible, disons)

Bon sinon sur d'autres sujets, j'ai mis en place des bots twitter : 
[wxcafe_ebooks](https://twitter.com/wxcafe_ebooks),
[petitefanfare](https://twitter.com/petitefanfare),
[capet_ebooks](https://twitter.com/capet_ebooks),
[zengisse](https://twitter.com/zengisse),
et [kim_ebooks](https://wxcafe.net/kim_ebooks). Ils sont tous basés sur [ce
code](https://github.com/wxcafe/ebooks_example), qui vient de
[@m1sp](https://twitter.com/m1sp)
([github.com/twitter_ebooks](https://github.com/twitter_ebooks)). Donc voila.

A plus

