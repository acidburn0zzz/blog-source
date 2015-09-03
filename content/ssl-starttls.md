Title: SSL - STARTTLS
Date: 2015-05-16 02:00
Author: Wxcafe
Category: Note
Slug: ssl-starttls

Le chiffrement SSL pour les services en ligne est un problème relativement
récent, par rapport a l'histoire d'Internet. Sa mise en place pose 
problème : les protocoles existants ne s'accommodent qu'assez mal de recevoir
soudainement un flot de données chiffrées, mais développer de nouveaux
protocoles est complexe et n'apporte rien d'intéressant. Pour palier a ce
problème, deux solutions sont apparues.

Le première consiste à faire écouter les services sur un
autre port, dans un tunnel SSL. De cette façon, le service existant écoute
normalement, mais il ne répond pas directement aux requêtes. A la place, un
tunnel SSL est mis en place, et les requêtes et les réponses passent dans le 
tunnel (ou elles apparaissent donc chiffrées pour l'extérieur). Cela permet de
proposer un service chiffré en modifiant de façon minimale le programme, au prix
de devoir aussi changer tous les clients, et de devoir les orienter sur un autre
port.

L'autre approche qui a été utilisée est une approche d'*upgrade*. La
communication commence en mode non chiffré, puis le client demande l'upgrade de
la connexion vers le mode chiffré s'il le supporte, les deux machines
machines font un *handshake* SSL et la communication continue a travers le
tunnel SSL. Le service peut continuer a écouter sur son port habituel, et seuls
les clients capables de passer en SSL le feront, ce qui permet de faire la "mise
a jour" en douceur.

Il est souvent demandé quelle est la meilleure méthode pour mettre en place un
service -- laisser un port pour le SSL et un pour le trafic non chiffré, ou bien
un seul, avec `STARTTLS`, qui *upgrade* les connexions si nécessaire.  
La réponse est que `STARTTLS` est plus interessant, pour plusieurs raisons. Tout
d'abord, il permet de n'utiliser qu'un seul port : ça permet de simplifier la
configuration du firewall. En plus de ça, il permet aux clients "anciens" (ceux
qui ne supportent pas SSL, donc ceux qui devraient être changés) de toujours se
connecter, même si cela signifie que leurs informations seront transmises en
clair. Surtout, il permet d'éviter aux utilisateurs d'avoir a configurer leurs
clients. Si le client supporte le chiffrement, il l'activera de lui même s'il
voit qu'il est disponible.  
Bref, mettez en place du `STARTTLS`, et pas du SSL. C'est mieux pour la sécurité
de tout le monde.
