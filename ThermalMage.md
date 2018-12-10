-------------------------------------------------
--------- Mage Thermique: présentation ----------
-------------------------------------------------
Le Mage Thermique est une classe possédant 2 états: feu et glace.
À l'exception de l'actif 4, 9 et 10, les capacités actives changent en fonction de l'état du Mage Thermique.
Exemple: l'actif 1 du Mage Thermique lance un Javelot Gelé si celui-ci est dans l´état "glace" ou une Projection 
Ardente si celui-ci est dans l'état "feu".

Avertissement: pour des raisons de taille de bouton et de noms de capacités trop longs (actif feu + actif glace), 
nous ne sommes pas en mesure de rentrer le nom COMPLET des actifs dans l'interface de sélection de classe. Les 
noms présentés seront donc des raccourcis pas tout à fait justes en termes de traduction. Ce problème sera résolu 
dès la prochaine mise à jour qui apportera une interface revisité, plus ergonomique, spacieuse et stylée.

-------------------------------------------------
-------------------- Actifs ---------------------
-------------------------------------------------
Actif 1) Javelot Gelé // boule de feu (2PE//3PE): 
-- le Javelot Gelé est une attaque à distance monocible d'une portée de 1 à 6 cases infligeant 6 points de dégâts 
et appliquant l'effet 'gelé' x1. Si le passif 4(Réactions en Chaîne) est équipé, le Javelot gelé peut aussi être 
lancé sur une case avec l'effet 'Geyser de Lave'. si c'est le cas, l'effet 'Geyser de Lave' est supprimé et 
l'effet 'Tapis de Braises' sur toutes les cases aux alentours sur une grande zone.

-- la Projection Ardente est une attaque à distance en petite zone d'une portée de 2 à 5 cases infligeant 8 points
de dégâts et appliquant l'effet 'enflammé' x1.



Actif 2) Stalactite // Rayon Incandescant (5PE//6PE):
-- le Stalactite est une attaque à distance en grande zone d'une portée de 2 à 4 cases infligeant 12 points de 
dégâts et appliquant l'effet 'gelé' x1.

-- le Rayon Incandescant est une attaque sur toute une ligne infligeant 15 points de dégâts et appliquant l'effet 
'enflammé' x1. les dégâts infligés sont 5% plus importants pour chaque effet 'gelé' sur la/les cibles touchées. 
Les effets 'gelé' des cibles touchées sont consommés.



Actif 3) Onde Glaciale // Cône de flammes (4PE//6PE):
-- l'Onde Glaciale est une attaque linéaire à distance en petit cône d'une portée de 3 à 5 cases infligeant 6 
points de dégâts et appliquant l'effet 'gelé': x3 au départ du cône et 2x sur le reste du cône. 1 utilisation par 
tour.

-- le Cône de flammes est une attaque linéaire à distance en grand cône d'une portée de 1 à 2 cases infligeant 12 
points de dégâts et appliquant l'effet 'enflammé': x3 au départ du cône et 2x sur le reste du cône.



Actif 4) Miroir Thermique (1PE):
-- le Miroir Thermique change l'état du Mage Thermique de l'état 'glace' à l'état 'feu' et vice-versa.



Actif 5) Bloc de Glace // Geyser de Lave (2PE//1PE):
-- le Bloc de Glace est l'invocation d'un Bloc de Glace sur une portée de 1 à 4 cases. 1 utilisation par tour ou 2 
utilisations par tour si le Passif 4(Réactions en Chaîne) est équipé. Le Bloc de Glace est une entité passive et 
immobile possédant 10 points de vie. 1 utilisation par tour ou 2 utilisations par tour si le passif 4(Réactions en 
chaîne) est équipé. 3 Blocs de Glace Maximum (par Mage Thermique sur le terrain). si le passif 4(Réactions en 
Chaîne) est équipé et qu'un Bloc de Glace se trouve sur une case avec l'effet 'Geyser de Lave': le Bloc de Glace 
et l'effet 'Geyser de Lave' sont supprimés; l'effet 'Tapis de Braises' est appliqué à toutes les cases aux 
alentours sur une grande zone; les entités dans la zone subissent 4 points de dégâts; les entités alignées avec la 
case ou se trouvait le Bloc de Glace sont poussés d'une case vers l'extérieur.

-- le Geyser de Lave est l'application de l'effet 'Geyser de Lave' à une case ciblée sur une portée de 2 à 4 
cases. le Geyser de Lave est un effet infligeant 4 points de dégâts à toute entité se déplaçant ou commençant son 
tour sur la case ciblée. cet effet dure 3 tours et ne peut être appliqué sur une case possédant l'effet 'Couche de 
Neige'. 2 'Geyser de Lave' Maximum (par Mage Thermique sur le Terrain). 2 utilisations par tour.



Actif 6) Bourrasque // Météorite (3PE//4PE):
-- la Bourrasque de Blizzard est une attaque linéaire à distance sur une petite ligne(zone) d'une portée de 2 à 4 
cases infligeant 5 points de dégâts, appliquant l'effet 'gelé' x1 et poussant les cibles touchées de 1 case vers 
l'extérieur.

-- la Météorite est une attaque à distance en petite zone sans LdV(Ligne de Vue) d'une portée de 3 à 4 cases 
infligeant 8 points de dégats et poussant les cibles touchées du centre de la zone vers l'extérieur. Si le passif 
4(Réactions en Chaîne) est équipé: si un Bloc de Glace se trouve au centre de la zone, la Météorite infligera 11 
points de dégats aux cibles touchées et celles-ci seront poussées de 2 cases vers l'extérieur au lieu d'une. le 
Bloc de Glace sera supprimé. la durée des effets 'enflammé' des cibles est remise à zéro.



Actif 7) Échardes de Glace // Pluie de Météores (3PE//8PE):
-- les Échardes de Glace est une attaque à distance monocible linéaire sans LdV d'une portée de 2 à 6 cases 
infligeant 3 points de dégâts et remettant à zéro la durée des effets 'gelé' de la cible touchée.

-- la Pluie de Météores est une attaque à distance en grande zone sans LdV d'une portée de 7 à 7 cases infligeant 
15 points de dégâts et appliquant l'effet 'enflammé': x2 au centre de la zone et x1 sur le reste de la zone. une 
utilisation tous les 3 tours.



Actif 8) Rideau de Neige // Tapis de Braises (2PE//3PE):
-- le Rideau de Neige est une application de 2 à 3 cases de portée de l'effet 'Couche de Neige' sur une petite 
zone l'effet 'Couche de Neige' est un effet de case retirant 1PM à toute entité marchant sur la case. l'effet 
'Couche de Neige' est supprimé ensuite. Cet effet reste 1 tour et ne peut pas être appliqué sur une case 
possédant l'effet 'Tapis de Braises' ou l'effet 'Geyser de Lave'. 1 utilisation par tour.

-- le Tapis de Braises est une application linéaire de 2 à 2 cases de portée de l'effet 'Tapis de Braises' sur une 
zone moyenne. l'effet 'Tapis de Braises' est un effet de case infligeant 2 points de dégâts à toute entité se 
déplaçant ou commençant son tour sur cette case. Cet effet dure 2 tours et ne peut pas être appliqué sur une case 
possédant l'effet 'Couche de Neige'. 1 utilisation par tour.



Actif 9) Cryogénisation (4PE):
-- la Cryogénisation met fin au tour du Mage Thermique qui gagne l'effet 'Cryogénisation', donnant 2PE 
supplémentaires pendant les 2 tours suivants. une utilisation tous les 3 tours.



Actif 10) Mur de Fumée (3PE):
-- le Mur de Fumée est une application linéaire de 1 à 2 cases en ligne perpendiculaire(zone) de l'effet 'Mur de 
Fumée'. une case l'effet 'Mur de Fumée' bloque la LdV comme un obstacle, tout en restant franchissable et 
attaquable. l'effet dure 2 tours et n'a aucune restriction par rapport aux autres effets des cases touchées. une 
utilisation tous les 2 tours.



-------------------------------------------------
-------------------- Passifs --------------------
-------------------------------------------------
Passif 1) Multipolarité:
-- Avec ce passif, Chaque actif (sauf le 4, 9 et 10) lancé dans l'état 'Feu' passe automatiquement le Mage 
Thermique dans l'état 'Glace' et vice-versa. chaque changement ainsi effectué augmente de 4 la valeur de l'effet 
'Dommages Collatéraux'. L'effet 'Dommages Collatéraux' inflige des dégâts égaux à sa valeur au début de chaque 
tour du Mage Thermique. La valeur redescend ensuite à 0 chaque tour.


Passif 2) Fusion des Pôles:
-- Avec ce passif, toute application de l'effet 'gelé' transforme tous les effets 'enflammé' de la cible en effets 
'gelé', et vice-versa.


Passif 3) Celsius Extrême:
-- Avec ce passif, l'effet 'gelé' diminue de 5% les attaques de la cible, et l'effet 'enflammé' diminue de 4% la
défense de la cible.
-- Remarque: sans ce passif, les effets 'gelé' et 'enflammé' n'applique aucun bonus ou malus aux cibles touchées.


Passif 4) Réactions en Chaîne:
-- Ce passif dévérouille des effets supplémentaires sur les actifs 1, 5 et 6 suivant certaines conditions (voir la 
description des actifs en question).


Passif 5) Polarité Glaciale:
-- Avec ce passif, le Mage Thermique commence systématiquement la partie dans l'état 'Glace'. Le Mage Thermique 
peut accumuler les effets 'gelé' sur ses cibles.


Passif 6) Polarité Flamboyante:
-- Avec ce passif, le Mage Thermique commence systématiquement la partie dans l'état 'Feu'. Le Mage Thermique 
peut accumuler les effets 'enflammé' sur ses cibles.
-- Remarque: sans le Passif 5 ou 6, l'état de départ du Mage Thermique est aléatoire.
-- Remarque: si les Passifs 5 et 6 sont tous deux équipés, c'est l'ordre de sélection qui détermine l'état de 
départ du Mage Thermique. Exemple: si le Passif 5 est sélectionné en premier, alors le Mage Thermique commencera 
la partie dans l'état 'Glace'.
