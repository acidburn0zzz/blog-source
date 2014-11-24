Title: Monter son propre serveur, partie 1: le serveur et l'apache.
Date: 2013-03-18 09:51
Author: Wxcafe
Category: Tutoriel
Slug: monter-son-propre-serveur-partie-1

Il y a un certain temps, j'avais parlé du concept du self-hosting. Il
s'agit de posséder son propre serveur, et donc, par extension, ses
données.  

Bien entendu, il n'est pas nécessaire pour cela de posséder
physiquement son propre serveur (encore que ce soit possible, mais ce
n'est pas le sujet abordé ici.)  
Nous expliquerons ici les étapes nécessaires pour arriver a avoir un
serveur utilisable, du moment ou vous arrivez sur le système fraichement
installé, au moment ou vous possédez un serveur avec tous les paquets
nécessaires a l'utilisation que l'on veut en faire ici d'installés.
Cette partie va consister a paramétrer le système (ici un debian
squeeze. Il est bien sur possible de faire la même chose avec a peu près
toutes les distributions Linux disponibles, tout comme avec les BSD et
tous les  autres systèmes UNIX, mais je vais ici me limiter a debian 6.0.x
squeeze, parce que c'est une distribution simple a utiliser comme
serveur, stable, et facile a configurer (puisqu'une bonne partie de la
configuration est déjà faite et incluse dans le paquet), donc adaptée au
but de cet article, a savoir rendre l'installation simple et
compréhensible).

La première chose a faire est bien entendu d'obtenir le serveur en lui
même. Cette partie de la chose ne sera pas traitée dans cet article. Il
existe en effet un nombre infini d'obtenir un serveur, que ce soit en le
louant chez OVH/1&1/n'importe quel autre hébergeur commercial, en
participant a un système d'hébergement collaboratif (je vous laisse
chercher), en achetant un serveur et en le faisant fonctionner de chez
vous, en utilisant un vieux PC... Bref, les possibilités sont multiples.
Dès  lors que vous avez accès a un système debian serveur, peu importe sur
quel matériel il fonctionne, et a priori peu importe aussi la manière
dont vous y accédez, le résultat est le même (et la procédure aussi...).
Dans cet article, nous parlerons de la configuration de base, du moment
ou vous avez le serveur vierge dans les mains au moment ou vous
installez le serveur http.

Dans cet article, lorsque est précisée le type d'IP a utiliser, il
convient de mettre ce type précisément. Quand le type n'est pas
précisée, libre a vous de choisir ipv4 ou ipv6.

Bref. Commençons au point ou vous avez un accès root a votre serveur,
n'ayant soit aucun mot de passe, soit un choisi par l'hébergeur, et ou
rien n'est configuré. Connectez vous a celui-ci (ssh root@). Commencez
donc par faire un ```passwd```, pour mettre au plus vite un mot de passe
solide sur le compte root. Continuons en allant vite mettre en place le
nom de domaine. Pour cela, votre registrar doit vous fournir une
interface vous permettant d'éditer l'entrée DNS pour votre nom de
domaine.  

Cette entrée doit donc pour l'instant ressembler a ca :

		<votre nom de domaine>	NS 1 
								IN MX 1 
								IN A		<IPv4 de votre serveur>
								IN AAAA		<IPv6 de votre serveur>

Cela vous permet de rediriger tout le trafic se référant a votre nom de
domaine vers votre ip (le fonctionnement exact du DNS est assez
compliqué a expliquer, donc on va dire que c'est de la magie pour
l'instant, ca sera peut être le sujet d'un autre article), et d'indiquer
que les mails @votre-nom-de-domai.ne doivent aussi être redirigés vers
votre serveur, ce qui est un bon début. Faisons un petit point sécurité
ici : pour accéder a votre serveur, il vous suffit actuellement de taper
le mot de passe root.

root est un utilisateur **assez** répandu, et il est assez simple de
bruteforcer le mot de passe. (*Relativement* assez simple, en fonction
du nombre de caractères, ça prend plus ou moins de temps, et si vous
avez suffisamment de caractères, ça peut prendre un temps assez
conséquent. Cela dit, il vaut mieux être prudent...) Ainsi, nous allons
arrêter d'utiliser root et nous allons commencer a utiliser des couples
clés publiques/privées pour nous connecter au serveur.  
Cela se fait en deux temps : tout d'abord, créer un nouvel utilisateur,
grâce auquel nous administrerons le serveur a l'avenir; puis configurer
OpenSSH pour que celui ci n'accepte que les connections par clés et plus
celles sur root.

Commençons par ajouter un utilisateur. Si vous êtes sous debian, cela se
fait avec adduser, qui est interactif (vous ne devriez pas avoir de
problème avec, puisqu'il crée tout les dossiers et fichiers nécessaires,
et vous pose toutes les questions utiles pour vous aider.) sinon, vous
devrez utiliser useradd, qui est (en plus d'être très chiant a
distinguer de l'autre, bien plus chiant a utiliser. (adduser est en fait
un simple script permettant l'utilisation d'useradd plus facilement.)

Avec adduser, vous pouvez soit utiliser le mode interactif en tapant
juste ```adduser <username>```, soit utiliser le mode non-interactif
en faisant un ```adduser --group <username>  
```

Avec useradd, vous devrez utiliser la commande suivante : ```useradd -m
-N -g <username>```. Cette commande ajoutera un utilisateur, créera
son dossier principal dans /home/, et l'ajoutera au groupe du même nom
que lui (ce qui est en général nécessaire pour des questions de vie
privée).

Il convient maintenant d'ajouter cet utilisateur aux groupes qu'il sera
amené a administrer: ```usermod <username> -a -G www-data postfix
users staff sudo wheel```, puis de changer son mot de passe
```passwd```. Enfin, ajoutons le aux utilisateurs autorisés a utiliser
sudo: ```echo "%sudo ALL=(ALL) ALL" >> /etc/sudoers```  
Enfin, changeons d'utilisateur : ```su```. A ce point, vous avec un
utilisateur complètement fonctionnel et utilisable pour toutes les
taches d'administration. Si vous devez encore utiliser root, c'est que
quelque chose ne va pas.

Vous êtes donc loggés sur le système en tant qu'utilisateur normal. Nous
allons maintenant passer a la phase 2 du plan : désactiver le login ssh
root et le login ssh par mot de passe.  
Tout d'abord, qu'est-ce qu'un login par clé ssh? Il s'agit en fait d'un
système assez semblable a celui vous permettant de chiffrer vos mail :
vous avec une clé publique et une clé privée sur le client, et la clé
publique est aussi sur le serveur. Lorsque vous vous connectez, openssh
vérifie que vous possédez la clé privée qui correspond a la clé publique
stockée sur le serveur (pour votre utilisateur, bien entendu). Il est
également possible d'utiliser plusieurs clés publique pour chaque  
utilisateur.

Bref, maintenant que nous avons la théorie, passons a la pratique : tout
d'abord, il nous faut générer un couple de clés publique/privée sur le
client. Openssh fait ça via la commande ```ssh-keygen -t rsa``` (le -t
rsa précise a ssh que nous voulons un chiffrement rsa, qui est
suffisamment solide pour cette utilisation.) Entrez les informations que
ssh-keygen vous demande. Trois fichiers devraient maintenant se trouver
dans votre dossier .ssh/ : id_rsa, id_rsa.pub, et known_hosts.  
known_hosts liste les serveurs auxquels vous vous êtes connectés déjà
une fois (pour éviter les attaques MITM, mais bref). Non, ce qui nous
intéresse ici c'est id_rsa et id_rsa.pub . id_rsa contient votre clé
privée, sauvegardez la sur une clé USB ou notez la sur un bout de
papier, si vous la perdez, vous ne pourrez plus vous connecter au
serveur. (planquez la clé usb/le bout de papier...) id_rsa.pub, quand a
lui, contient votre clé publique. Copiez la sur le serveur, avec un
```scp ~/.ssh/id_rsa.pub <username>@<votre nom de domaine>:~/``` , ou
en la copiant a la main, si ça vous amuse. 

Vous avez maintenant un fichier id_rsa.pub dans votre dossier personnel 
sur le serveur, il faut le mettre a un endroit ou openssh le reconnaitra.
Il est donc nécessaire de créer le dossier .ssh (```mkdir .ssh```), puis
de déplacer ce fichier a la bonne place (```mv ~/id_rsa.pub ~/.ssh/authorized_keys```).
Testez si ça fonctionne : ouvez un autre terminal, et  
connectez vous a votre serveur (```ssh <username>@<votre nom de
domaine>```), et il ne devrait pas vous demander de mot de passe.**Si
il vous en demande un, NE PASSEZ PAS A LA SUITE. Quelque chose a foiré,
donc vérifiez que vous avez suivi correctement les instruction
ci-dessus.**

Continuons. Il ne nous reste plus qu'a installer le serveur web, et a le
configurer: 

	sudo apt-get install \
	apache2 apache2.2-common apache2-doc apache2-mpm-prefork \
	apache2-utils libexpat1 ssl-cert libapache2-mod-php5 \
	php5 php5-common php5-gd php5-cgi libapache2-mod-fcgid \
	apache2-suexec php-pear php-auth php5-mcrypt mcrypt \
	php5-imagick imagemagick libapache2-mod-suphp libruby \
	libapache2-mod-ruby

(faisons large, on aura besoin de l'excédent plus tard...), puis activons les  
mods apache en faisant ```a2enmod suexec rewrite ssl actions include
dav_fs dav auth_digest```, et faisons en sorte que ces activations
soient prises en compte par apache via un ```sudo service apache2
restart```  

Le serveur fonctionne, maintenant, il est necessaire de lui expliquer
comment fonctionner sur notre nom de domaine et ou trouver les fichiers
a envoyer.  

Pour cela, nous allons faire un simple ```ln -s /etc/apache2/sites-{available,enabled}/default```, car apache est assez
sympa pour nous filer un fichier de configuration par défaut. Il nous
faut encore l'éditer, en changeant l'adresse mail au début du document
par la votre, et en changeant ``AllowOverride none`` en ``AllowOverride All``,
et enfin redémarrer apache pour qu'il prenne en compte les
modifications, par un ```sudo service apache2 restart```  

Et maintenant, il vous reste a apprendre le html, parce que ca y est,
votre serveur est fonctionnel! Voila voila. Dans la prochaine partie, on
verra l'installation du serveur mail (c'est suffisamment complexe pour
prendre un article seul...)
