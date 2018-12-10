from scene import *
import Constants as ct
import GameInterface as gi
import Classes as cl
import random, time, json

class Game(Scene):
	def setup(self):
		self.background_color = ct.BACKGROUND_COLOR
		self.z_value = 4.0
		self.map = []
		self.isMovingCam = False
		self.mainList = []
		self.IMGList = []
		self.entityList = []
		self.groundCells = []
		self.obstacles = []
		self.buttons = []
		self.playerList = []
		self.valueList = []
		self.active_player = None
		self.loadMap()
		self.touchX = 0
		self.touchY = 0
		self.touchX2 = 0
		self.touchY2 = 0
		self.play_button_touched = False
		self.informations = []
		self.entity_to_show = None
		self.isShowingEffects = False
		self.isShowingDetails = False
		self.shownEffects = []
		self.details = []
		self.selectedCell = None
		self.lastCell = None
		self.stats_background = None
		self.turn_indicator = None
		self.day_indicator = None
		self.day_effects = []
		self.day_counter = 0
		self.play_button_reset = time.time()
		self.turn_order = 0
		self.game_phase = None
		self.time = time.time()
		self.time2 = time.time()
		self.time3 = None
		self.time4 = None
		self.setupGame()
	
	def stop(self):
		ct.STARTED = False
		ct.LAUNCHED = False
		ct.SOUND_PLAYER.music.stop()
				
	def loadMap(self):
		# crée les instances de classe Cell qui composent la map à partir du mapC
		mapC = ct.SELECTED_MAP
		startPoint = [self.size.w / 2 - len(mapC[0]) * ct.CELL_X / 2,
									self.size.h / 2 + len(mapC) * ct.CELL_Y / 2]
		x, y = 0, 0
		
		for ligne in mapC:
			self.map.append([])
			i = self.map.index([])
			x = 0
			y += 1
			for cell in ligne: # génère les classes Cell de la map
				x += 1
				if cell == 0:
					cell = cl.Cell(spawnX= (x-1) * ct.CELL_X + startPoint[0],
												 spawnY= startPoint[1] - (y-1) * ct.CELL_Y,
												 cellType="freeCell", coordX=x,
												 coordY=y)
					self.add_child(cell.IMG)
					self.map[i].append(cell)
					self.groundCells.append(cell)
				elif cell == 1:
					cell = cl.Cell(spawnX= (x-1) * ct.CELL_X + startPoint[0],
												 spawnY= startPoint[1] - (y-1) * ct.CELL_Y,
												 cellType="obstacle", coordX=x,
												 coordY=y)
					cell.IMG.z_position += y*0.01-0.01
					self.add_child(cell.IMG)
					self.map[i].append(cell)
					self.obstacles.append(cell)
					
				elif cell == 2:
					cell = cl.Cell(spawnX= (x-1) * ct.CELL_X + startPoint[0],
												 spawnY= startPoint[1] - (y-1) * ct.CELL_Y,
												 cellType="VoidCell", coordX=x,
												 coordY=y)
					self.add_child(cell.IMG)
					self.map[i].append(cell)
	
				elif cell == 3:
					cell = cl.Cell(spawnX= (x-1) * ct.CELL_X + startPoint[0],
												 spawnY= startPoint[1] - (y-1) * ct.CELL_Y,
												 cellType="BlueCell", coordX=x,
												 coordY=y)
					self.add_child(cell.IMG)
					self.map[i].append(cell)
					self.groundCells.append(cell)
				elif cell == 4:
					cell = cl.Cell(spawnX= (x-1) * ct.CELL_X + startPoint[0],
												 spawnY= startPoint[1] - (y-1) * ct.CELL_Y,
												 cellType="RedCell", coordX=x,
												 coordY=y)
					self.add_child(cell.IMG)
					self.map[i].append(cell)
					self.groundCells.append(cell)
					
				self.mainList.append(cell)
		
	def touch_began(self, touch):
		self.touchX, self.touchY = touch.location
		self.touchX2, self.touchY2 = touch.location
		self.screen_touched = True
		if self.size.w-180 <= self.touchX <= self.size.w+1000 and \
		-1000 <= self.touchY <= 80 and self.play_button_reset <= time.time()-0.5 and \
		not self.isShowingEffects:
			if not ct.onlineMulti or self.active_player.id == ct.CLIENT_ID:
				self.play_button.color = self.active_player.team
				self.play_button_touched = True
				self.selectedCell = None
				self.lastCell = None
				self.play_button_reset = time.time()
			
		x = 0
		for button in self.buttons:
			if button[0].position[0]-40 < self.touchX < button[0].position[0]+40 \
			and button[0].position[1]-40 < self.touchY < button[0].position[1]+40 \
			and not self.active_player.entity.isMoving and not self.isMovingCam and \
			not self.isShowingEffects and (not ct.onlineMulti or self.active_player.id == ct.CLIENT_ID):
				if not button[2]:
					if self.active_player.selectedAbility:
						for button2 in self.buttons:
							if button2[2]:
								button2[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
								button2[2] = False
								if self.active_player.entity.targetedCells:
									self.hideCells(self.active_player.entity.targetedCells)
								self.active_player.selectedAbility = None
								self.active_player.entity.targetedCells = None
								self.selectedCell = None
								self.lastCell = None
								
					if self.active_player.team == 'blue':
						button[0].texture = Texture('Images/In-Game Ui/Ability(Blue).PNG')
					elif self.active_player.team == 'red':
						button[0].texture = Texture('Images/In-Game Ui/Ability(Red).PNG')
					button[2] = True
					self.active_player.selectedAbility = button[3]
					self.selectedCell = None
					self.lastCell = None
					self.time3 = time.time()
					self.time4 = time.time()
				elif button[2]:
					button[0].texture = Texture('Images/In-Game Ui/Ability(Grey).PNG')
					button[2] = False
					self.active_player.selectedAbility = None
					if self.active_player.entity.targetedCells:
						self.hideCells(self.active_player.entity.targetedCells)
					self.active_player.entity.targetedCells = None
					self.selectedCell = None
					self.lastCell = None
		
		if not self.isShowingEffects:
			self.eventScan()
			if self.selectedCell and self.game_phase == 'Fight':
				entity = self.entityScan(self.selectedCell.coordX, self.selectedCell.coordY)
				if entity:
					if self.entity_to_show != entity:
						self.entity_to_show = entity
						self.time2 = time.time()
					elif self.entity_to_show == entity:
						self.showEffects(self.entity_to_show)
		
		elif self.isShowingEffects:
			self.isShowingEffects = False
			for a in range(0,2):
				self.shownEffects[len(self.shownEffects)-1].remove_from_parent()
				del self.shownEffects[len(self.shownEffects)-1]
			for effect in self.shownEffects:
				effect[1].remove_from_parent()
				
			for effect2 in self.shownEffects:
				del effect2[1]
				del effect2[0]
			self.shownEffects = []
			self.entity_to_show = None
			
		if self.game_phase == 'Placement' or (self.game_phase == 'Fight' and not self.active_player.selectedAbility and not self.active_player.isMoving and not self.isShowingEffects):
			self.isMovingCam = True
				
	def touch_moved(self, touch):
		self.touchX2, self.touchY2 = touch.location
	
	def touch_ended(self, touch):
		self.touchX, self.touchX2, self.touchY, self.touchY2 = 0, 0, -20000, -20000
		self.play_button.color = None
		if not ct.onlineMulti or self.active_player.id == ct.CLIENT_ID:
			self.play_button_touched = False
		self.screen_touched = False
		self.isMovingCam = False
		self.time3 = None
		if self.isShowingDetails:
			for details in self.details:
				details.remove_from_parent()
			self.details = []
			self.isShowingDetails = False
		
	def eventScan(self):
		x = 0
		for cell in self.groundCells:
			if cell.IMG.position[0] < self.touchX2 < \
			cell.IMG.position[0] + ct.CELL_X and \
			cell.IMG.position[1] > self.touchY2 > \
			cell.IMG.position[1] - ct.CELL_Y and self.touchY2 > 85:
				if cell.cellType != 'hidenCell':
					cell.cellType = 'SelectedCell'
				self.selectedCell = cell
				self.lastCell = cell
				x = 1
			else:
				cell.cellType = cell.initialCellType
				
		if not x:
			self.selectedCell = None
	
	def update(self):
		x = None
		for player in self.playerList:
			if ct.singlePlayer:
				player.isPlaying = True
			if self.active_player == player:
				if not self.isShowingEffects and not self.isShowingDetails:
					self.eventScan()
					player.turnControl()
		
		if self.time3 and self.touchX:
			if self.touchX2:
				for button in self.buttons:
					if button[0].position[0]-40 < self.touchX2 < button[0].position[0]+40 \
					and button[0].position[1]-40 < self.touchY2 < button[0].position[1]+40 \
					and not self.active_player.entity.isMoving and not self.isMovingCam and \
					not self.isShowingEffects and (not ct.onlineMulti or self.active_player.id == ct.CLIENT_ID):
						if button[2] and time.time() >= self.time3+0.75 and not self.isShowingDetails:
							self.drawDetails(button)
							self.isShowingDetails = True
							
			else:
				for button in self.buttons:
					if button[0].position[0]-40 < self.touchX < button[0].position[0]+40 \
					and button[0].position[1]-40 < self.touchY < button[0].position[1]+40 \
					and not self.active_player.entity.isMoving and not self.isMovingCam and \
					not self.isShowingEffects and (not ct.onlineMulti or self.active_player.id == ct.CLIENT_ID):
						if button[2] and time.time() >= self.time3+0.75 and not self.isShowingDetails:
							self.drawDetails(button)
							self.isShowingDetails = True
		
		if self.isMovingCam:
			self.moveCam()
		
		if self.active_player.entity.name == 'Thermal Mage':
			for button in self.buttons:
				if button[4] == 'ability_1':
					button[5].texture = Texture('Images/Thermal Mage/Ability1['+
												self.active_player.entity.actualType+
												'].PNG')
				if button[4] == 'ability_2':
					button[5].texture = Texture('Images/Thermal Mage/Ability2['+
												self.active_player.entity.actualType+
												'].PNG')
				if button[4] == 'ability_3':
					button[5].texture = Texture('Images/Thermal Mage/Ability3['+
												self.active_player.entity.actualType+
												'].PNG')
				if button[4] == 'ability_5':
					button[5].texture = Texture('Images/Thermal Mage/Ability5['+
												self.active_player.entity.actualType+
												'].PNG')
				if button[4] == 'ability_6':
					button[5].texture = Texture('Images/Thermal Mage/Ability6['+
												self.active_player.entity.actualType+
												'].PNG')
				if button[4] == 'ability_7':
					button[5].texture = Texture('Images/Thermal Mage/Ability7['+
												self.active_player.entity.actualType+
												'].PNG')
				if button[4] == 'ability_8':
					button[5].texture = Texture('Images/Thermal Mage/Ability8['+
												self.active_player.entity.actualType+
												'].PNG')
		for entity in self.entityList:
			if entity.stats['EP'] < 0:
				entity.stats['EP'] = 0
			if entity.stats['MP'] < 0:
				entity.stats['MP'] = 0
				
			if entity.IMG:
				entity.IMG.z_position = 3+entity.coordY*0.01-0.01
			if len(entity.hud) and entity.controller in self.playerList:
				entity.hud[0].z_position = 3+entity.coordY*0.01
				entity.hud[6].z_position = 3+entity.coordY*0.01
				entity.hud[7].z_position = 3+entity.coordY*0.01
				entity.hud[8].z_position = 3+entity.coordY*0.01
				if entity.stats['health']/entity.Startstats['health'] > 0.75:
					entity.hud[8].x_scale = 0.55*(entity.stats['health']/entity.Startstats['health'])
					entity.hud[8].texture = Texture('Images/In-Game Ui/HealthBar(1).PNG')
				elif entity.stats['health']/entity.Startstats['health'] > 0.5:
					entity.hud[8].x_scale = 0.55*(entity.stats['health']/entity.Startstats['health'])
					entity.hud[8].texture = Texture('Images/In-Game Ui/HealthBar(2).PNG')
				elif entity.stats['health']/entity.Startstats['health'] > 0.25:
					entity.hud[8].x_scale = 0.55*(entity.stats['health']/entity.Startstats['health'])
					entity.hud[8].texture = Texture('Images/In-Game Ui/HealthBar(3).PNG')
				elif entity.stats['health']/entity.Startstats['health'] > 0:
					entity.hud[8].x_scale = 0.55*(entity.stats['health']/entity.Startstats['health'])
					entity.hud[8].texture = Texture('Images/In-Game Ui/HealthBar(4).PNG')
				elif entity.stats['health']/entity.Startstats['health'] <= 0:
					entity.hud[8].x_scale = 0
					
				entity.hud[2].text = 'PDV: '+str(entity.stats['health'])+'/'+str(entity.Startstats['health'])
				entity.hud[3].text = "PE: "+str(entity.stats['EP'])
				entity.hud[4].text = 'PM: '+str(entity.stats['MP'])
				if entity.stats['orientation'] == 'left':
					entity.hud[6].text = 'Gauche'
				elif entity.stats['orientation'] == 'right':
					entity.hud[6].text = 'Droite'
				elif entity.stats['orientation'] == 'top':
					entity.hud[6].text = 'Haut'
				elif entity.stats['orientation'] == 'bottom':
					entity.hud[6].text = 'Bas'
				if entity.controller.isPlaying:
					entity.hud[5].text = 'État: Joue'
				elif entity.isPlacing:
					entity.hud[5].text = 'État: Se Place'
				elif not 'Mort' in entity.hud[5].text:
					entity.hud[5].text = 'État: Attend'
			
			if not entity.controller:
				entity.stateCheck(self)
				if entity.stats['health'] <= 0:
					entity.IMG.remove_from_parent()
					self.entityList.remove(entity)
					self.mainList.remove(entity)
					del entity
			else:	
				entity.move(self)
			
		for ligne in self.map:
			for cell in ligne:
				cell.draw(self)
		
		for value in self.valueList:
			if time.time() - self.time >= 0.025 and value[2] > 0:
				if value[1] != 1:
					value[0].font = ('DIN Condensed', value[0].font[1]+1)
				x = 1
				if value[1] == 'right':
					value[0].position = (value[0].position[0]+2, value[0].position[1])
					value[2] -= 0.1
				elif value[1] == 'left':
					value[0].position = (value[0].position[0]-2, value[0].position[1])
					value[2] -= 0.1
				elif value[1] == 'top':
					value[0].position = (value[0].position[0], value[0].position[1]+2)
					value[2] -= 0.1
				elif value[1] == 'bottom':
					value[0].position = (value[0].position[0], value[0].position[1]-2)
					value[2] -= 0.1
				elif value[1] == None:
					value[0].position = (value[0].position[0], value[0].position[1])
					value[0].alpha -= 0.025
					value[2] -= 0.05
				elif value[1] == 1:
					value[0].position = (value[0].position[0], value[0].position[1]-0.5)
					value[0].alpha -= 0.020
					value[2] -= 0.025
			elif value[2] <= 0:
				value[0].remove_from_parent()
				if len(value) == 4:
					value[3].remove_from_parent()
				del value
		
		if self.entity_to_show and not self.isShowingEffects:
			if time.time()-0.5 >= self.time2:
				self.entity_to_show = None
		
		if x == 1:
			self.time = time.time()
		
		if ct.localMulti or ct.onlineMulti:
			self.playControl()
		
	
	def changeTime(self):
		if self.day_counter <= 4:
			self.day_counter += 1
		else:
			self.day_counter = 0
		
		if self.day_counter == 0:
			self.day_indicator.texture = Texture('Images/In-Game Ui/Day-0.PNG')
		if self.day_counter == 1:
			self.day_indicator.texture = Texture('Images/In-Game Ui/Day-1.PNG')
		if self.day_counter == 2:
			self.day_indicator.texture = Texture('Images/In-Game Ui/Day-2.PNG')
		if self.day_counter == 3:
			self.day_indicator.texture = Texture('Images/In-Game Ui/Night-0.PNG')
		if self.day_counter == 4:
			self.day_indicator.texture = Texture('Images/In-Game Ui/Night-1.PNG')
		if self.day_counter == 5:
			self.day_indicator.texture = Texture('Images/In-Game Ui/Night-2.PNG')
		
		for effect in self.day_effects:
			if effect[2] == self.day_counter:
				if effect[0] == 'Crusade':
					for entity in self.entityList:
						if effect[1].team == entity.team:
							crusade = {'name': 'Crusade',
									  'type': 'damage_%',
									  'situation': 'attacking',
									  'value': 0.30,
									  'duration_type': 'until_turns',
									  'duration': 2,
									  'source': entity}
							entity.effects.append(crusade)
				elif effect[0] == 'Divine Fury':
					for entity in self.entityList:
						divineFury = {'name': 'DivineFury',
								  'type': 'HPboost',
								  'situation': 'turnBegin',
								  'value': -3,
								  'duration_type': 'until_turns',
								  'duration': 2,
								  'source': entity}
						entity.effects.append(divineFury)
		
	def playControl(self):
		x = self.playerList.index(self.active_player)
		if self.play_button_touched == True:
			if self.game_phase == 'Placement' and self.active_player.entity.coordX:
				if ct.onlineMulti and self.active_player.id == ct.CLIENT_ID:
					action = {'type': 'turnEnd',
										'name': None,
										'coords': None}
					ct.CLIENT.dataList_to_send.append(action)
				self.play_button_touched = False
				self.active_player.entity.isPlacing = False
				if x+1 < len(self.playerList):
					self.turn_indicator[0].position = (self.turn_indicator[0].position[0]+90,
														self.turn_indicator[0].position[1])
					self.active_player = self.playerList[x+1]
					self.active_player.entity.isPlacing = True
					turn_info = [LabelNode(text='Placement de '+str(self.active_player.name), font=('DIN Condensed', 70), color='#ffffff'),
					None, 2]
					turn_info[0].z_position = 4.0
					turn_info[0].position = (self.size[0]/2, 
										 self.size[1]/2)
					self.valueList.append(turn_info)
					self.add_child(turn_info[0])
					if ct.onlineMulti:
						while len(ct.CLIENT.dataList_to_send) or ct.CLIENT.last_msg:
							None
						if self.active_player.id == ct.CLIENT_ID:
							ct.CLIENT.state = 'Sending Up'
							ct.CLIENT.sleep(0.5)
						elif self.active_player.id != ct.CLIENT_ID:
							ct.CLIENT.state = 'Receiving Up'
						print(ct.CLIENT.state, ct.CLIENT_ID, self.active_player.id)
						
				else:
					self.game_phase = 'Fight'
					self.turn_indicator[0].position = (self.turn_indicator[1],
														self.turn_indicator[0].position[1])
					for entity in self.entityList:
						entity.passiveCheck()
					self.day_indicator = SpriteNode('Images/In-Game Ui/Day-0.PNG', z_position=10,
													position=(50, 50))
					self.add_child(self.day_indicator)
					self.active_player = self.playerList[0]
					self.active_player.isPlaying = True
					self.drawAbilities(self.active_player.entity)
					self.active_player.entity.passiveCheck()
					self.active_player.entity.effectsCheck(['turnBegin'], self)
					for cell in self.groundCells:
						if cell.cellType == 'BlueCell' or cell.cellType == 'RedCell':
							cell.initialCellType = 'freeCell'
							cell.cellType = 'freeCell'
					turn_info = [LabelNode(text='Tour de '+str(self.active_player.name), font=('DIN Condensed', 70), color='#ffffff'),
					None, 2]
					turn_info[0].z_position = 4.0
					turn_info[0].position = (self.size[0]/2, 
											 self.size[1]/2)
					turn_arrow = [SpriteNode('Images/In-Game Ui/TurnArrow.PNG'), 1, 2]
					turn_arrow[0].z_position = 4.0
					turn_arrow[0].anchor_point = (0,0)
					turn_arrow[0].position = (self.active_player.entity.IMG.position[0]+5, 
											 self.active_player.entity.IMG.position[1]+5)
					
					self.valueList.append(turn_arrow)
					self.valueList.append(turn_info)
					self.add_child(turn_info[0])
					self.add_child(turn_arrow[0])
					if ct.onlineMulti:
						while len(ct.CLIENT.dataList_to_send) or ct.CLIENT.last_msg:
							None
						if self.active_player.id == ct.CLIENT_ID:
							ct.CLIENT.state = 'Sending Up'
							ct.CLIENT.sleep(0.5)
						elif self.active_player.id != ct.CLIENT_ID:
							ct.CLIENT.state = 'Receiving Up'
						print(ct.CLIENT.state)
							
			elif self.game_phase == 'Fight' and not self.active_player.isMoving and not self.active_player.selectedAbility:
				if ct.onlineMulti and self.active_player.id == ct.CLIENT_ID:
					action = {'type': 'turnEnd',
										'name': None,
										'coords': None}
					ct.CLIENT.dataList_to_send.append(action)
				self.play_button_touched = False
				self.active_player.isPlaying = False
				self.active_player.entity.lastMove = None
				self.active_player.entity.passiveCheck()
				self.active_player.entity.effectsCheck(['turnEnd'], self)
				self.active_player.entity.effectsClean()
				self.active_player.entity.played_turns.append(self.active_player.entity.played_abilities)
				self.active_player.entity.played_abilities = []
				if x+1 < len(self.playerList):
					self.active_player = self.playerList[x+1]
					self.turn_indicator[0].position = (self.turn_indicator[0].position[0]+90,
														self.turn_indicator[0].position[1])
				else:
					self.turn_indicator[0].position = (self.turn_indicator[1],
														self.turn_indicator[0].position[1])
					self.active_player = self.playerList[0]
					self.changeTime()
				x = self.playerList.index(self.active_player)
				for button in self.buttons:
					button[0].remove_from_parent()
					button[1].remove_from_parent()
					if len(button) >= 6:
						button[5].remove_from_parent()
					del button
				for info in self.informations:
					info.remove_from_parent()
					del info
				action = {'type': 'deads',
							'name': None,
							'coords': None}
				print(self.active_player.entity.deathCount)
				a = False
				while self.active_player.entity.stats['health'] <= 0:
					if self.active_player.entity.deathCount > 0:
						b = [self.active_player.id, self.active_player.name]
						self.active_player.entity.hud[5].text = str('État: Mort('+
								str(self.active_player.entity.deathCount)+')')
						self.active_player.entity.deathCount -= 1
						print('a')
						print(self.active_player)
						if x+1 < len(self.playerList):
							self.active_player = self.playerList[x+1]
							print(self.active_player)
							self.turn_indicator[0].position = (self.turn_indicator[0].position[0]+90,
															self.turn_indicator[0].position[1])
							print('b', len(self.playerList), x)
						else: 
							self.active_player = self.playerList[0]
							self.turn_indicator[0].position = (self.turn_indicator[1],
															self.turn_indicator[0].position[1])
							print('c')
						print(self.active_player)
					
					elif self.active_player.entity.deathCount <= 0:
						for hud in self.active_player.entity.hud:
							hud.remove_from_parent()
						self.active_player.entity.IMG.remove_from_parent()
						self.playerList.remove(self.active_player)
						for entity in self.entityList:
							if not entity == self.active_player.entity:
								if self.entityList.index(entity) < \
								self.entityList.index(self.active_player.entity):
									for hud in entity.hud:
										if not hud == entity.hud[0] and \
										not hud == entity.hud[6]:
											hud.position = (hud.position[0]+45, hud.position[1])
											if not a:
												self.turn_indicator[1] += 45
												a = True
								elif self.entityList.index(entity) > \
								self.entityList.index(self.active_player.entity):
									for hud in entity.hud:
										if not hud == entity.hud[0] and \
										not hud == entity.hud[6]:
											hud.position = (hud.position[0]-45, hud.position[1])
						self.entityList.remove(self.active_player.entity)
						del self.active_player.entity
						del self.active_player
						self.turn_indicator[0].position = (self.turn_indicator[0].position[0]+45,
														self.turn_indicator[0].position[1])
						
						if x+1 < len(self.playerList):
							self.active_player = self.playerList[x+1]
							self.turn_indicator[0].position = (self.turn_indicator[0].position[0]+90,
															self.turn_indicator[0].position[1])
						else: 
							self.active_player = self.playerList[0]
							self.turn_indicator[0].position = (self.turn_indicator[1],
															self.turn_indicator[0].position[1])
					#a['name'] = b
						
				self.active_player.isPlaying = True
				self.drawAbilities(self.active_player.entity)
				self.active_player.entity.oldCoordX = self.active_player.entity.coordX
				self.active_player.entity.oldCoordY = self.active_player.entity.coordY
				self.active_player.entity.stats['MP'] = int(self.active_player.entity.Startstats['MP'])
				self.active_player.entity.stats['EP'] = int(self.active_player.entity.Startstats['EP'])
				self.active_player.entity.passiveCheck()
				self.active_player.entity.effectsCheck(['turnBegin'], self)
				turn_info = [LabelNode(text='Tour de '+str(self.active_player.name), font=('DIN Condensed', 70), color='#ffffff'), None, 2]
				turn_info[0].z_position = 4.0
				turn_info[0].position = (self.size[0]/2, 
										 self.size[1]/2)
				turn_arrow = [SpriteNode('Images/In-Game Ui/TurnArrow.PNG'), 1, 2]
				turn_arrow[0].z_position = 4.0
				turn_arrow[0].anchor_point = (0,0)
				turn_arrow[0].position = (self.active_player.entity.IMG.position[0]+5, 
										 self.active_player.entity.IMG.position[1]+5)
				
				self.valueList.append(turn_arrow)
				self.valueList.append(turn_info)
				self.add_child(turn_info[0])
				self.add_child(turn_arrow[0])
				if ct.onlineMulti:
					while len(ct.CLIENT.dataList_to_send) or ct.CLIENT.last_msg:
						None
					if self.active_player.id == ct.CLIENT_ID:
						ct.CLIENT.state = 'Sending Up'
						ct.CLIENT.sleep(0.5)
					elif self.active_player.id != ct.CLIENT_ID:
						ct.CLIENT.state = 'Receiving Up'
					print(ct.CLIENT.state)
						
	def cellScan(self, coordX, coordY):
			for ligne in self.map:
				for cell in ligne:
					if cell.coordX == coordX and cell.coordY == coordY:
						return(cell)
			return(None)
	
	def entityScan(self, coordX, coordY):
		for entity in self.entityList:
				if entity.coordX == coordX and entity.coordY == coordY:
					return(entity)
		return(None)
	
	def setupGame(self):
		players = []
		for player in ct.PLAYERS:
			if player['class'] == 'Viking':
				entity = cl.Viking(player)
				self.add_child(entity.IMG)
				self.entityList.append(entity)
				self.mainList.append(entity)
			elif player['class'] == 'ThermalMage':
				entity = cl.ThermalMage(player)
				self.add_child(entity.IMG)
				self.entityList.append(entity)
				self.mainList.append(entity)
			elif player['class'] == 'Marshal':
				entity = cl.Marshal(player)
				self.add_child(entity.IMG)
				self.entityList.append(entity)
				self.mainList.append(entity)
			elif player['class'] == 'Paladin':
				entity = cl.Paladin(player)
				self.add_child(entity.IMG)
				self.entityList.append(entity)
				self.mainList.append(entity)
				
			if ct.singlePlayer:
				entity.isPlacing = True
				player = cl.Controller(self, player['team'], entity, player['name'], player['id'])
				self.drawAbilities(entity)
				self.active_player = player
				self.playerList.append(player)
			if ct.localMulti or ct.onlineMulti:
				player = cl.Controller(self, player['team'], entity, player['name'], player['id'])
				players.append(player)
		self.game_phase = 'Placement'
		
		if ct.localMulti:
			self.play_order(players)
			self.active_player = self.playerList[0]
			self.playerList[0].entity.isPlacing = True
			
		elif ct.onlineMulti:
			self.playerList = players
			self.active_player = self.playerList[0]
			self.playerList[0].entity.isPlacing = True
		
		a = []
		for player in self.playerList:
			a.append(player.entity)
			
		self.create_HUD(a)
		self.play_button = SpriteNode('IMG_0994.PNG', position=(self.size.w-100, 40), scale=0.4)
		self.play_text = LabelNode('Fin du Tour', position=(self.size.w-100, 40))
		self.play_button_touched = False
		self.screen_touched = False
		self.add_child(self.play_button)
		self.add_child(self.play_text)
		self.play_button.z_position = 4
		self.play_text.z_position = 4.1
		
	def play_order(self, players):
		if gi.bluePlayers > gi.redPlayers:
			x = 1
		elif gi.bluePlayers < gi.redPlayers:
			x = 2
		else:
			x = random.randint(1,2)
		
		while len(self.playerList) < len(players):
			for player in players:
				if (player.team == 'blue' and x == 1) or \
					(player.team == 'red' and x == 2):
					if not player in self.playerList:
						self.playerList.append(player)
						if x == 1 and gi.redPlayers > 0:
							gi.bluePlayers -= 1
							x = 2
						elif x == 2 and gi.bluePlayers > 0:
							gi.redPlayers -= 1
							x = 1
						break
	
	def drawAbilities(self, entity):
		self.buttons = []
		self.informations = []
		filePath = ''
		AbilityIMG = None
		actualType = None
		x = self.size[0]/2-90*2.5
		if entity.name == 'Viking':
			filePath = 'Images/Viking/'
		elif entity.name == 'Marshal':
			filePath = 'Images/Marshal/'
		elif entity.name == 'Thermal Mage':
			filePath = 'Images/Thermal Mage/'
			actualType = entity.actualType
		for ability in entity.abilities:
			if ability == entity.Ability1:
				button = [SpriteNode(texture='Images/In-Game Ui/Ability(Grey).PNG'), LabelNode('1', font=('Copperplate', 30)), False, entity.Ability1,  'ability_1']
				if filePath != '' and not actualType:
					AbilityIMG = SpriteNode(texture=str(filePath+'Ability1.PNG'))
				elif actualType:
					AbilityIMG = SpriteNode(texture=str(filePath+'Ability1['+actualType+'].PNG'))
			
			if ability == entity.Ability2:
				button = [SpriteNode(texture='Images/In-Game Ui/Ability(Grey).PNG'), LabelNode('2', font=('Copperplate', 30)), False, entity.Ability2, 'ability_2']
				if filePath != '' and not actualType:
					AbilityIMG = SpriteNode(texture=str(filePath+'Ability2.PNG'))
				elif actualType:
					AbilityIMG = SpriteNode(texture=str(filePath+'Ability2['+actualType+'].PNG'))
			
			if ability == entity.Ability3:
				button = [SpriteNode(texture='Images/In-Game Ui/Ability(Grey).PNG'), LabelNode('3', font=('Copperplate', 30)), False, entity.Ability3, 'ability_3']
				if filePath != '' and not actualType:
					AbilityIMG = SpriteNode(texture=str(filePath+'Ability3.PNG'))
				elif actualType:
					AbilityIMG = SpriteNode(texture=str(filePath+'Ability3['+actualType+'].PNG'))
			
			if ability == entity.Ability4:
				button = [SpriteNode(texture='Images/In-Game Ui/Ability(Grey).PNG'), LabelNode('4', font=('Copperplate', 30)), False, entity.Ability4, 'ability_4']
				if filePath != '':
					AbilityIMG = SpriteNode(texture=str(filePath+'Ability4.PNG'))
			
			if ability == entity.Ability5:
				button = [SpriteNode(texture='Images/In-Game Ui/Ability(Grey).PNG'), LabelNode('5', font=('Copperplate', 30)), False, entity.Ability5, 'ability_5']
				if filePath != '' and not actualType:
					AbilityIMG = SpriteNode(texture=str(filePath+'Ability5.PNG'))
				elif actualType:
					AbilityIMG = SpriteNode(texture=str(filePath+'Ability5['+actualType+'].PNG'))
			
			if ability == entity.Ability6:
				button = [SpriteNode(texture='Images/In-Game Ui/Ability(Grey).PNG'), LabelNode('6', font=('Copperplate', 30)), False, entity.Ability6, 'ability_6']
				if filePath != '' and not actualType:
					AbilityIMG = SpriteNode(texture=str(filePath+'Ability6.PNG'))
				elif actualType:
					AbilityIMG = SpriteNode(texture=str(filePath+'Ability6['+actualType+'].PNG'))
			
			if ability == entity.Ability7:
				button = [SpriteNode(texture='Images/In-Game Ui/Ability(Grey).PNG'), LabelNode('7', font=('Copperplate', 30)), False, entity.Ability7, 'ability_7']
				if filePath != '' and not actualType:
					AbilityIMG = SpriteNode(texture=str(filePath+'Ability7.PNG'))
				elif actualType:
					AbilityIMG = SpriteNode(texture=str(filePath+'Ability7['+actualType+'].PNG'))
			
			if ability == entity.Ability8:
				button = [SpriteNode(texture='Images/In-Game Ui/Ability(Grey).PNG'), LabelNode('8', font=('Copperplate', 30)), False, entity.Ability8, 'ability_8']
				if filePath != '' and not actualType:
					AbilityIMG = SpriteNode(texture=str(filePath+'Ability8.PNG'))
				elif actualType:
					AbilityIMG = SpriteNode(texture=str(filePath+'Ability8['+actualType+'].PNG'))
			
			if ability == entity.Ability9:
				button = [SpriteNode(texture='Images/In-Game Ui/Ability(Grey).PNG'), LabelNode('9', font=('Copperplate', 30)), False, entity.Ability9, 'ability_9']
				if filePath != '':
					AbilityIMG = SpriteNode(texture=str(filePath+'Ability9.PNG'))
					
			if ability == entity.Ability10:
				button = [SpriteNode(texture='Images/In-Game Ui/Ability(Grey).PNG'), LabelNode('10', font=('Copperplate', 30)), False, entity.Ability10, 'ability_10']
				if filePath != '':
					AbilityIMG = SpriteNode(texture=str(filePath+'Ability10.PNG'))
			
			if not ct.onlineMulti or self.active_player.id == ct.CLIENT_ID:
				self.add_child(button[0])
				self.add_child(button[1])
			button[0].scale = 0.8
			button[0].position = (x, 45)
			button[0].z_position = self.z_value
			self.z_value += 1
			if AbilityIMG:
				button.append(AbilityIMG)
				if not ct.onlineMulti or self.active_player.id == ct.CLIENT_ID:
					self.add_child(AbilityIMG)
				AbilityIMG.scale = 0.65
				AbilityIMG.position = (x, 45)
				AbilityIMG.z_position = self.z_value
				self.z_value += 1
				button[1].alpha = 0
			else:
				button[1].z_position = self.z_value
				button[1].position = (x-15, 25)
				button[1].color = 'black'
			x += 90
			self.buttons.append(button)
		
		a = []	
		for passive in entity.passives:
			if passive == entity.Passive1:
				a.append('1')
			elif passive == entity.Passive2:
				a.append('2')
			elif passive == entity.Passive3:
				a.append('3')
			elif passive == entity.Passive4:
				a.append('4')
			elif passive == entity.Passive5:
				a.append('5')
			elif passive == entity.Passive6:
				a.append('6')
		
		if entity.controller.team == 'blue':
			passivesDraw = SpriteNode('Images/In-Game Ui/PassivesBlue.png')
		elif entity.controller.team == 'red':
			passivesDraw = SpriteNode('Images/In-Game Ui/PassivesRed.png')
			
		passivesDraw.x_scale = 0.8
		passivesDraw.y_scale = 0.8
		passivesDraw.z_position = self.z_value
		passivesDraw.position = (x, 45)
		self.informations.append(passivesDraw)
		if not ct.onlineMulti or self.active_player.id == ct.CLIENT_ID:
			self.add_child(passivesDraw)
		
		for number in a:
			if len(self.informations) == 1:
				number = LabelNode(text=number, font=('Copperplate', 20), position=(x-19, 34))
				number.z_position = self.z_value+1
				self.informations.append(number)
				if not ct.onlineMulti or self.active_player.id == ct.CLIENT_ID:
					self.add_child(number)
			elif len(self.informations) == 2:
				number = LabelNode(text=number, font=('Copperplate', 20), position=(x+1, 55))
				number.z_position = self.z_value+1
				self.informations.append(number)
				if not ct.onlineMulti or self.active_player.id == ct.CLIENT_ID:
					self.add_child(number)
			elif len(self.informations) == 3:
				number = LabelNode(text=number, font=('Copperplate', 22), position=(x+20, 34))
				number.z_position = self.z_value+1
				self.informations.append(number)
				if not ct.onlineMulti or self.active_player.id == ct.CLIENT_ID:
					self.add_child(number)
	
	def drawDetails(self, button):
		abilityname = button[4]
		if self.active_player.entity.name == 'Viking':
			CL_ABILITIES = ct.VK_ABILITIES
		elif self.active_player.entity.name == 'Thermal Mage':
			CL_ABILITIES = ct.TM_ABILITIES
			z = ['ability_4', 'ability_9', 'ability_10']
			if abilityname not in z:
				if self.active_player.entity.actualType == 'ice':
					abilityname += '[ice]'
				elif self.active_player.entity.actualType == 'fire':
					abilityname += '[fire]'
		elif self.active_player.entity.name == 'Marshal':
			CL_ABILITIES = ct.MR_ABILITIES
			
		background = SpriteNode('IMG_0994.PNG')
		background.x_scale = 1.2
		background.y_scale = 1.2
		background.position = (button[0].position[0], button[0].position[1]+105)
		background.z_position = 10
		self.details.append(background)
		range_text = ('Portée: '+str(CL_ABILITIES[abilityname]['minRange'])
							+'-'+str(CL_ABILITIES[abilityname]['maxRange']))
		range_label = LabelNode(range_text, font=('Helvetica', 19))
		range_label.position = (background.position[0]+190, background.position[1]+46)
		range_label.z_position = 11
		self.details.append(range_label)
		
		name_label = LabelNode(CL_ABILITIES[abilityname]['name'], font=('Hoefler Text', 24))
		name_label.position = (background.position[0], background.position[1]+44)
		name_label.color = '#ffffff'
		name_label.z_position = 11
		self.details.append(name_label)
		
		if self.active_player.entity.name == 'Viking':
			all_details = json.loads(json.dumps(CL_ABILITIES[abilityname]['details']))
			if abilityname == 'ability_9':
				if self.active_player.entity.Passive4 in self.active_player.entity.passives:
					all_details = ['Augmente la défense de la cible de 15% pendant 3', 
									'tours. Cet actif ne peut être utilisé si deux cibles',
									'bénéficient déjà de son effet.']
				else:
					all_details = [all_details[0], all_details[1], all_details[2]]
			y = (len(all_details)-1)/2
					
		elif self.active_player.entity.name == 'Thermal Mage':
			all_details = json.loads(json.dumps(CL_ABILITIES[abilityname]['details']))
			if abilityname == 'ability_1[ice]':
				if self.active_player.entity.Passive4 in self.active_player.entity.passives:
					all_details = ["Inflige 6 dégâts à distance et applique l'effet 'gelé'.",
									"Faire cette attaque sur un geyser de lave crée des ",
									"tapis de braises dans une grande zone autour du",
									"geyser. Celui-ci est supprimé."]
				else:
					all_details = [all_details[0]]
					
			elif abilityname == 'ability_5[ice]':
				if self.active_player.entity.Passive4 in self.active_player.entity.passives:
					all_details = ["Invoque un Bloc de Glace de 10PDV (3 max). Sur un ",
									"Geyser de Lave: des Tapis de Braises sont créés",
									"autour du Bloc(supprimé) dans une grande zone. Les",
									"entitées dans la zone sont repoussées(1)/-4pdv."]
				else:
					all_details = [all_details[0], all_details[1]]
					
			elif abilityname == 'ability_6[fire]':
				if self.active_player.entity.Passive4 in self.active_player.entity.passives:
					all_details = ["Inflige 10 dégâts à distance et repousse d'une case ",
									"depuis le centre. Si un Bloc de glace est au centre",
									"de la zone: inflige 13 dégâts, et repousse de 2",
									"cases. Le Bloc est supprimé."]
				else:
					all_details = ["Inflige 10 dégâts à distance et repousse d'une case ",
									"depuis le centre."]
			y = (len(all_details)-1)/2
		
		elif self.active_player.entity.name == 'Marshal':
			all_details = json.loads(json.dumps(CL_ABILITIES[abilityname]['details']))
			if self.active_player.entity.Passive3 in self.active_player.entity.passives:
				if abilityname == 'ability_1':
					all_details = ['inflige 6 dégâts au corps à corps. Utilisable 2/tour.']
				elif abilityname == 'ability_2':
					all_details = ['inflige 8 dégâts à distance. Cette attaque peut être',
									'faite depuis la portée des alliés du Maréchal.']
				elif abilityname == 'ability_8':
					all_details = ["inflige 2xA+1 dégâts et repousse de A cases. A = nombre",
									"d'alliés du Maréchal+1. Utilisable 1/tour. La portée",
									"maximale de cette attaque augmente de A cases."]					
			y = (len(all_details)-1)/2
			
		for text in all_details:
			label = LabelNode(text, font=('Helvetica', 15))
			label.anchor_point = (0,0)
			label.z_position = 11
			label.position = (background.position[0]-180, background.position[1]+(y*16)-8)
			self.details.append(label)
			y-=1
		
		cost_text = 'Coût: '
		if CL_ABILITIES[abilityname]['EPcost'] and \
		CL_ABILITIES[abilityname]['MPcost']:
			cost_text += str(CL_ABILITIES[abilityname]['EPcost'])+'PE-'
			cost_text += str(CL_ABILITIES[abilityname]['MPcost'])+'PM'
		elif CL_ABILITIES[abilityname]['EPcost']:
			cost_text += str(CL_ABILITIES[abilityname]['EPcost'])+'PE'
		elif CL_ABILITIES[abilityname]['MPcost']:
			cost_text += str(CL_ABILITIES[abilityname]['MPcost'])+'MP'
		
		cost_label = LabelNode(cost_text, font=('Helvetica', 19))
		cost_label.anchor_point = (0,0)
		cost_label.position = (background.position[0]-235, background.position[1]-56)
		cost_label.z_position = 11
		self.details.append(cost_label)
		
		for thing in self.details:
			self.add_child(thing)
										
	def create_HUD(self, entities):
		self.stats_background = SpriteNode('Images/In-Game Ui/StatsBackground.PNG', 
											position=(512, 733),
											z_position=3.90,
											y_scale=0.85)
		self.add_child(self.stats_background)
		x = self.size[0]/2 - len(entities)*45
		y = self.size[1] - 19
		for entity in entities:
			head = LabelNode(text=str(entity.controller.name), font=('Arial Rounded MT Bold', 14), position=(-100, -100))
			if entity.controller.team == 'red':
				head.color = 'red'
			elif entity.controller.team == 'blue':
				head.color = 'blue'
			head.z_position = 3.0
			entity.hud.append(head)
			self.add_child(head)
			
			name = LabelNode(text=str(entity.controller.name), font=('Arial Rounded MT Bold', 12), position=(x, y), anchor_point=(0,0))
			name.color = entity.controller.team
			name.z_position = 4.0
			entity.hud.append(name)
			self.add_child(name)
			y -= 12
			
			healthPts = LabelNode(text='PDV: '+str(entity.stats['health'])+'/'+str(entity.Startstats['health']), font=('Arial Rounded MT Bold', 12), position=(x, y), anchor_point=(0,0))
			healthPts.z_position = 4.0
			entity.hud.append(healthPts)
			self.add_child(healthPts)
			y -= 12
			
			energyPts = LabelNode(text="PE: "+str(entity.stats['EP']), font=('Arial Rounded MT Bold', 12), position=(x, y), anchor_point=(0,0))
			energyPts.z_position = 4.0
			entity.hud.append(energyPts)
			self.add_child(energyPts)
			y -= 12
			
			movePts = LabelNode(text='PM: '+str(entity.stats['MP']), font=('Arial Rounded MT Bold', 12), position=(x, y), anchor_point=(0,0))
			movePts.z_position = 4.0
			entity.hud.append(movePts)
			self.add_child(movePts)
			y -= 12
			
			state = LabelNode(text='État: ', font=('Arial Rounded MT Bold', 11.9), position=(x, y), anchor_point=(0,0))
			state.z_position = 4.0
			entity.hud.append(state)
			self.add_child(state)		
			if entities.index(entity) == 0:
				self.turn_indicator = [SpriteNode('Images/In-Game Ui/TurnIndicator.PNG',
												z_position=3.91,
												position=(x+40, 733),
												scale=0.85), x+40]
				self.add_child(self.turn_indicator[0])
			
			y = self.size[1] - 19
			x += 90
			
			orientation = LabelNode(text=str(entity.stats['orientation']), font=('Arial Rounded MT Bold', 9), position=(-100, -100), anchor_point=(0,0))
			orientation.z_position = 3.0
			entity.hud.append(orientation)
			self.add_child(orientation)
			
			healthBar_1 = SpriteNode('Images/In-Game Ui/HealthBar.PNG', position=(-100, -100), scale=0.55)
			healthBar_1.z_position = 3.0
			entity.hud.append(healthBar_1)
			self.add_child(healthBar_1)
			
			healthBar_2 = SpriteNode('Images/In-Game Ui/HealthBar(1).PNG', position=(-100, -100), scale=0.55)
			healthBar_2.anchor_point = (0,0)
			healthBar_2.z_position = 3.0
			entity.hud.append(healthBar_2)
			self.add_child(healthBar_2)
			
			
	def showEffects(self, entity):
		if entity:
			if entity.name:
				effectWindow = SpriteNode('IMG_0994.PNG')
				effectWindow.x_scale = 1.5
				effectWindow.y_scale = 2
				effectWindow.position = (self.size[0]/2, self.size[1]/2)
				effectWindow.z_position = 10
				self.add_child(effectWindow)
				x = effectWindow.position[0]-225
				y = effectWindow.position[1]+effectWindow.size[1]/2-10
				
				name_label = LabelNode(text=entity.controller.name+'('+entity.name+')', font=('Hoefler Text', 21))
				name_label.position = (effectWindow.position[0],effectWindow.position[1]+85)
				name_label.z_position = 11
				self.add_child(name_label)
				for effect in entity.effects:
					if not self.shownEffects:
						shownEffect = self.createEffectText(effect, 1)
						shownEffect[1].position = (x, y)
						y -= effectWindow.size[1]*2/10
						print(effectWindow.size[1])
						self.add_child(shownEffect[1])
						shownEffect[1].z_position = 11
						self.shownEffects.append(shownEffect)
						
					elif self.shownEffects:
						z = 0
						for shownEffect2 in self.shownEffects:
							if shownEffect2[2]['name'] == effect['name'] and \
							shownEffect2[2]['source'] == effect['source']:
								shownEffect2[1].text = self.createEffectText(effect, shownEffect2[0]+1)[1].text
								shownEffect2[0] += 1
								z = 1
						
						if not z:
							shownEffect = self.createEffectText(effect, 1)
							shownEffect[1].position = (x, y)
							y -= effectWindow.size[1]*2/10
							self.add_child(shownEffect[1])
							shownEffect[1].z_position = 11
							self.shownEffects.append(shownEffect)
				
				self.shownEffects.append(name_label)
				self.shownEffects.append(effectWindow)
				self.isShowingEffects = True
				self.selectedCell = None
				self.lastCell = None
			
	def createEffectText(self, effect, value):
		shownEffect = [value]
		text = str(effect['name']) + ' x' + str(shownEffect[0]) + ' : '
		
		if effect['value'] > 0 and not \
		(effect['situation'] == 'defending' or effect['situation'] == 'defending_front'):
			text += '+'
			if effect['type'] == 'damage_%':
				text += str(effect['value']*100)
			else:
				text += str(effect['value'])
		
		elif effect['value'] > 0 and \
		(effect['situation'] == 'defending' or effect['situation'] == 'defending_front'):
			text += '-'
			if effect['type'] == 'damage_%':
				text += str(effect['value']*100*value)
			else:
				text += str(effect['value']*value)
		
		elif effect['value'] < 0 and \
		(effect['situation'] == 'defending' or effect['situation'] == 'defending_front'):
			text += '+'
			if effect['type'] == 'damage_%':
				text += str(abs(effect['value'])*100*value)
			else:
				text += str(abs(effect['value']*value))
		
		else:
			if effect['type'] == 'damage_%':
				text += str(effect['value']*100*value)
			else:
				text += str(effect['value']*value)
		
		if effect['type'] == 'damage_%':
			text += '% de dégâts'
		elif effect['type'] == 'MPboost':
			text += ' PM'
		elif effect['type'] == 'EPboost':
			text += ' PE'
		elif effect['type'] == 'HPboost':
			text += ' PDV'
		
		if effect['situation'] == 'gameBegin':
			text += ' | en début de partie | '
		elif effect['situation'] == 'turnBegin':
			text += ' | en début de tour | '
		elif effect['situation'] == 'turnEnd':
			text += ' | en début de tour | '
		elif effect['situation'] == 'attacking':
			text += ' | en attaquant | '
		elif effect['situation'] == 'defending':
			text += ' | en défendant | '
		elif effect['situation'] == 'defending_front':
			text += ' | en défendant de front | '
		
		if effect['duration_type'] == 'next_attack':
			if effect['duration'] == 1:
				text += 'pour la prochaine attaque'
			elif effect['duration'] > 1:
				text += 'pour les prochaines ' + str(effect['duration']) + ' attaques'
		elif effect['duration_type'] == 'until_turns':
			if effect['duration'] == 1:
				text += "jusqu'au prochain tour"
			elif effect['duration'] > 1:
				text += "jusqu'aux "+ str(effect['duration']) + ' prochains tours' 
		elif effect['duration_type'] == 'infinitely':
			text += 'pour toujours'
		
		text = LabelNode(text, font=('Avenir Next Condensed', 17.5))
		text.anchor_point = (0,0)
		'''while not 450-50 <= text.size[0] <= 450:
			if text.size[0] < 450:
				text.font = (text.font[0], text.font[1]+1)
				if text.font[1] >= 40:
					break
			elif text.size[1] < 450:
				text.font = (text.font[0], text.font[1]-1)'''
		shownEffect.append(text)
		shownEffect.append(effect)
		return(shownEffect)
		
	def rangeCalculator(self, entity, minRange, maxRange, SoV, isLine):
		targetedCells = []
		for cell in self.groundCells:
			distance = abs(cell.coordX-entity.coordX) + abs(cell.coordY-entity.coordY)
			if isLine:
				if minRange <= distance <= maxRange:
					if cell.coordX == entity.coordX or \
					cell.coordY == entity.coordY:
						if SoV and self.lineOfViewScan(entity, cell):
							targetedCells.append(cell)
						elif not SoV:
							targetedCells.append(cell)
			else:
				if minRange <= distance <= maxRange:
					if SoV and self.lineOfViewScan(entity, cell):
						targetedCells.append(cell)
					elif not SoV:
						targetedCells.append(cell)
		return(targetedCells)
			
	def lineOfViewScan(self, entity, cell):
		sight_obstacles = []
		for cell3 in self.groundCells:
			for effect in cell3.effects:
				if effect['type'] == 'hideSoV' and \
				not cell3 in sight_obstacles:
					sight_obstacles.append(cell3)
					
		entityCell = self.cellScan(entity.coordX, entity.coordY)
		entityMidle = [entityCell.IMG.position[0]+30,
						entityCell.IMG.position[1]-20]
		cellMidle = [cell.IMG.position[0]+30,
					 cell.IMG.position[1]-20]
		distance = abs(cell.coordX-entity.coordX) + abs(cell.coordY-entity.coordY)
		pointX = entityMidle[0]
		pointY = entityMidle[1]
		for x in range(1, distance):
			pointX += (cellMidle[0]-entityMidle[0])/distance
			pointY += (cellMidle[1]-entityMidle[1])/distance
			for obstacle in self.obstacles:
				if obstacle.IMG.position[0] < pointX < obstacle.IMG.position[0]+ct.CELL_X:
					if obstacle.IMG.position[1]-(ct.CELL_Y+20) < pointY < obstacle.IMG.position[1]-20:
						return(False)
			for cell2 in sight_obstacles:
				if cell2.IMG.position[0] < pointX < cell2.IMG.position[0]+ct.CELL_X:
					if cell2.IMG.position[1]-ct.CELL_Y < pointY < cell2.IMG.position[1]:
						return(False)
		return(True)
	
	def hideCells(self, cells):
		if cells != None and (not ct.onlineMulti or self.active_player.id == ct.CLIENT_ID):
			for cell in self.groundCells:
				if not cell in cells:
					if cell.cellType == 'freeCell' or cell.cellType == 'SelectedCell':
						cell.cellType = 'hidenCell'
						cell.initialCellType = 'hidenCell'
					elif cell.cellType == 'hidenCell':
						cell.cellType = 'freeCell'
						cell.initialCellType = 'freeCell'
				elif cell in cells:
					if cell.cellType == 'freeCell':
						cell.cellType = 'TargetedCell'
						cell.initialCellType = 'TargetedCell'
					elif cell.cellType == 'TargetedCell' or cell.cellType == 'SelectedCell':
						cell.cellType = 'freeCell'
						cell.initialCellType = 'freeCell'
	
	def valueCalculator(self, attacker, defender, atkValue, isAOE, changeAxis, abilityname, isHeal=False):
		if not isHeal:					
			pathFactor = self.pathMultiplicator(attacker, defender)
			
			Attacker_situation = ('attacking', pathFactor[2])
			Defender_situation = ('defending', pathFactor[2])
			
			attackerFactor = attacker.effectsCheck(Attacker_situation, self)
			defenderFactor = defender.effectsCheck(Defender_situation, self)
			finalFactor = attackerFactor - defenderFactor
			
			self.majorCheck(attacker, defender, ability=abilityname)				
			if changeAxis and pathFactor[1] != 'from_side':
				print('axis changed to ', pathFactor[1])
				attacker.stats['orientation'] = pathFactor[1]
			
			if not isAOE:
				finalValue = round(atkValue * (pathFactor[0] + finalFactor))
			else:
				finalValue = round(atkValue * (finalFactor+1))
				
			print(pathFactor, attackerFactor, defenderFactor)
			print(defender.effects)
			
		else:
			pathFactor = self.pathMultiplicator(attacker, defender)
			
			Attacker_situation = ('healing', pathFactor[2])
			Defender_situation = ('healed', pathFactor[2])
			
			attackerFactor = attacker.effectsCheck(Attacker_situation, self)
			defenderFactor = defender.effectsCheck(Defender_situation, self)
			if attacker != defender:
				finalFactor = attackerFactor + (defenderFactor-1)
			else:
				finalFactor = attackerFactor
			finalValue = round(atkValue*finalFactor)
			
		self.valueDraw(defender, finalValue, pathFactor[1])
		return(round(finalValue))

	def pathMultiplicator(self, attacker, defender):
		distanceX = attacker.coordX - defender.coordX
		distanceY = attacker.coordY - defender.coordY
		
		if abs(distanceX) == abs(distanceY):
			if distanceX > 0:
				if distanceY > 0:
					return(1.25, 'left', 'side')
				elif distanceY < 0:
					return(1.25, 'bottom', 'side')
			elif distanceX < 0:
				if distanceY > 0:
					return(1.25, 'top', 'side')
				elif distanceY < 0:
					return(1.25, 'right', 'side')
			elif distanceX == 0:
				return(1.25, attacker.stats['orientation'], 'side')
			
		elif defender.stats['orientation'] == 'right':
			if distanceX > abs(distanceY):
				return(1, 'left', 'front')
			elif distanceX < abs(distanceY) < abs(distanceX):
				return(1.5, 'right', 'back')
			elif distanceY > abs(distanceX):
				return(1.25, 'top', 'side')
			elif distanceY < abs(distanceX):
				return(1.25, 'bottom', 'side')
				
		elif defender.stats['orientation'] == 'left':
			if distanceX > abs(distanceY):
				return(1.5, 'left', 'back')
			elif distanceX < abs(distanceY) < abs(distanceX):
				return(1, 'right', 'front')
			elif distanceY > abs(distanceX):
				return(1.25, 'top', 'side')
			elif distanceY < abs(distanceX):
				return(1.25, 'bottom', 'side')
			
		elif defender.stats['orientation'] == 'top':
			if distanceX > abs(distanceY):
				return(1.25, 'left', 'side')
			elif distanceX < abs(distanceY) < abs(distanceX):
				return(1.25, 'right', 'side')
			elif distanceY > abs(distanceX):
				return(1.5, 'top', 'back')
			elif distanceY < abs(distanceX):
				return(1, 'bottom', 'front')
			
		elif defender.stats['orientation'] == 'bottom':
			if distanceX > abs(distanceY):
				return(1.25, 'left', 'side')
			elif distanceX < abs(distanceY) < abs(distanceX):
				return(1.25, 'right', 'side')
			elif distanceY > abs(distanceX):
				return(1, 'top', 'front')
			elif distanceY < abs(distanceX):
				return(1.5, 'bottom', 'back')
		
		elif defender.stats['orientation'] == None:
			if distanceX > abs(distanceY):
				return(1, 'left', 'front')
			elif distanceX < abs(distanceY) < abs(distanceX):
				return(1, 'right', 'front')
			elif distanceY > abs(distanceX):
				return(1, 'top', 'front')
			elif distanceY < abs(distanceX):
				return(1, 'bottom', 'front')
			
	def valueDraw(self, defender, value, direction):
		damage = [LabelNode(text=str(value), font=('DIN Condensed', 20), color='#ff0000', 
				  position=(defender.IMG.position[0] + 40, defender.IMG.position[1] - 40),
				  z_position=10.0), direction, abs(value)/10+0.5]
		if value > 0:
			damage[0].text = '+'+damage[0].text
			damage[0].color = '#00e714'
		self.add_child(damage[0])
		self.valueList.append(damage)
		
	def collisionCalculator(self, entity, value, source, isCell):
		directionX, directionY, x = 0, 0, 0
		if isCell:
			axis = self.pathMultiplicator(source, entity)[1]
		else:
			axis = source.stats['orientation']
			
		if axis == 'right':
			directionX += value
		elif axis == 'left':
			directionX -= value
		elif axis == 'top':
			directionY -= value
		elif axis == 'bottom':
			directionY += value

		if directionX < 0 or directionY < 0:
			direction = -1
		elif directionX > 0 or directionY > 0:
			direction = 1
			
		if directionX:
			while abs(x) < abs(directionX):
				if self.cellScan(entity.coordX+direction, entity.coordY) in self.groundCells \
				and not self.entityScan(entity.coordX+direction, entity.coordY):
					if direction == 1:
						entity.moveSteps.append('right')
						entity.coordX += 1
						entity.passiveCheck()
						entity.effectsCheck(['isPushed'], self)
						entity.effectsClean()
						if entity.controller:
							print(entity.controller.name + 'pushed right')
						
					elif direction == -1:
						entity.moveSteps.append('left')
						entity.coordX -= 1
						entity.passiveCheck()
						entity.effectsCheck(['isPushed'], self)
						entity.effectsClean()
						if entity.controller:
							print(entity.controller.name + 'pushed left')
						
				elif not self.cellScan(entity.coordX+direction, entity.coordY) \
				in self.groundCells and entity != source:
					entity.stats['health'] += -2
					if direction < 0:
						self.valueDraw(entity, -2, 'right')
					elif direction > 0:
						self.valueDraw(entity, -2, 'left')
					
				elif self.entityScan(entity.coordX+direction, entity.coordY) \
				and entity != source:
					entity2 = self.entityScan(entity.coordX+direction, entity.coordY)
					entity.stats['health'] += -2
					entity2.stats['health'] += -2
					if direction < 0:
						self.valueDraw(entity, -2, 'right')
						self.valueDraw(entity2, -2, 'left')
					elif direction > 0:
						self.valueDraw(entity, -2, 'left')
						self.valueDraw(entity2, -2, 'right')
				x += direction
		
		elif directionY:
			while abs(x) < abs(directionY):
				if self.cellScan(entity.coordX, entity.coordY+direction) in self.groundCells \
				and not self.entityScan(entity.coordX, entity.coordY+direction):
					if direction == 1:
						entity.moveSteps.append('bottom')
						entity.coordY += 1
						entity.passiveCheck()
						entity.effectsCheck(['isPushed'], self)
						entity.effectsClean()
						if entity.controller:
							print(entity.controller.name + 'pushed bottom')
						
					elif direction == -1:
						entity.moveSteps.append('top')
						entity.coordY -= 1
						entity.passiveCheck()
						entity.effectsCheck(['isPushed'], self)
						entity.effectsClean()
						if entity.controller:
							print(entity.controller.name + 'pushed top')
						
				elif not self.cellScan(entity.coordX, entity.coordY+direction) \
				in self.groundCells and entity != source:
					entity.stats['health'] += -2
					if direction < 0:
						self.valueDraw(entity, -2, 'bottom')
					elif direction > 0:
						self.valueDraw(entity, -2, 'top')
					
				elif self.entityScan(entity.coordX, entity.coordY+direction) \
				and entity != source:
					entity2 = self.entityScan(entity.coordX, entity.coordY+direction)
					entity.stats['health'] += -2
					entity2.stats['health'] += -2
					if direction < 0:
						self.valueDraw(entity, -2, 'bottom')
						self.valueDraw(entity2, -2, 'top')
					elif direction > 0:
						self.valueDraw(entity, -2, 'top')
						self.valueDraw(entity2, -2, 'bottom')
				x += direction
	
	def AreaCalculator(self, areaType, source, selectedcell, zoneCells):
		if areaType == 'smallArea':
			for cell in self.groundCells:
				if cell.coordX == selectedcell.coordX and \
				(cell.coordY-1 == selectedcell.coordY or \
				cell.coordY+1 == selectedcell.coordY):
					if not cell in zoneCells:
						zoneCells.append(cell)
				elif cell.coordY == selectedcell.coordY and \
				(cell.coordX-1 == selectedcell.coordX or \
				cell.coordX+1 == selectedcell.coordX):
					if not cell in zoneCells:
						zoneCells.append(cell)
				elif cell in zoneCells:
					zoneCells.remove(cell)
		
		elif areaType == 'mediumArea':
			for cell in self.groundCells:
				if cell.coordX == selectedcell.coordX and \
				(cell.coordY-1 == selectedcell.coordY or \
				cell.coordY+1 == selectedcell.coordY):
					if not cell in zoneCells:
						zoneCells.append(cell)
				elif cell.coordY == selectedcell.coordY and \
				(cell.coordX-1 == selectedcell.coordX or \
				cell.coordX+1 == selectedcell.coordX):
					if not cell in zoneCells:
						zoneCells.append(cell)
				elif (cell.coordX+1 == selectedcell.coordX or \
				cell.coordX-1 == selectedcell.coordX) and \
				(cell.coordY+1 == selectedcell.coordY or \
				cell.coordY-1 == selectedcell.coordY):
					if not cell in zoneCells:
						zoneCells.append(cell)
				elif cell in zoneCells:
					zoneCells.remove(cell)		
				
		elif areaType == 'bigArea':
			for cell in self.groundCells:
				distanceX = abs(selectedcell.coordX-cell.coordX)
				distanceY = abs(selectedcell.coordY-cell.coordY)
				if distanceX+distanceY <= 2:
					if not cell in zoneCells:
						zoneCells.append(cell)
				elif cell in zoneCells:
					zoneCells.remove(cell)
					
		elif areaType == 'smallCone':
			distanceX = selectedcell.coordX - source.coordX
			distanceY = selectedcell.coordY - source.coordY
			if distanceY == 0:
				if distanceX < 0:
					for cell in self.groundCells:
						if cell.coordX-selectedcell.coordX == -1 and \
						selectedcell.coordY-1 <= cell.coordY <= selectedcell.coordY+1:
							if not cell in zoneCells:
								zoneCells.append(cell)
						elif cell in zoneCells:
							zoneCells.remove(cell)
							
				elif distanceX > 0:
					for cell in self.groundCells:
						if cell.coordX-selectedcell.coordX == 1 and \
						selectedcell.coordY-1 <= cell.coordY <= selectedcell.coordY+1:
							if not cell in zoneCells:
								zoneCells.append(cell)
						elif cell in zoneCells:
							zoneCells.remove(cell)
			
			if distanceX == 0:
				if distanceY < 0:
					for cell in self.groundCells:
						if cell.coordY-selectedcell.coordY == -1 and \
						selectedcell.coordX-1 <= cell.coordX <= selectedcell.coordX+1:
							if not cell in zoneCells:
								zoneCells.append(cell)
						elif cell in zoneCells:
							zoneCells.remove(cell)
							
				elif distanceY > 0:
					for cell in self.groundCells:
						if cell.coordY-selectedcell.coordY == 1 and \
						selectedcell.coordX-1 <= cell.coordX <= selectedcell.coordX+1:
							if not cell in zoneCells:
								zoneCells.append(cell)
						elif cell in zoneCells:
							zoneCells.remove(cell)
							
		elif areaType == 'bigCone':
			distanceX = selectedcell.coordX - source.coordX
			distanceY = selectedcell.coordY - source.coordY
			if distanceY == 0:
				if distanceX < 0:
					for cell in self.groundCells:
						if (cell.coordX-selectedcell.coordX == -1 and \
						selectedcell.coordY-1 <= cell.coordY <= selectedcell.coordY+1) or \
						(cell.coordX-selectedcell.coordX == -2 and \
						selectedcell.coordY-2 <= cell.coordY <= selectedcell.coordY+2):
							if not cell in zoneCells:
								zoneCells.append(cell)
						elif cell in zoneCells:
							zoneCells.remove(cell)
							
				elif distanceX > 0:
					for cell in self.groundCells:
						if (cell.coordX-selectedcell.coordX == 1 and \
						selectedcell.coordY-1 <= cell.coordY <= selectedcell.coordY+1) or \
						(cell.coordX-selectedcell.coordX == 2 and \
						selectedcell.coordY-2 <= cell.coordY <= selectedcell.coordY+2):
							if not cell in zoneCells:
								zoneCells.append(cell)
						elif cell in zoneCells:
							zoneCells.remove(cell)
			
			if distanceX == 0:
				if distanceY < 0:
					for cell in self.groundCells:
						if (cell.coordY-selectedcell.coordY == -1 and \
						selectedcell.coordX-1 <= cell.coordX <= selectedcell.coordX+1) or \
						(cell.coordY-selectedcell.coordY == -2 and \
						selectedcell.coordX-2 <= cell.coordX <= selectedcell.coordX+2):
							if not cell in zoneCells:
								zoneCells.append(cell)
						elif cell in zoneCells:
							zoneCells.remove(cell)
							
				elif distanceY > 0:
					for cell in self.groundCells:
						if (cell.coordY-selectedcell.coordY == 2 and \
						selectedcell.coordX-1 <= cell.coordX <= selectedcell.coordX+1) or \
						(cell.coordY-selectedcell.coordY == 2 and \
						selectedcell.coordX-2 <= cell.coordX <= selectedcell.coordX+2):
							if not cell in zoneCells:
								zoneCells.append(cell)
						elif cell in zoneCells:
							zoneCells.remove(cell)
							
		elif areaType == 'smallLine':
			distanceX = selectedcell.coordX - source.coordX
			distanceY = selectedcell.coordY - source.coordY
			if distanceY == 0:
				if distanceX < 0:
					for cell in self.groundCells:
						if cell.coordX-selectedcell.coordX == -1 and \
						cell.coordY == selectedcell.coordY:
							if not cell in zoneCells:
								zoneCells.append(cell)
						elif cell in zoneCells:
							zoneCells.remove(cell)
				elif distanceX > 0:
					for cell in self.groundCells:
						if cell.coordX-selectedcell.coordX == 1 and \
						cell.coordY == selectedcell.coordY:
							if not cell in zoneCells:
								zoneCells.append(cell)
						elif cell in zoneCells:
							zoneCells.remove(cell)
							
			if distanceX == 0:
				if distanceY < 0:
					for cell in self.groundCells:
						if cell.coordY-selectedcell.coordY == -1 and \
						cell.coordX == selectedcell.coordX:
							if not cell in zoneCells:
								zoneCells.append(cell)
						elif cell in zoneCells:
							zoneCells.remove(cell)
				elif distanceY > 0:
					for cell in self.groundCells:
						if cell.coordY-selectedcell.coordY == 1 and \
						cell.coordX == selectedcell.coordX:
							if not cell in zoneCells:
								zoneCells.append(cell)
						elif cell in zoneCells:
							zoneCells.remove(cell)
		
		elif areaType == 'perpLine':
			distanceX = selectedcell.coordX - source.coordX
			distanceY = selectedcell.coordY - source.coordY
			if distanceY == 0:
				for cell in self.groundCells:
					if cell.coordX == selectedcell.coordX and \
					selectedcell.coordY-1 <= cell.coordY <= selectedcell.coordY+1:
						if not cell in zoneCells:
							zoneCells.append(cell)
					elif cell in zoneCells:
						zoneCells.remove(cell)
							
			if distanceX == 0:
				for cell in self.groundCells:
					if cell.coordY == selectedcell.coordY and \
					selectedcell.coordX-1 <= cell.coordX <= selectedcell.coordX+1:
						if not cell in zoneCells:
							zoneCells.append(cell)
					elif cell in zoneCells:
						zoneCells.remove(cell)
			
		return(zoneCells)
	
	def addStatEffect(self, source, target, effectName):
		effect = None
		badEffects = ['ice', 'fire', 'impious']
		negated = False
		if effectName == 'ice':
			if source.Passive3 in source.passives:
				effect = {'name': 'iced',
							  'type': 'damage_%',
							  'situation': 'attacking',
							  'value': -0.05,
							  'duration_type': 'until_turns',
							  'duration': 2,
							  'source': source}
			else:
				effect = {'name': 'iced',
							  'type': 'damage_%',
							  'situation': 'attacking',
							  'value': 0,
							  'duration_type': 'until_turns',
							  'duration': 2,
							  'source': source}
		elif effectName == 'fire':
			if source.Passive3 in source.passives:
				effect = {'name': 'fired',
								'type': 'damage_%',
								'situation': 'defending',
								'value': -0.05,
								'duration_type': 'until_turns',
								'duration': 2,
								'source': source}
			else:
				effect = {'name': 'fired',
								'type': 'damage_%',
								'situation': 'defending',
								'value': 0,
								'duration_type': 'until_turns',
								'duration': 2,
								'source': source}
		elif effectName == 'cryonics':
			effect = {'name': 'Cryonics',
					'type': 'EPboost',
					'situation': 'turnBegin',
					'value': ct.TM_ABILITIES['ability_9']['value'],
					'duration_type': 'until_turns',
					'duration': 3,
					'source': source}
		elif effectName == 'impious':
			effect = {'name': 'impious',
					 'type': 'heal_%',
					 'situation': 'healing&healed',
					 'value': -0.03,
					 'duration_type': 'until_turns',
					 'duration': 2,
					 'source': source}
		elif effectName == 'blessed':
			effect = {'name': 'blessed',
					 'type': None,
					 'situation': None,
					 'value': 1,
					 'duration_type': 'until_turns',
					 'duration': 1,
					 'source': source}
		
		for effect2 in target.effects:
			if effect2['name'] == 'blessed':
				negated = True
		
		if not (negated and effectName in badEffects):
			target.effects.append(effect)
	
	def addGroundEffect(self, source, target, effectName):
		effect = None
		ignoringEffects = ['ShieldProtection', 'Entranchment', 'SmokeWall',
							'Sanctuary', 'Hole', 'DivineBarrier']
		blockingEffects1 = ['LavaGusher', 'EmberMat']
		blockingEffects2 = ['SnowCover']
		negated = False
		targetCell = self.cellScan(target.coordX, target.coordY)
		
		if effectName == 'Sanctuary':
			effect = {'name': 'Sanctuary',
						'type': 'healing&healed',
						'situation': 'Stay',
						'value[1]': ct.PL_ABILITIES['ability_3']['value[1]'],
						'value[2]': ct.PL_ABILITIES['ability_3']['value[2]'],
						'duration_type': 'until_turns',
						'duration': 2,
						'source': source,
						'image': None}
		elif effectName == 'ShieldProtection':
			effect = {'name': 'ShieldProtection',
						'type': None,
						'situation': 'Stay',
						'value': ct.PL_ABILITIES['ability_2']['value'],
						'duration_type': 'until_turns',
						'duration': 1,
						'source': source,
						'image': None}			
		elif effectName == 'Entranchment':
			effect = {'name': 'Entranchment',
					'type': None,
					'situation': 'Stay',
					'value(1)': ct.MR_ABILITIES['ability_6']['value(1)'],
					'value(2)': ct.MR_ABILITIES['ability_6']['value(2)'],
					'duration_type': 'until_turns',
					'duration': 2,
					'source': source,
					'image': None}
		elif effectName == 'SmokeWall':
			SmokeWall = {'name': 'SmokeWall',
						  'type': 'hideSoV',
						  'situation': None,
						  'value': None,
						  'duration_type': 'until_turns',
						  'duration': 2,
						  'source': self,
						  'image': None}
		elif effectName == 'Hole':
			effect = {'name': 'Hole',
					'type': None,
					'situation': None,
					'value': None,
					'duration_type': 'until_turns',
					'duration': ct.MR_ABILITIES['ability_5']['value'],
					'source': source,
					'image': None}
		elif effectName == 'DivineBarrier':
			effect = {'name': 'DivineBarrier',
					'type': None,
					'situation': None,
					'value': None,
					'duration_type': 'until_turns',
					'duration': ct.PL_ABILITIES['ability_7']['value'],
					'source': source,
					'image': None}
		elif effectName == 'LavaGusher':
			effect = {'name': 'LavaGusher',
						'type': 'HPboost',
						'situation': 'Walk&Stay',
						'value': ct.TM_ABILITIES['ability_5[fire]']['value'],
						'duration_type': 'until_turns',
						'duration': 3,
						'source': source,
						'image': None}
		elif effectName == 'EmberMat':
			effect = {'name': 'EmberMat',
					  'type': 'HPboost',
					  'situation': 'Walk&Stay',
					  'value': -2,
					  'duration_type': 'until_turns',
					  'duration': 2,
					  'source': source,
					  'image': None}
		elif effectName == 'SnowCover':
			effect = {'name': 'SnowCover',
					'type': 'MPboost',
					'situation': 'Walk',
					'value': ct.TM_ABILITIES['ability_8[ice]']['value'],
					'duration_type': 'next_walk',
					'duration': 1,
					'source': source,
					'image': None}
		
		for effect2 in targetCell.effects:
			if (effect2['name'] in blockingEffects1 and effectName in blockingEffects2) or \
			(effectName in blockingEffects1 and effect2['name'] in blockingEffects2):
				negated = True
	
		if not negated or effectName in ignoringEffects:
			targetCell.effects.append(effect)
	
	def majorCheck(self, active_entity, target=None, situation=None, ability=None):
		cost = 0
		if ability:
			if active_entity.name == 'Viking':
				cost = ct.VK_ABILITIES[ability]['EPcost']
			elif active_entity.name == 'Thermal Mage':
				cost = ct.TM_ABILITIES[ability]['EPcost']
			elif active_entity.name == 'Marshal':
				cost = ct.MR_ABILITIES[ability]['EPcost']
			elif active_entity.name == 'Paladin':
				cost = ct.PL_ABILITIES[ability]['EPcost']
		if active_entity:
			if target:
				for effect2 in self.day_effects:
					if effect2[0] == 'Moment Of Peace' and effect[2] == self.day_counter:
						effect2[1].ImpiousGen(active_entity, cost*10)
				for effect in target.effects:
					if effect['name'] == 'blessed':
						effect['source'].ImpiousGen(active_entity, cost)
				targetCell = self.cellScan(target.coordX, target.coordY)
				for effect in targetCell.effects:
					if effect['name'] == 'Sanctuary':
						effect['source'].ImpiousGen(active_entity, 6)
				
						
			elif situation == 'turnEnd':
				a = []
				for effect in active_entity.effects:
					if effect['name'] == 'impious':
						a.append(effect)
				if not len(active_entity.played_abilities):
					for effect in a:
						effect['duration'] = 0
				else:
					for x in range(0, active_entity.stats['EP']):
						if x+1 <= len(a):
							a[x]['duration'] = 0
							
	
	def moveCam(self):
		if not self.active_player.isMoving:
			if self.touchX != self.touchX2 or \
			self.touchY != self.touchY2:
				moveX = self.touchX2 - self.touchX
				moveY = self.touchY2 - self.touchY
				if abs(moveX) < 100 and abs(moveY) < 100:
					for thing in self.mainList:
						thing.IMG.position = (thing.IMG.position[0]+moveX, thing.IMG.position[1]+moveY)
					
					for img in self.IMGList:
						img.position = (img.position[0]+moveX, img.position[1]+moveY)
					
					for value in self.valueList:
						value[0].position = (value[0].position[0]+moveX, value[0].position[1]+moveY)
							
				self.touchX = self.touchX2
				self.touchY = self.touchY2
			
		else:
			self.isMovingCam = False


def uncompose_msg(msg):
	a = []
	x = 0
	y = 0
	z = 0
	for char in msg:
		if char == ']' or char == '}':
			x = 1
		elif x and (char == '[' or char == '{'):
			if z == 0:
				a.append(msg[:y])
			else:
				a.append(msg[z:y])
			z = y
			x = 0
		else:
			x = 0
		y += 1
	a.append(msg[z:y])
	return(a)

def run_game():
	ct.STARTED = True
	run(Game(), show_fps = True, frame_interval=1, anti_alias=True, multi_touch=False)
