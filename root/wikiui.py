import ui, grp, dbg, uiWiki, chat
import chr
import localeInfo
import playersettingmodule
import item
import nonplayer
import player
import app
import renderTarget
import constInfo

IMG_DIR = "d:/ymir work/ui/game/wiki/"
IMG_DIR_CATEGORY = "d:/ymir work/ui/game/wiki/category/"

HIDE_Y_DIFFERENCE = 250

def calculateRect(curValue, maxValue):
	try:
		return -1.0 + float(curValue) / float(maxValue)
	except:
		return 0.0

def ChildToList(images, textLines, child):
	if isinstance(child, ui.ExpandedImageBox) or isinstance(child, ui.RenderTarget):
		images.append(child)
	elif isinstance(child, CategoryItem):
		images.append(child.children["directionIcon"])
		textLines.append(child.children["textLine"])
	elif isinstance(child, ui.TextLine) or isinstance(child, TextlineLink) or isinstance(child, ui.NumberLine) or isinstance(child, ScrollBarNew) or isinstance(child, CategorySubItem) or isinstance(child, HorizontalScrollBarNew):
		textLines.append(child)
	elif isinstance(child, ui.ToggleButton) or isinstance(child, ui.RadioButton):
		if child.ButtonText != None:
			if child.itsNeedDoubleRender and child.ButtonText.itsNeedDoubleRender == False:
				child.ButtonText.itsNeedDoubleRender = True
			textLines.append(child.ButtonText)
		images.append(child)
	elif isinstance(child, ui.SliderBar):
		if child.backGroundImage != None:
			if child.itsNeedDoubleRender and child.backGroundImage.itsNeedDoubleRender == False:
				child.backGroundImage.itsNeedDoubleRender = True

			images.append(child.backGroundImage)
		if child.cursor != None:
			if child.itsNeedDoubleRender and child.cursor.itsNeedDoubleRender == False:
				child.cursor.itsNeedDoubleRender = True
			images.append(child.cursor)
	return (textLines, images)

def RenderWindow(child, _wx, _wy, _height):
	(textLines,images) = ChildToList([], [], child)
	itsRendered = False
	topRender = 0
	bottomRender = 0

	for childItem in textLines:
		(_x,_y) = childItem.GetGlobalPosition()
		childHeight = childItem.GetHeight()
		if _y < _wy:
			if childItem.IsShow():
				childItem.Hide()
			continue
		
		if isinstance(childItem, ui.TextLine):
			if _y+childHeight > (_wy+_height-25):
				if childItem.IsShow():
					childItem.Hide()
				continue
		else:
			if _y+childHeight > (_wy+_height):
				if childItem.IsShow():
					childItem.Hide()
				continue

		if not childItem.IsShow():
			childItem.Show()

	for childItem in images:
		(_x,_y) = childItem.GetGlobalPosition()
		childHeight = childItem.GetHeight()
		if _y+childHeight < _wy-HIDE_Y_DIFFERENCE or _y > _wy+_height+HIDE_Y_DIFFERENCE:
			childItem.Hide()
			return

		if _y < _wy:
			topRender = _y-_wy
			itsRendered = True
		if _y+childHeight > (_wy+_height-15):
			bottomRender = (_wy+_height-15)-(_y+childHeight)
			itsRendered = True

		if itsRendered:
			childItem.SetRenderingRect(0,calculateRect(childHeight-abs(topRender), childHeight),0,calculateRect(childHeight-abs(bottomRender),childHeight))

		if not itsRendered and childItem.itsRendered:
			childItem.SetRenderingRect(0,0,0,0)

		if childItem.itsRendered != itsRendered:
			childItem.itsRendered = itsRendered

		if not childItem.IsShow():
			childItem.Show()

def RenderWindowMultiple(child, _wx, _wy, _height, _zx = 0, _zy = 0, _zheight = 0):
	(textLines,images) = ChildToList([], [], child)
	for childItem in textLines:
		(_x,_y) = childItem.GetGlobalPosition()
		childHeight = childItem.GetHeight()
		if _y < _wy or _y < _zy:
			if childItem.IsShow():
				childItem.Hide()
			continue
		
		if isinstance(childItem, ui.TextLine):
			if _y+childHeight > (_wy+_height-20) or (_y+childHeight > (_zy+_zheight) and _zy != 0):
				if childItem.IsShow():
					childItem.Hide()
				continue
		elif isinstance(childItem, HorizontalScrollBarNew):
			#if _y+childHeight > (_wy+_height-20) or (_y+childHeight > (_zy+_zheight) and _zy != 0):
			if _y+childHeight > (_wy+_height-20):
				if childItem.IsShow():
					childItem.Hide()
				continue
		else:
			if _y+childHeight > (_wy+_height) or (_y+childHeight > (_zy+_zheight) and _zy != 0):
				if childItem.IsShow():
					childItem.Hide()
				continue
		if not childItem.IsShow():
			childItem.Show()

	for childItem in images:
		(_x,_y) = childItem.GetGlobalPosition()
		childHeight = childItem.GetHeight()
		itsRendered = False
		topRender = 0
		bottomRender = 0
		if isinstance(child, uiWiki.ListBoxItemSpecial):
			if _y < _wy:
				topRender = _wy-_y
				itsRendered = True
			if _y+childHeight > (_wy+_height-1):
				bottomRender = (_wy+_height-1)-(_y+childHeight)
				itsRendered = True
			if itsRendered:
				childItem.SetRenderingRect(0,calculateRect(childHeight-abs(topRender), childHeight),0,calculateRect(childHeight-abs(bottomRender),childHeight))
		else:
			if _y < _zy and _zy != 0:
				topRender+=_zy-_y
				itsRendered = True
			if _y < _wy:
				topRender+=_wy-_y
				itsRendered = True
			_realY = _wy
			_realHeight = _height
			if _zy != 0:
				if _wy+_height > _zy+_zheight:
					_realY = _zy
					_realHeight = _zheight
			if _y+childHeight > (_realY+_realHeight-1):
				bottomRender = (_realY+_realHeight-1)-(_y+childHeight)
				itsRendered = True
			if itsRendered:
				childItem.SetRenderingRect(0,calculateRect(childHeight-abs(topRender), childHeight),0,calculateRect(childHeight-abs(bottomRender),childHeight))
		if not itsRendered and childItem.itsRendered:
			childItem.SetRenderingRect(0,0,0,0)
		if childItem.itsRendered != itsRendered:
			childItem.itsRendered = itsRendered

class CategoryList(ui.Window):
	class CategoryDefaultItem(ui.Window):
		def __del__(self):
			ui.Window.__del__(self)
		def Destroy(self):
			self.children={}
			self.id = 0
			self.parentId = 0
			self.offset = 0
			self.expanded = False
			self.event = None
			self.onCollapseEvent = None
			self.onExpandEvent = None
			self.parent = 0
			self.overLine = False
			self.itemList=[]
		def __init__(self):
			ui.Window.__init__(self)
			self.Destroy()
			self.id = -1
			self.parentId = -1
		def SetParent(self, parent):
			ui.Window.SetParent(self, parent)
			self.parent=ui.proxy(parent)
		def IsParent(self):
			return self.parentId == -1
		def IsExpanded(self):
			return self.expanded
		def Expand(self):
			self.expanded = True
			if self.onExpandEvent:
				self.onExpandEvent()
		def Collapse(self):
			self.expanded = False
			if self.onCollapseEvent:
				self.onCollapseEvent()
		def SetOnExpandEvent(self, event):
			self.onExpandEvent = event
		def SetOnCollapseEvent(self, event):
			self.onCollapseEvent = event
		def SetEvent(self, event):
			self.event = event
		def SetOffset(self, offset):
			self.offset = offset
		def GetOffset(self):
			return self.offset
		def OnSelect(self):
			if self.event:
				self.event()
			self.parent.SelectItem(self)
		def OnMouseLeftButtonDown(self):
			self.OnSelect()
	def __del__(self):
		ui.Window.__del__(self)
	def Destroy(self):
		self.scrollBar=None
		self.selectedItem = None
		self.itemList = []
	def __init__(self):
		ui.Window.__init__(self)
		self.Destroy()
	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(ui.__mem_func__(self.RefreshList))
		self.scrollBar=scrollBar
	def OnMouseWheel(self, nLen):
		if self.scrollBar:
			if nLen > 0:
				self.scrollBar.OnUp()
			else:
				self.scrollBar.OnDown()
			return True
		return False
	def GetSelectedItem(self):
		return self.selectedItem
	def SelectItem(self, selectedItem):
		self.selectedItem = selectedItem
		if selectedItem != None:
			try:
				if selectedItem.IsExpanded():
					selectedItem.Collapse()
				else:
					selectedItem.Expand()
			except:
				return
		self.RefreshList()
	def SetBasePos(self, basePos):
		self.basePos=basePos
		self.RefreshList()
	
	def ClearItem(self):
		self.selectedItem=None
		for j in xrange(len(self.itemList)):
			itemList = self.itemList[j].itemList
			for x in xrange(len(itemList)):
				itemList[x].Hide()
				itemList[x].Destroy()
			itemList=[]
		self.itemList=[]
		if self.scrollBar:
			self.scrollBar.SetPos(0)
		self.SetBasePos(0)

	def AppendItemList(self, categoryData):
		self.ClearItem()
		for categoryList in categoryData:
			categoryBtn = None
			if categoryList.has_key("item"):
				categoryBtn = categoryList["item"]
				categoryBtn.SetParent(self)
				if categoryList.has_key("children"):
					for _x in categoryList["children"]:
						childItems = _x["item"]
						childItems.SetParent(self)
						categoryBtn.itemList.append(childItems)
						if _x.has_key("children"):
							for _z in _x["children"]:
								childItemsLast = _z["item"]
								childItemsLast.SetParent(self)
								childItems.itemList.append(childItemsLast)
			if categoryBtn != None:
				self.itemList.append(categoryBtn)
		self.RefreshList()

	def RefreshDynamicPosition(self):
		y_pos = 0
		for j in xrange(len(self.itemList)):
			categoryBtn = self.itemList[j]
			categoryBtn.SetPosition(categoryBtn.GetOffset(), y_pos, True)
			y_pos +=categoryBtn.GetHeight()+1
			if categoryBtn.IsExpanded():
				for x in xrange(len(categoryBtn.itemList)):
					childItem = categoryBtn.itemList[x]
					childItem.SetPosition(childItem.GetOffset(), y_pos, True)
					childItem.Show()
					y_pos +=childItem.GetHeight()+1
					if childItem.IsExpanded():
						for z in xrange(len(childItem.itemList)):
							childItemLast = childItem.itemList[z]
							childItemLast.SetPosition(childItemLast.GetOffset(),  y_pos, True)
							childItemLast.Show()
							y_pos +=childItemLast.GetHeight()+1
		return y_pos

	def RefreshList(self):
		(screenSize, windowHeight) = (self.RefreshDynamicPosition(), self.GetHeight())
		basePos = 0

		scrollBar = self.scrollBar
		if screenSize > windowHeight and scrollBar != None:
			scrollLen = screenSize-windowHeight
			if scrollLen != 0:
				scrollLen += 10
			basePos = int(scrollBar.GetPos()*scrollLen)
			scrollBar.SetMiddleBarSize(float(windowHeight-5)/float(screenSize))
			scrollBar.Show()
			if scrollBar.middleBar.GetGlobalPosition()[1]+scrollBar.middleBar.GetHeight()-15 >= scrollBar.GetGlobalPosition()[1]+scrollBar.GetHeight():
				scrollBar.SetPos(0)
				self.SetBasePos(0)
				return
		else:
			self.scrollBar.Hide()

		(_wx,_wy) = self.GetGlobalPosition()
		_height = self.GetHeight()

		y_pos = 0
		for j in xrange(len(self.itemList)):
			categoryBtn = self.itemList[j]
			categoryBtn.SetPosition(categoryBtn.GetOffset(), categoryBtn.exPos[1]-basePos)
			RenderWindow(categoryBtn, _wx, _wy, _height)
			categoryBtn.Show()
			if categoryBtn.IsExpanded():
				for x in xrange(len(categoryBtn.itemList)):
					childItem = categoryBtn.itemList[x]
					childItem.SetPosition(childItem.GetOffset(), childItem.exPos[1]-basePos)
					RenderWindow(childItem, _wx, _wy, _height)
					childItem.Show()
					if childItem.IsExpanded():
						for z in xrange(len(childItem.itemList)):
							childItemLast = childItem.itemList[z]
							childItemLast.SetPosition(childItemLast.GetOffset(), childItemLast.exPos[1]-basePos)
							RenderWindow(childItemLast, _wx, _wy, _height)
							childItemLast.Show()
					else:
						for z in xrange(len(childItem.itemList)):
							childItem.itemList[z].Hide()
			else:
				for x in xrange(len(categoryBtn.itemList)):
					categoryBtn.itemList[x].Hide()
					for z in xrange(len(categoryBtn.itemList[x].itemList)):
						categoryBtn.itemList[x].itemList[z].Hide()

class CategoryItem(CategoryList.CategoryDefaultItem):
	def __del__(self):
		CategoryList.CategoryDefaultItem.__del__(self)
	def __init__(self, text):
		CategoryList.CategoryDefaultItem.__init__(self)
		directionIcon = ui.ExpandedImageBox()
		directionIcon.SetParent(self)
		directionIcon.AddFlag("not_pick")
		directionIcon.SetPosition(0,0)
		directionIcon.LoadImage(IMG_DIR +"plus.tga")
		directionIcon.Show()
		self.children["directionIcon"] = directionIcon
		textLine=ui.TextLine()
		textLine.SetParent(directionIcon)
		textLine.AddFlag("not_pick")
		textLine.SetPosition(0,1)
		textLine.SetWindowHorizontalAlignLeft()
		textLine.SetText("  "+text)
		textLine.Show()
		self.children["textLine"] = textLine
		self.SetOnExpandEvent(self.ExpandEvent)
		self.SetOnCollapseEvent(self.CollapseEvent)
		self.SetSize(100,20)
	def CollapseEvent(self):
		self.children["directionIcon"].LoadImage(IMG_DIR +"plus.tga")
		self.children["directionIcon"].Show()
	def ExpandEvent(self):
		self.children["directionIcon"].LoadImage(IMG_DIR +"minus.tga")
		self.children["directionIcon"].Show()
class CategorySubItem(CategoryList.CategoryDefaultItem):
	def __del__(self):
		CategoryList.CategoryDefaultItem.__del__(self)
	def __init__(self, text):
		CategoryList.CategoryDefaultItem.__init__(self)
		textLine=ui.TextLine()
		textLine.SetParent(self)
		textLine.AddFlag("not_pick")
		textLine.SetFontName(localeInfo.UI_DEF_FONT)
		textLine.SetWindowHorizontalAlignLeft()
		textLine.SetText("  "+text)
		textLine.Show()
		self.children["textLine"] = textLine
		self.SetSize(100,16)
	def OnMouseOverIn(self):
		self.overLine = True
	def OnMouseOverOut(self):
		self.overLine = False
	def OnRender(self):
		parent = self.parent
		if self.overLine and parent.GetSelectedItem() != self:
			grp.SetColor(grp.GenerateColor(1.0, 1.0, 1.0, 0.2))
		elif parent.GetSelectedItem() == self:
			grp.SetColor(grp.GenerateColor(0.0, 0.0, 1.0, 1.0))
		else:
			grp.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 1.0))
		(_x, _y) = self.GetGlobalPosition()
		(_wx, _wy) = parent.GetGlobalPosition()
		if _y < _wy+5:
			grp.RenderBar(_x, _y+(_wy-_y), self.GetWidth(), self.GetHeight()-(_wy-_y))
		elif _y+self.GetHeight() > _wy+parent.GetHeight():
			grp.RenderBar(_x, _y, self.GetWidth(), self.GetHeight()-((_y+self.GetHeight())-abs(_wy+parent.GetHeight())))
		else:
			grp.RenderBar(_x, _y, self.GetWidth(), self.GetHeight())

		if self.children.has_key("textLine"):
			textLine = self.children["textLine"]
			(_x, _y) = textLine.GetGlobalPosition()
			if _y < _wy:
				if textLine.IsShow():
					textLine.Hide()
			elif _y > _wy+parent.GetHeight()-10:
				if textLine.IsShow():
					textLine.Hide()
			else:
				if not textLine.IsShow():
					textLine.Show()

class ScrollBarNew(ui.Window):
	SCROLLBAR_WIDTH = 7
	SCROLL_BTN_XDIST = 0
	SCROLL_BTN_YDIST = 0
	class MiddleBar(ui.DragButton):
		def __init__(self):
			ui.DragButton.__init__(self)
			self.AddFlag("movable")
			self.SetWindowName("scrollbar_middlebar")
		def MakeImage(self):
			top = ui.ExpandedImageBox()
			top.SetParent(self)
			top.LoadImage(IMG_DIR+"scrollbar_ex/scrollbar_top.tga")
			top.AddFlag("not_pick")
			top.Show()
			topScale = ui.ExpandedImageBox()
			topScale.SetParent(self)
			topScale.SetPosition(0, top.GetHeight())
			topScale.LoadImage(IMG_DIR+"scrollbar_ex/scrollbar_scale.tga")
			topScale.AddFlag("not_pick")
			topScale.Show()
			bottom = ui.ExpandedImageBox()
			bottom.SetParent(self)
			bottom.LoadImage(IMG_DIR+"scrollbar_ex/scrollbar_bottom.tga")
			bottom.AddFlag("not_pick")
			bottom.Show()
			bottomScale = ui.ExpandedImageBox()
			bottomScale.SetParent(self)
			bottomScale.LoadImage(IMG_DIR+"scrollbar_ex/scrollbar_scale.tga")
			bottomScale.AddFlag("not_pick")
			bottomScale.Show()
			middle = ui.ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage(IMG_DIR+"scrollbar_ex/scrollbar_mid.tga")
			middle.AddFlag("not_pick")
			middle.Show()
			self.top = top
			self.topScale = topScale
			self.bottom = bottom
			self.bottomScale = bottomScale
			self.middle = middle
		def SetSize(self, height):
			minHeight = self.top.GetHeight() + self.bottom.GetHeight() + self.middle.GetHeight()
			height = max(minHeight, height)
			ui.DragButton.SetSize(self, 10, height)
			scale = (height - minHeight) / 2 
			extraScale = 0
			if (height - minHeight) % 2 == 1:
				extraScale = 1
			self.topScale.SetRenderingRect(0, 0, 0, scale - 1)
			self.middle.SetPosition(0, self.top.GetHeight() + scale)
			self.bottomScale.SetPosition(0, self.middle.GetBottom())
			self.bottomScale.SetRenderingRect(0, 0, 0, scale - 1 + extraScale)
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
		self.scrollStep = 0.2
		self.SetWindowName("NONAME_ScrollBar")
	def __del__(self):
		ui.Window.__del__(self)
	def CreateScrollBar(self):
		topImage = ui.ExpandedImageBox()
		topImage.SetParent(self)
		topImage.AddFlag("not_pick")
		topImage.LoadImage(IMG_DIR+"scrollbar_ex/scroll_top.tga")
		topImage.Show()
		bottomImage = ui.ExpandedImageBox()
		bottomImage.SetParent(self)
		bottomImage.AddFlag("not_pick")
		bottomImage.LoadImage(IMG_DIR+"scrollbar_ex/scroll_bottom.tga")
		bottomImage.Show()
		middleImage = ui.ExpandedImageBox()
		middleImage.SetParent(self)
		middleImage.AddFlag("not_pick")
		middleImage.SetPosition(0, topImage.GetHeight())
		middleImage.LoadImage(IMG_DIR+"scrollbar_ex/scroll_mid.tga")
		middleImage.Show()
		self.topImage = topImage
		self.bottomImage = bottomImage
		self.middleImage = middleImage
		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(ui.__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.MakeImage()
		middleBar.SetSize(12)
		self.middleBar = middleBar
	def Destroy(self):
		self.eventScroll = None
		self.eventArgs = None
	def SetScrollEvent(self, event, *args):
		self.eventScroll = event
		self.eventArgs = args
	def SetMiddleBarSize(self, pageScale):
		self.middleBar.SetSize(int(pageScale * float(self.GetHeight() - (self.SCROLL_BTN_YDIST*2))))
		realHeight = self.GetHeight() - (self.SCROLL_BTN_YDIST*2) - self.middleBar.GetHeight()
		self.pageSize = realHeight
	def SetScrollBarSize(self, height):
		self.SetSize(self.SCROLLBAR_WIDTH, height)
		self.pageSize = height - self.SCROLL_BTN_YDIST*2 - self.middleBar.GetHeight()
		middleImageScale = float((height - self.SCROLL_BTN_YDIST*2) - self.middleImage.GetHeight()) / float(self.middleImage.GetHeight())
		self.middleImage.SetRenderingRect(0, 0, 0, middleImageScale)
		self.bottomImage.SetPosition(0, height - self.bottomImage.GetHeight())
		self.middleBar.SetRestrictMovementArea(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST, \
			self.middleBar.GetWidth(), height - self.SCROLL_BTN_YDIST * 2)
		self.middleBar.SetPosition(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST)
	def SetScrollStep(self, step):
		self.scrollStep = step
	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep)
	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep)
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
class ListBox(ui.Window):
	def __del__(self):
		ui.Window.__del__(self)
	def Destroy(self):
		self.basePos=0
		self.itemList=[]
		self.scrollBar=None
		self.scrollLen=500
		self.isHorizontal= False
	def __init__(self, isHorizontal = False):
		ui.Window.__init__(self)
		self.itemList=[]
		self.scrollBar=None
		self.Destroy()
	def RemoveAllItems(self):
		for item in self.itemList:
			item.Hide()
			item.Destroy()
		self.itemList=[]
		if self.scrollBar:
			self.scrollBar.SetPos(0)
		self.Render(0)
	def GetItems(self):
		return self.itemList
	def AppendItem(self, newItem, setPosition = True):
		newItem.SetParent(self)
		if setPosition:
			(_x,_y) = (0, 0)
			for child in self.itemList:
				if child.exPos[1]+child.GetHeight() > _y:
					_y = child.exPos[1]+child.GetHeight()
			newItem.SetPosition(_x, _y, True)
		self.itemList.append(newItem)
		self.CalculateScroll()
	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
		self.scrollBar=scrollBar
	def OnMouseWheel(self, nLen):
		if self.scrollBar:
			if self.scrollBar.IsShow():
				if nLen > 0:
					self.scrollBar.OnUp()
				else:
					self.scrollBar.OnDown()
				return True
		return False
	def CalculateScroll(self):
		if len(self.itemList) == 0:
			return;
		screenSize = 0
		for child in self.itemList:
			if child.exPos[1]+child.GetHeight() > screenSize:
				screenSize = child.exPos[1]+child.GetHeight()
		if screenSize != 0:
			screenSize+=30
		windowHeight = self.GetHeight()
		scrollBar = self.scrollBar
		scrollLen = 0
		if scrollBar:
			if screenSize > windowHeight:
				scrollLen = screenSize-windowHeight
				scrollBar.SetMiddleBarSize(float(windowHeight-5)/float(screenSize))
				scrollBar.SetScrollStep(0.1)
				if scrollBar.middleBar.GetGlobalPosition()[1]+scrollBar.middleBar.GetHeight()-15 >= scrollBar.GetGlobalPosition()[1]+scrollBar.GetHeight():
					scrollBar.SetPos(0)
				scrollBar.Show()
			else:
				scrollBar.Hide()
		self.scrollLen = scrollLen
	def __OnScroll(self):
		if self.scrollBar:
			self.SetBasePos(int(self.scrollBar.GetPos()*self.scrollLen))
	def Render(self, basePos):
		for child in self.itemList:
			(ex,ey) = child.exPos
			if self.isHorizontal:
				child.SetPosition(ex-basePos,ey)
			else:
				child.SetPosition(ex,ey-basePos)
			child.OnRender()
		self.basePos=basePos
	def SetBasePos(self, basePos):
		if self.basePos == basePos:
			return
		self.Render(basePos)

class DefaultWikiWindow(ui.Window):
	Listbox=None
	renderTarget=None
	itsRendered=False
	def __del__(self):
		ui.Window.__del__(self)
	def __init__(self):
		ui.Window.__init__(self)
		self.Destroy()
	def Destroy(self):
		self.children=[]
		self.isType = 0
		self.itsRendered=False
		self.sortIndex=0
		self.renderIndex=0
		self.IsLoaded = False
		self.renderTarget = None
		if self.Listbox:
			self.Listbox.RemoveAllItems()
			self.Listbox.Destroy()
			self.Listbox=None
	def OnClickItem(self, arg, type, vnum):
		self.OverOutItem()
		parent = constInfo.GetMainParent()
		if parent != None:
			parent.ShowItemInfo(vnum,type)
	def OverOutItem(self):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			if interface.tooltipItem:
				interface.tooltipItem.HideToolTip()
	def OverInItem(self, index):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			if interface.tooltipItem:
				interface.tooltipItem.SetItemToolTip(index)
				interface.tooltipItem.ShowToolTip()
	def OnRender(self):
		listbox = constInfo.GetListBox()
		if listbox == None:
			return
		_height = listbox.GetHeight()
		(_x, _y) = listbox.GetGlobalPosition()
		(__x, __y, __height) = (0, 0, 0)
		if self.Listbox != None:
			(__x, __y) = self.Listbox.GetGlobalPosition()
			__height = self.Listbox.GetHeight()
			for child in self.children:
				if child.itsNeedDoubleRender:
					RenderWindowMultiple(child, _x, _y, _height, __x, __y, __height)
				else:
					RenderWindow(child, _x, _y, _height)
		else:
			for child in self.children:
				RenderWindow(child, _x, _y, _height)
class DefaultWikiImage(ui.ExpandedImageBox):
	Listbox=None
	renderTarget=None
	itsRendered=False
	isType=0
	sortIndex=0
	renderIndex=0
	def __del__(self):
		ui.ExpandedImageBox.__del__(self)
	def __init__(self):
		ui.ExpandedImageBox.__init__(self)
		self.Destroy()
	def Destroy(self):
		self.children=[]
		self.itsRendered=False
		self.isType = 0
		self.sortIndex=0
		self.renderIndex=0
		self.IsLoaded = False
		self.renderTarget = None
		if self.Listbox:
			self.Listbox.RemoveAllItems()
			self.Listbox.Destroy()
			self.Listbox=None
	def OnClickItem(self, arg, type, vnum):
		self.OverOutItem()
		parent = constInfo.GetMainParent()
		if parent != None:
			parent.ShowItemInfo(vnum,type)
	def OverOutItem(self):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			if interface.tooltipItem:
				interface.tooltipItem.HideToolTip()
	def OverInItem(self, index):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			if interface.tooltipItem:
				interface.tooltipItem.SetItemToolTip(index)
				interface.tooltipItem.ShowToolTip()
	def OnRender(self):
		listbox = constInfo.GetListBox()
		if listbox == None:
			return
		_height = listbox.GetHeight()
		(_x, _y) = listbox.GetGlobalPosition()
		(__x, __y, __height) = (0, 0, 0)

		if self.Listbox != None:
			(__x, __y) = self.Listbox.GetGlobalPosition()
			__height = self.Listbox.GetHeight()
			for child in self.children:
				if child.itsNeedDoubleRender:
					RenderWindowMultiple(child, _x, _y, _height, __x, __y, __height)
				else:
					RenderWindow(child, _x, _y, _height)
		else:
			for child in self.children:
				RenderWindow(child, _x, _y, _height)
class ListBoxEx(ui.Window):
	def __init__(self, isHorizontal=False):
		ui.Window.__init__(self)
		self.viewItemCount=10
		self.basePos=0
		self.itemHeight=16
		self.itemStep=20
		self.selItem=0
		self.itemList=[]
		self.onSelectItemEvent = lambda *arg: None
		self.itemWidth=100
		self.mouseWhell = True
		self.isHorizontal=isHorizontal
		self.scrollBar=None
		self.__UpdateSize()
	def __del__(self):
		ui.Window.__del__(self)
	def SetOnMouseWhell(self, flag):
		self.mouseWhell = flag
	def __UpdateSize(self):
		if self.isHorizontal:
			width = self.itemStep * self.__GetViewItemCount()
			self.SetSize(width, self.itemHeight)
		else:
			height = self.itemStep * self.__GetViewItemCount()
			self.SetSize(self.itemWidth, height)
	def IsEmpty(self):
		if len(self.itemList)==0:
			return 1
		return 0
	def SetItemStep(self, itemStep):
		self.itemStep=itemStep
		self.__UpdateSize()
	def SetItemSize(self, itemWidth, itemHeight):
		self.itemWidth=itemWidth
		self.itemHeight=itemHeight
		self.__UpdateSize()
	def SetViewItemCount(self, viewItemCount):
		self.viewItemCount=viewItemCount
	def SetSelectEvent(self, event):
		self.onSelectItemEvent = event
	def SAFE_SetSelectEvent(self, event):
		self.selectEvent=ui.__mem_func__(event)
	def SetBasePos(self, basePos):
		for oldItem in self.itemList[self.basePos:self.basePos+self.viewItemCount]:
			oldItem.Hide()
		self.basePos=basePos
		pos=basePos
		for newItem in self.itemList[self.basePos:self.basePos+self.viewItemCount]:
			(x, y)=self.GetItemViewCoord(pos, newItem.GetWidth())
			newItem.SetPosition(x, y)
			newItem.Show()
			pos+=1
	def GetItemIndex(self, argItem):
		return self.itemList.index(argItem)
	def GetSelectedItem(self):
		return self.selItem
	def SelectIndex(self, index):
		if index >= len(self.itemList) or index < 0:
			self.selItem = None
			return
		try:
			self.selItem=self.itemList[index]
		except:
			pass
	def SelectItem(self, selItem):
		self.selItem=selItem
		self.onSelectItemEvent(selItem)
	def RemoveAllItems(self):
		self.selItem=None
		for item in self.itemList:
			item.Hide()
			item.Destroy()
		self.itemList=[]
		if self.scrollBar:
			self.scrollBar.SetPos(0)
	def GetItems(self):
		return self.itemList
	def RemoveItem(self, delItem):
		if delItem==self.selItem:
			self.selItem=None
		self.itemList.remove(delItem)
	def AppendItem(self, newItem):
		newItem.SetParent(self)
		newItem.SetSize(self.itemWidth, self.itemHeight)
		self.itemList.append(newItem)
	def AppendItemWithIndex(self, index, newItem):
		newItem.SetParent(self)
		newItem.SetSize(self.itemWidth, self.itemHeight)
		self.itemList.insert(index,newItem)
		self.__OnScroll()
	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
		self.scrollBar=scrollBar
	def OnMouseWheel(self, nLen):
		if self.scrollBar and self.mouseWhell == True:
			if nLen > 0:
				self.scrollBar.OnUp()
			else:
				self.scrollBar.OnDown()
			return True
		return False
	def __OnScroll(self):
		self.SetBasePos(int(self.scrollBar.GetPos()*self.__GetScrollLen()))
	def __GetScrollLen(self):
		scrollLen=self.__GetItemCount()-self.__GetViewItemCount()
		if scrollLen<0:
			return 0
		return scrollLen
	def __GetViewItemCount(self):
		return self.viewItemCount
	def __GetItemCount(self):
		return len(self.itemList)
	def GetItemViewCoord(self, pos, itemWidth):
		if self.isHorizontal:
			return ((pos - self.basePos) * self.itemStep, 0)
		return (0, (pos - self.basePos) * self.itemStep)
	def __IsInViewRange(self, pos):
		if pos<self.basePos:
			return 0
		if pos>=self.basePos+self.viewItemCount:
			return 0
		return 1

class AutoLoad(object):
	def __init__(self):
		self.flagDict={}
	def __del__(self):
		self.flagDict={}
	def SetFlag(self, flag, value):
		self.flagDict[flag] = value
	def GetFlag(self, flag):
		if self.flagDict.has_key(flag):
			return self.flagDict[flag]
		return 0

class ListBoxGrid(ui.Window):
	def __init__(self, isHorizontal= False):
		ui.Window.__init__(self)
		self.scrollLen=0
		self.basePos=0
		self.itemList=[]
		self.func=None
		self.scrollBar=None
		self.isHorizontal=isHorizontal
	def __del__(self):
		ui.Window.__del__(self)
	def RemoveAllItems(self):
		for items in self.itemList:
			items.Hide()
			items.Destroy()
		self.itemList=[]
		if self.scrollBar:
			self.scrollBar.SetPos(0)
	def GetItems(self):
		return self.itemList
	def RemoveItem(self, delItem):
		self.itemList.remove(delItem)
	def AppendItem(self, newItem):
		self.itemList.append(newItem)
		self.CalculateScroll()
	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
		self.scrollBar=scrollBar
		self.CalculateScroll()
	def OnScroll(self):
		if self.scrollBar:
			self.SetBasePos(int(self.scrollBar.GetPos()*self.__GetScrollLen()))
			if player.GetName().find("[") != -1 or player.GetName()=="dracaryS":
				chat.AppendChat(1, "article scroll pos: %.2f"%self.scrollBar.GetPos())
	def AddRenderEvent(self, func):
		self.func = ui.__mem_func__(func)
	def OnMouseWheel(self, nLen):
		if self.scrollBar:
			if self.scrollBar.IsShow():
				if nLen > 0:
					self.scrollBar.OnUp()
				else:
					self.scrollBar.OnDown()
				return True
		return False
	def isNeedScrollBar(self):
		if self.scrollBar:
			return False
		screenSize = 0
		for child in self.itemList:
			if child.exPos[1]+child.GetHeight() > screenSize:
				screenSize = child.exPos[1]+child.GetHeight()
		return screenSize > self.GetHeight()
	def CalculateScroll(self):
		scrollBar = self.scrollBar
		if len(self.itemList) == 0:
			if scrollBar:
				scrollBar.Hide()
			return
		if scrollBar == None:
			return
		screenSize = 0
		for child in self.itemList:
			if child.exPos[1]+child.GetHeight() > screenSize:
				screenSize = child.exPos[1]+child.GetHeight()
		if screenSize != 0:
			screenSize+=30
		windowHeight = self.GetHeight()
		scrollLen = 0
		if screenSize > windowHeight:
			scrollLen = screenSize-windowHeight
			scrollBar.SetMiddleBarSize(float(windowHeight-5)/float(screenSize))
			scrollBar.Show()
			#stepSize = 1.0 / ((screenSize-windowHeight)/100)
			scrollBar.SetScrollStep(0.1)
			if scrollBar.middleBar.GetGlobalPosition()[1]+scrollBar.middleBar.GetHeight()-15 >= scrollBar.GetGlobalPosition()[1]+scrollBar.GetHeight():
				scrollBar.SetPos(0)
		else:
			scrollBar.Hide()
		self.scrollLen = scrollLen
	def __GetScrollLen(self):
		return self.scrollLen
	def SetBasePos(self, basePos, isAutomatic = True):
		if self.basePos == basePos and isAutomatic == True:
			return
		for items in self.itemList:
			(ex,ey) = items.exPos
			if self.isHorizontal:
				items.SetPosition(ex-(basePos),ey)
			else:
				items.SetPosition(ex,ey-(basePos))
		if self.func != None:
			self.func()
		self.basePos=basePos
def calculatePos(pos, maxWidth):
	yincrease = 0
	x , y = 0,0
	for j in xrange(50): # max item y pos..
		if pos <= maxWidth:
			#if yincrease > 0:
			#	pos -= 1
			if pos < 0:
				pos = 0
			x = 32*pos
			break
		else:
			pos-= maxWidth+1
			yincrease+=1
	if yincrease > 0:
		y = yincrease * 32
	return (x,y)

class TextlineLink(ui.Window):
	def __del__(self):
		ui.Window.__del__(self)
	def Destroy(self):
		self.TextLine=None
		self.linkIcon=None
	def __init__(self):
		ui.Window.__init__(self)
		self.TextLine = ui.TextLine()
		self.TextLine.SetParent(self)
		self.TextLine.SetPosition(0,0)
		self.TextLine.Show()
		self.linkIcon = ui.ExpandedImageBox()
		self.linkIcon.AddFlag("ltr")
		self.linkIcon.SetParent(self)
		self.linkIcon.SetPosition(0,0)
		self.linkIcon.LoadImage("d:/ymir work/ui/link_icon.tga")
	def SetText(self, text, scale):
		self.TextLine.SetText(text)
		(width, height) = self.TextLine.GetTextSize()
		self.linkIcon.SetScale(scale,scale)
		self.linkIcon.SetPosition(width+5, 7)
		self.linkIcon.Show()
		self.SetSize(width+10+self.linkIcon.GetWidth(), height)
	def GetText(self):
		return self.TextLine.GetText()
	def GetTextSize(self):
		return self.TextLine.GetTextSize()
	def SetPackedFontColor(self, hex):
		self.TextLine.SetPackedFontColor(hex)
	def SetColor(self, hex, r, g, b):
		self.linkIcon.SetDiffuseColor(r, g, b, 1.0)
		self.TextLine.SetPackedFontColor(hex)
	def SetFontName(self, fontname):
		self.TextLine.SetFontName(fontname)

class HorizontalScrollBarNew(ui.Window):
	WINDOW_HEIGHT = 10
	CORRECT_MIDDLE_BAR_Y = 0
	CORRECT_MIDDLE_BAR_WIDTH = 10
	CORRECT_Y_POS = 0
	class MiddleBar(ui.DragButton):
		def __init__(self):
			ui.DragButton.__init__(self)
			self.AddFlag("movable")
		def MakeImage(self):
			left = ui.ExpandedImageBox()
			left.SetParent(self)
			left.LoadImage(IMG_DIR+"scrollbar_ex/horizontal_scrollbar_left_new.tga")
			left.SetPosition(0, 0)
			left.AddFlag("not_pick")
			left.Show()
			right = ui.ExpandedImageBox()
			right.SetParent(self)
			right.LoadImage(IMG_DIR+"scrollbar_ex/horizontal_scrollbar_right_new.tga")
			right.AddFlag("not_pick")
			right.Show()
			middle = ui.ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage(IMG_DIR+"scrollbar_ex/horizontal_scrollbar_middle_new.tga")
			middle.SetPosition(left.GetWidth() - 1, 0)
			middle.AddFlag("not_pick")
			middle.Show()
			self.left = left
			self.right = right
			self.middle = middle
		def SetSize(self, width):
			width = max(10, width)
			ui.DragButton.SetSize(self, width, 15)
			self.right.SetPosition(width, 0)
			width -= self.right.GetWidth()
			self.middle.SetRenderingRect(0, 0, float(width) / 10.0, 0.0)
	def __init__(self):
		ui.Window.__init__(self)
		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = lambda *arg: None
		self.lockFlag = False
		self.scrollStep = 0.20
		self.CreateScrollBar()
	def __del__(self):
		ui.Window.__del__(self)
	def CreateScrollBar(self):
		barSlot = ui.Bar3D()
		barSlot.SetParent(self)
		barSlot.AddFlag("not_pick")
		barSlot.Show()
		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(ui.__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.MakeImage()
		middleBar.SetSize(12)
		self.middleBar = middleBar
		self.barSlot = barSlot
		self.MID_SCROLLBAR_WIDTH = self.middleBar.GetWidth()

	def Destroy(self):
		self.barSlot = None
		self.middleBar = None
		self.eventScroll = lambda *arg: None
	def SetScrollEvent(self, event):
		self.eventScroll = event
	def SetMiddleBarSize(self, pageScale):
		realWidth = self.GetWidth()
		self.MID_SCROLLBAR_WIDTH = int(pageScale * float(realWidth))
		self.middleBar.SetSize(self.MID_SCROLLBAR_WIDTH)
		self.pageSize = self.GetWidth() - self.MID_SCROLLBAR_WIDTH - self.CORRECT_MIDDLE_BAR_WIDTH
	def SetScrollBarSize(self, width):
		self.pageSize = width - self.MID_SCROLLBAR_WIDTH - self.CORRECT_MIDDLE_BAR_WIDTH
		self.SetSize(width, self.WINDOW_HEIGHT)
		self.middleBar.SetRestrictMovementArea(
			0,
			self.CORRECT_Y_POS,
			width - self.CORRECT_MIDDLE_BAR_WIDTH,
			self.WINDOW_HEIGHT,
		)
		self.middleBar.SetPosition(0, self.CORRECT_MIDDLE_BAR_Y)
		self.UpdateBarSlot()
	def UpdateBarSlot(self):
		self.barSlot.SetPosition(0, 0)
		self.barSlot.SetSize(self.GetWidth(),self.GetHeight())
	def GetPos(self):
		return self.curPos
	def SetPos(self, pos):
		pos = max(0.0, pos)
		pos = min(1.0, pos)
		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(int(newPos), self.CORRECT_Y_POS)
		self.OnMove()
	def SetScrollStep(self, step):
		self.scrollStep = step
	def GetScrollStep(self):
		return self.scrollStep
	def OnUp(self):
		self.SetPos(self.curPos - self.scrollStep)
	def OnDown(self):
		self.SetPos(self.curPos + self.scrollStep)
	def OnMove(self):
		if self.lockFlag:
			return
		if 0 == self.pageSize:
			return
		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(xLocal) / float(self.pageSize)
		if self.eventScroll:
			self.eventScroll()
	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		pickedPos = xMouseLocalPosition - self.MID_SCROLLBAR_WIDTH / 2
		newPos = float(pickedPos) / float(self.pageSize)
		self.SetPos(newPos)
	def LockScroll(self):
		self.lockFlag = True
	def UnlockScroll(self):
		self.lockFlag = False

def CanEquipItem(raceIndex):
	ANTI_FLAG_DICT = {
		0 : item.ITEM_ANTIFLAG_WARRIOR,
		1 : item.ITEM_ANTIFLAG_ASSASSIN,
		2 : item.ITEM_ANTIFLAG_SURA,
		3 : item.ITEM_ANTIFLAG_SHAMAN,
	}
	job = chr.RaceToJob(raceIndex)
	sex = chr.RaceToSex(raceIndex)
	MALE = 1
	FEMALE = 0
	if item.IsAntiFlag(ANTI_FLAG_DICT[job]):
		return 1
	elif item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and sex == MALE:
		return 2
	elif item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and sex == FEMALE:
		return 2
	return 0
def GetOtherSexRace(race):
	otherSexMapping = {
		playersettingmodule.RACE_WARRIOR_W : playersettingmodule.RACE_WARRIOR_M,
		playersettingmodule.RACE_ASSASSIN_W : playersettingmodule.RACE_ASSASSIN_M,
		playersettingmodule.RACE_SHAMAN_W :	playersettingmodule.RACE_SHAMAN_M,
		playersettingmodule.RACE_SURA_W :	playersettingmodule.RACE_SURA_M,
		playersettingmodule.RACE_WARRIOR_M :	playersettingmodule.RACE_WARRIOR_W,
		playersettingmodule.RACE_ASSASSIN_M :	playersettingmodule.RACE_ASSASSIN_W,
		playersettingmodule.RACE_SHAMAN_M :	playersettingmodule.RACE_SHAMAN_W,
		playersettingmodule.RACE_SURA_M : playersettingmodule.RACE_SURA_W,
	}
	return otherSexMapping[race]
def GetValidRace(raceIndex = 0):
	can_equip = CanEquipItem(raceIndex)
	race = raceIndex
	sex = chr.RaceToSex(race)
	MALE = 1
	FEMALE = 0
	if can_equip == 0:
		return race
	elif can_equip == 1:
		if item.GetItemType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_WEAPON:
			raceDict = {
				0 :	[ playersettingmodule.RACE_WARRIOR_W, playersettingmodule.RACE_WARRIOR_M, ],
				1 :	[ playersettingmodule.RACE_ASSASSIN_W, playersettingmodule.RACE_ASSASSIN_M ],
				2 :	[ playersettingmodule.RACE_ASSASSIN_W, playersettingmodule.RACE_ASSASSIN_M ],
				3 :	[ playersettingmodule.RACE_WARRIOR_W, playersettingmodule.RACE_WARRIOR_M, ],
				4 :	[ playersettingmodule.RACE_SHAMAN_W, playersettingmodule.RACE_SHAMAN_M ],
				5 :	[ playersettingmodule.RACE_SHAMAN_W, playersettingmodule.RACE_SHAMAN_M ],
			}
			item_type = item.GetValue(3)
			return raceDict[item_type][sex]
		else:
			raceDict = {
				0 :	[ playersettingmodule.RACE_WARRIOR_W, playersettingmodule.RACE_WARRIOR_M ],
				1 :	[ playersettingmodule.RACE_ASSASSIN_W, playersettingmodule.RACE_ASSASSIN_M ],
				2 :	[ playersettingmodule.RACE_SURA_W, playersettingmodule.RACE_SURA_M ],
				3 :	[ playersettingmodule.RACE_SHAMAN_W, playersettingmodule.RACE_SHAMAN_M ],
			}
			flags = []
			ANTI_FLAG_DICT = {
				0 : item.ITEM_ANTIFLAG_WARRIOR,
				1 : item.ITEM_ANTIFLAG_ASSASSIN,
				2 : item.ITEM_ANTIFLAG_SURA,
				3 : item.ITEM_ANTIFLAG_SHAMAN,
			}
			for i in xrange(len(ANTI_FLAG_DICT)):
				if not item.IsAntiFlag(ANTI_FLAG_DICT[i]):
					flags.append(i)
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
				sex = FEMALE
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
				sex = MALE
			return raceDict[flags[0]][sex] if len(flags) == 1 else 0
	elif can_equip == 2:
		return GetOtherSexRace(race)
def IsCanModelPreview(itemVnum):
	item.SelectItem(itemVnum)
	itemType = item.GetItemType()
	itemSubType = item.GetItemSubType()
	if itemType == item.ITEM_TYPE_WEAPON and itemSubType != item.WEAPON_ARROW:
		return True
	elif itemType == item.ITEM_TYPE_ARMOR and itemSubType == item.ARMOR_BODY:
		return True
	elif itemType == item.ITEM_TYPE_COSTUME and (itemSubType == item.COSTUME_TYPE_WEAPON or itemSubType == item.COSTUME_TYPE_BODY or itemSubType == item.COSTUME_TYPE_HAIR or itemSubType == item.COSTUME_TYPE_MOUNT or itemSubType == item.COSTUME_TYPE_ACCE):
		return True
	return False

HAIRSTYLE_CAMERA_CFG = {
	playersettingmodule.RACE_WARRIOR_M : ([311.4753, -16.3934, 150.0000], [0.0000, 0.0000, 152.3934]),
	playersettingmodule.RACE_ASSASSIN_W : ([344.2622, -16.3934, 150.0000], [0.0000, 0.0000, 147.3934]),
	playersettingmodule.RACE_SURA_M : ([311.4753, -16.3934, 150.0000], [0.0000, 0.0000, 172.1804]),
	playersettingmodule.RACE_SHAMAN_W : ([344.2622, -16.3934, 150.0000], [0.0000, 0.0000, 147.3934]),
	playersettingmodule.RACE_WARRIOR_W : ([344.2622, -16.3934, 150.0000], [0.0000, 0.0000, 147.3934]),
	playersettingmodule.RACE_ASSASSIN_M : ([344.2622, -16.3934, 150.0000], [0.0000, 0.0000, 156.7869]),
	playersettingmodule.RACE_SURA_W : ([311.4753, -16.3934, 150.0000], [0.0000, 0.0000, 156.7869]),
	playersettingmodule.RACE_SHAMAN_M : ([377.0492, -16.3934, 150.0000], [0.0000, 0.0000, 163.7869])
}

def GetCharTypeHairCamera(char_type):
	if not HAIRSTYLE_CAMERA_CFG.has_key(char_type):
		return tuple([], [])
	return HAIRSTYLE_CAMERA_CFG[char_type]

import chrmgr


def SetItemToModelPreview(modelIndex, itemVnum):
	item.SelectItem(itemVnum)
	itemType = item.GetItemType()
	itemSubType = item.GetItemSubType()

	if itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_MOUNT:
		renderTarget.SelectModel(modelIndex, item.GetValue(0))
		renderTarget.SetVisibility(modelIndex, True)
		renderTarget.SetArmor(modelIndex, 0)
	else:
		raceIndex = GetValidRace(app.GetRandom(0,4))
		renderTarget.SelectModel(modelIndex, raceIndex)
		renderTarget.SetVisibility(modelIndex, True)
		if itemType == item.ITEM_TYPE_WEAPON:
			renderTarget.SetArmor(modelIndex, 11299)
			renderTarget.SetWeapon(modelIndex, itemVnum)
		elif itemType == item.ITEM_TYPE_ARMOR:
			renderTarget.SetArmor(modelIndex, itemVnum)
		elif itemType == item.ITEM_TYPE_COSTUME:
			if itemSubType == item.COSTUME_TYPE_WEAPON:
				renderTarget.SetArmor(modelIndex, 11299)
				renderTarget.SetWeapon(modelIndex,itemVnum)
			elif itemSubType == item.COSTUME_TYPE_BODY:
				renderTarget.SetArmor(modelIndex, itemVnum)
			elif itemSubType == item.COSTUME_TYPE_ACCE:
				renderTarget.SetArmor(modelIndex, 11299)
				renderTarget.SetAcce(modelIndex, itemVnum - 85000)
			elif itemSubType == item.COSTUME_TYPE_HAIR:
				renderTarget.SetArmor(modelIndex, 11299)
				renderTarget.SetHair(modelIndex,itemVnum)
				(V3Eye, V3Target) = GetCharTypeHairCamera(raceIndex)
				if len(V3Eye) and len(V3Target):
					renderTarget.SetModelV3Eye(modelIndex, *V3Eye)
					renderTarget.SetModelV3Target(modelIndex, *V3Target)

def getRealVnum(vnum):
	isRefineItem = False
	item.SelectItem(vnum)
	isRefineItem = False
	level = "0"
	itemname = item.GetItemName()
	pos = itemname.find("+")
	#if pos != -1 and item.ITEM_TYPE_METIN != item.GetItemType():
	if pos != -1 and pos+1 < len(itemname):
		level = itemname[pos+1:]
		if level.isdigit():
			isRefineItem = True
			vnum -= int(level) if item.ITEM_TYPE_METIN != item.GetItemType() else int(level) * 100
	return (vnum, isRefineItem)
def MakeStringToList(args, buf):
	new_buf = buf
	arg_list = args.split("&")
	for j in xrange(len(arg_list)):
		if arg_list[j] == "" or arg_list[j] == " ":
			continue
		if len(arg_list[j]) <= 1:
			continue
		itemLink = arg_list[j].find("I")
		if itemLink>=0:
			if arg_list[j][itemLink+1].isdigit() == True:
				item.SelectItem(int(arg_list[j][1:]))
				new_buf = new_buf.replace(arg_list[j],item.GetItemName())
				continue
		mobLink = arg_list[j].find("M")
		if mobLink>= 0:
			if arg_list[j][mobLink+1].isdigit() == True:
				mobName = nonplayer.GetMonsterName(int(arg_list[j][1:]))
				if not mobName or mobName == "":
					mobName = "None"
				new_buf = new_buf.replace(arg_list[j],mobName)
				continue
		skillLink = arg_list[j].find("S")
		if skillLink >=0:
			if arg_list[j][skillLink+1].isdigit() == True:
				skillName = skill.GetSkillName(int(arg_list[j][1:]))
				if not skillName or skillName == "":
					skillName = "None"
				new_buf = new_buf.replace(arg_list[j],skillName)

				continue
		goldLink = arg_list[j].find("Y")
		if goldLink >=0:
			if arg_list[j][goldLink+1].isdigit() == True:
				new_buf = new_buf.replace(arg_list[j],constInfo.NumberToString(int(arg_list[j][1:])))
				continue
	return new_buf
def GetArgToString(buf):
	bufSplit = buf.split(" ")
	new_text=buf
	if len(bufSplit) >= 0:
		new_arg= ""
		for j in xrange(len(bufSplit)):
			new_arg+= "%s&"% str(bufSplit[j])
		try:
			text = MakeStringToList(new_arg[:len(new_arg)-1], new_text)
			new_text = text
		except:
			return new_text
	return new_text

def GetResultPageImage(argument):
	imgDict = {
		"Equipment":
			{
				0 : IMG_DIR_CATEGORY+"equipment_0.tga",
				1 : IMG_DIR_CATEGORY+"equipment_1.tga",
				2 : IMG_DIR_CATEGORY+"equipment_2.tga",
				3 : IMG_DIR_CATEGORY+"equipment_3.tga",
				4 : IMG_DIR_CATEGORY+"equipment_4.tga",
				5 : IMG_DIR_CATEGORY+"equipment_5.tga",
				6 : IMG_DIR_CATEGORY+"equipment_6.tga",
				7 : IMG_DIR_CATEGORY+"equipment_7.tga",
				8 : IMG_DIR_CATEGORY+"equipment_8.tga",
				9 : IMG_DIR_CATEGORY+"equipment_9.tga",
				10 : IMG_DIR_CATEGORY+"equipment_10.tga",
			},
		"Costume":
			{
				0 : IMG_DIR_CATEGORY+"costume_weapons.tga",
				1 : IMG_DIR_CATEGORY+"costume_armor.tga",
				2 : IMG_DIR_CATEGORY+"costume_hair.tga",
				3 : IMG_DIR_CATEGORY+"sash_skins.tga",
				4 : IMG_DIR_CATEGORY+"costume_shining.tga",
			},
		"Mount":
			{
				5 : IMG_DIR_CATEGORY+"costume_mount.tga",
				6 : IMG_DIR_CATEGORY+"costume_pet.tga",
				7 : IMG_DIR_CATEGORY+"costume_pet.tga",
			},
		"Chests":
			{
				0 : IMG_DIR_CATEGORY+"chests_0.tga",
				1 : IMG_DIR_CATEGORY+"dungeon_chests.tga",
				2 : IMG_DIR_CATEGORY+"chests_2.tga",
				3 : IMG_DIR_CATEGORY+"events_chests.tga",
			},
		"Bosses":
			{
				0 : IMG_DIR_CATEGORY+"bosses_wall.tga",
				1 : IMG_DIR_CATEGORY+"bosses_wall.tga",
				2 : IMG_DIR_CATEGORY+"bosses_wall.tga",
			},
		"Monster":
			{
				0 : IMG_DIR_CATEGORY+"monster_wall.tga",
				1 : IMG_DIR_CATEGORY+"monster_wall.tga",
				2 : IMG_DIR_CATEGORY+"monster_wall.tga",
			},
		"Metinstone":
			{
				0 : IMG_DIR_CATEGORY+"metinstone_wall.tga",
				1 : IMG_DIR_CATEGORY+"metinstone_wall.tga",
				2 : IMG_DIR_CATEGORY+"metinstone_wall.tga",
			},
	}
	if imgDict.has_key(argument[0]):
		if imgDict[argument[0]].has_key(int(argument[1])):
			return imgDict[argument[0]][int(argument[1])]
	return ""

def IsArticleCategory(argument):
	if argument[0] == "System" or argument[0] == "Dungeon":
		return True
	return False
