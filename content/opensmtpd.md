Title: OpenSMTPd comme serveur mail sous debian 
Date: 2014-11-07 13:04
Author: Wxcafé
Category: Tutorial
Slug: opensmtpd-debian

J'avais dit il y a un certain temps que j'allais écrire un tutoriel expliquant
comment gérer ses mails soi-même.  Il se trouve que j'ai récemment décidé de
changer le serveur qui héberge (entre autres) ce blog, et que ce dernier héberge
aussi mes emails. J'ai donc totalement changé d'infrastructure quand a la
gestion de mon système de mails.

Ainsi, j'ai décidé de passer de Postfix a OpenSMTPd, changement que je voulais
effectuer depuis un certain temps.  [OpenSMTPd](https://opensmtpd.org) est un
projet originaire d'[OpenBSD](http://openbsd.org) qui a pour but de fournir un
serveur SMTP fiable, simple, rapide, et surtout sécurisé (les même buts que ceux
qu'a le projet OpenBSD, globalement).

Pour rappel, le système d'emails fonctionne d'une façon très simple : votre MUA
(Mail User Agent, ou client email) contacte le MTA (Mail Transport Agent, ou
serveur SMTP) de votre fournisseur email, qui contacte le MTA du fournisseur du
destinataire, qui lui même contacte le MDA (Mail Delivery Agent) qui délivre le
mail au destinataire.

Si vous avez bien suivi, vous pouvez voir que je n'ai pas parlé de récupération
ni de lecture des mails. C'est pour une raison simple, qui est que ces taches
sont remplies par d'autres services encore (IMAP/POP pour la récupération depuis
le serveur, des yeux pour la lecture).

Or ce qui nous intéresse ici, ce n'est pas simplement d'envoyer et de recevoir
des emails mais bien aussi de pouvoir les récupérer et les lire, et c'est pour
ça que ce tutoriel ne parlera pas que d'OpenSMTPd mais aussi de
[Dovecot](http://dovecot.org/) qui fait office de serveur IMAP et
[amavis](http://www.ijs.si/software/amavisd/)/[spamassassin](http://spamassassin.apache.org/) 
pour filtrer les mails entrants et sortants. 
Le schéma suivant explique la façon dont les mails sont gérés sur le système

                ╭────────────────╮                    ╭──────────╮
                │╭──────────────>│────> to filter ───>│─╮        │
      mail in   ││               │                    │ │ amavis │
    ───────────>│╯ OpenSMTPd  ╭──│<─── from filter<───│<╯        │
                │             │  │                    ╰──────────╯
      mail out  │             │  │                    ╭──────────╮
    <───────────│<────────────┴─>│─────> to MDA ─────>│─────────>│──> to user's
                │                │                    │ dovecot  │     mailbox
                ╰────────────────╯                    ╰──────────╯

Normalement, ceci devrait être a peu près clair.
Pour expliquer vite fait, les emails entrants (venant des utilisateurs mais
aussi d'autres correspondants) sont transmis a OpenSMTPd, qui envoie tout a
`amavis`, qui vérifie a la fois les spams et les malwares pour les mails
venants de l'exterieur, et qui signe avec DKIM pour les mails venants de
nos utilisateurs, puis qui rentransmet les mails filtrés/signés a OpenSMTPd,
qui a ce moment-ci trie en fonction de la destination : les mails gérés 
par le domaine vont via dovecot dans les boites mail des destinataires 
locaux, les mails exterieurs vont directement vers le MTA du serveur 
distant.



Voyons comment mettre cela en place. Tout d'abord, il faut décider de la façon
dont les différents services vont communiquer.

Déjà, amavis étant configuré par défaut pour écouter (en SMTP) sur le port
10024 et répondre sur le port 10025 quand il s'agit de filtrer et
écouter sur le port 10026 et répondre sur le port 10027 quand il s'agit de
signer, nous allons profiter de cette configuration et donc lui parler en SMTP
sur ces ports.

Quand a Dovecot, nous allons lui transmettre les emails en LMTP (Local Mail
Transfer Protocol), non pas sur un port mais via un socket (dans ce cas précis,
`/var/run/dovecot/lmtp`).

Ainsi, pour reprendre le schéma présenté plus haut :

                ╭───────────────╮                    ╭───────────╮
                │╭─────────────>│──> SMTP (10026) ──>│─╮         │
      SMTP in   ││              │                    │ │ amavis  │
    ────────> 25│╯ OpenSMTPd ╭──│<── SMTP (10027) <──│<╯ (sign)  │
                │            │  │                    ╰───────────╯
      SMTP out  │            │  │
    25 <────────│<───────────╯  │
                ╰───────────────╯

Pour les mails sortants; et

                ╭───────────────╮                    ╭────────────╮
                │╭─────────────>│──> SMTP (10024) ──>│─╮          │
      SMTP in   ││              │                    │ │ amavis   │
    ────────> 25│╯ OpenSMTPd ╭──│<── SMTP (10025) <──│<╯(filter)  │
                │            │  │                    ╰────────────╯
                │            │  │                    ╭────────────╮
                │            ╰─>│──> LMTP (socket) ─>│───────────>│──> to user's
                │               │                    │  dovecot   │     mailbox
                ╰───────────────╯                    ╰────────────╯

Pour les mails entrants.

Maintenant que la théorie est claire, mettons en place tout cela. Je me baserai
ici sur le fait que vous utilisiez une plateforme Debian ou OpenBSD. Pour
d'autres plateformes, la configuration devrait être sensiblement la même

(Vous aurez besoin de certificats SSL pour ce guide, même self-signés.
Si vous ne savez pas comment en créer, vous pouvez aller voir [ce
post](http://wxcafe.net/posts/05/30/14/SSL-ou-la-securite-sur-internet/))

Tout d'abord, commençons par installer les programmes nécessaires :

	sudo apt-get install opensmtpd dovecot dovecot-pigeonhole amavisd-new dovecot-managesieved
	sudo pkg_add dovecot dovecot-pigeonhole amavisd-new

Continuons en configurant OpenSMTPd tel que nous avons vu plus haut :

`/etc/smtpd.conf`

	# This is the smtpd server system-wide configuration file.
	# See smtpd.conf(5) for more information.
	
	## Certs
	pki exem.pl certificate "/etc/certs/exem.pl.crt"
	pki exem.pl key 		"/etc/certs/exem.pl.key"
	
	## Ports to listen on, and how to listen on them
	listen on eth0 port 25 tls pki exem.pl hostname exem.pl auth-optional
	listen on eth0 port 465 tls-require pki exem.pl hostname exem.pl auth mask-source
	listen on eth0 port 587 tls-require pki exem.pl hostname exem.pl auth mask-source
	
	## Aliases
	table aliases file:/etc/aliases
	
	# coming from amavisd, checked for spam/malware
	listen on lo port 10025 tag Filtered
	# coming from amavisd, signed with DKIM
	listen on lo port 10027 tag Signed
	
	## Receiving
	# if the (incoming) mail has been through amavisd, then we can deliver it
	accept tagged Filtered for any alias <aliases> deliver to lmtp "/var/run/dovecot/lmtp"
	# we directly tranfer incoming mail to amavisd to be checked 
	accept from any for domain "exem.pl" relay via "smtp://localhost:10024"
	# we have to put these lines in this order to avoid infinite loops
	
	## Sending
	# if the (outgoint) mail has been through amavisd, then we can deliver it
	accept tagged Signed for any relay
	# we tranfer the outgoing mail to amavisd to be signed
	accept for any relay via "smtp://localhost:10026"
	# same, we have to put these lines in this order or infinite loops...

Expliquons un peu ce fichier de configuration :

- Tout d'abord, le paragraphe nommé "Certs" contient les déclaration
  d'emplacement des certificats SSL.
- Ensuite, le paragraphe contenant les ports externes sur lesquels nous écoutons :
  port 25 avec TLS optionel et ports 465 et 587 avec TLS obligatoire
- Les alias sont définis juste après
- Le paragraphe suivant contient les ports locaux sur lesquels nous écoutons :
  10025 (port de sortie du filtre de amavis) dont on taggue les mails sortants
  comme "Filtered" et 10027 (port de sortie des mails signés par amavis) dont on
  taggue les mails sortants comme "Signed"
- Nous avons ensuite le paragraphe qui traite les mails rentrants. Si le mail
  traité est taggué comme Filtered, alors il a été vérifié par amavis, et on
  peut donc le transmettre au destinataire. Sinon, c'est qu'il n'a pas encore
  été vérifié par amavis, donc on lui transmet pour analyse (sur le port 10024
  donc). Il est important de mettre les déclarations dans ce sens, car la
  première règle qui matche l'état du paquet est appliquée. Ici, la deuxième
  ligne matchant tous les mails arrivant et la première seulement ceux filtrés,
  inverser leur sens voudrait dire que les mails seraient toujours renvoyés a
  amavis
- Enfin, le dernier paragraphe traite les mails sortants. De la même façon que
  pour le paragraphe précédent, si le mail sortant est déjà taggué comme Signed
  on le transmet au MTA du destinataire, sinon il n'a pas encore été signé par
  DKIM par amavis et on le transmet donc a amavis pour qu'il le signe. Le
  problème de l'ordre des lignes se pose encore, pour la même raison qu'au
  dessus.

Nous allons maintenant configurer dovecot. Comme nous l'avons vu, dovecot doit
écouter en LMTP via la socket `/var/run/dovecot/lmtp` et transmettre les
emails a la boite email de l'utilisateur. Il serait aussi interessant
qu'il nous permette de récuperer les mails. Pour cette configuration, on ne
mettra en place que du IMAPS. Cependant, si vous voulez mettre en place du
POP3[s], différents guides sont trouvables facilement sur internet.

`/etc/dovecot/dovecot.conf`

	## Dovecot configuration file
	
	# basic config
	info_log_path = /var/log/dovecot-info.log
	log_path = /var/log/dovecot.log
	log_timestamp = "%Y-%m-%d %H:%M:%S "
	mail_location = maildir:%h/mail
	
	# authentication
	passdb {
		driver = pam
	}
	userdb {
		driver = passwd
	}
	
	# the protocols we use
	protocols = imap lmtp sieve
	
	# ssl config
	ssl_cert = </etc/certs/exem.pl.cert
	ssl_key = </etc/certs/exem.pl.key
	ssl_cipher_list = HIGH+kEDH:HIGH+kEECDH:HIGH:!PSK:!SRP:!3DES:!aNULL
	ssl = yes
	
	## configuring services	
	# disables imap login without SSL (yes dovecot is dumb that way)
	service imap-login {
		inet_listener imap {
			port=0 
		}
	}
	
	service lmtp {
	  	unix_listener lmtp {
	    	mode = 0666
	  	}
	}
	
	## configuring protocols
	# the dovecot lda, we set it to use sieve
	protocol lda {
		mail_plugins = $mail_plugins sieve
	}
	
	protocol lmtp {
		postmaster_address =  whoever@exem.pl
	  	mail_plugins = $mail_plugins sieve
	}
	
	plugin {
		sieve = ~/.dovecot.sieve
		sieve_dir = ~/sieve
	}

**ATTENTION: Sous OpenBSD, remplacez**

	passdb {
		driver = pam
	}

**par**

	passdb {
		driver = bsdauth
	}

**pour identifier les utilisateurs système**

Ici aussi, voyons comment ce fichier est structuré :

- Tout d'abord, les configurations de base : ou iront les logs, comment formater
  leur datation, et l'endroit ou seront stockés les mails des utilisateurs.
- Nous configurons ensuite la gestion de l'authentification des utilisateurs.
  Ici nous identifions les utilisateurs avec le fichier /etc/passwd et leurs
  mots de passe avec PAM (ou BSDAuth)
- Nous configurons ensuite les protocoles que nous servons. Ici, nous voulons de
  l'IMAPS, du LMTP local et Sieve (qui sert pour trier les messages).
- Nous configurons le SSL
- Le section suivante contient la configuration des services. Nous avons en
  premier lieu le service IMAP, dont la configuration sert uniquement a
  désactiver IMAP. En effet, dovecot ne permet d'activer IMAPS qu'en activant
  IMAP avec. Comme nous ne voulons pas d'IMAP sans SSL, nous le désactivons.
  La configuration de lmtp sert a attribuer des permissions plus correctes au
  fifo qu'il utilise
- Nous configurons maintenant les protocoles, pour faire fonctionner Sieve
- enfin, nous configurons le plugin sieve en lui indiquant quel fichier et
  quel dossier utiliser pour sa configuration.

Enfin, il nous reste a configurer amavis. Comme expliqué, amavis va nous servir
a deux choses : signer les emails sortants, et filtrer les emails entrants. Il
doit donc écouter sur les port 10026 pour les signatures et 10024 pour le
filtrage, et répondre respectivement sur les ports 10027 et 10025 (le tout, en
SMTP. Comme toutes les transactions se font sur le loopback, il n'y a aucun
risque a utiliser des protocoles non chiffrés.
Pour OpenBSD, pensez a copier la configuration par défaut depuis
`/usr/local/share/examples/amavisd-new/amavisd.conf` et ajoutez les
modifications nécessaires a la fin du fichier.

`/etc/amavis/conf.d/99-local.conf` (debian)
`/etc/amavis.conf` (OpenBSD)

	use strict;
	
	$enable_dkim_verification = 1;
	$enable_dkim_signing = 1;
	dkim_key("exem.pl", "main", "/etc/certs/dkim.key" );
	
	@dkim_signature_options_bysender_maps = (
		{ '.' =>
			{ ttl => 21*24*3600, c => 'relaxed/simple' }
		}
	);

	$inet_socket_port = [10024, 10026];
	$policy_bank{'MYNETS'} = {
			originating => 1,
			os_fingerprint_method => undef,
	};
	
	$interface_policy{'10026'} = 'ORIGINATING';
	
	$policy_bank{'ORIGINATING'} = {
			originating => 1,
			allow_disclaimers => 1,
			virus_admin_maps => ["root\@$mydomain"],
			spam_admin_maps => ["root\@$mydomain"],
			warnbadhsender => 1,
			forward_method => 'smtp:localhost:10027',
			smtpd_discard_ehlo_keywords => ['8BITMIME'],
			bypass_banned_checks_maps => [1],
			terminate_dsn_on_notify_success => 0,
	};
	
	#------------ Do not modify anything below this line -------------
	1;  # ensure a defined return

A nouveau, expliquons ce fichier :
- le premier paragraphe définit que nous voulons qu'amavis signe les emails
  sortants, vérifie la signature DKIM des emails rentrants, et l'endroit ou se
  trouve la clé privée servant a signer les emails.
- le second définit les options DKIM que nous souhaitons utiliser comme défaut.
  Je vous invite a consulter la [RFC 4871](https://tools.ietf.org/html/rfc4871)
- nous définissons ensuite les ports sur lesquels nous allons écouter, puis les
  paramètres que nous utiliserons pour les emails venant de nos utilisateurs :
  ils seront traités comme "originating" et nous ne vérifierons pas l'OS duquel
  ils viennent.
- nous savons que les emails venants du port 10026 sont sortants, nous les
  traitons donc comme tel
- le paragraphe suivant décrit le traitement que nous faisons subir aux emails
  sortants : tout d'abord, nous réaffirmons qu'ils viennent bien de notre
  serveur. Nous autorisons les disclaimers (voire encore une fois la [RFC
  4871](https://tools.ietf.org/html/rfc4871). Nous déclarons l'adresse a
  prévenir en cas de spam/virus venants de notre système, et que nous voulons
  être prévenus. Nous déclarons ou envoyer les mails une fois signés et filtrés,
  puis qu'il est nécessaire de convertir les emails au format 7 bits avant de
  les envoyer au MTA, que nous autorisons tous les types et noms de fichiers, et
  les notifications de succès d'envoi. Et voila!

Vous avez pu remarquer qu'a aucun moment nous ne configurions ni la signature
des emails sortants ni le filtrage des emails entrants. Ces paramètres sont en
fait inclus par défaut dans amavis.

Il nous reste cependant quelques opérations a faire, encore.
Tout d'abord, il nous faut générer notre clé DKIM. Pour cela, il existe
différentes méthodes, j'ai personnellement utilisé opendkim ([un
tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-dkim-with-postfix-on-debian-wheezy))
mais de nombreuses autre méthodes existent.
Il nous reste encore a configurer spamassassin :

	#rewrite_header Subject *****SPAM*****
	# report_safe 1
	required_score 2.0
	# use_bayes 1
	# bayes_auto_learn 1
	# bayes_ignore_header X-Bogosity
	# bayes_ignore_header X-Spam-Flag
	# bayes_ignore_header X-Spam-Status
	ifplugin Mail::SpamAssassin::Plugin::Shortcircuit
	# shortcircuit USER_IN_WHITELIST       on
	# shortcircuit USER_IN_DEF_WHITELIST   on
	# shortcircuit USER_IN_ALL_SPAM_TO     on
	# shortcircuit SUBJECT_IN_WHITELIST    on
	# shortcircuit USER_IN_BLACKLIST       on
	# shortcircuit USER_IN_BLACKLIST_TO    on
	# shortcircuit SUBJECT_IN_BLACKLIST    on
	shortcircuit ALL_TRUSTED             off
	# shortcircuit BAYES_99                spam
	# shortcircuit BAYES_00                ham
	
	endif # Mail::SpamAssassin::Plugin::Shortcircuit

Comme vous pouvez le voir, les modifications se résument globalement a baisser
le required_score pour ma part.

Pour finir, activez les services nécessaires : opensmtpd, dovecot, amavisd, et
spamassassin, et tout devrait fonctionner parfaitement

Bon courage pour votre hosting de mail ensuite...

