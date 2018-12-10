from scene import *
from Classes import *
import Constants as ct
import random

class Viking(Entity):
	def __init__(self, player):
		Entity.__init__(self)
		self.images = [['Images/Viking/VikingFace0-0.png', 'Images/Viking/VikingFace0-1.png', 
		'Images/Viking/VikingFace0-2.png'], 
		[None, None], 
		['Images/Viking/VikingFace2-1.PNG', 'Images/Viking/VikingFace2-2.PNG']]
		self.IMG = SpriteNode(self.images[0][0])
		self.IMG.anchor_point = (0, 1)
		self.IMG.x_scale = 0.01*ct.CELL_X
		self.IMG.y_scale = 0.01*ct.CELL_Y+0.15
		self.IMG.position = (-250,-250)
		self.IMG.z_position = 2.0
		self.classSetup(player['abilities'], player['passives'])
		self.targetedCells = None
		self.name = 'Viking'
		self.team = player['team']
		self.stats = {'health': ct.VK_STATS['health'],
					  'MP': ct.VK_STATS['MP'],
					  'EP': ct.VK_STATS['EP'],
					  'orientation': None}
		self.Startstats = {'health': ct.VK_STATS['health'],
					  'MP': ct.VK_STATS['MP'],
					  'EP': ct.VK_STATS['EP'],
					  'orientation': None}
			
	def Ability1(self, selectedcell, lastCell, game):
		x = 0
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.VK_ABILITIES['ability_1']['minRange'],
								 ct.VK_ABILITIES['ability_1']['maxRange'],
								 True, False)
			game.hideCells(self.targetedCells)
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.VK_ABILITIES['ability_1']['EPcost'] and \
		self.stats['MP'] >= ct.VK_ABILITIES['ability_1']['MPcost']:
			for ability in self.played_abilities:
				if ability == 'ability_1':
					x += 1
					
			if lastCell in self.targetedCells and x < 2:
				for entity in game.entityList:
					if entity.coordX == lastCell.coordX and \
					entity.coordY == lastCell.coordY:
						entity.stats['health'] += game.valueCalculator(self, entity,
						ct.VK_ABILITIES['ability_1']['value'], False, True, 'ability_1')
						self.stats['EP'] -= ct.VK_ABILITIES['ability_1']['EPcost']
						self.stats['MP'] -= ct.VK_ABILITIES['ability_1']['MPcost']
						for button in game.buttons:
							if button[2]:
								button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
								button[2] = False
								self.action_sender('ability_1', [lastCell.coordX, lastCell.coordY])
								game.active_player.selectedAbility = None
								game.hideCells(self.targetedCells)
								self.targetedCells = None
								game.lastCell = None
								game.selectedcell = None
								self.played_abilities.append('ability_1')
								self.effectsClean()
								
	def Ability2(self, selectedcell, lastCell, game):
		hit = False
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
										ct.VK_ABILITIES['ability_2']['minRange'],
										ct.VK_ABILITIES['ability_2']['maxRange'],
										True, False)
			game.hideCells(self.targetedCells)
		
		elif selectedcell and len(self.played_abilities) and self.Passive3 in self.passives:
			if self.played_abilities[len(self.played_abilities)-1] \
			== 'ability_1':
				path = game.pathMultiplicator(selectedcell, self)
				for cell in game.groundCells:
					if path[1] == 'right' or path[1] == 'left':
						if cell.coordX == selectedcell.coordX and \
						(cell.coordY-1 == selectedcell.coordY or \
						cell.coordY+1 == selectedcell.coordY):
							if not cell in self.zoneCells:
								self.zoneCells.append(cell)
						elif cell in self.zoneCells:
							self.zoneCells.remove(cell)
					elif path[1] == 'top' or path[1] == 'bottom':
						if cell.coordY == selectedcell.coordY and \
						(cell.coordX-1 == selectedcell.coordX or \
						cell.coordX+1 == selectedcell.coordX):
							if not cell in self.zoneCells:
								self.zoneCells.append(cell)
						elif cell in self.zoneCells:
							self.zoneCells.remove(cell)
							
				for cell in self.zoneCells:
					if selectedcell in self.targetedCells:
						cell.cellType = 'SelectedCell'
		
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.VK_ABILITIES['ability_2']['EPcost'] and \
		self.stats['MP'] >= ct.VK_ABILITIES['ability_2']['MPcost']:
			if lastCell in self.targetedCells:
				for entity in game.entityList:
					for cell2 in self.zoneCells:
						if entity.coordX == cell2.coordX and \
						entity.coordY == cell2.coordY:
							entity.stats['health'] += game.valueCalculator(self, entity, ct.VK_ABILITIES['ability_2']['value'], False, False, 'ability_2')
							hit = True
							
					if entity.coordX == lastCell.coordX and \
					entity.coordY == lastCell.coordY:
						entity.stats['health'] += game.valueCalculator(self, entity, ct.VK_ABILITIES['ability_2']['value'], False, True, 'ability_2')
						hit = True
				
				if hit:
					self.stats['EP'] -= ct.VK_ABILITIES['ability_2']['EPcost']
					self.stats['MP'] -= ct.VK_ABILITIES['ability_2']['MPcost']
					for button in game.buttons:
						if button[2]:
							button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
							button[2] = False
							self.action_sender('ability_2', [lastCell.coordX, lastCell.coordY])
							game.active_player.selectedAbility = None
							game.hideCells(self.targetedCells)
							self.targetedCells = None
							game.lastCell = None
							game.selectedcell = None
							self.zoneCells = []
							self.played_abilities.append('ability_2')
							self.effectsClean()
							
		
	def Ability3(self, selectedcell, lastCell, game):
		x = 0
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.VK_ABILITIES['ability_3']['minRange'],
								 ct.VK_ABILITIES['ability_3']['maxRange'],
								 True, False)
			game.hideCells(self.targetedCells)
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.VK_ABILITIES['ability_3']['EPcost'] and \
		self.stats['MP'] >= ct.VK_ABILITIES['ability_3']['MPcost']:
			
			for effect in self.effects:
				if effect['name'] == 'charge':
					x += 1
			
			if lastCell in self.targetedCells:
				for entity in game.entityList:
					if entity.coordX == lastCell.coordX and \
					entity.coordY == lastCell.coordY:
						
						if x < 3:
							entity.stats['health'] += game.valueCalculator(self, entity,
							ct.VK_ABILITIES['ability_3']['value'], False, True, 'ability_3')
						else:
							entity.stats['health'] += game.valueCalculator(self, entity,
							ct.VK_ABILITIES['ability_3']['value']*2, False, True, 'ability_3')
							
						self.stats['EP'] -= ct.VK_ABILITIES['ability_3']['EPcost']
						self.stats['MP'] -= ct.VK_ABILITIES['ability_3']['MPcost']
						for button in game.buttons:
							if button[2]:
								button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
								button[2] = False
								self.action_sender('ability_3', [lastCell.coordX, lastCell.coordY])
								game.active_player.selectedAbility = None
								game.hideCells(self.targetedCells)
								self.targetedCells = None
								game.lastCell = None
								game.selectedcell = None
								self.played_abilities.append('ability_3')
								self.effectsClean()
								
		
	def Ability4(self, selectedcell, lastCell, game):
		x = 0
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.VK_ABILITIES['ability_4']['minRange'],
								 ct.VK_ABILITIES['ability_4']['maxRange'],
								 True, False)
			game.hideCells(self.targetedCells)
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.VK_ABILITIES['ability_4']['EPcost'] and \
		self.stats['MP'] >= ct.VK_ABILITIES['ability_4']['MPcost']:
			if lastCell in self.targetedCells:
				for effect in self.effects:
					if effect['name'] == 'toughness':
						x = 1
						
				for entity in game.entityList:
					if entity.coordX == lastCell.coordX and \
					entity.coordY == lastCell.coordY and not x:
						toughness1 = {'name': 'toughness',
									  'type': 'MPboost',
									  'situation': 'turnBegin',
									  'value': 1,
									  'duration_type': 'until_turns',
									  'duration': 1,
									  'source': self} # utile uniquement pour une future application d'affichage d'effet
						toughness2 = {'name': 'toughness',
									  'type': 'MPboost',
									  'situation': 'turnBegin',
									  'value': 1,
									  'duration_type': 'until_turns',
									  'duration': 2,
									  'source': self}
						self.effects.append(toughness1)
						self.effects.append(toughness2)
						self.stats['MP'] += 2
						self.stats['EP'] -= ct.VK_ABILITIES['ability_4']['EPcost']
						self.stats['MP'] -= ct.VK_ABILITIES['ability_4']['MPcost']
						for button in game.buttons:
							if button[2]:
								button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
								button[2] = False
								self.action_sender('ability_4', [lastCell.coordX, lastCell.coordY])
								game.active_player.selectedAbility = None
								game.hideCells(self.targetedCells)
								self.targetedCells = None
								game.lastCell = None
								game.selectedcell = None
								self.played_abilities.append('ability_4')
								self.effectsClean()
								
						
	def Ability5(self, selectedcell, lastCell, game):
		x = 0
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.VK_ABILITIES['ability_5']['minRange'],
								 ct.VK_ABILITIES['ability_5']['maxRange'],
								 True, False)
			game.hideCells(self.targetedCells)
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.VK_ABILITIES['ability_5']['EPcost'] and \
		self.stats['MP'] >= ct.VK_ABILITIES['ability_5']['MPcost']:
			
			for effect in self.effects:
				if effect['name'] == 'charge':
					x += 1
			
			if lastCell in self.targetedCells:
				for entity in game.entityList:
					if entity.coordX == lastCell.coordX and \
					entity.coordY == lastCell.coordY:
						entity.stats['health'] += game.valueCalculator(self, entity,
						ct.VK_ABILITIES['ability_5']['value'], False, True, 'ability_5')
						game.collisionCalculator(entity, 1+x, self, False)
						self.stats['EP'] -= ct.VK_ABILITIES['ability_5']['EPcost']
						self.stats['MP'] -= ct.VK_ABILITIES['ability_5']['MPcost']
						for button in game.buttons:
							if button[2]:
								button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
								button[2] = False
								self.action_sender('ability_5', [lastCell.coordX, lastCell.coordY])
								game.active_player.selectedAbility = None
								game.hideCells(self.targetedCells)
								self.targetedCells = None
								game.lastCell = None
								game.selectedcell = None
								self.played_abilities.append('ability_5')
								self.effectsClean()
								
	
	def Ability6(self, selectedcell, lastCell, game):
		x = 0
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.VK_ABILITIES['ability_6']['minRange'],
								 ct.VK_ABILITIES['ability_6']['maxRange'],
								 True, False)
			game.hideCells(self.targetedCells)
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.VK_ABILITIES['ability_6']['EPcost'] and \
		self.stats['MP'] >= ct.VK_ABILITIES['ability_6']['MPcost']:
			for ability in self.played_abilities:
				if ability == 'ability_6':
					x = 1
			if lastCell in self.targetedCells and not x:
				for entity in game.entityList:
					if entity.coordX == lastCell.coordX and \
					entity.coordY == lastCell.coordY and not x:
						sharpened = {'name': 'sharpened',
									  'type': 'damage_%',
									  'situation': 'attacking',
									  'value': ct.VK_ABILITIES['ability_6']['value'],
									  'duration_type': 'next_attack',
									  'duration': 1,
									  'source': self}
						self.effects.append(sharpened)
						self.stats['EP'] -= ct.VK_ABILITIES['ability_6']['EPcost']
						self.stats['MP'] -= ct.VK_ABILITIES['ability_6']['MPcost']
						for button in game.buttons:
							if button[2]:
								button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
								button[2] = False
								self.action_sender('ability_6', [lastCell.coordX, lastCell.coordY])
								game.active_player.selectedAbility = None
								game.hideCells(self.targetedCells)
								self.targetedCells = None
								game.lastCell = None
								game.selectedcell = None
								self.played_abilities.append('ability_6')
								self.effectsClean()
								
	
	def Ability7(self, selectedcell, lastCell, game):
		x = 0
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.VK_ABILITIES['ability_7']['minRange'],
								 ct.VK_ABILITIES['ability_7']['maxRange'],
								 True, False)
			game.hideCells(self.targetedCells)
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.VK_ABILITIES['ability_7']['EPcost'] and \
		self.stats['MP'] >= ct.VK_ABILITIES['ability_7']['MPcost']:
			
			for ability in self.played_abilities:
				if ability == 'ability_7':
					x += 1
					
			if lastCell in self.targetedCells and x < 2:
				for entity in game.entityList:
					if entity.coordX == lastCell.coordX and \
					entity.coordY == lastCell.coordY:
						entity.stats['health'] += game.valueCalculator(self, entity,
						ct.VK_ABILITIES['ability_7']['value'], False, True, 'ability_7')
						game.collisionCalculator(entity, 2, self, False)
						game.collisionCalculator(self, 2, self, False)
						self.stats['EP'] -= ct.VK_ABILITIES['ability_7']['EPcost']
						self.stats['MP'] -= ct.VK_ABILITIES['ability_7']['MPcost']
						for button in game.buttons:
							if button[2]:
								button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
								button[2] = False
								self.action_sender('ability_7', [lastCell.coordX, lastCell.coordY])
								game.active_player.selectedAbility = None
								game.hideCells(self.targetedCells)
								self.targetedCells = None
								game.lastCell = None
								game.selectedcell = None
								self.played_abilities.append('ability_7')
								self.effectsClean()
								
	
	def Ability8(self, selectedcell, lastCell, game):
		hit = False
		x = 0
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
										ct.VK_ABILITIES['ability_8']['minRange'],
										ct.VK_ABILITIES['ability_8']['maxRange'],
										True, False)
			game.hideCells(self.targetedCells)
			
		elif selectedcell:
			if selectedcell in self.targetedCells:
				if len(self.played_abilities) >= 2:
					if self.Passive3 in self.passives and self.played_abilities[len(self.played_abilities)-1] == 'ability_2' and \
					self.played_abilities[len(self.played_abilities)-2] == 'ability_2':
						x = 1
				path = game.pathMultiplicator(selectedcell, self)
				if x == 1:
					for cell in game.groundCells:
						if (self.coordX-1 == cell.coordX or self.coordX+1 == cell.coordX) and \
						self.coordY-1 <= cell.coordY <= self.coordY+1:
							if not cell in self.zoneCells:
								self.zoneCells.append(cell)
						elif (self.coordY-1 == cell.coordY or self.coordY+1 == cell.coordY) and \
						self.coordX-1 <= cell.coordX <= self.coordX+1:
							if not cell in self.zoneCells:
								self.zoneCells.append(cell)
								
						elif cell in self.zoneCells:
							self.zoneCells.remove(cell)
							
				else:
					for cell in game.groundCells:
						if path[1] == 'right' or path[1] == 'left':
							if cell.coordX == selectedcell.coordX and \
							(cell.coordY-1 == selectedcell.coordY or \
							cell.coordY+1 == selectedcell.coordY):
								if not cell in self.zoneCells:
									self.zoneCells.append(cell)
							elif cell in self.zoneCells:
								self.zoneCells.remove(cell)
						elif path[1] == 'top' or path[1] == 'bottom':
							if cell.coordY == selectedcell.coordY and \
							(cell.coordX-1 == selectedcell.coordX or \
							cell.coordX+1 == selectedcell.coordX):
								if not cell in self.zoneCells:
									self.zoneCells.append(cell)
							elif cell in self.zoneCells:
								self.zoneCells.remove(cell)
				for cell in self.zoneCells:
					if selectedcell in self.targetedCells:
						cell.cellType = 'SelectedCell'
		
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.VK_ABILITIES['ability_8']['EPcost'] and \
		self.stats['MP'] >= ct.VK_ABILITIES['ability_8']['MPcost']:
			if lastCell in self.targetedCells:
				for entity in game.entityList:
					for cell2 in self.zoneCells:
						if entity.coordX == cell2.coordX and \
						entity.coordY == cell2.coordY:
							entity.stats['health'] += game.valueCalculator(self, entity, ct.VK_ABILITIES['ability_8']['value'], False, False, 'ability_8')
							hit = True
							
					if entity.coordX == lastCell.coordX and \
					entity.coordY == lastCell.coordY:
						entity.stats['health'] += game.valueCalculator(self, entity, ct.VK_ABILITIES['ability_8']['value'], False, True, 'ability_8')
						hit = True
				
				if hit:
					self.stats['EP'] -= ct.VK_ABILITIES['ability_8']['EPcost']
					self.stats['MP'] -= ct.VK_ABILITIES['ability_8']['MPcost']
					for button in game.buttons:
						if button[2]:
							button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
							button[2] = False
							self.action_sender('ability_8', [lastCell.coordX, lastCell.coordY])
							game.active_player.selectedAbility = None
							game.hideCells(self.targetedCells)
							self.targetedCells = None
							game.lastCell = None
							game.selectedcell = None
							self.zoneCells = []
							self.played_abilities.append('ability_8')
							self.effectsClean()
							
	
	def Ability9(self, selectedcell, lastCell, game):
		x, y = 0, 0
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.VK_ABILITIES['ability_9']['minRange'],
								 ct.VK_ABILITIES['ability_9']['maxRange'],
								 True, False)
			game.hideCells(self.targetedCells)
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.VK_ABILITIES['ability_9']['EPcost'] and \
		self.stats['MP'] >= ct.VK_ABILITIES['ability_9']['MPcost']:
			if lastCell in self.targetedCells:
				for entity2 in game.entityList:
					if entity2.controller.team == self.controller.team:
						for effect in self.effects:
							if effect['name'] == 'VKshield' and \
							effect['source'] == self:
								x += 1
						
				for entity in game.entityList:
					if entity.coordX == lastCell.coordX and \
					entity.coordY == lastCell.coordY:
						if x < 1 and not self.Passive4 in self.passives:
							vkShield = {'name': 'VKshield',
										  'type': 'damage_%',
										  'situation': 'defending',
										  'value': 0.10,
										  'duration_type': 'until_turns',
										  'duration': 2,
										  'source': self}
							y = 1
							
						elif x < 2 and self.Passive4 in self.passives:
							vkShield = {'name': 'VKshield',
										  'type': 'damage_%',
										  'situation': 'defending',
										  'value': 0.15,
										  'duration_type': 'until_turns',
										  'duration': 3,
										  'source': self}
							y = 1 
						
						if y:
							self.effects.append(vkShield)
							self.stats['EP'] -= ct.VK_ABILITIES['ability_9']['EPcost']
							self.stats['MP'] -= ct.VK_ABILITIES['ability_9']['MPcost']
							for button in game.buttons:
								if button[2]:
									button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
									button[2] = False
									self.action_sender('ability_9', [lastCell.coordX, lastCell.coordY])
									game.active_player.selectedAbility = None
									game.hideCells(self.targetedCells)
									self.targetedCells = None
									game.lastCell = None
									game.selectedcell = None
									self.played_abilities.append('ability_9')
									self.effectsClean()
									
	
	def Ability10(self, selectedcell, lastCell, game):
		x = 0
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.VK_ABILITIES['ability_10']['minRange'],
								 ct.VK_ABILITIES['ability_10']['maxRange'],
								 True, False)
			game.hideCells(self.targetedCells)
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.VK_ABILITIES['ability_10']['EPcost'] and \
		self.stats['MP'] >= ct.VK_ABILITIES['ability_10']['MPcost']:
			for ability in self.played_abilities:
				if ability == 'ability_10':
					x += 1
					
			if lastCell in self.targetedCells and x < 2:
				for entity in game.entityList:
					if entity.coordX == lastCell.coordX and \
					entity.coordY == lastCell.coordY:
						entity.stats['health'] += game.valueCalculator(self, entity, ct.VK_ABILITIES['ability_10']['value'], False, False, 'ability_10', True)
						
						if entity.stats['health'] > entity.Startstats['health']:
							entity.stats['health'] = entity.Startstats['health']
							
						self.stats['EP'] -= ct.VK_ABILITIES['ability_10']['EPcost']
						self.stats['MP'] -= ct.VK_ABILITIES['ability_10']['MPcost']
						for button in game.buttons:
							if button[2]:
								button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
								button[2] = False
								self.action_sender('ability_10', [lastCell.coordX, lastCell.coordY])
								game.active_player.selectedAbility = None
								game.hideCells(self.targetedCells)
								self.targetedCells = None
								game.lastCell = None
								game.selectedcell = None
								self.played_abilities.append('ability_10')
								self.effectsClean()
								
		
	def Passive1(self):
		if self.controller.isPlaying and len(self.moveSteps):
			charge = {'name': 'charge',
					  'type': 'damage_%',
					  'situation': 'attacking',
					  'value': 0.05,
					  'duration_type': 'next_attack',
					  'duration': 1,
					  'source': self}
					
			x = len(self.moveSteps)-1
			if self.lastMove == None:
				self.lastMove = self.moveSteps[x]
				self.effects.append(charge)
				print('charge +1')
			elif self.lastMove == self.moveSteps[x]:
				self.effects.append(charge)
				print('charge +1')
			elif self.lastMove != self.moveSteps[x]:
				y = []
				for effect in self.effects:
					if effect['name'] == 'charge':
						y.append(effect)
				for effect2 in y:
					self.effects.remove(effect2)
					del effect2
				print('charge reset')
				self.effects.append(charge)
				self.lastMove = self.moveSteps[x]
				print('charge +1')
				
	def Passive2(self):
		hardHead = {'name': 'hardHead',
					'type': 'damage_%',
					'situation': 'defending_front',
					'value': 0.15,
					'duration_type': 'infinitely',
					'duration': 999,
					'source': self}
		if not hardHead in self.effects:
			self.effects.append(hardHead)
	
	def Passive3(self):
		pass # active les combos si présent dans self.passives
		
	def Passive4(self):
		pass # booste l'actif 9'
	
	def Passive5(self):
		certifiedRunner = {'name': 'certifiedRunner',
							'type': 'MPboost',
							'situation': 'turnBegin',
							'value': 1,
							'duration_type': 'infinitely',
							'duration': 999,
							'source': self}
		if not certifiedRunner in self.effects:
			self.effects.append(certifiedRunner)
	
	def Passive6(self):
		HealthyArmor = {'name': 'HealthyArmor',
						'type': 'HPboost',
						'situation': 'gameBegin',
						'value': 30,
						'duration_type': 'infinitely',
						'duration': 999,
						'source': self}
		if not HealthyArmor in self.effects:
			self.effects.append(HealthyArmor)
			self.stats['health'] += 30
			self.Startstats['health'] += 30
