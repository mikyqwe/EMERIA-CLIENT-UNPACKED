import net
import snd
import localeInfo
import ui
import uiTip
import uiCommon
import os
import app

class MultiLanguage(ui.BoardWithTitleBar):
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		
	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)
		
	def Destroy(self):
		self.Hide()
		return TRUE
	
	def Open(self):
		self.LoadMultiLanguage()
		
	def LoadMultiLanguage(self):
		self.SetSize(127, 230)
		self.Show()
		self.AddFlag('movable')
		self.AddFlag("float")
		self.SetTitleName('Language')
		self.SetCenterPosition()
		self.SetCloseEvent(self.Close)
				
		self.LoadButtons()
		
	def LoadButtons(self):
	
		self.EnButton = ui.Button()
		self.EnButton.SetParent(self)
		self.EnButton.SetPosition(20, 50)
		self.EnButton.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
		self.EnButton.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
		self.EnButton.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
		self.EnButton.SetText("English")
		self.EnButton.SetEvent(self.__Language_1)
		self.EnButton.Show()
	
		self.ItButton = ui.Button()
		self.ItButton.SetParent(self)
		self.ItButton.SetPosition(20, 80)
		self.ItButton.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
		self.ItButton.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
		self.ItButton.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
		self.ItButton.SetText("Italiano")
		self.ItButton.SetEvent(self.__Language_2)
		self.ItButton.Show()
		
		self.DeButton = ui.Button()
		self.DeButton.SetParent(self)
		self.DeButton.SetPosition(20, 110)
		self.DeButton.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
		self.DeButton.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
		self.DeButton.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
		self.DeButton.SetText("Deutsch")
		self.DeButton.SetEvent(self.__Language_3)
		self.DeButton.Show()
		
		self.RoButton = ui.Button()
		self.RoButton.SetParent(self)
		self.RoButton.SetPosition(20, 140)
		self.RoButton.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
		self.RoButton.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
		self.RoButton.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
		self.RoButton.SetText("Romana")
		self.RoButton.SetEvent(self.__Language_4)
		self.RoButton.Show()
		
		self.TrButton = ui.Button()
		self.TrButton.SetParent(self)
		self.TrButton.SetPosition(20, 170)
		self.TrButton.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
		self.TrButton.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
		self.TrButton.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
		self.TrButton.SetText("Polski")
		self.TrButton.SetEvent(self.__Language_5)
		self.TrButton.Show()
		
		self.PlButton = ui.Button()
		self.PlButton.SetParent(self)
		self.PlButton.SetPosition(20, 200)
		self.PlButton.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
		self.PlButton.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
		self.PlButton.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
		self.PlButton.SetText("Turkce")
		self.PlButton.SetEvent(self.__Language_6)
		self.PlButton.Show()
				
	def __Language_1(self):
		file = open("locale.cfg", "w")
 		file.write("10002 %d en" % (self.CodePageReplace("en"))) 
		file.close()
		self.wndPopupDialog = uiCommon.PopupDialog()
		self.wndPopupDialog.SetText("The laguage of client was changed to English! Restart the Client.")
		self.wndPopupDialog.Open()
		self.Close()
		
	
	def __Language_2(self):
		file = open("locale.cfg", "w")
 		file.write("10002 %d it" % (self.CodePageReplace("it")))
		file.close()
		self.wndPopupDialog = uiCommon.PopupDialog()
		self.wndPopupDialog.SetText("La lingua del client è stata cambiata in Italiano! Riavvia il client.") ## usare locale_game per gli accenti e per le traduzioni
		self.wndPopupDialog.Open()
		self.Close()
		
	def __Language_3(self):
		file = open("locale.cfg", "w")
 		file.write("10002 %d de" % (self.CodePageReplace("de")))
		file.close()
		self.wndPopupDialog = uiCommon.PopupDialog()
		self.wndPopupDialog.SetText("The laguage of client was changed to Deutsch! Restart the Client.")
		self.wndPopupDialog.Open()
		self.Close()
	
	def __Language_4(self):
		file = open("locale.cfg", "w")
 		file.write("10002 %d ro" % (self.CodePageReplace("ro"))) 
		file.close()
		self.wndPopupDialog = uiCommon.PopupDialog()
		self.wndPopupDialog.SetText("The laguage of client was changed to Romana! Restart the Client.")
		self.wndPopupDialog.Open()
		self.Close()
		
	def __Language_5(self):
		file = open("locale.cfg", "w")
 		file.write("10002 %d tr" % (self.CodePageReplace("tr"))) 
		file.close()
		self.wndPopupDialog = uiCommon.PopupDialog()
		self.wndPopupDialog.SetText("The laguage of client was changed to Turkce! Restart the Client.")
		self.wndPopupDialog.Open()
		self.Close()
		
	def __Language_6(self):
		file = open("locale.cfg", "w")
 		file.write("10002 %d pl" % (self.CodePageReplace("pl"))) 
		file.close()
		self.wndPopupDialog = uiCommon.PopupDialog()
		self.wndPopupDialog.SetText("The laguage of client was changed to Polski! Restart the Client.")
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
			
	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE
		
