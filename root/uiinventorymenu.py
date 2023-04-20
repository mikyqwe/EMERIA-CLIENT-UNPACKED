import ui
import constInfo
import chat

class InventoryMenuWindow(ui.ScriptWindow):
	def __init__(self): 
		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def BindInterfaceClass(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)

	def Destroy(self):
		self.ClearDictionary()

		self.interface = None

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

		self.isLoaded = 0

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/InventoryMenu.py")
		except:
			import exception
			exception.Abort("InventoryMenuWindow.LoadWindow.LoadObject")

		try:
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))

			self.SafeBoxButton = self.GetChild("SafeBox")
			self.ItemShopButton = self.GetChild("ItemShop")
			# self.SkillBookStorageButton = self.GetChild("SkillBook_Storage")
			# self.UppItemStorageButton = self.GetChild("UppItem_Storage")
			# self.GhostStoneStorageButton = self.GetChild("GhostStone_Storage")
			self.GeneralStorageButton = self.GetChild("General_Storage")

			self.SafeBoxButton.SetEvent(ui.__mem_func__(self.__OnClickSafeBoxButton))
			self.ItemShopButton.SetEvent(ui.__mem_func__(self.__OnClickItemShopButton))
			# self.SkillBookStorageButton.SetEvent(lambda arg = 0 : self.ClickSpecialStorage(arg))
			# self.UppItemStorageButton.SetEvent(lambda arg = 1 : self.ClickSpecialStorage(arg))
			# self.GhostStoneStorageButton.SetEvent(lambda arg = 2 : self.ClickSpecialStorage(arg))
			self.GeneralStorageButton.SetEvent(lambda arg = 3 : self.ClickSpecialStorage(arg))
		except:
			import exception
			exception.Abort("InventoryMenuWindow.__LoadWindow.BindObject")

	def __OnClickSafeBoxButton(self):
		if constInfo.DROP_GUI_CHECK == 1:
			chat.AppendChat(1, "First of all, choose one option about drop gui.")
		else:
			self.interface.AskSafeboxPassword()
			self.Close()

	def __OnClickItemShopButton(self):
		self.interface.AskMallPassword()
		self.Close()

	def ClickSpecialStorage(self, arg):
		self.interface.ToggleSpecialStorageWindow(arg)
		self.Close()

	def OnPressEscapeKey(self):
		self.Close()
		return True
