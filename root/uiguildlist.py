import ui, app, net

IMG_DIR = "d:/ymir work/ui/game/guildlist/"

BOARD_WIDTH = 266
BOARD_HEIGHT = 250

def sortIndex(data):
  return data[2]

class GuildOnlineList(ui.BoardWithTitleBar):
	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.children = {}
		self.Destroy()
		self.LoadWindow()
	def Destroy(self):
		if self.children.has_key("listbox"):
			self.children["listbox"].RemoveAllItems()
			self.children["listbox"]=None
		self.children = {}

	def LoadWindow(self):
		#self.AddFlag("attach")
		self.AddFlag("float")
		#self.AddFlag("movable")

		self.SetTitleName("Lista breasla online")

		wpEx = ui.ThinBoard()
		wpEx.SetParent(self)
		wpEx.SetPosition(6,30)
		wpEx.SetSize(BOARD_WIDTH,BOARD_HEIGHT)
		wpEx.Show()
		self.children["wpEx"]=wpEx
		self.SetSize(wpEx.GetWidth()+13,wpEx.GetHeight()+38)
		self.SetCenterPosition()

		wp = ui.ThinBoardCircle()
		wp.SetParent(wpEx)
		wp.SetPosition(6,6)
		wp.SetSize(wpEx.GetWidth()-12,wpEx.GetHeight()-10)
		wp.SetAlpha(0.6)
		wp.Show()
		self.children["wp"]=wp

		editLineSlot = ui.SlotBar()
		editLineSlot.SetParent(wp)
		editLineSlot.SetPosition(5,5)
		editLineSlot.SetSize(wp.GetWidth()-10,21)
		editLineSlot.Show()
		self.children["editLineSlot"]=editLineSlot

		editLine = ui.EditLine()
		editLine.SetParent(editLineSlot)
		editLine.SetPosition(2,3)
		editLine.SetSize(editLineSlot.GetWidth(),editLineSlot.GetHeight())
		editLine.SetOverlayText("Cãutaþi o anumitã breaslã...")
		editLine.SetMax(15)
		editLine.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
		editLine.OnPressEscapeKey = ui.__mem_func__(self.Hide)
		editLine.Show()
		self.children["editLine"] = editLine

		scrollBar = Scrollbar()
		scrollBar.SetParent(wp)
		scrollBar.SetPosition(wp.GetWidth()-scrollBar.GetWidth()+3,5+editLineSlot.GetHeight()+2)
		scrollBar.SetScrollBarSize(editLineSlot.GetWidth()-scrollBar.GetWidth()-20)
		scrollBar.Show()
		self.children["scrollBar"] = scrollBar

		listbox = ui.ListBoxEx()
		listbox.SetParent(wp)
		listbox.SetSize(240,wp.GetHeight()-(editLineSlot.GetHeight()+10))
		listbox.SetPosition(5,5+editLineSlot.GetHeight()+5)
		listbox.SetItemSize(240,21)
		listbox.SetItemStep(24)
		listbox.SetViewItemCount(8)
		listbox.SetScrollBar(scrollBar)
		listbox.Show()
		self.children["listbox"] = listbox

		loadImage = ui.ExpandedImageBox()
		loadImage.SetParent(wp)
		loadImage.LoadImage(IMG_DIR+"load_.tga")
		loadImage.SetPosition(wp.GetWidth()/2,wp.GetHeight()/2)
		self.children["loadImage"] = loadImage

	def AppendWithSort(self, sortList):
		if len(sortList) == 0:
			return
		#sortList.sort(key=sortIndex)
		sortList.sort(reverse=True, key=sortIndex)
		for newIndex in sortList:
			self.AppendItem(newIndex[0], newIndex[1],newIndex[2])

	def __OnValueUpdate(self):
		textLine = self.children["editLine"]
		ui.EditLine.OnIMEUpdate(textLine)
		input_text = textLine.GetText().lower()
		self.ClearAllData()
		if len(input_text) > 0:
			if self.children.has_key("data"):
				sortList =[]
				for key, data in self.children["data"].items():
					if data[0].lower().find(input_text) != -1:
						sortList.append([key, data[0],data[1]])
						#self.AppendItem(key, data[0],data[1])
				self.AppendWithSort(sortList)
		else:
			self.AppendAllItem()

	def AppendAllItem(self):
		sortList =[]
		if self.children.has_key("data"):
			for key, data in self.children["data"].items():
				#self.AppendItem(key, data[0],data[1])
				sortList.append([key, data[0],data[1]])
		self.AppendWithSort(sortList)

	def Open(self):
		if not self.children.has_key("serverPacket"):
			self.children["serverPacket"] = False
			self.ClearAllData()
			self.children["loadImage"].Show()
			net.SendChatPacket("/guildlist load")
		self.Show()

	def ClearAllData(self):
		self.children["loadImage"].Hide()
		self.children["listbox"].RemoveAllItems()

	def SetData(self, guildID, guildNameText, masterOnline):
		if not self.children.has_key("data"):
			self.children["data"] = {}
		self.children["data"][guildID]=[guildNameText,masterOnline]
		self.CheckGuildItem(guildID, guildNameText, masterOnline)

	def CheckGuildItem(self, guildID, guildNameText, masterOnline):
		listData = self.children["listbox"].itemList
		for guildItem in listData:
			if guildItem.guildID == guildID:
				guildItem.masterOnline = masterOnline
				if masterOnline:
					guildItem.onlineImg.LoadImage(IMG_DIR+"online.tga")
				else:
					guildItem.onlineImg.LoadImage(IMG_DIR+"offline.tga")
				self.ClearAllData()
				self.AppendAllItem()
				return
		self.AppendItem(guildID, guildNameText, masterOnline)

		self.ClearAllData()
		self.AppendAllItem()

	def AppendItem(self, guildID, guildNameText, masterOnline):
		itemImage = ui.ImageBox()
		itemImage.LoadImage(IMG_DIR+"item.tga")
		itemImage.guildID = guildID
		itemImage.guildNameText = guildNameText
		itemImage.masterOnline = masterOnline
		itemImage.Show()

		guildName = ui.TextLine()
		guildName.SetParent(itemImage)
		guildName.SetPosition(150,4)
		guildName.SetHorizontalAlignCenter()
		guildName.SetText(str(guildNameText))
		guildName.SetOutline()
		guildName.Show()
		itemImage.guildName = guildName

		onlineImg = ui.ImageBox()
		onlineImg.SetParent(itemImage)
		onlineImg.SetPosition(23,4)
		if masterOnline:
			onlineImg.LoadImage(IMG_DIR+"online.tga")
		else:
			onlineImg.LoadImage(IMG_DIR+"offline.tga")
		onlineImg.Show()
		itemImage.onlineImg = onlineImg
		self.children["listbox"].AppendItem(itemImage)

	def OnUpdate(self):
		if self.children.has_key("loadImage"):
			if self.children["loadImage"].IsShow():
				rotationIndex = 0
				if not self.children.has_key("rotationIndex"):
					self.children["rotationIndex"] = 0
				else:
					rotationIndex = self.children["rotationIndex"]+15
					self.children["rotationIndex"] = rotationIndex
				self.children["loadImage"].SetRotation(rotationIndex)

	def OnPressEscapeKey(self):
		self.Hide()
		return True

class Scrollbar(ui.Window):
	SCROLLBAR_WIDTH = 13
	SCROLLBAR_MIDDLE_HEIGHT = 1
	SCROLLBAR_BUTTON_WIDTH = 17
	SCROLLBAR_BUTTON_HEIGHT = 17
	SCROLL_BTN_XDIST = 2
	SCROLL_BTN_YDIST = 2
	class MiddleBar(ui.DragButton):
		def __init__(self):
			ui.DragButton.__init__(self)
			self.AddFlag("movable")
			self.SetWindowName("scrollbar_middlebar")
		def MakeImage(self):
			top = ui.ExpandedImageBox()
			top.SetParent(self)
			top.LoadImage(IMG_DIR+"scrollbar/scroll_top.tga")
			top.AddFlag("not_pick")
			top.Show()
			bottom = ui.ExpandedImageBox()
			bottom.SetParent(self)
			bottom.LoadImage(IMG_DIR+"scrollbar/scroll_buttom.tga")
			bottom.AddFlag("not_pick")
			bottom.Show()
			middle = ui.ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage(IMG_DIR+"scrollbar/scroll_mid.tga")
			middle.AddFlag("not_pick")
			middle.Show()
			self.top = top
			self.bottom = bottom
			self.middle = middle
		def SetSize(self, height):
			minHeight = self.top.GetHeight() + self.bottom.GetHeight() + self.middle.GetHeight()
			height = max(minHeight, height)
			ui.DragButton.SetSize(self, 10, height)
			scale = (height - minHeight) / 2 
			extraScale = 0
			if (height - minHeight) % 2 == 1:
				extraScale = 1
			self.middle.SetPosition(0, self.top.GetHeight() + scale)
			self.bottom.SetPosition(0, height - self.bottom.GetHeight())
	def __init__(self):
		ui.Window.__init__(self)
		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = None
		self.eventArgs = None
		self.lockFlag = False
		self.CreateScrollBar()
		self.SetScrollBarSize(0)
		self.scrollStep = 0.09
		self.SetWindowName("NONAME_ScrollBar")
	def __del__(self):
		ui.Window.__del__(self)
	def CreateScrollBar(self):
		topImage = ui.ExpandedImageBox()
		topImage.SetParent(self)
		topImage.AddFlag("not_pick")
		topImage.LoadImage(IMG_DIR+"scrollbar/scrollbar_top.tga")
		topImage.Show()
		bottomImage = ui.ExpandedImageBox()
		bottomImage.SetParent(self)
		bottomImage.AddFlag("not_pick")
		bottomImage.LoadImage(IMG_DIR+"scrollbar/scrollbar_bottom.tga")
		bottomImage.Show()
		middleImage = ui.ExpandedImageBox()
		middleImage.SetParent(self)
		middleImage.AddFlag("not_pick")
		middleImage.SetPosition(0, topImage.GetHeight())
		middleImage.LoadImage(IMG_DIR+"scrollbar/scrollbar_middle.tga")
		middleImage.Show()
		self.topImage = topImage
		self.bottomImage = bottomImage
		self.middleImage = middleImage
		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(ui.__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.MakeImage()
		middleBar.SetSize(0) # set min height
		self.middleBar = middleBar
	def Destroy(self):
		self.eventScroll = None
		self.eventArgs = None
	def SetScrollEvent(self, event, *args):
		self.eventScroll = event
		self.eventArgs = args
	def SetMiddleBarSize(self, pageScale):
		self.middleBar.SetSize(int(pageScale * float(self.GetHeight() - self.SCROLL_BTN_YDIST*2)))
		realHeight = self.GetHeight() - self.SCROLL_BTN_YDIST*2 - self.middleBar.GetHeight()
		self.pageSize = realHeight
	def SetScrollBarSize(self, height):
		self.SetSize(self.SCROLLBAR_WIDTH, height)
		self.pageSize = height - self.SCROLL_BTN_YDIST*2 - self.middleBar.GetHeight()
		middleImageScale = float((height - self.SCROLL_BTN_YDIST*2) - self.middleImage.GetHeight()) / float(self.middleImage.GetHeight())
		self.middleImage.SetRenderingRect(0, 0, 0, middleImageScale)
		self.bottomImage.SetPosition(0, height - self.bottomImage.GetHeight())
		self.middleBar.SetRestrictMovementArea(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST, self.middleBar.GetWidth(), height - self.SCROLL_BTN_YDIST * 2)
		self.middleBar.SetPosition(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST)
	def SetScrollStep(self, step):
		self.scrollStep = step
	def GetScrollStep(self):
		return self.scrollStep
	def GetPos(self):
		return self.curPos
	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep)
	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep)
	def SetPos(self, pos, moveEvent = True):
		pos = max(0.0, pos)
		pos = min(1.0, pos)
		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.SCROLL_BTN_XDIST, int(newPos) + self.SCROLL_BTN_YDIST)
		if moveEvent == True:
			self.OnMove()
	def OnMove(self):
		if self.lockFlag:
			return
		if 0 == self.pageSize:
			return
		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal - self.SCROLL_BTN_YDIST) / float(self.pageSize)
		if self.eventScroll:
			apply(self.eventScroll, self.eventArgs)
	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		newPos = float(yMouseLocalPosition) / float(self.GetHeight())
		self.SetPos(newPos)
	def LockScroll(self):
		self.lockFlag = True
	def UnlockScroll(self):
		self.lockFlag = False