import net
import player
import item
import app
import skill
import shop
import background
import ui
import uiScriptLocale
import uiToolTip
import constInfo
import localeInfo
import uiCommon

from _weakref import proxy
from itertools import islice
import math

class PrivateShopSearchDialog(ui.ScriptWindow):
	class SearchResultItem(ui.Window):
		def __init__(self, parent, index):
			ui.Window.__init__(self)
			
			self.parent = parent
			
			self.isLoad = True
			self.isSelected = False
			
			self.index = index
			
			self.itemID = 0
			self.itemVnum = 0
			self.shopVid = 0
			self.shopItemPos = 0
			self.metinSlot = 0
			self.attrSlot = 0
			self.effectID = 0
			self.priceGold = 0
			if app.ENABLE_CHEQUE_SYSTEM:
				self.priceCheque = 0
			if app.ENABLE_CHANGELOOK_SYSTEM:
				self.transmutation = 0
			self.SetParent(parent)
			self.InitItem()

		def InitItem(self):
			startX = 13
			yPos = 3
			
			self.itemImage = ui.MakeImageBoxPrivateShopSearch(self, "d:/ymir work/ui/tab_01.tga", 0, yPos+2)
			self.itemImage.SAFE_SetStringEvent("MOUSE_OVER_IN",self.__OverInItem)
			self.itemImage.SAFE_SetStringEvent("MOUSE_OVER_OUT",self.__OverOutItem)
			self.itemImage.SAFE_SetStringEvent("MOUSE_LEFT_UP",self.__OnSelect)
			self.itemImage.SetTop()
			self.itemImage.Show()
			
			self.text = ui.TextLine()
			self.text.SetParent(self)
			self.text.SetPosition(startX+67, yPos+4)
			self.text.SetHorizontalAlignCenter()
			self.text.Show()
			
			self.seller = ui.TextLine()
			self.seller.SetParent(self)
			self.seller.SetPosition(startX+207, yPos+4)
			self.seller.SetHorizontalAlignCenter()
			self.seller.Show()
			
			self.count = ui.TextLine()
			self.count.SetParent(self)
			self.count.SetPosition(startX+303, yPos+4)
			self.count.SetHorizontalAlignCenter()
			self.count.Show()

			self.priceGoldText = ui.TextLine()
			self.priceGoldText.SetParent(self)
			self.priceGoldText.SetPosition(startX+377, yPos+4)
			self.priceGoldText.SetHorizontalAlignCenter()
			self.priceGoldText.Show()

			if app.ENABLE_CHEQUE_SYSTEM:
				self.priceChequeText = ui.TextLine()
				self.priceChequeText.SetParent(self)
				self.priceChequeText.SetPosition(startX+460, yPos+4)
				self.priceChequeText.SetHorizontalAlignCenter()
				self.priceChequeText.Show()

			self.tooltipItem = uiToolTip.ItemToolTip()
			self.tooltipItem.Hide()
			
			self.SetSize(self.itemImage.GetWidth(), self.itemImage.GetHeight())
			
		def __OverOutItem(self):
			if not self.isSelected:
				self.itemImage.LoadImage("d:/ymir work/ui/tab_01.tga")
			
			if None != self.tooltipItem:
				self.tooltipItem.HideToolTip()
			
		def __OverInItem(self):
			if not self.isSelected:
				self.itemImage.LoadImage("d:/ymir work/ui/tab_02.tga")

			if None == self.tooltipItem:
				return

			self.tooltipItem.ClearToolTip()
			if app.ENABLE_CHANGELOOK_SYSTEM:
				self.tooltipItem.AddItemData(self.itemVnum, self.metinSlot, self.attrSlot, 0, 0, player.INVENTORY, -1, self.transmutation)
			else:
				self.tooltipItem.AddItemData(self.itemVnum, self.metinSlot, self.attrSlot)

			self.tooltipItem.ShowToolTip()

		def SetItemName(self, name):
			self.text.SetText(name)

		def SetCount(self, count):
			self.count.SetText(count)
		
		def SetPriceGold(self, price):
			self.priceGoldText.SetText(price)
			
		def SetPriceGoldInt(self, price):
			self.priceGold = price
		
		if app.ENABLE_CHEQUE_SYSTEM:
			def SetPriceCheque(self, price2):
				self.priceChequeText.SetText(price2)
				
			def SetPriceChequeInt(self, price):
				self.priceCheque = price
			
		def SetSeller(self, seller):
			self.seller.SetText(seller)
		
		def SetMetinSlot(self, metinSlot):
			self.metinSlot = metinSlot

		def SetAttrSlot(self, attrSLot):
			self.attrSlot = attrSLot
			
		def SetShopVid(self, vid):
			self.shopVid = vid

		def GetShopVid(self):
			return self.shopVid

		def SetItemVnum(self, vnum):
			self.itemVnum = vnum

		def GetShopItemPos(self):
			return self.shopItemPos
		
		def SetShopItemPos(self, itemPos):
			self.shopItemPos = itemPos

		if app.ENABLE_CHANGELOOK_SYSTEM:
			def SetTransmutation(self, vnum):
				self.transmutation = vnum
			
		def __OnSelect(self):
			self.parent.OnSearchResultItemSelect(self.index)

		def Select(self):
			self.isSelected = True
			self.isLoad = True

		def UnSelect(self):
			self.isSelected = False
			self.isLoad = True

		def OnUpdate(self):
			pass

		def OnRender(self):
			if self.isLoad:
				if self.isSelected:
					self.itemImage.LoadImage("d:/ymir work/ui/tab_02.tga")
				else:
					self.itemImage.LoadImage("d:/ymir work/ui/tab_01.tga")
				self.isLoad = False

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.jobs = (localeInfo.JOB_WARRIOR, localeInfo.JOB_ASSASSIN, localeInfo.JOB_SURA, localeInfo.JOB_SHAMAN)

		self.items = {
			item.ITEM_TYPE_WEAPON 		: localeInfo.PRIVATESHOPSEARCH_WEAPON,
			item.ITEM_TYPE_ARMOR		: localeInfo.PRIVATESHOPSEARCH_ARMOR,
			item.ITEM_TYPE_USE			: localeInfo.PRIVATESHOPSEARCH_USEITEM,
			item.ITEM_TYPE_MATERIAL		: localeInfo.PRIVATESHOPSEARCH_MATERIAL,
			item.ITEM_TYPE_METIN		: localeInfo.PRIVATESHOPSEARCH_METIN,
##			item.ITEM_TYPE_FISH			: localeInfo.PRIVATESHOPSEARCH_FISH,
			item.ITEM_TYPE_BELT			: localeInfo.PRIVATESHOPSEARCH_BELT,
##			item.ITEM_TYPE_RESOURCE		: localeInfo.PRIVATESHOPSEARCH_RESOURCE,
			item.ITEM_TYPE_ROD			: localeInfo.PRIVATESHOPSEARCH_ROD,
			item.ITEM_TYPE_UNIQUE		: localeInfo.PRIVATESHOPSEARCH_UNIQUE,
			item.ITEM_TYPE_SKILLBOOK	: localeInfo.PRIVATESHOPSEARCH_SKILLBOOK,
			item.ITEM_TYPE_QUEST		: localeInfo.PRIVATESHOPSEARCH_QUEST,
			item.ITEM_TYPE_TREASURE_BOX	: localeInfo.PRIVATESHOPSEARCH_TREASUREBOX,
			item.ITEM_TYPE_PICK			: localeInfo.PRIVATESHOPSEARCH_PICK,
			item.ITEM_TYPE_BLEND		: localeInfo.PRIVATESHOPSEARCH_BLEND,
			item.ITEM_TYPE_COSTUME		: localeInfo.PRIVATESHOPSEARCH_COSTUME,
##			item.ITEM_TYPE_DS			: localeInfo.PRIVATESHOPSEARCH_DS,
			item.ITEM_TYPE_SPECIAL		: localeInfo.PRIVATESHOPSEARCH_SPECIAL, 
		}

		self.subItemsWeapon = {
			item.WEAPON_SWORD		: localeInfo.PRIVATESHOPSEARCH_SWORD,
			item.WEAPON_TWO_HANDED	: localeInfo.PRIVATESHOPSEARCH_TWOSWORD
		}

		self.subItemsArmor = {
			item.ARMOR_BODY		: localeInfo.PRIVATESHOPSEARCH_BODY,
			item.ARMOR_HEAD		: localeInfo.PRIVATESHOPSEARCH_HEAD,
			item.ARMOR_SHIELD	: localeInfo.PRIVATESHOPSEARCH_SHIELD,
			item.ARMOR_WRIST	: localeInfo.PRIVATESHOPSEARCH_WRIST,
			item.ARMOR_FOOTS	: localeInfo.PRIVATESHOPSEARCH_FOOTS,
			item.ARMOR_NECK		: localeInfo.PRIVATESHOPSEARCH_NECK,
			item.ARMOR_EAR		: localeInfo.PRIVATESHOPSEARCH_EAR,
		}

		self.subItemsUse = {
			item.USE_POTION					: localeInfo.PRIVATESHOPSEARCH_POTION,
			item.USE_TUNING					: localeInfo.PRIVATESHOPSEARCH_TUNING,
			item.USE_ABILITY_UP				: localeInfo.PRIVATESHOPSEARCH_ABLITY_POTION,
			item.USE_POTION_NODELAY			: localeInfo.PRIVATESHOPSEARCH_NODELAY_POTION,
			item.USE_CLEAR					: localeInfo.PRIVATESHOPSEARCH_CLEAR_POTION,
			item.USE_DETACHMENT				: localeInfo.PRIVATESHOPSEARCH_DETACHMENT,
		}

		self.subItemsMaterial = {
			0	: localeInfo.PRIVATESHOPSEARCH_MATERIAL,
		}

		self.subItemsMetin = {
			0	: localeInfo.PRIVATESHOPSEARCH_METIN,
		}

##		self.subItemsFish = {
##			item.FISH_ALIVE	: localeInfo.PRIVATESHOPSEARCH_LIVE,
##			item.FISH_DEAD	: localeInfo.PRIVATESHOPSEARCH_DEAD,
##		}

		self.subItemsBelt = {
			0	: localeInfo.PRIVATESHOPSEARCH_BELT,
		}

##		self.subItemsResource = {
##			0							: localeInfo.PRIVATESHOPSEARCH_MATERIAL,
##			item.RESOURCE_STONE			: localeInfo.PRIVATESHOPSEARCH_STONE,
##			item.RESOURCE_BLOOD_PEARL	: localeInfo.PRIVATESHOPSEARCH_BLOOD_PEARL,
##			item.RESOURCE_BLUE_PEARL	: localeInfo.PRIVATESHOPSEARCH_BLUE_PEARL,
##			item.RESOURCE_WHITE_PEARL	: localeInfo.PRIVATESHOPSEARCH_WHITE_PEARL,
##			item.RESOURCE_CRYSTAL		: localeInfo.PRIVATESHOPSEARCH_CRYSTAL,
##			item.RESOURCE_GEM			: localeInfo.PRIVATESHOPSEARCH_GEM,
##			item.RESOURCE_METIN			: localeInfo.PRIVATESHOPSEARCH_METIN,
##			item.RESOURCE_ORE			: localeInfo.PRIVATESHOPSEARCH_ORE,
##		}

		self.subItemsRod = {
			0	: localeInfo.PRIVATESHOPSEARCH_ROD,
		}

		self.subItemsUnique = {
			0				: localeInfo.PRIVATESHOPSEARCH_UNIQUE,
		}

		self.subItemsSkillbook = {
			0	: localeInfo.PRIVATESHOPSEARCH_SKILLBOOK,
		}

		self.subItemsQuest = {
			0	: localeInfo.PRIVATESHOPSEARCH_QUEST,
		}

		self.subItemsTreasureBox = {
			0 : localeInfo.PRIVATESHOPSEARCH_TREASUREBOX,
		}

		self.subItemsPick = {
			0 : localeInfo.PRIVATESHOPSEARCH_PICK,
		}

		self.subItemsBlend = {
			0	: localeInfo.PRIVATESHOPSEARCH_BLEND,
		}

		self.subItemsCostume = {
			item.COSTUME_TYPE_BODY : localeInfo.PRIVATESHOPSEARCH_COSTUMEBODY,
			item.COSTUME_TYPE_HAIR : localeInfo.PRIVATESHOPSEARCH_COSTUMEHAIR,
			item.COSTUME_TYPE_ACCE : localeInfo.PRIVATESHOPSEARCH_COSTUME_ACCE,
			item.COSTUME_TYPE_WEAPON : localeInfo.PRIVATESHOPSEARCH_COSTUME_WEAPON,
		}

##		self.subItemsDS = {
##			item.DS_WHITE : localeInfo.PRIVATESHOPSEARCH_DS_WHITE,
##			item.DS_RED : localeInfo.PRIVATESHOPSEARCH_DS_RED,
##			item.DS_GREEN : localeInfo.PRIVATESHOPSEARCH_DS_GREEN,
##			item.DS_BLUE : localeInfo.PRIVATESHOPSEARCH_DS_BLUE,
##			item.DS_YELLOW : localeInfo.PRIVATESHOPSEARCH_DS_YELLOW,
##			item.DS_BLACK : localeInfo.PRIVATESHOPSEARCH_DS_BLACK,
##		}

		self.subItemsSpecial = {
				0 : localeInfo.PRIVATESHOPSEARCH_SPECIAL, 
		}

##		self.subItemsRing = {
##				0 : localeInfo.PRIVATESHOPSEARCH_RING, 
##		}

		self.itemToSubItem = {
			item.ITEM_TYPE_WEAPON 		: self.subItemsWeapon,
			item.ITEM_TYPE_ARMOR 		: self.subItemsArmor,
			item.ITEM_TYPE_USE			: self.subItemsUse,
			item.ITEM_TYPE_MATERIAL		: self.subItemsMaterial,
			item.ITEM_TYPE_METIN		: self.subItemsMetin,
##			item.ITEM_TYPE_FISH			: self.subItemsFish,
			item.ITEM_TYPE_BELT			: self.subItemsBelt,
##			item.ITEM_TYPE_RESOURCE		: self.subItemsResource,
			item.ITEM_TYPE_ROD			: self.subItemsRod,
			item.ITEM_TYPE_UNIQUE		: self.subItemsUnique,
			item.ITEM_TYPE_SKILLBOOK	: self.subItemsSkillbook,
			item.ITEM_TYPE_QUEST		: self.subItemsQuest,
			item.ITEM_TYPE_TREASURE_BOX	: self.subItemsTreasureBox,
			item.ITEM_TYPE_PICK			: self.subItemsPick,
			item.ITEM_TYPE_BLEND		: self.subItemsBlend,
			item.ITEM_TYPE_COSTUME		: self.subItemsCostume,
###			item.ITEM_TYPE_RING			: self.subItemsRing,
###			item.ITEM_TYPE_DS			: self.subItemsDS,
			item.ITEM_TYPE_SPECIAL		: self.subItemsSpecial,
		}

		self.subItems = self.subItemsWeapon
		self.selectedItemIndex = -1
		self.board = None
		self.minLevel = None
		self.maxLevel = None
		self.minRefine = None
		self.maxRefine = None
		self.minPrice = None
		self.maxPrice = None

		if app.ENABLE_CHEQUE_SYSTEM:
			self.minCheque = None
			self.maxCheque = None

		self.itemNameSearch = None
		self.searchResultItems = []
		self.currentItemCat = item.ITEM_TYPE_WEAPON
		self.currentSubItemCat = item.WEAPON_SWORD
		self.currentJob = 0
		self.itemDataList = []

		self.currentPage = 1
		self.pageCount = 1
		self.perPage = 10
		self.itemCount = 0

		self.LoadWindow()

		self.subItemChoose.SelectItem(0)
		self.itemChoose.SelectItem(0)
		self.jobChoose.SelectItem(0)

	def __del__(self):
		self.Destroy()
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/PrivateShopSearchDialog.py")
		except:
			import exception
			exception.Abort("PrivateShopSearchDialog.LoadDialog.LoadScript")

		try:
			GetObject=self.GetChild
			self.board = GetObject("board")
			self.minLevel = GetObject("minLevelValue")
			self.maxLevel = GetObject("maxLevelValue")
			self.minRefine = GetObject("minrefineValue")
			self.maxRefine = GetObject("maxrefineValue")
			self.minPrice = GetObject("GoldminValue")
			self.maxPrice = GetObject("GoldmaxValue")
			self.minCheque = GetObject("ChequeminValue")
			self.maxCheque = GetObject("ChequemaxValue")
			self.itemNameSearch = GetObject("ItemNameValue")
			
			self.pageButtons = []
			self.pageButtons.append(GetObject("page1_button"))
			self.pageButtons.append(GetObject("page2_button"))
			self.pageButtons.append(GetObject("page3_button"))
			self.pageButtons.append(GetObject("page4_button"))
			self.pageButtons.append(GetObject("page5_button"))

			self.pageButtons[0].Show()
			self.pageButtons[1].Hide()
			self.pageButtons[2].Hide()
			self.pageButtons[3].Hide()
			self.pageButtons[4].Hide()
			self.pageButtons[0].Down()
			self.pageButtons[0].Disable()

			self.searchButton = GetObject("SearchButton")
			self.searchButton.SetEvent(ui.__mem_func__(self.StartSearch))

			self.buyButton = GetObject("BuyButton")
			self.buyButton.SetEvent(ui.__mem_func__(self.BuySelectedItem))

			
			self.nextButton = GetObject("next_button")
			self.lastButton = GetObject("last_next_button")
			self.prevButton = GetObject("prev_button")
			self.firstButton = GetObject("first_prev_button")
			
			self.nextButton.SetEvent(ui.__mem_func__(self.NextPage))
			self.prevButton.SetEvent(ui.__mem_func__(self.PrevPage))
			self.firstButton.SetEvent(ui.__mem_func__(self.FirstPage))
			self.lastButton.SetEvent(ui.__mem_func__(self.LastPage))
			
			self.board.SetCloseEvent(ui.__mem_func__(self.__OnCloseButtonClick))

			self.subItemChoose = ui.ComboBoxImage(self, "d:/ymir work/ui/privatesearch/private_leftSlotImg.sub",12,115)
			self.subItemChoose.SetCurrentItem(self.subItems.itervalues().next())
			
			for index, data in self.subItems.iteritems():
				self.subItemChoose.InsertItem(index, data)

			self.subItemChoose.SetEvent(lambda subItemNumber, argSelf=proxy(self): argSelf.OnChangeSubItemChange(subItemNumber))

			self.subItemChoose.Show()

			self.itemChoose = ui.ComboBoxImage(self, "d:/ymir work/ui/privatesearch/private_leftSlotImg.sub",12,95)
			self.itemChoose.SetCurrentItem(self.items.itervalues().next())

			for index, data in self.items.iteritems():
				self.itemChoose.InsertItem(index, data)

			self.itemChoose.SetEvent(lambda itemNumber, argSelf=proxy(self): argSelf.OnChangeItemChange(itemNumber))
			self.itemChoose.Show()

			self.jobChoose = ui.ComboBoxImage(self, "d:/ymir work/ui/privatesearch/private_leftSlotImg.sub",12,55)
			self.jobChoose.SetCurrentItem(self.jobs[0])
			
			for index, data in enumerate(self.jobs):
				self.jobChoose.InsertItem(index, data)

			self.jobChoose.SetEvent(lambda jobNumber, argSelf=proxy(self): argSelf.OnChangeJobChange(jobNumber))
			self.jobChoose.Show()

			self.Children.append(self.subItemChoose)
			self.Children.append(self.itemChoose)
			self.Children.append(self.jobChoose)
		except:
			import exception
			exception.Abort("PrivateShopSearchDialog.LoadDialog.BindObject")

	def Destroy(self):
		self.ClearDictionary()
		self.searchResultItems[:] = [] 
		self.titleBar = None

	def Open(self, type):
		if type == 0:
			self.buyButton.Hide()
		else:
			self.buyButton.Show()
		self.RefreshMe()
		self.Show()
		self.SetCenterPosition()

	def RefreshListBoxes(self):
		self.subItemChoose.ClearItem()

		if self.currentItemCat == item.ITEM_TYPE_WEAPON:
			if self.currentJob == 0:
				self.subItems = { item.WEAPON_SWORD : localeInfo.PRIVATESHOPSEARCH_SWORD, item.WEAPON_TWO_HANDED : localeInfo.PRIVATESHOPSEARCH_TWOSWORD}
		
			elif self.currentJob == 1:
				self.subItems = { 
								item.WEAPON_SWORD : localeInfo.PRIVATESHOPSEARCH_SWORD,
								item.WEAPON_DAGGER : localeInfo.PRIVATESHOPSEARCH_DAGGER,
								item.WEAPON_BOW : localeInfo.PRIVATESHOPSEARCH_BOW,
								item.WEAPON_ARROW : localeInfo.PRIVATESHOPSEARCH_ARROW,
								}
			elif self.currentJob == 2:
				self.subItems = { item.WEAPON_SWORD : localeInfo.PRIVATESHOPSEARCH_SWORD, }
			elif self.currentJob == 3:
				self.subItems = { 
								item.WEAPON_BELL : localeInfo.PRIVATESHOPSEARCH_BELL,
								item.WEAPON_FAN : localeInfo.PRIVATESHOPSEARCH_FAN,
								}
		else:
			self.subItems = self.itemToSubItem[self.currentItemCat]

		for index, data in self.subItems.iteritems():
			self.subItemChoose.InsertItem(index, data)
		
		self.subItemChoose.SetCurrentItem(self.subItems.itervalues().next())
		self.subItemChoose.SelectItem(0)

	def RefreshMe(self):
		background.DeletePrivateShopPos()
		self.itemDataList[:] = []
		self.searchResultItems[:] = []
		self.itemCount = shop.GetSearchItemResultCount()

		for idx in xrange(shop.GetSearchItemResultCount()):
			shopVID = shop.GetSearchItemShopVID(idx)
			ownerName = shop.GetSearchItemOwnerName(idx)
			itemPos = shop.GetSearchItemPos(idx)
			priceGold = shop.GetSearchItemGold(idx)
			itemVnum = shop.GetSearchItemVnum(idx)
			itemCount = shop.GetSearchItemCount(idx)

			metinSlot = []
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(shop.GetSearchItemMetinSocket(idx, i))

			attrSlot = []
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(shop.GetSearchItemAttribute(idx, i))

			if app.ENABLE_CHEQUE_SYSTEM:
				priceCheque = shop.GetSearchItemCheque(idx)

			if app.ENABLE_CHANGELOOK_SYSTEM:
				transmutation = shop.GetSearchItemTransmutation(idx)

			if app.ENABLE_CHEQUE_SYSTEM and app.ENABLE_CHANGELOOK_SYSTEM:
				self.itemDataList.append((itemVnum, itemCount, priceGold, priceCheque, ownerName, metinSlot, attrSlot, itemPos, shopVID, transmutation))
			elif app.ENABLE_CHEQUE_SYSTEM and not app.ENABLE_CHANGELOOK_SYSTEM:
				self.itemDataList.append((itemVnum, itemCount, priceGold, priceCheque, ownerName, metinSlot, attrSlot, itemPos, shopVID))
			elif not app.ENABLE_CHEQUE_SYSTEM and app.ENABLE_CHANGELOOK_SYSTEM:
				self.itemDataList.append((itemVnum, itemCount, priceGold, ownerName, metinSlot, attrSlot, itemPos, shopVID, transmutation))
			else:
				self.itemDataList.append((itemVnum, itemCount, priceGold, ownerName, metinSlot, attrSlot, itemPos, shopVID))

		self.pageCount = int(math.ceil(float(self.itemCount) / float(self.perPage)))
		self.currentPaginationPage = 1
		self.paginationPageCount = int(math.ceil(float(self.pageCount) / 5.0 ))
		
		self.FirstPage()
	
	def RefreshList(self):
		background.DeletePrivateShopPos()
		self.selectedItemIndex = -1
		self.RefreshPaginationButtons()
		self.searchResultItems[:] = []

		start = (self.currentPage - 1) * self.perPage
		end = ((self.currentPage - 1) * self.perPage) + self.perPage

		currentPageDict = self.itemDataList[start:end]

		basePos = 58
		for idx, data in enumerate(currentPageDict):
			itemVnum = data[0]
			itemCount = data[1]
			priceGold = int(data[2])

			if app.ENABLE_CHEQUE_SYSTEM:
				priceCheque = int(data[3])

			ownerName = data[4]
			metinSlot = data[5]
			attrSlot = data[6]
			itemPos = data[7]
			shopVID = data[8]
			if app.ENABLE_CHANGELOOK_SYSTEM:
				transmutation = data[9]

			item.SelectItem(itemVnum)

			resultItem = PrivateShopSearchDialog.SearchResultItem(self, idx)
			resultItem.SetPosition(136, basePos)
			resultItem.SetItemVnum(itemVnum)
			resultItem.SetMetinSlot(metinSlot)
			resultItem.SetAttrSlot(attrSlot)

			if 50300 == itemVnum:
				skillIndex = metinSlot[0]
				skillName = skill.GetSkillName(skillIndex)
				if localeInfo.IsVIETNAM():
					itemName = item.GetItemName() + " " + skillName
				else:
					itemName = skillName + " " + str(item.GetItemName())
				resultItem.SetItemName(itemName)			
			else:
				resultItem.SetItemName(item.GetItemName())

			resultItem.SetSeller(ownerName)
			resultItem.SetCount(str(itemCount))
			resultItem.SetPriceGold(localeInfo.NumberToString(priceGold))
			resultItem.SetPriceGoldInt(priceGold)

			if app.ENABLE_CHEQUE_SYSTEM:
				resultItem.SetPriceCheque(localeInfo.NumberToString(priceCheque))
				resultItem.SetPriceChequeInt(priceCheque)

			resultItem.SetShopItemPos(itemPos)
			resultItem.SetShopVid(shopVID)
			resultItem.SetTransmutation(transmutation)
			resultItem.Show()
			self.searchResultItems.append(resultItem)

			basePos += 25

	def RefreshPaginationButtons(self):
		self.currentPaginationPage = int(math.ceil(float(self.currentPage) / 5.0 ))
		self.shownPages = min(self.pageCount - (5 * (self.currentPaginationPage - 1)), 5)

		for x in xrange(5):
			currentPage = (x + ((self.currentPaginationPage-1) * 5) + 1)
			self.pageButtons[x].SetUp()
			self.pageButtons[x].SetText("%d" % currentPage)
			self.pageButtons[x].SetEvent(lambda arg=currentPage: self.GotoPage(arg))
		
		map(ui.Button.Hide, self.pageButtons)
		map(ui.Button.Enable, self.pageButtons)
		
		for x in xrange(self.shownPages):
			self.pageButtons[x].Show()

		self.pageButtons[(self.currentPage - ((self.currentPaginationPage - 1) * 5)) - 1].Down()
		self.pageButtons[(self.currentPage - ((self.currentPaginationPage - 1) * 5)) - 1].Disable()
	
	def GotoPage(self, page):
		self.currentPage = page
		self.RefreshList()

	def FirstPage(self):
		self.currentPage = 1
		self.RefreshList()
		
	def LastPage(self):
		self.currentPage = self.pageCount
		self.RefreshList()

	def NextPage(self):
		
		if self.currentPage < self.pageCount:
			self.currentPage += 1

		self.RefreshList()
			
	def PrevPage(self):
	
		if self.currentPage > 1:
			self.currentPage -= 1
		
		self.RefreshList()
	
	def RefreshRequest(self):
		self.StartSearch()
		self.RefreshList()

	def StartSearch(self):
		shop.SearchItemDataClear()
		background.DeletePrivateShopPos()
		self.RefreshMe()
		job = self.currentJob
		itemType = self.currentItemCat
		itemSubType = self.currentSubItemCat
		minLevel = int(self.minLevel.GetText())
		maxLevel = int(self.maxLevel.GetText())
		minRefine = int(self.minRefine.GetText())
		maxRefine = int(self.maxRefine.GetText())
		minGold = int(self.minPrice.GetText())
		maxGold = int(self.maxPrice.GetText())

		if app.ENABLE_CHEQUE_SYSTEM:
			minCheque = int(self.minCheque.GetText())
			maxCheque = int(self.maxCheque.GetText())

		itemName = self.itemNameSearch.GetText()
		isNameOnly = (len(itemName) != 0)

		if app.ENABLE_CHEQUE_SYSTEM:
			net.SendShopSearchInfo(job, itemType, itemSubType, minLevel, maxLevel, minRefine, maxRefine, minGold, maxGold, minCheque, maxCheque, itemName, isNameOnly)
		else:
			net.SendShopSearchInfo(job, itemType, itemSubType, minLevel, maxLevel, minRefine, maxRefine, minGold, maxGold, itemName, isNameOnly)

		self.Children.append(self.searchResultItems)

	def BuySelectedItem(self):
		if self.selectedItemIndex == -1:
			return

		dlgQuestion = uiCommon.QuestionDialog()
		dlgQuestion.SetText(localeInfo.CHECKSEARCH)
		dlgQuestion.SetAcceptEvent(ui.__mem_func__(self.AcceptPurchase))
		dlgQuestion.SetCancelEvent(ui.__mem_func__(dlgQuestion.Close))
		dlgQuestion.Open()
		self.dlgQuestion = dlgQuestion
		
	def AcceptPurchase(self):
		if self.selectedItemIndex == -1:
			return

		shopVid = self.searchResultItems[self.selectedItemIndex].GetShopVid()
		itemPos = self.searchResultItems[self.selectedItemIndex].GetShopItemPos()
		net.SendShopSerchBuyItem(shopVid, itemPos)
		self.dlgQuestion.Close()

	def OnChangeJobChange(self, jobNumber):
		self.currentJob = jobNumber
		self.jobChoose.SetCurrentItem(self.jobs[jobNumber])
		self.itemChoose.CloseListBox()
		self.subItemChoose.CloseListBox()

		self.RefreshListBoxes()
	
	def OnChangeSubItemChange(self, subItemNumber):
		self.currentSubItemCat = subItemNumber
		self.itemChoose.CloseListBox()
		self.jobChoose.CloseListBox()
		self.subItemChoose.SetCurrentItem(self.subItems[subItemNumber])

	def OnChangeItemChange(self, itemNumber):
		self.currentItemCat = itemNumber
		self.itemChoose.SetCurrentItem(self.items[itemNumber])

		self.subItemChoose.CloseListBox()
		self.jobChoose.CloseListBox()
		self.RefreshListBoxes()

	def OnSearchResultItemSelect(self, index):
		map(PrivateShopSearchDialog.SearchResultItem.UnSelect,  self.searchResultItems)
		background.DeletePrivateShopPos()
		import dbg
		dbg.TraceError("OnSearchResultItemSelect %u" % index)
		self.selectedItemIndex = index
		self.searchResultItems[self.selectedItemIndex].Select()
		shopVid = self.searchResultItems[self.selectedItemIndex].GetShopVid()
		itemPos = self.searchResultItems[self.selectedItemIndex].GetShopItemPos()
		constInfo.MARKED_SHOP_VID = shopVid
		background.CreatePrivateShopPos(shopVid)

	def Close(self):
		background.DeletePrivateShopPos()
		map(PrivateShopSearchDialog.SearchResultItem.Hide, self.searchResultItems)
		self.Hide()

	def SetItemToolTip(self, itemTooltip):
		self.tooltipItem = itemTooltip

	def __ShowToolTip(self, slotIndex):
		if self.tooltipItem:
			self.tooltipItem.SetAcceWindowItem(slotIndex)

	def OverInItem(self, slotIndex):
		slotIndex = slotIndex
		self.wndItem.SetUsableItem(False)
		self.__ShowToolTip(slotIndex)

	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def Clear(self):
		self.Refresh()

	def Refresh(self):
		pass

	def __OnCloseButtonClick(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()

