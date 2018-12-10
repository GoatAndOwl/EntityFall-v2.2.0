import mapFiles as mf

BACKGROUND_COLOR = '#a79b8d'
SELECTED_MAP = None
CELL_X = 60
CELL_Y = 40
singlePlayer = False
onlineMulti = False
localMulti = False
PLAYERS = []
PLAYERS_NB = None
LAUNCHED = False
UDP_ADDR = ('88.183.37.126', 1001)
SERVER_LIST = None
SERVER_TO_COONECT = None
LOCAL_SOCK = None
CLIENT = None
CLIENT_ID = None
SOUND_PLAYER = None
MUSIC = None
BETA_TESTERS = {'Maxence Parent, aka Redk': 6}
STARTED = False

VK_STATS = {'health': 150,
			'MP': 4,
			'EP': 10,
			'orientation': None}

TM_STATS = {'health': 95,
			'MP': 4,
			'EP': 10,
			'orientation': None}

MR_STATS = {'health': 110,
			'MP': 4,
			'EP': 10,
			'orientation': None}

PL_STATS = {'health': 200,
			'MP': 4,
			'EP': 10,
			'orientation': None}

def VK_A():
	pass

VK_ABILITIES = {
'ability_1': {'minRange': 1, 
				'maxRange': 1,
				'value': -8, # active 'combo' si passif 3 équipé 
				'EPcost': 2,
				'MPcost': 0, 
				'name': 'Coup de Pommeau',
				'details': ['Inflige 8 dégâts au corps à corps. utilisable 2/tour.']},

'ability_2': {'minRange': 1, 
				'maxRange': 1,
				'value': -10, # attaque monocible qui devient une zone si 'combo' activé
				'EPcost': 3,
				'MPcost': 0, 
				'name': "Coup d'Épée",
				'details': ['Inflige 10 dégâts au corps à corps.']},

'ability_3': {'minRange': 1, 
				'maxRange': 1,
				'value': -9, # valeur doublée si 3 effets 'charge' ou +
				'EPcost': 4,
				'MPcost': 0, 
				'name': 'Frappe Perçante',
				'details': ['Inflige 9 dégâts au corps à corps (x2 si 3 effets', 
							'"charge" ou +).']},

'ability_4': {'minRange': 0, 
				'maxRange': 0,
				'value': None, # applique endurance 2 fois
				'EPcost': 3,
				'MPcost': 0, 
				'name': 'Endurance',
				'details': ['Gagne 2PM ce tour et 1PM le tour suivant. Utilisable ', 
							'1tour/2.']},

'ability_5': {'minRange': 1, 
				'maxRange': 1,
				'value': -11, # coup de bouclier qui repousse de 1+x cases, x étant le nombre 
				'EPcost': 5, # d'effets [charge]
				'MPcost': 0, 
				'name': 'Charge au Bouclier',
				'details': ["Inflige 11 dégâts au corps à corps et repousse de 1+x ", 
							"cases. x = nombre d'effets 'charge'."]},

'ability_6': {'minRange': 0, 
				'maxRange': 0,
				'value': 0.20, # boost la prochaine attaque de 20%
				'EPcost': 1,
				'MPcost': 0, 
				'name': 'Affûtage',
				'details': ['Booste la prochaine attaque de 20%.']},

'ability_7': {'minRange': 1, 
				'maxRange': 1,
				'value': -3, 
				'EPcost': 2,
				'MPcost': 1, 
				'name': 'Kick enragé',
				'details': ['Inflige 3 dégâts au corps à corps et repousse de 2 ', 
							'cases. le Viking est poussé de 2 cases dans la même',
							'direction.']},

'ability_8': {'minRange': 1, 
				'maxRange': 1,
				'value': -12,
				'EPcost': 4,
				'MPcost': 0, 
				'name': 'Frappe Latérale',
				'details': ['Inflige 12 dégâts au corps à corps.']},
							
'ability_9': {'minRange': 1, 
				'maxRange': 4,
				'value': None, # donne un effet de protection a la cible
				'EPcost': 3,
				'MPcost': 0, 
				'name': 'Don de Bouclier',
				'details': ['Augmente la défense de la cible de 10% pendant 2 ', 
							'tours. Cet actif ne peut être utilisé si une cible',
							'bénéficie déjà de son effet.',
							'Si "bouclier boosté" choisi, augmente la défense de',
							'la cible de 15% pendant 3 tours à la place et 2 ',
							'entitées peuvent avoir cet effet en simultané.']},
							
'ability_10': {'minRange': 0, 
				'maxRange': 1,
				'value': 4,
				'EPcost': 2,
				'MPcost': 0, 
				'name': 'Chope de Bière',
				'details': ['Restore la cible de 5PDV. utilisable 2/tour']}}

def VK_P():
	pass

VK_PASSIVES = {
'passive_1': {'name': 'Charge Brutale',
'details': ["Le Viking gagne un effet 'charge' pour chaque déplacement dans la même",
			"direction. Charge: augmente la prochaine attaque du Viking de 5%.",
			"Disparaît après utilisation. cumulable."]},

'passive_2': {'name': 'Tête Dure',
'details': ["Le Viking augmente sa défense de front de 15%."]},

'passive_3': {'name': 'Enchaînements',
'details': ["Les attaques 'Coup d'Épée'/'Frappe Latérale' ont une plus grande zone",
			"d'attaque si la dernière attaque est un 'Coup de Pommeau'/'Coup d'Épée'."]},

'passive_4': {'name': 'Bouclier Boosté',
'details': ["L'actif 'Don de Bouclier' augmente la défense de la cible de 15% au lieu",
			"de 10% pendant 3 tours au lieu de 2, et l'effet peut être donné à deux ",
			"entités en simultané."]},

'passive_5': {'name': 'Coureur Aguerri',
'details': ["Le Viking possède 1PM supplémentaire."]},

'passive_6': {'name': 'Armure Saine',
'details': ["Le Viking possède 30PDV supplémentaires."]}}

####################################################		

def TM_A():
	pass
										
TM_ABILITIES = {
'ability_1[ice]': {'minRange': 1, 
					'maxRange': 6,
					'value': -6, # javelot gelé
					'EPcost': 2,
					'MPcost': 0,
					'name': 'Javelot Gelé',
					'details': ["Inflige 6 dégâts à distance et applique l'effet 'gelé'.",
								"Si 'Réactions en Chaîne' choisi, faire cette attaque sur",
								"un geyser de lave crée des tapis de braises dans une",
								"grande zone autour du geyser. le geyser est alors supprimé."]},
					
'ability_1[fire]': {'minRange': 2, 
					'maxRange': 5,
					'value': -9, # projection ardente
					'EPcost': 3,
					'MPcost': 0, 
					'name': 'Boule de Feu',
					'details': ["Inflige 9 dégâts à distance et applique l'effet 'enflammé'."]},

'ability_2[ice]': {'minRange': 2, 
				'maxRange': 4,
				'value': -13, # stalactite
				'EPcost': 5,
				'MPcost': 0, 
				'name': 'Stalactite',
				'details': ["Inflige 13 dégâts à distance et applique l'effet 'gelé'."]},

'ability_2[fire]': {'minRange': 1, 
					'maxRange': 1,
					'value': -18, # rayon incandescant
					'EPcost': 6,
					'MPcost': 0, 
					'name': 'Rayon Incandescant',
					'details': ["Inflige 18 dégâts à distance et applique l'effet 'enflammé'.",
								"L'attaque inflige 8% de dégâts supplémentaires par effet",
								"'gelé' sur la/les cibles. Les effets 'gelé' des cibles sont",
								"consommés."]},

'ability_3[ice]': {'minRange': 3, 
					'maxRange': 5,
					'value': -10, # onde glaciale (effet glacé +3 au centre et +2 derrière)
					'EPcost': 4,
					'MPcost': 0, 
					'name': 'Onde Gelée',
					'details': ["Inflige 10 dégâts à distance. Applique l'effet 'gelé'x3 au",
								"centre de la zone et x2 sur le reste de la zone. Utilisable",
								"1/tour."]},
				
'ability_3[fire]': {'minRange': 1, 
					'maxRange': 2,
					'value': -15, # cône de flammes (effet enflammé +3 au centre et +2 derrière)
					'EPcost': 6,
					'MPcost': 0, 
					'name': 'Cône de Flammes',
					'details': ["Inflige 15 dégâts à distance. Applique l'effet 'enflammé'x3",
								"au sommet de la zone et x2 sur le reste de la zone.",
								"Utilisable 1/tour."]},
				
'ability_4': {'minRange': 0, 
				'maxRange': 0,
				'value': None, # miroir polaire
				'EPcost': 1,
				'MPcost': 0, 
				'name': 'Miroir Thermique',
				'details': ["Le Mage Thermique passe de l'état 'glace' à l'état 'feu' ou",
							"vice-versa."]},

'ability_5[ice]': {'minRange': 1, 
					'maxRange': 4,
					'value': 10, # bloc de glace avec 10 pdv (1 par tour et 3 max)
					'EPcost': 2,
					'MPcost': 0, 
					'name': 'Bloc de Glace',
					'details': ["Invoque un Bloc de Glace de 10PDV sur la case ciblée. Le",
								"nombre de Blocs de Glace existants est limité à 2.",
								"Si 'Réactions en Chaîne' choisi, cette limite passe à 3,",
								"et si un Bloc est sur un Geyser de Lave: dans une grande",
								"zone autour du bloc: des Tapis de Braises sont créés, et les",
								"entitées dans cette zone sont repoussées d'une case et ",
								"subissent 4 dégâts."]},

'ability_5[fire]': {'minRange': 2, 
					'maxRange': 4,
					'value': -4, # geyser
					'EPcost': 1,
					'MPcost': 0, 
					'name': 'Geyser de Lave',
					'details': ["Crée un Geyser de Lave sur la case ciblée. Le Geyser reste",
								"3 tours et inflige 4 dégâts à quiconque marche sur la case",
								"ou commence son tour sur celle-ci."]},

'ability_6[ice]': {'minRange': 2, 
					'maxRange': 4,
					'value': -9, # bourrasque de blizzard
					'EPcost': 3,
					'MPcost': 0, 
					'name': 'Blizzard',
					'details': ["Inflige 9 dégâts à distance et applique l'effet 'gelé'. Les",
								"entitées touchées sont repoussées d'une case."]},
				
'ability_6[fire]': {'minRange': 3, 
					'maxRange': 4,
					'value': -10, # comète
					'EPcost': 4,
					'MPcost': 0, 
					'name': 'Météore',
					'details': ["Inflige 10 dégâts à distance et repousse d'une case depuis",
								"le centre."
								"Si 'Réactions en Chaîne' choisi: si un Bloc de glace est",
								"au centre de la zone: inflige 13 dégâts, et repousse de 2",
								"cases. Le Bloc est supprimé."]},


'ability_7[ice]': {'minRange': 2, 
					'maxRange': 6,
					'value': -8, # échardes de grêle
					'EPcost': 3,
					'MPcost': 0, 
					'name': 'Échardes gelées',
					'details': ["Inflige 8 dégâts à distance et réinitialise la durée des",
								"effets 'gelé' de la cible."]},

'ability_7[fire]': {'minRange': 7, 
					'maxRange': 7,
					'value': -18, # pluie de comètes
					'EPcost': 8,
					'MPcost': 0, 
					'name': 'Pluie de Météores',
					'details': ["Inflige 18 dégâts à distance et applique l'effet",
								"'enflammé'x2 au centre de la zone et x1 sur le reste",
								"de la zone. Utilisable 1tour/3."]},
								
'ability_8[ice]': {'minRange': 2, 
					'maxRange': 3,
					'value': -1, # tapis de neige
					'EPcost': 2,
					'MPcost': 0,
					'name': 'Tapis de Neige',
					'details': ["Crée des Couches de Neige dans une petite zone. Une",
								"Couche de Neige reste 1 tour et retire 1 PM à la",
								"prochaine entité marchant sur la case."]},

'ability_8[fire]': {'minRange': 2, 
				'maxRange': 2,
				'value': -2, # tapis de braises
				'EPcost': 3,
				'MPcost': 0, 
				'name': 'Tapis de Braises',
				'details': ["Crée des Tapis de Braises dans une zone moyenne. Un Tapis",
							"de Braises reste 2 tours et inflige 2 dégâts à quiconque",
							"marche sur la case ou commence son tour sur celle-ci."]},
							
'ability_9': {'minRange': 0, 
				'maxRange': 0,
				'value': 2, # cryogénisation
				'EPcost': 4,
				'MPcost': 0, 
				'name': 'Cryogénisation',
				'details': ['Le Mage Thermique met fin à son tour. il gagne alors 2PE',
							'pour ses 2 prochains tours. Utilisable 1tour/3.']},
							
'ability_10': {'minRange': 1, 
				'maxRange': 2,
				'value': 2, # mur de fumée
				'EPcost': 3,
				'MPcost': 0, 
				'name': 'Mur de Fumée',
				'details': ['Crée un Mur de fumée sur une ligne devant le Mage',
							'Thermique. Un Mur de fumée reste 2 tours et bloque',
							'la ligne de vue de toutes les entitées.']}}

def TM_P():
	pass

TM_PASSIVES = {
'passive_1': {'name': 'Multipolarité',
'details': ["À chaque attaque effectué, le Mage Thermique",
			"passe de l'état feu à l'état glace ou vice-versa.",
			"À son prochain tour, le Mage Thermique subit 4",
			"dégâts pour chaque changement de cette façon."]},

'passive_2': {'name': 'Fusion des pôles',
'details': ["Appliquer un ou plusieurs effets 'enflammé' sur",
			"une cible avec un ou plusieurs effets 'gelé'",
			"change chaque effet 'gelé' en 'enflammé', et",
			"vice-versa."]},

'passive_3': {'name': 'Celsius Extrême',
'details': ["l'effet enflammé' diminue dorénavant la défense de",
			"la cible de 5% au lieu de 0%."
			"l'effet gelé' diminue dorénavant l'attaque de la",
			"cible de 5% au lieu de 0%."]},

'passive_4': {'name': 'Réactions en Chaîne',
'details': ["Des nouveaux effets sont déverrouillés sur les actifs",
			"'Javelot Gelé', 'Bloc de Glace' et 'Météore'."]},

'passive_5': {'name': 'Pôle de Glace',
'details': ["Les effets 'gelé' sont dorénavant cumulables sur les cibles.",
			"Le Mage Thermique commence la partie dans l'état 'glace'."]},

'passive_6': {'name': 'Pôle de Feu',
'details': ["Les effets 'enflammé' sont dorénavant cumulables sur les",
			"cibles. Le Mage Thermique commence la partie dans l'état",
			"'feu'."]}}

####################################################

def MR_A():
	pass
	
MR_ABILITIES = {
'ability_1': {'minRange': 1, 
				'maxRange': 1,
				'value': -5, # coup de sabre
				'EPcost': 1,
				'MPcost': 0, 
				'name': 'Coup de Sabre',
				'details': ['inflige 5 dégâts au corps à corps. Utilisable 2/tour.']},

'ability_2': {'minRange': 2, 
				'maxRange': 4,
				'value': -6, # ordre de tir
				'EPcost': 3,
				'MPcost': 0, 
				'name': 'Ordre de Tir',
				'details': ['inflige 7 dégâts à distance. Cette attaque peut être',
							'faite depuis la portée des alliés du Maréchal.']},

'ability_3': {'minRange': 0, 
				'maxRange': 0,
				'value(1)': 0.10, # préparation
				'value(2)': 3,
				'EPcost': 5,
				'MPcost': 0, 
				'name': 'Préparation',
				'details': ['Met fin au tour du Maréchal. Celui-ci gagne 3PM et un',
							"bonus de 10% d'attaque à son prochain tour. Utilisable",
							"1tour/2."]},

'ability_4': {'minRange': 0, 
				'maxRange': 0,
				'value': 6, # retraite
				'EPcost': 10,
				'MPcost': 0, 
				'name': 'Retraite',
				'details': ["Le Maréchal gagne 6PM jusqu'a la fin du tour.",
							"Utilisable 1tour/3."]},

'ability_5': {'minRange': 1, 
				'maxRange': 2,
				'value': 2, # fossé
				'EPcost': 3,
				'MPcost': 0, 
				'name': 'Fossé',
				'details': ["La case ciblé devient infranchissable pendant 2",
							"tours. Utilisable 1tour/2."]},

'ability_6': {'minRange': 0, 
				'maxRange': 0,
				'value(1)': 4, # retranchements
				'value(2)': 0.10,
				'EPcost': 3,
				'MPcost': 0, 
				'name': 'Retranchements',
				'details': ['Crée des Retranchements autour du Maréchal dans une',
							"grande zone. Un Retranchement augmente la défense",
							"des alliés du Maréchal de 10%, et ceux-ci gagnent",
							"4PDV en commançant leur tour sur celui-ci. reste 2t."]},

'ability_7': {'minRange': 0, 
				'maxRange': 0,
				'value': 1, # mouvement des troupes
				'EPcost': 1,
				'MPcost': 1,
				'name': 'Mouvement des troupes',
				'details': ["Un allié du Maréchal se déplace d'une case dans la",
							"direction du Maréchal."]},

'ability_8': {'minRange': 1, 
				'maxRange': 1,
				'value': -2, # charge de dirigeant
				'EPcost': 3,
				'MPcost': 0, 
				'name': 'Charge de Dirigeant',
				'details': ["inflige 2xA dégâts et repousse de A cases. A = nombre",
							"d'alliés du Maréchal+1. Utilisable 1/tour. La portée",
							"maximale de cette attaque augmente de A cases."]},
							
'ability_9': {'minRange': 1, 
				'maxRange': 2,
				'value(1)': 4, # diplomatie
				'value(2)': 8,
				'EPcost': 2,
				'MPcost': 0, 
				'name': 'Diplomatie',
				'details': ["L'ennemi ciblé gagne 4PDV et le Maréchal gagne 8PDV.",
							"Utilisable 1/tour."]},
							
'ability_10': {'minRange': 0, 
				'maxRange': 0,
				'value(1)': 0.10, # armistice
				'value(2)': 0.10,
				'EPcost': 4,
				'MPcost': 0, 
				'name': 'Armistice',
				'details': ["Tous les joueurs ont leur attaque diminuée de 10% et",
							"leur défense augmentée de 10% jusqu'à la fin du tour.",
							"Utilisable 1tour/3."]}}

def MR_P():
	pass

MR_PASSIVES = {
'passive_1': {'name': 'Place Forte',
'details': ["Le Maréchal renforce les cases sur lesquelles sont",
			"ses alliés au premier tour, pour toute la partie. Un",
			"allié gagne 10% en defense en étant sur ces cases, et",
			"4PDV s'il commence son tour sur celle-ci."]},

'passive_2': {'name': 'Armure de Collection',
'details': ["Le Maréchal gagne 50 points de vie et perd 1PM de manière",
			"permanente."]},

'passive_3': {'name': 'Accord du Roi',
'details': ["Les attaques du Maréchal infligent 1 dégât supplémentaire."]},

'passive_4': {'name': 'Plan de Combat',
'details': ["Le Maréchal perd autant de PM que d'allié en vie. Chaque",
			"allié en vie gagne 1PM."]},

'passive_5': {'name': 'Soif de Vaincre',
'details': ["Le Maréchal perd 10% d'attaque pour chaque allié en vie.",
			"Chaque allié en vie gagne 10% d'attaque."]},

'passive_6': {'name': 'Défense de la Patrie',
'details': ["Le Maréchal perd 10% de défense pour chaque allié en vie.",
			"Chaque allié en vie gagne 10% de défense."]}}
			
####################################################

def PL_A():
	pass

PL_ABILITIES = {
'ability_1': {'minRange': 1, 
				'maxRange': 5,
				'value': 2, # Soins Divins 
				'EPcost': 1,
				'MPcost': 0, 
				'name': 'Soins Divins',
				'details': ['Soigne la Cible non ténébreuse et non impie. utilisable 3/tour.']},

'ability_2': {'minRange': 0, 
				'maxRange': 0,
				'value': 0.30, # Dôme de protection
				'EPcost': 4,
				'MPcost': 0, 
				'name': "Dôme de Protection",
				'details': ['Pendant 2 tours, les alliés en mêlée avec le Paladin gagnent 30% de défense. Utilisable 1tour/3.']},

'ability_3': {'minRange': 0, 
				'maxRange': 1,
				'value[1]': 0.25, # Sanctuaire
				'value[2]': 3,
				'EPcost': 7,
				'MPcost': 0, 
				'name': 'Frappe Perçante',
				'details': ['Inflige 9 dégâts au corps à corps (x2 si 3 effets', 
							'"charge" ou +).']},

'ability_4': {'minRange': 1, 
				'maxRange': 2,
				'value': 0.5, # resurrection
				'EPcost': 8,
				'MPcost': 0, 
				'name': 'Endurance',
				'details': ['Gagne 2PM ce tour et 1PM le tour suivant. Utilisable ', 
							'1tour/2.']},

'ability_5': {'minRange': 1, 
				'maxRange': 4,
				'value': 1, # benediction
				'EPcost': 2,
				'MPcost': 0, 
				'name': 'Charge au Bouclier',
				'details': ["Inflige 11 dégâts au corps à corps et repousse de 1+x ", 
							"cases. x = nombre d'effets 'charge'."]},

'ability_6': {'minRange': 0, 
				'maxRange': 0,
				'value': 0, # moment sacré
				'EPcost': 8,
				'MPcost': 0, 
				'name': 'Affûtage',
				'details': ['Booste la prochaine attaque de 20%.']},

'ability_7': {'minRange': 1, 
				'maxRange': 4,
				'value': 1, # barrière divine
				'EPcost': 2,
				'MPcost': 0, 
				'name': 'Kick enragé',
				'details': ['Inflige 3 dégâts au corps à corps et repousse de 2 ', 
							'cases. le Viking est poussé de 2 cases dans la même',
							'direction.']},

'ability_8': {'minRange': 1, 
				'maxRange': 1,
				'value': -12,
				'EPcost': 4,
				'MPcost': 0, 
				'name': 'Frappe Latérale',
				'details': ['Inflige 12 dégâts au corps à corps.']},
							
'ability_9': {'minRange': 1, 
				'maxRange': 4,
				'value': None, # donne un effet de protection a la cible
				'EPcost': 3,
				'MPcost': 0, 
				'name': 'Don de Bouclier',
				'details': ['Augmente la défense de la cible de 10% pendant 2 ', 
							'tours. Cet actif ne peut être utilisé si une cible',
							'bénéficie déjà de son effet.',
							'Si "bouclier boosté" choisi, augmente la défense de',
							'la cible de 15% pendant 3 tours à la place et 2 ',
							'entitées peuvent avoir cet effet en simultané.']},
							
'ability_10': {'minRange': 0, 
				'maxRange': 1,
				'value': 4,
				'EPcost': 2,
				'MPcost': 0, 
				'name': 'Chope de Bière',
				'details': ['Restore la cible de 5PDV. utilisable 2/tour']}}
