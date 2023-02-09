import ui
import net
import localeInfo
import uiScriptLocale

class DecorumStat(ui.ScriptWindow):

	DUEL = 0
	ARENA1 = 1
	ARENA2 = 2
	ARENA3 = 3
	
	STATE_HIDED = 0
	STATE_FADE_IN = 1
	STATE_SHOWED = 2
	STATE_FADE_OUT = 3
	
	LEGUE_NAME = (
		uiScriptLocale.DECORUM_LEGUE_1,
		uiScriptLocale.DECORUM_LEGUE_2,
		uiScriptLocale.DECORUM_LEGUE_3,
		uiScriptLocale.DECORUM_LEGUE_4,
		uiScriptLocale.DECORUM_LEGUE_5,
	)
	
	LEGUE_GRADE = (
		"IV",
		"III",
		"II",
		"I",
	)
	
	LEGUE_IMG = (
		"",
		"d:/ymir work/ui/universalelements/decorum/universalelements_legue_iron4.sub",
		"d:/ymir work/ui/universalelements/decorum/universalelements_legue_iron3.sub",
		"d:/ymir work/ui/universalelements/decorum/universalelements_legue_iron2.sub",
		"d:/ymir work/ui/universalelements/decorum/universalelements_legue_iron1.sub",
		"d:/ymir work/ui/universalelements/decorum/universalelements_legue_bronze4.sub",
		"d:/ymir work/ui/universalelements/decorum/universalelements_legue_bronze3.sub",
		"d:/ymir work/ui/universalelements/decorum/universalelements_legue_bronze2.sub",
		"d:/ymir work/ui/universalelements/decorum/universalelements_legue_bronze1.sub",
		"d:/ymir work/ui/universalelements/decorum/universalelements_legue_silver4.sub",
		"d:/ymir work/ui/universalelements/decorum/universalelements_legue_silver3.sub",
		"d:/ymir work/ui/universalelements/decorum/universalelements_legue_silver2.sub",
		"d:/ymir work/ui/universalelements/decorum/universalelements_legue_silver1.sub",
		"d:/ymir work/ui/universalelements/decorum/universalelements_legue_gold4.sub",
		"d:/ymir work/ui/universalelements/decorum/universalelements_legue_gold3.sub",
		"d:/ymir work/ui/universalelements/decorum/universalelements_legue_gold2.sub",
		"d:/ymir work/ui/universalelements/decorum/universalelements_legue_gold1.sub",
		"d:/ymir work/ui/universalelements/decorum/universalelements_legue_diamond4.sub",
		"d:/ymir work/ui/universalelements/decorum/universalelements_legue_diamond3.sub",
		"d:/ymir work/ui/universalelements/decorum/universalelements_legue_diamond2.sub",
		"d:/ymir work/ui/universalelements/decorum/universalelements_legue_diamond1.sub",
	)
	
	def __init__(self):
		ui.ScriptWindow.__init__(self, "TOP_MOST")

		self.State = self.STATE_HIDED
		self.LegueMark = None
		self.PgNameValue = None
		self.DecorumValue = None
		self.isSelf = True
		self.DecoredDuel = []
		self.DecoredArenas = []
		self.PromotionDemotion = []
		self.BlockCheks = {}
		self.LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):

		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "decorumwindow.py")
		except:
			import exception
			exception.Abort("DecorumStat.LoadDialog.LoadObject")

		try:
			GetObject = self.GetChild
			
			self.LegueMark = GetObject("LegueMark")
			self.LegueNameValue = GetObject("LegueNameValue")
			self.PgNameValue = GetObject("PgNameValue")
			self.DecorumValue = GetObject("DecorumValue")
			self.CloseButton = GetObject("CloseBotton")
			self.DecoredDuel = [GetObject("DecoredDuelFull"), GetObject("DecorumDuelRate"), GetObject("DecorumDuelText")]
			DecoredArena1 = [GetObject("DecoredArena1Full"), GetObject("DecorumArena1Rate"), GetObject("DecorumArena1Text")]
			DecoredArena2 = [GetObject("DecoredArena2Full"), GetObject("DecorumArena2Rate"), GetObject("DecorumArena2Text")]
			DecoredArena3 = [GetObject("DecoredArena3Full"), GetObject("DecorumArena3Rate"), GetObject("DecorumArena3Text")]
			self.PromotionDemotion = [GetObject("DecorumPromotionText"), GetObject("DecorumDemotionText")]
			self.KillDeath = [GetObject("DecorumKillsText"), GetObject("DecorumDeathText")]
			self.BlockCheks[self.DUEL] = GetObject("DuelCheckBox")
			self.BlockCheks[self.ARENA1] = GetObject("Arena1CheckBox")
			self.BlockCheks[self.ARENA2] = GetObject("Arena2CheckBox")
			self.BlockCheks[self.ARENA3] = GetObject("Arena3CheckBox")
			self.DecoredArenas = [DecoredArena1, DecoredArena2, DecoredArena3]
			
		except:
			import exception
			exception.Abort("DecorumStat.LoadDialog.BindObject")
			
		self.CloseButton.Hide()
		for i in xrange(len(self.BlockCheks)):
			self.BlockCheks[i].SetCheckEvent(lambda x = i:self.__ToggleMode(x))
			
	def SetBase(self, name, decorum, legue):
		if legue <= 0:
			return
		self.PgNameValue.SetText(name)
		self.DecorumValue.SetText("%d %s" % (decorum, uiScriptLocale.DECORUM))
		self.LegueNameValue.SetText(uiScriptLocale.DECORUM_LEGUE % (self.LEGUE_NAME[(legue-1) / 4], self.LEGUE_GRADE[(legue-1)%4]))
		self.LegueMark.LoadImage(self.LEGUE_IMG[legue])
		
	def SetDuel(self, done, won):
		rate = float(won) / max(done, 1)
		self.DecoredDuel[0].SetPercentage(rate, 1)
		self.DecoredDuel[1].SetText("%d%%" % int(rate * 100))
		self.DecoredDuel[2].SetText(uiScriptLocale.DECORUM_MATCH % (won, done))
		
	def SetArena(self, type, done, won):
		rate = float(won) / max(done, 1)
		self.DecoredArenas[type][0].SetPercentage(rate, 1)
		self.DecoredArenas[type][1].SetText("%d%%" % int(rate * 100))
		self.DecoredArenas[type][2].SetText(uiScriptLocale.DECORUM_MATCH % (won, done))
		
	def SetLegueInfo(self, promotion, demotion):
		self.PromotionDemotion[0].SetText(uiScriptLocale.DECORUM_PROMOTION % (promotion))
		self.PromotionDemotion[1].SetText(uiScriptLocale.DECORUM_DEMOTION % (demotion))
		
	def SetKD(self, kill, death):
		self.KillDeath[0].SetText(uiScriptLocale.DECORED_KILLS % (kill))
		self.KillDeath[1].SetText(uiScriptLocale.DECORED_DEATH % (death))
		
	def __ToggleMode(self, mode):
		if not self.isSelf:
			return
		net.SendChatPacket("/decorum_block %d" % mode)
		
	def SetBlock(self, block):
		for i in xrange(4):
			self.BlockCheks[i].SetCheck(not(block & 1<<i))
			
	def IsSelf(self, flag):
		self.isSelf = flag
		if flag:
			self.CloseButton.Hide()
		else:
			self.CloseButton.Show()
			
	def SetCloseEvent(self, event):
		self.CloseButton.SetEvent(event)

	def Open(self):
		self.Show()
		
	def Destroy(self):
		self.ClearDictionary()
		self.Close()

	def Close(self):
		self.Hide()
		
	def OnUpdate(self):

		if self.STATE_FADE_IN == self.State:
			x, y = self.GetGlobalPosition()
			newX = min(x + 25, 0)
			self.SetPosition(newX, y)
			if newX == 0 :
				self.State = self.STATE_SHOWED

		elif self.STATE_FADE_OUT == self.State:
			
			x, y = self.GetGlobalPosition()
			newX = max(x - 25, -self.GetWidth())
			self.SetPosition(newX, y)
			if newX == -self.GetWidth() :
				self.State = self.STATE_HIDED
				self.Hide()
		