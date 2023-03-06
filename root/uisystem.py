import net
import app
import ui
import uiOption
import uiChangeChannel
import channel
import uiSystemOption
import uiGameOption
import uiScriptLocale
import networkModule
import constInfo
import localeInfo
if app.ENABLE_PATCHNOTE_WINDOW:
	import uiPatchnotes

SYSTEM_MENU_FOR_PORTAL = False

class Component:
	def Button(self, parent, buttonName, tooltipText, x, y, func, UpVisual, OverVisual, DownVisual):
		button = ui.Button()
		if parent != None:
			button.SetParent(parent)
		button.SetPosition(x, y)
		button.SetUpVisual(UpVisual)
		button.SetOverVisual(OverVisual)
		button.SetDownVisual(DownVisual)
		button.SetText(buttonName)
		button.SetToolTipText(tooltipText)
		button.Show()
		button.SetEvent(func)
		return button

	def ToggleButton(self, parent, buttonName, tooltipText, x, y, funcUp, funcDown, UpVisual, OverVisual, DownVisual):
		button = ui.ToggleButton()
		if parent != None:
			button.SetParent(parent)
		button.SetPosition(x, y)
		button.SetUpVisual(UpVisual)
		button.SetOverVisual(OverVisual)
		button.SetDownVisual(DownVisual)
		button.SetText(buttonName)
		button.SetToolTipText(tooltipText)
		button.Show()
		button.SetToggleUpEvent(funcUp)
		button.SetToggleDownEvent(funcDown)
		return button

	def EditLine(self, parent, editlineText, x, y, width, heigh, max):
		SlotBar = ui.SlotBar()
		if parent != None:
			SlotBar.SetParent(parent)
		SlotBar.SetSize(width, heigh)
		SlotBar.SetPosition(x, y)
		SlotBar.Show()
		Value = ui.EditLine()
		Value.SetParent(SlotBar)
		Value.SetSize(width, heigh)
		Value.SetPosition(1, 1)
		Value.SetMax(max)
		Value.SetLimitWidth(width)
		Value.SetMultiLine()
		Value.SetText(editlineText)
		Value.Show()
		return SlotBar, Value
		
	def EditLine2(self, parent, editlineText, x, y, width, heigh, max):
		SlotBar = ui.SlotBar()
		if parent != None:
			SlotBar.SetParent(parent)
		SlotBar.SetSize(width, heigh)
		SlotBar.SetPosition(x, y)
		SlotBar.Show()
		Value = ui.EditLine()
		Value.SetParent(SlotBar)
		Value.SetSize(width, heigh)
		Value.SetPosition(2, 2)
		Value.SetMax(210)
		Value.SetLimitWidth(width)
		Value.SetMultiLine()
		Value.SetText(editlineText)
		Value.Show()
		return SlotBar, Value

	def TextLine(self, parent, textlineText, x, y, color):
		textline = ui.TextLine()
		if parent != None:
			textline.SetParent(parent)
		textline.SetPosition(x, y)
		if color != None:
			textline.SetFontColor(color[0], color[1], color[2])
		textline.SetText(textlineText)
		textline.Show()
		return textline

	def RGB(self, r, g, b):
		return (r*255, g*255, b*255)

	def SliderBar(self, parent, sliderPos, func, x, y):
		Slider = ui.SliderBar()
		if parent != None:
			Slider.SetParent(parent)
		Slider.SetPosition(x, y)
		Slider.SetSliderPos(sliderPos / 100)
		Slider.Show()
		Slider.SetEvent(func)
		return Slider

	def ExpandedImage(self, parent, x, y, img):
		image = ui.ExpandedImageBox()
		if parent != None:
			image.SetParent(parent)
		image.SetPosition(x, y)
		image.LoadImage(img)
		image.Show()
		return image

	def ComboBox(self, parent, text, x, y, width):
		combo = ui.ComboBox()
		if parent != None:
			combo.SetParent(parent)
		combo.SetPosition(x, y)
		combo.SetSize(width, 15)
		combo.SetCurrentItem(text)
		combo.Show()
		return combo

	def ThinBoard(self, parent, moveable, x, y, width, heigh, center):
		thin = ui.ThinBoard()
		if parent != None:
			thin.SetParent(parent)
		if moveable == TRUE:
			thin.AddFlag('movable')
			thin.AddFlag('float')
		thin.SetSize(width, heigh)
		thin.SetPosition(x, y)
		if center == TRUE:
			thin.SetCenterPosition()
		thin.Show()
		return thin

	def Gauge(self, parent, width, color, x, y):
		gauge = ui.Gauge()
		if parent != None:
			gauge.SetParent(parent)
		gauge.SetPosition(x, y)
		gauge.MakeGauge(width, color)
		gauge.Show()
		return gauge

	def ListBoxEx(self, parent, x, y, width, heigh):
		bar = ui.Bar()
		if parent != None:
			bar.SetParent(parent)
		bar.SetPosition(x, y)
		bar.SetSize(width, heigh)
		bar.SetColor(0x77000000)
		bar.Show()
		ListBox=ui.ListBoxEx()
		ListBox.SetParent(bar)
		ListBox.SetPosition(0, 0)
		ListBox.SetSize(width, heigh)
		ListBox.Show()
		scroll = ui.ScrollBar()
		scroll.SetParent(ListBox)
		scroll.SetPosition(width-15, 0)
		scroll.SetScrollBarSize(heigh)
		scroll.Show()
		ListBox.SetScrollBar(scroll)
		return bar, ListBox

###################################################################################################
## System
class SystemDialog(ui.ScriptWindow):

	def __init__(self, stream):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.stream = stream

	def __Initialize(self):
		self.eventOpenHelpWindow = None
		self.systemOptionDlg = None
		self.gameOptionDlg = None
		self.channelSwitch = None
		if app.ENABLE_PATCHNOTE_WINDOW:
			self.wndPatchNotes = None

	def LoadDialog(self):
		if SYSTEM_MENU_FOR_PORTAL:
			self.__LoadSystemMenu_ForPortal()
		else:
			self.__LoadSystemMenu_Default()

	def __LoadSystemMenu_Default(self):
		pyScrLoader = ui.PythonScriptLoader()
		if constInfo.IN_GAME_SHOP_ENABLE:
			pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "SystemDialog.py")
		else:
			pyScrLoader.LoadScriptFile(self, "uiscript/systemdialog.py")

		self.GetChild("change_ch_button").SAFE_SetEvent(self.__ClickChangeChannelButton)
		self.GetChild("system_option_button").SAFE_SetEvent(self.__ClickSystemOptionButton)
		self.GetChild("game_option_button").SAFE_SetEvent(self.__ClickGameOptionButton)
		self.GetChild("change_button").SAFE_SetEvent(self.__ClickChangeCharacterButton)
		self.GetChild("logout_button").SAFE_SetEvent(self.__ClickLogOutButton)
		self.GetChild("exit_button").SAFE_SetEvent(self.__ClickExitButton)
		self.GetChild("help_button").SAFE_SetEvent(self.__ClickHelpButton)
		self.GetChild("helptwo_button").SAFE_SetEvent(self.__ClickHelpTwoButton)
		self.GetChild("cancel_button").SAFE_SetEvent(self.Close)
		#if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
			#self.GetChild("language_button").SAFE_SetEvent(self.LanguageButton)
		if constInfo.IN_GAME_SHOP_ENABLE:
			self.GetChild("mall_button").SAFE_SetEvent(self.__ClickInGameShopButton)


	def __LoadSystemMenu_ForPortal(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/systemdialog_forportal.py")

		self.GetChild("system_option_button").SAFE_SetEvent(self.__ClickSystemOptionButton)
		self.GetChild("game_option_button").SAFE_SetEvent(self.__ClickGameOptionButton)
		self.GetChild("change_button").SAFE_SetEvent(self.__ClickChangeCharacterButton)
		self.GetChild("exit_button").SAFE_SetEvent(self.__ClickExitButton)
		self.GetChild("help_button").SAFE_SetEvent(self.__ClickHelpButton)
		self.GetChild("helptwo_button").SAFE_SetEvent(self.__ClickHelpTwoButton)
		self.GetChild("cancel_button").SAFE_SetEvent(self.Close)
		if app.ENABLE_PATCHNOTE_WINDOW:
			self.GetChild("patchnotes_button").SAFE_SetEvent(self.__ClickPatchnotesButton)

	def Destroy(self):
		self.ClearDictionary()

		if self.gameOptionDlg:
			self.gameOptionDlg.Destroy()

		if self.systemOptionDlg:
			self.systemOptionDlg.Destroy()
			
		if self.channelSwitch:
			self.channelSwitch.Destroy()

		self.__Initialize()

	def SetOpenHelpWindowEvent(self, event):
		self.eventOpenHelpWindow = event

	def OpenDialog(self):
		self.Show()

	def __ClickChangeCharacterButton(self):
		self.Close()
		net.ExitGame()

	def __ClickChangeChannelButton(self):
		self.Close()
		
		if not self.channelSwitch:
			self.channelSwitch = channel.Titan2_Channel_Changer()
			
		self.channelSwitch.Open()

	def __OnClosePopupDialog(self):
		self.popup = None

	def __ClickLogOutButton(self):
		if SYSTEM_MENU_FOR_PORTAL:
			if app.loggined:
				self.Close()
				net.ExitApplication()
			else:
				self.Close()
				net.LogOutGame()
		else:
			self.Close()
			net.LogOutGame()


	def __ClickExitButton(self):
		self.Close()
		net.ExitApplication()
	
	def __ClickSystemOptionButton(self):
		self.Close()

		if not self.systemOptionDlg:
			self.systemOptionDlg = uiSystemOption.OptionDialog()

		self.systemOptionDlg.Show()

	def __ClickGameOptionButton(self):
		self.Close()

		if not self.gameOptionDlg:
			self.gameOptionDlg = uiGameOption.OptionDialog()

		self.gameOptionDlg.Show()

	if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
		def LanguageButton(self):
			import multi
			self.MultiLang = multi.MultiLanguage()
			self.MultiLang.Open()
			self.Close()

	def __ClickHelpButton(self):
		self.Close()

		if None != self.eventOpenHelpWindow:
			self.eventOpenHelpWindow()

	def __ClickInGameShopButton(self):
		self.Close()
		net.SendChatPacket("/in_game_mall")

	def Close(self):
		self.Hide()
		return True

	def RefreshMobile(self):
		if self.gameOptionDlg:
			self.gameOptionDlg.RefreshMobile()
		#self.optionDialog.RefreshMobile()

	def OnMobileAuthority(self):
		if self.gameOptionDlg:
			self.gameOptionDlg.OnMobileAuthority()
		#self.optionDialog.OnMobileAuthority()

	def OnBlockMode(self, mode):
		uiGameOption.blockMode = mode
		if self.gameOptionDlg:
			self.gameOptionDlg.OnBlockMode(mode)
		#self.optionDialog.OnBlockMode(mode)

	def OnChangePKMode(self):
		if self.gameOptionDlg:
			self.gameOptionDlg.OnChangePKMode()
		#self.optionDialog.OnChangePKMode()

	def OnPressExitKey(self):
		self.Close()
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def __ClickHelpTwoButton(self):
		self.Close()
		import uiCommon
		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText("Vuoi aprire la finestra di report?")
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.ReportWindowOpen))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.ReportWindowEnd))
		questionDialog.Open()
		self.questionDialog = questionDialog
        
	def ReportWindowOpen(self):
		self.Close()
		self.questionDialog.Close()
		self.ReportLogin = ui.BoardWithTitleBar()
		self.ReportLogin.SetSize(400, 300)
		self.ReportLogin.SetCenterPosition()
		self.ReportLogin.AddFlag('float')
		self.ReportLogin.SetTitleName('Rapoarte')
		self.ReportLogin.SetCloseEvent(self.__ReportSend_FunctionsEND)
		self.ReportLogin.Show()
		self.comp = Component()

		self.send = self.comp.Button(self.ReportLogin, 'Trimite', '', 112, 202, self.__ReportSend_Functions, 'd:/ymir work/ui/public/XLarge_Button_01.sub', 'd:/ymir work/ui/public/XLarge_Button_02.sub', 'd:/ymir work/ui/public/XLarge_Button_03.sub')
		self.kurallar = self.comp.Button(self.ReportLogin, 'Regulament', '', 112, 232, self.__Kurallar, 'd:/ymir work/ui/public/XLarge_Button_01.sub', 'd:/ymir work/ui/public/XLarge_Button_02.sub', 'd:/ymir work/ui/public/XLarge_Button_03.sub')
		self.kapat = self.comp.Button(self.ReportLogin, 'Închide', ' ', 112, 262, self.WindowEND, 'd:/ymir work/ui/public/XLarge_Button_01.sub', 'd:/ymir work/ui/public/XLarge_Button_02.sub', 'd:/ymir work/ui/public/XLarge_Button_03.sub')
		self.slotbar_reports, self.report = self.comp.EditLine2(self.ReportLogin, '', 76, 105, 250, 75, 305)
		self.text = self.comp.TextLine(self.ReportLogin, 'Raportaþi orice eroare de jucãtor sau de joc aici.', 75, 45, self.comp.RGB(255, 255, 255))
		self.text2 = self.comp.TextLine(self.ReportLogin, 'Utilizarea incorectã a biletelor poate duce la interdicþie.', 75, 59, self.comp.RGB(255, 255, 255))
		self.text3 = self.comp.TextLine(self.ReportLogin, 'Scrieþi mesajul pe care doriþi sã-l trimiteþi echipei:', 95, 80, self.comp.RGB(255, 255, 255))
		
	def __ReportSend_Functions(self):
		import uiCommon
		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText("Sigur doriþi sã trimiteþi acest raport?")
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.__GonderButonunuOnayladim))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.__GonderButonunuOnaylamadim))
		questionDialog.Open()
		self.questionDialog = questionDialog
		
	def __GonderButonunuOnayladim(self):
		report = self.report.GetText()
		if report == "":
			self.Close()
			self.questionDialog.Close()
			import chat
			chat.AppendChat(chat.CHAT_TYPE_INFO, "[Emeria] > Nu este posibil sã anulaþi trimiterea mesajului.")
		elif len(report) < 30:
			self.Close()
			self.questionDialog.Close()
			import chat
			chat.AppendChat(chat.CHAT_TYPE_INFO, "[Emeria] > Lungimea mesajului trebuie sã fie între 30 ºi 120 de caractere.")
		else:
			self.Close()
			self.questionDialog.Close()
			self.ReportLogin.Hide()
			event.QuestButtonClick(constInfo.ReportLogin)
			constInfo.ReportEntered = report
			
	def __GonderButonunuOnaylamadim(self):
		self.Close()
		self.questionDialog.Close()
		
	def __ReportSend_FunctionsEND(self):
		import uiCommon
		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText("Doriþi sã închideþi fereastra de raport?")
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.__PencereyiKapatMesaji))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.__PencereyiKapatMesajiOnaylamadim))
		questionDialog.Open()
		self.questionDialog = questionDialog
		
	def __PencereyiKapatMesaji(self):
		self.Close()
		self.questionDialog.Close()
		self.ReportLogin.Hide()
		self.KurallarOpen.Hide()
		
	def __PencereyiKapatMesajiOnaylamadim(self):
		self.Close()
		self.questionDialog.Close()
	
	def __Kurallar(self):
		import uiCommon
		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText("Sigur vrei sã deschizi regulamentul?")
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.__KurallarPenceresiniAc))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.__KurallarPenceresiniKapa))
		questionDialog.Open()
		self.questionDialog = questionDialog
		
	def __KurallarPenceresiniAc(self):
		self.KurallarOpen = ui.BoardWithTitleBar()
		self.KurallarOpen.SetSize(370, 375)
		self.KurallarOpen.SetCenterPosition()
		self.KurallarOpen.AddFlag('float')
		self.KurallarOpen.SetTitleName('Regulament')
		self.KurallarOpen.SetCloseEvent(self.__Kurallar_END)
		self.KurallarOpen.Show()
		self.ReportLogin.Hide()
		self.comp2 = Component()
		
		self.send = self.comp2.Button(self.KurallarOpen, 'Înapoi', ' ', 98, 310, self.ReportWindowOpens, 'd:/ymir work/ui/public/XLarge_Button_01.sub', 'd:/ymir work/ui/public/XLarge_Button_02.sub', 'd:/ymir work/ui/public/XLarge_Button_03.sub')
		self.kapat = self.comp2.Button(self.KurallarOpen, 'Închide', ' ', 98, 340, self.WindowEND, 'd:/ymir work/ui/public/XLarge_Button_01.sub', 'd:/ymir work/ui/public/XLarge_Button_02.sub', 'd:/ymir work/ui/public/XLarge_Button_03.sub')
		self.text1 = self.comp2.TextLine(self.KurallarOpen, '1-) Raportul nu trebuie sã con?inã limbaj vulgar.', 17, 45, self.comp.RGB(255, 255, 255))
		self.text2 = self.comp2.TextLine(self.KurallarOpen, '2-) Trimiterea de rapoarte „inutile” paote fi pedepsitã cu ban.', 17, 59, self.comp.RGB(255, 255, 255))
		self.text3 = self.comp2.TextLine(self.KurallarOpen, '3-) Puteþi ataºa capturi de ecran la raport.', 17, 74, self.comp.RGB(255, 255, 255))
		self.text4 = self.comp2.TextLine(self.KurallarOpen, '4-) Solicitãrile de ban nu vor fi revizuite.', 17, 89, self.comp.RGB(255, 255, 255))
		self.text5 = self.comp2.TextLine(self.KurallarOpen, '5-) Raportul ar trebui utilizat numai pentru a raporta', 17, 104, self.comp.RGB(255, 255, 255))	
		self.text6 = self.comp2.TextLine(self.KurallarOpen, 'jucãtori (înºelãciune, comportament neadecvat) ºi erori de joc.', 17, 119, self.comp.RGB(255, 255, 255))
		self.text7 = self.comp2.TextLine(self.KurallarOpen, '6-) Fiecare ticket va fi vizualizat în 24 de ore.', 17, 134, self.comp.RGB(255, 255, 255))
		self.text8 = self.comp2.TextLine(self.KurallarOpen, '7-) Nu utilizaþi raportul pentru a solicita informaþii generale.', 17, 149, self.comp.RGB(255, 255, 255))
		self.text14 = self.comp2.TextLine(self.KurallarOpen, '', 17, 239, self.comp.RGB(255, 255, 255))
		self.text15 = self.comp2.TextLine(self.KurallarOpen, 'Multumim pentru vizionare,', 17, 254, self.comp.RGB(255, 255, 255))
		self.text16 = self.comp2.TextLine(self.KurallarOpen, 'echipa Emeria.', 17, 269, self.comp.RGB(255, 255, 255))
	
	def __KurallarPenceresiniKapa(self):
		self.Close()
		self.questionDialog.Close()
	
	def __Kurallar_END(self):
		import uiCommon
		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText("Doriþi sã închideþi fereastra de raport?")
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.__PencereyiKapatMesaji))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.__PencereyiKapatMesajiOnaylamadim))
		questionDialog.Open()
		self.questionDialog = questionDialog
		
	def __PencereyiKapatMesaji(self):
		self.Close()
		self.questionDialog.Close()
		self.ReportLogin.Hide()
		self.KurallarOpen.Hide()
		
	def __PencereyiKapatMesajiOnaylamadim(self):
		self.Close()
		self.questionDialog.Close()
		
	def WindowEND(self):
		import uiCommon
		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText("Doriþi sã închideþi fereastra de raport?")
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.__PencereyiKapatMesaji))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.__PencereyiKapatMesajiOnaylamadim))
		questionDialog.Open()
		self.questionDialog = questionDialog
		
	def __PencereyiKapatMesaji(self):
		self.Close()
		self.questionDialog.Close()
		self.ReportLogin.Hide()
		self.KurallarOpen.Hide()
		
	def __PencereyiKapatMesajiOnaylamadim(self):
		self.Close()
		self.questionDialog.Close()

	def ReportWindowOpens(self):
		import app
		self.Close()
		self.questionDialog.Close()
		self.ReportLogin = ui.BoardWithTitleBar()
		self.ReportLogin.SetSize(400, 300)
		self.ReportLogin.SetCenterPosition()
		self.ReportLogin.AddFlag('float')
		self.ReportLogin.SetTitleName('Rapoarte')
		self.ReportLogin.SetCloseEvent(self.__ReportSend_FunctionsEND)
		self.ReportLogin.Show()
		self.KurallarOpen.Hide()
		self.comp = Component()

		self.send = self.comp.Button(self.ReportLogin, 'Trimite', '', 112, 202, self.__ReportSend_Functions, 'd:/ymir work/ui/public/XLarge_Button_01.sub', 'd:/ymir work/ui/public/XLarge_Button_02.sub', 'd:/ymir work/ui/public/XLarge_Button_03.sub')
		self.kurallar = self.comp.Button(self.ReportLogin, 'Regulament', '', 112, 232, self.__Kurallar, 'd:/ymir work/ui/public/XLarge_Button_01.sub', 'd:/ymir work/ui/public/XLarge_Button_02.sub', 'd:/ymir work/ui/public/XLarge_Button_03.sub')
		self.kapat = self.comp.Button(self.ReportLogin, 'Închide', ' ', 112, 262, self.WindowEND, 'd:/ymir work/ui/public/XLarge_Button_01.sub', 'd:/ymir work/ui/public/XLarge_Button_02.sub', 'd:/ymir work/ui/public/XLarge_Button_03.sub')
		self.slotbar_reports, self.report = self.comp.EditLine2(self.ReportLogin, '', 76, 105, 250, 75, 305)
		self.text = self.comp.TextLine(self.ReportLogin, 'Raportaþi orice eroare de jucãtor sau de joc aici.', 75, 45, self.comp.RGB(255, 255, 255))
		self.text2 = self.comp.TextLine(self.ReportLogin, 'Utilizarea incorectã a biletelor poate duce la ban.', 75, 59, self.comp.RGB(255, 255, 255))
		self.text3 = self.comp.TextLine(self.ReportLogin, 'Scrieþi mesajul pe care doriþi sã-l trimite?i echipei:', 95, 80, self.comp.RGB(255, 255, 255))

	def __ReportSend_Functions(self):
		import uiCommon
		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText("Sigur doriþi sã trimiteþi acest raport?")
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.__GonderButonunuOnayladim))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.__GonderButonunuOnaylamadim))
		questionDialog.Open()
		self.questionDialog = questionDialog
		
	def __GonderButonunuOnayladim(self):
		import event
		report = self.report.GetText()
		if report == "":
			self.Close()
			self.questionDialog.Close()
			import chat
			chat.AppendChat(chat.CHAT_TYPE_INFO, "[Emeria] > Nu este posibil sã anulaþi trimiterea mesajului.")
		elif len(report) < 30:
			self.Close()
			self.questionDialog.Close()
			import chat
			chat.AppendChat(chat.CHAT_TYPE_INFO, "[Emeria] > Lungimea mesajului trebuie sã fie între 30 ºi 120 de caractere")
		else:
			self.Close()
			self.questionDialog.Close()
			self.ReportLogin.Hide()
			event.QuestButtonClick(constInfo.ReportLogin)
			constInfo.ReportEntered = report
			
	def __GonderButonunuOnaylamadim(self):
		self.Close()
		self.questionDialog.Close()

	def __ReportSend_FunctionsEND(self):
		import uiCommon
		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText("Doriþi sã închideþi fereastra de raport?")
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.__PencereyiKapatMesaji))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.__PencereyiKapatMesajiOnaylamadim))
		questionDialog.Open()
		self.questionDialog = questionDialog
		
	def __PencereyiKapatMesaji(self):
		self.Close()
		self.questionDialog.Close()
		self.ReportLogin.Hide()
		self.KurallarOpen.Hide()
		
	def __PencereyiKapatMesajiOnaylamadim(self):
		self.Close()
		self.questionDialog.Close()

	def ReportWindowEnd(self):
		self.Close()
		self.questionDialog.Close()

	if app.ENABLE_PATCHNOTE_WINDOW:
		def __ClickPatchnotesButton(self):
			self.Close()
			self.wndPatchnotes = uiPatchnotes.PatchNoteWindow()
			self.wndPatchnotes.Show()
			self.wndPatchnotes.SetTop()

if __name__ == "__main__":

	import app
	import wndMgr
	import systemSetting
	import mouseModule
	import grp
	import ui
	import chr
	import background
	import player

	#wndMgr.SetOutlineFlag(True)

	app.SetMouseHandler(mouseModule.mouseController)
	app.SetHairColorEnable(True)
	wndMgr.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetScreenSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	app.Create("METIN2 CLOSED BETA", systemSetting.GetWidth(), systemSetting.GetHeight(), 1)
	mouseModule.mouseController.Create()


	wnd = SystemDialog()
	wnd.LoadDialog()
	wnd.Show()

	app.Loop()

