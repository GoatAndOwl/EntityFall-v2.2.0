-------------------------------------------------
fichier listant les différentes mises à jour 
et patchs depuis le lancement de la version 1.0.0
-------------------------------------------------
Mise à Jour v2.1.0:
Bugs résolus:
- Pleins, pleins, pleins de bugs

Ajouts mineurs:
- Ajout de l’affichage des descriptifs de capacités (actifs) en jeu après un appui prolongé
- Ajout de l’affichage des descriptifs complets de capacités (actifs/passifs) dans l’interface de sélection
- Ajout d’une flèche indiquant le joueur actif au début de son tour
- Ajout d’une barre verticale indiquant le joueur actif
- Ajout d’une musique dans l’interface d’avant-partie
- Ajout d’une musique de combat
- Ajout du nom du personnage lors de l’affichage de ses effets

Modifications mineures:
- Traduction absolue en français (sauf pour les noms d’effets)
- Amélioration du sprite de case de sol
- Amélioration de l’affichage des stats de personnages
- Correction du nom français de plusieurs capacités
- Amélioration de la sélection de capacités en jeu; il n’est plus nécessaire de dé-sélectionner la précédente pour en choisir une nouvelle.
- Amélioration du look du nom du jeu en avant-partie

-------------------------------------------------

v2.0.0 (14/10/18):
Bugs résolus:
- Bug déplaçant toutes les images d’effets de case en un point lors d’un déplacement de caméra
- Bug activant automatiquement l’actif sélectionné si la dernière case sélectionnée est dans la portée de l’actif
- Bug d’affichage de l’effet du passif 6 du Viking
- Bugs sur différents actifs et effets du Mage Thermique
- Bug empêchant de lancer un actif en ayant un nombre de points de mouvement négatif

Ajouts majeurs:
- Ajout d'un nouveau mode, le MULTIJOUEUR EN LIGNE !!!
- Ajout d’une nouvelle interface revisitée, plus spacieuse et plus stylée
- Ajout d’une réelle perspective sur le terrain à 60º (2/3)

Ajouts mineurs:
- Ajout d’un système bloquant divers boutons après choix dans l’interface d’avant-partie
- Ajout des artworks d’actifs du Viking

Modifications mineures:
- Amélioration du sprite des cases bleues / rouges
- Amélioration du sprite de bouton de capacité (sa couleur en étant sélectionné varie en fonction de l’équipe du joueur actif)

Modifications du Mage Thermique:
Le mage thermique souffrait d’un Burst en dessous de la moyenne pour une classe ayant un rôle de dpt. La majorité de ses actifs ont gagnés en puissance:
- Actif 1[feu]: 8 -> 9 dégâts 
- Actif 2[glace]: 12 -> 13 dégâts
- Actif 2[feu]: 15 -> 18 dégâts / 5% -> 8% par effet « gelé »
- Actif 3[glace]: 6 -> 10 dégâts
- Actif 3[feu]: 12 -> 15 dégâts
- Actif 6[glace]: 5 -> 9 dégâts
- Actif 6[feu]: 8 -> 10 dégâts
- Actif 7[glace]: 3 -> 8 dégâts
- Actif 7[feu]: 15 -> 18 dégâts

- effet « enflammé »: -4% -> -5% de défense si le passif « Celsius Extrême » est équipé

-------------------------------------------------

v1.1.0 (10/08/18):
Bugs résolus:
- Bug créant le changement perpétuel entre deux orientations lorsque le joueur touchait une case diagonale à celui-ci;
- Bug sur l’actif 7 du Viking permettant de pousser l’attaquant sur le côté à l’infini s’il n’effectuait pas ses deux cases de déplacement;
- Bug qui plantait le jeu lorsqu’un joueur sans orientation recevait une attaque;

Ajouts majeurs:
- ajout d’un système permettant de déplacer la caméra sur le terrain
- Ajout de la map Void River
- Ajout de la classe Mage Thermique (voir fichier 'ThermalMage.md')
- Ajout d’un système d’affichage des effets d’une entité en la touchant rapidement 2 fois d’affilée

Ajouts mineurs:
- Ajout d’une animation du déplacement du Viking de face;

Modifications mineures:
- Amélioration du système de ligne de vue;
- Amélioration du système d’orientation;
- Amélioration de la qualité du sprite de sélection de case;
- Optimisation de la vitesse de navigation dans l’interface d’avant-partie

-------------------------------------------------

v1.0.1 (28/05/18):
Bugs résolus:
- bug permettant de créer une équipe de quatre joueurs alors qu’elle est limitée à trois joueurs
- bug permettant à deux joueurs de la même équipe de se placer sur la même case en début de partie
- Bug sur le facteur de dégâts en fonction de l’orientation (attaques de côté)

Ajouts:
- ajout d’un fichier retraçant les mises à jour et patchs du jeu (UpdateTrack.md)
- Ajout de l’affichage des passifs du joueur actif à droite des actifs
- Ajout de l’affichage des noms d’actifs et passifs de la classe sélectionnée sur l’interface de sélection de classe

Modifications mineures:
- apparence de la case de vide changée
- Le changement d’orientation peut dorénavant s’effectuer en sélectionnant n’importe quelle case sur le terrain si l’on n’utilise pas de capacité et si l’on ne se déplace pas. Le joueur actif se tournera alors automatiquement en direction de cette case.
- Dorénavant, le pseudo et l’orientation du joueur s’effacent lors de sa mort.

Modifications du Viking:
- actif 5: 12 -> 11 dégâts

-------------------------------------------------
v1.0.0 (25/05/2018):
lancement de la bêta fermée du jeu
