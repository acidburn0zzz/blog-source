Title: Docker et les ebooks sur Twitter
Date: 2015-02-28 14:11
Author: Wxcafe
Category: Note
Slug: docker-et-les-ebooks-sur-twitter

Vous avez peut être déjà entendu parler de [Docker](https://www.docker.com/). Si
ce n'est pas le cas, voila les bases : Docker est un système de containers. Les
containers sont une forme particulière de virtualisation, ou le kernel n'est pas
virtualisé, mais ou les processus du système hôte sont séparés de ceux des
systèmes invités. Cela est possible depuis longtemps sous FreeBSD avec les [Jails](https://www.freebsd.org/doc/en/books/handbook/jails.html),
mais n'est devenu possible sous linux que récemment grâce aux [cgroups](https://www.kernel.org/doc/Documentation/cgroups/cgroups.txt),
qui permettent justement de séparer des groupes de processus. Le principe de
Docker est donc d'avoir une machine hôte sur laquelle s'exécutent plusieurs
conteneurs Dockers, chacun séparé des autres et de l'hôte, mais utilisant tous
le même kernel. Cela pose quelques questions en terme de sécurités, puisque la
séparation est bien plus fine qu'avec de la virtualisation classique. En effet,
ici, en trouvant un exploit kernel, un attaquant aurait potentiellement la
capacité de remonter jusqu'à l'hôte, puisqu'il n'est pas vraiment séparé des
invités. 

Quoi qu'il en soit, Docker permet donc de virtualiser a moindre coût des
systèmes GNU/Linux. "Mais pourquoi utiliser Docker, dans ce cas", vous
demandez-vous peut être, "puisque Xen peut faire la même chose, et plus
(notamment, Xen est capable de virtualiser autre chose que GNU/Linux)?". Et bien
c'est très simple : Docker apporte la simplicité de déploiement d'applications.
Les conteneurs Dockers peuvent être décrit en un fichier, nommé Dockerfile, qui
permet de répliquer un conteneur en quelques minutes sur un autre hôte, en une
commande. Le [Docker Hub](https://hub.docker.com) permet aussi de récupérer
rapidement et facilement un grand nombre d'images déjà configurées. 

Maintenant que nous avons expliqué rapidement ce qu'était Docker, voyons le
rapport avec les ebooks et Twitter.

Les comptes dits "ebooks" (le nom vient a l'origine de [horse_ebooks](https://twitter.com/horse_ebooks),
voir [ici](https://en.wikipedia.org/wiki/Horse_ebooks) pourquoi) sont des bots
twitter utilisant des [Chaines de Markov](https://en.wikipedia.org/wiki/Markov_chain),
avec les tweets d'un utilisateur "source" comme corpus, pour produire des tweets
ressemblant a ceux de l'utilisateur source. Nous allons voir maintenant comment
en installer un.

C'est, comme disent certaines personnes, "fun".

Il existe de nombreuses librairies écrites pour créer ce genre de bots,
cependant dans ce cas nous nous concentrerons sur
[celle-ci](https://github.com/mispy/twitter_ebooks), qui est une lib ruby créée
par [@m1sp](https://twitter.com/m1sp), qui gère pour nous a la fois l'API
twitter et la génération des messages.

Cependant, cela n'explique toujours pas le lien avec Docker. Ce lien est très
simple : nous utilisons un container pour faire tourner les bots. Depuis la
version 3, la gem twitter_ebooks permet de faire tourner plusieurs bots dans une
seule instance. Cependant, il est toujours plus sûr d'isoler les bots, et les
containers dockers permettent de les déployer sur n'importe quelle machine
(celleux qui ont déjà tenté de mettre en place une application basée sur ruby
sauront le problème que cela pose habituellement). Pour ce faire, j'ai créé [un
repo github](https://github.com/wxcafe/ebooks_example) qui contient toutes les
pièces nécessaires pour mettre cela en place : le bot en lui même, les deux 
Dockerfiles, etc.

Le fonctionnement du bot est
simple : après avoir installé la gem twitter_ebooks, vous archivez le corpus de
l'utilisateur source avec `ebooks archive <username> <filename>` (c'est du json)
, puis vous convertissez le json en fichier utilisable par le bot : `ebooks
consume <filename>`. Cela fait, démarrer le bot revient a lancer le container :
`docker run -d <container name>` Pour plus d'informations, allez voir [la
documentation Docker](https://docs.docker.com/articles/basics/)

Bien entendu, dans l'idéal il faudrait mettre a jour les corpus de chaque
utilisateur régulièrement. Cela est très simple a mettre en place avec un simple
script cron : 

	00 00 * * *    /usr/local/bin/ebooks archive username /usr/local/ebooks/main/corpus/username.json >> /var/log/ebooks/update.log 2>&1
	00 05 * * *    cd /usr/local/ebooks/main/ && /usr/local/bin/ebooks consume corpus/username.json >> /var/log/ebooks/update.log 2>&1
	00 10 * * *    docker rm -f bots >/dev/null 2>&1
	00 15 * * *    docker rmi bots  > /dev/null 2>&1
	00 20 * * *    cd /usr/local/ebooks/main/ && docker build --rm -t bots . >> /var/log/ebooks/build.log 2>&1
	00 25 * * *    docker run -d --name bots bots >> /var/log/ebooks/run.log 2>&1

Les 5 minutes entre chaque commande sont laissées pour empécher que deux
commandes ne s'executent en même temps.

Et voila, vous avez un container Docker qui fait tourner une application en ruby
toute sale, et votre système hôte reste propre. Bien sûr, ce n'est qu'un exemple
des possibilités de Docker : par exemple, on peut aussi faire tourner [des
applications "usuelles"
dedans](https://blog.jessfraz.com/posts/docker-containers-on-the-desktop.html),
puisque l'overhead de Docker est minimal, et beaucoup d'autres applications
existent.
