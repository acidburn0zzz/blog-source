Title: OpenWRT, l'USBNet, et l'histoire des 4Mo
Date: 2015-10-16 10:27
Author: Wxcafe
Category: Hacking
Slug: openwrt-usbnet

Donc, j'ai récemment obtenu un [TP-Link
TL-MR12U](http://www.dx.com/p/tp-link-tl-mr12u-portable-5200mah-mobile-battery-3g-router-white-231188),
qui est vendu comme "routeur 3G portable", mais qui est en réalité une grosse
batterie avec une antenne wifi, un port USB, et un port Ethernet. Perso, ça me
va, vu que je comptais de toute façon pas prendre un deuxième abonnement 3G
juste pour ce truc là (surtout vu la couverture 3G qu'on se tape en France...)

Bref, tout ça pour dire : quand j'ai reçu ce truc, j'ai tout de suite commencé
par y installer OpenWRT (parce que de 1, je parle pas chinois, et de 2, j'aime
bien avoir des firmwares corrects sur mes routeurs). Bon, c'est super simple, il
suffit de chopper ce fichier
\[binaire\] [la](http://downloads.openwrt.org/chaos_calmer/15.05/ar71xx/generic/openwrt-15.05-ar71xx-generic-tl-mr12u-v1-squashfs-factory.bin),
et de trouver la page d'update (pas forcément super simple en chinois, mais avec
un peu de temps, ça se fait. C'est celle avec un bouton upload). Ensuite on
upload l'image sur le bouzin, et c'est parti. Pas de signatures, pas de
vérifications, osef total, mais bon pour le coup ça m'arrange.

Une fois ceci fait, je me trouva bien démuni de ne pas pouvoir utiliser le
partage de connexion USB de mon intelliphone android, car l'image OpenWRT par
defaut ne comprend pas USBNet, et ne peut donc pas créer de réseau sur de l'USB.
Qu'à cela ne tienne, me dis-je! Je vais l'installer!
Je courra donc installer le package grâce à `opkg`. Las! Le système n'avait plus
de place.

... Atta. Le système avait plus de place? J'ai encore rien mis dessus!

Eh bah ouais. Il se trouve que TP-Link, en 2015, trouve que 4Mo de flash sur un
routeur, c'est largement suffisant, et que de toute façon personne aura jamais
besoin de plus.

Serieux, mettre 8Mo c'était tellement plus cher? u_u

Bon, bref, je vais pas m'étendre la dessus. J'ai décidé de saisir mes petits
bras, et de tenter de pousser bien fort pour convaincre OpenWRT qu'il était tout
a fait possible de faire rentrer à la fois le système de base avec LuCi, uhttpd,
un serveur DHCP, etc; et USBNet, dans 4Mo. Ça à pas été vraiment facile, et j'ai
du virer pas mal de trucs, mais... ça fonctionne!

Bon, alors, comme je suis quelqu'un de sympa, je vais vous filer à la fois le
fichier de config et l'image finale. Si vous voulez pas utiliser une image qui
vient d'un mec que vous connaissez pas, vous pouvez toujours la rebuilder vous
même. Mais avant ça, je vais vite fait expliquer ce qui est dans l'image et ce
qui n'y est pas

Alors, pour faire rentrer tout ça, vous vous doutez que j'ai du faire quelques
concessions. J'ai donc viré tout ce qui a trait à *PPP*, *PPPoE*, le client
*DHCPv6*, tous les *outils de debug*, quelques *fonctionnalités de busybox*, et
bien sûr *opkg*. Dans ce qui à été ajouté, simplement ce qui est nécessaire au
fonctionnement de *l'USBNet*.

Une petite modification doit être effectuée pour que le tout fonctionne : le
fichier `package/feeds/luci/luci/Makefile` doit être modifié pour que la
dépendance sur `luci-proto-ppp` ne soit plus présente. Ainsi, on passe de

```makefile
LUCI_DEPENDS:= \
	+uhttpd +uhttpd-mod-ubus +luci-mod-admin-full +luci-theme-bootstrap \
	+luci-app-firewall +luci-proto-ppp +libiwinfo-lua +IPV6:luci-proto-ipv6
```

à

```makefile
LUCI_DEPENDS:= \
	+uhttpd +uhttpd-mod-ubus +luci-mod-admin-full +luci-theme-bootstrap \
	+luci-app-firewall +libiwinfo-lua +IPV6:luci-proto-ipv6
```

Une fois que c'est fait, ça devrait mieux marcher (et ça sauve un peu
d'espace...)

Bon. Le fichier de config est
[là](http://pub.wxcafe.net/static/openwrt/tl-mr12u/config), l'image finale est 
[là](http://pub.wxcafe.net/static/openwrt/tl-mr12u/openwrt-15.05-wx-ar71xx-generic-tl-mr12u-v1-squashfs-factory.bin),
et j'ai une petite surprise.

Bien sûr, le switch situé sur le côté du TL-MR12U ne fonctionne pas sous
OpenWRT de base, parce que c'est un truc lié au hardware et que du coup c'est
assez compliqué à gérer sur une base de matos aussi grande que celle d'OpenWRT.
Bah j'ai à peu près trouvé comment le faire fonctionner. 
Voilà le code :

```shell
#!/bin/sh
if [ $ACTION == "released" ]; then
	if [ $BUTTON == "BTN_0" ]; then
		# Position is 3G
		logger "slider 3G"
	elif [ $BUTTON == "BTN_1" ]; then
		# Position is Router
		logger "slider Router"
	fi
elif [ $BUTTON == "BTN_1" ] || [ $BUTTON == "BTN_0" ]; then
	if grep -qe "sw1.*in  hi" /sys/kernel/debug/gpio\
	&& grep -qe "sw2.*in  hi" /sys/kernel/debug/gpio; then
		# Position is AP
		logger "slider AP"
	fi
fi
```

Et ça va dans `/etc/hotplug.d/button/00-buttons` (créez le chemin, il existera
pas à la base). Du coup là comme ça ça fait rien, ça loggue juste les events.
Mais comme vous êtes pas cons vous avez peut être deviné qu'on pouvait très bien
activer l'USBNet que quand l'interrupteur est en position 3G, le wifi et
l'ethernet quand il est en position AP, et juste la batterie quand il est en
position Router. Par exemple.

Tiens, d'ailleurs. Pour activer le partage de connexion, suffit pas d'ajouter le
support USBNet. Il faut aussi configurer le système pour qu'il demande un lease
DHCP, toussa. Du coup vous pouvez (peut être, j'ai pas testé) le faire par LuCi,
mais sinon vous pouvez le faire en CLI :

```shell
uci del network.wan
uci set network.wan=interface
uci set network.wan.ifname=usb0
uci set network.wan.proto=dhcp
uci commit network
ifup wan
```

Et pouf, ça marche.

Voilà. Amusez vous bien avec votre grosse batterie portable, qui fait maintenant
point d'accès wifi/partage de connexion 3G/whatever.
