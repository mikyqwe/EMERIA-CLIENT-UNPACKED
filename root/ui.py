import app
import ime
import grp
import snd
import wndMgr
import item
import skill
if app.NEW_PET_SYSTEM:
	import petskill
import localeInfo
import dbg
import player
# MARK_BUG_FIX
import guild
# END_OF_MARK_BUG_FIX
import constInfo
import systemSetting

from _weakref import proxy

BACKGROUND_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 1.0)
DARK_COLOR = grp.GenerateColor(0.2, 0.2, 0.2, 1.0)
BRIGHT_COLOR = grp.GenerateColor(0.7, 0.7, 0.7, 1.0)

if localeInfo.IsCANADA():
	SELECT_COLOR = grp.GenerateColor(0.9, 0.03, 0.01, 0.4)
else:
	SELECT_COLOR = grp.GenerateColor(0.0, 0.0, 0.5, 0.3)

if app.INGAME_WIKI:
	SELECT_COLOR_WIKI = grp.GenerateColor(36.4 / 255.0, 17.6 / 255.0, 0.0 / 255.0, 1.0)

WHITE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.5)
HALF_WHITE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.2)

createToolTipWindowDict = {}
def RegisterCandidateWindowClass(codePage, candidateWindowClass):
	EditLine.candidateWindowClassDict[codePage]=candidateWindowClass
def RegisterToolTipWindow(type, createToolTipWindow):
	createToolTipWindowDict[type]=createToolTipWindow

app.SetDefaultFontName(localeInfo.UI_DEF_FONT)

## Window Manager Event List##
##############################
## "OnMouseLeftButtonDown"
## "OnMouseLeftButtonUp"
## "OnMouseLeftButtonDoubleClick"
## "OnMouseRightButtonDown"
## "OnMouseRightButtonUp"
## "OnMouseRightButtonDoubleClick"
## "OnMouseDrag"
## "OnSetFocus"
## "OnKillFocus"
## "OnMouseOverIn"
## "OnMouseOverOut"
## "OnRender"
## "OnUpdate"
## "OnKeyDown"
## "OnKeyUp"
## "OnTop"
## "OnIMEUpdate" ## IME Only
## "OnIMETab"	## IME Only
## "OnIMEReturn" ## IME Only
##############################
## Window Manager Event List##


class __mem_func__:
	class __noarg_call__:
		def __init__(self, cls, obj, func):
			self.cls=cls
			self.obj=proxy(obj)
			self.func=proxy(func)

		def __call__(self, *arg):
			return self.func(self.obj)

	class __arg_call__:
		def __init__(self, cls, obj, func):
			self.cls=cls
			self.obj=proxy(obj)
			self.func=proxy(func)

		def __call__(self, *arg):
			return self.func(self.obj, *arg)

	def __init__(self, mfunc):
		if mfunc.im_func.func_code.co_argcount>1:
			self.call=__mem_func__.__arg_call__(mfunc.im_class, mfunc.im_self, mfunc.im_func)
		else:
			self.call=__mem_func__.__noarg_call__(mfunc.im_class, mfunc.im_self, mfunc.im_func)

	def __call__(self, *arg):
		return self.call(*arg)


class Window(object):
	def NoneMethod(cls):
		pass

	NoneMethod = classmethod(NoneMethod)

	def __init__(self, layer = "UI"):
		self.hWnd = None
		self.parentWindow = 0
		self.onMouseLeftButtonUpEvent = None
		self.onRunMouseWheelEvent = None
		self.RegisterWindow(layer)
		self.exPos = (0,0)
		self.Hide()
		if app.BL_MAILBOX:
			self.onMouseLeftButtonUpEventArgs = None
			self.overFunc = None
			self.overArgs = None
			self.overOutFunc = None
			self.overOutArgs = None
		if app.INGAME_WIKI:
			self.mouseLeftButtonDownEvent = None
			self.mouseLeftButtonDownArgs = None
			self.overInEvent = None
			self.overInArgs = None
			self.overOutEvent = None
			self.overOutArgs = None
			
			self.SetWindowName("NONAME_Window")
		if app.ENABLE_QUEST_RENEWAL:
			self.propertyList = {}		
		if app.ENABLE_SEND_TARGET_INFO:
			self.mouseLeftButtonDownEvent = None
			self.mouseLeftButtonDownArgs = None
			self.mouseLeftButtonUpEvent = None
			self.mouseLeftButtonUpArgs = None
			self.mouseLeftButtonDoubleClickEvent = None
			self.mouseRightButtonDownEvent = None
			self.mouseRightButtonDownArgs = None
			self.moveWindowEvent = None
			self.renderEvent = None
			self.renderArgs = None

			self.overInEvent = None
			self.overInArgs = None

			self.overOutEvent = None
			self.overOutArgs = None

			self.baseX = 0
			self.baseY = 0

			self.SetWindowName("NONAME_Window")

	def __del__(self):
		wndMgr.Destroy(self.hWnd)

		if app.BL_MAILBOX:
			self.onMouseLeftButtonUpEventArgs = None
			self.overFunc = None
			self.overArgs = None
			self.overOutFunc = None
			self.overOutArgs = None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.Register(self, layer)

	def Destroy(self):
		pass

	def GetWindowHandle(self):
		return self.hWnd

	def AddFlag(self, style):
		wndMgr.AddFlag(self.hWnd, style)

	def IsRTL(self):
		return wndMgr.IsRTL(self.hWnd)

	def SetWindowName(self, Name):
		wndMgr.SetName(self.hWnd, Name)

	def GetWindowName(self):
		return wndMgr.GetName(self.hWnd)

	if app.ENABLE_WINDOW_SLIDE_EFFECT:
		def SetSpecialWindow(self):
			wndMgr.SetSpecialWindow(self.hWnd)

	if app.ENABLE_SEND_TARGET_INFO:
		def SetParent(self, parent):
			if parent:
				wndMgr.SetParent(self.hWnd, parent.hWnd)
			else:
				wndMgr.SetParent(self.hWnd, 0)
	
		def SetAttachParent(self, parent):
			wndMgr.SetAttachParent(self.hWnd, parent.hWnd)
	else:
		def SetParent(self, parent):
			wndMgr.SetParent(self.hWnd, parent.hWnd)

	def SetParentProxy(self, parent):
		self.parentWindow=proxy(parent)
		wndMgr.SetParent(self.hWnd, parent.hWnd)

	def GetParentProxy(self):
		return self.parentWindow

	def SetPickAlways(self):
		wndMgr.SetPickAlways(self.hWnd)

	def SetWindowHorizontalAlignLeft(self):
		wndMgr.SetWindowHorizontalAlign(self.hWnd, wndMgr.HORIZONTAL_ALIGN_LEFT)

	def SetWindowHorizontalAlignCenter(self):
		wndMgr.SetWindowHorizontalAlign(self.hWnd, wndMgr.HORIZONTAL_ALIGN_CENTER)

	def SetWindowHorizontalAlignRight(self):
		wndMgr.SetWindowHorizontalAlign(self.hWnd, wndMgr.HORIZONTAL_ALIGN_RIGHT)

	def SetWindowVerticalAlignTop(self):
		wndMgr.SetWindowVerticalAlign(self.hWnd, wndMgr.VERTICAL_ALIGN_TOP)

	def SetWindowVerticalAlignCenter(self):
		wndMgr.SetWindowVerticalAlign(self.hWnd, wndMgr.VERTICAL_ALIGN_CENTER)

	def SetWindowVerticalAlignBottom(self):
		wndMgr.SetWindowVerticalAlign(self.hWnd, wndMgr.VERTICAL_ALIGN_BOTTOM)

	def SetTop(self):
		wndMgr.SetTop(self.hWnd)

	def Show(self):
		wndMgr.Show(self.hWnd)

	def Hide(self):
		wndMgr.Hide(self.hWnd)
	if app.ENABLE_SEND_TARGET_INFO:
		def SetVisible(self, is_show):
			if is_show:
				self.Show()
			else:
				self.Hide()

	def Lock(self):
		wndMgr.Lock(self.hWnd)

	def Unlock(self):
		wndMgr.Unlock(self.hWnd)

	def IsShow(self):
		return wndMgr.IsShow(self.hWnd)

	def UpdateRect(self):
		wndMgr.UpdateRect(self.hWnd)

	def SetSize(self, width, height):
		wndMgr.SetWindowSize(self.hWnd, width, height)

	def GetWidth(self):
		return wndMgr.GetWindowWidth(self.hWnd)

	def GetHeight(self):
		return wndMgr.GetWindowHeight(self.hWnd)

	def GetLocalPosition(self):
		return wndMgr.GetWindowLocalPosition(self.hWnd)
	if app.ENABLE_SEND_TARGET_INFO:
		def GetLeft(self):
			x, y = self.GetLocalPosition()
			return x
	
		def GetGlobalLeft(self):
			x, y = self.GetGlobalPosition()
			return x
	
		def GetTop(self):
			x, y = self.GetLocalPosition()
			return y
	
		def GetGlobalTop(self):
			x, y = self.GetGlobalPosition()
			return y
	
		def GetRight(self):
			return self.GetLeft() + self.GetWidth()
	
		def GetBottom(self):
			return self.GetTop() + self.GetHeight()

	def GetGlobalPosition(self):
		return wndMgr.GetWindowGlobalPosition(self.hWnd)

	def GetMouseLocalPosition(self):
		return wndMgr.GetMouseLocalPosition(self.hWnd)

	def GetRect(self):
		return wndMgr.GetWindowRect(self.hWnd)
	if app.ENABLE_SEND_TARGET_INFO:
		def SetLeft(self, x):
			wndMgr.SetWindowPosition(self.hWnd, x, self.GetTop())

	def SetPosition(self, x, y, flag = False):
		if flag == True:
			self.exPos = (x,y)
		wndMgr.SetWindowPosition(self.hWnd, x, y)

	def SetCenterPosition(self, x = 0, y = 0):
		self.SetPosition((wndMgr.GetScreenWidth() - self.GetWidth()) / 2 + x, (wndMgr.GetScreenHeight() - self.GetHeight()) / 2 + y)
		
	if app.ENABLE_WINDOW_SLIDE_EFFECT:
		def SetStoredPosition(self, x,y):
			wndMgr.SetStoredPosition(self.hWnd, x, y)		
		
	if app.ENABLE_SEND_TARGET_INFO:
		def SavePosition(self):
			self.baseX = self.GetLeft()
			self.baseY = self.GetTop()
	
		def UpdatePositionByScale(self, scale):
			self.SetPosition(self.baseX * scale, self.baseY * scale)

	def IsFocus(self):
		return wndMgr.IsFocus(self.hWnd)

	def SetFocus(self):
		wndMgr.SetFocus(self.hWnd)

	def KillFocus(self):
		wndMgr.KillFocus(self.hWnd)

	def GetChildCount(self):
		return wndMgr.GetChildCount(self.hWnd)

	if app.INGAME_WIKI:
		def IsIn(self, checkChilds = False):
			return wndMgr.IsIn(self.hWnd, checkChilds)
		
		def GetRenderBox(self):
			return wndMgr.GetRenderBox(self.hWnd)
		
		def SetInsideRender(self, val):
			wndMgr.SetInsideRender(self.hWnd, val)
		
		def IsInPosition(self):
			xMouse, yMouse = wndMgr.GetMousePosition()
			x, y = self.GetGlobalPosition()
			return xMouse >= x and xMouse < x + self.GetWidth() and yMouse >= y and yMouse < y + self.GetHeight()
		
		def SetMouseLeftButtonDownEvent(self, event, *args):
			self.mouseLeftButtonDownEvent = event
			self.mouseLeftButtonDownArgs = args

		def OnMouseLeftButtonDown(self):
			if self.mouseLeftButtonDownEvent:
				apply(self.mouseLeftButtonDownEvent, self.mouseLeftButtonDownArgs)
		
		def SAFE_SetOverInEvent(self, func, *args):
			self.overInEvent = __mem_func__(func)
			self.overInArgs = args
		
		def SAFE_SetOverOutEvent(self, func, *args):
			self.overOutEvent = __mem_func__(func)
			self.overOutArgs = args
		
		def OnMouseOverIn(self):
			if self.overInEvent:
				apply(self.overInEvent, self.overInArgs)
		
		def OnMouseOverOut(self):
			if self.overOutEvent:
				apply(self.overOutEvent, self.overOutArgs)
		
		def AdjustSize(self):
			x, y = self.GetTextSize()
			wndMgr.SetWindowSize(self.hWnd, x, y)
	else:
		def IsIn(self):
			return wndMgr.IsIn(self.hWnd)

	if app.ENABLE_SEND_TARGET_INFO:
		def IsInPosition(self):
			xMouse, yMouse = wndMgr.GetMousePosition()
			x, y = self.GetGlobalPosition()
			return xMouse >= x and xMouse < x + self.GetWidth() and yMouse >= y and yMouse < y + self.GetHeight()
	
		def SetMouseLeftButtonDownEvent(self, event, *args):
			self.mouseLeftButtonDownEvent = event
			self.mouseLeftButtonDownArgs = args
	
		def OnMouseLeftButtonDown(self):
			if self.mouseLeftButtonDownEvent:
				apply(self.mouseLeftButtonDownEvent, self.mouseLeftButtonDownArgs)

	if app.BL_MAILBOX:
		def OnMouseOverIn(self):
			if self.overFunc:
				apply(self.overFunc, self.overArgs )
		def OnMouseOverOut(self):
			if self.overOutFunc:
				apply(self.overOutFunc, self.overOutArgs )
		def SetOverEvent(self, func, *args):
			self.overFunc = func
			self.overArgs = args
		def SetOverOutEvent(self, func, *args):
			self.overOutFunc = func
			self.overOutArgs = args

		def SetOnMouseLeftButtonUpEvent(self, event, *args):
			self.onMouseLeftButtonUpEvent		= event
			self.onMouseLeftButtonUpEventArgs	= args

	if app.ENABLE_SEND_TARGET_INFO:
		def SetMouseLeftButtonUpEvent(self, event, *args):
			self.mouseLeftButtonUpEvent = event
			self.mouseLeftButtonUpArgs = args
	else:
		def SetOnMouseLeftButtonUpEvent(self, event):
			self.onMouseLeftButtonUpEvent = event

	if app.ENABLE_SEND_TARGET_INFO:
		def SetMouseLeftButtonDoubleClickEvent(self, event):
			self.mouseLeftButtonDoubleClickEvent = event
	
		def OnMouseLeftButtonDoubleClick(self):
			if self.mouseLeftButtonDoubleClickEvent:
				self.mouseLeftButtonDoubleClickEvent()
	
		def SetMouseRightButtonDownEvent(self, event, *args):
			self.mouseRightButtonDownEvent = event
			self.mouseRightButtonDownArgs = args
	
		def OnMouseRightButtonDown(self):
			if self.mouseRightButtonDownEvent:
				apply(self.mouseRightButtonDownEvent, self.mouseRightButtonDownArgs)
	
		def SetMoveWindowEvent(self, event):
			self.moveWindowEvent = event
	
		def OnMoveWindow(self, x, y):
			if self.moveWindowEvent:
				self.moveWindowEvent(x, y)
	
		def SAFE_SetOverInEvent(self, func, *args):
			self.overInEvent = __mem_func__(func)
			self.overInArgs = args
	
		def SetOverInEvent(self, func, *args):
			self.overInEvent = func
			self.overInArgs = args
	
		def SAFE_SetOverOutEvent(self, func, *args):
			self.overOutEvent = __mem_func__(func)
			self.overOutArgs = args
	
		def SetOverOutEvent(self, func, *args):
			self.overOutEvent = func
			self.overOutArgs = args
	
		def OnMouseOverIn(self):
			if self.overInEvent:
				apply(self.overInEvent, self.overInArgs)
	
		def OnMouseOverOut(self):
			if self.overOutEvent:
				apply(self.overOutEvent, self.overOutArgs)
	
		def SAFE_SetRenderEvent(self, event, *args):
			self.renderEvent = __mem_func__(event)
			self.renderArgs = args
	
		def ClearRenderEvent(self):
			self.renderEvent = None
			self.renderArgs = None
	
		def OnRender(self):
			if self.renderEvent:
				apply(self.renderEvent, self.renderArgs)

	def OnMouseLeftButtonUp(self):
		if self.onMouseLeftButtonUpEvent:
			self.onMouseLeftButtonUpEvent()

	if app.ENABLE_QUEST_RENEWAL:
		def SetProperty(self, propName, propValue):
			self.propertyList[propName] = propValue

		def GetProperty(self, propName):
			if propName in self.propertyList:
				return self.propertyList[propName]

			return None
			
	if app.ENABLE_WINDOW_SLIDE_EFFECT:
		def EnableSlidingEffect(self):
			wndMgr.EnableSlidingEffect(self.hWnd)
		
		def DisableSlidingEffect(self):
			wndMgr.DisableSlidingEffect(self.hWnd)
		
		def SlideIn(self):
			wndMgr.SlideIn(self.hWnd)
			
		def SlideOut(self):
			wndMgr.SlideOut(self.hWnd)
			
		def StopSlideIn(self):
			wndMgr.StopSlideIn(self.hWnd)
		
		def StopSlidOut(self):
			wndMgr.StopSlidOut(self.hWnd)

def calculateRect(curValue, maxValue):
	try:
		return -1.0 + float(curValue) / float(maxValue)
	except:
		return 0.0

class ListBoxEx(Window):

	class Item(Window):
		def __init__(self):
			Window.__init__(self)

		def __del__(self):
			Window.__del__(self)

		def SetParent(self, parent):
			Window.SetParent(self, parent)
			self.parent=proxy(parent)

		def OnMouseLeftButtonDown(self):
			self.parent.SelectItem(self)

		def OnRender(self):
			if self.parent.GetSelectedItem()==self:
				self.OnSelectedRender()

		def OnSelectedRender(self):
			x, y = self.GetGlobalPosition()
			grp.SetColor(grp.GenerateColor(0.0, 0.0, 0.7, 0.7))
			grp.RenderBar(x, y, self.GetWidth(), self.GetHeight())

	def __init__(self):
		Window.__init__(self)

		self.viewItemCount=10
		self.basePos=0
		self.itemHeight=16
		self.itemStep=20
		self.isGuildStatistics=False
		self.selItem=0
		self.itemList=[]
		self.onSelectItemEvent = lambda *arg: None

		self.xExtra = 0
		self.yExtra = 0

		if localeInfo.IsARABIC():
			self.itemWidth=130
		else:
			self.itemWidth=100

		self.scrollBar=None
		self.__UpdateSize()

	def __del__(self):
		Window.__del__(self)

	def __UpdateSize(self):
		height=self.itemStep*self.__GetViewItemCount()

		self.SetSize(self.itemWidth, height)
		
	def SetGuildLogStatistics(self):
		self.isGuildStatistics = True
	def SetPositionExtra(self, x, y):
		self.xExtra = x
		self.yExtra = y
		
	def SetParinte(self, parent):
		self.parinte = proxy(parent)

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

	def SetBasePos(self, basePos):
		for oldItem in self.itemList[self.basePos:self.basePos+self.viewItemCount]:
			oldItem.Hide()

		self.basePos=basePos

		pos=basePos
		for newItem in self.itemList[self.basePos:self.basePos+self.viewItemCount]:
			(x, y)=self.GetItemViewCoord(pos, newItem.GetWidth())
			newItem.SetPosition(x + self.xExtra, y + self.yExtra)
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
		if self.isGuildStatistics:
			if self.selItem:
				self.selItem.UnSelectedRender()
		self.selItem=selItem
		self.onSelectItemEvent(selItem)
		if self.isGuildStatistics:
			if self.selItem:
				self.selItem.OnSelectedRender()

	def RemoveAllItems(self):
		self.selItem=None
		self.itemList=[]

		if self.scrollBar:
			self.scrollBar.SetPos(0)
			
	if app.ENABLE_SWITCHBOT:
		def GetItems(self):
			return self.itemList

	def RemoveItem(self, delItem):
		if delItem==self.selItem:
			self.selItem=None

		self.itemList.remove(delItem)

	def AppendItem(self, newItem, hiley = 0):
		if hiley == 0:
			newItem.SetParent(self)
		else:
			newItem.SetParent(self.parinte)
		newItem.SetSize(self.itemWidth, self.itemHeight)

		pos=len(self.itemList)
		if self.__IsInViewRange(pos):
			(x, y)=self.GetItemViewCoord(pos, newItem.GetWidth())
			newItem.SetPosition(x + self.xExtra, y + self.yExtra)
			newItem.Show()
		else:
			newItem.Hide()

		self.itemList.append(newItem)

	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(__mem_func__(self.__OnScroll))
		self.scrollBar=scrollBar

	def __OnScroll(self):
		self.SetBasePos(int(self.scrollBar.GetPos()*self.__GetScrollLen()))

	def __GetScrollLen(self):
		scrollLen=self.__GetItemCount()-self.__GetViewItemCount()
		if scrollLen<0:
			return 0

		return scrollLen

	def __GetViewItemCount(self):
		return self.viewItemCount

	def GetCount(self):
		return len(self.itemList)

	def __GetItemCount(self):
		return len(self.itemList)
		
	if app.INGAME_WIKI:
		def GetItemCount(self):
			return len(self.itemList)

	def GetItemViewCoord(self, pos, itemWidth):
		if localeInfo.IsARABIC():
			return (self.GetWidth()-itemWidth-10, (pos-self.basePos)*self.itemStep)
		else:
			return (0, (pos-self.basePos)*self.itemStep)

	def __IsInViewRange(self, pos):
		if pos<self.basePos:
			return 0
		if pos>=self.basePos+self.viewItemCount:
			return 0
		return 1

if app.ENABLE_SEND_TARGET_INFO:
	class ListBoxExNew(Window):
		class Item(Window):
			def __init__(self):
				Window.__init__(self)

				self.realWidth = 0
				self.realHeight = 0

				self.removeTop = 0
				self.removeBottom = 0

				self.SetWindowName("NONAME_ListBoxExNew_Item")

			def __del__(self):
				Window.__del__(self)
				
			
			def ShowCorner(self, corner):
				self.Corners[corner].Show()
				self.SetSize(self.GetWidth(), self.GetHeight())


			def SetParent(self, parent):
				Window.SetParent(self, parent)
				self.parent=proxy(parent)

			def SetSize(self, width, height):
				self.realWidth = width
				self.realHeight = height
				Window.SetSize(self, width, height)

			def SetRemoveTop(self, height):
				self.removeTop = height
				self.RefreshHeight()

			def SetRemoveBottom(self, height):
				self.removeBottom = height
				self.RefreshHeight()

			def SetCurrentHeight(self, height):
				Window.SetSize(self, self.GetWidth(), height)

			def GetCurrentHeight(self):
				return Window.GetHeight(self)

			def ResetCurrentHeight(self):
				self.removeTop = 0
				self.removeBottom = 0
				self.RefreshHeight()

			def RefreshHeight(self):
				self.SetCurrentHeight(self.GetHeight() - self.removeTop - self.removeBottom)

			def GetHeight(self):
				return self.realHeight

		def __init__(self, stepSize, viewSteps):
			Window.__init__(self)

			self.viewItemCount=10
			self.basePos=0
			self.baseIndex=0
			self.maxSteps=0
			self.viewSteps = viewSteps
			self.stepSize = stepSize
			self.itemList=[]

			self.scrollBar=None

			self.SetWindowName("NONAME_ListBoxEx")

		def __del__(self):
			Window.__del__(self)

		def IsEmpty(self):
			if len(self.itemList)==0:
				return 1
			return 0

		def __CheckBasePos(self, pos):
			self.viewItemCount = 0

			start_pos = pos

			height = 0
			while height < self.GetHeight():
				if pos >= len(self.itemList):
					return start_pos == 0
				height += self.itemList[pos].GetHeight()
				pos += 1
				self.viewItemCount += 1
			return height == self.GetHeight()

		def SetBasePos(self, basePos, forceRefresh = TRUE):
			if forceRefresh == FALSE and self.basePos == basePos:
				return

			for oldItem in self.itemList[self.baseIndex:self.baseIndex+self.viewItemCount]:
				oldItem.ResetCurrentHeight()
				oldItem.Hide()

			self.basePos=basePos

			baseIndex = 0
			while basePos > 0:
				basePos -= self.itemList[baseIndex].GetHeight() / self.stepSize
				if basePos < 0:
					self.itemList[baseIndex].SetRemoveTop(self.stepSize * abs(basePos))
					break
				baseIndex += 1
			self.baseIndex = baseIndex

			stepCount = 0
			self.viewItemCount = 0
			while baseIndex < len(self.itemList):
				stepCount += self.itemList[baseIndex].GetCurrentHeight() / self.stepSize
				self.viewItemCount += 1
				if stepCount > self.viewSteps:
					self.itemList[baseIndex].SetRemoveBottom(self.stepSize * (stepCount - self.viewSteps))
					break
				elif stepCount == self.viewSteps:
					break
				baseIndex += 1

			y = 0
			for newItem in self.itemList[self.baseIndex:self.baseIndex+self.viewItemCount]:
				newItem.SetPosition(0, y)
				newItem.Show()
				y += newItem.GetCurrentHeight()

		def GetItemIndex(self, argItem):
			return self.itemList.index(argItem)

		def GetSelectedItem(self):
			return self.selItem

		def GetSelectedItemIndex(self):
			return self.selItemIdx

		def RemoveAllItems(self):
			self.itemList=[]
			self.maxSteps=0

			if self.scrollBar:
				self.scrollBar.SetPos(0)

		def RemoveItem(self, delItem):
			self.maxSteps -= delItem.GetHeight() / self.stepSize
			self.itemList.remove(delItem)

		def AppendItem(self, newItem):
			if newItem.GetHeight() % self.stepSize != 0:
				import dbg
				dbg.TraceError("Invalid AppendItem height %d stepSize %d" % (newItem.GetHeight(), self.stepSize))
				return

			self.maxSteps += newItem.GetHeight() / self.stepSize
			newItem.SetParent(self)
			self.itemList.append(newItem)

		def SetScrollBar(self, scrollBar):
			scrollBar.SetScrollEvent(__mem_func__(self.__OnScroll))
			self.scrollBar=scrollBar

		def __OnScroll(self):
			self.SetBasePos(int(self.scrollBar.GetPos()*self.__GetScrollLen()), FALSE)

		def __GetScrollLen(self):
			scrollLen=self.maxSteps-self.viewSteps
			if scrollLen<0:
				return 0

			return scrollLen

		def __GetViewItemCount(self):
			return self.viewItemCount

		def __GetItemCount(self):
			return len(self.itemList)

		def GetViewItemCount(self):
			return self.viewItemCount

		def GetItemCount(self):
			return len(self.itemList)

class CandidateListBox(ListBoxEx):

	HORIZONTAL_MODE = 0
	VERTICAL_MODE = 1

	class Item(ListBoxEx.Item):
		def __init__(self, text):
			ListBoxEx.Item.__init__(self)

			self.textBox=TextLine()
			self.textBox.SetParent(self)
			self.textBox.SetText(text)
			self.textBox.Show()

		def __del__(self):
			ListBoxEx.Item.__del__(self)

	def __init__(self, mode = HORIZONTAL_MODE):
		ListBoxEx.__init__(self)
		self.itemWidth=32
		self.itemHeight=32
		self.mode = mode

	def __del__(self):
		ListBoxEx.__del__(self)

	def SetMode(self, mode):
		self.mode = mode

	def AppendItem(self, newItem):
		ListBoxEx.AppendItem(self, newItem)

	def GetItemViewCoord(self, pos):
		if self.mode == self.HORIZONTAL_MODE:
			return ((pos-self.basePos)*self.itemStep, 0)
		elif self.mode == self.VERTICAL_MODE:
			return (0, (pos-self.basePos)*self.itemStep)

class TextBoxMultiLine(Window):

	MULTILINE_DEFAULT_HEIGHT = 10
	MULTILINE_DEFAULT_WIDTH = 200
	MULTILINE_LINE_SPACE = 17
	MULTILINE_DEFAULT_NCHARS = 35
	
	
	def __init__(self):
		Window.__init__(self)
		
		self.multiLineHeight = self.MULTILINE_DEFAULT_HEIGHT
		self.multiLineWidth = self.MULTILINE_DEFAULT_WIDTH
		self.lines = []
		
		self.ResizeTexBox()
		
		
	def __del__(self):
		Window.__del__(self)
		
	def ClearAll(self):
		for textLine in self.lines:
			del textLine
		self.lines = []
		self.multiLineHeight = self.MULTILINE_DEFAULT_HEIGHT
		self.multiLineWidth = self.MULTILINE_DEFAULT_WIDTH
		
	def AppendSpace(self, size):
		self.multiLineHeight += size
		self.ResizeTexBox()
		
	def __AppendTextLine(self, text, color, centerAlign = True):
		textLine = TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(localeInfo.UI_DEF_FONT)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.Show()

		if centerAlign:
			textLine.SetPosition(self.multiLineWidth/2, self.multiLineHeight)
			textLine.SetHorizontalAlignCenter()

		else:
			textLine.SetPosition(10, self.multiLineHeight)

		self.lines.append(textLine)

		self.multiLineHeight += self.MULTILINE_LINE_SPACE
		self.ResizeTexBox()
		
		
	def SetText(self, text, color=grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)):
		lines = self.__SplitText(text)
		if not lines:
			return

		self.AppendSpace(5)
		for line in lines:
			self.__AppendTextLine(line, color)
	
	def ResizeTexBox(self):
		self.SetSize(self.multiLineWidth, self.multiLineHeight)
		
		
	def __SplitText(self, desc):
		total_tokens = desc.split()
		line_tokens = []
		line_len = 0
		lines = []
		for token in total_tokens:
			if "|" in token:
				sep_pos = token.find("|")
				line_tokens.append(token[:sep_pos])

				lines.append(" ".join(line_tokens))
				line_len = len(token) - (sep_pos + 1)
				line_tokens = [token[sep_pos+1:]]
			else:
				line_len += len(token)
				if len(line_tokens) + line_len > self.MULTILINE_DEFAULT_NCHARS:
					lines.append(" ".join(line_tokens))
					line_len = len(token)
					line_tokens = [token]
				else:
					line_tokens.append(token)
		
		if line_tokens:
			lines.append(" ".join(line_tokens))

		return lines
class TextLine(Window):
	def __init__(self):
		Window.__init__(self)

		self.max = 0
		self.SetFontName(localeInfo.UI_DEF_FONT)

		if app.ENABLE_WINDOW_SLIDE_EFFECT:
			self.SetSpecialWindow()

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterTextLine(self, layer)

		if app.ENABLE_WINDOW_SLIDE_EFFECT:
			self.SetSpecialWindow()

	if app.INGAME_WIKI:
		def GetRenderPos(self):
			return wndMgr.GetRenderPos(self.hWnd)

		def SetFixedRenderPos(self, startPos, endPos):
			wndMgr.SetFixedRenderPos(self.hWnd, startPos, endPos)


	def SetMax(self, max):
		wndMgr.SetMax(self.hWnd, max)

	def SetLimitWidth(self, width):
		wndMgr.SetLimitWidth(self.hWnd, width)

	def SetMultiLine(self):
		wndMgr.SetMultiLine(self.hWnd, True)

	def SetHorizontalAlignLeft(self):
		wndMgr.SetHorizontalAlign(self.hWnd, wndMgr.TEXT_HORIZONTAL_ALIGN_LEFT)

	def SetHorizontalAlignRight(self):
		wndMgr.SetHorizontalAlign(self.hWnd, wndMgr.TEXT_HORIZONTAL_ALIGN_RIGHT)

	def SetHorizontalAlignCenter(self):
		wndMgr.SetHorizontalAlign(self.hWnd, wndMgr.TEXT_HORIZONTAL_ALIGN_CENTER)

	def SetVerticalAlignTop(self):
		wndMgr.SetVerticalAlign(self.hWnd, wndMgr.TEXT_VERTICAL_ALIGN_TOP)

	def SetVerticalAlignBottom(self):
		wndMgr.SetVerticalAlign(self.hWnd, wndMgr.TEXT_VERTICAL_ALIGN_BOTTOM)

	def SetVerticalAlignCenter(self):
		wndMgr.SetVerticalAlign(self.hWnd, wndMgr.TEXT_VERTICAL_ALIGN_CENTER)

	def SetSecret(self, Value = True):
		wndMgr.SetSecret(self.hWnd, Value)

	def SetOutline(self, Value = True):
		wndMgr.SetOutline(self.hWnd, Value)

	def SetFeather(self, value = True):
		wndMgr.SetFeather(self.hWnd, value)

	def SetFontName(self, fontName):
		wndMgr.SetFontName(self.hWnd, fontName)

	def SetDefaultFontName(self):
		wndMgr.SetFontName(self.hWnd, localeInfo.UI_DEF_FONT)

	def SetFontColor(self, red, green, blue):
		wndMgr.SetFontColor(self.hWnd, red, green, blue)

	def SetPackedFontColor(self, color):
		wndMgr.SetFontColor(self.hWnd, color)

	def SetText(self, text):
		wndMgr.SetText(self.hWnd, text)

	def GetTextLineCount(self):
		return wndMgr.GetTextLineCount(self.hWnd)

	# def DisableEnterToken(self):
		# wndMgr.DisableEnterToken(self.hWnd)

	def GetText(self):
		return wndMgr.GetText(self.hWnd)

	def GetTextSize(self):
		return wndMgr.GetTextSize(self.hWnd)

	def GetTextWidth(self):
		w, h = self.GetTextSize()
		return w

	def GetTextHeight(self):
		w, h = self.GetTextSize()
		return h

class MouseReflector(Window):
	def __init__(self, parent):
		Window.__init__(self)
		self.SetParent(parent)
		self.AddFlag("not_pick")
		self.width = self.height = 0
		self.isDown = False

	def Down(self):
		self.isDown = True

	def Up(self):
		self.isDown = False

	def OnRender(self):

		if self.isDown:
			grp.SetColor(WHITE_COLOR)
		else:
			grp.SetColor(HALF_WHITE_COLOR)

		x, y = self.GetGlobalPosition()
		grp.RenderBar(x+2, y+2, self.GetWidth()-4, self.GetHeight()-4)
		
class CheckBox(Window):

	STATE_UNSELECTED = 0
	STATE_SELECTED = 1
	
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.backgroundImage = None
		self.checkImage = None
		self.textInfo = None
	
		self.state = self.STATE_UNSELECTED
		self.eventFunc = None
		self.eventArgs = None

		self.btnBox = {
			self.STATE_UNSELECTED : self.__init_MakeButton("d:/ymir work/ui/game/refine/checkbox.tga"),
			self.STATE_SELECTED : self.__init_MakeButton("d:/ymir work/ui/game/refine/checked.tga", "d:/ymir work/ui/game/refine/checked.tga"),
		}

		text = TextLine()
		text.SetParent(self)
		text.SetWindowVerticalAlignCenter()
		text.SetVerticalAlignCenter()
		text.Show()
		self.text = text

		self.__Refresh()

		self.SetWindowName("CheckBox")

	def __del__(self):
		Window.__del__(self)
		
		self.backgroundImage = None
		self.checkImage = None
		self.textInfo = None

	def CreateElements(self):
		self.backgroundImage = ImageBox()
		self.backgroundImage.SetParent(self)
		self.backgroundImage.AddFlag("not_pick")
		self.backgroundImage.LoadImage("d:/ymir work/ui/game/refine/checkbox.tga")
		self.backgroundImage.Show()

		self.checkImage = ImageBox()
		self.checkImage.SetParent(self)
		self.checkImage.AddFlag("not_pick")
		self.checkImage.SetPosition(0, -4)
		self.checkImage.LoadImage("d:/ymir work/ui/game/refine/checked.tga")
		self.checkImage.Hide()

		self.textInfo = TextLine()
		self.textInfo.SetParent(self)
		self.textInfo.SetPosition(20, -2)
		self.textInfo.Show()

		self.SetSize(self.backgroundImage.GetWidth() + self.textInfo.GetTextSize()[0], self.backgroundImage.GetHeight() + self.textInfo.GetTextSize()[1])

	def SetTextInfo(self, info):
		if self.textInfo:
			self.textInfo.SetText(info)

		#self.SetSize(self.backgroundImage.GetWidth() + self.textInfo.GetTextSize()[0], self.backgroundImage.GetHeight() + self.textInfo.GetTextSize()[1])

	def __ConvertPath(self, path, subStr):
		if path.find("%s") != -1:
			return path % subStr
		else:
			return path

	def __init_MakeButton(self, path, disablePath = None):
		btn = Button()
		btn.SetParent(self)
		btn.SetWindowVerticalAlignCenter()
		btn.SetUpVisual(self.__ConvertPath(path, "01"))
		btn.SetOverVisual(self.__ConvertPath(path, "02"))
		btn.SetDownVisual(self.__ConvertPath(path, "03"))
		if disablePath:
			btn.SetDisableVisual(disablePath)
		else:
			btn.SetDisableVisual(self.__ConvertPath(path, "01"))
		btn.SAFE_SetEvent(self.OnClickButton)
		btn.baseWidth = btn.GetWidth()
		return btn

	def __UpdateRect(self):
		if self.text.GetText():
			width = self.btnBox[self.state].baseWidth + 5 + self.text.GetTextWidth()
		else:
			width = self.btnBox[self.state].baseWidth
		height = max(self.btnBox[self.state].GetHeight(), self.text.GetTextHeight())
		self.SetSize(width, height)

		self.btnBox[self.state].SetSize(width, self.btnBox[self.state].GetHeight())
		self.text.SetPosition(self.btnBox[self.state].baseWidth + 5, 0)

		self.text.UpdateRect()
		self.btnBox[self.state].UpdateRect()
		self.UpdateRect()

	def __Refresh(self):
		self.__UpdateRect()

		self.btnBox[self.STATE_UNSELECTED].SetVisible(self.state == self.STATE_UNSELECTED)
		self.btnBox[self.STATE_SELECTED].SetVisible(self.state == self.STATE_SELECTED)

	def OnClickButton(self):
		if self.state == self.STATE_UNSELECTED:
			self.state = self.STATE_SELECTED
		else:
			self.state = self.STATE_UNSELECTED

		self.__Refresh()

		if self.eventFunc:
			apply(self.eventFunc, self.eventArgs)

	def SetChecked(self, state):
		self.state = state
		self.__Refresh()

	def IsChecked(self):
		return self.state != self.STATE_UNSELECTED


	def SetCheckStatus(self, flag):
		if self.checkImage:
			if self.checkImage.IsShow():
				self.checkImage.Hide()

	def GetCheckStatus(self):
		if self.checkImage:
			return self.checkImage.IsShow()

		return False
				
	def SetText(self, text):
		self.text.SetText(text)
		self.__UpdateRect()

	def SetEvent(self, event, *args):
		self.eventFunc = event
		self.eventArgs = args

	def SetBaseCheckImage(self, image):
		if not self.backgroundImage:
			return
		
		self.backgroundImage.LoadImage(image)

	def SAFE_SetEvent(self, event, *args):
		self.eventFunc = __mem_func__(event)
		self.eventArgs = args

	def Disable(self):
		self.btnBox[self.STATE_UNSELECTED].Disable()
		self.btnBox[self.STATE_SELECTED].Disable()

	def Enable(self):
		self.btnBox[self.STATE_UNSELECTED].Enable()
		self.btnBox[self.STATE_SELECTED].Enable()
		
	def OnMouseLeftButtonUp(self):
		if self.checkImage:
			if self.checkImage.IsShow():
				self.checkImage.Hide()

				if self.eventFunc["ON_UNCKECK"]:
					apply(self.eventFunc["ON_UNCKECK"], self.eventArgs["ON_UNCKECK"])
			else:
				self.checkImage.Show()

				if self.eventFunc["ON_CHECK"]:
					apply(self.eventFunc["ON_CHECK"], self.eventArgs["ON_CHECK"])
	
class EmptyCandidateWindow(Window):
	def __init__(self):
		Window.__init__(self)

	def __del__(self):
		Window.__init__(self)

	def Load(self):
		pass

	def SetCandidatePosition(self, x, y, textCount):
		pass

	def Clear(self):
		pass

	def Append(self, text):
		pass

	def Refresh(self):
		pass

	def Select(self):
		pass

class EditLine(TextLine):
	candidateWindowClassDict = {}

	def __init__(self):
		TextLine.__init__(self)
		if app.ENABLE_GUILD_REQUEST:
			self.infoMsg = ""
			self.backText=None
			self.isNeedEmpty=False
		self.eventReturn = Window.NoneMethod
		self.eventEscape = Window.NoneMethod
		self.eventTab = None
		self.numberMode = False
		self.useIME = True
		self.CanClick = None
		self.bCodePage = False
		if app.ENABLE_GUILD_REQUEST:
			self.infoMsg = ""
			self.backText=None
			self.isNeedEmpty=True
		self.candidateWindowClass = None
		self.candidateWindow = None
		self.SetCodePage(app.GetDefaultCodePage())

		self.readingWnd = ReadingWnd()
		self.readingWnd.Hide()
#PLACEHOLDER
		self.eventUpdate = None

		self.overLay = TextLine()
		self.overLay.SetParent(self)
		self.overLay.SetPosition(0, 0)
		self.overLay.SetPackedFontColor(WHITE_COLOR)
		self.overLay.Hide()
#PLACEHOLDER
		if app.INGAME_WIKI:
			self.eventUpdate = None
			
			self.overLay = TextLine()
			self.overLay.SetParent(self)
			self.overLay.SetPosition(0, 0)
			self.overLay.SetPackedFontColor(WHITE_COLOR)
			self.overLay.Hide()

	def __del__(self):
		TextLine.__del__(self)

		self.eventReturn = Window.NoneMethod
		self.eventEscape = Window.NoneMethod
		self.eventTab = None
		self.CanClick = None

	def SetCodePage(self, codePage):
		candidateWindowClass=EditLine.candidateWindowClassDict.get(codePage, EmptyCandidateWindow)
		self.__SetCandidateClass(candidateWindowClass)

	if app.ENABLE_GUILD_REQUEST:
		def SetInfoMessage(self, msg):
			self.infoMsg = msg
			if self.backText == None:
				self.backText = TextLine()
				self.backText.SetParent(self)
				self.backText.SetPosition(0,0)
				self.backText.SetFontColor(128,128,128)

			self.backText.SetText(msg)

			if self.isNeedEmpty:
				if len(self.GetText()) > 0:
					self.backText.Hide()
				else:
					self.backText.Show()
			else:
				self.backText.Show()

	def __SetCandidateClass(self, candidateWindowClass):
		if self.candidateWindowClass==candidateWindowClass:
			return

		self.candidateWindowClass = candidateWindowClass
		self.candidateWindow = self.candidateWindowClass()
		self.candidateWindow.Load()
		self.candidateWindow.Hide()

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterTextLine(self, layer)

		if app.ENABLE_WINDOW_SLIDE_EFFECT:
			self.SetSpecialWindow()

	def SAFE_SetReturnEvent(self, event):
		self.eventReturn = __mem_func__(event)

	def SetReturnEvent(self, event):
		self.eventReturn = event

	def SetEscapeEvent(self, event):
		self.eventEscape = event

	def SetTabEvent(self, event):
		self.eventTab = event

	def SetSelectEvent(self, event):
		self.eventSelect = event

#PLACEHOLDER
	def SetOverlayText(self, text):
		self.overLay.SetText(text)
		self.__RefreshOverlay()

	def GetOverlayText(self):
		return self.overLay.GetText()

	def GetDisplayText(self):
		if len(self.GetText()):
			return self.GetText()
		else:
			return self.overLay.GetText()

	def __RefreshOverlay(self):
		if len(self.GetText()):
			self.overLay.Hide()
		else:
			self.overLay.Show()
#PLACEHOLDER

	if app.INGAME_WIKI:
		def SetOverlayText(self, text):
			self.overLay.SetText(text)
			self.__RefreshOverlay()
		
		def GetOverlayText(self):
			return self.overLay.GetText()
		
		def SetUpdateEvent(self, event):
			self.eventUpdate = event
		
		def GetDisplayText(self):
			if len(self.GetText()):
				return self.GetText()
			else:
				return self.overLay.GetText()
		
		def __RefreshOverlay(self):
			if len(self.GetText()):
				self.overLay.Hide()
			else:
				self.overLay.Show()
		
		def IsShowCursor(self):
			return wndMgr.IsShowCursor(self.hWnd)

	def SetMax(self, max):
		self.max = max
		wndMgr.SetMax(self.hWnd, self.max)
		ime.SetMax(self.max)
		self.SetUserMax(self.max)

	def SetUserMax(self, max):
		self.userMax = max
		ime.SetUserMax(self.userMax)

	def SetNumberMode(self):
		self.numberMode = True

	#def AddExceptKey(self, key):
	#	ime.AddExceptKey(key)

	#def ClearExceptKey(self):
	#	ime.ClearExceptKey()

	def CanEdit(self, flag):
		self.CanClick = flag

	def SetIMEFlag(self, flag):
		self.useIME = flag

	def SetText(self, text):
		wndMgr.SetText(self.hWnd, text)

		if self.IsFocus():
			ime.SetText(text)
			
		if app.INGAME_WIKI:
			self.__RefreshOverlay()
#PLACEHOLDER
		self.__RefreshOverlay()
#PLACEHOLDER
	def Enable(self):
		wndMgr.ShowCursor(self.hWnd)

	def Disable(self):
		wndMgr.HideCursor(self.hWnd)

	def SetEndPosition(self):
		ime.MoveEnd()

	def OnSetFocus(self):
		Text = self.GetText()
		ime.SetText(Text)
		ime.SetMax(self.max)
		ime.SetUserMax(self.userMax)
		ime.SetCursorPosition(-1)
		if self.numberMode:
			ime.SetNumberMode()
		else:
			ime.SetStringMode()
		ime.EnableCaptureInput()
		if self.useIME:
			ime.EnableIME()
		else:
			ime.DisableIME()
		wndMgr.ShowCursor(self.hWnd, True)

	def OnKillFocus(self):
		self.SetText(ime.GetText(self.bCodePage))
		self.OnIMECloseCandidateList()
		self.OnIMECloseReadingWnd()
		ime.DisableIME()
		ime.DisableCaptureInput()
		wndMgr.HideCursor(self.hWnd)

	def OnIMEChangeCodePage(self):
		self.SetCodePage(ime.GetCodePage())

	def OnIMEOpenCandidateList(self):
		self.candidateWindow.Show()
		self.candidateWindow.Clear()
		self.candidateWindow.Refresh()

		gx, gy = self.GetGlobalPosition()
		self.candidateWindow.SetCandidatePosition(gx, gy, len(self.GetText()))

		return True

	def OnIMECloseCandidateList(self):
		self.candidateWindow.Hide()
		return True

	def OnIMEOpenReadingWnd(self):
		gx, gy = self.GetGlobalPosition()
		textlen = len(self.GetText())-2
		reading = ime.GetReading()
		readinglen = len(reading)
		self.readingWnd.SetReadingPosition( gx + textlen*6-24-readinglen*6, gy )
		self.readingWnd.SetText(reading)
		if ime.GetReadingError() == 0:
			self.readingWnd.SetTextColor(0xffffffff)
		else:
			self.readingWnd.SetTextColor(0xffff0000)
		self.readingWnd.SetSize(readinglen * 6 + 4, 19)
		self.readingWnd.Show()
		return True

	def OnIMECloseReadingWnd(self):
		self.readingWnd.Hide()
		return True

	def OnIMEUpdate(self):
		snd.PlaySound("sound/ui/type.wav")
		TextLine.SetText(self, ime.GetText(self.bCodePage))
		
		if app.ENABLE_GUILD_REQUEST:
			if self.backText:
				if self.isNeedEmpty:
					if len(self.GetText()) > 0:
						self.backText.Hide()
					else:
						self.backText.Show()
				else:
					self.backText.Show()		
#PLACEHOLDER
		self.__RefreshOverlay()

		if self.eventUpdate:
			self.eventUpdate()
#PLACEHOLDER
		if app.INGAME_WIKI:
			self.__RefreshOverlay()
			
			if self.eventUpdate:
				self.eventUpdate()


	def OnIMETab(self):
		if self.eventTab:
			self.eventTab()
			return True

		return False

	def OnIMEReturn(self):
		snd.PlaySound("sound/ui/click.wav")
		self.eventReturn()

		return True

	def OnPressEscapeKey(self):
		self.eventEscape()
		return True

	def OnKeyDown(self, key):
		if app.DIK_F1 == key:
			return False
		if app.DIK_F2 == key:
			return False
		if app.DIK_F3 == key:
			return False
		if app.DIK_F4 == key:
			return False
		if app.DIK_LALT == key:
			return False
		if app.DIK_SYSRQ == key:
			return False
		if app.DIK_LCONTROL == key:
			return False
		if app.DIK_V == key:
			if app.IsPressed(app.DIK_LCONTROL):
				ime.PasteTextFromClipBoard()

		return True

	def OnKeyUp(self, key):
		if app.DIK_F1 == key:
			return False
		if app.DIK_F2 == key:
			return False
		if app.DIK_F3 == key:
			return False
		if app.DIK_F4 == key:
			return False
		if app.DIK_LALT == key:
			return False
		if app.DIK_SYSRQ == key:
			return False
		if app.DIK_LCONTROL == key:
			return False

		return True

	def OnIMEKeyDown(self, key):
		# Left
		if app.VK_LEFT == key:
			ime.MoveLeft()
			return True
		# Right
		if app.VK_RIGHT == key:
			ime.MoveRight()
			return True

		# Home
		if app.VK_HOME == key:
			ime.MoveHome()
			return True
		# End
		if app.VK_END == key:
			ime.MoveEnd()
			return True

		# Delete
		if app.VK_DELETE == key:
			ime.Delete()
			TextLine.SetText(self, ime.GetText(self.bCodePage))
			return True

		return True

	#def OnMouseLeftButtonDown(self):
	#	self.SetFocus()
	def OnMouseLeftButtonDown(self):
		if False == self.IsIn():
			return False

		if False == self.CanClick:
			return False

		self.SetFocus()
		PixelPosition = wndMgr.GetCursorPosition(self.hWnd)
		ime.SetCursorPosition(PixelPosition)

class MarkBox(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterMarkBox(self, layer)

		if app.ENABLE_WINDOW_SLIDE_EFFECT:
			self.SetSpecialWindow()

	def Load(self):
		wndMgr.MarkBox_Load(self.hWnd)

	def SetScale(self, scale):
		wndMgr.MarkBox_SetScale(self.hWnd, scale)

	def SetIndex(self, guildID):
		MarkID = guild.GuildIDToMarkID(guildID)
		wndMgr.MarkBox_SetImageFilename(self.hWnd, guild.GetMarkImageFilenameByMarkID(MarkID))
		wndMgr.MarkBox_SetIndex(self.hWnd, guild.GetMarkIndexByMarkID(MarkID))

	def SetAlpha(self, alpha):
		wndMgr.MarkBox_SetDiffuseColor(self.hWnd, 1.0, 1.0, 1.0, alpha)


if app.ENABLE_OFFLINE_SHOP_SYSTEM:
	class ImageBoxPrivateShop(Window):
		def __init__(self, layer = "UI"):
			Window.__init__(self, layer)

			self.name=""
			self.eventDict={}
			self.argDict={}
			
			self.eventFunc = {"mouse_click" : None, "MOUSE_OVER_IN" : None, "MOUSE_OVER_OUT" : None}
			self.eventArgs = {"mouse_click" : None, "MOUSE_OVER_IN" : None, "MOUSE_OVER_OUT" : None}
			
			self.ToolTipText = None

		def __del__(self):
			Window.__del__(self)
			self.eventFunc = None
			self.eventArgs = None

		def RegisterWindow(self, layer):
			self.hWnd = wndMgr.RegisterImageBox(self, layer)

			if app.ENABLE_WINDOW_SLIDE_EFFECT:
				self.SetSpecialWindow()

		def LoadImage(self, imageName):
			self.name=imageName
			wndMgr.LoadImage(self.hWnd, imageName)

			if len(self.eventDict)!=0:
				print "LOAD IMAGE", self, self.eventDict

		def GetImageName(self):
			return self.name

		def SetAlpha(self, alpha):
			wndMgr.SetDiffuseColor(self.hWnd, 1.0, 1.0, 1.0, alpha)

		def GetWidth(self):
			return wndMgr.GetWidth(self.hWnd)

		def GetHeight(self):
			return wndMgr.GetHeight(self.hWnd)

		def ForceRender(self):
			wndMgr.ImageForceRender(self.hWnd)

		def SetFormToolTipText(self, type, text, x, y):
			if not self.ToolTipText:
				toolTip=createToolTipWindowDict[type]()
				toolTip.SetParent(self)
				toolTip.SetSize(0, 0)
				toolTip.SetHorizontalAlignCenter()
				toolTip.SetOutline()
				toolTip.Hide()
				toolTip.SetPosition(x + self.GetWidth()/2, y)
				self.ToolTipText=toolTip

			self.ToolTipText.SetText(text)

		def SetToolTipWindow(self, toolTip):		
			self.ToolTipText=toolTip		
			self.ToolTipText.SetParentProxy(self)

		def SetToolTipText(self, text, x=0, y = -19):
			self.SetFormToolTipText("TEXT", text, x, y)

		def CallEvent(self):
			snd.PlaySound("sound/ui/click.wav")

			if self.eventFunc:
				apply(self.eventFunc, self.eventArgs)

		def ShowToolTip(self):
			if self.ToolTipText:
				self.ToolTipText.Show()

		def HideToolTip(self):
			if self.ToolTipText:
				self.ToolTipText.Hide()

		def OnMouseOverIn(self):
			try:
				apply(self.eventDict["MOUSE_OVER_IN"], self.argDict["MOUSE_OVER_IN"])
			except KeyError:
				pass

		def OnMouseOverOut(self):
			try:
				apply(self.eventDict["MOUSE_OVER_OUT"], self.argDict["MOUSE_OVER_OUT"])
			except KeyError:
				pass
				
		def SetEvent(self, func, *args) :
			result = self.eventFunc.has_key(args[0])		
			if result :
				self.eventFunc[args[0]] = func
				self.eventArgs[args[0]] = args
			else :
				print "[ERROR] ui.py SetEvent, Can`t Find has_key : %s" % args[0]

		def OnMouseLeftButtonUp(self):
			try:
				apply(self.eventDict["MOUSE_LEFT_UP"], self.argDict["MOUSE_LEFT_UP"])
			except KeyError:
				pass

		def OnMouseLeftButtonDown(self):
			try:
				apply(self.eventDict["MOUSE_LEFT_DOWN"], self.argDict["MOUSE_LEFT_DOWN"])
			except KeyError:
				pass

		def SAFE_SetStringEvent(self, event, func, *args):
			self.eventDict[event]=__mem_func__(func)
			self.argDict[event]=args

		def SetStringEvent(self, event, func, *args):
			self.eventDict[event]=func
			self.argDict[event]=args

		def SAFE_SetMouseClickEvent(self, func, *args):
			self.eventDict["MOUSE_LEFT_DOWN"]=__mem_func__(func)
			self.argDict["MOUSE_LEFT_DOWN"]=args

class ImageBox(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		self.eventDict={}
		self.argDict={}
		self.eventFunc = {}
		self.eventArgs = {}
		
		if app.ENABLE_NEW_FISHING_SYSTEM:
			self.onMouseLeftButtonUpEvent = None

	def __del__(self):
		Window.__del__(self)
		if app.BL_MAILBOX:
			self.eventFunc = None
			self.eventArgs = None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterImageBox(self, layer)

		if app.ENABLE_WINDOW_SLIDE_EFFECT:
			self.SetSpecialWindow()

	def LoadImage(self, imageName):
		self.name=imageName
		wndMgr.LoadImage(self.hWnd, imageName)

	if app.INGAME_WIKI:
		def UnloadImage(self):
			wndMgr.UnloadImage(self.hWnd)
	
	def SetToolTipThinText(self, text, x=0, y = -19):
		self.SetFormToolTipText("TEXT", text, x, y)	
	
	def SetCoolTime(self, time):
		wndMgr.SetCoolTimeImageBox(self.hWnd, time)

	def SetStartCoolTime(self, time):
		wndMgr.SetStartCoolTimeImageBox(self.hWnd, time)

	def	SetCoolTimeInverse(self, flag):
		wndMgr.SetCoolTimeInverseImageBox(self.hWnd, flag)

	def	SetCoolTimeInvert(self, flag):
		wndMgr.SetCoolTimeInvertImageBox(self.hWnd, flag)

	def SetRectCircle(self, percent = 1.0):
		wndMgr.SetRectCircle(self.hWnd, percent)

	def SetAlpha(self, alpha):
		wndMgr.SetDiffuseColor(self.hWnd, 1.0, 1.0, 1.0, alpha)

	def GetWidth(self):
		return wndMgr.GetWidth(self.hWnd)

	def GetHeight(self):
		return wndMgr.GetHeight(self.hWnd)

	if app.INGAME_WIKI:
		def OnMouseOverIn(self):
			self.__OnMouseOverIn()

		def OnMouseOverOut(self):
			self.__OnMouseOverOut()

		def __OnMouseOverIn(self):
			try:
				apply(self.eventDict["MOUSE_OVER_IN"], self.argDict["MOUSE_OVER_IN"])
			except KeyError:
				pass

		def __OnMouseOverOut(self):
			try:
				apply(self.eventDict["MOUSE_OVER_OUT"], self.argDict["MOUSE_OVER_OUT"])
			except KeyError:
				pass

		def OnMouseLeftButtonDown(self):
			if self.eventDict.has_key("MOUSE_LEFT_DOWN"):
				apply(self.eventDict["MOUSE_LEFT_DOWN"], self.argDict["MOUSE_LEFT_DOWN"])
	else:
		def OnMouseOverIn(self):
			try:
				self.eventDict["MOUSE_OVER_IN"]()
			except KeyError:
				pass

		def OnMouseOverOut(self):
			try:
				self.eventDict["MOUSE_OVER_OUT"]()
			except KeyError:
				pass

	if app.BL_MAILBOX:
		def SetEvent(self, func, *args) :
			result = self.eventFunc.has_key(args[0])		
			if result :
				self.eventFunc[args[0]] = func
				self.eventArgs[args[0]] = args
			else :
				print "[ERROR] ui.py SetEvent, Can`t Find has_key : %s" % args[0]

		def OnMouseLeftButtonUp(self) :
			if self.eventFunc["mouse_click"] :
				apply(self.eventFunc["mouse_click"], self.eventArgs["mouse_click"])

		def OnMouseOverIn(self) :
			if self.eventFunc["mouse_over_in"] :
				apply(self.eventFunc["mouse_over_in"], self.eventArgs["mouse_over_in"])
			else:
				try:
					self.eventDict["MOUSE_OVER_IN"]()
				except KeyError:
					pass

		def OnMouseOverOut(self) :
			if self.eventFunc["mouse_over_out"] :
				apply(self.eventFunc["mouse_over_out"], self.eventArgs["mouse_over_out"])
			else :
				try:
					self.eventDict["MOUSE_OVER_OUT"]()
				except KeyError:
					pass

	def SAFE_SetStringEvent(self, event, func, *args):
		self.eventFunc[event]=__mem_func__(func)
		self.eventArgs[event]=args

	def SetStringEvent(self, event, func, *args):
		self.eventDict[event]=func
		self.argDict[event]=args

	def SetStringEventIntro(self, func, event, *args):
		self.eventDict[event]=func
		self.argDict[event]=args

	if app.ENABLE_NEW_FISHING_SYSTEM:
		def SetMouseLeftButtonUp(self, event):
			self.onMouseLeftButtonUpEvent = event

		def OnMouseLeftButtonUp(self):
			try:
				apply(self.eventDict["MOUSE_LEFT_UP"], self.argDict["MOUSE_LEFT_UP"])
			except KeyError:
				if self.onMouseLeftButtonUpEvent != None:
					self.onMouseLeftButtonUpEvent()


	def SetEvent(self, func, *args) :
		self.eventFunc[args[0]] = func
		self.eventArgs[args[0]] = args

	def OnMouseLeftButtonUp(self):
		try:
			if self.eventFunc.has_key("mouse_click"):
				if self.eventArgs.has_key("mouse_click"):
					apply(self.eventFunc["mouse_click"], self.eventArgs["mouse_click"])
				else:
					self.eventFunc["mouse_click"]()
		except:
			pass

	def OnMouseOverIn(self) :
		try:
			if self.eventFunc.has_key("MOUSE_OVER_IN"):
				if self.eventArgs.has_key("MOUSE_OVER_IN"):
					apply(self.eventFunc["MOUSE_OVER_IN"], self.eventArgs["MOUSE_OVER_IN"])
				else:
					self.eventFunc["MOUSE_OVER_IN"]()
		except:
			pass
		
	def OnMouseOverOut(self) :
		try:
			if self.eventFunc.has_key("MOUSE_OVER_OUT"):
				if self.eventArgs.has_key("MOUSE_OVER_OUT"):
					apply(self.eventFunc["MOUSE_OVER_OUT"], self.eventArgs["MOUSE_OVER_OUT"])
				else:
					self.eventFunc["MOUSE_OVER_OUT"]()
		except:
			pass

class ExpandedImageBox(ImageBox):
	def __init__(self, layer = "UI"):
		ImageBox.__init__(self, layer)
		self.eventFunc = None
		self.eventArgs = None
	
	def __del__(self):
		ImageBox.__del__(self)
		self.eventFunc = None
		self.eventArgs = None

	def OnMouseLeftButtonUp(self):
		if self.eventFunc:
			apply(self.eventFunc, self.eventArgs)

	def SAFE_SetEvent(self, func, *args):
		self.eventFunc = __mem_func__(func)
		self.eventArgs = args

	def SetEvent(self, func, *args):
		self.eventFunc = func
		self.eventArgs = args

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterExpandedImageBox(self, layer)

		if app.ENABLE_WINDOW_SLIDE_EFFECT:
			self.SetSpecialWindow()

	def SetScale(self, xScale, yScale):
		wndMgr.SetScale(self.hWnd, xScale, yScale)

	def SetOrigin(self, x, y):
		wndMgr.SetOrigin(self.hWnd, x, y)

	def SetRotation(self, rotation):
		wndMgr.SetRotation(self.hWnd, rotation)

	def SetRenderingMode(self, mode):
		wndMgr.SetRenderingMode(self.hWnd, mode)

	def SetRenderingRect(self, left, top, right, bottom):
		wndMgr.SetRenderingRect(self.hWnd, left, top, right, bottom)

	def SetClipRect(self, left, top, right, bottom, isVertical = False):
		wndMgr.SetClipRect(self.hWnd, left, top, right, bottom, isVertical)

	def SetPercentage(self, curValue, maxValue):
		if maxValue:
			self.SetRenderingRect(0.0, 0.0, -1.0 + float(curValue) / float(maxValue), 0.0)
		else:
			self.SetRenderingRect(0.0, 0.0, 0.0, 0.0)

	def SetPercentageEx(self, minValue, curValue, maxValue):
		if minValue and maxValue:
			self.SetRenderingRect(0.0, 0.0, -1.0 + (float(curValue) - float(minValue)) / (float(maxValue) - float(minValue)), 0.0)
		else:
			self.SetRenderingRect(0.0, 0.0, 0.0, 0.0)


	def GetWidth(self):
		return wndMgr.GetWindowWidth(self.hWnd)

	def GetHeight(self):
		return wndMgr.GetWindowHeight(self.hWnd)

	def SetOnMouseLeftButtonUpEvent(self, event, *args):
		self.eventFunc = event
		self.eventArgs = args

	if app.ENABLE_NEW_FISHING_SYSTEM:
		def SetImageDiffuseColor(self, r, g, b, a):
			wndMgr.SetDiffuseColor(self.hWnd, r, g, b, a)

class AniImage(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.endFrameEvent = None
		self.endFrameArgs = None
		
		# if app.ENABLE_FISH_EVENT:
		self.end_frame_event = None
		self.keyFrameEvent = None

	def SetScale(self, xScale, yScale):
		wndMgr.SetScale(self.hWnd, xScale, yScale)
		
	def __del__(self):
		Window.__del__(self)
		
		self.endFrameEvent = None
		self.endFrameArgs = None
		
		# if app.ENABLE_FISH_EVENT:
		self.end_frame_event = None
		self.keyFrameEvent = None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterAniImageBox(self, layer)

		if app.ENABLE_WINDOW_SLIDE_EFFECT:
			self.SetSpecialWindow()

	def SetDelay(self, delay):
		wndMgr.SetDelay(self.hWnd, delay)

	if app.BL_MAILBOX:
		def ResetFrame(self):
			wndMgr.ResetFrame(self.hWnd)

	def AppendImage(self, image, xs = 0, ys = 0):
		wndMgr.AppendImage(self.hWnd, image, xs, ys)

	def SetPercentage(self, curValue, maxValue):
		wndMgr.SetRenderingRect(self.hWnd, 0.0, 0.0, -1.0 + float(curValue) / float(maxValue), 0.0)

	def ResetFrame(self):
		wndMgr.ResetFrame(self.hWnd)
		
	def SetEndFrameEvent(self, event, *args):
		self.endFrameEvent = event
		self.endFrameArgs = args
	
	def SetOnEndFrame(self, event):
		self.eventEndFrame = event
		
	def OnEndFrame(self):
		if self.endFrameEvent:
			apply(self.endFrameEvent, self.endFrameArgs)
			
	def SetKeyFrameEvent(self, event):
		self.keyFrameEvent = event
	
	def OnKeyFrame(self, curFrame):
		if self.keyFrameEvent:
			self.keyFrameEvent(curFrame)
	
	if app.ENABLE_NEW_FISHING_SYSTEM:
		def SetRotation(self, r):
			wndMgr.AniSetRotation(self.hWnd, r)

class AniImageBox(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.endFrameEvent = None
		self.endFrameArgs = None
		
		# if app.ENABLE_FISH_EVENT:
		self.end_frame_event = None
		self.keyFrameEvent = None

	def SetScale(self, xScale, yScale):
		wndMgr.SetScale(self.hWnd, xScale, yScale)
		
	def __del__(self):
		Window.__del__(self)
		
		self.endFrameEvent = None
		self.endFrameArgs = None
		
		# if app.ENABLE_FISH_EVENT:
		self.end_frame_event = None
		self.keyFrameEvent = None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterAniImageBox(self, layer)

		if app.ENABLE_WINDOW_SLIDE_EFFECT:
			self.SetSpecialWindow()

	def SetDelay(self, delay):
		wndMgr.SetDelay(self.hWnd, delay)

	if app.BL_MAILBOX:
		def ResetFrame(self):
			wndMgr.ResetFrame(self.hWnd)

	def AppendImage(self, image, xs = 0, ys = 0):
		wndMgr.AppendImage(self.hWnd, image, xs, ys)

	def AppendImageScale(self, filename, scale_x, scale_y):
		wndMgr.AppendImageScale(self.hWnd, filename, scale_x, scale_y)

	def SetPercentage(self, curValue, maxValue):
		wndMgr.SetRenderingRect(self.hWnd, 0.0, 0.0, -1.0 + float(curValue) / float(maxValue), 0.0)

	def ResetFrame(self):
		wndMgr.ResetFrame(self.hWnd)
		
	def SetEndFrameEvent(self, event, *args):
		self.endFrameEvent = event
		self.endFrameArgs = args
	
	def SetOnEndFrame(self, event):
		self.eventEndFrame = event
		
	def OnEndFrame(self):
		if self.endFrameEvent:
			apply(self.endFrameEvent, self.endFrameArgs)
			
	def SetKeyFrameEvent(self, event):
		self.keyFrameEvent = event
	
	def OnKeyFrame(self, curFrame):
		if self.keyFrameEvent:
			self.keyFrameEvent(curFrame)
	
	def SetRotation(self, rotation):
		wndMgr.SetRotationAni(self.hWnd, rotation)

	if app.ENABLE_NEW_FISHING_SYSTEM:
		def SetRotation(self, r):
			wndMgr.AniSetRotation(self.hWnd, r)
	
class CheckBox2(Window):
	def __init__(self):
		Window.__init__(self)
		
		self.backgroundImage = None
		self.checkImage = None

		self.eventFunc = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
		self.eventArgs = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
	
		self.CreateElements()
		
	def __del__(self):
		Window.__del__(self)
		
		self.backgroundImage = None
		self.checkImage = None
		
		self.eventFunc = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
		self.eventArgs = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
		
	def CreateElements(self):
		self.backgroundImage = ImageBox()
		self.backgroundImage.SetParent(self)
		self.backgroundImage.AddFlag("not_pick")
		self.backgroundImage.LoadImage("d:/ymir work/ui/game/refine/checkbox.tga")
		self.backgroundImage.Show()
		
		self.checkImage = ImageBox()
		self.checkImage.SetParent(self)
		self.checkImage.AddFlag("not_pick")
		self.checkImage.SetPosition(0, -4)
		self.checkImage.LoadImage("d:/ymir work/ui/game/refine/checked.tga")
		self.checkImage.Hide()
		
		self.textInfo = TextLine()
		self.textInfo.SetParent(self)
		self.textInfo.SetPosition(20, -2)
		self.textInfo.Show()
		
		self.SetSize(self.backgroundImage.GetWidth() + self.textInfo.GetTextSize()[0], self.backgroundImage.GetHeight() + self.textInfo.GetTextSize()[1])
		
	def SetTextInfo(self, info):
		if self.textInfo:
			self.textInfo.SetText(info)
			
		self.SetSize(self.backgroundImage.GetWidth() + self.textInfo.GetTextSize()[0], self.backgroundImage.GetHeight() + self.textInfo.GetTextSize()[1])
		
	def SetCheckStatus(self, flag):
		if flag or systemSetting.IsRefineShow():
			constInfo.IS_AUTO_REFINE = True
			self.checkImage.Show()
		else:
			self.checkImage.Hide()
	
	def GetCheckStatus(self):
		if self.checkImage:
			return self.checkImage.IsShow()
			
		return False
		
	def SetEvent(self, func, *args) :
		result = self.eventFunc.has_key(args[0])		
		if result :
			self.eventFunc[args[0]] = func
			self.eventArgs[args[0]] = args
		else :
			print "[ERROR] ui.py SetEvent, Can`t Find has_key : %s" % args[0]
		
	def OnMouseLeftButtonUp(self):
		if self.checkImage:
			if self.checkImage.IsShow():
				self.checkImage.Hide()

				if self.eventFunc["ON_UNCKECK"]:
					apply(self.eventFunc["ON_UNCKECK"], self.eventArgs["ON_UNCKECK"])
					systemSetting.SetRefineStatus(False)
			else:
				self.checkImage.Show()

				if self.eventFunc["ON_CHECK"]:
					apply(self.eventFunc["ON_CHECK"], self.eventArgs["ON_CHECK"])
					systemSetting.SetRefineStatus(True)

if app.ENABLE_NEW_FISHING_SYSTEM:
	class FishBox(Window):
		def __init__(self, layer = "UI"):
			Window.__init__(self, layer)
			fishIcon = AniImageBox()
			fishIcon.SetParent(self)
			fishIcon.SetSize(30, 30)
			fishIcon.SetPosition(0, 0)
			for i in xrange(4):
				fishIcon.AppendImage("d:/ymir work/ui/game/fishing/fish/fishing_fish_%d.sub" % (i + 1), 1.0, 1.0)
			fishIcon.Show()
			self.fishIcon = fishIcon
			self.rotation = 0.0

			self.end_move_event = None

		def __del__(self):
			Window.__del__(self)
			self.end_move_event = None

		def RegisterWindow(self, layer):
			self.hWnd = wndMgr.RegisterFishBox(self, layer)

		def MoveStart(self):
			wndMgr.FishMoveStart(self.hWnd)

		def MoveStop(self):
			wndMgr.FishMoveStop(self.hWnd)

		def GetMove(self):
			return wndMgr.FishGetMove(self.hWnd)

		def SetEndMoveEvent(self, event):
			self.end_move_event = event

		def OnEndMove(self):
			if self.end_move_event:
				self.end_move_event()

		def GetPosition(self):
			return wndMgr.FishGetPosition(self.hWnd)

		def OnRotation(self, r):
			if self.rotation != r:
				self.rotation = r
				self.fishIcon.SetRotation(r)

class Button(Window):
##GM Online Board Extension
	def GetText(self):
		if not self.ButtonText:
			return# ""
		return self.ButtonText.GetText()

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.eventFunc = None
		self.eventArgs = None

		self.ButtonText = None
		self.ToolTipText = None
		self.overFunc = None
		self.overArgs = None
		self.overOutFunc = None
		self.overOutArgs = None

	def __del__(self):
		Window.__del__(self)

		self.eventFunc = None
		self.eventArgs = None
		self.overFunc = None
		self.overArgs = None
		self.overOutFunc = None
		self.overOutArgs = None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterButton(self, layer)

		if app.ENABLE_WINDOW_SLIDE_EFFECT:
			self.SetSpecialWindow()

	if app.ENABLE_NEW_GAMEOPTION:
		def SetRenderingRect(self, left, top, right, bottom):
			wndMgr.SetRenderingRect(self.hWnd, left, top, right, bottom)

	def SetUpVisual(self, filename):
		wndMgr.SetUpVisual(self.hWnd, filename)

	def SetOverVisual(self, filename):
		wndMgr.SetOverVisual(self.hWnd, filename)

	def SetDownVisual(self, filename):
		wndMgr.SetDownVisual(self.hWnd, filename)

	def SetDisableVisual(self, filename):
		wndMgr.SetDisableVisual(self.hWnd, filename)

	def GetUpVisualFileName(self):
		return wndMgr.GetUpVisualFileName(self.hWnd)

	def GetOverVisualFileName(self):
		return wndMgr.GetOverVisualFileName(self.hWnd)

	def GetDownVisualFileName(self):
		return wndMgr.GetDownVisualFileName(self.hWnd)

	def Flash(self):
		wndMgr.Flash(self.hWnd)

	def FlashEx(self):
		wndMgr.FlashEx(self.hWnd)


	def EnableFlash(self):
		wndMgr.EnableFlash(self.hWnd)

	def DisableFlash(self):
		wndMgr.DisableFlash(self.hWnd)

	def Enable(self):
		wndMgr.Enable(self.hWnd)

	def Disable(self):
		wndMgr.Disable(self.hWnd)

	def Down(self):
		wndMgr.Down(self.hWnd)

	def SetUp(self):
		wndMgr.SetUp(self.hWnd)

	def SAFE_SetEvent(self, func, *args):
		self.eventFunc = __mem_func__(func)
		self.eventArgs = args

	def SetEvent(self, func, *args):
		self.eventFunc = func
		self.eventArgs = args

	def SetTextColor(self, color):
		if not self.ButtonText:
			return
		self.ButtonText.SetPackedFontColor(color)

	def SetTextAddPos(self, text, x_add = 0, y_add = 0, height = 4):
		if not self.ButtonText:
			textLine = TextLine()
			textLine.SetParent(self)
			textLine.SetPosition(self.GetWidth() / 2 + x_add, self.GetHeight() / 2 + y_add)
			textLine.SetVerticalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.Show()
			self.ButtonText = textLine
		self.ButtonText.SetText(text)

	def SetText(self, text, height = 4):

		if not self.ButtonText:
			textLine = TextLine()
			textLine.SetParent(self)
			textLine.SetPosition(self.GetWidth()/2, self.GetHeight()/2)
			textLine.SetVerticalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.Show()
			self.ButtonText = textLine

		self.ButtonText.SetText(text)

	if constInfo.EXTRA_UI_FEATURE:
		def GetText(self):
			if not self.ButtonText:
				return ""
			return self.ButtonText.GetText()

	def SetFormToolTipText(self, type, text, x, y):
		if not self.ToolTipText:
			toolTip=createToolTipWindowDict[type]()
			toolTip.SetParent(self)
			toolTip.SetSize(0, 0)
			toolTip.SetHorizontalAlignCenter()
			toolTip.SetOutline()
			toolTip.Hide()
			toolTip.SetPosition(x + self.GetWidth()/2, y)
			self.ToolTipText=toolTip

		self.ToolTipText.SetText(text)

	def SetToolTipWindow(self, toolTip):
		self.ToolTipText=toolTip
		self.ToolTipText.SetParentProxy(self)

	def SetToolTipText(self, text, x=0, y = -19):
		self.SetFormToolTipText("TEXT", text, x, y)

	def CallEvent(self):
		snd.PlaySound("sound/ui/click.wav")

		if self.eventFunc:
			apply(self.eventFunc, self.eventArgs)

	def ShowToolTip(self):
		if self.overFunc:
			apply(self.overFunc, self.overArgs )
		if self.ToolTipText:
			self.ToolTipText.Show()

	def HideToolTip(self):
		if self.overOutFunc:
			apply(self.overOutFunc, self.overOutArgs )
		if self.ToolTipText:
			self.ToolTipText.Hide()

	def IsDown(self):
		return wndMgr.IsDown(self.hWnd)
	
	if app.ENABLE_NEW_GAMEOPTION:
		def SetListText(self, text, x = 8):
			if not self.ButtonText:
				textLine = TextLine()
				textLine.SetParent(self)
				textLine.SetPosition(x, self.GetHeight()/2)
				textLine.SetVerticalAlignCenter()
				textLine.SetHorizontalAlignLeft()
				textLine.Show()
				self.ButtonText = textLine
			self.ButtonText.SetText(text)
	
	if app.ENABLE_QUEST_RENEWAL:
		def GetText(self):
			if not self.ButtonText:
				return ""

			return self.ButtonText.GetText()

		def SetTextAlignLeft(self, text, height = 4):
			if not self.ButtonText:
				textLine = TextLine()
				textLine.SetParent(self)
				textLine.SetPosition(27, self.GetHeight()/2)
				textLine.SetVerticalAlignCenter()
				textLine.SetHorizontalAlignLeft()
				textLine.Show()
				self.ButtonText = textLine

			#����Ʈ ����Ʈ UI�� ���� ��ġ ����
			self.ButtonText.SetText(text)
			self.ButtonText.SetPosition(27, self.GetHeight()/2)
			self.ButtonText.SetVerticalAlignCenter()
			self.ButtonText.SetHorizontalAlignLeft()

	def OnMouseOverIn(self):
		if self.overFunc:
			apply(self.overFunc, self.overArgs )

	def OnMouseOverOut(self):
		if self.overOutFunc:
			apply(self.overOutFunc, self.overOutArgs )
	def SetOverEvent(self, func, *args):
		self.overFunc = func
		self.overArgs = args
	def SetOverOutEvent(self, func, *args):
		self.overOutFunc = func
		self.overOutArgs = args

	def SetAlpha(self, alpha):
		self.SetButtonColor(1.0,1.0,1.0,alpha)

	def SetButtonColorRGB(self, r, g, b, alpha):
		self.buttonColorR = float(r)/255.0
		self.buttonColorG = float(g)/255.0
		self.buttonColorB = float(b)/255.0
		self.buttonColorA = alpha

		wndMgr.SetButtonColor(self.hWnd, float(r)/255.0, float(g)/255.0, float(b)/255.0, alpha)

	def SetButtonColor(self, r, g, b, alpha):
		self.buttonColorR = r
		self.buttonColorG = g
		self.buttonColorB = b
		self.buttonColorA = alpha

		wndMgr.SetButtonColor(self.hWnd, r, g, b, alpha)

	def GetButtonColor(self):
		return self.buttonColorR, self.buttonColorG, self.buttonColorB, self.buttonColorA

class RadioButton(Button):
	def __init__(self):
		Button.__init__(self)

	def __del__(self):
		Button.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterRadioButton(self, layer)

class RadioButtonGroup:
	def __init__(self):
		self.buttonGroup = []
		self.selectedBtnIdx = -1

	def __del__(self):
		for button, ue, de in self.buttonGroup:
			button.__del__()

	def Show(self):
		for (button, selectEvent, unselectEvent) in self.buttonGroup:
			button.Show()

	def Hide(self):
		for (button, selectEvent, unselectEvent) in self.buttonGroup:
			button.Hide()

	def SetText(self, idx, text):
		if idx >= len(self.buttonGroup):
			return
		(button, selectEvent, unselectEvent) = self.buttonGroup[idx]
		button.SetText(text)

	def OnClick(self, btnIdx):
		if btnIdx == self.selectedBtnIdx:
			return
		(button, selectEvent, unselectEvent) = self.buttonGroup[self.selectedBtnIdx]
		if unselectEvent:
			unselectEvent()
		button.SetUp()

		self.selectedBtnIdx = btnIdx
		(button, selectEvent, unselectEvent) = self.buttonGroup[btnIdx]
		if selectEvent:
			selectEvent()

		button.Down()

	def AddButton(self, button, selectEvent, unselectEvent):
		i = len(self.buttonGroup)
		button.SetEvent(lambda : self.OnClick(i))
		self.buttonGroup.append([button, selectEvent, unselectEvent])
		button.SetUp()

	def Create(rawButtonGroup):
		radioGroup = RadioButtonGroup()
		for (button, selectEvent, unselectEvent) in rawButtonGroup:
			radioGroup.AddButton(button, selectEvent, unselectEvent)

		radioGroup.OnClick(0)

		return radioGroup

	Create=staticmethod(Create)

class ToggleButton(Button):
    def __init__(self):
        Button.__init__(self)

        self.eventUp = None
        self.eventDown = None

        self.eventUpArgs = None
        self.eventDownArgs = None

    def __del__(self):
        Button.__del__(self)

        self.eventUp = None
        self.eventDown = None

    def SetToggleUpEvent(self, event, *args):
        self.eventUp = event
        self.eventUpArgs = args

    def SetToggleDownEvent(self, event, *args):
        self.eventDown = event
        self.eventDownArgs = args

    def RegisterWindow(self, layer):
        self.hWnd = wndMgr.RegisterToggleButton(self, layer)

    def OnToggleUp(self):
        if self.eventUp:
            if self.eventUpArgs:
                apply(self.eventUp, self.eventUpArgs)
            else:
                self.eventUp()

    def OnToggleDown(self):
        if self.eventDown:
            if self.eventDownArgs:
                apply(self.eventDown, self.eventDownArgs)
            else:
                self.eventDown()

class DragButton(Button):
	def __init__(self):
		Button.__init__(self)
		self.AddFlag("movable")

		self.callbackEnable = True
		self.eventMove = lambda: None

	def __del__(self):
		Button.__del__(self)

		self.eventMove = lambda: None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterDragButton(self, layer)

	def SetMoveEvent(self, event):
		self.eventMove = event

	def SetRestrictMovementArea(self, x, y, width, height):
		wndMgr.SetRestrictMovementArea(self.hWnd, x, y, width, height)

	def TurnOnCallBack(self):
		self.callbackEnable = True

	def TurnOffCallBack(self):
		self.callbackEnable = False

	def OnMove(self):
		if self.callbackEnable:
			self.eventMove()

class NumberLine(Window):

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterNumberLine(self, layer)

	def SetHorizontalAlignCenter(self):
		wndMgr.SetNumberHorizontalAlignCenter(self.hWnd)

	def SetHorizontalAlignRight(self):
		wndMgr.SetNumberHorizontalAlignRight(self.hWnd)

	def SetPath(self, path):
		wndMgr.SetPath(self.hWnd, path)

	def SetNumber(self, number):
		wndMgr.SetNumber(self.hWnd, number)

###################################################################################################
## PythonScript Element
###################################################################################################

class Box(Window):

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBox(self, layer)

	def SetColor(self, color):
		wndMgr.SetColor(self.hWnd, color)

class Bar(Window):

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBar(self, layer)

	def SetColor(self, color):
		wndMgr.SetColor(self.hWnd, color)

class Line(Window):

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterLine(self, layer)

	def SetColor(self, color):
		wndMgr.SetColor(self.hWnd, color)

class SlotBar(Window):

	def __init__(self):
		Window.__init__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBar3D(self, layer)

## Same with SlotBar
class Bar3D(Window):

	def __init__(self):
		Window.__init__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBar3D(self, layer)

	def SetColor(self, left, right, center):
		wndMgr.SetColor(self.hWnd, left, right, center)

class SlotWindow(Window):

	def __init__(self):
		Window.__init__(self)

		self.StartIndex = 0

		self.eventSelectEmptySlot = None
		self.eventSelectItemSlot = None
		self.eventUnselectEmptySlot = None
		self.eventUnselectItemSlot = None
		self.eventUseSlot = None
		self.eventOverInItem = None
		self.eventOverOutItem = None
		self.eventPressedSlotButton = None
	

	def __del__(self):
		Window.__del__(self)

		self.eventSelectEmptySlot = None
		self.eventSelectItemSlot = None
		self.eventUnselectEmptySlot = None
		self.eventUnselectItemSlot = None
		self.eventUseSlot = None
		self.eventOverInItem = None
		self.eventOverOutItem = None
		self.eventPressedSlotButton = None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterSlotWindow(self, layer)

	def SetSlotStyle(self, style):
		wndMgr.SetSlotStyle(self.hWnd, style)

	if app.ENABLE_DSS_ACTIVE_EFFECT_BUTTON:
		def SetRenderSlot(self, renderingSlotNumber, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
			wndMgr.SetSlot(self.hWnd, renderingSlotNumber, 1, 1, 1, 0, diffuseColor)
			wndMgr.SetSlotCount(self.hWnd, renderingSlotNumber, 0)

	def HasSlot(self, slotIndex):
		return wndMgr.HasSlot(self.hWnd, slotIndex)

	def SetSlotBaseImage(self, imageFileName, r, g, b, a):
		wndMgr.SetSlotBaseImage(self.hWnd, imageFileName, r, g, b, a)
        
	def SetSlotBaseImageScale(self, imageFileName, r, g, b, a, sx, sy):
		wndMgr.SetSlotBaseImageScale(self.hWnd, imageFileName, r, g, b, a, sx, sy)

	def SetCoverButton(self,\
						slotIndex,\
						upName="d:/ymir work/ui/public/slot_cover_button_01.sub",\
						overName="d:/ymir work/ui/public/slot_cover_button_02.sub",\
						downName="d:/ymir work/ui/public/slot_cover_button_03.sub",\
						disableName="d:/ymir work/ui/public/slot_cover_button_04.sub",\
						LeftButtonEnable = False,\
						RightButtonEnable = True):
		wndMgr.SetCoverButton(self.hWnd, slotIndex, upName, overName, downName, disableName, LeftButtonEnable, RightButtonEnable)

	def EnableCoverButton(self, slotIndex):
		wndMgr.EnableCoverButton(self.hWnd, slotIndex)

	def DisableCoverButton(self, slotIndex):
		wndMgr.DisableCoverButton(self.hWnd, slotIndex)

	def SetAlwaysRenderCoverButton(self, slotIndex, bAlwaysRender = True):
		wndMgr.SetAlwaysRenderCoverButton(self.hWnd, slotIndex, bAlwaysRender)

	def AppendSlotButton(self, upName, overName, downName):
		wndMgr.AppendSlotButton(self.hWnd, upName, overName, downName)

	def ShowSlotButton(self, slotNumber):
		wndMgr.ShowSlotButton(self.hWnd, slotNumber)

	def HideAllSlotButton(self):
		wndMgr.HideAllSlotButton(self.hWnd)

	def AppendRequirementSignImage(self, filename):
		wndMgr.AppendRequirementSignImage(self.hWnd, filename)

	def ShowRequirementSign(self, slotNumber):
		wndMgr.ShowRequirementSign(self.hWnd, slotNumber)

	def HideRequirementSign(self, slotNumber):
		wndMgr.HideRequirementSign(self.hWnd, slotNumber)

	if app.GLOW_EFFECT:
		def AppendHighLightImage(self, index, fileName, alphaSpeed = 0.0, rotationSpeed = 0.0, curAlpha = 1.0, diffuse = 0xFFFFFFFF):
			wndMgr.AppendHighLightImage(self.hWnd, index, fileName, alphaSpeed, rotationSpeed, curAlpha, diffuse)

		def EnableHighLightImage(self, slotIndex):
			wndMgr.EnableHighLightImage(self.hWnd, slotIndex)

		def DisableHighLightImage(self, slotIndex):
			wndMgr.DisableHighLightImage(self.hWnd, slotIndex)

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def ActivateSlot(self, slotNumber, r = 1.0, g = 1.0, b = 1.0, a = 1.0):
			wndMgr.ActivateEffect(self.hWnd, slotNumber, r, g, b, a)

		def DeactivateSlot(self, slotNumber):
			wndMgr.DeactivateEffect(self.hWnd, slotNumber)

		def ActivateSlotOld(self, slotNumber):
			wndMgr.ActivateSlot(self.hWnd, slotNumber)

		def DeactivateSlotOld(self, slotNumber):
			wndMgr.DeactivateSlot(self.hWnd, slotNumber)
	else:
		def ActivateSlot(self, slotNumber):
			wndMgr.ActivateSlot(self.hWnd, slotNumber)

		def DeactivateSlot(self, slotNumber):
			wndMgr.DeactivateSlot(self.hWnd, slotNumber)

	# BEGIN_OFFLINE_SHOP
	def ActivateOfflineShopSlot(self, slotNumber):
		wndMgr.ActivateOfflineShopSlot(self.hWnd, slotNumber)

	def DeactivateOfflineShopSlot(self, slotNumber):
		wndMgr.DeactivateOfflineShopSlot(self.hWnd, slotNumber)
	# END_OF_OFFLINE_SHOP

	def ShowSlotBaseImage(self, slotNumber):
		wndMgr.ShowSlotBaseImage(self.hWnd, slotNumber)

	def HideSlotBaseImage(self, slotNumber):
		wndMgr.HideSlotBaseImage(self.hWnd, slotNumber)

	def SAFE_SetButtonEvent(self, button, state, event):
		if "LEFT"==button:
			if "EMPTY"==state:
				self.eventSelectEmptySlot=__mem_func__(event)
			elif "EXIST"==state:
				self.eventSelectItemSlot=__mem_func__(event)
			elif "ALWAYS"==state:
				self.eventSelectEmptySlot=__mem_func__(event)
				self.eventSelectItemSlot=__mem_func__(event)
		elif "RIGHT"==button:
			if "EMPTY"==state:
				self.eventUnselectEmptySlot=__mem_func__(event)
			elif "EXIST"==state:
				self.eventUnselectItemSlot=__mem_func__(event)
			elif "ALWAYS"==state:
				self.eventUnselectEmptySlot=__mem_func__(event)
				self.eventUnselectItemSlot=__mem_func__(event)

	def SetSelectEmptySlotEvent(self, empty):
		self.eventSelectEmptySlot = empty

	def SetSelectItemSlotEvent(self, item):
		self.eventSelectItemSlot = item

	def SetUnselectEmptySlotEvent(self, empty):
		self.eventUnselectEmptySlot = empty

	def SetUnselectItemSlotEvent(self, item):
		self.eventUnselectItemSlot = item

	def SetUseSlotEvent(self, use):
		self.eventUseSlot = use

	def SetOverInItemEvent(self, event):
		self.eventOverInItem = event

	def SetOverOutItemEvent(self, event):
		self.eventOverOutItem = event

	def SetPressedSlotButtonEvent(self, event):
		self.eventPressedSlotButton = event

	def GetSlotCount(self):
		return wndMgr.GetSlotCount(self.hWnd)

	def SetUseMode(self, flag):
		"True�϶��� ItemToItem �� �������� �����ش�"
		wndMgr.SetUseMode(self.hWnd, flag)

	def SetUsableItem(self, flag):
		"True�� ���� ����Ų �������� ItemToItem ���� �����ϴ�"
		wndMgr.SetUsableItem(self.hWnd, flag)

	if app.ENABLE_SWAPITEM_SYSTEM:
		def SetSwapItem(self, flag):
			wndMgr.SetSwapItem(self.hWnd, flag)

	if app.WJ_ENABLE_TRADABLE_ICON:
		def SetCanMouseEventSlot(self, slotIndex):
			wndMgr.SetCanMouseEventSlot(self.hWnd, slotIndex)

		def SetCantMouseEventSlot(self, slotIndex):
			wndMgr.SetCantMouseEventSlot(self.hWnd, slotIndex)

		def SetUsableSlotOnTopWnd(self, slotIndex):
			wndMgr.SetUsableSlotOnTopWnd(self.hWnd, slotIndex)

		def SetUnusableSlotOnTopWnd(self, slotIndex):
			wndMgr.SetUnusableSlotOnTopWnd(self.hWnd, slotIndex)

	## Slot
	def SetSlotCoolTime(self, slotIndex, coolTime, elapsedTime = 0.0):
		wndMgr.SetSlotCoolTime(self.hWnd, slotIndex, coolTime, elapsedTime)
		
	def StoreSlotCoolTime(self, key, slotIndex, coolTime, elapsedTime = 0.0):
		wndMgr.StoreSlotCoolTime(self.hWnd, key, slotIndex, coolTime, elapsedTime)
	
	def RestoreSlotCoolTime(self, key):
		wndMgr.RestoreSlotCoolTime(self.hWnd, key)

	def DisableSlot(self, slotIndex):
		wndMgr.DisableSlot(self.hWnd, slotIndex)

	def EnableSlot(self, slotIndex):
		wndMgr.EnableSlot(self.hWnd, slotIndex)

	def LockSlot(self, slotIndex):
		wndMgr.LockSlot(self.hWnd, slotIndex)

	def UnlockSlot(self, slotIndex):
		wndMgr.UnlockSlot(self.hWnd, slotIndex)

	def RefreshSlot(self):
		wndMgr.RefreshSlot(self.hWnd)

	def ClearSlot(self, slotNumber):
		wndMgr.ClearSlot(self.hWnd, slotNumber)

	def ClearAllSlot(self):
		wndMgr.ClearAllSlot(self.hWnd)

	def AppendSlot(self, index, x, y, width, height):
		wndMgr.AppendSlot(self.hWnd, index, x, y, width, height)

	def SetSlot(self, slotIndex, itemIndex, width, height, icon, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
		wndMgr.SetSlot(self.hWnd, slotIndex, itemIndex, width, height, icon, diffuseColor)
        
	def SetSlotScale(self, slotIndex, itemIndex, width, height, icon, sx, sy, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
		wndMgr.SetSlotScale(self.hWnd, slotIndex, itemIndex, width, height, icon, diffuseColor, sx, sy)

	def SetSlotCount(self, slotNumber, count):
		wndMgr.SetSlotCount(self.hWnd, slotNumber, count)

	def SetSlotCountNew(self, slotNumber, grade, count):
		wndMgr.SetSlotCountNew(self.hWnd, slotNumber, grade, count)
		
	def SetCardSlot(self, renderingSlotNumber, CardIndex, cardIcon, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
		if 0 == CardIndex or None == CardIndex:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		item.SelectItem(CardIndex)
		(width, height) = item.GetItemSize()
		
		wndMgr.SetCardSlot(self.hWnd, renderingSlotNumber, CardIndex, width, height, cardIcon, diffuseColor)

	def SetItemSlot(self, renderingSlotNumber, ItemIndex, ItemCount = 0, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
		if 0 == ItemIndex or None == ItemIndex:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		item.SelectItem(ItemIndex)
		itemIcon = item.GetIconImage()

		item.SelectItem(ItemIndex)
		(width, height) = item.GetItemSize()

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, ItemIndex, width, height, itemIcon, diffuseColor)
		wndMgr.SetSlotCount(self.hWnd, renderingSlotNumber, ItemCount)
		if app.ENABLE_CHANGELOOK_SYSTEM:
			wndMgr.SetCoverButton(self.hWnd, renderingSlotNumber, "d:/ymir work/ui/game/quest/slot_button_00.sub", "d:/ymir work/ui/game/quest/slot_button_00.sub", "d:/ymir work/ui/game/quest/slot_button_00.sub", "icon/item/ingame_convert_mark.tga", False, False)
	####Item level text/icon ###
		itemName=item.GetItemName().strip()
		itemNameP=item.GetItemName().rfind('+')
		if itemNameP>0 and len(itemName)>itemNameP+1:
			level=itemName[itemNameP+1:]
			if level.isdigit():
				wndMgr.SetSlotLevelImage(self.hWnd, renderingSlotNumber, ("icon/level/%d.tga"%int(level)))
	####Item level text/icon END ###

	def SetPetSkillSlot(self, renderingSlotNumber, skillIndex, skillLevel, sx = 1.0, sy = 1.0):

		skillIcon = petskill.GetIconImage(skillIndex)

		if 0 == skillIcon:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return
		petskill.SetSkillSlot(renderingSlotNumber, skillIndex)
		if sx != 1.0:
			wndMgr.SetSlotScale(self.hWnd, renderingSlotNumber, skillIndex, 1, 1, skillIcon, (1.0, 1.0, 1.0, 1.0), sx, sy)
		else:
			wndMgr.SetSlot(self.hWnd, renderingSlotNumber, skillIndex, 1, 1, skillIcon)
			wndMgr.SetSlotCount(self.hWnd, renderingSlotNumber, skillLevel)

	def SetSkillSlot(self, renderingSlotNumber, skillIndex, skillLevel):

		skillIcon = skill.GetIconImage(skillIndex)

		if 0 == skillIcon:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, skillIndex, 1, 1, skillIcon)
		wndMgr.SetSlotCount(self.hWnd, renderingSlotNumber, skillLevel)

	def SetSkillSlotNew(self, renderingSlotNumber, skillIndex, skillGrade, skillLevel):

		skillIcon = skill.GetIconImageNew(skillIndex, skillGrade)

		if 0 == skillIcon:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, skillIndex, 1, 1, skillIcon)
		
	if app.ENABLE_SPECIAL_STATS_SYSTEM:
		
		def SetSpecialStatSlot(self, renderingSlotNumber, specialStatIndex):
			import player
			icon = player.GetSpecialStatIconImage(specialStatIndex)

			if 0 == icon:
				wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
				return

			wndMgr.SetSlot(self.hWnd, renderingSlotNumber, renderingSlotNumber, 1, 1, icon)

	def SetEmotionSlot(self, renderingSlotNumber, emotionIndex):
		import player
		icon = player.GetEmotionIconImage(emotionIndex)

		if 0 == icon:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, emotionIndex, 1, 1, icon)

	## Event
	def OnSelectEmptySlot(self, slotNumber):
		if self.eventSelectEmptySlot:
			self.eventSelectEmptySlot(slotNumber)

	def OnSelectItemSlot(self, slotNumber):
		if self.eventSelectItemSlot:
			self.eventSelectItemSlot(slotNumber)

	def OnUnselectEmptySlot(self, slotNumber):
		if self.eventUnselectEmptySlot:
			self.eventUnselectEmptySlot(slotNumber)

	def OnUnselectItemSlot(self, slotNumber):
		if self.eventUnselectItemSlot:
			self.eventUnselectItemSlot(slotNumber)

	def OnUseSlot(self, slotNumber):
		if self.eventUseSlot:
			self.eventUseSlot(slotNumber)
			
	def OnOverInItem(self, slotNumber):
		if self.eventOverInItem:
			self.eventOverInItem(slotNumber)

	def OnOverOutItem(self):
		if self.eventOverOutItem:
			self.eventOverOutItem()

	def OnPressedSlotButton(self, slotNumber):
		if self.eventPressedSlotButton:
			self.eventPressedSlotButton(slotNumber)

	def GetStartIndex(self):
		return 0

class GridSlotWindow(SlotWindow):

	def __init__(self):
		SlotWindow.__init__(self)
		if app.ENABLE_REFINE_WINDOW_SLOT_EFFECT:
			self.__BuildText()
		self.startIndex = 0

	def __del__(self):
		SlotWindow.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterGridSlotWindow(self, layer)

	def ArrangeSlot(self, StartIndex, xCount, yCount, xSize, ySize, xBlank, yBlank):

		self.startIndex = StartIndex

		wndMgr.ArrangeSlot(self.hWnd, StartIndex, xCount, yCount, xSize, ySize, xBlank, yBlank)
		self.startIndex = StartIndex

	def ActivateSlotEffect(self, slotNumber, r = 1.0, g = 1.0, b = 1.0, a = 1.0):
		wndMgr.ActivateSlotEffect(self.hWnd, slotNumber, r, g, b, a)
	
	def DeactivateSlotEffect(self, slotNumber):
		wndMgr.DeactivateSlotEffect(self.hWnd, slotNumber)

	def GetStartIndex(self):
		return self.startIndex

	if app.ENABLE_REFINE_WINDOW_SLOT_EFFECT:
		def __BuildText(self):
			self.text = TextLine()
			self.text.SetParent(self)
			self.text.SetPosition(23, 19)
			self.text.SetOutline(16)
			self.text.SetFontName("Tohoma:12")
			self.text.SetPackedFontColor(0xffffffff)
			self.text.Show()
	
		def SetText(self, text):
			self.text.SetText(text)

class TitleBar(Window):

	BLOCK_WIDTH = 32
	BLOCK_HEIGHT = 23

	def __init__(self):
		Window.__init__(self)
		self.AddFlag("attach")

	def __del__(self):
		Window.__del__(self)

	def MakeTitleBar(self, width, color):

		## ���� Color�� ����ϰ� ���� ����

		width = max(64, width)

		imgLeft = ImageBox()
		imgCenter = ExpandedImageBox()
		imgRight = ImageBox()
		imgLeft.AddFlag("not_pick")
		imgCenter.AddFlag("not_pick")
		imgRight.AddFlag("not_pick")
		imgLeft.SetParent(self)
		imgCenter.SetParent(self)
		imgRight.SetParent(self)

		if localeInfo.IsARABIC():
			imgLeft.LoadImage("locale/ae/ui/pattern/titlebar_left.tga")
			imgCenter.LoadImage("locale/ae/ui/pattern/titlebar_center.tga")
			imgRight.LoadImage("locale/ae/ui/pattern/titlebar_right.tga")
		else:
			imgLeft.LoadImage("d:/ymir work/ui/pattern/titlebar_left.tga")
			imgCenter.LoadImage("d:/ymir work/ui/pattern/titlebar_center.tga")
			imgRight.LoadImage("d:/ymir work/ui/pattern/titlebar_right.tga")

		imgLeft.Show()
		imgCenter.Show()
		imgRight.Show()

		btnClose = Button()
		btnClose.SetParent(self)
		btnClose.SetUpVisual("d:/ymir work/ui/public/close_button_01.sub")
		btnClose.SetOverVisual("d:/ymir work/ui/public/close_button_02.sub")
		btnClose.SetDownVisual("d:/ymir work/ui/public/close_button_03.sub")
		btnClose.SetToolTipText(localeInfo.UI_CLOSE, 0, -23)
		btnClose.Show()

		if app.GLOW_EFFECT:
			btnMinimize = ImageBox()
			btnMinimize.AddFlag("not_pick")
			btnMinimize.SetParent(self)
			btnMinimize.LoadImage("d:/ymir work/ui/pattern/titlebar_minimize_baseframe.tga")
			btnMinimize.Hide()

			btnMinimize.Button = Button()
			btnMinimize.Button.SetParent(btnMinimize)
			btnMinimize.Button.SetPosition(3, 3)
			btnMinimize.Button.SetUpVisual("d:/ymir work/ui/public/minimize_button_01.sub")
			btnMinimize.Button.SetOverVisual("d:/ymir work/ui/public/minimize_button_02.sub")
			btnMinimize.Button.SetDownVisual("d:/ymir work/ui/public/minimize_button_03.sub")
			btnMinimize.Button.SetToolTipText(localeInfo.UI_MINIMIZE, 0, -23)
			btnMinimize.Button.Show()

		self.imgLeft = imgLeft
		self.imgCenter = imgCenter
		self.imgRight = imgRight
		self.btnClose = btnClose
		if app.GLOW_EFFECT:
			self.btnMinimize = btnMinimize

		self.SetWidth(width)

	if app.GLOW_EFFECT:
		def AdjustButtonsPosition(self):
			if localeInfo.IsARABIC():
				self.btnClose.SetPosition(3, 3)
				if self.btnClose.IsShow():
					self.btnMinimize.SetPosition(3 + self.btnClose.GetWidth(), 3)
				else:
					self.btnMinimize.SetPosition(3, 3)
			else:
				self.btnClose.SetPosition(self.GetWidth() - self.btnClose.GetWidth() - 3, 3)
				if self.btnClose.IsShow():
					self.btnMinimize.SetPosition(self.GetWidth() - self.btnClose.GetWidth() - self.btnMinimize.GetWidth() - 6, 0)
				else:
					self.btnMinimize.SetPosition(self.GetWidth() - self.btnMinimize.GetWidth(), 0)

	def SetWidth(self, width):
		self.imgCenter.SetRenderingRect(0.0, 0.0, float((width - self.BLOCK_WIDTH*2) - self.BLOCK_WIDTH) / self.BLOCK_WIDTH, 0.0)
		self.imgCenter.SetPosition(self.BLOCK_WIDTH, 0)
		self.imgRight.SetPosition(width - self.BLOCK_WIDTH, 0)

		if localeInfo.IsARABIC():
			self.btnClose.SetPosition(3, 3)
		else:
			self.btnClose.SetPosition(width - self.btnClose.GetWidth() - 3, 3)

		self.SetSize(width, self.BLOCK_HEIGHT)
		if app.GLOW_EFFECT:
			self.AdjustButtonsPosition()

	if app.GLOW_EFFECT:
		def SetMinimizeEvent(self, event):
			self.btnMinimize.Button.SetEvent(event)

		def MinimizeButtonShow(self):
			if not self.btnClose.IsShow():
				self.imgRight.LoadImage("d:/ymir work/ui/pattern/titlebar_right.tga")

			self.btnMinimize.Show()

			self.AdjustButtonsPosition()

	def SetCloseEvent(self, event):
		self.btnClose.SetEvent(event)
	if app.ENABLE_KILL_STATISTICS:
		def CloseButtonHide(self) :
			self.imgRight.LoadImage("d:/ymir work/ui/pattern/titlebar_right_02.tga")
			self.btnClose.Hide()
if app.ENABLE_QUEST_RENEWAL:
	class SubTitleBar(Button):
		def __init__(self):
			Button.__init__(self)

		def __del__(self):
			Button.__del__(self)

		def MakeSubTitleBar(self, width, color):
			width = max(64, width)
			self.SetWidth(width)
			self.SetUpVisual("d:/ymir work/ui/quest_re/quest_tab_01.tga")
			self.SetOverVisual("d:/ymir work/ui/quest_re/quest_tab_01.tga")
			self.SetDownVisual("d:/ymir work/ui/quest_re/quest_tab_01.tga")
			self.Show()

			scrollImage = ImageBox()
			scrollImage.SetParent(self)
			scrollImage.LoadImage("d:/ymir work/ui/quest_re/quest_down.tga")
			scrollImage.SetPosition(5, 2.5)
			scrollImage.AddFlag("not_pick")
			scrollImage.Show()
			self.scrollImage = scrollImage

		def OpenCategory(self, qcount = 0):
			if qcount > 0:
				self.scrollImage.LoadImage("d:/ymir work/ui/quest_re/quest_up.tga")
			else:
				self.scrollImage.LoadImage("d:/ymir work/ui/quest_re/quest_down.tga")

		def CloseCategory(self, qcount = 0):
			self.scrollImage.LoadImage("d:/ymir work/ui/quest_re/quest_down.tga")

		def SetQuestLabel(self, filename, qcount):
			tabColor = ImageBox()
			tabColor.SetParent(self)
			tabColor.LoadImage(filename)
			tabColor.AddFlag("not_pick")
			tabColor.SetPosition(188, 12)
			if qcount > 0:
				tabColor.Show()
			else:
				tabColor.Hide()
			self.tabColor = tabColor

		def SetWidth(self, width):
			self.SetPosition(32, 0)
			self.SetSize(width, 23)

	class ListBar(Button):
		def __init__(self):
			Button.__init__(self)

		def __del__(self):
			Button.__del__(self)

		def MakeListBar(self, width, color):
			width = max(64, width)
			self.SetWidth(width)
			self.Show()

			checkbox = ImageBox()
			checkbox.SetParent(self)
			checkbox.LoadImage("d:/ymir work/ui/quest_re/quest_new.tga")
			checkbox.SetPosition(10, 9)
			checkbox.AddFlag("not_pick")
			checkbox.Show()
			self.checkbox = checkbox
			self.isChecked = False

		def SetWidth(self, width):
			self.SetPosition(32, 0)
			self.SetSize(width, 23)

		def CallEvent(self):
			self.OnClickEvent()
			super(ListBar, self).CallEvent()

		def OnClickEvent(self):
			self.checkbox.Hide()
			self.isChecked = True

		def SetSlot(self, slotIndex, itemIndex, width, height, icon, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
			wndMgr.SetSlot(self.hWnd, slotIndex, itemIndex, width, height, icon, diffuseColor)

class HorizontalBar(Window):

	BLOCK_WIDTH = 32
	BLOCK_HEIGHT = 17

	def __init__(self):
		Window.__init__(self)
		self.AddFlag("attach")

	def __del__(self):
		Window.__del__(self)

	def Create(self, width):

		width = max(96, width)

		imgLeft = ImageBox()
		imgLeft.SetParent(self)
		imgLeft.AddFlag("not_pick")
		imgLeft.LoadImage("d:/ymir work/ui/pattern/horizontalbar_left.tga")
		imgLeft.Show()

		imgCenter = ExpandedImageBox()
		imgCenter.SetParent(self)
		imgCenter.AddFlag("not_pick")
		imgCenter.LoadImage("d:/ymir work/ui/pattern/horizontalbar_center.tga")
		imgCenter.Show()

		imgRight = ImageBox()
		imgRight.SetParent(self)
		imgRight.AddFlag("not_pick")
		imgRight.LoadImage("d:/ymir work/ui/pattern/horizontalbar_right.tga")
		imgRight.Show()

		self.imgLeft = imgLeft
		self.imgCenter = imgCenter
		self.imgRight = imgRight
		self.SetWidth(width)

	def SetWidth(self, width):
		self.imgCenter.SetRenderingRect(0.0, 0.0, float((width - self.BLOCK_WIDTH*2) - self.BLOCK_WIDTH) / self.BLOCK_WIDTH, 0.0)
		self.imgCenter.SetPosition(self.BLOCK_WIDTH, 0)
		self.imgRight.SetPosition(width - self.BLOCK_WIDTH, 0)
		self.SetSize(width, self.BLOCK_HEIGHT)

class Gauge(Window):

	SLOT_WIDTH = 16
	SLOT_HEIGHT = 7

	GAUGE_TEMPORARY_PLACE = 12
	GAUGE_WIDTH = 16

	def __init__(self):
		Window.__init__(self)
		self.width = 0
	def __del__(self):
		Window.__del__(self)

	def MakeGauge(self, width, color):

		self.width = max(48, width)

		imgSlotLeft = ImageBox()
		imgSlotLeft.SetParent(self)
		imgSlotLeft.LoadImage("d:/ymir work/ui/pattern/gauge_slot_left.tga")
		imgSlotLeft.Show()

		imgSlotRight = ImageBox()
		imgSlotRight.SetParent(self)
		imgSlotRight.LoadImage("d:/ymir work/ui/pattern/gauge_slot_right.tga")
		imgSlotRight.Show()
		imgSlotRight.SetPosition(width - self.SLOT_WIDTH, 0)

		imgSlotCenter = ExpandedImageBox()
		imgSlotCenter.SetParent(self)
		imgSlotCenter.LoadImage("d:/ymir work/ui/pattern/gauge_slot_center.tga")
		imgSlotCenter.Show()
		imgSlotCenter.SetRenderingRect(0.0, 0.0, float((width - self.SLOT_WIDTH*2) - self.SLOT_WIDTH) / self.SLOT_WIDTH, 0.0)
		imgSlotCenter.SetPosition(self.SLOT_WIDTH, 0)

		imgGauge = ExpandedImageBox()
		imgGauge.SetParent(self)
		imgGauge.LoadImage("d:/ymir work/ui/pattern/gauge_" + color + ".tga")
		imgGauge.Show()
		imgGauge.SetRenderingRect(0.0, 0.0, 0.0, 0.0)
		imgGauge.SetPosition(self.GAUGE_TEMPORARY_PLACE, 0)

		imgSlotLeft.AddFlag("attach")
		imgSlotCenter.AddFlag("attach")
		imgSlotRight.AddFlag("attach")

		self.imgLeft = imgSlotLeft
		self.imgCenter = imgSlotCenter
		self.imgRight = imgSlotRight
		self.imgGauge = imgGauge

		self.SetSize(width, self.SLOT_HEIGHT)

	def SetPercentage(self, curValue, maxValue):

		# PERCENTAGE_MAX_VALUE_ZERO_DIVISION_ERROR
		if maxValue > 0.0:
			percentage = min(1.0, float(curValue)/float(maxValue))
		else:
			percentage = 0.0
		# END_OF_PERCENTAGE_MAX_VALUE_ZERO_DIVISION_ERROR

		gaugeSize = -1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2) * percentage / self.GAUGE_WIDTH
		self.imgGauge.SetRenderingRect(0.0, 0.0, gaugeSize, 0.0)

	if app.ENABLE_POISON_GAUGE_EFFECT:
		def SetGaugeColor(self, color):
			if self.imgGauge:
				self.imgGauge.LoadImage("d:/ymir work/ui/pattern/gauge_" + color + ".tga")

class BattlePassGauge(Window):

	SLOT_WIDTH = 16
	SLOT_HEIGHT = 7

	GAUGE_TEMPORARY_PLACE = 12
	GAUGE_WIDTH = 16

	def __init__(self):
		Window.__init__(self)
		self.width = 0
		self.showtooltipevent = None
		self.showtooltiparg = None
		self.hidetooltipevent = None
		self.hidetooltiparg = None
		self.ToolTipText = None

	def __del__(self):
		Window.__del__(self)
		self.showtooltipevent = None
		self.showtooltiparg = None
		self.hidetooltipevent = None
		self.hidetooltiparg = None

	def MakeGauge(self, width, color):

		self.width = max(48, width)

		imgSlotLeft = ImageBox()
		imgSlotLeft.SetParent(self)
		imgSlotLeft.LoadImage("d:/ymir work/battle_pass/gauge/gauge_slot_left.tga")
		imgSlotLeft.Show()

		imgSlotRight = ImageBox()
		imgSlotRight.SetParent(self)
		imgSlotRight.LoadImage("d:/ymir work/battle_pass/gauge/gauge_slot_right.tga")
		imgSlotRight.Show()
		imgSlotRight.SetPosition(width - self.SLOT_WIDTH, 0)

		imgSlotCenter = ExpandedImageBox()
		imgSlotCenter.SetParent(self)
		imgSlotCenter.LoadImage("d:/ymir work/battle_pass/gauge/gauge_slot_center.tga")
		imgSlotCenter.Show()
		imgSlotCenter.SetRenderingRect(0.0, 0.0, float((width - self.SLOT_WIDTH*2) - self.SLOT_WIDTH) / self.SLOT_WIDTH, 0.0)
		imgSlotCenter.SetPosition(self.SLOT_WIDTH, 0)

		imgGaugeBack = ExpandedImageBox()
		imgGaugeBack.SetParent(self)
		imgGaugeBack.LoadImage("d:/ymir work/battle_pass/gauge/gauge_" + color + ".tga")
		imgGaugeBack.Hide()
		imgGaugeBack.SetRenderingRect(0.0, 0.0, 0.0, 0.0)
		imgGaugeBack.SetPosition(self.GAUGE_TEMPORARY_PLACE, 0)

		imgGauge = ExpandedImageBox()
		imgGauge.SetParent(self)
		imgGauge.LoadImage("d:/ymir work/battle_pass/gauge/gauge_" + color + ".tga")
		imgGauge.Show()
		imgGauge.SetRenderingRect(0.0, 0.0, 0.0, 0.0)
		imgGauge.SetPosition(self.GAUGE_TEMPORARY_PLACE, 0)

		imgSlotLeft.AddFlag("attach")
		imgSlotCenter.AddFlag("attach")
		imgSlotRight.AddFlag("attach")

		self.imgLeft = imgSlotLeft
		self.imgCenter = imgSlotCenter
		self.imgRight = imgSlotRight
		self.imgGauge = imgGauge
		self.imgGaugeBack = imgGaugeBack
		self.curValue = 100
		self.maxValue = 100
		self.currentGaugeColor = color

		self.SetSize(width, self.SLOT_HEIGHT)
		
	def SetColor(self, color):
		if (self.currentGaugeColor == color):
			return
			
		self.currentGaugeColor = color
		self.imgGauge.LoadImage("d:/ymir work/battle_pass/gauge/gauge_" + color + ".tga")
		self.SetPercentage(self.curValue, self.maxValue)

	def SetPercentage(self, curValue, maxValue):
		if maxValue > 0.0:
			percentage = min(1.0, float(curValue)/float(maxValue))
		else:
			percentage = 0.0
			
		self.lastCurValue = curValue
		self.lastMaxValue = maxValue

		gaugeSize = -1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2) * percentage / self.GAUGE_WIDTH
		self.imgGauge.SetRenderingRect(0.0, 0.0, gaugeSize, 0.0)
		
	def SetPercentageBack(self, curValue, maxValue):
		if not self.imgGaugeBack.IsShow():
			self.imgGaugeBack.Show()
			

		if maxValue > 0.0:
			percentage = min(1.0, float(curValue)/float(maxValue))
		else:
			percentage = 0.0


		gaugeSize = -1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2) * percentage / self.GAUGE_WIDTH
		self.imgGaugeBack.SetRenderingRect(0.0, 0.0, gaugeSize, 0.0)	

	def SetShowToolTipEvent(self, func, *args):

		self.showtooltipevent = func
		self.showtooltiparg = args

	def SetHideToolTipEvent(self, func, *args):
		self.hidetooltipevent = func
		self.hidetooltiparg = args

	def ShowToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Show()

	def HideToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Hide()

	def SetToolTipText(self, text, x=0, y = -19):
		self.SetFormToolTipText("TEXT", text, x, y)

	def SetFormToolTipText(self, type, text, x, y):
		if not self.ToolTipText:       
			toolTip=createToolTipWindowDict[type]()
			toolTip.SetParent(self)
			toolTip.SetSize(0, 0)
			toolTip.SetHorizontalAlignCenter()
			toolTip.SetOutline()
			toolTip.Hide()
			toolTip.SetPosition(x + self.GetWidth()/2, y)
			self.ToolTipText=toolTip
		self.ToolTipText.SetText(text)
		
class DynamicGauge(Gauge):
    dynamicGaugePerc = None
    newGaugePerc = 0
    def __init__(self):
        Gauge.__init__(self)
    def __del__(self):
        Gauge.__del__(self)
        
    def MakeGauge(self, width, color1, color2):
        Gauge.MakeGauge(self,width, color2)
        
        imgGauge2 = ExpandedImageBox()
        imgGauge2.SetParent(self)
        imgGauge2.LoadImage("d:/ymir work/ui/pattern/gauge_" + color1 + ".tga")
        imgGauge2.Show()
        imgGauge2.SetRenderingRect(0.0, 0.0, 0.0, 0.0)
        imgGauge2.SetPosition(self.GAUGE_TEMPORARY_PLACE, 0)
        
        self.imgGauge2 = imgGauge2
    
    def SetPercentage(self, curValue, maxValue):
        # PERCENTAGE_MAX_VALUE_ZERO_DIVISION_ERROR
        if maxValue > 0.0:
            percentage = min(1.0, float(curValue)/float(maxValue))
        else:
            percentage = 0.0
        # END_OF_PERCENTAGE_MAX_VALUE_ZERO_DIVISION_ERROR
        gaugeSize = -1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2) * percentage / self.GAUGE_WIDTH
        
        if self.dynamicGaugePerc == None:
            self.imgGauge.SetRenderingRect(0.0, 0.0, (-1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2) * percentage / self.GAUGE_WIDTH), 0.0)
            self.dynamicGaugePerc = percentage
        elif self.dynamicGaugePerc+0.2 < self.newGaugePerc:
            self.imgGauge.SetRenderingRect(0.0, 0.0, (-1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2) * self.newGaugePerc / self.GAUGE_WIDTH), 0.0)
            self.dynamicGaugePerc = self.newGaugePerc
        
        self.newGaugePerc = percentage
        self.imgGauge2.SetRenderingRect(0.0, 0.0, gaugeSize, 0.0)
        if percentage == 0:
            self.imgGauge.Hide()
        else:
            self.imgGauge.Show()
    
    def OnUpdate(self):
        if self.dynamicGaugePerc > self.newGaugePerc:
            self.dynamicGaugePerc = self.dynamicGaugePerc - 0.005
            self.imgGauge.SetRenderingRect(0.0, 0.0, (-1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2) * self.dynamicGaugePerc / self.GAUGE_WIDTH), 0.0)
        elif self.dynamicGaugePerc < self.newGaugePerc:
            self.dynamicGaugePerc = self.newGaugePerc
            self.imgGauge.SetRenderingRect(0.0, 0.0, (-1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2) * self.dynamicGaugePerc / self.GAUGE_WIDTH), 0.0)

class Board_Brown(Window):
	CORNER_WIDTH = 32
	CORNER_HEIGHT = 32
	LINE_WIDTH = 128
	LINE_HEIGHT = 128

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3
	
	BASE_PATH = "d:/ymir work/ui/shop/board_brown"
	IMAGES = {
		'CORNER' : {
			0 : "board_corner_lefttop",
			1 : "board_corner_Leftbottom",
			2 : "board_corner_righttop",
			3 : "board_corner_rightbottom"
		},
		'BAR' : {
			0 : "board_line_left",
			1 : "board_line_right",
			2 : "board_line_top",
			3 : "board_line_bottom"
		},
		'FILL' : "board_base"
	}

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.MakeBoard()
		
	def MakeBoard(self):
		CornerFileNames = [ ]
		LineFileNames = [ ]
		
		for imageDictKey in (['CORNER', 'BAR']):
			for x in xrange(len(self.IMAGES[imageDictKey])):
				if imageDictKey == "CORNER":
					CornerFileNames.append("%s/%s.png" % (self.BASE_PATH, self.IMAGES[imageDictKey][x]))
				elif imageDictKey == "BAR":
					LineFileNames.append("%s/%s.png" % (self.BASE_PATH, self.IMAGES[imageDictKey][x]))
		
		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

		self.Base = ExpandedImageBox()
		self.Base.AddFlag("not_pick")
		self.Base.LoadImage("%s/%s.tga" % (self.BASE_PATH, self.IMAGES['FILL']))
		self.Base.SetParent(self)
		self.Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Base.Show()

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):
		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		if self.Base:
			self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)


class Board(Window):

	CORNER_WIDTH = 32
	CORNER_HEIGHT = 32
	LINE_WIDTH = 128
	LINE_HEIGHT = 128

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self):
		Window.__init__(self)

		self.MakeBoard("d:/ymir work/ui/pattern/Board_Corner_", "d:/ymir work/ui/pattern/Board_Line_")
		self.MakeBase()

	def MakeBoard(self, cornerPath, linePath):

		CornerFileNames = [ cornerPath+dir+".tga" for dir in ("LeftTop", "LeftBottom", "RightTop", "RightBottom", ) ]
		LineFileNames = [ linePath+dir+".tga" for dir in ("Left", "Right", "Top", "Bottom", ) ]
		"""
		CornerFileNames = (
							"d:/ymir work/ui/pattern/Board_Corner_LeftTop.tga",
							"d:/ymir work/ui/pattern/Board_Corner_LeftBottom.tga",
							"d:/ymir work/ui/pattern/Board_Corner_RightTop.tga",
							"d:/ymir work/ui/pattern/Board_Corner_RightBottom.tga",
							)
		LineFileNames = (
							"d:/ymir work/ui/pattern/Board_Line_Left.tga",
							"d:/ymir work/ui/pattern/Board_Line_Right.tga",
							"d:/ymir work/ui/pattern/Board_Line_Top.tga",
							"d:/ymir work/ui/pattern/Board_Line_Bottom.tga",
							)
		"""

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def MakeBase(self):
		self.Base = ExpandedImageBox()
		self.Base.AddFlag("not_pick")
		self.Base.LoadImage("d:/ymir work/ui/pattern/Board_Base.tga")
		self.Base.SetParent(self)
		self.Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Base.Show()

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		if self.Base:
			self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

class BorderA(Window):
	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16
	BOARD_COLOR = grp.GenerateColor(0.17, 0.027, 0.0, 0.70)


	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		CornerFileNames = [ "d:/ymir work/ui/pattern/border_a/border_a_"+dir+".tga" for dir in ["Left_Top","Left_Bottom","Right_Top","Right_Bottom"] ]
		LineFileNames = [ "d:/ymir work/ui/pattern/border_a/border_a_"+dir+".tga" for dir in ["Left","Right","Top","Bottom"] ]
		#BaseFileName = "d:/ymir work/ui/pattern/border_a/border_center.tga"
		
		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		self.Base = ExpandedImageBox()
		self.Base.AddFlag("not_pick")
		self.Base.LoadImage("d:/ymir work/ui/pattern/border_a/border_a_center.tga")
		self.Base.SetParent(self)
		self.Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Base.Show()
		
		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		if self.Base:
			self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

	def ShowInternal(self):
		self.Base.Show()
		for wnd in self.Lines:
			wnd.Show()
		for wnd in self.Corners:
			wnd.Show()

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()

class BoardWithTitleBar(Board):
	def __init__(self):
		Board.__init__(self)

		titleBar = TitleBar()
		titleBar.SetParent(self)
		titleBar.MakeTitleBar(0, "red")
		titleBar.SetPosition(8, 7)
		titleBar.Show()

		titleName = TextLine()
		titleName.SetParent(titleBar)
		titleName.SetPosition(0, 4)
		titleName.SetWindowHorizontalAlignCenter()
		titleName.SetHorizontalAlignCenter()
		titleName.Show()

		self.titleBar = titleBar
		self.titleName = titleName

		self.SetCloseEvent(self.Hide)

	def __del__(self):
		Board.__del__(self)
		self.titleBar = None
		self.titleName = None

	def SetSize(self, width, height):
		self.titleBar.SetWidth(width - 15)
		#self.pickRestrictWindow.SetSize(width, height - 30)
		Board.SetSize(self, width, height)
		self.titleName.UpdateRect()

	def SetTitleColor(self, color):
		self.titleName.SetPackedFontColor(color)

	def SetTitleName(self, name):
		self.titleName.SetText(name)

	def SetCloseEvent(self, event):
		self.titleBar.SetCloseEvent(event)
		
	def MakeNewScrollBar(parent, x, y, height):
		scrollbar = NewScrollBar()
		scrollbar.SetParent(parent)
		scrollbar.SetPosition(x, y)
		scrollbar.SetScrollBarSize(height)
		scrollbar.Show()
		return scrollbar		

	# def MakeSliderBar(parent, x, y, event):
		# slideBar = NewSliderBar()
		# slideBar.SetParent(parent)
		# slideBar.SetEvent(event)
		# slideBar.SetPosition(x, y)
		# slideBar.Show()
		# return slideBar

class NewScrollBar(Window):
	SCROLLBAR_WIDTH = 17
	SCROLLBAR_MIDDLE_HEIGHT = 9
	SCROLLBAR_BUTTON_WIDTH = 17
	SCROLLBAR_BUTTON_HEIGHT = 17
	MIDDLE_BAR_POS = 0
	MIDDLE_BAR_UPPER_PLACE = 3
	MIDDLE_BAR_DOWNER_PLACE = 4
	TEMP_SPACE = MIDDLE_BAR_UPPER_PLACE + MIDDLE_BAR_DOWNER_PLACE

	class MiddleBar(DragButton):
		def __init__(self):
			DragButton.__init__(self)
			self.AddFlag("movable")

		def MakeImage(self):

			middle = ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage("d:/ymir work/ui/pattern/new_scroll/scrollbar_middle.tga")
			middle.SetPosition(0, 0)
			middle.AddFlag("not_pick")
			middle.Show()

			self.middle = middle

		def SetSize(self, height):
			height = max(12, height)
			DragButton.SetSize(self, 10, height)

			height -= 4*3
			self.middle.SetRenderingRect(0, 0, 0, float(height)/4.0)

	def __init__(self):
		Window.__init__(self)

		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = lambda *arg: None
		self.lockFlag = False
		self.scrollStep = 0.20

		self.eventFuncCall = True

		self.CreateScrollBar()

	def __del__(self):
		Window.__del__(self)

	def CreateScrollBar(self):
		barSlot = ExpandedImageBox()
		barSlot.SetParent(self)
		barSlot.LoadImage("d:/ymir work/ui/pattern/new_scroll/base_scroll.tga")
		barSlot.AddFlag("not_pick")
		barSlot.Show()

		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.MakeImage()
		middleBar.SetSize(12)
		
		self.middleBar = middleBar
		self.barSlot = barSlot

		self.SCROLLBAR_WIDTH = self.middleBar.GetWidth()
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
		self.SCROLLBAR_BUTTON_WIDTH = self.middleBar.GetWidth()
		self.SCROLLBAR_BUTTON_HEIGHT = self.middleBar.GetHeight()

	def Destroy(self):
		self.middleBar = None
		self.eventScroll = lambda *arg: None

		self.eventFuncCall	= True

	def SetEvnetFuncCall(self, callable):
		self.eventFuncCall = callable

	def SetScrollEvent(self, event):
		self.eventScroll = event

	def SetMiddleBarSize(self, pageScale):
		realHeight = self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2
		self.SCROLLBAR_MIDDLE_HEIGHT = int(pageScale * float(realHeight))
		self.middleBar.SetSize(self.SCROLLBAR_MIDDLE_HEIGHT)
		self.pageSize = (self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)

	def SetScrollBarSize(self, height):
		self.pageSize = (height - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)
		self.SetSize(self.SCROLLBAR_WIDTH, height)
		self.middleBar.SetRestrictMovementArea(self.MIDDLE_BAR_POS, self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE, self.MIDDLE_BAR_POS+2, height - self.SCROLLBAR_BUTTON_HEIGHT*2 - self.TEMP_SPACE)
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, 0)

		self.UpdateBarSlot()

	def UpdateBarSlot(self):
		self.barSlot.SetPosition(0, self.SCROLLBAR_BUTTON_HEIGHT)
		height =  - self.SCROLLBAR_BUTTON_HEIGHT*2 - 2
		new_height = float(self.GetHeight()) / float(self.barSlot.GetHeight())
		self.barSlot.SetRenderingRect(0.0, 0.0, 0.0, new_height - 2.8)

	def GetPos(self):
		return self.curPos

	def SetPos(self, pos, event_callable = True):
		pos = max(0.0, pos)
		pos = min(1.0, pos)

		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, int(newPos) + self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE)

		self.OnMove(event_callable)

	def SetScrollStep(self, step):
		self.scrollStep = step

	def GetScrollStep(self):
		return self.scrollStep

	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep, self.eventFuncCall)

	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep, self.eventFuncCall)

	def OnMove(self, event_callable = True):
		if self.lockFlag:
			return

		if 0 == self.pageSize:
			return

		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal - self.SCROLLBAR_BUTTON_HEIGHT - self.MIDDLE_BAR_UPPER_PLACE) / float(self.pageSize)

		if event_callable:
			self.eventScroll()

	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		pickedPos = yMouseLocalPosition - self.SCROLLBAR_BUTTON_HEIGHT - self.SCROLLBAR_MIDDLE_HEIGHT/2
		newPos = float(pickedPos) / float(self.pageSize)
		self.SetPos(newPos)

	def LockScroll(self):
		self.lockFlag = True

	if app.BL_MAILBOX:
		def SetUpButtonSizeRefresh(self):
			self.SCROLLBAR_WIDTH			= self.upButton.GetWidth()
			self.SCROLLBAR_BUTTON_WIDTH		= self.upButton.GetWidth()
			self.SCROLLBAR_BUTTON_HEIGHT	= self.upButton.GetHeight()
		
		def SetUpButtonUpVisual(self, img_path):
			if self.upButton:
				self.upButton.SetUpVisual( img_path )
		def SetUpButtonOverVisual(self, img_path):
			if self.upButton:
				self.upButton.SetOverVisual( img_path )
		def SetUpButtonDownVisual(self, img_path):
			if self.upButton:
				self.upButton.SetDownVisual( img_path )
		def SetDownButtonUpVisual(self, img_path):
			if self.downButton:
				self.downButton.SetUpVisual( img_path )
		def SetDownButtonOverVisual(self, img_path):
			if self.downButton:
				self.downButton.SetOverVisual( img_path )
		def SetDownButtonDownVisual(self, img_path):
			if self.downButton:
				self.downButton.SetDownVisual( img_path )

	def UnlockScroll(self):
		self.lockFlag = False

	def RunMouseWheel(self, nLen):
		if nLen > 0:
			self.OnUp()
		else:
			self.OnDown()
	
class ThinBoardCircle(Window):
	CORNER_WIDTH = 4
	CORNER_HEIGHT = 4

	LINE_WIDTH = 4
	LINE_HEIGHT = 4

	BOARD_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 1.0)

	LT = 0
	LB = 1
	RT = 2
	RB = 3

	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		CornerFileNames = [ "d:/ymir work/ui/pattern/thinboardcircle/ThinBoard_Corner_"+dir+"_Circle.tga" for dir in ["LeftTop","LeftBottom","RightTop","RightBottom"] ]
		LineFileNames = [ "d:/ymir work/ui/pattern/thinboardcircle/ThinBoard_Line_"+dir+"_Circle.tga" for dir in ["Left","Right","Top","Bottom"] ]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("attach")
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		Base = Bar()
		Base.SetParent(self)
		Base.AddFlag("attach")
		Base.AddFlag("not_pick")
		Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		Base.SetColor(self.BOARD_COLOR)
		Base.Show()
		self.Base = Base

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Base.SetSize(width - self.CORNER_WIDTH*2, height - self.CORNER_HEIGHT*2)

	def SetAlpha(self, alpha):
		color  = grp.GenerateColor(0.0, 0.0, 0.0, alpha)
		self.Base.SetColor(color)

	def ShowInternal(self):
		self.Base.Show()
		for wnd in self.Lines:
			wnd.Show()
		for wnd in self.Corners:
			wnd.Show()

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()

class ThinBoard(Window):

	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16
	BOARD_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.51)

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		CornerFileNames = [ "d:/ymir work/ui/pattern/ThinBoard_Corner_"+dir+".tga" for dir in ["LeftTop","LeftBottom","RightTop","RightBottom"] ]
		LineFileNames = [ "d:/ymir work/ui/pattern/ThinBoard_Line_"+dir+".tga" for dir in ["Left","Right","Top","Bottom"] ]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("attach")
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		Base = Bar()
		Base.SetParent(self)
		Base.AddFlag("attach")
		Base.AddFlag("not_pick")
		Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		Base.SetColor(self.BOARD_COLOR)
		Base.Show()
		self.Base = Base

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Base.SetSize(width - self.CORNER_WIDTH*2, height - self.CORNER_HEIGHT*2)

	def ShowInternal(self):
		self.Base.Show()
		for wnd in self.Lines:
			wnd.Show()
		for wnd in self.Corners:
			wnd.Show()

	if app.ENABLE_SEND_TARGET_INFO:
		def HideCorners(self, corner):
				self.Corners[corner].Hide()
				self.SetSize(self.GetWidth(), self.GetHeight())

		def ShowLine(self, line):
			self.Lines[line].Show()
			self.SetSize(self.GetWidth(), self.GetHeight())

		def HideLine(self, line):
			self.Lines[line].Hide()
			self.SetSize(self.GetWidth(), self.GetHeight())
			
	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()

class ThinBoardGold(Window):
	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16
	BOARD_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.51)

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		CornerFileNames = [ "d:/ymir work/ui/pattern/thinboardgold/ThinBoard_Corner_"+dir+".tga" for dir in ["LeftTop_gold", "LeftBottom_gold","RightTop_gold", "RightBottom_gold"]]
		LineFileNames = [ "d:/ymir work/ui/pattern/thinboardgold/ThinBoard_Line_"+dir+".tga" for dir in ["Left_gold", "Right_gold", "Top_gold", "Bottom_gold"]]
		
		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("attach")
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		Base = ExpandedImageBox()
		Base.SetParent(self)
		Base.AddFlag("attach")
		Base.AddFlag("not_pick")
		Base.LoadImage("d:/ymir work/ui/pattern/thinboardgold/thinboard_bg_gold.tga")
		Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		Base.Show()
		self.Base = Base

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		if self.Base:
			self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

	def ShowInternal(self):
		self.Base.Show()
		for wnd in self.Lines:
			wnd.Show()
		for wnd in self.Corners:
			wnd.Show()

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()
			
class CheckBox3(Window):
	def __init__(self):
		Window.__init__(self)
		
		self.backgroundImage = None
		self.checkImage = None

		self.eventFunc = { "ON_CHECK" : None, "ON_UNCHECK" : None, }
		self.eventArgs = { "ON_CHECK" : None, "ON_UNCHECK" : None, }
	
		self.CreateElements()
		
	def __del__(self):
		Window.__del__(self)
		
		self.backgroundImage = None
		self.checkImage = None
		
		self.eventFunc = { "ON_CHECK" : None, "ON_UNCHECK" : None, }
		self.eventArgs = { "ON_CHECK" : None, "ON_UNCHECK" : None, }
		
	def CreateElements(self):
		self.backgroundImage = ImageBox()
		self.backgroundImage.SetParent(self)
		self.backgroundImage.AddFlag("not_pick")
		self.backgroundImage.SetPosition(0,0)
		self.backgroundImage.LoadImage("d:/ymir work/ui/game/refine/checkbox.tga")
		self.backgroundImage.Show()
		
		self.checkImage = ImageBox()
		self.checkImage.SetParent(self)
		self.checkImage.AddFlag("not_pick")
		self.checkImage.SetPosition(0, -4)
		self.checkImage.LoadImage("d:/ymir work/ui/game/refine/checked.tga")
		self.checkImage.Hide()
		
		self.textInfo = TextLine()
		self.textInfo.SetParent(self)
		self.textInfo.SetPosition(20, -2)
		self.textInfo.Show()
		
		self.SetSize(self.backgroundImage.GetWidth() + self.textInfo.GetTextSize()[0], self.backgroundImage.GetHeight() + self.textInfo.GetTextSize()[1])
		
	def SetTextInfo(self, info):
		if self.textInfo:
			self.textInfo.SetText(info)
			
		self.SetSize(self.backgroundImage.GetWidth() + self.textInfo.GetTextSize()[0], self.backgroundImage.GetHeight() + self.textInfo.GetTextSize()[1])
		
	def SetCheckStatus(self, flag):
		if flag:
			self.checkImage.Show()
		else:
			self.checkImage.Hide()
	
	def GetCheckStatus(self):
		if self.checkImage:
			return self.checkImage.IsShow()
			
		return False
		
	def SetEvent(self, func, *args) :
		result = self.eventFunc.has_key(args[0])		
		if result :
			self.eventFunc[args[0]] = func
			self.eventArgs[args[0]] = args
		else :
			print "[ERROR] ui.py SetEvent, Can`t Find has_key : %s" % args[0]
		
	def OnMouseLeftButtonUp(self):
		if self.checkImage:
			if self.checkImage.IsShow():
				self.checkImage.Hide()

				if self.eventFunc["ON_UNCHECK"]:
					apply(self.eventFunc["ON_UNCHECK"], self.eventArgs["ON_UNCHECK"])
			else:
				self.checkImage.Show()

				if self.eventFunc["ON_CHECK"]:
					apply(self.eventFunc["ON_CHECK"], self.eventArgs["ON_CHECK"])
			
class ScrollBar(Window):

	SCROLLBAR_WIDTH = 17
	SCROLLBAR_MIDDLE_HEIGHT = 9
	SCROLLBAR_BUTTON_WIDTH = 17
	SCROLLBAR_BUTTON_HEIGHT = 17
	MIDDLE_BAR_POS = 5
	MIDDLE_BAR_UPPER_PLACE = 3
	MIDDLE_BAR_DOWNER_PLACE = 4
	TEMP_SPACE = MIDDLE_BAR_UPPER_PLACE + MIDDLE_BAR_DOWNER_PLACE

	class MiddleBar(DragButton):
		def __init__(self):
			DragButton.__init__(self)
			self.AddFlag("movable")
			#self.AddFlag("restrict_x")

		def MakeImage(self):
			top = ImageBox()
			top.SetParent(self)
			top.LoadImage("d:/ymir work/ui/pattern/ScrollBar_Top.tga")
			top.SetPosition(0, 0)
			top.AddFlag("not_pick")
			top.Show()
			bottom = ImageBox()
			bottom.SetParent(self)
			bottom.LoadImage("d:/ymir work/ui/pattern/ScrollBar_Bottom.tga")
			bottom.AddFlag("not_pick")
			bottom.Show()

			middle = ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage("d:/ymir work/ui/pattern/ScrollBar_Middle.tga")
			middle.SetPosition(0, 4)
			middle.AddFlag("not_pick")
			middle.Show()

			self.top = top
			self.bottom = bottom
			self.middle = middle

		def SetSize(self, height):
			height = max(12, height)
			DragButton.SetSize(self, 10, height)
			self.bottom.SetPosition(0, height-4)

			height -= 4*3
			self.middle.SetRenderingRect(0, 0, 0, float(height)/4.0)

	def __init__(self):
		Window.__init__(self)

		if app.ENABLE_WINDOW_SLIDE_EFFECT:
			self.SetSpecialWindow()

		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = lambda *arg: None
		self.lockFlag = False
		self.scrollStep = 0.20


		self.CreateScrollBar()

	def __del__(self):
		Window.__del__(self)

	def CreateScrollBar(self):
		barSlot = Bar3D()
		barSlot.SetParent(self)
		barSlot.AddFlag("not_pick")
		barSlot.Show()

		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.MakeImage()
		middleBar.SetSize(12)

		upButton = Button()
		upButton.SetParent(self)
		upButton.SetEvent(__mem_func__(self.OnUp))
		upButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_up_button_01.sub")
		upButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_up_button_02.sub")
		upButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_up_button_03.sub")
		upButton.Show()

		downButton = Button()
		downButton.SetParent(self)
		downButton.SetEvent(__mem_func__(self.OnDown))
		downButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_down_button_01.sub")
		downButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_down_button_02.sub")
		downButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_down_button_03.sub")
		downButton.Show()

		self.upButton = upButton
		self.downButton = downButton
		self.middleBar = middleBar
		self.barSlot = barSlot

		self.SCROLLBAR_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
		self.SCROLLBAR_BUTTON_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_BUTTON_HEIGHT = self.upButton.GetHeight()

	def Destroy(self):
		self.middleBar = None
		self.upButton = None
		self.downButton = None
		self.eventScroll = lambda *arg: None

	def SetScrollEvent(self, event):
		self.eventScroll = event

	def SetMiddleBarSize(self, pageScale):
		realHeight = self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2
		self.SCROLLBAR_MIDDLE_HEIGHT = int(pageScale * float(realHeight))
		self.middleBar.SetSize(self.SCROLLBAR_MIDDLE_HEIGHT)
		self.pageSize = (self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)

	def SetScrollBarSize(self, height):
		self.pageSize = (height - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)
		self.SetSize(self.SCROLLBAR_WIDTH, height)
		self.upButton.SetPosition(0, 0)
		self.downButton.SetPosition(0, height - self.SCROLLBAR_BUTTON_HEIGHT)
		self.middleBar.SetRestrictMovementArea(self.MIDDLE_BAR_POS, self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE, self.MIDDLE_BAR_POS+2, height - self.SCROLLBAR_BUTTON_HEIGHT*2 - self.TEMP_SPACE)
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, 0)

		self.UpdateBarSlot()

	def UpdateBarSlot(self):
		self.barSlot.SetPosition(0, self.SCROLLBAR_BUTTON_HEIGHT)
		self.barSlot.SetSize(self.GetWidth() - 2, self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2 - 2)

	def GetPos(self):
		return self.curPos

	def SetPos(self, pos):
		pos = max(0.0, pos)
		pos = min(1.0, pos)

		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, int(newPos) + self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE)
		self.OnMove()

	def SetScrollStep(self, step):
		self.scrollStep = step

	def GetScrollStep(self):
		return self.scrollStep

	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep)

	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep)

	def OnMove(self):

		if self.lockFlag:
			return

		if 0 == self.pageSize:
			return

		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal - self.SCROLLBAR_BUTTON_HEIGHT - self.MIDDLE_BAR_UPPER_PLACE) / float(self.pageSize)

		self.eventScroll()

	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		pickedPos = yMouseLocalPosition - self.SCROLLBAR_BUTTON_HEIGHT - self.SCROLLBAR_MIDDLE_HEIGHT/2
		newPos = float(pickedPos) / float(self.pageSize)
		self.SetPos(newPos)

	def LockScroll(self):
		self.lockFlag = True

	def UnlockScroll(self):
		self.lockFlag = False

	if app.BL_MAILBOX:
		def SetUpButtonSizeRefresh(self):
			self.SCROLLBAR_WIDTH			= self.upButton.GetWidth()
			self.SCROLLBAR_BUTTON_WIDTH		= self.upButton.GetWidth()
			self.SCROLLBAR_BUTTON_HEIGHT	= self.upButton.GetHeight()
		
		def SetUpButtonUpVisual(self, img_path):
			if self.upButton:
				self.upButton.SetUpVisual( img_path )
		def SetUpButtonOverVisual(self, img_path):
			if self.upButton:
				self.upButton.SetOverVisual( img_path )
		def SetUpButtonDownVisual(self, img_path):
			if self.upButton:
				self.upButton.SetDownVisual( img_path )
		def SetDownButtonUpVisual(self, img_path):
			if self.downButton:
				self.downButton.SetUpVisual( img_path )
		def SetDownButtonOverVisual(self, img_path):
			if self.downButton:
				self.downButton.SetOverVisual( img_path )
		def SetDownButtonDownVisual(self, img_path):
			if self.downButton:
				self.downButton.SetDownVisual( img_path )

	def OnMouseWheel(self, nLen):
		if nLen > 0:
			self.OnUp()
			return True
		elif nLen < 0:
			self.OnDown()
			return True
		return False

class ThinScrollBar(ScrollBar):

	def CreateScrollBar(self):
		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.SetUpVisual("d:/ymir work/ui/public/scrollbar_thin_middle_button_01.sub")
		middleBar.SetOverVisual("d:/ymir work/ui/public/scrollbar_thin_middle_button_02.sub")
		middleBar.SetDownVisual("d:/ymir work/ui/public/scrollbar_thin_middle_button_03.sub")

		upButton = Button()
		upButton.SetParent(self)
		upButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_thin_up_button_01.sub")
		upButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_thin_up_button_02.sub")
		upButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_thin_up_button_03.sub")
		upButton.SetEvent(__mem_func__(self.OnUp))
		upButton.Show()

		downButton = Button()
		downButton.SetParent(self)
		downButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_01.sub")
		downButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_02.sub")
		downButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_03.sub")
		downButton.SetEvent(__mem_func__(self.OnDown))
		downButton.Show()

		self.middleBar = middleBar
		self.upButton = upButton
		self.downButton = downButton

		self.SCROLLBAR_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
		self.SCROLLBAR_BUTTON_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_BUTTON_HEIGHT = self.upButton.GetHeight()
		self.MIDDLE_BAR_POS = 0
		self.MIDDLE_BAR_UPPER_PLACE = 0
		self.MIDDLE_BAR_DOWNER_PLACE = 0
		self.TEMP_SPACE = 0

	def UpdateBarSlot(self):
		pass
		
class ScrollBar_New(Window):

	SCROLLBAR_WIDTH = 17
	SCROLLBAR_MIDDLE_HEIGHT = 9
	SCROLLBAR_BUTTON_WIDTH = 17
	SCROLLBAR_BUTTON_HEIGHT = 17
	MIDDLE_BAR_POS = 5
	MIDDLE_BAR_UPPER_PLACE = 3
	MIDDLE_BAR_DOWNER_PLACE = 4
	TEMP_SPACE = MIDDLE_BAR_UPPER_PLACE + MIDDLE_BAR_DOWNER_PLACE

	class MiddleBar(DragButton):
		def __init__(self):
			DragButton.__init__(self)
			self.AddFlag("movable")
			#self.AddFlag("restrict_x")

		def MakeImage(self):
			top = ImageBox()
			top.SetParent(self)
			top.LoadImage("d:/ymir work/ui/pattern/ScrollBar_New_Top.tga")
			top.SetPosition(0, 0)
			top.AddFlag("not_pick")
			top.Show()
			bottom = ImageBox()
			bottom.SetParent(self)
			bottom.LoadImage("d:/ymir work/ui/pattern/ScrollBar_New_Bottom.tga")
			bottom.AddFlag("not_pick")
			bottom.Show()

			middle = ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage("d:/ymir work/ui/pattern/ScrollBar_New_Middle.tga")
			middle.SetPosition(0, 4)
			middle.AddFlag("not_pick")
			middle.Show()

			self.top = top
			self.bottom = bottom
			self.middle = middle

		def SetSize(self, height):
			height = max(12, height)
			DragButton.SetSize(self, 10, height)
			self.bottom.SetPosition(0, height-4)

			height -= 4*3
			self.middle.SetRenderingRect(0, 0, 0, float(height)/4.0)

	def __init__(self):
		Window.__init__(self)

		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = lambda *arg: None
		self.lockFlag = False
		self.scrollStep = 0.20


		self.CreateScrollBar_New()

	def __del__(self):
		Window.__del__(self)

	def CreateScrollBar_New(self):
		barSlot = Bar3D()
		barSlot.SetParent(self)
		barSlot.AddFlag("not_pick")
		# barSlot.Show()

		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.MakeImage()
		middleBar.SetSize(12)

		upButton = Button()
		upButton.SetParent(self)
		upButton.SetEvent(__mem_func__(self.OnUp))
		upButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_up_button_01.sub")
		upButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_up_button_02.sub")
		upButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_up_button_03.sub")
		# upButton.Show()

		downButton = Button()
		downButton.SetParent(self)
		downButton.SetEvent(__mem_func__(self.OnDown))
		downButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_down_button_01.sub")
		downButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_down_button_02.sub")
		downButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_down_button_03.sub")
		# downButton.Show()

		self.upButton = upButton
		self.downButton = downButton
		self.middleBar = middleBar
		self.barSlot = barSlot

		self.SCROLLBAR_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
		self.SCROLLBAR_BUTTON_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_BUTTON_HEIGHT = self.upButton.GetHeight()

	def Destroy(self):
		self.middleBar = None
		self.upButton = None
		self.downButton = None
		self.eventScroll = lambda *arg: None

	def SetScrollEvent(self, event):
		self.eventScroll = event

	def SetMiddleBarSize(self, pageScale):
		realHeight = self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2
		self.SCROLLBAR_MIDDLE_HEIGHT = int(pageScale * float(realHeight))
		self.middleBar.SetSize(self.SCROLLBAR_MIDDLE_HEIGHT)
		self.pageSize = (self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)

	def SetScrollBarSize(self, height):
		self.pageSize = (height - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)
		self.SetSize(self.SCROLLBAR_WIDTH, height)
		self.upButton.SetPosition(0, 0)
		self.downButton.SetPosition(0, height - self.SCROLLBAR_BUTTON_HEIGHT)
		self.middleBar.SetRestrictMovementArea(self.MIDDLE_BAR_POS, self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE, self.MIDDLE_BAR_POS+2, height - self.SCROLLBAR_BUTTON_HEIGHT*2 - self.TEMP_SPACE)
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, 0)

		self.UpdateBarSlot()

	def UpdateBarSlot(self):
		self.barSlot.SetPosition(0, self.SCROLLBAR_BUTTON_HEIGHT)
		self.barSlot.SetSize(self.GetWidth() - 2, self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2 - 2)

	def GetPos(self):
		return self.curPos

	def SetPos(self, pos):
		pos = max(0.0, pos)
		pos = min(1.0, pos)

		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, int(newPos) + self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE)
		self.OnMove()

	def SetScrollStep(self, step):
		self.scrollStep = step

	def GetScrollStep(self):
		return self.scrollStep

	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep)

	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep)

	def OnMove(self):

		if self.lockFlag:
			return

		if 0 == self.pageSize:
			return

		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal - self.SCROLLBAR_BUTTON_HEIGHT - self.MIDDLE_BAR_UPPER_PLACE) / float(self.pageSize)

		self.eventScroll()

	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		pickedPos = yMouseLocalPosition - self.SCROLLBAR_BUTTON_HEIGHT - self.SCROLLBAR_MIDDLE_HEIGHT/2
		newPos = float(pickedPos) / float(self.pageSize)
		self.SetPos(newPos)

	def LockScroll(self):
		self.lockFlag = True

	def UnlockScroll(self):
		self.lockFlag = False
		
class ScrollBar2(Window):

	SCROLLBAR_WIDTH = 13
	SCROLLBAR_MIDDLE_HEIGHT = 1
	SCROLLBAR_BUTTON_WIDTH = 17
	SCROLLBAR_BUTTON_HEIGHT = 17
	SCROLL_BTN_XDIST = 2
	SCROLL_BTN_YDIST = 2

	class MiddleBar(DragButton):
		def __init__(self):
			DragButton.__init__(self)
			self.AddFlag("movable")

			self.SetWindowName("scrollbar_middlebar")

		def MakeImage(self):
			top = ImageBox()
			top.SetParent(self)
			top.LoadImage("d:/ymir work/battle_pass/scrollbar/scrollbar_middle_top.tga")
			top.AddFlag("not_pick")
			top.Show()
			topScale = ExpandedImageBox()
			topScale.SetParent(self)
			topScale.SetPosition(0, top.GetHeight())
			topScale.LoadImage("d:/ymir work/battle_pass/scrollbar/scrollbar_middle_topscale.tga")
			topScale.AddFlag("not_pick")
			topScale.Show()

			bottom = ImageBox()
			bottom.SetParent(self)
			bottom.LoadImage("d:/ymir work/battle_pass/scrollbar/scrollbar_middle_bottom.tga")
			bottom.AddFlag("not_pick")
			bottom.Show()
			bottomScale = ExpandedImageBox()
			bottomScale.SetParent(self)
			bottomScale.LoadImage("d:/ymir work/battle_pass/scrollbar/scrollbar_middle_bottomscale.tga")
			bottomScale.AddFlag("not_pick")
			bottomScale.Show()

			middle = ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage("d:/ymir work/battle_pass/scrollbar/scrollbar_middle_middle.tga")
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
			DragButton.SetSize(self, 10, height)

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
		Window.__init__(self)

		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = None
		self.eventArgs = None
		self.lockFlag = False

		self.CreateScrollBar()
		self.SetScrollBarSize(0)

		self.scrollStep = 0.20
		self.SetWindowName("NONAME_ScrollBar")

	def __del__(self):
		Window.__del__(self)

	def CreateScrollBar(self):
		topImage = ImageBox()
		topImage.SetParent(self)
		topImage.AddFlag("not_pick")
		topImage.LoadImage("d:/ymir work/battle_pass/scrollbar/scrollbar_top.tga")
		topImage.Show()
		bottomImage = ImageBox()
		bottomImage.SetParent(self)
		bottomImage.AddFlag("not_pick")
		bottomImage.LoadImage("d:/ymir work/battle_pass/scrollbar/scrollbar_bottom.tga")
		bottomImage.Show()
		middleImage = ExpandedImageBox()
		middleImage.SetParent(self)
		middleImage.AddFlag("not_pick")
		middleImage.SetPosition(0, topImage.GetHeight())
		middleImage.LoadImage("d:/ymir work/battle_pass/scrollbar/scrollbar_middle.tga")
		middleImage.Show()
		self.topImage = topImage
		self.bottomImage = bottomImage
		self.middleImage = middleImage

		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(__mem_func__(self.OnMove))
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

		self.middleBar.SetRestrictMovementArea(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST, \
			self.middleBar.GetWidth(), height - self.SCROLL_BTN_YDIST * 2)
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

class SmallThinScrollBar(ScrollBar):

	def CreateScrollBar(self):
		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.SetUpVisual("d:/ymir work/ui/public/scrollbar_small_thin_middle_button_01.sub")
		middleBar.SetOverVisual("d:/ymir work/ui/public/scrollbar_small_thin_middle_button_01.sub")
		middleBar.SetDownVisual("d:/ymir work/ui/public/scrollbar_small_thin_middle_button_01.sub")

		upButton = Button()
		upButton.SetParent(self)
		upButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_small_thin_up_button_01.sub")
		upButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_small_thin_up_button_02.sub")
		upButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_small_thin_up_button_03.sub")
		upButton.SetEvent(__mem_func__(self.OnUp))
		upButton.Show()

		downButton = Button()
		downButton.SetParent(self)
		downButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_small_thin_down_button_01.sub")
		downButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_small_thin_down_button_02.sub")
		downButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_small_thin_down_button_03.sub")
		downButton.SetEvent(__mem_func__(self.OnDown))
		downButton.Show()

		self.middleBar = middleBar
		self.upButton = upButton
		self.downButton = downButton

		self.SCROLLBAR_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
		self.SCROLLBAR_BUTTON_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_BUTTON_HEIGHT = self.upButton.GetHeight()
		self.MIDDLE_BAR_POS = 0
		self.MIDDLE_BAR_UPPER_PLACE = 0
		self.MIDDLE_BAR_DOWNER_PLACE = 0
		self.TEMP_SPACE = 0

	def UpdateBarSlot(self):
		pass

class SliderBar(Window):

	def __init__(self):
		Window.__init__(self)

		self.curPos = 1.0
		self.pageSize = 1.0
		self.eventChange = None

		self.__CreateBackGroundImage()
		self.__CreateCursor()

	def __del__(self):
		Window.__del__(self)

	def __CreateBackGroundImage(self):
		if app.ENABLE_NEW_GAMEOPTION:
			img = ExpandedImageBox()
		else:
			img = ImageBox()
		img.SetParent(self)
		img.LoadImage("d:/ymir work/ui/game/windows/sliderbar.sub")
		img.Show()
		self.backGroundImage = img

		##
		self.SetSize(self.backGroundImage.GetWidth(), self.backGroundImage.GetHeight())

	def __CreateCursor(self):
		cursor = DragButton()
		cursor.AddFlag("movable")
		cursor.AddFlag("restrict_y")
		cursor.SetParent(self)
		cursor.SetMoveEvent(__mem_func__(self.__OnMove))
		cursor.SetUpVisual("d:/ymir work/ui/game/windows/sliderbar_cursor.sub")
		cursor.SetOverVisual("d:/ymir work/ui/game/windows/sliderbar_cursor.sub")
		cursor.SetDownVisual("d:/ymir work/ui/game/windows/sliderbar_cursor.sub")
		cursor.Show()
		self.cursor = cursor

		##
		self.cursor.SetRestrictMovementArea(0, 0, self.backGroundImage.GetWidth(), 0)
		self.pageSize = self.backGroundImage.GetWidth() - self.cursor.GetWidth()

	def __OnMove(self):
		(xLocal, yLocal) = self.cursor.GetLocalPosition()
		self.curPos = float(xLocal) / float(self.pageSize)

		if self.eventChange:
			self.eventChange()

	def SetSliderPos(self, pos):
		self.curPos = pos
		self.cursor.SetPosition(int(self.pageSize * pos), 0)

	def GetSliderPos(self):
		return self.curPos

	def SetEvent(self, event):
		self.eventChange = event

	def Enable(self):
		self.cursor.Show()

	def Disable(self):
		self.cursor.Hide()

	if app.ENABLE_FOV_OPTION:
		def SetBackgroundVisual(self, filename):
			if self.backGroundImage:
				self.backGroundImage.LoadImage(filename)

				self.SetSize(self.backGroundImage.GetWidth(), self.backGroundImage.GetHeight())
				self.pageSize = self.backGroundImage.GetWidth() - self.cursor.GetWidth()

			if self.cursor:
				self.cursor.SetRestrictMovementArea(0, 0, self.backGroundImage.GetWidth(), 0)

		def SetButtonVisual(self, path, up, over, down):
			if self.cursor:
				self.cursor.SetUpVisual(path + up)
				self.cursor.SetOverVisual(path + over)
				self.cursor.SetDownVisual(path + down)


class ListBox(Window):

	TEMPORARY_PLACE = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		self.overLine = -1
		self.selectedLine = -1
		self.width = 0
		self.height = 0
		self.stepSize = 17
		self.basePos = 0
		self.showLineCount = 0
		self.itemCenterAlign = True
		self.itemList = []
		self.keyDict = {}
		self.textDict = {}
		self.event = lambda *arg: None
	def __del__(self):
		Window.__del__(self)

	def SetWidth(self, width):
		self.SetSize(width, self.height)

	def SetSize(self, width, height):
		Window.SetSize(self, width, height)
		self.width = width
		self.height = height

	def SetTextCenterAlign(self, flag):
		self.itemCenterAlign = flag

	def SetBasePos(self, pos):
		self.basePos = pos
		self._LocateItem()

	def ClearItem(self):
		self.keyDict = {}
		self.textDict = {}
		self.itemList = []
		self.overLine = -1
		self.selectedLine = -1

	def InsertItem(self, number, text):
		self.keyDict[len(self.itemList)] = number
		self.textDict[len(self.itemList)] = text

		textLine = TextLine()
		textLine.SetParent(self)
		textLine.SetText(text)
		textLine.Show()

		if self.itemCenterAlign:
			textLine.SetWindowHorizontalAlignCenter()
			textLine.SetHorizontalAlignCenter()

		self.itemList.append(textLine)

		self._LocateItem()

	def ChangeItem(self, number, text):
		for key, value in self.keyDict.items():
			if value == number:
				self.textDict[key] = text

				if number < len(self.itemList):
					self.itemList[key].SetText(text)

				return

	def LocateItem(self):
		self._LocateItem()

	def _LocateItem(self):

		skipCount = self.basePos
		yPos = 0
		self.showLineCount = 0

		for textLine in self.itemList:
			textLine.Hide()

			if skipCount > 0:
				skipCount -= 1
				continue

			if localeInfo.IsARABIC():
				w, h = textLine.GetTextSize()
				textLine.SetPosition(w+10, yPos + 3)
			else:
				textLine.SetPosition(0, yPos + 3)

			yPos += self.stepSize

			if yPos <= self.GetHeight():
				self.showLineCount += 1
				textLine.Show()

	def ArrangeItem(self):
		self.SetSize(self.width, len(self.itemList) * self.stepSize)
		self._LocateItem()

	def GetViewItemCount(self):
		return int(self.GetHeight() / self.stepSize)

	def GetItemCount(self):
		return len(self.itemList)

	def SetEvent(self, event):
		self.event = event

	def SelectItem(self, line):

		if not self.keyDict.has_key(line):
			return

		if line == self.selectedLine:
			return

		self.selectedLine = line
		self.event(self.keyDict.get(line, 0), self.textDict.get(line, "None"))

	def GetSelectedItem(self):
		return self.keyDict.get(self.selectedLine, 0)

	def OnMouseLeftButtonDown(self):
		if self.overLine < 0:
			return

	def OnMouseLeftButtonUp(self):
		if self.overLine >= 0:
			self.SelectItem(self.overLine+self.basePos)

	def OnUpdate(self):

		self.overLine = -1

		if self.IsIn():
			x, y = self.GetGlobalPosition()
			height = self.GetHeight()
			xMouse, yMouse = wndMgr.GetMousePosition()

			if yMouse - y < height - 1:
				self.overLine = (yMouse - y) / self.stepSize

				if self.overLine < 0:
					self.overLine = -1
				if self.overLine >= len(self.itemList):
					self.overLine = -1

	def OnRender(self):
		xRender, yRender = self.GetGlobalPosition()
		yRender -= self.TEMPORARY_PLACE
		widthRender = self.width
		heightRender = self.height + self.TEMPORARY_PLACE*2

		if localeInfo.IsCIBN10:
			if -1 != self.overLine and self.keyDict[self.overLine] != -1:
				grp.SetColor(HALF_WHITE_COLOR)
				grp.RenderBar(xRender + 2, yRender + self.overLine*self.stepSize + 4, self.width - 3, self.stepSize)

			if -1 != self.selectedLine and self.keyDict[self.selectedLine] != -1:
				if self.selectedLine >= self.basePos:
					if self.selectedLine - self.basePos < self.showLineCount:
						grp.SetColor(SELECT_COLOR)
						grp.RenderBar(xRender + 2, yRender + (self.selectedLine-self.basePos)*self.stepSize + 4, self.width - 3, self.stepSize)

		else:
			if -1 != self.overLine:
				grp.SetColor(HALF_WHITE_COLOR)
				grp.RenderBar(xRender + 2, yRender + self.overLine*self.stepSize + 4, self.width - 3, self.stepSize)

			if -1 != self.selectedLine:
				if self.selectedLine >= self.basePos:
					if self.selectedLine - self.basePos < self.showLineCount:
						grp.SetColor(SELECT_COLOR)
						grp.RenderBar(xRender + 2, yRender + (self.selectedLine-self.basePos)*self.stepSize + 4, self.width - 3, self.stepSize)



class ListBox2(ListBox):
	def __init__(self, *args, **kwargs):
		ListBox.__init__(self, *args, **kwargs)
		self.rowCount = 10
		self.barWidth = 0
		self.colCount = 0

	def SetRowCount(self, rowCount):
		self.rowCount = rowCount

	def SetSize(self, width, height):
		ListBox.SetSize(self, width, height)
		self._RefreshForm()

	def ClearItem(self):
		ListBox.ClearItem(self)
		self._RefreshForm()

	def InsertItem(self, *args, **kwargs):
		ListBox.InsertItem(self, *args, **kwargs)
		self._RefreshForm()

	def OnUpdate(self):
		mpos = wndMgr.GetMousePosition()
		self.overLine = self._CalcPointIndex(mpos)

	def OnRender(self):
		x, y = self.GetGlobalPosition()
		pos = (x + 2, y)

		if -1 != self.overLine:
			grp.SetColor(HALF_WHITE_COLOR)
			self._RenderBar(pos, self.overLine)

		if -1 != self.selectedLine:
			if self.selectedLine >= self.basePos:
				if self.selectedLine - self.basePos < self.showLineCount:
					grp.SetColor(SELECT_COLOR)
					self._RenderBar(pos, self.selectedLine-self.basePos)



	def _CalcPointIndex(self, mpos):
		if self.IsIn():
			px, py = mpos
			gx, gy = self.GetGlobalPosition()
			lx, ly = px - gx, py - gy

			col = lx / self.barWidth
			row = ly / self.stepSize
			idx = col * self.rowCount + row
			if col >= 0 and col < self.colCount:
				if row >= 0 and row < self.rowCount:
					if idx >= 0 and idx < len(self.itemList):
						return idx

		return -1

	def _CalcRenderPos(self, pos, idx):
		x, y = pos
		row = idx % self.rowCount
		col = idx / self.rowCount
		return (x + col * self.barWidth, y + row * self.stepSize)

	def _RenderBar(self, basePos, idx):
		x, y = self._CalcRenderPos(basePos, idx)
		grp.RenderBar(x, y, self.barWidth - 3, self.stepSize)

	def _LocateItem(self):
		pos = (0, self.TEMPORARY_PLACE)

		self.showLineCount = 0
		for textLine in self.itemList:
			x, y = self._CalcRenderPos(pos, self.showLineCount)
			textLine.SetPosition(x, y)
			textLine.Show()

			self.showLineCount += 1

	def _RefreshForm(self):
		if len(self.itemList) % self.rowCount:
			self.colCount = len(self.itemList) / self.rowCount + 1
		else:
			self.colCount = len(self.itemList) / self.rowCount

		if self.colCount:
			self.barWidth = self.width / self.colCount
		else:
			self.barWidth = self.width


class ComboBox(Window):

	class ListBoxWithBoard(ListBox):

		def __init__(self, layer):
			ListBox.__init__(self, layer)

		def OnRender(self):
			xRender, yRender = self.GetGlobalPosition()
			yRender -= self.TEMPORARY_PLACE
			widthRender = self.width
			heightRender = self.height + self.TEMPORARY_PLACE*2
			grp.SetColor(BACKGROUND_COLOR)
			grp.RenderBar(xRender, yRender, widthRender, heightRender)
			grp.SetColor(DARK_COLOR)
			grp.RenderLine(xRender, yRender, widthRender, 0)
			grp.RenderLine(xRender, yRender, 0, heightRender)
			grp.SetColor(BRIGHT_COLOR)
			grp.RenderLine(xRender, yRender+heightRender, widthRender, 0)
			grp.RenderLine(xRender+widthRender, yRender, 0, heightRender)

			ListBox.OnRender(self)

	def __init__(self):
		Window.__init__(self)
		self.x = 0
		self.y = 0
		self.width = 0
		self.height = 0
		self.isSelected = False
		self.isOver = False
		self.isListOpened = False
		self.event = lambda *arg: None
		self.enable = True

		self.textLine = MakeTextLine(self)
		self.textLine.SetText(localeInfo.UI_ITEM)

		self.listBox = self.ListBoxWithBoard("TOP_MOST")
		self.listBox.SetPickAlways()
		self.listBox.SetParent(self)
		self.listBox.SetEvent(__mem_func__(self.OnSelectItem))
		self.listBox.Hide()

	def __del__(self):
		Window.__del__(self)

	def Destroy(self):
		self.textLine = None
		self.listBox = None

	def SetPosition(self, x, y):
		Window.SetPosition(self, x, y)
		self.x = x
		self.y = y
		self.__ArrangeListBox()

	def SetSize(self, width, height):
		Window.SetSize(self, width, height)
		self.width = width
		self.height = height
		self.textLine.UpdateRect()
		self.__ArrangeListBox()

	def __ArrangeListBox(self):
		self.listBox.SetPosition(0, self.height + 5)
		self.listBox.SetWidth(self.width)

	def Enable(self):
		self.enable = True

	def Disable(self):
		self.enable = False
		self.textLine.SetText("")
		self.CloseListBox()

	def SetEvent(self, event):
		self.event = event

	def ClearItem(self):
		self.CloseListBox()
		self.listBox.ClearItem()

	def InsertItem(self, index, name):
		self.listBox.InsertItem(index, name)
		self.listBox.ArrangeItem()

	def SetCurrentItem(self, text):
		self.textLine.SetText(text)

	def SelectItem(self, key):
		self.listBox.SelectItem(key)

	def OnSelectItem(self, index, name):

		self.CloseListBox()
		self.event(index)

	def CloseListBox(self):
		self.isListOpened = False
		self.listBox.Hide()

	def OnMouseLeftButtonDown(self):

		if not self.enable:
			return

		self.isSelected = True

	def OnMouseLeftButtonUp(self):

		if not self.enable:
			return

		self.isSelected = False

		if self.isListOpened:
			self.CloseListBox()
		else:
			if self.listBox.GetItemCount() > 0:
				self.isListOpened = True
				self.listBox.Show()
				self.__ArrangeListBox()

	def OnUpdate(self):

		if not self.enable:
			return

		if self.IsIn():
			self.isOver = True
		else:
			self.isOver = False

	def OnRender(self):
		self.x, self.y = self.GetGlobalPosition()
		xRender = self.x
		yRender = self.y
		widthRender = self.width
		heightRender = self.height
		grp.SetColor(BACKGROUND_COLOR)
		grp.RenderBar(xRender, yRender, widthRender, heightRender)
		grp.SetColor(DARK_COLOR)
		grp.RenderLine(xRender, yRender, widthRender, 0)
		grp.RenderLine(xRender, yRender, 0, heightRender)
		grp.SetColor(BRIGHT_COLOR)
		grp.RenderLine(xRender, yRender+heightRender, widthRender, 0)
		grp.RenderLine(xRender+widthRender, yRender, 0, heightRender)

		if self.isOver:
			grp.SetColor(HALF_WHITE_COLOR)
			grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)

			if self.isSelected:
				grp.SetColor(WHITE_COLOR)
				grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)

class ComboBoxImage(Window):
	class ListBoxWithBoard(ListBox):

		def __init__(self, layer):
			ListBox.__init__(self, layer)

		def OnRender(self):
			xRender, yRender = self.GetGlobalPosition()
			yRender -= self.TEMPORARY_PLACE
			widthRender = self.width
			heightRender = self.height + self.TEMPORARY_PLACE*2
			grp.SetColor(BACKGROUND_COLOR)
			grp.RenderBar(xRender, yRender, widthRender, heightRender)
			grp.SetColor(DARK_COLOR)
			grp.RenderLine(xRender, yRender, widthRender, 0)
			grp.RenderLine(xRender, yRender, 0, heightRender)
			ListBox.OnRender(self)

	def __init__(self, parent, name, x ,y):
		Window.__init__(self)
		self.isSelected = False
		self.isOver = False
		self.isListOpened = False
		self.event = lambda *arg: None
		self.enable = True
		self.imagebox = None
		
		## imagebox
		image = ImageBox()
		image.SetParent(parent)
		image.LoadImage(name)
		image.SetPosition(x, y)
		image.Show()
		self.imagebox = image
		
		## BaseSetting
		self.x = x + 1
		self.y = y + 1
		self.width = self.imagebox.GetWidth() - 3
		self.height = self.imagebox.GetHeight() - 3
		self.SetParent(parent)

		## TextLine
		self.textLine = MakeTextLine(self)
		self.textLine.SetText(localeInfo.UI_ITEM)
		
		## ListBox
		self.listBox = self.ListBoxWithBoard("TOP_MOST")
		self.listBox.SetPickAlways()
		self.listBox.SetParent(self)
		self.listBox.SetEvent(__mem_func__(self.OnSelectItem))
		self.listBox.Hide()

		Window.SetPosition(self, self.x, self.y)
		Window.SetSize(self, self.width, self.height)
		self.textLine.UpdateRect()
		self.__ArrangeListBox()
		
	def __del__(self):
		Window.__del__(self)

	def Destroy(self):
		self.textLine = None
		self.listBox = None
		self.imagebox = None

	def SetPosition(self, x, y):
		Window.SetPosition(self, x, y)
		self.imagebox.SetPosition(x, y)
		self.x = x
		self.y = y
		self.__ArrangeListBox()

	def SetSize(self, width, height):
		Window.SetSize(self, width, height)
		self.width = width
		self.height = height
		self.textLine.UpdateRect()
		self.__ArrangeListBox()

	def __ArrangeListBox(self):
		self.listBox.SetPosition(0, self.height + 5)
		self.listBox.SetWidth(self.width)

	def Enable(self):
		self.enable = True

	def Disable(self):
		self.enable = False
		self.textLine.SetText("")
		self.CloseListBox()

	def SetEvent(self, event):
		self.event = event

	def ClearItem(self):
		self.CloseListBox()
		self.listBox.ClearItem()

	def InsertItem(self, index, name):
		self.listBox.InsertItem(index, name)
		self.listBox.ArrangeItem()

	def SetCurrentItem(self, text):
		self.textLine.SetText(text)

	def SelectItem(self, key):
		self.listBox.SelectItem(key)

	def OnSelectItem(self, index, name):
		self.CloseListBox()
		self.event(index)

	def CloseListBox(self):
		self.isListOpened = False
		self.listBox.Hide()

	def OnMouseLeftButtonDown(self):
	
		if not self.enable:
			return

		self.isSelected = True

	def OnMouseLeftButtonUp(self):
		if not self.enable:
			return
		
		self.isSelected = False
		
		if self.isListOpened:
			self.CloseListBox()
		else:
			if self.listBox.GetItemCount() > 0:
				self.isListOpened = True
				self.listBox.Show()
				self.__ArrangeListBox()

	def OnUpdate(self):

		if not self.enable:
			return

		if self.IsIn():
			self.isOver = True
		else:
			self.isOver = False

	def OnRender(self):
		self.x, self.y = self.GetGlobalPosition()
		xRender = self.x
		yRender = self.y
		widthRender = self.width
		heightRender = self.height
		if self.isOver:
			grp.SetColor(HALF_WHITE_COLOR)
			grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)
			if self.isSelected:
				grp.SetColor(WHITE_COLOR)
				grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)


###################################################################################################
## Python Script Loader
###################################################################################################

class ScriptWindow(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		self.Children = []
		self.ElementDictionary = {}
	def __del__(self):
		Window.__del__(self)

	def ClearDictionary(self):
		self.Children = []
		self.ElementDictionary = {}
	def InsertChild(self, name, child):
		self.ElementDictionary[name] = child

	def IsChild(self, name):
		return self.ElementDictionary.has_key(name)
	def GetChild(self, name):
		return self.ElementDictionary[name]

	def GetChild2(self, name):
		return self.ElementDictionary.get(name, None)


class PythonScriptLoader(object):

	BODY_KEY_LIST = ( "x", "y", "width", "height" )

	#####

	DEFAULT_KEY_LIST = ( "type", "x", "y", )
	WINDOW_KEY_LIST = ( "width", "height", )
	IMAGE_KEY_LIST = ( "image", )
	EXPANDED_IMAGE_KEY_LIST = ( "image", )
	ANI_IMAGE_KEY_LIST = ( "images", )
	SLOT_KEY_LIST = ( "width", "height", "slot", )
	CANDIDATE_LIST_KEY_LIST = ( "item_step", "item_xsize", "item_ysize", )
	GRID_TABLE_KEY_LIST = ( "start_index", "x_count", "y_count", "x_step", "y_step", )
	EDIT_LINE_KEY_LIST = ( "width", "height", "input_limit", )
	COMBO_BOX_KEY_LIST = ( "width", "height", "item", )
	TITLE_BAR_KEY_LIST = ( "width", )
	HORIZONTAL_BAR_KEY_LIST = ( "width", )
	BOARD_KEY_LIST = ( "width", "height", )
	BOARD_WITH_TITLEBAR_KEY_LIST = ( "width", "height", "title", )
	BOX_KEY_LIST = ( "width", "height", )
	BAR_KEY_LIST = ( "width", "height", )
	LINE_KEY_LIST = ( "width", "height", )
	SLOTBAR_KEY_LIST = ( "width", "height", )
	GAUGE_KEY_LIST = ( "width", "color", )
	SCROLLBAR_KEY_LIST = ( "size", )
	LIST_BOX_KEY_LIST = ( "width", "height", )
	if app.BL_MAILBOX:
		RENDER_BOX_KEY_LIST = ( "color", )

	if app.ENABLE_QUEST_RENEWAL:
		SUB_TITLE_BAR_KEY_LIST = ( "width", )
		LIST_BAR_KEY_LIST = ( "width", )
	if app.RENDER_TARGET:
		RENDER_TARGET_KEY_LIST = ( "index", )

	def __init__(self):
		self.Clear()

	def Clear(self):
		self.ScriptDictionary = { "SCREEN_WIDTH" : wndMgr.GetScreenWidth(), "SCREEN_HEIGHT" : wndMgr.GetScreenHeight() }
		self.InsertFunction = 0

	def LoadScriptFile(self, window, FileName):
		import exception
		import exceptions
		import os
		import errno
		self.Clear()

		print "===== Load Script File : %s" % (FileName)

		#ui �ڵ�� sandbox ������ ����Ǿ���Ѵ�.(���� ������ ������ �ֱ� ������)
		import sys
		from utils import Sandbox
		sandbox = Sandbox(True, ["uiScriptLocale", "localeInfo", "sys", "item", "app", "player"])

		# chr, player ���� sandbox ������ import�� ������ �ʱ� ������,(���� �ǿ��� ������ �ſ� ŭ.)
		#  �̸� script dictionary�� �ʿ��� ����� �־���´�.
		import chr
		import player
		import app
		self.ScriptDictionary["PLAYER_NAME_MAX_LEN"] = chr.PLAYER_NAME_MAX_LEN
		self.ScriptDictionary["DRAGON_SOUL_EQUIPMENT_SLOT_START"] = player.DRAGON_SOUL_EQUIPMENT_SLOT_START
		self.ScriptDictionary["LOCALE_PATH"] = app.GetLocalePath()

		if __USE_EXTRA_CYTHON__:
			# sub functions
			from os.path import splitext as op_splitext, basename as op_basename, dirname as op_dirname
			def GetModName(filename):
				return op_splitext(op_basename(filename))[0]
			def IsInUiPath(filename):
				def ICmp(s1, s2):
					return s1.lower() == s2.lower()
				return ICmp(op_dirname(filename), "uiscript")
			# module name to import
			modname = GetModName(FileName)
			# lazy loading of uiscriptlib
			import uiscriptlib
			# copy scriptdictionary stuff to builtin scope (otherwise, import will fail)
			tpl2Main = (
				"SCREEN_WIDTH","SCREEN_HEIGHT",
				"PLAYER_NAME_MAX_LEN", "DRAGON_SOUL_EQUIPMENT_SLOT_START","LOCALE_PATH"
			)
			import __builtin__ as bt
			for idx in tpl2Main:
				tmpVal = self.ScriptDictionary[idx]
				exec "bt.%s = tmpVal"%idx in globals(), locals()
			# debug stuff
			import dbg
			dbg.TraceError("Loading %s (%s %s)"%(FileName, GetModName(FileName), IsInUiPath(FileName)))
		try:
			if __USE_EXTRA_CYTHON__ and IsInUiPath(FileName) and uiscriptlib.isExist(modname):
				m1 = uiscriptlib.moduleImport(modname)
				self.ScriptDictionary["window"] = m1.window.copy()
				del m1
			else:
				sandbox.execfile(FileName, self.ScriptDictionary)
		except IOError, err:
			import sys
			import dbg
			dbg.TraceError("Failed to load script file : %s" % (FileName))
			dbg.TraceError("error  : %s" % (err))
			exception.Abort("LoadScriptFile1")
		except RuntimeError,err:
			import sys
			import dbg
			dbg.TraceError("Failed to load script file : %s" % (FileName))
			dbg.TraceError("error  : %s" % (err))
			exception.Abort("LoadScriptFile2")
		except:
			import sys
			import dbg
			dbg.TraceError("Failed to load script file : %s" % (FileName))
			exception.Abort("LoadScriptFile!!!!!!!!!!!!!!")

		#####

		Body = self.ScriptDictionary["window"]
		self.CheckKeyList("window", Body, self.BODY_KEY_LIST)

		window.ClearDictionary()
		self.InsertFunction = window.InsertChild

		window.SetPosition(int(Body["x"]), int(Body["y"]))

		if localeInfo.IsARABIC():
			w = wndMgr.GetScreenWidth()
			h = wndMgr.GetScreenHeight()
			if Body.has_key("width"):
				w = int(Body["width"])
			if Body.has_key("height"):
				h = int(Body["height"])

			window.SetSize(w, h)
		else:
			window.SetSize(int(Body["width"]), int(Body["height"]))
			if True == Body.has_key("style"):
				for StyleList in Body["style"]:
					window.AddFlag(StyleList)


		self.LoadChildren(window, Body)

	def LoadChildren(self, parent, dicChildren):

		if localeInfo.IsARABIC():
			parent.AddFlag( "rtl" )

		if True == dicChildren.has_key("style"):
			for style in dicChildren["style"]:
				parent.AddFlag(style)

		if False == dicChildren.has_key("children"):
			return False

		Index = 0

		ChildrenList = dicChildren["children"]
		parent.Children = range(len(ChildrenList))
		for ElementValue in ChildrenList:
			try:
				Name = ElementValue["name"]
			except KeyError:
				Name = ElementValue["name"] = "NONAME"

			try:
				Type = ElementValue["type"]
			except KeyError:
				Type = ElementValue["type"] = "window"

			if False == self.CheckKeyList(Name, ElementValue, self.DEFAULT_KEY_LIST):
				del parent.Children[Index]
				continue

			if Type == "window":
				parent.Children[Index] = ScriptWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementWindow(parent.Children[Index], ElementValue, parent)

			#if app.RENDER_TARGET:
			elif Type == "render_target":
				parent.Children[Index] = RenderTarget()
				parent.Children[Index].SetParent(parent)
				self.LoadElementRenderTarget(parent.Children[Index], ElementValue, parent)

			elif Type == "button":
				parent.Children[Index] = Button()
				parent.Children[Index].SetParent(parent)
				self.LoadElementButton(parent.Children[Index], ElementValue, parent)

			elif Type == "radio_button":
				parent.Children[Index] = RadioButton()
				parent.Children[Index].SetParent(parent)
				self.LoadElementButton(parent.Children[Index], ElementValue, parent)

			elif Type == "toggle_button":
				parent.Children[Index] = ToggleButton()
				parent.Children[Index].SetParent(parent)
				self.LoadElementButton(parent.Children[Index], ElementValue, parent)

			elif Type == "mark":
				parent.Children[Index] = MarkBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementMark(parent.Children[Index], ElementValue, parent)

			elif Type == "image":
				parent.Children[Index] = ImageBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementImage(parent.Children[Index], ElementValue, parent)

			elif Type == "expanded_image":
				parent.Children[Index] = ExpandedImageBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementExpandedImage(parent.Children[Index], ElementValue, parent)

			elif Type == "ani_image":
				parent.Children[Index] = AniImageBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementAniImage(parent.Children[Index], ElementValue, parent)

			elif Type == "slot":
				parent.Children[Index] = SlotWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSlot(parent.Children[Index], ElementValue, parent)

			elif Type == "candidate_list":
				parent.Children[Index] = CandidateListBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementCandidateList(parent.Children[Index], ElementValue, parent)

			elif Type == "grid_table":
				parent.Children[Index] = GridSlotWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementGridTable(parent.Children[Index], ElementValue, parent)

			elif Type == "text":
				parent.Children[Index] = TextLine()
				parent.Children[Index].SetParent(parent)
				self.LoadElementText(parent.Children[Index], ElementValue, parent)

			elif Type == "extended_text":
				parent.Children[Index] = ExtendedTextLine()
				parent.Children[Index].SetParent(parent)
				self.LoadElementExtendedText(parent.Children[Index], ElementValue, parent)
				
			elif Type == "textboxmultiline":
					parent.Children[Index] = TextBoxMultiLine()
					parent.Children[Index].SetParent(parent)
					self.LoadElementTexBoxMultiline(parent.Children[Index], ElementValue, parent)
			elif Type == "checkbox":
				parent.Children[Index] = CheckBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementCheckBox(parent.Children[Index], ElementValue, parent)

			elif Type == "checkBox_classic":
				parent.Children[Index] = CheckBox_Classic()
				parent.Children[Index].SetParent(parent)
				self.LoadElementCheckBox(parent.Children[Index], ElementValue, parent)

			elif Type == "editline":
				parent.Children[Index] = EditLine()
				parent.Children[Index].SetParent(parent)
				self.LoadElementEditLine(parent.Children[Index], ElementValue, parent)

			elif Type == "titlebar":
				parent.Children[Index] = TitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "horizontalbar":
				parent.Children[Index] = HorizontalBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementHorizontalBar(parent.Children[Index], ElementValue, parent)

			elif Type == "board":
				parent.Children[Index] = Board()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "board_with_titlebar_without_button":
				parent.Children[Index] = BoardWithTitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoardWithTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "new_scrollbar":
				parent.Children[Index] = NewScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "board_brown":
				parent.Children[Index] = Board_Brown()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "board_with_titlebar":
				parent.Children[Index] = BoardWithTitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoardWithTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "border_a":
				parent.Children[Index] = BorderA()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBorderA(parent.Children[Index], ElementValue, parent)

			elif Type == "thinboard":
				parent.Children[Index] = ThinBoard()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "thinboard_gold":
				parent.Children[Index] = ThinBoardGold()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoardGold(parent.Children[Index], ElementValue, parent)

			elif Type == "thinboard_circle":
				parent.Children[Index] = ThinBoardCircle()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "prettyboard":
				parent.Children[Index] = PrettyBoard()
				parent.Children[Index].SetParent(parent)
				self.LoadElementPrettyBoard(parent.Children[Index], ElementValue, parent)
				
			elif Type == "box":
				parent.Children[Index] = Box()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBox(parent.Children[Index], ElementValue, parent)

			elif Type == "bar":
				parent.Children[Index] = Bar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBar(parent.Children[Index], ElementValue, parent)

			elif Type == "line":
				parent.Children[Index] = Line()
				parent.Children[Index].SetParent(parent)
				self.LoadElementLine(parent.Children[Index], ElementValue, parent)

			elif Type == "slotbar":
				parent.Children[Index] = SlotBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSlotBar(parent.Children[Index], ElementValue, parent)

			elif Type == "gauge":
				parent.Children[Index] = Gauge()
				parent.Children[Index].SetParent(parent)
				self.LoadElementGauge(parent.Children[Index], ElementValue, parent)

			elif Type == "scrollbar":
				parent.Children[Index] = ScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "scrollbar2":
				parent.Children[Index] = ScrollBar2()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "thin_scrollbar":
				parent.Children[Index] = ThinScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "small_thin_scrollbar":
				parent.Children[Index] = SmallThinScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "scrollbar_search":
				parent.Children[Index] = ScrollBar_New()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)


			elif Type == "sliderbar":
				parent.Children[Index] = SliderBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSliderBar(parent.Children[Index], ElementValue, parent)

			elif Type == "listbox":
				parent.Children[Index] = ListBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBox(parent.Children[Index], ElementValue, parent)
				
			elif Type == "combobox":
				parent.Children[Index] = ComboBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementComboBox(parent.Children[Index], ElementValue, parent)

			elif Type == "listbox2":
				parent.Children[Index] = ListBox2()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBox2(parent.Children[Index], ElementValue, parent)
			elif Type == "listboxex":
				parent.Children[Index] = ListBoxEx()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBoxEx(parent.Children[Index], ElementValue, parent)
			elif app.BL_MAILBOX and Type == "renderbox":
				parent.Children[Index] = RenderBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementRenderBox(parent.Children[Index], ElementValue, parent)				
			elif Type == "subtitlebar" and app.ENABLE_QUEST_RENEWAL:
				parent.Children[Index] = SubTitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSubTitleBar(parent.Children[Index], ElementValue, parent)

			#if app.WON_EXCHANGE:
			elif Type == "editline_centered":
				parent.Children[Index] = EditLineCentered()
				parent.Children[Index].SetParent(parent)
				self.LoadElementEditLine(parent.Children[Index], ElementValue, parent)

			elif Type == "listbar" and app.ENABLE_QUEST_RENEWAL:
				parent.Children[Index] = ListBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBar(parent.Children[Index], ElementValue, parent)
			else:
				Index += 1
				continue

			parent.Children[Index].SetWindowName(Name)
			if 0 != self.InsertFunction:
				self.InsertFunction(Name, parent.Children[Index])

			self.LoadChildren(parent.Children[Index], ElementValue)
			Index += 1

	if app.ENABLE_KILL_STATISTICS:
		def LoadElementThinBoardCircle(self, window, value, parentWindow):

			if False == self.CheckKeyList(value["name"], value, self.BOARD_KEY_LIST):
				return False

			window.SetSize(int(value["width"]), int(value["height"]))
			self.LoadDefaultData(window, value, parentWindow)

			return True

	def CheckKeyList(self, name, value, key_list):

		for DataKey in key_list:
			if False == value.has_key(DataKey):
				print "Failed to find data key", "[" + name + "/" + DataKey + "]"
				return False

		return True

	def LoadDefaultData(self, window, value, parentWindow):
		loc_x = int(value["x"])
		loc_y = int(value["y"])
		if value.has_key("vertical_align"):
			if "center" == value["vertical_align"]:
				window.SetWindowVerticalAlignCenter()
			elif "bottom" == value["vertical_align"]:
				window.SetWindowVerticalAlignBottom()

		if parentWindow.IsRTL():
			loc_x = int(value["x"]) + window.GetWidth()
			if value.has_key("horizontal_align"):
				if "center" == value["horizontal_align"]:
					window.SetWindowHorizontalAlignCenter()
					loc_x = - int(value["x"])
				elif "right" == value["horizontal_align"]:
					window.SetWindowHorizontalAlignLeft()
					loc_x = int(value["x"]) - window.GetWidth()
					## loc_x = parentWindow.GetWidth() - int(value["x"]) + window.GetWidth()
			else:
				window.SetWindowHorizontalAlignRight()

			if value.has_key("all_align"):
				window.SetWindowVerticalAlignCenter()
				window.SetWindowHorizontalAlignCenter()
				loc_x = - int(value["x"])
		else:
			if value.has_key("horizontal_align"):
				if "center" == value["horizontal_align"]:
					window.SetWindowHorizontalAlignCenter()
				elif "right" == value["horizontal_align"]:
					window.SetWindowHorizontalAlignRight()

		window.SetPosition(loc_x, loc_y)
		window.Show()

	## Window
	def LoadElementWindow(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.WINDOW_KEY_LIST):
			return False

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Button
	def LoadElementButton(self, window, value, parentWindow):

		if value.has_key("width") and value.has_key("height"):
			window.SetSize(int(value["width"]), int(value["height"]))

		if True == value.has_key("default_image"):
			window.SetUpVisual(value["default_image"])
		if True == value.has_key("over_image"):
			window.SetOverVisual(value["over_image"])
		if True == value.has_key("down_image"):
			window.SetDownVisual(value["down_image"])
		if True == value.has_key("disable_image"):
			window.SetDisableVisual(value["disable_image"])

		if True == value.has_key("text"):
			if True == value.has_key("text_height"):
				window.SetText(value["text"], value["text_height"])
			elif TRUE == value.has_key("text_x") and app.ENABLE_NEW_GAMEOPTION:
				window.SetListText(value["text"], value["text_x"])
			else:
				window.SetText(value["text"])

			if value.has_key("text_color"):
				window.SetTextColor(value["text_color"])

		if True == value.has_key("tooltip_text"):
			if True == value.has_key("tooltip_x") and True == value.has_key("tooltip_y"):
				window.SetToolTipText(value["tooltip_text"], int(value["tooltip_x"]), int(value["tooltip_y"]))
			else:
				window.SetToolTipText(value["tooltip_text"])

		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Mark
	def LoadElementMark(self, window, value, parentWindow):

		#if False == self.CheckKeyList(value["name"], value, self.MARK_KEY_LIST):
		#	return False

		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Image
	def LoadElementImage(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.IMAGE_KEY_LIST):
			return False

		window.LoadImage(value["image"])
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## AniImage
	def LoadElementAniImage(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.ANI_IMAGE_KEY_LIST):
			return False

		if True == value.has_key("delay"):
			window.SetDelay(value["delay"])

		xs = 0
		ys = 0

		for image in value["images"]:
			window.AppendImage(image, xs, ys)

		if True == value.has_key("x_scale") and True == value.has_key("y_scale"):
			window.SetScale(float(value["x_scale"]), float(value["y_scale"]))

		if value.has_key("width") and value.has_key("height"):
			window.SetSize(value["width"], value["height"])

		self.LoadDefaultData(window, value, parentWindow)

		return True
	## Expanded Image
	def LoadElementExpandedImage(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.EXPANDED_IMAGE_KEY_LIST):
			return False

		window.LoadImage(value["image"])

		if True == value.has_key("x_origin") and True == value.has_key("y_origin"):
			window.SetOrigin(float(value["x_origin"]), float(value["y_origin"]))

		if True == value.has_key("x_scale") and True == value.has_key("y_scale"):
			window.SetScale(float(value["x_scale"]), float(value["y_scale"]))

		if True == value.has_key("rect"):
			RenderingRect = value["rect"]
			window.SetRenderingRect(RenderingRect[0], RenderingRect[1], RenderingRect[2], RenderingRect[3])

		if True == value.has_key("mode"):
			mode = value["mode"]
			if "MODULATE" == mode:
				window.SetRenderingMode(wndMgr.RENDERING_MODE_MODULATE)

		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Slot
	def LoadElementSlot(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.SLOT_KEY_LIST):
			return False

		global_x = int(value["x"])
		global_y = int(value["y"])
		global_width = int(value["width"])
		global_height = int(value["height"])

		window.SetPosition(global_x, global_y)
		window.SetSize(global_width, global_height)
		window.Show()

		r = 1.0
		g = 1.0
		b = 1.0
		a = 1.0

		if True == value.has_key("image_r") and \
			True == value.has_key("image_g") and \
			True == value.has_key("image_b") and \
			True == value.has_key("image_a"):
			r = float(value["image_r"])
			g = float(value["image_g"])
			b = float(value["image_b"])
			a = float(value["image_a"])

		SLOT_ONE_KEY_LIST = ("index", "x", "y", "width", "height")

		for slot in value["slot"]:
			if True == self.CheckKeyList(value["name"] + " - one", slot, SLOT_ONE_KEY_LIST):
				wndMgr.AppendSlot(window.hWnd,
									int(slot["index"]),
									int(slot["x"]),
									int(slot["y"]),
									int(slot["width"]),
									int(slot["height"]))

		if TRUE == value.has_key("image"):
			if TRUE == value.has_key("x_scale") and TRUE == value.has_key("y_scale"):
				wndMgr.SetSlotBaseImageScale(window.hWnd,
										value["image"],
										r, g, b, a, float(value["x_scale"]), float(value["y_scale"]))
			else:
				wndMgr.SetSlotBaseImage(window.hWnd,
										value["image"],
										r, g, b, a)

		return True

	def LoadElementCandidateList(self, window, value, parentWindow):
		if False == self.CheckKeyList(value["name"], value, self.CANDIDATE_LIST_KEY_LIST):
			return False

		window.SetPosition(int(value["x"]), int(value["y"]))
		window.SetItemSize(int(value["item_xsize"]), int(value["item_ysize"]))
		window.SetItemStep(int(value["item_step"]))
		window.Show()

		return True

	## Table
	def LoadElementGridTable(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.GRID_TABLE_KEY_LIST):
			return False

		xBlank = 0
		yBlank = 0
		if True == value.has_key("x_blank"):
			xBlank = int(value["x_blank"])
		if True == value.has_key("y_blank"):
			yBlank = int(value["y_blank"])

		if localeInfo.IsARABIC():
			pass
		else:
			window.SetPosition(int(value["x"]), int(value["y"]))

		window.ArrangeSlot(	int(value["start_index"]),
							int(value["x_count"]),
							int(value["y_count"]),
							int(value["x_step"]),
							int(value["y_step"]),
							xBlank,
							yBlank)
		if True == value.has_key("image"):
			r = 1.0
			g = 1.0
			b = 1.0
			a = 1.0
			if True == value.has_key("image_r") and \
				True == value.has_key("image_g") and \
				True == value.has_key("image_b") and \
				True == value.has_key("image_a"):
				r = float(value["image_r"])
				g = float(value["image_g"])
				b = float(value["image_b"])
				a = float(value["image_a"])
			wndMgr.SetSlotBaseImage(window.hWnd, value["image"], r, g, b, a)

		if True == value.has_key("style"):
			if "select" == value["style"]:
				wndMgr.SetSlotStyle(window.hWnd, wndMgr.SLOT_STYLE_SELECT)
		if localeInfo.IsARABIC():
			self.LoadDefaultData(window, value, parentWindow)
		else:
			window.Show()

		return True

	##TexBoxMultiLine
	
	def LoadElementTexBoxMultiline(self, window, value, parentWindow):
	
		self.LoadDefaultData(window, value, parentWindow)
		return True
	## Text
	def LoadElementText(self, window, value, parentWindow):

		if value.has_key("fontsize"):
			fontSize = value["fontsize"]

			if "LARGE" == fontSize:
				window.SetFontName(localeInfo.UI_DEF_FONT_LARGE)
			elif "ULTRA_LARGE" == fontSize:
				window.SetFontName(localeInfo.UI_DEF_FONT_ULTRA)

		elif value.has_key("fontname"):
			fontName = value["fontname"]
			window.SetFontName(fontName)

		if value.has_key("text_horizontal_align"):
			if "left" == value["text_horizontal_align"]:
				window.SetHorizontalAlignLeft()
			elif "center" == value["text_horizontal_align"]:
				window.SetHorizontalAlignCenter()
			elif "right" == value["text_horizontal_align"]:
				window.SetHorizontalAlignRight()

		if value.has_key("text_vertical_align"):
			if "top" == value["text_vertical_align"]:
				window.SetVerticalAlignTop()
			elif "center" == value["text_vertical_align"]:
				window.SetVerticalAlignCenter()
			elif "bottom" == value["text_vertical_align"]:
				window.SetVerticalAlignBottom()

		if value.has_key("all_align"):
			window.SetHorizontalAlignCenter()
			window.SetVerticalAlignCenter()
			window.SetWindowHorizontalAlignCenter()
			window.SetWindowVerticalAlignCenter()

		if value.has_key("r") and value.has_key("g") and value.has_key("b"):
			window.SetFontColor(float(value["r"]), float(value["g"]), float(value["b"]))
		elif value.has_key("color"):
			window.SetPackedFontColor(value["color"])
		else:
			window.SetFontColor(0.8549, 0.8549, 0.8549)

		if value.has_key("outline"):
			if value["outline"]:
				window.SetOutline()
		if True == value.has_key("text"):
			window.SetText(value["text"])

		self.LoadDefaultData(window, value, parentWindow)

		return True
	## CheckBox
	def LoadElementCheckBox(self, window, value, parentWindow):

		if value.has_key("text"):
			window.SetText(value["text"])

		if value.has_key("checked") and value["checked"] == True:
			window.SetChecked(window.STATE_SELECTED)

		if value.has_key("disabled") and value["disabled"] == True:
			window.Disable()

		self.LoadDefaultData(window, value, parentWindow)

		return True

	## EditLine
	if app.ENABLE_MAINTENANCE_SYSTEM:	
		## ExtendedTextLine
		def LoadElementExtendedText(self, window, value, parentWindow):

			if TRUE == value.has_key("text"):
				window.SetText(value["text"])

			self.LoadDefaultData(window, value, parentWindow)

			return TRUE	
	
	
	def LoadElementEditLine(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.EDIT_LINE_KEY_LIST):
			return False


		if value.has_key("secret_flag"):
			window.SetSecret(value["secret_flag"])
		if value.has_key("with_codepage"):
			if value["with_codepage"]:
				window.bCodePage = True
		if value.has_key("only_number"):
			if value["only_number"]:
				window.SetNumberMode()
		if value.has_key("enable_codepage"):
			window.SetIMEFlag(value["enable_codepage"])
		if value.has_key("enable_ime"):
			window.SetIMEFlag(value["enable_ime"])
		if value.has_key("limit_width"):
			window.SetLimitWidth(value["limit_width"])
		if value.has_key("multi_line"):
			if value["multi_line"]:
				window.SetMultiLine()

		window.SetMax(int(value["input_limit"]))
		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadElementText(window, value, parentWindow)

		return True

	if app.RENDER_TARGET:
		def LoadElementRenderTarget(self, window, value, parentWindow):
			if False == self.CheckKeyList(value["name"], value, self.RENDER_TARGET_KEY_LIST):
				return False
			window.SetSize(value["width"], value["height"])

			if True == value.has_key("style"):
				for style in value["style"]:
					window.AddFlag(style)
			self.LoadDefaultData(window, value, parentWindow)
			if value.has_key("index"):
				window.SetRenderTarget(int(value["index"]))
			return True

	## TitleBar
	def LoadElementTitleBar(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.TITLE_BAR_KEY_LIST):
			return False

		window.MakeTitleBar(int(value["width"]), value.get("color", "red"))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## HorizontalBar
	def LoadElementHorizontalBar(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.HORIZONTAL_BAR_KEY_LIST):
			return False

		window.Create(int(value["width"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Board
	def LoadElementBoard(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.BOARD_KEY_LIST):
			return False

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Board With TitleBar
	def LoadElementBoardWithTitleBar(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.BOARD_WITH_TITLEBAR_KEY_LIST):
			return False

		window.SetSize(int(value["width"]), int(value["height"]))
		window.SetTitleName(value["title"])
		self.LoadDefaultData(window, value, parentWindow)

		return True

	def LoadElementBorderA(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.BOARD_KEY_LIST):
			return False

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## ThinBoard
	def LoadElementThinBoard(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.BOARD_KEY_LIST):
			return False

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True
		
	def LoadElementThinBoardGold(self, window, value, parentWindow):
		if FALSE == self.CheckKeyList(value["name"], value, self.BOARD_KEY_LIST):
			return FALSE
		
		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)
		return TRUE		

	if app.ENABLE_QUEST_RENEWAL:
		## SubTitleBar
		def LoadElementSubTitleBar(self, window, value, parentWindow):
			if False == self.CheckKeyList(value["name"], value, self.SUB_TITLE_BAR_KEY_LIST):
				return False

			window.MakeSubTitleBar(int(value["width"]), value.get("color", "red"))
			self.LoadElementButton(window, value, parentWindow)
			window.Show()
			return True

		## ListBar
		def LoadElementListBar(self, window, value, parentWindow):
			if False == self.CheckKeyList(value["name"], value, self.LIST_BAR_KEY_LIST):
				return False

			window.MakeListBar(int(value["width"]), value.get("color", "red"))
			self.LoadElementButton(window, value, parentWindow)

			return True

	## PrettyBoard
	def LoadElementPrettyBoard(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.BOARD_KEY_LIST):
			return False

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True
		
	## Box
	def LoadElementBox(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.BOX_KEY_LIST):
			return False

		if True == value.has_key("color"):
			window.SetColor(value["color"])

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Bar
	def LoadElementBar(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.BAR_KEY_LIST):
			return False

		if True == value.has_key("color"):
			window.SetColor(value["color"])

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Line
	def LoadElementLine(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.LINE_KEY_LIST):
			return False

		if True == value.has_key("color"):
			window.SetColor(value["color"])

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Slot
	def LoadElementSlotBar(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.SLOTBAR_KEY_LIST):
			return False

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Gauge
	def LoadElementGauge(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.GAUGE_KEY_LIST):
			return False

		window.MakeGauge(value["width"], value["color"])
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## ScrollBar
	def LoadElementScrollBar(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.SCROLLBAR_KEY_LIST):
			return False

		window.SetScrollBarSize(value["size"])
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## SliderBar
	def LoadElementSliderBar(self, window, value, parentWindow):

		self.LoadDefaultData(window, value, parentWindow)

		return True

	## ListBox
	def LoadElementListBox(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.LIST_BOX_KEY_LIST):
			return False

		if value.has_key("item_align"):
			window.SetTextCenterAlign(value["item_align"])

		window.SetSize(value["width"], value["height"])
		self.LoadDefaultData(window, value, parentWindow)

		return True
		
	def LoadElementComboBox(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.COMBO_BOX_KEY_LIST):
			return FALSE

		window.SetSize(value["width"], value["height"])
		self.LoadDefaultData(window, value, parentWindow)

		if value.has_key("default_text"):
			window.textLine.SetText(value["default_text"])

		c = 0
		for cbitem in value["item"]:
			window.InsertItem(c, cbitem)
			c += 1

	## ListBox2
	def LoadElementListBox2(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.LIST_BOX_KEY_LIST):
			return False

		window.SetRowCount(value.get("row_count", 10))
		window.SetSize(value["width"], value["height"])
		self.LoadDefaultData(window, value, parentWindow)

		if value.has_key("item_align"):
			window.SetTextCenterAlign(value["item_align"])

		return True
	def LoadElementListBoxEx(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.LIST_BOX_KEY_LIST):
			return False

		window.SetSize(value["width"], value["height"])
		self.LoadDefaultData(window, value, parentWindow)

		if value.has_key("itemsize_x") and value.has_key("itemsize_y"):
			window.SetItemSize(int(value["itemsize_x"]), int(value["itemsize_y"]))

		if value.has_key("itemstep"):
			window.SetItemStep(int(value["itemstep"]))

		if value.has_key("viewcount"):
			window.SetViewItemCount(int(value["viewcount"]))

		return True

	if app.BL_MAILBOX:
		def	LoadElementRenderBox(self, window, value, parentWindow):
			if False == self.CheckKeyList(value["name"], value, self.RENDER_BOX_KEY_LIST):
				return False
			
			window.SetSize(value["width"], value["height"])
			self.LoadDefaultData(window, value, parentWindow)
			
			if value.has_key("color"):
				window.SetColor(int(value["color"]))
				
			return True

class CheckBox_Classic(ImageBox):
	def __init__(self, parent = None, x = 0, y = 0, event = None, filename = "d:/ymir work/ui/public/Parameter_Slot_01.sub"):
		ImageBox.__init__(self)
		if parent:
			self.SetParent(parent)
		self.SetPosition(x, y)
		self.LoadImage(filename)

		self.mouseReflector = MouseReflector(self)
		self.mouseReflector.SetSize(self.GetWidth(), self.GetHeight())

		image = MakeImageBox(self, "d:/ymir work/ui/public/check_image.sub", 0, 0)
		image.AddFlag("not_pick")
		image.SetWindowHorizontalAlignCenter()
		image.SetWindowVerticalAlignCenter()
		image.Hide()
		self.enable = True
		self.image = image
		self.event = event
		self.Show()

		self.mouseReflector.UpdateRect()

	def __del__(self):
		ImageBox.__del__(self)
		
	def SetBackground(self, Image):
		self.LoadImage(Image)
		if not self.mouseReflector:
			self.mouseReflector = MouseReflector(self)
			
		self.mouseReflector.SetSize(self.GetWidth(), self.GetHeight())
		self.UpdateRect()
		
	def SetCheckEvent(self, event):
		self.event = event

	def SetCheck(self, flag):
		if flag:
			self.image.Show()
		else:
			self.image.Hide()

	def Disable(self):
		self.enable = False
		
	def Enable(self):
		self.enable = True

	def OnMouseOverIn(self):
		if not self.enable:
			return
		self.mouseReflector.Show()

	def OnMouseOverOut(self):
		if not self.enable:
			return
		self.mouseReflector.Hide()

	def OnMouseLeftButtonDown(self):
		if not self.enable:
			return
		self.mouseReflector.Down()

	def OnMouseLeftButtonUp(self):
		if not self.enable:
			return
		self.mouseReflector.Up()
		if self.event:
			self.event()

class ReadingWnd(Bar):

	def __init__(self):
		Bar.__init__(self,"TOP_MOST")

		self.__BuildText()
		self.SetSize(80, 19)
		self.Show()

	def __del__(self):
		Bar.__del__(self)

	def __BuildText(self):
		self.text = TextLine()
		self.text.SetParent(self)
		self.text.SetPosition(4, 3)
		self.text.Show()

	def SetText(self, text):
		self.text.SetText(text)

	def SetReadingPosition(self, x, y):
		xPos = x + 2
		yPos = y  - self.GetHeight() - 2
		self.SetPosition(xPos, yPos)

	def SetTextColor(self, color):
		self.text.SetPackedFontColor(color)


def MakeSlotBar(parent, x, y, width, height):
	slotBar = SlotBar()
	slotBar.SetParent(parent)
	slotBar.SetSize(width, height)
	slotBar.SetPosition(x, y)
	slotBar.Show()
	return slotBar

def MakeImageBox(parent, name, x, y):
	image = ImageBox()
	image.SetParent(parent)
	image.LoadImage(name)
	image.SetPosition(x, y)
	image.Show()
	return image
	
if app.ENABLE_OFFLINE_SHOP_SYSTEM:
	def MakeImageBoxPrivateShopSearch(parent, name, x, y):
		image = ImageBoxPrivateShop()
		image.SetParent(parent)
		image.LoadImage(name)
		image.SetPosition(x, y)
		image.Show()
		return image


def MakeGauge(parent, x, y, size):
	gauge_make = BattlePassGauge()
	gauge_make.SetParent(parent)
	gauge_make.MakeGauge(size, "bpass")
	gauge_make.SetPosition(x, y)
	gauge_make.Show()
	return gauge_make
	
def MakeImageBoxNoImg(parent, x, y):
	image = ImageBox()
	image.SetParent(parent)
	image.SetPosition(x, y)
	image.Show()
	return image
	
def MakeGridSlot(parent, x, y , vnum, count, y_grid = 1, Horizontal_Align = False):
	grid = GridSlotWindow()
	grid.SetParent(parent)
	grid.SetPosition(x, y)
	grid.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
	grid.ArrangeSlot(0, 1, y_grid, 32, 32, 0, 3)
	grid.SetItemSlot(0, vnum, count)
	grid.RefreshSlot()
	if Horizontal_Align == True:
		grid.SetWindowHorizontalAlignLeft()
		grid.SetWindowVerticalAlignCenter()
	grid.Show()
	return grid
	
def AddTextLine(parent, x, y, text, outline = 0):
	textLine = TextLine()
	textLine.SetParent(parent)
	textLine.SetPosition(x, y)
	if outline != 0:
		textLine.SetOutline()
	textLine.SetText(text)
	textLine.Show()
	return textLine

def MakeNewTextLine(parent, horizontalAlign = True, verticalAlgin = True, x = 0, y = 0):
	textLine = TextLine()
	textLine.SetParent(parent)

	if horizontalAlign == True:
		textLine.SetWindowHorizontalAlignCenter()

	if verticalAlgin == True:
		textLine.SetWindowVerticalAlignCenter()

	textLine.SetHorizontalAlignCenter()
	textLine.SetVerticalAlignCenter()

	if x != 0 and y != 0:
		textLine.SetPosition(x, y)

	textLine.Show()
	return textLine

def MakeExpandedImageBox(parent, name, x, y, flag = ""):
	image = ExpandedImageBox()
	image.SetParent(parent)
	image.LoadImage(name)
	image.SetPosition(x, y)

	if flag != "":
		image.AddFlag(flag)

	image.Show()

	return image

def MakeTextLine(parent):
	textLine = TextLine()
	textLine.SetParent(parent)
	textLine.SetWindowHorizontalAlignCenter()
	textLine.SetWindowVerticalAlignCenter()
	textLine.SetHorizontalAlignCenter()
	textLine.SetVerticalAlignCenter()
	textLine.Show()
	return textLine


def MakeText(parent, textlineText, x, y, color = None):
	textline = TextLine()
	if parent != None:
		textline.SetParent(parent)
	textline.SetPosition(x, y)
	if color != None:
		textline.SetFontColor(color[0], color[1], color[2])
	textline.SetText(textlineText)
	textline.Show()
	return textline
	
def MakeThinBoard(parent,  x, y, width, heigh, moveable=FALSE,center=FALSE):
	thin = ThinBoard()
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
def MakeButton(parent, x, y, tooltipText, path, up, over, down, btn = True):
	button = Button()
	button.SetParent(parent)
	button.SetPosition(x, y)
	button.SetUpVisual(path + up)
	button.SetOverVisual(path + over)
	button.SetDownVisual(path + down)
	button.SetToolTipText(tooltipText)
	if btn == True:
		button.Show()
	return button

def MakeButtonSearch(parent, x, y, tooltipText, path, up, over, down):
	button = Button()
	button.SetParent(parent)
	button.SetPosition(x, y)
	button.SetUpVisual(path + up)
	button.SetOverVisual(path + over)
	button.SetDownVisual(path + down)
	button.SetToolTipText(tooltipText)
	button.Show()
	return button

def MakeGridSlotSearch(parent, x, y , vnum, count):
	grid = GridSlotWindow()
	grid.SetParent(parent)
	grid.SetPosition(x, y)
	grid.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
	grid.ArrangeSlot(0, 1, 1, 32, 32, 0, 3)
	grid.SetItemSlot(0, vnum, count)
	grid.RefreshSlot()
	grid.Show()
	return grid

def RenderRoundBox(x, y, width, height, color):
	grp.SetColor(color)
	grp.RenderLine(x+2, y, width-3, 0)
	grp.RenderLine(x+2, y+height, width-3, 0)
	grp.RenderLine(x, y+2, 0, height-4)
	grp.RenderLine(x+width, y+1, 0, height-3)
	grp.RenderLine(x, y+2, 2, -2)
	grp.RenderLine(x, y+height-2, 2, 2)
	grp.RenderLine(x+width-2, y, 2, 2)
	grp.RenderLine(x+width-2, y+height, 2, -2)

def GenerateColor(r, g, b):
	r = float(r) / 255.0
	g = float(g) / 255.0
	b = float(b) / 255.0
	return grp.GenerateColor(r, g, b, 1.0)

def EnablePaste(flag):
	ime.EnablePaste(flag)

def GetHyperlink():
	return wndMgr.GetHyperlink()
	
def GetTextFromMousePos():
	return wndMgr.GetTextFromMousePos()

if app.ENABLE_KILL_STATISTICS:
	class ThinBoardCircle(Window):
		CORNER_WIDTH = 4
		CORNER_HEIGHT = 4
		LINE_WIDTH = 4
		LINE_HEIGHT = 4
		BOARD_COLOR = grp.GenerateColor(255.0, 255.0, 255.0, 1.0)
		
		BOARD_COLOR_IN = grp.GenerateColor(0.0, 0.0, 0.7, 0.7)
		BOARD_COLOR_OUT = grp.GenerateColor(0.0, 0.0, 0.0, 0.51)

		LT = 0
		LB = 1
		RT = 2
		RB = 3
		L = 0
		R = 1
		T = 2
		B = 3

		def __init__(self, layer = "UI"):
			Window.__init__(self, layer)

			CornerFileNames = [ "d:/ymir work/ui/pattern/thinboardcircle/ThinBoard_Corner_"+dir+".tga" for dir in ["LeftTop_circle","LeftBottom_circle","RightTop_circle","RightBottom_circle"] ]
			LineFileNames = [ "d:/ymir work/ui/pattern/thinboardcircle/ThinBoard_Line_"+dir+".tga" for dir in ["Left_circle","Right_circle","Top_circle","Bottom_circle"] ]

			self.Corners = []
			for fileName in CornerFileNames:
				Corner = ExpandedImageBox()
				Corner.AddFlag("attach")
				Corner.AddFlag("not_pick")
				Corner.LoadImage(fileName)
				Corner.SetParent(self)
				Corner.SetPosition(0, 0)
				Corner.Show()
				self.Corners.append(Corner)

			self.Lines = []
			for fileName in LineFileNames:
				Line = ExpandedImageBox()
				Line.AddFlag("attach")
				Line.AddFlag("not_pick")
				Line.LoadImage(fileName)
				Line.SetParent(self)
				Line.SetPosition(0, 0)
				Line.Show()
				self.Lines.append(Line)

			Base = Bar()
			Base.SetParent(self)
			Base.AddFlag("attach")
			Base.AddFlag("not_pick")
			Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
			Base.SetColor(self.BOARD_COLOR)
			Base.Show()
			self.Base = Base

			self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
			self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

		def __del__(self):
			Window.__del__(self)

		def SetSize(self, width, height):

			width = max(self.CORNER_WIDTH*2, width)
			height = max(self.CORNER_HEIGHT*2, height)
			Window.SetSize(self, width, height)

			self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
			self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
			self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
			self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
			self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

			verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
			horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
			self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
			self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
			self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
			self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
			self.Base.SetSize(width - self.CORNER_WIDTH*2, height - self.CORNER_HEIGHT*2)

		def SetColor(self, color):
			self.Base.SetColor(color)

		def SetAlpha(self, alpha):
			color  = grp.GenerateColor(0.0, 0.0, 0.0, alpha)
			self.Base.SetColor(color)
		def ShowInternal(self):
			self.Base.Show()
			for wnd in self.Lines:
				wnd.Show()
			for wnd in self.Corners:
				wnd.Show()

		def HideInternal(self):
			self.Base.Hide()
			for wnd in self.Lines:
				wnd.Hide()
			for wnd in self.Corners:
				wnd.Hide()

if app.INGAME_WIKI:
	class WikiRenderTarget(Window):
		def __init__(self):
			Window.__init__(self)
		
		def __del__(self):
			Window.__del__(self)
		
		def RegisterWindow(self, layer):
			self.hWnd = wndMgr.RegisterWikiRenderTarget(self, layer)
	
	class InGameWikiCheckBox(Window):
		def __init__(self):
			Window.__init__(self)
			
			self.backgroundImage = None
			self.checkImage = None
			
			self.eventFunc = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
			self.eventArgs = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
			
			self.CreateElements()
		
		def __del__(self):
			Window.__del__(self)
			
			self.backgroundImage = None
			self.checkImage = None
			
			self.eventFunc = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
			self.eventArgs = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
		
		def CreateElements(self):
			self.backgroundImage = ImageBox()
			self.backgroundImage.SetParent(self)
			self.backgroundImage.AddFlag("not_pick")
			self.backgroundImage.LoadImage("d:/ymir work/ui/wiki/wiki_check_box_clean.tga")
			self.backgroundImage.Show()
			
			self.checkImage = ImageBox()
			self.checkImage.SetParent(self)
			self.checkImage.AddFlag("not_pick")
			self.checkImage.LoadImage("d:/ymir work/ui/wiki/wiki_check_box_checked.tga")
			self.checkImage.Hide()
			
			self.textInfo = TextLine()
			self.textInfo.SetParent(self)
			self.textInfo.SetPosition(20, 0)
			self.textInfo.Show()
			
			self.SetSize(self.backgroundImage.GetWidth() + self.textInfo.GetTextSize()[0], self.backgroundImage.GetHeight() + self.textInfo.GetTextSize()[1])
		
		def SetTextInfo(self, info):
			if self.textInfo:
				self.textInfo.SetText(info)
			
			self.SetSize(self.backgroundImage.GetWidth() + self.textInfo.GetTextSize()[0], self.backgroundImage.GetHeight() + self.textInfo.GetTextSize()[1])
		
		def SetCheckStatus(self, flag):
			if flag:
				self.checkImage.Show()
			else:
				self.checkImage.Hide()
		
		def GetCheckStatus(self):
			if self.checkImage:
				return self.checkImage.IsShow()
			
			return False
		
		def SetEvent(self, func, *args) :
			result = self.eventFunc.has_key(args[0])
			if result:
				self.eventFunc[args[0]] = func
				self.eventArgs[args[0]] = args
			else:
				print "[ERROR] ui.py SetEvent, Can`t Find has_key : %s" % args[0]
		
		def SetBaseCheckImage(self, image):
			if not self.backgroundImage:
				return
			
			self.backgroundImage.LoadImage(image)
		
		def OnMouseLeftButtonUp(self):
			if self.checkImage:
				if self.checkImage.IsShow():
					self.checkImage.Hide()
					
					if self.eventFunc["ON_UNCKECK"]:
						apply(self.eventFunc["ON_UNCKECK"], self.eventArgs["ON_UNCKECK"])
				else:
					self.checkImage.Show()
					
					if self.eventFunc["ON_CHECK"]:
						apply(self.eventFunc["ON_CHECK"], self.eventArgs["ON_CHECK"])

RegisterToolTipWindow("TEXT", TextLine)

if app.BL_MAILBOX:
	class RenderBox(Window):
		def __init__(self, layer = "UI"):
			Window.__init__(self, layer)
			self.color = 0xFF000000
		def __del__(self):
			Window.__del__(self)
			self.color = 0xFF000000
			
		def RegisterWindow(self, layer):
			self.hWnd = wndMgr.Register(self, layer)
			
		def SetColor(self, color):
			self.color = color
			
		def OnRender(self):
			(x, y, width, height) = self.GetRect()
			grp.SetColor( self.color )
			grp.RenderBar( x, y, width, height )


if app.WON_EXCHANGE:
	class EditLineCentered(EditLine):
		def __init__(self):
			EditLine.__init__(self)
			self.basePos = (0, 0)

		def __del__(self):
			EditLine.__del__(self)
			del self.basePos

		def SetFocus(self):
			EditLine.SetFocus(self)
			self.AdjustTextPosition()

		def SetPosition(self, x, y):
			EditLine.SetPosition(self, x, y)
			self.basePos = (x, y)
			self.AdjustTextPosition()

		def OnIMEUpdate(self):
			EditLine.OnIMEUpdate(self)
			self.AdjustTextPosition()

		def SetText(self, text):
			EditLine.SetText(self, text)
			self.AdjustTextPosition()

		def OnMouseLeftButtonDown(self):
			if False == self.canEdit:
				return False

			if self.IsIn():
				EditLine.SetFocus(self)
				ime.SetCursorPosition(wndMgr.GetCursorPosition(self.hWnd))

		def AdjustTextPosition(self):
			(textX, textY) = EditLine.GetTextSize(self)
			(locX, locY) = self.basePos
			TextLine.SetPosition(self, locX + (self.GetWidth() / 2) - textX / 2, locY)

class MultiTextLine(Window):
	def __del__(self):
		Window.__del__(self)
	def Destroy(self):
		self.children = []
		self.rangeText = 0
	def __init__(self):
		Window.__init__(self)
		self.children = []
		self.rangeText = 15
		self.textType = ""
	def SetTextType(self, textType):
		self.textType = textType
		for text in self.children:
			self.AddTextType(self.textType.split("#"),text)
	def SetTextRange(self, range):
		self.rangeText = range
		yPosition = 0
		for text in self.children:
			text.SetPosition(0,yPosition)
			yPosition+=self.rangeText
	def AddTextType(self, typeArg, text):
		if len(typeArg) > 1:
			if typeArg[0] == "vertical":
				if typeArg[1] == "top":
					text.SetVerticalAlignTop()
				elif typeArg[1] == "bottom":
					text.SetVerticalAlignBottom()
				elif typeArg[1] == "center":
					text.SetVerticalAlignCenter()
			elif typeArg[0] == "horizontal":
				if typeArg[1] == "left":
					text.SetHorizontalAlignLeft()
				elif typeArg[1] == "right":
					text.SetHorizontalAlignRight()
				elif typeArg[1] == "center":
					text.SetHorizontalAlignCenter()
	def SetText(self, cmd):
		if len(self.children) > 1:
			self.children=[]
		multi_arg = cmd.split("\n")
		yPosition = 0
		for text in multi_arg:
			childText = TextLine()
			childText.SetParent(self)
			childText.SetPosition(0,yPosition)
			if self.textType != "":
				self.AddTextType(self.textType.split("#"),childText)
			childText.SetText(str(text))
			childText.Show()
			self.children.append(childText)
			yPosition+=self.rangeText	
		
class PrettyBoard(Window):

	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16
	BOARD_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.51)

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		CornerFileNames = [ "d:/ymir work/ui/pattern/ThinBoard_Corner_LeftTop.tga", "d:/ymir work/ui/pattern/ThinBoard_Corner_LeftBottom.tga", "d:/ymir work/ui/pattern/ThinBoard_Corner_RightTop.tga", "d:/ymir work/ui/pattern/ThinBoard_Corner_RightBottom.tga" ]
		LineFileNames = [ "d:/ymir work/ui/pattern/ThinBoard_Line_"+dir+".tga" for dir in ["Left","Right","Top","Bottom"] ]
		
		self.cloudDisable = False

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("attach")
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)
			
			
		Pretty = ExpandedImageBox()
		Pretty.AddFlag("attach")
		Pretty.AddFlag("not_pick")
		Pretty.LoadImage("d:/ymir work/ui/universalelements/pet_gui/universalelements_pet_rightbottom_corner.sub")
		Pretty.SetParent(self)
		Pretty.SetPosition(0, 0)
		Pretty.Show()
		
		Base = Bar()
		Base.SetParent(self)
		Base.AddFlag("attach")
		Base.AddFlag("not_pick")
		Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		Base.SetColor(self.BOARD_COLOR)
		Base.Show()
		
		Nice = ExpandedImageBox()
		Nice.AddFlag("attach")
		#Nice.AddFlag("not_pick")
		Nice.LoadImage("d:/ymir work/ui/universalelements/pet_gui/universalelements_pet_cloud.sub")
		Nice.SetParent(self)
		Nice.SetPosition(0, 0)
		Nice.Show()
		
		self.Base = Base
		self.PrettyCorner = Pretty
		self.NiceCloud = Nice

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Base.SetSize(width - self.CORNER_WIDTH*2, height - self.CORNER_HEIGHT*2)
		
		self.PrettyCorner.SetPosition(width - self.CORNER_WIDTH - 7, height - self.CORNER_HEIGHT - 7)
		self.NiceCloud.SetPosition(width - 120, - 16)
		if width < self.NiceCloud.GetWidth() or self.cloudDisable:
			self.NiceCloud.Hide()
		else:
			self.NiceCloud.Show()
		
		self.width = width
		self.height = height

	def ShowInternal(self):
		self.Base.Show()
		for wnd in self.Lines:
			wnd.Show()
		for wnd in self.Corners:
			wnd.Show()
			
		self.PrettyCorner.Show()
		if not self.cloudDisable:
			self.NiceCloud.Show()

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()
			
		self.PrettyCorner.Hide()
		self.NiceCloud.Hide()
		
	def DisableNiceCloud(self):
		self.cloudDisable = True
		self.NiceCloud.Hide()
			
	def GetHeight(self):
		return self.height
	
	def GetWidth(self):
		return self.width

if app.RENDER_TARGET:
	class RenderTarget(Window):

		def __init__(self, layer = "UI"):
			Window.__init__(self, layer)
			
			self.number = -1

		def __del__(self):
			Window.__del__(self)

		def RegisterWindow(self, layer):
			self.hWnd = wndMgr.RegisterRenderTarget(self, layer)
			
			if app.ENABLE_WINDOW_SLIDE_EFFECT:
				self.SetSpecialWindow()			
			
		def SetRenderTarget(self, number):
			self.number = number
			wndMgr.SetRenderTarget(self.hWnd, self.number)

class MultiTextLine(Window):
	def __del__(self):
		Window.__del__(self)
	def Destroy(self):
		self.children = []
		self.rangeText = 0
	def __init__(self):
		Window.__init__(self)
		self.children = []
		self.rangeText = 15
		self.textType = ""
	def SetTextType(self, textType):
		self.textType = textType
		for text in self.children:
			self.AddTextType(self.textType.split("#"),text)
	def SetTextRange(self, range):
		self.rangeText = range
		yPosition = 0
		for text in self.children:
			text.SetPosition(0,yPosition)
			yPosition+=self.rangeText
	def AddTextType(self, typeArg, text):
		if len(typeArg) > 1:
			if typeArg[0] == "vertical":
				if typeArg[1] == "top":
					text.SetVerticalAlignTop()
				elif typeArg[1] == "bottom":
					text.SetVerticalAlignBottom()
				elif typeArg[1] == "center":
					text.SetVerticalAlignCenter()
			elif typeArg[0] == "horizontal":
				if typeArg[1] == "left":
					text.SetHorizontalAlignLeft()
				elif typeArg[1] == "right":
					text.SetHorizontalAlignRight()
				elif typeArg[1] == "center":
					text.SetHorizontalAlignCenter()
	def SetText(self, cmd):
		if len(self.children) > 1:
			self.children=[]
		multi_arg = cmd.split("\n")
		yPosition = 0
		for text in multi_arg:
			childText = TextLine()
			childText.SetParent(self)
			childText.SetPosition(0,yPosition)
			if self.textType != "":
				self.AddTextType(self.textType.split("#"),childText)
			childText.SetText(str(text))
			childText.Show()
			self.children.append(childText)
			yPosition+=self.rangeText

if app.ENABLE_NEW_TARGET_HP:
	import pack
	class NewTargetInfo(ImageBox):
		def __del__(self):
			ImageBox.__del__(self)
		def __init__(self):
			ImageBox.__init__(self)
			self.Destroy()
			self.IMG_DIR = "d:/ymir work/ui/game/renewal_target/"
			self.__Load()
		def Destroy(self):
			self.children = {}
			self.IMG_DIR = ""

		def __Load(self):

			self.LoadImage(self.IMG_DIR+"bg.tga")

			barImage = ImageBox()
			barImage.SetParent(self)
			barImage.LoadImage(self.IMG_DIR+"bar.tga")
			barImage.SetPosition(0,0)
			barImage.Show()
			self.children["barImage"] = barImage

			raceImage = ImageBox()
			raceImage.SetParent(self)
			raceImage.SetPosition(10,-10)
			raceImage.Show()
			self.children["raceImage"] = raceImage

		def SetRaceImage(self, raceIndex, isBg):
			if self.children.has_key("raceIndex"):
				if self.children["raceIndex"] == raceIndex:
					return
			if not pack.Exist(self.IMG_DIR+"race_%d.tga"%raceIndex):
				raceIndex = 0
			self.children["raceIndex"] = raceIndex
			if isBg:
				self.children["barImage"].LoadImage(self.IMG_DIR+str("race_%d.tga"%raceIndex))
				self.children["raceImage"].Hide()
			else:
				self.children["barImage"].LoadImage(self.IMG_DIR+"bar.tga")
				self.children["raceImage"].LoadImage(self.IMG_DIR+str("race_%d.tga"%raceIndex))
				self.children["raceImage"].Show()


		def IsImageHasMountVnums(self, raceVnum):
			if raceVnum == 20213:
				return True
			if raceVnum == 20113:
				return True
			if raceVnum == 20117:
				return True
			if raceVnum == 20118:
				return True
			if raceVnum == 20122:
				return True
			if raceVnum == 20123:
				return True
			if raceVnum == 20248:
				return True
			# etc etc.
			return True

		def SetHP(self, raceIndex = 0, hpPercent = 100):
			isBg = False
			if raceIndex > 8:
				if self.IsImageHasMountVnums(raceIndex) == False:
					self.Hide()
				else:
					isBg = True
					self.Show()
			else:
				self.Show()
			self.SetRaceImage(raceIndex, isBg)
			percent = 99.0
			if hpPercent <= 0:
				percent = 1.0
			elif hpPercent >= 100:
				percent = 99.0
			else:
				percent = float(100-hpPercent)/100.0
			self.children["barImage"].SetRectCircle(percent)
			
if app.ENABLE_MAINTENANCE_SYSTEM:
	class ExtendedTextLine(Window):

		OBJECT_TYPE_IMAGE = 0
		OBJECT_TYPE_TEXT = 1
		OBJECT_TYPE_HEIGHT = 2
		OBJECT_TYPE_WIDTH = 3

		OBJECT_TAGS = {
			OBJECT_TYPE_IMAGE : "IMAGE",
			OBJECT_TYPE_TEXT : "TEXT",
			OBJECT_TYPE_HEIGHT : "HEIGHT",
			OBJECT_TYPE_WIDTH : "WIDTH",
		}

		def __init__(self):
			Window.__init__(self)

			self.inputText = ""
			self.childrenList = []

			self.limitWidth = 0
			self.x = 0
			self.maxHeight = 0
			self.extraHeight = 0

			# self.SetWindowName("NONAME_ExtendedTextLine")

		def __del__(self):
			Window.__del__(self)

		def SetLimitWidth(self, width):
			self.limitWidth = width
			if self.inputText != "":
				self.SetText(self.inputText)

		def IsText(self, text):
			return self.inputText == text

		def SetText(self, text):
			self.childrenList = []
			self.x = 0
			self.maxHeight = 0
			self.extraHeight = 0

			charIndex = 0
			currentWord = ""

			textLine = None

			while charIndex < len(text):
				c = text[charIndex:charIndex+1] 

				# tags
				if c == "<":
					if textLine:
						self.childrenList.append(textLine)
						self.x += textLine.GetTextWidth()
						self.maxHeight = max(self.maxHeight, textLine.GetTextHeight() + 2)
						textLine = None

					tagStart = charIndex
					tagEnd = text[tagStart:].find(">")
					if tagEnd == -1:
						tagEnd = len(text)
					else:
						tagEnd += tagStart

					tagNameStart = charIndex + 1
					tagNameEnd = text[tagNameStart:].find(" ")
					if tagNameEnd == -1 or tagNameEnd > tagEnd:
						tagNameEnd = tagEnd
					else:
						tagNameEnd += tagNameStart
					tag = text[tagNameStart:tagNameEnd]

					content = {}
					tagContentPos = tagNameEnd + 1
					while tagContentPos < tagEnd:
						tagContentStart = -1
						for i in xrange(tagContentPos, tagEnd):
							if text[i:i+1] != " " and text[i:i+1] != "\t":
								tagContentStart = i
								break
						if tagContentStart == -1:
							break

						tagContentPos = text[tagContentStart:].find("=") + tagContentStart
						tagKey = text[tagContentStart:tagContentPos]

						tagContentPos += 1

						tagContentEnd = -1
						isBreakAtSpace = TRUE
						for i in xrange(tagContentPos, tagEnd+1):
							if isBreakAtSpace == TRUE and (text[i:i+1] == " " or text[i:i+1] == "\t" or text[i:i+1] == ">"):
								tagContentEnd = i
								break
							elif text[i:i+1] == "\"":
								if isBreakAtSpace == TRUE:
									isBreakAtSpace = FALSE
									tagContentPos = i + 1
								else:
									tagContentEnd = i
									break
						if tagContentEnd == -1:
							break

						tagValue = text[tagContentPos:tagContentEnd]
						content[tagKey] = tagValue

						tagContentPos = text[tagContentEnd:].find(" ")
						if tagContentPos == -1:
							tagContentPos = tagContentEnd
						else:
							tagContentPos += tagContentEnd

					bRet = TRUE
					for key in self.OBJECT_TAGS:
						if self.OBJECT_TAGS[key] == tag.upper():
							bRet = self.__ComputeTag(key, content)
							break

					if bRet == FALSE:
						break

					charIndex = tagEnd + 1
					continue

				# text
				if not textLine:
					textLine = TextLine()
					textLine.SetParent(self)
					textLine.SetPosition(self.x, 0)
					textLine.SetWindowVerticalAlignCenter()
					textLine.SetVerticalAlignCenter()
					textLine.Show()
				subtext = textLine.GetText()
				textLine.SetText(subtext + c)
				if textLine.GetTextWidth() + self.x >= self.limitWidth and self.limitWidth != 0:
					if subtext != "":
						textLine.SetText(subtext)
						self.childrenList.append(textLine)
						self.x += textLine.GetTextWidth()
						self.maxHeight = max(self.maxHeight, textLine.GetTextHeight() + 2)
						textLine = None
					else:
						textLine = None
					break

				# increase char index
				charIndex += 1

			if textLine:
				self.childrenList.append(textLine)
				self.x += textLine.GetTextWidth()
				self.maxHeight = max(self.maxHeight, textLine.GetTextHeight() + 2)
				textLine = None

			self.inputText = text[:charIndex]
			self.SetSize(self.x, self.maxHeight + self.extraHeight)
			self.UpdateRect()

			return charIndex

		def __ComputeTag(self, index, content):
			# tag <IMAGE []>
			if index == self.OBJECT_TYPE_IMAGE:
				if not content.has_key("path"):
					import dbg
					dbg.TraceError("Cannot read image tag : no path given")
					return FALSE

				image = ImageBox()
				image.SetParent(self)
				image.SetPosition(self.x, 0)
				image.SetWindowVerticalAlignCenter()
				image.LoadImage(content["path"])
				image.Show()

				if content.has_key("align") and content["align"].lower() == "center":
					image.SetPosition(self.limitWidth / 2 - image.GetWidth() / 2, 0)
				else:
					if self.x + image.GetWidth() >= self.limitWidth and self.limitWidth != 0:
						return FALSE
					self.x += image.GetWidth()

				self.childrenList.append(image)
				self.maxHeight = max(self.maxHeight, image.GetHeight())

				return TRUE

			# tag <TEXT []>
			elif index == self.OBJECT_TYPE_TEXT:
				if not content.has_key("text"):
					import dbg
					dbg.TraceError("Cannot read text tag : no text given")
					return FALSE

				textLine = TextLine()
				textLine.SetParent(self)
				textLine.SetPosition(self.x, 0)
				textLine.SetWindowVerticalAlignCenter()
				textLine.SetVerticalAlignCenter()
				if content.has_key("r") and content.has_key("g") and content.has_key("b"):
					textLine.SetFontColor(int(content["r"]) / 255.0, int(content["g"]) / 255.0, int(content["b"]) / 255.0)
				if content.has_key("font_size"):
					if content["font_size"].lower() == "large":
						textLine.SetFontName(localeInfo.UI_DEF_FONT_LARGE)
				elif content.has_key("color"):
					textLine.SetPackedFontColor(int(content["color"]))
				if content.has_key("outline") and content["outline"] == "1":
					textLine.SetOutline()
				textLine.SetText(content["text"])
				textLine.Show()

				if self.x + textLine.GetTextWidth() >= self.limitWidth and self.limitWidth != 0:
					return FALSE

				self.childrenList.append(textLine)
				self.x += textLine.GetTextWidth()
				self.maxHeight = max(self.maxHeight, textLine.GetTextHeight() + 2)

				return TRUE

			# tag <HEIGHT []>
			elif index == self.OBJECT_TYPE_HEIGHT:
				if not content.has_key("size"):
					import dbg
					dbg.TraceError("Cannot read height tag : no size given")
					return FALSE

				self.extraHeight += int(content["size"])

				return TRUE

			# tag <WIDTH []>
			elif index == self.OBJECT_TYPE_WIDTH:
				if not content.has_key("size"):
					import dbg
					dbg.TraceError("Cannot read width tag : no size given")
					return FALSE

				self.x += int(content["size"])

				return TRUE

			return FALSE
		
def MakeTextLineWithoutAlign(parent, text, x, y):
	textLine = TextLine()
	textLine.SetParent(parent)
	textLine.SetPosition(x, y)
	textLine.SetText(text)
	textLine.Show()
	return textLine
		
def MakeOptionsCheckBox(parent, text, x, y):
	checkBox = CheckBox()
	checkBox.SetParent(parent)
	checkBox.SetPosition(x, y)
	checkBox.SetTextInfo(text)
	checkBox.SetBaseCheckImage("d:/ymir work/ui/new_options/options_checkbox.tga")
	checkBox.Show()
	return checkBox



if app.ENABLE_GUILD_REQUEST:
	class MouseReflector(Window):
		def __init__(self, parent):
			Window.__init__(self)
			self.SetParent(parent)
			self.AddFlag("not_pick")
			self.width = self.height = 0
			self.isDown = False
		def __del__(self):
			Window.__del__(self)
		def Down(self):
			self.isDown = True
		def Up(self):
			self.isDown = False
		def OnRender(self):
			if self.isDown:
				grp.SetColor(WHITE_COLOR)
			else:
				grp.SetColor(HALF_WHITE_COLOR)
			x, y = self.GetGlobalPosition()
			grp.RenderBar(x + 2, y + 2, self.GetWidth() - 4, self.GetHeight() - 4)
	class CheckBoxNew(ImageBox):
		def __init__(self, parent, x, y, event, filename = "d:/ymir work/ui/chat/chattingoption_check_box_off.sub"):
			ImageBox.__init__(self)
			self.SetParent(parent)
			self.SetPosition(x, y)
			self.LoadImage(filename)
			self.mouseReflector = MouseReflector(self)
			self.mouseReflector.SetSize(self.GetWidth(), self.GetHeight())
			image = MakeImageBox(self, "d:/ymir work/ui/public/check_image.sub", 0, 0)
			image.AddFlag("not_pick")
			image.SetWindowHorizontalAlignCenter()
			image.SetWindowVerticalAlignCenter()
			image.Hide()
			self.check = False
			self.enable = True
			self.image = image
			self.event = event
			self.Show()
			self.mouseReflector.UpdateRect()
		def __del__(self):
			ImageBox.__del__(self)
		def GetCheck(self):
			return self.check
		def SetCheck(self, flag):
			if flag:
				self.check = True
				self.image.Show()
			else:
				self.check = False
				self.image.Hide()
		def Disable(self):
			self.enable = False
		def OnMouseOverIn(self):
			if not self.enable:
				return
			self.mouseReflector.Show()
		def OnMouseOverOut(self):
			if not self.enable:
				return
			self.mouseReflector.Hide()
		def OnMouseLeftButtonDown(self):
			if not self.enable:
				return
			self.mouseReflector.Down()
		def OnMouseLeftButtonUp(self):
			if not self.enable:
				return
			self.mouseReflector.Up()
			self.event()