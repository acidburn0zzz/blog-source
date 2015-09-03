Title: La cryptographie avec PGP et principalement GnuPG 
Date: 2012-11-19 00:36
Author: Wxcafe
Category: Tutoriel 
Slug: la-cryptographie-avec-pgp-et-principalement-gnupg

PGP (pour [pretty good privacy][]) est un système de
chiffrement asymétrique (pour plus d'information sur le chiffrement
asymétrique, voir [ici][]) utilisant en général les algorithmes RSA
et/ou DSA, et pouvant servir a chiffrer tout fichier, mais aussi a
signer des emails. Le système de signature consiste a s'identifier en
tant que la personne que l'on est, en certifiant de son identité, et
repose sur un système dit de *Web of Trust*.  

Ce concept de Web of Trust est simple: si je valide le code vous
identifiant (votre clé), en certifiant que vous êtes qui vous êtes et
que je vous connais, et que d'autres personnes m'ont déjà
personnellement validé, les autres utilisateurs seront enclins a croire
que vous êtes en effet la personne que vous prétendez être. Bien
entendu, les utilisateurs validant trop de clés rapportées comme fausses
voient la valeur de leurs signatures baissée, et toutes les clés signées
par ces utilisateurs voient leur crédibilité baisser.  
Inversement, les "bons utilisateurs" voient la valeur de leurs
signatures augmentée, ce qui augmente la crédibilité des clés qu'ils ont
signées.

Ceci dit, un email peut être a la fois signé et chiffré, de façon a être
sûr, non seulement que l’expéditeur de l'email est bien celui qu'il dit
être, mais aussi que l'email n'a pas été modifié entre l'envoi et
la réception (en effet, avec un chiffrement de type RSA/DSA, une
modification du corps de l'email rend ce dernier illisible, la clé
publique ne  correspondant plus a la phrase de passe du message), ce qui
offre bien évidemment des avantages non négligeables dans un
environnement ou la protection des échanges est importante (soit a peu
près partout sur internet, si vous tenez a votre vie privée. Pensez a
[quitter Gmail][] aussi, par exemple).

Il est cependant a noter que les clés publiques sont généralement
situées sur un serveur de clés publiques, tel pgp.mit.edu ou encore
subkeys.pgp.net (certaines personnes préfèrent garder leur clés hors des
serveurs de clés publiques, craignant une compromission de ces serveurs.
Dans le cas d'utilisateurs normaux (c'est a dire n'échangeant pas de
secrets classés secret-défense par email), la protection offerte par les
serveurs de clé publiques est suffisante)

L'une des implémentations les plus connues et utilisées de PGP est sans
conteste GPG ([GNU Privacy Guard][]) , qui comme son nom l'indique fait
partie du projet GNU, et qui (`<troll>` de façon surprenante pour un
programme GNU`</troll>`) est extrêmement efficace et claire.

Après ces explications techniques, voici venue le
moment intéressant/utile, a savoir l'application. Le chiffrement et la
signature de mails doivent cependant attendre un petit peu, étant donné
qu'il vous faut d'abord créer votre clé et la placer sur un serveur de
clés publiques, de façon à ce que votre destinataire puisse vous
identifier lorsqu'il recevra le mail, mais aussi a configurer votre
client mail pour utiliser gpg (je baserai les explications de cet
article sur Thunderbird, mais des explications efficaces sont trouvables
facilement sur les interwebs).

Tout d'abord, générons une clé GPG :

	 gpg --gen-key 

GPG va vous demander les méthodes de chiffrement que vous voulez
utiliser, le plus sur est de laisser la valeur par défaut. La question
suivante est de savoir quelle taille votre clé doit faire, il est
préférable de choisir la taille la plus importante possible (4096). GPG
veut ensuite savoir quand votre clé doit expirer. La méthode simple est
bien évidemment de ne jamais la faire expirer, il est cependant plus
intéressant dans une logique de sécurité de régler cette durée a six
mois/un an. 

Des informations personnelles vous sont ensuite demandées,
concernant votre nom (mettez le vrai, tel qu'il apparaît sur votre carte
d'identité, si vous souhaitez utiliser votre véritable identité), votre
adresse mail (mettez la plus utilisée, vous pourrez en rajouter plus
tard), et un mot de passe pour la clé (utilisez un mot de passe
sécurisé!! Il est conseillé d'utiliser au moins 8 caractères, dont majuscules,
minuscules, caractères spéciaux et nombres (vous pouvez utiliser la
commande `makepasswd`, qui génère automatiquement un mot de
passe)  

GPG va maintenant prendre un peu de temps pour générer le couple clé
publique/clé privée, vous devriez profiter de ce temps pour effectuer
des opérations autres sur votre ordinateur : taper des textes, lancer
des films, écouter de la musique... De façon à augmenter les chances
d'obtenir un nombre bien aléatoire (le générateur d'aléatoire se base
sur la RAM pour obtenir des bits au hasard)  

Une fois cela fini, vous obtenez un couple clé publique/clé privée, que
vous ne pouvez pas visualiser entièrement pour l'instant. Il est
cependant possible (et recommandé) de les exporter pour les sauvegarder
via une commande:

	gpg --armor --export --output=pubkey.gpg 

pour la clé publique, et

	gpg --armor --export-secret-keys --output=seckey.gpg 

pour la clé privée. Il est possible et même souhaitable de copier ces
clés sur une clé USB, une carte SD, ou un autre support de stockage
résistant, de façon a avoir une solution de sauvegarde, au cas ou vous
perdiez ces clés sur ce PC.  

Cela fait, listons les informations sur votre clé publique :

	$ gpg --list-keys --fingerprint
	pub		4096R/27D81AC8 2012-11-17
		Key fingerprint = 6345 A91A FF89 97E0 13D0 96A9 9E2A 1917 27D8 1AC8
	uid				Clément Hertling (Wxcafe) 
	uid				[jpeg image of size 14692]
	sub		4096R/9ED7F77F 2012-11-17

La partie `pub` indique que c'est une clé publique, `4096R` indique que c'est 
une clé RSA sur 4096 bits.  La partie `27D81AC8` est 
l'identifiant de la clé publique, `Key fingerprint = 6345 A91A FF89 97E0 13D0 
96A9 9E2A 1917 27D8 1AC8` est appelé fingerprint de la clé. Les champs
`uid` sont des manières d'identifier la clé et la personne associée a
celle-ci, et enfin le champ `sub` est indicateur d'une subkey, système 
uniquement pris en charge par GPG et non inclus dans les premières 
versions de PGP, donc non-implémentées dans nombre de clients pgp.  
Passons maintenant a la mise en place de cette clé publique sur un
serveur de clés : nous utiliserons ici le serveur pgp.mit.edu.

	gpg --keyserver pgp.mit.edu --send-keys *ID de la clé a uploader* 

Maintenant que votre clé publique a été uploadée, vous pouvez l'utiliser
pour signer et chiffrer vos emails!  
Installons donc l'extension Enigmail pour Thunderbird, permettant de
chiffrer/signer vos emails de façon transparente. Il conviendra de
paramétrer cette extension, via le menu OpenPGP dans Thunderbird, puis
Setup Wizard (l'option entre Help et About OpenPGP). Normalement,
Enigmail détecte votre installation de gpg automatiquement, si cependant
ce n'était pas le cas, vous pouvez utiliser la clé exportée tout a
l'heure (pubkey.gpg) en l'important (import key from file).  

Selon les options que vous avez utilisées, vos emails seront
automatiquement signés et/ou chiffrés a l'envoi. Gardez cependant a
l'esprit que si tout le monde peut lire les mails signés, il n'en est
pas de même pour les mails chiffrés, pour lesquels il est nécessaire de
posséder la clé publique du correspondant en question, et de posséder
soi même une clé privée, donc d'utiliser OpenPGP aussi.  
Concernant les signatures de clés, elles fonctionnent de manière très
simple :  
Vous devez télécharger la clé de votre correspondant, via un

	 gpg --keyserver pgp.mit.edu --search-keys *ID de la clé de votre correspondant* 

(a noter que cette commande fonctionne aussi en cherchant une adresse
email ou un nom. Cependant, en cherchant via l'identifiant de la clé,
vous êtes sur de trouver votre correspondant. Globalement, l'email est
lui aussi assez sûr en terme de recherche de clés, tandis que le nom
donne rarement un résultat). L'étape suivante est de vérifier que votre
correspondant est bien la personne qui est spécifiée sur sa clé. Pour
cela, il convient d'avoir déjà vu physiquement cette personne et si
possible d'avoir vu une pièce d'identité lui appartenant, et d'avoir une
confirmation de cette personne que la clé que vous voyez lui appartient
bien.  
Ceci fait, vous pouvez signer la clé via un

	 gpg --sign *ID de la clé a signer* 

puis la renvoyer au serveur via

	 gpg --keyserver pgp.mit.edu --send-key *ID de la clé a signer* 

Voila, la clé de votre correspondant est signée!

Ce tutoriel sur PGP/GPG est terminé, et votre sécurité est améliorée
grâce a cette superbe invention qu'est la cryptographie!

  [pretty good privacy]: http://fr.wikipedia.org/wiki/Pretty_Good_Privacy
  [ici]: http://fr.wikipedia.org/wiki/Cryptographie_asym%C3%A9trique
  [quitter Gmail]: http://www.hauteresolution.net/pourquoi-je-vais-quitter-gmail/
  [GNU Privacy Guard]: http://fr.wikipedia.org/wiki/GNU_Privacy_Guard
