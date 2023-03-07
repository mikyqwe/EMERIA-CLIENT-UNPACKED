import ui
import item
import net
import constInfo
import localeInfo
import wndMgr
import app
import renderTarget
import grp
import chat 
import player

class ItemFinder(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.name_item = ""
		self.viewItemCount=2
		self.itemStep=134
		self.basePos=0
		self.add = {}
		self.text0 = {}
		self.text1 = {}
		self.text2 = {}
		self.text3 = {}
		self.grid  = {}
		self.buttons = []
		self.LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def Show(self):
		self.LoadWindow()
		self.SetCenterPosition()
		self.ModelPreviewBoard.Hide()
		self.ModelPreview.Hide()
		ui.ScriptWindow.Show(self)

	def AppendInfo(self, index, name_monster, prob, activi, vnum, count, name_item):
		get_rare_text = "Dont know"
		if prob <= 5:#chance less than 5%
			get_rare_text = "Very rare"
		elif prob > 5 and prob <= 20: #chance between 5-20%
			get_rare_text = "Rare"
		elif prob > 20 and prob <= 50:#chance between 20-50%
			get_rare_text = "Common"
		else:
			get_rare_text = "Average"

		self.add[index] = ui.MakeButtonSearch(self, 20, 76*index + 50, False, "d:/ymir work/ui/itemfinder/", "tab.tga", "tab.tga", "tab.tga")
		self.add[index].SetEvent(ui.__mem_func__(self.ButtonFunc), index)
		self.add[index].SetOverEvent(ui.__mem_func__(self.OverIn), index)
		self.add[index].SetOverOutEvent(ui.__mem_func__(self.OverOut))
		self.text0[index] = ui.MakeText(self.add[index], str(name_monster), 56, 0)
		self.text1[index] = ui.MakeText(self.add[index], "- Nume: " + str(name_item), 5, 36)
		self.text2[index] = ui.MakeText(self.add[index], "- ªansa de drop: " + get_rare_text, 5, 69)
		self.text3[index] = ui.MakeText(self.add[index], "- Monºtri activi: " + str(activi), 5, 100)
		self.grid[index] = ui.MakeGridSlotSearch(self.add[index], 145, 27, vnum, count)

		if index < self.viewItemCount:
			self.add[index].SetPosition(25, 95+(128*index))
			self.add[index].Show()
		else:
			self.add[index].Hide()
		self.buttons.append(self.add[index])

	def LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/itemfinder.py")
		except:
			import exception
			exception.Abort("itemfinder.LoadWindow.LoadObject")
		try:
			self.titleBar = self.GetChild("TitleBar")
			self.board = self.GetChild("board")
			self.editline = self.GetChild("ItemNameValue")
			self.searchbutton = self.GetChild("search_button")
			self.clearbutton = self.GetChild("clear_button")
			self.scrollBar = self.GetChild("ScrollBar")
			self.bg_finder = self.GetChild("bg_findere")
		except:
			import exception
			exception.Abort("itemfinder.__LoadWindow.BindObject")

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.RENDER_TARGET_INDEX = 3

		self.ModelPreviewBoard = ui.ThinBoard()
		self.ModelPreviewBoard.SetParent(self)
		self.ModelPreviewBoard.SetSize(200+10, 230+30-12)
		self.ModelPreviewBoard.SetPosition(238, 114)
		self.ModelPreviewBoard.Show()

		self.ModelPreview = ui.RenderTarget()
		self.ModelPreview.SetParent(self.ModelPreviewBoard)
		self.ModelPreview.SetSize(200, 230)
		self.ModelPreview.SetPosition(5, 22-12)
		self.ModelPreview.SetRenderTarget(self.RENDER_TARGET_INDEX)
		self.ModelPreview.Show()

		# self.scrollBar.SetScrollEvent(self.__OnScroll)
		self.scrollBar.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
		self.searchbutton.SetEvent(ui.__mem_func__(self.OnSearch))
		self.clearbutton.SetEvent(ui.__mem_func__(self._StergeText))


	def Close(self):
		self.__ModelPreviewClose()
		self.Hide()

	def SetBasePos(self, basePos):
		for oldItem in self.buttons[self.basePos:self.basePos+self.viewItemCount]:
			oldItem.Hide()

		self.basePos=basePos

		range_c = 0
		pos=basePos
		for newItem in self.buttons[self.basePos:self.basePos+self.viewItemCount]:
			newItem.SetPosition(25, 95+(128*range_c))
			newItem.Show()
			pos+=1
			range_c+=1

	def __OnScroll(self):
		self.SetBasePos(int(self.scrollBar.GetPos()*self.__GetScrollLen()))

	def __GetScrollLen(self):
		scrollLen=len(self.buttons)-2
		if scrollLen<0:
			return 0

		return scrollLen

	# def __OnScroll(self):
		# if self.scrollBar.IsShow():
			# range_counter = 0
			# pos = int(self.scrollBar.GetPos() * (len(self.buttons) - self.viewItemCount))
			# for x in xrange(constInfo.finder_counts-1):
				# self.buttons[x].Hide()

			# for i in range(pos, pos+self.viewItemCount):
				# self.buttons[i].SetPosition(25, 95+(128*range_counter))
				# self.buttons[i].Show()
				# range_counter += 1

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def OverIn(self, i):
		if self.tooltipItem:
			self.tooltipItem.ClearToolTip()
			constInfo.OVER_IN = True
			self.tooltipItem.AddItemData(self.GetItemVnum(i), 0, 0, 0)

	def OverOut(self):
		if self.tooltipItem:
			constInfo.OVER_IN = False
			self.tooltipItem.Hide()

	def ButtonFunc(self, arg):
		self.__ModelPreview(self.GetVnumPreview(arg))

	def OnUpdate(self):
		if app.IsPressed(app.DIK_RETURN) and self.editline.IsFocus():
			self.OnSearch()
		if constInfo.finder_counts > 3:
			self.scrollBar.SetMiddleBarSize(float(self.viewItemCount) / float(len(self.buttons)+1))
			self.scrollBar.Show()
		else:
			self.scrollBar.Hide()

	def GetItemVnum(self, i):
		try:
			return int(constInfo.finder_items_v[int(i)]["iItemVnum"])
		except KeyError:
			return 0

	def GetVnumPreview(self, i):
		try:
			return int(constInfo.finder_items[int(i)]["iMobVnum"])
		except KeyError:
			return 0
	
	def OnSearch(self):
		if self.editline.GetText() == None or self.editline.GetText() == "":
			return 
		self.RemoveAllItems()
		self.scrollBar.SetPos(0)
		self.scrollBar.Hide()
		item_name = self.editline.GetText().replace(" ", "_")
		net.SendChatPacket("/cauta_drop %s" % item_name)

	def __ModelPreview(self, Vnum):
		self.ModelPreviewBoard.Show()
		self.ModelPreview.Show()
		renderTarget.SetBackground(self.RENDER_TARGET_INDEX, "d:/ymir work/ui/game/myshop_deco/model_view_bg.sub")
		renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, True)
		renderTarget.SelectModel(self.RENDER_TARGET_INDEX, Vnum)

	def RemoveAllItems(self):
		constInfo.finder_counts = 0
		self.name_item=""
		self.add = {}
		self.text0 = {}
		self.text1 = {}
		self.text2 = {}
		self.text3 = {}
		self.grid  = {}
		self.buttons = []

	def _StergeText(self):
		self.editline.SetText("")

	def __ModelPreviewClose(self):
		self.RENDER_TARGET_INDEX = 3

		if self.ModelPreviewBoard:
			self.ModelPreviewBoard.Hide()
			self.ModelPreview.Hide()

			self.ModelPreviewBoard = None
			self.ModelPreview = None

			renderTarget.SetVisibility(self.RENDER_TARGET_INDEX, False)

	def Destroy(self):
		self.RemoveAllItems()
		self.ClearDictionary()
