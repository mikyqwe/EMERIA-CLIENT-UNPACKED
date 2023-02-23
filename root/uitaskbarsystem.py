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

import uifastequip
import uiBonusPage
import teleport_system

class TaskBarS(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.LoadWindow()
		self.ToggleSwitchbotWindow = None
		self.fastequipdlg = None
		self.BonusPageBoard = None
		self.teleportsystem = None
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
		self.teleportsystem = teleport_system.teleportwindow()

	def __MenuFunction1(self):
		if self.interface:
			self.interface.ToggleSwitchbotWindow()

	def __MenuFunction2(self):
		self.interface.wndFastEquip.Show()

	def __MenuFunction3(self):
		self.interface.daily_reward.Show()
			
	def BindInterface(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)

	def __MenuFunction4(self):
		self.interface.OpenEventCalendar()

	def __MenuFunction5(self):
		constInfo.need_open_pickup_filter=1

	def Destroy(self):
		self.Close()

	def Close(self):
		self.Hide()
