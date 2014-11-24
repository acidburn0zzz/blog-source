Title: Les systèmes de fichiers
Date: 2012-09-25 10:28
Author: Wxcafe
Category: Teaching 
Slug: les-systemes-de-fichiers

Un système de fichiers. Vous en avez surement déjà entendu parlé si vous
avec déjà installé Linux, ou formaté une clé USB. Dans ces cas, vous
connaissez surement NTFS, EXT4, ou encore FAT32.

Ces différents noms désignent en effet des systèmes de fichiers. Mais
qu'est-ce qu'un système de fichiers?

Pour comprendre cela, il faut déjà savoir ce qu'est exactement un
fichier. Un fichier est un ensemble de blocs (les blocs sont l'unité la
plus petite traitable par le matériel, ils font généralement 1 ou 4 Kio
([kibioctet][]), en fonction du système de fichier utilisé.), qui est
donc composé de bits, interprétés différemment en fonction du type de
fichier. Cependant, seul, le fichier n'est pas accessible, puisqu'il
n'est pas indexé, c'est a dire que l'OS ne sait pas qu'il est présent,
ou il commence ni où il s'arrête (je schématise un peu, mais c'est
l'idée). 

Ainsi, le système de fichier donne un cadre et un standard à
l'arborescence des fichiers. Par exemple, le système de fichier ext4
utilise des blocs de 1 Kio, et de ce fait, toutes les partitions de
disque dur formatées en ext4 peuvent prendre comme unité de base 1 Kio
et mesurer la taille des fichiers en blocs de cette façon. Les systèmes
de fichiers nécessitent l'inclusion de drivers dans le noyau pour
pouvoir être pris en compte. 

Le noyau linux inclut par défaut les drivers pour ext2/3/4, btrfs, 
reiserfs, ntfs, fat16/32 et hfsx, ce qui permet de monter a peu 
près tout type de partition récente.

Il convient de bien faire la différence entre le système de fichier et
l'arborescence des fichiers. Si l'arborescence des fichiers est en fait
une entité virtuelle englobant la racine / et tous les fichiers et
dossiers contenus dedans, le système de fichier permet a votre système
GNU/Linux de distinguer les différents fichiers composants cette
arborescence.

Détaillons maintenant les types de fichiers les plus répandus:

- FAT16/32 : Les systèmes de fichier FAT (pour File Allocation Table,
	soit la définition d'un système de fichier), remplissent leur rôle le
	plus simplement possible. Ne permettant (historiquement) que des noms de
	8 caractères (plus extension de trois caractères), ni chiffrement, ni
	système de distinction d'utilisateurs (DOS étant un système
	mono-utilisateur), Il fut décliné par microsoft en FAT16 et en FAT32,
	utlisants respectivement des blocs de 16 et 32 Kio.

- NTFS :. Le NTFS (pour New Technology File System, rapport a Windows
	NT) est un système de fichier qui est apparu avec Windows XP, et qui
	était une mise a jour nécessaire du FAT32 vieillissant. NTFS ajoute a
	FAT différentes capacités dont le chiffrement, les liens symboliques, la
	compression et les quotas pour les volumes, permettant de limiter la
	taille maximum occupée dans une partition.

- ReFS : ReFS est le système de fichiers introduit dans Windows Server 2012.
	Ne différant pas énormément de NTFS, je le mentionne principalement 
	parce qu'il est prévu qu'il soit le défaut pour Windows 8. 
	Il apporte principalement la redondance, c'est a dire que chaque
	fichier possède une somme de contrôle en 64 bits stockée dans un fichier
	séparé pour éviter les corruption de disque.

- Ext2/3/4 : les systèmes ext (extended) sont les systèmes de fichiers
	les plus utilisés sous linux pour le grand public. (Je traiterai ici
	d'ext4, puisque c'est le plus récent.) Il dispose de toutes les
	fonctions que l'on peut attendre d'un système de fichiers moderne, ni
	plus ni moins. Ainsi, ext4 est un système de fichiers journalisé,
	acceptant les capacités jusqu’à 1 Exioctet, et utilise l'allocation dite
	"par extent", ce qui signifie que la création d'un fichier réserve
	automatiquement les zones contiguës de façon a réduire la fragmentation.

- ReiserFS : ce système de fichiers, créé par le (légèrement mégalo)
	programmeur Hans Reiser, est a retenir pour avoir été le premier système
	de fichiers journalisé, et accepte un nombre de fichiers de l'ordre des
	4 milliards. Le but de ce système est de créer un système polyvalent, a
	la fois système de fichiers et base de donnée (de part sa grande
	capacité en terme de nombre de fichiers et de l'utilisation d'un
	journal.)

- Btrfs : ce système est l'évolution logique d'ext4, et inclut lui aussi
	l'allocation par extent, mais possède de plus un système de
	sous-volumes, qui permet d’accéder a plusieurs arborescences de fichiers
	montées en même temps (système pratique et utile pour faire des
	snapshots de systèmes.). Il permet aussi de redimensionner a chaud la
	taille des partitions, en les agrandissant ou en les rétrécissant, est
	compatible avec [LVM][], a un système de checking intégré (btrfsck), et
	utilise un algorithme de compression appelé LZ4, qui accélère les accès
	aux fichiers compressés d'environ 30% par rapport a LZO, le système
	utilisé dans ext4.

- HFS+ : le système de fichier présent sur tous les macs a des capacités
	relativement standards, et ressemble énormément a l'ext3. Il supporte
	cependant les liens directs vers les dossiers, fonction rare sur les
	systèmes de fichiers actuels. Il est possible qu'il évolue a nouveau
	dans les années a venir

- ZFS : Ce système de fichier, venu de Solaris mais utilisable par Linux
	et \*BSD, est, tel Btrfs, a la fois un système de fichier et un
	remplaçant/compatible avec LVM, C'est un système de fichiers conçu
	principalement pour les serveurs, et il intègre ainsi un système de
	redondance des données pour éviter les corruptions, un mode RAID-Z
	(apparenté au RAID5), des checks d’intégrité en continu, des snapshots,
	etc...

Comme on a pu le voir, les systèmes de fichiers disponibles sont
légions. Cependant, le plus adapté a Linux et a une utilisation grand
public aujourd'hui est probablement Btrfs. Malheureusement, ce dernier
n'est pas aujourd'hui proposé par défaut sur les distributions les plus
utilisées, au profit de l'ext4, qui commence a accuser son âge...

Les systèmes de fichiers, s'ils peuvent ne pas sembler primordiaux au
fonctionnement du système, sont en fait de première importance, et ce
choix ne devrait pas être laissé au hasard, et être mis a jour
régulièrement (pour éviter les failles de sécurité...)

Bon courage, et bon choix pour votre prochain système.

  [kibioctet]: http://fr.wikipedia.org/wiki/Kibioctet#Multiples_normalis.C3.A9s
  [LVM]: http://fr.wikipedia.org/wiki/LVM
