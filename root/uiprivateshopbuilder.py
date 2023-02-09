import ui
import snd
import shop
import mouseModule
import player
import chr
import net
import uiCommon
import localeInfo
import chat
import item
import systemSetting
import player
import app
import constInfo

g_isBuildingPrivateShop = False

g_itemPriceDict={}
if app.ENABLE_CHEQUE_SYSTEM:
	g_itemChequeDict={}

g_privateShopAdvertisementBoardDict={}

def Clear():
	global g_itemPriceDict
	global g_isBuildingPrivateShop
	g_itemPriceDict={}
	g_isBuildingPrivateShop = False
	if app.ENABLE_CHEQUE_SYSTEM:
		global g_itemChequeDict
		g_itemChequeDict={}

def IsPrivateShopItemPriceList():
	global g_itemPriceDict
	if g_itemPriceDict:
		return True
	else:
		return False

def IsBuildingPrivateShop():
	global g_isBuildingPrivateShop
	if player.IsOpenPrivateShop() or g_isBuildingPrivateShop:
		return True
	else:
		return False

def SetPrivateShopItemPrice(itemVNum, itemPrice):
	global g_itemPriceDict
	g_itemPriceDict[int(itemVNum)]=itemPrice
	
def GetPrivateShopItemPrice(itemVNum):
	try:
		global g_itemPriceDict
		return g_itemPriceDict[itemVNum]
	except KeyError:
		return 0

if app.ENABLE_CHEQUE_SYSTEM:
	def IsPrivateShopItemChequePriceList():
		global g_itemChequeDict
		if g_itemChequeDict:
			return True
		return False

	def SetPrivateShopItemCheque(itemVNum, itemCheque):
		global g_itemChequeDict
		g_itemChequeDict[int(itemVNum)]=itemCheque

	def GetPrivateShopItemCheque(itemVNum):
		try:
			global g_itemChequeDict
			return g_itemChequeDict[itemVNum]
		except KeyError:
			return 0
		
def UpdateADBoard():	
	for key in g_privateShopAdvertisementBoardDict.keys():
		g_privateShopAdvertisementBoardDict[key].Show()
		
def DeleteADBoard(vid):
	if not g_privateShopAdvertisementBoardDict.has_key(vid):
		return
			
	del g_privateShopAdvertisementBoardDict[vid]
		

class PrivateShopAdvertisementBoard(ui.ThinBoard):
	def __init__(self):
		ui.ThinBoard.__init__(self, "UI_BOTTOM")
		self.vid = None
		self.__MakeTextLine()

	def __del__(self):
		ui.ThinBoard.__del__(self)

	def __MakeTextLine(self):
		self.textLine = ui.TextLine()
		self.textLine.SetParent(self)
		self.textLine.SetWindowHorizontalAlignCenter()
		self.textLine.SetWindowVerticalAlignCenter()
		self.textLine.SetHorizontalAlignCenter()
		self.textLine.SetVerticalAlignCenter()
		self.textLine.Show()

	def Open(self, vid, text):
		self.vid = vid

		self.textLine.SetText(text)
		self.textLine.UpdateRect()
		self.SetSize(len(text)*6 + 10*2, 20)
		self.Show() 
				
		g_privateShopAdvertisementBoardDict[vid] = self
		
	def OnMouseLeftButtonUp(self):
		if not self.vid:
			return
		net.SendOnClickPacket(self.vid)
		
		return True
		
	def OnUpdate(self):
		if not self.vid:
			return
		
		if systemSetting.IsShowSalesText():
			if not app.ENABLE_SHOPNAMES_RANGE:
				self.Show()
				(x, y) = chr.GetProjectPosition(self.vid, 220)
				self.SetPosition(x - self.GetWidth() / 2, y - self.GetHeight() / 2)
			else:
				if systemSetting.GetShopNamesRange() == 1.000:
					self.Show()
					(x, y) = chr.GetProjectPosition(self.vid, 220)
					self.SetPosition(x - self.GetWidth() / 2, y - self.GetHeight() / 2)
				else:
					LIMIT_RANGE = abs(constInfo.SHOPNAMES_RANGE * systemSetting.GetShopNamesRange())
					(to_x, to_y, to_z) = chr.GetPixelPosition(self.vid)
					(my_x, my_y, my_z) = player.GetMainCharacterPosition()
					if abs(my_x - to_x) <= LIMIT_RANGE and abs(my_y - to_y) <= LIMIT_RANGE:
						(x, y) = chr.GetProjectPosition(self.vid, 220)
						self.SetPosition(x - self.GetWidth() / 2, y - self.GetHeight() / 2)
						self.Show()
					else:
						self.Hide()
						self.SetPosition(-70, 0)
		else:
			for key in g_privateShopAdvertisementBoardDict.keys():
				if player.GetMainCharacterIndex() == key:
					g_privateShopAdvertisementBoardDict[key].Show()
					x, y = chr.GetProjectPosition(player.GetMainCharacterIndex(), 220)
					g_privateShopAdvertisementBoardDict[key].SetPosition(x - self.GetWidth()/2, y - self.GetHeight()/2)
				else:
					g_privateShopAdvertisementBoardDict[key].Hide()

class PrivateShopBuilder(ui.ScriptWindow):

	def __init__(self):
		#print "NEW MAKE_PRIVATE_SHOP_WINDOW ----------------------------------------------------------------"
		ui.ScriptWindow.__init__(self)

		self.__LoadWindow()
		self.itemStock = {}
		self.tooltipItem = None
		self.priceInputBoard = None
		self.title = ""
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.interface = None
			self.wndInventory = None
			self.lockedItems = {i:(-1,-1) for i in range(shop.SHOP_SLOT_COUNT)}
	def __del__(self):
		#print "------------------------------------------------------------- DELETE MAKE_PRIVATE_SHOP_WINDOW"
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/PrivateShopBuilder.py")
		except:
			import exception
			exception.Abort("PrivateShopBuilderWindow.LoadWindow.LoadObject")

		try:
			GetObject = self.GetChild
			self.nameLine = GetObject("NameLine")
			self.itemSlot = GetObject("ItemSlot")
			self.btnOk = GetObject("OkButton")
			self.btnClose = GetObject("CloseButton")
			self.titleBar = GetObject("TitleBar")
		except:
			import exception
			exception.Abort("PrivateShopBuilderWindow.LoadWindow.BindObject")

		self.btnOk.SetEvent(ui.__mem_func__(self.OnOk))
		self.btnClose.SetEvent(ui.__mem_func__(self.OnClose))
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.OnClose))

		self.itemSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.OnSelectEmptySlot))
		self.itemSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.OnSelectItemSlot))
		self.itemSlot.SetOverInItemEvent(ui.__mem_func__(self.OnOverInItem))
		self.itemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))

	def Destroy(self):
		self.ClearDictionary()

		self.nameLine = None
		self.itemSlot = None
		self.btnOk = None
		self.btnClose = None
		self.titleBar = None
		self.priceInputBoard = None
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.interface = None
			self.wndInventory = None
			self.lockedItems = {i:(-1,-1) for i in range(shop.SHOP_SLOT_COUNT)}

	def Open(self, title):

		self.title = title

		if len(title) > 25:
			title = title[:22] + "..."

		self.itemStock = {}
		shop.ClearPrivateShopStock()
		self.nameLine.SetText(title)
		self.SetCenterPosition()
		self.Refresh()
		self.Show()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.lockedItems = {i:(-1,-1) for i in range(shop.SHOP_SLOT_COUNT)}
			self.interface.SetOnTopWindow(player.ON_TOP_WND_PRIVATE_SHOP)
			self.interface.RefreshMarkInventoryBag()
		global g_isBuildingPrivateShop
		g_isBuildingPrivateShop = True

	def Close(self):
		global g_isBuildingPrivateShop
		g_isBuildingPrivateShop = False

		self.title = ""
		self.itemStock = {}
		shop.ClearPrivateShopStock()
		self.Hide()

		if self.priceInputBoard:
			self.priceInputBoard.Close()
			self.priceInputBoard = None

		if app.WJ_ENABLE_TRADABLE_ICON:
			for privatePos, (itemInvenPage, itemSlotPos) in self.lockedItems.items():
				if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
					self.wndInventory.wndItem.SetCanMouseEventSlot(itemSlotPos)

			self.lockedItems = {i:(-1,-1) for i in range(shop.SHOP_SLOT_COUNT)}
			self.interface.SetOnTopWindow(player.ON_TOP_WND_NONE)
			self.interface.RefreshMarkInventoryBag()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def Refresh(self):
		getitemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setitemVNum=self.itemSlot.SetItemSlot
		delItem=self.itemSlot.ClearSlot

		for i in xrange(shop.SHOP_SLOT_COUNT):

			if not self.itemStock.has_key(i):
				delItem(i)
				continue

			pos = self.itemStock[i]

			itemCount = getItemCount(*pos)
			if itemCount <= 1:
				itemCount = 0
			setitemVNum(i, getitemVNum(*pos), itemCount)
			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = player.GetItemTransmutation(*pos)
				if itemTransmutedVnum:
					self.itemSlot.DisableCoverButton(i)
				else:
					self.itemSlot.EnableCoverButton(i)
		self.itemSlot.RefreshSlot()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.RefreshLockedSlot()

	def OnSelectEmptySlot(self, selectedSlotPos):

		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()

			if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
				if player.SLOT_TYPE_INVENTORY != attachedSlotType and\
					player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedSlotType and\
					player.SLOT_TYPE_SKILLBOOK_INVENTORY != attachedSlotType and\
					player.SLOT_TYPE_UPPITEM_INVENTORY != attachedSlotType and\
					player.SLOT_TYPE_GHOSTSTONE_INVENTORY != attachedSlotType and\
					player.SLOT_TYPE_GENERAL_INVENTORY != attachedSlotType:
					return
			else:
				if player.SLOT_TYPE_INVENTORY != attachedSlotType and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedSlotType:
					return

			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				
			itemVNum = player.GetItemIndex(attachedInvenType, attachedSlotPos)
			item.SelectItem(itemVNum)

			if item.IsAntiFlag(item.ANTIFLAG_GIVE) or item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.PRIVATE_SHOP_CANNOT_SELL_ITEM)
				return
			if app.WJ_ENABLE_TRADABLE_ICON and player.SLOT_TYPE_INVENTORY == attachedSlotType:
				self.CantTradableItem(selectedSlotPos, attachedSlotPos)
			priceInputBoard = uiCommon.MoneyInputDialog()
			priceInputBoard.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_PRICE_DIALOG_TITLE)
			priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrice))
			priceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrice))
			priceInputBoard.Open()

			itemPrice=GetPrivateShopItemPrice(itemVNum)
			if app.ENABLE_CHEQUE_SYSTEM:
				itemCheque=GetPrivateShopItemCheque(itemVNum)

			if itemPrice>0:
				priceInputBoard.SetValue(itemPrice)
			
			if app.ENABLE_CHEQUE_SYSTEM and itemCheque > 0:
				priceInputBoard.SetChequeValue(itemCheque)
				priceInputBoard.SetFocus()
			
			self.priceInputBoard = priceInputBoard
			self.priceInputBoard.itemVNum = itemVNum
			self.priceInputBoard.sourceWindowType = attachedInvenType
			self.priceInputBoard.sourceSlotPos = attachedSlotPos
			self.priceInputBoard.targetSlotPos = selectedSlotPos

	def OnSelectItemSlot(self, selectedSlotPos):

		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			snd.PlaySound("sound/ui/loginfail.wav")
			mouseModule.mouseController.DeattachObject()

		else:
			if not selectedSlotPos in self.itemStock:
				return

			invenType, invenPos = self.itemStock[selectedSlotPos]
			shop.DelPrivateShopItemStock(invenType, invenPos)
			snd.PlaySound("sound/ui/drop.wav")
			if app.WJ_ENABLE_TRADABLE_ICON:
				(itemInvenPage, itemSlotPos) = self.lockedItems[selectedSlotPos]
				if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
					self.wndInventory.wndItem.SetCanMouseEventSlot(itemSlotPos)

				self.lockedItems[selectedSlotPos] = (-1, -1)
			del self.itemStock[selectedSlotPos]

			self.Refresh()

	def AcceptInputPrice(self):

		if not self.priceInputBoard:
			return True

		text = self.priceInputBoard.GetText()

		if app.ENABLE_CHEQUE_SYSTEM:
			cheText = self.priceInputBoard.GetChequeText()
			if not text and not cheText:
				return True

			if not text.isdigit() and not cheText.isdigit():
				return True

			if int(text) <= 0 and int(cheText) <= 0:
				return True
		else:
			if not text:
				return True

			if not text.isdigit():
				return True

			if int(text) <= 0:
				return True

		attachedInvenType = self.priceInputBoard.sourceWindowType
		sourceSlotPos = self.priceInputBoard.sourceSlotPos
		targetSlotPos = self.priceInputBoard.targetSlotPos

		for privatePos, (itemWindowType, itemSlotIndex) in self.itemStock.items():
			if itemWindowType == attachedInvenType and itemSlotIndex == sourceSlotPos:
				shop.DelPrivateShopItemStock(itemWindowType, itemSlotIndex)
				del self.itemStock[privatePos]

		price = int(self.priceInputBoard.GetText())
		if app.ENABLE_CHEQUE_SYSTEM:
			cheque = int(self.priceInputBoard.GetChequeText())

		if IsPrivateShopItemPriceList():
			SetPrivateShopItemPrice(self.priceInputBoard.itemVNum, price)
		if app.ENABLE_CHEQUE_SYSTEM and IsPrivateShopItemChequePriceList():
			SetPrivateShopItemCheque(self.priceInputBoard.itemVNum, cheque)

		if app.ENABLE_CHEQUE_SYSTEM:
			shop.AddPrivateShopItemStock(attachedInvenType, sourceSlotPos, targetSlotPos, price, cheque)
		else:
			shop.AddPrivateShopItemStock(attachedInvenType, sourceSlotPos, targetSlotPos, price)
		self.itemStock[targetSlotPos] = (attachedInvenType, sourceSlotPos)
		snd.PlaySound("sound/ui/drop.wav")

		self.Refresh()

		#####

		self.priceInputBoard = None
		return True

	def CancelInputPrice(self):
		if app.WJ_ENABLE_TRADABLE_ICON:
			itemInvenPage = self.priceInputBoard.sourceSlotPos / player.INVENTORY_PAGE_SIZE
			itemSlotPos = self.priceInputBoard.sourceSlotPos - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
			if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
				self.wndInventory.wndItem.SetCanMouseEventSlot(itemSlotPos)

			self.lockedItems[self.priceInputBoard.targetSlotPos] = (-1, -1)

		if self.priceInputBoard:
			self.priceInputBoard.Close()
		self.priceInputBoard = None
		return 1

	def OnOk(self):

		if not self.title:
			return

		if 0 == len(self.itemStock):
			return

		shop.BuildPrivateShop(self.title)
		self.Close()

	def OnClose(self):
		self.Close()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnOverInItem(self, slotIndex):

		if self.tooltipItem:
			if self.itemStock.has_key(slotIndex):
				self.tooltipItem.SetPrivateShopBuilderItem(*self.itemStock[slotIndex] + (slotIndex,))

	def OnOverOutItem(self):

		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	if app.WJ_ENABLE_TRADABLE_ICON:
		def CantTradableItem(self, destSlotIndex, srcSlotIndex):
			itemInvenPage = srcSlotIndex / player.INVENTORY_PAGE_SIZE
			localSlotPos = srcSlotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
			self.lockedItems[destSlotIndex] = (itemInvenPage, localSlotPos)
			if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
				self.wndInventory.wndItem.SetCantMouseEventSlot(localSlotPos)

		def RefreshLockedSlot(self):
			if self.wndInventory:
				for privatePos, (itemInvenPage, itemSlotPos) in self.lockedItems.items():
					if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
						self.wndInventory.wndItem.SetCantMouseEventSlot(itemSlotPos)

				self.wndInventory.wndItem.RefreshSlot()

		def BindInterface(self, interface):
			self.interface = interface

		def OnTop(self):
			if self.interface:
				self.interface.SetOnTopWindow(player.ON_TOP_WND_PRIVATE_SHOP)
				self.interface.RefreshMarkInventoryBag()

		def SetInven(self, wndInventory):
			from _weakref import proxy
			self.wndInventory = proxy(wndInventory)