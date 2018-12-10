from scene import *
from Classes import *
import Constants as ct
import random

class Marshal(Entity):
	def __init__(self, player):
		Entity.__init__(self)
		#self.images = [['VikingFace2-2.PNG'], [None, None]]
		self.IMG = SpriteNode('Images/Marshal/MarshalFace0-0.PNG')
		self.IMG.anchor_point = (0, 1)
		self.name = 'Marshal'
		self.IMG.x_scale = 0.01*ct.CELL_X
		self.IMG.y_scale = 0.01*ct.CELL_Y+0.15
		self.IMG.position = (-250,-250)
		self.IMG.z_position = 2.0
		self.classSetup(player['abilities'], player['passives'])
		self.targetedCells = None
		self.team = player['team']
		self.stats = {'health': ct.MR_STATS['health'],
					  'MP': ct.MR_STATS['MP'],
					  'EP': ct.MR_STATS['EP'],
					  'orientation': None}
		self.Startstats = {'health': ct.MR_STATS['health'],
					  'MP': ct.MR_STATS['MP'],
					  'EP': ct.MR_STATS['EP'],
					  'orientation': None}
		self.passive1_done = False
	
	def Ability1(self, selectedcell, lastCell, game):
		x = 0
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.MR_ABILITIES['ability_1']['minRange'],
								 ct.MR_ABILITIES['ability_1']['maxRange'],
								 True, False)
			game.hideCells(self.targetedCells)
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.MR_ABILITIES['ability_1']['EPcost'] and \
		self.stats['MP'] >= ct.MR_ABILITIES['ability_1']['MPcost']:
			for ability in self.played_abilities:
				if ability == 'ability_1':
					x += 1
					
			if lastCell in self.targetedCells and x < 2:
				for entity in game.entityList:
					if entity.coordX == lastCell.coordX and \
					entity.coordY == lastCell.coordY:
						if self.Passive3 in self.passives:
							entity.stats['health'] += game.valueCalculator(self, entity,
							ct.MR_ABILITIES['ability_1']['value']-1, False, True, 'ability_1')
						else:
							entity.stats['health'] += game.valueCalculator(self, entity,
							ct.MR_ABILITIES['ability_1']['value'], False, True, 'ability_1')
							
						self.stats['EP'] -= ct.MR_ABILITIES['ability_1']['EPcost']
						self.stats['MP'] -= ct.MR_ABILITIES['ability_1']['MPcost']
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
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.MR_ABILITIES['ability_2']['minRange'],
								 ct.MR_ABILITIES['ability_2']['maxRange'],
								 True, False)
								 
			for entity in game.entityList:
				if entity.team == self.team:
					otherCells = game.rangeCalculator(entity, 
								 ct.MR_ABILITIES['ability_2']['minRange'],
								 ct.MR_ABILITIES['ability_2']['maxRange'],
								 True, False)
					for cell in otherCells:
						if not cell in self.targetedCells:
							self.targetedCells.append(cell)
			game.hideCells(self.targetedCells)
			
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.MR_ABILITIES['ability_2']['EPcost'] and \
		self.stats['MP'] >= ct.MR_ABILITIES['ability_2']['MPcost']:
			if lastCell in self.targetedCells and not game.touchX:
				for entity in game.entityList:
					if entity.coordX == lastCell.coordX and \
					entity.coordY == lastCell.coordY:
						if self.Passive3 in self.passives:
							entity.stats['health'] += game.valueCalculator(self, entity,
							ct.MR_ABILITIES['ability_2']['value']-1, True, True, 'ability_2')
						else:
							entity.stats['health'] += game.valueCalculator(self, entity,
							ct.MR_ABILITIES['ability_2']['value'], True, True, 'ability_2')
							
						self.stats['EP'] -= ct.MR_ABILITIES['ability_2']['EPcost']
						self.stats['MP'] -= ct.MR_ABILITIES['ability_2']['MPcost']
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
								self.played_abilities.append('ability_2')
								self.effectsClean()
	
	def Ability3(self, selectedcell, lastCell, game):
		x = 0
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.MR_ABILITIES['ability_3']['minRange'],
								 ct.MR_ABILITIES['ability_3']['maxRange'],
								 True, True)
			game.hideCells(self.targetedCells)
		
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.MR_ABILITIES['ability_3']['EPcost'] and \
		self.stats['MP'] >= ct.MR_ABILITIES['ability_3']['MPcost']:
			if lastCell in self.targetedCells and not game.touchX:
				PreparedEffect1 = {'name': 'Prepared(1)',
								'type': 'damage_%',
								'situation': 'attacking',
								'value': ct.MR_ABILITIES['ability_3']['value(1)'],
								'duration_type': 'until_turns',
								'duration': 2,
								'source': self}
				PreparedEffect2 = {'name': 'Prepared(2)',
								'type': 'EPboost',
								'situation': 'turnBegin',
								'value': ct.MR_ABILITIES['ability_3']['value(2)'],
								'duration_type': 'until_turns',
								'duration': 2,
								'source': self}
								
				for effect in self.effects:
					if effect['name'] == 'Prepared(1)':
						x += 1
				
				if not x:
					self.effects.append(PreparedEffect1)
					self.effects.append(PreparedEffect2)
					self.stats['EP'] -= ct.MR_ABILITIES['ability_3']['EPcost']
					self.stats['MP'] -= ct.MR_ABILITIES['ability_3']['MPcost']
					for button in game.buttons:
						if button[2]:
							button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
							button[2] = False
							self.action_sender('ability_3', [lastCell.coordX, lastCell.coordY])
							game.active_player.selectedAbility = None
							game.hideCells(self.targetedCells)
							self.targetedCells = None
							self.zoneCells = []
							self.played_abilities.append('ability_3')
							self.effectsClean()
							game.lastCell = None
							game.selectedcell = None
							game.play_button_touched = True
	
	def Ability4(self, selectedcell, lastCell, game):
		x = 0
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.MR_ABILITIES['ability_4']['minRange'],
								 ct.MR_ABILITIES['ability_4']['maxRange'],
								 True, False)
			game.hideCells(self.targetedCells)
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.MR_ABILITIES['ability_4']['EPcost'] and \
		self.stats['MP'] >= ct.MR_ABILITIES['ability_4']['MPcost']:
			y = len(self.played_turns)
			for ability in self.played_abilities:
				if ability == 'ability_4':
					x += 1
			if y >= 1:
				for ability in self.played_turns[y-1]:
					if ability == 'ability_4':
						x += 1 
			if y >= 2:
				for ability in self.played_turns[y-2]:
					if ability == 'ability_4':
						x += 1
			if lastCell in self.targetedCells and not game.touchX and not x:
				self.stats['MP'] += ct.MR_ABILITIES['ability_4']['value']
				self.stats['EP'] -= ct.MR_ABILITIES['ability_4']['EPcost']
				self.stats['MP'] -= ct.MR_ABILITIES['ability_4']['MPcost']
				for button in game.buttons:
					if button[2]:
						button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
						button[2] = False
						self.action_sender('ability_4', [lastCell.coordX, lastCell.coordY])
						game.active_player.selectedAbility = None
						game.hideCells(self.targetedCells)
						self.targetedCells = None
						self.zoneCells = []
						self.played_abilities.append('ability_4')
						self.effectsClean()
						game.lastCell = None
						game.selectedcell = None
				
	def Ability5(self, selectedcell, lastCell, game):
		x = 0
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.MR_ABILITIES['ability_5']['minRange'],
								 ct.MR_ABILITIES['ability_5']['maxRange'],
								 True, False)
								 
			for entity in game.entityList:
				if entity.team == self.team:
					otherCells = game.rangeCalculator(entity, 
								 ct.MR_ABILITIES['ability_5']['minRange'],
								 ct.MR_ABILITIES['ability_5']['maxRange'],
								 True, False)
					for cell in otherCells:
						if not cell in self.targetedCells:
							self.targetedCells.append(cell)
			game.hideCells(self.targetedCells)
			
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.MR_ABILITIES['ability_5']['EPcost'] and \
		self.stats['MP'] >= ct.MR_ABILITIES['ability_5']['MPcost']:
			y = len(self.played_turns)
			for ability in self.played_abilities:
				if ability == 'ability_5':
					x += 1
			if y >= 1:
				for ability in self.played_turns[y-1]:
					if ability == 'ability_5':
						x += 1 
						
			if lastCell in self.targetedCells and not game.touchX and not x:
				x = 0
				for entity in game.entityList:
					if entity.coordX == lastCell.coordX and \
					entity.coordY == lastCell.coordY:
						x += 1
				
				if not x:
					holeEffect = {'name': 'Hole',
								'type': None,
								'situation': None,
								'value': None,
								'duration_type': 'until_turns',
								'duration': ct.MR_ABILITIES['ability_5']['value'],
								'source': self,
								'image': None}
					
					game.addGroundEffect(self, lastCell, "Hole")
					self.stats['EP'] -= ct.MR_ABILITIES['ability_5']['EPcost']
					self.stats['MP'] -= ct.MR_ABILITIES['ability_5']['MPcost']
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
		hit = False
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.MR_ABILITIES['ability_6']['minRange'],
								 ct.MR_ABILITIES['ability_6']['maxRange'],
								 True, False)
			game.hideCells(self.targetedCells)
		elif selectedcell:
			self.zoneCells = game.AreaCalculator('mediumArea', self, selectedcell, self.zoneCells)
			for cell in self.zoneCells:
				if selectedcell in self.targetedCells:
					cell.cellType = 'SelectedCell'
		
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.MR_ABILITIES['ability_6']['EPcost'] and \
		self.stats['MP'] >= ct.MR_ABILITIES['ability_6']['MPcost']:
			y = len(self.played_turns)
			for ability in self.played_abilities:
				if ability == 'ability_6':
					x += 1
			if y >= 1:
				for ability in self.played_turns[y-1]:
					if ability == 'ability_6':
						x += 1 
						
			if lastCell in self.targetedCells and not game.touchX and not x:
				entrenchmantEffect = {'name': 'Entranchment',
									'type': None,
									'situation': 'Stay',
									'value(1)': ct.MR_ABILITIES['ability_6']['value(1)'],
									'value(2)': ct.MR_ABILITIES['ability_6']['value(2)'],
									'duration_type': 'until_turns',
									'duration': 2,
									'source': self,
									'image': None}
				x = 0
				for effect in lastCell.effects:
					if effect['name'] == 'Entrenchmant':
						x += 1
				if not x:
					game.addGroundEffect(self, lastCell, "Entranchment")	
					hit = True
				
				for cell in self.zoneCells:
					x = 0
					entrenchmantEffect = {'name': 'Entranchment',
										'type': None,
										'situation': 'Stay',
										'value(1)': ct.MR_ABILITIES['ability_6']['value(1)'],
										'value(2)': ct.MR_ABILITIES['ability_6']['value(2)'],
										'duration_type': 'until_turns',
										'duration': 2,
										'source': self,
										'image': None}
					for effect in cell.effects:
						if effect['name'] == 'Entrenchmant' and effect['source'].team == self.team:
							x += 1
							
					if not x:
						game.addGroundEffect(self, cell, "Entranchment")	
						hit = True
				
				if hit:
					self.stats['EP'] -= ct.MR_ABILITIES['ability_6']['EPcost']
					self.stats['MP'] -= ct.MR_ABILITIES['ability_6']['MPcost']
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
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.MR_ABILITIES['ability_7']['minRange'],
								 ct.MR_ABILITIES['ability_7']['maxRange'],
								 True, False)
			for entity in game.entityList:
				if entity.team == self.team:
					otherCells = game.rangeCalculator(entity, 
								 ct.MR_ABILITIES['ability_7']['minRange'],
								 ct.MR_ABILITIES['ability_7']['maxRange'],
								 True, False)
					for cell in otherCells:
						if not cell in self.targetedCells:
							self.targetedCells.append(cell)
			game.hideCells(self.targetedCells)
							
		elif selectedcell:
			for cell in game.groundCells:
				if self.stats['orientation'] == 'right':
					if cell == game.cellScan(selectedcell.coordX+1, selectedcell.coordY):
						if not cell in self.zoneCells:
							self.zoneCells.append(cell)
					elif cell in self.zoneCells:
						self.zoneCells.remove(cell)
				elif self.stats['orientation'] == 'left':
					if cell == game.cellScan(selectedcell.coordX-1, selectedcell.coordY):
						if not cell in self.zoneCells:
							self.zoneCells.append(cell)
					elif cell in self.zoneCells:
						self.zoneCells.remove(cell)
				elif self.stats['orientation'] == 'top':
					if cell == game.cellScan(selectedcell.coordX, selectedcell.coordY-1):
						if not cell in self.zoneCells:
							self.zoneCells.append(cell)
					elif cell in self.zoneCells:
						self.zoneCells.remove(cell)
				elif self.stats['orientation'] == 'bottom':
					if cell == game.cellScan(selectedcell.coordX, selectedcell.coordY+1):
						if not cell in self.zoneCells:
							self.zoneCells.append(cell)
					elif cell in self.zoneCells:
						self.zoneCells.remove(cell)
						
			for cell in self.zoneCells:
				if selectedcell in self.targetedCells:
					cell.cellType = 'SelectedCell'
			
		elif lastCell and not selectedcell and self.stats['orientation'] and \
		self.stats['EP'] >= ct.MR_ABILITIES['ability_7']['EPcost'] and \
		self.stats['MP'] >= ct.MR_ABILITIES['ability_7']['MPcost'] and \
		len(self.zoneCells):
			if lastCell in self.targetedCells and not game.touchX:
				for entity in game.entityList:
					if entity.coordX == lastCell.coordX and \
					entity.coordY == lastCell.coordY :
						x = 0
						for entity2 in game.entityList:
							for cell in self.zoneCells:
								if entity2.coordX == cell.coordX and \
								entity2.coordY == cell.coordY:
									x += 1
									
						if not x and entity.team == self.team:
							if self.stats['orientation'] == 'right':
								entity.moveSteps.append('right')
								entity.coordX += 1
								entity.effectsCheck(['isMoving'], game)
							elif self.stats['orientation'] == 'left':
								entity.moveSteps.append('left')
								entity.coordX -= 1
								entity.effectsCheck(['isMoving'], game)
							if self.stats['orientation'] == 'top':
								entity.moveSteps.append('top')
								entity.coordY -= 1
								entity.effectsCheck(['isMoving'], game)
							elif self.stats['orientation'] == 'bottom':
								entity.moveSteps.append('bottom')
								entity.coordY += 1
								entity.effectsCheck(['isMoving'], game)
								
							self.stats['EP'] -= ct.MR_ABILITIES['ability_7']['EPcost']
							self.stats['MP'] -= ct.MR_ABILITIES['ability_7']['MPcost']
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
		x, y = 0, 0
		for entity in game.entityList:
			if entity != self and entity.team == self.team:
				y += 1
				
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.MR_ABILITIES['ability_8']['minRange'],
								 ct.MR_ABILITIES['ability_8']['maxRange']+y,
								 True, True)
			game.hideCells(self.targetedCells)
			
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.MR_ABILITIES['ability_8']['EPcost'] and \
		self.stats['MP'] >= ct.MR_ABILITIES['ability_8']['MPcost']:
			for ability in self.played_abilities:
				if ability == 'ability_8':
					x += 1
					
			if lastCell in self.targetedCells and x < 2:
				for entity in game.entityList:
					if entity.coordX == lastCell.coordX and \
					entity.coordY == lastCell.coordY:
						if self.Passive3 in self.passives:
							entity.stats['health'] += game.valueCalculator(self, entity,
							ct.MR_ABILITIES['ability_8']['value']-1-y*2, False, True, 'ability_8')
						else:
							entity.stats['health'] += game.valueCalculator(self, entity,
							ct.MR_ABILITIES['ability_8']['value']-y*2, False, True, 'ability_8')
							
						game.collisionCalculator(entity, y, self, False)
						self.stats['EP'] -= ct.MR_ABILITIES['ability_8']['EPcost']
						self.stats['MP'] -= ct.MR_ABILITIES['ability_8']['MPcost']
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
								self.played_abilities.append('ability_8')
								self.effectsClean()
	
	def Ability9(self, selectedcell, lastCell, game):
		x = 0
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.MR_ABILITIES['ability_9']['minRange'],
								 ct.MR_ABILITIES['ability_9']['maxRange'],
								 True, False)
			game.hideCells(self.targetedCells)
			
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.MR_ABILITIES['ability_9']['EPcost'] and \
		self.stats['MP'] >= ct.MR_ABILITIES['ability_9']['MPcost']:
			for ability in self.played_abilities:
				if ability == 'ability_9':
					x += 1
					
			if lastCell in self.targetedCells and x < 1:
				for entity in game.entityList:
					if entity.coordX == lastCell.coordX and \
					entity.coordY == lastCell.coordY and \
					entity.team != self.team and entity.stats['health']+5 <= entity.Startstats['health']:
						entity.stats['health'] += ct.MR_ABILITIES['ability_9']['value(1)']
						
						if self.stats['health']+ct.MR_ABILITIES['ability_9']['value(2)'] \
						<= self.Startstats['health']:
							self.stats['health'] += ct.MR_ABILITIES['ability_9']['value(2)']
						else:
							self.stats['health'] = self.Startstats['health']
							
						self.stats['EP'] -= ct.MR_ABILITIES['ability_9']['EPcost']
						self.stats['MP'] -= ct.MR_ABILITIES['ability_9']['MPcost']
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
								 ct.MR_ABILITIES['ability_10']['minRange'],
								 ct.MR_ABILITIES['ability_10']['maxRange'],
								 True, False)
			game.hideCells(self.targetedCells)
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.TM_ABILITIES['ability_10']['EPcost'] and \
		self.stats['MP'] >= ct.TM_ABILITIES['ability_10']['MPcost']:
			x = 0
			y = len(self.played_turns)
			for ability in self.played_abilities:
				if ability == 'ability_10':
					x += 1
			if y >= 1:
				for ability in self.played_turns[y-1]:
					if ability == 'ability_10':
						x += 1 
			if y >= 2:
				for ability in self.played_turns[y-2]:
					if ability == 'ability_10':
						x += 1
			
			if lastCell in self.targetedCells and x < 1:
				for entity in game.entityList:
					ArmisticeEffect1 = {'name': 'Armistice(1)',
								'type': 'damage_%',
								'situation': 'attacking',
								'value': ct.MR_ABILITIES['ability_10']['value(1)'],
								'duration_type': 'until_turns',
								'duration': 1,
								'source': self}
					ArmisticeEffect2 = {'name': 'Armistice(2)',
									'type': 'damage_%',
									'situation': 'defending',
									'value': ct.MR_ABILITIES['ability_10']['value(2)'],
									'duration_type': 'until_turns',
									'duration': 1,
									'source': self}
					entity.effects.append(ArmisticeEffect1)
					entity.effects.append(ArmisticeEffect2)
					
				self.stats['EP'] -= ct.MR_ABILITIES['ability_10']['EPcost']
				self.stats['MP'] -= ct.MR_ABILITIES['ability_10']['MPcost']
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
		if not self.passive1_done:						
			for cell in self.controller.game.groundCells:
				entrenchmantEffect = {'name': 'Entranchment',
									'type': None,
									'situation': 'Stay',
									'value(1)': ct.MR_ABILITIES['ability_6']['value(1)'],
									'value(2)': ct.MR_ABILITIES['ability_6']['value(2)'],
									'duration_type': 'forever',
									'duration': 999,
									'source': self,
									'image': None}
				y = self.controller.game.entityScan(cell.coordX, cell.coordY)
				if y:
					if y.team == self.team:
						cell.effects.append(entrenchmantEffect)
			self.passive1_done = True
	
	def Passive2(self):
		collectionArmor = {'name': 'Collection Armor',
							'type': 'MPboost',
							'situation': 'turnBegin',
							'value': -1,
							'duration_type': 'infinitely',
							'duration': 999,
							'source': self} 
		
		if not collectionArmor in self.effects:
			self.effects.append(collectionArmor)
			self.stats['health'] += 50
			self.Startstats['health'] += 50
			
	def Passive3(self):
		pass # Accord du Roi
	
	def Passive4(self):
		x, y = 0, None
		for entity in self.controller.game.entityList:
			if entity.team == self.team and entity != self:
				x += 1
		BattlePlan1 = {'name': 'Battle Plan(1)',
							'type': 'MPboost',
							'situation': 'turnBegin',
							'value': -x,
							'duration_type': 'infinitely',
							'duration': 999,
							'source': self}
							
		for effect in self.effects:
			if effect['name'] == 'Battle Plan(1)':
				y = self.effects.index(effect)
				
		if y == None:
			self.effects.append(BattlePlan1)
			for entity in self.controller.game.entityList:
				if entity.team == self.team and entity != self:
					BattlePlan2 = {'name': 'Battle Plan(2)',
									'type': 'MPboost',
									'situation': 'turnBegin',
									'value': 1,
									'duration_type': 'infinitely',
									'duration': 999,
									'source': self}
					entity.effects.append(BattlePlan2)
		elif y:
			self.effects[y]['value'] = -x
		
	def Passive5(self):
		x, y = 0, None
		for entity in self.controller.game.entityList:
			if entity.team == self.team and entity != self:
				x += 1
		VictoryThirst1 = {'name': 'Victory Thirst(1)',
							'type': 'damage_%',
							'situation': 'attacking',
							'value': -x*0.1,
							'duration_type': 'infinitely',
							'duration': 999,
							'source': self}
							
		for effect in self.effects:
			if effect['name'] == 'Victory Thirst(1)':
				y = self.effects.index(effect)
				
		if y == None:
			self.effects.append(VictoryThirst1)
			for entity in self.controller.game.entityList:
				if entity.team == self.team and entity != self:
					VictoryThirst2 = {'name': 'Victory Thirst(2)',
									'type': 'damage_%',
									'situation': 'attacking',
									'value': 0.10,
									'duration_type': 'infinitely',
									'duration': 999,
									'source': self}
					entity.effects.append(VictoryThirst2)
		elif y:
			self.effects[y]['value'] = -x*0.1
	
	def Passive6(self):
		x, y = 0, None
		for entity in self.controller.game.entityList:
			if entity.team == self.team and entity != self:
				x += 1
		HomelandDefence1 = {'name': 'Homeland Defence(1)',
							'type': 'damage_%',
							'situation': 'defending',
							'value': -x*0.1,
							'duration_type': 'infinitely',
							'duration': 999,
							'source': self}
							
		for effect in self.effects:
			if effect['name'] == 'Homeland Defence(1)':
				y = self.effects.index(effect)
		
		if y == None:
			self.effects.append(HomelandDefence1)
			for entity in self.controller.game.entityList:
				if entity.team == self.team and entity != self:
					HomelandDefence2 = {'name': 'Homeland Defence(2)',
									'type': 'damage_%',
									'situation': 'defending',
									'value': 0.10,
									'duration_type': 'infinitely',
									'duration': 999,
									'source': self}
					entity.effects.append(HomelandDefence2)
		elif y:
			self.effects[y]['value'] = -x*0.1
