import app
import ui
import localeInfo
import uiScriptLocale

class FlagItem(ui.ListBoxEx.Item):
	def __init__(self, fileName):
		ui.ListBoxEx.Item.__init__(self)
		self.imgWidth=0
		self.imgHeight=0
		self.canLoad=0
		self.textLine=self.__CreateTextLine(fileName)
		self.imgBox=self.__CreateImageBox("d:/ymir work/ui/language_flag/"+fileName)

	def __del__(self):
		ui.ListBoxEx.Item.__del__(self)

	def GetText(self):
		return self.textLine.GetText()

	def SetSize(self, width, height):
		ui.ListBoxEx.Item.SetSize(self, 20 + 6*len(self.textLine.GetText()) + 4, height)

	def __CreateTextLine(self, fileName):
		textLine=ui.TextLine()
		textLine.SetParent(self)
		textLine.SetPosition(20, 0)
		textLine.SetText(fileName)
		textLine.Show()
		return textLine

	def __CreateImageBox(self, fileName):
		imgBox = ui.ExpandedImageBox()
		imgBox.SetParent(self)
		imgBox.LoadImage(fileName)
		imgBox.SetPosition(0, 2)
		imgBox.SetScale(1, 1)
		imgBox.Show()
		return imgBox

class SymbolItem(ui.ListBoxEx.Item):
	def __init__(self, fileName):
		ui.ListBoxEx.Item.__init__(self)
		self.textLine=self.__CreateTextLine(fileName)
		(self.canLoad, self.imgWidth, self.imgHeight)=app.GetImageInfo("d:/ymir work/ui/language_flag/"+fileName)

	def __del__(self):
		ui.ListBoxEx.Item.__del__(self)

	def GetText(self):
		return self.textLine.GetText()

	def SetSize(self, width, height):
		ui.ListBoxEx.Item.SetSize(self, 6*len(self.textLine.GetText()) + 4, height)

	def __CreateTextLine(self, fileName):
		textLine=ui.TextLine()
		textLine.SetParent(self)
		textLine.SetPosition(1, 2)
		textLine.SetText(fileName)
		textLine.Show()
		return textLine

class PopupDialog(ui.ScriptWindow):
	def __init__(self, parent):
		print "NEW POPUP WINDOW   ----------------------------------------------------------------------------"
		ui.ScriptWindow.__init__(self)

		self.__Load()
		self.__Bind()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		print "---------------------------------------------------------------------------- DELETE POPUP WINDOW"

	def __Load(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/PopupDialog.py")
		except:
			import exception
			exception.Abort("PopupDialog.__Load")

	def __Bind(self):
		try:
			self.textLine=self.GetChild("message")
			self.okButton=self.GetChild("accept")
		except:
			import exception
			exception.Abort("PopupDialog.__Bind")

		self.okButton.SetEvent(ui.__mem_func__(self.__OnOK))

	def Open(self, msg):
		self.textLine.SetText(msg)
		self.SetCenterPosition()
		self.Show()
		self.SetTop()

	def __OnOK(self):
		self.Hide()

class FlagSelectDialog(ui.ScriptWindow):
	def __init__(self):
		print "NEW MARK LIST WINDOW   ----------------------------------------------------------------------------"
		ui.ScriptWindow.__init__(self)

		self.selectEvent=None
		self.isLoaded=0

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		print "---------------------------------------------------------------------------- DELETE MARK LIST WINDOW"

	def Show(self):
		if self.isLoaded==0:
			self.isLoaded=1

			self.__Load()

		ui.ScriptWindow.Show(self)

	def Open(self):
		self.Show()

		self.SetCenterPosition()
		self.SetTop()

		if self.flagListBox.IsEmpty():
			self.__PopupMessage(localeInfo.GUILDMARK_UPLOADER_ERROR_PATH)

	def Close(self):
		self.popupDialog.Hide()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def SAFE_SetSelectEvent(self, event):
		self.selectEvent=ui.__mem_func__(event)

	def __CreateMarkListBox(self):
		flagListBox=ui.ListBoxEx()
		flagListBox.SetParent(self)
		flagListBox.SetPosition(15, 50)
		flagListBox.Show()
		return flagListBox

	def __Load(self):
		self.popupDialog=PopupDialog(self)

		try:
			pyScrLoader = ui.PythonScriptLoader()
			if localeInfo.IsVIETNAM():
				pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "MarkListWindow.py")
			else:
				pyScrLoader.LoadScriptFile(self, "UIScript/MarkListWindow.py")
		except:
			import exception
			exception.Abort("flagListBox.__Load")

		try:
			self.flagListBox=self.__CreateMarkListBox()
			self.flagListBox.SetScrollBar(self.GetChild("ScrollBar"))

			self.popupText = self.popupDialog.GetChild("message")
			self.popupDialog.GetChild("accept").SetEvent(ui.__mem_func__(self.popupDialog.Hide))

			self.board=self.GetChild("board")
			self.okButton=self.GetChild("ok")
			self.cancelButton=self.GetChild("cancel")
			self.refreshButton=self.GetChild("refresh")

		except:
			import exception
			exception.Abort("flagListBox.__Bind")

		self.refreshButton.SetEvent(ui.__mem_func__(self.__OnRefresh))
		self.cancelButton.SetEvent(ui.__mem_func__(self.__OnCancel))
		self.okButton.SetEvent(ui.__mem_func__(self.__OnOK))
		self.board.SetCloseEvent(ui.__mem_func__(self.__OnCancel))
		self.UpdateRect()

		self.__RefreshFileList()

	def __PopupMessage(self, msg):
		self.popupDialog.Open(msg)

	def __OnOK(self):
		selItem=self.flagListBox.GetSelectedItem()
		if selItem:
			import net
			import dbg
			net.SendChatPacket("/changecountryflag %s" % (selItem.GetText()[0:2]))
			self.Hide()
			dbg.LogBox("Trebuie să reporniţi clientul!")
		else:
			self.__PopupMessage("Nu puteţi schimba limba")

	def __OnCancel(self):
		self.Hide()

	def __OnRefresh(self):
		self.__RefreshFileList()

	def __RefreshFileList(self):
		self.__ClearFileList()
		self.__AppendFileList("tga")

	def __ClearFileList(self):
		self.flagListBox.RemoveAllItems()

	def __AppendFileList(self, filter):
		fileNameList = ["oo", "ro", "cz", "de", "hu", "pl", "pt", "it", "es", "tr"]
		for fileName in fileNameList:
			self.__AppendFile(fileName + "." + filter)

	def __AppendFile(self, fileName):
		self.flagListBox.AppendItem(FlagItem(fileName))

class SymbolSelectDialog(ui.ScriptWindow):
	def __init__(self):
		print "NEW SYMBOL LIST WINDOW   ----------------------------------------------------------------------------"
		ui.ScriptWindow.__init__(self)

		self.selectEvent=None
		self.isLoaded=0

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		print "---------------------------------------------------------------------------- DELETE SYMBOL LIST WINDOW"

	def Show(self):
		if self.isLoaded==0:
			self.isLoaded=1

			self.__Load()

		ui.ScriptWindow.Show(self)

	def Open(self):
		self.Show()

		self.SetCenterPosition()
		self.SetTop()

		if self.symbolListBox.IsEmpty():
			self.__PopupMessage(localeInfo.GUILDMARK_UPLOADER_ERROR_PATH)

	def Close(self):
		self.popupDialog.Hide()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def SAFE_SetSelectEvent(self, event):
		self.selectEvent=ui.__mem_func__(event)

	def __CreateSymbolListBox(self):
		symbolListBox=ui.ListBoxEx()
		symbolListBox.SetParent(self)
		symbolListBox.SetPosition(15, 50)
		symbolListBox.Show()
		return symbolListBox

	def __Load(self):
		self.popupDialog=PopupDialog(self)

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/MarkListWindow.py")
		except:
			import exception
			exception.Abort("SymbolListBox.__Load")

		try:
			self.symbolListBox=self.__CreateSymbolListBox()
			self.symbolListBox.SetScrollBar(self.GetChild("ScrollBar"))

			self.popupText = self.popupDialog.GetChild("message")
			self.popupDialog.GetChild("accept").SetEvent(ui.__mem_func__(self.popupDialog.Hide))

			self.board=self.GetChild("board")
			self.okButton=self.GetChild("ok")
			self.cancelButton=self.GetChild("cancel")
			self.refreshButton=self.GetChild("refresh")

		except:
			import exception
			exception.Abort("SymbolListBox.__Bind")

		self.refreshButton.SetEvent(ui.__mem_func__(self.__OnRefresh))
		self.cancelButton.SetEvent(ui.__mem_func__(self.__OnCancel))
		self.okButton.SetEvent(ui.__mem_func__(self.__OnOK))
		self.board.SetCloseEvent(ui.__mem_func__(self.__OnCancel))
		self.board.SetTitleName(localeInfo.SYMBOLLIST_TITLE)
		self.UpdateRect()

		self.__RefreshFileList()

	def __PopupMessage(self, msg):
		self.popupDialog.Open(msg)

	def __OnOK(self):
		selItem=self.symbolListBox.GetSelectedItem()
		if selItem:
			if selItem.canLoad!=1:
				self.__PopupMessage(localeInfo.GUILDMARK_UPLOADER_ERROR_FILE_FORMAT)
			elif selItem.imgWidth!=64:
				self.__PopupMessage(localeInfo.GUILDMARK_UPLOADER_ERROR_64_WIDTH)
			elif selItem.imgHeight!=128:
				self.__PopupMessage(localeInfo.GUILDMARK_UPLOADER_ERROR_128_HEIGHT)
			else:
				self.selectEvent(selItem.GetText())
				self.Hide()
		else:
			self.__PopupMessage(localeInfo.GUILDMARK_UPLOADER_ERROR_SELECT)

	def __OnCancel(self):
		self.Hide()

	def __OnRefresh(self):
		self.__RefreshFileList()

	def __RefreshFileList(self):
		self.__ClearFileList()
		self.__AppendFileList("tga")

	def __ClearFileList(self):
		self.symbolListBox.RemoveAllItems()

	def __AppendFileList(self, filter):
		fileNameList=app.GetFileList("upload/*."+filter)
		for fileName in fileNameList:
			self.__AppendFile(fileName)

	def __AppendFile(self, fileName):
		self.symbolListBox.AppendItem(SymbolItem(fileName))
