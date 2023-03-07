import ui, app, net, constInfo, player
import datetime
import chat
import wndMgr
import localeInfo

from uiToolTip import ItemToolTip
IMG_DIR = "d:/ymir work/ui/game/event_calendar/"
IMG_ICON_DIR = "d:/ymir work/ui/game/event_calendar/icons/"
IMG_ICON_EX_DIR = "d:/ymir work/ui/game/event_calendar/icons/icons/"

events_default_data = {
	# img , eventName
	player.BONUS_EVENT:["bonus_event",""],
	player.DOUBLE_BOSS_LOOT_EVENT:["double_boss_loot_event",localeInfo.DOUBLE_BOSS_LOOT_EVENT],
	player.DOUBLE_METIN_LOOT_EVENT:["double_metin_loot_event", localeInfo.DOUBLE_METIN_LOOT_EVENT],
	player.DOUBLE_MISSION_BOOK_EVENT:["double_mission_book_event",localeInfo.DOUBLE_MISSION_BOOK_EVENT],
	player.DUNGEON_COOLDOWN_EVENT:["dungeon_cooldown_event",localeInfo.DUNGEON_COOLDOWN_EVENT],
	player.DUNGEON_TICKET_LOOT_EVENT:["dungeon_ticket_loot_event",localeInfo.DUNGEON_TICKET_LOOT_EVENT],
	player.EMPIRE_WAR_EVENT:["empire_war_event",""],
	player.MOONLIGHT_EVENT:["moonlight_event",localeInfo.MOONLIGHT_EVENT],
	player.TOURNAMENT_EVENT:["tournament_event",""],
	player.WHELL_OF_FORTUNE_EVENT:["whell_of_fortune_event",localeInfo.WHELL_OF_FORTUNE_EVENT],
	player.HALLOWEEN_EVENT:["halloween_event",localeInfo.HALLOWEEN_EVENT],
	player.NPC_SEARCH_EVENT:["npc_search",""],
}

class ImageBoxSpecial(ui.Window):
	imageList=[]
	waitingTime = 0.0
	sleepTime = 0.0
	alphaValue = 0.0
	increaseValue = 0.0
	minAlpha = 0.0
	maxAlpha = 0.0
	alphaStatus = False
	imageIndex = 0
	board=None
	img = None

	def Destroy(self):
		self.imageList=[]
		self.waitingTime = 0.0
		self.sleepTime = 0.0
		self.alphaValue = 0.0
		self.increaseValue = 0.0
		self.minAlpha = 0.0
		self.maxAlpha = 0.0
		self.alphaStatus = False
		self.imageIndex = 0
		self.board=None
		self.img = None

	def __init__(self):
		ui.Window.__init__(self)
		self.Destroy()

		self.waitingTime = 2.0
		self.alphaValue = 0.3
		self.increaseValue = 0.05
		self.minAlpha = 0.3
		self.maxAlpha = 1.0

	def SetBackgroundImage(self, image):
		if self.board == None:
			self.board = ui.ImageBox()
			self.board.SetParent(self)
		self.board.LoadImage(image)
		self.board.SAFE_SetStringEvent("MOUSE_OVER_IN",self.OverInItem)
		self.board.SAFE_SetStringEvent("MOUSE_OVER_OUT",self.OverOutItem)
		self.board.SetEvent(ui.__mem_func__(self.OnClick),"mouse_click")
		self.board.Show()
		self.SetSize(self.board.GetWidth(), self.board.GetHeight())

	def __del__(self):
		ui.Window.__del__(self)

	def SetImage(self, folder):
		(x, y) = (6,6)
		if self.board == None:
			if self.img == None:
				(x,y) = (wndMgr.GetScreenWidth()-289, 7)
			else:
				(x, y) = self.img.GetGlobalPosition()

		if self.img == None:
			img = ui.ImageBox()
			if self.board != None:
				img.SetParent(self.board)
			else:
				img.AddFlag("movable")
			img.SAFE_SetStringEvent("MOUSE_OVER_IN",self.OverInItem)
			img.SAFE_SetStringEvent("MOUSE_OVER_OUT",self.OverOutItem)
			img.SetMouseLeftButtonDoubleClickEvent(ui.__mem_func__(self.OnClick))
			#img.SetEvent(ui.__mem_func__(self.OnClick),"mouse_click")
			self.img = img


		self.img.LoadImage(folder)
		self.img.SetPosition(x, y)
		self.img.Show()

	def OnClick(self):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			if self.board == None:
				interface.OpenEventCalendar()
			else:
				if interface.wndEventManager:
					interface.wndEventManager.OnClick(self.dayIndex)

	def OverOutItem(self):
		if self.board == None:
			return

		interface = constInfo.GetInterfaceInstance()
		if interface:
			if interface.tooltipItem:
				interface.tooltipItem.HideToolTip()

	def OverInItem(self):
		if self.board == None:
			return
		interface = constInfo.GetInterfaceInstance()
		if interface:
			if interface.wndEventManager:
				interface.wndEventManager.OverInItem(self.dayIndex)

	def Clear(self):
		self.img = None
		self.imageList = []

	def DeleteImage(self, imgIndex):
		del self.imageList[imgIndex]

	def LoadImage(self, folder):
		if folder in self.imageList:
			return
		self.imageList.append(folder)
		if self.img == None:
			self.SetImage(folder)

	def GetNextImage(self, listIndex):
		if listIndex >= len(self.imageList):
			if len(self.imageList) > 0:
				return (0,self.imageList[0])
			return (0,"")
		return (listIndex, self.imageList[listIndex])

	def OnUpdate(self):
		if len(self.imageList) <= 1:
			self.imageIndex=0
			return
		elif self.sleepTime > app.GetTime():
			return
		if self.alphaStatus == True:
			self.alphaValue -= self.increaseValue
			if self.alphaValue < self.minAlpha:
				self.alphaValue = self.minAlpha
				self.alphaStatus = False
				(imageIndex, imageFolder) = self.GetNextImage(self.imageIndex+1)
				if imageFolder != "":
					self.SetImage(imageFolder)
				self.imageIndex = imageIndex
		else:
			self.alphaValue += self.increaseValue
			if self.alphaValue > self.maxAlpha:
				self.alphaStatus = True
				self.sleepTime = app.GetTime()+self.waitingTime
		if self.img != None:
			self.img.SetAlpha(self.alphaValue)

class EventCalendarWindow(ui.BoardWithTitleBar):
	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)
	def Destroy(self):
		self.children = {}
		self.eventData = {}
		self.realMonth =0
		self.realYear = 0
		self.dayCountinThisMounth=0
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.Destroy()
		self.LoadWindow()

	def CalculateDayCount(self, month, year):
		if month == 2:
			if ((year%400==0) or (year%4==0 and year%100!=0)):
				return 29
			else:
				return 28
		elif month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month==12:
			return 31
		else:
			return 30

	def GetMonthName(self, monthIndex):
		monthName = {
			1:localeInfo.EVENT_MONTH_1,
			2:localeInfo.EVENT_MONTH_2,
			3:localeInfo.EVENT_MONTH_3,
			4:localeInfo.EVENT_MONTH_4,
			5:localeInfo.EVENT_MONTH_5,
			6:localeInfo.EVENT_MONTH_6,
			7:localeInfo.EVENT_MONTH_7,
			8:localeInfo.EVENT_MONTH_8,
			9:localeInfo.EVENT_MONTH_9,
			10:localeInfo.EVENT_MONTH_10,
			11:localeInfo.EVENT_MONTH_11,
			12:localeInfo.EVENT_MONTH_12
		}
		if monthName.has_key(monthIndex):
			return monthName[monthIndex]
		return "None"

	def LoadWindow(self):
		board = ui.ImageBox()
		board.SetParent(self)
		board.AddFlag("not_pick")
		board.LoadImage(IMG_DIR+"board.tga")
		board.SetPosition(8, 28)
		board.Show()
		self.children["board"] = board

		dt = datetime.datetime.today()
		self.realMonth = dt.month
		self.realYear = dt.year
		self.dayCountinThisMounth = self.CalculateDayCount(dt.month, dt.year)

		self.SetSize(8+board.GetWidth()+8, 294)
		self.AddFlag("attach")
		self.AddFlag("movable")
		self.AddFlag("float")
		self.AddFlag("animate")
		self.SetTitleName(localeInfo.EVENT_MANAGER_WINDOW_TITLE % (self.GetMonthName(dt.month),dt.year))
		self.SetCloseEvent(self.Close)
		self.SetCenterPosition()

		self.LoadCalendarDay(self.dayCountinThisMounth)

	def LoadCalendarDay(self, dayCount):
		if not self.children.has_key("board"):
			return
		board = self.children["board"]

		for day in xrange(dayCount):
			yCalculate = day/8
			xCalculate = day-(yCalculate*8)

			dayImages = ImageBoxSpecial()
			dayImages.SetParent(board)
			dayImages.SetBackgroundImage(IMG_DIR+"board_black_item.tga")
			dayImages.AddFlag("not_pick")
			dayImages.SetPosition(8 + (xCalculate*66),8+(yCalculate*62))
			dayImages.dayIndex = day+1
			dayImages.Show()
			self.children["dayImages%d"%day] = dayImages

			dayIndex = ui.NumberLine()
			dayIndex.SetParent(dayImages)
			dayIndex.SetNumber(str(day+1))
			dayIndex.SetPosition(8,8)
			dayIndex.Show()
			self.children["dayIndex%d"%day] = dayIndex

	def ClearEventData(self):
		self.eventData = {}
		for day in xrange(self.dayCountinThisMounth):
			if self.children.has_key("dayImages%d"%day):
				self.children["dayImages%d"%day].Clear()

	def Open(self):
		if len(self.eventData) == 0:
			self.ClearEventData()
			net.SendChatPacket("/event_manager")
		self.Show()
		self.SetTop()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def AppendEvent(self, dayIndex, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3):
		if not self.eventData.has_key(dayIndex):
			self.eventData[dayIndex] = []
		self.eventData[dayIndex].append([dayIndex, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3])
		if self.children.has_key("dayImages%d"%(dayIndex-1)):
			self.children["dayImages%d"%(dayIndex-1)].LoadImage(IMG_ICON_DIR+events_default_data[eventIndex][0]+".tga")

	def textToColorFull(self, text):
		return localeInfo.EVENT_COLORFULL_TEXT % text

	def GetBonusName(self, affect, value):
		return ItemToolTip.AFFECT_DICT[affect](value)

	def CalculateTime(self, eventIndex, startTime, endTime):
		if eventIndex == player.TOURNAMENT_EVENT:
			startTimeSecond = startTime.split(" ")[1]
			return localeInfo.PVP_EVENT_TIME % self.textToColorFull(startTimeSecond)

		startTimeFirst = startTime.split(" ")[0]
		startTimeSecond = startTime.split(" ")[1]

		endTimeFirst = endTime.split(" ")[0]
		endTimeSecond = endTime.split(" ")[1]

		beginTimeText = ""
		endTimeText = ""

		if startTimeFirst != endTimeFirst:
			beginTimeText += startTimeFirst.split("-")[2]+"/"+startTimeFirst.split("-")[1]
			beginTimeText+=" "
			endTimeText += endTimeFirst.split("-")[2]+"/"+endTimeFirst.split("-")[1]
			endTimeText+=" "

		beginTimeText+=startTimeSecond
		endTimeText+=endTimeSecond
		return localeInfo.NORMAL_EVENT_TIME % (self.textToColorFull(beginTimeText),self.textToColorFull(endTimeText))


	def GetMapName(self, mapIndex):
		mapNames = {
			61:localeInfo.MOUNT_SOHAN_MAP_NAME,
			62:localeInfo.MOUNT_DOYUMHWAN_MAP_NAME,
			63:localeInfo.MOUNT_YONGBI_MAP_NAME,
		}
		if mapNames.has_key(mapIndex):
			return mapNames[mapIndex]
		return ""

	def OverInItem(self, dayIndex):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			tooltipItem = interface.tooltipItem
			if tooltipItem:
				tooltipItem.ClearToolTip()
				tooltipItem.ShowToolTip()
				tooltipItem.AppendTextLine(localeInfo.EVENT_TOOLTIP_TITLE % self.textToColorFull("%04d-%02d-%02d" % (int(self.realYear), int(self.realMonth), int(dayIndex))))
				tooltipItem.AppendSpace(5)
				if self.eventData.has_key(dayIndex):
					global events_default_data
					listofEvent = self.eventData[dayIndex]
					#[dayIndex, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3]
					for event in listofEvent:
						eventName=""
						if event[1] == player.BONUS_EVENT:
							empireTexts = [localeInfo.ALL_KINGDOMS,localeInfo.RED_KINGDOM, localeInfo.YELLOW_KINGDOM, localeInfo.BLUE_KINGDOM]
							if event[4] >= len(empireTexts):
								event[4] = 0
							eventName = empireTexts[event[4]]
							if event[6] > 0 and event[7] > 0:
								eventName+=" "
								eventName+=self.textToColorFull(self.GetBonusName(event[6],event[7]))
							else:
								eventName+=localeInfo.NONE_AFFECT

						elif event[1] == player.EMPIRE_WAR_EVENT:
							eventName = self.textToColorFull(localeInfo.EMPIRE_WAR_EVENT % (event[6],event[7]))

						elif event[1] == player.TOURNAMENT_EVENT:
							warType = [localeInfo.TOURNAMENT_ALL_CHARACTER, localeInfo.CHARACTER_WARRIOR, localeInfo.CHARACTER_ASSASSIN,localeInfo.CHARACTER_SURA, localeInfo.CHARACTER_SHAMAN]
							if event[6] >= len(warType):
								event[6] = 0
							eventName = self.textToColorFull(localeInfo.TOURNAMENT_EVENT % (warType[event[6]], event[7], event[8]))

						elif event[1] == player.NPC_SEARCH_EVENT:
							tooltipItem.AppendTextLine(self.textToColorFull(localeInfo.NPC_SEARCH))
							tooltipItem.AppendTextLine(self.textToColorFull(localeInfo.NPC_SEARCH_TEXT))
							for j in xrange(4):
								if event[6+j] > 0:
									tooltipItem.AppendTextLine(self.textToColorFull(self.GetMapName(event[6+j])))
							tooltipItem.AppendTextLine(self.CalculateTime(event[1],event[2],event[3]))
							tooltipItem.AppendSpace(5)
							continue
						else:
							eventName = self.textToColorFull(events_default_data[event[1]][1])

						tooltipItem.AppendTextLine(eventName)
						tooltipItem.AppendTextLine(self.CalculateTime(event[1],event[2],event[3]))
						tooltipItem.AppendSpace(5)
				else:
					tooltipItem.AppendTextLine(localeInfo.EVENT_TOOLTIP_DOESNT_HAVE_EVENT,interface.tooltipItem.NEGATIVE_COLOR)

	def OnClick(self, dayIndex):
		pass

class MovableImage(ImageBoxSpecial):
	timeText = None
	def __del__(self):
		ImageBoxSpecial.__del__(self)
	def __init__(self):
		self.Destroy()
		ImageBoxSpecial.__init__(self)
		self.AddFlag("attach")
		self.AddFlag("movable")
		self.AddFlag("float")
		self.timeText = ui.TextLine()
		self.timeText.SetParent(self)
		self.timeText.SetPosition(self.GetWidth()+5, self.GetHeight()+5)
		self.timeText.Show()
		self.dayIndex = 0
	def Destroy(self):
		if self.img != None:
			self.img.Hide()
		self.eventCache = []
		self.timeList = []
		self.textLine = None
		ImageBoxSpecial.Destroy(self)
	def LoadTime(self, eventIndex, startTime, endTime, isAlreadyStart):
		self.LoadImage(IMG_ICON_EX_DIR+events_default_data[eventIndex][0]+".tga")
		self.timeList.append([startTime, endTime, isAlreadyStart])
		self.Show()
	def CheckCacheEvent(self):
		if len(self.eventCache) == 0:
			return
		clientGlobalTime = app.GetGlobalTimeStamp()
		for j in xrange(len(self.eventCache)):
			startTime = self.eventCache[j][1]-clientGlobalTime
			endTime = self.eventCache[j][2]-clientGlobalTime
			if startTime <= 0 and endTime <= 0:
				del self.eventCache[j]
				break
			elif startTime >= 0 and startTime <= (60*30):
				self.LoadTime(self.eventCache[j][0], clientGlobalTime+startTime, clientGlobalTime+endTime, 0)
				del self.eventCache[j]
				break
			elif startTime <= 0 and endTime >= 0:
				self.LoadTime(self.eventCache[j][0], 0, clientGlobalTime+endTime, 1)
				del self.eventCache[j]
				break
	def AppendEvent(self, eventIndex, startTime, endTime, isAlreadyStart):
		clientGlobalTime = app.GetGlobalTimeStamp()
		if startTime <= 0 and endTime <= 0:
			return
		elif startTime >= 0 and startTime <= (60*30):
			self.LoadTime(eventIndex, clientGlobalTime+startTime, clientGlobalTime+endTime, 0)
		elif startTime <= 0 and endTime >= 0:
			self.LoadTime(eventIndex, 0, clientGlobalTime+endTime, 1)
		else:
			self.eventCache.append([eventIndex, startTime+clientGlobalTime, endTime+clientGlobalTime, isAlreadyStart])
	def DeleteEvent(self, index):
		self.DeleteImage(index)
		del self.timeList[index]
		if len(self.timeList) == 0:
			self.Hide()
	def Show(self):
		ImageBoxSpecial.Show(self)
		if self.timeText != None:
			self.timeText.Show()
		if self.img != None:
			self.img.Show()
	def Hide(self):
		ImageBoxSpecial.Hide(self)
		if self.timeText != None:
			self.timeText.Hide()
		if self.img != None:
			self.img.Hide()
	def FormatTime(self, seconds):
		if seconds == 0:
			return ""
		m, s = divmod(seconds, 60)
		h, m = divmod(m, 60)
		return "%02d:%02d:%02d" % (h, m, s)
	def OnUpdate(self):
		ImageBoxSpecial.OnUpdate(self)
		self.CheckCacheEvent()
		if self.img != None:
			(x,y) = self.img.GetLocalPosition()
			self.timeText.SetPosition(x+self.img.GetWidth()-60,y+self.img.GetHeight()+5)
		if self.imageIndex < len(self.timeList):
			timeData = self.timeList[self.imageIndex]
			if timeData[2]:
				leftTime = timeData[1] - app.GetGlobalTimeStamp()
				if leftTime <= 0:
					self.DeleteEvent(self.imageIndex)
					self.imageIndex = 0
					self.alphaValue = self.minAlpha
					self.alphaStatus = False
					(imageIndex, imageFolder) = self.GetNextImage(self.imageIndex+1)
					if imageFolder != "":
						self.SetImage(imageFolder)
					return
				else:
					self.timeText.SetText("Se terminã în %s"%self.FormatTime(leftTime))
			else:
				leftTime = timeData[0] - app.GetGlobalTimeStamp()
				if leftTime <= 0:
					timeData[2] = 1
					return
				else:
					self.timeText.SetText("Începe în %s"%self.FormatTime(leftTime))
