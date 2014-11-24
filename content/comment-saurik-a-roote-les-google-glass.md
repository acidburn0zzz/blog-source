Title: Comment Saurik a rooté les Google Glass
Date: 2013-05-06 06:24
Author: Wxcafe
Category: Hacking
Slug: comment-saurik-a-roote-les-google-glass

Comme vous avez pu le lire dans les médias, Saurik (Jay Freeman, connu
pour avoir développé Cydia, un "app store" alternatif pour les iTrucs),
après avoir reçu une paire de Google glass de la part de Google (de
façon assez évidente...), a trouvé intéressant d'obtenir un accès root
sur celles-ci, ce qu'il a accompli très rapidement. Des démentis de la
part de Google et de certains autres sites sont vite arrivés, disant que
les lunettes possédaient un bootloader débloqué et que de fait, le root
était facile a obtenir : il suffisait de débloquer le bootloader,
d'extraire l'OS, de le rooter hors-fonctionnement, puis de le
réinstaller, rooté, sur les lunettes.

Le fait est que de débloquer le bootloader laisse une trace permanente
sur les lunettes, et que Saurik n'a pas utilisé cette technique pour
rooter sa paire. Voyons comment il a fait :

_Je tiens tout d'abord a préciser que toutes les informations qui vont
suivre sont extraites de [cet article][], et plus précisément de la
partie "How does this exploit work".  Je tente d'apporter ma maigre
contribution a cette explication._

Donc, d'après les témoignages des quelques utilisateurs de Glass dans le
monde, il semblerait que ces dernières fonctionnent avec un système
d'exploitation Android, avec une nouvelle interface, mais avec les mêmes
outils internes: un kernel Linux, des outils userland GNU et une machine
virtuelle Java Dalvik pour les applications.

Saurik a donc cherché un exploit connu pour cette version d'android, et
l'a appliqué a son problème. L'exploit en question est relativement
simple. Depuis la version 4.0 d'android, le système permet la sauvegarde
des données des différentes applications, une a une, via ADB (Android
Debug Bridge, un protocole USB permettant l'accès a de nombreuses
fonctions avancées des machines fonctionnant sous android, dont, entre
autre, un shell, un accès au logs de debugging, etc... Cette
fonctionnalité est bien entendu désactivable.) Ce backup est très simple : 
il crée un fichier .tgz contenant le dossier de configuration de
l'application. Lors de la restauration, le système supprime la
configuration existante, puis la remplace par celle dans l'archive gzip.

Le problème de sécurité vient du fait que les applications android
voient leurs données stockées dans /data/data/identifiant/, et que
/data/ a pour permissions drwxrwx--x  27  system  system, ce qui
signifie que seul system et les membres du groupe system peuvent lire
dessus. Or, le fichier /data/local.prop définit de nombreux paramètres
au démarrage, et notamment un qui permet au système de déterminer s'il
fonctionne dans une VM ou sur un véritable appareil. S'il fonctionne sur
une machine virtuelle, il donne les droits root a tout utilisateur se
connectant via ADB, ce qui est ce que l'on cherche pour l'instant. Le
fait que /data/ appartienne a system veut dire que le programme de
restauration doit être setuid pour accéder aux données a l’intérieur qui
appartiennent a root (soit toutes les applications système d'android,
dont l'application paramètres, et, dans ce cas précis, l'application de
log système présente sur les google glass de test. Ainsi, nous avons un
processus tournant en tant que root, qui va écrire sur une partition qui
nous intéresse des données que nous possédons.

Cependant, un problème reste : le système de restauration d'Android
vérifie les données avant de restaurer, et ne restaure pas les symlinks,
ce qui nous empêche d'avoir accès directement a /data/local.prop, le
fichier qu'on cherche a modifier. Cela dit, il nous reste une
possiblité. Plaçons un dossier world-writable dans le fichier de backup,
et nous pourrons écrire dedans pendant quelques secondes, le temps que
la restauration se termine et que le système remette les permissions en
place. Ainsi, nous pouvons créer le fichier
/data/local/com.google.glass.logging/whatev/x, lien vers
/data/local.prop, et nous avons un toujours un processus tournant en
tant que root qui est en train d'écrire dans ce dossier.

Donc, nous allons lancer deux processus en même temps :  

- Le premier tentera en boucle de créer le symlink. Il sera consitué de
	la commande suivante, depuis un shell sur les lunettes :

		while ! ln -s /data/local.prop /data/data/com.google.glass.logging/whatev/x 2>/dev/null
		do :
		done

- Le deuxième sera le processus de restauration de notre exploit. Celui
	ci, pour une plus grande chance de réussite, devra être suffisamment
	lourd : au moins \~50Mo. Il devra contenir whatev/bigfile et whatev/x,
	pour qu'il crée whatev, prenne du temps a copier bigfile, puis écrive
	dans x après que le symlink soit effectif. La commande sera, depuis
	l'ordinateur host :

		adb restore exploit.ab

	Ces commandes vont fonctionner de concert pour nous donner un accès root :  
	- Le processus de restauration va créer le dossier whatev, qui sera
		world-readable. Il va commencer a copier le fichier bigfile.  
	- Le processus de symlink va créer le lien
		/data/data/com.google.glass.logging/whatev/x, pointant vers
		/data/local.prop, puis rendre l'âme proprement.  
	- Le processus de restauration, ayant enfin fini de copier
		whatev/bigfile, copiera les contenus que nous voulons dans whatev/x, qui
		est lié a /data/local.prop. Comme le processus est setuid root, il ne se
		rendra compte de rien, et écrira tout dans /data/local.prop.

And voilà! On a écrit ce que l'on veut dans /data/local.prop, ce qui
nous permet de faire croire a android qu'il tourne dans une machine
virtuelle (ce que l'on veut, c'est en fait "ro.kernel.qemu=1", qui
indique au noyau qu'il tourne dans qemu, un système de VM).

Il nous reste a rebooter, depuis l'ordinateur host :

	adb reboot

Puis nous remontons la partitions système en lecture/écriture (r/w),
depuis le host :

	adb shell "mount -o remount,rw /system"

Nous copions le binaire [su][] vers l'appareil :

	adb push su /system/xbin

Nous donnons les bonnes permissions a ce binaire, afin de pouvoir
l’exécuter plus tard :

	adb shell "chmod 6755 /system/xbin/su"

Ensuite, nous supprimons le fichier /data/local.prop, pour pouvoir
redémarrer normalement :

	adb shell "rm /data/local.prop"

Enfin, nous redemarrons a nouveau :

	adb reboot

Et voila, une paire de google glass rootée!

Il est bon de préciser que cette manipulation n'est possible que parce
que les lunettes tournent sous une ancienne version d'android, et que ce
bug a été fixé depuis.

Il serait aussi interessant de couvrir les problèmes de vie privée
qu'engendrent les Google Glass, et ce sera fait dans un autre billet.

A bientôt!

  [cet article]: http://www.saurik.com/id/16
  [su]: https://data.wxcafe.net/uploads/android/glass/su
