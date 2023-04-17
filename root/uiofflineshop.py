import app
import player
import offlineshop
import ui
import item
import dbg
import uiCommon
import uiTooltip
import localeInfo
import ime
import snd
import uiPickMoney
import grp
import mouseModule
import constInfo
  
SUBTYPE_NOSET = 255
SEARCH_RESULT_LIMIT = 250
COLOR_TEXT_SHORTCUT = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
				
def IsBuildingShop():
	interface = offlineshop.GetOfflineshopBoard()
	if not interface:
		return False
	return interface.IsBuildingShop()

def IsSaleSlot(win,slot):
	interface = offlineshop.GetOfflineshopBoard()
	if not interface:
		return False
	
	return interface.IsForSaleSlot(win,slot)

def IsForAuctionSlot(win,slot):
	interface = offlineshop.GetOfflineshopBoard()
	if not interface:
		return False

	return interface.IsForAuctionSlot(win, slot)

def IsBuildingAuction():
	interface = offlineshop.GetOfflineshopBoard()
	if not interface:
		return False

	return interface.IsBuildingAuction()

def PutsError(line):
	dbg.TraceError("offlineshop interface error : %s "%line)

def NumberToString(num):
	if num < 0:
		return "-" + NumberToString(-num)
	parts = []
	while num >= 1000:
		parts.insert(0,"%03d"%(num%1000))
		num = num//1000

	parts.insert(0,"%d"%num)
	return '.'.join(parts)

def GetDurationString(dur):
	days    = dur // (24 * 60)
	hours   = (dur//60)%24
	minutes = dur%60

	res = ""

	if days > 0:
		res += localeInfo.OFFLINESHOP_DAY_TEXT%days + " "
	
	if hours > 0:
		res += localeInfo.OFFLINESHOP_HOUR_TEXT%hours + " "
	
	if minutes > 0:
		res += localeInfo.OFFLINESHOP_MINUTE_TEXT%minutes
	
	if days == 0 and hours == 0 and minutes == 0:
		return localeInfo.OFFLINESHOP_MINUTE_TEXT%0
		
	return res


def GetDurationStringRB(dur):
	days    = dur // (24 * 60)
	hours   = (dur//60)%24
	minutes = dur%60

	res = "|cff82ff7d|H|h"

	if days > 0:
		res += "%dd"%days + " "
	else:
		res += "%dd"%0 + " "

	if hours > 0:
		res += "%02dh"%hours + " "
	else:
		res += "%02dh"%0 + " "

	if minutes > 0:
		res += "%02dm"%minutes
	else:
		res += "%02dm"%0 + " "

	if days == 0 and hours == 0 and minutes == 0:
		return localeInfo.OFFLINESHOP_MINUTE_TEXT%0

	res += "|h|r"
	return res


def MakeSlotInfo(window, slotIndex, yang):
	res = {}
	
	itemIndex = player.GetItemIndex(window, slotIndex)
	itemCount = player.GetItemCount(window, slotIndex)
	
	res["slot"]	 = slotIndex
	res["window"]= window
	res["vnum"]	 = itemIndex
	res["count"] = itemCount
	
	res["socket"]= {}
	res["attr"]  = {}
	
	res['locked_attr'] = player.GetItemAttrLocked(window, slotIndex)

	for x in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
		attr = player.GetItemAttribute(window, slotIndex, x)
		
		res['attr'][x] = {}
		res['attr'][x]["type"]  = attr[0]
		res['attr'][x]["value"] = attr[1]
	
	for x in xrange(player.METIN_SOCKET_MAX_NUM):
		res['socket'][x] = player.GetItemMetinSocket(window, slotIndex, x)
	
	res["price"] = yang
	return res

def MakeOfferCancelButton():
	btn = ui.Button()
	btn.SetUpVisual("offlineshop/myoffers/deleteoffer_default.png")
	btn.SetDownVisual("offlineshop/myoffers/deleteoffer_down.png")
	btn.SetOverVisual("offlineshop/myoffers/deleteoffer_over.png")
	btn.Show()
	return btn

def MakeOfferViewImage(isView):
	flag = "0"
	if isView:
		flag="1"

	img = ui.ImageBox()
	img.LoadImage("scripts/offlineshop/viewicon_%s.png"%flag)
	img.Show()
	return img

def MakeDefaultEmptySlot(event = None):
	slot = Slot(False)
	if event:
		slot.SetOnMouseLeftButtonUpEvent(event)
	return slot

def GetBestOfferPriceYang(lst):
	if not lst:
		return 0

	max =0
	for info in lst:
		if info['price_yang'] > max:
			max = info['price_yang']

	return max

def SortByDatetime(lst):
	def CustomSortByDatetime(a,b):
		def CmpFunc(a,b):
			if a > b:
				return -1
			if b > a:
				return 1
			return 0

		keys = ('year' , 'month' , 'day', 'hour', 'minute')
		for k in keys:
			if a[k] != b[k]:
				return CmpFunc(a[k] , b[k])
		return 0

	lst.sort(cmp=CustomSortByDatetime)

def SortOffersByPrice(lst):
	def CustomSortByOfferPrice(a,b):
		price_a = a.get('price_yang', 0)
		price_b = b.get('price_yang', 0)

		if price_a > price_b:
			return -1

		if price_b < price_b:
			return 1
		return 0

	lst.sort(cmp=CustomSortByOfferPrice)
	return lst

class TableWindow(ui.Window):
	
	def __init__(self, col, row, width, height, realw, realh):
		ui.Window.__init__(self)
		self.rows 			= row
		self.columns		= col

		self.width			= width
		self.height			= height

		ui.Window.SetSize(self, realw, realh)

	def __del__(self):
		ui.Window.__del__(self)
	

	def __GetCoordByPos(self, col,row, child):
		stepx = self.width/self.columns
		stepy = self.height/self.rows

		x = stepx * col
		y = stepy * row

		x += stepx/2 - child.GetWidth() /2
		y += stepy/2 - child.GetHeight()/2

		return x,y

	def SetTableElement(self, column , row, child= None):
		if self.rows <= row:
			PutsError("cannot SetTableElement on row %d"%row)
			return
		
		if self.columns <= column:
			PutsError("cannot SetTableElement on column %d (row %d )"%(column,row))
			return

		if child == None:
			return
		
		x,y = self.__GetCoordByPos(column, row, child)

		child.SetParent(self)
		child.SetPosition( x, y)
		child.Show()

class TableWindowData(ui.Window):

	def __init__(self, col, row, width, height, realw, realh):
		ui.Window.__init__(self)
		self.rows 			= row
		self.columns		= col

		self.width			= width
		self.height			= height

		ui.Window.SetSize(self, realw, realh)


	def __del__(self):
		ui.Window.__del__(self)


	def __GetCoordByPos(self, col,row, child):
		stepx = self.width/self.columns
		stepy = self.height/self.rows

		x = stepx * col
		y = stepy * row

		x += stepx/2 - child.GetWidth() /2
		y += stepy/2 - child.GetHeight()/2

		return x,y

	def SetTableElement(self, column , row, child= None):
		if self.rows <= row:
			PutsError("cannot SetTableElement on row %d"%row)
			return

		if self.columns <= column:
			PutsError("cannot SetTableElement on column %d (row %d )"%(column,row))
			return

		if child == None:
			return

		x,y = self.__GetCoordByPos(column, row, child)

		child.SetParent(self)
		child.SetPosition( x, y)
		child.Show()


import grp
class NewListBoxOfflineShop(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)

		self.items = []
		self.selected = None
		self.basePos = 0
		self.itemWidth = 100
		self.itemStep = 4
		self.scrollbar = None
		self.scrollBarPos = 0.0

		self.selectEvent = None

	def SetSize(self, w, h):
		ui.Window.SetSize(self, w, h + self.itemStep)
		self.SetItemWidth(w)

		self.UpdateList()

	def SetScrollBar(self, scrollbar):
		self.scrollbar = scrollbar
		self.scrollbar.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
		self.scrollbar.SetScrollStep(0.10)
		self.UpdateList()

	def GetScrollLen(self):
		return self.CalcTotalItemHeight() - self.GetHeight() - 8
	def GetBasePos(self):
		return self.basePos
		
	def CalcTotalItemHeight(self):
		total_height = 0
		for item in self.items:
			total_height += item.GetHeight()
			total_height += self.itemStep

		return total_height

	def ConfigureScrollBar(self):
		if self.scrollbar:
			itemheight = self.CalcTotalItemHeight()
			myheight = self.GetHeight() - 8# - 2 * self.itemStep
			dif = 0.97
			if itemheight > myheight and itemheight != 0:
				dif = 1.0 * myheight / itemheight

			self.scrollbar.SetMiddleBarSize(dif)

	def __OnScroll(self, position = None):
		pos = self.scrollbar.GetPos() if position == None else position
		self.scrollBarPos = pos
		toscr = self.CalcTotalItemHeight() - self.GetHeight() - 8# + 2 * self.itemStep
		self.basePos = toscr * pos

		self.UpdateList()

	def OnRunMouseWheel(self, nLen):
		if self.scrollbar:
			self.scrollbar.OnRunMouseWheel(nLen)

	def GetScrollBarPosition(self):
		return self.scrollBarPos

	def OnScroll(self, pos):
		self.__OnScroll(pos)

	def SelectItem(self, item):
		self.selected = item

		if self.selectEvent:
			self.selectEvent(item)

	def AppendItem(self, item):
		item.SetParent(self)
		item.SetWidth(self.itemWidth)
		item.Show()
		self.items.append(item)

		self.UpdateList()

	def RemoveItem(self, item):
		item.Hide()

		self.items.remove(item)
		self.UpdateList()

	def ClearItems(self):
		map(lambda wnd: wnd.Hide(), self.items)
		del self.items[:]

		self.basePos = 0
		if self.scrollbar:
			self.scrollbar.SetPos(0)
		self.UpdateList()

	def UpdateList(self):
		self.ConfigureScrollBar()
		self.RecalcItemPositions()

	def IsEmpty(self):
		return len(self.itemList) == 0

	def SetItemWidth(self, w):
		self.itemWidth = w
		for item in self.items:
			item.SetWidth(w)

	def RecalcItemPositions(self):
		curbp = self.basePos

		itemheight = self.CalcTotalItemHeight()
		myheight = self.GetHeight() - 2 * self.itemStep

		if itemheight < myheight:
			curbp = 0

		fromPos = curbp
		curPos = 0
		toPos = curbp + self.GetHeight()
		for item in self.items:
			hw = item.GetHeight()
			if curPos + hw < fromPos:
				item.Hide()
			elif curPos < fromPos and curPos + hw > fromPos:
				item.SetRenderMin(fromPos - curPos)
				item.Show()
			elif curPos < toPos and curPos + hw > toPos:
				item.SetRenderMax(toPos - curPos)
				item.Show()
			elif curPos > toPos:
				item.Hide()
			else:
				item.SetRenderMin(0)
				item.Show()

			item.SetPosition(0, curPos - fromPos)
			curPos += hw + self.itemStep

class NewListBoxOfflineShopItem(ui.Window):
	DEFAULT_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.3)
	HOVER_COLOR = grp.GenerateColor(0.0, 0.0, 1.1, 0.3)
	LEFT_COLOR = grp.GenerateColor(0.0, 0.7, 1.1, 0.3)

	def __init__(self):
		ui.Window.__init__(self)

		self.width = 0
		self.height = 0
		self.minh = 0
		self.maxh = 0

		self.isLeft = 0

		self.components = []

	def __del__(self):
		ui.Window.__del__(self)

	def SetColor(self, color):
		self.color = color

	def OnMouseOverIn(self):
		if self.isLeft:
			self.color = LEFT_COLOR = grp.GenerateColor(0.0, 0.7, 1.1, 0.3)
		else:
			self.color = NewListBoxOfflineShopItem.HOVER_COLOR

	def OnMouseOverOut(self):
		if self.isLeft:
			self.color = LEFT_COLOR = grp.GenerateColor(0.0, 0.7, 1.1, 0.3)
		else:
			self.color = NewListBoxOfflineShopItem.DEFAULT_COLOR

	def SetColorLeft(self):
		self.color = NewListBoxOfflineShopItem.LEFT_COLOR
		self.isLeft = 1

	def SetParent(self, parent):
		ui.Window.SetParent(self, parent)

	def SetHeight(self, h):
		self.SetSize(self.width, h)

	def SetWidth(self, w):
		self.SetSize(w, self.height)

	def SetSize(self, w, h):
		self.width = w
		self.height = h
		self.maxh = h
		ui.Window.SetSize(self, w, h)

	def SetRenderMin(self, minh):
		self.minh = minh
		self.maxh = self.height
		self.RecalculateRenderedComponents()

	def SetRenderMax(self, maxh):
		self.maxh = maxh
		self.minh = 0
		self.RecalculateRenderedComponents()

	def RegisterComponent(self, component):
		mtype = type(component).__name__
		if mtype == "Bar" or mtype == "line":
			(x, y, w, h) = component.GetRect()
			(x, y) = component.GetLocalPosition()
			component.__list_data = [x, y, w, h]
		self.components.append(component)

	def UnregisterComponent(self, component):
		self.components.remove(component)
		#if component.__list_data:
		#	component.__list_data = None

	def RecalculateRenderedComponents(self):
		for component in self.components:
			(xl, yl) = component.GetLocalPosition()
			(x, y, w, h) = component.GetRect()
			mtype = type(component).__name__
			if mtype == "TextLine":
				(w, h) = component.GetTextSize()

			if yl + h < self.minh:
				component.Hide()
			elif yl > self.maxh:
				component.Hide()
			else:
				if mtype == "ExpandedImageBox" or mtype == "ExpandedButton":

					miny = 0
					if self.minh > 0 and yl < self.minh:
						miny = -float(self.minh - yl) / float(h)

					maxy = 0
					if h != 0:
						maxy = float(self.maxh - yl - h) / float(h)

					maxy = min(0, max(-1, maxy))

					component.SetRenderingRect(0.0, miny, 0.0, maxy)
					component.Show()

				else:
					if yl < self.minh or yl + h > self.maxh:
						component.Hide()
					else:
						component.Show()

	def OnRender(self):
		self.DARK_COLOR = 0xFF3D3331
		x, y = self.GetGlobalPosition()
		xRender, yRender = self.GetGlobalPosition()
		yRender -= 3
		widthRender = self.GetWidth()
		heightRender = self.GetHeight() + 3
		grp.SetColor(self.color)
		grp.RenderBar(x, y + self.minh, self.GetWidth(), self.maxh - self.minh)

class ShopSearchItem(NewListBoxOfflineShopItem):
	MARGIN = 7.5
	COUNT_FONT_SIZE = 14
	SPECIAL_TITLE_COLOR = grp.GenerateColor(1.0, 0.7843, 0.0, 1.0)
	HIGH_PRICE_COLOR = SPECIAL_TITLE_COLOR
	MIDDLE_PRICE_COLOR = grp.GenerateColor(0.85, 0.85, 0.85, 1.0)
	LOW_PRICE_COLOR = grp.GenerateColor(0.7, 0.7, 0.7, 1.0)

	def __init__(self):
		NewListBoxOfflineShopItem.__init__(self)
		self.slot = []

		self.slotInfo = {}
		self.tooltipItem = uiTooltip.ItemToolTip()
		self.tooltipItem.Hide()

		self.eventClick = None
		self.index = 0

		self.Instance = self

		self.LoadDialog()
		self.LoadTexts()
		self.SetColor(NewListBoxOfflineShopItem.DEFAULT_COLOR)

	def __del__(self):
		self.__clear()
		NewListBoxOfflineShopItem.__del__(self)

	def __clear(self):
		self.slotInfo = {}
		self.eventClick = None
		self.index = 0

	def Destroy(self):
		self.__clear()

	def LoadDialog(self):
		slotImageFileName = ["slot_32x32.tga", "slot_32x64.tga", "slot_32x96.tga"]
		for i in xrange(3):
			slot = ui.ExpandedImageBox()
			slot.SetParent(self)
			slot.SetPosition(16, ShopSearchItem.MARGIN)
			slot.LoadImage("scripts/shop/%s" % (slotImageFileName[i]))
			slot.OnMouseOverIn = self.__OverInItem
			slot.OnMouseOverOut = self.__OverOutItem
			slot.Show()

			self.RegisterComponent(slot)

			self.slot.append(slot)

		self.itemImage = ui.ExpandedImageBox()
		self.itemImage.SetParent(self)
		self.itemImage.SetPosition(0, ShopSearchItem.MARGIN)
		self.itemImage.Show()

		self.itemImage.OnMouseOverIn = self.__OverInItem
		self.itemImage.OnMouseOverOut = self.__OverOutItem

		self.RegisterComponent(self.itemImage)

		self.itemCount = ui.TextLine()
		self.itemCount.SetParent(self)
		self.itemCount.SetText("")
		self.itemCount.SetFontName("Arial:%d" % ShopSearchItem.COUNT_FONT_SIZE)
		self.itemCount.SetHorizontalAlignLeft()
		self.itemCount.Show()

		self.RegisterComponent(self.itemCount)

		self.itemName = ui.TextLine()
		self.itemName.SetParent(self)
		self.itemName.SetText("")
		self.itemName.SetFontName("Arial:%d" % ShopSearchItem.COUNT_FONT_SIZE)
		self.itemName.SetHorizontalAlignLeft()
		self.itemName.Show()

		self.RegisterComponent(self.itemName)

		self.itemOwner = ui.TextLine()
		self.itemOwner.SetParent(self)
		self.itemOwner.SetText("")
		self.itemOwner.SetFontName("Arial:%d" % ShopSearchItem.COUNT_FONT_SIZE)
		self.itemOwner.SetHorizontalAlignLeft()
		self.itemOwner.Show()

		self.RegisterComponent(self.itemOwner)

		self.itemPriceYang = ui.TextLine()
		self.itemPriceYang.SetParent(self)
		self.itemPriceYang.SetText("")
		self.itemPriceYang.SetFontName("Arial:%d" % ShopSearchItem.COUNT_FONT_SIZE)
		self.itemPriceYang.SetHorizontalAlignRight()
		self.itemPriceYang.Show()

		self.RegisterComponent(self.itemPriceYang)

		self.itemPriceYangIcon = ui.TextLine()
		self.itemPriceYangIcon.SetParent(self)
		self.itemPriceYangIcon.SetText("")
		self.itemPriceYangIcon.SetFontName("Arial:%d" % ShopSearchItem.COUNT_FONT_SIZE)
		self.itemPriceYangIcon.SetHorizontalAlignRight()
		self.itemPriceYangIcon.Show()

		self.RegisterComponent(self.itemPriceYangIcon)

		self.buyQuestionDlg = uiCommon.QuestionDialog()
		self.buyQuestionDlg.SetText("uiScriptLocale.SEARCH_SHOP_BUY_CONFIGM")
		self.buyQuestionDlg.SetAcceptEvent(lambda: self.__BuyItem(True))
		self.buyQuestionDlg.SetCancelEvent(lambda: self.__BuyItem(False))

		self.__AppendItem()

	def LoadTexts(self):
		pass

	def SetInfo(self, info):
		self.slotInfo = info
		self.SetSlot(info["vnum"] , info["count"])

	def GetInfo(self):
		return self.slotInfo

	def SetIndex(self, index):
		self.index = index

	def GetIndex(self):
		return self.index

	def SetSlot(self, itemVnum, itemCount):
		item.SelectItem(itemVnum)

		image 	= item.GetIconImageFileName()
		name	= item.GetItemName()
		width, height = item.GetItemSize()

		self.__SetItemIconImage(image)

		self.__SetData(name, itemCount, width, height)

		self.SetSize(300, ShopSearchItem.MARGIN*2+32*height)

		self.BottomLine = ui.Line()
		self.BottomLine.SetParent(self)
		self.BottomLine.SetPosition(0, self.GetHeight() + 2)
		self.BottomLine.SetSize(375, 0)
		self.BottomLine.SetColor(0xFF3D3331)
		self.BottomLine.Show()

		self.RegisterComponent(self.BottomLine)

	def __SetItemIconImage(self, icon):
		self.itemImage.LoadImage(item.GetIconImageFileName())

	def __SetData(self, itemName, itemCount, itemWidth, itemHeight):
		lSpace = 55-15
		ownerName = self.slotInfo["owner_name"]
		priceYang = self.slotInfo["price"]

		priceYangColor = self.GetPriceColor(priceYang)

		if itemCount > 1:
			self.itemCount.SetText("x" + str(itemCount))
			lSpace = 80-15

		self.itemName.SetText(itemName)

		if self.slotInfo["owner_name"] != "":
			self.itemOwner.SetText("|Eemoji/mail|e " + ownerName)
			w, h = self.itemOwner.GetTextSize()
			self.itemOwner.SetSize(w, h)
			self.itemOwner.OnMouseLeftButtonDown = lambda : player.OpenPrivateMessage(ownerName)
		else:
			self.itemOwner.SetText("|Eemoji/offline|e Offline")

		self.itemPriceYang.SetText(localeInfo.NumberToStringAsType(priceYang))
		self.itemPriceYangIcon.SetText(localeInfo.SHOP_TYPE_MONEY)
		self.itemPriceYang.SetTextColor(priceYangColor)

		self.itemCount.SetPosition(45-13, ShopSearchItem.MARGIN + (itemHeight * 32 + ShopSearchItem.COUNT_FONT_SIZE - 27) / 2)
		self.itemName.SetPosition(lSpace, ShopSearchItem.MARGIN + (itemHeight * 32 - ShopSearchItem.COUNT_FONT_SIZE) / 2)
		self.itemOwner.SetPosition(195-12, ShopSearchItem.MARGIN + (itemHeight * 32 - ShopSearchItem.COUNT_FONT_SIZE) / 2)
		self.itemPriceYang.SetPosition(376, ShopSearchItem.MARGIN + (itemHeight * 20 - ShopSearchItem.COUNT_FONT_SIZE + 10) / 2)
		self.itemPriceYangIcon.SetPosition(395, ShopSearchItem.MARGIN + (itemHeight * 20 - ShopSearchItem.COUNT_FONT_SIZE + 10) / 2)

	def __AppendItem(self):
		for slot in self.slot:
			slot.Hide()
			try:
				self.UnregisterComponent(slot)
			except:
				pass

	def FormatWaitTime(self, time):
		m, s = divmod(time, 60)
		h, m = divmod(m, 60)
		d, h = divmod(h, 24)
		return "%02d:%02d:%02d:%02d" % (d, h, m, s)

	def GetPriceColor(self, price):
		if price>= 500000:
			return ShopSearchItem.HIGH_PRICE_COLOR
		if price>=50000:
			return ShopSearchItem.MIDDLE_PRICE_COLOR
		else:
			return ShopSearchItem.LOW_PRICE_COLOR

	def __OverInItem(self):
		if not self.tooltipItem.IsShow():
			info = self.slotInfo
			sockets = [info["socket"][num] for num in xrange(player.METIN_SOCKET_MAX_NUM)]
			attrs	= [(info["attr"][num]['type'], info["attr"][num]['value']) for num in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

			self.tooltipItem.ClearToolTip()
			self.tooltipItem.AddItemData(info["vnum"], sockets, attrs, 0, 0, player.INVENTORY, -1, -1, 0, 0, False)

			self.tooltipItem.AppendPrice(info["price"])

			self.tooltipItem.Show()

	def __OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def SetOnMouseLeftButtonUpEvent(self, event):
		self.eventClick = event
		ui.Window.SetOnMouseLeftButtonUpEvent(self, self.__OnClick)

		if self.itemImage:
			self.itemImage.SetOnMouseLeftButtonUpEvent(self.__OnClick)

	def __OnClick(self):
		if self.eventClick!=None:
			self.eventClick(self)

	def OnMouseLeftButtonUp(self):
		self.__OnClick()
		pass

	def OnMouseRightButtonUp(self):
		pass

class TableWindowWithScrollbar(TableWindow):

	SCROLLBAR_HORIZONTAL 	= 0
	SCROLLBAR_VERTICAL		= 1

	def __init__(self, w, h , columns, rows, scrollbar=0):
		htable = h if scrollbar == self.SCROLLBAR_VERTICAL else h-18
		wtable = w if scrollbar == self.SCROLLBAR_HORIZONTAL else w -18

		TableWindow.__init__(self , columns, rows , wtable, htable, w ,h)

		self.childrenDict 	= {}
		self.scrollbar 		= None
		self.rows_count 	= rows
		self.columns_count	= columns
		self.total_row		= 0
		self.elementCount	= 0

		self.defaultCreate  	= None
		self.defaultCreateArgs 	= None
		self.defaultChildren 	= []

		self.__loadScrollbar(scrollbar)
		self.ClearElement()
	
	def __del__(self):
		self.childrenDict = {}
		self.scrollbar = None
		self.defaultCreate  	= None
		self.defaultCreateArgs 	= None
		self.defaultChildren 	= []
		TableWindow.__del__(self)

	def __loadScrollbar(self, scrollbar):

		if scrollbar == self.SCROLLBAR_VERTICAL:
			template = {
				'button1' 	: {
					'default' 	: 'offlineshop/scrollbar/vertical/button1_default.png',
					'over' 		: 'offlineshop/scrollbar/vertical/button1_over.png',
					'down' 		: 'offlineshop/scrollbar/vertical/button1_down.png',
				},
				'button2' 		: {
					'default'	: 'offlineshop/scrollbar/vertical/button2_default.png',
					'over'		: 'offlineshop/scrollbar/vertical/button2_over.png',
					'down'		: 'offlineshop/scrollbar/vertical/button2_down.png',
				},
				'middle'  		: {
					'default'	: 'scripts/shop/slimscroll/middle.png',
					'over'		: 'scripts/shop/slimscroll/middle.png',
					'down'		: 'scripts/shop/slimscroll/middle.png',
				},
				'base'	  		: "scripts/shop/slimscroll/base.png",
				'onscroll'		: self.__refreshViewList,
				'parent'		: self,
				'orientation'	: ui.CustomScrollBar.VERTICAL,
				'align'			: {'mode': ui.CustomScrollBar.RIGHT,'offset2':5},
			}
		else:
			template = {
				'button1' 	: {
					'default' 	: 'offlineshop/scrollbar/horizontal/button1_default.png',
					'over' 		: 'offlineshop/scrollbar/horizontal/button1_over.png',
					'down' 		: 'offlineshop/scrollbar/horizontal/button1_down.png',
				},
				'button2' 		: {
					'default'	: 'offlineshop/scrollbar/horizontal/button2_default.png',
					'over'		: 'offlineshop/scrollbar/horizontal/button2_over.png',
					'down'		: 'offlineshop/scrollbar/horizontal/button2_down.png',
				},
				'middle'  		: {
					'default'	: 'offlineshop/scrollbar/horizontal/middle_default.png',
					'over'		: 'offlineshop/scrollbar/horizontal/middle_over.png',
					'down'		: 'offlineshop/scrollbar/horizontal/middle_down.png',
				},
				'base'	  		: "offlineshop/scrollbar/horizontal/base_image.png",
				'onscroll'		: self.__refreshViewList,
				'parent'		: self,

				'orientation'	: ui.CustomScrollBar.HORIZONTAL,
				'align'			: {'mode':ui.CustomScrollBar.BOTTOM,},
			}

		self.scrollbar = ui.CustomScrollBar(template)

	def SetElement(self, column, row, child):
		if not row  in self.childrenDict:
			self.childrenDict[row] = {}

		self.childrenDict[row][column] = child
		self.__refreshViewList()


	def SetDefaultCreateChild(self, func, *args):
		self.defaultCreate = func
		self.defaultCreateArgs = args

	def __refreshViewList(self):
		if self.scrollbar.orientation == ui.CustomScrollBar.VERTICAL:
			if len(self.childrenDict.keys()) <= self.rows_count:
				self.scrollbar.Hide()
			else:
				self.scrollbar.Show()

			init_row = self.__getInitRow()

			for row, dct in self.childrenDict.items():
				for column, child in dct.items():
					if row < init_row or row >= init_row + self.rows_count:
						child.Hide()
						continue
					self.SetTableElement(column, row-init_row , child)

			for s in self.defaultChildren:
				s.Destroy()

			self.defaultChildren = []
			if self.defaultCreate:
				for row in xrange(init_row, init_row + self.rows_count):
					for col in xrange(self.columns_count):
						if not row in self.childrenDict or not col in self.childrenDict[row]:
							defaultChild = self.defaultCreate(*self.defaultCreateArgs) if self.defaultCreateArgs else self.defaultCreate()
							defaultChild.Show()
							self.SetTableElement(col, row - init_row, defaultChild)
							self.defaultChildren.append(defaultChild)

		elif self.scrollbar.orientation == ui.CustomScrollBar.HORIZONTAL:
			if len(self.childrenDict.get(0, [])) <= self.columns_count:
				self.scrollbar.Hide()
			else:
				self.scrollbar.Show()

			init_column = self.__getInitColumn()
			end_column  = init_column+ self.columns_count

			for dct in self.childrenDict.values():
				for elm in dct.values():
					elm.Hide()

			for col in xrange(init_column, end_column):
				for row, dct in self.childrenDict.items():
					if col in dct:
						self.SetTableElement(col-init_column, row , dct[col])
						dct[col].Show()

			for s in self.defaultChildren:
				s.Destroy()

			self.defaultChildren = []
			if self.defaultCreate:
				for row in xrange(0, self.rows_count):
					for col in xrange(init_column, end_column):
						if not row in self.childrenDict or not col in self.childrenDict[row]:
							defaultChild = self.defaultCreate(*self.defaultCreateArgs) if self.defaultCreateArgs else self.defaultCreate()
							defaultChild.Show()
							self.SetTableElement(col-init_column, row, defaultChild)
							self.defaultChildren.append(defaultChild)

	def __getInitRow(self):
		if not self.scrollbar.IsShow():
			return 0

		return int((len(self.childrenDict.keys()) - self.rows_count ) * self.scrollbar.GetPos())

	def __getInitColumn(self):
		if not self.scrollbar.IsShow():
			return 0

		return int((len(self.childrenDict.get(0,[])) - self.columns_count ) * self.scrollbar.GetPos())

	def __AdjustScrollbarStep(self):
		total_slots		= self.rows_count*self.columns_count
		extra_element 	= self.elementCount - (total_slots)

		if extra_element <= 0:
			return

		if self.scrollbar.orientation == ui.CustomScrollBar.HORIZONTAL:
			extra_col = int(extra_element // self.rows_count)
			if extra_element % self.rows_count != 0:
				extra_col += 1
			self.scrollbar.SetScrollStep(1.0 / float(extra_col+1))

		else:
			extra_row_count = int(extra_element/self.columns_count)
			if extra_element % self.columns_count != 0:
				extra_row_count += 1

			self.scrollbar.SetScrollStep(1.0/float(extra_row_count+1))

	def ClearElement(self):
		for a in self.childrenDict.values():
			for child in a.values():
				child.Hide()

		self.childrenDict = {}
		self.elementCount = 0
		self.__refreshViewList()


	def AddElement(self, child):
		normElement =  self.columns_count*self.rows_count

		if self.elementCount < normElement or self.scrollbar.orientation == ui.CustomScrollBar.VERTICAL:
			column 	= self.elementCount%self.columns_count
			row		= self.elementCount//self.columns_count

		else:
			index = self.elementCount - normElement
			row   = index % self.rows_count
			column= index //self.rows_count

			column += self.columns_count

		self.SetElement(column, row, child)
		self.elementCount += 1

		self.__AdjustScrollbarStep()

	def GetElementDict(self):
		return self.childrenDict

	def OnRunMouseWheel(self, nLen):
		if self.scrollbar:
			self.scrollbar.OnRunMouseWheel(nLen)

class TableWindowWithScrollbarData(TableWindowData):

	SCROLLBAR_HORIZONTAL 	= 0
	SCROLLBAR_VERTICAL		= 1

	def __init__(self, w, h , columns, rows, scrollbar=0):
		htable = h if scrollbar == self.SCROLLBAR_VERTICAL else h-18
		wtable = w if scrollbar == self.SCROLLBAR_HORIZONTAL else w -18

		TableWindowData.__init__(self , columns, rows , wtable, htable, w ,h)

		self.childrenDict 	= {}
		self.scrollbar 		= None
		self.rows_count 	= rows
		self.columns_count	= columns
		self.total_row		= 0
		self.elementCount	= 0

		self.defaultCreate  	= None
		self.defaultCreateArgs 	= None
		self.defaultChildren 	= []

		self.__loadScrollbar(scrollbar)
		self.ClearElement()


	def __del__(self):
		self.childrenDict = {}
		self.scrollbar = None
		self.defaultCreate  	= None
		self.defaultCreateArgs 	= None
		self.defaultChildren 	= []
		TableWindowData.__del__(self)

	def __loadScrollbar(self, scrollbar):

		if scrollbar == self.SCROLLBAR_VERTICAL:
			template = {
				'button1' 	: {
					'default' 	: 'offlineshop/scrollbar/vertical/button1_default.png',
					'over' 		: 'offlineshop/scrollbar/vertical/button1_over.png',
					'down' 		: 'offlineshop/scrollbar/vertical/button1_down.png',
				},
				'button2' 		: {
					'default'	: 'offlineshop/scrollbar/vertical/button2_default.png',
					'over'		: 'offlineshop/scrollbar/vertical/button2_over.png',
					'down'		: 'offlineshop/scrollbar/vertical/button2_down.png',
				},
				'middle'  		: {
					'default'	: 'offlineshop/scrollbar/vertical/middle_default.png',
					'over'		: 'offlineshop/scrollbar/vertical/middle_over.png',
					'down'		: 'offlineshop/scrollbar/vertical/middle_down.png',
				},
				'base'	  		: "offlineshop/scrollbar/vertical/base_image.png",
				'onscroll'		: self.__refreshViewList,
				'parent'		: self,
				'orientation'	: ui.CustomScrollBar.VERTICAL,
				'align'			: {'mode': ui.CustomScrollBar.RIGHT,},
			}

		else:
			template = {
				'button1' 	: {
					'default' 	: 'offlineshop/scrollbar/horizontal/button1_default.png',
					'over' 		: 'offlineshop/scrollbar/horizontal/button1_over.png',
					'down' 		: 'offlineshop/scrollbar/horizontal/button1_down.png',
				},
				'button2' 		: {
					'default'	: 'offlineshop/scrollbar/horizontal/button2_default.png',
					'over'		: 'offlineshop/scrollbar/horizontal/button2_over.png',
					'down'		: 'offlineshop/scrollbar/horizontal/button2_down.png',
				},
				'middle'  		: {
					'default'	: 'offlineshop/scrollbar/horizontal/middle_default.png',
					'over'		: 'offlineshop/scrollbar/horizontal/middle_over.png',
					'down'		: 'offlineshop/scrollbar/horizontal/middle_down.png',
				},
				'base'	  		: "offlineshop/scrollbar/horizontal/base_image.png",
				'onscroll'		: self.__refreshViewList,
				'parent'		: self,

				'orientation'	: ui.CustomScrollBar.HORIZONTAL,
				'align'			: {'mode':ui.CustomScrollBar.BOTTOM,},
			}
		
		self.scrollbar = ui.CustomScrollBar(template)
	
	def SetElement(self, column, row, child):
		if not row  in self.childrenDict:
			self.childrenDict[row] = {}
		
		self.childrenDict[row][column] = child
		self.__refreshViewList()
	

	def SetDefaultCreateChild(self, func, *args):
		self.defaultCreate = func
		self.defaultCreateArgs = args

	def __refreshViewList(self):
		if self.scrollbar.orientation == ui.CustomScrollBar.VERTICAL:
			if len(self.childrenDict.keys()) <= self.rows_count:
				self.scrollbar.Hide()
			else:
				self.scrollbar.Show()

			init_row = self.__getInitRow()

			for row, dct in self.childrenDict.items():
				for column, child in dct.items():
					if row < init_row or row >= init_row + self.rows_count:
						child.Hide()
						continue
					self.SetTableElement(column, row-init_row , child)
			
			
			#updated 25-01-2020 #topatch
			for s in self.defaultChildren:
				s.Destroy()
			
			self.defaultChildren = []
			if self.defaultCreate:
				for row in xrange(init_row, init_row + self.rows_count):
					for col in xrange(self.columns_count):
						if not row in self.childrenDict or not col in self.childrenDict[row]:
							defaultChild = self.defaultCreate(*self.defaultCreateArgs) if self.defaultCreateArgs else self.defaultCreate()
							defaultChild.Show()

							self.SetTableElement(col, row - init_row, defaultChild)
							self.defaultChildren.append(defaultChild)

		elif self.scrollbar.orientation == ui.CustomScrollBar.HORIZONTAL:
			if len(self.childrenDict.get(0, [])) <= self.columns_count:
				self.scrollbar.Hide()
			else:
				self.scrollbar.Show()

			init_column = self.__getInitColumn()
			end_column  = init_column+ self.columns_count

			for dct in self.childrenDict.values():
				for elm in dct.values():
					elm.Hide()

			for col in xrange(init_column, end_column):
				for row, dct in self.childrenDict.items():
					if col in dct:
						self.SetTableElement(col-init_column, row , dct[col])
						dct[col].Show()
			
			
			#updated 25-01-2020 #topatch
			for s in self.defaultChildren:
				s.Destroy()
			
			self.defaultChildren = []
			if self.defaultCreate:
				for row in xrange(0, self.rows_count):
					for col in xrange(init_column, end_column):
						if not row in self.childrenDict or not col in self.childrenDict[row]:
							defaultChild = self.defaultCreate(*self.defaultCreateArgs) if self.defaultCreateArgs else self.defaultCreate()
							defaultChild.Show()

							self.SetTableElement(col-init_column, row, defaultChild)
							self.defaultChildren.append(defaultChild)

	def __getInitRow(self):
		if not self.scrollbar.IsShow():
			return 0
		
		return int((len(self.childrenDict.keys()) - self.rows_count ) * self.scrollbar.GetPos())

	def __getInitColumn(self):
		if not self.scrollbar.IsShow():
			return 0

		return int((len(self.childrenDict.get(0,[])) - self.columns_count ) * self.scrollbar.GetPos())

	def __AdjustScrollbarStep(self):
		total_slots		= self.rows_count*self.columns_count
		extra_element 	= self.elementCount - (total_slots)
		
		if extra_element <= 0:
			return

		if self.scrollbar.orientation == ui.CustomScrollBar.HORIZONTAL:
			extra_col = int(extra_element // self.rows_count)
			if extra_element % self.rows_count != 0:
				extra_col += 1
			self.scrollbar.SetScrollStep(1.0 / float(extra_col+1))

		else:
			extra_row_count = int(extra_element/self.columns_count)
			if extra_element % self.columns_count != 0:
				extra_row_count += 1

			self.scrollbar.SetScrollStep(1.0/float(extra_row_count+1))

	def ClearElement(self):
		for a in self.childrenDict.values():
			for child in a.values():
				child.Hide()
		
		self.childrenDict = {}
		self.elementCount = 0
		self.__refreshViewList()

	def AddElement(self, child):
		normElement =  self.columns_count*self.rows_count

		if self.elementCount < normElement or self.scrollbar.orientation == ui.CustomScrollBar.VERTICAL:
			column 	= self.elementCount%self.columns_count
			row		= self.elementCount//self.columns_count

		else:
			index = self.elementCount - normElement
			row   = index % self.rows_count
			column= index //self.rows_count

			column += self.columns_count

		self.SetElement(column, row, child)
		self.elementCount += 1
		
		self.__AdjustScrollbarStep()
	
	def GetElementDict(self):
		return self.childrenDict

	def OnRunMouseWheel(self, nLen):
		if self.scrollbar:
			self.scrollbar.OnRunMouseWheel(nLen)

class ResultListElement(ui.Window):
	def __init__(self , info):
		ui.Window.__init__(self)
		self.__LoadWindow(info)

	def __del__(self):
		ui.Window.__del__(self)


	def __LoadWindow(self, info):
		self.__LoadOpenShopButton()

	def __LoadOpenShopButton(self):
		button = ui.Button()
		button.SetParent(self)
		button.SetUpVisual("scripts/offlineshop/test_1.png")
		button.SetDownVisual("scripts/offlineshop/test_2.png")
		button.SetOverVisual("scripts/offlineshop/test_3.png")

		button.SetPosition(0, 0)
		button.Show()

		self.SetSize(button.GetWidth(), button.GetHeight())
		self.openShopButton = button

	def SetInfo(self, info):
		self.slotInfo = info
		self.SetSlot(info["vnum"] , info["count"])

	def SetSlot(self, itemvnum, itemcount):
		item.SelectItem(itemvnum)

		image 	= item.GetIconImageFileName()
		name	= item.GetItemName()
		width, height = item.GetItemSize()

		self.__SetItemIconImage(image, width, height)

	def __SetItemIconImage(self, icon, w, h):
		image = ui.ExpandedImageBox()
		image.LoadImage(icon)
		image.SetParent(self)
		image.SetScale(0.7, 0.7)
		image.SetPosition(0,5)
		image.Show()

		self.iconImage = image
		
class Slot(ui.Window):

	def __init__(self, isSold=False):
		ui.Window.__init__(self)

		self.background = None
		self.background_sold = None
		self.iconImage = None
		self.countText = None
		self.upgradeImage = None

		self.slotInfo = {}
		self.index = 0
		self.eventClick = None
		self.childrens = []

		self.__loadBackground(isSold)

		print("initializing Slot")

	#updated 25-01-2020 #topatch
	def __del__(self):
		self.__clear()
		ui.Window.__del__(self)

	#updated 25-01-2020 #topatch
	def __clear(self):
		self.background 		= None
		self.iconImage  		= None
		self.countText			= None
		self.upgradeImage		= None
		self.background_sold	= None

		ui.Window.SetOnMouseLeftButtonUpEvent(self, None)

		if self.background:
			self.background.SetOnMouseLeftButtonUpEvent(None)

		if self.iconImage:
			self.iconImage.SetOnMouseLeftButtonUpEvent(None)

		if self.countText:
			self.countText.SetOnMouseLeftButtonUpEvent(None)

		if self.upgradeImage:
			self.upgradeImage.SetOnMouseLeftButtonUpEvent(None)

		if self.background_sold:
			self.background_sold.SetOnMouseLeftButtonUpEvent(None)

		self.slotInfo 		= {}
		self.index			= 0
		self.eventClick		= None
		self.childrens		= []

	#updated 25-01-2020 #topatch
	def Destroy(self):
		self.__clear()

	def __loadBackground(self, isSold):
		bg = ui.ImageBox()
		bg.LoadImage("offlineshop/slot/base_image.png")
		bg.SetParent(self)
		bg.SetPosition(0,0)
		bg.Show()

		self.SetSize(bg.GetWidth(), bg.GetHeight())
		self.background = bg

		sold = ui.ImageBox()
		sold.LoadImage("offlineshop/slot/base_image_sold.png")
		sold.SetParent(self.background)
		sold.SetPosition(0, 0)

		if isSold:
			sold.Show()
		else:
			sold.Hide()

		self.background_sold = sold

	def SetInfo(self, info):
		self.slotInfo = info
		self.SetSlot(info["vnum"] , info["count"])

	def GetInfo(self):
		return self.slotInfo

	def SetSlot(self, itemvnum, itemcount):
		item.SelectItem(itemvnum)

		image 	= item.GetIconImageFileName()
		name	= item.GetItemName()

		self.__SetItemIconImage(image)
		self.__SetItemCount(itemcount)
		self.__SetUpgradeByName(name)


	def SetIndex(self, index):
		self.index = index


	def GetIndex(self):
		return self.index


	def SetSold(self, flag):
		if flag:
			self.background_sold.Show()
		else:
			self.background_sold.Hide()


	def __GetIconPosition(self, image):
		w = image.GetWidth()
		h = image.GetHeight()

		return (self.background.GetWidth()/2 - w/2,  self.background.GetHeight()/2 - h/2)

	def __SetItemIconImage(self, icon):
		image = ui.ImageBox()
		image.LoadImage(icon)
		image.SetParent(self.background)

		x,y = self.__GetIconPosition(image)

		image.SetPosition(x,y)
		image.Show()

		self.iconImage = image


	def __GetCountPosition(self):
		x,y = self.iconImage.GetLocalPosition()
		x += self.iconImage.GetWidth()/2
		y += self.iconImage.GetHeight()

		return (x,y)


	def __SetItemCount(self, count):
		if count <= 1:
			self.countText = None
			return

		countText = ui.TextLine()
		countText.SetParent(self.background)

		x,y = self.__GetCountPosition()
		countText.SetPosition(x,y)
		countText.SetHorizontalAlignCenter()
		countText.SetText("x"+str(count))
		countText.Show()

		self.countText = countText



	def __GetUpgradeImagePosition(self,img):
		w = img.GetWidth()
		h = img.GetHeight()

		bw = self.background.GetWidth()
		bh = self.background.GetHeight()

		return (bw - (w+5), bh-(h+5))


	def __SetUpgradeByName(self, name):
		name = name.strip()
		if len(name) > 2:
			if name[-2] == '+':
				if name[-1].isdigit():
					value = int(name[-1])

					upgrade = ui.ImageBox()
					upgrade.LoadImage("offlineshop/slot/upgrade/%d.png"%value)
					upgrade.SetParent(self.background)

					x,y = self.__GetUpgradeImagePosition(upgrade)
					upgrade.SetPosition(x,y)
					upgrade.Show()

					self.upgradeImage = upgrade


	def SetOnMouseLeftButtonUpEvent(self, event):
		self.eventClick = event
		ui.Window.SetOnMouseLeftButtonUpEvent(self, self.__OnClick)

		if self.background:
			self.background.SetOnMouseLeftButtonUpEvent(self.__OnClick)

		if self.iconImage:
			self.iconImage.SetOnMouseLeftButtonUpEvent(self.__OnClick)

		if self.countText:
			self.countText.SetOnMouseLeftButtonUpEvent(self.__OnClick)

		if self.upgradeImage:
			self.upgradeImage.SetOnMouseLeftButtonUpEvent(self.__OnClick)

		if self.background_sold:
			self.background_sold.SetOnMouseLeftButtonUpEvent(self.__OnClick)

	def __OnClick(self):
		if self.eventClick!=None:
			self.eventClick(self)

	def IsInSlot(self):
		if not self.IsShow():
			return False

		if self.IsIn():
			return True

		if self.background:
			if self.background.IsIn():
				return True

		if self.iconImage:
			if self.iconImage.IsIn():
				return True

		if self.countText:
			if self.countText.IsIn():
				return True

		if self.upgradeImage:
			if self.upgradeImage.IsIn():
				return True

		if self.background_sold:
			if self.background_sold.IsShow() and self.background_sold.IsIn():
				return True

		if self.childrens:
			for child in self.childrens:
				if child.IsIn():
					return True

		return False


	def AppendChild(self, child):
		child.SetParent(self.background)
		self.childrens.append(child)

class Offer(ui.Window):
	def __init__(self, info):
		ui.Window.__init__(self)

		self.bgImage = None
		self.guestName = None
		self.priceText = None
		self.acceptButton = None
		self.deleteButton = None
		self.itemText = None
		self.info = {}
		self.index = 0
		self.is_accept = 0
		self.acceptEvent = None
		self.deniedEvent = None

		self.info  		= info
		self.index 		= info["id"]
		self.is_accept	= info["is_accept"]

		self.__loadBackground()
		self.__loadButtons()
		self.SetGuestName(info['buyer_name'])
		self.SetPriceYang(info["price"])

	def __del__(self):

		self.bgImage = None
		self.guestName = None
		self.priceText = None
		self.acceptButton = None
		self.deleteButton = None
		self.itemText = None
		self.info = {}
		self.index = 0
		self.is_accept = 0
		self.acceptEvent = None
		self.deniedEvent = None

		ui.Window.__del__(self)
	
	def __loadBackground(self):
		bg = ui.ImageBox()
		bg.SetParent(self)
		bg.SetPosition(0,0)
		bg.LoadImage("scripts/offlineshop/data_input_1_norm.png")
		bg.Show()

		self.SetSize(bg.GetWidth(), bg.GetHeight())
		self.bgImage = bg

	def SetGuestName(self, name):
		text = ui.TextLine()
		text.SetParent(self.bgImage)
		text.SetPosition(77 , 0)
		text.SetHorizontalAlignCenter()
		text.Show()
		text.SetText(name)
		self.guestName = text

	def SetPriceYang(self, yang):
		text = ui.TextLine()
		text.SetParent(self.bgImage)
		text.SetPosition(355 , 0)
		# text.SetHorizontalAlignCenter()
		text.Show()
		text.SetText(localeInfo.NumberToMoneyString(yang))
		self.priceText = text

	def SetItemName(self, name):
		text = ui.TextLine()
		text.SetParent(self.bgImage)
		text.SetPosition(239 , 0)
		text.SetHorizontalAlignCenter()
		text.Show()
		text.SetText(name)
		self.itemText = text
	
	def __loadButtons(self):
		if self.info["is_accept"]:
			return
		#accept
		button = ui.Button()
		button.SetParent(self.bgImage)
		button.SetPosition(self.bgImage.GetWidth() - 50, 0)
		
		path = "offlineshop/offer/accept_%s.png"
		button.SetUpVisual(path%"default")
		button.SetOverVisual(path%"over")
		button.SetDownVisual(path%"down")
		button.Show()
		
		self.acceptButton = button

		button = ui.Button()
		button.SetParent(self.bgImage)
		button.SetPosition(self.bgImage.GetWidth() - 30, 0)
		
		path = "offlineshop/offer/cancel_%s.png"
		button.SetUpVisual(path%"default")
		button.SetOverVisual(path%"over")
		button.SetDownVisual(path%"down")
		button.Show()

		self.deleteButton = button

	def SetAcceptButtonEvent(self, event):
		if self.acceptButton:
			self.acceptButton.SAFE_SetEvent(self.__OnAccept)
		self.acceptEvent = event
		
	def SetDeleteButtonEvent(self, event):
		if self.deleteButton:
			self.deleteButton.SAFE_SetEvent(self.__OnCancel)
		self.deniedEvent = event

	def GetInfo(self):
		return self.info

	def __OnAccept(self):
		if self.acceptEvent:
			self.acceptEvent(self)

	def __OnCancel(self):
		if self.deniedEvent:
			self.deniedEvent(self)

class AuctionOffer(ui.Window):
	def __init__(self, info):
		ui.Window.__init__(self)

		self.background = None
		self.ownerName = None
		self.offerText = None

		self.__LoadWindow(info)

	def __del__(self):
		self.background = None
		self.ownerName = None
		self.offerText = None
		ui.Window.__del__(self)

	def __LoadWindow(self, info):
		name = info["buyer_name"]
		best_yang = info['price_yang']

		self.__LoadBackground()
		self.__LoadOwnerName(name)
		self.__LoadOfferText(best_yang)

	def GetInfo(self):
		return self.info

	def __LoadBackground(self):
		bg = ui.ImageBox()
		bg.LoadImage("scripts/offlineshop/data_input_2_norm.png")
		bg.SetParent(self)
		bg.SetPosition(0, 0)
		bg.Show()

		self.SetSize(bg.GetWidth(), bg.GetHeight())
		self.background = bg

	def __LoadOwnerName(self, ownerName):
		if not ownerName:
			return

		text = ui.TextLine()
		text.SetParent(self.background)
		text.SetPosition(186, 5)
		text.SetHorizontalAlignCenter()
		text.SetText(ownerName)
		text.Show()

		self.ownerName = text

	def __LoadOfferText(self, yang):
		text = ui.TextLine()
		text.SetParent(self.background)
		text.SetPosition(403, 5)
		text.SetHorizontalAlignCenter()
		text.SetText(localeInfo.NumberToMoneyString(yang))
		text.Show()

		self.offerText = text

class MyOffer(ui.Window):
	def __init__(self, info):
		ui.Window.__init__(self)
		self.info = info
		self.clear()

		self.__LoadBackground()
		self.__LoadSlots()
		self.__LoadOwnerName()
		self.__LoadOfferText()
		self.__LoadSlot()
		self.__LoadCancelButton()

	def clear(self):
		self.background   		= None
		self.slotName			= None
		self.slotOffer			= None
		self.slot1				= None
		self.slot2				= None
		self.ownerName    		= None
		self.offerText    		= None
		self.slot		  		= None
		self.cancelButton 		= None
		self.cancelButtonEvent	= None

	def __del__(self):
		self.clear()
		ui.Window.__del__(self)

	def __LoadBackground(self):
		bg = ui.ImageBox()
		bg.SetParent(self)
		bg.SetPosition(0,0)
		bg.LoadImage("scripts/offlineshop/my_offers_background.png")
		bg.Show()

		self.SetSize(bg.GetWidth(), bg.GetHeight())
		self.background = bg

	def __LoadSlots(self):
		slotName = ui.TextLine()
		slotName.SetParent(self.background)
		slotName.SetPosition(100, 10)
		slotName.SetText(localeInfo.OFFLINESHOP_SHOPS_NAME_TEXT)
		slotName.SetPackedFontColor(0xfff4ead5)
		slotName.Show()

		slotOffer = ui.TextLine()
		slotOffer.SetParent(self.background)
		slotOffer.SetPosition(115, 60)
		slotOffer.SetText(localeInfo.OFFLINESHOP_OFFER_TEXT)
		slotOffer.SetPackedFontColor(0xfff4ead5)
		slotOffer.Show()

		self.slotName = slotName
		self.slotOffer = slotOffer

		slot1 = ui.SlotBar_RB()
		slot1.SetParent(self.background)
		slot1.SetPosition(55, 25)
		slot1.SetSize(140, 20)
		slot1.SetColor(0xff2A2522, 0xff433B38, 0xff000000)
		slot1.Show()

		slot2 = ui.SlotBar_RB()
		slot2.SetParent(self.background)
		slot2.SetPosition(55, 75)
		slot2.SetSize(140, 20)
		slot2.SetColor(0xff2A2522, 0xff433B38, 0xff000000)
		slot2.Show()

		self.slot1 = slot1
		self.slot2 = slot2

	def __LoadOwnerName(self):
		text = ui.TextLine()
		text.SetParent(self.slot1)
		text.SetPosition(3, 3)
		text.SetText(self.info.get('shop_name', ""))
		text.Show()

		self.ownerName = text

	def __LoadOfferText(self):
		text = ui.TextLine()
		text.SetParent(self.slot2)
		text.SetPosition(3, 3)
		text.SetText(NumberToString(self.info.get('price', "")))
		text.Show()

		self.offerText = text

	def __LoadSlot(self):
		slot = Slot(self.info['is_accept'])
		slot.SetInfo(self.info['item'])
		slot.SetParent(self.background)
		slot.SetPosition(9,4)
		slot.Show()

		self.slot = slot


	def __LoadCancelButton(self):
		button = ui.Button()
		button.SetParent(self.background)
		button.SetPosition(185, 1)

		button.SetUpVisual("offlineshop/myoffers/deleteoffer_default.png")
		button.SetDownVisual("offlineshop/myoffers/deleteoffer_down.png")
		button.SetOverVisual("offlineshop/myoffers/deleteoffer_over.png")


		button.Show()
		button.SAFE_SetEvent(self.__OnClickCancelButton)
		self.cancelButton = button

	def SetCancelButtonEvent(self, event):
		self.cancelButtonEvent = event

	def __OnClickCancelButton(self):
		if self.cancelButtonEvent:
			self.cancelButtonEvent(self.info['offer_id'])

	def IsInSlot(self):
		return self.slot.IsInSlot()


	def GetIndex(self):
		return self.info['offer_id']

	#updated 25-01-2020 #topatch
	def DisableCancelButton(self):
		if self.cancelButton:
			self.cancelButton.Hide()

class AuctionListElement(ui.Window):
	def __init__(self, info):
		ui.Window.__init__(self)

		self.ownerName = None
		self.durationText = None
		self.offerCountText = None
		self.owner_id = -1
		self.info = info
		self.button = None
		self.buttonEvent = None
		self.bestYangText = None

		self.__LoadWindow(info)

	def __del__(self):
		self.ownerName = None
		self.durationText = None
		self.offerCountText = None
		self.owner_id = -1
		self.info = {}
		self.button = None
		self.buttonEvent = None
		self.bestYangText = None
		ui.Window.__del__(self)

	def __LoadWindow(self, info):
		owner_id 	= info["owner_id"]
		duration 	= info["duration"]
		count 		= info["offer_count"]
		name 		= info["owner_name"]
		best_yang	= info['best_yang']

		self.owner_id = owner_id

		self.__LoadOpenAuctionButton()
		self.__LoadOwnerName(name)
		self.__LoadDuration(duration)
		self.__LoadCount(count)
		self.__LoadBestYang(best_yang)

	def SetIndex(self,index):
		self.owner_id = index

	def GetIndex(self):
		return self.owner_id

	def GetInfo(self):
		return self.info

	def SetOnClickOpenShopButton(self, event):
		self.openShopButton.SAFE_SetEvent(self.__OnClickOpenShop)
		self.openShopButtonEvent = event

	def __LoadOwnerName(self, ownerName):
		if not ownerName:
			return

		text = ui.TextLine()
		text.SetParent(self.button)
		text.SetPosition(48, 5)
		text.SetHorizontalAlignCenter()
		text.SetText(ownerName)
		text.Show()

		self.ownerName = text

	def __LoadBestYang(self, yang):
		text = ui.TextLine()
		text.SetParent(self.button)
		text.SetPosition(198 , 5)
		text.SetHorizontalAlignCenter()
		text.SetText(localeInfo.NumberToMoneyString(yang))
		text.Show()
		self.bestYangText = text

	def __LoadDuration(self, duration):
		text = ui.TextLine()
		text.SetParent(self.button)
		text.SetPosition(358 , 5)
		text.SetHorizontalAlignCenter()
		text.SetText(GetDurationString(duration))
		text.Show()

		self.durationText = text

	def __LoadCount(self, count):
		text = ui.TextLine()
		text.SetParent(self.button)
		text.SetPosition(510 , 5)
		text.SetHorizontalAlignCenter()
		text.SetText(str(count))
		text.Show()

		self.offerCountText = text

	def SetOnClickOpenAuctionButton(self, event):
		self.button.SAFE_SetEvent(self.__OnClickMe)
		self.buttonEvent = event

	def __OnClickMe(self):
		if self.buttonEvent:
			self.buttonEvent(self.owner_id)

	def __LoadOpenAuctionButton(self):
		button = ui.Button()
		button.SetParent(self)
		button.SetUpVisual("scripts/offlineshop/data_input_2_norm.png")
		button.SetDownVisual("scripts/offlineshop/data_input_2_down.png")
		button.SetOverVisual("scripts/offlineshop/data_input_2_over.png")

		button.SetPosition(0, 0)
		button.Show()
		self.SetSize(button.GetWidth(), button.GetHeight())
		self.button = button

	def IsInSlot(self):
		if self.IsIn():
			return True

		if self.ownerName:
			if self.ownerName.IsIn():
				return True

		if self.durationText:
			if self.durationText.IsIn():
				return True

		if self.offerCountText:
			if self.offerCountText.IsIn():
				return True

		if self.button:
			if self.button.IsIn():
				return True

		return False

class ShopListElement(ui.Window):
	def __init__(self , info):
		ui.Window.__init__(self)

		self.ownerName = None
		self.shopName = None
		self.durationText = None
		self.countText = None
		self.openShopButton = None
		self.openShopButtonEvent = None
		self.owner_id = -1

		self.__LoadWindow(info)

	def __del__(self):
		self.ownerName = None
		self.shopName = None
		self.durationText = None
		self.countText = None
		self.openShopButton = None
		self.openShopButtonEvent = None

		self.owner_id = -1
		ui.Window.__del__(self)

	def __LoadWindow(self, info):
		owner_id	= info["owner_id"]
		duration	= info["duration"]
		count		= info["count"]
		name		= info["name"]
		
		ownerName	= name[:name.find('@')] if '@' in name else "NONAME"
		name		= name[name.find('@')+1:] if '@' in name else name
		
		self.owner_id  = owner_id
		
		self.__LoadOpenShopButton()
		self.__LoadOwnerName(ownerName)
		self.__LoadShopName(name)
		self.__LoadDuration(duration)
		self.__LoadCount(count)

	def SetOnClickOpenShopButton(self, event):
		self.openShopButton.SAFE_SetEvent(self.__OnClickOpenShop)
		self.openShopButtonEvent = event

	def __OnClickOpenShop(self):
		if self.openShopButtonEvent:
			self.openShopButtonEvent(self.owner_id)

	def __LoadOpenShopButton(self):
		button = ui.Button()
		button.SetParent(self)
		button.SetUpVisual("scripts/offlineshop/data_input_2_norm.png")
		button.SetDownVisual("scripts/offlineshop/data_input_2_down.png")
		button.SetOverVisual("scripts/offlineshop/data_input_2_over.png")

		button.SetPosition(0, 0)
		button.Show()

		self.SetSize(button.GetWidth(), button.GetHeight())
		self.openShopButton = button

	def __LoadOwnerName(self ,ownerName):
		if not ownerName:
			return
		
		text = ui.TextLine()
		text.SetParent(self.openShopButton)
		text.SetPosition(48 , 5)
		text.SetHorizontalAlignCenter()
		text.SetText(ownerName)
		text.Show()
		
		self.ownerName = text

	def __LoadShopName(self ,name):
		text = ui.TextLine()
		text.SetParent(self.openShopButton)
		text.SetPosition(198 , 5)
		text.SetHorizontalAlignCenter()
		text.SetText(name)
		text.Show()
		
		self.shopName = text

	def __LoadDuration(self ,duration):
		text = ui.TextLine()
		text.SetParent(self.openShopButton)
		text.SetPosition(358 , 5)
		text.SetHorizontalAlignCenter()
		text.SetText(GetDurationString(duration))
		text.Show()
		
		self.durationText = text
	
	def __LoadCount(self ,count):
		text = ui.TextLine()
		text.SetParent(self.openShopButton)
		text.SetPosition(510 , 5)
		text.SetHorizontalAlignCenter()
		text.SetText(str(count))
		text.Show()
		
		self.countText = text

class Suggestions():
	def __init__(self):
		self.inputBox = None
		self.comboBox = None

		self.mainDict = {}
		self.tempDict = {}
		self.isRefreshing = False
		self.isSelecting = False
	
	def SetInputBox(self, box):
		box.OnIMEUpdate = self.__OnUpdateInputBox
		self.inputBox = box
	
	def SetComboBox(self, box):
		box.SetEvent(ui.__mem_func__(self.__OnSelectItem))
		box.ClearItem()
		box.SetCurrentItem(localeInfo.OFFLINESHOP_NAME_SUGGESTION_UNSELECT)
		
		self.comboBox = box
	
	def SetMainDict(self, inDict):
		def getUnrefined(st):
			pos = st.find('+')
			if pos == -1:
				return st
			
			if pos > len(st) -4 and pos > 4:
				return st[:pos]
			return st
		
		cleanDict = {}
		inserted  = []
		
		for name , vnum in inDict.items():
			unrefined = getUnrefined(name).lower().strip()
			if unrefined in inserted:
				continue
			
			cleanDict[unrefined] = vnum
			inserted.append(unrefined)
		
		self.mainDict = cleanDict
	
	def __OnUpdateInputBox(self):
		snd.PlaySound("sound/ui/type.wav")
		ui.TextLine.SetText(self.inputBox, ime.GetText(self.inputBox.bCodePage))
		
		self.__RefreshComboBox()
	
	def __RefreshComboBox(self):
		if self.isSelecting:
			return
		
		self.isRefreshing = True
		
		self.tempDict 	= {}
		inputText		= self.inputBox.GetText().lower().strip()
		
		if len(inputText) < 3:
			return
		
		self.comboBox.ClearItem()
		self.comboBox.SetCurrentItem(localeInfo.OFFLINESHOP_NAME_SUGGESTION_UNSELECT)
		
		
		idx = 0
		for k,v in self.mainDict.items():
			if inputText in k.lower():
				self.tempDict[idx] = k
				self.comboBox.InsertItem(idx, k)
				
				idx += 1
				
				if idx == 20:
					break
		
		self.isRefreshing = False
	
	def __OnSelectItem(self, index):
		if self.isRefreshing:
			return
		
		self.isSelecting = True
		self.inputBox.SetText(self.tempDict[index])
		self.isSelecting = False
	
	def __del__(self):
		self.inputBox		= None
		self.comboBox	= None
		
		self.mainDict	= {}
		self.tempDict	= {}
	
	def Clear(self):
		self.comboBox.ClearItem()
		self.comboBox.SetCurrentItem(localeInfo.OFFLINESHOP_NAME_SUGGESTION_UNSELECT)

class SuggestionElement(ui.Button):
	def __init__(self):
		self.clickEvent = None
		self.index = 0

		ui.Button.__init__(self)
	
	def __del__(self):
		self.clickEvent = None
		ui.Button.__del__(self)
	
	def SetClickEvent(self, event):
		self.clickEvent = event
		self.SAFE_SetEvent(self.__OnClickMe)
	
	def __OnClickMe(self):
		if self.clickEvent:
			self.clickEvent(self.index)
	
	
	def SetElement(self, index, text):
		self.index = index
		self.SetText(text)

class SuggestionSelector(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)

		self.scrollbar = None
		self.background = None
		self.attributeDict = {}
		self.onSelectEvent = None

		self.elements = []

		self.__loadBackground()
		self.__loadElements()
		self.__loadScrollbar()
	
	def __loadBackground(self):
		bg = ui.ImageBox()
		bg.LoadImage("scripts/offlineshop/attribute_data_background.png")
		bg.SetParent(self)
		bg.SetPosition(0,-1)

		bg.Show()
		self.background = bg
		self.SetSize(bg.GetWidth() , bg.GetHeight())
	
	def __loadElements(self):
		for x in xrange(6):
			element = SuggestionElement()
			element.SetParent(self.background)
			element.SetPosition(0, x * 23)

			path = "scripts/offlineshop/"
			element.SetUpVisual(path + "ss_input_norm.png")
			element.SetDownVisual(path +"ss_input_down.png")
			element.SetOverVisual(path + "ss_input_hover.png")

			element.Show()
			
			element.SetClickEvent(self.__OnSelectAttribute)
			self.elements.append(element)
	
	def __loadScrollbar(self):
		scroll = ui.NewScrollBar()
		scroll.SetParent(self.background)
		scroll.SetPosition(self.GetWidth()-6, 0)
		scroll.SetScrollBarSize(self.GetHeight())
		scroll.SetScrollEvent(self.__OnScroll)
		scroll.Show()
		
		self.scrollbar = scroll
	
	def __OnSelectAttribute(self, index):
		if self.onSelectEvent:
			self.onSelectEvent(index)

	def __OnScroll(self):
		self.__refreshViewList()
	
	def OnRunMouseWheel(self, nLen):
		if self.scrollbar:
			self.scrollbar.OnRunMouseWheel(nLen)
	
	def __refreshViewList(self):
		pos 		= self.scrollbar.GetPos()
		initIndex	= int(pos * (len(self.attributeDict) - len(self.elements) ))
		
		for x in xrange(initIndex , initIndex + len(self.elements)):
			index 	= self.attributeDict.keys()[x]
			text	= self.attributeDict[index]
			
			self.elements[x-initIndex].SetElement(index, text)

	def SetAttributeDict(self, dct):
		self.attributeDict = dct
		self.__refreshViewList()

	def SetSelectEvent(self, event):
		self.onSelectEvent = event

	def __del__(self):
		self.background 	= None
		self.elements		= []
		self.scrollbar		= None
		self.onSelectEvent	= None
		
		ui.Window.__del__(self)

	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.scrollbar.OnUp()
		else:
			self.scrollbar.OnDown()	

class FilterHistoryElement(ui.Window):
	def __init__(self, info):
		ui.Window.__init__(self)

		self.button = None
		self.datetext = None
		self.timetext = None
		self.counttext = None
		self.buttonEvent = None
		self.info = {}



		self.__loadButton()
		self.__loadDateText(info)
		self.__loadTimeText(info)
		self.__loadCountText(info)

		self.info = info


	def GetInfo(self):
		return self.info


	def SetButtonEvent(self , event):
		self.buttonEvent = event
		self.button.SAFE_SetEvent(self.__OnClickMe)


	def __OnClickMe(self):
		if self.buttonEvent:
			self.buttonEvent(self)

	def __loadButton(self):
		button = ui.Button()
		button.SetParent(self)
		button.SetPosition(0,0)

		path = "scripts/offlineshop/data_input_2_%s.png"

		button.SetUpVisual(path%"norm")
		button.SetDownVisual(path%"down")
		button.SetOverVisual(path%"over")
		button.Show()

		self.SetSize(button.GetWidth(), button.GetHeight())
		self.button = button

	def __loadDateText(self,info):
		text = ui.TextLine()
		text.SetParent(self.button)
		text.SetPosition(60, 5)

		day		= info["day"]
		month	= info["month"]
		year	= info["year"]

		text.SetText("%02d - %02d - %d "%(day, month, year))
		text.Show()

		self.datetext = text


	def __loadTimeText(self, info):
		text = ui.TextLine()
		text.SetParent(self.button)
		text.SetPosition(190+75, 5)


		hour 	= info["hour"]
		minute 	= info["minute"]

		text.SetText("%02d : %02d " % (hour, minute))
		text.Show()

		self.timetext = text

	def __loadCountText(self, info):
		text = ui.TextLine()
		text.SetParent(self.button)
		text.SetPosition(485, 5)

		count = info["count"]

		text.SetText(" %d " % (count))
		text.SetHorizontalAlignCenter()
		text.Show()

		self.counttext = text




	def __del__(self):
		self.button 	= None
		self.datetext	= None
		self.timetext	= None
		self.counttext	= None
		self.buttonEvent= None
		ui.Window.__del__(self)

	def IsInSlot(self):
		if not self.IsShow():
			return False

		if self.IsIn():
			return True

		if self.button:
			if self.button.IsIn():
				return True

		if self.datetext:
			if self.datetext.IsIn():
				return True

		if self.timetext:
			if self.timetext.IsIn():
				return True

		if self.counttext:
			if self.counttext.IsIn():
				return True

		return False

	def GetIndex(self):
		return self.info['id']


class FilterPatternElement(ui.Window):



	def __init__(self, info):
		ui.Window.__init__(self)

		self.button = None
		self.datetext = None
		self.nametext = None
		self.buttonEvent = None
		self.info = {}

		self.__loadButton()
		self.__loadDateText(info)
		self.__loadNameText(info)

		self.info = info


	def GetInfo(self):
		return self.info


	def SetButtonEvent(self , event):
		self.buttonEvent = event
		self.button.SAFE_SetEvent(self.__OnClickMe)


	def __OnClickMe(self):
		if self.buttonEvent:
			self.buttonEvent(self)

	def __loadButton(self):
		button = ui.Button()
		button.SetParent(self)
		button.SetPosition(0,0)

		path = "scripts/offlineshop/data_input_2_%s.png"

		button.SetUpVisual(path%"norm")
		button.SetDownVisual(path%"down")
		button.SetOverVisual(path%"over")
		button.Show()

		self.SetSize(button.GetWidth(), button.GetHeight())
		self.button = button

	def __loadDateText(self,info):
		text = ui.TextLine()
		text.SetParent(self.button)
		text.SetPosition(380, 5)

		day		= info["day"]
		month	= info["month"]
		year	= info["year"]
		hour	= info["hour"]
		minute	= info["minute"]

		text.SetText("%02d - %02d - %d  %02d : %02d"%(day, month, year, hour, minute))
		text.Show()

		self.datetext = text


	def __loadNameText(self, info):
		text = ui.TextLine()
		text.SetParent(self.button)
		text.SetPosition(48, 5)

		text.SetText(info["name"])
		text.Show()

		self.nametext = text




	def __del__(self):
		self.button = None
		self.datetext = None
		self.nametext = None
		self.buttonEvent = None
		ui.Window.__del__(self)

	def IsInSlot(self):
		if not self.IsShow():
			return False

		if self.IsIn():
			return True

		if self.button:
			if self.button.IsIn():
				return True

		if self.datetext:
			if self.datetext.IsIn():
				return True

		if self.nametext:
			if self.nametext.IsIn():
				return True
		return False


	def GetIndex(self):
		return self.info['id']

class NewOfflineShopBoard(ui.ScriptWindow):

	MAX_CATEGORY_ITEMS = 13

	#constants
	BOARD_KEYS = ("create_shop" , "my_shop", "open_shop", "shop_list", "search_history", )
	
	ITEM_TYPES = {
		item.ITEM_TYPE_NONE		: {
			"name" 		: localeInfo.OFFLINESHOP_TYPE_COMBOBOX_NOSET,
		},
		
		item.ITEM_TYPE_WEAPON		: {
			"name" : localeInfo.OFFLINESHOP_TYPE_COMBOBOX_WEAPON,
			"subtypes"	: {
				item.WEAPON_SWORD			:	localeInfo.OFFLINESHOP_COMBOBOX_WEAPON_SWORD,
				item.WEAPON_DAGGER			:	localeInfo.OFFLINESHOP_COMBOBOX_WEAPON_DAGGER,
				item.WEAPON_BOW				:	localeInfo.OFFLINESHOP_COMBOBOX_WEAPON_BOW,
				item.WEAPON_TWO_HANDED		:	localeInfo.OFFLINESHOP_COMBOBOX_WEAPON_TWO_HANDED,
				item.WEAPON_BELL			:	localeInfo.OFFLINESHOP_COMBOBOX_WEAPON_BELL,
				item.WEAPON_FAN				:	localeInfo.OFFLINESHOP_COMBOBOX_WEAPON_FAN,
			},
		},
		
		item.ITEM_TYPE_ARMOR		: {
			"name" : localeInfo.OFFLINESHOP_TYPE_COMBOBOX_ARMOR,
			"subtypes"	: {
				item.ARMOR_BODY			:	localeInfo.OFFLINESHOP_COMBOBOX_ARMOR_BODY,
				item.ARMOR_HEAD			:	localeInfo.OFFLINESHOP_COMBOBOX_ARMOR_HEAD,
				item.ARMOR_SHIELD		:	localeInfo.OFFLINESHOP_COMBOBOX_ARMOR_SHIELD,
				item.ARMOR_WRIST		:	localeInfo.OFFLINESHOP_COMBOBOX_ARMOR_WRIST,
				item.ARMOR_FOOTS		:	localeInfo.OFFLINESHOP_COMBOBOX_ARMOR_FOOTS,
				item.ARMOR_NECK			:	localeInfo.OFFLINESHOP_COMBOBOX_ARMOR_NECK,
				item.ARMOR_EAR			:	localeInfo.OFFLINESHOP_COMBOBOX_ARMOR_EAR,
			},
		},
		
		item.ITEM_TYPE_METIN		: {
			"name" : localeInfo.OFFLINESHOP_TYPE_COMBOBOX_METIN,
		},
		
		item.ITEM_TYPE_FISH		: {
			"name" : localeInfo.OFFLINESHOP_TYPE_COMBOBOX_FISH,
		},
		
		item.ITEM_TYPE_SKILLBOOK		: {
			"name" : localeInfo.OFFLINESHOP_TYPE_COMBOBOX_SKILLBOOK,
		},
		
		item.ITEM_TYPE_USE		: {
			"name" : localeInfo.OFFLINESHOP_TYPE_COMBOBOX_BLEND,
		},
		
		item.ITEM_TYPE_DS		: {
			"name" : localeInfo.OFFLINESHOP_TYPE_COMBOBOX_DS,
		},
		
		item.ITEM_TYPE_UNIQUE		: {
			"name" : localeInfo.OFFLINESHOP_TYPE_COMBOBOX_RING,
		},
		
		item.ITEM_TYPE_BELT		: {
			"name" : localeInfo.OFFLINESHOP_TYPE_COMBOBOX_BELT,
		},


		item.ITEM_TYPE_METIN		: {
			"name" : localeInfo.OFFLINESHOP_TYPE_COMBOBOX_METIN,
		},

		23		: {
			"name" : localeInfo.OFFLINESHOP_TYPE_COMBOBOX_GIFTBOX,
		},

		item.ITEM_TYPE_COSTUME		: {
			"name" : localeInfo.OFFLINESHOP_TYPE_COMBOBOX_COSTUME,
			"subtypes"	: {
				item.COSTUME_TYPE_BODY			:	localeInfo.OFFLINESHOP_COMBOBOX_COSTUME_BODY,
				item.COSTUME_TYPE_HAIR			:	localeInfo.OFFLINESHOP_COMBOBOX_COSTUME_HAIR,
				item.COSTUME_TYPE_MOUNT			:	localeInfo.OFFLINESHOP_COMBOBOX_COSTUME_MOUNT,
				item.COSTUME_TYPE_ACCE			:	localeInfo.OFFLINESHOP_COMBOBOX_COSTUME_ACCE,
				item.COSTUME_TYPE_WEAPON		:	localeInfo.OFFLINESHOP_COMBOBOX_COSTUME_WEAPON,
			},
		},

		item.ITEM_TYPE_MATERIAL		:{
			"name": localeInfo.OFFLINESHOP_TYPE_COMBOBOX_REFINE,
		},
	}
	
	ATTRIBUTES = {
		0	: localeInfo.OFFLINESHOP_ATTR_UNSET,
		
		item.APPLY_MAX_HP 				: localeInfo.OFFLINESHOP_ATTR_MAX_HP,
		item.APPLY_MAX_SP 				: localeInfo.OFFLINESHOP_ATTR_MAX_SP,
		item.APPLY_CON 					: localeInfo.OFFLINESHOP_ATTR_CON,
		item.APPLY_INT 					: localeInfo.OFFLINESHOP_ATTR_INT,
		item.APPLY_STR 					: localeInfo.OFFLINESHOP_ATTR_STR,
		item.APPLY_DEX 					: localeInfo.OFFLINESHOP_ATTR_DEX,
		item.APPLY_ATT_SPEED 			: localeInfo.OFFLINESHOP_ATTR_ATT_SPEED,
		item.APPLY_MOV_SPEED 			: localeInfo.OFFLINESHOP_ATTR_MOV_SPEED,
		item.APPLY_CAST_SPEED 			: localeInfo.OFFLINESHOP_ATTR_CAST_SPEED,
		item.APPLY_HP_REGEN 			: localeInfo.OFFLINESHOP_ATTR_HP_REGEN,
		item.APPLY_SP_REGEN 			: localeInfo.OFFLINESHOP_ATTR_SP_REGEN,
		item.APPLY_POISON_PCT 			: localeInfo.OFFLINESHOP_ATTR_APPLY_POISON_PCT,
		item.APPLY_STUN_PCT 			: localeInfo.OFFLINESHOP_ATTR_APPLY_STUN_PCT,
		item.APPLY_SLOW_PCT 			: localeInfo.OFFLINESHOP_ATTR_APPLY_SLOW_PCT,
		item.APPLY_CRITICAL_PCT 		: localeInfo.OFFLINESHOP_ATTR_APPLY_CRITICAL_PCT,
		item.APPLY_PENETRATE_PCT 		: localeInfo.OFFLINESHOP_ATTR_APPLY_PENETRATE_PCT,

		item.APPLY_ATTBONUS_WARRIOR 	: localeInfo.OFFLINESHOP_ATTR_APPLY_ATTBONUS_WARRIOR,
		item.APPLY_ATTBONUS_ASSASSIN 	: localeInfo.OFFLINESHOP_ATTR_APPLY_ATTBONUS_ASSASSIN,
		item.APPLY_ATTBONUS_SURA 		: localeInfo.OFFLINESHOP_ATTR_APPLY_ATTBONUS_SURA,
		item.APPLY_ATTBONUS_SHAMAN 		: localeInfo.OFFLINESHOP_ATTR_APPLY_ATTBONUS_SHAMAN,
		item.APPLY_ATTBONUS_MONSTER 	: localeInfo.OFFLINESHOP_ATTR_APPLY_ATTBONUS_MONSTER,

		item.APPLY_ATTBONUS_HUMAN 		: localeInfo.OFFLINESHOP_ATTR_APPLY_ATTBONUS_HUMAN,
		item.APPLY_ATTBONUS_ANIMAL 		: localeInfo.OFFLINESHOP_ATTR_APPLY_ATTBONUS_ANIMAL,
		item.APPLY_ATTBONUS_ORC 		: localeInfo.OFFLINESHOP_ATTR_APPLY_ATTBONUS_ORC,
		item.APPLY_ATTBONUS_MILGYO 		: localeInfo.OFFLINESHOP_ATTR_APPLY_ATTBONUS_MILGYO,
		item.APPLY_ATTBONUS_UNDEAD 		: localeInfo.OFFLINESHOP_ATTR_APPLY_ATTBONUS_UNDEAD,
		item.APPLY_ATTBONUS_DEVIL 		: localeInfo.OFFLINESHOP_ATTR_APPLY_ATTBONUS_DEVIL,
		item.APPLY_STEAL_HP 			: localeInfo.OFFLINESHOP_ATTR_APPLY_STEAL_HP,
		item.APPLY_STEAL_SP 			: localeInfo.OFFLINESHOP_ATTR_APPLY_STEAL_SP,
		item.APPLY_MANA_BURN_PCT 		: localeInfo.OFFLINESHOP_ATTR_APPLY_MANA_BURN_PCT,
		item.APPLY_DAMAGE_SP_RECOVER 	: localeInfo.OFFLINESHOP_ATTR_APPLY_DAMAGE_SP_RECOVER,
		item.APPLY_BLOCK 				: localeInfo.OFFLINESHOP_ATTR_APPLY_BLOCK,
		item.APPLY_DODGE 				: localeInfo.OFFLINESHOP_ATTR_APPLY_DODGE,
		item.APPLY_RESIST_SWORD 		: localeInfo.OFFLINESHOP_ATTR_APPLY_RESIST_SWORD,
		item.APPLY_RESIST_TWOHAND 		: localeInfo.OFFLINESHOP_ATTR_APPLY_RESIST_TWOHAND,
		item.APPLY_RESIST_DAGGER 		: localeInfo.OFFLINESHOP_ATTR_APPLY_RESIST_DAGGER,
		item.APPLY_RESIST_BELL 			: localeInfo.OFFLINESHOP_ATTR_APPLY_RESIST_BELL,
		item.APPLY_RESIST_FAN 			: localeInfo.OFFLINESHOP_ATTR_APPLY_RESIST_FAN,
		item.APPLY_RESIST_BOW 			: localeInfo.OFFLINESHOP_ATTR_RESIST_BOW,
		item.APPLY_RESIST_FIRE 			: localeInfo.OFFLINESHOP_ATTR_RESIST_FIRE,
		item.APPLY_RESIST_ELEC 			: localeInfo.OFFLINESHOP_ATTR_RESIST_ELEC,
		item.APPLY_RESIST_MAGIC 		: localeInfo.OFFLINESHOP_ATTR_RESIST_MAGIC,
		item.APPLY_RESIST_WIND 			: localeInfo.OFFLINESHOP_ATTR_APPLY_RESIST_WIND,
		item.APPLY_REFLECT_MELEE 		: localeInfo.OFFLINESHOP_ATTR_APPLY_REFLECT_MELEE,
		item.APPLY_POISON_REDUCE 		: localeInfo.OFFLINESHOP_ATTR_APPLY_POISON_REDUCE,
		item.APPLY_EXP_DOUBLE_BONUS 	: localeInfo.OFFLINESHOP_ATTR_APPLY_EXP_DOUBLE_BONUS,
		item.APPLY_GOLD_DOUBLE_BONUS 	: localeInfo.OFFLINESHOP_ATTR_APPLY_GOLD_DOUBLE_BONUS,
		item.APPLY_ITEM_DROP_BONUS 		: localeInfo.OFFLINESHOP_ATTR_APPLY_ITEM_DROP_BONUS,
		item.APPLY_IMMUNE_STUN 			: localeInfo.OFFLINESHOP_ATTR_APPLY_IMMUNE_STUN,
		item.APPLY_IMMUNE_SLOW 			: localeInfo.OFFLINESHOP_ATTR_APPLY_IMMUNE_SLOW,
		item.APPLY_IMMUNE_FALL 			: localeInfo.OFFLINESHOP_ATTR_APPLY_IMMUNE_FALL,
		item.APPLY_DEF_GRADE_BONUS 		: localeInfo.OFFLINESHOP_ATTR_DEF_GRADE,
		item.APPLY_ATT_GRADE_BONUS 		: localeInfo.OFFLINESHOP_ATTR_ATT_GRADE,
		item.APPLY_MAGIC_ATT_GRADE 		: localeInfo.OFFLINESHOP_ATTR_MAGIC_ATT_GRADE,
		item.APPLY_MAGIC_DEF_GRADE 		: localeInfo.OFFLINESHOP_ATTR_MAGIC_DEF_GRADE,
		item.APPLY_SKILL_DAMAGE_BONUS 	: localeInfo.OFFLINESHOP_ATTR_SKILL_DAMAGE_BONUS,

		item.APPLY_NORMAL_HIT_DAMAGE_BONUS 	: localeInfo.OFFLINESHOP_ATTR_NORMAL_HIT_DAMAGE_BONUS,
		item.APPLY_SKILL_DEFEND_BONUS 		: localeInfo.OFFLINESHOP_ATTR_SKILL_DEFEND_BONUS,
		item.APPLY_NORMAL_HIT_DEFEND_BONUS 	: localeInfo.OFFLINESHOP_ATTR_NORMAL_HIT_DEFEND_BONUS,

		item.APPLY_MAGIC_ATTBONUS_PER 		: localeInfo.OFFLINESHOP_ATTR_MAGIC_ATTBONUS_PER,
		item.APPLY_MELEE_MAGIC_ATTBONUS_PER : localeInfo.OFFLINESHOP_ATTR_MELEE_MAGIC_ATTBONUS_PER,
		item.APPLY_RESIST_ICE 				: localeInfo.OFFLINESHOP_ATTR_RESIST_ICE,
		item.APPLY_RESIST_EARTH 			: localeInfo.OFFLINESHOP_ATTR_RESIST_EARTH,
		item.APPLY_RESIST_DARK 				: localeInfo.OFFLINESHOP_ATTR_RESIST_DARK,
		item.APPLY_ANTI_CRITICAL_PCT 		: localeInfo.OFFLINESHOP_ATTR_ANTI_CRITICAL_PCT,
		item.APPLY_ANTI_PENETRATE_PCT 		: localeInfo.OFFLINESHOP_ATTR_ANTI_PENETRATE_PCT,
# NEW BONUS
		#item.APPLY_ATTBONUS_BOSS			: localeInfo.TOOLTIP_APPLY_ATTBONUS_BOSS,
		#item.APPLY_ATTBONUS_METIN			: localeInfo.TOOLTIP_APPLY_ATTBONUS_METIN,
# END
	}

	# if app.ELEMENT_NEW_BONUSES:
		# ATTRIBUTES.update({
			# item.APPLY_ATTBONUS_ELEC 		: localeInfo.TOOLTIP_APPLY_ENCHANT_ELECT,
			# item.APPLY_ATTBONUS_FIRE 		: localeInfo.TOOLTIP_APPLY_ENCHANT_FIRE,
			# item.APPLY_ATTBONUS_ICE 			: localeInfo.TOOLTIP_APPLY_ENCHANT_ICE,
			# item.APPLY_ATTBONUS_WIND 		: localeInfo.TOOLTIP_APPLY_ENCHANT_WIND,
			# item.APPLY_ATTBONUS_EARTH 		: localeInfo.TOOLTIP_APPLY_ENCHANT_EARTH,
			# item.APPLY_ATTBONUS_DARK 		: localeInfo.TOOLTIP_APPLY_ENCHANT_DARK,
			# item.APPLY_ATTBONUS_FORT_ZODIAC	 		: localeInfo.TOOLTIP_APPLY_ATTBONUS_CZ,
			# item.APPLY_ATTBONUS_INSECT 		: localeInfo.TOOLTIP_APPLY_ATTBONUS_INSECT,
			# item.APPLY_ATTBONUS_DESERT 		: localeInfo.TOOLTIP_APPLY_ATTBONUS_DESERT,
		# })

	# if app.ENABLE_PENDANT:
		# ATTRIBUTES.update({
			# item.APPLY_ATTBONUS_IRR_SPADA 		: localeInfo.TOOLTIP_APPLY_ATTBONUS_SWORD,
			# item.APPLY_ATTBONUS_IRR_SPADONE 	: localeInfo.TOOLTIP_APPLY_ATTBONUS_TWOHAND,
			# item.APPLY_ATTBONUS_IRR_PUGNALE 		: localeInfo.TOOLTIP_APPLY_ATTBONUS_DAGGER,
			# item.APPLY_ATTBONUS_IRR_FRECCIA 		: localeInfo.TOOLTIP_APPLY_ATTBONUS_BELL,
			# item.APPLY_ATTBONUS_IRR_VENTAGLIO 		: localeInfo.TOOLTIP_APPLY_ATTBONUS_FAN,
			# item.APPLY_ATTBONUS_IRR_CAMPANA 		: localeInfo.TOOLTIP_APPLY_ATTBONUS_BOW,
			# item.APPLY_RESIST_MEZZIUOMINI 		: localeInfo.TOOLTIP_APPLY_RESIST_HUMAN,
			# item.APPLY_DEF_TALISMAN 	: localeInfo.TOOLTIP_APPLY_RESIST_MOUNT_FALL,
		# })

# END

	if app.ENABLE_MAGIC_REDUCTION_SYSTEM:
		ATTRIBUTES.update({
			item.APPLY_RESIST_MAGIC_REDUCTION : localeInfo.OFFLINESHOP_ATTR_RESIST_MAGIC_REDUCTION,
		})

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.clear()
		offlineshop.SetOfflineshopBoard(self)
		self.__loadWindow()

	def clear(self):
		self.MyShopButton = None
		self.ListOfShopButton = None
		self.SearchFilterButton = None
		self.SearchHistoryButton = None
		self.MyPatternsButton = None

		# self.MyAuctionButton = None
		self.ListOfAuctionsButton = None

		self.pageBoards = {}
		self.pageCategory = "my_shop"
		self.updateEvents = {}
		self.itemTooltip = None
		self.popupMessage = None
		self.ShopItemForSale = []
		self.ShopItemSold = []
		self.EditPriceSlot = None
		self.AddItemSlotIndex = -1
		self.CommonInputPriceDlg = None
		self.CommonQuestionDlg = None
		self.CommonPickValuteDlg = None
		self.TitleBar = None

		self.SearchFilterShopItemResult = []
		self.FilterHistory = []
		self.FilterPatterns = {}

		self.ShopList = []
		self.ShopOpenInfo = {}
		self.ShopListTable = None

		self.InsertedItems = []
		self.CreateShopNameEdit = None
		self.CreateShopDaysCountText = None
		self.CreateShopHoursCountText = None
		self.CreateShopItemsTable = None
		self.CreateShopItemsInfos = {}

		self.MyShopItemsTable = None
		self.MyShopShopTitle = None
		self.MyShopShopDuration = None
		self.MyShopCloseButton = None

		self.MyShopGauge = None

		self.MyShopEditNameDlg = None
		self.MyShopOffers = None
		self.MyShopOffersTable = None

		self.OpenShopItemsTable = None
		self.OpenShopBackToListButton = None
		self.OpenShopShopTitle = None
		self.OpenShopShopDuration = None
		self.OpenShopBuyItemID = -1
		self.BuyPriceSeenTotal = 0

		self.SearchFilterItemsNameDict = {}
		self.SearchFilterCheckBoxesRace = {}
		self.SearchFilterCheckBoxes = {}

		self.SearchFilterComboBoxSuggestion = None
		self.SearchFilterSuggestionObj = None
		self.SearchFilterItemNameInput = None
		self.SearchFilterResetFilterButton = None
		self.SearchFilterSavePatternButton = None
		self.SearchFilterStartSearch = None
		self.MainScrollBar = None

		self.SearchFilterResultItemsTable = None

		self.SearchHistoryTable = None

		self.SearchPatternsTable = None
		self.SearchPatternsInputNameDlg = None

		self.ShopSafeboxItems = []
		self.ShopSafeboxItemsTable = None
		self.ShopSafeboxValuteAmount=0
		self.ShopSafeboxValuteText = None
		self.ShopSafeboxWithdrawYangButton = None

		self.MyOffersList = None
		self.MyOffersTable = None

		self.MyAuctionInfo = {}
		self.MyAuctionOffers = []
		self.MyAuctionOfferTable = None

		self.MyAuctionOwnerName = None
		self.MyAuctionDuration = None
		self.MyAuctionBestOffer = None
		self.MyAuctionMinRaise = None
		self.MyAuctionSlot = None

		self.OpenAuctionInfo = {}
		self.OpenAuctionOffers = []
		self.OpenAuctionOfferTable = None

		self.OpenAuctionBackToListButton = None

		self.OpenAuctionOwnerName = None
		self.OpenAuctionDuration = None
		self.OpenAuctionBestOffer = None
		self.OpenAuctionMinRaise = None
		self.OpenAuctionSlot = None

		self.AuctionListInfo = {}
		self.AuctionListTable = None

		self.CreateAuctionCreateAuctionButton = None
		self.CreateAuctionDaysInput = None
		self.CreateAuctionStartingPriceInput = None
		self.CreateAuctionSlot = None
		self.CreateAuctionDaysIncreaseButton = None
		self.CreateAuctionDaysDecreaseButton = None

		self.RefreshSymbol = None

		if app.KASMIR_PAKET_SYSTEM:
			#self.wndRender = None
			#self.wndRenderPreview = None
			self.KasmirNpc = 0
			# self.btnIncRender = None
			# self.btnDecRender = None

	def Destroy(self):
		self.Hide()
		self.clear()
		self.ClearDictionary()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def __del__(self):
		self.Destroy()
		print("------------ DESTROYED OFFLINESHOP INTERFACE ------------")
		ui.ScriptWindow.__del__(self)

	def __loadWindow(self):
		pyLoader = ui.PythonScriptLoader()
		pyLoader.LoadScriptFile(self , "uiscript/offlineshopwindow.py")
		
		childDict = {
			"create_shop"		: "MyShopBoardNoShop",
			"my_shop"			: "MyShopBoard",
			"open_shop"			: "ListOfShop_OpenShop",
			"shop_list"			: "ListOfShop_List",
			"shop_safebox"		: "ShopSafeboxPage",
			"my_offers"			: "MyOffersPage",

			"search_history"	: "SearchHistoryBoard",
			"my_patterns"		: "MyPatternsBoard",
			"search_filter"		: "SearchFilterBoard",

			"my_auction"		: "MyAuction",
			"auction_list"		: "AuctionList",
			"open_auction"		: "OpenAuction",
			"create_auction"	: "CreateAuction",

		}

		self.pageBoards = {}
		
		for k, v in childDict.items():
			self.pageBoards[k] = self.GetChild(v)
			self.pageBoards[k].Hide()

		if app.KASMIR_PAKET_SYSTEM:
			self.KasmirNpc = 30000

		#refresh symbol
		self.RefreshSymbol = self.GetChild("AnimationWindow")

		self.CreateShopNameEdit				= self.GetChild("ShopNameInput")
		self.CreateShopDaysCountText		= self.GetChild("DaysCountText")
		self.CreateShopHoursCountText		= self.GetChild("HoursCountText")
		
		self.CreateShopIncreaseDaysButton	= self.GetChild("IncreaseDaysButton")
		self.CreateShopDecreaseDaysButton	= self.GetChild("DecreaseDaysButton")
		
		self.CreateShopIncreaseHoursButton	= self.GetChild("IncreaseHoursButton")
		self.CreateShopDecreaseHoursButton	= self.GetChild("DecreaseHoursButton")
		
		self.CreateShopButton				= self.GetChild("CreateShopButton")
		
		self.CreateShopIncreaseDaysButton.SAFE_SetEvent(self.__OnClickCreateShopIncreaseDaysButton)
		self.CreateShopDecreaseDaysButton.SAFE_SetEvent(self.__OnClickCreateShopDecreaseDaysButton)
		
		self.CreateShopIncreaseHoursButton.SAFE_SetEvent(self.__OnClickCreateShopIncreaseHoursButton)
		self.CreateShopDecreaseHoursButton.SAFE_SetEvent(self.__OnClickCreateShopDecreaseHoursButton)

		self.CreateShopButton.SAFE_SetEvent(self.__OnClickCreateShopButton)
		self.__MakeCreateShopItemsTable()

		self.MyShopShopDuration		= self.GetChild("MyShopShopDuration")
		self.MyShopShopTitle		= self.GetChild("MyShopShopTitle")
		self.MyShopCloseButton		= self.GetChild("MyShopCloseButton")
		self.MyShopGauge			= self.GetChild("Shop_Time_Gauge")
		self.MyShopEditTitleButton	= self.GetChild("MyShopEditTitleButton")
		self.__MakeMyShopItemsTable()
		self.__MakeMyShopOffersTable()
		
		self.MyShopCloseButton.SAFE_SetEvent(self.__OnClickCloseButton)
		self.MyShopEditTitleButton.SAFE_SetEvent(self.__OnClickMyShopEditNameButton)
		
		self.MyShopEditNameDlg	= uiCommon.InputDialogWithDescription()
		self.MyShopEditNameDlg.SetMaxLength(35)
		self.MyShopEditNameDlg.SetDescription(localeInfo.OFFLINESHOP_EDIT_SHOPNAME_DESCRIPTION)
		self.MyShopEditNameDlg.SetAcceptEvent(self.__OnAcceptChangeShopNameDlg)
		self.MyShopEditNameDlg.SetCancelEvent(self.__OnCancelChangeShopNameDlg)
		self.MyShopEditNameDlg.SetTitle(localeInfo.OFFLINESHOP_EDIT_SHOPNAME_TITLE)
		self.MyShopEditNameDlg.Hide()

		self.__MakeShopListTable()

		self.OpenShopBackToListButton	= self.GetChild("OpenShopBackToListButton")
		self.OpenShopShopTitle			= self.GetChild("OpenShopShopTitle")
		self.OpenShopShopDuration		= self.GetChild("OpenShopShopDuration")
		
		self.CommonQuestionDlg 	= uiCommon.QuestionDialog()

		self.CommonPickValuteDlg = uiPickMoney.PickMoneyDialog()
		self.CommonPickValuteDlg.LoadDialog()

		self.OpenShopBackToListButton.SAFE_SetEvent(self.__OnClickShopListPage)
		self.__MakeOpenShopItemsTable()


		self.TitleBar = self.GetChild("TitleBar")
		self.TitleBar.SetCloseEvent(self.Close)

		self.MyShopButton			= self.GetChild("MyShopButton")
		# self.MyAuctionButton		= self.GetChild("MyAuctionButton")
		self.ShopSafeboxButton		= self.GetChild("ShopSafeboxButton")
		self.SearchFilterButton		= self.GetChild("SearchFilterButton")

		self.MenuButton 			= ExpandingMenu(self, localeInfo.OFFLINE_SHOP_MENU)
		self.MenuButton.SetPosition(426, 32)

		self.MenuButton.AddMenuOption(localeInfo.OFFLINESHOP_TITLE_LIST_OF_SHOPS , self.__OnClickShopListPage)
		self.MenuButton.AddMenuOption(localeInfo.OFFLINESHOP_TITLE_MY_OFFERS, self.__OnClickMyOffersPage)
		self.MenuButton.AddMenuOption(localeInfo.OFFLINESHOP_TITLE_SEARCH_HISTORY, self.__OnClickSearchHistoryPage)
		self.MenuButton.AddMenuOption(localeInfo.OFFLINESHOP_TITLE_MY_PATTERNS, self.__OnClickMyPatternsPage)
		# self.MenuButton.AddMenuOption(localeInfo.OFFLINESHOP_TITLE_AUCTION_LIST, self.__OnClickAuctionListPage)

		#events setting
		self.MyShopButton.SAFE_SetEvent(self.__OnClickMyShopPage)


		self.ShopSafeboxButton.SAFE_SetEvent(self.__OnClickShopSafeboxPage)
		self.SearchFilterButton.SAFE_SetEvent(self.__OnClickSearchFilterPage)
		# self.MyAuctionButton.SAFE_SetEvent(self.__OnClickMyAuctionPage)


		self.updateEvents = {
			"my_shop"		: self.__OnUpdateMyShopPage,
			"create_shop"	: self.__OnUpdateCreateShopPage,
			"open_shop"		: self.__OnUpdateOpenShopPage,
			"search_filter"	: self.__OnUpdateSearchFilterPage,
			"shop_safebox"	: self.__OnUpdateShopSafeboxPage,
			"my_offers"		: self.__OnUpdateMyOffersPage,
			"search_history": self.__OnUpdateSearchHistoryPage,
			"my_patterns"	: self.__OnUpdateMyPatternPage,
			"create_auction": self.__OnUpdateCreateAuctionPage,
			"my_auction"	: self.__OnUpdateMyAuctionPage,
			"open_auction"	: self.__OnUpdateOpenAuctionPage,
			"auction_list"  : self.__OnUpdateAuctionListPage,
		}

		tooltip = uiTooltip.ItemToolTip(width=300)
		tooltip.ClearToolTip()
		tooltip.SetFollow(True)
		tooltip.Hide()
		self.itemTooltip = tooltip

		popup = uiCommon.PopupDialog()
		popup.SetWidth(250)
		popup.Hide()
		self.popupMessage = popup

		self.CommonInputPriceDlg =  uiCommon.MoneyInputDialog()
		self.CommonInputPriceDlg.SetAcceptEvent(self.__OnAcceptInputPrice)
		self.CommonInputPriceDlg.SetCancelEvent(self.__OnCancelInputPrice)

		offlineshop.RefreshItemNameMap()
		self.__MakeSearchFilterResultItemsTable()

		self.SearchFilterItemNameInput 		= self.GetChild("SearchFilterItemNameInput")
		self.SearchFilterResetFilterButton	= self.GetChild("SearchFilterResetFilterButton")
		self.SearchFilterSavePatternButton	= self.GetChild("SearchFilterSavePatternButton")
		self.SearchFilterStartSearch		= self.GetChild("SearchFilterStartSearch")
		
		self.__MakeSearchFilterCheckBoxes()
		self.SearchFilterComboBoxSuggestion	= ui.ComboBox()
		self.SearchFilterComboBoxSuggestion.SetParent(self.pageBoards["search_filter"])
		self.SearchFilterComboBoxSuggestion.SetPosition(15+5,51)
		self.SearchFilterComboBoxSuggestion.SetSize(175,24)
		self.SearchFilterComboBoxSuggestion.Show()


		self.SearchFilterSuggestionObj = Suggestions()
		self.SearchFilterSuggestionObj.SetComboBox(self.SearchFilterComboBoxSuggestion)
		self.SearchFilterSuggestionObj.SetInputBox(self.SearchFilterItemNameInput)
		self.SearchFilterSuggestionObj.SetMainDict(self.SearchFilterItemsNameDict)
		
		self.SearchFilterResetFilterButton.SAFE_SetEvent(self.__OnClickSearchFilterResetFilterButton)
		self.SearchFilterSavePatternButton.SAFE_SetEvent(self.__OnClickSearchFilterSavePatternButton)
		self.SearchFilterStartSearch.SAFE_SetEvent(self.__OnClickSearchFilterStartSearch)


		self.categoryButtons = []
		self.selectedCategory = 0
		self.selectedSubCategory = 0
		self.categoryButtonCount = 0

		self.CategoryContainer = self.GetChild("CategoryContainer")
		self.CategoryScrollBar = self.GetChild("CategoryScrollBar")
		self.CategoryScrollBar.SetScrollEvent(self.OnCategoryScroll)

		for k,v in self.ITEM_TYPES.items():
			btn = self.__AddCategoryButton(v["name"], k)
			if self.ITEM_TYPES.has_key(k) and self.ITEM_TYPES[k].has_key('subtypes'):
				for sub, name in self.ITEM_TYPES[k]['subtypes'].items():
					btn.AddSubButton(name, sub)

		self.RefreshButtons()

		self.SearchFilterTypeComboBoxIndex = 0
		self.SearchFilterSubTypeComboBoxIndex = SUBTYPE_NOSET

		selector = SuggestionSelector()
		selector.SetParent(self.pageBoards["search_filter"])
		selector.SetSelectEvent(self.__OnSelectSearchFilterSuggestionSelector)
		selector.SetAttributeDict(self.ATTRIBUTES)
		selector.Hide()
		
		
		self.SearchFilterSuggestionSelector = selector
		self.SearchFilterAttributeSetting = [0 for x in xrange(player.ATTRIBUTE_SLOT_NORM_NUM)]

		self.__MakeSearchHistoryTable()

		self.__MakeSearchPatternsTable()
		self.SearchPatternsInputNameDlg = uiCommon.InputDialogWithDescription()
		self.SearchPatternsInputNameDlg.SetMaxLength(25)
		self.SearchPatternsInputNameDlg.SetDescription(localeInfo.OFFLINESHOP_MY_PATTERN_INSERT_NAME_DESC)
		self.SearchPatternsInputNameDlg.SetAcceptEvent(self.__OnAcceptMyPatternInputName)
		self.SearchPatternsInputNameDlg.SetCancelEvent(self.__OnCancelMyPatternInputName)
		self.SearchPatternsInputNameDlg.SetTitle(localeInfo.OFFLINESHOP_MY_PATTERN_INSERT_NAME_TITLE)
		self.SearchPatternsInputNameDlg.Hide()

		self.__MakeShopSafeboxItemsTable()
		self.ShopSafeboxValuteText 			= self.GetChild("ShopSafeboxValuteText")
		self.ShopSafeboxWithdrawYangButton	= self.GetChild("ShopSafeboxWithdrawYangButton")

		self.ShopSafeboxWithdrawYangButton.SAFE_SetEvent(self.__OnClickShopSafeboxWithdrawYang)

		self.__MakeMyOffersTable()

		self.MyAuctionOwnerName 	= self.GetChild("MyAuction_OwnerName")
		self.MyAuctionDuration 		= self.GetChild("MyAuction_Duration")
		self.MyAuctionBestOffer 	= self.GetChild("MyAuction_BestOffer")
		self.MyAuctionMinRaise 		= self.GetChild("MyAuction_MinRaise")
		
		self.__MakeMyAuctionOffersTable()

		#open auction page
		self.OpenAuctionBackToListButton = self.GetChild("OpenAuctionBackToListButton")
		self.OpenAuctionOwnerName	= self.GetChild("OpenAuction_OwnerName")
		self.OpenAuctionDuration 	= self.GetChild("OpenAuction_Duration")
		self.OpenAuctionBestOffer 	= self.GetChild("OpenAuction_BestOffer")
		self.OpenAuctionMinRaise 	= self.GetChild("OpenAuction_MinRaise")

		self.OpenAuctionBackToListButton.SAFE_SetEvent(self.__OnClickAuctionListPage)
		self.__MakeOpenAuctionOffersTable()

		self.__MakeAuctionListTable()

		self.CreateAuctionCreateAuctionButton 	= self.GetChild("CreateAuctionCreateAuctionButton")
		self.CreateAuctionDaysInput 			= self.GetChild("CreateAuctionDaysInput")
		self.CreateAuctionStartingPriceInput 	= self.GetChild("CreateAuctionStartingPriceInput")

		self.CreateAuctionWindowPos =-1
		self.CreateAuctionSlotPos=-1

		self.CreateAuctionDaysDecreaseButton	= self.GetChild("CreateAuctionIncreaseDaysButton")
		self.CreateAuctionDaysIncreaseButton	= self.GetChild("CreateAuctionDecreaseDaysButton")

		self.CreateAuctionCreateAuctionButton.SAFE_SetEvent(self.__OnClickCreateAuctionButton)
		self.CreateAuctionDaysDecreaseButton.SAFE_SetEvent(self.__OnClickCreateAuctionDaysDecreaseButton)
		self.CreateAuctionDaysIncreaseButton.SAFE_SetEvent(self.__OnClickCreateAuctionDaysIncreaseButton)
		self.__MakeCreateAuctionSlot()

		items = (
			self.CreateShopNameEdit,
			self.SearchFilterItemNameInput,
			self.CreateAuctionStartingPriceInput,
		)

		autokill = lambda arg: arg.KillFocus()

		for item in items:
			item.OnPressEscapeKey = autokill

	if app.KASMIR_PAKET_SYSTEM:
		def OnClickIncBtn(self):
			if self.pageBoards["create_shop"].IsShow():
				if self.KasmirNpc >= 30007:
					self.KasmirNpc = 30000
				else:
					self.KasmirNpc += 1
			
				#renderTarget.SelectModel(2, self.KasmirNpc)

		def OnClickDecBtn(self):
			if self.pageBoards["create_shop"].IsShow():
				if self.KasmirNpc <= 30000:
					self.KasmirNpc = 30007
				else:
					self.KasmirNpc -= 1
			
				#renderTarget.SelectModel(2, self.KasmirNpc)

	def Open(self):
		events = {
			"my_shop"			: self.__OnClickMyShopPage,
			"open_shop"			: self.__OnClickShopListPage,
			"shop_list"			: self.__OnClickShopListPage,
			"shop_safebox"		: self.__OnClickShopSafeboxPage,
			"my_offers"			: self.__OnClickMyOffersPage,

			"search_history"	: self.__OnClickSearchHistoryPage,
			"my_patterns"		: self.__OnClickMyPatternsPage,
			"search_filter"		: self.__OnClickSearchFilterPage,

			"my_auction"		: self.__OnClickMyAuctionPage,
			"auction_list"		: self.__OnClickAuctionListPage,
			"open_auction"		: self.__OnClickAuctionListPage,
		}

		if self.pageCategory in events.keys():
			events[self.pageCategory]()

		if app.KASMIR_PAKET_SYSTEM:
			if self.pageBoards["create_shop"].IsShow() or self.pageCategory == "my_shop":
				#if self.wndRenderPreview:
				self.KasmirNpc = 30000
					#renderTarget.SelectModel(2, self.KasmirNpc)

		self.Show()

	def OpenSearch(self):
		offlineshop.SendCloseBoard()
		self.pageCategory = "search_filter"
		for page in self.pageBoards.values():
			page.Hide()

		self.pageBoards["search_filter"].Show()
		self.Show()
		
	def Close(self):
		self.Hide()
		self.itemTooltip.Hide()
		self.MyShopEditNameDlg.Hide()
		self.CommonQuestionDlg.Hide()
		self.CommonPickValuteDlg.Hide()
		self.CommonInputPriceDlg.Hide()

		offlineshop.SendCloseBoard()

	def __ResetCreateShopPage(self):
		self.CreateShopItemsTable.ClearElement()
		self.CreateShopItemsInfos = {}

	def __MakeCreateShopItemsTable(self):
		board = self.pageBoards["create_shop"]
		
		table = TableWindowWithScrollbar(575, 325, 11,3, TableWindowWithScrollbar.SCROLLBAR_HORIZONTAL)
		table.SetParent(board)
		table.SetPosition(24, 95)
		table.SetDefaultCreateChild(MakeDefaultEmptySlot, self.__OnClickCreateShopEmptySlot)
		
		table.Show()
		self.CreateShopItemsTable = table
	
	def __MakeMyShopItemsTable(self):
		board = self.pageBoards["my_shop"]

		table = TableWindowWithScrollbar(575, 315, 11,3, TableWindowWithScrollbar.SCROLLBAR_VERTICAL)
		table.SetParent(board)
		table.SetPosition(24, 35)
		table.SetDefaultCreateChild(MakeDefaultEmptySlot, self.__OnClickMyShopEmptySlot)

		table.Show()
		self.MyShopItemsTable = table
	
	def __MakeMyShopOffersTable(self):
		board = self.pageBoards["my_shop"]

		table = TableWindowWithScrollbar(585, 90-5, 1,6 , TableWindowWithScrollbar.SCROLLBAR_VERTICAL)
		table.SetParent(board)
		table.SetPosition(16, 408)

		table.Show()
		self.MyShopOffersTable = table


	def __MakeShopListTable(self):
		board = self.pageBoards["shop_list"]

		table = TableWindowWithScrollbar(590, 500-15, 1, 20, TableWindowWithScrollbar.SCROLLBAR_VERTICAL)
		table.SetParent(board)
		table.SetPosition(10, 19)

		table.Show()
		self.ShopListTable = table

	def __MakeOpenShopItemsTable(self):
		board = self.pageBoards["open_shop"]
		
		table = TableWindowWithScrollbar(584, 440, 11,4, TableWindowWithScrollbar.SCROLLBAR_HORIZONTAL)
		table.SetParent(board)
		table.SetPosition(20,55)
		table.SetDefaultCreateChild(MakeDefaultEmptySlot)
		
		table.Show()
		self.OpenShopItemsTable = table

	def __MakeOpenAuctionOffersTable(self):
		board = self.pageBoards["open_auction"]

		table = TableWindowWithScrollbar(590, 290, 1, 12, TableWindowWithScrollbar.SCROLLBAR_VERTICAL)
		table.SetParent(board)
		table.SetPosition(10, 165)

		table.Show()
		self.OpenAuctionOfferTable = table


	def __MakeMyAuctionOffersTable(self):
		board = self.pageBoards["my_auction"]

		table = TableWindowWithScrollbar(590, 290, 1, 12, TableWindowWithScrollbar.SCROLLBAR_VERTICAL)
		table.SetParent(board)
		table.SetPosition(10, 165)

		table.Show()
		self.MyAuctionOfferTable = table


	def __MakeAuctionListTable(self):
		board = self.pageBoards["auction_list"]

		table = TableWindowWithScrollbar(590, 500-15, 1, 20, TableWindowWithScrollbar.SCROLLBAR_VERTICAL)
		table.SetParent(board)
		table.SetPosition(10, 19)

		table.Show()
		self.AuctionListTable = table

	def SetCategory(self, category, subcategory):
		self.SearchFilterTypeComboBoxIndex = category
		self.SearchFilterSubTypeComboBoxIndex = subcategory

		for i in range(len(self.categoryButtons)):
			self.categoryButtons[i].UpdateSubButtons(category, subcategory)

	def RefreshButtons(self):
		self.__RefreshCategoryButtons(False)

	def __AddCategoryButton(self, name, category_id):
		button = CategoryButton(self.CategoryContainer, self, name, category_id)
		button.SetPosition(0, len(self.categoryButtons) * 28)

		self.categoryButtons.append(button)

		return button

	def __RefreshCategoryButtons(self, isScroll):
		self.categoryButtonCount = 0
		for i in range(len(self.categoryButtons)):
			self.categoryButtonCount += 1
			if self.categoryButtons[i].active:
				self.categoryButtonCount += len(self.categoryButtons[i].subButtons)

		pos = int(self.CategoryScrollBar.GetPos() * (self.categoryButtonCount - NewOfflineShopBoard.MAX_CATEGORY_ITEMS))

		top = 0
		count = 0
		for i in range(len(self.categoryButtons)):
			if count < pos or count >= (pos + NewOfflineShopBoard.MAX_CATEGORY_ITEMS):
				self.categoryButtons[i].SetPositionHelper(0, top - (pos - count) * 28)
				self.categoryButtons[i].Hide()
			else:
				self.categoryButtons[i].SetPositionHelper(0, top)
				self.categoryButtons[i].Show()
				top += 28

			if self.categoryButtons[i].active:
				for sub in range(len(self.categoryButtons[i].subButtons)):
					count += 1

					if count < pos or count >= (pos + NewOfflineShopBoard.MAX_CATEGORY_ITEMS):
						self.categoryButtons[i].subButtons[sub][0].Hide()
					else:
						self.categoryButtons[i].subButtons[sub][0].Show()

						top += 28

			count += 1

		if not isScroll:
			self.CategoryScrollBar.SetMiddleBarSize(float(NewOfflineShopBoard.MAX_CATEGORY_ITEMS) / float(self.categoryButtonCount))

		if self.categoryButtonCount > 13:
			self.CategoryScrollBar.Show()
		else:
			self.CategoryScrollBar.Hide()

	def OnCategoryScroll(self):
		self.__RefreshCategoryButtons(True)


	def __MakeSearchFilterCheckBoxes(self):
		positions = {
			"name" 	: { "x" : 6+98-5,	"y" : 6, 	},
			"wear" 	: { "x" : 6+98-5, 	"y" : 78, 	},
			"type" 	: { "x" : 6+98-5, 	"y" : 120, 	},
		}

		race = {
			"warrior"	: {   "x" : 140-6, 	"y" : 95, 	},
			"assassin"	: { "x" : 110-6, 	"y" : 95, 	},
			"sura"		: { "x" : 75, 	"y" : 95, 	},
			"shaman"	: { "x" : 50-4, 	"y" : 95, 	},
		}

		for k, v in positions.items():
			checkbox = ui.CustomCheckBox({'base' : "d:/ymir work/ui/checkbox/checkbox_new_unselected.tga", 'tip' : "d:/ymir work/ui/checkbox/checkbox_new_selected.tga",})
			checkbox.SetParent(self.pageBoards["search_filter"])
			checkbox.SetPosition(v["x"] , v["y"])
			checkbox.Show()
			
			self.SearchFilterCheckBoxes[k] = checkbox
		
		
		for k, v in race.items():
			checkbox = ui.CustomCheckBox({'base' : "offlineshop/checkbox/%s_base.png"%k , 'tip' : "offlineshop/checkbox/%s_tip.png"%k,})
			checkbox.SetParent(self.pageBoards["search_filter"])
			checkbox.SetPosition(v["x"] , v["y"])
			checkbox.Show()
			checkbox.Enable()

			self.SearchFilterCheckBoxesRace[k] = checkbox


	def __MakeSearchFilterResultItemsTable(self):
		board = self.pageBoards["search_filter"]

		ItemContainerListBox = NewListBoxOfflineShop()
		ItemContainerListBox.SetParent(board)
		ItemContainerListBox.SetSize(375, 460)
		ItemContainerListBox.SetPosition(204, 2)
		ItemContainerListBox.Show()

		ItemContainerListBox.ClearItems()

		self.MainScrollBar = self.GetChild("ContainerScrollBar")

		self.SearchFilterResultItemsTable = ItemContainerListBox
		self.SearchFilterResultItemsTable.SetScrollBar(self.MainScrollBar)

	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.MainScrollBar.OnUp()
		else:
			self.MainScrollBar.OnDown()

	def __MakeSearchHistoryTable(self):
		board = self.pageBoards["search_history"]

		table = TableWindowWithScrollbar(590, 500-15, 1, 20 , TableWindowWithScrollbar.SCROLLBAR_VERTICAL)
		table.SetParent(board)
		table.SetPosition(10, 19)

		table.Show()
		self.SearchHistoryTable = table


	def __MakeSearchPatternsTable(self):
		board = self.pageBoards["my_patterns"]

		table = TableWindowWithScrollbar(590, 500-15, 1, 20, TableWindowWithScrollbar.SCROLLBAR_VERTICAL)
		table.SetParent(board)
		table.SetPosition(10, 19)

		table.Show()
		self.SearchPatternsTable = table


	def __MakeShopSafeboxItemsTable(self):
		board = self.pageBoards["shop_safebox"]

		table = TableWindowWithScrollbar(582, 443, 11, 4, TableWindowWithScrollbar.SCROLLBAR_HORIZONTAL)
		table.SetParent(board)
		table.SetPosition(18, 50)
		table.SetDefaultCreateChild(MakeDefaultEmptySlot)

		table.Show()
		self.ShopSafeboxItemsTable = table


	def __MakeMyOffersTable(self):
		board = self.pageBoards["my_offers"]

		table = TableWindowWithScrollbar(570, 445, 2, 3, TableWindowWithScrollbar.SCROLLBAR_VERTICAL)
		table.SetParent(board)
		table.SetPosition(30, 25)

		table.Show()
		self.MyOffersTable = table


	def __MakeCreateAuctionSlot(self):
		if self.CreateAuctionSlot:
			del self.CreateAuctionSlot

		slot = Slot()
		slot.Show()
		slot.SetParent(self.pageBoards['create_auction'])
		slot.SetPosition(400,141)
		# slot.SetInfo(info)

		self.CreateAuctionSlot = slot


	def __MakeMyAuctionSlot(self, info):
		if self.MyAuctionSlot:
			del self.MyAuctionSlot

		slot = Slot()
		slot.SetParent(self.pageBoards['my_auction'])
		slot.SetPosition(339+65,97-73)
		slot.SetInfo(info)
		slot.Show()

		self.MyAuctionSlot = slot


	def __MakeOpenAuctionSlot(self, info):
		if self.OpenAuctionSlot:
			del self.OpenAuctionSlot

		slot = Slot()
		slot.SetParent(self.pageBoards['open_auction'])
		slot.SetPosition(339+65,97-73)
		slot.SetInfo(info)
		slot.Show()

		slot.SetOnMouseLeftButtonUpEvent(self.__OnClickOpenAuctionMakeOffer)

		self.OpenAuctionSlot = slot

	def __OnClickCreateShopIncreaseDaysButton(self):
		days = int(self.CreateShopDaysCountText.GetText())
		
		if days == offlineshop.OFFLINESHOP_MAX_DAYS:
			self.CreateShopDaysCountText.SetText("0")
		
		else:
			self.CreateShopDaysCountText.SetText(str(days+1))

	def __OnClickCreateShopDecreaseDaysButton(self):
		days = int(self.CreateShopDaysCountText.GetText())
		
		if days == 0:
			self.CreateShopDaysCountText.SetText(str(offlineshop.OFFLINESHOP_MAX_DAYS))
		
		else:
			self.CreateShopDaysCountText.SetText(str(days-1))

	def __OnClickCreateShopIncreaseHoursButton(self):
		hours = int(self.CreateShopHoursCountText.GetText())
		
		if hours == offlineshop.OFFLINESHOP_MAX_HOURS:
			self.CreateShopHoursCountText.SetText("0")
		
		else:
			self.CreateShopHoursCountText.SetText(str(hours+1))
	
	def __OnClickCreateShopDecreaseHoursButton(self):
		hours = int(self.CreateShopHoursCountText.GetText())
		
		if hours == 0:
			self.CreateShopHoursCountText.SetText(str(offlineshop.OFFLINESHOP_MAX_HOURS))
		
		else:
			self.CreateShopHoursCountText.SetText(str(hours-1))

	def __OnClickCloseButton(self):
		offlineshop.SendForceCloseShop()
		self.Close()

	def __OnClickMyShopEditNameButton(self):
		self.MyShopEditNameDlg.inputValue.SetText("")
		self.MyShopEditNameDlg.Open()
	
	def __OnClickMyShopPage(self):
		offlineshop.SendCloseBoard()
		offlineshop.SendOpenShopOwner()
		self.EnableRefreshSymbol()

	def __OnClickShopListPage(self):
		offlineshop.SendCloseBoard()
		offlineshop.SendRequestShopList()
		self.EnableRefreshSymbol()

	def __OnClickShopSafeboxPage(self):
		offlineshop.SendCloseBoard()
		offlineshop.SendSafeboxOpen()
		self.EnableRefreshSymbol()

	def __OnClickMyOffersPage(self):
		offlineshop.SendCloseBoard()
		offlineshop.SendOfferListRequest()
		self.EnableRefreshSymbol()

	def __OnClickSearchFilterPage(self):
		offlineshop.SendCloseBoard()
		self.pageCategory = "search_filter"
		for page in self.pageBoards.values():
			page.Hide()
		
		self.pageBoards["search_filter"].Show()

	def __OnSelectSearchFilterSuggestionSelector(self, index):
		pass
		
	def __OnClickSearchFilterAttributeButton(self, index):
		pass

	def __OnClickSearchHistoryPage(self):
		offlineshop.SendCloseBoard()
		self.pageCategory = "search_history"

		for v in self.pageBoards.values():
			v.Hide()

		self.pageBoards["search_history"].Show()
		self.RefreshSearchHistoryPage()

	def __OnClickMyPatternsPage(self):
		offlineshop.SendCloseBoard()
		for v in self.pageBoards.values():
			v.Hide()

		self.pageBoards["my_patterns"].Show()
		self.pageCategory = "my_patterns"
		self.RefreshMyPatternsPage()

	def __OnClickSearchPatternElement(self, element):
		info = element.GetInfo()
		self.__SetSearchFilterPattern(info)

		offlineshop.UpdateLastUseFilterPattern(info["id"])
		
	def __OnClickMyAuctionPage(self):
		offlineshop.SendCloseBoard()
		offlineshop.SendAuctionOpenMy()
		self.EnableRefreshSymbol()

	def __OnClickAuctionListPage(self):
		offlineshop.SendCloseBoard()
		offlineshop.SendAuctionListRequest()
		self.EnableRefreshSymbol()
	
	def __OnClickCreateAuctionButton(self):
		if self.CreateAuctionWindowPos == -1:
			return

		if self.CreateAuctionSlotPos == -1:
			return

		daystext = self.CreateAuctionDaysInput.GetText()
		days = int(daystext) if daystext and daystext.isdigit() else 0

		if 0 == days or offlineshop.OFFLINESHOP_MAX_DAYS<days:
			self.__PopupMessage(localeInfo.OFFLINESHOP_CREATE_SHOP_INVALID_DURATION)
			return

		pricetext = self.CreateAuctionStartingPriceInput.GetText()
		price = long(pricetext) if pricetext and pricetext.isdigit() else 0

		if price <= 0:
			self.__PopupMessage(localeInfo.OFFLINESHOP_CREATE_AUCTION_INVALID_PRICE)
			return

		offlineshop.SendAuctionCreate(self.CreateAuctionWindowPos, self.CreateAuctionSlotPos, price, days*24*60)
		self.EnableRefreshSymbol()

	def __OnClickCreateAuctionDaysDecreaseButton(self):
		days = int(self.CreateAuctionDaysInput.GetText())
		if days ==0:
			self.CreateAuctionDaysInput.SetText(str(offlineshop.OFFLINESHOP_MAX_DAYS))
		else:
			self.CreateAuctionDaysInput.SetText(str(days-1))

	def __OnClickCreateAuctionDaysIncreaseButton(self):
		days = int(self.CreateAuctionDaysInput.GetText())
		if days == offlineshop.OFFLINESHOP_MAX_DAYS:
			self.CreateAuctionDaysInput.SetText("0")
		else:
			self.CreateAuctionDaysInput.SetText(str(days + 1))

	def __OnClickSearchFilterResetFilterButton(self):
		for k, v in self.SearchFilterCheckBoxes.items():
			v.Disable()

		for v in self.SearchFilterCheckBoxesRace.values():
			v.Enable()

		self.SetCategory(0, SUBTYPE_NOSET)

		self.SearchFilterItemNameInput.SetText("")
		self.SearchFilterSuggestionObj.Clear()

		# self.SearchFilterResultItemsTable.ClearElement()
		self.SearchFilterResultItemsTable.ClearItems()
		#offlineshop-updated 04/08/19
		# self.__OnSelectSearchFilterTypeComboBox(0)
		# self.__OnSelectSearchFilterSubTypeComboBox(SUBTYPE_NOSET)

	def __OnClickSearchFilterSavePatternButton(self):
		bActiveOne = False

		for v in self.SearchFilterCheckBoxes.values():
			if v.IsEnabled():
				bActiveOne = True
				break

		if not bActiveOne:
			self.__PopupMessage(localeInfo.OFFLINESHOP_NO_FILTER_ACTIVE_MESSAGE)
			return

		if not self.SearchPatternsInputNameDlg.IsShow():
			self.SearchPatternsInputNameDlg.inputValue.SetText("")
			self.SearchPatternsInputNameDlg.Open()

	def OnClickSearchFilterStartSearch(self):
		self.__OnClickSearchFilterStartSearch()
		
	def __OnClickSearchFilterStartSearch(self):
		bActiveOne = False
		
		for v in self.SearchFilterCheckBoxes.values():
			if v.IsEnabled():
				bActiveOne = True
				break
		
		if not bActiveOne:
			self.__PopupMessage(localeInfo.OFFLINESHOP_NO_FILTER_ACTIVE_MESSAGE)
			return

		if self.SearchFilterCheckBoxes["name"].IsEnabled():
			if not self.SearchFilterItemNameInput.GetText():
				self.__PopupMessage(localeInfo.OFFLINESHOP_SEARCH_FILTER_NAME_NOSET)
				return

		self.SearchFilterLastUsedSetting = self.GetSearchFilterSettings()
		offlineshop.SendFilterRequest(*self.SearchFilterLastUsedSetting)
		self.EnableRefreshSymbol()

	def __OnClickFilterHistoryElement(self , element):
		info = element.GetInfo()
		self.__SetSearchFilterPattern(info)

	def __OnClickDeleteMyOfferButton(self, id):
		offer = None

		for element in self.MyOffersList:
			if element["offer_id"] == id:
				offer = element
				break

		if not offer:
			return

		accepttext = localeInfo.OFFLINESHOP_CANCEL_OFFER_QUESTION_ACCEPT
		canceltext = localeInfo.OFFLINESHOP_CANCEL_OFFER_QUESTION_CANCEL

		question   = localeInfo.OFFLINESHOP_CANCEL_OFFER_QUESTION

		self.MyOffersCancelOfferInfo = (offer['offer_id'], offer['owner_id'])
		self.__OpenQuestionDialog(len(question)*6 , accepttext, canceltext, self.__OnAcceptCancelOfferQuestion, self.__OnCancelCancelOfferQuestion, question)

	def __SetSearchFilterPattern(self, info):
		self.__OnClickSearchFilterPage()

		for k, v in self.SearchFilterCheckBoxes.items():
			v.Disable()

		raceFlags = {
			"warrior" :item.ITEM_ANTIFLAG_WARRIOR,
			"assassin" :item.ITEM_ANTIFLAG_ASSASSIN,
			"sura" :item.ITEM_ANTIFLAG_SURA,
			"shaman": item.ITEM_ANTIFLAG_SHAMAN,
		}

		flag = info["filter_wearflag"]

		for k, v in raceFlags.items():
			if flag & v != 0:
				self.SearchFilterCheckBoxesRace[k].Disable()
				if not self.SearchFilterCheckBoxes["wear"].IsEnabled():
					self.SearchFilterCheckBoxes["wear"].Enable()

			else:
				self.SearchFilterCheckBoxesRace[k].Enable()

		if info["filter_type"] == 0:
			self.SetCategory(0, SUBTYPE_NOSET)

		else:
			if not self.SearchFilterCheckBoxes["type"].IsEnabled():
				self.SearchFilterCheckBoxes["type"].Enable()

			typeCategory = self.ITEM_TYPES[info["filter_type"]]

			subtype = info["filter_subtype"]
			if subtype != SUBTYPE_NOSET and typeCategory.has_key('subtypes'):
				self.SetCategory(info["filter_type"], subtype)
			else:
				self.SetCategory(info["filter_type"], SUBTYPE_NOSET)

		if info["filter_name"]:
			self.SearchFilterCheckBoxes["name"].Enable()
			self.SearchFilterItemNameInput.SetText(info["filter_name"])

	def __PopupMessage(self, message):
		self.popupMessage.SetText(message)
		self.popupMessage.Open()

	def __OpenQuestionDialog(self , width, accepttext, canceltext, acceptevent, cancelevent, text):
		self.CommonQuestionDlg.SetAcceptText(accepttext)
		self.CommonQuestionDlg.SetCancelText(canceltext)
		self.CommonQuestionDlg.SAFE_SetAcceptEvent(acceptevent)
		self.CommonQuestionDlg.SAFE_SetCancelEvent(cancelevent)
		self.CommonQuestionDlg.SetText(text)
		self.CommonQuestionDlg.SetWidth(width)

		self.CommonQuestionDlg.Open()

	def __OnPickValute(self, title, acceptEvent, maxValue, max=13):
		self.CommonPickValuteDlg.SetMax(max)
		self.CommonPickValuteDlg.SetTitleName(title)
		self.CommonPickValuteDlg.SetAcceptEvent(acceptEvent)
		self.CommonPickValuteDlg.Open(maxValue)

	def OnShowPage(self):
		showEvents = {
			"my_shop"		: self.__OnClickMyShopPage,
		}
		
		if self.pageCategory in showEvents:
			showEvents[self.pageCategory]()

	def BINARY_EnableRefreshSymbol(self):
		if self.IsShow():
			self.EnableRefreshSymbol()

	def EnableRefreshSymbol(self):
		self.RefreshSymbol.Show()
	
	
	def DisableRefreshSymbol(self):
		self.RefreshSymbol.Hide()

	def ShopListClear(self):
		self.ShopList = []

	def ShopListAddItem( self, owner_id, duration , count , name):
		newelement = {}
		newelement["owner_id"]		= owner_id
		newelement["duration"]		= duration
		newelement["count"]			= count
		newelement["name"]			= name
		
		self.ShopList.append(newelement)

	def ShopListShow(self):
		self.RefreshShopListPage()
		self.DisableRefreshSymbol()

	def OpenShop( self, owner_id, duration, count, name):
		self.ShopItemSold 		= []
		self.ShopItemForSale 	= []
		
		self.ShopOpenInfo["owner_id"]	= owner_id
		self.ShopOpenInfo["duration"]	= duration
		self.ShopOpenInfo["count"]		= count
		self.ShopOpenInfo["name"]		= name
		self.ShopOpenInfo["my_shop"]	= False

	def OpenShopItem_Alloc(self):
		self.ShopItemForSale.append({})

	def OpenShopItem_SetValue( self, key,	index,	*args):
		if key == "id":
			self.ShopItemForSale[index][key] = args[0]

		elif key == "vnum":
			self.ShopItemForSale[index][key] = args[0]

		elif key == 'locked_attr':
			self.ShopItemForSale[index][key] = args[0]

		elif key == 'element':
			self.ShopItemForSale[index][key] = args[0]

		elif key == "count":
			self.ShopItemForSale[index][key] = args[0]
			
		elif key == "attr":
			if not key in self.ShopItemForSale[index]:
				self.ShopItemForSale[index][key] = {}
			
			attr_index = args[0]
			attr_type  = args[1]
			attr_value = args[2]
			
			self.ShopItemForSale[index][key][attr_index] = {}
			self.ShopItemForSale[index][key][attr_index]["type"]  = attr_type
			self.ShopItemForSale[index][key][attr_index]["value"] = attr_value
		
		elif key == "socket":
			if not key in self.ShopItemForSale[index]:
				self.ShopItemForSale[index][key] = {}
			
			socket_index = args[0]
			socket_val	 = args[1]
			
			self.ShopItemForSale[index][key][socket_index] = socket_val
		
		elif key == "price":
			self.ShopItemForSale[index][key] = args[0]

	def OpenShop_End(self):
		self.RefreshOpenShopPage()
		self.DisableRefreshSymbol()

		if not self.IsShow():
			self.Show()

	def OpenShopOwner_Start( self, owner_id, duration , count , name):
		self.ShopItemSold 		= []
		self.ShopItemForSale 	= []
		self.MyShopOffers		= []

		self.ShopOpenInfo["owner_id"]	= owner_id
		self.ShopOpenInfo["duration"]	= duration
		self.ShopOpenInfo["count"]		= count
		self.ShopOpenInfo["name"]		= name
		self.ShopOpenInfo["my_shop"]	= True
	
	def OpenShopOwner_End(self):
		self.DisableRefreshSymbol()
		self.RefreshMyShopPage()

		if not self.IsShow():
			self.Show()

	def OpenShopOwnerItem_Alloc(self):
		self.ShopItemForSale.append({})
	
	def OpenShopOwnerItem_SetValue( self, key, index, *args):
		if key == "id":
			self.ShopItemForSale[index][key] = args[0]

		elif key == "vnum":
			self.ShopItemForSale[index][key] = args[0]
			
		elif key == 'locked_attr':
			self.ShopItemForSale[index][key] = args[0]
			
		elif key == 'element':
			self.ShopItemForSale[index][key] = args[0]

		elif key == "count":
			self.ShopItemForSale[index][key] = args[0]
			
		elif key == "attr":
			if not key in self.ShopItemForSale[index]:
				self.ShopItemForSale[index][key] = {}
			
			attr_index = args[0]
			attr_type  = args[1]
			attr_value = args[2]
			
			self.ShopItemForSale[index][key][attr_index] = {}
			self.ShopItemForSale[index][key][attr_index]["type"]  = attr_type
			self.ShopItemForSale[index][key][attr_index]["value"] = attr_value
		
		elif key == "socket":
			if not key in self.ShopItemForSale[index]:
				self.ShopItemForSale[index][key] = {}
			
			socket_index = args[0]
			socket_val	 = args[1]
			
			self.ShopItemForSale[index][key][socket_index] = socket_val
		
		elif key == "price":
			self.ShopItemForSale[index][key] = args[0]

	def OpenShopOwner_SetOffer(self, itemid , buyerid, offerid, price, is_accept, buyer_name ):
		newoffer = {}
		newoffer["id"] 			= offerid
		newoffer["item_id"]		= itemid
		newoffer["buyer_id"]	= buyerid
		newoffer["price"]		= price
		newoffer["is_accept"]	= is_accept
		newoffer['buyer_name']  = buyer_name

		self.MyShopOffers.append(newoffer)

	def OpenShopOwnerItemSold_Alloc( self ):
		self.ShopItemSold.append({})
	
	def OpenShopOwnerItemSold_SetValue( self,  key , index , *args):
		if key == "id":
			self.ShopItemSold[index][key] = args[0]

		elif key == "vnum":
			self.ShopItemSold[index][key] = args[0]

		elif key == 'locked_attr':
			self.ShopItemSold[index][key] = args[0]

		elif key == 'element':
			self.ShopItemSold[index][key] = args[0]

		elif key == "count":
			self.ShopItemSold[index][key] = args[0]
			
		elif key == "attr":
			if not key in self.ShopItemSold[index]:
				self.ShopItemSold[index][key] = {}
			
			attr_index = args[0]
			attr_type  = args[1]
			attr_value = args[2]
			
			self.ShopItemSold[index][key][attr_index] = {}
			self.ShopItemSold[index][key][attr_index]["type"]  = attr_type
			self.ShopItemSold[index][key][attr_index]["value"] = attr_value
		
		elif key == "socket":
			if not key in self.ShopItemSold[index]:
				self.ShopItemSold[index][key] = {}
			
			socket_index = args[0]
			socket_val	 = args[1]
			
			self.ShopItemSold[index][key][socket_index] = socket_val
		
		elif key == "price":
			self.ShopItemSold[index][key] = args[0]
	
	def OpenShopOwnerItemSold_Show( self):
		pass

	def OpenShopOwnerNoShop(self):
		for v in self.pageBoards.values():
			v.Hide()
		
		self.pageBoards["create_shop"].Show()
		self.pageCategory = "create_shop"

		self.DisableRefreshSymbol()
		self.__ResetCreateShopPage()

	def ClearItemNames(self):
		self.SearchFilterItemsNameDict = {}

	def AppendItemName(self, vnum, name):
		self.SearchFilterItemsNameDict[name] = vnum

	def ShopClose( self):
		pass

	def ShopFilterResult( self , size):
		self.SearchFilterShopItemResult = []
	
	def ShopFilterResultItem_Alloc(self):
		self.SearchFilterShopItemResult.append({})

	def ShopFilterResultItem_SetValue( self,  key, index, *args):
		if key in ( "id", "vnum", "count", "price", "owner", "owner_name"):
			self.SearchFilterShopItemResult[index][key] = args[0]
			
		elif key == "attr":
			if not key in self.SearchFilterShopItemResult[index]:
				self.SearchFilterShopItemResult[index][key] = {}
			
			attr_index = args[0]
			attr_type  = args[1]
			attr_value = args[2]
			
			self.SearchFilterShopItemResult[index][key][attr_index] = {}
			self.SearchFilterShopItemResult[index][key][attr_index]["type"]  = attr_type
			self.SearchFilterShopItemResult[index][key][attr_index]["value"] = attr_value
		
		elif key == "socket":
			if not key in self.SearchFilterShopItemResult[index]:
				self.SearchFilterShopItemResult[index][key] = {}
			
			socket_index = args[0]
			socket_val	 = args[1]
			
			self.SearchFilterShopItemResult[index][key][socket_index] = socket_val

	def ShopFilterResult_Show(self):
		self.SearchFilterResultItemsTable.ClearItems()

		for info in self.SearchFilterShopItemResult:
			slot = ShopSearchItem()
			slot.SetInfo(info)
			slot.SetIndex((info["id"], info["owner"]))
			slot.SetOnMouseLeftButtonUpEvent(self.__OnLeftClickSearchFilterShopResultItem)
			slot.Show()
			self.SearchFilterResultItemsTable.AppendItem(slot)

		if len(self.SearchFilterShopItemResult) == SEARCH_RESULT_LIMIT:
			self.__PopupMessage(localeInfo.OFFLINESHOP_SEARCH_RISE_LIMIT%SEARCH_RESULT_LIMIT)

		setting = self.GetSearchFilterSettings()
		setting = (len(self.SearchFilterShopItemResult),) + setting

		offlineshop.AppendNewFilterHistory(*setting)
		self.DisableRefreshSymbol()
	
	def OfferReceived( self, offer_id , notified, accepted, owner_id, offerer_id, item_id, yang):
		pass
	
	def OfferAccept( self, offer_id , notified, accepted, owner_id, offerer_id, item_id, yang):
		pass

	def ClearFilterHistory(self):
		self.FilterHistory = []
	
	def AllocFilterHistory( self):
		self.FilterHistory.append({'id' : len(self.FilterHistory)})
	
	def SetFilterHistoryValue( self, key, *args):
		elm = self.FilterHistory[-1]
		
		if key == "datetime":
			elm["minute"]	= args[0]
			elm["hour"]		= args[1]
			elm["day"]		= args[2]
			elm["month"]	= args[3]
			elm["year"]		= args[4]
		
		elif key in ('count' , 'filter_type' , 'filter_subtype', 'filter_name' ,'filter_wearflag'):
			elm[key]		= args[0]
		
		
		elif key in ('filter_price_yang_start', 'filter_price_yang_end'):
			if not 'price' in elm:
				elm['price'] = {}
			
			elm['price'][key.replace('filter_price_yang_', '')] = args[0]
		
		
		elif key in ('filter_level_start', 'filter_level_end'):
			if not 'level' in elm:
				elm['level'] = {}
			
			elm['level'][key.replace('filter_level_', '')] = args[0]
		
		
		elif key in ('filter_attr_type' , 'filter_attr_value'):
			if not 'attr' in elm:
				elm['attr'] = {}
				elm['attr']['type']  = [0 for x in xrange(offlineshop.FILTER_ATTRIBUTE_NUM)]
				elm['attr']['value'] = [0 for x in xrange(offlineshop.FILTER_ATTRIBUTE_NUM)]
			
			elm['attr'][key.replace('filter_attr_', '')][args[0]] = args[1]

	def ClearFilterPatterns( self):
		self.FilterPatterns = {}
	
	def AllocFilterPattern( self , id):
		self.FilterPatterns[id] = {"id": id,}
	
	def SetFilterPatternValue( self, key, idx, *args):
		elm = self.FilterPatterns[idx]
		
		if key == "datetime":
			elm["minute"]	= args[0]
			elm["hour"]		= args[1]
			elm["day"]		= args[2]
			elm["month"]	= args[3]
			elm["year"]		= args[4]
		
		elif key in ('filter_type' , 'filter_subtype', 'filter_name' ,'filter_wearflag', 'name'):
			elm[key]		= args[0]
		
		
		elif key in ('filter_price_yang_start', 'filter_price_yang_end'):
			if not 'price' in elm:
				elm['price'] = {}
			
			elm['price'][key.replace('filter_price_yang_', '')] = args[0]
		
		
		elif key in ('filter_level_start', 'filter_level_end'):
			if not 'level' in elm:
				elm['level'] = {}
			
			elm['level'][key.replace('filter_level_', '')] = args[0]
		
		
		elif key in ('filter_attr_type' , 'filter_attr_value'):
			if not 'attr' in elm:
				elm['attr'] = {}
				elm['attr']['type']  = [0 for x in xrange(offlineshop.FILTER_ATTRIBUTE_NUM)]
				elm['attr']['value'] = [0 for x in xrange(offlineshop.FILTER_ATTRIBUTE_NUM)]
			
			elm['attr'][key.replace('filter_attr_', '')][args[0]] = args[1]

	def GetSearchFilterSettings(self):
		name		= ""
		raceflag	= 0
		type		= 0
		subtype		= SUBTYPE_NOSET
		levelmin	= 0
		levelmax	= 0
		
		yangmin		= 0
		yangmax		= 0
		
		attributes	= tuple([(0,0) for x in xrange(player.ATTRIBUTE_SLOT_NORM_NUM)])

		if self.SearchFilterCheckBoxes["name"].IsEnabled():
			name = self.SearchFilterItemNameInput.GetText()
		
		if self.SearchFilterCheckBoxes["type"].IsEnabled():
			type	= self.SearchFilterTypeComboBoxIndex
			subtype = self.SearchFilterSubTypeComboBoxIndex

		if self.SearchFilterCheckBoxes["wear"].IsEnabled():
			raceFlagDct = {
				"warrior"	: item.ITEM_ANTIFLAG_WARRIOR,
				"assassin"	: item.ITEM_ANTIFLAG_ASSASSIN,
				"sura" 		: item.ITEM_ANTIFLAG_SURA,
				"shaman" 	: item.ITEM_ANTIFLAG_SHAMAN,
			}

			for k,v in raceFlagDct.items():
				if not self.SearchFilterCheckBoxesRace[k].IsEnabled():
					raceflag |= v


		return (type, subtype, name, (yangmin,yangmax), (levelmin, levelmax), raceflag, attributes)

	def __IsSaleableSlot(self, win , pos):
		if win == player.INVENTORY:
			if player.IsEquipmentSlot(pos):
				return False

		if self.pageCategory in ("create_shop", "my_shop" ) and self.IsForSaleSlot(win, pos):
			return False

		if self.pageCategory == "create_auction" and self.IsForAuctionSlot(win,pos):
			return False

		
		try:
			if app.ENABLE_EXTRA_INVENTORY:
				if not win in (player.INVENTORY, player.DRAGON_SOUL_INVENTORY, player.EXTRA_INVENTORY):
					return False
			else:
				if not win in (player.INVENTORY, player.DRAGON_SOUL_INVENTORY):
					return False
		
		except:
			if not win in (player.INVENTORY, player.DRAGON_SOUL_INVENTORY):
				return False
		
		try:
			if ENABLE_SOULBIND_SYSTEM:
				itemSealDate = player.GetItemSealDate(win, pos)
				if itemSealDate != item.E_SEAL_DATE_DEFAULT_TIMESTAMP:
					return False
		except:
			pass

		itemIndex = player.GetItemIndex(win,pos)
		if itemIndex == 0:
			return False

		item.SelectItem(itemIndex)
		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MYSHOP) or item.IsAntiFlag(item.ITEM_ANTIFLAG_GIVE):
			return False

		return True

	def ShopBuilding_AddInventoryItem(self, slot):
		if player.GetItemIndex(player.INVENTORY, slot) ==0:
			return

		if player.IsEquipmentSlot(slot):
			return

		if self.IsForSaleSlot(player.INVENTORY,slot):
			return
		
		if self.__IsSaleableSlot(player.INVENTORY, slot):
			self.OpenInsertPriceDialog(player.INVENTORY,slot)

	def ShopBuilding_AddItem(self, win, pos):
		if self.__IsSaleableSlot(win, pos):
			self.OpenInsertPriceDialog(win,pos)

	def AuctionBuilding_AddInventoryItem(self, slot):
		if player.GetItemIndex(player.INVENTORY, slot) ==0:
			return

		if player.IsEquipmentSlot(slot):
			return

		if self.IsForAuctionSlot(player.INVENTORY, slot):
			return

		self.__OnSetCreateAuctionSlot(player.INVENTORY, slot)

	def AuctionBuilding_AddItem(self, win, pos):
		if self.__IsSaleableSlot(win, pos):
			self.__OnSetCreateAuctionSlot(win, pos)

	def SearchFilter_BuyFromSearch(self, ownerid, itemid):
		if self.pageCategory != 'search_filter':
			return

		for item in self.SearchFilterShopItemResult:
			if item['id'] == itemid and item['owner'] == ownerid:
				self.SearchFilterShopItemResult.remove(item)
				break

		self.SearchFilterResultItemsTable.ClearItems()

		for info in self.SearchFilterShopItemResult:
			slot = ShopSearchItem()
			slot.SetInfo(info)
			slot.SetIndex((info["id"], info["owner"]))
			slot.SetOnMouseLeftButtonUpEvent(self.__OnLeftClickSearchFilterShopResultItem)
			slot.Show()

			self.SearchFilterResultItemsTable.AppendItem(slot)

	def ShopSafebox_Clear(self):
		self.ShopSafeboxItems = []
		self.ShopSafeboxItemsTable.ClearElement()

	def ShopSafebox_SetValutes(self, yang):
		self.ShopSafeboxValuteAmount = yang
		self.ShopSafeboxValuteText.SetText(localeInfo.NumberToMoneyString(yang))

	def ShopSafebox_AllocItem(self):
		self.ShopSafeboxItems.append({})

	def ShopSafebox_SetValue(self, key , *args):
		elm = self.ShopSafeboxItems[-1]

		if key in ("id", "vnum", "count"):
			elm[key] = args[0]
			
		elif key == "locked_attr":
			elm[key] = args[0]
			
		elif key == "element":
			elm[key] = args[0]

		elif key == "socket":
			if not key in elm:
				elm[key] = [0 for x in xrange(player.METIN_SOCKET_MAX_NUM)]
			elm[key][args[0]] = args[1]

		elif key in ("attr_type", "attr_value"):
			if not 'attr' in elm:
				elm['attr'] = {}

			if not args[0] in elm['attr']:
				elm['attr'][args[0]] = {}

			elm['attr'][args[0]][key.replace('attr_','')] = args[1]

	def ShopSafebox_RefreshEnd(self):
		for item in self.ShopSafeboxItems:
			slot = Slot()
			slot.SetIndex(item["id"])
			slot.SetInfo(item)
			slot.SetOnMouseLeftButtonUpEvent(self.__OnLeftClickShopSafeboxItem)
			slot.Show()

			self.ShopSafeboxItemsTable.AddElement(slot)

		if not self.pageBoards["shop_safebox"].IsShow():
			self.pageCategory = "shop_safebox"

			for page in self.pageBoards.values():
				page.Hide()

			self.pageBoards["shop_safebox"].Show()

		self.DisableRefreshSymbol()

	def OfferList_Clear(self):
		self.MyOffersList = []

	def OfferList_AddOffer(self , shopname, offer_id, buyer_id, owner_id, item_id, yang, is_notified, is_accept):
		self.MyOffersList.append({})
		elm = self.MyOffersList[-1]

		if '@' in shopname:
			shopname = shopname[shopname.find('@') + 1:]

		elm["shop_name"] 	= shopname
		elm["offer_id"]		= offer_id
		elm["buyer_id"]		= buyer_id
		elm["owner_id"]		= owner_id
		elm["item_id"]		= item_id
		elm["price"]		= yang
		elm["is_notified"]	= is_notified
		elm["is_accept"]	= is_accept

	def	OfferList_ItemSetValue(self, key , *args):
		offer = self.MyOffersList[-1]
		if not offer.has_key('item'):
			offer['item']={}

		elm = offer['item']

		if key in ("id", "vnum", "count", "owner", "price"):
			elm[key] = args[0]
			
		elif key == "locked_attr":
			elm[key] = args[0]
			
		elif key == "element":
			elm[key] = args[0]
			
		elif key == "socket":
			if not key in elm:
				elm[key] = [0 for x in xrange(player.METIN_SOCKET_MAX_NUM)]
			elm[key][args[0]] = args[1]

		elif key in ("attr_type", "attr_value"):
			if not 'attr' in elm:
				elm['attr'] = {}

			if not args[0] in elm['attr']:
				elm['attr'][args[0]] = {}

			elm['attr'][args[0]][key.replace('attr_','')] = args[1]

	def OfferList_End(self):
		self.RefreshMyOffersPage()
		self.DisableRefreshSymbol()

	def AuctionList_Clear(self):
		self.AuctionListInfo = []
		self.AuctionListTable.ClearElement()

	def AuctionList_Alloc(self):
		self.AuctionListInfo.append({"item":{},})

	def AuctionList_SetInto(self, ownerid, owner_name, duration, init_yang, best_yang, offer_count):
		elm = self.AuctionListInfo[-1]

		info = {
			"owner_id" 		: ownerid,
			"owner_name"	: owner_name,
			"duration"		: duration,
			"init_yang"		: init_yang,
			"best_yang"		: best_yang,
			"offer_count"	: offer_count,
		}

		for k,v in info.items():
			elm[k] = v

	def AuctionList_SetItemInfo(self, vnum, count, *args):
		elm = self.AuctionListInfo[-1]['item']
		elm['count'] 	= count
		elm['vnum']		= vnum

		try:
			if ENABLE_CHANGELOOK_SYSTEM and len(args) !=0 :
				elm['trans'] = args[0]
		except:
			pass

	def AuctionList_SetItemSocket(self, index, value):
		elm = self.AuctionListInfo[-1]['item']
		if not 'socket' in elm:
			elm['socket'] = [0 for x in xrange(player.METIN_SOCKET_MAX_NUM)]

		elm['socket'][index] = value

	def AuctionList_SetItemAttribute(self, key, index, value):
		elm = self.AuctionListInfo[-1]['item']
		if not 'attr' in elm:
			elm['attr'] = [{'type' :0, 'value': 0,} for x in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
		elm['attr'][index][key] = value

	def AuctionList_End(self):
		self.RefreshAuctionListPage()
		self.DisableRefreshSymbol()

	def MyAuction_Clear(self):
		self.MyAuctionInfo = {'item':{},}

	def MyAuction_SetInto(self, owner_id, owner_name, duration, init_yang):
		info = {
			"owner_id" 		: owner_id,
			"owner_name"	: owner_name,
			"duration"		: duration,
			"init_yang"		: init_yang,
		}

		for k ,v in info.items():
			self.MyAuctionInfo[k] = v

	def MyAuction_SetItemInfo(self, vnum, count, *args):
		elm = self.MyAuctionInfo['item']
		elm['vnum']  = vnum
		elm['count'] = count
		try:
			if ENABLE_CHANGELOOK_SYSTEM and len(args)>0:
				elm['trans'] = args[0]
		except:
			pass

	def MyAuction_SetItemSocket(self, index , value):
		elm = self.MyAuctionInfo['item']
		if not 'socket' in elm:
			elm['socket'] = [0 for x in xrange(player.METIN_SOCKET_MAX_NUM)]

		elm['socket'][index] = value

	def MyAuction_SetItemAttribute(self, key , index , value):
		elm = self.MyAuctionInfo['item']
		if not 'attr' in elm:
			elm['attr'] = [{'type' :0, 'value': 0,} for x in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
		elm['attr'][index][key] = value


	def MyAuction_AddOffer(self, buyer_id, buyer_name, owner_id, price_yang):
		if not 'offers' in self.MyAuctionInfo:
			self.MyAuctionInfo['offers'] = []

		new = {}
		new['buyer_name'] = buyer_name
		new['price_yang'] = price_yang

		self.MyAuctionInfo['offers'].append(new)

	def MyAuction_End(self):
		self.RefreshMyAuctionPage()
		self.DisableRefreshSymbol()

	def OpenAuction_Clear(self):
		self.OpenAuctionInfo = {'item':{},}

	def OpenAuction_SetInto(self, owner_id, owner_name, duration, init_yang):
		info = {
			"owner_id" 		: owner_id,
			"owner_name"	: owner_name,
			"duration"		: duration,
			"init_yang"		: init_yang,
		}

		for k ,v in info.items():
			self.OpenAuctionInfo[k] = v

	def OpenAuction_SetItemInfo(self, vnum, count, *args):
		elm = self.OpenAuctionInfo['item']
		elm['vnum']  = vnum
		elm['count'] = count
		try:
			if ENABLE_CHANGELOOK_SYSTEM and len(args!=0):
				elm['trans'] = args[0]
		except:
			pass
			
	def OpenAuction_SetItemSocket(self, index , value):
		elm = self.OpenAuctionInfo['item']
		if not 'socket' in elm:
			elm['socket'] = [0 for x in xrange(player.METIN_SOCKET_MAX_NUM)]

		elm['socket'][index] = value

	def OpenAuction_SetItemAttribute(self, key , index , value):
		elm = self.OpenAuctionInfo['item']
		if not 'attr' in elm:
			elm['attr'] = [{'type' :0, 'value': 0,} for x in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
		elm['attr'][index][key] = value

	def OpenAuction_AddOffer(self, buyer_id, buyer_name, owner_id, price_yang):
		if not 'offers' in self.OpenAuctionInfo:
			self.OpenAuctionInfo['offers'] = []

		new = {}
		new['buyer_name'] = buyer_name
		new['price_yang'] = price_yang

		self.OpenAuctionInfo['offers'].append(new)

	def OpenAuction_End(self):
		self.RefreshOpenAuctionPage()
		self.DisableRefreshSymbol()

	def MyAuction_NoAuction(self):
		self.pageCategory = "create_auction"
		for page in self.pageBoards.values():
			page.Hide()

		self.pageBoards['create_auction'].Show()
		self.DisableRefreshSymbol()

	def OpenInsertPriceDialog(self, win, slot):
		self.AddItemSlotIndex = (win,slot)
		self.CommonInputPriceDlg.Open()

		vnum  = player.GetItemIndex(win, slot)
		count = player.GetItemCount(win, slot)
		price = self.LoadInputPrice(vnum, count)
		if price > 0:
			self.CommonInputPriceDlg.SetValue(price)

	def __OnAcceptMyShopAcceptOffer(self):
		offlineshop.SendOfferAccept(self.MyShopAcceptOfferID)
		self.CommonQuestionDlg.Hide()
		self.MyShopAcceptOfferID = -1

	def __OnCancelMyShopAcceptOffer(self):
		self.CommonQuestionDlg.Hide()
		self.MyShopAcceptOfferID = -1

	def __OnAcceptMyShopCancelOffer(self):
		offlineshop.SendOfferCancel(self.MyShopCancelOfferID, self.ShopOpenInfo['owner_id'])
		self.CommonQuestionDlg.Hide()
		self.MyShopCancelOfferID = -1

	def __OnCancelMyShopCancelOffer(self):
		self.CommonQuestionDlg.Hide()
		self.MyShopCancelOfferID = -1

	def __OnCancelCancelOfferQuestion(self):
		self.CommonQuestionDlg.Hide()
		self.MyOffersCancelOfferInfo = []

	def __OnAcceptCancelOfferQuestion(self):
		info = self.MyOffersCancelOfferInfo
		offlineshop.SendOfferCancel(info[0], info[1])

		self.CommonQuestionDlg.Hide()
		self.MyOffersCancelOfferInfo = []

	def SaveInputPrice(self, vnum, count, price):
		import os
		path = "lib/encodings/offlineshop/price"

		if not os.path.exists(path):
			os.makedirs(path)

		n = path + "/" + str(vnum) + "_" + str(count) + ".txt"
		f = file(n, "w+")
		f.write(str(price))
		f.close()

	def LoadInputPrice(self, vnum, count):
		import os
		path = "lib/encodings/offlineshop/price"

		if not os.path.exists(path):
			os.makedirs(path)

		oldPrice = 0

		n = path + "/" + str(vnum) + "_" + str(count) + ".txt"

		if os.path.exists(n):
			fd = open( n,'r')
			oldPrice = int(fd.readlines()[0])

		return oldPrice

	def __OnAcceptInputPrice(self):
		yang = self.CommonInputPriceDlg.GetText()
		yang = constInfo.ConvertMoneyText(yang)
		# if not yang.isdigit():
			# return

		yang = int(yang)

		if yang == 0:
			return

		if self.pageCategory == "create_shop" and self.AddItemSlotIndex != -1:
			slot = Slot()
			slot.SetIndex(self.AddItemSlotIndex)
			slot.SetInfo(MakeSlotInfo(self.AddItemSlotIndex[0] , self.AddItemSlotIndex[1], yang))
			slot.SetOnMouseLeftButtonUpEvent(self.__OnLeftClickInsertedItem)
			slot.Show()

			self.CreateShopItemsTable.AddElement(slot)
			self.CreateShopItemsInfos[slot.GetIndex()] = slot.GetInfo()

			vnum  = player.GetItemIndex(self.AddItemSlotIndex[0], self.AddItemSlotIndex[1])
			count = player.GetItemCount(self.AddItemSlotIndex[0], self.AddItemSlotIndex[1])
			self.SaveInputPrice(vnum, count, yang)

			self.CommonInputPriceDlg.Hide()
			
			self.AddItemSlotIndex = -1

		elif self.pageCategory == "create_shop" and self.EditPriceSlot != None:
			slot  = self.EditPriceSlot
			index = slot.GetIndex()
			
			info 			= slot.GetInfo()
			info["price"] 	= yang
			self.CreateShopItemsInfos[slot.GetIndex()] = info
			self.EditPriceSlot = None
			self.CommonInputPriceDlg.Hide()

		elif self.pageCategory == "my_shop" and self.AddItemSlotIndex != -1:
			offlineshop.SendAddItem(self.AddItemSlotIndex[0],  self.AddItemSlotIndex[1],  yang)

			vnum  = player.GetItemIndex(self.AddItemSlotIndex[0], self.AddItemSlotIndex[1])
			count = player.GetItemCount(self.AddItemSlotIndex[0], self.AddItemSlotIndex[1])
			self.SaveInputPrice(vnum, count, yang)

			self.AddItemSlotIndex = -1
			self.CommonInputPriceDlg.Hide()
		
		elif self.pageCategory == "my_shop" and self.EditPriceSlot != None:
			slot  = self.EditPriceSlot
			index = slot.GetIndex()
			offlineshop.SendEditItem(index, yang)

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()

			vnum  = player.GetItemIndex(attachedSlotType, attachedSlotPos)
			count = player.GetItemCount(attachedSlotType, attachedSlotPos)
			self.SaveInputPrice(vnum, count, yang)

			self.CommonInputPriceDlg.Hide()
			self.EditPriceSlot = None
	
	def __OnCancelInputPrice(self):
		self.CommonInputPriceDlg.Hide()
		self.AddItemSlotIndex 	= -1
		self.EditPriceSlot		= None

	def __OnAcceptOpenShopBuyItemQuestion(self):
		self.CommonQuestionDlg.Hide()
		offlineshop.SendBuyItem(self.ShopOpenInfo["owner_id"] , self.OpenShopBuyItemID)
		self.OpenShopBuyItemID = -1

	def __OnCancelOpenShopBuyItemQuestion(self):
		self.CommonQuestionDlg.Hide()
		self.OpenShopBuyItemID = -1

	def __OnAcceptSearchFilterBuyItemQuestion(self):
		id,owner = self.SearchFilterResultClickedInfo
		offlineshop.SendBuyItemFromSearch(owner, id)

		self.CommonQuestionDlg.Hide()
		self.SearchFilterResultClickedInfo = []

	def __OnCancelSearchFilterBuyItemQuestion(self):
		self.CommonQuestionDlg.Hide()
		self.SearchFilterResultClickedInfo = []

	def __OnAcceptChangeShopNameDlg(self):
		newname = self.MyShopEditNameDlg.GetText()
		self.MyShopEditNameDlg.Hide()
		
		offlineshop.SendChangeName(newname)
	
	def __OnCancelChangeShopNameDlg(self):
		self.MyShopEditNameDlg.Hide()

	def __OnAcceptMyPatternInputName(self):
		name = self.SearchPatternsInputNameDlg.GetText()
		self.SearchPatternsInputNameDlg.Hide()
		if name:
			setting = self.GetSearchFilterSettings()
			setting = (name,) + setting
			offlineshop.AppendNewFilterPattern(*setting)
			self.__PopupMessage(localeInfo.OFFLINESHOP_PATTERN_SAVED_SUCCESS)

	def __OnCancelMyPatternInputName(self):
		self.SearchPatternsInputNameDlg.Hide()

	def __OnAcceptShopSafeboxGetItemQuestion(self):
		self.CommonQuestionDlg.Hide()
		offlineshop.SendSafeboxGetItem(self.ShopSafeboxGetItemIndex)
		self.ShopSafeboxGetItemIndex = -1

	def __OnCancelShopSafeboxGetItemQuestion(self):
		self.CommonQuestionDlg.Hide()
		self.ShopSafeboxGetItemIndex = -1

	def __OnAcceptShopSafeboxGetValuteInput(self , yang):
		offlineshop.SendSafeboxGetValutes(yang)

	def __OnAcceptMakeOffer(self, yang):
		offlineshop.SendOfferCreate(self.MakeOfferOwnerID, self.MakeOfferItemID, yang)
		self.MakeOfferOwnerID 	= -1
		self.MakeOfferItemID	= -1

	def __OnClickCreateShopButton(self):
		shopname = self.CreateShopNameEdit.GetText()
		if not shopname:
			self.__PopupMessage(localeInfo.OFFLINESHOP_CREATE_SHOP_NO_NAME_INSERTED)
			return
		
		days  = int(self.CreateShopDaysCountText.GetText())
		hours = int(self.CreateShopHoursCountText.GetText())
		
		totaltime = days * 24 * 60
		totaltime += hours * 60
		
		if totaltime > offlineshop.OFFLINESHOP_MAX_MINUTES or totaltime <= 0:
			self.__PopupMessage(localeInfo.OFFLINESHOP_CREATE_SHOP_INVALID_DURATION)
			return
		
		elements = self.CreateShopItemsTable.GetElementDict()
		if not elements:
			self.__PopupMessage(localeInfo.OFFLINESHOP_CREATE_SHOP_NO_ITEMS_INSERTED)
			return
		
		itemLst = []
		
		for dct in elements.values():
			for item in dct.values():
				info = item.GetInfo()
				

				tupleinfo = (info["window"], info["slot"] , info["price"] )
				itemLst.append(tupleinfo)
		itemTuple = tuple(itemLst)
		if app.KASMIR_PAKET_SYSTEM:
			offlineshop.SendShopCreate(shopname, totaltime, self.KasmirNpc, itemTuple)
		else:
			offlineshop.SendShopCreate(shopname, totaltime, itemTuple)
		
		self.EnableRefreshSymbol()

	if app.KASMIR_PAKET_SYSTEM:
		def OpeningFailded(self):
			self.DisableRefreshSymbol()
			if self.pageBoards["create_shop"].IsShow():
				self.KasmirNpc = 30000
				#renderTarget.SelectModel(2, self.KasmirNpc)

	def __OnLeftClickInsertedItem(self, slot):
		if mouseModule.mouseController.isAttached():
			if self.pageCategory == "create_shop":
				self.__OnClickCreateShopEmptySlot()
			elif self.pageCategory == "my_shop":
				self.__OnClickMyShopEmptySlot()
			return


		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			self.__OnRemoveShopItem(slot)
		
		else:
			self.EditPriceSlot = slot
			self.CommonInputPriceDlg.Open()

	def __OnLeftClickShopItem(self, slot):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			itemid  = slot.GetIndex()
			ownerid = self.ShopOpenInfo["owner_id"]

			self.__OnMakeShopItemOffer(itemid, ownerid)
		else:
			self.OpenShopBuyItemID = slot.GetIndex()
			info = slot.GetInfo()

			self.BuyPriceSeenTotal = info['price']
			item.SelectItem(info["vnum"])
			name 	= item.GetItemName()
			count	= info["count"]
			yang	= info["price"]

			if count > 1:
				text	= localeInfo.OFFLINESHOP_BUY_ITEM_QUESTION_COUNT % (name, count, yang)
			else:
				text	= localeInfo.OFFLINESHOP_BUY_ITEM_QUESTION % (name, yang)


			width		= 6 * len(text)
			accept_text	= localeInfo.OFFLINESHOP_BUY_ITEM_QUESTION_ACCEPT
			cancel_text	= localeInfo.OFFLINESHOP_BUY_ITEM_QUESTION_CANCEL
			accept_event= self.__OnAcceptOpenShopBuyItemQuestion
			cancel_event= self.__OnCancelOpenShopBuyItemQuestion

			self.__OpenQuestionDialog(width, accept_text, cancel_text, accept_event, cancel_event, text)

	def __OnLeftClickSearchFilterShopResultItem(self, slot):
		self.SearchFilterResultClickedInfo = slot.GetIndex()
		info = slot.GetInfo()

		self.BuyPriceSeenTotal = info['price']
		item.SelectItem(info["vnum"])
		name = item.GetItemName()
		count = info["count"]
		yang = info["price"]

		if count > 1:
			text = localeInfo.OFFLINESHOP_BUY_ITEM_QUESTION_COUNT % (name, count, yang)
		else:
			text = localeInfo.OFFLINESHOP_BUY_ITEM_QUESTION % (name, yang)

		width = 6 * len(text)
		accept_text = localeInfo.OFFLINESHOP_BUY_ITEM_QUESTION_ACCEPT
		cancel_text = localeInfo.OFFLINESHOP_BUY_ITEM_QUESTION_CANCEL
		accept_event = self.__OnAcceptSearchFilterBuyItemQuestion
		cancel_event = self.__OnCancelSearchFilterBuyItemQuestion

		self.__OpenQuestionDialog(width, accept_text, cancel_text, accept_event, cancel_event, text)

	def __OnClickCreateShopEmptySlot(self, *args):
		if not mouseModule.mouseController.isAttached():
			return

		type = mouseModule.mouseController.GetAttachedType()
		slot = mouseModule.mouseController.GetAttachedSlotNumber()

		#tofix slot type to window type
		type = player.SlotTypeToInvenType(type)

		mouseModule.mouseController.DeattachObject()
		self.ShopBuilding_AddItem(type,slot)

	def __OnClickMyShopEmptySlot(self, *args):
		# todebug
		print("my shop shop empty slot")

		if not mouseModule.mouseController.isAttached():
			return

		type = mouseModule.mouseController.GetAttachedType()
		slot = mouseModule.mouseController.GetAttachedSlotNumber()

		#tofix slot type to window type
		type = player.SlotTypeToInvenType(type)

		mouseModule.mouseController.DeattachObject()
		self.ShopBuilding_AddItem(type,slot)

	def __OnClickShopListOpenShop(self, id):
		offlineshop.SendOpenShop(id)

	def __OnClickOpenAuctionMakeOffer(self, slot):
		self.__OnPickValute(localeInfo.OFFLINESHOP_AUCTION_MAKE_OFFER, self.__OnClickAcceptOpenAuctionPickValute, player.GetMoney())

	def __OnClickAcceptOpenAuctionPickValute(self, yang):
		if not self.OpenAuctionInfo.has_key('min_raise'):
			return

		if yang < self.OpenAuctionInfo['min_raise']:
			self.__PopupMessage(localeInfo.OFFLINESHOP_AUCTION_MIN_RAISE%NumberToString(self.OpenAuctionInfo['min_raise']) )
			return

		offlineshop.SendAuctionAddOffer(self.OpenAuctionInfo['owner_id'] , yang)

	def __OnClickShopSafeboxWithdrawYang(self):
		maxval = self.ShopSafeboxValuteAmount
		self.__OnPickValute(localeInfo.OFFLINESHOP_SAFEBOX_GET_VALUTE_TITLE, self.__OnAcceptShopSafeboxGetValuteInput, maxval)

	def __OnClickMyShopOfferAcceptButton(self, offer):
		self.MyShopAcceptOfferID = offer.GetInfo()['id']

		question 	= localeInfo.OFFLINESHOP_ACCEPT_OFFER_QUESTION
		accepttext 	= localeInfo.OFFLINESHOP_ACCEPT_OFFER_QUESTION_ACCEPT
		canceltext 	= localeInfo.OFFLINESHOP_ACCEPT_OFFER_QUESTION_CANCEL

		self.__OpenQuestionDialog(len(question)*6 , accepttext, canceltext, self.__OnAcceptMyShopAcceptOffer, self.__OnCancelMyShopAcceptOffer, question)

	def __OnClickMyShopOfferCancelButton(self, offer):
		self.MyShopCancelOfferID = offer.GetInfo()['id']
		question 	= localeInfo.OFFLINESHOP_CANCEL_OFFER_QUESTION
		accepttext 	= localeInfo.OFFLINESHOP_CANCEL_OFFER_QUESTION_ACCEPT
		canceltext 	= localeInfo.OFFLINESHOP_CANCEL_OFFER_QUESTION_CANCEL

		self.__OpenQuestionDialog(len(question) * 6, accepttext, canceltext, self.__OnAcceptMyShopCancelOffer, self.__OnCancelMyShopCancelOffer, question)

	def __OnClickOpenAuctionButton(self, idx):
		offlineshop.SendAuctionOpenAuction(idx)
		self.EnableRefreshSymbol()

	def __OnLeftClickShopSafeboxItem(self, slot):
		id = slot.GetIndex()
		self.ShopSafeboxGetItemIndex = id
		self.__OnAcceptShopSafeboxGetItemQuestion()

	def __OnRemoveShopItem(self, slot):
		if self.pageCategory == "create_shop":
			self.__OnRemoveShopItemCreateShopPage(slot)

		elif self.pageCategory == "my_shop":
			self.__OnRemoveShopItemMyShop(slot)


	def __OnRemoveShopItemCreateShopPage(self, slot):
		slot.Hide()
		del self.CreateShopItemsInfos[slot.GetIndex()]
		self.CreateShopItemsTable.ClearElement()
		
		for k, v in self.CreateShopItemsInfos.items():
			newslot = Slot()
			newslot.SetIndex(k)
			newslot.SetInfo(v)
			newslot.SetOnMouseLeftButtonUpEvent(self.__OnLeftClickInsertedItem)
			newslot.Show()
			
			self.CreateShopItemsTable.AddElement(newslot)

	def __OnRemoveShopItemMyShop(self, slot):
		offlineshop.SendRemoveItem(slot.GetIndex())

	def __OnMakeShopItemOffer(self ,  itemid , ownerid):
		self.MakeOfferItemID = itemid
		self.MakeOfferOwnerID= ownerid

		title = localeInfo.OFFLINESHOP_MAKE_OFFER_TITLE

		self.__OnPickValute(title, self.__OnAcceptMakeOffer, player.GetMoney())

	def __OnSetCreateAuctionSlot(self, win,slot):
		vnum = player.GetItemIndex(win,slot)
		if vnum ==0:
			return

		item.SelectItem(vnum)
		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MYSHOP) or item.IsAntiFlag(item.ITEM_ANTIFLAG_GIVE):
			return

		self.CreateAuctionWindowPos = win
		self.CreateAuctionSlotPos	= slot

		count 	= player.GetItemCount(win,slot)
		attrs 	= [{"type" : player.GetItemAttribute(win, slot, x)[0], "value" : player.GetItemAttribute(win, slot, x)[1]} for x in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
		sockets = [player.GetItemMetinSocket(win,slot,x) for x in xrange(player.METIN_SOCKET_MAX_NUM)]
		
		try:
			if ENABLE_CHANGELOOK_SYSTEM:
				trans = player.GetItemTransmutation(win, slot)
		except:
			pass

		info = {
			"vnum" 		: vnum,
			"count" 	: count,
			'attr'		: attrs,
			'socket'	: sockets,
		}
		
		try:
			if ENABLE_CHANGELOOK_SYSTEM:
				info.update({
					'trans' : trans,
				})
		except:
			pass

		self.CreateAuctionSlot.SetInfo(info)
		self.CreateAuctionSlot.SetOnMouseLeftButtonUpEvent(self.OnClickAuctionSlot)

	def IsBuildingShop(self):
		return self.IsShow() and (self.pageCategory == "create_shop" or self.pageCategory=="my_shop")

	def IsForSaleSlot(self,win,slot):
		idx = (win,slot)

		if not self.pageCategory=="create_shop" or not self.IsShow():
			return False
		
		if not self.CreateShopItemsTable:
			return False
		
		elementDict = self.CreateShopItemsTable.GetElementDict()
		for dct in elementDict.values():
			for value in dct.values():
				if value.GetIndex() == idx:
					return True
		return False

	def IsBuildingAuction(self):
		if not self.IsShow():
			return False

		if self.pageCategory != "create_auction":
			return False
		return True

	def IsForAuctionSlot(self, win, slot):
		if not self.IsShow():
			return False

		if self.pageCategory != "create_auction":
			return False

		return self.CreateAuctionWindowPos == win and self.CreateAuctionSlotPos == slot

	def __SetTooltip(self,info):
		infocolor = COLOR_TEXT_SHORTCUT

		is_building = self.IsBuildingShop()
		
		self.itemTooltip.ClearToolTip()
		
		sockets = [info["socket"][num] for num in xrange(player.METIN_SOCKET_MAX_NUM)]
		attrs	= [(info["attr"][num]['type'], info["attr"][num]['value']) for num in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

		self.itemTooltip.AddItemData(info["vnum"], sockets, attrs, 0, 0, player.INVENTORY, -1, -1, 0, 0, False)

		if self.pageCategory in ("open_shop", "my_shop", "search_filter", "create_shop"):
			self.itemTooltip.AppendPrice(info["price"])

		if is_building and not info.get('sold', False):
			self.itemTooltip.AppendSpace(10)
			self.itemTooltip.AppendTextLine(localeInfo.OFFLINESHOP_BUILDING_LEFT_CLICK_EDIT_PRICE, infocolor)
			self.itemTooltip.AppendTextLine(localeInfo.OFFLINESHOP_BUILDING_LEFT_CLICK_CTRL_REMOVE_ITEM, infocolor)
		
		elif self.pageCategory == "open_shop":
			self.itemTooltip.AppendSpace(10)
			self.itemTooltip.AppendTextLine(localeInfo.OFFLINESHOP_OPEN_SHOP_LEFT_CLICK_BUY_ITEM, infocolor)
			self.itemTooltip.AppendTextLine(localeInfo.OFFLINESHOP_OPEN_SHOP_LEFT_CLICK_MAKE_OFFER, infocolor)

		elif self.pageCategory == "shop_safebox":
			self.itemTooltip.AppendSpace(10)
			self.itemTooltip.AppendTextLine(localeInfo.OFFLINESHOP_SAFEBOX_TOOLTIP_GETITEM, infocolor)

	def __SetTooltipMyOffer(self, offer):
		slot = offer.slot
		self.__SetTooltip(slot.GetInfo())
		index = offer.info['offer_id']

		for elm in self.MyOffersList:
			if elm['offer_id'] == index:
				self.itemTooltip.AppendSpace(10)
				self.itemTooltip.AppendPrice(elm['item']['price'])
				self.itemTooltip.AppendTextLine(localeInfo.OFFLINESHOP_MY_OFFER_OFFER_TEXT%localeInfo.NumberToMoneyString(elm['price']))
				break

	def __SetTooltipSearch(self, element):
		print("updating tooltip")

		appendLine = lambda arg : (
			uiTooltip.ToolTip.AutoAppendTextLine(self.itemTooltip, arg),
			self.itemTooltip.AlignHorizonalCenter())

		self.itemTooltip.ClearToolTip()

		info = element.info

		name 		= info.get('filter_name', "")
		wearflag	= info.get('filter_wearflag', 0)

		price_min	= info.get('price', {}).get('start', 0)
		price_max	= info.get('price', {}).get('end', 0)

		level_min	= info.get('level', {}).get('start',0)
		level_max	= info.get('level', {}).get('end',0)

		type		= info.get('filter_type', 0)
		subtype		= info.get('filter_subtype', 255)

		attrs		= info.get('attr')

		if name:
			appendLine(localeInfo.OFFLINESHOP_TOOLTIP_NAME_INFO +" "+ name)

		if type:
			type_phrase  = localeInfo.OFFLINESHOP_TOOLTIP_TYPE_INFO+  " "
			type_phrase += self.ITEM_TYPES[type]['name']

			if subtype != SUBTYPE_NOSET and self.ITEM_TYPES[type].has_key('subtypes'):
				type_phrase += ", "+self.ITEM_TYPES[type]['subtypes'][subtype]

			appendLine(type_phrase)

		if price_min or price_max:
			price_phrase = localeInfo.OFFLINESHOP_TOOLTIP_PRICE_INFO + " "
			if price_min and price_max:
				price_phrase += NumberToString(price_min) + "  -  "+ localeInfo.NumberToMoneyString(price_max)

			elif price_min:
				price_phrase += " > "+ localeInfo.NumberToMoneyString(price_min)
			elif price_max:
				price_phrase += " < "+ localeInfo.NumberToMoneyString(price_max)

			appendLine(price_phrase)

		if level_min or level_max:
			level_phrase = localeInfo.OFFLINESHOP_TOOLTIP_LEVEL_INFO + " "
			if level_min and level_max:
				level_phrase += "%d  -  %d"%(level_min, level_max)

			elif level_min:
				level_phrase += " >= %d"%level_min

			elif level_max:
				level_phrase += " <= %d"%level_max

			appendLine(level_phrase)

		raceFlagDct = {
			item.ITEM_ANTIFLAG_WARRIOR : localeInfo.OFFLINESHOP_WEAR_WARRIOR,
			item.ITEM_ANTIFLAG_ASSASSIN	: localeInfo.OFFLINESHOP_WEAR_ASSASSIN,
			item.ITEM_ANTIFLAG_SURA		: localeInfo.OFFLINESHOP_WEAR_SURA,
			item.ITEM_ANTIFLAG_SHAMAN	: localeInfo.OFFLINESHOP_WEAR_SHAMAN,
		}

		wearphrase = ""
		for k ,v in raceFlagDct.items():
			if not wearflag & k:
				if wearphrase:
					wearphrase += ", "
				wearphrase += v

		if wearphrase:
			wearphrase = localeInfo.OFFLINESHOP_TOOLTIP_WEAR_INFO + wearphrase
			appendLine(wearphrase)

		attribute_phrase = ""
		for type in attrs['type']:
			if type != 0:
				if attribute_phrase:
					attribute_phrase += ', '
				attribute_phrase += self.ATTRIBUTES[type]

		if attribute_phrase:
			attribute_phrase = localeInfo.OFFLINESHOP_TOOLTIP_ATTR_INFO +' '+attribute_phrase
			appendLine(attribute_phrase)

		self.itemTooltip.ShowToolTip()

	def __SetTooltipAuctionList(self, element):
		itemInfo = element.GetInfo()['item']
		self.__SetTooltip(itemInfo)

	def OnUpdate(self):
		self.MenuButton.OnUpdate()
		# try:
		if self.pageCategory in self.updateEvents:
			self.updateEvents[self.pageCategory]()
	
	def __OnUpdateMyShopPage(self):
		self.__RefreshingTooltip(self.MyShopItemsTable)

	def __OnUpdateCreateShopPage(self):
		self.__RefreshingTooltip(self.CreateShopItemsTable)

	def __OnUpdateOpenShopPage(self):
		self.__RefreshingTooltip(self.OpenShopItemsTable)
	
	def __OnUpdateSearchFilterPage(self):
		pass
		# self.__RefreshingTooltip(self.SearchFilterResultItemsTable)

	def __OnUpdateSearchHistoryPage(self):
		self.__RefreshingTooltip(self.SearchHistoryTable , self.__SetTooltipSearch)

	def __OnUpdateMyPatternPage(self):
		self.__RefreshingTooltip(self.SearchPatternsTable, self.__SetTooltipSearch)

	def __OnUpdateShopSafeboxPage(self):
		self.__RefreshingTooltip(self.ShopSafeboxItemsTable)

	def __OnUpdateMyOffersPage(self):
		self.__RefreshingTooltip(self.MyOffersTable, self.__SetTooltipMyOffer)

	def __OnUpdateCreateAuctionPage(self):
		if self.CreateAuctionSlot.IsShow():
			if self.itemTooltip.IsShow():
				if not self.CreateAuctionSlot.IsInSlot():
					self.itemTooltip.Hide()
			else:
				if self.CreateAuctionSlot.IsInSlot() and self.CreateAuctionSlot.GetInfo():
					self.__SetTooltip(self.CreateAuctionSlot.GetInfo())

	def __OnUpdateMyAuctionPage(self):
		if self.MyAuctionSlot.IsShow():
			if self.itemTooltip.IsShow():
				if not self.MyAuctionSlot.IsInSlot():
					self.itemTooltip.Hide()
			else:
				if self.MyAuctionSlot.IsInSlot() and self.MyAuctionSlot.GetInfo():
					self.__SetTooltip(self.MyAuctionSlot.GetInfo())


	def __OnUpdateOpenAuctionPage(self):
		if self.OpenAuctionSlot.IsShow():
			if self.itemTooltip.IsShow():
				if not self.OpenAuctionSlot.IsInSlot():
					self.itemTooltip.Hide()
			else:
				if self.OpenAuctionSlot.IsInSlot() and self.OpenAuctionSlot.GetInfo():
					self.__SetTooltip(self.OpenAuctionSlot.GetInfo())
					self.itemTooltip.AppendTextLine(localeInfo.OFFLINESHOP_TOOLTIP_LEFT_CLICK_MAKE_OFFER)


	def __OnUpdateAuctionListPage(self):
		self.__RefreshingTooltip(self.AuctionListTable, self.__SetTooltipAuctionList)

	def __RefreshingTooltip(self, table, event = None):
		if not self.itemTooltip.IsShow():
			elementDict = table.GetElementDict()
			for dct in elementDict.values():
				for value in dct.values():
					if value.IsInSlot():
						self.slotTooltipIndex = value.GetIndex()
						if event == None:
							self.__SetTooltip(value.GetInfo())
						else:
							event(value)

						return

			self.itemTooltip.Hide()
			self.slotTooltipIndex = -1

		else:
			elementDict = table.GetElementDict()
			for dct in elementDict.values():
				for value in dct.values():
					if value.IsInSlot():
						if self.slotTooltipIndex == value.GetIndex():
							return

						self.slotTooltipIndex = value.GetIndex()
						if event == None:
							self.__SetTooltip(value.GetInfo())
						else:
							event(value)

						return

			self.itemTooltip.Hide()
			self.slotTooltipIndex = -1

	def RefreshMyShopPage(self):
		self.pageCategory = "my_shop"
		for board in self.pageBoards.values():
			board.Hide()
		
		self.pageBoards["my_shop"].Show()
		name = self.ShopOpenInfo["name"]

		if '@' in name:
			name = name[name.find('@')+1:]

		self.MyShopShopTitle.SetText(name + "  " + localeInfo.OFFLINESHOP_ITEMS_COUNT_TEXT%self.ShopOpenInfo["count"])
		self.MyShopShopDuration.SetText(localeInfo.BATTLEPASS_TEXT_7 +  GetDurationStringRB(self.ShopOpenInfo["duration"])  + localeInfo.OFFLINE_SHOP_MAX_DAYS)
		self.MyShopGauge.SetPercentage(self.ShopOpenInfo["duration"],8*24*60)

		self.MyShopItemsTable.ClearElement()
		for item_info in self.ShopItemForSale:
			
			slot = Slot()
			slot.SetInfo(item_info)
			slot.SetIndex(item_info["id"])
			slot.SetOnMouseLeftButtonUpEvent(self.__OnLeftClickInsertedItem)
			slot.Show()
			
			self.MyShopItemsTable.AddElement(slot)

		for item_info in self.ShopItemSold:
			item_info["sold"] = True

			slot = Slot(isSold=True)
			slot.SetInfo(item_info)
			slot.SetIndex(item_info["id"])
			slot.Show()

			self.MyShopItemsTable.AddElement(slot)

		self.MyShopOffersTable.ClearElement()
		for info in self.MyShopOffers:
			itemname = ""
			for saleitem in self.ShopItemForSale:
				if saleitem["id"] == info["item_id"]:
					item.SelectItem(saleitem["vnum"])
					itemname = item.GetItemName()
					break

			if not itemname:
				continue

			offer = Offer(info)
			offer.Show()
			offer.SetItemName(itemname)
			if not info["is_accept"]:
				offer.SetAcceptButtonEvent(self.__OnClickMyShopOfferAcceptButton)
				offer.SetDeleteButtonEvent(self.__OnClickMyShopOfferCancelButton)

			self.MyShopOffersTable.AddElement(offer)
	
	def RefreshShopListPage(self):
		self.pageCategory = "shop_list"
		for board in self.pageBoards.values():
			board.Hide()
		
		self.pageBoards["shop_list"].Show()
		self.ShopListTable.ClearElement()
		
		for shop in self.ShopList:
			element = ShopListElement(shop)
			element.SetOnClickOpenShopButton(self.__OnClickShopListOpenShop)
			element.Show()

			self.ShopListTable.AddElement(element)
		
		if self.itemTooltip.IsShow():
			self.itemTooltip.Hide()

	def RefreshOpenShopPage(self):
		self.pageCategory = "open_shop"
		for board in self.pageBoards.values():
			board.Hide()
		
		self.pageBoards["open_shop"].Show()
		
		self.OpenShopItemsTable.ClearElement()
		for info in self.ShopItemForSale:
			slot = Slot()
			slot.SetInfo(info)
			slot.SetIndex(info["id"])
			slot.SetOnMouseLeftButtonUpEvent(self.__OnLeftClickShopItem)
			slot.Show()
			
			self.OpenShopItemsTable.AddElement(slot)
		
		name 		= self.ShopOpenInfo["name"]
		duration	= self.ShopOpenInfo["duration"]
		
		if '@' in name:
			name = name[name.find('@')+1:]
		
		self.OpenShopShopTitle.SetText(name+ "  " + localeInfo.OFFLINESHOP_ITEMS_COUNT_TEXT%self.ShopOpenInfo["count"])
		self.OpenShopShopDuration.SetText(localeInfo.BATTLEPASS_TEXT_7 +  GetDurationStringRB(duration)  + localeInfo.OFFLINE_SHOP_MAX_DAYS)

	def RefreshSearchHistoryPage(self):
		self.SearchHistoryTable.ClearElement()
		offlineshop.RefreshFilterHistory()

		SortByDatetime(self.FilterHistory)

		for elm in self.FilterHistory:
			newElement = FilterHistoryElement(elm)
			newElement.SetButtonEvent(self.__OnClickFilterHistoryElement)
			newElement.Show()
			self.SearchHistoryTable.AddElement(newElement)

	def RefreshMyPatternsPage(self):
		self.SearchPatternsTable.ClearElement()
		offlineshop.RefreshFilterPatterns()

		lst = self.FilterPatterns.values()
		SortByDatetime(lst)

		for v in lst:
			pattern = FilterPatternElement(v)
			pattern.SetButtonEvent(self.__OnClickSearchPatternElement)
			pattern.Show()

			self.SearchPatternsTable.AddElement(pattern)

	def RefreshMyOffersPage(self):
		self.pageCategory = "my_offers"
		for board in self.pageBoards.values():
			board.Hide()

		self.pageBoards["my_offers"].Show()

		self.MyOffersTable.ClearElement()

		for info in self.MyOffersList:

			offer = MyOffer(info)
			offer.Show()
			offer.SetCancelButtonEvent(self.__OnClickDeleteMyOfferButton)
			slot  = offer.slot


			if not info['is_accept']:
				viewImage = MakeOfferViewImage(info['is_notified'])
				slot.AppendChild(viewImage)
				viewImage.SetPosition(-20,-10)
				viewImage.Show()
			#updated 25-01-2020 #topatch
			else:
				offer.DisableCancelButton()

			self.MyOffersTable.AddElement(offer)

	def RefreshAuctionListPage(self):
		self.pageCategory = "auction_list"
		for board in self.pageBoards.values():
			board.Hide()

		self.pageBoards["auction_list"].Show()

		self.AuctionListTable.ClearElement()

		for info in self.AuctionListInfo:
			elm = AuctionListElement(info)
			elm.Show()
			elm.SetIndex(info['owner_id'])
			elm.SetOnClickOpenAuctionButton(self.__OnClickOpenAuctionButton)

			self.AuctionListTable.AddElement(elm)

	def RefreshMyAuctionPage(self):
		self.pageCategory = "my_auction"
		for board in self.pageBoards.values():
			board.Hide()

		self.pageBoards["my_auction"].Show()

		self.MyAuctionOfferTable.ClearElement()

		if 'offers' in self.MyAuctionInfo:
			for info in SortOffersByPrice(self.MyAuctionInfo['offers']):
				elm = AuctionOffer(info)
				elm.Show()

				self.MyAuctionOfferTable.AddElement(elm)

		best_price = GetBestOfferPriceYang(self.MyAuctionInfo.get('offers', []))
		if best_price ==0:
			min_raise  = self.MyAuctionInfo['init_yang']

		else:
			if best_price < 1000:
				min_raise = best_price + 1000
			else:
				min_raise  = long(float(best_price)*1.1)

		self.MyAuctionBestOffer.SetText(localeInfo.NumberToMoneyString(best_price))
		self.MyAuctionDuration.SetText(GetDurationString(self.MyAuctionInfo['duration']))
		self.MyAuctionMinRaise.SetText(localeInfo.NumberToMoneyString(min_raise))
		self.MyAuctionOwnerName.SetText(self.MyAuctionInfo['owner_name'])

		if 'item' in self.MyAuctionInfo:
			self.__MakeMyAuctionSlot(self.MyAuctionInfo['item'])

	def RefreshOpenAuctionPage(self):
		self.pageCategory = "open_auction"
		for board in self.pageBoards.values():
			board.Hide()

		self.pageBoards["open_auction"].Show()

		self.OpenAuctionOfferTable.ClearElement()

		if 'offers' in self.OpenAuctionInfo:
			for info in SortOffersByPrice(self.OpenAuctionInfo['offers']):
				elm = AuctionOffer(info)
				elm.Show()

				self.OpenAuctionOfferTable.AddElement(elm)

		best_price = GetBestOfferPriceYang(self.OpenAuctionInfo.get('offers' , []))
		if best_price == 0:
			min_raise = self.OpenAuctionInfo['init_yang']

		else:
			if best_price < 1000:
				min_raise = best_price + 1000
			else:
				min_raise = long(float(best_price) * 1.1)

		self.OpenAuctionInfo['min_raise'] = min_raise

		self.OpenAuctionBestOffer.SetText(localeInfo.NumberToMoneyString(best_price))
		self.OpenAuctionDuration.SetText(GetDurationString(self.OpenAuctionInfo['duration']))
		self.OpenAuctionMinRaise.SetText(localeInfo.NumberToMoneyString(min_raise))
		self.OpenAuctionOwnerName.SetText(self.OpenAuctionInfo['owner_name'])

		if 'item' in self.OpenAuctionInfo:
			self.__MakeOpenAuctionSlot(self.OpenAuctionInfo['item'])

class CategoryButton(ui.Button):
	def __init__(self, parent, parentClass, name, category_id):
		ui.Button.__init__(self)

		self.active = False
		self.categoryId = category_id
		icons = [3, 5, 10, 12, 16, 17, 23, 29, 34, 38]
		iconspng = [1, 2, 28]

		self.subButtons = []
		if (category_id in iconspng):
			self.parent = parentClass
			self.parentNode = parent
			self.SetParent(parent)
			self.SetUpVisual("d:/ymir work/ui/game/shopsearchp2p/button_01_arrow.png")
			self.SetOverVisual("d:/ymir work/ui/game/shopsearchp2p/button_02_arrow.png")
			self.SetDownVisual("d:/ymir work/ui/game/shopsearchp2p/button_03_arrow.png")
			self.SetDisableVisual("d:/ymir work/ui/game/shopsearchp2p/button_03_arrow.png")
			self.SAFE_SetEvent(self.event)
		else:
			self.parent = parentClass
			self.parentNode = parent
			self.SetParent(parent)
			self.SetUpVisual("d:/ymir work/ui/game/shopsearchp2p/button_01.png")
			self.SetOverVisual("d:/ymir work/ui/game/shopsearchp2p/button_02.png")
			self.SetDownVisual("d:/ymir work/ui/game/shopsearchp2p/button_03.png")
			self.SetDisableVisual("d:/ymir work/ui/game/shopsearchp2p/button_03.png")
			self.SAFE_SetEvent(self.event)

		if (category_id in icons):
			self.icon = ui.ImageBox()
			self.icon.SetParent(self)
			self.icon.SetPosition(185/2-85, 5)
			self.icon.LoadImage("d:/ymir work/ui/game/shopsearchp2p/icon/%d.dds" % category_id)
			self.icon.Show()

		if (category_id in iconspng):
			self.icon = ui.ImageBox()
			self.icon.SetParent(self)
			self.icon.SetPosition(185/2-85, 5)
			self.icon.LoadImage("d:/ymir work/ui/game/shopsearchp2p/icon/%d.png" % category_id)
			self.icon.Show()

		self.valueName = ui.TextLine()
		self.valueName.SetParent(self)
		self.valueName.SetPosition(185/2-50, 5)
		self.valueName.SetText(name)
		self.valueName.Show()

		self.Show()

	def SetPositionHelper(self, x, y):
		self.SetPosition(x, y)

		for i in range(len(self.subButtons)):
			y += 28
			self.subButtons[i][0].SetPosition(0, y)

	def UpdateSubButtons(self, category, subcategory):
		if category == self.categoryId and subcategory == 255:
			self.Disable()
		else:
			self.Enable()

		for i in range(len(self.subButtons)):
			if self.subButtons[i][1] == subcategory and self.categoryId == category:
				self.subButtons[i][0].Disable()
			else:
				self.subButtons[i][0].Enable()

	def event(self):
		self.active = self.active != True

		if self.active or len(self.subButtons) == 0:
			self.parent.SetCategory(self.categoryId, 255)

		for i in range(len(self.subButtons)):
			if self.active:
				self.subButtons[i][0].Show()
			else:
				self.subButtons[i][0].Hide()

		self.parent.RefreshButtons()

	def __del__(self):
		ui.Button.__del__(self)

	def AddSubButton(self, name, subcategory):
		button = ui.Button()
		button.SetParent(self.parentNode)
		button.SetUpVisual("d:/ymir work/ui/game/shopsearchp2p/button_01.png")
		button.SetOverVisual("d:/ymir work/ui/game/shopsearchp2p/button_02.png")
		button.SetDownVisual("d:/ymir work/ui/game/shopsearchp2p/button_03.png")
		button.SetDisableVisual("d:/ymir work/ui/game/shopsearchp2p/button_03.png")
		button.SetText(name)
		button.SAFE_SetEvent(self.parent.SetCategory, self.categoryId, subcategory)
		button.Hide()

		self.subButtons.append([button, subcategory])

		return button

class ExpandingMenu(ui.Button):
	ANIMATION_DURATION = 0.3

	def __init__(self, parent, name):
		ui.Button.__init__(self)
		self.SetParent(parent)

		self.name = name
		self.animationStart = 0

		self.animation = 0
		self.isExpanded = False
		self.parent = parent
		self.menuOptions = []

		self.valueName = ui.TextLine()
		self.valueName.SetParent(self)
		self.valueName.SetPosition(185/2-60, 5)
		self.valueName.SetText(name)
		self.valueName.Show()

		self.SetUpVisual("d:/ymir work/ui/game/shopsearchp2p/button_01.png")
		self.SetOverVisual("d:/ymir work/ui/game/shopsearchp2p/button_02.png")
		self.SetDownVisual("d:/ymir work/ui/game/shopsearchp2p/button_01.png")

		self.SAFE_SetEvent(self.OnClick)
		self.OnUpdate()
		self.Show()

	def OnClick(self):
		if app.GetGlobalTimeStamp() - self.animationStart < ExpandingMenu.ANIMATION_DURATION:
			return

		if self.isExpanded:
			self.Collapse()
		else:
			self.Expand()

	def AddMenuOption(self, name, event, *args):
		button = ui.Button()
		button.SetParent(self.parent)
		button.SetUpVisual("d:/ymir work/ui/game/shopsearchp2p/button_01.png")
		button.SetOverVisual("d:/ymir work/ui/game/shopsearchp2p/button_02.png")
		button.SetDownVisual("d:/ymir work/ui/game/shopsearchp2p/button_01.png")
		button.SetText(name)
		button.name = name
		button.Hide()

		event = ui.__mem_func__(event)
		button.SAFE_SetEvent(self.SubEvent, button, event, *args)

		self.menuOptions.append(button)

		return button

	def SubEvent(self, btn, event, *args):
		self.valueName.SetText(localeInfo.OFFLINE_SHOP_MENU_ % btn.name)

		event(*args)

	def OnUpdate(self):
		if self.animation != 0:
			timeDiff = app.GetTime() - self.animationStart
			percent = min(1.0, 1.0 * timeDiff / ExpandingMenu.ANIMATION_DURATION)

			yProgress = percent
			if self.animation == -1:
				yProgress = 1.0 - percent

			(x, y) = self.GetLocalPosition()
			h = self.GetHeight() - 1
			for btn, i in zip(self.menuOptions, xrange(1, 1 + len(self.menuOptions))):
				btnY = y + (i * h * yProgress)
				btn.SetPosition(426, btnY)

			if percent == 1.0:
				if self.animation == 1:
					self.isExpanded = True
				else:
					self.isExpanded = False
					for btn in self.menuOptions:
						btn.Hide()

				self.animation = 0

		self.SetTop()

	def Expand(self):
		(x, y) = self.GetLocalPosition()

		for btn in self.menuOptions:
			btn.SetPosition(x, y)
			btn.Show()

		self.SetTop()

		self.animationStart = app.GetTime()
		self.animation = 1

	def Collapse(self):
		self.SetTop()

		self.animationStart = app.GetTime()
		self.animation = -1

	def __del__(self):
		ui.Button.__del__(self)
