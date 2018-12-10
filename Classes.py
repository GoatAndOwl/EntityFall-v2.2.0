#from scene import *
import Constants as ct
import GameInterface as gi
import Core as co
import random
import socket
import threading
import json
import time
import sound

class Cell():
	def __init__(self, cellType, coordX, coordY, spawnX, spawnY):
		if cellType == 'freeCell':
			self.IMG = SpriteNode('Images/Field/EmptyCell.GIF')
		elif cellType == 'VoidCell':
			self.IMG = SpriteNode('Images/Field/VoidCell.png')
		elif cellType == 'obstacle':
			self.IMG = SpriteNode('Images/Field/BoxIMG.GIF')
		elif cellType == 'BlueCell':
			self.IMG = SpriteNode('Images/Field/BlueCell.PNG')
		elif cellType == 'RedCell':
			self.IMG = SpriteNode('Images/Field/RedCell.PNG')
		
		self.effects = []
		self.effects_images = []
		self.cellType = cellType
		self.initialCellType = cellType
		self.coordX = coordX
		self.coordY = coordY
		self.IMG.anchor_point = (0, 1)
		self.IMG.x_scale = ct.CELL_X*0.01
		if cellType != 'obstacle':
			self.IMG.position = (spawnX, spawnY)
			self.IMG.y_scale = ct.CELL_Y*0.01
		else:
			self.IMG.position = (spawnX, spawnY+14*(1+ct.CELL_Y/100))
			self.IMG.y_scale = ct.CELL_Y*0.01+0.2
			self.IMG.z_position = 3.0
		
	def draw(self, game):
		if self.cellType == 'freeCell':
			self.IMG.texture = Texture('Images/Field/EmptyCell.GIF')
			self.IMG.alpha = 1.0
		if self.cellType == 'VoidCell':
			self.IMG.texture = Texture('Images/Field/VoidCell.png')
			self.IMG.alpha = 1.0
		if self.cellType == 'BlueCell':
			self.IMG.texture = Texture('Images/Field/BlueCell.PNG')
			self.IMG.alpha = 1.0
		if self.cellType == 'RedCell':
			self.IMG.texture = Texture('Images/Field/RedCell.PNG')
			self.IMG.alpha = 1.0
		if self.cellType == 'SelectedCell':
			self.IMG.texture = Texture('Images/Field/SelectedCell.png')
			self.IMG.alpha = 1.0
		if self.cellType == 'hidenCell':
			self.IMG.texture = Texture('Images/Field/EmptyCell.GIF')
			self.IMG.alpha = 0.2
		if self.cellType == 'TargetedCell':
			self.IMG.texture = Texture('Images/Field/TargetedCell.PNG')
			self.IMG.alpha = 1.0
		
		x = []
		for effect in self.effects:
			if effect['duration'] > 0:
				if effect['name'] == 'SnowCover':
					if not effect['image']:
						effectIMG = SpriteNode('Images/Ground Effects/SnowCover.png')
						effectIMG.anchor_point = (0, 1)
						effectIMG.x_scale = 0.6
						effectIMG.y_scale = ct.CELL_Y*0.01
						effectIMG.position = (self.IMG.position[0], self.IMG.position[1])
						self.effects_images.append(effectIMG)
						effect['image'] = effectIMG
						game.add_child(effectIMG)
						game.IMGList.append(effectIMG)
				if effect['name'] == 'EmberMat':
					if not effect['image']:
						effectIMG = SpriteNode('Images/Ground Effects/EmberMat.png')
						effectIMG.anchor_point = (0, 1)
						effectIMG.z_position = 0.1
						effectIMG.x_scale = 0.6
						effectIMG.y_scale = ct.CELL_Y*0.01
						effectIMG.position = (self.IMG.position[0], self.IMG.position[1])
						effect['image'] = effectIMG
						self.effects_images.append(effect['image'])
						game.add_child(effect['image'])
						game.IMGList.append(effect['image'])
				if effect['name'] == 'LavaGusher':
					if not effect['image']:
						effectIMG = SpriteNode('Images/Ground Effects/LavaGusher.png')
						effectIMG.anchor_point = (0, 1)
						effectIMG.x_scale = 0.6
						effectIMG.y_scale = ct.CELL_Y*0.01
						effectIMG.position = (self.IMG.position[0], self.IMG.position[1])
						self.effects_images.append(effectIMG)
						effect['image'] = effectIMG
						game.add_child(effectIMG)
						game.IMGList.append(effectIMG)
				if effect['name'] == 'SmokeWall':
					if not effect['image']:
						effectIMG = SpriteNode('Images/Ground Effects/SmokeWall.PNG')
						effectIMG.anchor_point = (0, 1)
						effectIMG.z_position = 3.99
						effectIMG.x_scale = 0.6
						effectIMG.y_scale = ct.CELL_Y*0.01
						effectIMG.position = (self.IMG.position[0], self.IMG.position[1])
						self.effects_images.append(effectIMG)
						effect['image'] = effectIMG
						game.add_child(effectIMG)
						game.IMGList.append(effectIMG)		
				if effect['name'] == 'Hole':
					if not effect['image']:
						self.cellType = 'VoidCell'
						self.initialCellType = 'VoidCell'
						game.groundCells.remove(self)
						effect['image'] = 1
				if effect['name'] == 'DivineBarrier':
					if not effect['image']:
						effectIMG = SpriteNode('Images/Ground Effects/DivineBarrier.PNG') # à changer
						effectIMG.anchor_point = (0, 1)
						effectIMG.z_position = 0.1
						effectIMG.x_scale = 0.6
						effectIMG.y_scale = ct.CELL_Y*0.01
						effectIMG.position = (self.IMG.position[0], self.IMG.position[1])
						effect['image'] = effectIMG
						self.effects_images.append(effect['image'])
						game.add_child(effect['image'])
						game.IMGList.append(effect['image'])
						game.
				if effect['name'] == 'Entranchment':
					if not effect['image']:
						effectIMG = SpriteNode('Images/Ground Effects/Entranchment.PNG') # à changer
						effectIMG.anchor_point = (0, 1)
						effectIMG.z_position = 0.1
						effectIMG.x_scale = 0.6
						effectIMG.y_scale = ct.CELL_Y*0.01
						effectIMG.position = (self.IMG.position[0], self.IMG.position[1])
						effect['image'] = effectIMG
						self.effects_images.append(effect['image'])
						game.add_child(effect['image'])
						game.IMGList.append(effect['image'])
				if effect['name'] == 'ShieldProtection':
					if not effect['image']:
						effectIMG = SpriteNode('Images/Ground Effects/ShieldProtection.PNG') # à changer
						effectIMG.anchor_point = (0, 1)
						effectIMG.z_position = 0.1
						effectIMG.x_scale = 0.6
						effectIMG.y_scale = ct.CELL_Y*0.01
						effectIMG.position = (self.IMG.position[0], self.IMG.position[1])
						effect['image'] = effectIMG
						self.effects_images.append(effect['image'])
						game.add_child(effect['image'])
						game.IMGList.append(effect['image'])
				if effect['name'] == 'Sanctuary':
					if not effect['image']:
						effectIMG = SpriteNode('Images/Ground Effects/Sanctuary.PNG')
						effectIMG.anchor_point = (0, 1)
						effectIMG.z_position = 0.1
						effectIMG.x_scale = 0.6
						effectIMG.y_scale = ct.CELL_Y*0.01
						effectIMG.position = (self.IMG.position[0], self.IMG.position[1])
						effect['image'] = effectIMG
						self.effects_images.append(effect['image'])
						game.add_child(effect['image'])
						game.IMGList.append(effect['image'])
						
			elif effect['duration'] <= 0:
				if effect['image'] and effect['name'] != 'Hole':
					effect['image'].remove_from_parent()
					self.effects_images.remove(effect['image'])
					game.IMGList.remove(effect['image'])
					x.append(effect)
				elif effect['name'] == 'Hole':
					self.cellType = 'freeCell'
					self.initialCellType = 'freeCell'
					game.groundCells.append(self)
					x.append(effect)
					
		if len(x):
			for effect in x:
				self.effects.remove(effect)
				del effect
	
class Entity():
	def __init__(self):
		self.deathCount = 3
		self.type = None
		self.coordX = 0
		self.coordY = 0
		self.images = []
		self.IMG = None
		self.moveSteps = []
		self.stepY = 0
		self.totalMoves = []
		self.actualMove = 0
		self.oldOrientation = None
		self.lastMove = None
		self.isPlacing = False
		self.isMoving = False
		self.controller = None
		self.name = None
		self.source = None
		self.team = None
		self.actualType = None
		self.stats = {'health': None,
					  'MP': None,
					  'EP': None,
					  'orientation': None}
		self.Startstats = {'health': None,
					  'MP': None,
					  'EP': None,
					  'orientation': None}
		self.zoneCells = []
		self.abilities = []
		self.played_abilities = []
		self.played_turns = []
		self.passives = []
		self.effects = []
		self.hud = []
	
	def move(self, game):
		a = [1, 2, 1]
		if len(self.moveSteps): 
			self.isMoving = True
			move = self.moveSteps[0]
			if move == 'right' and self.actualMove < ct.CELL_X:
				self.IMG.position = (self.IMG.position[0]+2, self.IMG.position[1])
				self.actualMove += 2
			elif move == 'left' and self.actualMove < ct.CELL_X:
				self.IMG.position = (self.IMG.position[0]-2, self.IMG.position[1])
				self.actualMove += 2
			elif move == 'top' and self.actualMove < 60:
				self.IMG.position = (self.IMG.position[0], self.IMG.position[1]+a[self.stepY])
				self.actualMove += 2
				if self.stepY == 2:
					self.stepY = 0
				else:
					self.stepY += 1
			elif move == 'bottom' and self.actualMove < 60:
				self.IMG.position = (self.IMG.position[0], self.IMG.position[1]-a[self.stepY])
				self.actualMove += 2
				if self.stepY == 2:
					self.stepY = 0
				else:
					self.stepY += 1
			
			if self.name == 'Thermal Mage':
				if self.actualType == 'ice':
					self.images = [self.imagesIce]
				elif self.actualType == 'fire':
					self.images = [self.imagesFire]
			if len(self.images) and not self.name == 'Paladin':
				if self.actualMove == 16: # or self.actualMove == 32:
					self.IMG.texture = Texture(self.images[0][1])
				elif self.actualMove == 32: #or self.actualMove == 28 or self.actualMove == 44:
					self.IMG.texture = Texture(self.images[0][0])
				elif self.actualMove == 46: #16 or self.actualMove == 46:
					self.IMG.texture = Texture(self.images[0][2])
			if self.actualMove == 60:
				self.actualMove = 0
				if len(self.images):
					self.IMG.texture = Texture(self.images[0][0])
				self.totalMoves.append(self.moveSteps[0])
				del self.moveSteps[0]
				
		else:
			self.isMoving = False
		if len(self.hud):
			self.hud[0].position = (self.IMG.position[0]+30, self.IMG.position[1]+3)
			self.hud[6].position = (self.IMG.position[0], self.IMG.position[1]-23)
			self.hud[7].position = (self.IMG.position[0]+30, self.IMG.position[1]-7)
			self.hud[8].position = (self.IMG.position[0]+3, self.IMG.position[1]-9.25)
			
	def classSetup(self, abilities, passives):
		for ability in abilities:
			if ability == 'ability_1':
				self.abilities.append(self.Ability1)
			elif ability == 'ability_2':
				self.abilities.append(self.Ability2)
			elif ability == 'ability_3':
				self.abilities.append(self.Ability3)
			elif ability == 'ability_4':
				self.abilities.append(self.Ability4)
			elif ability == 'ability_5':
				self.abilities.append(self.Ability5)
			elif ability == 'ability_6':
				self.abilities.append(self.Ability6)
			elif ability == 'ability_7':
				self.abilities.append(self.Ability7)
			elif ability == 'ability_8':
				self.abilities.append(self.Ability8)
			elif ability == 'ability_9':
				self.abilities.append(self.Ability9)
			elif ability == 'ability_10':
				self.abilities.append(self.Ability10)
			
		for passive in passives:
			if passive == 'passive_1':
				self.passives.append(self.Passive1)
			elif passive == 'passive_2':
				self.passives.append(self.Passive2)
			elif passive == 'passive_3':
				self.passives.append(self.Passive3)
			elif passive == 'passive_4':
				self.passives.append(self.Passive4)
			elif passive == 'passive_5':
				self.passives.append(self.Passive5)
			elif passive == 'passive_6':
				self.passives.append(self.Passive6)
		
	def passiveCheck(self):
		for passive in self.passives:
			passive()
	
	def effectsCheck(self, situation, game):
		x = 1
		localCell = game.cellScan(self.coordX, self.coordY)
		if situation[0] == 'turnBegin':
			for entity in game.entityList:
				for effect in entity.effects:
					if effect['source'] == self and effect['duration_type'] == 'until_turns':
						effect['duration'] -= 1
				entity.effectsClean()
		
		for effect in self.effects:
			if situation[0] == 'attacking': 
				if effect['situation'] == 'attacking':
					if effect['type'] == 'damage_%':
						x += effect['value']
					if effect['duration_type'] == 'next_attack':
						effect['duration'] -= 1
			
			elif situation[0] == 'defending':
				for effect in localCell.effects:
					if effect['name'] == 'ShieldProtection' and effect['source'].team == self.team:
						x += effect['value']
					if effect['name'] == 'Entranchment' and effect['source'].team == self.team:
						x += effect['value(2)']
				if situation[1] == 'front' and effect['situation'] == 'defending_front':
					if effect['type'] == 'damage_%':
						x += effect['value']
					if effect['duration_type'] == 'next_defense':
						effect['duration'] -= 1
						
				elif effect['situation'] == 'defending':
					if effect['type'] == 'damage_%':
						x += effect['value']
			
			elif situation[0] == 'healing':
				if 'healing' in effect['situation']:
					if effect['type'] == 'heal_%':
						x += effect['value']
			
			elif situation[0] == 'healed':
				if 'healed' in effect['situation']:
					if effect['type'] == 'heal_%':
						x += effect['value']
						
			elif situation[0] == 'turnBegin':
				if effect['situation'] == 'turnBegin':
					if effect['type'] == 'MPboost':
						self.stats['MP'] += effect['value']
					if effect['type'] == 'EPboost':
						self.stats['EP'] += effect['value']
					elif effect['type'] == 'HPboost':
						if effect['name'] == 'DivineFury':
							x = 0
							for effect2 in self.effects:
								if effect2['name'] == 'impious':
									x += 1
							self.stats['health'] += effect['value']*x
							game.valueDraw(self, effect['value']*x, 'top')
						else:
							self.stats['health'] += effect['value']
							if effect['value']:
								game.valueDraw(self, effect['value'], 'top')
							if effect['name'] == 'thermalCasualties':
								effect['value'] = 0
			
			elif situation[0] == 'turnEnd':
				game.majorCheck(self, situation=situation[0])
				if effect['duration_type'] == 'next_attack':
					effect['duration'] = 0
		
		if situation[0] == 'turnBegin':
			for ligne in game.map:
				for cell in ligne:
					for effect in cell.effects:
						if effect['source'] == self:	
							if effect['duration_type'] == 'until_turns':
								effect['duration'] -= 1
							elif effect['duration_type'] == 'next_walk':
								effect['duration'] = 0
		
		for effect in localCell.effects:
			if effect['situation'] == 'Walk&Stay' or \
			(effect['situation'] == 'Walk' and (situation[0] == 'isMoving' or \
			situation[0] == 'isPushed')) or \
			(effect['situation'] == 'Stay' and situation[0] == 'turnBegin') or \
			((effect['type'] == 'healing' or effect['type'] == 'healing&healed') and \
			situation[0] == 'healing') or \
			((effect['type'] == 'healed' or effect['type'] == 'healing&healed') and \
			situation[0] == 'healed'):
				if effect['type'] == 'HPboost':
					self.stats['health'] += effect['value']
				elif effect['type'] == 'MPboost':
					self.stats['MP'] += effect['value']
				if effect['duration_type'] == 'next_walk':
					effect['duration'] -= 1	
				if effect['name'] == 'Entranchment' and effect['source'].team == self.team:
					if self.stats['health']+effect['value(1)'] <= self.Startstats['health']:
						self.stats['health'] += effect['value(1)']
						if effect['value(1)']:
							game.valueDraw(self, effect['value(1)'], 'top')
					else:
						self.stats['health'] = self.Startstats['health']
						if effect['value(1)']:
							game.valueDraw(self, effect['value(1)'], 'top')
						
				elif effect['name'] == 'Sanctuary' and effect['source'].team == self.team:
					if situation[0] in effect['type']:
						x += effect['value[1]']
					elif situation[0] == 'turnBegin':
						if self.stats['health']+effect['value[2]'] <= self.Startstats['health']:
							self.stats['health'] += effect['value[2]']
							if effect['value[2]']:
								game.valueDraw(self, effect['value[2]'], 'top')
						else:
							self.stats['health'] = self.Startstats['health']
							if effect['value[2]']:
								game.valueDraw(self, effect['value[2]'], 'top')
			
			elif situation[0] == 'attacking':
				if effect['name'] == 'Sanctuary':
					effect['source'].ImpiousGen(self, 4)							
		return(x)
		
	def effectsClean(self):
		x = []
		for effect in self.effects:
			if effect['duration'] <= 0:
				x.append(effect)
		
		for y in x:
			self.effects.remove(y)
			del y
	
	def action_sender(self, type, coords):
		if ct.onlineMulti:
			if type == 'ability_1':
				action = {'type': 'ability',
						  'name': '1',
						  'coords': coords}
			elif type == 'ability_2':
				action = {'type': 'ability',
						  'name': '2',
						  'coords': coords}
			elif type == 'ability_3':
				action = {'type': 'ability',
						  'name': '3',
						  'coords': coords}
			elif type == 'ability_4':
				action = {'type': 'ability',
						  'name': '4',
						  'coords': coords}
			elif type == 'ability_5':
				action = {'type': 'ability',
						  'name': '5',
						  'coords': coords}
			elif type == 'ability_6':
				action = {'type': 'ability',
						  'name': '6',
						  'coords': coords}
			elif type == 'ability_7':
				action = {'type': 'ability',
						  'name': '7',
						  'coords': coords}
			elif type == 'ability_8':
				action = {'type': 'ability',
						  'name': '8',
						  'coords': coords}
			elif type == 'ability_9':
				action = {'type': 'ability',
						  'name': '9',
						  'coords': coords}
			elif type == 'ability_10':
				action = {'type': 'ability',
						  'name': '10',
						  'coords': coords}
			ct.CLIENT.dataList_to_send.append(action)
	
		
class Controller():
	def __init__(self, game, teamNb, entity, name, id):
		self.entity = entity
		self.entity.controller = self
		self.id = id
		self.game = game
		self.selectedAbility = None
		self.selectedCell = None
		self.lastCell = None
		self.isPlaying = False 
		self.isMoving = False
		self.name = name
		
		
		if teamNb == 1:
			self.team = 'blue'
		elif teamNb == 2:
			self.team = 'red'
	
	def turnControl(self):
		self.selectedCell = self.game.selectedCell
		self.lastCell = self.game.lastCell
		if self.id == ct.CLIENT_ID:
			if self.entity.isPlacing:
				x = 0
				for cell in self.game.groundCells:
					if cell.cellType == 'SelectedCell':
						if (cell.initialCellType == 'BlueCell' \
							 and self.team == 'blue') or \
							(cell.initialCellType == 'RedCell' \
							 and self.team == 'red'):
							for entity in self.game.entityList:
								if entity.coordX == cell.coordX and \
								entity.coordY == cell.coordY:
									x = 1
							if not x:
								self.entity.IMG.position = (cell.IMG.position[0], 
								cell.IMG.position[1]+30)
								self.entity.coordX = cell.coordX
								self.entity.coordY = cell.coordY
								if ct.onlineMulti:
									action = {'type': 'placement',
											  'name': None,
											  'coords':(cell.coordX, cell.coordY)}
									ct.CLIENT.dataList_to_send.append(action)
							
				if ct.singlePlayer:		
					if self.game.play_button_touched and self.entity.isPlacing:
						self.entity.isPlacing = False
						for cell2 in self.game.groundCells:
							if cell2.cellType == 'BlueCell' or cell2.cellType == 'RedCell':
								cell2.initialCellType = 'freeCell'
								cell2.cellType = 'freeCell'
			
			elif self.isPlaying:	
				if not self.isMoving:
					if self.selectedAbility != None:
						self.selectedAbility(self.selectedCell, self.lastCell, self.game)
					elif self.selectedCell:
						if self.selectedCell.coordX != self.entity.coordX or \
						self.selectedCell.coordY != self.entity.coordY:
							a = self.game.pathMultiplicator(self.selectedCell, self.entity)
							if a:
								if a[1] == 'left':
									self.entity.stats['orientation'] = 'right'
								elif a[1] == 'right':
									self.entity.stats['orientation'] = 'left'
								elif a[1] == 'top':
									self.entity.stats['orientation'] = 'bottom'
								elif a[1] == 'bottom':
									self.entity.stats['orientation'] = 'top'
								if ct.onlineMulti and self.entity.stats['orientation'] != \
								self.entity.oldOrientation:
									action = {'type': 'orientation',
											'name': self.entity.stats['orientation'],
											'coords': None}
									ct.CLIENT.dataList_to_send.append(action)
								self.entity.oldOrientation = self.entity.stats['orientation']
									
						elif self.selectedCell.coordX == self.entity.coordX and \
						self.selectedCell.coordY == self.entity.coordY:
							self.isMoving = True
							self.game.touchX = self.selectedCell.IMG.position[0]+(ct.CELL_X/2)
							self.game.touchY = self.selectedCell.IMG.position[1]-(ct.CELL_Y/2)
							print('isMoving')
					
				elif self.isMoving and not self.entity.targetedCells:
					if not self.game.screen_touched:
						self.isMoving = False
						self.game.selectedCell = None
						self.game.lastCell = None
						print('is not moving anymore')
					elif self.selectedCell:
						if self.game.screen_touched and self.selectedCell.cellType == 'SelectedCell':
							if self.game.touchY+ct.CELL_Y/2 > self.game.touchY2 > self.game.touchY-ct.CELL_Y/2:
								if self.game.touchX+ct.CELL_X/2 < self.game.touchX2 < \
								self.game.touchX+ct.CELL_X*1.5 and self.entity.stats['MP'] > 0 and \
								self.game.cellScan(self.entity.coordX+1, self.entity.coordY) in \
								self.game.groundCells and not \
								self.game.entityScan(self.entity.coordX+1, self.entity.coordY):
									self.entity.stats['orientation'] = 'right'
									self.entity.moveSteps.append('right')
									self.entity.coordX += 1
									self.game.touchX += ct.CELL_X
									self.entity.stats['MP'] -= 1
									self.entity.passiveCheck()
									self.entity.effectsCheck(['isMoving'], self.game)
									self.entity.effectsClean()
									if ct.onlineMulti:
										action = {'type': 'move',
												'name': 'right',
												'coords': None}
										ct.CLIENT.dataList_to_send.append(action)
									
								if self.game.touchX-ct.CELL_X/2 > self.game.touchX2 > \
								self.game.touchX-ct.CELL_X*1.5 and self.entity.stats['MP'] > 0 and \
								self.game.cellScan(self.entity.coordX-1, self.entity.coordY) in \
								self.game.groundCells and not \
								self.game.entityScan(self.entity.coordX-1, self.entity.coordY):
									self.entity.stats['orientation'] = 'left'
									self.entity.moveSteps.append('left')
									self.entity.coordX -= 1
									self.game.touchX -= ct.CELL_X
									self.entity.stats['MP'] -= 1
									self.entity.passiveCheck()
									self.entity.effectsCheck(['isMoving'], self.game)
									self.entity.effectsClean()
									if ct.onlineMulti:
										action = {'type': 'move',
												'name': 'left',
												'coords': None}
										ct.CLIENT.dataList_to_send.append(action)
									
							elif self.game.touchX+ct.CELL_X/2 > self.game.touchX2 > self.game.touchX-ct.CELL_X/2:
								if self.game.touchY+ct.CELL_Y/2 < self.game.touchY2 < \
								self.game.touchY+ct.CELL_Y*1.5 and self.entity.stats['MP'] > 0 and \
								self.game.cellScan(self.entity.coordX, self.entity.coordY-1) in \
								self.game.groundCells and not \
								self.game.entityScan(self.entity.coordX, self.entity.coordY-1):
									self.entity.stats['orientation'] = 'top'
									self.entity.moveSteps.append('top')
									self.entity.coordY -= 1
									self.game.touchY += ct.CELL_Y
									self.entity.stats['MP'] -= 1
									self.entity.passiveCheck()
									self.entity.effectsCheck(['isMoving'], self.game)
									self.entity.effectsClean()
									if ct.onlineMulti:
										action = {'type': 'move',
												'name': 'top',
												'coords': None}
										ct.CLIENT.dataList_to_send.append(action)
									
								if self.game.touchY-ct.CELL_Y/2 > self.game.touchY2 > \
								self.game.touchY-ct.CELL_Y*1.5 and self.entity.stats['MP'] > 0 and \
								self.game.cellScan(self.entity.coordX, self.entity.coordY+1) in \
								self.game.groundCells and not \
								self.game.entityScan(self.entity.coordX, self.entity.coordY+1):
									self.entity.stats['orientation'] = 'bottom'
									self.entity.moveSteps.append('bottom')
									self.entity.coordY += 1
									self.game.touchY -= ct.CELL_Y
									self.entity.stats['MP'] -= 1
									self.entity.passiveCheck()
									self.entity.effectsCheck(['isMoving'], self.game)
									self.entity.effectsClean()
									if ct.onlineMulti:
										action = {'type': 'move',
												'name': 'bottom',
												'coords': None}
										ct.CLIENT.dataList_to_send.append(action)

		elif self.id != ct.CLIENT_ID:
			if len(ct.CLIENT.data_received):
				action = ct.CLIENT.data_received[0]
				if action['type'] == 'turnEnd':
						self.game.play_button_touched = True
						ct.CLIENT.data_received.remove(action)
						del action
				elif self.game.game_phase == 'Placement':
					if action['type'] == 'placement' and self.game.game_phase == 'Placement':
						cell = self.game.cellScan(action['coords'][0], action['coords'][1])
						self.entity.IMG.position = (cell.IMG.position[0]+3, 
						cell.IMG.position[1]+20)
						self.entity.coordX = cell.coordX
						self.entity.coordY = cell.coordY
						ct.CLIENT.data_received.remove(action)
						del action
				
				elif self.game.game_phase == 'Fight':
					if action['type'] == 'orientation':
						self.entity.stats['orientation'] = action['name']
						ct.CLIENT.data_received.remove(action)
						del action
					elif action['type'] == 'move':
						if action['name'] == 'right':
							self.entity.stats['orientation'] = 'right'
							self.entity.moveSteps.append('right')
							self.entity.coordX += 1
							self.entity.stats['MP'] -= 1
							self.entity.passiveCheck()
							self.entity.effectsCheck(['isMoving'], self.game)
							self.entity.effectsClean()
						elif action['name'] == 'left':
							self.entity.stats['orientation'] = 'left'
							self.entity.moveSteps.append('left')
							self.entity.coordX -= 1
							self.entity.stats['MP'] -= 1
							self.entity.passiveCheck()
							self.entity.effectsCheck(['isMoving'], self.game)
							self.entity.effectsClean()
						elif action['name'] == 'top':
							self.entity.stats['orientation'] = 'top'
							self.entity.moveSteps.append('top')
							self.entity.coordY -= 1
							self.entity.stats['MP'] -= 1
							self.entity.passiveCheck()
							self.entity.effectsCheck(['isMoving'], self.game)
							self.entity.effectsClean()
						elif action['name'] == 'bottom':
							self.entity.stats['orientation'] = 'bottom'
							self.entity.moveSteps.append('bottom')
							self.entity.coordY += 1
							self.entity.stats['MP'] -= 1
							self.entity.passiveCheck()
							self.entity.effectsCheck(['isMoving'], self.game)
							self.entity.effectsClean()
						ct.CLIENT.data_received.remove(action)
						del action
					
					elif action['type'] == 'ability':
						x = int(action['name'])
						if x == 1:
							self.selectedAbility = self.entity.Ability1
						elif x == 2:
							self.selectedAbility = self.entity.Ability2
						elif x == 3:
							self.selectedAbility = self.entity.Ability3
						elif x == 4:
							self.selectedAbility = self.entity.Ability4
						elif x == 5:
							self.selectedAbility = self.entity.Ability5
						elif x == 6:
							self.selectedAbility = self.entity.Ability6
						elif x == 7:
							self.selectedAbility = self.entity.Ability7
						elif x == 8:
							self.selectedAbility = self.entity.Ability8
						elif x == 9:
							self.selectedAbility = self.entity.Ability9
						elif x == 10:
							self.selectedAbility = self.entity.Ability10
						self.lastCell = self.game.cellScan(action['coords'][0], action['coords'][1])
						self.selectedAbility(None, self.lastCell, self.game)
						self.selectedAbility(self.lastCell, self.lastCell, self.game)
						self.selectedAbility(None, self.lastCell, self.game)
						self.selectedAbility = None
						ct.CLIENT.data_received.remove(action)
						del action
		

class Client(threading.Thread):
	def __init__(self, addr, state):
		threading.Thread.__init__(self)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print(addr)
		self.sock.connect(addr)
		self.isStarted = False
		self.isWorking = True
		self.state = state
		self.last_msg = None
		self.data_to_send = None
		self.dataList_to_send = []
		self.data_received = []
		self.start()
	
	def sleep(self,x):
		time.sleep(x)
	
	def run(self):
		while self.isWorking:
			if self.state == 'New Coonection':
				if not self.last_msg:
					self.last_msg = bytes.decode(self.sock.recv(1024))
				while not self.data_to_send:
					continue
				if self.data_to_send:
					self.data_to_send = str.encode(json.dumps(self.data_to_send))
					self.sock.sendall(self.data_to_send)
					
					self.data_to_send = None
					self.last_msg = json.loads(bytes.decode(self.sock.recv(8192)))
					if len(self.last_msg) >= 3:
						if self.last_msg[2] == 'Waiting' or self.last_msg[2] == 'Waiting for Start':
							self.state = self.last_msg[2]
							ct.CLIENT_ID = self.last_msg[3]
					
			elif self.state == 'Waiting':
				msg = str.encode('nothing')
				self.sock.sendall(msg)
				
				self.last_msg = json.loads(bytes.decode(self.sock.recv(8192)))
				if self.last_msg[0] == 'refresh':
					gi.refresh_Waiting(self.last_msg[1])
				elif self.last_msg[0] == 'setting up Game':
					self.state = 'Sending Up'
					self.data_to_send = None
					gi.refresh_Waiting(self.last_msg[1])
					for entity in ct.PLAYERS:
						if entity['id'] == ct.CLIENT_ID:
							gi.player = entity
							break
					
					gi.mainView.remove_subview(gi.waitingScreenView)
					gi.mainView.add_subview(gi.clSelectView)
					gi.clSelectView['playerWord'].text = gi.player['name']+', choose your class:'
					gi.clSelectView['next_button'].enabled = False
			
			elif self.state == 'Waiting for Start':
				if not self.data_to_send:
					msg = str.encode('nothing')
					self.sock.sendall(msg)
					
				elif self.data_to_send:
					self.sock.sendall(self.data_to_send)
					
				self.last_msg = json.loads(bytes.decode(self.sock.recv(8192)))
				if self.last_msg[0] == 'refresh':
					gi.refresh_Waiting(self.last_msg[1])
					x, y = 0, 0
					for entity in ct.PLAYERS:
						if entity['team'] == 1 and x == 0:
							x = 1
						if entity['team'] == 2 and y == 0:
							y = 1
							
					if x and y and not self.data_to_send:
						if not gi.waitingScreenView['next_button'].enabled:
							gi.waitingScreenView['next_button'].enabled = True
				
				elif self.last_msg[0] == 'setting up Game':
					self.state = 'Sending Up'
					self.data_to_send = None
					gi.refresh_Waiting(self.last_msg[1])
					for entity in ct.PLAYERS:
						if entity['id'] == ct.CLIENT_ID:
							gi.player = entity
							break
					
					gi.mainView.remove_subview(gi.waitingScreenView)
					gi.mainView.add_subview(gi.clSelectView)
					gi.clSelectView['playerWord'].text = gi.player['name']+', choose your class:'
					gi.clSelectView['next_button'].enabled = False
					
			elif self.state == 'Sending Up':
				if not self.isStarted:
					while not self.data_to_send and self.state == 'Sending Up':
						continue
					if self.data_to_send:
						print(self.data_to_send)
						self.sock.sendall(self.data_to_send)
						self.data_to_send = None
					
				else:
					if len(self.dataList_to_send):
						print(self.dataList_to_send)
						self.data_to_send = str.encode(json.dumps(self.dataList_to_send[0]))
						self.sock.sendall(self.data_to_send)
						print(self.data_to_send)
						
						#if self.dataList_to_send[0]['type'] == 'turnEnd':
						#	self.state = None
						self.dataList_to_send.remove(self.dataList_to_send[0])
						self.data_to_send = None
			
			elif self.state == 'Receiving Up':
				print('start receiving data')
				self.last_msg = bytes.decode(self.sock.recv(8192))
				a = co.uncompose_msg(self.last_msg)
				for x in a:
					self.last_msg = json.loads(x)
					if not self.isStarted:
						if self.last_msg[0] == 'add entity':
							for entity in ct.PLAYERS:
								if entity['name'] == self.last_msg[1] and \
								entity['id'] == self.last_msg[5]:
									entity['class'] = self.last_msg[2]
									entity['abilities'] = self.last_msg[3]
									entity['passives'] = self.last_msg[4]
									entity['randN'] = self.last_msg[6]
									self.sock.sendall(str.encode(json.dumps({'type':'ok'})))
									break
									
						elif self.last_msg[0] == 'play order':
							for entity2 in self.last_msg[1]:
								for entity3 in ct.PLAYERS:
									if entity3['name'] == entity2[0] and \
									entity3['id'] == entity2[1]:
										ct.PLAYERS.remove(entity3)
										ct.PLAYERS.append(entity3)
										break
										
							print(ct.PLAYERS)
							self.sock.sendall(str.encode(json.dumps({'type':'ok'})))
							
						
						elif self.last_msg[0] == 'start Game':
							gi.mainView.close()
							gi.mainView.wait_modal()
							co.run_game()
							print('game Started')
							self.isStarted = True
							if ct.PLAYERS[0]['id'] == ct.CLIENT_ID:
								self.state = 'Sending Up'
								self.last_msg = None
							else:
								self.state = 'Receiving Up'
					
					elif self.isStarted:
						self.data_received.append(self.last_msg)
						print(self.last_msg)
						if self.last_msg['type'] == 'turnEnd':
							self.state = None
						self.last_msg = None


class SoundPlayer():
	def __init__(self):
		ct.SOUND_PLAYER = self
		self.run()
	
	def run(self):
		self.music = sound.Player('Musics/EntityFall-menu.m4a')
		while ct.LAUNCHED:
			if not ct.STARTED and ct.LAUNCHED:
				self.music.play()
			else:
				self.music.stop()
				break
		self.music.stop()
		self.music = sound.Player('Musics/EntityFall-fight.m4a')
		while ct.STARTED:
			self.music.play()
		self.music.stop()
				
#==========================================

from Viking import *
from ThermalMage import *
from Marshal import *
from Paladin import *

#==========================================


# realiser un systeme d'enregistrement des actions permettrait de gérer les cooldowns de capacités, 
# en attendant: presence d'un systeme archaique et conçu sur du cas par cas (toujours pour les 
# cooldowns)
# faire attention: certaines capacités buguent sur le mode solo (actif 4 VK) et le mode solo ne fonctionne pas 
# bien
