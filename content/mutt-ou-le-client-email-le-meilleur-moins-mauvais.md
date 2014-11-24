Title: Mutt ou le client email le <del>meilleur</del> moins mauvais
Date: 2013-01-02 02:12
Author: Wxcafe
Category: Tutoriel
Slug: mutt-ou-le-client-email-le-meilleur-moins-mauvais

Les clients mails ont une particularité en commun : ils sont tous
<del>très</del> mauvais. Cela pour nombre de raisons, mais la principale reste
que leurs interfaces/raccourcis claviers ne sont pas efficaces pour une
utilisation __a la__ UNIX  
Cependant, un d'entre eux se démarque par sa moins-mauvais-itude, c'est
le relativement bien connu <del>Outlook Express 2003</del> Mutt!  
Mutt est un client mail en ligne de commande, qui, comme le dit sa page
d’accueil, ["just sucks less"][]. Dans les faits, mutt est assez
chiant a configurer mais particulièrement pratique a utiliser après.

La configuration de mutt se fait dans le fichier ```.muttrc``` ou dans
```/etc/Muttrc```, et il est courant d'utiliser offlineimap en
conjonction avec celui ci, de façon a accéder aux mails même sans accès
internet (mutt dispose d'un système d'accès IMAP/POP et SMTP, mais ne
crée pas de cache, ce qui empêche la consultation des emails sans
connexion internet.) La configuration d'offlineimap se fait dans
```~/.offlineimaprc``` ou dans rien d'autre en fait, c'est une config
par user. Offlineimap est un petit logiciel en python qui synchronise un
dossier en Maildir avec un serveur IMAP, ce qui tombe bien puisque
justement mutt accepte les dossiers au format Maildir. (De plus, cela va
tout a fait dans le sens de la libération des données en cela que vous
possédez vos mails en local.)  
Bref, passons aux choses serieuses : le code. Déjà, installez
offlineimap et [ce script][] fait par moi, qui vous permet d'installer
mutt avec le patch sidebar, qui crée un listing des dossiers sur la
partie gauche.  
Ensuite, voyons pour la partie configuration :  
Ma configuration d'offlineimap :

	## Config file for offlineimap
	## Originally located in ~/.offlineimaprc
	## This should not be edited without creating a copy before
	## Created by Wxcafe (Clément Hertling)
	## Published under CC-BY-SA

	[general]
	# List of accounts to be synced, separated by a comma.
	accounts = main

	[Account main]
	# Identifier for the local repository; e.g. the maildir to be synced via IMAP.
	localrepository = main-local
	# Identifier for the remote repository; i.e. the actual IMAP, usually non-local.
	remoterepository = main-remote
	# Status cache. Default is plain, which eventually becomes huge and slow.
	status_backend = sqlite				 # le type de cache. (plain ou sqlite)

	[Repository main-local]
	# Currently, offlineimap only supports maildir and IMAP for local repositories.
	type = Maildir						  # le type de stockage (Maildir ou IMAP)
	# Where should the mail be placed?
	localfolders = ~/Emails/				# le dossier dans lequel vous
											# voulez que vos emails apparaissent

	[Repository main-remote]
	# Remote repos can be IMAP or Gmail, the latter being a preconfigured IMAP.
	type = IMAP
	remotehost = //placeholderhost//		# le serveur de votre messagerie
	remoteuser = //placeholderusername//	# votre nom d'utilisateur
	remotepass = //placeholderpassword//	# votre mot de passe
	cert_fingerprint = //placeholdercert//  # le certificat du serveur (IMAPS only)

Ça devrait être assez simple a lire, j'ai tout bien commenté :3  
Puis ma config mutt :

	## Mutt MUA configuration file
	## This file should not be edited without creating a copy
	## File Created and edited by Wxcafe (Clément Hertling)
	## Published under CC-BY-SA

	# General config for reading (fetched via offlineimap) 

	set mbox_type = Maildir
	# type de boite mail (voir dans offlineimap, mailbox par defaut)

	set folder = ~/Email/
	# dossier root mailbox/imap 

	set spoolfile = +INBOX
	# dossier d'inbox

	set mbox = +'All Mail'
	# dossier ou archiver les emails

	set copy = yes
	# yes pour copier les messages dans les differents dossier, no pour...
	# enfin voila quoi.

	set header_cache = /.hcache/
	# dossier ou sont stockés les headers (pour le cache)

	set record = +Sent
	# dossier dans lequel sont stockés les messages envoyés

	set postponed = +Drafts
	# dossier dans lequel sont stockés les brouillons

	mailboxes = +INBOX +Drafts +Sent +Trash  +All\ Mail 
	# liste des dossiers qui vont apparaitre dans la colonne de gauche

	# General config for sending (using Mutt's native support)

	set smtp_pass = 'password_placeholder'
	# votre mot de passe

	set smtp_url = "smtp://username@whatev.org:465/"
	# l'url ou envoyer les emails

	set send_charset = "utf-8"
	# UTF8, NE PAS CHANGER

	set signature = ".sign"
	# vous pouvez mettre votre signature dans .sign

	set sig_on_top = yes
	# il est d'usge de mettre no ici. Cependant, je trouve ca plus lisible 
	# comme ca.

	set ssl_verify_host = no
	# mettez yes ici si votre serveur a un certificat configuré correctement

	set hostname = "wxcafe.net"
	# mettez l'adresse de votre serveur ici

	# Misc settings

	auto_view text/html
	# la façon de voir les emails par défaut.

	set date_format = "%y-%m-%d %T"
	# format de date d'envoi/de reception.

	set index_format = "%2C | %Z [%D] %-30.30F (%-4.4c) %s"
	# format de l'index (la présentation de l'interface)
	# voir http://www.mutt.org/doc/manual/manual-6.html#index_format 

	set sort_alias = alias
	set reverse_alias = yes 
	set alias_file = "$HOME/.mutt/aliases"
	# liste des alias noms/email. a créer et remplir vous même.
	# format : "alias short_name long_email_adress"
	source $alias_file

	set beep = no
	# ne pas biper. CE SON ME TUE T.T

	set tilde = yes
	set sleep_time = 0
	# ?

	set sidebar_visible = yes
	set sidebar_width = 15
	# parametres de la barre coté gauche

	set realname = "Clément Hertling (Wxcafé)"
	set from = "wxcafe@wxcafe.net"
	set use_from = yes
	set certificate_file = "$HOME/.mutt/cacert"
	# parametres d'envoi. mettez vos propres infos a la place des miennes...

	set edit_headers = yes
	# vous permet de vois les headers des mails. j'aime, donc je laisse.

	# Macros

	# le titre dit tout. index veut dire que la macro est active dans les menus,
	# pager qu'elle l'est dans la visionneuse, les deux qu'elle l'est dans les 
	# deux
	# \C represente la touche Control

	bind index,pager \Cp sidebar-prev
	# Control+p -> remonter d'un dossier dans la sidebar

	bind index,pager \Cn sidebar-next
	# Control+n -> descendre d'un dossier dans la sidebar

	bind index,pager \Co sidebar-open
	# Control+o -> ouvrir le dossier selectionné dans la sidebar

	macro index,pager d "=Trash" "Trash"
	# d supprime le message en cours

	bind pager   previous-line
	# permet de monter d'une ligne avec la touche up, au lieu de changer de message.

	bind pager   next-line
	# permet de descendre d'une ligne avec la touche down, au lieu de changer de 
	# message

	bind pager j next-line
	bind pager k previous-line
	# raccourcis vim

	# PGP signing commands

	set pgp_decode_command="gpg %?p?--passphrase-fd 0? --no-verbose --batch --output - %f"
	set pgp_verify_command="gpg --no-verbose --batch --output - --verify %s %f"
	set pgp_decrypt_command="gpg --passphrase-fd 0 --no-verbose --batch --output - %f"
	set pgp_sign_command="gpg --no-verbose --batch --output - --passphrase-fd 0 --armor --detach-sign --textmode %?a?-u %a? %f"
	set pgp_clearsign_command="gpg --no-verbose --batch --output - --passphrase-fd 0 --armor --textmode --clearsign %?a?-u %a? %f"
	set pgp_encrypt_only_command="pgpewrap gpg --batch --quiet --no-verbose --output - --encrypt --textmode --armor --always-trust --encrypt-to 0x******** -- -r %r -- %f"
	set pgp_encrypt_sign_command="pgpewrap gpg --passphrase-fd 0 --batch --quiet --no-verbose --textmode --output - --encrypt --sign %?a?-u %a? --armor --always-trust --encrypt-to 0x******** -- -r %r -- %f"
	set pgp_import_command="gpg --no-verbose --import -v %f"
	set pgp_export_command="gpg --no-verbose --export --armor %r"
	set pgp_verify_key_command="gpg --no-verbose --batch --fingerprint --check-sigs %r"
	set pgp_list_pubring_command="gpg --no-verbose --batch --with-colons --list-keys %r" 
	set pgp_list_secring_command="gpg --no-verbose --batch --with-colons --list-secret-keys %r" 
	set pgp_autosign=yes
	set pgp_sign_as=0x********
	# remplacez 0x******** par votre identifiant PGP!!!!!

	set pgp_replyencrypt=no
	set pgp_timeout=7200
	set pgp_good_sign="^gpg: Good signature from"

	# si vous ne comptez pas utiliser PGP, commentez toute cette section, depuis
	# PGP signing options 

	# Palette for use with the Linux console.  Black background.

	# Schéma de couleur Rouge et Noir. Commentez si vous voulez le 
	# défaut noir et blanc.
	# d'autres schémas sont trouvables sur google et autre.

	color hdrdefault red black
	color quoted brightblack black
	color signature brightblack black
	color attachment red black
	color message brightwhite black
	color error brightred black
	color indicator black red
	color status white black
	color tree white black
	color normal white black
	color markers red black
	color search white black
	color tilde brightmagenta black
	color index red black ~F
	color index red black "~N|~O"

Voila, pour plus d'informations vous pouvez aller voir le manuel de mutt
@ [http://www.mutt.org/doc/manual/][]  
J'espère que cette configuration "toute faite" vous aidera a commencer
a utiliser mutt. Il est tout de fois important de se souvenir
qu'utiliser une configuration toute faire n'aide pas a comprendre un
programme ou un système, et que cette façon de faire devrait être
réservée a l'introduction ou a des situations ou il est absolument
nécessaire d'avoir rapidement une configuration fonctionnelle (c'est a
dire, dans le cas d'un client email, euh... jamais?). Je vous invite
donc a relire les annotations dont sont parsemés les fichiers de
configuration en question, et surtout a lire le manuel, a chercher sur
<del>Bing</del> <del>Google</del> <del>Yahoo</del> Seeks, et globalement 
a tenter de comprendre les configurations en question et a les améliorer!

  ["just sucks less"]: http://www.mutt.org
  [ce script]: http://data.wxcafe.net/scripts/mutt-sidebar.sh
  [http://www.mutt.org/doc/manual/]: http://www.mutt.org/doc/manual/
