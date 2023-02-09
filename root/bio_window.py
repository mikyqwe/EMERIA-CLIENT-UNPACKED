import ui
import app
import chat
import grp
import uiToolTip
import item
import mouseModule
import player
import snd
import constInfo
import net
import localeInfo

class BioWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)	
		self.Data = constInfo.BIO_DICT
		self.NeedUpdate = False
		self.AttachedSlot = -1
		self.is_loaded = FALSE
		self.__LoadGui()

	def __LoadGui(self):
		self.board = self.CreateBoard(330, 270+145, 200, 100)

		self.board.SetTitleName('Biolog')
		self.board.SetCloseEvent(self.board.Hide)
	
		self.bioBoard = self.CreateImageBox(self.board, 9, 215+138+4, "bio_assets/category_pressed2.tga")
		self.bioInfo = self.CreateImageBox(self.board, 9, 270+36, "bio_assets/category_pressed2.tga")
		
		self.levelBar = self.TextBar(self.bioBoard, 7, 4, 90, 17)
		self.statusBar = self.TextBar(self.bioBoard, 7, 23 + 4,90, 17)
		self.timeBar = self.TextBar(self.bioBoard, 7 + 90 + 5 + 45, 4, 155, 17)
		self.rateBar = self.TextBar(self.bioBoard, 7 + 90 + 5 + 45, 23+4, 65, 17)
		
		self.magicslot = self.CreateImageBox(self.bioBoard, 7 + 90 + 5, 4, "bio_assets/ital.tga")
		self.item_slot = self.CreateRealSlot(self.magicslot, 4, 4)

		self.item_slot.SetSelectEmptySlotEvent(self.SelectEmptySlot)
		self.item_slot.SetSelectItemSlotEvent(self.SelectItemSlot)		
		self.item_slot.SetUseSlotEvent(self.UseItemSlot)	
		self.item_slot.SetUnselectItemSlotEvent(self.UseItemSlot)	

		self.bioInfoLine1 = self.TextBar(self.bioInfo, 7, 4, 295, 17)
		self.bioInfoLine2 = self.TextBar(self.bioInfo, 7, 20+4, 295, 17)
		
		self.bioInfoData1 = self.CreateTextline(self.bioInfoLine1, 0, 0, localeInfo.BIO_NO_MIX_S, 1)
		self.bioInfoData2 = self.CreateTextline(self.bioInfoLine2, 0, 0, localeInfo.BIO_NO_MIX_ICON, 1)


		self.bioLevel = self.CreateTextline(self.levelBar, 0, 0, localeInfo.BIO_NO_MIX, 1)
		self.bioTime = self.CreateTextline(self.timeBar, 0, 0, "Next Try: 0", 1)
		self.bioRate = self.CreateTextline(self.rateBar, 0, 0, "Luck: 0%", 1)
		self.bioStatus = self.CreateTextline(self.statusBar, 0, 0, "Status: 0 / 0", 1)
		
		self.gui = {
				'scrollbar' : self.CreateScrollbar(self.board,185+90,305,30),
				'boards' : []
				}
				
				
		board_count = 6
		self.UpdateInfoBoard()

		for i in xrange(min(board_count, len(self.Data))):		
			self.gui['boards'].append(CreateBioBoard(self.board, 10, 30 + 46 * i, self))
			self.gui['boards'][i].SetBoardInfo(i, self.Data[i])
		
		if len(self.Data) <= board_count:
			self.gui['scrollbar'].Hide()
		else:
			self.gui['scrollbar'].SetMiddleBarSize(float(board_count) / float(len(self.Data)))
			self.gui['scrollbar'].Show()
			
		self.gui['scrollbar'].SetScrollEvent(self.__OnScroll)
		
		self.SendBtn = ui.Button()
		self.SendBtn.SetParent(self.bioBoard)
		self.SendBtn.SetPosition(7 + 90 + 5 + 45 + 70, 25)
		self.SendBtn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.SendBtn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.SendBtn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.SendBtn.SetText("Consegna")
		self.SendBtn.SetEvent(lambda : self.SendTry())
		self.SendBtn.Show()

		#self.SendBtn.Down()
		#self.SendBtn.Disable()		
		
		self.is_loaded = TRUE

	def ClearBio(self):
		self.Data = constInfo.BIO_DICT

	def OpenWindow(self):
		if self.board.IsShow():
			self.board.Hide()
		else:
			self.board.Show()

	def UpdateBio(self):
		self.Data = constInfo.BIO_DICT
		
		self.UpdateInfoBoard()
		
		self.gui['boards'] = []
		
		board_count = 6
		
		for i in xrange(min(board_count, len(self.Data))):		
			self.gui['boards'].append(CreateBioBoard(self.board, 10, 30 + 46 * i, self))
			self.gui['boards'][i].SetBoardInfo(i, self.Data[i])
		
		if len(self.Data) <= board_count:
			self.gui['scrollbar'].Hide()
		else:
			self.gui['scrollbar'].SetMiddleBarSize(float(board_count) / float(len(self.Data)))
			self.gui['scrollbar'].Show()		

		for i in xrange(len(self.Data)):
			if self.Data[i]["STATUS"] == 1 and player.GetStatus(player.LEVEL) >= self.Data[i]["LEVEL"]:
				self.UpdateTextLine(self.bioRate, localeInfo.BIO_LUCKK % self.Data[i]["PERCENT"])
		
		self.SendBtn.SetText(localeInfo.BIO_CONSEGNA)
		
		#self.SendBtn.Down()
		#self.SendBtn.Disable()		
		
		self.__OnScroll()

	def UpdateInfoBoard(self):
		for i in xrange(len(self.Data)):
			if self.Data[i]["STATUS"] == 1 and player.GetStatus(player.LEVEL) >= self.Data[i]["LEVEL"]:
				self.UpdateTextLine(self.bioLevel, localeInfo.BIO_CURRET_LV % self.Data[i]["LEVEL"])
				self.UpdateTextLine(self.bioTime, localeInfo.BIO_CURRENT_NEXT_TRY % localeInfo.SecondToDHM(self.Data[i]["LAST_TRY"] - app.GetGlobalTimeStamp()))
				#self.UpdateTextLine(self.bioRate, "Luck: %d%%" % self.Data[i]["PERCENT"])
				
				if self.Data[i]["STATE"] == 0:
					self.UpdateTextLine(self.bioStatus, "Status: %d / %d" % (self.Data[i]["COUNT"], self.Data[i]["NEED_COUNT"]))
				elif self.Data[i]["STATE"] == 1:
					self.UpdateTextLine(self.bioStatus, "Status: 0 / 1")
				elif self.Data[i]["STATE"] == 2:	
					self.SendBtn.SetText(localeInfo.BIO_RREWARD)
				else:
					self.UpdateTextLine(self.bioStatus, "Status: 0 / 0")
					
					
				#self.SendBtn.SetUp()
				#self.SendBtn.Enable()	

		if player.GetItemIndex(self.AttachedSlot) != 71035:
			self.item_slot.SetItemSlot(0, 0, 0)
			self.item_slot.DeactivateSlot(0)
			self.item_slot.RefreshSlot()
			self.AttachedSlot = -1
			
			for i in xrange(len(self.Data)):
				if self.Data[i]["STATUS"] == 1:
					self.UpdateTextLine(self.bioRate, localeInfo.BIO_LUCKK % self.Data[i]["PERCENT"])
					break				
		else:
			self.UpdateTextLine(self.bioRate, localeInfo.BIO_LUCK1)

	def SendTry(self):
		net.SendChatPacket("/bio_sys %d" % self.AttachedSlot)

	def UseItemSlot(self, slotIndex):
	
		for i in xrange(len(self.Data)):
			if self.Data[i]["STATUS"] == 1 and player.GetStatus(player.LEVEL) >= self.Data[i]["LEVEL"]:
				self.UpdateTextLine(self.bioRate, localeInfo.BIO_LUCKK % self.Data[i]["PERCENT"])
	
		self.item_slot.SetItemSlot(0, 0, 0)
		self.item_slot.DeactivateSlot(0)
		self.item_slot.RefreshSlot()
		self.AttachedSlot = -1

	def SelectEmptySlot(self, iSlotIndex):
		if not mouseModule.mouseController.isAttached():
			return

		attachedSlotType = mouseModule.mouseController.GetAttachedType()
		attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
		mouseModule.mouseController.DeattachObject()

		if player.SLOT_TYPE_INVENTORY != attachedSlotType:
			return

		if player.GetItemIndex(attachedSlotPos) != 71035:
			return

		#self.item_slot = attachedSlotPos
		self.item_slot.SetItemSlot(0, player.GetItemIndex(attachedSlotPos), 1)
		self.AttachedSlot = attachedSlotPos
		self.item_slot.ActivateSlot(0)
		
		self.UpdateTextLine(self.bioRate, localeInfo.BIO_LUCK1)
		
		snd.PlaySound("sound/ui/drop.wav")
		self.item_slot.RefreshSlot()

	def SelectItemSlot(self, iSlotIndex):
		isAttached = mouseModule.mouseController.isAttached()

		if isAttached:
			snd.PlaySound("sound/ui/loginfail.wav")
			mouseModule.mouseController.DeattachObject()
		else:
			snd.PlaySound("sound/ui/drop.wav")
			self.item_slot.RefreshSlot()

		for i in xrange(len(self.Data)):
			if self.Data[i]["STATUS"] == 1:
				self.UpdateTextLine(self.bioRate, "Rate: %d%%" % self.Data[i]["PERCENT"])
				break


	def UpdateSelection(self, i):
		self.UpdateTextLine(self.bioInfoData1, localeInfo.BIO_S_L_B % (self.Data[i]["LEVEL"], self.Data[i]["LIMIT_TIME"] / 60))
		self.UpdateTextLine(self.bioInfoData2, "Bonus: %s" % uiToolTip.ItemToolTip.AFFECT_DICT[self.Data[i]["BONUS"][0]](self.Data[i]["BONUS"][1]))
		
	def OnUpdate(self):
		board_count = len(self.gui['boards'])
		
		for i in xrange(board_count):
			self.gui['boards'][i].Refresh()
		
		self.UpdateInfoBoard()
		

	def __OnScroll(self):
		board_count = len(self.gui['boards'])
		pos = int(self.gui['scrollbar'].GetPos() * (len(self.Data) - board_count))
		
		for i in xrange(board_count):
			realPos = i + pos
			self.gui['boards'][i].SetBoardInfo(realPos, self.Data[realPos])

	def TextBar(self, parent, x, y, w, h):
		bar = ui.Bar()
		bar.SetParent(parent)
		bar.SetPosition(x, y)
		bar.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.40))
		bar.SetSize(w, h)
		bar.Show()
		return bar

	def UpdateTextLine(self, textline, text):
		textline.SetText(text)
		textline.SetWindowHorizontalAlignCenter()
		textline.SetWindowVerticalAlignCenter()
		textline.SetHorizontalAlignCenter()
		textline.SetVerticalAlignCenter()		

	def CreateRealSlot(self, parent, x, y):
		ItemSlot = ui.GridSlotWindow()	
		ItemSlot.SetParent(parent)
		ItemSlot.SetPosition(x, y)
		ItemSlot.ArrangeSlot(0, 1, 1, 32, 32, 1, 0)
		ItemSlot.SetItemSlot(0, 0, 0)		
		ItemSlot.RefreshSlot()
		ItemSlot.Show()
		
		return ItemSlot
	
	def CreateTextline(self, parent, x, y, text, center = 0):
		textline = ui.TextLine()
		textline.SetParent(parent)
		textline.SetPosition(x,y)
		textline.SetText(text)
		if center == 1:
			textline.SetWindowHorizontalAlignCenter()
			textline.SetWindowVerticalAlignCenter()
			textline.SetHorizontalAlignCenter()
			textline.SetVerticalAlignCenter()	
			
		textline.Show()
		return textline
		
	def CreateBoard(self, width, height, x, y):
		board = ui.BoardWithTitleBar()
		board.SetSize(width, height)
		board.SetPosition(x, y)
		board.AddFlag("movable")
		board.AddFlag("float")
		board.AddFlag("animate")
		#board.Show()
		return board

	def CreateThinBoard(self, parent, width, height, x, y):
		board = ui.ThinBoard()
		board.SetParent(parent)
		board.SetSize(width, height)
		board.SetPosition(x, y)
		board.Show()
		return board

	def CreateScrollbar(self, parent, height, x, y):
		scrollbar = ui.ScrollBar()
		scrollbar.SetParent(parent)
		scrollbar.SetScrollBarSize(height)
		scrollbar.SetPosition(x, y)
		#scrollbar.HideButtons()
		scrollbar.Show()
		return scrollbar

	def CreateImageBox(self, parent, x, y, image = ""):
		img = ui.ExpandedImageBox()
		img.SetParent(parent)
		img.SetPosition(x,y)
		img.LoadImage(image)
		#textline.SetText(text)
		img.Show()
		return img		
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.Hide()

	def Open(self):
		if FALSE == self.is_loaded:
			self.__LoadGui()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE

	def OnPressExitKey(self):
		self.Close()
		return TRUE
		

class CreateBioBoard(ui.ScriptWindow):
	def __init__(self, parent, x, y, iface):
		ui.ScriptWindow.__init__(self)
		
		self.PulseSpeed = 0.018
		self.PulseCounter = 0.01
		self.PulseVector = "+"
		self.PulseMode = False
		
		self.LastLevel = 0
		self.DataSave = None
		self.QuestState = 0
		
		self.tooltipItems = []
		BOARD_SIZE_H = 44
		BOARD_SIZE_W = 290
		SLOT_SIZE = 32
		
		self.interface = iface
		
		self.board = self.CreateBoard(parent, 350, 50, x, y)
		self.bg_board = self.CreateBGBoard(self.board, 350, 50, 0, 0)
		
		if self.PulseMode == False:
			self.bg_board.Hide()
		
		self.StatusText = self.CreateTextline(self.board, 12 + 24, BOARD_SIZE_H / 2 - 8, "Lv. 30: Completed")
		self.BackgroundImg = self.CreateImageBox(self.board, 8, BOARD_SIZE_H / 2 - 8 - 4, "bio_assets/design_info.tga"),
		self.BG_Select = self.CreateCustomButton(self.board, 8, BOARD_SIZE_H / 2 - 8 - 4, "", None),
		self.Arrow1 = self.CreateImageBox(self.board, BOARD_SIZE_W - 32 - 33, (BOARD_SIZE_H / 2) - (8 / 2) -2, "bio_assets/right_arrow1.tga"),
		self.Arrow2 = self.CreateImageBox(self.board, BOARD_SIZE_W - SLOT_SIZE - 20 - 32 - 37, (BOARD_SIZE_H / 2) - (8 / 2) -2, "bio_assets/right_arrow1.tga"),
		self.SlotImages = [
			self.CreateImageBox(self.board, BOARD_SIZE_W - SLOT_SIZE - 20 - 32 - 24- 32 - 24, (BOARD_SIZE_H / 2) - (SLOT_SIZE / 2) -5, "bio_assets/slot_base_01.tga"),		
			self.CreateImageBox(self.board, BOARD_SIZE_W - SLOT_SIZE - 20 - 32 - 24, (BOARD_SIZE_H / 2) - (SLOT_SIZE / 2) -5, "bio_assets/slot_base_01.tga"),	
			self.CreateImageBox(self.board, BOARD_SIZE_W - SLOT_SIZE - 20, (BOARD_SIZE_H / 2) - (SLOT_SIZE / 2) -5, "bio_assets/slot_base_01.tga"),					
		]					
		
		self.tooltipItems.append(uiToolTip.ItemToolTip())
		self.tooltipItems.append(uiToolTip.ItemToolTip())
		self.tooltipItems.append(uiToolTip.ItemToolTip())
		
	def ChatIndex(self, text):
		chat.AppendChat(chat.CHAT_TYPE_INFO, '%s on index %d' % (text, self.index))
		
	def GetStatus(self, status):
		if status == 0:
			return localeInfo.BIO_NO_MIX_INACTIVE
		elif status == 1:
			return localeInfo.BIO_NO_MIX_RUNNING
		else:
			return localeInfo.BIO_NO_MIX_COMPLETED
		

	def SetBoardInfo(self, index, data):
		self.index = index
		self.DataSave = data
		
		self.StatusText.SetText("Lv. %d: %s" % (data["LEVEL"], self.GetStatus(data["STATUS"])))
		
		self.BG_Select[0].SetEvent(lambda : self.interface.UpdateSelection(self.index))
		
		self.slots = []
		
		counter = 0
		for x in data["ITEMS"]:
			self.slots.append(self.CreateSlot(self.SlotImages[counter], x))	
			self.tooltipItems[counter].ClearToolTip()
			self.tooltipItems[counter].SetItemToolTip(x)
			self.tooltipItems[counter].HideToolTip()
			
			counter += 1
		
		
		data_status = data["STATUS"]
		self.LastLevel = player.GetStatus(player.LEVEL)
		if self.LastLevel < data["LEVEL"]:
			data_status = 0
		
		self.QuestState = data["STATE"]
		
		if data_status == 0:
			self.board.LoadImage("bio_assets/tab_normal_off.tga")
			self.BackgroundImg[0].LoadImage("bio_assets/design_info_off.tga")
			self.bg_board.Hide()
			self.PulseMode = False			
		elif data_status == 1:
			self.board.LoadImage("bio_assets/tab_normal.tga")
			self.BackgroundImg[0].LoadImage("bio_assets/design_info.tga")	
			self.bg_board.Show()
			
			for x in range(self.QuestState): ## 0 -> Semmi, 1 -> Az elsőt
				self.slots[x].SetAlpha(0.4)	
			
			self.PulseMode = True
		elif data_status == 2:
			self.board.LoadImage("bio_assets/tab_green1.tga")
			self.BackgroundImg[0].LoadImage("bio_assets/design_info_green.tga")		
			
			for x in range(len(self.slots)):
				self.slots[x].SetAlpha(0.4)				
				
			self.bg_board.Hide()
			self.PulseMode = False				
		

	def GetIndex(self):
		return self.index
	
	def CreateSlot(self, parent, vnum):
		item.SelectItem(vnum)
		
		ItemSlotImg = ui.ExpandedImageBox()
		ItemSlotImg.SetParent(parent)
		ItemSlotImg.SetPosition(4, 3)
		ItemSlotImg.LoadImage(item.GetIconImageFileName())
		ItemSlotImg.Show()
		
		return ItemSlotImg
		
	def HideBoard(self):
		self.board.Hide()
		
	def ShowBoard(self):
		self.board.Show()

	def Refresh(self):
		if self.LastLevel != player.GetStatus(player.LEVEL):
			self.SetBoardInfo(self.index, self.DataSave)
	
		for i in range(3):
			if self.slots[i].IsIn() == True:
				if self.tooltipItems[i]:
					self.tooltipItems[i].ShowToolTip()
			else:
				if self.tooltipItems[i]:
					self.tooltipItems[i].HideToolTip()	

		if self.PulseMode:
			if self.PulseVector == "+" and self.PulseCounter + self.PulseSpeed <= 0.75:
				self.PulseCounter += self.PulseSpeed
			elif self.PulseVector == "+" and self.PulseCounter + self.PulseSpeed > 0.75:
				self.PulseVector = "-"
			elif self.PulseVector == "-" and self.PulseCounter - self.PulseSpeed >= 0:
				self.PulseCounter -= self.PulseSpeed
			elif self.PulseVector == "-" and self.PulseCounter - self.PulseSpeed < 0:
				self.PulseVector = "+"		
				self.PulseCounter += self.PulseSpeed
				
			self.slots[self.QuestState].SetAlpha(self.PulseCounter)
			self.bg_board.SetAlpha(self.PulseCounter)	
		
	def CreateBar(self, parent, x, y, w, h):
		bar = ui.Bar()
		bar.SetParent(parent)
		bar.SetPosition(x, y)
		bar.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 1))
		bar.SetSize(w, h)
		bar.Show()
		return bar

	def CreateImageBox(self, parent, x, y, image = ""):
		img = ui.ExpandedImageBox()
		img.SetParent(parent)
		img.SetPosition(x,y)
		img.LoadImage(image)
		#textline.SetText(text)
		img.Show()
		return img		
	
	def CreateTextline(self, parent, x, y, text = ""):
		textline = ui.TextLine()
		textline.SetParent(parent)
		textline.SetPosition(x,y)
		textline.SetText(text)
		textline.Show()
		return textline
		
	def CreateBoard(self, parent, width, height, x, y):
		board = ui.ExpandedImageBox()
		board.SetParent(parent)
		board.SetSize(width, height)
		board.SetPosition(x, y)
		board.LoadImage("bio_assets/tab_normal.tga")
		board.SetTop()
		board.Show()
		return board

	def CreateBGBoard(self, parent, width, height, x, y):
		board = ui.ExpandedImageBox()
		board.SetParent(parent)
		board.SetSize(width, height)
		board.SetPosition(x, y)
		##board.LoadImage("bio_assets/tab_normal1_pulse.tga")
		board.LoadImage("bio_assets/tab_normal5.tga")
		board.SetTop()
		board.Show()
		return board

	def CreateCustomButton(self, parent, x, y, text, event):
		button = ui.Button()
		button.SetParent(parent)
		button.SetPosition(x, y)
		button.SetUpVisual("bio_assets/select.tga")
		button.SetOverVisual("bio_assets/select_1.tga")
		button.SetDownVisual("bio_assets/select_2.tga")
		button.SetText(text)
		button.SetEvent(event)
		button.Show()
		return button
		
	def CreateButton(self, parent, x, y, text, event):
		button = ui.Button()
		button.SetParent(parent)
		button.SetPosition(x, y)
		button.SetUpVisual("d:/ymir work/ui/public/Middle_Button_01.sub")
		button.SetOverVisual("d:/ymir work/ui/public/Middle_Button_02.sub")
		button.SetDownVisual("d:/ymir work/ui/public/Middle_Button_03.sub")
		button.SetText(text)
		button.SetEvent(event)
		button.Show()
		return button
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.Hide()
		