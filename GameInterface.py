import ui
import time
import socket
import json
import random
import Core as game
import Constants as ct
import Classes as cl
from mapFiles import *

selectMenu = True
global player
global onlinePlayer
global mainView
global playerConfigView
global clSelectView
global buildSelectView
global onlineLobbyView
global waitingScreenView
global mapSelectView
global redPlayers
global bluePlayers
global player_id
onlinePlayer = {'team': None,
				'name': None,
				'eNumber': None}
player = {'class': None,
		  'abilities': [],
		  'passives': [],
		  'team': None,
		  'name': None,
		  'id': None,
		  'randN': None}
redPlayers = 0
bluePlayers = 0
pick_pattern = [1,2,2,1,1,2]
player_id = 0

def changeServerName(serverList, server):
	serverName = str(serverList[server]['title']) + ' | '
	serverName += str(serverList[server]['redEntities']+serverList[server]['blueEntities']) 
	serverName += '/6 Entities | '
	serverName += 'Map: ' + str(serverList[server]['map']) + ' | '
	serverName += 'State: ' + str(serverList[server]['State'])
	return(serverName)
	
def refreshButton_touched(sender):
	if not ct.LOCAL_SOCK:
		ct.LOCAL_SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		ct.LOCAL_SOCK.settimeout(3)
	msg = str.encode(json.dumps(['send Servers Data']))
	ct.LOCAL_SOCK.sendto(msg, ct.UDP_ADDR)
	ct.SERVER_LIST = json.loads(bytes.decode(ct.LOCAL_SOCK.recv(8192)))
	for subview in onlineLobbyView['ServerButtonScroll'].subviews:
			subview.title = changeServerName(ct.SERVER_LIST, subview.name)

def server_touched(sender):
	if ct.SERVER_TO_COONECT == None:
		ct.SERVER_TO_COONECT = sender.name
		sender.background_color = '#00deff'
		sender.tint_color = '#00deff'
		onlineLobbyView['next_button'].enabled = True
	elif ct.SERVER_TO_COONECT == sender.name:
		ct.SERVER_TO_COONECT = None
		sender.background_color = '#ffffff'
		sender.tint_color = '#ffffff'
		onlineLobbyView['next_button'].enabled = False
		
def singlePlayer_touched(sender):
	ct.singlePlayer = True
	ct.onlineMulti = False
	ct.localMulti = False
	mainView.add_subview(mapSelectView)
	mapSelectView['playerNbSelector'].enabled = False
	mapSelectView['next_button'].enabled = False

def localMulti_touched(sender):
	ct.localMulti = True
	ct.onlineMulti = False
	ct.singlePlayer = False
	mainView.add_subview(mapSelectView)
	mapSelectView['next_button'].enabled = False
	
def onlineMulti_touched(sender):
	ct.onlineMulti = True
	ct.localMulti = False
	ct.singlePlayer = False
	mainView.add_subview(onlineLobbyView)
	onlineLobbyView['next_button'].enabled = False
	refreshButton_touched(None)
	#sender.title = 'C0M1NG S00N'

def parameters_touched(sender):
	sender.title = 'C0M1NG S00N'

def quitButton_touched(sender):
	ct.LAUNCHED = False
	ct.SOUND_PLAYER.music.stop()
	mainView.close()	
	
def teamButton_touched(sender):
	if ct.onlineMulti:
		onlinePlayer['team'] = sender.selected_index+1
	else:
		player['team'] = sender.selected_index+1
		if (bluePlayers >= 3 and player['team'] == 1) and \
		(redPlayers >= 3 and player['team'] == 2):
			playerConfigView['next_button'].enabled = False
		else:
			playerConfigView['next_button'].enabled = True

def entityBar_touched(sender):
	if ct.onlineMulti:
		onlinePlayer['eNumber'] = sender.selected_index+1

def ShowTeams(view, active_player):
	rplayers = 1
	bplayers = 1
	for player in ct.PLAYERS:
		if player['team'] == 1:
			view['Pseudo'+str(bplayers)+'Blue'].text = player['name']
			if player['class']:
				if player['class'] == 'Viking':
					img = ui.Image.named('Images/In-Game Ui/VK-BlueLogo.PNG')
				elif player['class'] == 'ThermalMage':
					img = ui.Image.named('Images/In-Game Ui/TM-BlueLogo.PNG')
				elif player['class'] == 'Marshal':
					img = ui.Image.named('Images/In-Game Ui/MR-BlueLogo.PNG')
				elif player['class'] == 'Paladin':
					img = ui.Image.named('Images/In-Game Ui/TM-BlueLogo.PNG')
			else:
				img = ui.Image.named('Images/In-Game Ui/NO-BlueLogo.PNG')
			view['Player'+str(bplayers)+'Blue'].background_image = img
			
			if player == active_player:
				view['Pseudo'+str(bplayers)+'Blue'].border_color = '#ff8500'
				view['Pseudo'+str(bplayers)+'Blue'].border_width = 4
				view['Pseudo'+str(bplayers)+'Blue'].corner_radius = 10
			bplayers += 1
			
		elif player['team'] == 2:
			view['Pseudo'+str(rplayers)+'Red'].text = player['name']
			if player['class']:
				if player['class'] == 'Viking':
					img = ui.Image.named('Images/In-Game Ui/VK-RedLogo.PNG')
				elif player['class'] == 'ThermalMage':
					img = ui.Image.named('Images/In-Game Ui/TM-RedLogo.PNG')
				elif player['class'] == 'Marshal':
					img = ui.Image.named('Images/In-Game Ui/MR-RedLogo.PNG')
				elif player['class'] == 'Paladin':
					img = ui.Image.named('Images/In-Game Ui/TM-RedLogo.PNG')
			else:
				img = ui.Image.named('Images/In-Game Ui/NO-RedLogo.PNG')
			view['Player'+str(rplayers)+'Red'].background_image = img
			
			if player == active_player:
				view['Pseudo'+str(rplayers)+'Red'].border_color = '#ff8500'
				view['Pseudo'+str(rplayers)+'Red'].border_width = 4
				view['Pseudo'+str(rplayers)+'Red'].corner_radius = 10
			rplayers += 1
			

def toggleEnabling(situation):
	mapNumbers = ['0', '1', '2', '3', '4', '5', '6', '7']
	classes = ['Viking', 'ThermalMage', 'Marshal', 'Paladin']
	abilities = ['ability_1', 'ability_2', 'ability_3', 'ability_4', 'ability_5', 
	'ability_6', 'ability_7', 'ability_8', 'ability_9', 'ability_10']
	passives = ['passive_1', 'passive_2', 'passive_3', 
	'passive_4', 'passive_5', 'passive_6']
	
	if situation == 'map':
		for subview in mapSelectView['mapScrollView'].subviews:
			if (ct.SELECTED_MAP == voidAndBoxesC and subview.number != '0') \
			or (ct.SELECTED_MAP == lostWarehouseC and subview.number != '1') \
			or (ct.SELECTED_MAP == voidRiverC and subview.number != '2') \
			or (ct.SELECTED_MAP == DilemnaC and subview.number != '3') \
			or (ct.SELECTED_MAP == SweetAnarchyC and subview.number != '4') \
			or (ct.SELECTED_MAP == testMap1C and subview.number != '5') \
			or (ct.SELECTED_MAP == testMap2C and subview.number != '6') \
			or (ct.SELECTED_MAP == testMap3C and subview.number != '7'):
				if subview.number in mapNumbers:
					if subview.enabled:
						subview.enabled = False
					else:
						subview.enabled = True
	
	elif situation == 'class':
		for subview in clSelectView['classScrollView'].subviews:
			if subview.name != player['class'] and subview.name in classes:
				if subview.enabled:
					subview.enabled = False
				else:
					subview.enabled = True
	
	elif situation == 'abilities':
		for subview in buildSelectView.subviews:
			if subview.name not in player['abilities'] and subview.name in abilities:
				if subview.enabled:
					subview.enabled = False
				else:
					subview.enabled = True
	
	elif situation == 'passives':
		for subview in buildSelectView.subviews:
			if subview.name not in player['passives'] and subview.name in passives:
				if subview.enabled:
					subview.enabled = False
				else:
					subview.enabled = True
	
def changeNames(selectedClass):
	if selectedClass == 'Viking':
		for subview in buildSelectView.subviews:
			if subview.name == 'ability_1':
				subview.title = 'Coup de Pommeau'
			elif subview.name == 'ability_2':
				subview.title = "Coup d'Épée"
			elif subview.name == 'ability_3':
				subview.title = 'Attaque Perçante'
			elif subview.name == 'ability_4':
				subview.title = 'Endurance'
			elif subview.name == 'ability_5':
				subview.title = 'Charge au Bouclier'
			elif subview.name == 'ability_6':
				subview.title = 'Affûtage'
			elif subview.name == 'ability_7':
				subview.title = 'Kick Enragé'
			elif subview.name == 'ability_8':
				subview.title = 'Frappe Latérale'
			elif subview.name == 'ability_9':
				subview.title = 'Don de Bouclier'
			elif subview.name == 'ability_10':
				subview.title = 'Chope de Bière'
				
			elif subview.name == 'passive_1':
				subview.title = 'Charge Brutale'
				subview.font = (subview.font[0], subview.font[1]-6)
			elif subview.name == 'passive_2':
				subview.title = 'Tête Dure'
			elif subview.name == 'passive_3':
				subview.title = 'Enchaînements'
				subview.font = (subview.font[0], subview.font[1]-3)
			elif subview.name == 'passive_4':
				subview.title = 'Bouclier Boosté'
				subview.font = (subview.font[0], subview.font[1]-3)
			elif subview.name == 'passive_5':
				subview.title = 'Coureur Aguerri'
				subview.font = (subview.font[0], subview.font[1]-4)
			elif subview.name == 'passive_6':
				subview.title = 'Armure Saine'
				subview.font = (subview.font[0], subview.font[1]-1)
	
	if selectedClass == 'ThermalMage':
		for subview in buildSelectView.subviews:
			if subview.name == 'ability_1':
				subview.title = 'Javelot//Boule de Feu'
				subview.font = (subview.font[0], subview.font[1]-1)
			elif subview.name == 'ability_2':
				subview.title = 'Stalactite//Rayon'
			elif subview.name == 'ability_3':
				subview.title = 'Onde Gelé//Cône de Flammes'
				subview.font = (subview.font[0], subview.font[1]-6)
			elif subview.name == 'ability_4':
				subview.title = 'Miroir Thermique'
			elif subview.name == 'ability_5':
				subview.title = 'Bloc de Glace//Geyser'
				subview.font = (subview.font[0], subview.font[1]-1)
			elif subview.name == 'ability_6':
				subview.title = 'Blizzard//Météore'
			elif subview.name == 'ability_7':
				subview.title = 'Échardes//Pluie de Météores'
				subview.font = (subview.font[0], subview.font[1]-6)
			elif subview.name == 'ability_8':
				subview.title = 'Neige//Tapis Brûlant'
				subview.font = (subview.font[0], subview.font[1]-1)
			elif subview.name == 'ability_9':
				subview.title = 'Cryogénisation'
			elif subview.name == 'ability_10':
				subview.title = 'Mur de Fumée'
				
			elif subview.name == 'passive_1':
				subview.title = 'MultiPolarité'
			elif subview.name == 'passive_2':
				subview.title = 'Fusion des Pôles'
				subview.font = (subview.font[0], subview.font[1]-4)
			elif subview.name == 'passive_3':
				subview.title = 'Celsius Extrême'
				subview.font = (subview.font[0], subview.font[1]-3)
			elif subview.name == 'passive_4':
				subview.title = 'Réactions en Chaîne'
				subview.font = (subview.font[0], subview.font[1]-9)
			elif subview.name == 'passive_5':
				subview.title = 'Pôle de Glace'
			elif subview.name == 'passive_6':
				subview.title = 'Pôle de Feu'
	
	if selectedClass == 'Marshal':
		for subview in buildSelectView.subviews:
			if subview.name == 'ability_1':
				subview.title = 'Coup de Sabre'
			elif subview.name == 'ability_2':
				subview.title = 'Ordre de Tir'
			elif subview.name == 'ability_3':
				subview.title = 'Préparation'
			elif subview.name == 'ability_4':
				subview.title = 'Retraite'
			elif subview.name == 'ability_5':
				subview.title = 'Fossé'
			elif subview.name == 'ability_6':
				subview.title = 'Renforcements'
			elif subview.name == 'ability_7':
				subview.title = 'Mouvement des Troupes'
				subview.font = (subview.font[0], subview.font[1]-3)
			elif subview.name == 'ability_8':
				subview.title = 'Charge du Leader'
			elif subview.name == 'ability_9':
				subview.title = 'Diplomatie'
			elif subview.name == 'ability_10':
				subview.title = 'Armistice'
				
			elif subview.name == 'passive_1':
				subview.title = 'Place Forte'
			elif subview.name == 'passive_2':
				subview.title = 'Armure de Collection'
				subview.font = (subview.font[0], subview.font[1]-9)
			elif subview.name == 'passive_3':
				subview.title = "Accord du Roi"
				subview.font = (subview.font[0], subview.font[1]-1)
			elif subview.name == 'passive_4':
				subview.title = 'Plan de Combat'
				subview.font = (subview.font[0], subview.font[1]-3)
			elif subview.name == 'passive_5':
				subview.title = 'Soif de Vaincre'
				subview.font = (subview.font[0], subview.font[1]-3)
			elif subview.name == 'passive_6':
				subview.title = 'Défense Nationale'
				subview.font = (subview.font[0], subview.font[1]-6)

def refresh_Waiting(entitylist):
	blueP = 1
	redP = 1
	if entitylist != ct.PLAYERS:
		for entity in entitylist:
			if entity['team'] == 1:
				if blueP == 1 and waitingScreenView['BlueSlot1'].text != entity['name'] and \
				waitingScreenView['BlueSlot1'].id != entity['id']:
					waitingScreenView['BlueSlot1'].font = ('<System-Bold>', 18)
					waitingScreenView['BlueSlot1'].text_color = '#00aaff'
					waitingScreenView['BlueSlot1'].text = entity['name']
					waitingScreenView['BlueSlot1'].id = entity['id']
					blueP += 1
				elif blueP == 2 and waitingScreenView['BlueSlot2'].text != entity['name'] and \
				waitingScreenView['BlueSlot2'].id != entity['id']:
					waitingScreenView['BlueSlot2'].font = ('<System-Bold>', 18)
					waitingScreenView['BlueSlot2'].text_color = '#00aaff'
					waitingScreenView['BlueSlot2'].text = entity['name']
					waitingScreenView['BlueSlot2'].id = entity['id']
					blueP += 1
				elif blueP == 3 and waitingScreenView['BlueSlot3'].text != entity['name'] and \
				waitingScreenView['BlueSlot3'].id != entity['id']:
					waitingScreenView['BlueSlot3'].font = ('<System-Bold>', 18)
					waitingScreenView['BlueSlot3'].text_color = '#00aaff'
					waitingScreenView['BlueSlot3'].text = entity['name']
					waitingScreenView['BlueSlot3'].id = entity['id']
					blueP += 1
			elif entity['team'] == 2:
				if redP == 1 and waitingScreenView['RedSlot1'].text != entity['name'] and \
				waitingScreenView['RedSlot1'].id != entity['id']:
					waitingScreenView['RedSlot1'].font = ('<System-Bold>', 18)
					waitingScreenView['RedSlot1'].text_color = '#ff5400'
					waitingScreenView['RedSlot1'].text = entity['name']
					waitingScreenView['RedSlot1'].id = entity['id']
					redP += 1
				elif redP == 2 and waitingScreenView['RedSlot2'].text != entity['name'] and \
				waitingScreenView['RedSlot2'].id != entity['id']:
					waitingScreenView['RedSlot2'].font = ('<System-Bold>', 18)
					waitingScreenView['RedSlot2'].text_color = '#ff5400'
					waitingScreenView['RedSlot2'].text = entity['name']
					waitingScreenView['RedSlot2'].id = entity['id']
					redP += 1
				elif redP == 3 and waitingScreenView['RedSlot3'].text != entity['name'] and \
				waitingScreenView['RedSlot3'].id != entity['id']:
					waitingScreenView['RedSlot3'].font = ('<System-Bold>', 18)
					waitingScreenView['RedSlot3'].text_color = '#ff5400'
					waitingScreenView['RedSlot3'].text = entity['name']
					waitingScreenView['RedSlot3'].id = entity['id']
					redP += 1
		
		if blueP > 4 and waitingScreenView['BlueSlot3'].text != 'Free Entity Slot':
			waitingScreenView['BlueSlot3'].font = ('<System>', 18)
			waitingScreenView['BlueSlot3'].text_color = '#ffffff'
			waitingScreenView['BlueSlot3'].text = 'Free Entity Slot'
			if blueP > 3 and waitingScreenView['BlueSlot2'].text != 'Free Entity Slot':
				waitingScreenView['BlueSlot2'].font = ('<System>', 18)
				waitingScreenView['BlueSlot2'].text_color = '#ffffff'
				waitingScreenView['BlueSlot2'].text = 'Free Entity Slot'
				if blueP > 2 and waitingScreenView['BlueSlot1'].text != 'Free Entity Slot':
					waitingScreenView['BlueSlot1'].font = ('<System>', 18)
					waitingScreenView['BlueSlot1'].text_color = '#ffffff'
					waitingScreenView['BlueSlot1'].text = 'Free Entity Slot'
		
		if redP > 4 and waitingScreenView['RedSlot3'].text != 'Free Entity Slot':
			waitingScreenView['RedSlot3'].font = ('<System>', 18)
			waitingScreenView['RedSlot3'].text_color = '#ffffff'
			waitingScreenView['RedSlot3'].text = 'Free Entity Slot'
			if redP > 3 and waitingScreenView['RedSlot2'].text != 'Free Entity Slot':
				waitingScreenView['RedSlot2'].font = ('<System>', 18)
				waitingScreenView['RedSlot2'].text_color = '#ffffff'
				waitingScreenView['RedSlot2'].text = 'Free Entity Slot'
				if redP > 2 and waitingScreenView['RedSlot1'].text != 'Free Entity Slot':
					waitingScreenView['RedSlot1'].font = ('<System>', 18)
					waitingScreenView['RedSlot1'].text_color = '#ffffff'
					waitingScreenView['RedSlot1'].text = 'Free Entity Slot'
		ct.PLAYERS = entitylist
		
def class_touched(sender):
	if sender.name != player['class'] and player['class'] == None:
		if player['team'] == 1:
			sender.background_color = '#00deff'
			sender.tint_color = '#00deff'
		elif player['team'] == 2:
			sender.background_color = '#ff5400'
			sender.tint_color = '#ff5400'
		player['class'] = sender.name
		clSelectView['next_button'].enabled = True
		toggleEnabling('class')
		
	elif sender.name == player['class']:
		toggleEnabling('class')
		sender.background_color = '#ffffff'
		sender.tint_color = '#ffffff'
		clSelectView['next_button'].enabled = False
		player['class'] = None

def ability_touched(sender):
	if not sender.name in player['abilities'] and len(player['abilities']) < 5:
		if player['team'] == 1:
			sender.background_color = '#00deff'
			sender.tint_color = '#00deff'
		elif player['team'] == 2:
			sender.background_color = '#ff5400'
			sender.tint_color = '#ff5400'
		player['abilities'].append(sender.name)
		draw_ability(player['class'], sender.name)
		if len(player['abilities']) == 5 and \
		len(player['passives']) == 3:
			buildSelectView['next_button'].enabled = True
		if len(player['abilities']) == 5:
			toggleEnabling('abilities')
			
	elif sender.name in player['abilities']:
		if len(player['abilities']) == 5:
			toggleEnabling('abilities')
		sender.background_color = '#ffffff'
		sender.tint_color = '#ffffff'
		x = player['abilities'].index(sender.name)
		del player['abilities'][x]
		buildSelectView['next_button'].enabled = False

def draw_ability(clas, ability):
	x = 0
	y = 0
	z = ['ability_4', 'ability_9', 'ability_10']
	if clas == 'Viking':
		x = ct.VK_ABILITIES
	elif clas == 'ThermalMage':
		x = ct.TM_ABILITIES
	elif clas == 'Marshal':
		x = ct.MR_ABILITIES
		
	if buildSelectView['abilityName1'].text:
		if buildSelectView['abilityName2'].text:
			y = 1
		else:
			y = 2
	else:
		y = 1
	
	if y == 1 and (not clas == 'ThermalMage' or ability in z) and not clas == 'Paladin':
		if buildSelectView['abilityName1'].text:
			buildSelectView['abilityName2'].text = buildSelectView['abilityName1'].text
			buildSelectView['abilityText2'].text = buildSelectView['abilityText1'].text
			buildSelectView['abilityCost2'].text = buildSelectView['abilityCost1'].text
			buildSelectView['abilityRange2'].text = buildSelectView['abilityRange1'].text
		buildSelectView['abilityName1'].text = x[ability]['name']
		abilityText = ''
		for text in x[ability]['details']:
			abilityText += text
			abilityText += ' '
		buildSelectView['abilityText1'].alignment = ui.ALIGN_JUSTIFIED
		buildSelectView['abilityText1'].text = abilityText
		rangeText = 'Portée: '+str(x[ability]['minRange'])+'-'+str(x[ability]['maxRange'])
		buildSelectView['abilityRange1'].text = rangeText
		if x[ability]['EPcost']:
			if x[ability]['MPcost']:
				costText = 'Coût: '+str(x[ability]['EPcost'])+'PE/'+str(x[ability]['MPcost'])+'PM'
			else:
				costText = 'Coût: '+str(x[ability]['EPcost'])+'PE'
		else:
			costText = 'Coût: '+str(x[ability]['MPcost'])+'PM'
		buildSelectView['abilityCost1'].text = costText
	
	elif y == 2 and (not clas == 'ThermalMage' or ability in z):
		buildSelectView['abilityName2'].text = x[ability]['name']
		abilityText = ''
		for text in x[ability]['details']:
			abilityText += text
			abilityText += ' '
		buildSelectView['abilityText2'].alignment = ui.ALIGN_JUSTIFIED
		buildSelectView['abilityText2'].text = abilityText
		rangeText = 'Portée: '+str(x[ability]['minRange'])+'-'+str(x[ability]['maxRange'])
		buildSelectView['abilityRange2'].text = rangeText
		if x[ability]['EPcost']:
			if x[ability]['MPcost']:
				costText = 'Coût: '+str(x[ability]['EPcost'])+'PE/'+str(x[ability]['MPcost'])+'PM'
			else:
				costText = 'Coût: '+str(x[ability]['EPcost'])+'PE'
		else:
			costText = 'Coût: '+str(x[ability]['MPcost'])+'PM'
		buildSelectView['abilityCost2'].text = costText
		
	##########################################################################################
	elif clas == 'ThermalMage':
		abilityI = ability+'[ice]'
		buildSelectView['abilityName1'].text = x[abilityI]['name']+'[glace]'
		abilityText = ''
		for text in x[abilityI]['details']:
			abilityText += text
			abilityText += ' '
		buildSelectView['abilityText1'].alignment = ui.ALIGN_JUSTIFIED
		buildSelectView['abilityText1'].text = abilityText
		rangeText = 'Portée: '+str(x[abilityI]['minRange'])+'-'+str(x[abilityI]['maxRange'])
		buildSelectView['abilityRange1'].text = rangeText
		if x[abilityI]['EPcost']:
			if x[abilityI]['MPcost']:
				costText = 'Coût: '+str(x[abilityI]['EPcost'])+'PE/'+str(x[abilityI]['MPcost'])+'PM'
			else:
				costText = 'Coût: '+str(x[abilityI]['EPcost'])+'PE'
		else:
			costText = 'Coût: '+str(x[abilityI]['MPcost'])+'PM'
		buildSelectView['abilityCost1'].text = costText
		################################################################
		abilityF = ability+'[fire]'
		buildSelectView['abilityName2'].text = x[abilityF]['name']+'[feu]'
		abilityText = ''
		for text in x[abilityF]['details']:
			abilityText += text
			abilityText += ' '
		buildSelectView['abilityText2'].alignment = ui.ALIGN_JUSTIFIED
		buildSelectView['abilityText2'].text = abilityText
		rangeText = 'Portée: '+str(x[abilityF]['minRange'])+'-'+str(x[abilityF]['maxRange'])
		buildSelectView['abilityRange2'].text = rangeText
		if x[abilityF]['EPcost']:
			if x[abilityF]['MPcost']:
				costText = 'Coût: '+str(x[abilityF]['EPcost'])+'PE/'+str(x[abilityF]['MPcost'])+'PM'
			else:
				costText = 'Coût: '+str(x[abilityF]['EPcost'])+'PE'
		else:
			costText = 'Coût: '+str(x[abilityF]['MPcost'])+'PM'
		buildSelectView['abilityCost2'].text = costText		
	##########################################################################################

def passive_touched(sender):
	if not sender.name in player['passives'] and len(player['passives']) < 3:
		if player['team'] == 1:
			sender.background_color = '#00deff'
			sender.tint_color = '#00deff'
		elif player['team'] == 2:
			sender.background_color = '#ff5400'
			sender.tint_color = '#ff5400'
		player['passives'].append(sender.name)
		draw_passive(player['class'], sender.name)
		if len(player['abilities']) == 5 and \
		len(player['passives']) == 3:
			buildSelectView['next_button'].enabled = True
		if len(player['passives']) == 3:
			toggleEnabling('passives')
			
	elif sender.name in player['passives']:
		if len(player['passives']) == 3:
			toggleEnabling('passives')
		sender.background_color = '#ffffff'
		sender.tint_color = '#ffffff'
		x = player['passives'].index(sender.name)
		del player['passives'][x]
		buildSelectView['next_button'].enabled = False

def draw_passive(clas, passive):
	x = 0
	y = 0
	if clas == 'Viking':
		x = ct.VK_PASSIVES
	elif clas == 'ThermalMage':
		x = ct.TM_PASSIVES
	elif clas == 'Marshal':
		x = ct.MR_PASSIVES
	
	if buildSelectView['PassiveName1'].text:
		if buildSelectView['PassiveName2'].text:
			y = 1
		else:
			y = 2
	else:
		y = 1
	
	if y == 1 and not clas == 'Paladin':
		if buildSelectView['PassiveName1'].text:
			buildSelectView['PassiveName2'].text = buildSelectView['PassiveName1'].text
			buildSelectView['PassiveText2'].text = buildSelectView['PassiveText1'].text
		
		buildSelectView['PassiveName1'].text = x[passive]['name']
		a = ''
		for text in x[passive]['details']:
			a += text
			a += ' '
		buildSelectView['PassiveText1'].alignment = ui.ALIGN_JUSTIFIED
		buildSelectView['PassiveText1'].text = a
		
	elif y == 2:
		buildSelectView['PassiveName2'].text = x[passive]['name']
		a = ''
		for text in x[passive]['details']:
			a += text
			a += ' '
		buildSelectView['PassiveText2'].alignment = ui.ALIGN_JUSTIFIED
		buildSelectView['PassiveText2'].text = a
		
			

def back_touched(sender):
	global player
	global onlinePlayer
	global mainView
	global playerConfigView
	global onlineLobbyView
	global clSelectView
	global buildSelectView
	global mapSelectView
	global redPlayers
	global bluePlayers
	if ct.singlePlayer:
		if mapSelectView.on_screen:
			ct.singlePlayer = False
			ct.SELECTED_MAP = None
			mainView.remove_subview(mapSelectView)
			mapSelectView = ui.load_view('MapSelector')
		elif playerConfigView.on_screen:
			mainView.remove_subview(playerConfigView)
			mainView.add_subview(mapSelectView)
			playerConfigView = ui.load_view('PlayerConfig')
			player = {'class': None,
					  'abilities': [],
					  'passives': [],
					  'team': None,
					  'name': None,
					  'id': None}
		elif clSelectView.on_screen:
			mainView.remove_subview(clSelectView)
			mainView.add_subview(playerConfigView)
			clSelectView = ui.load_view('ClassSelector')
			player['class'] = None
		elif buildSelectView.on_screen:
			mainView.remove_subview(buildSelectView)
			mainView.add_subview(clSelectView)
			buildSelectView = ui.load_view('AbilityPicker')
			player['passives'] = []
			player['abilities'] = []
		
	elif ct.localMulti:
		if mapSelectView.on_screen:
			ct.localMulti = False
			ct.SELECTED_MAP = None
			mainView.remove_subview(mapSelectView)
			mapSelectView = ui.load_view('MapSelector')
		elif playerConfigView.on_screen:
			if len(ct.PLAYERS):
				player = ct.PLAYERS[len(ct.PLAYERS)-1]
				if player['team'] == 1:
					bluePlayers -= 1
				if player['team'] == 2:
					redPlayers -= 1	
				ct.PLAYERS.remove(player)
				player = {'class': None,
						  'abilities': [],
						  'passives': [],
						  'team': None,
						  'name': None,
						  'id': None}
				mainView.remove_subview(playerConfigView)
				playerConfigView = ui.load_view('PlayerConfig')
				mainView.add_subview(playerConfigView)
				playerConfigView['EntityNb_button'].enabled = False
				if bluePlayers >= 3:	
					playerConfigView['next_button'].enabled = False
				ShowTeams(playerConfigView, None)
			else:
				player = {'class': None,
						  'abilities': [],
						  'passives': [],
						  'team': None,
						  'name': None,
						  'id': None}
				mainView.remove_subview(playerConfigView)
				playerConfigView = ui.load_view('PlayerConfig')
				mainView.add_subview(mapSelectView)
		
		elif clSelectView.on_screen:
			if player != ct.PLAYERS[0]:
				player['class'] = None
				player = ct.PLAYERS[ct.PLAYERS.index(player)-1]
				player['class'] = None
				mainView.remove_subview(clSelectView)
				clSelectView = ui.load_view('ClassSelector')
				mainView.add_subview(clSelectView)
				clSelectView['next_button'].enabled = False
				ShowTeams(clSelectView, player)
				
			elif player == ct.PLAYERS[0]:
				player['class'] = None
				player = ct.PLAYERS[len(ct.PLAYERS)-1]
				if player['team'] == 1:
					bluePlayers -= 1
				if player['team'] == 2:
					redPlayers -= 1	
				ct.PLAYERS.remove(player)
				player = {'class': None,
						  'abilities': [],
						  'passives': [],
						  'team': None,
						  'name': None,
						  'id': None}
				mainView.remove_subview(clSelectView)
				playerConfigView = ui.load_view('PlayerConfig')
				clSelectView = ui.load_view('ClassSelector')
				mainView.add_subview(playerConfigView)
				if bluePlayers >= 3:	
					playerConfigView['next_button'].enabled = False
				ShowTeams(playerConfigView, player)
		
		elif buildSelectView.on_screen:
			if player != ct.PLAYERS[0]:
				player['abilities'] = []
				player['passives'] = []
				player = ct.PLAYERS[ct.PLAYERS.index(player)-1]
				player['abilities'] = []
				player['passives'] = []
				mainView.remove_subview(buildSelectView)
				buildSelectView = ui.load_view('AbilityPicker')
				mainView.add_subview(buildSelectView)
				buildSelectView['next_button'].enabled = False
				changeNames(player['class'])
				ShowTeams(buildSelectView, player)
				
			elif player == ct.PLAYERS[0]:
				player['abilities'] = []
				player['passives'] = []
				player = ct.PLAYERS[len(ct.PLAYERS)-1]
				player['class'] = None
				mainView.remove_subview(buildSelectView)
				buildSelectView = ui.load_view('AbilityPicker')
				clSelectView = ui.load_view('ClassSelector')
				mainView.add_subview(clSelectView)
				clSelectView['next_button'].enabled = False
				ShowTeams(clSelectView, player)
	
	elif ct.onlineMulti:
		if onlineLobbyView.on_screen:
			ct.onlineMulti = False
			ct.SERVER_LIST = None
			ct.SERVER_TO_COONECT = None
			ct.LOCAL_SOCK = None
			mainView.remove_subview(onlineLobbyView)
			onlineLobbyView = ui.load_view('OnlineLobby')
		elif mapSelectView.on_screen:
			msg = str.encode(json.dumps(['negate map pick', ct.SERVER_TO_COONECT]))
			ct.LOCAL_SOCK.sendto(msg, ct.UDP_ADDR)
			ans = bytes.decode(ct.LOCAL_SOCK.recv(1024))
			if ans == 'negation applied':
				mainView.remove_subview(mapSelectView)
				mapSelectView = ui.load_view('MapSelector')
				mainView.add_subview(onlineLobbyView)
				
def next_touched(sender):
	global player
	global onlinePlayer
	global mainView
	global playerConfigView
	global clSelectView
	global buildSelectView
	global mapSelectView
	global redPlayers
	global bluePlayers
	global player_id
	if ct.singlePlayer:
		if mapSelectView.on_screen:
			if ct.SELECTED_MAP != None:
				mainView.remove_subview(mapSelectView)
				mainView.add_subview(playerConfigView)
				playerConfigView['EntityNb_button'].enabled = False
		elif playerConfigView.on_screen:
			if player['team'] == None:
				player['team'] = 1
			if player['name'] == None:
				player['name'] = 'Player'
			mainView.remove_subview(playerConfigView)
			mainView.add_subview(clSelectView)
			clSelectView['playerWord'].text = player['name']+', choose your class:'
			clSelectView['next_button'].enabled = False
		elif clSelectView.on_screen:
			mainView.remove_subview(clSelectView)
			mainView.add_subview(buildSelectView)
			buildSelectView['next_button'].enabled = False
			changeNames(player['class'])
		elif buildSelectView.on_screen:
			ct.PLAYERS.append(player)
			mainView.close()
			mainView.wait_modal()
			game.run_game()
	
	elif ct.localMulti:
		if mapSelectView.on_screen:
			if ct.SELECTED_MAP != None:
				mainView.remove_subview(mapSelectView)
				if ct.PLAYERS_NB == None:
					ct.PLAYERS_NB = 2
				mainView.add_subview(playerConfigView)
				playerConfigView['EntityNb_button'].enabled = False
		elif playerConfigView.on_screen:
			if player['team'] == None:
				player['team'] = 1
			if player['name'] == None:
				player['name'] = 'Player '+(str(len(ct.PLAYERS)+1))

			if player['team'] == 1:
				bluePlayers += 1
			if player['team'] == 2:
				redPlayers += 1
				
			if len(ct.PLAYERS) + 1 < ct.PLAYERS_NB:
				ct.PLAYERS.append(player)
				mainView.remove_subview(playerConfigView)
				playerConfigView = ui.load_view('PlayerConfig')
				if bluePlayers == 3:
					playerConfigView['next_button'].enabled = False
				player = {'class': None,
						  'abilities': [],
						  'passives': [],
						  'team': None,
						  'name': None,
						  'id': None}
				mainView.add_subview(playerConfigView)
				ShowTeams(playerConfigView, None)
				playerConfigView['EntityNb_button'].enabled = False
			else:
				ct.PLAYERS.append(player)
				x = 0
				for number in pick_pattern:
					if x+1 <= len(ct.PLAYERS):
						if ct.PLAYERS[x]['team'] != number:
							for player2 in ct.PLAYERS:
								if player2['team'] == number and \
								player2['team'] != pick_pattern[ct.PLAYERS.index(player2)]:
									ct.PLAYERS.remove(player2)
									ct.PLAYERS.insert(x, player2)
									break
					x += 1
				player = ct.PLAYERS[0]
				mainView.remove_subview(playerConfigView)
				mainView.add_subview(clSelectView)
				ShowTeams(clSelectView, player)
				clSelectView['playerWord'].text = player['name']+', choose your class:'
				clSelectView['next_button'].enabled = False
			
		elif clSelectView.on_screen:
			x = 0
			for player2 in ct.PLAYERS:
				if player2['class']:
					x += 1
			if x < len(ct.PLAYERS):
				player = ct.PLAYERS[ct.PLAYERS.index(player)+1]
				mainView.remove_subview(clSelectView)
				clSelectView = ui.load_view('ClassSelector')
				mainView.add_subview(clSelectView)
				ShowTeams(clSelectView, player)
				clSelectView['playerWord'].text = player['name']+', choose your class:'
				clSelectView['next_button'].enabled = False
			else:
				player = ct.PLAYERS[0]
				mainView.remove_subview(clSelectView)
				mainView.add_subview(buildSelectView)
				ShowTeams(buildSelectView, player)
				buildSelectView['next_button'].enabled = False
				changeNames(player['class'])
		
		elif buildSelectView.on_screen:
			x = 0
			for player2 in ct.PLAYERS:
				if len(player2['abilities']):
					x += 1
					
			if x < len(ct.PLAYERS):
				player = ct.PLAYERS[ct.PLAYERS.index(player)+1]
				mainView.remove_subview(buildSelectView)
				buildSelectView = ui.load_view('AbilityPicker')
				mainView.add_subview(buildSelectView)
				ShowTeams(buildSelectView, player)
				buildSelectView['next_button'].enabled = False
				changeNames(player['class'])
			else:
				mainView.close()
				mainView.wait_modal()
				game.run_game()
	
	elif ct.onlineMulti:
		if onlineLobbyView.on_screen:
			msg = str.encode(json.dumps(['coonect to Server', ct.SERVER_TO_COONECT]))
			ct.LOCAL_SOCK.sendto(msg, ct.UDP_ADDR)
			ans = bytes.decode(ct.LOCAL_SOCK.recv(1024))
			if ans == 'choose the map':
				mainView.remove_subview(onlineLobbyView)
				mainView.add_subview(mapSelectView)
				mapSelectView['next_button'].enabled = False
				mapSelectView['playerNbSelector'].enabled = False
				
			elif ans == 'coonection available':
				refreshButton_touched(None)
				if ct.SERVER_LIST[ct.SERVER_TO_COONECT]['map'] == 'Void&Boxes':
					ct.SELECTED_MAP = voidAndBoxesC
				elif ct.SERVER_LIST[ct.SERVER_TO_COONECT]['map'] == 'LostWarehouse':
					ct.SELECTED_MAP = lostWarehouseC
				elif ct.SERVER_LIST[ct.SERVER_TO_COONECT]['map'] == 'VoidRiver':
					ct.SELECTED_MAP = voidRiverC
				elif ct.SERVER_LIST[ct.SERVER_TO_COONECT]['map'] == 'Dilemma':
					ct.SELECTED_MAP = DilemnaC
				elif ct.SERVER_LIST[ct.SERVER_TO_COONECT]['map'] == 'SweetAnarchy':
					ct.SELECTED_MAP = SweetAnarchyC
					
				addr = (ct.UDP_ADDR[0], 
						ct.SERVER_LIST[ct.SERVER_TO_COONECT]['address'][1])
				ct.CLIENT = cl.Client(addr, 'New Coonection')
				while not ct.CLIENT.last_msg:
					continue
				if ct.CLIENT.last_msg == 'give player parameters':
					ct.CLIENT.last_msg = None
					mainView.remove_subview(onlineLobbyView)
					mainView.add_subview(playerConfigView)
					
		elif mapSelectView.on_screen:
			if ct.SELECTED_MAP == voidAndBoxesC:
				msg = str.encode(json.dumps(['map chosen for', ct.SERVER_TO_COONECT, 'Void&Boxes']))
			elif ct.SELECTED_MAP == lostWarehouseC:
				msg = str.encode(json.dumps(['map chosen for', ct.SERVER_TO_COONECT, 'LostWarehouse']))
			elif ct.SELECTED_MAP == voidRiverC:
				msg = str.encode(json.dumps(['map chosen for', ct.SERVER_TO_COONECT, 'VoidRiver']))
			elif ct.SELECTED_MAP == DilemnaC:
				msg = str.encode(json.dumps(['map chosen for', ct.SERVER_TO_COONECT, 'Dilemma']))
			elif ct.SELECTED_MAP == SweetAnarchyC:
				msg = str.encode(json.dumps(['map chosen for', ct.SERVER_TO_COONECT, 'SweetAnarchy']))
			ct.LOCAL_SOCK.sendto(msg, ct.UDP_ADDR)
			ans = bytes.decode(ct.LOCAL_SOCK.recv(1024))
			if ans == 'map pick applied':
				addr = (ct.UDP_ADDR[0], 
						ct.SERVER_LIST[ct.SERVER_TO_COONECT]['address'][1])
				ct.CLIENT = cl.Client(addr, 'New Coonection')
				while not ct.CLIENT.last_msg:
					continue
				if ct.CLIENT.last_msg == 'give player parameters':
					ct.CLIENT.last_msg = None
					mainView.remove_subview(mapSelectView)
					mainView.add_subview(playerConfigView)
					
		elif playerConfigView.on_screen:
			if not onlinePlayer['eNumber']:
				onlinePlayer['eNumber'] = 1
			if not onlinePlayer['name']:
				onlinePlayer['name'] = 'player'
			if not onlinePlayer['team']:
				onlinePlayer['team'] = 1
				
			ct.CLIENT.data_to_send = onlinePlayer
			while not ct.CLIENT.last_msg:
				continue
			if ct.CLIENT.last_msg[0] == 'player settings OK':
				mainView.remove_subview(playerConfigView)
				refresh_Waiting(ct.CLIENT.last_msg[1])
				if ct.SELECTED_MAP == voidAndBoxesC:
					maptext = 'Void&Boxes'
				elif ct.SELECTED_MAP == lostWarehouseC:
					maptext = 'LostWarehouse'
				elif ct.SELECTED_MAP == voidRiverC:
					maptext = 'VoidRiver'
				elif ct.SELECTED_MAP == DilemnaC:
					maptext = 'Dilemma'
				elif ct.SELECTED_MAP == DilemnaC:
					maptext = 'SweetAnarchy'
					
				waitingScreenView['mapLabel'].text = 'on '+maptext
				ct.CLIENT.last_msg = None
				mainView.add_subview(waitingScreenView)
				
		elif waitingScreenView.on_screen:
			ct.CLIENT.data_to_send = str.encode('start Setting Up')
			while not ct.CLIENT.last_msg:
				continue
			if ct.CLIENT.last_msg[0] == 'setting up Game':
				refresh_Waiting(ct.CLIENT.last_msg[1])
				for entity in ct.PLAYERS:
					if entity['id'] == ct.CLIENT_ID:
						player = entity
						break
				
				mainView.remove_subview(waitingScreenView)
				mainView.add_subview(clSelectView)
				clSelectView['playerWord'].text = player['name']+', choose your class:'
				clSelectView['next_button'].enabled = False
				
		elif clSelectView.on_screen:
			mainView.remove_subview(clSelectView)
			mainView.add_subview(buildSelectView)
			buildSelectView['next_button'].enabled = False
			changeNames(player['class'])
		
		elif buildSelectView.on_screen:
			x = 0
			for entity in ct.PLAYERS:
				if entity['name'] == player['name'] and entity['id'] == ct.CLIENT_ID:
					entity = player
					entity['RandN'] = random.randint(0, 1)
					ct.CLIENT.data_to_send = str.encode(json.dumps(['add entity', entity['name'], entity['class'], 
					entity['abilities'], entity['passives'], entity['id'], entity['randN']]))
					print(ct.CLIENT.data_to_send)
					break
					
			for entity2 in ct.PLAYERS:
				if entity2['id'] == ct.CLIENT_ID and entity2['class']:
					x += 1
			
			if x < onlinePlayer['eNumber']:
				for entity in ct.PLAYERS:
					if entity['id'] == ct.CLIENT_ID and not entity['class']:
						player = entity
						clSelectView = ui.load_view('ClassSelector')
						mainView.remove_subview(buildSelectView)
						mainView.add_subview(clSelectView)
						buildSelectView = ui.load_view('AbilityPicker')
						clSelectView['playerWord'].text = player['name']+', choose your class:'
						clSelectView['next_button'].enabled = False
			
			elif x == onlinePlayer['eNumber']:
				mainView.remove_subview(buildSelectView)
				clSelectView = ui.load_view('ClassSelector')
				buildSelectView = ui.load_view('AbilityPicker')
				mainView.add_subview(waitingScreenView)
				ct.CLIENT.state = 'Receiving Up'
				waitingScreenView['next_button'].enabled = False
				waitingScreenView['back_button'].enabled = False
				waitingScreenView['next_button'].title = 'Wait'
				waitingScreenView['back_button'].title = 'Wait'
			
def map_touched(sender):
	if ct.SELECTED_MAP == None:
		if sender.number:
			sender.background_color = '#00deff'
			sender.font = ('<System-Bold>', sender.font[1])
			sender.tint_color = '#00deff'
			if sender.number == '0':
				ct.SELECTED_MAP = voidAndBoxesC
			if sender.number == '1':
				ct.SELECTED_MAP = lostWarehouseC
			if sender.number == '2':
				ct.SELECTED_MAP = voidRiverC
			if sender.number == '3':
				ct.SELECTED_MAP = DilemnaC
			if sender.number == '4':
				ct.SELECTED_MAP = SweetAnarchyC
			if sender.number == '5':
				ct.SELECTED_MAP = testMap1C
			if sender.number == '6':
				ct.SELECTED_MAP = testMap2C
			if sender.number == '7':
				ct.SELECTED_MAP = testMap3C
			if ct.SELECTED_MAP != None:
				mapSelectView['next_button'].enabled = True
				toggleEnabling('map')
	elif (ct.SELECTED_MAP == voidAndBoxesC and sender.number == '0') \
	or (ct.SELECTED_MAP == lostWarehouseC and sender.number == '1') \
	or (ct.SELECTED_MAP == voidRiverC and sender.number == '2') \
	or (ct.SELECTED_MAP == DilemnaC and sender.number == '3') \
	or (ct.SELECTED_MAP == SweetAnarchyC and sender.number == '4') \
	or (ct.SELECTED_MAP == testMap1C and sender.number == '5') \
	or (ct.SELECTED_MAP == testMap2C and sender.number == '6') \
	or (ct.SELECTED_MAP == testMap3C and sender.number == '7'):
		toggleEnabling('map')
		sender.background_color = '#ffffff'
		sender.font = ('<System>', sender.font[1])
		sender.tint_color = '#ffffff'
		ct.SELECTED_MAP = None
		mapSelectView['next_button'].enabled = False

def playerNb_touched(sender):
	ct.PLAYERS_NB = sender.selected_index+2
	
def playerName_touched(sender):
	if ct.onlineMulti and len(sender.text) <= 20:
		onlinePlayer['name'] = sender.text
	elif ct.onlineMulti and len(sender.text) > 20:
		text = ''
		for x in range(0,20):
			text += sender.text[x]
		onlinePlayer['name'] = text
	elif len(sender.text) <= 20:
		player['name'] = sender.text
	elif len(sender.text) > 20:
		text = ''
		for x in range(0,20):
			text += sender.text[x]
		player['name'] = text

if not ct.LAUNCHED:
	ct.LAUNCHED = True
	mainView = ui.load_view('mainUI')
	mapSelectView = ui.load_view('MapSelector')
	playerConfigView = ui.load_view('PlayerConfig')
	clSelectView = ui.load_view('ClassSelector')
	buildSelectView = ui.load_view('AbilityPicker')
	onlineLobbyView = ui.load_view('OnlineLobby')
	waitingScreenView = ui.load_view('WaitingScreen')
	mainView.present('fullscreen', hide_title_bar = True)
	soundPlayer = cl.SoundPlayer()
