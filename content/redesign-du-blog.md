Date: 2013-06-12 19:14
Title: Redesign du blog, etc
Author: wxcafe
Category: Notes
Slug: redesign-du-blog

Comme vous avez pu le remarquer, ce blog a "un peu" changé récemment.

Du coup, expliquons. J'ai récemment monté [serverporn][], et ai par la même
occasion découvert [pelican][]. J'ai tout de suite accroché a ce générateur de
site statique en python, du fait de son efficacité, de sa facilité d'utilisation
et de sa grande customisation. En gros, pelican est un logiciel qui prend des
fichiers markdown ou reStructuredText, les passe a la moulinette d'un "thème"
constitué de templates pour les fichiers html et l'organisation du projet et
d'une partie "statique" contenant le css, et les autres fichiers nécessaires au
projet, et en fait des pages html.  

Globalement, un thème est constitué ainsi :

	thème
	├── static
	│	├─ css
	│	│  └─ [css files]
	│	├─ img
	│	│  └─ [image files]
	│	└─ js
	│	   └─ [javascript files]
	└── template
		├─ base.html
		├─ index.html
		├─ page.html
		├─ [...]
		└─ article.html

Sachant que les fichiers .html sont en réalité des fichiers suivant la syntaxe 
django, et utilisent des variables particulières telles `{{ article.content }}`,
par exemple. La syntaxe complète est très bien documentée dans la [doc][] de
pelican.

L'un des grands avantages de pelican est aussi la facilité qu'il offre quand a
la mise a jour du blog.  
En effet, il offre un système de Makefiles permettant, grâce a de nombreuses
cibles de compilation, de régénérer le site entier, de ne générer que les
fichiers modifiés depuis la dernière génération, de générer uniquement les
fichiers n'existant pas la dernière fois, etc...
La gestion du projet en devient donc très simple, puisque après avoir écrit un
article, il suffit de faire un `make html` pour mettre a jour le blog.

De plus, le système de wordpress commençait a ne plus me convenir, du fait du
manque de customisation, du fait que ça soit du PHP (beurk), etc. La, avec
pelican, je contrôle bien plus ce qui est mis sur le serveur (puisque c'est moi
qui ait modifié les templates et le css), c'est lisible (puisque c'est du
python, par opposition au PHP...), et c'est plus "efficace". Le markdown est
très pratique, je peux utiliser mon éditeur de texte de prédilection pour faire
les articles, je n'ai pas besoin d'un accès continu au net, bref, c'est plus
efficace.

En ce qui concerne les points négatifs : 

- Perte des commentaires: 
	Je vous propose de vous référer a l'article de Gordontesos [ici][] quand a 
	mon avis sur ce sujet.
 
- Perte du bouton flattr:
	Il va bientôt être remis, c'est juste un manque de temps de ma part, mais vu
	que toutes les pages passent par les mêmes templates, c'est assez facile a
	faire.

- Perte du spam:
	Pourquoi c'est dans les points négatifs, ca?

- Temps d'adaptation et d'appréhension du système:
	Oui, pendant encore un certain temps, il y aura des glitchs plus ou moins
	réguliers sur le blog, c'est parce que j'apprend a me servir de ce système
	et que j'apprend du css et du html. Ca arrive, ca passera, mais dans tous
	les cas ca me permet d'apprendre plein de choses, donc je mets plutôt ca
	dans la catëgorie positive.

Voila, c'est mon retour d'expérience sur pelican. A plus. 

[serverporn]: http://serverporn.fr
[pelican]: http://getpelican.com
[doc]: http://docs.getpelican.com/en/3.2/themes.html#templates-and-variables
[ici]: http://gordon.re/hacktivisme/la-necessite-des-commentaires.html
