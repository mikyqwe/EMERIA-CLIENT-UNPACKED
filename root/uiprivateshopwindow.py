import ui
import constInfo
import chat


class PrivateShopWindow(ui.ScriptWindow):
	def __init__(self): 
		ui.ScriptWindow.__init__(self)
		self.interface = None
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def Destroy(self):
		self.ClearDictionary()
		
		self.interface = None

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def __LoadWindow(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "UIScript/privateshopwindow.py")

		self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))

		self.RemoteShopButton = self.GetChild("RemoteShopButton")
		self.SearchShopButton = self.GetChild("SearchShopButton")

		self.RemoteShopButton.SetEvent(ui.__mem_func__(self.ClickRemoteShopButton))
		self.SearchShopButton.SetEvent(ui.__mem_func__(self.ClickSearchShopButton))

	def ClickRemoteShopButton(self):
		self.interface.ToggleOfflineShopDialog()
		self.Close()

	def ClickSearchShopButton(self):
		self.interface.OpenSearchShop()
		self.Close()

	def BindInterfaceClass(self, interface):
		self.interface = interface

	def OnPressEscapeKey(self):
		self.Close()
		return True
