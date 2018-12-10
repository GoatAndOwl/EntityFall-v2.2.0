from scene import *
from Classes import *
import Constants as ct
import random

class Paladin(Entity):
	def __init__(self, player):
		Entity.__init__(self)
		self.type = 'Light'
		self.images = [['Images/Paladin/PaladinFace0-0.PNG']]
		self.IMG = SpriteNode(self.images[0][0])
		self.IMG.anchor_point = (0, 1)
		self.IMG.x_scale = 0.01*ct.CELL_X
		self.IMG.y_scale = 0.01*ct.CELL_Y+0.15
		self.IMG.position = (-250,-250)
		self.IMG.z_position = 2.0
		self.classSetup(player['abilities'], player['passives'])
		self.targetedCells = None
		self.name = 'Paladin'
		self.team = player['team']
		self.stats = {'health': ct.PL_STATS['health'],
					  'MP': ct.PL_STATS['MP'],
					  'EP': ct.PL_STATS['EP'],
					  'orientation': None}
		self.Startstats = {'health': ct.PL_STATS['health'],
					  'MP': ct.PL_STATS['MP'],
					  'EP': ct.PL_STATS['EP'],
					  'orientation': None}

	def ImpiousGen(self, entity, nb):
		for x in range(0, nb):
			self.controller.game.addStatEffect(self, entity, 'impious')
	
	def Ability1(self, selectedcell, lastCell, game):
		x = 0
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.PL_ABILITIES['ability_1']['minRange'],
								 ct.PL_ABILITIES['ability_1']['maxRange'],
								 True, False)
			game.hideCells(self.targetedCells)
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.PL_ABILITIES['ability_1']['EPcost'] and \
		self.stats['MP'] >= ct.PL_ABILITIES['ability_1']['MPcost']:
			for ability in self.played_abilities:
				if ability == 'ability_1':
					x += 1
					
			if lastCell in self.targetedCells and x < 3:
				for entity in game.entityList:
					for effect in entity.effects:
						if effect['name'] == 'impious':
							x += 3
					if entity.coordX == lastCell.coordX and \
					entity.coordY == lastCell.coordY and x < 3:
						entity.stats['health'] += game.valueCalculator(self, 
						entity, ct.PL_ABILITIES['ability_1']['value'], False, True, True)
						
						if entity.stats['health'] > entity.Startstats['health']:
							entity.stats['health'] = entity.Startstats['health']
							
						self.stats['EP'] -= ct.PL_ABILITIES['ability_1']['EPcost']
						self.stats['MP'] -= ct.PL_ABILITIES['ability_1']['MPcost']
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
		x = 0
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.PL_ABILITIES['ability_2']['minRange'],
								 ct.PL_ABILITIES['ability_2']['maxRange'],
								 True, False)
			game.hideCells(self.targetedCells)
		elif selectedcell:
			self.zoneCells = game.AreaCalculator('bigArea', self, selectedcell, self.zoneCells)
			for cell in self.zoneCells:
				if selectedcell in self.targetedCells:
					cell.cellType = 'SelectedCell'
			if not selectedcell in self.zoneCells:
				self.zoneCells.append(selectedcell)
			
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.PL_ABILITIES['ability_2']['EPcost'] and \
		self.stats['MP'] >= ct.PL_ABILITIES['ability_2']['MPcost']:
			x = 0
			y = len(self.played_turns)
			for ability in self.played_abilities:
				if ability == 'ability_2':
					x += 1
			if y >= 1:
				for ability in self.played_turns[y-1]:
					if ability == 'ability_2':
						x += 1
					
			if lastCell in self.targetedCells and x < 1:
				for cell in self.zoneCells:
					if cell in game.groundCells:
						game.addGroundEffect(self, cell, 'ShieldProtection')
					
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
								 ct.PL_ABILITIES['ability_3']['minRange'],
								 ct.PL_ABILITIES['ability_3']['maxRange'],
								 True, False)
			game.hideCells(self.targetedCells)
		elif selectedcell:
			self.zoneCells = game.AreaCalculator('mediumArea', self, selectedcell, self.zoneCells)
			for cell in self.zoneCells:
				if selectedcell in self.targetedCells:
					cell.cellType = 'SelectedCell'
			if not selectedcell in self.zoneCells:
				self.zoneCells.append(selectedcell)
			
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.PL_ABILITIES['ability_3']['EPcost'] and \
		self.stats['MP'] >= ct.PL_ABILITIES['ability_3']['MPcost']:
			x = 0
			y = len(self.played_turns)
			for ability in self.played_abilities:
				if ability == 'ability_3':
					x += 1
			if y >= 1:
				for ability in self.played_turns[y-1]:
					if ability == 'ability_3':
						x += 1
			
			for cell in self.zoneCells:
				entity = game.entityScan(cell.coordX, cell.coordY)
				if entity:
					if entity != self:
						x += 1
				
			if lastCell in self.targetedCells and x < 1:
				for cell in self.zoneCells:
					if cell in game.groundCells:
						game.addGroundEffect(self, cell, 'Sanctuary')
					
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
						self.played_abilities.append('ability_3')
						self.effectsClean()					
	
	def Ability4(self, selectedcell, lastCell, game):
		x = 0
		if not self.targetedCells:
			self.targetedCells = game.rangeCalculator(self, 
								 ct.PL_ABILITIES['ability_4']['minRange'],
								 ct.PL_ABILITIES['ability_4']['maxRange'],
								 True, False)
			game.hideCells(self.targetedCells)
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.PL_ABILITIES['ability_4']['EPcost'] and \
		self.stats['MP'] >= ct.PL_ABILITIES['ability_4']['MPcost']:
			if lastCell in self.targetedCells:
				for entity in game.entityList:
					if entity.coordX == lastCell.coordX and \
					entity.coordY == lastCell.coordY:
						if entity.stats['health'] <= 0:
							y = round(entity.Startstats['health']*ct.PL_ABILITIES['ability_4']['value'])
							entity.stats['health'] = y
							entity.deathCount -= 1
							game.valueDraw(entity, y, 'top')
							
							self.stats['EP'] -= ct.PL_ABILITIES['ability_4']['EPcost']
							self.stats['MP'] -= ct.PL_ABILITIES['ability_4']['MPcost']
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
								 ct.PL_ABILITIES['ability_5']['minRange'],
								 ct.PL_ABILITIES['ability_5']['maxRange'],
								 True, False)
			game.hideCells(self.targetedCells)
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.PL_ABILITIES['ability_5']['EPcost'] and \
		self.stats['MP'] >= ct.PL_ABILITIES['ability_5']['MPcost']:
			if lastCell in self.targetedCells:
				for ability in self.played_abilities:
					if ability == 'ability_5':
						x += 1
				for entity in game.entityList:
					if entity.coordX == lastCell.coordX and \
					entity.coordY == lastCell.coordY and not x:
						game.addStatEffect(self, entity, 'blessed')
						
						self.stats['EP'] -= ct.PL_ABILITIES['ability_5']['EPcost']
						self.stats['MP'] -= ct.PL_ABILITIES['ability_5']['MPcost']
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
								 ct.PL_ABILITIES['ability_6']['minRange'],
								 ct.PL_ABILITIES['ability_6']['maxRange'],
								 True, False)
			for entity in game.entityList:
				self.targetedCells.append(game.cellScan(entity.coordX, entity.coordY))
				
			game.hideCells(self.targetedCells)
		elif lastCell and not selectedcell and \
		self.stats['EP'] >= ct.PL_ABILITIES['ability_6']['EPcost'] and \
		self.stats['MP'] >= ct.PL_ABILITIES['ability_6']['MPcost']:
			if lastCell in self.targetedCells:
				for ability in self.played_abilities:
					if ability == 'ability_6':
						x += 1
				for entity in game.entityList:
					if entity.coordX == lastCell.coordX and \
					entity.coordY == lastCell.coordY and not x:
						if entity == self:
							effect = ['Moment Of Peace', self, int(game.day_counter)]
						elif entity.team == self.team:
							effect = ['Crusade', self, int(game.day_counter)]
						elif entity.team != self.team:
							effect = ['Divine Fury', self, int(game.day_counter)]
							print('divine fury applied')
						for effect2 in game.day_effects:
							if effect2[1] == self:
								game.day_effects.remove(effect2)
						game.day_effects.append(effect)
						self.stats['EP'] -= ct.PL_ABILITIES['ability_6']['EPcost']
						self.stats['MP'] -= ct.PL_ABILITIES['ability_6']['MPcost']
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
		pass
	
	def Ability8(self, selectedcell, lastCell, game):
		pass
	
	def Ability9(self, selectedcell, lastCell, game):
		pass
	
	def Ability10(self, selectedcell, lastCell, game):
		pass
	
	def Passive1(self):
		pass
		
	def Passive2(self):
		pass
		
	def Passive3(self):
		pass
		
	def Passive4(self):
		pass
		
	def Passive5(self):
		pass
	
	def Passive6(self):
		pass
