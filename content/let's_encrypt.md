Title: Let's Encrypt, enfin
Date: 2015-12-13T18:48+0100
Author: Wxcafé
Category: Tutoriel
Slug: lets-encrypt-enfin

Vous avez peut être vu que ce blog, entre autres sites que j'administre, n'est
disponible depuis quelques jours qu'en HTTPS, et avec un certificat valide. Bon,
si vous êtes là, vous avez déjà entendu parler de Let's Encrypt, mais pour les
deux trois du fond on va résumer:

LE est une nouvelle autorité de certification (ceux qui valident les certificats
SSL), basée sur une organisation, et dont le but est de fournir des certificats
valides, automatiquement et gratuitement. Leur certificat racine est signé par
IdenTrust, et est donc considéré valide par tous les navigateurs modernes.

Bon, maintenant qu'on est tous au même point, voyons comment ça marche. Depuis
dix jours LE est ouvert en bêta publique, donc il n'est plus nécessaire de
préciser les domaines pour lesquels on veut un certificat sur un formulaire,
comme c'était le cas pendant la période de bêta fermée. Le système qui est
utilisé repose sur le protocole ACME (Automatic Certificate Management
Environment), qui automatise complètement la signature des certificats. Du coup,
les certificats que délivre LE ne sont valides que 90 jours, ce qui serait super
chiant avec une autorité de certification classique, mais qui la veut simplement
dire qu'il faut mettre un cron en place.

Bref, comment mettre en place vos certificats? On va faire ça sans trop modifier
vos sites, et en automatisant au maximum. LE utilise, dans son système par
défaut, un fichier sur le site web, dont le serveur de certification vérifie
l'existence lors de la requête (si le fichier est présent avec le bon contenu,
c'est que le client tourne bien sur ce domaine, et donc que la personne qui
a demandé le certificat contrôle bien le domaine). Ce fichier est situé dans un
dossier dans la racine, `.well-known`. Plutôt que de se faire chier a gérer ce
dossier pour tous nos vhosts nginx, on va simplement créer un alias vers un
dossier commun sur le système de fichier, que tous les vhosts partagerons, et
qui permettra aussi de valider tous les domaines pour lesquels on veut un
certificat à la fois (avec un AltName) (sur un seul serveur, par contre. Enfin
si vous voulez vraiment vous pouvez faire des mounts cross-serveurs (avec du
sshfs ou des trucs du genre), mais c'est un peu sale quand même. Et faudra quand
même distribuer le certificat après, donc bon...).

Donc, on va rajouter ça dans nos blocs `server` :

```shell
location /.well-known {
	alias /srv/letsencrypt/.well-known;
}
```

(bien sûr il faut créer le dossier, hein.)  
Après, on `git clone https://github.com/letsencrypt/letsencrypt`, dans `/opt/` ou
dans `/usr/local/`, peu importe, on le clone quelque part, et on cd dans le
dossier en question. Une fois là, on demande un certificat :

```shell
sudo ./letsencrypt-auto certonly \
	-a webroot \
	--webroot-path /srv/letsencrypt/ \
	-d <domaine> \
	-d <altName1> \
	-d <altName2> \
	--server https://acme-v01.api.letsencrypt.org/directory
```

Normalement, maintenant, on a un certificat valide dans
`/etc/letsencrypt/live/<domaine>/`. Reste à configurer nginx pour qu'il serve
nos sites en https en utilisant notre nouveau certificat. Perso, j'utilise une
template qui ressemble à ça :

```shell
server {
	listen 80;
	listen [::]:80;
	server_name SERVERNAME;
	return 302 https://$server_name$request_uri;
}

server {
	listen 443 ssl;
	listen [::]:443 ssl;
	ssl_certificate /etc/letsencrypt/live/DOMAIN/fullchain.pem;
	ssl_certificate_key /etc/letsencrypt/live/DOMAIN/privkey.pem;
	ssl_dhparam /etc/nginx/dhparams.4096;
	ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
	ssl_ciphers "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 EECDH EDH+aRSA !RC4 !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS";
	ssl_prefer_server_ciphers on;
	add_header Strict-Transport-Security "max-age=15552000; includeSubDomains; preload";

	root SERVERROOT;

	index index.html index.htm;

	server_name SERVERNAME;

	server_tokens off;
	client_max_body_size 5m;

	access_log /var/log/nginx/access.log;
	error_log /var/log/nginx/error.log;

	location /.well-known {
		alias /srv/letsencrypt/.well-known;
	}

	location / {
		try_files $uri $uri/ =404;
	}
}
```

Alors c'est pas /tout à fait ça/ d'un point de vue parano du TLS (genre je
devrais désactiver TLS 1.0 et EECDH+aRSA+RC4, notamment) mais ça marche pas trop
mal et c'est plus compatible comme ça (mon telephone est sous Android 4.4, donc
je suis content d'avoir encore TLS 1.0 par exemple).

Vous pouvez ajouter votre domaine à la liste préloadée dans Chrome/ium, Firefox,
IE, Edge, Safari, le Tor Browser Bundle, etc...
[ici](https://hstspreload.appspot.com/) (oui ça fait clairement site de
phishing, mais apparemment c'est serieux...)

Enfin, il nous faut un renouvellement automatique, puisque notre certificat ne
sera valide que 90 jours. On va utiliser un cron tout con, avec un script :

```shell
00 01 */14 * * /usr/local/bin/cert-renew 2>&1 | mail -s "certificates renewal report" <votre email>
```

(oubliez pas que ça doit aller dans le crontab du root)
Et le script qui va bien :

```shell
#!/bin/bash

if [[ $UID != 0 ]]; then
	echo "please run as root"
	exit 1
fi

cd /opt/letsencrypt/

git pull 2>&1 >> /dev/null


# Renewing the cert
./letsencrypt-auto certonly \
	-a webroot --webroot-path /srv/letsencrypt \
	-d <domaine> \
	-d <altName1> \
	-d <altName2> \
	--server https://acme-v01.api.letsencrypt.org/directory \
	--renew \
	2>&1

systemctl restart nginx
exit 0
```

Notez bien le `--renew` qui spécifie qu'on renouvelle le certificat, le `git pull`
qui met à jour le client, et le `systemctl restart nginx` qui prend en compte le
nouveau certificat automatiquement

Et puis voilà, normalement avec ça vous devriez pouvoir chopper des certificats
valides. C'est plutôt cool, en pratique.

Merci Let's Encrypt
