import ui
import localeInfo
import player
import item
import uiToolTip
import wndMgr
import app
import constInfo
	
class KillStatisticsUI(ui.ScriptWindow):
	def __init__(self, parent):
		self.uiCharacterStatus = parent
		ui.ScriptWindow.__init__(self)
		
		self.__LoadScript()

	def __del__(self):
		self.uiCharacterStatus = None
		ui.ScriptWindow.__del__(self)

	def __LoadScript(self):
		
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/KillStatisticsWindow.py")
		except:
			import exception
			exception.Abort("KillStatisticsUI.__LoadScript")

		self.Width = 253 - 3
		self.GetChild("TitleBar").CloseButtonHide()

		self.__Initialize()

	def __Initialize(self):
		self.jinno_kills_obj = self.GetChild("jinno_kills")
		self.shinsoo_kills_obj = self.GetChild("shinsoo_kills")
		self.chunjo_kills_obj = self.GetChild("chunjo_kills")
		self.total_kills_obj = self.GetChild("total_kills")
		self.total_deaths_obj = self.GetChild("total_deaths")
		self.kd_obj = self.GetChild("kd")
		self.duels_t_obj = self.GetChild("duels_t")
		self.duels_w_obj = self.GetChild("duels_w")
		self.duels_l_obj = self.GetChild("duels_l")
		self.bosses_kills_obj = self.GetChild("bosses_kills")
		self.stones_kills_obj = self.GetChild("stones_kills")
		
	def Refresh(self):
		kd_zero_fix = 0
		if constInfo.KILL_STATISTICS_DATA[4] == 0:
			kd_zero_fix = 1
			
		self.jinno_kills_obj.SetText("%i" % constInfo.KILL_STATISTICS_DATA[0])
		self.shinsoo_kills_obj.SetText("%i" % constInfo.KILL_STATISTICS_DATA[1])
		self.chunjo_kills_obj.SetText("%i" % constInfo.KILL_STATISTICS_DATA[2])
		self.total_kills_obj.SetText("%i" % constInfo.KILL_STATISTICS_DATA[3])
		self.total_deaths_obj.SetText("%i" % constInfo.KILL_STATISTICS_DATA[4])
		self.kd_obj.SetText("%.2f" % (float(constInfo.KILL_STATISTICS_DATA[3])/(kd_zero_fix+float(constInfo.KILL_STATISTICS_DATA[4]))))
		self.duels_t_obj.SetText("%i" % (constInfo.KILL_STATISTICS_DATA[5]+constInfo.KILL_STATISTICS_DATA[6]))
		self.duels_w_obj.SetText("%i" % constInfo.KILL_STATISTICS_DATA[5])
		self.duels_l_obj.SetText("%i" % constInfo.KILL_STATISTICS_DATA[6])
		self.bosses_kills_obj.SetText("%i" % constInfo.KILL_STATISTICS_DATA[7])
		self.stones_kills_obj.SetText("%i" % constInfo.KILL_STATISTICS_DATA[8])
		
	def OnUpdate(self):
		self.Refresh()

	def Show(self):
		ui.ScriptWindow.Show(self)
		self.SetTop()

	def Close(self): # try
		self.Hide()

	def AdjustPosition(self, x, y):
		self.SetPosition(x + self.Width, y)

	def OnTop(self):
		if self.uiCharacterStatus:
			self.uiCharacterStatus.SetTop()