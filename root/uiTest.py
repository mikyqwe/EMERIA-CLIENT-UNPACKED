import chat, net, player, wndMgr, mouseModule, ui

class TestWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "inv.py")
		except:
			import exception
			exception.Abort("TestWindow.__LoadWindow.LoadObject")

		self.GetChild("Equipment_Base").Hide()
		self.GetChild("Equipment_Page_Secondary").Hide()
		self.GetChild("Equipment_Page_Cosmetics").Hide()
		self.GetChild("Equipment_Page_Talismans").Hide()


		#self.GetChild("Equipment_Base").Show()
		#self.GetChild("Equipment_Page_Secondary").Show()
		self.GetChild("Equipment_Page_Cosmetics").Show()
		#self.GetChild("Equipment_Page_Talismans").Show()

		for x in xrange(0, 5000):
			self.GetChild("EquipmentSlot").SetItemSlot(x, 30001, 1)
			self.GetChild("Equipment_Slot_Secondary").SetItemSlot(x, 30001, 1)
			self.GetChild("Equipment_Slot_Cosmetics").SetItemSlot(x, 30001, 1)
			self.GetChild("Equipment_Slot_Talismans").SetItemSlot(x, 30001, 1)

		self.SetCenterPosition()

	def Close(self):
		self.Hide()

	def Destroy(self):
		self.ClearDictionary()

	def Open(self):
		self.Show()
		self.SetCenterPosition()

	def OnPressEscapeKey(self):
		self.Close()
		return True
