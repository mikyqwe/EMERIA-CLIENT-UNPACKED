import ui, localeInfo, mouseModule, exception, net, chat, app, player, item


class AuraUpgrade(ui.ScriptWindow):
	def __init__(self, isUpgradeExp = False):
		ui.ScriptWindow.__init__(self)
		self.AURA_LEVEL = 0
		self.AURA_SUB_LEVEL = 1
		self.AURA_EXP = 2
		self.pos= [-1,-1]
		self.Text=[]
		self.x_y=[0,0]
		self.interface = None
		self.tooltipItem = None
		
		self.IsUpgradeExp = isUpgradeExp
		
		self.Initialize()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
	def SetTooltip(self, tooltip):
		self.tooltipItem = tooltip
	def SetInterface(self, interface):
		self.interface = interface
	def Initialize(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/aura_up.py" )
			self.titleBar = self.GetChild("TitleBar")
			self.UpBtn = self.GetChild("UpButton")
			self.CloseButton = self.GetChild("CloseButton")
			for j in xrange(6):
				self.Text.append(self.GetChild("AuraText%d"%j))
			self.AuraSlot = self.GetChild("AuraSlot")
		except:
			exception.Abort("AuraUpgrade Initialize have problem! <>")
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.UpBtn.SetEvent(ui.__mem_func__(self.__UpButton))
		self.CloseButton.SetEvent(ui.__mem_func__(self.Close))
		self.AuraSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.__OnSelectEmptySlot))
		self.AuraSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.__OnSelectItemSlot))
		self.AuraSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.__OnSelectItemSlot))
		self.AuraSlot.SetOverInItemEvent(ui.__mem_func__(self.__OnOverInItem))
		self.AuraSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OnOverOutItem))
		for j in xrange(6):
			self.Text[j].Hide()

	def __UpButton(self):
		#if player.GetStatus(player.ELK) < 25000000: # OLD

		if not self.IsUpgradeExp:
			if player.GetMoney() < 25000000: # LONG LONG
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_EVOLUTION_GOLD)
				return

		if self.pos[0] == -1 or self.pos[1] == -1:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_ITEM_NEED_REGISTER)
			return
		exp = player.GetItemMetinSocket(player.INVENTORY, self.pos[0], 2)
		if not self.IsUpgradeExp:
			if exp != 100:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_ITEM_NEED_EXP)
				return
		else:
			if exp == 100:
				chat.AppendChat(chat.CHAT_TYPE_INFO, "Experienþa este 100%")
				return		

		if not self.IsUpgradeExp:
			net.SendChatPacket("/aura 2 %d %d"%(self.pos[0],self.pos[1]))
		else:
			net.SendChatPacket("/aura 5 %d %d"%(self.pos[0],self.pos[1]))

	def SelectRightClick(self, selectedSlotPos, index):
		attachedSlotPos = index
		itemIndex = player.GetItemIndex(attachedSlotPos)
		item.SelectItem(itemIndex)
		if attachedSlotPos >= 180:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EQUIPITEM)
			return

		if selectedSlotPos == 0:
			if (item.GetItemType() == item.ITEM_TYPE_COSTUME) and (item.GetItemSubType() == item.COSTUME_TYPE_AURA) and (itemIndex >= 49000 and itemIndex <= 49006):
				self.AuraSlot.SetItemSlot(0, player.GetItemIndex(player.INVENTORY, attachedSlotPos), player.GetItemCount(player.INVENTORY, attachedSlotPos))
				self.pos[0] = attachedSlotPos
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)
				return
		elif selectedSlotPos == 1:
			if self.pos[0] == -1:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_REGISTER_AURAITEM)
				return
			metinSlot = [player.GetItemMetinSocket(player.INVENTORY, self.pos[0], i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
			needvnum = 49990
			numbers = [[9,49991],[49,49992],[99,49993],[249,49994],[499,49995]]
			for x in xrange(len(numbers)):
				if metinSlot[self.AURA_SUB_LEVEL] == numbers[x][0]:
					needvnum = numbers[x][1]
			item.SelectItem(needvnum)
			if itemIndex == needvnum:
				self.AuraSlot.SetItemSlot(1, player.GetItemIndex(player.INVENTORY, attachedSlotPos), player.GetItemCount(player.INVENTORY, attachedSlotPos))
				self.pos[1] = attachedSlotPos
				self.SetAuroInfo()
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_TOOLTIP_RESOURCE_ITEM%item.GetItemName())

	def __OnSelectEmptySlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			itemIndex = player.GetItemIndex(attachedSlotPos)
			item.SelectItem(itemIndex)
			mouseModule.mouseController.DeattachObject()

			if attachedSlotPos >= 180:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EQUIPITEM)
				return

			if selectedSlotPos == 0:
				if (item.GetItemType() == item.ITEM_TYPE_COSTUME) and (item.GetItemSubType() == item.COSTUME_TYPE_AURA) and (itemIndex >= 49000 and itemIndex <= 49006):
					self.AuraSlot.SetItemSlot(0, player.GetItemIndex(player.INVENTORY, attachedSlotPos), player.GetItemCount(player.INVENTORY, attachedSlotPos))
					self.pos[0] = attachedSlotPos
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)
					return
			elif selectedSlotPos == 1:
				if self.pos[0] == -1:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_REGISTER_AURAITEM)
					return
				metinSlot = [player.GetItemMetinSocket(player.INVENTORY, self.pos[0], i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
				needvnum = 49990
				numbers = [[9,49991],[49,49992],[99,49993],[249,49994],[499,49995]]
				for x in xrange(len(numbers)):
					if metinSlot[self.AURA_SUB_LEVEL] == numbers[x][0]:
						needvnum = numbers[x][1]
				item.SelectItem(needvnum)
				if itemIndex == needvnum:
					self.AuraSlot.SetItemSlot(1, player.GetItemIndex(player.INVENTORY, attachedSlotPos), player.GetItemCount(player.INVENTORY, attachedSlotPos))
					self.pos[1] = attachedSlotPos
					self.SetAuroInfo()
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_TOOLTIP_RESOURCE_ITEM%item.GetItemName())
	def __OnSelectItemSlot(self, selectedSlotPos):
		if selectedSlotPos == 0:
			self.AuraSlot.ClearSlot(0)
			self.AuraSlot.ClearSlot(1)
			self.pos=[-1,-1]
		else:
			self.AuraSlot.ClearSlot(selectedSlotPos)
			self.pos=[self.pos[0],-1]
		for j in xrange(6):
			self.Text[j].Hide()
	def __OnOverInItem(self, slotIndex):
		if slotIndex == 0:
			if self.pos[0] != -1:
				self.tooltipItem.SetInventoryItem(self.pos[0])
		elif slotIndex == 1:
			if self.pos[1] != -1:
				self.tooltipItem.SetInventoryItem(self.pos[1])
	def __OnOverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
	def GetAbsorb(self, level):
		new_level = str(level)
		if len(new_level) == 1:
			return "0.%d"%level
		elif len(new_level) == 2:
			return "%d.%d"%(int(new_level[0]),int(new_level[1]))
		elif len(new_level) == 3:
			return "%d%d.%d"%(int(new_level[0]),int(new_level[1]),int(new_level[2]))
	def SetAuroInfo(self):
		metinSlot = [player.GetItemMetinSocket(player.INVENTORY, self.pos[0], i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
		self.Text[0].SetText(localeInfo.AURA_TOOLTIP_NOW)
		self.Text[1].SetText(localeInfo.AURA_LEVEL_STEP%(metinSlot[self.AURA_LEVEL],metinSlot[self.AURA_SUB_LEVEL],float(self.GetAbsorb(metinSlot[self.AURA_SUB_LEVEL]))))
		self.Text[2].SetText(localeInfo.AURA_TOOLTIP_EXP%metinSlot[self.AURA_EXP])
		self.Text[3].SetText(localeInfo.AURA_TOOLTIP_NEXT)
		self.Text[4].SetText(localeInfo.AURA_LEVEL_STEP%(metinSlot[self.AURA_LEVEL]+1,metinSlot[self.AURA_SUB_LEVEL]+1,float(self.GetAbsorb(metinSlot[self.AURA_SUB_LEVEL]+1))))
		# self.Text[5].SetText(localeInfo.AURA_TOOLTIP_EXP%metinSlot2)

		if self.IsUpgradeExp:
			aura_vnum = player.GetItemIndex(player.INVENTORY, self.pos[1])
			aura_count = player.GetItemCount(player.INVENTORY, self.pos[1])
			item.SelectItem(aura_vnum)       
			metinSlot2 = item.GetValue(2)
			value = int(aura_count) * int(metinSlot2) + int(metinSlot[self.AURA_EXP])
			if value > 100:
				self.Text[5].SetText(localeInfo.AURA_TOOLTIP_EXP%100)
			else:
				self.Text[5].SetText(localeInfo.AURA_TOOLTIP_EXP%int(value))

		for j in xrange(6):
			self.Text[j].Show()
	def OnPressEscapeKey(self):
		self.Close()
		return True
	def Show(self):
		self.ClearSlot()
		ui.ScriptWindow.Show(self)
		(self.x_y[0], self.x_y[1], z) = player.GetMainCharacterPosition()
		
	def GetGameInfo(self, arg):
		if arg == 1:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_REFINE_SUCCESS)
			self.ClearSlot()
		elif arg == 2:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_EVO_SUCCESS)
			self.AuraSlot.SetItemSlot(1, player.GetItemIndex(player.INVENTORY, self.pos[1]), player.GetItemCount(player.INVENTORY, self.pos[1]))
			self.SetAuroInfo()
		elif arg == 3:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_ABS_SUCCESS)
			self.ClearSlot()
		elif arg == 111:
			self.AuraSlot.SetItemSlot(1, player.GetItemIndex(player.INVENTORY, self.pos[1]), player.GetItemCount(player.INVENTORY, self.pos[1]))
			self.SetAuroInfo()

	def OnUpdate(self):
		(x, y, z) = player.GetMainCharacterPosition()
		if abs(x-self.x_y[0]) > 1000 or abs(y-self.x_y[1]) > 1000:
			self.Close()

	def Close(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
		self.ClearSlot()
		net.SendChatPacket("/aura 1")
		self.Hide()

	def ClearSlot(self):
		self.pos=[-1,-1]
		self.AuraSlot.ClearSlot(0)
		self.AuraSlot.ClearSlot(1)
		for j in xrange(6):
			self.Text[j].Hide()

class AuraAbsorb(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.AURA_LEVEL = 0
		self.AURA_SUB_LEVEL = 1
		self.AURA_EXP = 2
		self.tooltipItem = None
		self.interface = None
		self.pos=[-1,-1]
		self.x_y=[0,0]
		self.Initialize()
	def __del__(self):
		ui.ScriptWindow.__del__(self)
	def SetTooltip(self, tooltipItem):
		self.tooltipItem = tooltipItem
	def SetInterface(self, interface):
		self.interface = interface
	def Initialize(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/aura_abs.py" )
			self.titleBar = self.GetChild("TitleBar")
			self.UpButton = self.GetChild("UpButton")
			self.CloseButton = self.GetChild("CloseButton")
			self.AuraSlot = self.GetChild("AuraSlot")
		except:
			exception.Abort("AuraAbsorb Initialize have problem! <>")
		self.AuraSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.__OnSelectEmptySlot))
		self.AuraSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.__OnSelectItemSlot))
		self.AuraSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.__OnSelectItemSlot))
		self.AuraSlot.SetOverInItemEvent(ui.__mem_func__(self.__OnOverInItem))
		self.AuraSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OnOverOutItem))
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.UpButton.SetEvent(ui.__mem_func__(self.__UpButton))
		self.CloseButton.SetEvent(ui.__mem_func__(self.Close))

	def __UpButton(self):
		if self.pos[1] != -1 and self.pos[0] != -1:
			net.SendChatPacket("/aura 4 %d %d"%(self.pos[0],self.pos[1]))

	def SelectRightClick(self, selectedSlotPos, index):
		attachedSlotPos = index
		itemIndex = player.GetItemIndex(attachedSlotPos)
		item.SelectItem(itemIndex)
		if attachedSlotPos >= 180:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EQUIPITEM)
			return
		if selectedSlotPos == 0:
			attr = player.GetItemAttribute(player.INVENTORY, attachedSlotPos, 0)
			if attr[0] > 0 or attr[1] > 0:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_ABSORBITEM)
				return
			if ((item.GetItemType() == item.ITEM_TYPE_COSTUME) and (item.GetItemSubType() == item.COSTUME_TYPE_AURA)):
				self.AuraSlot.SetItemSlot(0, player.GetItemIndex(player.INVENTORY, attachedSlotPos), 0)
				self.pos[0] = attachedSlotPos
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)

		if selectedSlotPos == 1:
			if self.pos[0] == -1:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_REGISTER_AURAITEM)
				return
			if ((item.GetItemType() == item.ITEM_TYPE_ARMOR) and\
				(item.GetItemSubType() == item.ARMOR_HEAD \
				or item.GetItemSubType() == item.ARMOR_SHIELD\
				or item.GetItemSubType() == item.ARMOR_WRIST\
				or item.GetItemSubType() == item.ARMOR_FOOTS\
				or item.GetItemSubType() == item.ARMOR_NECK\
				or item.GetItemSubType() == item.ARMOR_TALISMAN\
				or item.GetItemSubType() == item.ARMOR_EAR)):
				self.AuraSlot.SetItemSlot(1, player.GetItemIndex(player.INVENTORY, attachedSlotPos), 0)
				self.AuraSlot.SetItemSlot(2, player.GetItemIndex(player.INVENTORY, self.pos[0]), 0)
				self.pos[1] = attachedSlotPos
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_REFINEITEM)

	def __OnSelectEmptySlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			itemIndex = player.GetItemIndex(attachedSlotPos)
			item.SelectItem(itemIndex)
			mouseModule.mouseController.DeattachObject()

			if attachedSlotPos >= 180:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EQUIPITEM)
				return

			if selectedSlotPos == 0:
				attr = player.GetItemAttribute(player.INVENTORY, attachedSlotPos, 0)
				if attr[0] > 0 or attr[1] > 0:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_GROWTHITEM)
					return

				if ((item.GetItemType() == item.ITEM_TYPE_COSTUME) and (item.GetItemSubType() == item.COSTUME_TYPE_AURA)):
					self.AuraSlot.SetItemSlot(0, player.GetItemIndex(player.INVENTORY, attachedSlotPos), 0)
					self.pos[0] = attachedSlotPos
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)

			if selectedSlotPos == 1:
				if self.pos[0] == -1:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_REGISTER_AURAITEM)
					return
				attr = player.GetItemAttribute(player.INVENTORY, attachedSlotPos, 0)
				if attr[0] == 0 or attr[1] == 0:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_GROWTHITEM)
					return

				if ((item.GetItemType() == item.ITEM_TYPE_ARMOR) and\
					(item.GetItemSubType() == item.ARMOR_HEAD \
					or item.GetItemSubType() == item.ARMOR_SHIELD\
					or item.GetItemSubType() == item.ARMOR_WRIST\
					or item.GetItemSubType() == item.ARMOR_FOOTS\
					or item.GetItemSubType() == item.ARMOR_NECK\
					or item.GetItemSubType() == item.ARMOR_TALISMAN\
					or item.GetItemSubType() == item.ARMOR_EAR)):
					self.AuraSlot.SetItemSlot(1, player.GetItemIndex(player.INVENTORY, attachedSlotPos), 0)
					self.AuraSlot.SetItemSlot(2, player.GetItemIndex(player.INVENTORY, self.pos[0]), 0)
					self.pos[1] = attachedSlotPos
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_REFINEITEM)

	def __OnSelectItemSlot(self, selectedSlotPos):
		if selectedSlotPos < 2:
			if selectedSlotPos == 0:
				self.ClearSlot()
			elif selectedSlotPos == 1:
				self.AuraSlot.ClearSlot(1)
				self.AuraSlot.ClearSlot(2)
				self.pos=[self.pos[0],-1]

	def __OnOverInItem(self, slotIndex):
		if slotIndex == 0 and self.pos[0] != -1:
			self.tooltipItem.SetInventoryItem(self.pos[0])
		elif slotIndex == 1 and self.pos[1] != -1:
			self.tooltipItem.SetInventoryItem(self.pos[1])
		if slotIndex == 2 and self.pos[1] != -1 and self.pos[0] != -1:
			self.tooltipItem.SetAuraAbsorb(self.pos[0], self.pos[1])

	def __OnOverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def GetGameInfo(self, arg):
		if arg == 1:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_REFINE_SUCCESS)
			self.ClearSlot()
		elif arg == 2:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_EVO_SUCCESS)
			self.AuraSlot.SetItemSlot(1, player.GetItemIndex(player.INVENTORY, self.pos[1]), player.GetItemCount(player.INVENTORY, self.pos[1])) # update count
		elif arg == 3:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_ABS_SUCCESS)
			self.ClearSlot()

	def Show(self):
		ui.ScriptWindow.Show(self)
		(self.x_y[0], self.x_y[1], z) = player.GetMainCharacterPosition()
		self.ClearSlot()

	def OnUpdate(self):
		(x, y, z) = player.GetMainCharacterPosition()
		if abs(x-self.x_y[0]) > 1000 or abs(y-self.x_y[1]) > 1000:
			self.Close()

	def Close(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
		self.ClearSlot()
		net.SendChatPacket("/aura 3")
		self.Hide()

	def ClearSlot(self):
		self.pos=[-1,-1]
		self.AuraSlot.ClearSlot(0)
		self.AuraSlot.ClearSlot(1)
		self.AuraSlot.ClearSlot(2)
