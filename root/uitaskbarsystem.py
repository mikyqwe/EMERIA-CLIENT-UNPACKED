import uiCommon
import ui
import time
import playersettingmodule
import localeInfo
import mouseModule
import constInfo
import uiScriptLocale
import interfaceModule
import dbg
import wndMgr
import snd
import item
import player
import net
import app
import chat
import uiGameOptionNew
import uilootingsystem

class TaskBarS(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.LoadWindow()
		self.ToggleSwitchbotWindow = None
		self.fastequipdlg = None
		self.BonusPageBoard = None
		self.teleportsystem = None
		self.gameOptionDlg = None
		self.interface = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/taskbarsystem.py")
		except:
			import exception
			exception.Abort("TaskBarS.LoadWindow.LoadObject")
		try:
			self.GetChild("new_button_1").SAFE_SetEvent(self.__MenuFunction5)
			self.GetChild("new_button_2").SAFE_SetEvent(self.__MenuFunction3)
			self.GetChild("new_button_3").SAFE_SetEvent(self.__MenuFunction2)
			self.GetChild("new_button_4").SAFE_SetEvent(self.__MenuFunction4)
			self.GetChild("new_button_5").SAFE_SetEvent(self.__MenuFunction1)
		except:
			import exception
			exception.Abort("TaskBarS.LoadWindow.BindObject")

		#self.fastequipdlg = uifastequip.changeequip()
		#self.BonusPageBoard = uiBonusPage.BonusBoardDialog()
		#self.teleportsystem = teleport_system.teleportwindow()

	def __MenuFunction1(self):
		if self.interface:
			self.interface.ToggleSwitchbotWindow()

	def __MenuFunction2(self):
		self.interface.wndFastEquip.Show()

	def __MenuFunction3(self):
		self.interface.game.OpenMarbleShop()
			
	def BindInterface(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)

	def __MenuFunction4(self):
		if constInfo.TELEPORT_SYSTEM_GUI == 0:
			self.teleportsystem.Show()
			self.teleportsystem.SetTop()
			constInfo.TELEPORT_SYSTEM_GUI = 1
		else:
			self.teleportsystem.Close()
			constInfo.TELEPORT_SYSTEM_GUI = 0

	def __MenuFunction5(self):
		if self.interface:
			self.interface.OpenLootingSystemWindow()

	def Destroy(self):
		self.Close()

	def Close(self):
		self.Hide()
