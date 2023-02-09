import ui
import wndMgr
import localeInfo

class SideBarWindow(ui.ScriptWindow):
	def __init__(self, wndInventory):
		import exception
		
		if not wndInventory:
			exception.Abort("Missing wndInventory.")
			return
			
		ui.ScriptWindow.__init__(self)
		
		self.isLoaded = 0
		self.wndInventory = wndInventory
		
		self.__LoadWindow()
		self.MaxBtn.SetParent(self.wndInventory)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
		
		self.isLoaded = 1
		
		try:
			self.board = ui.Board()
			self.board.SetParent(self)

			self.MaxBtn = ui.Button()
			self.MaxBtn.SetUpVisual("d:/ymir work/ui/game/belt_inventory/btn_expand_normal.tga")
			self.MaxBtn.SetOverVisual("d:/ymir work/ui/game/belt_inventory/btn_expand_over.tga")
			self.MaxBtn.SetDownVisual("d:/ymir work/ui/game/belt_inventory/btn_expand_down.tga")
			self.MaxBtn.SetEvent(self.OpenInventory)
			self.MaxBtn.SetParent(self.wndInventory)
			self.MinBtn = ui.Button()
			self.MinBtn.SetUpVisual("d:/ymir work/ui/game/belt_inventory/btn_minimize_normal.tga")
			self.MinBtn.SetOverVisual("d:/ymir work/ui/game/belt_inventory/btn_minimize_over.tga")
			self.MinBtn.SetDownVisual("d:/ymir work/ui/game/belt_inventory/btn_minimize_down.tga")
			self.MinBtn.SetParent(self.board)
			self.MinBtn.SetEvent(self.CloseInventory)
			self.MinBtn.SetPosition(0, 15)
			self.MaxBtn.SetPosition(24, 200) # y its ok? are you here

			self.board.SetPosition(0, 0)
		except:
			import exception
			exception.Abort("uisdebar.__LoadInventory fail")
	
		
		self.wndHeight = 0
		self.wndWidth = 0
		self.btnmod = 86
		
		self.btns = []
		self.minimized = True
		
	def AddButton(self, event, up, over, down, tooltip):
		height = len(self.btns) * 41
		btn = ui.Button()
		btn.SetParent(self.board)
		btn.SetTop()
		btn.SetPosition(16, 26 + height)
		btn.SetUpVisual(up)
		btn.SetOverVisual(over)
		btn.SetDownVisual(down)
		btn.SetEvent(event)
		btn.SetToolTipText(tooltip)
		btn.ToolTipText.SetParent(self.wndInventory)
		btn.ToolTipText.SetTop()
		(x, y) = btn.GetGlobalPosition()
		txtlen = len(tooltip) / 2
		btn.ToolTipText.SetPosition(x - btn.GetWidth() - txtlen, y + 100)
		btn.Show()

		self.wndHeight = 88 + height
		
		if (btn.GetWidth()-14) > self.wndWidth:
			self.wndWidth = btn.GetWidth()-14

		self.btns.append(btn)
		
		self.MinBtn.SetPosition(-3, (self.wndHeight / 2) - (self.MinBtn.GetHeight() / 2))

	def __del__(self):
		self.Destroy()
		ui.ScriptWindow.__del__(self)

	def ClearButtons(self):
		for obj in self.btns:
			obj.Hide()
			del obj
			obj = None
		del self.btns[:]

		self.btns = []

	def Destroy(self):
		self.Hide()
		self.ClearButtons()

		if self.board:
			del self.board
		
		if self.MaxBtn:
			del self.MaxBtn
			
		if self.MinBtn:
			del self.MinBtn
			
		self.MaxBtn = None
		self.MinBtn = None
		self.board = None
		
	def GetBasePosition(self):
		x, y = self.wndInventory.GetGlobalPosition()
		return x- 8 + 30, y + 12 + self.btnmod

	def OpenInventory(self):
		self.MinBtn.Show()
		self.board.Show()
		self.MaxBtn.Hide()

		if localeInfo.IsARABIC() == 0:
			self.AdjustPositionAndSize()

		self.wndInventory.SetTop()
		
	def CloseInventory(self):
		self.MinBtn.Hide()
		self.board.Hide()
		self.MaxBtn.Show()
		
		if localeInfo.IsARABIC() == 0:
			self.AdjustPositionAndSize()
		
	def Close(self):
		self.Hide()
		
	def IsOpeningInventory(self):
		return self.MinBtn.IsShow()
	
	def AdjustPositionAndSize(self):
		bx, by = self.GetBasePosition()
		
		if self.IsOpeningInventory():			
			self.SetPosition(bx-self.board.GetWidth()+14, by)
			self.board.SetSize(self.wndWidth, self.wndHeight)

		else:
			self.SetPosition(bx, by)
			self.board.SetSize(self.MaxBtn.GetWidth(), self.MaxBtn.GetHeight())

		self.SetSize(self.board.GetWidth()+5, self.board.GetHeight()+5)


	def Show(self, openSidebar = FALSE):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)
		
		if openSidebar:
			self.OpenInventory()
		else:
			self.CloseInventory()
