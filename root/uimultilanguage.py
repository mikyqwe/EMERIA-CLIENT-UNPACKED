import net
import snd
import locale
import ui
import uiTip
import dbg
import os
import app
import chr
import uiuploadflagcountry

class MultiLanguage(ui.BoardWithTitleBar):
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.LoadMultiLanguage()
		
	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)
		
	def Destroy(self):
		self.Hide()
		return TRUE
		
	def LoadMultiLanguage(self):
		self.SetSize(227, 245)
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
		self.EnButton.SetEvent(self.__LoadLangCFG, 1)
		self.EnButton.Show()
	
		self.ItButton = ui.Button()
		self.ItButton.SetParent(self)
		self.ItButton.SetPosition(20, 80)
		self.ItButton.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
		self.ItButton.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
		self.ItButton.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
		self.ItButton.SetText("Italy")
		self.ItButton.SetEvent(self.__LoadLangCFG, 2)
		self.ItButton.Show()
		
		self.DeButton = ui.Button()
		self.DeButton.SetParent(self)
		self.DeButton.SetPosition(20, 110)
		self.DeButton.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
		self.DeButton.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
		self.DeButton.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
		self.DeButton.SetText("Germany")
		self.DeButton.SetEvent(self.__LoadLangCFG, 3)
		self.DeButton.Show()
		
		self.EsButton = ui.Button()
		self.EsButton.SetParent(self)
		self.EsButton.SetPosition(20, 140)
		self.EsButton.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
		self.EsButton.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
		self.EsButton.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
		self.EsButton.SetText("Spanish")
		self.EsButton.SetEvent(self.__LoadLangCFG, 4)
		self.EsButton.Show()
		
		self.RoButton = ui.Button()
		self.RoButton.SetParent(self)
		self.RoButton.SetPosition(20, 170)
		self.RoButton.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
		self.RoButton.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
		self.RoButton.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
		self.RoButton.SetText("Romanian")
		self.RoButton.SetEvent(self.__LoadLangCFG, 5)
		self.RoButton.Show()
		
		self.TrButton = ui.Button()
		self.TrButton.SetParent(self)
		self.TrButton.SetPosition(20, 200)
		self.TrButton.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
		self.TrButton.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
		self.TrButton.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
		self.TrButton.SetText("Turky")
		self.TrButton.SetEvent(self.__LoadLangCFG, 6)
		self.TrButton.Show()
		
		self.FlagButton = ui.Button()
		self.FlagButton.SetParent(self)
		self.FlagButton.SetPosition(115, 125)
		self.FlagButton.SetUpVisual("d:/ymir work/ui/public/Large_Button_01.sub")
		self.FlagButton.SetOverVisual("d:/ymir work/ui/public/Large_Button_02.sub")
		self.FlagButton.SetDownVisual("d:/ymir work/ui/public/Large_Button_03.sub")
		self.FlagButton.SetText("Change Flag")
		self.FlagButton.SetEvent(self.__OpenFlagUpload)
		self.FlagButton.Show()
		
		self.itemImage = ui.ExpandedImageBox()
		self.itemImage.SetParent(self)
		self.itemImage.LoadImage("d:/ymir work/ui/language_flag/%s.tga" % (chr.GetLang()))
		self.itemImage.SetPosition(120, 50)
		self.itemImage.SetScale(5, 5)
		self.itemImage.Show()
				
	def __LoadLangCFG(self, lang):
		language = ""
		file = open("locale.cfg", "w")
		if lang == 1:
			file.write("10002 1252 en") 
			language = "English"
			net.SendChatPacket("/changegamelanguage en")
		elif lang == 2:
			file.write("10002 1252 it") 
			language = "Italian"
			net.SendChatPacket("/changegamelanguage it")
		elif lang == 3:
			file.write("10002 1252 de")
			language = "Deutsch"
			net.SendChatPacket("/changegamelanguage de")
		elif lang == 4:
			file.write("10002 1252 es") 
			language = "Espanish"
			net.SendChatPacket("/changegamelanguage es")
		elif lang == 5:
			file.write("10002 1250 ro") 
			language = "Romanian"	
			net.SendChatPacket("/changegamelanguage ro")
		elif lang == 6:
			file.write("10002 1254 tr") 
			language = "Turky"
			net.SendChatPacket("/changegamelanguage tr")
			
		file.close()
		dbg.LogBox("The laguage of client was changed to %s!" % (language))
		dbg.LogBox("Client need to be restarted.")
		self.Close()			
	
	def __OpenFlagUpload(self):
		self.flagSelectDialog = uiuploadflagcountry.FlagSelectDialog()
		self.flagSelectDialog.Open()
		#ret = net.UploadMark("upload/"+markFileName)
	
	def Close(self):
		self.Hide()
		self.flagSelectDialog = None

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE
		