import app
import ui
import uiCommon
import uiToolTip
import mouseModule
import localeInfo
import constInfo
import net
import player
import item
import snd
import shop
import wndMgr
import chat
import chr

g_isEditingOfflineShop = False

def IsEditingOfflineShop():
	global g_isEditingOfflineShop
	if g_isEditingOfflineShop:
		return True
	else:
		return False

class TextBoard(ui.ThinBoard):

	def __init__(self):
		ui.ThinBoard.__init__(self)
		self.lineHeight = 12
		self.childrenList = []

	def __del__(self):
		ui.ThinBoard.__del__(self)

	def Clear(self):
		self.lineHeight = 12
		self.childrenList = []

	def AppendTextLine(self, text):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(localeInfo.UI_DEF_FONT_LARGE)
		textLine.SetText(str(text))
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.Show()
		textLine.SetPosition(10, self.lineHeight)
		self.childrenList.append(textLine)
		self.lineHeight += 17
		return textLine

if app.ENABLE_CHEQUE_SYSTEM:
	class myBankWindow(ui.ScriptWindow):
		def __init__(self):
			ui.ScriptWindow.__init__(self)
			self.Children = []
			self.withdrawQuestionDialog = None
			self.__LoadWindow()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def Destroy(self):
			self.ClearDictionary()
			self.Children = []

		def __LoadWindow(self):
			self.SetSize(240, 90)
			self.AddFlag("movable")
			self.AddFlag("float")

			myBankBoard = ui.BoardWithTitleBar()
			myBankBoard.SetParent(self)
			myBankBoard.AddFlag("attach")
			myBankBoard.SetSize(220, 90)
			myBankBoard.SetTitleName("Banca")
			myBankBoard.Show()
			self.Children.append(myBankBoard)

			moneySlotBar = ui.SlotBar()
			moneySlotBar.SetParent(myBankBoard)
			moneySlotBar.SetSize(110, 18)
			moneySlotBar.SetPosition(10, 35)
			moneySlotBar.Show()
			self.Children.append(moneySlotBar)

			moneyText = ui.TextLine()
			moneyText.SetParent(moneySlotBar)
			moneyText.SetPosition(2, 3)
			moneyText.SetText("0 Yang")
			moneyText.SetWindowHorizontalAlignRight()
			moneyText.SetHorizontalAlignRight()
			moneyText.Show()
			self.Children.append(moneyText)

			withdrawMoneyButton = ui.Button()
			withdrawMoneyButton.SetParent(myBankBoard)
			withdrawMoneyButton.SetPosition(125, 35)
			withdrawMoneyButton.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
			withdrawMoneyButton.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
			withdrawMoneyButton.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
			withdrawMoneyButton.SetText("Retrage Yang")
			withdrawMoneyButton.SetEvent(self.__WithdrawMoneyOrCheque, 0)
			withdrawMoneyButton.Show()
			self.Children.append(withdrawMoneyButton)

			chequeSlotBar = ui.SlotBar()
			chequeSlotBar.SetParent(myBankBoard)
			chequeSlotBar.SetSize(110, 18)
			chequeSlotBar.SetPosition(10, 60)
			chequeSlotBar.Show()
			self.Children.append(chequeSlotBar)

			chequeText = ui.TextLine()
			chequeText.SetParent(chequeSlotBar)
			chequeText.SetPosition(2, 3)
			chequeText.SetText("0 Won")
			chequeText.SetWindowHorizontalAlignRight()
			chequeText.SetHorizontalAlignRight()
			chequeText.Show()
			self.Children.append(chequeText)

			withdrawChequeButton = ui.Button()
			withdrawChequeButton.SetParent(myBankBoard)
			withdrawChequeButton.SetPosition(125, 60)
			withdrawChequeButton.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
			withdrawChequeButton.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
			withdrawChequeButton.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
			withdrawChequeButton.SetText("Retrage Won")
			withdrawChequeButton.SetEvent(self.__WithdrawMoneyOrCheque, 1)
			withdrawChequeButton.Show()
			self.Children.append(withdrawChequeButton)

		def Open(self):
			net.SendRefreshOfflineShopMoney()

			currentMoney = player.GetCurrentOfflineShopMoney()
			currentCheque = player.GetCurrentOfflineShopCheque()

			self.SetMoney(currentMoney)
			self.SetCheque(currentCheque)

			self.SetCenterPosition()
			ui.ScriptWindow.Show(self)

		def Close(self):
			ui.ScriptWindow.Hide(self)
			return TRUE

		def OnPressEscapeKey(self):
			self.Close()
			return TRUE

		def SetMoney(self, money):
			try:
				self.Children[2].SetText(localeInfo.NumberToMoneyString(money))
			except:
				pass

		def SetCheque(self, cheque):
			try:
				self.Children[5].SetText(localeInfo.NumberToChequeString(cheque))
			except:
				pass

		def __WithdrawMoneyOrCheque(self, type):
			self.Close()
			net.SendRefreshOfflineShopMoney()
			withdrawQuestionDialog = uiCommon.QuestionDialogOfflineShopMoney()
			withdrawQuestionDialog.SetText(localeInfo.OFFLINE_SHOP_WITHDRAW_MONEY)

			if type == 0:
				currentMoney = player.GetCurrentOfflineShopMoney()
				withdrawQuestionDialog.SetText2("[Total: " + localeInfo.NumberToMoneyString(currentMoney) + "]")
			else:
				currentCheque = player.GetCurrentOfflineShopCheque()
				withdrawQuestionDialog.SetText2("[Total: " + localeInfo.NumberToChequeString(currentCheque) + "]")

			withdrawQuestionDialog.SetAcceptEvent(lambda arg = True: self.AnswerMyBankQuestion(arg, type))
			withdrawQuestionDialog.SetCancelEvent(lambda arg = False: self.AnswerMyBankQuestion(arg, type))
			withdrawQuestionDialog.Open()
			self.withdrawQuestionDialog = withdrawQuestionDialog

		def AnswerMyBankQuestion(self, flag, type):
			if flag:
				if type == 0:
					net.SendChatPacket("/withdraw_offline_shop_money")
				else:
					net.SendChatPacket("/withdraw_offline_shop_cheque")

			self.withdrawQuestionDialog.Close()
			self.withdrawQuestionDialog = None
			return True

class OfflineShopInputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.hour = 168
		self.pos = 0
		self.priceInputBoard = None
		self.interface = None
		self.LoadWindow()

		return

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/OfflineShopInputDialog.py")
		except:
			import exception
			exception.Abort("OfflineShopInputDialog.LoadWindow.LoadObject")

		try:
			self.titleBar = self.GetChild("TitleBar")
			self.offlineShopTime = self.GetChild("OfflineShopTime")
			self.bankButton = self.GetChild("BankButton")
			self.retrieveItemButton = self.GetChild("RetrieveItems")
			self.closeOfflineShopButton = self.GetChild("CloseOfflineShop")
			self.btnEditMode = self.GetChild("EditModeShopOffline")
			self.searchButton = self.GetChild("SearchButton")
			self.acceptButton = self.GetChild("AgreeButton")
			self.inputValue = self.GetChild("InputValue")
			self.timeInputValue = self.GetChild("TimeInputValue")
##			self.itemSlot = self.GetChild("ItemSlot")
##			self.watchButton = self.GetChild("WatchButton")
		except:
			import exception
			exception.Abort("OfflineShopInputDialog.LoadWindow.BindObject")

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.offlineShopTime.SetSliderPos(1.0)
		self.offlineShopTime.SetEvent(ui.__mem_func__(self.OnChangeOfflineShopTime))
		self.bankButton.SetEvent(ui.__mem_func__(self.ClickMyBankButton))
		self.retrieveItemButton.SetEvent(ui.__mem_func__(self.ClickRetrieveItem))
		self.closeOfflineShopButton.SetEvent(ui.__mem_func__(self.ClickCloseOfflineShopButton))
		self.btnEditMode.SetEvent(ui.__mem_func__(self.EventOfflineEdit))
		self.searchButton.SetEvent(ui.__mem_func__(self.ClickSearch))
##		self.itemSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.OnSelectEmptySlot))
##		self.watchButton.SetEvent(ui.__mem_func__(self.OnClickWatchButton))
##		self.textBoard = TextBoard()
##		self.textBoard.SetParent(self)
##		self.textBoard.SetPosition(11, 32)
##		self.textBoard.SetSize(528, 245)
##		self.textBoard.AddFlag("not_pick")
##		self.textBoard.Show()
##		self.RefreshText()

		net.SendRefreshOfflineShopMoney()

	def BindInterfaceClass(self, interface):
		self.interface = interface

	def EventOfflineEdit(self):
		if self.interface:
			self.interface.OpenOfflineShopEdit()
			net.SendChatPacket("/edit_shop_offline")

	def SplitDescription(self, desc, limit):
		total_tokens = desc.split()
		line_tokens = []
		line_len = 0
		lines = []
		for token in total_tokens:
			if "|" in token:
				sep_pos = token.find("|")
				line_tokens.append(token[:sep_pos])
				lines.append(" ".join(line_tokens))
				line_len = len(token) - (sep_pos + 1)
				line_tokens = [token[sep_pos + 1:]]
			else:
				line_len += len(token)
				if len(line_tokens) + line_len > limit:
					lines.append(" ".join(line_tokens))
					line_len = len(token)
					line_tokens = [token]
				else:
					line_tokens.append(token)

		if line_tokens:
			lines.append(" ".join(line_tokens))
		return lines

##	def RefreshText(self):
##		self.textBoard.Clear()
##		lines = self.SplitDescription("Market Tezg\xe2h\xfd sistemi sen oyunda olmasan da senin belirledi\xf0in s\xfcre boyunca nesnelerinin ticaretinin yap\xfdlmas\xfdn\xfd sa\xf0lar. Bu sistem sadece CH1 ve kendi birinci k\xf6y\xfcnde kullan\xfdlabilir. Oyundan \xe7\xfdkman tezg\xe2h\xfdn\xfd kapatmaz. Market Tezg\xe2h\xfdn\xfd kurabilmek i\xe7in en az 15. seviye ve 10K yang gerekir. Diledi\xf0in zaman Yang \xc7ek butonuna t\xfdklay\xfdp sat\xfdlan nesnelerinin paras\xfdn\xfd alabilirsin. Nesneleri Getir butonu tezg\xe2h\xfdn otomatik olarak kapand\xfd\xf0\xfd vakit giden itemlerini Market Tezg\xe2h\xfd depondan geri \xe7ekmek i\xe7in kullan\xfdl\xfdr. Market Tezg\xe2h\xfdn\xfd kurduktan sonra e\xf0er ekstra olarak nesne eklemek istersen, envanterinden itemi a\xfea\xf0\xfddaki bo\xfe slota s\xfcr\xfckleyip b\xfdrak ve fiyat\xfdn\xfd gir, sistem Market Tezg\xe2h\xfdnda en yak\xfdn bo\xfe yeri otomatik olarak bulup nesneni senin i\xe7in sat\xfd\xfea \xe7\xfdkaracakt\xfdr, unutma bu i\xfelemi yapabilmek i\xe7in Market Tezg\xe2h\xfdn\xfdn yan\xfdnda olman gerekiyor. Tezg\xe2ha Bak butonu ile kanal ya da harita fark etmeksizin Market Tezg\xe2h\xfdn\xfdn son durumunu g\xf6rebilirsin. [Yap\xfdm A\xfeamas\xfdnda] [A\xe7\xfdklama daha fazla geni\xfeletilecek.]", 94)
##		if not lines:
##			return
##		for line in lines:
##			self.textBoard.AppendTextLine(line)

	def OnSelectEmptySlot(self, selectedSlotPos):
		# chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINE_SHOP_UNAVAILABLE)
		try:
			if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
				return

			if (mouseModule.mouseController.isAttached()):
				attachedSlotType = mouseModule.mouseController.GetAttachedType()
				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				mouseModule.mouseController.DeattachObject()

				if (player.SLOT_TYPE_INVENTORY != attachedSlotType and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedSlotType and player.SLOT_TYPE_BOOK_INVENTORY != attachedSlotType and player.SLOT_TYPE_UPGRADE_INVENTORY != attachedSlotType and player.SLOT_TYPE_STONE_INVENTORY != attachedSlotType):
				# if player.SLOT_TYPE_BOOK_INVENTORY == attachedSlotType or player.SLOT_TYPE_UPGRADE_INVENTORY == attachedSlotType or player.SLOT_TYPE_STONE_INVENTORY == attachedSlotType or player.SLOT_TYPE_INVENTORY == attachedSlotType or player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType:
					return

				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				itemVnum = player.GetItemIndex(attachedInvenType, attachedSlotPos)
				item.SelectItem(itemVnum)

				if (item.IsAntiFlag(item.ANTIFLAG_GIVE) or item.IsAntiFlag(item.ANTIFLAG_MYSHOP)):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.PRIVATE_SHOP_CANNOT_SELL_ITEM)
					return

				priceInputBoard = uiCommon.MoneyInputDialog()
				priceInputBoard.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_PRICE_DIALOG_TITLE)
				priceInputBoard.SetAcceptEvent(lambda arg = True: self.InputPriceStatus(arg))
				priceInputBoard.SetCancelEvent(lambda arg = False: self.InputPriceStatus(arg))
				priceInputBoard.Open()

				self.priceInputBoard = priceInputBoard
				self.priceInputBoard.itemVNum = itemVnum
				self.priceInputBoard.bPos = attachedSlotPos

				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
		except Exception, e:
			import dbg
			dbg.TraceError("Exception : SelectEmptySlot, %s" %(e))

	def InputPriceStatus(self, flag):
		if not self.priceInputBoard:
			return True

		if flag:
			text = self.priceInputBoard.GetText()

			if not text or not text.isdigit() or int(text) <= 0:
				return True

			if app.ENABLE_CHEQUE_SYSTEM:
				cheText = self.priceInputBoard.GetChequeText()

				if not cheText or not cheText.isdigit() or int(cheText) < 0:
					return True

			price = int(self.priceInputBoard.GetText())

			if app.ENABLE_CHEQUE_SYSTEM:
				cheque = int(self.priceInputBoard.GetChequeText())

			if app.ENABLE_CHEQUE_SYSTEM:
				net.SendAddOfflineShopItemPacket(self.priceInputBoard.bPos, price, cheque)
			else:
				net.SendAddOfflineShopItemPacket(self.priceInputBoard.bPos, price)

			snd.PlaySound("sound/ui/drop.wav")
			self.priceInputBoard.Close()
			self.priceInputBoard = None
		else:
			self.priceInputBoard.Close()
			self.priceInputBoard = None

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
		return True

	def OnClickWatchButton(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINE_SHOP_UNAVAILABLE)
	
	def ClickSearch(self):
		if self.interface:
			self.interface.ShowShopSearch()
	
	def ClickCloseOfflineShopButton(self):
		# self.Close()
		net.SendRefreshOfflineShopMoney()
		closeQuestionDialog = uiCommon.QuestionDialog()
		closeQuestionDialog.SetText(localeInfo.OFFLINE_SHOP_CLOSE_OFFLINE_SHOP)
		closeQuestionDialog.SetAcceptEvent(lambda arg = True: self.AnswerCloseOfflineShop(arg))
		closeQuestionDialog.SetCancelEvent(lambda arg = False: self.AnswerCloseOfflineShop(arg))
		closeQuestionDialog.Open()
		self.closeQuestionDialog = closeQuestionDialog

	def AnswerCloseOfflineShop(self, flag):
		if flag:
			net.SendDestroyOfflineShop()
			shop.ClearOfflineShopStock()
			net.SendChatPacket("/destroy_my_offline_shop")
		self.closeQuestionDialog = None
		return True

	def ClickRetrieveItem(self):
		self.Close()
		retrieveQuestionDialog = uiCommon.QuestionDialog()
		retrieveQuestionDialog.SetText(localeInfo.OFFLINE_SHOP_RETRIEVE_ITEM)
		retrieveQuestionDialog.SetAcceptEvent(lambda arg = True: self.AnswerRetieveItemQuestion(arg))
		retrieveQuestionDialog.SetCancelEvent(lambda arg = False: self.AnswerRetieveItemQuestion(arg))
		retrieveQuestionDialog.Open()
		self.retrieveQuestionDialog = retrieveQuestionDialog

	def AnswerRetieveItemQuestion(self, flag):
		if flag:
			net.SendChatPacket("/retrieve_offline_shop_item")
		self.retrieveQuestionDialog = None
		return True

	def ClickMyBankButton(self):
		self.Close()
		if not app.ENABLE_CHEQUE_SYSTEM:
			net.SendRefreshOfflineShopMoney()
			currentMoney = player.GetCurrentOfflineShopMoney()
			withdrawQuestionDialog = uiCommon.QuestionDialogOfflineShopMoney()
			withdrawQuestionDialog.SetText(localeInfo.OFFLINE_SHOP_WITHDRAW_MONEY)
			withdrawQuestionDialog.SetText2("[Total: " + localeInfo.NumberToMoneyString(currentMoney) + "]")
			withdrawQuestionDialog.SetAcceptEvent(lambda arg = True: self.AnswerMyBankQuestion(arg))
			withdrawQuestionDialog.SetCancelEvent(lambda arg = False: self.AnswerMyBankQuestion(arg))
			withdrawQuestionDialog.Open()
			self.withdrawQuestionDialog = withdrawQuestionDialog
		else:
			self.withdrawQuestionDialog = myBankWindow()
			self.withdrawQuestionDialog.Open()

	if not app.ENABLE_CHEQUE_SYSTEM:
		def AnswerMyBankQuestion(self, flag):
			if flag:
				net.SendChatPacket("/withdraw_offline_shop_money")
			self.withdrawQuestionDialog = None
			return True

	def OnChangeOfflineShopTime(self):
		self.pos = self.offlineShopTime.GetSliderPos() * 168 / 1
		conv = str(int(self.pos))

		#if str(0) == conv:
		#	self.offlineShopTime.SetSliderPos(1.0)
		#	self.timeInputValue.SetText("168 Hours")
		#	self.hour = 168
		#	return True

		self.timeInputValue.SetText(conv + " Ore")
		self.hour = self.pos

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def OnPressExitKey(self):
		self.Close()
		return True

	def Close(self):
		self.ClearDictionary()
		self.acceptButton = None
		self.inputValue = None
		self.priceInputBoard = None
		self.Hide()
		return

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.inputValue.OnPressEscapeKey = event

	def GetTitle(self):
		return self.inputValue.GetText()

	def GetTime(self):
		return self.hour

class OfflineShopDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.CurrentShopVID = 0
		self.tooltipItem = 0
		self.questionDialog = None
		self.popup = None
		self.itemBuyQuestionDialog = None
		return

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Refresh(self):
		for i in xrange(shop.OFFLINE_SHOP_SLOT_COUNT):
			itemCount = shop.GetOfflineShopItemCount(i)
			if itemCount <= 1:
				itemCount = 0

			self.itemSlotWindow.SetItemSlot(i, shop.GetOfflineShopItemID(i), itemCount)

			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = shop.GetOfflineShopItemTransmutation(i)
				if itemTransmutedVnum:
					self.itemSlotWindow.DisableCoverButton(i)
				else:
					self.itemSlotWindow.EnableCoverButton(i)

			status, who = shop.GetOfflineShopItemStatus(i)
			if status:
				self.itemSlotWindow.ActivateOfflineShopSlot(i)
			else:
				self.itemSlotWindow.DeactivateOfflineShopSlot(i)

		wndMgr.RefreshSlot(self.itemSlotWindow.GetWindowHandle())

		self.wndDisplayedCount.SetText(localeInfo.NumberToDisplayedCount(shop.GetDisplayedCount()))
		self.wndDisplayedCount.SetToolTipText("Il tuo shop e' stato visitato " + localeInfo.NumberToString(shop.GetDisplayedCount()) + " volte.")
		wndMgr.RefreshSlot(self.itemSlotWindow.GetWindowHandle())

	def LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/OfflineShopDialog.py")
		except:
			import exception
			exception.Abort("OfflineShopDialog.LoadDialog.LoadObject")

		try:
			self.itemSlotWindow = self.GetChild("ItemSlot")
			self.btnBuy = self.GetChild("BuyButton")
			self.btnDestroy = self.GetChild("DestroyButton")
			self.titleBar = self.GetChild("TitleBar")
			self.titleName = self.GetChild("TitleName")
			self.wndDisplayedCount = self.GetChild("DisplayedCount")
		except:
			import exception
			exception.Abort("OfflineShopDialog.LoadDialog.BindObject")

		self.itemSlotWindow.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		self.itemSlotWindow.SAFE_SetButtonEvent("LEFT", "EXIST", self.SelectItemSlot)
		self.itemSlotWindow.SAFE_SetButtonEvent("RIGHT", "EXIST", self.UnselectItemSlot)
		self.itemSlotWindow.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.itemSlotWindow.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.btnBuy.SetToggleUpEvent(ui.__mem_func__(self.CancelShopping))
		self.btnBuy.SetToggleDownEvent(ui.__mem_func__(self.OnBuy))

		if player.GetName().find("[") != -1:
			self.btnDestroy.SetEvent(ui.__mem_func__(self.OnDestroyOfflineShop))
			self.wndDisplayedCount.SetPosition(150, 295)
		else:
			self.btnDestroy.Hide()
			self.wndDisplayedCount.SetPosition(80, 295)
	
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.Refresh()

	def OnDestroyOfflineShop(self):
		net.SendChatPacket("/destroy_offline_shop " + str(self.CurrentShopVID))

	def Destroy(self):
		self.Close()
		self.ClearDictionary()
		self.CurrentShopVID = 0
		self.tooltipItem = 0
		self.itemSlotWindow = 0
		self.btnBuy = 0
		self.titleBar = 0
		self.questionDialog = None
		self.popup = None
		return

	def Open(self, vid):
		shop.Open(False, False, True)
		self.SetCenterPosition()
		self.SetTop()
		self.Refresh()
		self.Show()
		self.CurrentShopVID = vid
		self.titleName.SetText(chr.GetNameByVID(vid))

	def Open(self, vid):
		shop.Open(False, False, True)
		self.SetCenterPosition()
		self.SetTop()
		self.Refresh()
		self.Show()
		self.CurrentShopVID = vid
		self.titleName.SetText(chr.GetNameByVID(vid))

	def Close(self):
		if self.itemBuyQuestionDialog:
			self.itemBuyQuestionDialog.Close()
			self.itemBuyQuestionDialog = None

		if self.questionDialog:
			self.OnCloseQuestionDialog()

		shop.Close()
		net.SendOfflineShopEndPacket()
		self.CancelShopping()
		self.tooltipItem.HideToolTip()
		self.Hide()
		return

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnPressExitKey(self):
		self.Close()
		return True

	def OnBuy(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINE_SHOP_WARNING_1)
		app.SetCursor(app.BUY)

	def CancelShopping(self):
		self.btnBuy.SetUp()
		app.SetCursor(app.NORMAL)

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return
		else:
			self.questionDialog.Close()
			self.questionDialog = None
			return

	def UnselectItemSlot(self, selectedSlotPos):
		self.AskBuyItem(selectedSlotPos)

	def SelectItemSlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if not isAttached:
			curCursorNum = app.GetCursor()

			if app.BUY == curCursorNum:
				net.SendOfflineShopBuyPacket(selectedSlotPos)
			else:
				selectedItemID = shop.GetOfflineShopItemID(selectedSlotPos)
				itemCount = shop.GetOfflineShopItemCount(selectedSlotPos)
				type = player.SLOT_TYPE_OFFLINE_SHOP
				mouseModule.mouseController.AttachObject(self, type, selectedSlotPos, selectedItemID, itemCount)
				mouseModule.mouseController.SetCallBack("INVENTORY", ui.__mem_func__(self.DropToInventory))
				snd.PlaySound("sound/ui/pick.wav")

	def DropToInventory(self):
		attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
		self.AskBuyItem(attachedSlotPos)

	def AskBuyItem(self, slotPos):
		itemIndex = shop.GetOfflineShopItemID(slotPos)
		itemPrice = shop.GetOfflineShopItemPrice(slotPos)
		if app.ENABLE_CHEQUE_SYSTEM:
			itemCheque = shop.GetOfflineShopItemCheque(slotPos)
		itemCount = shop.GetOfflineShopItemCount(slotPos)

		item.SelectItem(itemIndex)
		itemName = item.GetItemName()

		itemBuyQuestionDialog = uiCommon.QuestionDialog()

		if app.ENABLE_CHEQUE_SYSTEM:
			itemBuyQuestionDialog.SetText(localeInfo.DO_YOU_BUY_ITEM_NEW(itemName, itemCount, localeInfo.NumberToMoney(itemPrice), localeInfo.NumberToChequeString(itemCheque)))
		else:
			itemBuyQuestionDialog.SetText(localeInfo.DO_YOU_BUY_ITEM(itemName, itemCount, localeInfo.NumberToMoneyString(itemPrice)))

		itemBuyQuestionDialog.SetAcceptEvent(lambda arg = True: self.AnswerBuyItem(arg))
		itemBuyQuestionDialog.SetCancelEvent(lambda arg = False: self.AnswerBuyItem(arg))
		itemBuyQuestionDialog.Open()

		itemBuyQuestionDialog.pos = slotPos
		self.itemBuyQuestionDialog = itemBuyQuestionDialog

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def AnswerBuyItem(self, flag):
		if flag:
			pos = self.itemBuyQuestionDialog.pos
			net.SendOfflineShopBuyPacket(pos)
	
		self.itemBuyQuestionDialog.Close()
		self.itemBuyQuestionDialog = None

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
		return

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def OverInItem(self, slotIndex):
		if mouseModule.mouseController.isAttached():
			return
		if self.tooltipItem != 0:
			self.tooltipItem.SetOfflineShopItem(slotIndex)

	def OverOutItem(self):
		if self.tooltipItem != 0:
			self.tooltipItem.HideToolTip()


class OfflineShopEditMode(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.CurrentShopVID = 0
		self.tooltipItem = 0
		self.questionDialog = None
		self.popup = None
		self.AddItemInputBoard = None
		self.PriceQuestionDialog = None
		self.itemBuyQuestionDialog = None
		self.interface = None
		self.RemainTime = 0
		return

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Refresh(self):
		for i in xrange(shop.OFFLINE_SHOP_SLOT_COUNT):
			self.itemSlotWindow.ClearSlot(i)
		
			itemCount = shop.GetOfflineShopItemCount(i)
			if itemCount <= 1:
				itemCount = 0
				
			if shop.GetOfflineShopItemID(i) <= 0:
				continue

			self.itemSlotWindow.SetItemSlot(i, shop.GetOfflineShopItemID(i), itemCount)

			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = shop.GetOfflineShopItemTransmutation(i)
				if itemTransmutedVnum:
					self.itemSlotWindow.DisableCoverButton(i)
				else:
					self.itemSlotWindow.EnableCoverButton(i)

			status, who = shop.GetOfflineShopItemStatus(i)
			if status:
				self.itemSlotWindow.ActivateOfflineShopSlot(i)
			else:
				self.itemSlotWindow.DeactivateOfflineShopSlot(i)

		# wndMgr.RefreshSlot(self.itemSlotWindow.GetWindowHandle())
		self.itemSlotWindow.RefreshSlot()

	def LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/OfflineShopEditDialog.py")
		except:
			import exception
			exception.Abort("OfflineShopEditDialog.LoadDialog.LoadObject")

		try:
			self.itemSlotWindow = self.GetChild("ItemSlot")
			self.titleBar = self.GetChild("TitleBar")
			self.titleName = self.GetChild("TitleName")
			self.wndTimeRemain = self.GetChild("TimeLeft")
			self.wndLocation = self.GetChild("LocationText")
		except:
			import exception
			exception.Abort("OfflineShopEditDialog.LoadDialog.BindObject")

		# self.itemSlotWindow.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		self.itemSlotWindow.SetSelectEmptySlotEvent(ui.__mem_func__(self.OnSelectEmptySlot))
		# self.itemSlotWindow.SAFE_SetButtonEvent("LEFT", "EXIST", self.SelectItemSlot)
		# self.itemSlotWindow.SAFE_SetButtonEvent("RIGHT", "EXIST", self.UnselectItemSlot)
		self.itemSlotWindow.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		self.itemSlotWindow.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.itemSlotWindow.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

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

			AddItemInputBoard = uiCommon.MoneyInputDialog()
			AddItemInputBoard.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_PRICE_DIALOG_TITLE)
			AddItemInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrice))
			AddItemInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrice))
			AddItemInputBoard.Open()

			# itemPrice=GetPrivateShopItemPrice(itemVNum)
			# if app.ENABLE_CHEQUE_SYSTEM:
				# itemCheque=GetPrivateShopItemCheque(itemVNum)

			# if itemPrice>0:
				# AddItemInputBoard.SetValue(itemPrice)
			
			# if app.ENABLE_CHEQUE_SYSTEM and itemCheque > 0:
				# AddItemInputBoard.SetChequeValue(itemCheque)
			AddItemInputBoard.SetFocus()
			
			self.AddItemInputBoard = AddItemInputBoard
			self.AddItemInputBoard.itemVNum = itemVNum
			self.AddItemInputBoard.sourceWindowType = attachedInvenType
			self.AddItemInputBoard.sourceSlotPos = attachedSlotPos
			self.AddItemInputBoard.targetSlotPos = selectedSlotPos

	def AcceptInputPrice(self):

		if not self.AddItemInputBoard:
			return True

		text = self.AddItemInputBoard.GetText()

		if app.ENABLE_CHEQUE_SYSTEM:
			cheText = self.AddItemInputBoard.GetChequeText()
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

		attachedInvenType = self.AddItemInputBoard.sourceWindowType
		sourceSlotPos = self.AddItemInputBoard.sourceSlotPos
		targetSlotPos = self.AddItemInputBoard.targetSlotPos

		price = int(self.AddItemInputBoard.GetText())
		cheque = int(self.AddItemInputBoard.GetChequeText())
		
		net.SendChatPacket("/offline_add_item %d|%d|%d|%d|%d" % (attachedInvenType, sourceSlotPos, targetSlotPos, price, cheque))

		self.Refresh()
		#####
		self.AddItemInputBoard = None
		return True

	def CancelInputPrice(self):
		if self.AddItemInputBoard:
			self.AddItemInputBoard.Close()
		self.AddItemInputBoard = None
		return True

	def OnDestroyOfflineShop(self):
		net.SendChatPacket("/destroy_offline_shop " + str(self.CurrentShopVID))

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()
		self.CurrentShopVID = 0
		self.tooltipItem = 0
		self.itemSlotWindow = 0
		self.btnBuy = 0
		self.titleBar = 0
		self.questionDialog = None
		self.popup = None
		return

	def OnUpdate(self):
		if self.RemainTime > 0:
			self.wndTimeRemain.SetText("Timp ramas: " + localeInfo.SecondToDHM(self.RemainTime))

	def Open(self, vid, remain, map_index, x, y):
		self.Refresh()
		self.CurrentShopVID = vid
		self.RemainTime = remain
		self.titleName.SetText(chr.GetNameByVID(vid))
		self.wndLocation.SetText("Oraº: " + str(x) + " " + str(y))
		
		shop.Close()
		net.SendOfflineShopEndPacket()

		if not self.IsShow():
			self.Show()

	def SetOpen(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Refresh()
		# self.Show()

	def Close(self):
		if self.PriceQuestionDialog:
			self.PriceQuestionDialog.Close()
			self.PriceQuestionDialog = None
			
		if self.AddItemInputBoard:
			self.AddItemInputBoard.Close()
			self.AddItemInputBoard = None
			
		if self.itemBuyQuestionDialog:
			self.itemBuyQuestionDialog.Close()
			self.itemBuyQuestionDialog = None

		if self.questionDialog:
			self.OnCloseQuestionDialog()

		
		net.SendChatPacket("/close_edit_mode")
		self.tooltipItem.HideToolTip()
		self.Hide()
		return

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnPressExitKey(self):
		self.Close()
		return True

	def OnBuy(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINE_SHOP_WARNING_1)
		app.SetCursor(app.BUY)

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return
		else:
			self.questionDialog.Close()
			self.questionDialog = None
			return

	def UnselectItemSlot(self, selectedSlotPos):
		self.AskEditItem(selectedSlotPos)

	def SelectItemSlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			mouseModule.mouseController.DeattachObject()
			return

		self.AskEditItem(selectedSlotPos)

	def DropToInventory(self):
		self.AskEditItem(attachedSlotPos)

	def AskEditItem(self, slotPos):
		itemIndex = shop.GetOfflineShopItemID(slotPos)
		itemPrice = shop.GetOfflineShopItemPrice(slotPos)
		if app.ENABLE_CHEQUE_SYSTEM:
			itemCheque = shop.GetOfflineShopItemCheque(slotPos)
		itemCount = shop.GetOfflineShopItemCount(slotPos)

		item.SelectItem(itemIndex)
		itemName = item.GetItemName()

		itemBuyQuestionDialog = uiCommon.QuestionDialog()
		itemBuyQuestionDialog.SetWidth(165)
		itemBuyQuestionDialog.SetText("Alegeþi o optiune")
		itemBuyQuestionDialog.SetAcceptText("Editaþi pret")
		itemBuyQuestionDialog.SetCancelText("Inlaturã Item")

		itemBuyQuestionDialog.SetAcceptEvent(lambda arg = True: self.AnswerEditItem(arg))
		itemBuyQuestionDialog.SetCancelEvent(lambda arg = False: self.AnswerEditItem(arg))
		itemBuyQuestionDialog.Open()

		itemBuyQuestionDialog.pos = slotPos
		self.itemBuyQuestionDialog = itemBuyQuestionDialog

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def AnswerEditItem(self, flag):
		pos = self.itemBuyQuestionDialog.pos
		
		if flag:
			self.EditPriceItem(pos)
		else:
			net.SendChatPacket("/delete_item %d" % (pos))
	
		self.itemBuyQuestionDialog.Close()
		self.itemBuyQuestionDialog = None

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
		shop.Close()
		net.SendOfflineShopEndPacket()
		
		net.SendChatPacket("/edit_shop_offline")
		self.Refresh()
		return

	def EditPriceItem(self, pos):
		if self.PriceQuestionDialog:
			return
	
		PriceQuestionDialog = uiCommon.MoneyInputDialog()
		PriceQuestionDialog.SetTitle("Alegeþi suma!")
		#Set money default 
		itemPrice = shop.GetOfflineShopItemPrice(pos)
		itemCheque = shop.GetOfflineShopItemCheque(pos)
		PriceQuestionDialog.SetValue(itemPrice)
		PriceQuestionDialog.SetChequeValue(itemCheque)
		#Set money default 
		PriceQuestionDialog.SetMoneyHeaderText("Yang: ")
		PriceQuestionDialog.SetAcceptEvent(lambda arg = True, pos2 = pos: self.SumEdit(arg, pos2))
		PriceQuestionDialog.SetCancelEvent(lambda arg = False, pos2 = pos: self.SumEdit(arg, pos2))
		PriceQuestionDialog.Open()
		self.PriceQuestionDialog = PriceQuestionDialog

	def SumEdit(self, flag, pos):
		if not self.PriceQuestionDialog:
			return
			
		Yang = self.PriceQuestionDialog.GetText()
		Cheque = self.PriceQuestionDialog.GetChequeText()
		
		if flag:

			if Yang <= 0:
				self.PriceQuestionDialog.Close()
				self.PriceQuestionDialog = None			
				return
			
			net.SendChatPacket("/price_item %d %d %d" % (pos, int(Yang), int(Cheque)))
			
		shop.Close()
		net.SendOfflineShopEndPacket()
		
		net.SendChatPacket("/edit_shop_offline")
			
		self.PriceQuestionDialog.Close()
		self.PriceQuestionDialog = None		

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def OverInItem(self, slotIndex):
		if mouseModule.mouseController.isAttached():
			return
		if self.tooltipItem != 0:
			self.tooltipItem.SetOfflineShopItem(slotIndex)

	def OverOutItem(self):
		if self.tooltipItem != 0:
			self.tooltipItem.HideToolTip()
