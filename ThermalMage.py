from scene import *
from Classes import *
import Constants as ct
import random

class ThermalMage(Entity):
	def __init__(self, player):
		Entity.__init__(self)
		self.imagesIce = ['Images/Thermal Mage/ThermalMage[ice]0-0.png',
							'Images/Thermal Mage/ThermalMage[ice]0-1.png',
							'Images/Thermal Mage/ThermalMage[ice]0-2.png']
		self.imagesFire = ['Images/Thermal Mage/ThermalMage[fire]0-0.png',
							'Images/Thermal Mage/ThermalMage[fire]0-1.png',
							'Images/Thermal Mage/ThermalMage[fire]0-2.png']
		self.IMG = SpriteNode('Images/Viking/VikingFace2-2.PNG')
		self.IMG.anchor_point = (0, 1)
		self.IMG.x_scale = 0.01*ct.CELL_X
		self.IMG.y_scale = 0.01*ct.CELL_Y+0.15
		self.IMG.position = (-250,-250)
		self.IMG.z_position = 2.0
		self.targetedCells = None
		self.name = 'Thermal Mage'
		self.team = player['team']
		self.classSetup(player['abilities'], player['passives'])
		self.stats = {'health': ct.TM_STATS['health'],
					  'MP': ct.TM_STATS['MP'],
					  'EP': ct.TM_STATS['EP'],
					  'orientation': None}
		self.Startstats = {'health': ct.TM_STATS['health'],
					  'MP': ct.TM_STATS['MP'],
					  'EP': ct.TM_STATS['EP'],
					  'orientation': None}
					  
		if self.Passive5 in self.passives and not self.Passive6 in self.passives:
			self.actualType = 'ice'
			self.IMG.texture = Texture(self.imagesIce[0])
		elif self.Passive6 in self.passives and not self.Passive5 in self.passives:
			self.actualType = 'fire'
			self.IMG.texture = Texture(self.imagesFire[0])
		elif self.Passive5 in self.passives and self.Passive6 in self.passives:
			if self.passives.index(self.Passive5) < self.passives.index(self.Passive6):
				self.actualType = 'ice'
				self.IMG.texture = Texture(self.imagesIce[0])
			else:
				self.actualType = 'fire'
				self.IMG.texture = Texture(self.imagesFire[0])
		else:
			if ct.onlineMulti:
				x = player['randN']
			else:
				x = random.randint(0,1)
			if x:
				self.actualType = 'ice'
				self.IMG.texture = Texture(self.imagesIce[0])
			else:
				self.actualType = 'fire'
				self.IMG.texture = Texture(self.imagesFire[0])

	def Ability1(self, selectedcell, lastCell, game):
		x = 0
		hit = None
		if self.actualType == 'ice':
			if not self.targetedCells:
				self.targetedCells = game.rangeCalculator(self, 
									 ct.TM_ABILITIES['ability_1[ice]']['minRange'],
									 ct.TM_ABILITIES['ability_1[ice]']['maxRange'],
									 True, False)
				if self.targetedCells:
					game.hideCells(self.targetedCells)
			
			elif selectedcell and self.Passive4 in self.passives:
				for effect in selectedcell.effects:
					if effect['name'] == 'LavaGusher' and \
					effect['source'] == self:
						x +=1
			
				if x:
					self.zoneCells = game.AreaCalculator('bigArea', self, selectedcell, self.zoneCells)
					for cell in self.zoneCells:
						if selectedcell in self.targetedCells:
							cell.cellType = 'SelectedCell'
			
			elif lastCell and not selectedcell and \
			self.stats['EP'] >= ct.TM_ABILITIES['ability_1[ice]']['EPcost'] and \
			self.stats['MP'] >= ct.TM_ABILITIES['ability_1[ice]']['MPcost']:
				if lastCell in self.targetedCells and not game.touchX:
					for entity in game.entityList:
						if (entity.coordX == lastCell.coordX and \
						entity.coordY == lastCell.coordY) or \
						(len(self.zoneCells) and self.Passive4 in self.passives):
							
							
							
							if entity.coordX == lastCell.coordX and \
							entity.coordY == lastCell.coordY:
								for effect in entity.effects:
									if effect['name'] == 'iced' and \
									effect['source'] == self:
										if self.Passive5 in self.passives and \
										effect['duration'] == 1:
											effect['duration'] = 2
										x += 1
								
								if not x or self.Passive5 in self.passives:
									game.addStatEffect(self, entity, "ice")
									print('iced +1')
								if self.Passive2 in self.passives:
									y = []
									for effect in entity.effects:
										if effect['name'] == 'fired' and \
										effect['source'] == self:
											y.append(effect)
									for effect2 in y:
										entity.effects.remove(effect2)
										
										game.addStatEffect(self, entity, "ice")
										
								entity.stats['health'] += game.valueCalculator(self, entity,
								ct.TM_ABILITIES['ability_1[ice]']['value'], False, True, 'ability_1[ice]')
							
							if self.Passive4 in self.passives:
								for cell in self.zoneCells:
									x = 0
									EmberMat = {'name': 'EmberMat',
											  'type': 'HPboost',
											  'situation': 'Walk&Stay',
											  'value': -2,
											  'duration_type': 'until_turns',
											  'duration': 2,
											  'source': self,
											  'image': None}
									for effect in cell.effects:
										if effect['name'] == 'EmberMat':
											x +=1	
									if not x:
										game.addGroundEffect(self, cell, "EmberMat")
								
								for effect in lastCell.effects:
									if effect['name'] == 'LavaGusher':
										effect['duration'] = 0
								
							self.stats['EP'] -= ct.TM_ABILITIES['ability_1[ice]']['EPcost']
							self.stats['MP'] -= ct.TM_ABILITIES['ability_1[ice]']['MPcost']
							for button in game.buttons:
								if button[2]:
									button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
									button[2] = False
									self.action_sender('ability_1', [lastCell.coordX, lastCell.coordY])
									game.active_player.selectedAbility = None
									game.hideCells(self.targetedCells)
									self.targetedCells = None
									self.zoneCells = []
									self.played_abilities.append('ability_1[ice]')
									self.effectsClean()
									game.lastCell = None
									game.selectedcell = None
									if self.Passive1 in self.passives:
										self.actualType = 'fire'
										self.IMG.texture = Texture(self.imagesFire[0])
										effect = next(effect for effect in self.effects if effect['name'] == 
										'thermalCasualties')
										effect['value'] += -2
									
		elif self.actualType == 'fire':
			if not self.targetedCells:
				self.targetedCells = game.rangeCalculator(self, 
									 ct.TM_ABILITIES['ability_1[fire]']['minRange'],
									 ct.TM_ABILITIES['ability_1[fire]']['maxRange'],
									 True, False)
									 
				if self.targetedCells:			
					game.hideCells(self.targetedCells)
				
			elif selectedcell:
				self.zoneCells = game.AreaCalculator('smallArea', self, selectedcell, self.zoneCells)
				for cell in self.zoneCells:
					if selectedcell in self.targetedCells:
						cell.cellType = 'SelectedCell'
						
			elif lastCell and not selectedcell and \
			self.stats['EP'] >= ct.TM_ABILITIES['ability_1[fire]']['EPcost'] and \
			self.stats['MP'] >= ct.TM_ABILITIES['ability_1[fire]']['MPcost']:
				if lastCell in self.targetedCells and not game.touchX:
					
					
					for entity in game.entityList:
						for cell2 in self.zoneCells:
							if entity.coordX == cell2.coordX and \
							entity.coordY == cell2.coordY:
								x = 0
								for effect in entity.effects:
									if effect['name'] == 'fired' and \
									effect['source'] == self:
										if self.Passive6 in self.passives and \
										effect['duration'] == 1:
											effect['duration'] = 2
										x += 1
								
								if not x or self.Passive6 in self.passives:
									
									game.addStatEffect(self, entity, "fire")
									print('fired +1')
								entity.stats['health'] += game.valueCalculator(self, entity,
								ct.TM_ABILITIES['ability_1[fire]']['value'], True, False, 'ability_1[fire]')
								hit = True
								if self.Passive2 in self.passives:
									y = []
									for effect in entity.effects:
										if effect['name'] == 'iced' and \
										effect['source'] == self:
											y.append(effect)
									for effect2 in y:
										entity.effects.remove(effect2)
										
										game.addStatEffect(self, entity, "fire")
										
						if entity.coordX == lastCell.coordX and \
						entity.coordY == lastCell.coordY:
							x = 0
							for effect in entity.effects:
								if effect['name'] == 'fired' and \
								effect['source'] == self:
									if self.Passive6 in self.passives and \
									effect['duration'] == 1:
										effect['duration'] = 2
									x += 1
									
							if not x or self.Passive6 in self.passives:
								
								game.addStatEffect(self, entity, "fire")
								print('fired +1')
							entity.stats['health'] += game.valueCalculator(self, entity,
							ct.TM_ABILITIES['ability_1[fire]']['value'], True, True, 'ability_1[fire]')
							hit = True
							if self.Passive2 in self.passives:
								x = []
								for effect in entity.effects:
									if effect['name'] == 'iced' and \
										effect['source'] == self:
										x.append(effect)
								for effect2 in x:
									entity.effects.remove(effect2)
									del effect2
									
									game.addStatEffect(self, entity, "fire")
						
					if hit:
						self.stats['EP'] -= ct.TM_ABILITIES['ability_1[fire]']['EPcost']
						self.stats['MP'] -= ct.TM_ABILITIES['ability_1[fire]']['MPcost']
						for button in game.buttons:
							if button[2]:
								button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
								button[2] = False
								self.action_sender('ability_1', [lastCell.coordX, lastCell.coordY])
								game.active_player.selectedAbility = None
								game.hideCells(self.targetedCells)
								self.targetedCells = None
								self.zoneCells = []
								self.played_abilities.append('ability_1[fire]')
								self.effectsClean()
								game.lastCell = None
								game.selectedcell = None
								if self.Passive1 in self.passives:
									self.actualType = 'ice'
									self.IMG.texture = Texture(self.imagesIce[0])
									effect = next(effect for effect in self.effects if effect['name'] == 
									'thermalCasualties')
									effect['value'] += -2
	
	def Ability2(self, selectedcell, lastCell, game):
		x = 0
		hit = None
		if self.actualType == 'ice':
			if not self.targetedCells:
				self.targetedCells = game.rangeCalculator(self, 
									 ct.TM_ABILITIES['ability_2[ice]']['minRange'],
									 ct.TM_ABILITIES['ability_2[ice]']['maxRange'],
									 True, False)
				game.hideCells(self.targetedCells)
			
			elif selectedcell:
				self.zoneCells = game.AreaCalculator('bigArea', self, selectedcell, self.zoneCells)
				for cell in self.zoneCells:
					if selectedcell in self.targetedCells:
						cell.cellType = 'SelectedCell'
					if selectedcell == cell:
						self.zoneCells.remove(cell)
						
			elif lastCell and not selectedcell and \
			self.stats['EP'] >= ct.TM_ABILITIES['ability_2[ice]']['EPcost'] and \
			self.stats['MP'] >= ct.TM_ABILITIES['ability_2[ice]']['MPcost']:
				if lastCell in self.targetedCells and not game.touchX:
					
							
					for entity in game.entityList:
						for cell2 in self.zoneCells:
							if entity.coordX == cell2.coordX and \
							entity.coordY == cell2.coordY:
								x = 0
								for effect in entity.effects:
									if effect['name'] == 'iced' and \
									effect['source'] == self:
										if self.Passive5 in self.passives and \
										effect['duration'] == 1:
											effect['duration'] = 2
										x += 1
								
								if not x or self.Passive5 in self.passives:
									
									game.addStatEffect(self, entity, "ice")
									print('iced +1')
								entity.stats['health'] += game.valueCalculator(self, entity,
								ct.TM_ABILITIES['ability_2[ice]']['value'], True, False, 'ability_2[ice]')
								hit = True
								if self.Passive2 in self.passives:
									x = []
									for effect in entity.effects:
										if effect['name'] == 'fired' and \
										effect['source'] == self:
											x.append(effect)
									for effect2 in x:
										entity.effects.remove(effect2)
										del effect2
										
										game.addStatEffect(self, entity, "ice")
								
						if entity.coordX == lastCell.coordX and \
						entity.coordY == lastCell.coordY:
							x = 0
							for effect in entity.effects:
								if effect['name'] == 'iced' and \
								effect['source'] == self:
									if self.Passive6 in self.passives and \
									effect['duration'] == 1:
										effect['duration'] = 2
									x += 1
									
							if not x or self.Passive6 in self.passives:
								
								game.addStatEffect(self, entity, "ice")
								print('iced +1')
							entity.stats['health'] += game.valueCalculator(self, entity,
							ct.TM_ABILITIES['ability_2[ice]']['value'], True, True, 'ability_2[ice]')
							hit = True
							if self.Passive2 in self.passives:
									x = []
									for effect in entity.effects:
										if effect['name'] == 'fired' and \
										effect['source'] == self:
											x.append(effect)
									for effect2 in x:
										entity.effects.remove(effect2)
										del effect2
										
										game.addStatEffect(self, entity, "ice")
						
					if hit:
						self.stats['EP'] -= ct.TM_ABILITIES['ability_2[ice]']['EPcost']
						self.stats['MP'] -= ct.TM_ABILITIES['ability_2[ice]']['MPcost']
						for button in game.buttons:
							if button[2]:
								button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
								button[2] = False
								self.action_sender('ability_2', [lastCell.coordX, lastCell.coordY])
								game.active_player.selectedAbility = None
								game.hideCells(self.targetedCells)
								self.targetedCells = None
								self.zoneCells = []
								self.played_abilities.append('ability_2[ice]')
								self.effectsClean()
								game.lastCell = None
								game.selectedcell = None
								if self.Passive1 in self.passives:
									self.actualType = 'fire'
									self.IMG.texture = Texture(self.imagesFire[0])
									effect = next(effect for effect in self.effects if effect['name'] == 
									'thermalCasualties')
									effect['value'] += -2
		
		elif self.actualType == 'fire':
			if not self.targetedCells:
				self.targetedCells = game.rangeCalculator(self, 
									 ct.TM_ABILITIES['ability_2[fire]']['minRange'],
									 ct.TM_ABILITIES['ability_2[fire]']['maxRange'],
									 True, False)
				game.hideCells(self.targetedCells)
			
			elif selectedcell:
				distanceX = selectedcell.coordX - self.coordX
				distanceY = selectedcell.coordY - self.coordY
				if distanceY == 0:
					if distanceX < 0:
						for cell in game.groundCells:
							if cell.coordY == self.coordY and \
							cell.coordX < self.coordX and \
							game.lineOfViewScan(self, cell):
								if not cell in self.zoneCells:
									self.zoneCells.append(cell)
							elif cell in self.zoneCells:
								self.zoneCells.remove(cell)
					
					elif distanceX > 0:
						for cell in game.groundCells:
							if cell.coordY == self.coordY and \
							cell.coordX > self.coordX and \
							game.lineOfViewScan(self, cell):
								if not cell in self.zoneCells:
									self.zoneCells.append(cell)
							elif cell in self.zoneCells:
								self.zoneCells.remove(cell)

				elif distanceX == 0:
					if distanceY < 0:
						for cell in game.groundCells:
							if cell.coordX == self.coordX and \
							cell.coordY < self.coordY and \
							game.lineOfViewScan(self, cell):
								if not cell in self.zoneCells:
									self.zoneCells.append(cell)
							elif cell in self.zoneCells:
								self.zoneCells.remove(cell)
								
					elif distanceY > 0:
						for cell in game.groundCells:
							if cell.coordX == self.coordX and \
							cell.coordY > self.coordY and \
							game.lineOfViewScan(self, cell):
								if not cell in self.zoneCells:
									self.zoneCells.append(cell)
							elif cell in self.zoneCells:
								self.zoneCells.remove(cell)
				
				for cell in self.zoneCells:
					if selectedcell in self.targetedCells:
						cell.cellType = 'SelectedCell'
			
			elif lastCell and not selectedcell and \
			self.stats['EP'] >= ct.TM_ABILITIES['ability_2[fire]']['EPcost'] and \
			self.stats['MP'] >= ct.TM_ABILITIES['ability_2[fire]']['MPcost']:
				if lastCell in self.targetedCells and not game.touchX:
					
					
					for entity in game.entityList:
						for cell2 in self.zoneCells:
							if entity.coordX == cell2.coordX and \
							entity.coordY == cell2.coordY:
								x = 0
								y = 0
								z = []
								for effect in entity.effects:
									if effect['name'] == 'fired' and \
									effect['source'] == self:
										if self.Passive5 in self.passives and \
										effect['duration'] == 1:
											effect['duration'] = 2
										x += 1
									elif effect['name'] == 'iced' and \
									effect['source'] == self:
										y += 1
										z.append(effect)
										
								if not x or self.Passive6 in self.passives:
									
									game.addStatEffect(self, entity, "fire")
									print('fired +1')
								
								entity.stats['health'] += game.valueCalculator(self, entity,
								ct.TM_ABILITIES['ability_2[fire]']['value']*(1+y*0.08), True, False, 'ability_2[fire]')
								hit = True
								for effect2 in z:
									entity.effects.remove(effect2)
									del effect2
					if hit:
						self.stats['EP'] -= ct.TM_ABILITIES['ability_2[fire]']['EPcost']
						self.stats['MP'] -= ct.TM_ABILITIES['ability_2[fire]']['MPcost']
						for button in game.buttons:
							if button[2]:
								button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
								button[2] = False
								self.action_sender('ability_2', [lastCell.coordX, lastCell.coordY])
								game.active_player.selectedAbility = None
								game.hideCells(self.targetedCells)
								self.targetedCells = None
								self.zoneCells = []
								self.played_abilities.append('ability_2[fire]')
								self.effectsClean()
								game.lastCell = None
								game.selectedcell = None
								if self.Passive1 in self.passives:
									self.actualType = 'ice'
									self.IMG.texture = Texture(self.imagesIce[0])
									effect = next(effect for effect in self.effects if effect['name'] == 
									'thermalCasualties')
									effect['value'] += -2
									
	def Ability3(self, selectedcell, lastCell, game):
		x = 0
		hit = None
		if self.actualType == 'ice':
			if not self.targetedCells:
				self.targetedCells = game.rangeCalculator(self, 
									 ct.TM_ABILITIES['ability_3[ice]']['minRange'],
									 ct.TM_ABILITIES['ability_3[ice]']['maxRange'],
									 True, True)
				game.hideCells(self.targetedCells)
				if not self.targetedCells:
					self.targetedCells.append(0)
				
			elif selectedcell:
				self.zoneCells = game.AreaCalculator('smallCone', self, selectedcell, self.zoneCells)
				for cell in self.zoneCells:
					if selectedcell in self.targetedCells:
						cell.cellType = 'SelectedCell'
						
			elif lastCell and not selectedcell and \
			self.stats['EP'] >= ct.TM_ABILITIES['ability_3[ice]']['EPcost'] and \
			self.stats['MP'] >= ct.TM_ABILITIES['ability_3[ice]']['MPcost']:
				for ability in self.played_abilities:
					if ability == 'ability_3[ice]':
						x += 1
				if lastCell in self.targetedCells and not game.touchX and not x:
					
							
					for entity in game.entityList:
						for cell2 in self.zoneCells:
							if entity.coordX == cell2.coordX and \
							entity.coordY == cell2.coordY:
								x = 0
								for effect in entity.effects:
									if effect['name'] == 'iced' and \
									effect['source'] == self:
										if self.Passive5 in self.passives and \
										effect['duration'] == 1:
											effect['duration'] = 2
										x += 1
								
								if not x or self.Passive5 in self.passives:
									
									game.addStatEffect(self, entity, "ice")
									
									game.addStatEffect(self, entity, "ice")
									print('iced +2')
								entity.stats['health'] += game.valueCalculator(self, entity,
								ct.TM_ABILITIES['ability_3[ice]']['value'], True, False, 'ability_3[ice]')
								hit = True
								if self.Passive2 in self.passives:
									x = []
									for effect in entity.effects:
										if effect['name'] == 'fired' and \
										effect['source'] == self:
											x.append(effect)
									for effect2 in x:
										entity.effects.remove(effect2)
										del effect2
										
										game.addStatEffect(self, entity, "ice")
								
						if entity.coordX == lastCell.coordX and \
						entity.coordY == lastCell.coordY:
							x = 0
							for effect in entity.effects:
								if effect['name'] == 'iced' and \
								effect['source'] == self:
									if self.Passive6 in self.passives and \
									effect['duration'] == 1:
										effect['duration'] = 2
									x += 1
									
							if not x or self.Passive5 in self.passives:
								
								game.addStatEffect(self, entity, "ice")
								
								game.addStatEffect(self, entity, "ice")
								
								game.addStatEffect(self, entity, "ice")
								print('iced +3')
							entity.stats['health'] += game.valueCalculator(self, entity,
							ct.TM_ABILITIES['ability_3[ice]']['value'], True, True, 'ability_3[ice]')
							hit = True
							if self.Passive2 in self.passives:
									x = []
									for effect in entity.effects:
										if effect['name'] == 'fired' and \
										effect['source'] == self:
											x.append(effect)
									for effect2 in x:
										entity.effects.remove(effect2)
										del effect2
										
										game.addStatEffect(self, entity, "ice")
						
					if hit:
						self.stats['EP'] -= ct.TM_ABILITIES['ability_3[ice]']['EPcost']
						self.stats['MP'] -= ct.TM_ABILITIES['ability_3[ice]']['MPcost']
						for button in game.buttons:
							if button[2]:
								button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
								button[2] = False
								self.action_sender('ability_3', [lastCell.coordX, lastCell.coordY])
								game.active_player.selectedAbility = None
								game.hideCells(self.targetedCells)
								self.targetedCells = None
								self.zoneCells = []
								self.played_abilities.append('ability_3[ice]')
								self.effectsClean()
								game.lastCell = None
								game.selectedcell = None
								if self.Passive1 in self.passives:
									self.actualType = 'fire'
									self.IMG.texture = Texture(self.imagesFire[0])
									effect = next(effect for effect in self.effects if effect['name'] == 
									'thermalCasualties')
									effect['value'] += -2
		
		elif self.actualType == 'fire':
			if not self.targetedCells:
				self.targetedCells = game.rangeCalculator(self, 
									 ct.TM_ABILITIES['ability_3[fire]']['minRange'],
									 ct.TM_ABILITIES['ability_3[fire]']['maxRange'],
									 True, True)
				game.hideCells(self.targetedCells)
			
			elif selectedcell:
				self.zoneCells = game.AreaCalculator('bigCone', self, selectedcell, self.zoneCells)
				for cell in self.zoneCells:
					if selectedcell in self.targetedCells:
						cell.cellType = 'SelectedCell'
						
			elif lastCell and not selectedcell and \
			self.stats['EP'] >= ct.TM_ABILITIES['ability_3[fire]']['EPcost'] and \
			self.stats['MP'] >= ct.TM_ABILITIES['ability_3[fire]']['MPcost']:
				if lastCell in self.targetedCells and not game.touchX:
					
							
					for entity in game.entityList:
						for cell2 in self.zoneCells:
							if entity.coordX == cell2.coordX and \
							entity.coordY == cell2.coordY:
								x = 0
								for effect in entity.effects:
									if effect['name'] == 'fired' and \
									effect['source'] == self:
										if self.Passive6 in self.passives and \
										effect['duration'] == 1:
											effect['duration'] = 2
										x += 1
								
								if not x or self.Passive6 in self.passives:
									
									game.addStatEffect(self, entity, "fire")
									
									game.addStatEffect(self, entity, "fire")
									print('fired +2')
								entity.stats['health'] += game.valueCalculator(self, entity,
								ct.TM_ABILITIES['ability_3[fire]']['value'], True, False, 'ability_3[fire]')
								hit = True
								if self.Passive2 in self.passives:
									x = []
									for effect in entity.effects:
										if effect['name'] == 'iced' and \
										effect['source'] == self:
											x.append(effect)
									for effect2 in x:
										entity.effects.remove(effect2)
										del effect2
										
										game.addStatEffect(self, entity, "fire")
								
						if entity.coordX == lastCell.coordX and \
						entity.coordY == lastCell.coordY:
							x = 0
							for effect in entity.effects:
								if effect['name'] == 'fired' and \
								effect['source'] == self:
									if self.Passive6 in self.passives and \
									effect['duration'] == 1:
										effect['duration'] = 2
									x += 1
									
							if not x or self.Passive6 in self.passives:
								
								game.addStatEffect(self, entity, "fire")
								
								game.addStatEffect(self, entity, "fire")
								
								game.addStatEffect(self, entity, "fire")
								print('fired +3')
							entity.stats['health'] += game.valueCalculator(self, entity,
							ct.TM_ABILITIES['ability_3[fire]']['value'], True, True, 'ability_3[fire]')
							hit = True
							if self.Passive2 in self.passives:
									x = []
									for effect in entity.effects:
										if effect['name'] == 'iced' and \
										effect['source'] == self:
											x.append(effect)
									for effect2 in x:
										entity.effects.remove(effect2)
										del effect2
										
										game.addStatEffect(self, entity, "fire")
						
					if hit:
						self.stats['EP'] -= ct.TM_ABILITIES['ability_3[fire]']['EPcost']
						self.stats['MP'] -= ct.TM_ABILITIES['ability_3[fire]']['MPcost']
						for button in game.buttons:
							if button[2]:
								button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
								button[2] = False
								self.action_sender('ability_3', [lastCell.coordX, lastCell.coordY])
								game.active_player.selectedAbility = None
								game.hideCells(self.targetedCells)
								self.targetedCells = None
								self.zoneCells = []
								self.played_abilities.append('ability_3[fire]')
								self.effectsClean()
								game.lastCell = None
								game.selectedcell = None
								if self.Passive1 in self.passives:
									self.actualType = 'ice'
									self.IMG.texture = Texture(self.imagesIce[0])
									effect = next(effect for effect in self.effects if effect['name'] == 
									'thermalCasualties')
									effect['value'] += -2
									
	def Ability4(self, selectedcell, lastCell, game):
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.TM_ABILITIES['ability_4']['minRange'],
								 ct.TM_ABILITIES['ability_4']['maxRange'],
								 True, False)
			game.hideCells(self.targetedCells)
		
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.TM_ABILITIES['ability_4']['EPcost'] and \
		self.stats['MP'] >= ct.TM_ABILITIES['ability_4']['MPcost']:
			if lastCell in self.targetedCells and not game.touchX:
				if self.actualType == 'ice':
					self.actualType = 'fire'
					self.IMG.texture = Texture(self.imagesFire[0])
				else:
					self.actualType = 'ice'
					self.IMG.texture = Texture(self.imagesIce[0])
		
				self.stats['EP'] -= ct.TM_ABILITIES['ability_4']['EPcost']
				self.stats['MP'] -= ct.TM_ABILITIES['ability_4']['MPcost']
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
		y = 0
		if self.actualType == 'ice':
			if not self.targetedCells:
				self.targetedCells = game.rangeCalculator(self, 
									 ct.TM_ABILITIES['ability_5[ice]']['minRange'],
									 ct.TM_ABILITIES['ability_5[ice]']['maxRange'],
									 True, False)
				game.hideCells(self.targetedCells)
			elif lastCell and not selectedcell and \
			self.stats['EP'] >= ct.TM_ABILITIES['ability_5[ice]']['EPcost'] and \
			self.stats['MP'] >= ct.TM_ABILITIES['ability_5[ice]']['MPcost']:
				if lastCell in self.targetedCells and not game.touchX:
					for ability in self.played_abilities:
						if ability == 'ability_5[ice]':
							x += 1
					
					for entity in game.entityList:
						if entity.coordX == lastCell.coordX and \
						entity.coordY == lastCell.coordY:
							x += 10
						elif entity.source == self:
							y += 1
					
					if y >= 3:
						x += 10
							
					if x == 0 or (x <= 1 and self.Passive4 in self.passives):
						iceBlock = IceBlock(lastCell.coordX, lastCell.coordY, game, self)
						self.stats['EP'] -= ct.TM_ABILITIES['ability_5[ice]']['EPcost']
						self.stats['MP'] -= ct.TM_ABILITIES['ability_5[ice]']['MPcost']
						for button in game.buttons:
							if button[2]:
								button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
								button[2] = False
								self.action_sender('ability_5', [lastCell.coordX, lastCell.coordY])
								game.active_player.selectedAbility = None
								game.hideCells(self.targetedCells)
								self.targetedCells = None
								self.zoneCells = []
								self.played_abilities.append('ability_5[ice]')
								self.effectsClean()
								game.lastCell = None
								game.selectedcell = None
								if self.Passive1 in self.passives:
									self.actualType = 'fire'
									self.IMG.texture = Texture(self.imagesFire[0])
									effect = next(effect for effect in self.effects if effect['name'] == 
									'thermalCasualties')
									effect['value'] += -2
		
		elif self.actualType == 'fire':
			if not self.targetedCells:
				self.targetedCells = game.rangeCalculator(self, 
									 ct.TM_ABILITIES['ability_5[fire]']['minRange'],
									 ct.TM_ABILITIES['ability_5[fire]']['maxRange'],
									 True, False)
				game.hideCells(self.targetedCells)
			elif lastCell and not selectedcell and \
			self.stats['EP'] >= ct.TM_ABILITIES['ability_5[fire]']['EPcost'] and \
			self.stats['MP'] >= ct.TM_ABILITIES['ability_5[fire]']['MPcost']:
				if lastCell in self.targetedCells and not game.touchX:
					lavaGusher = {'name': 'LavaGusher',
								'type': 'HPboost',
								'situation': 'Walk&Stay',
								'value': ct.TM_ABILITIES['ability_5[fire]']['value'],
								'duration_type': 'until_turns',
								'duration': 3,
								'source': self,
								'image': None}
					
					for ability in self.played_abilities:
						if ability == 'ability_5[fire]':
							x += 1
					
					for effect in lastCell.effects:
						if effect['name'] == 'LavaGusher' or \
						effect['name'] == 'SnowCover':
							x += 10
							
					if x < 2:
						lastCell.effects.append(lavaGusher)
						self.stats['EP'] -= ct.TM_ABILITIES['ability_5[fire]']['EPcost']
						self.stats['MP'] -= ct.TM_ABILITIES['ability_5[fire]']['MPcost']
						for button in game.buttons:
							if button[2]:
								button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
								button[2] = False
								self.action_sender('ability_5', [lastCell.coordX, lastCell.coordY])
								game.active_player.selectedAbility = None
								game.hideCells(self.targetedCells)
								self.targetedCells = None
								self.zoneCells = []
								self.played_abilities.append('ability_5[fire]')
								self.effectsClean()
								game.lastCell = None
								game.selectedcell = None
								if self.Passive1 in self.passives:
									self.actualType = 'ice'
									self.IMG.texture = Texture(self.imagesIce[0])
									effect = next(effect for effect in self.effects if effect['name'] == 
									'thermalCasualties')
									effect['value'] += -2
		
	def Ability6(self, selectedcell, lastCell, game):
		hit = None
		centerEntity = None
		if self.actualType == 'ice':
			if not self.targetedCells:
				self.targetedCells = game.rangeCalculator(self, 
									 ct.TM_ABILITIES['ability_6[ice]']['minRange'],
									 ct.TM_ABILITIES['ability_6[ice]']['maxRange'],
									 True, True)
				game.hideCells(self.targetedCells)
			elif selectedcell:
				self.zoneCells = game.AreaCalculator('smallLine', self, selectedcell, self.zoneCells)
				for cell in self.zoneCells:
						if selectedcell in self.targetedCells:
							cell.cellType = 'SelectedCell'
			
			elif lastCell and not selectedcell and \
			self.stats['EP'] >= ct.TM_ABILITIES['ability_6[ice]']['EPcost'] and \
			self.stats['MP'] >= ct.TM_ABILITIES['ability_6[ice]']['MPcost']:
				if lastCell in self.targetedCells and not game.touchX:
					for entity in game.entityList:
						
						
						for cell2 in self.zoneCells:
							if entity.coordX == cell2.coordX and \
							entity.coordY == cell2.coordY:
								x = 0
								for effect in entity.effects:
									if effect['name'] == 'iced' and \
									effect['source'] == self:
										if self.Passive5 in self.passives and \
										effect['duration'] == 1:
											effect['duration'] = 2
										x += 1
								
								if not x or self.Passive5 in self.passives:
									
									game.addStatEffect(self, entity, "ice")
									print('iced +1')
								entity.stats['health'] += game.valueCalculator(self, entity,
								ct.TM_ABILITIES['ability_6[ice]']['value'], True, False, 'ability_6[ice]')
								game.collisionCalculator(entity, 1, self, False)
								hit = True
								if self.Passive2 in self.passives:
									x = []
									for effect in entity.effects:
										if effect['name'] == 'fired' and \
										effect['source'] == self:
											x.append(effect)
									for effect2 in x:
										entity.effects.remove(effect2)
										del effect2
										
										game.addStatEffect(self, entity, "ice")
								
						if entity.coordX == lastCell.coordX and \
						entity.coordY == lastCell.coordY:
							x = 0
							for effect in entity.effects:
								if effect['name'] == 'iced' and \
								effect['source'] == self:
									if self.Passive5 in self.passives and \
									effect['duration'] == 1:
										effect['duration'] = 2
									x += 1
									
							if not x or self.Passive5 in self.passives:
								
								game.addStatEffect(self, entity, "ice")
								print('iced +1')
							entity.stats['health'] += game.valueCalculator(self, entity,
							ct.TM_ABILITIES['ability_6[ice]']['value'], True, True, 'ability_6[ice]')
							game.collisionCalculator(entity, 1, self, False)
							hit = True
							if self.Passive2 in self.passives:
									x = []
									for effect in entity.effects:
										if effect['name'] == 'fired' and \
										effect['source'] == self:
											x.append(effect)
									for effect2 in x:
										entity.effects.remove(effect2)
										del effect2
										
										game.addStatEffect(self, entity, "ice")
						
					if hit:
						self.stats['EP'] -= ct.TM_ABILITIES['ability_6[ice]']['EPcost']
						self.stats['MP'] -= ct.TM_ABILITIES['ability_6[ice]']['MPcost']
						for button in game.buttons:
							if button[2]:
								button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
								button[2] = False
								self.action_sender('ability_6', [lastCell.coordX, lastCell.coordY])
								game.active_player.selectedAbility = None
								game.hideCells(self.targetedCells)
								self.targetedCells = None
								self.zoneCells = []
								self.played_abilities.append('ability_6[ice]')
								self.effectsClean()
								game.lastCell = None
								game.selectedcell = None
								if self.Passive1 in self.passives:
									self.actualType = 'fire'
									self.IMG.texture = Texture(self.imagesFire[0])
									effect = next(effect for effect in self.effects if effect['name'] == 
									'thermalCasualties')
									effect['value'] += -2
		
		elif self.actualType == 'fire':
			if not self.targetedCells:
				self.targetedCells = game.rangeCalculator(self, 
									 ct.TM_ABILITIES['ability_6[fire]']['minRange'],
									 ct.TM_ABILITIES['ability_6[fire]']['maxRange'],
									 False, False)
				game.hideCells(self.targetedCells)
			elif selectedcell:
				self.zoneCells = game.AreaCalculator('smallArea', self, selectedcell, self.zoneCells)
				self.zoneCells.append(selectedcell)
				for cell in self.zoneCells:
					if selectedcell in self.targetedCells:
						cell.cellType = 'SelectedCell'
			
			elif lastCell and not selectedcell and \
			self.stats['EP'] >= ct.TM_ABILITIES['ability_6[fire]']['EPcost'] and \
			self.stats['MP'] >= ct.TM_ABILITIES['ability_6[fire]']['MPcost']:
				if lastCell in self.targetedCells and not game.touchX:
					for entity in game.entityList:
						
						
						for cell in self.zoneCells:
							if entity.coordX == cell.coordX and \
							entity.coordY == cell.coordY:
								x = 0
								for effect in entity.effects:
									if effect['name'] == 'fired' and \
									effect['source'] == self:
										if self.Passive6 in self.passives and \
										effect['duration'] == 1:
											effect['duration'] = 2
										x += 1
								
								if self.Passive2 in self.passives:
									x = []
									for effect in entity.effects:
										if effect['name'] == 'iced' and \
										effect['source'] == self:
											x.append(effect)
									for effect2 in x:
										entity.effects.remove(effect2)
										del effect2
										
										game.addStatEffect(self, entity, "fire")
										
								centerEntity = 0
								if self.Passive4 in self.passives:
									centerEntity = game.entityScan(lastCell.coordX, lastCell.coordY)
									if centerEntity:
										if centerEntity.source == self:
											if cell != lastCell:
												entity.stats['health'] += game.valueCalculator(self, entity,
												ct.TM_ABILITIES['ability_6[fire]']['value']+3, True, False,
												'ability_6[fire]')
												hit = True
												game.collisionCalculator(entity, 2, lastCell, True)
										else:
											if cell != lastCell:
												entity.stats['health'] += game.valueCalculator(self, entity,
												ct.TM_ABILITIES['ability_6[fire]']['value'], True, False,
												'ability_6[fire]')
												hit = True
												game.collisionCalculator(entity, 1, lastCell, True)
											else:
												entity.stats['health'] += game.valueCalculator(self, entity,
												ct.TM_ABILITIES['ability_6[fire]']['value'], True, False,
												'ability_6[fire]')
												hit = True
									else:
										entity.stats['health'] += game.valueCalculator(self, entity,
										ct.TM_ABILITIES['ability_6[fire]']['value'], True, False,
										'ability_6[fire]')
										hit = True
										
								else:
									entity.stats['health'] += game.valueCalculator(self, entity,
									ct.TM_ABILITIES['ability_6[fire]']['value'], True, False,'ability_6[fire]')
									hit = True
									if cell != lastCell:
										game.collisionCalculator(entity, 1, lastCell, True)
										
					if hit:
						if centerEntity:
							if centerEntity.source == self:
								centerEntity.stats['health'] = 0
						self.stats['EP'] -= ct.TM_ABILITIES['ability_6[fire]']['EPcost']
						self.stats['MP'] -= ct.TM_ABILITIES['ability_6[fire]']['MPcost']
						for button in game.buttons:
							if button[2]:
								button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
								button[2] = False
								self.action_sender('ability_6', [lastCell.coordX, lastCell.coordY])
								game.active_player.selectedAbility = None
								game.hideCells(self.targetedCells)
								self.targetedCells = None
								self.zoneCells = []
								self.played_abilities.append('ability_6[fire]')
								self.effectsClean()
								game.lastCell = None
								game.selectedcell = None
								if self.Passive1 in self.passives:
									self.actualType = 'ice'
									self.IMG.texture = Texture(self.imagesIce[0])
									effect = next(effect for effect in self.effects if effect['name'] == 
									'thermalCasualties')
									effect['value'] += -2								
			
	def Ability7(self, selectedcell, lastCell, game):
		hit = None
		if self.actualType == 'ice':
			if not self.targetedCells:
				self.targetedCells = game.rangeCalculator(self, 
									 ct.TM_ABILITIES['ability_7[ice]']['minRange'],
									 ct.TM_ABILITIES['ability_7[ice]']['maxRange'],
									 False, True)
				game.hideCells(self.targetedCells)
			
			elif lastCell and not selectedcell and \
			self.stats['EP'] >= ct.TM_ABILITIES['ability_7[ice]']['EPcost'] and \
			self.stats['MP'] >= ct.TM_ABILITIES['ability_7[ice]']['MPcost']:
				if lastCell in self.targetedCells and not game.touchX:
					for entity in game.entityList:
						
						
						if entity.coordX == lastCell.coordX and \
						entity.coordY == lastCell.coordY:
							for effect in entity.effects:
								if effect['name'] == 'iced' and \
								effect['source'] == self:
									if self.Passive5 in self.passives and \
									effect['duration'] == 1:
										effect['duration'] = 2
							
							if self.Passive2 in self.passives:
								x = []
								for effect in entity.effects:
									if effect['name'] == 'fired' and \
									effect['source'] == self:
										x.append(effect)
								for effect2 in x:
									entity.effects.remove(effect2)
									del effect2
									
									game.addStatEffect(self, entity, "ice")
							
							entity.stats['health'] += game.valueCalculator(self, entity,
							ct.TM_ABILITIES['ability_7[ice]']['value'], True, False, 'ability_7[ice]')
							self.stats['EP'] -= ct.TM_ABILITIES['ability_7[ice]']['EPcost']
							self.stats['MP'] -= ct.TM_ABILITIES['ability_7[ice]']['MPcost']
							for button in game.buttons:
								if button[2]:
									button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
									button[2] = False
									self.action_sender('ability_7', [lastCell.coordX, lastCell.coordY])
									game.active_player.selectedAbility = None
									game.hideCells(self.targetedCells)
									self.targetedCells = None
									self.zoneCells = []
									self.played_abilities.append('ability_7[ice]')
									self.effectsClean()
									game.lastCell = None
									game.selectedcell = None
									if self.Passive1 in self.passives:
										self.actualType = 'fire'
										self.IMG.texture = Texture(self.imagesFire[0])
										effect = next(effect for effect in self.effects if effect['name'] == 
										'thermalCasualties')
										effect['value'] += -2
										
		elif self.actualType == 'fire':
			if not self.targetedCells:
				self.targetedCells = game.rangeCalculator(self, 
									 ct.TM_ABILITIES['ability_7[fire]']['minRange'],
									 ct.TM_ABILITIES['ability_7[fire]']['maxRange'],
									 False, False)
				game.hideCells(self.targetedCells)
			
			elif selectedcell:
				self.zoneCells = game.AreaCalculator('bigArea', self, selectedcell, self.zoneCells)
				for cell in self.zoneCells:
						if selectedcell in self.targetedCells:
							cell.cellType = 'SelectedCell'
						if selectedcell == cell:
							self.zoneCells.remove(cell)
			
			elif lastCell and not selectedcell and \
			self.stats['EP'] >= ct.TM_ABILITIES['ability_7[fire]']['EPcost'] and \
			self.stats['MP'] >= ct.TM_ABILITIES['ability_7[fire]']['MPcost']:
				x = 0
				y = len(self.played_turns)
				for ability in self.played_abilities:
					if ability == 'ability_7[fire]':
						x += 1
				if y >= 1:
					for ability in self.played_turns[y-1]:
						if ability == 'ability_7[fire]':
							x += 1 
				if y >= 2:
					for ability in self.played_turns[y-2]:
						if ability == 'ability_7[fire]':
							x += 1
				
				if lastCell in self.targetedCells and not game.touchX and not x:
					for entity in game.entityList:
						
								
						for cell2 in self.zoneCells:
							if entity.coordX == cell2.coordX and \
							entity.coordY == cell2.coordY:
								x = 0
								for effect in entity.effects:
									if effect['name'] == 'fired' and \
									effect['source'] == self:
										if self.Passive6 in self.passives and \
										effect['duration'] == 1:
											effect['duration'] = 2
										x += 1
								
								if not x or self.Passive6 in self.passives:
									
									game.addStatEffect(self, entity, "fire")
									print('fired +1')
								entity.stats['health'] += game.valueCalculator(self, entity,
								ct.TM_ABILITIES['ability_7[fire]']['value'], True, False, 'ability_1[fire]')
								hit = True
								if self.Passive2 in self.passives:
									x = []
									for effect in entity.effects:
										if effect['name'] == 'iced' and \
										effect['source'] == self:
											x.append(effect)
									for effect2 in x:
										entity.effects.remove(effect2)
										del effect2
										
										game.addStatEffect(self, entity, "fire")
								
						if entity.coordX == lastCell.coordX and \
						entity.coordY == lastCell.coordY:
							x = 0
							for effect in entity.effects:
								if effect['name'] == 'fired' and \
								effect['source'] == self:
									if self.Passive6 in self.passives and \
									effect['duration'] == 1:
										effect['duration'] = 2
									x += 1
									
							if not x or self.Passive6 in self.passives:
								
								game.addStatEffect(self, entity, "fire")
								
								game.addStatEffect(self, entity, "fire")
								print('fired +2')
							entity.stats['health'] += game.valueCalculator(self, entity,
							ct.TM_ABILITIES['ability_7[fire]']['value'], True, True, 'ability_7[ice]')
							hit = True
							if self.Passive2 in self.passives:
									x = []
									for effect in entity.effects:
										if effect['name'] == 'iced' and \
										effect['source'] == self:
											x.append(effect)
									for effect2 in x:
										entity.effects.remove(effect2)
										del effect2
										
										game.addStatEffect(self, entity, "fire")
							
					if hit:
						self.stats['EP'] -= ct.TM_ABILITIES['ability_7[fire]']['EPcost']
						self.stats['MP'] -= ct.TM_ABILITIES['ability_7[fire]']['MPcost']
						for button in game.buttons:
							if button[2]:
								button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
								button[2] = False
								self.action_sender('ability_7', [lastCell.coordX, lastCell.coordY])
								game.active_player.selectedAbility = None
								game.hideCells(self.targetedCells)
								self.targetedCells = None
								self.zoneCells = []
								self.played_abilities.append('ability_7[fire]')
								self.effectsClean()
								game.lastCell = None
								game.selectedcell = None
								if self.Passive1 in self.passives:
									self.actualType = 'ice'
									self.IMG.texture = Texture(self.imagesIce[0])
									effect = next(effect for effect in self.effects if effect['name'] == 
									'thermalCasualties')
									effect['value'] += -2
									
	def Ability8(self, selectedcell, lastCell, game):
		x = 0
		hit = None
		if self.actualType == 'ice':
			if not self.targetedCells:
				self.targetedCells = game.rangeCalculator(self, 
									 ct.TM_ABILITIES['ability_8[ice]']['minRange'],
									 ct.TM_ABILITIES['ability_8[ice]']['maxRange'],
									 True, True)
				game.hideCells(self.targetedCells)
			elif selectedcell:
				self.zoneCells = game.AreaCalculator('smallArea', self, selectedcell, self.zoneCells)
				for cell in self.zoneCells:
						if selectedcell in self.targetedCells:
							cell.cellType = 'SelectedCell'
								
			elif lastCell and not selectedcell and \
			self.stats['EP'] >= ct.TM_ABILITIES['ability_8[ice]']['EPcost'] and \
			self.stats['MP'] >= ct.TM_ABILITIES['ability_8[ice]']['MPcost']:
				for ability in self.played_abilities:
					if ability == 'ability_8[ice]':
						x +=1
						
				if lastCell in self.targetedCells and not game.touchX and not x:
					self.zoneCells.append(lastCell)
					for cell in self.zoneCells:
						x = 0
						SnowCover = {'name': 'SnowCover',
									'type': 'MPboost',
									'situation': 'Walk',
									'value': ct.TM_ABILITIES['ability_8[ice]']['value'],
									'duration_type': 'next_walk',
									'duration': 1,
									'source': self,
									'image': None}
						for effect in cell.effects:
							if effect['name'] == 'SnowCover' or \
							effect['name'] == 'LavaGusher' or \
							effect['name'] == 'EmberMat':
								x += 1
						
						if not x:
							game.addGroundEffect(self, cell, "SnowCover")
							hit = True
					
					if hit:
						self.stats['EP'] -= ct.TM_ABILITIES['ability_8[ice]']['EPcost']
						self.stats['MP'] -= ct.TM_ABILITIES['ability_8[ice]']['MPcost']
						for button in game.buttons:
							if button[2]:
								button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
								button[2] = False
								self.action_sender('ability_8', [lastCell.coordX, lastCell.coordY])
								game.active_player.selectedAbility = None
								game.hideCells(self.targetedCells)
								self.targetedCells = None
								self.zoneCells = []
								self.played_abilities.append('ability_8[ice]')
								self.effectsClean()
								game.lastCell = None
								game.selectedcell = None
								if self.Passive1 in self.passives:
									self.actualType = 'fire'
									self.IMG.texture = Texture(self.imagesFire[0])
									effect = next(effect for effect in self.effects if effect['name'] == 
									'thermalCasualties')
									effect['value'] += -2
									
		elif self.actualType == 'fire':
			if not self.targetedCells:
				self.targetedCells = game.rangeCalculator(self, 
									 ct.TM_ABILITIES['ability_8[fire]']['minRange'],
									 ct.TM_ABILITIES['ability_8[fire]']['maxRange'],
									 True, True)
				game.hideCells(self.targetedCells)
			elif selectedcell:
				self.zoneCells = game.AreaCalculator('mediumArea', self, selectedcell, self.zoneCells)
				for cell in self.zoneCells:
					if selectedcell in self.targetedCells:
						cell.cellType = 'SelectedCell'
								
			elif lastCell and not selectedcell and \
			self.stats['EP'] >= ct.TM_ABILITIES['ability_8[fire]']['EPcost'] and \
			self.stats['MP'] >= ct.TM_ABILITIES['ability_8[fire]']['MPcost']:
				for ability in self.played_abilities:
					if ability == 'ability_8[fire]':
						x +=1
						
				if lastCell in self.targetedCells and not game.touchX and not x:
					self.zoneCells.append(lastCell)
					for cell in self.zoneCells:
						x = 0
						EmberMat = {'name': 'EmberMat',
								  'type': 'HPboost',
								  'situation': 'Walk&Stay',
								  'value': -2,
								  'duration_type': 'until_turns',
								  'duration': 2,
								  'source': self,
								  'image': None}
						for effect in cell.effects:
							if effect['name'] == 'SnowCover' or \
							effect['name'] == 'EmberMat':
								x += 1
						
						if not x:
							game.addGroundEffect(self, cell, "EmberMat")
							hit = True
					
					if hit:
						self.stats['EP'] -= ct.TM_ABILITIES['ability_8[fire]']['EPcost']
						self.stats['MP'] -= ct.TM_ABILITIES['ability_8[fire]']['MPcost']
						for button in game.buttons:
							if button[2]:
								button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
								button[2] = False
								self.action_sender('ability_8', [lastCell.coordX, lastCell.coordY])
								game.active_player.selectedAbility = None
								game.hideCells(self.targetedCells)
								self.targetedCells = None
								self.zoneCells = []
								self.played_abilities.append('ability_8[fire]')
								self.effectsClean()
								game.lastCell = None
								game.selectedcell = None
								if self.Passive1 in self.passives:
									self.actualType = 'ice'
									self.IMG.texture = Texture(self.imagesIce[0])
									effect = next(effect for effect in self.effects if effect['name'] == 
									'thermalCasualties')
									effect['value'] += -2
							
	def Ability9(self, selectedcell, lastCell, game):
		x = 0
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.TM_ABILITIES['ability_9']['minRange'],
								 ct.TM_ABILITIES['ability_9']['maxRange'],
								 True, True)
			game.hideCells(self.targetedCells)
		
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.TM_ABILITIES['ability_9']['EPcost'] and \
		self.stats['MP'] >= ct.TM_ABILITIES['ability_9']['MPcost']:
			if lastCell in self.targetedCells and not game.touchX:
				for effect in self.effects:
					if effect['name'] == 'Cryonics':
						x += 1
				
				if not x:
					game.addStatEffect(self, self, "cryonics")
					self.stats['EP'] -= ct.TM_ABILITIES['ability_9']['EPcost']
					self.stats['MP'] -= ct.TM_ABILITIES['ability_9']['MPcost']
					for button in game.buttons:
						if button[2]:
							button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
							button[2] = False
							self.action_sender('ability_9', [lastCell.coordX, lastCell.coordY])
							game.active_player.selectedAbility = None
							game.hideCells(self.targetedCells)
							self.targetedCells = None
							self.zoneCells = []
							self.played_abilities.append('ability_9')
							self.effectsClean()
							game.lastCell = None
							game.selectedcell = None
							game.play_button_touched = True
						
	def Ability10(self, selectedcell, lastCell, game):
		x = 0
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.TM_ABILITIES['ability_10']['minRange'],
								 ct.TM_ABILITIES['ability_10']['maxRange'],
								 True, True)
			game.hideCells(self.targetedCells)
			
		elif selectedcell:
			game.AreaCalculator('perpLine', self, selectedcell, self.zoneCells)
			for cell in self.zoneCells:
				if selectedcell in self.targetedCells:
					cell.cellType = 'SelectedCell'
		
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.TM_ABILITIES['ability_10']['EPcost'] and \
		self.stats['MP'] >= ct.TM_ABILITIES['ability_10']['MPcost']:
			if lastCell in self.targetedCells and not game.touchX:
				for cell2 in game.groundCells:
					for effect in cell2.effects:
						if effect['name'] == 'SmokeWall' and \
						effect['source'] == self:
							x += 1
				if not x:
					for cell in self.zoneCells:
						game.addGroundEffect(self, cell, "SmokeWall")
						
					self.stats['EP'] -= ct.TM_ABILITIES['ability_10']['EPcost']
					self.stats['MP'] -= ct.TM_ABILITIES['ability_10']['MPcost']
					for button in game.buttons:
						if button[2]:
							button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
							button[2] = False
							self.action_sender('ability_10', [lastCell.coordX, lastCell.coordY])
							game.active_player.selectedAbility = None
							game.hideCells(self.targetedCells)
							self.targetedCells = None
							self.zoneCells = []
							self.played_abilities.append('ability_10')
							game.lastCell = None
							game.selectedcell = None
							self.effectsClean()			
				
	def Passive1(self):
		thermalCasualties = {'name': 'thermalCasualties',
							'type': 'HPboost',
							'situation': 'turnBegin',
							'value': 0,
							'duration_type': 'infinitely',
							'duration': 999,
							'source': self}
		if not thermalCasualties in self.effects:
			self.effects.append(thermalCasualties)
		
	def Passive2(self):
		pass # fusion des pôles (fait)
		
	def Passive3(self):
		pass # celsius extrême (fait)
		
	def Passive4(self):
		pass # reaction en chaine (fait)
		
	def Passive5(self):
		pass # polarité glaciale (fait)
		
	def Passive6(self):
		pass # polarité flamboyante (fait)
			
			
class IceBlock(Entity):
	def __init__(self, coordX, coordY, game, source):
		Entity.__init__(self)
		self.IMG = SpriteNode('Images/Thermal Mage/IceBlock.PNG')
		self.IMG.anchor_point = (0, 1)
		self.IMG.z_position = 3.0+0.01*coordY-0.01
		self.IMG.x_scale = 0.01*ct.CELL_X-0.04
		self.IMG.y_scale = 0.01*ct.CELL_Y+0.15
		self.IMG.position = (game.cellScan(coordX, coordY).IMG.position[0]+2, 
							game.cellScan(coordX, coordY).IMG.position[1]+15)
		game.add_child(self.IMG)
		game.entityList.append(self)
		game.mainList.append(self)
		self.coordX = coordX
		self.coordY = coordY
		self.source = source
		self.stats = {'health': ct.TM_ABILITIES['ability_5[ice]']['value'],
					  'MP': 0,
					  'EP': 0,
					  'orientation': None}
		self.Startstats = {'health': ct.TM_ABILITIES['ability_5[ice]']['value'],
						  'MP': 0,
						  'EP': 0,
						  'orientation': None}
	
	def stateCheck(self, game):
		if self.source.Passive4 in self.source.passives:
			self.cell = game.cellScan(self.coordX, self.coordY)
			for effect in self.cell.effects:
				if effect['name'] == 'LavaGusher' and \
				effect['source'] == self.source:
					zoneCells = []
					zoneCells = game.AreaCalculator('bigArea', self, self.cell, zoneCells)
					entitiesToPush = []
					for cell in zoneCells:
						x = 0
						EmberMat = {'name': 'EmberMat',
								  'type': 'HPboost',
								  'situation': 'Walk&Stay',
								  'value': -2,
								  'duration_type': 'until_turns',
								  'duration': 2,
								  'source': self,
								  'image': None}
						for effect2 in cell.effects:
							if effect2['name'] == 'EmberMat':
								effect2['duration'] += 1
								x += 1
							elif effect2['name'] == 'SnowCover':
								x += 1
						if not x:
							game.addGroundEffect(self, cell, "EmberMat")
							
						for entity in game.entityList:
							if entity.coordX == cell.coordX and \
							entity.coordY == cell.coordY and not entity == self:
								entity.stats['health'] += game.valueCalculator(self, entity,
								ct.TM_ABILITIES['ability_5[fire]']['value'], True, True, 'ability_5[fire]')
								if self.cell.coordX == entity.coordX or \
								self.cell.coordY == entity.coordY:
									if not entity in entitiesToPush:
										entitiesToPush.append(entity)
					
					for entity2 in entitiesToPush:
						distanceX = abs(self.coordX-entity2.coordX)
						distanceY = abs(self.coordY-entity2.coordY)
						if distanceX == 2 or distanceY == 2:
							game.collisionCalculator(entity2, 1, self, False)
					
					for entity3 in entitiesToPush:
						distanceX = abs(self.coordX-entity3.coordX)
						distanceY = abs(self.coordY-entity3.coordY)
						if distanceX == 1 or distanceY == 1:
							game.collisionCalculator(entity3, 1, self, False)
					
					effect['duration'] = 0
					self.stats['health'] = 0
					
