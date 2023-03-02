import ui
import player
import uiSoulStone
import mouseModule
import net
import app
import snd
import item
if app.ENABLE_BIOLOG_SYSTEM:
	import uiprofessionalbiolog, uiToolTip
import player
import chat
import grp
import uiScriptLocale
import uiRefine
import uiAttachMetin
import os
import uiToolTip
if app.ENABLE_OFFLINE_SHOP_SYSTEM:
	import uiOfflineShopBuilder
	import uiOfflineShop
import uiPickMoney2
import uiCommon
import uiPrivateShopBuilder # 개인상점 열동안 ItemMove 방지
import localeInfo
import constInfo
if app.ENABLE_REMEMBER_LAST_SPLIT:
	import systemSetting
import ime
import wndMgr
if app.ENABLE_SWAPITEM_SYSTEM:
	SWAPITEM_STAT = 1
import skybox_system
#import uiSideBar
import uifastequip
import teleport_system
import uiBonusPage
if app.ENABLE_CHANGELOOK_SYSTEM:
	import changelook
import event
if app.ENABLE_DRAGON_SOUL_CHANGE_BONUS_WORLDARD:
	import extern_wa_dragonsoul_bonus
ITEM_MALL_BUTTON_ENABLE = True

SCREENSHOT_CWDSAVE = False
SCREENSHOT_DIR = None

if localeInfo.IsEUROPE():
	SCREENSHOT_CWDSAVE = True

if localeInfo.IsCIBN10():
	SCREENSHOT_CWDSAVE = False
	SCREENSHOT_DIR = "YT2W"

if app.ENABLE_ACCE_COSTUME_SYSTEM:
	import acce
ITEM_FLAG_APPLICABLE = 1 << 14


class BeltInventoryWindow(ui.ScriptWindow):

	def __init__(self, wndInventory):
		import exception

		if not app.ENABLE_NEW_EQUIPMENT_SYSTEM:
			exception.Abort("What do you do?")
			return

		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;

		self.wndBeltInventoryLayer = None
		self.wndBeltInventorySlot = None
		self.expandBtn = None
		self.minBtn = None

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self, openBeltSlot = False):
		self.__LoadWindow()
		self.RefreshSlot()

		ui.ScriptWindow.Show(self)

		if openBeltSlot:
			self.OpenInventory()
		else:
			self.CloseInventory()

	def Close(self):
		self.Hide()

	def IsOpeningInventory(self):
		return self.wndBeltInventoryLayer.IsShow()

	def OpenInventory(self):
		self.wndBeltInventoryLayer.Show()
		#self.expandBtn.Hide()
		self.minBtn.Show()

		if localeInfo.IsARABIC() == 0:
			self.AdjustPositionAndSize()

	def CloseInventory(self):
		self.wndBeltInventoryLayer.Hide()
		self.minBtn.Hide()
		x = 0
		self.wndInventory.ShowShitButton(x)

		if localeInfo.IsARABIC() == 0:
			self.AdjustPositionAndSize()

	## 현재 인벤토리 위치를 기준으로 BASE 위치를 계산, 리턴.. 숫자 하드코딩하기 정말 싫지만 방법이 없다..
	if app.ENABLE_BIOLOG_SYSTEM:
		def GetBasePosition(self):
			x, y = self.wndInventory.GetGlobalPosition()
			return x - 148 + 30, y + 355
	else:
		def GetBasePosition(self):
			x, y = self.wndInventory.GetGlobalPosition()
			return x - 148 + 30, y + 241	

	def AdjustPositionAndSize(self):
		bx, by = self.GetBasePosition()

		if self.IsOpeningInventory():
			self.SetPosition(bx, by)
			self.SetSize(self.ORIGINAL_WIDTH, self.GetHeight())

		else:
			self.SetPosition(bx + 138, by);
			self.SetSize(10, self.GetHeight())

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/BeltInventoryWindow.py")
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			self.ORIGINAL_WIDTH = self.GetWidth()
			wndBeltInventorySlot = self.GetChild("BeltInventorySlot")
			self.wndBeltInventoryLayer = self.GetChild("BeltInventoryLayer")
			self.expandBtn = self.GetChild("ExpandBtn")
			self.minBtn = self.GetChild("MinimizeBtn")
			
			self.minBtn.Hide()
			self.expandBtn.Hide()
			self.expandBtn.SetEvent(ui.__mem_func__(self.OpenInventory))
			self.minBtn.SetEvent(ui.__mem_func__(self.CloseInventory))

			if localeInfo.IsARABIC() :
				self.expandBtn.SetPosition(self.expandBtn.GetWidth() - 2, 15)
				self.wndBeltInventoryLayer.SetPosition(self.wndBeltInventoryLayer.GetWidth() - 5, 0)
				self.minBtn.SetPosition(self.minBtn.GetWidth() + 3, 15)

			for i in xrange(item.BELT_INVENTORY_SLOT_COUNT):
				slotNumber = item.BELT_INVENTORY_SLOT_START + i
				wndBeltInventorySlot.SetCoverButton(slotNumber,	"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/belt_inventory/slot_disabled.tga", False, False)

		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		## Equipment
		wndBeltInventorySlot.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndBeltInventorySlot.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndBeltInventorySlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndBeltInventorySlot.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndBeltInventorySlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		wndBeltInventorySlot.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))

		self.wndBeltInventorySlot = wndBeltInventorySlot

	def RefreshSlot(self):
		getItemVNum=player.GetItemIndex

		for i in xrange(item.BELT_INVENTORY_SLOT_COUNT):
			slotNumber = item.BELT_INVENTORY_SLOT_START + i
			self.wndBeltInventorySlot.SetItemSlot(slotNumber, getItemVNum(slotNumber), player.GetItemCount(slotNumber))
			self.wndBeltInventorySlot.SetAlwaysRenderCoverButton(slotNumber, True)

			avail = "0"

			if player.IsAvailableBeltInventoryCell(slotNumber):
				self.wndBeltInventorySlot.EnableCoverButton(slotNumber)
			else:
				self.wndBeltInventorySlot.DisableCoverButton(slotNumber)

		self.wndBeltInventorySlot.RefreshSlot()

if app.ENABLE_BIOLOG_SYSTEM:
###################################################################
# title_name		: Professional Biolog System
# date_created		: 2016.08.07
# filename			: uiInventory.py
# author			: VegaS
# version_actual	: Version 0.2.6
#
	class CollectInventoryWindow(ui.ScriptWindow):
		def __init__(self, wndInventory):
			import exception
			if not wndInventory:
				exception.Abort("wndInventory parameter must be set to CollectInventoryWindow")
				return
			ui.ScriptWindow.__init__(self)
			self.isLoaded = 0
			self.updated = 0
			self.wndInventory = wndInventory;
			self.tooltipItem = uiToolTip.ItemToolTip()
			self.tooltipItem.Hide()
			self.wndBeltInventoryLayer = None
			self.wndBeltInventorySlot = None
			self.expandBtn = None
			self.minBtn = None
			self.gameWindow = None
			self.__LoadWindow()
			self.expandBtn.SetParent(wndInventory)
			self.expandBtn.SetPosition(28, 410)

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def Show(self, openBeltSlot = False):
			self.__LoadWindow()
			ui.ScriptWindow.Show(self)

			if openBeltSlot:
				self.OpenInventory()
			else:
				self.CloseInventory()

		def Close(self):
			self.Hide()

		def IsOpeningInventory(self):
			return self.wndBeltInventoryLayer.IsShow()

		def OpenInventory(self):
			self.wndBeltInventoryLayer.Show()
			self.expandBtn.Hide()

			self.AdjustPositionAndSize()

		def CloseInventory(self):
			self.wndBeltInventoryLayer.Hide()
			self.expandBtn.Show()

			self.AdjustPositionAndSize()

		def GetBasePosition(self):
			x, y = self.wndInventory.GetGlobalPosition()
			return 30 + x - 148, y + 260
			
		def AdjustPositionAndSize(self):
			bx, by = self.GetBasePosition()

			if self.IsOpeningInventory():
				self.SetPosition(bx, by)
				self.SetSize(self.ORIGINAL_WIDTH, self.GetHeight())
			else:
				self.SetPosition(bx + 138, by);
				self.SetSize(10, self.GetHeight())

		def __LoadWindow(self):
			if self.isLoaded == 1:
				return

			self.isLoaded = 1

			try:
				pyScrLoader = ui.PythonScriptLoader()
				pyScrLoader.LoadScriptFile(self, "UIScript/biolog_collectinventorywindow.py")
			except:
				import exception
				exception.Abort("CollectInventoryWindow.LoadWindow.LoadObject")

			try:
				self.ORIGINAL_WIDTH = self.GetWidth()
				self.wndBeltInventoryLayer = self.GetChild("BeltInventoryLayer")
				self.wndItem = self.GetChild("BeltInventorySlot")
				self.time_value = self.GetChild("time_value")
				self.biolog_count = self.GetChild("count_value")
				self.expandBtn = self.GetChild("ExpandBtn")
				self.minBtn = self.GetChild("MinimizeBtn")
				self.sendBtn = self.GetChild("send_biolog")
				self.expandBtn.SetEvent(ui.__mem_func__(self.OpenInventory))
				self.minBtn.SetEvent(ui.__mem_func__(self.CloseInventory))
				self.wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
				self.wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			except:
				import exception
				exception.Abort("CollectInventoryWindow.LoadWindow.BindObject")

			if self.sendBtn:
				self.sendBtn.SetEvent(ui.__mem_func__(self.AcceptBiolog))

		def SetItem(self, arg1, arg2, arg3):
			self.wndItem.SetItemSlot(0, int(uiprofessionalbiolog.BIOLOG_BINARY_LOADED["vnum"][0]), 0)
			
		def AcceptBiolog(self):
			net.SendChatPacket("/biolog")

		def SetTime(self, time):
			time_collect = time - app.GetGlobalTimeStamp()

			if time_collect < 0:
				time_collect = 0 

			if time_collect == 1:
				self.wndLeftTime = uiprofessionalbiolog.Biolog_TimeExpired()
				self.wndLeftTime.OpenWindow()
				self.wndLeftTime.Show()

			self.time_value.SetText(localeInfo.FormatTime(time_collect))

		def OnUpdate(self):
			self.SetTime(int(uiprofessionalbiolog.BIOLOG_BINARY_LOADED["time"][0]))
			self.SetItem(0, uiprofessionalbiolog.BIOLOG_BINARY_LOADED["vnum"][0], 0)
			self.biolog_count.SetText(uiprofessionalbiolog.BIOLOG_BINARY_LOADED['countActual'][0] + "/" + uiprofessionalbiolog.BIOLOG_BINARY_LOADED['countNeed'][0])

		def OverInItem(self):
			if uiprofessionalbiolog.BIOLOG_BINARY_LOADED["vnum"][0]:
				self.tooltipItem.SetItemToolTip(uiprofessionalbiolog.BIOLOG_BINARY_LOADED["vnum"][0])

		def OverOutItem(self):
			if self.tooltipItem:
				self.tooltipItem.HideToolTip()	

class InventoryWindow(ui.ScriptWindow):
	liHighlightedItems = []

	USE_TYPE_TUPLE = ("USE_CLEAN_SOCKET", "USE_CHANGE_ATTRIBUTE", "USE_ADD_ATTRIBUTE", "USE_ADD_ATTRIBUTE2", "USE_ADD_ACCESSORY_SOCKET", "USE_PUT_INTO_ACCESSORY_SOCKET", "USE_PUT_INTO_BELT_SOCKET", "USE_PUT_INTO_RING_SOCKET", "USE_CHANGE_COSTUME_ATTR", "USE_RESET_COSTUME_ATTR")
	if app.ENABLE_6_7_BONUS_NEW_SYSTEM:
		W =	list(USE_TYPE_TUPLE)
		W.append("USE_CHANGE_ATTRIBUTE2")
		USE_TYPE_TUPLE=tuple(W)
	if app.CHANGE_PETSYSTEM:
		CP =	list(USE_TYPE_TUPLE)
		CP.append("USE_CHANGE_LV_P")
		USE_TYPE_TUPLE=tuple(CP)

	questionDialog = None
	INVENTAR_BONUS_PAGE = False
	tooltipItem = None
	wndCostume = None
	wndRune = None
	wndBelt = None
	wndSoulStone = None
	dlgPickMoney = None
	interface = None
	if app.WJ_ENABLE_TRADABLE_ICON:
		bindWnds = []
	#HAVE_SIDEBAR = True
	#wndSidebar = None
	if app.ENABLE_BIOLOG_SYSTEM:
		wndCollect = None
	wndSystem = None
		
	SPACE_BONUS_INVENTORY = 130 # 

	sellingSlotNumber = -1
	isLoaded = 0
	isOpenedCostumeWindowWhenClosingInventory = 0		# 인벤토리 닫을 때 코스츔이 열려있었는지 여부-_-; 네이밍 ㅈㅅ
	isOpenedBeltWindowWhenClosingInventory = 0		# 인벤토리 닫을 때 벨트 인벤토리가 열려있었는지 여부-_-; 네이밍 ㅈㅅ
	#isOpenedSideBarWindowWhenClosingInventory = 0
	if app.ENABLE_BIOLOG_SYSTEM:
		isOpenedCollectWindowWhenClosingInventory = 0
	isOpenedSystemWindowWhenClosingInventory = 0	
	canShowSwitchLow = 0
	canShowEquipChange = 0

	if app.GLOW_EFFECT:
		GLOW_EFFECT = {
			0 : [0,  "d:/ymir work/ui/game/glow/slot_glow.tga", 0.01, 0.0, 1.0, grp.GenerateColor(1.0, 0.0, 0.0, 1.0)],#fire
			1 : [0, "d:/ymir work/ui/game/glow/slot_glow.tga", 0.01, 0.0, 1.0, grp.GenerateColor(0.0, 0.6863, 0.0, 1.0)],#wind
			2 : [0, "d:/ymir work/ui/game/glow/slot_glow.tga", 0.01, 0.0, 1.0, grp.GenerateColor(0.7451, 0.0, 1.0, 1.0)],#dark
			3 : [0, "d:/ymir work/ui/game/glow/slot_glow.tga", 0.01, 0.0, 1.0, grp.GenerateColor(0.7647, 0.7647, 0.0, 1.0)],#earth
			4 : [0, "d:/ymir work/ui/game/glow/slot_glow.tga", 0.01, 0.0, 1.0, grp.GenerateColor(0.0, 0.0, 1.0, 1.0)],#ice
			5 : [0,  "d:/ymir work/ui/game/glow/slot_glow.tga", 0.01, 0.0, 1.0, grp.GenerateColor(0.0, 0.8235, 1.0, 1.0)],#ligtning
		}

	def __init__(self, interface):
	
		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyBar = None
			self.wndGem = None		
			
		ui.ScriptWindow.__init__(self)
		self.isOpenedBeltWindowWhenClosingInventory = 0		# AIº￥Aa¸® ´YA≫ ¶§ º§Æ® AIº￥Aa¸®°¡ ¿­·AAO¾u´AAo ¿ⓒºI-_-; ³×AI¹O ¤¸¤μ
		#self.isOpenedSideBarWindowWhenClosingInventory = 0
		
		self.inventoryPageIndex = 0
		
		self.BonusPageBoard = None
		self.interface=interface

		self.canShowSwitchLow = 0
		self.canShowEquipChange = 0	
		
		self.status_autopickup = False

		self.teleportsystem = teleport_system.teleportwindow()
		self.skyboxsystem = skybox_system.MentaLGui()		

		#start edit...
		if app.__ENABLE_TRASH_BIN__:
			self.trashBinTargetSlot  = 0
			self.trashBinTargetIndex = 0
			self.trashBinTargetCount = 0
			
			self.trashBin		 = None
			self.showTrashBinBtn = None
			self.hideTrashBinBtn = None

		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			self.elemets_hide = []
			self.elemets_world = {}

		self.CurrPage = 0
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyBar = None
			self.wndGem = None

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)

		if self.wndSystem:
			self.wndSystem.Show(self.isOpenedSystemWindowWhenClosingInventory)

		# 인벤토리를 닫을 때 코스츔이 열려있었다면 인벤토리를 열 때 코스츔도 같이 열도록 함.
		if self.isOpenedCostumeWindowWhenClosingInventory and self.wndCostume:
			self.wndCostume.Show()
			
		if app.ENABLE_BIOLOG_SYSTEM:
			if self.wndCollect:
				self.wndCollect.Show(self.isOpenedCollectWindowWhenClosingInventory)

		# AIº￥Aa¸®¸| ´YA≫ ¶§ º§Æ® AIº￥Aa¸®°¡ ¿­·AAO¾u´U¸e °°AI ¿­μμ·I CO.
		if self.wndBelt:
			self.wndBelt.Show(self.isOpenedBeltWindowWhenClosingInventory)

		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyBar:
				self.wndExpandedMoneyBar.Show()
			
		#if self.wndSidebar:
		#	self.wndSidebar.Show(self.isOpenedSideBarWindowWhenClosingInventory)
			
		#start edit.....
# CESTINO DISABILITATO!
#		if app.__ENABLE_TRASH_BIN__:
#			try:
#				self.showTrashBinBtn.Show()
#				self.AlignTrashBin()
#			except:
#				pass
		#end edit.....
		
		if self.INVENTAR_BONUS_PAGE == True:
			self.GetChild("Money_Slot").SetPosition(8, 28)
		else:
			self.GetChild("Money_Slot").SetPosition(-55, 28)
			
		if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
			constInfo.IsInventoryOpened = True

		# 인벤토리를 닫을 때 벨트 인벤토리가 열려있었다면 같이 열도록 함.
		if self.wndBelt:
			self.wndBelt.Show(self.isOpenedBeltWindowWhenClosingInventory)
			
		#if self.wndSidebar:
		#	self.wndSidebar.Show(self.isOpenedSideBarWindowWhenClosingInventory)

	#def BindInterfaceClass(self, interface):
	#	self.interface = interface
	if app.WJ_ENABLE_TRADABLE_ICON:
		def BindWindow(self, wnd):
			self.bindWnds.append(wnd)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()

			#if app.ENABLE_EXTEND_INVEN_SYSTEM:
			pyScrLoader.LoadScriptFile(self, "UIScript/InventoryWindowEx.py")
 			#else:
			#	if ITEM_MALL_BUTTON_ENABLE:
			#		pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "InventoryWindow.py")
			#	else:
			#		pyScrLoader.LoadScriptFile(self, "UIScript/InventoryWindow.py")
		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.LoadObject")

		try:
			wndItem = self.GetChild("ItemSlot")
			talizmaneffect1 = self.GetChild("talizmaneffect1")
			talizmaneffect2 = self.GetChild("talizmaneffect2")
			talizmaneffect3 = self.GetChild("talizmaneffect3")
			talizmaneffect4 = self.GetChild("talizmaneffect4")
			talizmaneffect5 = self.GetChild("talizmaneffect5")
			talizmaneffect6 = self.GetChild("talizmaneffect6")
			wndEquip = self.GetChild2("EquipmentSlot")
			self.talisman_info_btn = self.GetChild("talisman_info_btn")
			if app.ENABLE_ANTI_EXP:
				self.GetChild("AntiExp").SetEvent(ui.__mem_func__(self.__ClickAntiExp))
			
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.wndMoney = self.GetChild("Money")
			self.wndMoneySlot = self.GetChild("Money_Slot")
			#if app.ENABLE_EXTEND_INVEN_SYSTEM:
			#	self.EX_INVEN_COVER_IMG_CLOSE = []
			#	self.EX_INVEN_COVER_IMG_OPEN = []
			#	for i in xrange(9):
			#		self.EX_INVEN_COVER_IMG_OPEN.append(self.GetChild("cover_open_" + str(i)))
			#		self.EX_INVEN_COVER_IMG_CLOSE.append(self.GetChild("cover_close_" + str(i)))
			self.mallButton = self.GetChild2("MallButton")
			self.LagerButton = self.GetChild2("LagerButton")
			self.DSSButton = self.GetChild2("DSSButton")
			self.MantelloButton = self.GetChild2("MantelloButton")
			#self.costumeButton = self.GetChild2("CostumeButton")
			self.runeButton = self.GetChild2("RuneButton")
			#/////////
			self.wndMoneyIcon = self.GetChild("Money_Icon")
			
			self.wndSystem = SystemInventoryWindow(self)
			if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR == 1:
				self.wndMoney.Hide()
				self.wndMoneyIcon.Hide()
				self.wndMoneySlot.Hide()
			else:
				self.wndMoneyIcon.Show()
				self.wndMoneySlot.Show()

			height = self.GetHeight()
			width = self.GetWidth()
			self.SetSize(width + 30, height - 22)
			self.GetChild("board").SetSize(width, height - 22)
			
			self.toolTip = uiToolTip.ToolTip()
			self.toolTip.ClearToolTip()
			#////////////
			
			# BEGIN_OFFLINE_SHOP
			self.offlineShopButton = self.GetChild2("OfflineShopButton")
			# END_OF_OFFLINE_SHOP			
			#self.ButonMinimize = self.GetChild2("MinimierenButton")

			self.inventoryTab = []
			for i in xrange(player.INVENTORY_PAGE_COUNT):
				self.inventoryTab.append(self.GetChild("Inventory_Tab_%02d" % (i+1)))

			self.equipmentTab = []
			self.equipmentTab.append(self.GetChild("Equipment_Tab_01"))
			self.equipmentTab.append(self.GetChild("Equipment_Tab_02"))
			

			## New Pagination
			
			# Bg-Show/Hide
			self.equipPage = []
			self.equipPage.append(self.GetChild("Equipment_Base"))
			self.equipPage.append(self.GetChild("Equipment_Page_Secondary"))
			self.equipPage.append(self.GetChild("Equipment_Page_Cosmetics"))
			self.equipPage.append(self.GetChild("Equipment_Page_Talismans"))
			
			#Btn-Pages
			self.btnPages = []
			self.btnPages.append(self.GetChild2("PaginationOne"))
			self.btnPages.append(self.GetChild2("PaginationTwo"))
			self.btnPages.append(self.GetChild2("PaginationThree"))
			self.btnPages.append(self.GetChild2("PaginationFourth"))
			
			self.btnPages[0].Down() # Let's select first page            

			self.shitbuttons = []
			self.shitbuttons.append(self.GetChild2("beltbuttonshit"))
			#self.shitbuttons.append(self.GetChild2("systembuttonshit"))

			if app.ENABLE_SORT_INVEN:
				#self.yenilebutton = self.GetChild2("YenileButton")
				#self.yenilebutton.SetEvent(ui.__mem_func__(self.ClickYenileButton))
				self.tooltipI = uiToolTip.ToolTip()
				self.tooltipI.Hide()
				self.tooltipInfo = [self.tooltipI]*4
				self.InformationText = [localeInfo.YENILE_BUTTON_TITLE,
										localeInfo.YENILE_BUTTON,
										localeInfo.YENILE_BUTTON2,
										localeInfo.YENILE_BUTTON3
				]
				for i in xrange(len(self.tooltipInfo)):
					self.tooltipInfo[i].SetFollow(True)
					self.tooltipInfo[i].AlignHorizonalCenter()
					if i == 0:
						self.tooltipInfo[i].AppendTextLine(self.InformationText[i], 0xffffff00)
					else:
						self.tooltipInfo[i].AppendTextLine(self.InformationText[i])
					self.tooltipInfo[i].Hide()
			if app.ENABLE_CHEQUE_SYSTEM:
				self.wndCheque = self.GetChild("Cheque")
				self.wndChequeIcon = self.GetChild("Cheque_Icon")
				self.wndChequeSlot = self.GetChild("Cheque_Slot")
				if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR == 1:
					self.wndCheque.Hide()
					self.wndChequeIcon.Hide()
					self.wndChequeSlot.Hide()
			#if self.costumeButton and not app.ENABLE_COSTUME_SYSTEM:
			#	self.costumeButton.Hide()
			#	self.costumeButton.Destroy()
			#	self.costumeButton = 0

			#if app.ENABLE_EXTEND_INVEN_SYSTEM:
			#	for i in xrange(9):
			#		self.EX_INVEN_COVER_IMG_CLOSE[i].Hide()
			#		self.EX_INVEN_COVER_IMG_OPEN[i].Hide()

			# Belt Inventory Window
			self.wndBelt = None
			
			#self.fastequipdlg = uifastequip.changeequip()
			
			if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
				self.wndBelt = BeltInventoryWindow(self)
			if app.ENABLE_BIOLOG_SYSTEM:
				self.wndCollect = None
				self.wndCollect = CollectInventoryWindow(self)
			
			
				
			#self.wndSidebar = None
			#if self.HAVE_SIDEBAR:
			#	self.wndSidebar = uiSideBar.SideBarWindow(self)
			#	## QUI DEVI MODIFICARE I BOTTONI CON LE RELATIVE FUNZIONI
			#	## Nome funzione, immagine up, immagine over, immagine down
			#	self.wndSidebar.AddButton(ui.__mem_func__(self.ToggleSwitchbotWindow), "d:/ymir work/ui/sidebarinventory/buy_switch_item_button_default.tga", "d:/ymir work/ui/sidebarinventory/buy_switch_item_button_over.tga", "d:/ymir work/ui/sidebarinventory/buy_switch_item_button_default.tga", "Switcher")
			#	self.wndSidebar.AddButton(ui.__mem_func__(self.__quikeqchange), "d:/ymir work/ui/sidebarinventory/shirt_default.tga", "d:/ymir work/ui/sidebarinventory/shirt_over.tga", "d:/ymir work/ui/sidebarinventory/shirt_default.tga", "Equipment")
			#	self.wndSidebar.AddButton(ui.__mem_func__(self.__BonusPage), "d:/ymir work/ui/sidebarinventory/bonus_default.tga", "d:/ymir work/ui/sidebarinventory/bonus_over.tga", "d:/ymir work/ui/sidebarinventory/bonus_default.tga", "Bonus")	
			#	self.wndSidebar.AddButton(ui.__mem_func__(self.OpenTeleportSystem), "d:/ymir work/ui/sidebarinventory/map_default.tga", "d:/ymir work/ui/sidebarinventory/map_over.tga", "d:/ymir work/ui/sidebarinventory/map_default.tga", "Map")
			#	self.wndSidebar.AddButton(ui.__mem_func__(self.OpenMentaLSkyGui), "d:/ymir work/ui/sidebarinventory/sky_default.tga", "d:/ymir work/ui/sidebarinventory/sky_over.tga", "d:/ymir work/ui/sidebarinventory/sky_default.tga", "Sky")
			#	self.wndSidebar.AddButton(ui.__mem_func__(self.__EnablePickUpItem), "d:/ymir work/ui/sidebarinventory/pick_default.tga", "d:/ymir work/ui/sidebarinventory/pick_over.tga", "d:/ymir work/ui/sidebarinventory/pick_default.tga", "Pick Up")
			#	self.wndSidebar.AddButton(ui.__mem_func__(self.__OpenDSGui), "d:/ymir work/ui/sidebarinventory/screen_default.tga", "d:/ymir work/ui/sidebarinventory/screen_over.tga", "d:/ymir work/ui/sidebarinventory/screen_default.tga", "Dragon Soul")

		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.BindObject")

		## Item
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		## Equipment
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		# self.talisman_info_btn.OnMouseOverIn = ui.__mem_func__(self.OverInTIB)
		# self.talisman_info_btn.OnMouseOverOut = ui.__mem_func__(self.OverOutTIB)
		self.talisman_info_btn.SetOverEvent(ui.__mem_func__(self.OverInTIB))
		self.talisman_info_btn.SetOverOutEvent(ui.__mem_func__(self.OverOutTIB))

		## PickMoneyDialog
		dlgPickMoney = uiPickMoney2.PickMoneyDialog2()
		dlgPickMoney.LoadDialog()
		dlgPickMoney.Hide()

		## RefineDialog
		self.refineDialog = uiRefine.RefineDialog()
		self.refineDialog.Hide()

		## AttachMetinDialog
		if app.WJ_ENABLE_TRADABLE_ICON:  
			self.attachMetinDialog = uiAttachMetin.AttachMetinDialog(self)
			self.BindWindow(self.attachMetinDialog)
		else:
			self.attachMetinDialog = uiAttachMetin.AttachMetinDialog()
		self.attachMetinDialog.Hide()


		for i in xrange(player.INVENTORY_PAGE_COUNT):
			self.inventoryTab[i].SetEvent(lambda arg=i: self.SetInventoryPage(arg))
		self.inventoryTab[0].Down()

		self.equipmentTab[0].SetEvent(lambda arg=0: self.SetEquipmentPage(arg))
		self.equipmentTab[1].SetEvent(lambda arg=1: self.SetEquipmentPage(arg))
		self.equipmentTab[0].Down()
		self.equipmentTab[0].Hide()
		self.equipmentTab[1].Hide()


		self.talizmaneffect1 = talizmaneffect1
		self.talizmaneffect2 = talizmaneffect2
		self.talizmaneffect3 = talizmaneffect3
		self.talizmaneffect4 = talizmaneffect4
		self.talizmaneffect5 = talizmaneffect5
		self.talizmaneffect6 = talizmaneffect6

		self.wndItem = wndItem
		self.wndEquip = wndEquip
		self.dlgPickMoney = dlgPickMoney
		#if app.ENABLE_EXTEND_INVEN_SYSTEM:
		#	for i in xrange(9):
		#		self.EX_INVEN_COVER_IMG_OPEN[i].SetEvent(ui.__mem_func__(self.en_ac))
				
		# MallButton
		if self.mallButton:
			self.mallButton.SetEvent(ui.__mem_func__(self.ClickMallButton))
			
		if self.LagerButton:
			self.LagerButton.SetEvent(ui.__mem_func__(self.ClickLagerButton))

		if self.MantelloButton:
			self.MantelloButton.SetEvent(ui.__mem_func__(self.ClickMantelloButton))
			
		#if self.ButonMinimize:
			#self.ButonMinimize.SetEvent(ui.__mem_func__(self.MinimiereBonus))

		if self.DSSButton:
			self.DSSButton.SetEvent(ui.__mem_func__(self.ClickDSSButton))

		# Costume Button
		#if self.costumeButton:
		#	self.costumeButton.SetEvent(ui.__mem_func__(self.ClickCostumeButton))

		# Rune Button
		if self.runeButton:
			self.runeButton.SetEvent(ui.__mem_func__(self.ClickRuneButton))

		# BEGIN_OFFLINE_SHOP
		if self.offlineShopButton:
			self.offlineShopButton.SetEvent(ui.__mem_func__(self.ClickOfflineShopButton))
		# END_OF_OFFLINE_SHOP
		for x in xrange(len(self.btnPages)):
			self.btnPages[x].SetEvent(ui.__mem_func__(self.SelectPage), x)
		
		#self.wndCostume = None
		self.wndSoulStone = None
 		#####

		for x in xrange(len(self.shitbuttons)):
			self.shitbuttons[x].SetEvent(ui.__mem_func__(self.ClickShitButton), x)


		## Refresh
		if app.ENABLE_HIGHLIGHT_SYSTEM:
			self.listHighlightedSlot = []
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.listAttachedAcces = []
		if app.ENABLE_CHANGELOOK_SYSTEM:
			self.listAttachedCl = []
		
		self.RefreshItemSlot() # for this 
		self.SetInventoryPage(0)
		self.SetEquipmentPage(0)
		self.SelectPage(0)
		self.RefreshStatus()
		self.ReloadBonus()
		
		if app.__ENABLE_TRASH_BIN__:
			trashBin = ui.ImageBox()
			trashBin.LoadImage("d:/ymir work/ui/trash_bin/trash_bin.sub")
			trashBin.Hide()
			trashBin.SetOnMouseLeftButtonUpEvent(ui.__mem_func__(self.OnMouseLeftButtonUpTrashBinCheck))
			
			
			showTrashBinBtn = ui.Button()
			showTrashBinBtn.SetUpVisual("d:/ymir work/ui/trash_bin/show_trashbin_up.sub")
			showTrashBinBtn.SetOverVisual("d:/ymir work/ui/trash_bin/show_trashbin_over.sub")
			showTrashBinBtn.SetDownVisual("d:/ymir work/ui/trash_bin/show_trashbin_down.sub")
			showTrashBinBtn.Hide()
			showTrashBinBtn.SetEvent(ui.__mem_func__(self.OnClickShowTrashBinBtn))
			
			hideTrashBinBtn = ui.Button()
			hideTrashBinBtn.SetUpVisual("d:/ymir work/ui/trash_bin/hide_trashbin_up.sub")
			hideTrashBinBtn.SetOverVisual("d:/ymir work/ui/trash_bin/hide_trashbin_over.sub")
			hideTrashBinBtn.SetDownVisual("d:/ymir work/ui/trash_bin/hide_trashbin_down.sub")
			hideTrashBinBtn.Hide()
			hideTrashBinBtn.SetEvent(ui.__mem_func__(self.OnClickHideTrashBinBtn))
			
			if not trashBin or not showTrashBinBtn or not hideTrashBinBtn:
				print("DEBUG")
			
			self.trashBin = trashBin
			self.showTrashBinBtn = showTrashBinBtn
			self.hideTrashBinBtn = hideTrashBinBtn
			
			self.AlignTrashBin()
	
		self.CreateTalismanTT()
		self.MinimiereBonus() # @test

	if app.ENABLE_ANTI_EXP:
		def __ClickAntiExp(self):
			net.SendChatPacket("/anti_exp")

	def SelectPage(self, page):
		for x in xrange(len(self.equipPage)):
			if x == page:
				self.equipPage[x].Show()
				if x == 0:
					self.ReloadPage("EquipmentSlot")
				elif x == 1:
					self.ReloadPage("Equipment_Slot_Secondary")
				elif x == 2:
					self.ReloadPage("Equipment_Slot_Cosmetics")
				elif x == 3:
					self.ReloadPage("Equipment_Slot_Talismans")
				## Add here more.
				continue
				
			self.equipPage[x].Hide()
			
		self.RefreshButtonPage(page)
		self.RefreshItemSlot()
		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			self.RefreshCostumeHideButtonPage(page)
	
	def RefreshButtonPage(self, SelectPage):
		for x in xrange(len(self.btnPages)):
			if x == SelectPage:
				self.btnPages[x].Down()
				continue
				
			self.btnPages[x].SetUp()


	def CreateTalismanTT(self):
		self.toolTipTalismanINFO = uiToolTip.ToolTip()
		self.toolTipTalismanINFO.AppendTextLine(localeInfo.TALISMAN_WHHEL)
		self.toolTipTalismanINFO.HideToolTip()

	def OverInTIB(self):
		self.toolTipTalismanINFO.ShowToolTip()

	def OverOutTIB(self):
		self.toolTipTalismanINFO.HideToolTip()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def RefreshCostumeHideButtonPage(self, SelectPage):
			if SelectPage == 2:
				constInfo.hide_buttons = 0
				for i in xrange(self.GetSlotCount()):
					self.elemets_world["hide_button_%d"%i].Show()
			else:
				if constInfo.hide_buttons == 0:
					constInfo.hide_buttons = 1
					for i in xrange(self.GetSlotCount()):
						self.elemets_world["hide_button_%d"%i].Hide()

	def ReloadPage(self, namePage):
		self.wndEquip = self.GetChild(namePage)
		
		## Equipment
		self.wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		self.wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		self.wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		self.wndEquip.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		self.wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))	

	
	def ToggleSwitchbotWindow(self):
		if self.interface:
			self.interface.ToggleSwitchbotWindow()

	def __Switchlow(self):
		if self.canShowSwitchLow == 0:
			self.switch.Show()
			self.canShowSwitchLow = 1
		else:
			self.switch.Hide()
			self.canShowSwitchLow = 0    
            
	def quikeqchange(self):
		if self.canShowEquipChange == 0:
			self.fastequipdlg.Show()
			self.canShowEquipChange = 1
		else:
			self.fastequipdlg.Hide()
			self.canShowEquipChange = 0

	# Ashens Bonus
	def BonusPage(self):
		
		try:
			if not self.BonusPageBoard:
				self.BonusPageBoard = uiBonusPage.BonusBoardDialog()
			else:
				if self.BonusPageBoard.IsShow():
					self.BonusPageBoard.Hide()
					
				else:
					self.BonusPageBoard.Show()
		
		
		except ImportError:
			import dbg,app
			dbg.Trace('uiBonusPage.py Importing error')
			app.Abort()
	# Ashens Bonus END
	
	def OpenTeleportSystem(self):
		if constInfo.TELEPORT_SYSTEM_GUI == 0:
			self.teleportsystem.Show()
			self.teleportsystem.SetTop()
			constInfo.TELEPORT_SYSTEM_GUI = 1
		else:
			self.teleportsystem.Close()
			constInfo.TELEPORT_SYSTEM_GUI = 0
			
	def OpenMentaLSkyGui(self):
		if constInfo.SKYBOX_GUI == 0:
			self.skyboxsystem.OpenWindow()
			self.skyboxsystem.SetTop()
			constInfo.SKYBOX_GUI = 1
		else:
			self.skyboxsystem.Close()
			constInfo.SKYBOX_GUI = 0
			
	# Ashens PickUP
	def	EnablePickUpItem(self):
		constInfo.need_open_pickup_filter=1

	def IsPickUpItem(self):
		return self.status_autopickup

	# Ashens PickEND
	
	if app.ENABLE_DRAGON_SOUL_SYSTEM:
		def OpenDSGui(self):
			self.interface.ToggleDragonSoulWindowWithNoInfo()

	def __GuildWar_OpenRank(self):
		if constInfo.canShowRankingGuild == 0:
			self.rankwindow.Show()
			constInfo.canShowRankingGuild = 1
		else:
			self.rankwindow.Hide()
			constInfo.canShowRankingGuild = 0

	def SaveScreen(self):
		print "save screen"

		# SCREENSHOT_CWDSAVE
		if SCREENSHOT_CWDSAVE:
			if not os.path.exists(os.getcwd()+os.sep+"screenshot"):
				os.mkdir(os.getcwd()+os.sep+"screenshot")

			(succeeded, name) = grp.SaveScreenShotToPath(os.getcwd()+os.sep+"screenshot"+os.sep)
		elif SCREENSHOT_DIR:
			(succeeded, name) = grp.SaveScreenShot(SCREENSHOT_DIR)
		else:
			(succeeded, name) = grp.SaveScreenShot()
		# END_OF_SCREENSHOT_CWDSAVE

		if succeeded:
			pass
			"""
			chat.AppendChat(chat.CHAT_TYPE_INFO, name + localeInfo.SCREENSHOT_SAVE1)
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SCREENSHOT_SAVE2)
			"""
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SCREENSHOT_SAVE_FAILURE)

	def MinimiereBonus(self):
		if self.INVENTAR_BONUS_PAGE == False:
			#####Ursprunglicher Inventar
			self.GetChild("board").SetSize(175, 543)
			self.GetChild("TitleBar").SetWidth(161)
			self.GetChild("TitleName").SetPosition(-8, 3)
			#self.GetChild("MinimierenButton").SetPosition(161 - 30, 10)
			self.SetSize(175 + 37, 543)
			#self.SetPosition(wndMgr.GetScreenWidth() - 176, wndMgr.GetScreenHeight() - 37 - 565)
			self.GetChild("Money_Slot").SetPosition(8, 28)
			#Tabelle
			self.GetChild("Defensiv").Hide()
			self.INVENTAR_BONUS_PAGE = True
		else:
			#####Bearbeitete Inventar
			self.GetChild("board").SetSize(176 + self.SPACE_BONUS_INVENTORY, 543)
			self.GetChild("TitleBar").SetWidth(161 + self.SPACE_BONUS_INVENTORY)
			self.GetChild("TitleName").SetPosition(-4, 3)
			#self.GetChild("MinimierenButton").SetPosition(161 + self.SPACE_BONUS_INVENTORY - 30, 10)
			self.SetSize(176 + self.SPACE_BONUS_INVENTORY + 37, 543)
			#self.SetPosition(wndMgr.GetScreenWidth() - 176 - 130, wndMgr.GetScreenHeight() - 37 - 565)
			self.GetChild("Money_Slot").SetPosition(-55, 28)
			#Tabelle
			self.GetChild("Defensiv").Show()
			self.INVENTAR_BONUS_PAGE = False

		self.MinimierenInfoTable(self.INVENTAR_BONUS_PAGE)
		if self.wndBelt:
			self.wndBelt.AdjustPositionAndSize()
		if app.ENABLE_BIOLOG_SYSTEM:
			if self.wndCollect:
				self.wndCollect.AdjustPositionAndSize()
		#if self.wndSidebar:
		#	self.wndSidebar.AdjustPositionAndSize()
			
		#self.AlignTrashBin()
		
			
	def ReferencePages(self, token):
		GetObject = self.GetChild
		
		ar_ListObjects = [
			GetObject("Defensiv"),GetObject("Schwert"),GetObject("Schwert_info"),GetObject("2Hand"),GetObject("2Hand_info"),GetObject("Dolch"),GetObject("Dolch_info"),GetObject("Pfeilwiderstand"),GetObject("Pfeilwiderstand_info"),GetObject("Glocke"),GetObject("Glocke_info"),GetObject("Faecher"),GetObject("Faecher_info"),GetObject("Magiewiederstand"),GetObject("Magiewiederstand_info"),GetObject("Giftwiederstand"),GetObject("Giftwiederstand_info"),GetObject("Krieger"),GetObject("Krieger_info"),GetObject("Ninja"),GetObject("Ninja_info"),GetObject("Sura"),GetObject("Sura_info"),GetObject("Schamane"),GetObject("Schamane_info"),GetObject("Offensive"),GetObject("Krit"),GetObject("Krit_info"),GetObject("DB"),GetObject("DB_info"),GetObject("DSS"),GetObject("DSS_info"),GetObject("FKS"),GetObject("FKS_info"),GetObject("Halbmenschen"),GetObject("Halbmenschen_info"),GetObject("Untote"),GetObject("Untote_info"),GetObject("Teufel"),GetObject("Teufel_info"),GetObject("KriegerO"),GetObject("KriegerO_info"),GetObject("NinjaO"),GetObject("NinjaO_info"),GetObject("SuraO"),GetObject("SuraO_info"),GetObject("SchamaneO"),GetObject("SchamaneO_info")
		]
		for it in ar_ListObjects:
			if token == 0:
				it.Hide()
			else:
				it.Show()

	def MinimierenInfoTable(self, arg):
		if arg == True:
			self.ReferencePages(0)
		else:
			self.ReferencePages(1)
	
	def ReloadBonus(self):
		ar_ListBonus = [ 69, 70, 71, 74, 72, 73, 77, 81, 59, 60, 61, 62, 40, 41, 122, 121, 43, 47, 48, 54, 55, 56, 57 ]

		for it in range(1, len(ar_ListBonus) + 1):
			self.GetChild("bonus_%d" % it).SetText(str(player.GetStatus(ar_ListBonus[it - 1])))

	def Destroy(self):
		self.ClearDictionary()
		if self.wndSystem:
			self.wndSystem.Destroy()
			self.wndSystem = None

		for i in xrange(self.GetSlotCount()):
			if self.elemets_world["hide_button_%d"%i].IsShow():
				self.elemets_world["hide_button_%d"%i].Hide()

		self.dlgPickMoney.Destroy()
		self.dlgPickMoney = 0

		self.refineDialog.Destroy()
		self.refineDialog = 0

		self.attachMetinDialog.Destroy()
		self.attachMetinDialog = 0

		self.tooltipItem = None
		self.wndItem = 0
		self.wndEquip = 0
		self.dlgPickMoney = 0
		self.wndMoney = 0
		self.wndMoneySlot = 0

		

		if app.ENABLE_CHEQUE_SYSTEM:
			self.wndCheque = 0
			self.wndChequeSlot = 0
			self.wndChequeIcon = 0
		self.questionDialog = None
		if app.ENABLE_BIOLOG_SYSTEM:
			wndCollect = None
			self.mallButton = None
		if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
			self.InventoryMenuButton = None
		self.DSSButton = None
		self.interface = None
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.bindWnds = []
		#if app.ENABLE_EXTEND_INVEN_SYSTEM:
		#	self.EX_INVEN_COVER_IMG_CLOSE = None
		#	self.EX_INVEN_COVER_IMG_OPEN = None

		self.MantelloButton = None
		#self.ButonMinimize = None

		#if self.wndCostume:
		#	self.wndCostume.Destroy()
		#	self.wndCostume = 0

		if self.wndRune:
			self.wndRune.Destroy()
			self.wndRune = 0

		if self.wndSoulStone:
			self.wndSoulStone.Destroy()
			self.wndSoulStone = None

		if app.ENABLE_BIOLOG_SYSTEM:
			if self.wndCollect:
				self.isOpenedCollectWindowWhenClosingInventory = self.wndCollect.IsOpeningInventory()
				print "Is opening Biolog Inventory", self.isOpenedCollectWindowWhenClosingInventory
				self.wndCollect.Close()	

		if self.wndBelt:
			self.wndBelt.Destroy()
			self.wndBelt = None
			
		if app.ENABLE_BIOLOG_SYSTEM:
			if self.wndCollect:
				self.wndCollect.Destroy()
				self.wndCollect = None
			
		#if self.wndSidebar:
		#	self.wndSidebar.Destroy()
		#	self.wndSidebar = None

		self.inventoryTab = []
		self.equipmentTab = []
		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyBar = None		
		if app.__ENABLE_TRASH_BIN__:
			self.trashBinTargetSlot  = 0
			self.trashBinTargetIndex = 0
			self.trashBinTargetCount = 0
			
			del self.trashBin
			del self.hideTrashBinBtn
			del self.showTrashBinBtn

	def Hide(self):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			self.OnCloseQuestionDialog()
			return
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		#if self.wndCostume:
		#	self.isOpenedCostumeWindowWhenClosingInventory = self.wndCostume.IsShow()			# 인벤토리 창이 닫힐 때 코스츔이 열려 있었는가?
		#	self.wndCostume.Close()

		if app.ENABLE_BIOLOG_SYSTEM:
			if self.wndCollect:
				self.isOpenedCollectWindowWhenClosingInventory = self.wndCollect.IsOpeningInventory()
				print "Is opening Biolog Inventory", self.isOpenedCollectWindowWhenClosingInventory
				self.wndCollect.Close()	
				
		if self.wndBelt:
			self.isOpenedBeltWindowWhenClosingInventory = self.wndBelt.IsOpeningInventory()		# 인벤토리 창이 닫힐 때 벨트 인벤토리도 열려 있었는가?
			print "Is Opening Belt Inventory ", self.isOpenedBeltWindowWhenClosingInventory
			self.wndBelt.Close()

		if self.wndSystem:
			self.isOpenedSystemWindowWhenClosingInventory = self.wndSystem.IsOpeningInventory()
			self.wndSystem.Close()

		#if self.wndSidebar:
		#	self.isOpenedSideBarWindowWhenClosingInventory = self.wndSidebar.IsOpeningInventory()
		#	self.wndSidebar.Close()

		if self.dlgPickMoney:
			self.dlgPickMoney.Close()
			
		if self.wndSoulStone:
			self.wndSoulStone.Close()

		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyBar:
				self.wndExpandedMoneyBar.Close()
		wndMgr.Hide(self.hWnd)
		
		if app.__ENABLE_TRASH_BIN__:
			try:
				self.trashBin.Hide()
				self.hideTrashBinBtn.Hide()
				self.showTrashBinBtn.Hide()
			except:
				pass


	def Close(self):
		self.Hide()		
		if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
			constInfo.IsInventoryOpened = False
			
		self.teleportsystem.Close()
		self.skyboxsystem.Close()
		
	if app.ENABLE_SORT_INVEN:
		def ClickYenileButton(self):
			if app.IsPressed(app.DIK_LALT):
				net.SortInven(2)
			elif app.IsPressed(app.DIK_LCONTROL):
				net.SortInven(3)
			else:
				net.SortInven(1)		
			
	if app.ENABLE_HIGHLIGHT_SYSTEM:
		def HighlightSlot(self, slot):
			if not slot in self.listHighlightedSlot:
				self.listHighlightedSlot.append(slot)
				
		def __RefreshHighlights(self):
			for i in xrange(player.INVENTORY_PAGE_SIZE*4):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
				if slotNumber in self.liHighlightedItems:
					self.wndItem.ActivateSlot(i)
	#if app.ENABLE_EXTEND_INVEN_SYSTEM:
	#	def UpdateInven(self):
	#		page = self.inventoryPageIndex
	#		for i in xrange(9):
	#			inv_plus = player.GetEnvanter() + i
	#			inv_pluss = player.GetEnvanter() - i
	#			if page == 2:
	#				if player.GetEnvanter() > 8:
	#					self.EX_INVEN_COVER_IMG_OPEN[i].Hide()
	#					self.EX_INVEN_COVER_IMG_CLOSE[i].Hide()
	#				else:
	#					self.EX_INVEN_COVER_IMG_OPEN[player.GetEnvanter()].Show()
	#					self.EX_INVEN_COVER_IMG_CLOSE[player.GetEnvanter()].Hide()
	#					if inv_pluss >= 0:
	#						self.EX_INVEN_COVER_IMG_OPEN[inv_pluss].Hide()
	#						self.EX_INVEN_COVER_IMG_CLOSE[inv_pluss].Hide()
	#					if inv_plus < 9:
	#						self.EX_INVEN_COVER_IMG_CLOSE[inv_plus].Show()
	#						self.EX_INVEN_COVER_IMG_OPEN[inv_plus].Hide()	
	#			elif page == 3:
	#				if player.GetEnvanter() < 9:	
	#					self.EX_INVEN_COVER_IMG_OPEN[i].Hide()
	#					self.EX_INVEN_COVER_IMG_CLOSE[i].Show()
	#				elif player.GetEnvanter() > 17:
	#					self.EX_INVEN_COVER_IMG_OPEN[i].Hide()
	#					self.EX_INVEN_COVER_IMG_CLOSE[i].Hide()
	#				else:
	#					self.EX_INVEN_COVER_IMG_OPEN[player.GetEnvanter()-9].Show()
	#					self.EX_INVEN_COVER_IMG_CLOSE[player.GetEnvanter()-9].Hide()
	#					if inv_pluss >= 0:
	#						self.EX_INVEN_COVER_IMG_OPEN[inv_pluss-9].Hide()
	#					if inv_plus < 18:
	#						self.EX_INVEN_COVER_IMG_CLOSE[inv_plus-9].Show()
	#			else:
	#				self.EX_INVEN_COVER_IMG_OPEN[i].Hide()
	#				self.EX_INVEN_COVER_IMG_CLOSE[i].Hide()
	#				
	#	def genislet(self):
	#		if uiPrivateShopBuilder.IsBuildingPrivateShop():
	#			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ENVANTER_UYARI)
	#			return
	#		net.Envanter_genislet()
	#		self.OnCloseQuestionDialog()
	#		
	#	def en_ac(self):
	#		envanter = None
	#		if player.GetEnvanter() > 17:
	#			self.wndPopupDialog = uiCommon.PopupDialog()
	#			self.wndPopupDialog.SetText(localeInfo.ENVANTER_ZATEN_GENIS_3)
	#			self.wndPopupDialog.Open()
	#		elif player.GetEnvanter() < 4:
	#			envanter = 2
	#		elif player.GetEnvanter() > 3 and player.GetEnvanter() < 6:
	#			envanter = 3
	#		elif player.GetEnvanter() > 5 and player.GetEnvanter() < 9:
	#			envanter = 4
	#		elif player.GetEnvanter() > 8 and player.GetEnvanter() < 12:
	#			envanter = 5
	#		elif player.GetEnvanter() > 11 and player.GetEnvanter() < 15:
	#			envanter = 6
	#		elif player.GetEnvanter() > 14 and player.GetEnvanter() < 18:
	#			envanter = 7
	#		self.questionDialog = uiCommon.QuestionDialog()
	#		self.questionDialog.SetText(localeInfo.ENVANTER_GENIS_1 % envanter)
	#		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.genislet))
	#		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
	#		self.questionDialog.Open()
			
	if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
		def SetExpandedMoneyBar(self, wndBar):
			self.wndExpandedMoneyBar = wndBar
			if self.wndExpandedMoneyBar:
				self.wndMoneySlot = self.wndExpandedMoneyBar.GetMoneySlot()
				self.wndMoney = self.wndExpandedMoneyBar.GetMoney()
				self.wndChequeSlot = self.wndExpandedMoneyBar.GetChequeSlot()
				self.wndCheque = self.wndExpandedMoneyBar.GetCheque()	

	def SetInventoryPage(self, page):
		self.inventoryPageIndex = page
		self.inventoryTab[(page+1)%4].SetUp()
		self.inventoryTab[(page+2)%4].SetUp()
		self.inventoryTab[(page+3)%4].SetUp()
		#if app.ENABLE_EXTEND_INVEN_SYSTEM:
		#	self.UpdateInven()
		self.RefreshBagSlotWindow()

	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			if self.inventoryPageIndex < 3:
				self.SetInventoryPage(self.inventoryPageIndex + 1)
		else:
			if self.inventoryPageIndex > 0:
				self.SetInventoryPage(self.inventoryPageIndex - 1)

	def SetEquipmentPage(self, page):
		self.equipmentPageIndex = page
		self.equipmentTab[1-page].SetUp()
		self.RefreshEquipSlotWindow()

	def ClickMallButton(self):
		print "click_mall_button"
		net.SendChatPacket("/click_mall")
		
	def ClickLagerButton(self):
		if constInfo.DROP_GUI_CHECK == 1:
			chat.AppendChat(1, "First of all, choose one option about drop gui.")
		else:
			self.interface.ToggleInventoryMenuWindow()
		# eventt.QuestButtonClick(1)

	def OpenSoulStoneWindow(self, slotIndex):
		if not self.wndSoulStone:
			self.wndSoulStone = uiSoulStone.SoulStoneBoard()
		self.wndSoulStone.Open(slotIndex)

	def CheckSoulStoneSlot(self):
		if self.wndSoulStone and self.wndSoulStone.IsShow():
			self.wndSoulStone.RefreshSlot()

	# DSSButton
	def ClickDSSButton(self):
		print "click_dss_button"
		self.interface.ToggleDragonSoulWindow()
		
	#def ClickCostumeButton(self):
	#	print "Click Costume Button"
	#	if self.wndCostume:
	#		if self.wndCostume.IsShow():
	#			self.wndCostume.Hide()
	#		else:
	#			self.wndCostume.Show()
	#	else:
	#		self.wndCostume = CostumeWindow(self)
	#		self.wndCostume.Show()

	def ClickRuneButton(self):
		print "Click Rune Button"
		if self.wndRune:
			if self.wndRune.IsShow(): 
				self.wndRune.Hide()
			else:
				self.wndRune.Show()
		else:
			self.wndRune = RuneWindow(self)
			self.wndRune.Show()

	if app.ENABLE_OFFLINE_SHOP_SYSTEM:
		def ClickOfflineShopButton(self):
			net.SendChatPacket('/open_offlineshop')

	def OpenPickMoneyDialog(self):

		if mouseModule.mouseController.isAttached():

			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			if player.SLOT_TYPE_SAFEBOX == mouseModule.mouseController.GetAttachedType():

				if player.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

			mouseModule.mouseController.DeattachObject()

		else:
			curMoney = player.GetElk()

			if curMoney <= 0:
				return

			self.dlgPickMoney.SetTitleName(localeInfo.PICK_MONEY_TITLE)
			self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickMoney))
			if app.ENABLE_CHEQUE_SYSTEM:
				self.dlgPickMoney.Open(curMoney, player.GetCheque())
			else:
				self.dlgPickMoney.Open(curMoney)
			self.dlgPickMoney.SetMax(7) # 인벤토리 990000 제한 버그 수정

	def OnPickMoney(self, money, cheque = None):
		mouseModule.mouseController.AttachMoney(self, player.SLOT_TYPE_INVENTORY, money)


	if app.ENABLE_CHEQUE_SYSTEM:
		def __SetChequeSystemToolTip(self):
			self.toolTipChequeTitle = uiToolTip.ToolTip(20)
			self.toolTipChequeTitle.AutoAppendTextLine(localeInfo.CHEQUE_SYSTEM_UNIT_WON, uiToolTip.ToolTip.PRICE_INFO_COLOR)
			self.toolTipChequeTitle.AlignHorizonalCenter()
			self.toolTipMoneyTitle = uiToolTip.ToolTip(20)
			self.toolTipMoneyTitle.AutoAppendTextLine(localeInfo.CHEQUE_SYSTEM_UNIT_YANG, uiToolTip.ToolTip.PRICE_INFO_COLOR)
			self.toolTipMoneyTitle.AlignHorizonalCenter()

		def __ShowMoneyTitleToolTip(self):
			self.toolTipMoneyTitle.ShowToolTip()

		def __HideMoneyTitleToolTip(self):
			self.toolTipMoneyTitle.HideToolTip()

		def __ShowChequeTitleToolTip(self):
			self.toolTipChequeTitle.ShowToolTip()

		def __HideChequeTitleToolTip(self):
			self.toolTipChequeTitle.HideToolTip()

	def OnPickItem(self, count):
		itemSlotIndex = self.dlgPickMoney.itemGlobalSlotIndex
		selectedItemVNum = player.GetItemIndex(itemSlotIndex)
		mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, count)
		if app.ENABLE_REMEMBER_LAST_SPLIT:
			systemSetting.SetLastSplitData(count)

	def __InventoryLocalSlotPosToGlobalSlotPos(self, local):
		if player.IsEquipmentSlot(local) or player.IsCostumeSlot(local) or (app.ENABLE_NEW_EQUIPMENT_SYSTEM and player.IsBeltInventorySlot(local)):
			return local

		return self.inventoryPageIndex*player.INVENTORY_PAGE_SIZE + local

	def GetInventoryPageIndex(self):
		return self.inventoryPageIndex

	if app.WJ_ENABLE_TRADABLE_ICON:
		def RefreshMarkSlots(self, localIndex=None):
			if not self.interface:
				return

			onTopWnd = self.interface.GetOnTopWindow()
			if localIndex:
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(localIndex)
				if onTopWnd == player.ON_TOP_WND_NONE:
					self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_SHOP:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SELL):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_EXCHANGE:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_GIVE):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_PRIVATE_SHOP:
					if player.IsAntiFlagBySlot(slotNumber, item.ITEM_ANTIFLAG_MYSHOP):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_SAFEBOX:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SAFEBOX):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)
				elif app.BL_MAILBOX and onTopWnd == player.ON_TOP_WND_MAILBOX:
					if self.interface.MarkUnusableDSInvenSlotOnTopWnd(onTopWnd, slotNumber, player.INVENTORY):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)
				return

			for i in xrange(player.INVENTORY_PAGE_SIZE):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

				if onTopWnd == player.ON_TOP_WND_NONE:
					self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_SHOP:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SELL):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_EXCHANGE:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_GIVE):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_PRIVATE_SHOP:
					if player.IsAntiFlagBySlot(slotNumber, item.ITEM_ANTIFLAG_MYSHOP):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_SAFEBOX:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SAFEBOX):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)
				elif app.BL_MAILBOX and onTopWnd == player.ON_TOP_WND_MAILBOX:
					if self.interface.MarkUnusableDSInvenSlotOnTopWnd(onTopWnd, slotNumber, player.INVENTORY):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

	def RefreshBagSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndItem.SetItemSlot
		for i in xrange(player.INVENTORY_PAGE_SIZE):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

			itemCount = getItemCount(slotNumber)
			# itemCount == 0이면 소켓을 비운다.
			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0

			itemVnum = getItemVNum(slotNumber)
			setItemVNum(i, itemVnum, itemCount)
			self.wndItem.DeactivateSlot(i)
			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = player.GetItemTransmutation(slotNumber)
				if itemTransmutedVnum:
					self.wndItem.DisableCoverButton(i)
				else:
					self.wndItem.EnableCoverButton(i)
	
			if constInfo.ENABLE_AURA_SYSTEM:
				if self.interface.auraUpgrade and self.interface.auraUpgrade.IsShow():
					if slotNumber == self.interface.auraUpgrade.pos[0]:
						self.wndItem.ActivateSlot(i)
					if slotNumber == self.interface.auraUpgrade.pos[1]:
						self.wndItem.ActivateSlot(i)
				if self.interface.auraAbs and self.interface.auraAbs.IsShow():
					if slotNumber == self.interface.auraAbs.pos[0]:
						self.wndItem.ActivateSlot(i)
					if slotNumber == self.interface.auraAbs.pos[1]:
						self.wndItem.ActivateSlot(i)
	## 자동물약 (HP: #72723 ~ #72726, SP: #72727 ~ #72730) 특수처리 - 아이템인데도 슬롯에 활성화/비활성화 표시를 위한 작업임 - [hyo]
			if constInfo.IS_AUTO_POTION(itemVnum):
				# metinSocket - [0] : 활성화 여부, [1] : 사용한 양, [2] : 최대 용량
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]

				if app.WJ_ENABLE_TRADABLE_ICON:
					self.RefreshMarkSlots(i)
				
					if constInfo.IS_N_PET(itemVnum):
						isActivatedPet = 0!= metinSocket[1]
						if isActivatedPet:
							self.wndItem.ActivateSlot(i)
						else:
							self.wndItem.DeactivateSlot(i)
					else:
						isActivated = 0 != metinSocket[0]
				
						if isActivated:
							self.wndItem.ActivateSlot(i)
							potionType = 0;
							if constInfo.IS_AUTO_POTION_HP(itemVnum):
								potionType = player.AUTO_POTION_TYPE_HP
							elif constInfo.IS_AUTO_POTION_SP(itemVnum):
								potionType = player.AUTO_POTION_TYPE_SP

							usedAmount = int(metinSocket[1])
							totalAmount = int(metinSocket[2])
							player.SetAutoPotionInfo(potionType, isActivated, (totalAmount - usedAmount), totalAmount, self.__InventoryLocalSlotPosToGlobalSlotPos(i))
						else:
							self.wndItem.DeactivateSlot(i)

			elif app.ENABLE_HIGHLIGHT_SYSTEM:
				if slotNumber in self.listHighlightedSlot:
					self.wndItem.ActivateSlot(i)
			
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				slotNumberChecked = 0
				if not constInfo.IS_AUTO_POTION(itemVnum):
					if app.ENABLE_HIGHLIGHT_SYSTEM:
						if not slotNumber in self.listHighlightedSlot:
							self.wndItem.DeactivateSlot(i)
					else:
						self.wndItem.DeactivateSlot(i)
				
				for j in xrange(acce.WINDOW_MAX_MATERIALS):
					(isHere, iCell) = acce.GetAttachedItem(j)
					if isHere:
						if iCell == slotNumber:
							self.wndItem.ActivateSlot(i, (36.00 / 255.0), (222.00 / 255.0), (3.00 / 255.0), 1.0)
							if not slotNumber in self.listAttachedAcces:
								self.listAttachedAcces.append(slotNumber)
							
							slotNumberChecked = 1
					else:
						if slotNumber in self.listAttachedAcces and not slotNumberChecked:
							self.wndItem.DeactivateSlot(i)
							self.listAttachedAcces.remove(slotNumber)
			if app.ENABLE_CHANGELOOK_SYSTEM:
				slotClNumberChecked = 0
				for q in xrange(changelook.WINDOW_MAX_MATERIALS):
					(isHere, iCell) = changelook.GetAttachedItem(q)
					if isHere:
						if iCell == slotNumber:
							self.wndItem.ActivateSlot(i, (238.00 / 255.0), (11.00 / 255.0), (11.00 / 255.0), 1.0)
							if not slotNumber in self.listAttachedCl:
								self.listAttachedCl.append(slotNumber)
							
							slotClNumberChecked = 1
					else:
						if slotNumber in self.listAttachedCl and not slotClNumberChecked:
							self.wndItem.DeactivateSlot(i)
							self.listAttachedCl.remove(slotNumber)	

		self.wndItem.RefreshSlot()

		if self.wndBelt:
			self.wndBelt.RefreshSlot()

		if app.WJ_ENABLE_TRADABLE_ICON:
			map(lambda wnd:wnd.RefreshLockedSlot(), self.bindWnds)

	if app.WON_EXCHANGE:
		def IsDlgQuestionShow(self):
			if self.questionDialog and self.questionDialog.IsShow() or self.attachMetinDialog.IsShow():
				return True

			return False

		def ExternQuestionDialog_Close(self):
			if self.attachMetinDialog.IsShow():
				self.attachMetinDialog.Close()
			self.questionDialog.Close()
			self.srcItemPos = (0, 0)
			self.dstItemPos = (0, 0)


	def RefreshEquipSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndEquip.SetItemSlot
		for i in xrange(player.EQUIPMENT_PAGE_COUNT):
			slotNumber = player.EQUIPMENT_SLOT_START + i
			itemCount = getItemCount(slotNumber)
			if itemCount <= 1:
				itemCount = 0
			setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)
			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = player.GetItemTransmutation(slotNumber)
				if itemTransmutedVnum:
					self.wndEquip.DisableCoverButton(slotNumber)
				else:
					self.wndEquip.EnableCoverButton(slotNumber)
		
		if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
			for i in xrange(player.NEW_EQUIPMENT_SLOT_COUNT):
				slotNumber = player.NEW_EQUIPMENT_SLOT_START + i
				itemCount = getItemCount(slotNumber)
				if itemCount <= 1:
					itemCount = 0
				setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)
				if app.ENABLE_CHANGELOOK_SYSTEM:
					itemTransmutedVnum = player.GetItemTransmutation(slotNumber)
					if itemTransmutedVnum:
						self.wndEquip.DisableCoverButton(slotNumber)
					else:
						self.wndEquip.EnableCoverButton(slotNumber)

				print "ENABLE_NEW_EQUIPMENT_SYSTEM", slotNumber, itemCount, getItemVNum(slotNumber)

		self.wndEquip.SetItemSlot(1120, constInfo.PetVnum, 0)
		self.wndEquip.SetItemSlot(1121, constInfo.PetOfficialVnum, 0)

		self.wndEquip.SetItemSlot(item.NEW_EQUIPMENT_SLOT_START+8, getItemVNum(item.NEW_EQUIPMENT_SLOT_START+8), 0)
				
		for i in xrange(item.COSTUME_SLOT_COUNT+4):
			slotNumber = item.COSTUME_SLOT_START + i
			self.wndEquip.SetItemSlot(slotNumber, getItemVNum(slotNumber), 0)

			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = player.GetItemTransmutation(slotNumber)
				if itemTransmutedVnum:
					self.wndEquip.DisableCoverButton(slotNumber)
				else:
					self.wndEquip.EnableCoverButton(slotNumber)

		if app.ENABLE_WEAPON_COSTUME_SYSTEM:
			self.wndEquip.SetItemSlot(item.COSTUME_SLOT_WEAPON, getItemVNum(item.COSTUME_SLOT_WEAPON), 0)

		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			self.elemets_hide = self.get_costume_hide_list()
			self.ButtonsHideCostume()
			self.costume_hide_load()

		if app.GLOW_EFFECT:
			self.ref_talizmaneffect()
		self.wndEquip.RefreshSlot()
		self.RefreshCostumeSlot()

		if self.wndRune:
			self.wndRune.RefreshEquipSlotWindow()
	if app.GLOW_EFFECT:
		def ref_talizmaneffect(self):
			slot_index = [205, 209, 208, 207, 206, 210]
			function = [self.talizmaneffect1, self.talizmaneffect2, self.talizmaneffect3, self.talizmaneffect4, self.talizmaneffect5, self.talizmaneffect6]
			for x in xrange(6):
				if (player.GetItemIndex(slot_index[x]) > 0):
					function[x].AppendHighLightImage(0, *self.GLOW_EFFECT[x][1:])
					function[x].EnableHighLightImage(0)
				else:
					function[x].DisableHighLightImage(0)

		#if self.wndCostume:
		#	self.wndCostume.RefreshCostumeSlot()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def costume_hide_clear(self):
			self.elemets_hide = []

		def costume_hide_list(self,slot,index):
			self.elemets_hide.append([int(slot),int(index)])

		def costume_hide_load(self):
				self.costume_hide_load_c()

		def get_costume_hide_list(self):
			return self.elemets_hide

	def RefreshCostumeSlot(self):
		getItemVNum=player.GetItemIndex

		for i in xrange(item.COSTUME_SLOT_COUNT+4):
			slotNumber = item.COSTUME_SLOT_START + i
			self.wndEquip.SetItemSlot(slotNumber, getItemVNum(slotNumber), 0)

			if app.ENABLE_CHANGELOOK_SYSTEM:
				itemTransmutedVnum = player.GetItemTransmutation(slotNumber)
				if itemTransmutedVnum:
					self.wndEquip.DisableCoverButton(slotNumber)
				else:
					self.wndEquip.EnableCoverButton(slotNumber)

		if app.ENABLE_WEAPON_COSTUME_SYSTEM:
			self.wndEquip.SetItemSlot(item.COSTUME_SLOT_WEAPON, getItemVNum(item.COSTUME_SLOT_WEAPON), 0)

		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			self.elemets_hide = self.get_costume_hide_list()
			self.ButtonsHideCostume()
			self.costume_hide_load_c()

		self.wndEquip.RefreshSlot()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def ButtonsHideCostume(self):
			self.elemets_world["position"] = [
			[95+3+15,65],#body_costume
			[95+3+15,24],#hair_costume
			[62,48],#weapon_costume
			[164, 11]#sash

			]

			for i in xrange(self.GetSlotCount()):
				self.elemets_world["hide_button_%d"%i] = ui.Button()
				self.elemets_world["hide_button_%d"%i].SetParent(self)
				self.elemets_world["hide_button_%d"%i].SetPosition(self.elemets_world["position"][i][0]+12,self.elemets_world["position"][i][1]+37)
				self.elemets_world["hide_button_%d"%i].SetUpVisual("d:/ymir work/ui/hidecostume/button_show_0.tga")
				self.elemets_world["hide_button_%d"%i].SetOverVisual("d:/ymir work/ui/hidecostume/button_show_1.tga")
				self.elemets_world["hide_button_%d"%i].SetDownVisual("d:/ymir work/ui/hidecostume/button_show_0.tga")
				self.elemets_world["hide_button_%d"%i].SetEvent(self.FuncHide,i)
				self.elemets_world["hide_button_%d"%i].Hide()

		def FuncHide(self,index):
			import chat
			net.SendChatPacket("/costume_hide %d" %index)

		def costume_hide_load_c(self):
			if constInfo.hide_buttons == 0:
				for i in xrange(self.GetSlotCount()):
					if len(self.elemets_hide) > 0:
						self.elemets_world["hide_button_%d"%self.elemets_hide[i][0]].SetUpVisual("d:/ymir work/ui/hidecostume/button_%s_0.tga"%self.ButtonInfoHide(self.elemets_hide[i][1]))
						self.elemets_world["hide_button_%d"%self.elemets_hide[i][0]].SetOverVisual("d:/ymir work/ui/hidecostume/button_%s_1.tga"%self.ButtonInfoHide(self.elemets_hide[i][1]))
						self.elemets_world["hide_button_%d"%self.elemets_hide[i][0]].SetDownVisual("d:/ymir work/ui/hidecostume/button_%s_0.tga"%self.ButtonInfoHide(self.elemets_hide[i][1]))
					self.elemets_world["hide_button_%d"%i].Show()

		def ButtonInfoHide(self,index):
			if index == 0:
				return "show"
			return "hide"

		def GetSlotCount(self):
			slot_total = 2

			if app.ENABLE_HIDE_COSTUME_SYSTEM_ACCE:
				slot_total += 1
			if app.ENABLE_HIDE_COSTUME_SYSTEM_WEAPON_COSTUME:
				slot_total += 1

			return slot_total

	def RefreshItemSlot(self):
		self.RefreshBagSlotWindow()
		self.RefreshEquipSlotWindow()
		self.RefreshCostumeSlot()
		self.CheckSoulStoneSlot()

		
	if app.__ENABLE_TRASH_BIN__:
		def OnMouseLeftButtonUpTrashBinCheck(self):
			if not self.trashBin.IsShow() or not self.trashBin.IsIn() or not mouseModule.mouseController.isAttached():
				return False
			
			attachedSlotPos   = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedSlotType  = mouseModule.mouseController.GetAttachedType()
			attachedCount	  = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
			
			if attachedSlotType != player.SLOT_TYPE_INVENTORY or attachedSlotPos < 0:
				return False
			
			if item.IsUnbreakableItem(attachedItemIndex):
				chat.AppendChat(chat.CHAT_TYPE_INFO , localeInfo.CANNOT_DESTROY_ITEM)
				return False
			
			itemRewardCount = item.GetTrashBinRewardCount(attachedItemIndex)
			itemRewardCount*= attachedCount
			
			
			item.SelectItem(attachedItemIndex)
			itemName = item.GetItemName()
			
			self.questionDialog = uiCommon.QuestionDialog()
			
			if itemRewardCount > 0:
				self.questionDialog.SetText(localeInfo.DO_YOU_DESTROY_ITEM_WITH_REWARD%(itemName, attachedCount,itemRewardCount))
			
			else:
				self.questionDialog.SetText(localeInfo.DO_YOU_DESTROY_ITEM%(itemName, attachedCount))
			
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.PutItemInTrashBin))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			
			self.trashBinTargetSlot		= attachedSlotPos
			self.trashBinTargetIndex	= attachedItemIndex
			self.trashBinTargetCount	= attachedCount
			
			mouseModule.mouseController.DeattachObject()
			return True
		
		def PutItemInTrashBin(self):
			net.SendChatPacket("/trash_bin %d %d %d"%(self.trashBinTargetSlot,self.trashBinTargetIndex,self.trashBinTargetCount))
			self.OnCloseQuestionDialog()
			
		def AlignTrashBin(self):
			x_inv , y_inv = self.GetGlobalPosition()
			
			if self.trashBin.IsShow():
				self.trashBin.SetPosition(x_inv - self.trashBin.GetWidth() +2 , y_inv + 496)
				self.hideTrashBinBtn.SetPosition(x_inv - (self.trashBin.GetWidth() + self.hideTrashBinBtn.GetWidth() +2), y_inv + 496)
				
			else:
				self.showTrashBinBtn.SetPosition(x_inv - self.showTrashBinBtn.GetWidth() +2 , y_inv + 496)
		
		
		def OnClickShowTrashBinBtn(self):
			self.showTrashBinBtn.Hide()
			self.hideTrashBinBtn.Show()
			self.trashBin.Show()
			
			self.AlignTrashBin()
			
		
		def OnClickHideTrashBinBtn(self):
			self.showTrashBinBtn.Show()
			self.hideTrashBinBtn.Hide()
			self.trashBin.Hide()
			
			self.AlignTrashBin()

	def RefreshStatus(self):
		money = player.GetElk()
		cheque = player.GetCheque()
		self.wndMoney.SetText(localeInfo.NumberToMoney(money))
		if app.ENABLE_CHEQUE_SYSTEM:
			self.wndCheque.SetText(localeInfo.NumberToCheque(cheque))	

	def RefreshSkill(self):
		if self.wndSoulStone and self.wndSoulStone.IsShow():
			self.wndSoulStone.RefreshSkill()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def SellItem(self):
		if self.sellingSlotitemIndex == player.GetItemIndex(self.sellingSlotNumber):
			if self.sellingSlotitemCount == player.GetItemCount(self.sellingSlotNumber):
				## 용혼석도 팔리게 하는 기능 추가하면서 인자 type 추가
				net.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, player.INVENTORY)
				snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnDetachMetinFromItem(self):
		if None == self.questionDialog:
			return

		#net.SendItemUseToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
		self.__SendUseItemToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return

		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	## Slot Event
	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos)

		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				itemCount = player.GetItemCount(attachedSlotPos)
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				self.__SendMoveItemPacket(attachedSlotPos, selectedSlotPos, attachedCount)
				
				if item.IsRefineScroll(attachedItemIndex):
					self.wndItem.SetUseMode(False)
					
			elif app.ENABLE_SWITCHBOT and player.SLOT_TYPE_SWITCHBOT == attachedSlotType:
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				net.SendItemMovePacket(player.SWITCHBOT, attachedSlotPos, player.INVENTORY, selectedSlotPos, attachedCount)

			elif player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				mouseModule.mouseController.RunCallBack("INVENTORY")

			elif player.SLOT_TYPE_CHANGE_EQUIP == attachedSlotType and app.FAST_EQUIP_WORLDARD:
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				net.SendItemMovePacket(player.CHANGE_EQUIP, attachedSlotPos, player.INVENTORY, selectedSlotPos, attachedCount)

			# BEGIN_OFFLINE_SHOP
			elif player.SLOT_TYPE_OFFLINE_SHOP == attachedSlotType:
				mouseModule.mouseController.RunCallBack('INVENTORY')
			# END_OF_OFFLINE_SHOP

			elif player.SLOT_TYPE_SHOP == attachedSlotType:
				net.SendShopBuyPacket(attachedSlotPos)

			elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:

				if player.ITEM_MONEY == attachedItemIndex:
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

				else:
					net.SendSafeboxCheckoutPacket(attachedSlotPos, selectedSlotPos)
	
			elif player.SLOT_TYPE_MALL == attachedSlotType:
				net.SendMallCheckoutPacket(attachedSlotPos, selectedSlotPos)
			
			elif app.ENABLE_SPECIAL_STORAGE_SYSTEM and attachedSlotType >= player.SLOT_TYPE_SKILLBOOK_INVENTORY and attachedSlotType <= player.SLOT_TYPE_GENERAL_INVENTORY:
				net.SendItemMovePacket(player.SlotTypeToInvenType(attachedSlotType), attachedSlotPos, player.INVENTORY, selectedSlotPos, attachedItemCount)

			mouseModule.mouseController.DeattachObject()

	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex)

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()

			if player.SLOT_TYPE_INVENTORY == attachedSlotType or attachedSlotType == player.SLOT_TYPE_SKILLBOOK_INVENTORY or attachedSlotType == player.SLOT_TYPE_GENERAL_INVENTORY or attachedSlotType == player.SLOT_TYPE_GHOSTSTONE_INVENTORY or attachedSlotType == player.SLOT_TYPE_UPPITEM_INVENTORY:
				self.__DropSrcItemToDestItemInInventory(attachedItemVID, attachedSlotPos, itemSlotIndex, attachedSlotType, player.SLOT_TYPE_INVENTORY)

			mouseModule.mouseController.DeattachObject()

		else:

			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)

			elif app.BUY == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)

			elif app.IsPressed(app.DIK_LALT):
				link = player.GetItemLink(itemSlotIndex)
				ime.PasteString(link)

			elif app.IsPressed(app.DIK_LSHIFT):
				itemCount = player.GetItemCount(itemSlotIndex)

				if itemCount > 1:
					self.dlgPickMoney.SetTitleName(localeInfo.PICK_ITEM_TITLE)
					self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
					if app.ENABLE_REMEMBER_LAST_SPLIT:
						if itemCount >= systemSetting.GetLastSplitData():
							self.dlgPickMoney.Open(itemCount, systemSetting.GetLastSplitData())
						else:
							self.dlgPickMoney.Open(itemCount)
					else:
						self.dlgPickMoney.Open(itemCount)
					self.dlgPickMoney.itemGlobalSlotIndex = itemSlotIndex
				#else:
					#selectedItemVNum = player.GetItemIndex(itemSlotIndex)
					#mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum)

			elif app.IsPressed(app.DIK_LCONTROL):
				itemIndex = player.GetItemIndex(itemSlotIndex)
				if constInfo.ENABLE_SHOW_CHEST_DROP:
					item.SelectItem(itemIndex)
					# this is only chesthbox!
					if item.GetItemType() == item.ITEM_TYPE_GIFTBOX:
						net.SendChestDropInfo(0,itemIndex)
						return
				if True == item.CanAddToQuickSlotItem(itemIndex):
					player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_INVENTORY, itemSlotIndex)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.QUICKSLOT_REGISTER_DISABLE_ITEM)

			else:
				selectedItemVNum = player.GetItemIndex(itemSlotIndex)
				itemCount = player.GetItemCount(itemSlotIndex)
				mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)

				if self.__IsUsableItemToItem(selectedItemVNum, itemSlotIndex):
					self.wndItem.SetUseMode(True)
				else:
					self.wndItem.SetUseMode(False)

				snd.PlaySound("sound/ui/pick.wav")

	def UseTransportBox(self):
		self.__SendUseItemToItemPacket(self.questionDialog.src, self.questionDialog.dst)
		self.OnCloseQuestionDialog()

	#if app.CLEAR_BONUS_AURA:
	def ClearAuraBonuses(self):
		net.SendChatPacket("/do_clear_bonus_aura %d" % (self.questionDialog.dst))
		self.OnCloseQuestionDialog()

	def UseProtein(self):
		self.__SendUseItemToItemPacket(self.questionDialog.src, self.questionDialog.dst)
		self.OnCloseQuestionDialog()

	def __DropSrcItemToDestItemInInventory(self, srcItemVID, srcItemSlotPos, dstItemSlotPos, srcItemSlotWin = player.SLOT_TYPE_INVENTORY, dstItemSlotWin = player.SLOT_TYPE_INVENTORY):
		if srcItemSlotPos == dstItemSlotPos:
			return
 
		if app.ENABLE_COSTUME_SWITCHBOT:
			#import constInfo   || Se non hai importato in headers constInfo togli questo simbolo "#"
			if srcItemSlotWin == player.SLOT_TYPE_INVENTORY:
				if constInfo.IS_SWITCHER(player.GetItemIndex(srcItemSlotPos)) and player.GetItemIndex(dstItemSlotPos) > 9:
					self.OpenSwitch(player.GetItemIndex(dstItemSlotPos), dstItemSlotPos, player.GetItemIndex(srcItemSlotPos), player.GetItemCount(srcItemSlotPos), srcItemSlotPos)
					return

		#if app.CLEAR_BONUS_AURA:
		if srcItemVID == 49007:
			item.SelectItem(player.GetItemIndex(dstItemSlotPos))
			if item.GetItemType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_AURA:
				self.questionDialog = uiCommon.QuestionDialog()
				self.questionDialog.SetText("Vuoi pulire i tuoi bonus?")
				self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.ClearAuraBonuses))
				self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
				self.questionDialog.Open()
				self.questionDialog.src = srcItemSlotPos
				self.questionDialog.dst = dstItemSlotPos
			else:
				if srcItemVID != player.GetItemIndex(dstItemSlotPos):
					chat.AppendChat(1, "< Aura > Puoi usare quest'item solo sull'aura!")

		if srcItemVID >= 55701 and srcItemVID <= 55710 and player.GetItemIndex(dstItemSlotPos) == 55002:
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText("Vuoi aggiungere il pet al trasportino?")
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.UseTransportBox))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.src = srcItemSlotPos
			self.questionDialog.dst = dstItemSlotPos
			
		if srcItemVID == 55001 and player.GetItemIndex(dstItemSlotPos) >= 55701 and player.GetItemIndex(dstItemSlotPos) <= 55710:
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText("Vuoi dare da mangiare al tuo pet?")
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.UseProtein))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.src = srcItemSlotPos
			self.questionDialog.dst = dstItemSlotPos

		if srcItemVID == 58500 or srcItemVID == 58501 or srcItemVID == 58502:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos, srcItemSlotWin, dstItemSlotWin)
		# cyh itemseal 2013 11 08
		if app.ENABLE_SOULBIND_SYSTEM and item.IsSealScroll(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos, srcItemSlotWin, dstItemSlotWin)
		elif item.IsRefineScroll(srcItemVID):
			self.RefineItem(srcItemSlotPos, dstItemSlotPos)
			self.wndItem.SetUseMode(False)

		## Fix Stone
		elif item.IsMetin(srcItemVID):
			ItemVNumDest = player.GetItemIndex(dstItemSlotPos)
			item.SelectItem(ItemVNumDest)
			if not (item.ITEM_TYPE_METIN == item.GetItemType() and item.METIN_NORMAL == item.GetItemSubType()):
				self.AttachMetinToItem(srcItemSlotPos, dstItemSlotPos)
			else:
				if not player.IsEquipmentSlot(dstItemSlotPos):
					self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
		
		#End Fix Stone

		elif item.IsDetachScroll(srcItemVID):
			self.DetachMetinFromItem(srcItemSlotPos, dstItemSlotPos)

		elif item.IsKey(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos, srcItemSlotWin, dstItemSlotWin)

		elif (player.GetItemFlags(srcItemSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos, srcItemSlotWin, dstItemSlotWin)

		elif item.GetUseType(srcItemVID) in self.USE_TYPE_TUPLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos, srcItemSlotWin, dstItemSlotWin)

		else:
			#snd.PlaySound("sound/ui/drop.wav")

			## 이동시킨 곳이 장착 슬롯일 경우 아이템을 사용해서 장착 시킨다 - [levites]
			if player.IsEquipmentSlot(dstItemSlotPos):

				## 들고 있는 아이템이 장비일때만
				if item.IsEquipmentVID(srcItemVID):
					self.__UseItem(srcItemSlotPos)

			else:
				self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
				#net.SendItemMovePacket(srcItemSlotPos, dstItemSlotPos, 0)

	def __SellItem(self, itemSlotPos):
		if not player.IsEquipmentSlot(itemSlotPos):
			self.sellingSlotNumber = itemSlotPos
			itemIndex = player.GetItemIndex(itemSlotPos)
			itemCount = player.GetItemCount(itemSlotPos)


			self.sellingSlotitemIndex = itemIndex
			self.sellingSlotitemCount = itemCount

			item.SelectItem(itemIndex)
			## 안티 플레그 검사 빠져서 추가
			## 20140220
			if item.IsAntiFlag(item.ANTIFLAG_SELL):
				popup = uiCommon.PopupDialog()
				popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
				popup.SetAcceptEvent(self.__OnClosePopupDialog)
				popup.Open()
				self.popup = popup
				return

			itemPrice = item.GetISellItemPrice()

			if item.Is1GoldItem():
				itemPrice = itemCount / itemPrice / 5
			else:
				itemPrice = itemPrice * itemCount / 5

			item.GetItemName(itemIndex)
			itemName = item.GetItemName()

			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, itemCount, itemPrice))
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.count = itemCount

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def __OnClosePopupDialog(self):
		self.pop = None

	def RefineItem(self, scrollSlotPos, targetSlotPos):

		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		if player.REFINE_OK != player.CanRefine(scrollIndex, targetSlotPos):
			return

		if app.ENABLE_REFINE_RENEWAL:
			constInfo.AUTO_REFINE_TYPE = 1
			constInfo.AUTO_REFINE_DATA["ITEM"][0] = scrollSlotPos
			constInfo.AUTO_REFINE_DATA["ITEM"][1] = targetSlotPos

		###########################################################
		self.__SendUseItemToItemPacket(scrollSlotPos, targetSlotPos)
		#net.SendItemUseToItemPacket(scrollSlotPos, targetSlotPos)
		return
		###########################################################

		###########################################################
		#net.SendRequestRefineInfoPacket(targetSlotPos)
		#return
		###########################################################

		result = player.CanRefine(scrollIndex, targetSlotPos)

		if player.REFINE_ALREADY_MAX_SOCKET_COUNT == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_MORE_SOCKET)

		elif player.REFINE_NEED_MORE_GOOD_SCROLL == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NEED_BETTER_SCROLL)

		elif player.REFINE_CANT_MAKE_SOCKET_ITEM == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_SOCKET_DISABLE_ITEM)

		elif player.REFINE_NOT_NEXT_GRADE_ITEM == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_UPGRADE_DISABLE_ITEM)

		elif player.REFINE_CANT_REFINE_METIN_TO_EQUIPMENT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)

		if player.REFINE_OK != result:
			return

		self.refineDialog.Open(scrollSlotPos, targetSlotPos)

	def DetachMetinFromItem(self, scrollSlotPos, targetSlotPos):
		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if not player.CanDetach(scrollIndex, targetSlotPos):
				item.SelectItem(scrollIndex)
				if item.GetValue(0) == acce.CLEAN_ATTR_VALUE0:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ACCE_FAILURE_CLEAN)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
				
				return
		if app.ENABLE_CHANGELOOK_SYSTEM:
			if not player.CanDetach(scrollIndex, targetSlotPos):
				item.SelectItem(scrollIndex)
				if item.GetValue(0) == changelook.CLEAN_ATTR_VALUE0:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_FAILURE_CLEAN)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
				
				return
		else:
			if not player.CanDetach(scrollIndex, targetSlotPos):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
				return
		
		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText(localeInfo.REFINE_DO_YOU_SEPARATE_METIN)
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			item.SelectItem(targetIndex)
			if item.GetItemType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_ACCE:
				item.SelectItem(scrollIndex)
				if item.GetValue(0) == acce.CLEAN_ATTR_VALUE0:
					self.questionDialog.SetText(localeInfo.ACCE_DO_YOU_CLEAN)
		if app.ENABLE_CHANGELOOK_SYSTEM:
			item.SelectItem(targetIndex)
			if item.GetItemType() == item.ITEM_TYPE_WEAPON or item.GetItemType() == item.ITEM_TYPE_ARMOR or item.GetItemType() == item.ITEM_TYPE_COSTUME:
				item.SelectItem(scrollIndex)
				if item.GetValue(0) == changelook.CLEAN_ATTR_VALUE0:
					self.questionDialog.SetText(localeInfo.CHANGE_LOOK_DO_YOU_CLEAN)		
		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnDetachMetinFromItem))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		self.questionDialog.Open()
		self.questionDialog.sourcePos = scrollSlotPos
		self.questionDialog.targetPos = targetSlotPos

	def AttachMetinToItem(self, metinSlotPos, targetSlotPos):
		metinIndex = player.GetItemIndex(metinSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		item.SelectItem(metinIndex)
		itemName = item.GetItemName()

		result = player.CanAttachMetin(metinIndex, targetSlotPos)

		if player.ATTACH_METIN_NOT_MATCHABLE_ITEM == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_CAN_NOT_ATTACH(itemName))

		if player.ATTACH_METIN_NO_MATCHABLE_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_SOCKET(itemName))

		elif player.ATTACH_METIN_NOT_EXIST_GOLD_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_GOLD_SOCKET(itemName))

		elif player.ATTACH_METIN_CANT_ATTACH_TO_EQUIPMENT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)

		if player.ATTACH_METIN_OK != result:
			return

		self.attachMetinDialog.Open(metinSlotPos, targetSlotPos)



	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if app.ENABLE_SWAPITEM_SYSTEM:
			global SWAPITEM_STAT
			SWAPITEM_STAT = 1
			self.wndItem.SetSwapItem(FALSE)
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, overSlotPos):
		# PET SLOTS
		if overSlotPos == 1120 and constInfo.PetVnum != 0:
			self.tooltipItem.SetItemToolTip(constInfo.PetVnum)
			return

		if overSlotPos == 1121 and constInfo.PetOfficialVnum != 0:
			self.tooltipItem.SetItemToolTip(constInfo.PetOfficialVnum)
			return

		if app.ENABLE_HIGHLIGHT_SYSTEM:
			stat = 0
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)
			itemVnum = player.GetItemIndex(slotNumber)

			if constInfo.IS_AUTO_POTION(itemVnum):
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]
				if slotNumber >= player.INVENTORY_PAGE_SIZE*self.inventoryPageIndex:
					slotNumber -= player.INVENTORY_PAGE_SIZE*self.inventoryPageIndex
				
				isActivated = 0 != metinSocket[0]
				if isActivated:
					stat = 1
	
			if not stat:
				if slotNumber in self.listHighlightedSlot:
					self.wndItem.DeactivateSlot(overSlotPos)
					try:
						if app.ENABLE_ACCE_COSTUME_SYSTEM and app.ENABLE_CHANGELOOK_SYSTEM:
							if not slotNumber in self.listAttachedAcces:
								self.listHighlightedSlot.remove(slotNumber)
							if not slotNumber in self.listAttachedCl:
								self.listHighlightedSlot.remove(slotNumber)
						else:
							self.listHighlightedSlot.remove(slotNumber)
					except:
						pass
						
		
		overSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)
		self.wndItem.SetUsableItem(False)
		if app.ENABLE_SWAPITEM_SYSTEM:
			global SWAPITEM_STAT
			SWAPITEM_STAT = 1
			self.wndItem.SetSwapItem(FALSE)

		if mouseModule.mouseController.isAttached():
			attachedItemType = mouseModule.mouseController.GetAttachedType()
			if player.SLOT_TYPE_INVENTORY == attachedItemType:

				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()
				if app.ENABLE_SWAPITEM_SYSTEM:
					item.SelectItem(player.GetItemIndex(attachedSlotPos))
					isItemType = item.GetItemType()
					if isItemType == item.ITEM_TYPE_ARMOR or isItemType == item.ITEM_TYPE_WEAPON or isItemType == item.ITEM_TYPE_COSTUME or isItemType == item.ITEM_TYPE_BELT or isItemType == item.ITEM_TYPE_RING:
						(width1, height1) = item.GetItemSize()
						itemSize = height1
						item.SelectItem(player.GetItemIndex(overSlotPos))
						(width2, height2) = item.GetItemSize()
						itemDestSize = height2
						if itemDestSize > itemSize:
							SWAPITEM_STAT = 0
							self.wndItem.SetSwapItem(FALSE)
						elif itemSize == itemDestSize:
							self.wndItem.SetSwapItem(TRUE)
						elif itemSize > itemDestSize:
							error = 0
							if itemDestSize == 1 and overSlotPos >= 40 and overSlotPos < 45 or itemDestSize == 1 and overSlotPos >= 85 and overSlotPos < 90 or itemDestSize == 1 and overSlotPos >= 130 and overSlotPos < 135 or itemDestSize == 1 and overSlotPos >= 175 and overSlotPos < 180:
								error = 1
							
							if itemDestSize == 1 and itemSize == 3 and overSlotPos >= 35 and overSlotPos < 40 or itemDestSize == 1 and itemSize == 3 and overSlotPos >= 80 and overSlotPos < 85 or itemDestSize == 1 and itemSize == 3 and overSlotPos >= 125 and overSlotPos < 130 or itemDestSize == 1 and itemSize == 3 and overSlotPos >= 170 and overSlotPos < 175:
								error = 1
							
							if itemDestSize == 2 and itemSize == 3 and overSlotPos >= 35 and overSlotPos < 40 or itemDestSize == 2 and itemSize == 3 and overSlotPos >= 80 and overSlotPos < 85 or itemDestSize == 2 and itemSize == 3 and overSlotPos >= 125 and overSlotPos < 130 or itemDestSize == 2 and itemSize == 3 and overSlotPos >= 170 and overSlotPos < 175:
								error = 1
							
							if error:
								SWAPITEM_STAT = 0
								self.wndItem.SetSwapItem(FALSE)
								self.ShowToolTip(attachedSlotPos)
								return
							
							if itemSize == 2 and itemDestSize == 1 or itemSize == 3 and itemDestSize == 2:
								if itemDestSize == 2:
									overSlotPosNew = overSlotPos + 10
								else:
									overSlotPosNew = overSlotPos + 5
								itemCount = player.GetItemCount(overSlotPosNew)
								if itemCount == 0:
									self.wndItem.SetSwapItem(TRUE)
								else:
									item.SelectItem(player.GetItemIndex(overSlotPosNew))
									(width3, height3) = item.GetItemSize()
									itemDest2Size = height3
									if itemDest2Size == 1:
										self.wndItem.SetSwapItem(TRUE)
									else:
										SWAPITEM_STAT = 0
										self.wndItem.SetSwapItem(FALSE)
							elif itemSize == 3 and itemDestSize == 1:
								overSlotPosNew = overSlotPos + 5
								itemCount = player.GetItemCount(overSlotPosNew)
								if itemCount == 0:
									overSlotPosNew = overSlotPos + 10
									itemCountNew = player.GetItemCount(overSlotPosNew)
									if itemCountNew == 0:
										self.wndItem.SetSwapItem(TRUE)
									else:
										item.SelectItem(player.GetItemIndex(overSlotPosNew))
										(width3, height3) = item.GetItemSize()
										itemDest2Size = height3
										if itemDest2Size != 3:
											self.wndItem.SetSwapItem(TRUE)
										else:
											SWAPITEM_STAT = 0
											self.wndItem.SetSwapItem(FALSE)
								else:
									item.SelectItem(player.GetItemIndex(overSlotPosNew))
									(width3, height3) = item.GetItemSize()
									itemDest2Size = height3
									if itemDest2Size == 1:
										overSlotPosNew = overSlotPos + 10
										itemCountNew = player.GetItemCount(overSlotPosNew)
										if itemCountNew == 0:
											self.wndItem.SetSwapItem(TRUE)
										else:
											item.SelectItem(player.GetItemIndex(overSlotPosNew))
											(width3, height3) = item.GetItemSize()
											itemDest2Size = height3
											if itemDest2Size == 1:
												self.wndItem.SetSwapItem(TRUE)
											else:
												SWAPITEM_STAT = 0
												self.wndItem.SetSwapItem(FALSE)
									elif itemDest2Size == 2:
										self.wndItem.SetSwapItem(TRUE)
									else:
										SWAPITEM_STAT = 0
										self.wndItem.SetSwapItem(FALSE)
							else:
								SWAPITEM_STAT = 0
								self.wndItem.SetSwapItem(FALSE)
						else:
							SWAPITEM_STAT = 0
							self.wndItem.SetSwapItem(FALSE)
						
						self.ShowToolTip(attachedSlotPos)
						return

				if attachedItemVNum==player.ITEM_MONEY: # @fixme005
					pass
				elif self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPos):
					self.wndItem.SetUsableItem(True)
					self.ShowToolTip(overSlotPos)
					return

		self.ShowToolTip(overSlotPos)


	def __IsUsableItemToItem(self, srcItemVNum, srcSlotPos):
		"다른 아이템에 사용할 수 있는 아이템인가?"
        
		if srcItemVNum >= 55701 and srcItemVNum <= 55710:
			return True
		
		if srcItemVNum == 55001:
			return True

		if item.IsRefineScroll(srcItemVNum):
			return True
		elif item.IsMetin(srcItemVNum):
			return True
		elif item.IsDetachScroll(srcItemVNum):
			return True
		elif item.IsKey(srcItemVNum):
			return True
		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True
		elif (srcItemVNum == 58500 or srcItemVNum == 58501 or srcItemVNum == 58502):
			return True
		else:
			if item.GetUseType(srcItemVNum) in self.USE_TYPE_TUPLE:
				return True

		return False

	def __CanUseSrcItemToDstItem(self, srcItemVNum, srcSlotPos, dstSlotPos):
		"대상 아이템에 사용할 수 있는가?"
        
		srcItemVNum = player.GetItemIndex(srcSlotPos)
		
		if srcItemVNum >= 55701 and  srcItemVNum <= 55710 and player.GetItemIndex(dstSlotPos) == 55002:			
			return True		
		
		if srcItemVNum == 55001 and player.GetItemIndex(dstSlotPos) >= 55701 and player.GetItemIndex(dstSlotPos) <= 55710:			
			return True

		if srcSlotPos == dstSlotPos:
			return False

		if item.IsRefineScroll(srcItemVNum):
			if player.REFINE_OK == player.CanRefine(srcItemVNum, dstSlotPos):
				return True
		
		# Fix Stone
		elif item.IsMetin(srcItemVNum):
			ItemVNumDest = player.GetItemIndex(dstSlotPos)
			item.SelectItem(ItemVNumDest)
			if not (item.ITEM_TYPE_METIN == item.GetItemType() and item.METIN_NORMAL == item.GetItemSubType()):
				if player.ATTACH_METIN_OK == player.CanAttachMetin(srcItemVNum, dstSlotPos):
					return True
			else:
				if ItemVNumDest == srcItemVNum:
					return True
		# End Fix Stone		
				
		elif item.IsDetachScroll(srcItemVNum):
			if player.DETACH_METIN_OK == player.CanDetach(srcItemVNum, dstSlotPos):
				return True
		elif item.IsKey(srcItemVNum):
			if player.CanUnlock(srcItemVNum, dstSlotPos):
				return True

		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True
			
		elif  srcItemVNum == 58500 or srcItemVNum == 58501 or srcItemVNum == 58502:
			item.SelectItem(player.GetItemIndex(dstSlotPos))
			return ( (item.GetItemType() == 1 and item.GetItemSubType() < 6) or (item.GetItemType() == 2 and item.GetItemSubType() < 5))

		else:
			useType=item.GetUseType(srcItemVNum)

			if "USE_CLEAN_SOCKET" == useType:
				if self.__CanCleanBrokenMetinStone(dstSlotPos):
					return True
			elif "USE_CHANGE_ATTRIBUTE" == useType:
				if app.ENABLE_DRAGON_SOUL_CHANGE_BONUS_WORLDARD:
					if extern_wa_dragonsoul_bonus.CanChangeItemAttrList(dstSlotPos,srcItemVNum):
						return True
				else:
					if self.__CanChangeItemAttrList(dstSlotPos):
						return True
			elif "USE_ADD_ATTRIBUTE" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			if app.ENABLE_6_7_BONUS_NEW_SYSTEM:
				if "USE_CHANGE_ATTRIBUTE2" == useType:
					if self.__CanChange2ItemAttrList(dstSlotPos):
						return True
			elif "USE_ADD_ATTRIBUTE2" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			elif "USE_ADD_ACCESSORY_SOCKET" == useType:
				if self.__CanAddAccessorySocket(dstSlotPos):
					return True
			elif "USE_PUT_INTO_ACCESSORY_SOCKET" == useType:
				if self.__CanPutAccessorySocket(dstSlotPos, srcItemVNum):
					return True;
			elif "USE_PUT_INTO_BELT_SOCKET" == useType:
				dstItemVNum = player.GetItemIndex(dstSlotPos)
				print "USE_PUT_INTO_BELT_SOCKET", srcItemVNum, dstItemVNum

				item.SelectItem(dstItemVNum)

				if item.ITEM_TYPE_BELT == item.GetItemType():
					return True
			elif "USE_CHANGE_COSTUME_ATTR" == useType:
				if self.__CanChangeCostumeAttrList(dstSlotPos):
					return True
			elif "USE_RESET_COSTUME_ATTR" == useType:
				if self.__CanResetCostumeAttr(dstSlotPos):
					return True

			if app.CHANGE_PETSYSTEM:
				if "USE_CHANGE_LV_P" == useType:
					if self.CanChangePet(dstSlotPos):
						return True


		return False

	if app.CHANGE_PETSYSTEM:
		def CanChangePet(self, dstSlotPos):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			item.SelectItem(dstItemVNum)

			pet_seals = [55701, 55702, 55703, 55704, 55705, 55706, 55716]

			if dstItemVNum in pet_seals:
				return True

			return False

	if app.ENABLE_6_7_BONUS_NEW_SYSTEM:	
		def __CanChange2ItemAttrList(self,dstSlotPos):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False

			item.SelectItem(dstItemVNum)

			if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
				return False


			if item.GetItemSubType() == item.WEAPON_ARROW or item.GetItemSubType() == item.ARMOR_TALISMAN:
				return False

			if self.__GetAttribute67Bonus(dstSlotPos) <= 5:
				return False

			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				if player.GetItemAttribute(dstSlotPos, i) != 0:
					return True

			return False

		def __GetAttribute67Bonus(self,slot):
			count = 0
			attrSlot = []

			for attr in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(player.GetItemAttribute(slot, attr))
				
			if 0 == attrSlot:
				return count
			
			for q in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				type = attrSlot[q][0]
				value = attrSlot[q][1]
				if type != 0:
					count += 1
			
			return count


	def __CanCleanBrokenMetinStone(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.ITEM_TYPE_WEAPON != item.GetItemType():
			return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemMetinSocket(dstSlotPos, i) == constInfo.ERROR_METIN_STONE:
				return True

		return False

	def __CanChangeItemAttrList(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
			return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				return True

		return False

	def __CanChangeCostumeAttrList(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_COSTUME:
			return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				return True

		return False

	def __CanResetCostumeAttr(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_COSTUME:
			return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				return True

		return False

	def __CanPutAccessorySocket(self, dstSlotPos, mtrlVnum):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)

		if mtrlVnum != constInfo.GET_ACCESSORY_MATERIAL_VNUM(dstItemVNum, item.GetItemSubType()):
			return False

		if curCount>=maxCount:
			return False

		return True

	def __CanAddAccessorySocket(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)

		ACCESSORY_SOCKET_MAX_SIZE = 3
		if maxCount >= ACCESSORY_SOCKET_MAX_SIZE:
			return False

		return True

	def __CanAddItemAttr(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
			return False

		attrCount = 0
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				attrCount += 1

		if attrCount<4:
			return True

		return False

	def ShowToolTip(self, slotIndex):
		if None != self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex)
			
			if constInfo.ENABLE_SHOW_CHEST_DROP:
				itemVnum = player.GetItemIndex(slotIndex)
				item.SelectItem(itemVnum)
				if item.GetItemType() == item.ITEM_TYPE_GIFTBOX:
					self.tooltipItem.AppendSpace(5)
					text = self.tooltipItem.AppendTextLine("|Ekey_ctrl|e"+" + "+"|Ekey_lclick|e - Visualizza contenuto",grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0),False)
					text.SetHorizontalAlignLeft()
					self.tooltipItem.AppendSpace(5)
					text = self.tooltipItem.AppendTextLine("|Ekey_alt|e"+" + "+"|Ekey_rclick|e - Apri %dpcs"%constInfo.ULTIMATE_TOOLTIP_MAX_CLICK,grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0),False)
					text.SetHorizontalAlignLeft()
				elif constInfo.IsNewChest(itemVnum):
					self.tooltipItem.AppendSpace(5)
					text = self.tooltipItem.AppendTextLine("|Ekey_alt|e"+" + "+"|Ekey_rclick|e - Apri %dpcs"%constInfo.ULTIMATE_TOOLTIP_MAX_CLICK,grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0),False)
					text.SetHorizontalAlignLeft()
				if player.CanMoveItem(itemVnum):
					self.tooltipItem.AppendSpace(5)
					text = self.tooltipItem.AppendTextLine("|Ekey_ctrl|e"+" + "+"|Ekey_rclick|e - Muovi a inv./ speciale",grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0),False)
					text.SetHorizontalAlignLeft()

	def OnTop(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetTop()

		if app.WJ_ENABLE_TRADABLE_ICON:
			map(lambda wnd:wnd.RefreshLockedSlot(), self.bindWnds)
			self.RefreshMarkSlots()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	# EMPTY FUNCTION 
	def UseItem(self, slotIndex):
		ItemVNum = player.GetItemIndex(slotIndex)
		item.SelectItem(ItemVNum)
		if item.IsFlag(item.ITEM_FLAG_CONFIRM_WHEN_USE):
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM)
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
			self.questionDialog.Open()
			self.questionDialog.slotIndex = slotIndex
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
		else:
			self.__SendUseItemPacket(slotIndex)

	def UseItemSlot(self, slotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return
		
		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			if self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.AutoSetItem((player.INVENTORY, slotIndex), 1)
				return
		
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if self.isShowAcceWindow():
				acce.Add(player.INVENTORY, slotIndex, 255)
				return
		if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
			if app.IsPressed(app.DIK_LCONTROL) and player.CanMoveItem(player.GetItemIndex(slotIndex)):
			#if self.interface.wndSpecialStorage.IsShow() and app.IsPressed(app.DIK_LCONTROL) and player.CanMoveItem(player.GetItemIndex(slotIndex)):
				net.SendChatPacket("/transfer_inv_storage %d" % (slotIndex))
 
		if app.ENABLE_CHANGELOOK_SYSTEM:
			if self.isShowChangeLookWindow():
				changelook.Add(player.INVENTORY, slotIndex, 255)
				return

		if constInfo.ENABLE_AURA_SYSTEM:
			if self.interface.auraUpgrade.IsShow():
				if self.interface.auraUpgrade.pos[0] == -1:
					self.interface.auraUpgrade.SelectRightClick(0,slotIndex)
				elif self.interface.auraUpgrade.pos[1] == -1:
					self.interface.auraUpgrade.SelectRightClick(1,slotIndex)
				return True
			if self.interface.auraAbs.IsShow():
				if self.interface.auraAbs.pos[0] == -1:
					self.interface.auraAbs.SelectRightClick(0,slotIndex)
				elif self.interface.auraAbs.pos[1] == -1:
					self.interface.auraAbs.SelectRightClick(1,slotIndex)
				return True
				
		self.__UseItem(slotIndex)
		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()

	def __UseItem(self, slotIndex):
		ItemVNum = player.GetItemIndex(slotIndex)
		item.SelectItem(ItemVNum)
		if app.ENABLE_SELL_ITEM:		
			if app.IsPressed(app.DIK_LSHIFT) and app.IsPressed(app.DIK_X) and self.IsSellItems(slotIndex):
				self.__SendSellItemPacket(slotIndex)
				return
		if constInfo.ENABLE_SHOW_CHEST_DROP:
			if app.IsPressed(app.DIK_LALT):
				itemVnum = player.GetItemIndex(slotIndex)
				if constInfo.IsNewChest(itemVnum) or item.GetItemType() == item.ITEM_TYPE_GIFTBOX:
					count = player.GetItemCount(slotIndex)
					if count > constInfo.ULTIMATE_TOOLTIP_MAX_CLICK:
						count = constInfo.ULTIMATE_TOOLTIP_MAX_CLICK
					for j in xrange(count):
						self.__SendUseItemPacket(slotIndex)
					return
			#elif app.IsPressed(app.DIK_LCONTROL):
			#	# here
			#	return
		#if app.ENABLE_EXTEND_INVEN_SYSTEM:
		#	if ItemVNum == 72320:
		#		envanter = None
		#		if player.GetEnvanter() > 17:
		#			self.wndPopupDialog = uiCommon.PopupDialog()
		#			self.wndPopupDialog.SetText(localeInfo.ENVANTER_ZATEN_GENIS_3)
		#			self.wndPopupDialog.Open()
		#		elif player.GetEnvanter() < 4:
		#			envanter = 2
		#		elif player.GetEnvanter() > 3 and player.GetEnvanter() < 6:
		#			envanter = 3
		#		elif player.GetEnvanter() > 5 and player.GetEnvanter() < 9:
		#			envanter = 4
		#		elif player.GetEnvanter() > 8 and player.GetEnvanter() < 12:
		#			envanter = 5
		#		elif player.GetEnvanter() > 11 and player.GetEnvanter() < 15:
		#			envanter = 6
		#		elif player.GetEnvanter() > 14 and player.GetEnvanter() < 18:
		#			envanter = 7
		#		self.questionDialog = uiCommon.QuestionDialog()
		#		self.questionDialog.SetText(localeInfo.ENVANTER_GENIS_1 % envanter)
		#		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.genislet))
		#		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		#		self.questionDialog.Open()
		#		self.questionDialog.slotIndex = slotIndex
		if item.IsFlag(item.ITEM_FLAG_CONFIRM_WHEN_USE):
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM)
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
			self.questionDialog.Open()
			self.questionDialog.slotIndex = slotIndex

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
		elif uiSoulStone.SOUL_STONE_VNUM == ItemVNum:
			self.OpenSoulStoneWindow(slotIndex)
		else:
			self.__SendUseItemPacket(slotIndex)
			#net.SendItemUsePacket(slotIndex)

	def __UseItemQuestionDialog_OnCancel(self):
		self.OnCloseQuestionDialog()

	def __UseItemQuestionDialog_OnAccept(self):
		self.__SendUseItemPacket(self.questionDialog.slotIndex)
		self.OnCloseQuestionDialog()

	def __SendUseItemToItemPacket(self, srcSlotPos, dstSlotPos, srcSlotWin = player.SLOT_TYPE_INVENTORY, dstSlotWin = player.SLOT_TYPE_INVENTORY):
		# 개인상점 열고 있는 동안 아이템 사용 방지
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return
		# BEGIN_OFFLINE_SHOP
		if uiOfflineShopBuilder.IsBuildingOfflineShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, "USE_ITEM_FAILURE_OFFLINE_SHOP")
			return

		if uiOfflineShop.IsEditingOfflineShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, "USE_ITEM_FAILURE_OFFLINE_SHOP")
			return
		# END_OF_OFFLINE_SHOP
		net.SendItemUseToItemPacket(player.SlotTypeToInvenType(srcSlotWin), srcSlotPos, player.SlotTypeToInvenType(dstSlotWin), dstSlotPos)

	def __SendUseItemPacket(self, slotPos):
		# 개인상점 열고 있는 동안 아이템 사용 방지
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return
		# BEGIN_OFFLINE_SHOP
		if uiOfflineShopBuilder.IsBuildingOfflineShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, "USE_ITEM_FAILURE_OFFLINE_SHOP")
			return

		if uiOfflineShop.IsEditingOfflineShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, "USE_ITEM_FAILURE_OFFLINE_SHOP")
			return
		# END_OF_OFFLINE_SHOP
		net.SendItemUsePacket(slotPos)

	def __SendMoveItemPacket(self, srcSlotPos, dstSlotPos, srcItemCount):
		# 개인상점 열고 있는 동안 아이템 사용 방지
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
			return
		# BEGIN_OFFLINE_SHOP
		if uiOfflineShopBuilder.IsBuildingOfflineShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_OFFLINE_SHOP)
			return

		if uiOfflineShop.IsEditingOfflineShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_OFFLINE_SHOP)
			return
		# END_OF_OFFLINE_SHOP
		if app.ENABLE_SWAPITEM_SYSTEM:
			global SWAPITEM_STAT
			if SWAPITEM_STAT:
				net.SendItemMovePacket(srcSlotPos, dstSlotPos, srcItemCount)
			else:
				return
		else:
			net.SendItemMovePacket(srcSlotPos, dstSlotPos, srcItemCount)

	if app.ENABLE_SELL_ITEM:
		def IsSellItems(self, slotIndex):
			itemVnum = player.GetItemIndex(slotIndex)
			item.SelectItem(itemVnum)
			itemPrice = item.GetISellItemPrice()
			
			# if item.GetItemType() == item.ITEM_TYPE_WEAPON or item.GetItemType() == item.ITEM_TYPE_ARMOR:
				# return True
				
			if itemPrice > 1:
				return True
				
			return False
			
		def __SendSellItemPacket(self, itemVNum):
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
				return
				
			net.SendItemSellPacket(itemVNum)

	def SetDragonSoulRefineWindow(self, wndDragonSoulRefine):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoulRefine = wndDragonSoulRefine
	
	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def SetAcceWindow(self, wndAcceCombine, wndAcceAbsorption):
			self.wndAcceCombine = wndAcceCombine
			self.wndAcceAbsorption = wndAcceAbsorption

		def isShowAcceWindow(self):
			if self.wndAcceCombine:
				if self.wndAcceCombine.IsShow():
					return 1

			if self.wndAcceAbsorption:
				if self.wndAcceAbsorption.IsShow():
					return 1
			
			return 0

	if app.ENABLE_CHANGELOOK_SYSTEM:
		def SetChangeLookWindow(self, wndChangeLook):
			self.wndChangeLook = wndChangeLook

		def isShowChangeLookWindow(self):
			if self.wndChangeLook:
				if self.wndChangeLook.IsShow():
					return 1
			
			return 0

	def ClickMantelloButton(self):
		net.SendChatPacket("/aggregate")

	def ClickShitButton(self, shit_button):
		if shit_button == 1:
			self.wndSystem.OpenInventory()
			self.HideAllShitButton()
		else:
			self.wndBelt.OpenInventory()
			self.shitbuttons[shit_button].Hide()

	def ShowShitButton(self, x):
		self.shitbuttons[x].Show()

	def ShowShitButtonAll(self):
		for x in xrange(len(self.shitbuttons)):
			self.shitbuttons[x].Show()

	def HideAllShitButton(self):
		for x in xrange(len(self.shitbuttons)):
			self.shitbuttons[x].Hide()

	def OnMoveWindow(self, x, y):
#		print "Inventory Global Pos : ", self.GetGlobalPosition()
		if self.wndBelt:
#			print "Belt Global Pos : ", self.wndBelt.GetGlobalPosition()
			self.wndBelt.AdjustPositionAndSize()
		#if self.wndSidebar:
		#	self.wndSidebar.AdjustPositionAndSize()
		if app.ENABLE_BIOLOG_SYSTEM:
			if self.wndCollect:
				self.wndCollect.AdjustPositionAndSize()
		if app.__ENABLE_TRASH_BIN__:
			self.AlignTrashBin()
		if self.wndSystem:
			self.wndSystem.AdjustPositionAndSize()

	def ReferencePages(self, token):
		GetObject = self.GetChild
		
		ar_ListObjects = [
			GetObject("Defensiv"),GetObject("Schwert"),GetObject("Schwert_info"),GetObject("2Hand"),GetObject("2Hand_info"),GetObject("Dolch"),GetObject("Dolch_info"),GetObject("Pfeilwiderstand"),GetObject("Pfeilwiderstand_info"),GetObject("Glocke"),GetObject("Glocke_info"),GetObject("Faecher"),GetObject("Faecher_info"),GetObject("Magiewiederstand"),GetObject("Magiewiederstand_info"),GetObject("Giftwiederstand"),GetObject("Giftwiederstand_info"),GetObject("Krieger"),GetObject("Krieger_info"),GetObject("Ninja"),GetObject("Ninja_info"),GetObject("Sura"),GetObject("Sura_info"),GetObject("Schamane"),GetObject("Schamane_info"),GetObject("Offensive"),GetObject("Krit"),GetObject("Krit_info"),GetObject("DB"),GetObject("DB_info"),GetObject("DSS"),GetObject("DSS_info"),GetObject("FKS"),GetObject("FKS_info"),GetObject("Halbmenschen"),GetObject("Halbmenschen_info"),GetObject("Untote"),GetObject("Untote_info"),GetObject("Teufel"),GetObject("Teufel_info"),GetObject("KriegerO"),GetObject("KriegerO_info"),GetObject("NinjaO"),GetObject("NinjaO_info"),GetObject("SuraO"),GetObject("SuraO_info"),GetObject("SchamaneO"),GetObject("SchamaneO_info")
		]
		for it in ar_ListObjects:
			if token == 0:
				it.Hide()
			else:
				it.Show()
		
	def MinimierenInfoTable(self, arg):
		if arg == True:
			self.ReferencePages(0)
		else:
			self.ReferencePages(1)
	
	def ReloadBonus(self):
		ar_ListBonus = [ 69, 70, 71, 74, 72, 73, 77, 81, 59, 60, 61, 62, 40, 41, 122, 121, 43, 47, 48, 54, 55, 56, 57 ]

		for it in range(1, len(ar_ListBonus) + 1):
			try:
				self.GetChild("bonus_%d" % it).SetText(str(player.GetStatus(ar_ListBonus[it - 1])))
			except:
				pass
			
	def OnUpdate(self):
		#if app.ENABLE_SORT_INVEN and self.tooltipInfo:
		#	for i in xrange(len(self.tooltipInfo)):
		#		if self.yenilebutton.IsIn():
		#			self.tooltipInfo[i].Show()
		#		else:
		#			self.tooltipInfo[i].Hide()
		self.ReloadBonus()

	if app.ENABLE_COSTUME_SWITCHBOT:
		def OpenSwitch(self, itemindex1, itemindex1pos, itemindex2, itemindex2count, itemindex2pos):
			import uimanualswitchbot
			self.manualswitchbotWnd = uimanualswitchbot.Switcher() 
			self.manualswitchbotWnd.Show()
			self.manualswitchbotWnd.switchslot.SetItemSlot(0, itemindex1, 0)	
			self.manualswitchbotWnd.switchslot.SetItemSlot(1, itemindex2, itemindex2count)	
			self.manualswitchbotWnd.slotgira = itemindex2pos
			self.manualswitchbotWnd.slotitem = itemindex1pos


class RuneWindow(ui.ScriptWindow):

	def __init__(self, wndInventory):				
			 	 
		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		self.RefreshEquipSlotWindow()
		self.SetCenterPosition()

		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/RuneWindow.py")
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			wndEquip = self.GetChild("RuneSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		## Equipment
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))						
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))

		self.wndEquip = wndEquip

	def RefreshEquipSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndEquip.SetItemSlot
		for i in xrange(player.EQUIPMENT_PAGE_COUNT):
			slotNumber = player.EQUIPMENT_SLOT_START + i
			itemCount = getItemCount(slotNumber)
			if itemCount <= 1:
				itemCount = 0
			setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)

		if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
			for i in xrange(player.NEW_EQUIPMENT_SLOT_COUNT):
				slotNumber = player.NEW_EQUIPMENT_SLOT_START + i
				itemCount = getItemCount(slotNumber)
				if itemCount <= 1:
					itemCount = 0
				setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)
				print "ENABLE_NEW_EQUIPMENT_SYSTEM", slotNumber, itemCount, getItemVNum(slotNumber)

		self.wndEquip.RefreshSlot()

class SystemInventoryWindow(ui.ScriptWindow):

	def __init__(self, wndInventory):
		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;
		
		self.wndSystemInventoryLayer = None
		self.wndSystemInventorySlot = None
		self.minBtn = None

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self, openSystemSlot = False):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)
		
		if openSystemSlot:
			self.OpenInventory()
		else:
			self.CloseInventory()

	def Close(self):
		self.Hide()
		
	def IsOpeningInventory(self):
		return self.wndSystemInventoryLayer.IsShow()
		
	def OpenInventory(self):
		self.wndSystemInventoryLayer.Show()
		#self.expandBtn.Hide()
		#self.minBtn.Show()
		self.AdjustPositionAndSize()

	def CloseInventory(self):
		self.wndSystemInventoryLayer.Hide()
		#self.expandBtn.Show()
		self.AdjustPositionAndSize()
		#self.minBtn.Hide()
		self.wndInventory.ShowShitButtonAll()

	def ButtonOne(self):
		self.wndInventory.ToggleSwitchbotWindow()
		
	def ButtonTwo(self):
		self.wndInventory.quikeqchange()
		
	def ButtonThree(self):
		self.wndInventory.BonusPage()
		
	def ButtonFour(self):
		self.wndInventory.OpenTeleportSystem()
		
	def ButtonFive(self):
		self.wndInventory.OpenMentaLSkyGui()
		
	def ButtonSix(self):
		self.wndInventory.EnablePickUpItem()

	def ButtonSeven(self):
		self.wndInventory.OpenDSGui()

	def GetBasePosition(self):
		x, y = self.wndInventory.GetGlobalPosition()
		return x -110-20-5-5-3, y+120
		
	def AdjustPositionAndSize(self):
		bx, by = self.GetBasePosition()
		
		if self.IsOpeningInventory():
			self.SetPosition(bx, by)
			self.SetSize(self.ORIGINAL_WIDTH, self.GetHeight())
			
		else:
			self.SetPosition(bx+120+5+5+3, by);
			self.SetSize(110, self.GetHeight())

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/SystemInventoryWindow.py")
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			self.ORIGINAL_WIDTH = self.GetWidth()
			self.wndSystemInventoryLayer = self.GetChild("SystemInventoryLayer")
			self.expandBtn = self.GetChild("ExpandBtn")
			self.RaktarBtn = self.GetChild("RaktarGomb")
			self.OffShopBtn = self.GetChild("OfflineShopButton")
			self.biologBtn = self.GetChild("biolog")
			self.OkeyCardBtn = self.GetChild("OkeyCardButton")
			self.specialBtn = self.GetChild("special")
			self.clickbpBtn = self.GetChild("clickbattlepasschoose")
			self.bonusBtn = self.GetChild("bonus")
			self.minBtn = self.GetChild("MinimizeBtn")
			
			self.minBtn.Hide()
			self.expandBtn.Hide()
			self.expandBtn.SetEvent(ui.__mem_func__(self.OpenInventory))
			self.RaktarBtn.SetEvent(ui.__mem_func__(self.ButtonOne))
			self.OffShopBtn.SetEvent(ui.__mem_func__(self.ButtonTwo))
			self.biologBtn.SetEvent(ui.__mem_func__(self.ButtonThree))
			self.OkeyCardBtn.SetEvent(ui.__mem_func__(self.ButtonFour))
			self.specialBtn.SetEvent(ui.__mem_func__(self.ButtonFive))
			self.clickbpBtn.SetEvent(ui.__mem_func__(self.ButtonSix))
			self.bonusBtn.SetEvent(ui.__mem_func__(self.ButtonSeven))
			self.minBtn.SetEvent(ui.__mem_func__(self.CloseInventory))
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

