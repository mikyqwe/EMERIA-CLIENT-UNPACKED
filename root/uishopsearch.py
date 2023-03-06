# Development By Grimm @ 2020
import ui
import item
import net
import constInfo
import localeInfo
import uiCommon
import wndMgr
import app
import grp
import chat
import player
import skill
import shop

CATEGORY_SHOP_PATH = "d:/ymir work/ui/shop/category_icons/"

class ShopSearchFilter(ui.ScriptWindow):
	
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.bAlready = False
		self.MakeFilterWindow()
	
	def MakeFilterWindow(self):
		if self.bAlready == True:
			return
	
		self.SetSize(200, 230)
		self.AddFlag("movable")
		self.AddFlag("float")
	
		self.wndFilterBoard = ui.Board_Brown()
		self.wndFilterBoard.SetParent(self)
		self.wndFilterBoard.AddFlag("attach")
		self.wndFilterBoard.SetSize(200, 230)
		self.wndFilterBoard.Hide()
		
		self.wndFilterTitleBar = ui.TitleBar()
		self.wndFilterTitleBar.SetParent(self.wndFilterBoard)
		self.wndFilterTitleBar.MakeTitleBar(200 - 15, 0)
		self.wndFilterTitleBar.SetPosition(7, 8)
		self.wndFilterTitleBar.SetCloseEvent(ui.__mem_func__(self.CloseFilter))
		self.wndFilterTitleBar.Show()

		self.wndFilterTitleName = ui.MakeText(self.wndFilterTitleBar, "Filtru preþ", 200 / 2 - 30, 6)
	
		self.wndYangTitle = ui.MakeText(self.wndFilterTitleBar, "Filtru Yang", 200 / 2 - 30, 14+5)
	
		self.wndFilterDesign1 = ui.MakeImageBox(self.wndFilterBoard, "d:/ymir work/ui/shop/insert.png", 30, 33+14+5)
		self.wndFilterDesign2 = ui.MakeImageBox(self.wndFilterBoard, "d:/ymir work/ui/shop/insert.png", 30, 63+14+5)

		self.img_icon_gold = ui.MakeImageBox(self.wndFilterBoard, "d:/ymir work/ui/game/windows/money_icon.sub", 13, 49+14+5)

		self.wndMinPrice = ui.EditLine()
		self.wndMinPrice.SetParent(self.wndFilterDesign1)
		self.wndMinPrice.SetPosition(3, 3)
		self.wndMinPrice.SetSize(136, 15+5)
		self.wndMinPrice.SetMax(10)
		self.wndMinPrice.SetNumberMode()
		self.wndMinPrice.SetText("0")
		self.wndMinPrice.Show()
		
		self.wndMaxPrice = ui.EditLine()
		self.wndMaxPrice.SetParent(self.wndFilterDesign2)
		self.wndMaxPrice.SetPosition(3, 3)
		self.wndMaxPrice.SetSize(136, 15+5)
		self.wndMaxPrice.SetMax(10)
		self.wndMaxPrice.SetNumberMode()
		self.wndMaxPrice.SetText("1999999999")
		self.wndMaxPrice.Show()

	
		self.wndChequeTitle = ui.MakeText(self.wndFilterTitleBar, "Filtru Won", 200 / 2 - 30, 2+95)
	
		self.wndFilterDesignC1 = ui.MakeImageBox(self.wndFilterBoard, "d:/ymir work/ui/shop/insert.png", 30, 33+95)
		self.wndFilterDesignC2 = ui.MakeImageBox(self.wndFilterBoard, "d:/ymir work/ui/shop/insert.png", 30, 63+95)

		self.img_icon_cheque = ui.MakeImageBox(self.wndFilterBoard, "d:/ymir work/ui/game/windows/cheque_icon.sub", 13, 49+95)

		self.wndMinCheque = ui.EditLine()
		self.wndMinCheque.SetParent(self.wndFilterDesignC1)
		self.wndMinCheque.SetPosition(3, 3)
		self.wndMinCheque.SetSize(136, 15+95)
		self.wndMinCheque.SetMax(2)
		self.wndMinCheque.SetNumberMode()
		self.wndMinCheque.SetText("0")
		self.wndMinCheque.Show()
		
		self.wndMaxCheque = ui.EditLine()
		self.wndMaxCheque.SetParent(self.wndFilterDesignC2)
		self.wndMaxCheque.SetPosition(3, 3)
		self.wndMaxCheque.SetSize(136, 15+95)
		self.wndMaxCheque.SetMax(2)
		self.wndMaxCheque.SetNumberMode()
		self.wndMaxCheque.SetText("99")
		self.wndMaxCheque.Show()
	
		self.btnClose = ui.MakeButton(self.wndFilterBoard, 200 / 2 - 30, 63+95+15, False, "d:/ymir work/ui/shop/", "small_btn.dds", "small_btn_over.dds", "small_btn_down.dds")
		self.btnClose.SetEvent(ui.__mem_func__(self.CloseFilter))
		self.btnClose.SetText("Închide filtru")
	
		self.Hide()
		
		self.bAlready = True
		
	def GetMinCheque(self):
		return int(self.wndMinCheque.GetText())
	
	def GetMaxCheque(self):
		return int(self.wndMaxCheque.GetText())
		
	def GetMinPrice(self):
		return int(self.wndMinPrice.GetText())
		
	def GetMaxPrice(self):
		return int(self.wndMaxPrice.GetText())
	
	def ShowFilter(self):
		if not self.wndFilterBoard.IsShow():
			self.SetTop()
			self.SetCenterPosition()
			self.Show()
			self.wndFilterBoard.Show()
		else:
			self.CloseFilter()

	def CloseFilter(self):
		self.Hide()
		self.wndFilterBoard.Hide()

class ShopSearch(ui.ScriptWindow):

	# Config Shop Search 
	
	MAX_ITEMS_PAGE = 9
	pos_x = [10, 160+40, 310+80]
	pos_y = [10, 10, 10, 130, 130, 130, 250, 250, 250]

	Categories=[
		{"name": "Tutti", "icon": "dragonsoul.dds", "type": 99},
		{"name": "Armi", "icon": "weapons.dds", "type": item.ITEM_TYPE_WEAPON},
		{"name": "Equipaggiamenti", "icon":"equipment.dds", "type": item.ITEM_TYPE_ARMOR},
		{"name": "Costumi - Mounts", "icon":"skins.dds", "type": 28},
		{"name": "Consumabili", "icon": "consumable.dds", "type": 3},
		{"name": "Materiali", "icon":"items.dds", "type": 4},
		{"name": "Buffs", "icon":"aid.dds", "type": 33},
		{"name": "Miglioramento", "icon":"shop.dds", "type": 5},
		{"name": "Libri", "icon": "books.dds", "type": 17},
		{"name": "Forzieri", "icon": "shop.dds", "type": 23},
		{"name": "Pietre", "icon": "mining.dds", "type": 10},
	]
	
	SubCategoriesEquipments = [
		{"name": "Archi", "icon":"equipment.dds", "type": item.WEAPON_BOW, "ExpandForType" : 1},
		{"name": "Campane", "icon":"equipment.dds", "type": item.WEAPON_BELL, "ExpandForType" : 1},
		{"name": "Ventagli", "icon":"equipment.dds", "type": item.WEAPON_FAN, "ExpandForType" : 1},
		{"name": "Frecce", "icon":"equipment.dds", "type": item.WEAPON_ARROW, "ExpandForType" : 1},
		{"name": "Pugnali", "icon":"equipment.dds", "type": item.WEAPON_DAGGER, "ExpandForType" : 1},
		{"name": "Spade", "icon":"equipment.dds", "type": item.WEAPON_SWORD, "ExpandForType" : 1},
		{"name": "Spadoni", "icon":"equipment.dds", "type": item.WEAPON_TWO_HANDED, "ExpandForType" : 1},	
		{"name": "Armature", "icon": "weapons.dds", "type": item.ARMOR_BODY, "ExpandForType" : 2},
		{"name": "Elmi", "icon":"equipment.dds", "type": item.ARMOR_HEAD, "ExpandForType" : 2},
		{"name": "Scudi", "icon":"equipment.dds", "type": item.ARMOR_SHIELD, "ExpandForType" : 2},
		{"name": "Bracciali", "icon":"equipment.dds", "type": item.ARMOR_WRIST, "ExpandForType" : 2},
		{"name": "Scarpe", "icon":"equipment.dds", "type": item.ARMOR_FOOTS, "ExpandForType" : 2},
		{"name": "Collane", "icon":"equipment.dds", "type": item.ARMOR_NECK, "ExpandForType" : 2},
		{"name": "Orecchini", "icon":"equipment.dds", "type": item.ARMOR_EAR, "ExpandForType" : 2},
		
	]
	# You understand how to config here types-subtypes?
	
	# Config Shop Search
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.loaded = 0
		self.tooltip = None
		self.interface = None
		self.bItem = {}
		self.bGrid = {}
		self.wndNameItem = {}
		self.wndSeller = {}
		self.wndPrice = {}
		self.wndPriceCheque = {}
		self.wndQuantity = {}
		self.btnBuy = {}
		self.btnWhisper = {}
		self.LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def Show(self):
		self.OverOutItem()
		self.LoadWindow()
		self.SetCenterPosition()
		ui.ScriptWindow.Show(self)
		self.test_y = 0
		self.test_x = 0
		self.cPage = 1
		self.cLastPage = 1
		self.bDone = False
		self.dlgQuestion = None
		self.ListExpanded = {}
		self.SelectCategory(0, 99) # Select default category.
		self.OnSearchItem()

	def LoadWindow(self):
		if self.loaded == 1:
			return
		self.loaded == 1
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/shopsearch.py")
		except:
			import exception
			exception.Abort("shopsearch.LoadWindow.LoadObject")
		try:
			self.titleBar = self.GetChild("TitleBar")
			self.board = self.GetChild("board")
			self.bSearch = self.GetChild("ThiniSearch")
			self.AnimBoard = self.GetChild("Animation_Board")
			self.SearchButton = self.GetChild("search_button")
			self.sItemName = self.GetChild("ItemNameValue")
			self.wndAnim = self.GetChild("SearchAnim")
			self.btnFilter = self.GetChild("FilterButton")
			self.ScrollBar = self.GetChild("Scrollbar")
		except:
			import exception
			exception.Abort("shopsearch.__LoadWindow.BindObject")
		
		self.AppendCategories()
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.SearchButton.SetEvent(ui.__mem_func__(self.OnSearchItem))
		self.ScrollBar.Hide()

		self.wndAnim.SetEndFrameEvent(ui.__mem_func__(self.OnSearchItemReady))
		self.AnimBoard.Hide()
		self.wndAnim.Hide()
		for i in xrange(30):
			self.wndAnim.AppendImage("d:/ymir work/ui/shop/searching/shoploader_%d.dds" % int(i))	
		
		self.btnPrev = ui.MakeButton(self.board, 520, 410, False, "d:/ymir work/ui/privatesearch/", "private_prev_btn_01.sub", "private_prev_btn_02.sub", "private_prev_btn_01.sub")
		self.btnPrev.SetEvent(ui.__mem_func__(self.Prev))

		self.btnNext = ui.MakeButton(self.board, 670, 410, False, "d:/ymir work/ui/privatesearch/", "private_next_btn_01.sub", "private_next_btn_02.sub", "private_next_btn_01.sub")
		self.btnNext.SetEvent(ui.__mem_func__(self.Next))
		self.btnFilter.SetEvent(ui.__mem_func__(self.OnFilter))

	def OnFilter(self):
		if self.interface:
			self.interface.ManageFilterShopSearch()

	def AppendCategories(self):
		i = 0
		self.bCategory =  {}
		self.bIcon =  {}

		self.ListBox = ui.ListBoxEx()
		self.ListBox.SetParent(self.board)
		self.ListBox.SetParinte(self.board)
		self.ListBox.SetViewItemCount(14)
		self.ListBox.SetItemStep(20)
		self.ListBox.SetItemSize(100, 20)
		self.ListBox.SetPositionExtra(12, 120)
		self.ListBox.SetScrollBar(self.ScrollBar)

		for category in self.Categories:
			self.bCategory[i] = ui.MakeButton(self.board, 12, 20*i+120, False, "d:/ymir work/ui/shop/", "tab_01.png", "tab_02.png", "tab_03.png")
			self.bCategory[i].SetText(category["name"])
			self.bCategory[i].SetEvent(lambda index = i, categorie = category["type"]: self.SelectCategory(index, categorie))
			
			self.bIcon[i] = ui.MakeImageBox(self.bCategory[i], CATEGORY_SHOP_PATH + category["icon"], 5, 0)
			
			self.ListBox.AppendItem(self.bCategory[i], 1)
			i += 1
		
	def SelectCategory(self, index, category):
		for i in xrange(len(self.bCategory)):
			try:
				self.bCategory[i].SetUpVisual("d:/ymir work/ui/shop/tab_01.png")
				self.bCategory[i].SetOverVisual("d:/ymir work/ui/shop/tab_02.png")
				self.bCategory[i].SetUp()
			except KeyError:
				continue
			
		#Expand Sub-Category
		self.ListBox.RemoveAllItems()
		self.DeleteCategories()
		self.MakeAgain(index, False)
		self.SubCategory = 99
		
		self.bSubCategory =  {}
		self.bIconSubCategory =  {}

		i = 0
		if not self.IsExpanded(category):
			for subcat in self.SubCategoriesEquipments:
				if subcat["ExpandForType"] == category:
					self.ListExpanded[category] = True
					self.bSubCategory[i] = ui.MakeButton(self.board, 35, 20*i+30, False, "d:/ymir work/ui/shop/", "tab_01.png", "tab_02.png", "tab_03.png")
					self.bSubCategory[i].SetText(subcat["name"])
					self.bSubCategory[i].SetEvent(lambda index = i, categorie = subcat["type"]: self.SelectSubCategory(index, categorie))
					
					self.bIconSubCategory[i] = ui.MakeImageBox(self.bSubCategory[i], CATEGORY_SHOP_PATH + subcat["icon"], 5, 0)
				
					self.ListBox.AppendItem(self.bSubCategory[i], 1)
					i += 1
		else:
			try:
				del self.ListExpanded[category]
			except KeyError:
				pass
				
		self.MakeAgain(index, True)
			
		self.bCategory[index].SetUpVisual("d:/ymir work/ui/shop/tab_03.png")
		self.bCategory[index].SetOverVisual("d:/ymir work/ui/shop/tab_03.png")
		self.category = category
		
		# scroll-bar hide - show (manage)
		if self.ListBox.GetCount() <= 14:
			self.ScrollBar.Hide()
		else:
			self.ScrollBar.Show()
		
	def IsExpanded(self, category):
		try:
			if self.ListExpanded[category]:
				return True
		except KeyError:
			return False
		
		return False

	def SelectSubCategory(self, index, type):
		for i in xrange(len(self.bSubCategory)):
			try:
				self.bSubCategory[i].SetUpVisual("d:/ymir work/ui/shop/tab_01.png")
				self.bSubCategory[i].SetOverVisual("d:/ymir work/ui/shop/tab_02.png")
				self.bSubCategory[i].SetUp()
			except KeyError:
				continue
			
		self.SubCategory = type
		
	def DeleteCategories(self):
		for i in xrange(len(self.bCategory)):
			try:
				self.bCategory[i].Hide
				del self.bCategory[i]
			except KeyError:
				continue
		
	def MakeAgain(self, index, bCanDo):
		ip = 0
		for category in self.Categories:
			if ip > index and bCanDo == False:
				# ip += 1
				break
				
			if ip <= index and bCanDo == True:
				ip += 1
				continue

			self.bCategory[ip] = ui.MakeButton(self.board, 12, 20*ip+120, False, "d:/ymir work/ui/shop/", "tab_01.png", "tab_02.png", "tab_03.png")
			self.bCategory[ip].SetText(category["name"])
			self.bCategory[ip].SetEvent(lambda index = ip, categorie = category["type"]: self.SelectCategory(index, categorie))
			
			self.bIcon[ip] = ui.MakeImageBox(self.bCategory[ip], CATEGORY_SHOP_PATH + category["icon"], 5, 0)
			
			self.ListBox.AppendItem(self.bCategory[ip], 1)
			ip += 1
		
	def BindInterface(self, interface):
		self.interface = interface

	def DeleteLastPage(self):
		self.test_y = 0
		self.test_x = 0

		for i in xrange(self.MAX_ITEMS_PAGE):
			try:
				self.bItem[i].Hide()
			except KeyError:
				continue

	def SearchDone(self):
		if self.bDone == True:
			return

		self.Page(1)

	def Prev(self):
		if self.cPage == 1 or self.wndAnim.IsShow():
			return

		self.Page(self.cPage - 1)
		
		self.cLastPage = self.cPage

	def Next(self):
		Size = shop.GetSearchItemResultCount() - 1
		
		if self.cPage > Size / self.MAX_ITEMS_PAGE or self.wndAnim.IsShow():
			return

		# check if you can pass to next page; (If next page is empty, then stop at current page.)
		if Size < self.MAX_ITEMS_PAGE * self.cPage+1 - self.MAX_ITEMS_PAGE+1:
			return
			
		self.Page(self.cPage + 1)
		
		self.cLastPage = self.cPage

	def Page(self, page):
		Size = shop.GetSearchItemResultCount()
		
		if Size < 0:
			self.cPage = 1
			return

		# check if you can pass to next page; (If next page is empty, then stop at current page.)
		if Size < self.MAX_ITEMS_PAGE * page - self.MAX_ITEMS_PAGE+1:
			return

		self.DeleteLastPage()
		self.cPage = page
	
		for i in xrange(self.MAX_ITEMS_PAGE):
			iPoss = self.MAX_ITEMS_PAGE * page - self.MAX_ITEMS_PAGE + i
			
			if shop.GetSearchItemVnum(iPoss) < 1 or iPoss > Size-1:
				continue

			Vid = shop.GetSearchItemShopVID(iPoss)
			iPos = shop.GetSearchItemPos(iPoss)
			NameOwner = shop.GetSearchItemOwnerName(iPoss)
			iPrice = shop.GetSearchItemGold(iPoss)
			iVnum = shop.GetSearchItemVnum(iPoss)
			iCount = shop.GetSearchItemCount(iPoss)
			iPriceCheque = shop.GetSearchItemCheque(iPoss)
			Trans = shop.GetSearchItemTransmutation(iPoss)
			
			self.bItem[i] = ui.ImageBox()
			self.bItem[i].SetParent(self.bSearch)
			self.bItem[i].LoadImage("d:/ymir work/ui/shop/search_bg.png")
			self.bItem[i].SetPosition(self.pos_x[self.test_x], self.pos_y[self.test_y])
			self.bItem[i].Show()

			item.SelectItem(iVnum)
			d, size = item.GetItemSize()

			self.bGrid[i] = ui.MakeGridSlot(self.bItem[i], 7, 0, iVnum, iCount, size, True)
			self.bGrid[i].SetOverInItemEvent(lambda slotindex = 0, position = iPoss: self.OverInItem(slotindex, position))
			self.bGrid[i].SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.bGrid[i].SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)

			if Trans:
				self.bGrid[i].DisableCoverButton(0)
			else:
				self.bGrid[i].EnableCoverButton(0)
	
			self.btnBuy[i] = ui.MakeButton(self.bItem[i], 7, 87, False, "d:/ymir work/ui/shop/", "small_btn.dds", "small_btn_over.dds", "small_btn_down.dds")
			self.btnBuy[i].SetEvent(lambda pVid = Vid, pItem = iPos: self.BuyItem(pVid, pItem))
			self.btnBuy[i].SetText("Cumpãrã")
			self.btnBuy[i].SetWindowHorizontalAlignCenter()
	
			self.btnWhisper[i] = ui.MakeButton(self.bItem[i], 20, 5, False, "d:/ymir work/ui/shop/", "message.dds", "message_hover.dds", "message_pressed.dds")
			self.btnWhisper[i].SetWindowHorizontalAlignRight()
			self.btnWhisper[i].SetWindowVerticalAlignTop()
			self.btnWhisper[i].SetEvent(lambda szName = NameOwner: self.WhisperFunc(szName))

			if iVnum == 50300 or iVnum == 70037:
				name = self.__GetSkillBookName(iPoss, iVnum)
			else:
				name = item.GetItemName()

			self.wndNameItem[i] = ui.MakeText(self.bItem[i], "|cFFF4A460" + name, 7, 15)
			self.wndNameItem[i].SetWindowHorizontalAlignCenter()
			self.wndNameItem[i].SetHorizontalAlignCenter()
	
			self.wndSeller[i] = ui.MakeText(self.bItem[i], "Vânzãtor: " + NameOwner, 7, 35)
			self.wndSeller[i].SetWindowHorizontalAlignCenter()
			self.wndSeller[i].SetHorizontalAlignCenter()

			self.wndQuantity[i] = ui.MakeText(self.bItem[i], "Cantitate: x" + str(iCount), 7, 50)
			self.wndQuantity[i].SetWindowHorizontalAlignCenter()
			self.wndQuantity[i].SetHorizontalAlignCenter()
	
			self.wndPrice[i] = ui.MakeText(self.bItem[i], "|cFFF4A460Preþ: " + localeInfo.MoneyFormat(iPrice), 7, 65)
			self.wndPrice[i].SetWindowHorizontalAlignCenter()
			self.wndPrice[i].SetHorizontalAlignCenter()
			
			self.wndPriceCheque[i] = ui.MakeText(self.bItem[i], "|cFFF4A460Won: " + str(iPriceCheque), 7, 75)
			self.wndPriceCheque[i].SetWindowHorizontalAlignCenter()
			self.wndPriceCheque[i].SetHorizontalAlignCenter()
			
			# REPOSITION
			self.test_y += 1
			self.test_x += 1
			
			if self.test_x >= len(self.pos_x):
				self.test_x = 0
			
			if self.test_y >= len(self.pos_y):
				self.test_y = 0
			# REPOSITION
			
		self.bDone = True

	def BuyItem(self, iVid, iPos):
		dlgQuestion = uiCommon.QuestionDialog()
		dlgQuestion.SetText(localeInfo.CHECKSEARCH)
		dlgQuestion.SetAcceptEvent(lambda vid = iVid, pos = iPos: self.AcceptPurchase(iVid, iPos))
		dlgQuestion.SetCancelEvent(ui.__mem_func__(dlgQuestion.Close))
		dlgQuestion.Open()
		self.dlgQuestion = dlgQuestion

	def AcceptPurchase(self, vid, pos):
		net.SendShopSerchBuyItem(vid, pos)
		self.dlgQuestion.Close()

	def BuyItemDone(self):
		self.OnSearchItem()

	def __GetSkillBookName(self, pos, iVnum):
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(shop.GetSearchItemMetinSocket(pos, i))

		skillName = skill.GetSkillName(metinSlot[0])

		if not skillName:
			return "NO_NAME_BOOK"
		
		itemName = "NO_NAME_BOOK"
		
		if 50300 == iVnum:
			itemName = skillName + " " + localeInfo.TOOLTIP_SKILLBOOK_NAME
		elif 70037 == iVnum:
			itemName = skillName + " " + localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME
		
		return itemName

	def OnSearchItem(self, bExecept = False):
		if self.wndAnim.IsShow():
			return
			
		self.bDone = False
			
		if bExecept == False:
			self.cPage = 1
			self.cLastPage = 1

		self.DeleteLastPage()
		shop.SearchItemDataClear()

		name = self.sItemName.GetText()
		isNameOnly = (len(name) != 0)
		net.SendShopSearchInfo(self.category, self.SubCategory, self.interface.GetMinPriceShopSearch(), self.interface.GetMaxPriceShopSearch(), self.interface.GetMinChequeShopSearch(), self.interface.GetMaxChequeShopSearch(), name, isNameOnly)

		self.AnimBoard.Show()
		self.wndAnim.SetPosition(240, 170)
		self.wndAnim.ResetFrame()
		self.wndAnim.Show()
		
	def OnSearchItemReady(self):
		self.cPage = self.cLastPage
		if self.cPage != 1:
			# Check Size Shop
			Size = shop.GetSearchItemResultCount() - 1
			if Size < self.MAX_ITEMS_PAGE * self.cPage - self.MAX_ITEMS_PAGE+1:
				if self.cPage > 1:
					self.cPage -= 1
				else:
					self.cPage = 1
			# Check Size Shop
			self.Page(self.cPage)
		else:
			self.Page(1)

		self.AnimBoard.Hide()
		self.wndAnim.Hide()

	def WhisperFunc(self, name):
		if self.interface:
			self.interface.OpenWhisperDialog(name)

	def OverInItem(self, none, pos):
		iPos = shop.GetSearchItemPos(pos)
		NameOwner = shop.GetSearchItemOwnerName(pos)
		iPrice = shop.GetSearchItemGold(pos)
		iVnum = shop.GetSearchItemVnum(pos)
		iCount = shop.GetSearchItemCount(pos)
		iPriceCheque = shop.GetSearchItemCheque(pos)
		Trans = shop.GetSearchItemTransmutation(pos)

		item.SelectItem(iVnum)

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(shop.GetSearchItemMetinSocket(pos, i))

		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(shop.GetSearchItemAttribute(pos, i))

		if self.tooltip:
			self.tooltip.ClearToolTip()
			self.tooltip.AddItemData(iVnum, metinSlot, attrSlot, 0, 0, player.INVENTORY, -1, Trans)
			self.tooltip.AppendSellingPrice(iPrice)
			self.tooltip.AppendSellingChequePrice(iPriceCheque)
			self.tooltip.AppendSpace(5)
			self.tooltip.AppendTextLine("Category: %s" % (self.GetCategoryByType(item.GetItemType())))
	
	def GetCategoryByType(self, type):
		self.ItemsTypes = [
			{"Type": item.ITEM_TYPE_WEAPON, "Category": "Weapons"},
			{"Type": item.ITEM_TYPE_ARMOR, "Category": "Equipments"},
		]

		for search in self.ItemsTypes:
			if search["Type"] == type:
				return search["Category"]
			
		return "All"
	
	def OverOutItem(self):
		if self.tooltip:
			self.tooltip.HideToolTip()

	def SetItemToolTip(self, tooltip):
		self.tooltip = tooltip

	def Close(self):
		if self.dlgQuestion:
			self.dlgQuestion.Close()
			
		if self.interface:
			self.interface.FilterShopSearchHide()
	
		self.OverOutItem()
		self.Hide()

	def Destroy(self):
		self.ClearDictionary()

	def OnPressEscapeKey(self):
		self.Close()
		return True	
		