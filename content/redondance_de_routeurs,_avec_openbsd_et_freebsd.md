Title: Redondance de routeurs, avec OpenBSD et FreeBSD
Date: 2016-07-29T17:53+02:00
Author: Wxcafé
Category:
Slug: redondance-routeurs-openbsd-freebsd

Depuis le début de mon DUT (il y a deux ans), j'ai découvert le monde du réseau,
alors que j'étais plus système auparavant. Au cours de ce processus, j'ai
pu observer quelques coutumes étranges de ce milieu. Ainsi donc, dans cet étrange
domaine, il arrive parfois qu'on cherche à avoir un réseau stable pendant une
période relativement longue. Bien évidemment, ceci se trouve être un problème
Complexe®, a cause notamment des différents constructeurs de matériel réseau, et
des différents systèmes d'exploitation des machines qui font passer les chatons
dans les tuyaux.

Bref, en général on règle ce problème de façon relativement simple : en
utilisant un système stable, _par exemple_ OpenBSD. Cependant, ça ne suffit pas
toujours: on peut aussi rencontrer des erreurs hardware. Et puis même OpenBSD
peut rencontrer des problèmes softwares aussi, de temps en temps. Il paraît.
J'ai lu un truc la dessus quelque part.

Bref, après cette intro complètement objective, on va parler de redondance de
routeurs (c'est a dire la mise en place de deux routeurs hardwares en même
temps, avec un qui prend le relai de l'autre en cas de problème). On va aussi
faire en sorte qu'ils utilisent deux réseaux externes différents (d'opérateurs
séparés, par exemple), pour faire bonne mesure.
Vu que c'est un projet pour mon DUT à la base, et qu'on a fait que du Linux la
bas, j'ai décidé de le réaliser avec un OpenBSD et un FreeBSD, sur un laptop et
une Cubieboard 2 (une board ARM qui traînait chez moi), en utilisant des VLANs
(puisqu'ils n'ont qu'une seule NIC). C'est aussi pour ça qu'il y a un FreeBSD,
vu que la Cubieboard ne supporte qu'assez mal OpenBSD (en tout cas d'après mon
expérience)

Tout d'abord, je vais mettre [ici](https://pub.wxcafe.net/static/redondance.pdf)
le rapport produit pour mon DUT, comme le veut la tradition du TL;DR (tu le sens
mon LaTeX?). Si vous voulez pas lire cette explication, vous pouvez lire l'autre
explication qui est en PDF et orientée pour des profs de DUT. Si vous êtes prof
de DUT j'imagine que ça peut être intéressant.

Bon, donc la première chose a faire c'est de définir quelques trucs. La
redondance, on l'a dit, c'est le fait d'avoir plusieurs équipements effectuant
une tâche similaire, pour qu'en cas de panne l'un prenne la place de l'autre
sans interruption. Quelques acronymes :

- CARP, *Common Address Redundancy
Protocol*, est un protocole (développé par OpenBSD pour remplacer VRRP) qui
permet de faire de la redondance entre des équipements IP, en leur permettant
de partager une adresse IP en switchant rapidement en cas de problème avec l'un
des équipements.

- PF, *Packet Filter*, est le firewall d'OpenBSD et de FreeBSD.
Enfin, des versions différentes. Mais l'idée est la. (en pratique, la version de
FreeBSD est plus ancienne mais supporte le multi-CPU, contrairement a celle
d'OpenBSD (mais bon, on connait le support multi-CPU d'OpenBSD...)).

- PfSync, *Packet Filter Synchronisation*, est un service qui permet de
synchroniser la table d'état de deux instances de PF. De cette façon, quand un
des deux crashe, le second peut reprendre les connexions en cours et évite de
couper trop de transmissions.

- IfStated est un petit programme qui permet de vérifier l'état d'une interface
réseau régulièrement et de lancer des commandes en fonction de l'état de celle
ci.


Bon, maintenant que ces définitions sont claires, passons à la réalisation. Le
système OpenBSD sera le serveur primaire, et le FreeBSD sera la réplique, car
OpenBSD est capable de routage multipath (répartition du traffic entre deux
routes de manière égale), ce que FreeBSD ne sait pas faire. Ainsi, si R1 (la
machine OpenBSD) est primaire, elle est capable de transférer une partie du
traffic vers R2 (la machine FreeBSD). Si elle s'arrête de fonctionner, R2 n'a
pas besoin de faire de multipath, puisqu'a ce moment la une seule route valide
est encore disponible.

La première chose à faire est de configurer le réseau sur nos deux machines.
Puisqu'elles ont toutes les deux une seule interface réseau, nous utilisons des
VLANs (en conjonction avec un switch correct, je vous laisse trouver la
configuration de celui-ci. Il faut connecter les deux machines sur des ports
Trunk). Le VLAN 300 sera utilisé pour le réseau interne, le 400 pour le réseau
externe A et le 500 pour le réseau externe B. Ainsi, on aura un réseau qui
ressemble à ceci :

```
╭──╮   ╭─────────────╮   ╭──╮
│  │   │    Switch   │   │  │
│R1│   │             │   │R2│
│  │   │             │   │  │
╰──╯   ╰─────────────╯   ╰──╯
  ╚════════╝     ╚═════════╝
```

en terme physique, et ceci :

```
            ╔══════╗   ╔══════╗
╭──╮    ╭────╮    ╭─────╮    ╭────╮   ╭──╮
│OP│    │    │    │     │    │    │   │OP│
│  │    │ R1 │    │ LAN │    │ R2 │   │  │
│A │    │    │    │     │    │    │   │B │
╰──╯    ╰────╯    ╰─────╯    ╰────╯   ╰──╯
  ╚════════╝                   ╚════════╝
```

au niveau réseau.
On va aussi utiliser le réseau 30.30.30.0/24 sur le réseau interne pour cet
exemple.

Pour ce faire, on configure les routeurs ainsi :

#### R1 (OpenBSD):

**/etc/hostname.em0:**

```
up
```

**/etc/hostname.vlan0:**

```
inet 30.30.30.1 255.255.255.0 30.30.30.255 vlan 300 vlandev em0
```

**/etc/hostname.vlan1:**

```
dhcp vlan 400 vlandev em0
```

#### R2 (FreeBSD):

**/etc/rc.conf**

```
[...]
vlans_dcw0="300 500"
ifconfig_dwc0_300="inet 30.30.30.2 netmask 255.255.255.0"
ifconfig_dwc0_500="DHCP"
```

Une fois ceci fait, nos machines sont configurées sur leurs réseaux externes
respectifs (via DHCP, adaptez si votre réseau externe utilise une autre
méthode) et sur le réseau interne. Il faut bien entendu remplacer les noms
d'interfaces (`em0`, `dcw0`) par le noms des interfaces présentes sur vos
machines.

Nous allons maintenant configurer la redondance elle même avec CARP. Le réseau
avec lequel nous allons nous retrouver ressemble à ceci :

```
                 ╭───────╮
           ╔═════│  VIP  │══════╗
           ║     ╰───────╯      ║
           ║         ║          ║
╭──╮    ╭────╮    ╭─────╮    ╭────╮   ╭──╮
│OP│    │    │    │     │    │    │   │OP│
│  │    │ R1 │    │ LAN │    │ R2 │   │  │
│A │    │    │    │     │    │    │   │B │
╰──╯    ╰────╯    ╰─────╯    ╰────╯   ╰──╯
  ╚════════╝                   ╚════════╝
```

La configuration de CARP se fait en fait comme pour une interface réseau
classique :

#### R1:

**/etc/hostname.carp0:**

```
vhid 125 pass pwd12345 carpdev vlan0 advbase 3 advskew 1 state master
30.30.30.254 netmask 255.255.255.0
```

#### R2:

**/etc/rc.conf:**

```
[...]
ifconfig_dwc0_300_alias0="vhid 125 advbase 3 advskew 200 \
  state backup pass pwd12345 alias 30.30.30.254/24"
```

Une fois que CARP est mis en place, nous configurons PF, pour filtrer les flux
que nous laissons passer sur notre réseau. Les configurations suivantes,
différentes pour R1 et R2 (puisque FreeBSD et OpenBSD n'utilisent pas les mêmes
versions de PF), sont évidemment à modifier en fonction de votre installation:
elles sont très minimales (ne laissant même pas passer le http...)

#### Pour R1:

**/etc/pf.conf:**

```
set skip on lo

# définition des variables
int="30.30.30.0/24"
ext="0.0.0.0/0"
int_addr="30.30.30.1"
int_if="vlan0"
ext_if="vlan1"

# defaut : bloquage
block all

# vérification des paquets, anti-spoofing
antispoof for $int_if
antispoof for $ext_if

# nous laissons passer l'icmp
pass proto icmp

# nous mettons en place le NAT de l'interieur vers Internet
pass in on $int_if from $int to any keep state
pass out on $ext_if from $int to $ext nat-to $int_if keep state

# carp, pfsync et dhcpsync
pass out on $int_if proto carp keep state
pass quick on $int_if proto pfsync keep state
pass in on $int_if proto udp to any port 8067 keep state
pass out on $int_if proto udp to any port 8067 keep state

# nous laissons passer les connexions SSH vers le routeur
pass in on $int_if proto tcp from $int to $int_addr port ssh keep state
pass out on $int_if proto tcp from $int_addr port ssh to $int keep state
```

#### Et pour R2:

**/etc/pf.conf:**

```
set skip on lo

# définition des variables
int="30.30.30.0/24"
ext="0.0.0.0/0"
int_addr="30.30.30.2"
int_if="dwc0.300"
ext_if="dwc0.500"

# défaut : bloquage
block all

# vérification des paquets, anti-spoofing
antispoof for $int_if
antispoof for $ext_if

# nous laissons passer l'icmp
pass proto icmp

# nous mettons en place le NAT de l'interieur vers Internet
nat on $ext_if from $int to any -> ($ext_if)
pass in on $int_if from $int to any keep state
pass out on $ext_if from any to $ext

# carp, pfsync et dhcpsync
pass out on $int_if inet proto carp keep state
pass quick on $int_if inet proto pfsync keep state
pass in on $int_if inet proto udp to port 8067 keep state
pass out on $int_if inet proto udp to port 8067 keep state

# nous laissons passer les connexions SSH vers le routeur
pass in on $int_if inet proto tcp from $int to $int_addr \
port ssh keep state
pass out on $int_if inet proto tcp from $int to $int_addr \
port ssh keep state
```

Une fois que PF est configuré, on passe a pfsync, qui permet de synchroniser
l'état de deux instances de PF, même de versions différentes (je trouve ce truc
génial):

#### Pour R1:

**/etc/hostname.pfsync0:**

```
syncdev vlan0 syncpeer 30.30.30.2
```

#### Et pour R2:

**/etc/rc.conf:**

```
pfsync_enable="YES"
pfsync_syncdev="dwc0.300"
pfsync_syncpeer="30.30.30.1"
```

Passons à ifstated. Puisque R1 supporte le multihoming mais pas R2, nous allons
faire en sorte que R1 aie une route multipath vers R2. De cette façon, R1 (qui
est la machine principale pour CARP, et reçoit donc toutes les connexions venant
du réseau interne), transmet la moitié de ces connexions vers R2, qui les gère
comme nécessaire. Si R1 arrête de fonctionner, R2 récupère l'ensemble des
connexions (grâce a CARP), qui ne sont pas interrompues (grâce a pfsync). Si R2
arrête de fonctionner, ifstated rentre en action et retire la route multipath de
R1 vers R2, ce qui permet d'éviter de transmettre la moitié des connexions à un
routeur qui ne fonctionne plus (c'est en général une chose a éviter).

Par conséquent, la configuration d'ifstated n'a à être effectuée que sur R1 :

**/etc/ifstated.conf:**

```
peer = '( "ping -q -c 1 -w 3 30.30.30.2>/dev/null" every 5 )'

state auto {
	if $peer
		set-state multihome
	if ! $peer
		set-state singlehome
}
state multihome {
	init {
		run "route add -mpath default 30.30.30.2"
	}
	if ! $peer
		set-state singlehome
}
state singlehome {
	init {
		run "route delete default 30.30.30.2"
	}
	if $peer
		set-state multihome
	}

init-state auto
```

Enfin, dernier point a configurer, la synchronisation DHCP. Elle nous permet de
faire en sorte que les machines gardent les mêmes adresses IP même si un des
deux routeurs reste en rade pendant une période prolongée. On configure donc
`isc-dhcpd` sur les deux routeurs, comme suit:

#### R1:

**/etc/dhcpd.conf:**

```
authoritative;
ddns-update-style none;

failover peer "dhcp-failover" {
	primary;
	address 30.30.30.1;
	port 8067;
	peer address 30.30.30.2;
	peer port 8067;
}

subnet 30.30.30.0 netmask 255.255.255.0 {
	option routers 30.30.30.254;
	option domain-name-servers 30.30.30.254;
	pool {
		failover peer "dhcp-failover";
		max-lease-time 86400;
		range 30.30.30.10 30.30.30.250;
	}
}
```

#### Et pour R2:

**/usr/local/etc/dhcpd.conf:**

```
authoritative;
ddns-update-style none;

failover peer "dhcp-failover" {
	secondary;
	address 30.30.30.2;
	port 8067;
	peer address 30.30.30.1;
	peer port 8067;
}

subnet 30.30.30.0 netmask 255.255.255.0 {
	option routers 30.30.30.254;
	option domain-name-servers 30.30.30.254;
	pool {
		failover peer "dhcp-failover";
		max-lease-time 86400;
		range 30.30.30.10 30.30.30.250;
	}
}
```

Et voilà! Notre réseau ressemble désormais à ça (j'ai repris le schéma de mon
rapport, j'ai pas le courage de le refaire en texte encore):

![schéma](https://pub.wxcafe.net/img/schema_redondance_routeurs.png)

avec le PC1 qui représente le réseau local.

Si vous avez bien lu la configuration du serveur DHCP, il reste encore à mettre
en place un serveur DNS écoutant sur l'IP virtuelle, donc a priori synchronisé
entre les deux routeurs. Comme c'est quelque chose de simple a mettre en place
et que c'est assez bien documenté ailleurs, je laisse cette tâche comme exercice
aux lecteurs-ices.
