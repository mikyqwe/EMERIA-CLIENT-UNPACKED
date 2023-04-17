import ui
import localeInfo
import app
import ime
import uiScriptLocale
import net
import item
import player
import constInfo

class PopupDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.acceptEvent = lambda *arg: None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/PopupDialog.py")

			self.board = self.GetChild("board")
			self.message = self.GetChild("message")
			self.accceptButton = self.GetChild("accept")
			self.accceptButton.SetEvent(ui.__mem_func__(self.Close))

		except:
			import exception
			exception.Abort("PopupDialog.LoadDialog.BindObject")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()
		self.acceptEvent()

	def Destroy(self):
		self.Close()
		self.ClearDictionary()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SetText(self, text):
		self.message.SetText(text)

	def SetAcceptEvent(self, event):
		self.acceptEvent = event

	def SetButtonName(self, name):
		self.accceptButton.SetText(name)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True

class InputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialog.py")

		getObject = self.GetChild
		self.board = getObject("Board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputSlot = getObject("InputSlot")
		self.inputValue = getObject("InputValue")

	def Open(self):
		self.inputValue.SetFocus()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputSlot = None
		self.inputValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetNumberMode(self):
		self.inputValue.SetNumberMode()

	def SetSecretMode(self):
		self.inputValue.SetSecret()

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		width = length * 6 + 10
		self.SetBoardWidth(max(width + 50, 160))
		self.SetSlotWidth(width)
		self.inputValue.SetMax(length)

	def SetSlotWidth(self, width):
		self.inputSlot.SetSize(width, self.inputSlot.GetHeight())
		self.inputValue.SetSize(width, self.inputValue.GetHeight())
		if self.IsRTL():
			self.inputValue.SetPosition(self.inputValue.GetWidth(), 0)

	def SetBoardWidth(self, width):
		self.SetSize(max(width + 50, 160), self.GetHeight())
		self.board.SetSize(max(width + 50, 160), self.GetHeight())
		if self.IsRTL():
			self.board.SetPosition(self.board.GetWidth(), 0)
		self.UpdateRect()

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def GetText(self):
		return self.inputValue.GetText()

class InputDialogWithDescription(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		if localeInfo.IsARABIC() :
			pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "inputdialogwithdescription.py")
		else:
			pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription.py")

		try:
			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = getObject("InputSlot")
			self.inputValue = getObject("InputValue")
			self.description = getObject("Description")

		except:
			import exception
			exception.Abort("InputDialogWithDescription.LoadBoardDialog.BindObject")

	def SetDescription(self, text):
		self.description.SetText(text)

class InputDialogWithDescription2(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription2.py")

		try:
			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = getObject("InputSlot")
			self.inputValue = getObject("InputValue")
			self.description1 = getObject("Description1")
			self.description2 = getObject("Description2")

		except:
			import exception
			exception.Abort("InputDialogWithDescription.LoadBoardDialog.BindObject")

	def SetDescription1(self, text):
		self.description1.SetText(text)

	def SetDescription2(self, text):
		self.description2.SetText(text)

class QuestionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog.py")

		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		constInfo.DROP_GUI_CHECK = 0
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
		self.Hide()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SAFE_SetAcceptEvent(self, event):
		self.acceptButton.SAFE_SetEvent(event)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def OnPressEscapeKey(self):
		self.Close()
		return True

class QuestionDialog2(QuestionDialog):

	def __init__(self):
		QuestionDialog.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		QuestionDialog.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def SetText1(self, text):
		self.textLine1.SetText(text)

	def SetText2(self, text):
		self.textLine2.SetText(text)

class QuestionDialogItemNew(ui.ScriptWindow):
	def __init__(self, tooltip):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = tooltip
		self.state = 0
		self.__CreateDialog()
	def __del__(self):
		ui.ScriptWindow.__del__(self)
	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialogitemnew.py")
		self.board = self.GetChild("board")
		self.dropButton = self.GetChild("drop")
		self.destroyButton = self.GetChild("destroy")
		self.sellButton = self.GetChild("sell")
		self.ItemImage = self.GetChild("Item")
		#self.ItemImage.SAFE_SetStringEvent("MOUSE_OVER_IN",self.ShowTooltip)
		#self.ItemImage.SAFE_SetStringEvent("MOUSE_OVER_OUT",self.HideTooltip)
		self.ItemName = self.GetChild("ItemName")
		self.cancelButton = self.GetChild("cancel")
		self.GetChild("TitleBar").SetCloseEvent(self.Close)

		self.dropButton.SAFE_SetEvent(self.DropItem)
		self.destroyButton.SetEvent(self.DestroyItem)
		self.sellButton.SetEvent(self.SellItem)
		self.cancelButton.SetEvent(self.Close)

		self.Input = QuestionDialog()
		self.Input.Hide()

	def ConfirmCancel(self):
		self.state=0
		self.Input.Hide()

	def ConfirmAccept(self):
		self.Input.Hide()
		if self.state == 1:
			net.SendChatPacket("/qitem %d %d %d"%(2,self.dropType, self.dropNumber))
			self.Close()
		elif self.state == 2:
			net.SendChatPacket("/qitem %d %d %d"%(1,self.dropType, self.dropNumber))
			self.Close()

	def ShowTooltip(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetInventoryItem(self.dropNumber,self.dropType)
	def HideTooltip(self):
		if None != self.tooltipItem:
			self.tooltipItem.ClearToolTip()
			self.tooltipItem.Hide()

	def DropItem(self):
		net.SendItemDropPacketNew(self.dropType, self.dropNumber, self.dropCount)
		self.Input.Hide()
		self.Close()

	def DestroyItem(self):
		self.state=2
		itemVnum = player.GetItemIndex(self.dropType, self.dropNumber)
		item.SelectItem(itemVnum)
		self.Input.SetText("Sei sicuro di voler distruggere %s ?"%(item.GetItemName()))
		self.Input.SetAcceptEvent(ui.__mem_func__(self.ConfirmAccept))
		self.Input.SetCancelEvent(ui.__mem_func__(self.ConfirmCancel))
		self.Input.SetTop()
		self.Input.Show()

	def SellItem(self):
		self.state=1

		itemVnum = player.GetItemIndex(self.dropType, self.dropNumber)
		item.SelectItem(itemVnum)
		self.Input.SetText("Sei sicuro di voler vendere %s ? - Prezzo: %s Yang"%(item.GetItemName(), localeInfo.NumberToString(item.GetISellItemPrice()*self.dropCount)))
		self.Input.SetAcceptEvent(ui.__mem_func__(self.ConfirmAccept))
		self.Input.SetCancelEvent(ui.__mem_func__(self.ConfirmCancel))
		self.Input.SetTop()
		self.Input.Show()

	def Open(self):
		itemVnum = player.GetItemIndex(self.dropType, self.dropNumber)
		item.SelectItem(itemVnum)
		self.ItemImage.LoadImage(item.GetIconImageFileName())
		self.ItemName.SetText("x%d %s"%(self.dropCount,item.GetItemName()))
		self.SetCenterPosition()
		self.SetTop()
		self.Show()
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def Close(self):
		constInfo.DROP_GUI_CHECK = 0
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
		self.Hide()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def OnPressEscapeKey(self):
		self.Close()
		return True


class QuestionDialogWithTimeLimit(QuestionDialog2):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()
		self.endTime = 0

	def __del__(self):
		QuestionDialog2.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self, msg, timeout):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

		self.SetText1(msg)
		self.endTime = app.GetTime() + timeout

	def OnUpdate(self):
		leftTime = max(0, self.endTime - app.GetTime())
		self.SetText2(localeInfo.UI_LEFT_TIME % (leftTime))

class MoneyInputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.moneyHeaderText = localeInfo.MONEY_INPUT_DIALOG_SELLPRICE
		self.__CreateDialog()
		self.SetMaxLength(9)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/moneyinputdialog.py")

		getObject = self.GetChild
		self.board = self.GetChild("board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputValue = getObject("InputValue")
		self.inputValue.SetNumberMode()
		self.inputValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
		self.moneyText = getObject("MoneyValue")

	def Open(self):
		self.inputValue.SetText("")
		self.inputValue.SetFocus()
		self.__OnValueUpdate()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		length = min(9, length)
		self.inputValue.SetMax(length)

	def SetMoneyHeaderText(self, text):
		self.moneyHeaderText = text

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def SetValue(self, value):
		value=str(value)
		self.inputValue.SetText(value)
		self.__OnValueUpdate()
		ime.SetCursorPosition(len(value))


	def GetText(self):
		return self.inputValue.GetText()

	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.inputValue)

		text = self.inputValue.GetText()

		money = 0
		if text and text.isdigit():
			try:
				money = int(text)
			except ValueError:
				money = 199999999

		self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(money))
		
if app.__ENABLE_NEW_OFFLINESHOP__:
	import wndMgr

	class MoneyInputDialogNew(ui.ScriptWindow):
		PATH_ROOT = "cream/shopseller/"
		
		def __init__(self, ItemVnum):
			ui.ScriptWindow.__init__(self)

			self.moneyHeaderText = localeInfo.MONEY_INPUT_DIALOG_SELLPRICE
			self.__CreateDialog(ItemVnum)
			self.SetMaxLength(13)
			self.SetCenterPosition()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def __CreateDialog(self, ItemVnum):

			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/moneyinputdialog.py")

			getObject = self.GetChild
			self.board = self.GetChild("board")
			self.board.Hide()
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputValue = getObject("InputValue")
			self.inputValue.SetNumberMode()
			self.inputValue.SetText("0")

			self.inputValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
			self.inputValue.OnPressEscapeKey = ui.__mem_func__(self.OnPressEscapeKey)
			self.moneyText = getObject("MoneyValue")
			
			self.__OnValueUpdate()

			self.board = ui.ExpandedImageBox()
			self.board.SetParent(self)
			self.board.AddFlag("not_pick")
			self.board.LoadImage(self.PATH_ROOT + "bg.tga")
			self.board.Show()

			self.acceptButton = ui.MakeButton(self, 25, 280, False, self.PATH_ROOT, "btn_norm.dds", "btn_hover.dds", "btn_down.dds")
			self.acceptButton.SetText("OK")

			self.cancelButton = ui.MakeButton(self, 125, 280, False, self.PATH_ROOT, "btn_norm.dds", "btn_hover.dds", "btn_down.dds")
			self.cancelButton.SetText("Close")
			
			self.boardItem = ui.ExpandedImageBox()
			self.boardItem.SetParent(self)
			self.boardItem.SetPosition(0, 140)
			self.boardItem.AddFlag("not_pick")
			self.boardItem.LoadImage(self.PATH_ROOT + "bg_item.dds")
			self.boardItem.SetWindowHorizontalAlignCenter()
			self.boardItem.Show()
			
			import item

			item.SelectItem(ItemVnum)

			self.ItemIcon = ui.ExpandedImageBox()
			self.ItemIcon.SetParent(self.boardItem)
			self.ItemIcon.SetPosition(0, 0)
			self.ItemIcon.LoadImage(item.GetIconImageFileName())
			self.ItemIcon.SetWindowHorizontalAlignCenter()
			self.ItemIcon.SetWindowVerticalAlignCenter()
			self.ItemIcon.Show()

			self.boardYang = ui.ExpandedImageBox()
			self.boardYang.SetParent(self)
			self.boardYang.SetPosition(25, 80)
			self.boardYang.LoadImage(self.PATH_ROOT + "price.dds")
			self.boardYang.Show()
			
			self.inputValue.SetParent(self.boardYang)
			self.inputValue.SetPosition(29, 8)
		
			self.wndNameItem = ui.MakeTextLineNew(self, 0, 120, item.GetItemName())
			self.wndNameItem.SetWindowHorizontalAlignCenter()
			self.wndNameItem.SetHorizontalAlignCenter()
			
			self.wndNameLine1 = ui.MakeTextLineNew(self, 0, 23, "For how much Yang")
			self.wndNameLine1.SetWindowHorizontalAlignCenter()
			self.wndNameLine1.SetHorizontalAlignCenter()

			self.wndNameLine2 = ui.MakeTextLineNew(self, 0, 40, "you want to sell this item?")
			self.wndNameLine2.SetWindowHorizontalAlignCenter()
			self.wndNameLine2.SetHorizontalAlignCenter()

			self.moneyText.SetParent(self)
			self.moneyText.SetPosition(0, 257)
			self.moneyText.SetWindowHorizontalAlignCenter()
			self.moneyText.SetHorizontalAlignCenter()

			self.SetSize(self.board.GetWidth(), self.board.GetHeight())

		def OnPressEscapeKey(self):
			self.Close()
			return True

		def Open(self):
			self.inputValue.SetText("")
			self.inputValue.SetFocus()
			self.__OnValueUpdate()
			self.SetCenterPosition()
			self.SetTop()
			self.Show()

		def Close(self):
			self.ClearDictionary()
			self.board = None
			self.acceptButton = None
			self.cancelButton = None
			self.inputValue = None
			self.Hide()

		def SetTitle(self, name):
			pass
			# self.board.SetTitleName(name)

		def SetFocus(self):
			self.inputValue.SetFocus()

		def SetMaxLength(self, length):
			length = min(13, length)
			self.inputValue.SetMax(length)

		def SetMoneyHeaderText(self, text):
			self.moneyHeaderText = text

		def SetAcceptEvent(self, event):
			self.acceptButton.SetEvent(event)
			self.inputValue.OnIMEReturn = event

		def SetCancelEvent(self, event):
			# self.board.SetCloseEvent(event)
			self.cancelButton.SetEvent(event)
			self.inputValue.OnPressEscapeKey = event

		def SetValue(self, value):
			value=str(value)
			self.inputValue.SetText(value)
			self.__OnValueUpdate()
			ime.SetCursorPosition(len(value))


		def GetText(self):
			return self.inputValue.GetText()

		def __OnValueUpdate(self):
			ui.EditLine.OnIMEUpdate(self.inputValue)

			text = self.inputValue.GetText()
			countK = text.count('x')
			if countK <= 3:
				text = text.replace('k', '000')
			money = 0
			if text and text.isdigit():
				try:
					money = min(9999999999999, long(text))
				except ValueError:
					money = 199999999
			
			self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(money))

	
	class ShopOfflinePopup(ui.Board):
		def __init__(self):
			ui.Board.__init__(self)
			
			self.isActiveSlide = False
			self.isActiveSlideOut = False
			self.endTime = 0
			self.wndWidth = 0
			
			self.textInfo = ui.TextLine()
			self.textInfo.SetParent(self)
			self.textInfo.SetWindowHorizontalAlignCenter()
			self.textInfo.SetWindowVerticalAlignCenter()
			self.textInfo.SetHorizontalAlignCenter()
			self.textInfo.SetVerticalAlignCenter()
			self.textInfo.SetPosition(20, 0)
			self.textInfo.SetText("|cff90EE90You sold:|r")
			self.textInfo.Show()

			self.textLineItemName = ui.TextLine()
			self.textLineItemName.SetParent(self)
			self.textLineItemName.SetWindowHorizontalAlignCenter()
			self.textLineItemName.SetWindowVerticalAlignCenter()
			self.textLineItemName.SetHorizontalAlignCenter()
			self.textLineItemName.SetVerticalAlignCenter()
			self.textLineItemName.SetPosition(20, 10)
			self.textLineItemName.SetText("itemName")
			self.textLineItemName.Show()
			
			self.textLineItemPrice = ui.TextLine()
			self.textLineItemPrice.SetParent(self)
			self.textLineItemPrice.SetWindowHorizontalAlignCenter()
			self.textLineItemPrice.SetWindowVerticalAlignCenter()
			self.textLineItemPrice.SetHorizontalAlignCenter()
			self.textLineItemPrice.SetVerticalAlignCenter()
			self.textLineItemPrice.SetPosition(20, 20)
			self.textLineItemPrice.SetText("itemPrice")
			self.textLineItemPrice.Show()

			self.slotItem = ui.GridSlotWindow()
			self.slotItem.SetParent(self)
			self.slotItem.SetPosition(10, 10)
			self.slotItem.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			self.slotItem.ArrangeSlot(0, 1, 3, 32, 32, 0, 0)
			self.slotItem.RefreshSlot()
			self.slotItem.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
			self.slotItem.Show()

			self.listNotification = {}

		def AddNotification(self, dwItemID, itemName, itemPrice, dwItemCount):
			self.listNotification[dwItemID] = [itemName, itemPrice, dwItemCount]
			self.Close()

		def __del__(self):
			ui.Board.__del__(self)

		def SlideIn(self, dwItemID, itemName, itemPrice, dwItemCount):
			self.SetTop()
			self.Show()
			
			self.isActiveSlide = True
			self.endTime = app.GetGlobalTimeStamp() + 4
			
			self.textLineItemName.SetText("|cffFFD700"+str(itemName)+"|r")
			self.textLineItemPrice.SetText("|cffFFB96D"+localeInfo.NumberToMoneyString(itemPrice)+"|r")

			self.wndWidth = 220
			self.SetSize(self.wndWidth, 118)
			self.textInfo.SetPosition(21, -30)
			self.textLineItemName.SetPosition(21, 4)
			self.textLineItemPrice.SetPosition(21, 14)
			self.SetPosition(-self.wndWidth, wndMgr.GetScreenHeight() - 290 - 32*4)
			
			self.slotItem.ClearSlot(0)
			self.slotItem.SetItemSlot(0, dwItemID, dwItemCount)

		def Close(self):
			if self.isActiveSlide:
				return

			if len(self.listNotification) == 0:
				self.Hide()
			else:
				for itemf in self.listNotification:
					self.SlideIn(itemf, self.listNotification[itemf][0], self.listNotification[itemf][1], self.listNotification[itemf][2])
					del self.listNotification[itemf]
					break

		def Destroy(self):
			self.Hide()
			self.listNotification = {}

		def OnUpdate(self):
			if self.isActiveSlide and self.isActiveSlide == True:
				x, y = self.GetLocalPosition()
				if x < 0:
					self.SetPosition(x + 4, y)
					
			if self.endTime - app.GetGlobalTimeStamp() <= 0 and self.isActiveSlideOut == False and self.isActiveSlide == True:
				self.isActiveSlide = False
				self.isActiveSlideOut = True
					
			if self.isActiveSlideOut and self.isActiveSlideOut == True:
				x, y = self.GetLocalPosition()
				if x > -(self.wndWidth):
					self.SetPosition(x - 4, y)
					
				if x <= -(self.wndWidth):
					self.isActiveSlideOut = False
					self.Close()
					