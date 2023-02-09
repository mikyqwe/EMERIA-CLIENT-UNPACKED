import dbg
import ui
import snd
import systemSetting
import net
import chat
import app
import localeInfo
import constInfo
import chrmgr
import background
import player
import musicInfo

import uiSelectMusic
import background

MUSIC_FILENAME_MAX_LEN = 25

blockMode = 0

#new
import app
import ui
import uiCommon
import uiToolTip
import mouseModule
import localeInfo
import constInfo
import net
import player
import item
import snd
import shop
import wndMgr
import chat
import chr
import constInfo
g_isEditingOfflineShop = False
#new

## Offline Shop Bank Dialog
class OfflineShopBankDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.updateTime = 0
		self.withdrawMoneyTime = 0
		self.LoadWindow()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/offlineshop_bankdialog.py")
		except:
			import exception
			exception.Abort("OfflineShopBankDialog.LoadWindow.LoadScript")
			
		try:
			self.Board = self.GetChild("Board")
			self.currentMoneyLine = self.GetChild("CurrentMoneyLine")
			self.currentMoneyLine3 = self.GetChild("CurrentMoneyLine2")
			self.currentMoneyLine4 = self.GetChild("CurrentMoneyLine3")
			self.currentMoneyLine5 = self.GetChild("CurrentMoneyLine4")
			self.currentMoneyLine6 = self.GetChild("CurrentMoneyLine5")
			self.currentMoneyLine2 = self.GetChild("CurrentMoneyLine6")
			self.currentMoneyLine7 = self.GetChild("CurrentMoneyLine7")
			self.currentMoneyLine8 = self.GetChild("CurrentMoneyLine8")
			self.currentMoneyLine9 = self.GetChild("CurrentMoneyLine9")
		#	self.requiredMoneyLine = self.GetChild("RequiredMoneyLine")
			self.WithdrawMoneyButton = self.GetChild("withdraw_button")
			self.refeshButton = self.GetChild("refesh_button")
		except:
			import exception
			exception.Abort("OfflineShopBankDialog.LoadWindow.BindObject")
			
		self.Board.SetCloseEvent(ui.__mem_func__(self.Close))
		self.refeshButton.SetEvent(ui.__mem_func__(self.umutkyenile))
		self.WithdrawMoneyButton.SetEvent(ui.__mem_func__(self.WithdrawMoney))
		
		
		
	def umutkyenile(self):
		if (app.GetTime() < self.withdrawMoneyTime + 5):
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Banka'dakileri tekrar Yenilemek icin 5 saniye beklemelisiniz.")
			return
		else:
			net.SendChatPacket('/umutk_bank_refresh')
			self.withdrawMoneyTime = app.GetTime()
			chat.AppendChat(chat.CHAT_TYPE_INFO, "|cffFFC125Banka Yenilendi.")
		
	def Close(self):
		self.currentMoneyLine.SetText("")
		self.currentMoneyLine2.SetText("")
		self.currentMoneyLine3.SetText("")
		self.currentMoneyLine4.SetText("")
		self.currentMoneyLine5.SetText("")
		self.currentMoneyLine6.SetText("")
		self.currentMoneyLine7.SetText("")
		self.currentMoneyLine8.SetText("")
		self.currentMoneyLine9.SetText("")
		self.Hide()
		
	def Open(self):
		self.SetCenterPosition()
		self.SetTop()

		self.currentMoneyLine.SetText(str(constInfo.weed_stone1) + " Kirmizi Ot")
		self.currentMoneyLine2.SetText(str(constInfo.gold_bar) + " 400'mlik bar")
		self.currentMoneyLine3.SetText(str(constInfo.weed_stone2) + " Mavi Ot")
		self.currentMoneyLine4.SetText(str(constInfo.weed_stone3) + " Yesil Ot")
		self.currentMoneyLine5.SetText(str(constInfo.weed_stone4) + " Mor Ot")
		self.currentMoneyLine6.SetText(str(constInfo.soul_stone) + " Ruh Tasi")
		self.currentMoneyLine7.SetText(str(constInfo.gold) + " Yang")
		self.currentMoneyLine8.SetText(str(constInfo.cheque) + " Won")
		self.currentMoneyLine9.SetText(str(constInfo.ep) + " EP ")
		self.Show()
		
		
	def WithdrawMoney(self):
		net.SendChatPacket('/withdraw_offline_shop_money')
		

	def OnUpdate(self):
		self.currentMoneyLine.SetText(str(constInfo.weed_stone1) + " Kirmizi Ot")
		self.currentMoneyLine2.SetText(str(constInfo.gold_bar) + " 400'mlik bar")
		self.currentMoneyLine3.SetText(str(constInfo.weed_stone2) + " Mavi Ot")
		self.currentMoneyLine4.SetText(str(constInfo.weed_stone3) + " Yesil Ot")
		self.currentMoneyLine5.SetText(str(constInfo.weed_stone4) + " Mor Ot")
		self.currentMoneyLine6.SetText(str(constInfo.soul_stone) + " Ruh Tasi")
		self.currentMoneyLine7.SetText(str(constInfo.gold) + " Yang")
		self.currentMoneyLine8.SetText(str(constInfo.cheque) + " Won")
		self.currentMoneyLine9.SetText(str(constInfo.ep) + " EP")

