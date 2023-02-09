import net
import snd
import locale
import localeInfo
import uiCommon
import ui
import uiTip
import dbg
import os
import app
import uiScriptLocale
import chat
import time

class MultiLanguage(ui.BoardWithTitleBar):
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.LoadMultiLanguage()
		
	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)
		
	def Destroy(self):
		self.Hide()
		return TRUE
		
	def Open(self):
		self.LoadMultiLanguage()
		
	def LoadMultiLanguage(self):
		self.SetSize(185, 250)
		self.Show()
		self.AddFlag('movable')
		self.AddFlag("float")
		self.AddFlag("animate")
		self.SetTitleName('Multi-Language')
		self.SetCenterPosition()
		self.SetCloseEvent(self.Close)
		self.intr = ui.Button()
		self.intr.SetParent(self)
		self.intr.SetPosition(140, 9)
		self.intr.SetUpVisual("d:/ymir work/q_mark_01.tga")
		self.intr.SetOverVisual("d:/ymir work/q_mark_02.tga")
		self.intr.SetDownVisual("d:/ymir work/q_mark_02.tga")
		self.intr.SetEvent(self.Informatii)
		self.intr.SetToolTipText(uiScriptLocale.MULTILANGUAGE_SYSTEM_TEXT)
		self.intr.Show()
				
		self.LoadButtons()
		
	def LoadButtons(self):
	
## FUNDAL ##
		self.Fundal = ui.Button()
		self.Fundal.SetParent(self)
		self.Fundal.SetPosition(11, 38)
		self.Fundal.SetUpVisual("d:/ymir work/fundal.tga")
		self.Fundal.SetOverVisual("d:/ymir work/fundal.tga")
		self.Fundal.SetDownVisual("d:/ymir work/fundal.tga")
		self.Fundal.Show()
## FUNDAL ##
	
		self.EnButton = ui.Button()
		self.EnButton.SetParent(self)
		self.EnButton.SetPosition(20, 50)
		self.EnButton.SetUpVisual("d:/ymir work/buton_nou1.tga")
		self.EnButton.SetOverVisual("d:/ymir work/buton_nou2.tga")
		self.EnButton.SetDownVisual("d:/ymir work/buton_nou3.tga")
		self.EnButton.SetText("English")
		self.EnButton.SetEvent(self.__Language_1)
		self.EnButton.Show()
	
		self.RoButton = ui.Button()
		self.RoButton.SetParent(self)
		self.RoButton.SetPosition(20, 80)
		self.RoButton.SetUpVisual("d:/ymir work/buton_nou1.tga")
		self.RoButton.SetOverVisual("d:/ymir work/buton_nou2.tga")
		self.RoButton.SetDownVisual("d:/ymir work/buton_nou3.tga")
		self.RoButton.SetText("Romana")
		self.RoButton.SetEvent(self.__Language_4)
		self.RoButton.Show()
		
		self.ItButton = ui.Button()
		self.ItButton.SetParent(self)
		self.ItButton.SetPosition(20, 110)
		self.ItButton.SetUpVisual("d:/ymir work/buton_nou1.tga")
		self.ItButton.SetOverVisual("d:/ymir work/buton_nou2.tga")
		self.ItButton.SetDownVisual("d:/ymir work/buton_nou3.tga")
		self.ItButton.SetText("Italiano")
		self.ItButton.SetEvent(self.__Language_2)
		self.ItButton.Show()
		
		self.DeButton = ui.Button()
		self.DeButton.SetParent(self)
		self.DeButton.SetPosition(20, 140)
		self.DeButton.SetUpVisual("d:/ymir work/buton_nou1.tga")
		self.DeButton.SetOverVisual("d:/ymir work/buton_nou2.tga")
		self.DeButton.SetDownVisual("d:/ymir work/buton_nou3.tga")
		self.DeButton.SetText(" Deutsche")
		self.DeButton.SetEvent(self.__Language_3)
		self.DeButton.Show()
		
		self.TrButton = ui.Button()
		self.TrButton.SetParent(self)
		self.TrButton.SetPosition(20, 170)
		self.TrButton.SetUpVisual("d:/ymir work/buton_nou1.tga")
		self.TrButton.SetOverVisual("d:/ymir work/buton_nou2.tga")
		self.TrButton.SetDownVisual("d:/ymir work/buton_nou3.tga")
		self.TrButton.SetText("Turkce")
		self.TrButton.SetEvent(self.__Language_5)
		self.TrButton.Show()
		
		self.PlButton = ui.Button()
		self.PlButton.SetParent(self)
		self.PlButton.SetPosition(20, 200)
		self.PlButton.SetUpVisual("d:/ymir work/buton_nou1.tga")
		self.PlButton.SetOverVisual("d:/ymir work/buton_nou2.tga")
		self.PlButton.SetDownVisual("d:/ymir work/buton_nou3.tga")
		self.PlButton.SetText("Polska")
		self.PlButton.SetEvent(self.__Language_6)
		self.PlButton.Show()
	
## STEGULETE
		self.RoIcon = ui.Button()
		self.RoIcon.SetParent(self)
		self.RoIcon.SetPosition(55, 87)
		self.RoIcon.SetUpVisual("d:/ymir work/romania.tga")
		self.RoIcon.SetOverVisual("d:/ymir work/romania.tga")
		self.RoIcon.SetDownVisual("d:/ymir work/romania.tga")
		self.RoIcon.Show()
	
		self.EnIcon = ui.Button()
		self.EnIcon.SetParent(self)
		self.EnIcon.SetPosition(55, 57)
		self.EnIcon.SetUpVisual("d:/ymir work/english.tga")
		self.EnIcon.SetOverVisual("d:/ymir work/english.tga")
		self.EnIcon.SetDownVisual("d:/ymir work/english.tga")
		self.EnIcon.Show()
		
		self.ItIcon = ui.Button()
		self.ItIcon.SetParent(self)
		self.ItIcon.SetPosition(55, 117)
		self.ItIcon.SetUpVisual("d:/ymir work/italiano.tga")
		self.ItIcon.SetOverVisual("d:/ymir work/italiano.tga")
		self.ItIcon.SetDownVisual("d:/ymir work/italiano.tga")
		self.ItIcon.Show()
		
		self.DeIcon = ui.Button()
		self.DeIcon.SetParent(self)
		self.DeIcon.SetPosition(55, 147)
		self.DeIcon.SetUpVisual("d:/ymir work/tedesco.tga")
		self.DeIcon.SetOverVisual("d:/ymir work/tedesco.tga")
		self.DeIcon.SetDownVisual("d:/ymir work/tedesco.tga")
		self.DeIcon.Show()
		
		self.TrIcon = ui.Button()
		self.TrIcon.SetParent(self)
		self.TrIcon.SetPosition(55, 177)
		self.TrIcon.SetUpVisual("d:/ymir work/turco.tga")
		self.TrIcon.SetOverVisual("d:/ymir work/turco.tga")
		self.TrIcon.SetDownVisual("d:/ymir work/turco.tga")
		self.TrIcon.Show()
		
		self.PlIcon = ui.Button()
		self.PlIcon.SetParent(self)
		self.PlIcon.SetPosition(55, 207)
		self.PlIcon.SetUpVisual("d:/ymir work/polacco.tga")
		self.PlIcon.SetOverVisual("d:/ymir work/polacco.tga")
		self.PlIcon.SetDownVisual("d:/ymir work/polacco.tga")
		self.PlIcon.Show()
	
## STEGULETE

			
	def __Language_1(self):
		file = open("locale.cfg", "w")
 		file.write("10002 %d en" % (self.CodePageReplace("en"))) 
		file.close()
		self.wndPopupDialog = uiCommon.PopupDialog()
		self.wndPopupDialog.SetText("Restart to apply the changes. [EN]")
		self.wndPopupDialog.Open()
		self.Close()
		
	
	def __Language_2(self):
		file = open("locale.cfg", "w")
 		file.write("10002 %d it" % (self.CodePageReplace("it")))
		file.close()
		self.wndPopupDialog = uiCommon.PopupDialog()
		self.wndPopupDialog.SetText("Riavvia per applicare le modifiche. [IT]") ## usare locale_game per gli accenti e per le traduzioni
		self.wndPopupDialog.Open()
		self.Close()
		
	def __Language_3(self):
		file = open("locale.cfg", "w")
 		file.write("10002 %d de" % (self.CodePageReplace("de")))
		file.close()
		self.wndPopupDialog = uiCommon.PopupDialog()
		self.wndPopupDialog.SetText("Restart to apply the changes. [DE]")
		self.wndPopupDialog.Open()
		self.Close()
	
	def __Language_4(self):
		file = open("locale.cfg", "w")
 		file.write("10002 %d ro" % (self.CodePageReplace("ro"))) 
		file.close()
		self.wndPopupDialog = uiCommon.PopupDialog()
		self.wndPopupDialog.SetText("Restart to apply the changes. [RO]")
		self.wndPopupDialog.Open()
		self.Close()
		
	def __Language_5(self):
		file = open("locale.cfg", "w")
 		file.write("10002 %d tr" % (self.CodePageReplace("tr"))) 
		file.close()
		self.wndPopupDialog = uiCommon.PopupDialog()
		self.wndPopupDialog.SetText("Restart to apply the changes. [TR]")
		self.wndPopupDialog.Open()
		self.Close()
		
	def __Language_6(self):
		file = open("locale.cfg", "w")
 		file.write("10002 %d pl" % (self.CodePageReplace("pl"))) 
		file.close()
		self.wndPopupDialog = uiCommon.PopupDialog()
		self.wndPopupDialog.SetText("Restart to apply the changes. [PL]")
		self.wndPopupDialog.Open()
		self.Close()
	
	def CodePageReplace(self, langName):
		cpReplace = {
			"gr" : 1253,
			"tr" : 1254,
			"bg" : 1251,
			"ru" : 1251,
			"ae" : 1256,
			"ar" : 1256,
			"cz" : 1250,
			"hr" : 1250,
			"pl" : 1250,
			"hu" : 1250,
			"ro" : 1251,
			"vi" : 1258,
		}

		try:
			return cpReplace[langName]
		except:
			return 1252
	
		
	def Informatii(self):
		chat.AppendChat(chat.CHAT_TYPE_NOTICE, uiScriptLocale.MULTILANGUAGE_SYSTEM_TEXT)
		
	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE
		
