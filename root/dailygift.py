import ui
import uiScriptLocale, event, dbg, uiCommon, uiToolTip, item, localeInfo

import net
import app

class DailyGift(ui.Window):

	ITEMS = []
	CANTS = []
	
	def __init__(self):
		ui.Window.__init__(self)
		self.LoadWindow()

	def __del__(self):
		ui.Window.__del__(self)

	def Close(self):
		if self.board.IsShow():
			self.Show()

	def Show(self):
		if self.board.IsShow():
			self.board.Hide()
		else:
			self.board.Show()
			net.SendChatPacket("/daily_reward_reload")

	def LoadWindow(self):
		self.slots = {}
		self.daily = 0
		self.endTime = None

		self.board = ui.BoardWithTitleBar()
		self.board.SetSize(347, 640)
		self.board.SetCenterPosition()
		self.board.AddFlag("movable")
		self.board.AddFlag("float")
		self.board.AddFlag("animate")
		self.board.SetTitleName(uiScriptLocale.DAILY_REWARD01)
		self.board.SetCloseEvent(self.Close)
		self.board.Hide()
		
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.Hide()
		
		self.reward = ui.ImageBox()
		self.reward.SetParent(self.board)
		self.reward.SetPosition(8, 30)
		self.reward.LoadImage("d:/ymir work/ui/public/drakon2/dailygift/fundal3.tga")
		self.reward.Show()
		
		self.img = ui.ImageBox()
		self.img.SetParent(self.board)
		self.img.SetPosition(14, 35)
		self.img.LoadImage("d:/ymir work/ui/public/drakon2/dailygift/fundal.tga")
		self.img.Show()
		
		self.tab = ui.ImageBox()
		self.tab.SetParent(self.board)
		self.tab.SetPosition(333, 380)
		self.tab.LoadImage("d:/ymir work/ui/public/drakon2/dailygift/tab.tga")
		self.tab.Show()
		
		self.bg = {}
		for i in xrange(7): #7
			self.bg[i] = {}
			self.bg[i]["image"] = ui.ImageBox()
			self.bg[i]["image"].SetParent(self.board)
			self.bg[i]["image"].SetPosition(14, 50*i+120)
			self.bg[i]["image"].LoadImage("d:/ymir work/ui/public/drakon2/dailygift/fundal2.tga")
			self.bg[i]["image"].Show()

			self.bg[i]["text"] = ui.TextLine()
			self.bg[i]["text"].SetParent(self.bg[i]["image"])
			self.bg[i]["text"].SetPosition(5,14)
			self.bg[i]["text"].SetWindowHorizontalAlignLeft()
			self.bg[i]["text"].SetHorizontalAlignLeft()
			self.bg[i]["text"].SetText(uiScriptLocale.DAILY_REWARD02+" "+str(i+1))
			self.bg[i]["text"].Show()
			
			self.bg[i]["button"] = ui.Button()
			self.bg[i]["button"].SetParent(self.bg[i]["image"])
			self.bg[i]["button"].SetPosition(145,7)
			self.bg[i]["button"].SetUpVisual("d:/ymir work/ui/public/drakon2/button/1.tga")
			self.bg[i]["button"].SetOverVisual("d:/ymir work/ui/public/drakon2/button/2.tga")
			self.bg[i]["button"].SetDownVisual("d:/ymir work/ui/public/drakon2/button/3.tga")
			self.bg[i]["button"].SetDisableVisual("d:/ymir work/ui/public/drakon2/button/3.tga")
			# self.bg[i]["button"].SetText(uiScriptLocale.DAILY_REWARD03)
			self.bg[i]["button"].SetEvent(lambda x = i : self.GetReward(x))
			self.bg[i]["button"].Disable()
			self.bg[i]["button"].Show()
		
		self.items = ui.GridSlotWindow()
		self.items.SetParent(self.board)
		self.items.SetPosition(12, 490)
		self.items.ArrangeSlot(0,10,3,32,32,0,0)
		self.items.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.items.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.items.SetSlotBaseImage("d:/ymir work/ui/public/drakon2/inventory/slot.png",1.0,1.0,1.0,1.0)
		self.items.RefreshSlot()
		self.items.Show()

		self.text = {}
		self.pos = [[112,465], [-200+(32*10)+15,104]]
		for i in xrange(2):
			self.text[i] = ui.TextLine()
			self.text[i].SetParent(self.board)
			self.text[i].SetPosition(self.pos[i][0], self.pos[i][1])
			self.text[i].SetText((uiScriptLocale.DAILY_REWARD04,uiScriptLocale.DAILY_REWARD05)[i])
			self.text[i].Show()

		# self.SetDailyReward(1)
		# self.SetTime(app.GetGlobalTimeStamp()*100)

	def SetDailyReward(self, idx):
		self.daily = int(idx)
		self.bg[self.daily]["button"].Enable()

	def GetActualDailyReward(self):
		return self.daily

	def SetTime(self, time):
		self.endTime = int(time)
		if self.endTime > 0:
			time = self.endTime - app.GetGlobalTimeStamp()
			day = int(int((time / 60) / 60) / 24)
			leftTime = localeInfo.SecondToDHM(self.endTime - app.GetGlobalTimeStamp())
			text = " %s : %s" % (localeInfo.LEFT_TIME, leftTime)
			self.text[1].SetText(text)
		# else:
			# self.bg[self.GetActualDailyReward()]["button"].Enable()
	
	def CheckTime(self):
		if self.endTime != None:
			time = self.endTime - app.GetGlobalTimeStamp()
			day = int(int((time / 60) / 60) / 24)
			leftTime = localeInfo.SecondToDHM(self.endTime - app.GetGlobalTimeStamp())
			text = " (%s : %s)" % (localeInfo.LEFT_TIME, leftTime)
			self.text[1].SetText(text)
			# if self.endTime <= 0:
				# self.bg[self.GetActualDailyReward()]["button"].Enable()

	def DeleteRewards(self):
		for i in xrange(len(self.ITEMS)):
			self.items.SetItemSlot(i,0)
			self.slots[i] = 0
		self.ITEMS = []
		self.CANTS = []

	def SetReward(self, items, cant):
		self.ITEMS.append(int(items))
		self.CANTS.append(int(cant))

	def SetRewardDone(self):
		for i in xrange(len(self.ITEMS)):
			self.items.SetItemSlot(i,self.ITEMS[i], self.CANTS[i])
			self.slots[i] = self.ITEMS[i]

	def GetReward(self,x):
		for i in xrange(7):
			self.bg[i]["button"].Disable()
		net.SendChatPacket("/daily_reward_get_reward")
		net.SendChatPacket("/daily_reward_reload")

	def OverInItem(self, slot):
		self.tooltipItem.SetItemToolTip(self.slots[slot])
		
	def OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnUpdate(self):
		self.CheckTime()

# x=DailyGift().Show()