Title: Mise en place d'un serveur DNS
Date: 2014-02-24 02:49
Author: Wxcafe
Category: Tutoriel
Slug: mise-en-place-dun-serveur-dns

Le DNS (Domain Name System) est le service permettant la résolution des noms de
domaines en différentes informations : adresses IPv4, adresses IPv6, certificats
DNSSEC ou IPsec, localisation géographique, ou encore texte. En général, le DNS
est utilisé pour résoudre des noms de domaines en adresses IP, et ainsi pour
simplifier la vie de tous les utilisateurs (je doute que tout le monde retienne
de se connecter a [http://173.194.45.66](http://173.194.45.66), ou a 
[http://199.16.156.70](http://199.16.156.70). Voire même a 
[http://5.39.76.46](http://5.39.76.46)).

Cependant, le DNS est un système qui date de 1984, et les exigences de l'époque
en termes d'expérience utilisateur n'étaient pas forcément aussi importantes que
de nos jours. La configuration des serveurs DNS peut ainsi être assez
contre intuitive.
Cela étant dit, comprendre le fonctionnement de DNS et contrôler ses
enregistrements est important.

Tout d'abord, une petite explication théorique. Le DNS fonctionne de la même
façon que le système de fichiers : en arborescence. Cependant, là ou la racine
du FS est `/`, celle de DNS est `.`, et là ou il convient d'écrire, par exemple,
`/usr/` et ou la progression se fait de gauche a droite pour le FS, pour DNS le
`.` n'est pas obligatoire et la progression se fait de droite a gauche. Par
exemple, le tld(top level domain, domaine de haut niveau) `com`, et le domaine
`google.com` appartient a `com`, on écrit donc `google.com` sans écrire le point
a la fin de façon courante.

Le reverse DNS est une variante du DNS "classique" permettant de résoudre les
adresses IP en nom de domaine. Ainsi, 5.39.46.76 a pour domaine wxcafe.net. 
Cependant, le reverse DNS n'a, par définition, pas de TLD sur lequel se diriger
quand on lui adresse une query. Les "adresses" que l'on query en reverse DNS
sont donc constituées de l'adresse IP, **_dans le sens contraire a l'ordre
habituel_**, et du faux domaine .in-addr.arpa
Par exemple, pour connaitre le reverse de 5.39.46.76, il faudra faire `dig PTR
76.46.39.5.in-addr.arpa`. La réponse sera, évidemment, `wxcafe.net`

Voyons maintenant comment mettre en place son propre serveur DNS. Tout d'abord,
quelques informations. DNS fonctionne sur le port 53 en UDP, et la commande
utilisée pour faire des tests DNS est `dig`. Le DNS fonctionne avec des
"enregistrements", records en anglais. Par exemple, un record A indique une
adresse IP, un record NS indique un Serveur de nom, etc. `dig` se base sur ces
records : par défaut, il ira chercher le(s) record(s) A correspondant(s) au nom
de domaine que vous donnez en argument, mais en précisant un autre type de
record, vous pouvez obtenir n'importe quelle information : par exemple, `dig NS
wxcafe.net` devrait vous renvoyer

	; <<>> DiG 9.8.4-rpz2+rl005.12-P1 <<>> NS wxcafe.net
	;; global options: +cmd
	;; Got answer:
	;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 13846
	;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 0
	
	;; QUESTION SECTION:
	;wxcafe.net.			IN	NS
	
	;; ANSWER SECTION:
	wxcafe.net.		3600	IN	NS	ns.wxcafe.net.
	wxcafe.net.		3600	IN	NS	ns.home.wxcafe.net.
	
	;; Query time: 60 msec
	;; SERVER: 10.0.42.1#53(10.0.42.1)
	;; WHEN: Tue Dec 10 13:31:18 2013
	;; MSG SIZE  rcvd: 67

Comme vous pouvez le voir, les serveurs DNS principaux pour 
[wxcafe.net](http://wxcafe.net) sont `ns.wxcafe.net` et `ns.home.wxcafe.net`,
qui sont respectivement des alias pour `wxcafe.net` et `home.wxcafe.net`. Ainsi,
chacun fait autorité pour lui même, et le problème évident est que le résolveur
ne peut résoudre la query si il est renvoyé encore et encore vers le même
serveur. Il convient donc de définir dans le même fichier de configuration
l'adresse de ces deux serveurs. Ainsi, le résolveur, au bout de son deuxième
loop, se rendra compte qu'il est en train de faire une boucle infinie et
demandera l'adresse au serveur auquel il est connecté. La première indication de
direction se fait grâce au serveur du TLD.

La configuration de bind est assez simple dans le principe, le plus complexe
étant en fait d'écrire les fichiers de zone.
La configuration de bind sous debian se fait dans le dossier /etc/bind/. Il
existe 4 fichiers de configuration principaux : `named.conf`,
`named.conf.default-zones`, `named.conf.local` et `named.conf.options`. 
`named.conf` contient les options par défaut de bind, `named.conf.default-zones`
les déclarations des zones par défaut (auxquelles il vaut mieux ne pas toucher),
`named.conf.local` contient les déclarations de vos zones, et
named.conf.options contient les options que vous rajoutez pour changer le
comportement de bind.

Pour commencer, il convient de préciser que nous allons parler ici du cas dans
lequel se trouve wxcafe.net: deux domaines dont nous voulons faire l'autorité,
deux serveurs DNS, et un service de résolution récursive limitée a quelques IPs
(notamment mon accès chez moi). 

Examinons tout d'abord les fichiers de configuration de named.
`named.conf.local` contient les définitions des zones forward et reverse. 
Sur wxcafe.net, les zones `wxcafe.net` et `76.46.39.5.in-addr.arpa` sont gérées
en master, et les zones `home.wxcafe.net` et `103.177.67.80.in-addr.arpa` sont
gérées en slave. Nous n'examinerons ici que les déclarations de zones sur ce
serveur, et pas sur home., car elles sont sensiblement les mêmes. La différence
principale étant que l'un héberge en slave les masters de l'autre.
Le fichier `named.conf.local` sur wxcafe.net contient donc 

    zone "wxcafe.net" {
        type master;
        file "/etc/bind/master/wxcafe.net";
        allow-transfer {
            80.67.177.103;
        };
    };

    zone "home.wxcafe.net" {
        type slave;
        file "/etc/bind/slave/home.wxcafe.net";
        masters {
            80.67.177.103;
        };
    };

    zone "46.76.39.5.in-addr.arpa" {
        type master;
        file "/etc/bind/master/46.76.39.5.in-addr.arpa";
        allow-transfer {
            80.67.177.103;
        };
    };

    zone "103.177.67.80.in-addr.arpa" {
        type slave;
        file "/etc/bind/slave/103.177.67.80.in-addr.arpa";
        masters {
            80.67.177.103;
        };
    };

Cela devrait être relativement clair. Globalement, les zones master ont un
fichier dans `/etc/bind/master/`, et les slaves un fichier dans
`/etc/bind/slave/`, les masters autorisent le transfert vers home.wxcafe.net
tandis que les slaves déclarent home.wxcafe.net comme master, et le reste est
assez parlant.

Voyons maintenant le fichier de zone concernant wxcafe.net, soit
`/etc/bind/master/wxcafe.net` : 
    
    $TTL 3600    ; 1 hour
    @               IN SOA ns.wxcafe.net. wxcafe.wxcafe.net. (
                            2014011001  ; serial
                            3h          ; refresh  
                            1h          ; retry
                            168h        ; expire
                            300         ; negative response ttl
                            )
    
    ; Name servers
                    IN  NS      ns.wxcafe.net.
                    IN  NS      ns.home.wxcafe.net.
    
    ; Mail exchangers
                    IN  MX  10  wxcafe.net.
                    IN  SPF "v=spf1 ip4:5.39.76.46 a -all"
    
    ; Main A/AAAA records
                    IN  A       5.39.76.46
    ns              IN  A       5.39.76.46
    
    ; Aliases
    data            IN  CNAME   wxcafe.net.
    ;        [...]
    www             IN  CNAME   wxcafe.net.
    
    
    ; home.wxcafe.net. definition
    $ORIGIN home.wxcafe.net.
    @               IN  NS      ns.home.wxcafe.net.
                    IN  NS      ns.wxcafe.net.
    ns              IN  A       80.67.177.103
                    IN  A       80.67.177.103



Alors. Expliquons ligne par ligne.  
Tout d'abord, le TTL (time to live) est un paramètre définissant le temps
pendant lequel les serveurs récursif (qui font un cache des données) doivent
cacher ce fichier de zone.   
Le @ est un raccourci pour exprimer le nom de domaine courant. Ici, donc,
wxcafe.net.   
Maintenant, nous arrivons a un record important : SOA (Start of Authority). 
Ce record prend de nombreux arguments, dans l'ordre :  
    - Le nameserver autoritaire pour le nom de domaine en question,  
    - L'adresse email du responsable de cette zone, avec le premier point
      remplacé par un @,   

puis entre parenthèses :  
    - Le numéro de série ("version" du fichier de zone, ici au format
      YYYYMMDDNN)   
    - La période de refresh, période entre chaque mise a jour du nameserver
      authoritaire secondaire,   
    - La période de retry, le temps entre chaque essai de mise a jour si le
      nameserveur authoritaire primaire est indisponible,   
    - La période d'expire, le temps qu'attendra le serveur autoritaire
      secondaire avant de supprimer les informations de son cache si le primaire
      reste indisponible, et enfin   
    - La période de TTL négatif, le temps qu'attendra le serveur secondaire
      avant de ne plus offrir les informations de cette zone si le serveur
      primaire est injoignable.   

Bon, tout ceci est peut-être un peu confus, mais ce n'est pas le record le plus
important a lire (pour les humains en tout cas). Continuons :   

NS (nameserver) permet de désigner les différents nameservers faisant autorité
pour ce domaine.  

MX permet d'indiquer ou il convient d'envoyer les emails pour ce domaine. 
SPF est un record d'authentification pour les emails.
Les records A désignent l'association entre un nom de domaine et une adresse
IPv4. Les records AAAA font de même pour les IPv6, mais malheureusement ce site
n'est pas encore en IPv6.

Les CNAME (canonical name) sont en quelque sorte des alias, ils permettent de
mettre en place des domaines exactement semblables a d'autre (ce qui permet par
exemple de filtrer ensuite avec les Virtual Hosts d'Apache, pour le web)

Enfin, la partie qui suit commence avec une déclaration $ORIGIN, ce qui permet
de changer la valeur du @ et des noms de domaine non complets (qui ne se
terminent pas avec un .). Ainsi, la partie suivant définit les nameservers et
l'adresse IP principale de home.wxcafe.net et de ns.home.wxcafe.net. Comme on
l'a vu, étant donné que ce nom de domaine est géré par un autre serveur DNS,
cela permet de rediriger les requêtes nous parvenant et demandant un domaine se
trouvant sous home.wxcafe.net.

Les autres fichiers de zone sont sensiblement similaires, avec les quelques
différences n'étant en fin de compte que des différences de valeurs (dues au
fait que, eh bah, c'est pas les mêmes domaines...).

Voila donc une courte explication de ce qu'est le DNS. Bien entendu, tout n'est
pas expliqué ici, je ne suis passé que sur ce qui est en place au niveau de
wxcafe.net, et encore, rapidement. Si vous voulez en savoir plus, vous pouvez
aller vous renseigner directement a la source : le [RFC
1034](https://www.ietf.org/rfc/rfc1034.txt) et le 
[RFC 1035](https://www.ietf.org/rfc/rfc1035.txt). Dans un autre style (bien plus
avancé) le blog de [Stéphane Bortzmeyer](http://bortzmeyer.org) est interessant
aussi.

