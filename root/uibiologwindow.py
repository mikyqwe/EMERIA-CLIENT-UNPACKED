import uiCommon, snd, chat, app, net, player, item, wndMgr, mouseModule, localeInfo, constInfo, uiToolTip, ui, grp, uiScriptLocale, pack, event, nonplayer, biolog

MAX_BONUS_ARRAY = 4

class BiologWindow(ui.ScriptWindow):

	eventToolTip = None
	eventToolTipItem = None
	eventToolTipShown = -1

	sendBonusButtons = []
	sendBonusText = []

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.eventToolTip = None
		self.eventToolTipItem = None
		self.eventToolTipShown = None	
		self.secondsCoolDown = 0

		self.resetBiolog = 0
		self.succesPercentage = 0

		self.itemName = None
		self.ItemSlotBiolog = None
		self.infoButton = None

		self.SendButton = None
		self.gaugeText = None
		self.gauge = None

		self.sendBonusButtons = []
		self.sendBonusText = []


		self.__LoadWindow()

	
	def __del__(self):
		ui.ScriptWindow.__del__(self)
	
	def __LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "uiscript/biologwindow.py")


			self.itemName = self.GetChild("CurrentBiologName")
			self.ItemSlotBiolog = self.GetChild("ItemSlotBiolog")
			self.infoButton = self.GetChild("info")	

			self.SendButton = self.GetChild("DeliverButton")
			self.gaugeText = self.GetChild("gaugeText")
			self.gauge = self.GetChild("CoolTime")			

			self.GetChild("ItemSlotPercent").SetOverInItemEvent(ui.__mem_func__(self.OverInPercent))
			self.GetChild("ItemSlotPercent").SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.GetChild("ItemSlotReset").SetOverInItemEvent(ui.__mem_func__(self.OverInReset))
			self.GetChild("ItemSlotReset").SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))


			self.GetChild("ToggleReset").SetToggleDownEvent(lambda arg=1: self.SetToggleResetDown(arg))
			self.GetChild("ToggleReset").SetToggleUpEvent(lambda arg=0: self.SetToggleResetUp(arg))		

			self.GetChild("ToggleChance").SetToggleDownEvent(lambda arg=1: self.SetTogglePercentage(arg))
			self.GetChild("ToggleChance").SetToggleUpEvent(lambda arg=0: self.SetTogglePercentage(arg))

			self.GetChild("ItemSlotReset").SetItemSlot(0, 72350, 0)
			self.GetChild("ItemSlotPercent").SetItemSlot(0, 72349, 0)

			self.GetChild("CloseButton").SetEvent(ui.__mem_func__(self.Hide))
			self.GetChild("ShopButton").SetEvent(ui.__mem_func__(self.OpenShop))

			self.sendBonusButtons = []
			self.sendBonusText = []
			for x in xrange(MAX_BONUS_ARRAY):
				self.sendBonusButtons.append(self.GetChild("selectBonus{}".format(x)))	
				self.sendBonusText.append(self.GetChild("selectText{}".format(x)))

			for items in xrange(len(self.sendBonusButtons)):
				self.sendBonusButtons[items].SetEvent(lambda arg = items: self.SendDeliverArg(arg))
				

			self.ItemSlotBiolog.SetOverInItemEvent(ui.__mem_func__(self.OverInBiolog))
			self.ItemSlotBiolog.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.SendButton.SetEvent(ui.__mem_func__(self.SendDeliver))					


			self.eventToolTip = uiToolTip.ToolTip(45)
			self.eventToolTipItem = uiToolTip.ItemToolTip(45)

		except:
			import exception
			exception.Abort("ItemCombionation.__LoadWindow.BindObject")

		self.SetCenterPosition()

	def ClearWindow(self):
		self.itemName.SetText("-")
		self.ItemSlotBiolog.ClearSlot(0)
		self.gauge.SetPercentage(1, 1)

		for x in xrange(len(self.sendBonusText)):
			self.sendBonusText[x].SetText("-")

	def Open(self):
		if self.eventToolTip:
			self.eventToolTip.ClearToolTip()
			self.eventToolTip.HideToolTip()
			
		if self.eventToolTipItem:
			self.eventToolTipItem.ClearToolTip()
			self.eventToolTipItem.HideToolTip()
		self.SetCenterPosition()
		self.Show()


	def OverInBiolog(self, slotIndex):
		if self.eventToolTipItem:		
			self.eventToolTipItem.ClearToolTip()
			itemIndex = self.ItemSlotBiolog.GetItemIndex(slotIndex)
			if itemIndex:
				self.eventToolTipItem.AddItemData(itemIndex, [0, 0, 0, 0])
				self.eventToolTipItem.ShowToolTip()			


	def OverInReset(self, slotIndex):
		if self.eventToolTipItem:		
			self.eventToolTipItem.ClearToolTip()
			itemIndex = self.GetChild("ItemSlotReset").GetItemIndex(slotIndex)
			if itemIndex:
				self.eventToolTipItem.AddItemData(itemIndex, [0, 0, 0, 0])
				self.eventToolTipItem.ShowToolTip()						

	def OverInPercent(self, slotIndex):
		if self.eventToolTipItem:		
			self.eventToolTipItem.ClearToolTip()
			itemIndex = self.GetChild("ItemSlotPercent").GetItemIndex(slotIndex)
			if itemIndex:
				self.eventToolTipItem.AddItemData(itemIndex, [0, 0, 0, 0])
				self.eventToolTipItem.ShowToolTip()	


	def OpenShop(self):
		net.SendChatPacket("/remote 1")

	def OverInGrid(self, slotIndex):		
		if self.eventToolTipItem:		
			self.eventToolTipItem.ClearToolTip()
			itemIndex = self.shopGrid.GetItemIndex(slotIndex)
			if itemIndex:
				self.eventToolTipItem.AddItemData(itemIndex, [0, 0, 0, 0])
				self.eventToolTipItem.ShowToolTip()	

	def OverOutItem(self):
		if self.eventToolTipItem:		
			self.eventToolTipItem.ClearToolTip()	
			self.eventToolTipItem.HideToolTip()	

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def AppendSingleText(self, stringChat):
		if self.eventToolTip:
			self.eventToolTip.ClearToolTip()

		self.eventToolTip.AutoAppendTextLine(stringChat, grp.GenerateColor(0.9490, 0.9058, 0.7568, 1.0))	
		self.eventToolTip.ResizeToolTip()
		self.eventToolTip.ShowToolTip()

	def GetAffectString(self, affectType, affectValue):
		return uiToolTip.ItemToolTip.AFFECT_DICT[affectType](affectValue)

	def ShowToolTip(self):
		if self.eventToolTip:
			self.eventToolTip.ClearToolTip()
			
			(biologLevel, requestItem, actualCount, requestItemCount, secondsCoolDown, isBonusSelectable) = biolog.GetBiologData()
			(realCooldown, rewardItem, rewardCount) = biolog.GetBiologDataExtra()
			if biologLevel == 99:
				self.AppendSingleText("Biolog Terminat")
				return

			if player.GetStatus(player.LEVEL) < 35:
				self.AppendSingleText("Ai nevoie de nivel 35!")
				return


			if isBonusSelectable:
				self.eventToolTip.AutoAppendTextLine("La final, ai de selectat bonusurile:", grp.GenerateColor(0.9490, 0.9058, 0.7568, 1.0))
			else:
				self.eventToolTip.AutoAppendTextLine("La final, o sa primesti bonusurile:", grp.GenerateColor(0.9490, 0.9058, 0.7568, 1.0))

			(bonusType0, bonusValue0, bonusType1, bonusValue1, bonusType2, bonusValue2) = biolog.GetBiologDataBonus()

			bonusValue = [ bonusValue0, bonusValue1, bonusValue2 ]
			bonusType = [ bonusType0, bonusType1, bonusType2 ]

			for x in xrange(len(bonusValue)):
				if bonusValue[x]:
					self.eventToolTip.AutoAppendTextLine(self.GetAffectString(bonusType[x], bonusValue[x]), ui.GenerateColor(232, 80, 16))
			
			self.eventToolTip.AppendSpace(5)

			self.eventToolTip.AutoAppendTextLine("Premiu Final Stagiu", grp.GenerateColor(0.286, 0.796, 1, 1.0))
			self.eventToolTip.AppendItem(rewardItem, rewardCount)

			self.eventToolTip.ResizeToolTip()
			self.eventToolTip.ShowToolTip()

	def ShowToolTipCheck(self):
		if self.eventToolTip:
			self.eventToolTip.ClearToolTip()

			self.eventToolTip.AutoAppendTextLine("Resetare timp automata!")	

			self.eventToolTip.ResizeToolTip()
			self.eventToolTip.ShowToolTip()

	def HideToolTip(self):
		if self.eventToolTip:
			self.eventToolTip.ClearToolTip()
			self.eventToolTip.HideToolTip()

	def SendDeliver(self):
		biolog.SendBiolog(biolog.DELIVER, -1, self.resetBiolog, self.succesPercentage)

	def SendDeliverArg(self, arg):
		biolog.SendBiolog(biolog.DELIVER, arg, self.resetBiolog, self.succesPercentage)

	def SetToggleResetDown(self, state):
		realCooldown = self.secondsCoolDown - app.GetGlobalTimeStamp()
		if realCooldown > 0:
			chat.AppendChat(3, "Nu ai cum sa faci asta! Intai reseteaza timpul manual, iar apoi bifeaza casuta.")
			self.GetChild("ToggleReset").SetUp()
			return
		
		self.resetBiolog = state

	def SetToggleResetUp(self, state):
		self.resetBiolog = state

	def SetTogglePercentage(self, state):
		self.succesPercentage = state

	def OnUpdate(self):
		if self.infoButton.IsIn():
			self.ShowToolTip()
		else:
			self.HideToolTip()
		(biologLevel, requestItem, actualCount, requestItemCount, secondsCoolDown, isBonusSelectable) = biolog.GetBiologData()
		(realCooldown, rewardItem, rewardCount) = biolog.GetBiologDataExtra()
		self.ClearWindow()

		if biologLevel == 99:
			self.ClearWindow()
			return

		if player.GetStatus(player.LEVEL) < 35:
			self.ClearWindow()
			return

		if biologLevel > 0:	
			item.SelectItem(int(requestItem))
			self.ItemSlotBiolog.SetItemSlot(0, requestItem, 0)
			self.itemName.SetText("{} ({} / {})".format(item.GetItemName(), actualCount, requestItemCount))

			self.secondsCoolDown = secondsCoolDown

			realCooldown = self.secondsCoolDown - app.GetGlobalTimeStamp()

			if realCooldown <= 0:
				self.gaugeText.SetText("Poti livra!")
				self.gauge.SetPercentage(0, 1)
			else:
				self.gaugeText.SetText("Timp Ramas : %s" % localeInfo.SecondToDHMS(self.secondsCoolDown - app.GetGlobalTimeStamp()))
				self.gauge.SetPercentage(self.secondsCoolDown - app.GetGlobalTimeStamp(), realCooldown)

			if isBonusSelectable:
				self.GetChild("SelectThing").SetText("Selecteaza bonus la final")
			else:
				self.GetChild("SelectThing").SetText("O sa primesti bonusurile")			

			(bonusType0, bonusValue0, bonusType1, bonusValue1, bonusType2, bonusValue2) = biolog.GetBiologDataBonus()
			if bonusValue0 > 0:
				self.sendBonusText[0].SetText("{}".format(self.GetAffectString(bonusType0, bonusValue0), ui.GenerateColor(232, 80, 16)))

			if bonusValue1 > 0:
				self.sendBonusText[1].SetText("{}".format(self.GetAffectString(bonusType1, bonusValue1), ui.GenerateColor(232, 80, 16)))

			if bonusValue2 > 0:
				self.sendBonusText[2].SetText("{}".format(self.GetAffectString(bonusType2, bonusValue2), ui.GenerateColor(232, 80, 16)))
			

	def OnPressEscapeKey(self):
		if self.eventToolTip:
			self.eventToolTip.ClearToolTip()
			self.eventToolTip.HideToolTip()
			
		if self.eventToolTipItem:
			self.eventToolTipItem.ClearToolTip()
			self.eventToolTipItem.HideToolTip()		
		self.Hide()
		return True

