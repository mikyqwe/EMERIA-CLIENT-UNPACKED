import ui
import player
import mouseModule
import net as m2netm2g
import app
import snd
import item
import chat as chatm2g
import uiCommon
import uiPrivateShopBuilder
import localeInfo
import constInfo
import ime

if constInfo.ENABLE_SHOW_CHEST_DROP:
	import grp
import uiSplitItem

class SpecialStorageWindow(ui.ScriptWindow):
	SKILLBOOK_TYPE = 0
	UPPITEM_TYPE = 1
	GHOSTSTONE_TYPE = 2
	GENERAL_TYPE = 3

	SLOT_WINDOW_TYPE = {
		SKILLBOOK_TYPE		:	{"window" : player.SKILLBOOK_INVENTORY,		"slot" : player.SLOT_TYPE_SKILLBOOK_INVENTORY},
		UPPITEM_TYPE		:	{"window" : player.UPPITEM_INVENTORY,		"slot" : player.SLOT_TYPE_UPPITEM_INVENTORY},
		GHOSTSTONE_TYPE		:	{"window" : player.GHOSTSTONE_INVENTORY,	"slot" : player.SLOT_TYPE_GHOSTSTONE_INVENTORY},
		GENERAL_TYPE		:	{"window" : player.GENERAL_INVENTORY,		"slot" : player.SLOT_TYPE_GENERAL_INVENTORY}
	}

	WINDOW_NAMES = {
		SKILLBOOK_TYPE		:	"Inventarul cărţilor",
		UPPITEM_TYPE		:	"Inventar de iteme upgrade",
		GHOSTSTONE_TYPE		:	"Inventar pietre",
		GENERAL_TYPE		:	"Inventarul general",
	}

	if 1 == 0:
		bindWnds = []

	interface = None

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		if 1 == 0:
			self.listHighlightedSlot = [[], [], [], []]

		self.questionDialog = None
		self.tooltipItem = None
		self.dlgSplitItem = None
		self.sellingSlotNumber = -1
		self.isLoaded = 0
		self.inventoryPageIndex = 0
		self.categoryPageIndex = 0

		self.SetWindowName("SpecialStorageWindow")

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		ui.ScriptWindow.Show(self)

		constInfo.IsSpecialStorageOpened = True

		self.__LoadWindow()

	def BindInterfaceClass(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)

	if 1 == 0:
		def BindWindow(self, wnd):
			self.bindWnds.append(wnd)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/SpecialStorageWindow.py")
		except:
			import exception
			exception.Abort("SpecialStorageWindow.LoadWindow.LoadObject")

		try:
			wndItem = self.GetChild("ItemSlot")

			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.titleName = self.GetChild("TitleName")

			#if 1 == 1:
			#	self.separateButton = self.GetChild2("SeparateButton")

			self.inventoryTab = []
			self.inventoryTab.append(self.GetChild("Inventory_Tab_01"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_02"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_03"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_04"))

			self.categoryTab = []
			self.categoryTab.append(self.GetChild("Category_Tab_01"))
			self.categoryTab.append(self.GetChild("Category_Tab_02"))
			self.categoryTab.append(self.GetChild("Category_Tab_03"))
			self.categoryTab.append(self.GetChild("Category_Tab_04"))
		except:
			import exception
			exception.Abort("SpecialStorageWindow.LoadWindow.BindObject")

		## Item
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))

		#if 1 == 1 and self.separateButton:
		#	self.separateButton.SetEvent(ui.__mem_func__(self.SortSpecialStorageDlgMsg))

		## Grade button
		self.inventoryTab[0].SetEvent(lambda arg = 0: self.SetInventoryPage(arg))
		self.inventoryTab[1].SetEvent(lambda arg = 1: self.SetInventoryPage(arg))
		self.inventoryTab[2].SetEvent(lambda arg = 2: self.SetInventoryPage(arg))
		self.inventoryTab[3].SetEvent(lambda arg = 3: self.SetInventoryPage(arg))
		self.inventoryTab[0].Down()

		self.categoryTab[0].SetEvent(lambda arg = 0: self.SetCategoryPage(arg))
		self.categoryTab[1].SetEvent(lambda arg = 1: self.SetCategoryPage(arg))
		self.categoryTab[2].SetEvent(lambda arg = 2: self.SetCategoryPage(arg))
		self.categoryTab[3].SetEvent(lambda arg = 3: self.SetCategoryPage(arg))
		self.categoryTab[0].Down()

		## Etc
		self.wndItem = wndItem

		self.wndPopupDialog = uiCommon.PopupDialog()

		## SplitItemDialog
		self.dlgSplitItem = uiSplitItem.SplitItemDialog()
		self.dlgSplitItem.LoadDialog()
		self.dlgSplitItem.Hide()

		#####

		## Refresh & Set
		self.SetInventoryPage(0)
		self.SetCategoryPage(0)

		## Refresh
		self.RefreshItemSlot()
		self.RefreshBagSlotWindow()

	def ClickButton(self, arg):
		self.SetInventoryPage(0)
		self.SetCategoryPage(arg)

	if 1 == 1:
		def SortSpecialStorageDlgMsg(self):
			if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SORT_INV_A_WINDOW_IS_OPEN)
				return

			self.questionDialog = uiCommon.QuestionDialog2()
			self.questionDialog.SetText1(localeInfo.INVENTORY_SORT_DLG_MSG)
			self.questionDialog.SetText2(localeInfo.INVENTORY_SORT_DLG_MSG_2)
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SortSpecialStorageWindow))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()

		def __CanStackItem(self, itemVnum):
			item.SelectItem(itemVnum)

			if item.IsFlag(item.ITEM_FLAG_STACKABLE) and not item.IsAntiFlag(item.ITEM_ANTIFLAG_STACK):
				return True

			return False

		def GetCurrentItemGrid(self):
			itemGrid = [[False for cell in xrange(player.SPECIAL_STORAGE_PAGE_SIZE)] for page in xrange(player.SPECIAL_STORAGE_PAGE_COUNT)]

			for page in xrange(player.SPECIAL_STORAGE_PAGE_COUNT):
				for cell in xrange(player.SPECIAL_STORAGE_PAGE_SIZE):
					realCell = page * player.SPECIAL_STORAGE_PAGE_SIZE + cell

					itemVnum = player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], realCell)

					if itemVnum != 0:
						item.SelectItem(itemVnum)

						width, height = item.GetItemSize()

						for i in xrange(height):
							itemGrid[page][cell + (i * 5)] = True

			return itemGrid

		def FindEmptyCellForSize(self, itemGrid, size):
			for page in xrange(player.SPECIAL_STORAGE_PAGE_COUNT):
				for cell in xrange(player.SPECIAL_STORAGE_PAGE_SIZE):
					if itemGrid[page][cell] == False:
						check = True

						for i in xrange(size):
							checkCell = cell + 5 * i

							try:
								if itemGrid[page][checkCell] == True:
									check = False
									break
							except IndexError:
								check = False
								break

						if check:
							return cell + (page * player.SPECIAL_STORAGE_PAGE_SIZE)

			return -1

		def SortSpecialStorageWindow(self):
			## Needed because if you open first the questionDialog and
			## a second dialog you can continue.
			if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SORT_INV_A_WINDOW_IS_OPEN)
				self.OnCloseQuestionDialog()
				return

			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
				self.OnCloseQuestionDialog()
				return

			m2netm2g.SendChatPacket("/sort_special_storage %d 1" % self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"])

			self.OnCloseQuestionDialog()

		# Working with serverside command.
		def AutoStackStorage(self):
			specialInventoryCopy = []

			for cell in xrange(player.SPECIAL_STORAGE_PAGE_COUNT * player.SPECIAL_STORAGE_PAGE_SIZE):
				itemVnum = player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], cell)

				if itemVnum != 0:
					specialInventoryCopy.append({"vnum" : itemVnum, "count" : player.GetItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], cell), "old_cell" : cell})
				else:
					specialInventoryCopy.append({"vnum" : 0, "count" : 0, "old_cell" : cell})

			itemGrid = self.GetCurrentItemGrid()

			for page in xrange(player.SPECIAL_STORAGE_PAGE_COUNT):
				for cell in xrange(player.SPECIAL_STORAGE_PAGE_SIZE):
					realCell = page * player.SPECIAL_STORAGE_PAGE_SIZE + cell

					itemVnum = specialInventoryCopy[realCell]["vnum"]
					itemCount = specialInventoryCopy[realCell]["count"]

					metinSlot = [player.GetItemMetinSocket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], realCell, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]

					if (itemVnum == 0) or (itemCount >= 200) or (not self.__CanStackItem(itemVnum)):
						continue

					for checkCell in xrange(realCell):
						checkItemVnum = specialInventoryCopy[checkCell]["vnum"]
						checkItemCount = specialInventoryCopy[checkCell]["count"]
						checkMetinSlot = [player.GetItemMetinSocket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], checkCell, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]

						if (checkItemVnum == 0) or (checkItemCount >= 200) \
						or (not self.__CanStackItem(checkItemVnum)) or (checkMetinSlot != metinSlot) \
						or (checkItemVnum != itemVnum):
							continue

						self.__SendMoveItemPacket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], realCell, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], checkCell, itemCount)

						specialInventoryCopy[realCell]["count"] -= 200 - checkItemCount
						specialInventoryCopy[checkCell]["count"] = min(200, checkItemCount + itemCount)

						if specialInventoryCopy[realCell]["count"] <= 0:
							specialInventoryCopy[realCell]["vnum"] = 0
							specialInventoryCopy[realCell]["count"] = 0

							itemGrid[page][cell] = False
						else:
							item.SelectItem(itemVnum)

							emptyCell = self.FindEmptyCellForSize(itemGrid, item.GetItemSize()[1])

							self.__SendMoveItemPacket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], realCell, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], checkCell, itemCount)

							item.SelectItem(specialInventoryCopy[realCell]["vnum"])

							width, height = item.GetItemSize()

							specialInventoryCopy[emptyCell]["vnum"] = specialInventoryCopy[realCell]["vnum"]
							specialInventoryCopy[emptyCell]["count"] = specialInventoryCopy[realCell]["count"]
							specialInventoryCopy[emptyCell]["old_cell"] = realCell
							specialInventoryCopy[realCell]["vnum"] = 0
							specialInventoryCopy[realCell]["count"] = 0

							for i in xrange(height):
								itemGrid[page][cell + i * 5] = False
								itemGrid[page][cell + i * 5] = True

						break

			m2netm2g.SendChatPacket("/sort_special_storage %d 0" % self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"])

	def Destroy(self):
		self.ClearDictionary()
		self.tooltipItem = None
		self.wndItem = 0
		self.questionDialog = None
		self.dlgSplitItem.Destroy()
		self.dlgSplitItem = None
		self.inventoryTab = []
		self.categoryTab = []
		self.titleName = None

		if 1 == 0:
			self.bindWnds = []

		self.interface = None

	def Close(self):
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		if self.dlgSplitItem:
			self.dlgSplitItem.Close()

		constInfo.IsSpecialStorageOpened = False

		self.Hide()

	def SetInventoryPage(self, page):
		self.inventoryTab[self.inventoryPageIndex].SetUp()
		self.inventoryPageIndex = page
		self.inventoryTab[self.inventoryPageIndex].Down()

		self.RefreshBagSlotWindow()

	def SetCategoryPage(self, page):
		self.categoryTab[self.categoryPageIndex].SetUp()
		self.categoryPageIndex = page
		self.categoryTab[self.categoryPageIndex].Down()

		self.titleName.SetText(self.WINDOW_NAMES[self.categoryPageIndex])

		constInfo.SpecialStorageCategory = self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"]

		self.RefreshBagSlotWindow()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def RefreshItemSlot(self):
		self.RefreshBagSlotWindow()

	def RefreshStatus(self):
		self.RefreshItemSlot()

	def __SpecialStorageLocalSlotPosToGlobalSlotPos(self, localSlotPos):
		return self.inventoryPageIndex * player.SPECIAL_STORAGE_PAGE_SIZE + localSlotPos

	if 1 == 0:
		def SetCanMouseEventSlot(self, slotPos):
			# slotNumber = self.__SpecialStorageLocalSlotPosToGlobalSlotPos(slotPos)

			self.wndItem.SetCantMouseEventSlot(slotPos)

		def SetCantMouseEventSlot(self, slotPos):
			# slotNumber = self.__SpecialStorageLocalSlotPosToGlobalSlotPos(slotPos)

			self.wndItem.SetCantMouseEventSlot(slotPos)

		def GetSpecialStoragePageIndex(self):
			return self.inventoryPageIndex

		def RefreshMarkSlots(self, localIndex = None):
			if not self.interface:
				return

			onTopWnd = self.interface.GetOnTopWindow()

			if localIndex:
				slotNumber = self.__SpecialStorageLocalSlotPosToGlobalSlotPos(localIndex)

				windowType = self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"]

				if onTopWnd == player.ON_TOP_WND_NONE:
					self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_SHOP:
					if player.IsAntiFlagBySlot(windowType, slotNumber, item.ANTIFLAG_SELL):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_EXCHANGE:
					if player.IsAntiFlagBySlot(windowType, slotNumber, item.ANTIFLAG_GIVE):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_PRIVATE_SHOP:
					if player.IsAntiFlagBySlot(windowType, slotNumber, item.ITEM_ANTIFLAG_MYSHOP):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_SAFEBOX:
					if player.IsAntiFlagBySlot(windowType, slotNumber, item.ANTIFLAG_SAFEBOX):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				return

			for i in xrange(player.SPECIAL_STORAGE_PAGE_SIZE * player.SPECIAL_STORAGE_PAGE_COUNT):
				slotNumber = self.__SpecialStorageLocalSlotPosToGlobalSlotPos(i)

				windowType = self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"]

				if onTopWnd == player.ON_TOP_WND_NONE:
					self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_SHOP:
					if player.IsAntiFlagBySlot(windowType, slotNumber, item.ANTIFLAG_SELL):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_EXCHANGE:
					if player.IsAntiFlagBySlot(windowType, slotNumber, item.ANTIFLAG_GIVE):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_PRIVATE_SHOP:
					if player.IsAntiFlagBySlot(windowType, slotNumber, item.ITEM_ANTIFLAG_MYSHOP):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_SAFEBOX:
					if player.IsAntiFlagBySlot(windowType, slotNumber, item.ANTIFLAG_SAFEBOX):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

	def RefreshBagSlotWindow(self):
		getItemVNum = player.GetItemIndex
		getItemCount = player.GetItemCount
		setItemVnum = self.wndItem.SetItemSlot

		for i in xrange(player.SPECIAL_STORAGE_PAGE_SIZE * player.SPECIAL_STORAGE_PAGE_COUNT):
			self.wndItem.EnableSlot(i)

			slotNumber = self.__SpecialStorageLocalSlotPosToGlobalSlotPos(i)

			itemCount = getItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotNumber)
			itemVnum = getItemVNum(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotNumber)

			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0

			setItemVnum(i, itemVnum, itemCount)

			if 1 == 0:
				ITEM_AND_POS = { 30071 : [12, 12], }

				if itemVnum and item.GetItemType() == item.ITEM_TYPE_MATERIAL and item.GetItemName()[-1:] == "+":
					if itemVnum in ITEM_AND_POS:
						self.wndItem.AppendPlusOnSlot(i, ITEM_AND_POS[itemVnum][0], ITEM_AND_POS[itemVnum][1])
					else:
						self.wndItem.AppendPlusOnSlot(i, 12, -1)
				else:
					self.wndItem.AppendPlusOnSlot(i, 0, 0)

			if 1 == 0:
				if slotNumber in self.listHighlightedSlot[self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"] - 6]:
					self.wndItem.ActivateSlot(i)
				else:
					self.wndItem.DeactivateSlot(i)

			if 1 == 0:
				self.RefreshMarkSlots(i)

		self.wndItem.RefreshSlot()

		if 1 == 0:
			map(lambda wnd:wnd.RefreshLockedSlot(), self.bindWnds)

	def ShowToolTip(self, slotIndex):
		if None != self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"])
			if constInfo.ENABLE_SHOW_CHEST_DROP:
				itemVnum = player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotIndex)
				item.SelectItem(itemVnum)
				if item.GetItemType() == item.ITEM_TYPE_GIFTBOX:
					self.tooltipItem.AppendSpace(5)
					text = self.tooltipItem.AppendTextLine("|Ekey_ctrl|e"+" + "+"|Ekey_lclick|e - Pentru previzualizarea conţinutului",grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0),False)
					text.SetHorizontalAlignLeft()
					self.tooltipItem.AppendSpace(5)
					text = self.tooltipItem.AppendTextLine("|Ekey_alt|e"+" + "+"|Ekey_rclick|e - Deschizi %dpcs"%constInfo.ULTIMATE_TOOLTIP_MAX_CLICK,grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0),False)
					text.SetHorizontalAlignLeft()
				elif constInfo.IsNewChest(itemVnum):
					self.tooltipItem.AppendSpace(5)
					text = self.tooltipItem.AppendTextLine("|Ekey_alt|e"+" + "+"|Ekey_rclick|e - Deschizii %dpcs"%constInfo.ULTIMATE_TOOLTIP_MAX_CLICK,grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0),False)
					text.SetHorizontalAlignLeft()
				if player.CanMoveItem(itemVnum):
					self.tooltipItem.AppendSpace(5)
					text = self.tooltipItem.AppendTextLine("|Ekey_ctrl|e"+" + "+"|Ekey_rclick|e - Mutare în inventar.",grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0),False)
					text.SetHorizontalAlignLeft()
	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnTop(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetTop()

		if 1 == 0:
			map(lambda wnd:wnd.RefreshLockedSlot(), self.bindWnds)

			self.RefreshMarkSlots()

	def OverOutItem(self):	
		self.wndItem.SetUsableItem(False)

		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, overSlotPos):
		if 1 == 0:
			slotNumber = self.__SpecialStorageLocalSlotPosToGlobalSlotPos(overSlotPos)
			itemVnum = player.GetItemIndex(slotNumber)

			self.wndItem.DeactivateSlot(overSlotPos)

			try:
				self.listHighlightedSlot[self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"] - 6].remove(slotNumber)
			except:
				pass

		overSlotPos = self.__SpecialStorageLocalSlotPosToGlobalSlotPos(overSlotPos)

		self.wndItem.SetUsableItem(False)
		self.ShowToolTip(overSlotPos)

	def OnPickItem(self, count, split = False):
		itemSlotIndex = self.dlgSplitItem.itemGlobalSlotIndex
		selectedItemVNum = player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex)

		mouseModule.mouseController.AttachObject(self, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["slot"], itemSlotIndex, selectedItemVNum, count)

	if 1 == 0:
		def HighlightSlot(self, slot, invtype):
			if slot not in self.listHighlightedSlot[invtype - 6]:
				self.listHighlightedSlot[invtype - 6].append(slot)

	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		itemSlotIndex = self.__SpecialStorageLocalSlotPosToGlobalSlotPos(itemSlotIndex)
		selectedItemVNum = player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex)
		itemCount = player.GetItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex)

		if app.ENABLE_SELL_ITEM:		
			if app.IsPressed(app.DIK_LSHIFT) and app.IsPressed(app.DIK_X) and self.IsSellItems(itemSlotIndex):
				self.__SendSellItemPacket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex)
				return

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()

			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				m2netm2g.SendItemMovePacket(player.SLOT_TYPE_INVENTORY, attachedSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex, attachedItemCount)

			if self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["slot"] == attachedSlotType:
				if attachedItemVID == selectedItemVNum:
					m2netm2g.SendItemMovePacket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], attachedSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex, attachedItemCount)
				else:
					m2netm2g.SendItemUseToItemPacket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], attachedSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex)

			mouseModule.mouseController.DeattachObject()
		else:
			curCursorNum = app.GetCursor()

			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)
			elif app.BUY == curCursorNum:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)
			elif app.IsPressed(app.DIK_LALT):
				link = player.GetItemLink(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex)
				ime.PasteString(link)
			elif app.IsPressed(app.DIK_LCONTROL):
				if constInfo.ENABLE_SHOW_CHEST_DROP:
					item.SelectItem(selectedItemVNum)
					if item.GetItemType() == item.ITEM_TYPE_GIFTBOX:
						m2netm2g.SendChestDropInfo(0,selectedItemVNum)
						return
			elif app.IsPressed(app.DIK_LSHIFT):
				item.SelectItem(selectedItemVNum)
				if item.IsAntiFlag(item.ITEM_ANTIFLAG_STACK):
					return
				if itemCount > 1:
					self.dlgSplitItem.SetTitleName(localeInfo.PICK_ITEM_TITLE)
					self.dlgSplitItem.SetAcceptEvent(ui.__mem_func__(self.OnSplitItem))
					self.dlgSplitItem.Open(itemCount)
					self.dlgSplitItem.itemGlobalSlotIndex = itemSlotIndex
			else:
				mouseModule.mouseController.AttachObject(self, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["slot"], itemSlotIndex, selectedItemVNum, itemCount)
				self.wndItem.SetUseMode(False)
				snd.PlaySound("sound/ui/pick.wav")

	def OnSplitItem(self, count, full_split):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		if full_split:
			m2netm2g.SendChatPacket("/storage_split_item %d %d %d" % (self.dlgSplitItem.itemGlobalSlotIndex, count, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"]))
		else:
			self.OnPickItem(count)

	def __SellItem(self, itemSlotPos):
		self.sellingSlotNumber = itemSlotPos

		itemIndex = player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotPos)
		itemCount = player.GetItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotPos)

		item.SelectItem(itemIndex)

		if item.IsAntiFlag(item.ANTIFLAG_SELL):
			popup = uiCommon.PopupDialog()
			popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
			popup.SetAcceptEvent(self.__OnClosePopupDialog)
			popup.Open()
			self.popup = popup
			return

		itemPrice = item.GetISellItemPrice()

		if item.Is1GoldItem():
			itemPrice = itemCount / itemPrice / 5
		else:
			itemPrice = itemPrice * itemCount / 5

		item.GetItemName(itemIndex)

		self.questionDialog = uiCommon.QuestionShopSellDialog()
		self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM3)
		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		self.questionDialog.Open(itemIndex, self.sellingSlotNumber, itemCount, itemPrice, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"])
		self.questionDialog.count = itemCount

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def SellItem(self):
		m2netm2g.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"])
		snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if self.questionDialog:
			self.questionDialog.Close()

		self.questionDialog = None

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def __OnClosePopupDialog(self):
		self.pop = None

	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		selectedSlotPos = self.__SpecialStorageLocalSlotPosToGlobalSlotPos(selectedSlotPos)

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)

			if player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				mouseModule.mouseController.RunCallBack("INVENTORY")
			elif player.SLOT_TYPE_SHOP == attachedSlotType:
				m2netm2g.SendShopBuyPacket(attachedSlotPos)
			elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:
				m2netm2g.SendSafeboxCheckoutPacket(attachedSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], selectedSlotPos)
			elif player.SLOT_TYPE_MALL == attachedSlotType:
				m2netm2g.SendMallCheckoutPacket(attachedSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], selectedSlotPos)
			elif player.RESERVED_WINDOW != attachedInvenType:
				self.__SendMoveItemPacket(attachedInvenType, attachedSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], selectedSlotPos, attachedItemCount)

			mouseModule.mouseController.DeattachObject()

	def UseItemSlot(self, slotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		slotIndex = self.__SpecialStorageLocalSlotPosToGlobalSlotPos(slotIndex)

		import shop

		itemCount = player.GetItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotIndex)
		windowType = self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"]
		
		if constInfo.ENABLE_SHOW_CHEST_DROP:
			if app.IsPressed(app.DIK_LALT):
				itemVnum = player.GetItemIndex(windowType, slotIndex)
				if constInfo.IsNewChest(itemVnum) or item.GetItemType() == item.ITEM_TYPE_GIFTBOX:
					if itemCount > constInfo.ULTIMATE_TOOLTIP_MAX_CLICK:
						itemCount = constInfo.ULTIMATE_TOOLTIP_MAX_CLICK
					for j in xrange(itemCount):
						m2netm2g.SendItemUsePacket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotIndex)
					return
			elif app.IsPressed(app.DIK_LCONTROL) and player.CanMoveItem(player.GetItemIndex(windowType, slotIndex)):
				m2netm2g.SendChatPacket("/transfer_storage_inv %d %d" % (slotIndex, windowType))
				return

		if app.IsPressed(app.DIK_LCONTROL):
			if app.IsPressed(app.DIK_X) and shop.IsOpen():
				m2netm2g.SendShopSellPacketNew(slotIndex, itemCount, windowType)
			else:
				m2netm2g.SendChatPacket("/transfer_storage_inv %d %d" % (slotIndex, windowType))
		else:
			m2netm2g.SendItemUsePacket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotIndex)

		mouseModule.mouseController.DeattachObject()

		self.OverOutItem()

	def __SendMoveItemPacket(self, srcSlotWindow, srcSlotPos, dstSlotWindow, dstSlotPos, srcItemCount):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		m2netm2g.SendItemMovePacket(srcSlotWindow, srcSlotPos, dstSlotWindow, dstSlotPos, srcItemCount)

	if app.ENABLE_SELL_ITEM:
		def IsSellItems(self, slotIndex):
			itemVnum = player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotIndex)
			item.SelectItem(itemVnum)
			itemPrice = item.GetISellItemPrice()
			
			# if item.GetItemType() == item.ITEM_TYPE_WEAPON or item.GetItemType() == item.ITEM_TYPE_ARMOR:
				# return True
				
			if itemPrice > 1:
				return True
				
			return False
			
		def __SendSellItemPacket(self, itemInvenType, itemVNum):
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
				return
				
			m2netm2g.SendItemSellPacket(itemInvenType, itemVNum)