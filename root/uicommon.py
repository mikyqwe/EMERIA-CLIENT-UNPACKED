import ui
import localeInfo
import app
import ime
import net
import uiScriptLocale
import item
import player
import constInfo

#for debug
import dbg

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
		
	def ResetInput(self):
		self.inputValue.SetText("")
		
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

if app.ENABLE_OFFLINE_SHOP_SYSTEM:
	class QuestionDialogOfflineShopMoney(ui.ScriptWindow):

		def __init__(self):
			ui.ScriptWindow.__init__(self)
			self.__CreateDialog()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def __CreateDialog(self):
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/questiondialogofflineshopmoney.py")

			self.board = self.GetChild("board")
			self.textLine = self.GetChild("message")
			self.textLine2 = self.GetChild("message2")
			self.acceptButton = self.GetChild("accept")
			self.cancelButton = self.GetChild("cancel")

		def Open(self):
			self.SetCenterPosition()
			self.SetTop()
			self.Show()

		def Close(self):
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

		def SetText2(self, text):
			self.textLine2.SetText(text)

		def SetAcceptText(self, text):
			self.acceptButton.SetText(text)

		def SetCancelText(self, text):
			self.cancelButton.SetText(text)

		def OnPressEscapeKey(self):
			self.Close()
			return True
class QuestionDialogItem(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()
	def __del__(self):
		ui.ScriptWindow.__del__(self)
	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialogitem.py")
		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.acceptButton = self.GetChild("accept")
		self.destroyButton = self.GetChild("destroy")
		self.sellButton = self.GetChild("sell")
		self.cancelButton = self.GetChild("cancel")
	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()
	def Close(self):
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
	def SetDestroyEvent(self, event):
		self.destroyButton.SetEvent(event)
	def SetSellEvent(self, event):
		self.sellButton.SetEvent(event)
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
		return TRUE


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

	def SetText1(self, text, alignLeft = False):
		self.textLine1.SetText(text)
		if alignLeft == True:
			self.textLine1.SetPosition(15, 30)
			self.textLine1.SetWindowHorizontalAlignLeft()
			self.textLine1.SetHorizontalAlignLeft()
		else:
			self.textLine1.SetPosition(0, 25)
			self.textLine1.SetWindowHorizontalAlignCenter()
			self.textLine1.SetHorizontalAlignCenter()

	def SetText2(self, text, alignLeft = False):
		self.textLine2.SetText(text)
		if alignLeft == True:
			self.textLine2.SetPosition(15, 50)
			self.textLine2.SetWindowHorizontalAlignLeft()
			self.textLine2.SetHorizontalAlignLeft()
		else:
			self.textLine2.SetPosition(0, 50)
			self.textLine2.SetWindowHorizontalAlignCenter()
			self.textLine2.SetHorizontalAlignCenter()
		
	def AutoResize(self):
		if self.textLine1.GetTextSize()[0] > self.textLine2.GetTextSize()[0]:
			self.SetWidth(self.textLine1.GetTextSize()[0] + 30)
		else:
			self.SetWidth(self.textLine2.GetTextSize()[0] + 30)

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
		self.timeoverMsg = None
		self.isCancelOnTimeover = False

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
		if leftTime<0.5:
			if self.timeoverMsg:
				chat.AppendChat(chat.CHAT_TYPE_INFO, self.timeoverMsg)
			if self.isCancelOnTimeover:
				self.cancelButton.CallEvent()

	def SetTimeOverMsg(self, msg):
		self.timeoverMsg = msg

	def SetCancelOnTimeOver(self):
		self.isCancelOnTimeover = True

class MoneyInputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		if not app.ENABLE_CHEQUE_SYSTEM:
			self.moneyHeaderText = localeInfo.MONEY_INPUT_DIALOG_SELLPRICE
		self.__CreateDialog()
		self.SetMaxLength(9)
		if app.ENABLE_CHEQUE_SYSTEM:
			self.SetMaxLengthCheque(3)

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
		if app.ENABLE_CHEQUE_SYSTEM:
			self.SellInfoText = getObject("SellInfoText")
			self.InputValue_Cheque = getObject("InputValue_Cheque")
			self.InputValue_Cheque.SetNumberMode()
			self.InputValue_Cheque.OnIMEUpdate = ui.__mem_func__(self.__OnChequeValueUpdate)
			self.chequeText = getObject("ChequeValue")

	def Open(self):
		self.inputValue.SetText("")
		self.inputValue.SetFocus()
		if app.ENABLE_CHEQUE_SYSTEM:
			self.__OnChequeValueUpdate()
			self.InputValue_Cheque.SetText("0")
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
		if app.ENABLE_CHEQUE_SYSTEM:
			self.InputValue_Cheque = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		length = min(9, length)
		self.inputValue.SetMax(length)
		#self.inputValue.SetUserMax(length)

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
#		final_text = ""
#		
#		for char in text:
#			if char.isdigit():
#				final_text+=char
#		
#		self.inputValue.SetText(final_text)
#		
#		self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(text))

		money = 0
		if text and text.isdigit():
			try:
				money = int(text)
			except ValueError:
				money = 199999999

		if app.ENABLE_CHEQUE_SYSTEM:
			self.moneyText.SetText(localeInfo.NumberToMoneyString(money))
		else:
			self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(money))

	if app.ENABLE_CHEQUE_SYSTEM:		
		def SetChequeValue(self, value):
			value=str(value)
			self.InputValue_Cheque.SetText(value)
			self.InputValue_Cheque.SetFocus()
			self.__OnChequeValueUpdate()
			ime.SetCursorPosition(len(value))
		
		def SetMaxLengthCheque(self, length):
			length = min(3, length)
			self.InputValue_Cheque.SetMax(length)
		
		def GetChequeText(self):
			return self.InputValue_Cheque.GetText()
		
		def __OnChequeValueUpdate(self):
			ui.EditLine.OnIMEUpdate(self.InputValue_Cheque)

			text = self.InputValue_Cheque.GetText()

			cheque = 0
			if text and text.isdigit():
				try:
					cheque = int(text)
				except ValueError:
					cheque = 999

			self.chequeText.SetText(localeInfo.NumberToChequeString(cheque))