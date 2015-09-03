Title: SSL ou la sécurité sur l'internet
Date: 2014-05-30 08:25
Author: Wxcafe
Category: Note
Slug: SSL-ou-la-securite-sur-internet

*Disclaimer: Ce billet est écrit après le visionnage de la conférence de Moxie 
Marlinspike suivante: [More Tricks for Defeating SSL](https://www.youtube.com/watch?v=ibF36Yyeehw),
présentée a la DefCon 17 (en 2011), et la lecture du billet suivant: 
[A Critique of Lavabit](http://www.thoughtcrime.org/blog/lavabit-critique/), 
ce qui peut avoir l'effet de rendre légèrement parano. Si vous considérez que 
c'est le cas ici, veuillez ne pas tenir compte de ce billet (et vous pouvez dès
a présent dire coucou aux différentes personnes qui écoutent votre connection)*

Si vous venez ici souvent (vous devriez), et que vous utilisez SSL pour vous
connecter a ce site (vous devriez, vraiment, dans ce cas), vous avez peut être
remarqué quelque chose récemment : il se trouve que le certificat qui permet de
desservir ce site a changé.

Cela fait suite aux évènements évoqués dans le *Disclaimer*, mais aussi a des
doigts sortis d'un endroit particulier du corps de l'admin/auteur de ce "blog",
qui a pris **enfin** les 5 minutes nécessaires a la compréhension superficielle
du fonctionnement de SSL, et les 10 nécessaires a la mise en place d'un système
fonctionnel utilisant cette compréhension récemment acquise.

Bref, le certificat a changé. Mais de quelle façon, vous demandez vous peut
être (ou pas, mais bon, je vais expliquer de toute façon). Et bien c'est très
simple : il existait auparavant un certificat pour `wxcafe.net`, un pour
`paste.wxcafe.net`, un pour `mail.wxcafe.net`, etc... Bref, un certificat
différent pour chaque sous-domaine.

Il s'avère que c'est a la fois très peu pratique a utiliser (les utilisateurs
doivent ajouter chaque certificat a leur navigateur séparément, chaque 
changement de sous-domaine conduit a un message d'erreur, etc) et pas plus
sécurisé que d'avoir un seul certificat wildcard. J'ai donc généré un certificat
pour `*.wxcafe.net` hier, et il sera dorénavant utilisé pour tous les
sous-domaine de `wxcafe.net`; et un certificat pour `wxcafe.net`, qui ne matche
pas `*.wxcafe.net`, et qui sera donc utilisé... bah pour `wxcafe.net`.

Il serait préférable de faire des redirections automatiques des adresses http
vers les adresses https, cependant, étant donné que le certificat est
self-signed, il me semble préférable que l'arrivée sur le site ne commence pas
par une page firefox disant "Something's Wrong!", et ces redirections ne seront
donc pas mises en place.

De plus, après la lecture de l'article de blog sur Lavabit dont le lien est plus
haut, il semble intéressant (et assez important) de faire en sorte que le
serveur utilise en priorité (et si possible, uniquement) des ciphers supportant
PFS, soit EDH et EECDH (Ephemeral Diffie-Helmann et la version Elliptic Curves 
de ce même algorithme). Cela permet de faire en sorte que toutes les 
communications avec ce serveur soient future-proof, c'est a dire que, même si 
quelqu'un récupérait la clé privée, elle ne serait pas utile pour déchiffrer les 
communications passées.

Bon, maintenant que les explications basiques sont faites, voyons
l'implémentation :   
Pour générer la clé, tout d'abord, il convient d'utiliser les commandes
suivantes:  

	::console
    sudo openssl genrsa -out example.key 4096
    # nous utilisons ici une clé de 4096 bits, la taille est laissée a votre appréciation
    sudo openssl req -new -key example.key -out example.csr
    # OpenSSL va ici vous demander de nombreuses informations, "Common Name" devant contenir le FQDN
    sudo openssl X509 -req -days 1095 -in example.csr -signkey example.key -out example.crt
    # enfin, nous générons la clé, d'une durée de vie de 3 ans

Bien entendu, si vous voulez utiliser une clé wildcard, il vous faut préciser
`*.example.com` comme common name.
Une fois la clé générée, il faut dire aux différents services de l'utiliser, et
de n'utiliser que des ciphers PFS. La méthode dépend donc du service.
Je vais lister ici les methodes pour quelques services que j'utilise :

###apache : 

	::apache
    # /etc/apache2/mods_enabled/ssl.conf
    # [...]
    SSLProtocol all -SSLv2 -SSLv3
    SSLHonorCipherOrder on
    SSLCipherSuite "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 \
      EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 \
      EECDH EDH+aRSA RC4 !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS"
    # [...]
    # /etc/apache2/sites-enabled/default-ssl
    # [...]
    SSLEngine on
    SSLCertificateFile /etc/certs/example.com.crt
    SSLCertificateKeyFile /etc/certs/example.com.key
    # [...]

###nginx :

	::nginx
    # /etc/nginx/nginx.conf 
    # [...]
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;
    ssl_ciphers "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 \
      EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 \
      EECDH EDH+aRSA RC4 !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS";
    # [...]
    # /etc/nginx/sites-enabled/default-ssl
    # [...]
    ssl on;
    ssl_certificate /etc/certs/example.com.crt
    ssl_certificate_key /etc/certs/example.com.key
    # [...]

###prosody (jabber) :

	::lua
    # tout d'abord, lancez la commande suivante :
    sudo openssl dhparam -out /etc/prosody/certs/dh-2048.pem 2048
    # ensuite, pour chaque VirtualHost dans /etc/prosody/prosody.conf :
    ssl = {
      dhparam = "/etc/prosody/certs/dh-2048.pem";
      key = "/etc/certs/example.com.key";
      certificate = "/etc/certs/example.com.crt";
    }
    # la cipher suite de prosody utilise par défaut EDH et EECDH

###postfix (email) :

	::shell
    # /etc/postfix/main.cf
    # [...]
    smtpd_tls_cert_file = /etc/certs/example.com.crt
    smtpd_tls_key_file = /etc/certs/example.com.key
    tls_preempt_cipherlist = yes
    smtpd_tls_eecdh_grade = strong
    smtdp_tls_mandatory_ciphers = high
    smtpd_tls_mandatory_exclude_ciphers = aNULL, eNULL, MD5, LOW, 3DES, EXP, PSK, SRP, DSS
    smtpd_tls_security_level = encrypt
    smtpd_tls_mandatory_protocols = !SSLv2, !SSLv3
    smtpd_use_tls = yes
    # [...]

###dovecot (imap) :

	::shell
    # /etc/dovecot/dovecot.conf 
    # [...]
    ssl_cert = </etc/certs/example.com.crt
    ssl_key = </etc/certs/example.com.key
    ssl_cipher_list = HIGH+kEDH:HIGH+kEECDH:HIGH:!PSK:!SRP:!3DES:!aNULL 

Voila. Pour d'autres protocoles/services, je vous invite a RTFM^W vous reporter
au manuel approprié.

Cela étant dit, je conseille a tout le monde d'aller voir la conférence dans le
disclaimer, et tant qu'a faire la conférence du même hacker [SSL and the future
of Authenticity](https://www.youtube.com/watch?v=8N4sb-SEpcg) qui parle de son
implémentation d'une technologie "remplaçant" le système de CAs qui existe
actuellement.

