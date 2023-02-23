##
## Interface
##
import constInfo
import systemSetting
import wndMgr
import chat
import app

import uiguildstorage
if app.ENABLE_NEW_FISHING_SYSTEM:
	import uifishing
if app.WORLD_BOSS_YUMA:
	import uiworldbosstext
if app.ENABLE_EVENT_MANAGER:
	import uiEventCalendar
if app.ENABLE_GUILD_ONLINE_LIST:
	import uiGuildList
if app.GUILD_RANK_SYSTEM:
	import uiGuildRanking
if app.__BL_RANKING__:
	import uiPlayerRanking
if app.ENABLE_RENEWAL_PVP:
	import uiPvP
import player
import uibattlepass
import uiTaskBar
import uiTaskBarSystem
import uiCharacter
import uiDungeonTimer
import uiInventory
import uiDragonSoul
import uiChat
import uiMessenger
import guild

if app.ENABLE_GUILD_REQUEST:
	import uiGuildRequest
if app.ENABLE_HUNTING_SYSTEM:
	import uiHunting
if app.ENABLE_DUNGEON_INFO_SYSTEM:
	import uiDungeonInfo
#import uibattlepass
import ui
import uiHelp
import uiWhisper
if app.__BL_SOUL_ROULETTE__:
	import uiMiniGameRoulette
if constInfo.ENABLE_AURA_SYSTEM:
	import uiaura
import uiPointReset
import uiShop
if app.ENABLE_MAINTENANCE_SYSTEM:
	import uiMaintenance
import bio_window
if app.BL_REMOTE_SHOP:
	import uiRemoteShop
import uiExchange
import uiSystem
import uiRestart
import uiToolTip
import uiMiniMap
import uiParty
import uiSafebox
import uiGuild
import uiQuest
if app.BL_MAILBOX:
	import uiMailBox
	import item
import uiPrivateShopBuilder
if app.ENABLE_OFFLINE_SHOP_SYSTEM:
	import uiOfflineShop
	import uiOfflineShopBuilder
if app.ENABLE_CHANGELOOK_SYSTEM:
	import uichangelook	
import uiCommon
import uiRefine
import uiEquipmentDialog
import uiGameButton
import uiTip
import uiCube
import miniMap
if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
	import uiPrivateShopSearch
# ACCESSORY_REFINE_ADD_METIN_STONE
import uiselectitem
# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE
import uiScriptLocale
if app.ENABLE_SWITCHBOT:
	import uiSwitchbot
import event
import localeInfo
import dbg
import grp
import net
import uifastequip
if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
	import uiSpecialStorage

	import uiInventoryMenu
IsQBHide = 0
if app.ENABLE_ACCE_COSTUME_SYSTEM:
	import uiacce
	
import uishopsearch

if app.WON_EXCHANGE:
	import uiWonExchange

if app.ENABLE_6_7_BONUS_NEW_SYSTEM:
	import uiSkillBookCombination
	import uiattr67adddialog

if app.ENABLE_DECORUM:
	import uiDecorum
	import chr
if app.ENABLE_ANTI_MULTIPLE_FARM:
	import uiAntiMultipleFarm
	import anti_multiple_farm
import uiitemfinder
if app.GUILD_WAR_COUNTER:
	import uiGuildWar
class Interface(object):
	CHARACTER_STATUS_TAB = 1
	CHARACTER_SKILL_TAB = 2

	def __init__(self):
		systemSetting.SetInterfaceHandler(self)
		if app.ENABLE_GUILD_REQUEST:
			self.wndGuildRequest = None
		self.windowOpenPosition = 0
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.onTopWindow = player.ON_TOP_WND_NONE
		self.wndDungeonTimer=None
		self.dlgWhisperWithoutTarget = None
		self.inputDialog = None
		self.tipBoard = None
		self.bigBoard = None
		self.missionBoard = None
		self.game = None
		if app.ENABLE_RENEWAL_PVP:
			self.wndPvP = None
		if app.ENABLE_GUILD_ONLINE_LIST:
			self.wndGuildList = None
		if app.__BL_SOUL_ROULETTE__:
			self.wndMiniGameRoulette = None

		# ITEM_MALL
		self.mallPageDlg = None
		# END_OF_ITEM_MALL
		if app.ENABLE_CUBE_RENEWAL_WORLDARD:
			self.wndCubeRenewal = None
		if app.ENABLE_EVENT_MANAGER:
			self.wndEventManager = None
			self.wndEventIcon = None
		self.wndWeb = None
		self.wndTaskBarS = None
		self.wndTaskBar = None
		if app.BL_REMOTE_SHOP:
			self.wndRemoteShop = None
		self.wndCharacter = None
		self.wndInventory = None
		self.wndBio = None
		self.wndExpandedTaskBar = None
		self.wndDragonSoul = None
		self.wndDragonSoulRefine = None
		self.wndChat = None
		self.wndMessenger = None
		self.wndMiniMap = None
		self.wndGuild = None
		if app.ENABLE_SHIP_DEFENSE:
			self.uiAllianceTargetBoard = None
		if app.GUILD_WAR_COUNTER:
			self.wndGuildWar = None
			self.wndGuildWarCSMsg = None
			self.wndGuildWarLog = None
		if constInfo.ENABLE_AURA_SYSTEM:
			self.auraUpgrade = None
			self.auraAbs = None
			self.auraEXP = None
		self.wndGuildBuilding = None
		if app.ENABLE_NEW_FISHING_SYSTEM:
			self.wndFishingWindow = None
		if app.ENABLE_ANTI_MULTIPLE_FARM:
			self.wndAntiMultipleFarm = None
		if app.ENABLE_MAINTENANCE_SYSTEM:
			self.wndMaintenance = None
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			self.wndDungeonInfo = None
		if constInfo.ENABLE_SHOW_CHEST_DROP:
			self.dlgChestDrop = None
		if app.ENABLE_6_7_BONUS_NEW_SYSTEM:
			self.wndSkillBookCombination = None
			self.wndAttr67Add = None
		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot = None
		if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
			self.wndSpecialStorage = None

			self.wndInventoryMenu = None
		
		self.wndCalendarButton = None
		self.wndCalendar = None
		if app.ENABLE_HUNTING_SYSTEM:
			self.wndHunting = None
			self.wndHuntingSelect = None
			self.wndHuntingReward = None	
			
		self.listGMName = {}
		self.wndQuestWindow = {}
		
		self.wndQuestWindowNewKey = 0
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}
		if app.BL_MAILBOX:
			self.mail_box = None
		# BEGIN_OFFLINE_SHOP
		self.offlineShopAdvertisementBoardDict = {}
		# END_OF_OFFLINE_SHOP		
		self.wndExpandedMoneyTaskBar = None	
		if app.WORLD_BOSS_YUMA:
			self.WorldbossHwnd = {}		
		event.SetInterfaceWindow(self)
		if app.ENABLE_DECORUM:
			self.wndDecorumSelf = None
			self.wndDecorumOther = None

	def __del__(self):
		systemSetting.DestroyInterfaceHandler()
		event.SetInterfaceWindow(None)
		
	def SetStream(self, stream):
		self.stream = stream
		
	

	################################
	## Make Windows & Dialogs
	def __MakeUICurtain(self):
		wndUICurtain = ui.Bar("TOP_MOST")
		wndUICurtain.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		wndUICurtain.SetColor(0x77000000)
		wndUICurtain.Hide()
		self.wndUICurtain = wndUICurtain

	def __MakeMessengerWindow(self):
		self.wndMessenger = uiMessenger.MessengerWindow()

		from _weakref import proxy
		self.wndMessenger.SetWhisperButtonEvent(lambda n,i=proxy(self):i.OpenWhisperDialog(n))
		self.wndMessenger.SetGuildButtonEvent(ui.__mem_func__(self.ToggleGuildWindow))

	def __MakeGuildWindow(self):
		self.wndGuild = uiGuild.GuildWindow()

	def __MakeChatWindow(self):

		wndChat = uiChat.ChatWindow()

		wndChat.SetSize(wndChat.CHAT_WINDOW_WIDTH, 0)
		wndChat.SetPosition(wndMgr.GetScreenWidth()/2 - wndChat.CHAT_WINDOW_WIDTH/2, wndMgr.GetScreenHeight() - wndChat.EDIT_LINE_HEIGHT - 37)
		wndChat.SetHeight(200)
		wndChat.Refresh()
		wndChat.Show()

		self.wndChat = wndChat
		self.wndChat.BindInterface(self)
		self.wndChat.SetSendWhisperEvent(ui.__mem_func__(self.OpenWhisperDialogWithoutTarget))
		self.wndChat.SetOpenChatLogEvent(ui.__mem_func__(self.ToggleChatLogWindow))	

	def __MakeTaskBarS(self):
		wndTaskBarS = uiTaskBarSystem.TaskBarS()
		wndTaskBarS.LoadWindow()
		self.wndTaskBarS = wndTaskBarS
		self.wndTaskBarS.BindInterface(self)
	def __MakeTaskBar(self):
		wndTaskBar = uiTaskBar.TaskBar()
		wndTaskBar.LoadWindow()
		self.wndTaskBar = wndTaskBar
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHARACTER, ui.__mem_func__(self.ToggleCharacterWindowStatusPage))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_INVENTORY, ui.__mem_func__(self.ToggleInventoryWindow))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_MESSENGER, ui.__mem_func__(self.ToggleMessenger))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_SYSTEM, ui.__mem_func__(self.ToggleSystemDialog))	
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_OFFLINESHOP, ui.__mem_func__(self.ToggleOfflineShopDialog))
		#self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_DSS, ui.__mem_func__(self.ToggleDragonSoulWindow))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_ANTI_MULTIPLE_FARM, ui.__mem_func__(self.ToggleAntiMultipleFarmWindow))
		#self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_ANTI_MULTIPLE_FARM_OLD, ui.__mem_func__(self.ToggleAntiMultipleFarmWindow))
		#self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_BATTLEPASS, ui.__mem_func__(self.ToggleBattlePassExtended))

		if uiTaskBar.TaskBar.IS_EXPANDED:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_EXPAND, ui.__mem_func__(self.ToggleExpandedButton))
			self.wndExpandedTaskBar = uiTaskBar.ExpandedTaskBar()
			self.wndExpandedTaskBar.LoadWindow()
			self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_DRAGON_SOUL, ui.__mem_func__(self.ToggleDragonSoulWindow))			
		else:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHAT, ui.__mem_func__(self.ToggleChat))

		self.wndEnergyBar = None
		import app
		if app.ENABLE_ENERGY_SYSTEM:
			wndEnergyBar = uiTaskBar.EnergyBar()
			wndEnergyBar.LoadWindow()
			self.wndEnergyBar = wndEnergyBar

		if app.BL_REMOTE_SHOP:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_REMOTE_SHOP, ui.__mem_func__(self.OpenRemoteShop))
		
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_EXPAND_MONEY, ui.__mem_func__(self.ToggleExpandedMoneyButton))
		self.wndExpandedMoneyTaskBar = uiTaskBar.ExpandedMoneyTaskBar()
		self.wndExpandedMoneyTaskBar.LoadWindow()
		self.wndExpandedMoneyTaskBar.BindInterface(self)
		if self.wndInventory:
			self.wndInventory.SetExpandedMoneyBar(self.wndExpandedMoneyTaskBar)

	def __MakeParty(self):
		wndParty = uiParty.PartyWindow()
		wndParty.Hide()
		self.wndParty = wndParty

	def __MakeGameButtonWindow(self):
		wndGameButton = uiGameButton.GameButtonWindow()
		wndGameButton.SetTop()
		wndGameButton.Show()
		wndGameButton.SetButtonEvent("STATUS", ui.__mem_func__(self.__OnClickStatusPlusButton))
		wndGameButton.SetButtonEvent("SKILL", ui.__mem_func__(self.__OnClickSkillPlusButton))
		wndGameButton.SetButtonEvent("QUEST", ui.__mem_func__(self.__OnClickQuestButton))
		wndGameButton.SetButtonEvent("HELP", ui.__mem_func__(self.__OnClickHelpButton))
		wndGameButton.SetButtonEvent("BUILD", ui.__mem_func__(self.__OnClickBuildButton))

		self.wndGameButton = wndGameButton

	def __IsChatOpen(self):
		return True

	def __MakeWindows(self):
		wndCharacter = uiCharacter.CharacterWindow()
		self.wndBio = bio_window.BioWindow()
		wndInventory = uiInventory.InventoryWindow(self)
		#wndInventory.BindInterfaceClass(self)
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			wndDragonSoul = uiDragonSoul.DragonSoulWindow()
			wndDragonSoul.BindInterfaceClass(self)
			wndDragonSoulRefine = uiDragonSoul.DragonSoulRefineWindow()
		else:
			wndDragonSoul = None
			wndDragonSoulRefine = None
			if app.BL_MAILBOX:
				wndDragonSoul.BindInterfaceClass(self)
		if app.WON_EXCHANGE:
			self.wndWonExchange = uiWonExchange.WonExchangeWindow()
			self.wndWonExchange.BindInterface(self)
		if app.ENABLE_DECORUM:
			self.wndDecorumSelf = uiDecorum.DecorumStat()			
		wndMiniMap = uiMiniMap.MiniMap()
		wndSafebox = uiSafebox.SafeboxWindow()
		if app.WJ_ENABLE_TRADABLE_ICON:
			wndSafebox.BindInterface(self)		
		#self.wndCalendarButton = ui.Button()
		#self.wndCalendarButton.SetEvent(ui.__mem_func__(self.OpenEventCalendar))
		#self.wndCalendarButton.SetToolTipText("Events")
		#self.wndCalendarButton.SetPosition(wndMgr.GetScreenWidth() - 80 - 136, 17)
		#self.wndCalendarButton.SetUpVisual("butoane/calendar1.tga")
		#self.wndCalendarButton.SetOverVisual("butoane/calendar2.tga")
		#self.wndCalendarButton.SetDownVisual("butoane/calendar1.tga")

		# ITEM_MALL
		wndMall = uiSafebox.MallWindow()
		self.wndMall = wndMall
		# END_OF_ITEM_MALL

		wndChatLog = uiChat.ChatLogWindow()
		if app.__BL_SOUL_ROULETTE__:
			self.wndMiniGameRoulette = uiMiniGameRoulette.RouletteWindow()
		wndChatLog.BindInterface(self)

		if app.BL_REMOTE_SHOP:
			self.wndRemoteShop = uiRemoteShop.RemoteShopDialog()

		self.wndCharacter = wndCharacter
		self.wndInventory = wndInventory
		self.wndDragonSoul = wndDragonSoul
		self.wndDragonSoulRefine = wndDragonSoulRefine
		self.wndMiniMap = wndMiniMap
		self.wndMiniMap.SetInterface(self)
		self.wndSafebox = wndSafebox
		self.wndChatLog = wndChatLog
		
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			self.wndDungeonInfo = uiDungeonInfo.DungeonInfoWindow()
			self.wndMiniMap.BindInterfaceClass(self)
		if app.GUILD_RANK_SYSTEM:
			self.wndGuildRanking = uiGuildRanking.GuildRankingDialog()
		if app.__BL_RANKING__:
			self.wndPlayerRanking = uiPlayerRanking.PlayerRankingDialog()
		if app.ENABLE_6_7_BONUS_NEW_SYSTEM:
			self.wndSkillBookCombination = uiSkillBookCombination.SkillBookCombinationWindow()
			self.wndSkillBookCombination.Open()
			self.wndAttr67Add = uiattr67adddialog.Attr67AddWindow()
			self.wndAttr67Add.Open()

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)
			self.wndDragonSoulRefine.SetInventoryWindows(self.wndInventory, self.wndDragonSoul)
			self.wndInventory.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)

		if app.ENABLE_NEW_FISHING_SYSTEM:
			self.wndFishingWindow = uifishing.FishingWindow()
		else:
			self.wndFishingWindow = None

		if app.BL_MAILBOX:
			self.mail_box = uiMailBox.MailBox()
			self.mail_box.BindInterface(self)
			self.mail_box.SetInven(self.wndInventory)
			self.mail_box.SetDSWindow(self.wndDragonSoul)

		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot = uiSwitchbot.SwitchbotWindow()
			
		if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
			self.wndSpecialStorage = uiSpecialStorage.SpecialStorageWindow()
			self.wndSpecialStorage.BindInterfaceClass(self)

			self.wndInventoryMenu = uiInventoryMenu.InventoryMenuWindow()
			self.wndInventoryMenu.BindInterfaceClass(self)

		if app.ENABLE_HUNTING_SYSTEM:
			self.wndHunting = uiHunting.HuntingWindow()
			self.wndHuntingSelect = uiHunting.HuntingSelectWindow()
			self.wndHuntingReward = uiHunting.HuntingRewardWindow()

	def __MakeDialogs(self):
		self.dlgExchange = uiExchange.ExchangeDialog()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgExchange.BindInterface(self)
			self.dlgExchange.SetInven(self.wndInventory)
			self.wndInventory.BindWindow(self.dlgExchange)
		self.dlgExchange.LoadDialog()
		self.dlgExchange.SetCenterPosition()
		self.dlgExchange.Hide()
		self.GuildStorageWindow = uiguildstorage.GuildStorage()
		self.GuildStorageWindow.Hide()
		self.dlgPointReset = uiPointReset.PointResetDialog()
		self.dlgPointReset.LoadDialog()
		self.dlgPointReset.Hide()

		self.dlgShop = uiShop.ShopDialog()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgShop.BindInterface(self)
		self.dlgShop.LoadDialog()
		self.dlgShop.Hide()
		# BEGIN_OFFLINE_SHOP
		self.dlgOfflineShop = uiOfflineShop.OfflineShopDialog()
		self.dlgOfflineShop.LoadDialog()
		self.dlgOfflineShop.Hide()
		# END_OF_OFFLINE_SHOP
		self.dlgRestart = uiRestart.RestartDialog()
		self.dlgRestart.LoadDialog()
		self.dlgRestart.Hide()

		self.dlgSystem = uiSystem.SystemDialog(self.stream)
		self.dlgSystem.LoadDialog()
		self.dlgSystem.SetOpenHelpWindowEvent(ui.__mem_func__(self.OpenHelpWindow))

		self.dlgSystem.Hide()

		self.dlgPassword = uiSafebox.PasswordDialog()
		self.dlgPassword.Hide()

		self.hyperlinkItemTooltip = uiToolTip.HyperlinkItemToolTip()
		self.hyperlinkItemTooltip.Hide()

		if app.ENABLE_DECORUM:
			self.hyperlinkArenaTooltip = uiToolTip.HyperlinkArenaToolTip()
			self.hyperlinkArenaTooltip.Hide()

		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.Hide()

		self.tooltipSkill = uiToolTip.SkillToolTip()
		self.tooltipSkill.Hide()

		if constInfo.ENABLE_AURA_SYSTEM:
			self.auraUpgrade = uiaura.AuraUpgrade()
			self.auraUpgrade.SetTooltip(self.tooltipItem)
			self.auraUpgrade.SetInterface(self)
			self.auraUpgrade.Hide()

			self.auraAbs = uiaura.AuraAbsorb()
			self.auraAbs.SetTooltip(self.tooltipItem)
			self.auraAbs.SetInterface(self)
			self.auraAbs.Hide()

			self.auraEXP = uiaura.AuraUpgrade(True)
			self.auraEXP.SetTooltip(self.tooltipItem)
			self.auraEXP.SetInterface(self)
			self.auraEXP.Hide()

		self.privateShopBuilder = uiPrivateShopBuilder.PrivateShopBuilder()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.privateShopBuilder.BindInterface(self)
			self.privateShopBuilder.SetInven(self.wndInventory)
			self.wndInventory.BindWindow(self.privateShopBuilder)
		self.privateShopBuilder.Hide()
		# BEGIN_OFFLINE_SHOP
		self.offlineShopBuilder = uiOfflineShopBuilder.OfflineShopBuilder()
		self.offlineShopBuilder.Hide()
	
		self.offlineShopEditMode = uiOfflineShop.OfflineShopEditMode()
		self.offlineShopEditMode.LoadDialog()
		self.offlineShopEditMode.Hide()
		
		# END_OF_OFFLINE_SHOP
		self.dlgRefineNew = uiRefine.RefineDialogNew()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgRefineNew.SetInven(self.wndInventory)
			self.wndInventory.BindWindow(self.dlgRefineNew)
		self.dlgRefineNew.Hide()


	if app.FAST_EQUIP_WORLDARD:
		def __MakeFastEquip(self):
			self.wndFastEquip = uifastequip.UiFastEquip()
			self.wndFastEquip.LoadWindow()
			self.wndFastEquip.Hide()

	def __MakeHelpWindow(self):
		self.wndHelp = uiHelp.HelpWindow()
		self.wndHelp.LoadDialog()
		self.wndHelp.SetCloseEvent(ui.__mem_func__(self.CloseHelpWindow))
		self.wndHelp.Hide()

	def __MakeTipBoard(self):
		self.tipBoard = uiTip.TipBoard()
		self.tipBoard.Hide()

		self.bigBoard = uiTip.BigBoard()
		self.bigBoard.Hide()
		self.missionBoard = uiTip.MissionBoard()
		self.missionBoard.Hide()

	def __MakeWebWindow(self):
		if constInfo.IN_GAME_SHOP_ENABLE:
			import uiWeb
			self.wndWeb = uiWeb.WebWindow()
			self.wndWeb.LoadWindow()
			self.wndWeb.Hide()

	if app.ENABLE_GUILD_ONLINE_LIST:
		def MakeGuildListWindow(self):
			if self.wndGuildList == None:
				self.wndGuildList = uiGuildList.GuildOnlineList()
		def GuildListRemove(self):
			self.MakeGuildListWindow()
			self.wndGuildList.ClearAllData()
		def GuildListSetData(self,guildID, guildName, masterOnline):
			self.MakeGuildListWindow()
			self.wndGuildList.SetData(guildID, guildName, masterOnline)
		def OpenGuildListWindow(self):
			self.MakeGuildListWindow()
			#if self.wndGuildList.IsShow():
			#	self.wndGuildList.Hide()
			#else:
			self.wndGuildList.Open()

	if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
		def __MakePrivateShopSearchWindow(self):
			self.wndPrivateShopSearch = uiPrivateShopSearch.PrivateShopSearchDialog()
			self.wndPrivateShopSearch.LoadWindow()
			self.wndPrivateShopSearch.Hide()

	if app.ENABLE_CHANGELOOK_SYSTEM:
		def __MakeChangeLookWindow(self):
			self.wndChangeLook = uichangelook.Window()
			self.wndChangeLook.LoadWindow()
			self.wndChangeLook.Hide()
			
			if self.wndInventory:
				self.wndInventory.SetChangeLookWindow(self.wndChangeLook)

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def __MakeAcceWindow(self):
			self.wndAcceCombine = uiacce.CombineWindow()
			self.wndAcceCombine.LoadWindow()
			self.wndAcceCombine.Hide()
			
			self.wndAcceAbsorption = uiacce.AbsorbWindow()
			self.wndAcceAbsorption.LoadWindow()
			self.wndAcceAbsorption.Hide()
			
			if self.wndInventory:
				self.wndInventory.SetAcceWindow(self.wndAcceCombine, self.wndAcceAbsorption)

	if app.ENABLE_ANTI_MULTIPLE_FARM:
		def __MakeAntiMultipleFarmWnd(self):
			self.wndAntiMultipleFarm = uiAntiMultipleFarm.AntiMultipleFarmWnd()
			self.wndAntiMultipleFarm.Hide()

	def __MakeCubeWindow(self):
		self.wndCube = uiCube.CubeWindow()
		self.wndCube.LoadWindow()
		self.wndCube.Hide()

	def __BoardShopSearch(self):
		self.wndShopSearch = uishopsearch.ShopSearch()
		self.wndShopSearch.LoadWindow()
		self.wndShopSearch.Hide()
		
		self.wndShopSearchFilter = uishopsearch.ShopSearchFilter()
		self.wndShopSearchFilter.MakeFilterWindow()
		self.wndShopSearchFilter.Hide()

	def __MakeItemFinder(self):
		self.wndItemFinder = uiitemfinder.ItemFinder()
		self.wndItemFinder.LoadWindow()
		self.wndItemFinder.Hide()

	def __MakeCubeResultWindow(self):
		self.wndCubeResult = uiCube.CubeResultWindow()
		self.wndCubeResult.LoadWindow()
		self.wndCubeResult.Hide()
	
	def __BoardBpass(self):
		self.wndbpass = uibattlepass.Battlepass()
		self.wndbpass.LoadWindow()
		self.wndbpass.Hide()		

	# ACCESSORY_REFINE_ADD_METIN_STONE
	def __MakeItemSelectWindow(self):
		self.wndItemSelect = uiselectitem.SelectItemWindow()
		self.wndItemSelect.Hide()
	# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE
	
	if app.ENABLE_CUBE_RENEWAL_WORLDARD:
		def __MakeCubeRenewal(self):
			import uicuberenewal
			self.wndCubeRenewal = uicuberenewal.CubeRenewalWindows()
			self.wndCubeRenewal.Hide()		

	def MakeInterface(self):
		self.__MakeMessengerWindow()
		self.__MakeGuildWindow()
		self.__MakeChatWindow()
		self.__MakeParty()
		self.__MakeWindows()
		self.__MakeDialogs()
		if app.ENABLE_ANTI_MULTIPLE_FARM:
			self.__MakeAntiMultipleFarmWnd()
		self.__MakeUICurtain()
		self.__MakeTaskBarS()
		self.__MakeTaskBar()
		self.__MakeGameButtonWindow()
		self.__MakeHelpWindow()
		self.__MakeTipBoard()
		self.__MakeWebWindow()
		# shop search
		self.__BoardShopSearch()
		self.wndShopSearch.BindInterface(self)
		# shop search
		if app.ENABLE_CUBE_RENEWAL_WORLDARD:
			self.__MakeCubeRenewal()
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.__MakeAcceWindow()
		if app.ENABLE_CHANGELOOK_SYSTEM:
			self.__MakeChangeLookWindow()			
		if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
			self.__MakePrivateShopSearchWindow()
		self.__MakeCubeWindow()
		self.__MakeCubeResultWindow()
		self.__MakeItemFinder()
		self.__BoardBpass()
		# ACCESSORY_REFINE_ADD_METIN_STONE
		if app.FAST_EQUIP_WORLDARD:
			self.__MakeFastEquip()
		self.__MakeItemSelectWindow()
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE
		if constInfo.ENABLE_SHOW_CHEST_DROP:
			self.MakeChestDrop()
		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}

		self.wndInventory.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.SetItemToolTip(self.tooltipItem)
			self.wndDragonSoulRefine.SetItemToolTip(self.tooltipItem)
		self.wndSafebox.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.wndAcceCombine.SetItemToolTip(self.tooltipItem)
			self.wndAcceAbsorption.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
			self.wndPrivateShopSearch.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_CHANGELOOK_SYSTEM:
			self.wndChangeLook.SetItemToolTip(self.tooltipItem)
		self.wndCube.SetItemToolTip(self.tooltipItem)
		self.wndCubeResult.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
			self.wndSpecialStorage.SetItemToolTip(self.tooltipItem)

		# ITEM_MALL
		self.wndMall.SetItemToolTip(self.tooltipItem)
		# END_OF_ITEM_MALL

		self.wndCharacter.SetSkillToolTip(self.tooltipSkill)
		self.wndTaskBar.SetItemToolTip(self.tooltipItem)
		self.wndTaskBar.SetSkillToolTip(self.tooltipSkill)
		self.wndGuild.SetSkillToolTip(self.tooltipSkill)

		# ACCESSORY_REFINE_ADD_METIN_STONE
		self.wndItemSelect.SetItemToolTip(self.tooltipItem)
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE
		
		self.wndbpass.SetItemToolTip(self.tooltipItem)

		self.wndItemFinder.SetItemToolTip(self.tooltipItem)
		self.dlgShop.SetItemToolTip(self.tooltipItem)
		self.dlgExchange.SetItemToolTip(self.tooltipItem)
		self.privateShopBuilder.SetItemToolTip(self.tooltipItem)
		if app.__BL_SOUL_ROULETTE__:
			self.wndMiniGameRoulette.SetItemToolTip(self.tooltipItem)
		# BEGIN_OFFLINE_SHOP
		self.dlgOfflineShop.SetItemToolTip(self.tooltipItem)
		self.offlineShopBuilder.SetItemToolTip(self.tooltipItem)
		self.offlineShopEditMode.SetItemToolTip(self.tooltipItem)
		# END_OF_OFFLINE_SHOP
		self.wndShopSearch.SetItemToolTip(self.tooltipItem)

		self.__InitWhisper()
		self.DRAGON_SOUL_IS_QUALIFIED = False

		if app.BL_MAILBOX:
			if self.mail_box:
				self.mail_box.SetItemToolTip(self.tooltipItem)

	def MakeHyperlinkTooltip(self, hyperlink):
		tokens = hyperlink.split(":")
		if tokens and len(tokens):
			type = tokens[0]
			if "item" == type:
				self.hyperlinkItemTooltip.SetHyperlinkItem(tokens)
			elif "link" == type:
				if tokens[1][:4] == "www.":
					webbrowser.open_new(tokens[1])
				elif tokens[1] == "http" or tokens[1] == "https":
					webbrowser.open_new(tokens[1]+":"+tokens[2])
			elif "Chitra" == type or "msg" == type and str(tokens[1]) != player.GetMainCharacterName():
				self.OpenWhisperDialog(str(tokens[1]))
			if app.ENABLE_DECORUM:
				if "arena" == type:
					if tokens[1] == "start":
						self.hyperlinkArenaTooltip.SetHyperlinkArenaStart(tokens)
					elif tokens[1] == "end":
						self.hyperlinkArenaTooltip.SetHyperlinkArenaEnd(tokens)				

	## Make Windows & Dialogs
	################################

	def Close(self):
		if app.ENABLE_GUILD_REQUEST:
			if self.wndGuildRequest:
				self.wndGuildRequest.Hide()
				self.wndGuildRequest.Destroy()
				self.wndGuildRequest = None
		if self.GuildStorageWindow:
			self.GuildStorageWindow.Destroy()
			del self.GuildStorageWindow
		if app.ENABLE_RENEWAL_PVP:
			if self.wndPvP:
				self.wndPvP.SaveData()
				self.wndPvP.Hide()
				self.wndPvP.Destroy()
				self.wndPvP = None
		if constInfo.ENABLE_SHOW_CHEST_DROP:
			if self.dlgChestDrop:
				self.dlgChestDrop.Destroy()
				self.dlgChestDrop=None
		if self.dlgWhisperWithoutTarget:
			self.dlgWhisperWithoutTarget.Destroy()
			del self.dlgWhisperWithoutTarget

		if self.wndDungeonTimer:
			self.wndDungeonTimer.Hide()
			self.wndDungeonTimer=0

		if uiQuest.QuestDialog.__dict__.has_key("QuestCurtain"):
			uiQuest.QuestDialog.QuestCurtain.Close()

		if self.wndQuestWindow:
			for key, eachQuestWindow in self.wndQuestWindow.items():
				eachQuestWindow.nextCurtainMode = -1
				eachQuestWindow.CloseSelf()
				eachQuestWindow = None
		self.wndQuestWindow = {}

		if app.ENABLE_ANTI_MULTIPLE_FARM:
			if self.wndAntiMultipleFarm:
				self.wndAntiMultipleFarm.Hide()
				self.wndAntiMultipleFarm.Destroy()
		
		if app.ENABLE_GUILD_ONLINE_LIST:
			if self.wndGuildList:
				self.wndGuildList.Hide()
				self.wndGuildList.Destroy()
				self.wndGuildList=None

		if app.WON_EXCHANGE:
			if self.wndWonExchange:
				self.wndWonExchange.Destroy()

		if app.GUILD_WAR_COUNTER:
			if self.wndGuildWar:
				self.wndGuildWar.Destroy()
				self.wndGuildWar.Hide()
				self.wndGuildWar = None
			if self.wndGuildWarCSMsg:
				self.wndGuildWarCSMsg.Destroy()
				self.wndGuildWarCSMsg.Hide()
				self.wndGuildWarCSMsg = None
			if self.wndGuildWarLog:
				self.wndGuildWarLog.Hide()
				self.wndGuildWarLog.Destroy()
				self.wndGuildWarLog = None
		if self.wndChat:
			self.wndChat.Destroy()

		if app.ENABLE_EVENT_MANAGER:
			if self.wndEventManager:
				self.wndEventManager.Hide()
				self.wndEventManager.Destroy()
				self.wndEventManager = None

			if self.wndEventIcon:
				self.wndEventIcon.Hide()
				self.wndEventIcon.Destroy()
				self.wndEventIcon = None

		if self.wndShopSearch:
			self.wndShopSearch.Hide()
			self.wndShopSearch.Destroy()

		if self.wndShopSearchFilter:
			self.wndShopSearchFilter.Destroy()

		if self.wndbpass:
			self.wndbpass.Destroy()

		if self.wndTaskBar:
			self.wndTaskBar.Destroy()

		if self.wndTaskBarS:
			self.wndTaskBarS.Destroy()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Destroy()

		if self.wndEnergyBar:
			self.wndEnergyBar.Destroy()

		if self.wndCharacter:
			self.wndCharacter.Destroy()

		if self.wndBio:
			self.wndBio.Destroy()

		if self.wndInventory:
			constInfo.hide_buttons = 1
			self.wndInventory.Destroy()
			
		if self.wndCalendar:
			self.wndCalendar.Close()

		if self.wndDragonSoul:
			self.wndDragonSoul.Hide()
			self.wndDragonSoul.Destroy()

		if self.wndDragonSoulRefine:
			self.wndDragonSoul.Hide()
			self.wndDragonSoulRefine.Destroy()
		if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
			if self.wndSpecialStorage:
				self.wndSpecialStorage.Destroy()

			if self.wndInventoryMenu:
				self.wndInventoryMenu.Destroy()

		if self.dlgExchange:
			self.dlgExchange.Destroy()

		if self.dlgPointReset:
			self.dlgPointReset.Destroy()

		if self.dlgShop:
			self.dlgShop.Destroy()

		if self.dlgRestart:
			self.dlgRestart.Destroy()

		if self.dlgSystem:
			self.dlgSystem.Destroy()

		if self.dlgPassword:
			self.dlgPassword.Destroy()

		if self.wndMiniMap:
			self.wndMiniMap.Destroy()

		if self.wndSafebox:
			self.wndSafebox.Destroy()

		if app.GUILD_RANK_SYSTEM:
			if self.wndGuildRanking:
				self.wndGuildRanking.Destory()

		if app.__BL_RANKING__:
			if self.wndPlayerRanking:
				self.wndPlayerRanking.Destory()
				
		if self.wndCalendarButton:
			self.wndCalendarButton.Destroy()

		if self.wndWeb:
			self.wndWeb.Destroy()
			self.wndWeb = None

		if self.wndMall:
			self.wndMall.Destroy()

		if self.wndParty:
			self.wndParty.Destroy()

		if self.wndHelp:
			self.wndHelp.Destroy()

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if self.wndAcceCombine:
				self.wndAcceCombine.Destroy()

		if app.ENABLE_CHANGELOOK_SYSTEM:
			if self.wndChangeLook:
				self.wndChangeLook.Destroy()

		if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch.Destroy()	
			
			if self.wndAcceAbsorption:
				self.wndAcceAbsorption.Destroy()

		if self.wndCube:
			self.wndCube.Destroy()

		if self.wndCubeResult:
			self.wndCubeResult.Destroy()

		if app.__BL_SOUL_ROULETTE__:
			if self.wndMiniGameRoulette:
				self.wndMiniGameRoulette.Destroy()
				del self.wndMiniGameRoulette

		if self.wndMessenger:
			self.wndMessenger.Destroy()

		if self.wndItemFinder:
			self.wndItemFinder.Destroy()

		if self.wndGuild:
			self.wndGuild.Destroy()
			
		if self.privateShopBuilder:
			self.privateShopBuilder.Destroy()

		if self.dlgRefineNew:
			self.dlgRefineNew.Destroy()

		if constInfo.ENABLE_AURA_SYSTEM:
			if self.auraUpgrade:
				self.auraUpgrade.Hide()
				self.auraUpgrade.Destroy()
			del self.auraUpgrade
			if self.auraAbs:
				self.auraAbs.Hide()
				self.auraAbs.Destroy()
			del self.auraAbs
            
			if self.auraEXP:
				self.auraEXP.Hide()
				self.auraEXP.Destroy()
			del self.auraEXP

		if self.wndGuildBuilding:
			self.wndGuildBuilding.Destroy()

		if self.wndGameButton:
			self.wndGameButton.Destroy()
		# ITEM_MALL
		if self.mallPageDlg:
			self.mallPageDlg.Destroy()

			if self.wndItemSelectEx:
				self.wndItemSelectEx.Destroy()

		if app.ENABLE_MAINTENANCE_SYSTEM:
			if self.wndMaintenance:
				self.wndMaintenance.Destroy()	
		# END_OF_ITEM_MALL

		if app.ENABLE_HUNTING_SYSTEM:
			if self.wndHunting:
				self.wndHunting.Destroy()
			if self.wndHuntingSelect:
				self.wndHuntingSelect.Destroy()
			if self.wndHuntingReward:
				self.wndHuntingReward.Destroy()

		# ACCESSORY_REFINE_ADD_METIN_STONE
		if self.wndItemSelect:
			self.wndItemSelect.Destroy()
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE
		
		if app.ENABLE_NEW_FISHING_SYSTEM:
			if self.wndFishingWindow:
				self.wndFishingWindow.Destroy()
				del self.wndFishingWindow		
		
		# BEGIN_OFFLINE_SHOP
		if self.dlgOfflineShop:
			self.dlgOfflineShop.Destroy()

		if self.offlineShopBuilder:
			self.offlineShopBuilder.Destroy()
			
		if self.offlineShopEditMode:
			self.offlineShopEditMode.Destroy()
		# END_OF_OFFLINE_SHOP	
		
		if app.ENABLE_SWITCHBOT:
			if self.wndSwitchbot:
				self.wndSwitchbot.Destroy()
		if self.wndExpandedMoneyTaskBar:
			self.wndExpandedMoneyTaskBar.Destroy()

		if app.ENABLE_DECORUM:
			if self.wndDecorumSelf:
				self.wndDecorumSelf.Hide()
				self.wndDecorumSelf.Destroy()
				
			if self.wndDecorumOther:
				self.wndDecorumOther.Hide()
				self.wndDecorumOther.Destroy()

		if app.ENABLE_CUBE_RENEWAL_WORLDARD:
			if self.wndCubeRenewal:
				self.wndCubeRenewal.Destroy()
				self.wndCubeRenewal.Close()
				
		if app.ENABLE_6_7_BONUS_NEW_SYSTEM:
			if self.wndSkillBookCombination:
				self.wndSkillBookCombination.Destroy()
				self.wndSkillBookCombination.Close()
				del self.wndSkillBookCombination

			if self.wndAttr67Add:
				self.wndAttr67Add.Destroy()
				self.wndAttr67Add.Close()
				del self.wndAttr67Add
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			if self.wndDungeonInfo:
				self.wndDungeonInfo.Destroy()
				del self.wndDungeonInfo
		if app.WORLD_BOSS_YUMA:
			if self.WorldbossHwnd:
				self.WorldbossHwnd = {}
		if app.FAST_EQUIP_WORLDARD:
			if self.wndFastEquip:
				self.wndFastEquip.Close()
				self.wndFastEquip.Destroy()
				del self.wndFastEquip
		self.wndChatLog.Destroy()	
		for btn in self.questButtonList:
			btn.SetEvent(0)
		for btn in self.whisperButtonList:
			btn.SetEvent(0)
		for dlg in self.whisperDialogDict.itervalues():
			dlg.Destroy()
		for brd in self.guildScoreBoardDict.itervalues():
			brd.Destroy()
		for dlg in self.equipmentDialogDict.itervalues():
			dlg.Destroy()
			
		if app.ENABLE_ANTI_MULTIPLE_FARM:
			del self.wndAntiMultipleFarm
		# ITEM_MALL
		del self.mallPageDlg
		# END_OF_ITEM_MALL
		if app.WON_EXCHANGE:
			del self.wndWonExchange
		del self.wndGuild
		del self.wndMessenger
		del self.wndUICurtain
		del self.wndChat		
		del self.wndTaskBar
		del self.wndTaskBarS
		if app.ENABLE_CUBE_RENEWAL_WORLDARD:
			del self.wndCubeRenewal
		if self.wndExpandedTaskBar:
			del self.wndExpandedTaskBar
		del self.wndEnergyBar
		del self.wndCharacter
		del self.wndInventory
		del self.wndBio
		del self.wndCalendar
		if self.wndDragonSoul:
			del self.wndDragonSoul
		if app.BL_REMOTE_SHOP:
			if self.wndRemoteShop:
				del self.wndRemoteShop
		if self.wndDragonSoulRefine:
			del self.wndDragonSoulRefine
		if app.BL_MAILBOX:
			if self.mail_box:
				self.mail_box.Destroy()
				del self.mail_box			
		if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
			if self.wndSpecialStorage:
				del self.wndSpecialStorage

			if self.wndInventoryMenu:
				del self.wndInventoryMenu
		del self.dlgExchange
		del self.dlgPointReset
		del self.dlgShop
		del self.dlgRestart
		del self.dlgSystem
		del self.dlgPassword
		del self.hyperlinkItemTooltip
		if app.ENABLE_DECORUM:
			del self.hyperlinkArenaTooltip		
		del self.tooltipItem
		del self.tooltipSkill
		del self.wndMiniMap
		del self.wndSafebox
		del self.wndCalendarButton
		del self.wndMall
		del self.wndParty
		del self.wndHelp
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			del self.wndAcceCombine
			del self.wndAcceAbsorption
		if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
			del self.wndPrivateShopSearch
		if app.ENABLE_CHANGELOOK_SYSTEM:
			del self.wndChangeLook
		del self.wndCube
		del self.wndCubeResult
		del self.privateShopBuilder
		del self.inputDialog
		del self.wndItemFinder
		del self.wndShopSearch
		del self.wndShopSearchFilter
		del self.wndbpass
		del self.wndChatLog
		del self.dlgRefineNew
		del self.wndGuildBuilding
		del self.wndGameButton
		del self.tipBoard
		del self.bigBoard
		if app.ENABLE_MAINTENANCE_SYSTEM:
			del self.wndMaintenance
		del self.missionBoard
		del self.wndItemSelect

		if app.GUILD_RANK_SYSTEM:
			del self.wndGuildRanking
		if app.__BL_RANKING__:
			del self.wndPlayerRanking
		if app.ENABLE_DECORUM:
			del self.wndDecorumOther
			del self.wndDecorumSelf		
		# BEGIN_OFFLINE_SHOP
		del self.dlgOfflineShop
		# END_OF_OFFLINE_SHOP
		
		if app.ENABLE_SWITCHBOT:
			del self.wndSwitchbot

		if self.wndExpandedMoneyTaskBar:
			del self.wndExpandedMoneyTaskBar
	
		self.questButtonList = []
		self.whisperButtonList = []
		if app.ENABLE_HUNTING_SYSTEM:
			del self.wndHunting
			del self.wndHuntingSelect
			del self.wndHuntingReward
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}
		# BEGIN_OFFLINE_SHOP
		self.offlineShopAdvertisementBoardDict = {}
		# END_OF_OFFLINE_SHOP
		uiChat.DestroyChatInputSetWindow()

	## Skill
	def OnUseSkill(self, slotIndex, coolTime):
		self.wndCharacter.OnUseSkill(slotIndex, coolTime)
		self.wndTaskBar.OnUseSkill(slotIndex, coolTime)
		self.wndGuild.OnUseSkill(slotIndex, coolTime)

	def OnActivateSkill(self, slotIndex):
		self.wndCharacter.OnActivateSkill(slotIndex)
		self.wndTaskBar.OnActivateSkill(slotIndex)

	def OnDeactivateSkill(self, slotIndex):
		self.wndCharacter.OnDeactivateSkill(slotIndex)
		self.wndTaskBar.OnDeactivateSkill(slotIndex)

	def OnChangeCurrentSkill(self, skillSlotNumber):
		self.wndTaskBar.OnChangeCurrentSkill(skillSlotNumber)

	if app.SKILL_COOLTIME_UPDATE:
		def	SkillClearCoolTime(self, slotIndex):
			self.wndCharacter.SkillClearCoolTime(slotIndex)
			self.wndTaskBar.SkillClearCoolTime(slotIndex)

	def SelectMouseButtonEvent(self, dir, event):
		self.wndTaskBar.SelectMouseButtonEvent(dir, event)

	## Refresh
	def RefreshAlignment(self):
		self.wndCharacter.RefreshAlignment()

	def RefreshStatus(self):
		self.wndTaskBar.RefreshStatus()
		self.wndCharacter.RefreshStatus()
		self.wndInventory.RefreshStatus()
		if self.wndEnergyBar:
			self.wndEnergyBar.RefreshStatus()
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.RefreshStatus()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def costume_hide_clear(self):
			self.wndInventory.costume_hide_clear()
		def costume_hide_list(self,slot,index):
			self.wndInventory.costume_hide_list(slot,index)
		def costume_hide_load(self):
			self.wndInventory.costume_hide_load()

	if app.ENABLE_EXPRESSING_EMOTION:
		def RefreshEmotionsNew(self):
			self.wndCharacter.RefreshEmotion()

		def ClearEmotionsNew(self):
			self.wndCharacter.ClearEmotionsNew()

		def AddEmotionsNew(self, id_emotion, time_emotion):
			self.wndCharacter.AddEmotionsNew(id_emotion,time_emotion)

	def RefreshStamina(self):
		self.wndTaskBar.RefreshStamina()

	def HPPoisonEffectShow(self):
		self.wndTaskBar.HPPoisonEffectShow()
	
	def HPPoisonEffectHide(self):
		self.wndTaskBar.HPPoisonEffectHide()

	def RefreshSkill(self):
		self.wndCharacter.RefreshSkill()
		self.wndTaskBar.RefreshSkill()
	
	if app.ENABLE_SPECIAL_STATS_SYSTEM:	
		def RefreshSpecialStatsSkill(self, slotIndex, level):
			self.wndCharacter.RefreshTalentSlot(slotIndex, level)

	def RefreshInventory(self):
		self.wndTaskBar.RefreshQuickSlot()
		self.wndInventory.RefreshItemSlot()

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.RefreshItemSlot()
		if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
			self.wndSpecialStorage.RefreshItemSlot()
		if app.FAST_EQUIP_WORLDARD:
			self.wndFastEquip.RefreshEquipSlotWindow()
			
	if app.ENABLE_EXTEND_INVEN_SYSTEM:
		def SetInventoryPageKilit(self):
			self.wndInventory.UpdateInven()

	def RefreshCharacter(self): ## Character 페이지의 얼굴, Inventory 페이지의 전신 그림 등의 Refresh
		self.wndCharacter.RefreshCharacter()
		self.wndTaskBar.RefreshQuickSlot()

	def RefreshQuest(self):
		self.wndCharacter.RefreshQuest()

	def RefreshSafebox(self):
		self.wndSafebox.RefreshSafebox()

	if app.GUILD_RANK_SYSTEM:
		def OpenGuildRanking(self):
			self.wndGuildRanking.Open()

	if app.__BL_RANKING__:
		def OpenPlayerRanking(self):
			self.wndPlayerRanking.Open()

	# ITEM_MALL
	def RefreshMall(self):
		self.wndMall.RefreshMall()

	def OpenItemMall(self):
		if not self.mallPageDlg:
			self.mallPageDlg = uiShop.MallPageDialog()

		self.mallPageDlg.Open()
	# END_OF_ITEM_MALL

	def RefreshMessenger(self):
		self.wndMessenger.RefreshMessenger()
		self.UpdateWhisperButtons()

	def UpdateWhisperButtons(self, name = ""):
		for key, whisper in self.whisperDialogDict.items():
			if name != "":
				if name != key:
					continue
			whisper.SetFriendButton()
			whisper.SetBlockButton()

	def RefreshGuildInfoPage(self):
		self.wndGuild.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.wndGuild.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.wndGuild.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.wndGuild.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.wndGuild.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.wndGuild.RefreshGuildGradePage()

	def DeleteGuild(self):
		self.wndMessenger.ClearGuildMember()
		self.wndGuild.DeleteGuild()

	def RefreshMobile(self):
		self.dlgSystem.RefreshMobile()

	def OnMobileAuthority(self):
		self.dlgSystem.OnMobileAuthority()

	def OnBlockMode(self, mode):
		self.dlgSystem.OnBlockMode(mode)

	## Calling Functions
	# PointReset
	def OpenPointResetDialog(self):
		self.dlgPointReset.Show()
		self.dlgPointReset.SetTop()

	def ClosePointResetDialog(self):
		self.dlgPointReset.Close()

	# Shop
	def OpenShopDialog(self, vid):
		self.wndInventory.Show()
		self.wndInventory.SetTop()
		self.dlgShop.Open(vid)
		self.dlgShop.SetTop()

	def CloseShopDialog(self):
		self.dlgShop.Close()

	def RefreshShopDialog(self):
		self.dlgShop.Refresh()
	# BEGIN_OFFLINE_SHOP
	def OpenOfflineShopDialog(self, vid):
		self.wndInventory.Show()
		self.wndInventory.SetTop()
		self.dlgOfflineShop.Open(vid)
		self.dlgOfflineShop.SetTop()

	def CloseOfflineShopDialog(self):
		self.dlgOfflineShop.Close()

	def RefreshOfflineShopDialog(self):
		self.dlgOfflineShop.Refresh()
	# END_OF_OFFLINE_SHOP

	## Quest
	def OpenCharacterWindowQuestPage(self):
		self.wndCharacter.Show()
		self.wndCharacter.SetState("QUEST")

	def OpenQuestWindow(self, skin, idx):

		wnds = ()

		q = uiQuest.QuestDialog(skin, idx)
		q.SetWindowName("QuestWindow" + str(idx))
		q.Show()
		if skin:
			q.Lock()
			wnds = self.__HideWindows()

			# UNKNOWN_UPDATE
			q.AddOnDoneEvent(lambda tmp_self, args=wnds: self.__ShowWindows(args))
			# END_OF_UNKNOWN_UPDATE

		if skin:
			q.AddOnCloseEvent(q.Unlock)
		q.AddOnCloseEvent(lambda key = self.wndQuestWindowNewKey:ui.__mem_func__(self.RemoveQuestDialog)(key))
		self.wndQuestWindow[self.wndQuestWindowNewKey] = q

		self.wndQuestWindowNewKey = self.wndQuestWindowNewKey + 1

		# END_OF_UNKNOWN_UPDATE

	def RemoveQuestDialog(self, key):
		del self.wndQuestWindow[key]

	## Exchange
	def StartExchange(self):
		self.dlgExchange.OpenDialog()
		self.dlgExchange.Refresh()

	def EndExchange(self):
		self.dlgExchange.CloseDialog()

	def RefreshExchange(self):
		self.dlgExchange.Refresh()

	if app.WJ_ENABLE_TRADABLE_ICON:
		def CantTradableItemExchange(self, dstSlotIndex, srcSlotIndex):
			self.dlgExchange.CantTradableItem(dstSlotIndex, srcSlotIndex)

	## Party
	def AddPartyMember(self, pid, name):
		self.wndParty.AddPartyMember(pid, name)

		self.__ArrangeQuestButton()

	def UpdatePartyMemberInfo(self, pid):
		self.wndParty.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.wndParty.RemovePartyMember(pid)

		##!! 20061026.levites.퀘스트_위치_보정
		self.__ArrangeQuestButton()

	def LinkPartyMember(self, pid, vid):
		self.wndParty.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.wndParty.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.wndParty.UnlinkAllPartyMember()

	def ExitParty(self):
		self.wndParty.ExitParty()

		##!! 20061026.levites.퀘스트_위치_보정
		self.__ArrangeQuestButton()

	def PartyHealReady(self):
		self.wndParty.PartyHealReady()

	def ChangePartyParameter(self, distributionMode):
		self.wndParty.ChangePartyParameter(distributionMode)

	def PartyPoisonGuageShow(self):
		self.wndParty.PartyPoisonGuageShow()
	
	def PartyPoisonGuageHide(self):
		self.wndParty.PartyPoisonGuageHide()

	## Safebox
	def AskSafeboxPassword(self):
		if self.wndSafebox.IsShow():
			return

		# SAFEBOX_PASSWORD
		self.dlgPassword.SetTitle(localeInfo.PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/safebox_password ")
		# END_OF_SAFEBOX_PASSWORD

		self.dlgPassword.ShowDialog()

	def OpenSafeboxWindow(self, size):
		self.dlgPassword.CloseDialog()
		self.wndSafebox.ShowWindow(size)

	def RefreshSafeboxMoney(self):
		self.wndSafebox.RefreshSafeboxMoney()

	def CommandCloseSafebox(self):
		self.wndSafebox.CommandCloseSafebox()

	if app.WORLD_BOSS_YUMA:
		def WorldbossNotification(self, szString):
			for i in range(len(constInfo.WORLD_BOSS_TEXT_POSITION)):
				if constInfo.WORLD_BOSS_TEXT_POSITION[i] == 0:
					constInfo.WORLD_BOSS_TEXT_POSITION[i] = 1
					self.WorldbossHwnd[i] = uiworldbosstext.WorldbossNotification(szString, i)
					break
		
	if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
		def AutoStackStorage(self):
			self.wndSpecialStorage.AutoStackStorage()

	if app.ENABLE_6_7_BONUS_NEW_SYSTEM:
		def OpenSkillbookCombinationDialog(self):
			import bonus67
			
			if self.wndSkillBookCombination.IsShow():
				return

			if self.privateShopBuilder.IsShow():
				return
						
			self.wndSkillBookCombination.OpenNew()
			self.wndSkillBookCombination.Show()
			

			if not self.wndInventory.IsShow():
				self.wndInventory.Show()

		def OpenAttr67BonusNew(self):
			if self.wndAttr67Add.IsShow():
				return

			self.wndAttr67Add.OpenNew()
			self.wndAttr67Add.Show()

			if not self.wndInventory.IsShow():
				self.wndInventory.Show()

		def AddMaterialSlot(self, vnum):
			if not self.wndAttr67Add.IsShow():
				return

			self.wndAttr67Add.AddMaterialSlot(vnum)

	# ITEM_MALL
	def AskMallPassword(self):
		if self.wndMall.IsShow():
			return
		self.dlgPassword.SetTitle(localeInfo.MALL_PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/mall_password ")
		self.dlgPassword.ShowDialog()

	def OpenMallWindow(self, size):
		self.dlgPassword.CloseDialog()
		self.wndMall.ShowWindow(size)

	def CommandCloseMall(self):
		self.wndMall.CommandCloseMall()
	# END_OF_ITEM_MALL

	## Guild
	def OnStartGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnStartGuildWar(guildSelf, guildOpp)

		guildWarScoreBoard = uiGuild.GuildWarScoreBoard()
		guildWarScoreBoard.Open(guildSelf, guildOpp)
		guildWarScoreBoard.Show()
		self.guildScoreBoardDict[uiGuild.GetGVGKey(guildSelf, guildOpp)] = guildWarScoreBoard

	def OnEndGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnEndGuildWar(guildSelf, guildOpp)

		key = uiGuild.GetGVGKey(guildSelf, guildOpp)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].Destroy()
		del self.guildScoreBoardDict[key]
	# END_OF_GUILDWAR_MEMBER_COUNT
	
	# GUILDWAR_MEMBER_COUNT
	def UpdateMemberCount(self, gulidID1, memberCount1, guildID2, memberCount2):
		key = uiGuild.GetGVGKey(gulidID1, guildID2)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].UpdateMemberCount(gulidID1, memberCount1, guildID2, memberCount2)
	# END_OF_GUILDWAR_MEMBER_COUNT

	def OnRecvGuildWarPoint(self, gainGuildID, opponentGuildID, point):
		key = uiGuild.GetGVGKey(gainGuildID, opponentGuildID)
		if not self.guildScoreBoardDict.has_key(key):
			return

		guildBoard = self.guildScoreBoardDict[key]
		guildBoard.SetScore(gainGuildID, opponentGuildID, point)
		
	## PK Mode
	def OnChangePKMode(self):
		self.wndCharacter.RefreshAlignment()
		self.dlgSystem.OnChangePKMode()

	## Refine
	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type):
		self.dlgRefineNew.Open(targetItemPos, nextGradeItemVnum, cost, prob, type)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.dlgRefineNew.AppendMaterial(vnum, count)

	if app.ENABLE_REFINE_RENEWAL:
		def CheckRefineDialog(self, isFail):
			self.dlgRefineNew.CheckRefine(isFail)

	if app.ENABLE_SHIP_DEFENSE:
		def SetAllianceTargetBoard(self, targetBoard):
			self.uiAllianceTargetBoard = targetBoard

	## Show & Hide
	def ShowDefaultWindows(self):
		self.wndTaskBarS.Show()
		self.wndTaskBar.Show()
		self.wndMiniMap.Show()
		self.wndMiniMap.ShowMiniMap()
		#self.wndCalendarButton.Show()
		if self.wndEnergyBar:
			self.wndEnergyBar.Show()

	def ShowAllWindows(self):
		if app.ENABLE_NEW_FISHING_SYSTEM:
			if self.wndFishingWindow:
				self.wndFishingWindow.Open()
		if app.WON_EXCHANGE:
			if self.wndWonExchange:
				self.wndWonExchange.Show()
		self.wndTaskBarS.Show()
		self.wndTaskBar.Show()
		self.wndCharacter.Show()
		self.wndInventory.Show()
		self.wndCalendar.Show()
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.Show()
			self.wndDragonSoulRefine.Show()
		self.wndChat.Show()		
		self.wndMiniMap.Show()

		if self.wndEnergyBar:
			self.wndEnergyBar.Show()
		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Show()
			self.wndExpandedTaskBar.SetTop()
		if self.wndExpandedMoneyTaskBar:
			self.wndExpandedMoneyTaskBar.Show()
			self.wndExpandedMoneyTaskBar.SetTop()
			
		if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
			if self.wndSpecialStorage:
				self.wndSpecialStorage.Show()

			if self.wndInventoryMenu:
				self.wndInventoryMenu.Show()

	if app.WON_EXCHANGE:
		def IsShowDlgQuestionWindow(self):
			if self.wndInventory.IsDlgQuestionShow():
				return True
			elif self.wndDragonSoul.IsDlgQuestionShow():
				return True
			elif self.dlgShop.IsDlgQuestionShow():
				return True
			elif self.wndWonExchange.IsDlgQuestionShow():
				return True
			else:
				return False

		def CloseDlgQuestionWindow(self):
			if self.wndInventory.IsDlgQuestionShow():
				self.wndInventory.ExternQuestionDialog_Close()
			if self.wndDragonSoul.IsDlgQuestionShow():
				self.wndDragonSoul.ExternQuestionDialog_Close()
			if self.dlgShop.IsDlgQuestionShow():
				self.dlgShop.ExternQuestionDialog_Close()
			if self.wndWonExchange.IsDlgQuestionShow():
				self.wndWonExchange.ExternQuestionDialog_Close()

		def ToggleWonExchangeWindow(self):
			if player.IsObserverMode():
				return

			if False == self.wndWonExchange.IsShow():
				self.wndWonExchange.SetPage(uiWonExchange.WonExchangeWindow.PAGE_DESC)
				if False == self.wndExpandedMoneyTaskBar.IsShow():
					self.wndExpandedMoneyTaskBar.Show()
					self.wndExpandedMoneyTaskBar.SetTop()
				self.wndWonExchange.Show()
				self.wndWonExchange.SetTop()
			else:
				self.wndWonExchange.Hide()

	def HideAllWindows(self):
		if app.ENABLE_ANTI_MULTIPLE_FARM:
			if self.wndAntiMultipleFarm:
				self.wndAntiMultipleFarm.Hide()
		if app.WON_EXCHANGE:
			if self.wndWonExchange:
				self.wndWonExchange.Hide()
		if self.wndTaskBar:
			self.wndTaskBar.Hide()
		if self.wndTaskBarS:
			self.wndTaskBarS.Hide()
		if app.ENABLE_SWITCHBOT:
			if self.wndSwitchbot:
				self.wndSwitchbot.Hide()
		if self.wndEnergyBar:
			self.wndEnergyBar.Hide()
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			if self.wndDungeonInfo:
				self.wndDungeonInfo.Hide()
		if app.ENABLE_KILL_STATISTICS:
			if self.wndCharacter:
				self.wndCharacter.Close()
		else:
			if self.wndCharacter:
				self.wndCharacter.Hide()

		if self.wndInventory:
			self.wndInventory.Hide()
			
		if self.wndCalendar:
			self.wndCalendar.Hide()

		if app.ENABLE_SHIP_DEFENSE:
			if self.uiAllianceTargetBoard:
				self.uiAllianceTargetBoard.Hide()

		if self.wndExpandedMoneyTaskBar:
			self.wndExpandedMoneyTaskBar.Hide()

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.Hide()
			self.wndDragonSoulRefine.Hide()

		if self.wndChat:
			self.wndChat.Hide()

		if self.wndMiniMap:
			self.wndMiniMap.Hide()

		if self.wndMessenger:
			self.wndMessenger.Hide()

		if self.wndGuild:
			self.wndGuild.Hide()

		if app.ENABLE_HUNTING_SYSTEM:
			if self.wndHunting:
				self.wndHunting.Hide()
			if self.wndHuntingSelect:
				self.wndHuntingSelect.Hide()
			if self.wndHuntingReward:
				self.wndHuntingReward.Hide()

		if app.ENABLE_DECORUM:
			if self.wndDecorumSelf:
				self.wndDecorumSelf.Hide()
				
			if self.wndDecorumOther:
				self.wndDecorumOther.Hide()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Hide()
	
		if app.BL_MAILBOX:
			if self.mail_box:
				self.mail_box.Hide()
	
		if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
			if self.wndSpecialStorage:
				self.wndSpecialStorage.Hide()

			if self.wndInventoryMenu:
				self.wndInventoryMenu.Hide()

		if app.ENABLE_NEW_FISHING_SYSTEM:
			if self.wndFishingWindow:
				self.wndFishingWindow.Close()

	def ShowMouseImage(self):
		self.wndTaskBar.ShowMouseImage()

	def HideMouseImage(self):
		self.wndTaskBar.HideMouseImage()

	def ToggleChat(self):
		if True == self.wndChat.IsEditMode():
			self.wndChat.CloseChat()
		else:
			# 웹페이지가 열렸을때는 채팅 입력이 안됨
			if self.wndWeb and self.wndWeb.IsShow():
				pass
			else:
				self.wndChat.OpenChat()

	def IsOpenChat(self):
		return self.wndChat.IsEditMode()

	def SetChatFocus(self):
		self.wndChat.SetChatFocus()

	if app.RENEWAL_DEAD_PACKET:
		def OpenRestartDialog(self, d_time):
			self.dlgRestart.OpenDialog(d_time)
			self.dlgRestart.SetTop()
	else:
		def OpenRestartDialog(self):
			self.dlgRestart.OpenDialog()
			self.dlgRestart.SetTop()

	def CloseRestartDialog(self):
		self.dlgRestart.Close()

	def ToggleSystemDialog(self):
		if False == self.dlgSystem.IsShow():
			self.dlgSystem.OpenDialog()
			self.dlgSystem.SetTop()
		else:
			self.dlgSystem.Close()
			
	def ToggleOfflineShopDialog(self):
		net.SendChatPacket("/open_offlineshop")

	def OpenSystemDialog(self):
		self.dlgSystem.OpenDialog()
		self.dlgSystem.SetTop()

	def ToggleMessenger(self):
		if self.wndMessenger.IsShow():
			self.wndMessenger.Hide()
		else:
			self.wndMessenger.SetTop()
			self.wndMessenger.Show()

	def ToggleMiniMap(self):
		if app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT):
			if False == self.wndMiniMap.isShowMiniMap():
				self.wndMiniMap.ShowMiniMap()
				self.wndMiniMap.SetTop()
			else:
				self.wndMiniMap.HideMiniMap()

		else:
			self.wndMiniMap.ToggleAtlasWindow()

	def PressMKey(self):
		if app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT):
			self.ToggleMessenger()

		else:
			self.ToggleMiniMap()

	def SetMapName(self, mapName):
		self.wndMiniMap.SetMapName(mapName)

	def MiniMapScaleUp(self):
		self.wndMiniMap.ScaleUp()

	def MiniMapScaleDown(self):
		self.wndMiniMap.ScaleDown()

	def ToggleCharacterWindow(self, state):
		if False == player.IsObserverMode():
			if False == self.wndCharacter.IsShow():
				self.OpenCharacterWindowWithState(state)
			else:
				if state == self.wndCharacter.GetState():
					self.wndCharacter.OverOutItem()
					if app.ENABLE_KILL_STATISTICS:
						self.wndCharacter.Close()
					else:
						self.wndCharacter.Hide()
				else:
					self.wndCharacter.SetState(state)

	def OpenCharacterWindowWithState(self, state):
		if False == player.IsObserverMode():
			self.wndCharacter.SetState(state)
			self.wndCharacter.Show()
			self.wndCharacter.SetTop()

	def ToggleCharacterWindowStatusPage(self):
		self.ToggleCharacterWindow("STATUS")

	if app.BL_KILL_BAR:
		def AddKillInfo(self, killer, victim, killer_race, victim_race, weapon_type):
			self.wndMiniMap.AddKillInfo(killer, victim, killer_race, victim_race, weapon_type)

	def ToggleInventoryWindow(self):
		if False == player.IsObserverMode():
			if False == self.wndInventory.IsShow():
				self.wndInventory.Show()
				self.wndInventory.SetTop()
			else:
				self.wndInventory.OverOutItem()
				self.wndInventory.Close()

	if app.ENABLE_HUNTING_SYSTEM:
		def ToggleHuntingWindow(self):
			if self.wndHunting.IsShow():
				self.wndHunting.Close()
			elif self.wndHuntingSelect.IsShow():
				self.wndHuntingSelect.Close()
			else:
				net.SendHuntingAction(1, 0)
				
		def OpenHuntingWindowMain(self, level, monster, cur_count, dest_count, money_min, money_max, exp_min, exp_max, race_item, race_item_count):
			if self.wndHunting:
				self.wndHunting.OpenMain(level, monster, cur_count, dest_count, money_min, money_max, exp_min, exp_max, race_item, race_item_count)
				self.wndHunting.SetTop()
				constInfo.HUNTING_BUTTON_FLASH = 0
				
		def OpenHuntingWindowSelect(self, level, type ,monster, count, money_min, money_max, exp_min, exp_max, race_item, race_item_count):
			if self.wndHunting and self.wndHunting.IsShow():
				self.wndHunting.CloseWithMini()
			self.wndHuntingSelect.OpenSelect(level, type ,monster, count, money_min, money_max, exp_min, exp_max, race_item, race_item_count)
			constInfo.HUNTING_BUTTON_FLASH = 0
			
		def OpenHuntingWindowReward(self, level, reward, reward_count, random_reward, random_reward_count, money, exp):
			if False == self.wndHuntingReward.IsShow():
				self.wndHuntingReward.OpenReward(level, reward, reward_count, random_reward, random_reward_count, money, exp)
				self.wndHuntingReward.SetTop()
				
		def UpdateHuntingMission(self, count):
			if self.wndHunting:
				self.wndHunting.UpdateMission(count)
		
		def HuntingSetRandomItemsMain(self, item_vnum, item_count):
			if self.wndHunting:
				self.wndHunting.SetRandomItemTable(item_vnum, item_count)
				
		def HuntingSetRandomItemsSelect(self, item_vnum, item_count):
			if self.wndHuntingSelect:
				self.wndHuntingSelect.SetRandomItemTable(item_vnum, item_count)
 
	def TogglePetMain(self):
		if FALSE == player.IsObserverMode():
			if FALSE == self.wndExpandedTaskBar.IsShow():
				self.wndExpandedTaskBar.Show()
				self.wndExpandedTaskBar.SetTop()
			else:
				self.wndExpandedTaskBar.Close()
		net.SendChatPacket("/gift")

	def ToggleExpandedButton(self):
		if False == player.IsObserverMode():
			if False == self.wndExpandedTaskBar.IsShow():
				self.wndExpandedTaskBar.Show()
				self.wndExpandedTaskBar.SetTop()
			else:
				self.wndExpandedTaskBar.Close()

	def ToggleExpandedMoneyButton(self):
		if False == self.wndExpandedMoneyTaskBar.IsShow():
			self.wndExpandedMoneyTaskBar.Show()
			self.wndExpandedMoneyTaskBar.SetTop()
		else:
			self.wndExpandedMoneyTaskBar.Close()

	# 용혼석
	def DragonSoulActivate(self, deck):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.ActivateDragonSoulByExtern(deck)

	def DragonSoulDeactivate(self):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.DeactivateDragonSoul()			

	def Highlight_Item(self, inven_type, inven_pos):
		if not app.ENABLE_HIGHLIGHT_SYSTEM:
			if player.DRAGON_SOUL_INVENTORY == inven_type:
				if app.ENABLE_DRAGON_SOUL_SYSTEM:
					self.wndDragonSoul.HighlightSlot(inven_pos)
		else:
			if inven_type == player.INVENTORY:
				self.wndInventory.HighlightSlot(inven_pos)
			elif inven_type == player.DRAGON_SOUL_INVENTORY:
				if app.ENABLE_DRAGON_SOUL_SYSTEM:
					self.wndDragonSoul.HighlightSlot(inven_pos)

	def DragonSoulGiveQuilification(self):
		self.DRAGON_SOUL_IS_QUALIFIED = True
		self.wndExpandedTaskBar.SetToolTipText(uiTaskBar.ExpandedTaskBar.BUTTON_DRAGON_SOUL, uiScriptLocale.TASKBAR_DRAGON_SOUL)

	def ToggleDragonSoulWindow(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if False == self.wndDragonSoul.IsShow():
					if self.DRAGON_SOUL_IS_QUALIFIED:
						self.wndDragonSoul.Show()
					else:
						try:
							self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_UNQUALIFIED)
							self.wndPopupDialog.Open()
						except:
							self.wndPopupDialog = uiCommon.PopupDialog()
							self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_UNQUALIFIED)
							self.wndPopupDialog.Open()
				else:
					self.wndDragonSoul.Close()

	def ToggleDragonSoulWindowWithNoInfo(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if False == self.wndDragonSoul.IsShow():
					if self.DRAGON_SOUL_IS_QUALIFIED:
						self.wndDragonSoul.Show()
				else:
					self.wndDragonSoul.Close()

	def FailDragonSoulRefine(self, reason, inven_type, inven_pos):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.RefineFail(reason, inven_type, inven_pos)

	def SucceedDragonSoulRefine(self, inven_type, inven_pos):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.RefineSucceed(inven_type, inven_pos)

	def OpenDragonSoulRefineWindow(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if False == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.Show()
					if None != self.wndDragonSoul:
						if False == self.wndDragonSoul.IsShow():
							self.wndDragonSoul.Show()

	def CloseDragonSoulRefineWindow(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.Close()

	# 용혼석 끝
		
	if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
		def ToggleSpecialStorageWindow(self, arg = 0):
			if False == player.IsObserverMode():
				self.wndSpecialStorage.Show()
				self.wndSpecialStorage.ClickButton(arg)

		def ToggleKeySpecialStorageWindow(self, arg = 0):
			if False == player.IsObserverMode():
				if False == self.wndSpecialStorage.IsShow():
					self.wndSpecialStorage.Show()
					self.wndSpecialStorage.ClickButton(arg)
				else:
					self.wndSpecialStorage.Close()
	
		def ToggleInventoryMenuWindow(self):
			if False == player.IsObserverMode():
				if False == self.wndInventoryMenu.IsShow():
					self.wndInventoryMenu.Show()
					self.wndInventoryMenu.SetTop()
				else:
					self.wndInventoryMenu.Close()

	def ToggleGuildWindow(self):
		if not self.wndGuild.IsShow():
			if self.wndGuild.CanOpen():
				self.wndGuild.Open()
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GUILD_YOU_DO_NOT_JOIN)
		else:
			self.wndGuild.OverOutItem()
			self.wndGuild.Hide()
			
	def ToggleChatLogWindow(self):
		if self.wndChatLog.IsShow():
			self.wndChatLog.Hide()
		else:
			self.wndChatLog.Show()

	if app.ENABLE_SWITCHBOT:
		def ToggleSwitchbotWindow(self):
			if self.wndSwitchbot.IsShow():
				self.wndSwitchbot.Close()
			else:
				self.wndSwitchbot.Open()
				
		def RefreshSwitchbotWindow(self):
			if self.wndSwitchbot and self.wndSwitchbot.IsShow():
				self.wndSwitchbot.RefreshSwitchbotWindow()

		def RefreshSwitchbotItem(self, slot):
			if self.wndSwitchbot and self.wndSwitchbot.IsShow():
				self.wndSwitchbot.RefreshSwitchbotItem(slot)

	if app.ENABLE_DECORUM:
		def CloseDecorumStatOther(self):
			if not self.wndDecorumOther:
				return
			
			self.wndDecorumOther.Destroy()
			self.wndDecorumOther = None
		
		def ToggleDecorumStat(self):
			if player.IsObserverMode():
				return
				
			if 0 == player.GetDecorum():
				import textTail
				textTail.RegisterInfoTail(player.GetMainCharacterIndex(), localeInfo.CANNOT_OPEN_DECORUM)
				return
				
			if not self.wndDecorumSelf.IsShow():
				self.wndDecorumSelf.Show()
				self.wndDecorumSelf.SetTop()
				self.wndDecorumSelf.State = self.wndDecorumSelf.STATE_FADE_IN
			else:
				self.wndDecorumSelf.State = self.wndDecorumSelf.STATE_FADE_OUT

	def CheckGameButton(self):
		if self.wndGameButton:
			self.wndGameButton.CheckGameButton()
			
	def Bind(self, game):
		self.game = game

	def __OnClickStatusPlusButton(self):
		self.ToggleCharacterWindow("STATUS")

	def __OnClickSkillPlusButton(self):
		self.ToggleCharacterWindow("SKILL")

	def __OnClickQuestButton(self):
		self.ToggleCharacterWindow("QUEST")

	def __OnClickHelpButton(self):
		player.SetPlayTime(1)
		self.CheckGameButton()
		self.OpenHelpWindow()

	def __OnClickBuildButton(self):
		self.BUILD_OpenWindow()

	def OpenHelpWindow(self):
		self.wndUICurtain.Show()
		self.wndHelp.Open()

	def CloseHelpWindow(self):
		self.wndUICurtain.Hide()
		self.wndHelp.Close()

	def OpenWebWindow(self, url):
		self.wndWeb.Open(url)

		# 웹페이지를 열면 채팅을 닫는다
		self.wndChat.CloseChat()

	# show GIFT
	def ShowGift(self):
		self.wndTaskBar.ShowGift()

	if app.ENABLE_CUBE_RENEWAL_WORLDARD:
		def BINARY_CUBE_RENEWAL_OPEN(self):
			self.wndCubeRenewal.Show()

	if app.FAST_EQUIP_WORLDARD:
		def OpenFastEquip(self):
			if self.wndFastEquip:
				if self.wndFastEquip.IsShow():
					self.wndFastEquip.Hide()
				else:
					self.wndFastEquip.Show()

	def CloseWbWindow(self):
		self.wndWeb.Close()
		
	def ToggleCalenderWindow(self):
		if self.wndCalendar.IsShow():
			self.wndCalendar.Close()
		else:
			self.wndCalendar.Open()

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def ActAcce(self, iAct, bWindow):
			if iAct == 1:
				if bWindow == True:
					if not self.wndAcceCombine.IsOpened():
						self.wndAcceCombine.Open()
					
					if not self.wndInventory.IsShow():
						self.wndInventory.Show()
				else:
					if not self.wndAcceAbsorption.IsOpened():
						self.wndAcceAbsorption.Open()
					
					if not self.wndInventory.IsShow():
						self.wndInventory.Show()
				
				self.wndInventory.RefreshBagSlotWindow()
			elif iAct == 2:
				if bWindow == True:
					if self.wndAcceCombine.IsOpened():
						self.wndAcceCombine.Close()
				else:
					if self.wndAcceAbsorption.IsOpened():
						self.wndAcceAbsorption.Close()
				
				self.wndInventory.RefreshBagSlotWindow()
			elif iAct == 3 or iAct == 4:
				if bWindow == True:
					if self.wndAcceCombine.IsOpened():
						self.wndAcceCombine.Refresh(iAct)
				else:
					if self.wndAcceAbsorption.IsOpened():
						self.wndAcceAbsorption.Refresh(iAct)
				
				self.wndInventory.RefreshBagSlotWindow()

	if app.ENABLE_CHANGELOOK_SYSTEM:
		def ActChangeLook(self, iAct):
			if iAct == 1:
				if not self.wndChangeLook.IsOpened():
					self.wndChangeLook.Open()
				
				if not self.wndInventory.IsShow():
					self.wndInventory.Show()
				
				self.wndInventory.RefreshBagSlotWindow()
			elif iAct == 2:
				if self.wndChangeLook.IsOpened():
					self.wndChangeLook.Close()
				
				self.wndInventory.RefreshBagSlotWindow()
			elif iAct == 3 or iAct == 4:
				if self.wndChangeLook.IsOpened():
					self.wndChangeLook.Refresh()
				
				self.wndInventory.RefreshBagSlotWindow()


	def ShopSearchReady(self):
		self.wndShopSearch.SearchDone()

	def ShopSearchBuyDone(self):
		self.wndShopSearch.BuyItemDone()

	def ShowShopSearch(self):
		self.wndShopSearch.Show()

	#Filter Shop Search
	def GetMinChequeShopSearch(self):
		return self.wndShopSearchFilter.GetMinCheque()

	def GetMaxChequeShopSearch(self):
		return self.wndShopSearchFilter.GetMaxCheque()

	def GetMinPriceShopSearch(self):
		return self.wndShopSearchFilter.GetMinPrice()

	def GetMaxPriceShopSearch(self):
		return self.wndShopSearchFilter.GetMaxPrice()

	def ManageFilterShopSearch(self):
		self.wndShopSearchFilter.ShowFilter()

	def FilterShopSearchHide(self):
		self.wndShopSearchFilter.CloseFilter()

	def ShowItemFinder(self):
		self.wndItemFinder.Show()

	def AppendInfoFinder(self, index, name_monster, prob, activi, vnum, count, name_item):
		self.wndItemFinder.AppendInfo(index, name_monster, prob, activi, vnum, count, name_item)

	def OpenCubeWindow(self):
		self.wndCube.Open()

		if False == self.wndInventory.IsShow():
			self.wndInventory.Show()
			
	def ShowBoardBpass(self):
		self.wndbpass.Show()

	def UpdateCubeInfo(self, gold, itemVnum, count):
		self.wndCube.UpdateInfo(gold, itemVnum, count)

	def CloseCubeWindow(self):
		self.wndCube.Close()

	def FailedCubeWork(self):
		self.wndCube.Refresh()

	def SucceedCubeWork(self, itemVnum, count):
		self.wndCube.Clear()

		print "큐브 제작 성공! [%d:%d]" % (itemVnum, count)

		if 0: # 결과 메시지 출력은 생략 한다
			self.wndCubeResult.SetPosition(*self.wndCube.GetGlobalPosition())
			self.wndCubeResult.SetCubeResultItem(itemVnum, count)
			self.wndCubeResult.Open()
			self.wndCubeResult.SetTop()

	if app.ENABLE_DUNGEON_INFO_SYSTEM:
		def ToggleDungeonInfoWindow(self):
			if False == player.IsObserverMode():
				if False == self.wndDungeonInfo.IsShow():
					self.wndDungeonInfo.Open()
				else:
					self.wndDungeonInfo.Close()

		def DungeonInfoOpen(self):
			if self.wndDungeonInfo:
				self.wndDungeonInfo.OnOpen()

		def DungeonRankingRefresh(self):
			if self.wndDungeonInfo:
				self.wndDungeonInfo.OnRefreshRanking()

		def DungeonInfoReload(self, onReset):
			if self.wndDungeonInfo:
				self.wndDungeonInfo.OnReload(onReset)

	def __HideWindows(self):
		hideWindows = self.wndTaskBar,\
						self.wndTaskBarS,\
						self.wndCharacter,\
						self.wndInventory,\
						self.wndGuild,\
						self.wndMessenger,\
						self.wndChat,\
						self.wndParty,\
						self.wndGameButton,

		if self.wndEnergyBar:
			hideWindows += self.wndEnergyBar,

		if app.WON_EXCHANGE:
			hideWindows += self.wndWonExchange,

		if self.wndExpandedTaskBar:
			hideWindows += self.wndExpandedTaskBar,
		if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
			if self.wndSpecialStorage:
				hideWindows += self.wndSpecialStorage,

			if self.wndInventoryMenu:
				hideWindows += self.wndInventoryMenu,

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			hideWindows += self.wndDragonSoul,\
						self.wndDragonSoulRefine,
						
		if app.BL_MAILBOX:
			if self.mail_box:
				hideWindows += self.mail_box,						

		if app.ENABLE_SWITCHBOT and self.wndSwitchbot:
			hideWindows += self.wndSwitchbot,

		if app.ENABLE_DECORUM and self.wndDecorumSelf and self.wndDecorumSelf.IsShow():
			hideWindows += self.wndDecorumSelf,

		if app.ENABLE_DECORUM and self.wndDecorumOther and self.wndDecorumOther.IsShow():
			hideWindows += self.wndDecorumOther,

		if app.ENABLE_ANTI_MULTIPLE_FARM and self.wndAntiMultipleFarm:
			hideWindows += self.wndAntiMultipleFarm,
			
		if self.wndExpandedMoneyTaskBar:
			hideWindows += self.wndExpandedMoneyTaskBar,	

		if app.ENABLE_HUNTING_SYSTEM:
			if self.wndHunting:
				hideWindows += self.wndHunting,
			if self.wndHuntingSelect:
				hideWindows += self.wndHuntingSelect,
			if self.wndHuntingReward:
				hideWindows += self.wndHuntingReward,
	
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			if self.wndDungeonInfo:
				hideWindows += self.wndDungeonInfo,			
				
		hideWindows = filter(lambda x:x.IsShow(), hideWindows)
		map(lambda x:x.Hide(), hideWindows)
		
		self.wndMiniMap.HideMiniMap()
		self.wndMiniMap.Hide()
		
		import sys

		self.HideAllQuestButton()
		self.HideAllWhisperButton()

		if self.wndChat.IsEditMode():
			self.wndChat.CloseChat()

		return hideWindows

	def __ShowWindows(self, wnds):
		import sys
		map(lambda x:x.Show(), wnds)
		global IsQBHide
		if not IsQBHide:
			self.ShowAllQuestButton()
		else:
			self.HideAllQuestButton()
		
		self.wndMiniMap.ShowMiniMap()
		self.wndMiniMap.Show()

		self.ShowAllWhisperButton()

	def BINARY_OpenAtlasWindow(self):
		if self.wndMiniMap:
			self.wndMiniMap.ShowAtlas()

	def BINARY_SetObserverMode(self, flag):
		self.wndGameButton.SetObserverMode(flag)

	# ACCESSORY_REFINE_ADD_METIN_STONE
	def BINARY_OpenSelectItemWindow(self):
		self.wndItemSelect.Open()
	# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

	#####################################################################################
	### Private Shop ###

	if app.ENABLE_MAINTENANCE_SYSTEM:
		def ShowMaintenanceSign(self, timeLeft, duration):
			if not self.wndMaintenance:
				self.wndMaintenance = uiMaintenance.MaintenanceBoard()
			self.wndMaintenance.Open(timeLeft, duration)

		def HideMaintenanceSign(self):
			if self.wndMaintenance:
				self.wndMaintenance.Close()

	def OpenPrivateShopInputNameDialog(self):
		#if player.IsInSafeArea():
		#	chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_OPEN_PRIVATE_SHOP_IN_SAFE_AREA)
		#	return

		inputDialog = uiCommon.InputDialog()
		inputDialog.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_NAME_DIALOG_TITLE)
		inputDialog.SetMaxLength(32)
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.OpenPrivateShopBuilder))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.ClosePrivateShopInputNameDialog))
		inputDialog.Open()
		self.inputDialog = inputDialog

	def ClosePrivateShopInputNameDialog(self):
		self.inputDialog = None
		return True

	def OpenPrivateShopBuilder(self):

		if not self.inputDialog:
			return True

		if not len(self.inputDialog.GetText()):
			return True

		self.privateShopBuilder.Open(self.inputDialog.GetText())
		self.ClosePrivateShopInputNameDialog()
		return True

	def AppearPrivateShop(self, vid, text):

		board = uiPrivateShopBuilder.PrivateShopAdvertisementBoard()
		board.Open(vid, text)

		self.privateShopAdvertisementBoardDict[vid] = board

	def DisappearPrivateShop(self, vid):

		if not self.privateShopAdvertisementBoardDict.has_key(vid):
			return

		del self.privateShopAdvertisementBoardDict[vid]
		uiPrivateShopBuilder.DeleteADBoard(vid)

	# BEGIN_OFFLINE_SHOP
	def OpenOfflineShopInputNameDialog(self):
		inputDialog = uiOfflineShop.OfflineShopInputDialog()
		inputDialog.BindInterfaceClass(self)
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.OpenOfflineShopBuilder))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.CloseOfflineShopInputNameDialog))
		inputDialog.Open()
		self.inputDialog = inputDialog

	def CloseOfflineShopInputNameDialog(self):
		self.inputDialog = None
		return True

	def OpenOfflineShopEditMode(self, vid, remain, map_index, x, y):
		self.offlineShopEditMode.Open(vid, remain, map_index, x, y)
	
	def OpenOfflineShopEdit(self):
		self.offlineShopEditMode.SetOpen()
	
	def RefreshOfflineShopEditMode(self):
		self.offlineShopEditMode.Refresh()

	def OpenOfflineShopBuilder(self):
		if not self.inputDialog:
			return True
		if not len(self.inputDialog.GetTitle()):
			return True
		if self.inputDialog.GetTime() < 0 or self.inputDialog.GetTime() == 0:
			return True
		self.offlineShopBuilder.Open(self.inputDialog.GetTitle(), self.inputDialog.GetTime())
		self.CloseOfflineShopInputNameDialog()
		return True

	def CloseOfflineShopBuilder(self):
		self.offlineShopBuilder.Close()

	def AppearOfflineShop(self, vid, text):
		board = uiOfflineShopBuilder.OfflineShopAdvertisementBoard()
		board.Open(vid, text)
		self.offlineShopAdvertisementBoardDict[vid] = board

	def DisappearOfflineShop(self, vid):
		if not self.offlineShopAdvertisementBoardDict.has_key(vid):
			return
		del self.offlineShopAdvertisementBoardDict[vid]
		uiOfflineShopBuilder.DeleteADBoard(vid)
	# END_OF_OFFLINE_SHOP

	#####################################################################################
	### Equipment ###

	def OpenEquipmentDialog(self, vid):
		dlg = uiEquipmentDialog.EquipmentDialog()
		dlg.SetItemToolTip(self.tooltipItem)
		dlg.SetCloseEvent(ui.__mem_func__(self.CloseEquipmentDialog))
		dlg.Open(vid)

		self.equipmentDialogDict[vid] = dlg

	def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogItem(slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogSocket(slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogAttr(slotIndex, attrIndex, type, value)

	def CloseEquipmentDialog(self, vid):
		if not vid in self.equipmentDialogDict:
			return
		del self.equipmentDialogDict[vid]

	#####################################################################################

	#####################################################################################
	### Quest ###
	def BINARY_ClearQuest(self, index):
		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

	def RecvQuest(self, index, name):
		# QUEST_LETTER_IMAGE
		self.BINARY_RecvQuest(index, name, "file", localeInfo.GetLetterImageName())
		# END_OF_QUEST_LETTER_IMAGE

	def BINARY_RecvQuest(self, index, name, iconType, iconName):

		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

		btn = uiWhisper.WhisperButton()

		# QUEST_LETTER_IMAGE
		##!! 20061026.levites.퀘스트_이미지_교체
		import item
		if "item"==iconType:
			item.SelectItem(int(iconName))
			buttonImageFileName=item.GetIconImageFileName()
		else:
			buttonImageFileName=iconName

		if iconName and (iconType not in ("item", "file")): # type "ex" implied
			btn.SetUpVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName.replace("open", "close")))
			btn.SetOverVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName))
			btn.SetDownVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName))
		else:
			if localeInfo.IsEUROPE():
				btn.SetUpVisual(localeInfo.GetLetterCloseImageName())
				btn.SetOverVisual(localeInfo.GetLetterOpenImageName())
				btn.SetDownVisual(localeInfo.GetLetterOpenImageName())
			else:
				btn.SetUpVisual(buttonImageFileName)
				btn.SetOverVisual(buttonImageFileName)
				btn.SetDownVisual(buttonImageFileName)
				btn.Flash()
		# END_OF_QUEST_LETTER_IMAGE

		if not app.ENABLE_QUEST_RENEWAL:
			if localeInfo.IsARABIC():
				btn.SetToolTipText(name, -20, 35)
				btn.ToolTipText.SetHorizontalAlignRight()
			else:
				btn.SetToolTipText(name, -20, 35)
				btn.ToolTipText.SetHorizontalAlignLeft()

			btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)
			btn.Show()
		else:
			btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)

		btn.index = index
		btn.name = name

		self.questButtonList.insert(0, btn)
		self.__ArrangeQuestButton()
		
		
		listOfTypes = iconType.split(",")
		if "blink" in listOfTypes:
			btn.Flash()

		listOfColors = {
			"golden":	0xFFffa200,
			"green":	0xFF00e600,
			"blue":		0xFF0099ff,
			"purple":	0xFFcc33ff,

			"fucsia":	0xFFcc0099,
			"aqua":		0xFF00ffff,
		}
		for k,v in listOfColors.iteritems():
			if k in listOfTypes:
				btn.ToolTipText.SetPackedFontColor(v)		

	def __ArrangeQuestButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		##!! 20061026.levites.퀘스트_위치_보정
		if self.wndParty.IsShow():
			xPos = 100 + 30
		else:
			xPos = 20

		if localeInfo.IsARABIC():
			xPos = xPos + 15

		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63

		count = 0
		for btn in self.questButtonList:
			if app.ENABLE_QUEST_RENEWAL:
				btn.SetToolTipText(str(len(self.questButtonList)))
				btn.ToolTipText.SetHorizontalAlignCenter()

			btn.SetPosition(xPos + (int(count/yCount) * 100), yPos + (count%yCount * 63))
			count += 1

			global IsQBHide
			if IsQBHide:
				btn.Hide()
			else:
				if app.ENABLE_QUEST_RENEWAL and count > 0:
					btn.Hide()
				else:
					btn.Show()

	def __StartQuest(self, btn):
		if app.ENABLE_QUEST_RENEWAL:
			self.__OnClickQuestButton()
			self.HideAllQuestButton()
		else:
			event.QuestButtonClick(btn.index)
			self.__DestroyQuestButton(btn)

	def __FindQuestButton(self, index):
		for btn in self.questButtonList:
			if btn.index == index:
				return btn

		return 0

	def MakeDungeonTimerWindow(self):
		self.wndDungeonTimer = uiDungeonTimer.Cooldown()
		self.wndDungeonTimer.Hide()

	def __DestroyQuestButton(self, btn):
		btn.SetEvent(0)
		self.questButtonList.remove(btn)
		self.__ArrangeQuestButton()

	def HideAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Hide()

	def ShowAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Show()
			if app.ENABLE_QUEST_RENEWAL:
				break

	#####################################################################################
	#####################################################################################
	### Decorum ###
	if app.ENABLE_DECORUM:	
		def SetDecorumBase(self, vid, decorum, legue, promotion, demotion, block):
			window = None
			if player.IsMainCharacterIndex(vid) or not vid:
				window = self.wndDecorumSelf
				
			else:
				self.CloseDecorumStatOther()
				self.wndDecorumOther = uiDecorum.DecorumStat()
				self.wndDecorumOther.AddFlag("movable")
				self.wndDecorumOther.SetCloseEvent(self.CloseDecorumStatOther)
				self.wndDecorumOther.IsSelf(False)
				self.wndDecorumOther.Show()
				self.wndDecorumOther.SetCenterPosition()
				window = self.wndDecorumOther

			if window == self.wndDecorumSelf:	
				window.SetBase(player.GetName(), decorum, legue)
			else:
				window.SetBase(chr.GetNameByVID(vid), decorum, legue)
			window.SetLegueInfo(promotion, demotion)
			window.SetBlock(block)
				
		def SetDecorumBattle(self, vid, type, done, won):
			window = None
			if player.IsMainCharacterIndex(vid) or not vid:
				window = self.wndDecorumSelf
			else:
				window = self.wndDecorumOther
			
			if type == 255:
				window.SetDuel(done, won)
			else:
				window.SetArena(type, done, won)
				
		def SetDecorumKD(self, vid, kill, death):
			window = None
			if player.IsMainCharacterIndex(vid) or not vid:
				window = self.wndDecorumSelf
			else:
				window = self.wndDecorumOther
			
			window.SetKD(kill, death)

	#####################################################################################

	#####################################################################################
	### Whisper ###

	def __InitWhisper(self):
		chat.InitWhisper(self)

	## 채팅창의 "메시지 보내기"를 눌렀을때 이름 없는 대화창을 여는 함수
	## 이름이 없기 때문에 기존의 WhisperDialogDict 와 별도로 관리된다.
	def OpenWhisperDialogWithoutTarget(self):
		if not self.dlgWhisperWithoutTarget:
			dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
			dlgWhisper.BindInterface(self)
			dlgWhisper.LoadDialog()
			dlgWhisper.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)
			dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
			dlgWhisper.Show()
			self.dlgWhisperWithoutTarget = dlgWhisper

			self.windowOpenPosition = (self.windowOpenPosition+1) % 5

		else:
			self.dlgWhisperWithoutTarget.SetTop()
			self.dlgWhisperWithoutTarget.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)

	## 이름 없는 대화창에서 이름을 결정했을때 WhisperDialogDict에 창을 넣어주는 함수
	def RegisterTemporaryWhisperDialog(self, name):
		if not self.dlgWhisperWithoutTarget:
			return

		btn = self.__FindWhisperButton(name)
		if 0 != btn:
			self.__DestroyWhisperButton(btn)

		elif self.whisperDialogDict.has_key(name):
			oldDialog = self.whisperDialogDict[name]
			oldDialog.Destroy()
			del self.whisperDialogDict[name]

		self.whisperDialogDict[name] = self.dlgWhisperWithoutTarget
		self.dlgWhisperWithoutTarget.OpenWithTarget(name)
		self.dlgWhisperWithoutTarget = None
		self.__CheckGameMaster(name)

	## 캐릭터 메뉴의 1:1 대화 하기를 눌렀을때 이름을 가지고 바로 창을 여는 함수
	if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
		def OpenWhisperDialog(self, name, language = "", empire = ""):
			if not self.whisperDialogDict.has_key(name):
				dlg = self.__MakeWhisperDialog(name)
				dlg.OpenWithTarget(name)
				if language != "" and empire != "":
					dlg.SetFlag(language, empire)
				dlg.chatLine.SetFocus()
				dlg.Show()

				self.__CheckGameMaster(name)
				btn = self.__FindWhisperButton(name)
				if 0 != btn:
					dlg.SetFlag(btn.languageID, btn.empireID)
					self.__DestroyWhisperButton(btn)
	else:
		def OpenWhisperDialog(self, name):
			if not self.whisperDialogDict.has_key(name):
				dlg = self.__MakeWhisperDialog(name)
				dlg.OpenWithTarget(name)
				dlg.chatLine.SetFocus()
				dlg.Show()

				self.__CheckGameMaster(name)
				btn = self.__FindWhisperButton(name)
				if 0 != btn:
					self.__DestroyWhisperButton(btn)

	## 다른 캐릭터로부터 메세지를 받았을때 일단 버튼만 띄워 두는 함수

	if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
		def RecvWhisper(self, name, language = "", empire = ""):
			app.FlashApplication()
			if not self.whisperDialogDict.has_key(name):
				btn = self.__FindWhisperButton(name)

				if 0 == btn:
					btn = self.__MakeWhisperButton(name, language, empire)
					btn.Flash()
						
					chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.RECEIVE_MESSAGE % (name))
				else:
					if language != "" and empire != "":
						btn.languageID = language
						btn.empireID = empire						
					btn.Flash()
					
			elif self.IsGameMasterName(name):
				dlg = self.whisperDialogDict[name]
				dlg.SetGameMasterLook()

				if language != "" and empire != "":
					dlg.SetFlag(language, empire)
	else:
		def RecvWhisper(self, name):
			app.FlashApplication()
			if not self.whisperDialogDict.has_key(name):
				btn = self.__FindWhisperButton(name)
				if 0 == btn:
					btn = self.__MakeWhisperButton(name)
					btn.Flash()

					chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.RECEIVE_MESSAGE % (name))

				else:
					btn.Flash()
			elif self.IsGameMasterName(name):
				dlg = self.whisperDialogDict[name]
				dlg.SetGameMasterLook()
	
	def MakeWhisperButton(self, name):
		self.__MakeWhisperButton(name)

	if app.BL_REMOTE_SHOP:
		def OpenRemoteShop(self):
			if self.wndRemoteShop:
				if self.wndRemoteShop.IsShowWindow():				
					self.wndRemoteShop.Close()
				else:
					self.wndRemoteShop.Show()

	if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
		def SetInterfaceFlag(self, name, language, empire):
			if self.whisperDialogDict.has_key(name):
				self.whisperDialogDict[name].SetFlag(language, empire)
			else:
				btn = self.__FindWhisperButton(name)
				if btn != 0:
					btn.languageID = language
					btn.empireID = empire

	## 버튼을 눌렀을때 창을 여는 함수
	if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
		def ShowWhisperDialog(self, btn):
			try:
				self.__MakeWhisperDialog(btn.name)
				dlgWhisper = self.whisperDialogDict[btn.name]
				dlgWhisper.OpenWithTarget(btn.name)
				if btn.languageID != "" and btn.empireID != "":
					dlgWhisper.SetFlag(btn.languageID, btn.empireID)
				dlgWhisper.Show()
				self.__CheckGameMaster(btn.name)
			except:
				import dbg
				dbg.TraceError("interface.ShowWhisperDialog - Failed to find key#11111")
			self.__DestroyWhisperButton(btn)
	else:
		def ShowWhisperDialog(self, btn):
			try:
				self.__MakeWhisperDialog(btn.name)
				dlgWhisper = self.whisperDialogDict[btn.name]
				dlgWhisper.OpenWithTarget(btn.name)
				dlgWhisper.Show()
				self.__CheckGameMaster(btn.name)
			except:
				import dbg
				dbg.TraceError("interface.ShowWhisperDialog - Failed to find key")

			## 버튼 초기화
			self.__DestroyWhisperButton(btn)

	## WhisperDialog 창에서 최소화 명령을 수행했을때 호출되는 함수
	## 창을 최소화 합니다.
	if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
		def MinimizeWhisperDialog(self, name, languageID, empireID):
			if 0 != name:
				self.__MakeWhisperButton(name, languageID, empireID)
			self.CloseWhisperDialog(name)
	else:
		def MinimizeWhisperDialog(self, name):

			if 0 != name:
				self.__MakeWhisperButton(name)

			self.CloseWhisperDialog(name)


	def CloseWhisperDialog(self, name):
		if 0 == name:

			if self.dlgWhisperWithoutTarget:
				self.dlgWhisperWithoutTarget.Destroy()
				self.dlgWhisperWithoutTarget = None

			return

		try:
			dlgWhisper = self.whisperDialogDict[name]
			dlgWhisper.Destroy()
			del self.whisperDialogDict[name]
		except:
			import dbg
			dbg.TraceError("interface.CloseWhisperDialog - Failed to find key")
				
	## 버튼의 개수가 바뀌었을때 버튼을 재정렬 하는 함수
	def __ArrangeWhisperButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		xPos = screenWidth - 70
		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63
		#yCount = (screenHeight - 285) / 63

		count = 0
		for button in self.whisperButtonList:

			button.SetPosition(xPos + (int(count/yCount) * -50), yPos + (count%yCount * 63))
			count += 1

	## 이름으로 Whisper 버튼을 찾아 리턴해 주는 함수
	## 버튼은 딕셔너리로 하지 않는 것은 정렬 되어 버려 순서가 유지 되지 않으며
	## 이로 인해 ToolTip들이 다른 버튼들에 의해 가려지기 때문이다.
	def __FindWhisperButton(self, name):
		for button in self.whisperButtonList:
			if button.name == name:
				return button

		return 0

	## 창을 만듭니다.
	def __MakeWhisperDialog(self, name):
		dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
		dlgWhisper.BindInterface(self)
		dlgWhisper.LoadDialog()
		dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
		self.whisperDialogDict[name] = dlgWhisper

		self.windowOpenPosition = (self.windowOpenPosition+1) % 5

		return dlgWhisper

	## 버튼을 만듭니다.
	if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
		def __MakeWhisperButton(self, name, languageID = "", empireID = ""):
			whisperButton = uiWhisper.WhisperButton()
			whisperButton.SetUpVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			whisperButton.SetOverVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			whisperButton.SetDownVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			if self.IsGameMasterName(name):
				whisperButton.SetToolTipTextWithColor(name, 0xffffa200)
			else:
				whisperButton.SetToolTipText(name)
			whisperButton.ToolTipText.SetHorizontalAlignCenter()
			whisperButton.SetEvent(ui.__mem_func__(self.ShowWhisperDialog), whisperButton)
			whisperButton.Show()
			whisperButton.name = name
			whisperButton.languageID = languageID
			whisperButton.empireID = empireID
			self.whisperButtonList.insert(0, whisperButton)
			self.__ArrangeWhisperButton()
			return whisperButton
	else:
		def __MakeWhisperButton(self, name):
			whisperButton = uiWhisper.WhisperButton()
			whisperButton.SetUpVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			whisperButton.SetOverVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			whisperButton.SetDownVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			if self.IsGameMasterName(name):
				whisperButton.SetToolTipTextWithColor(name, 0xffffa200)
			else:
				whisperButton.SetToolTipText(name)
			whisperButton.ToolTipText.SetHorizontalAlignCenter()
			whisperButton.SetEvent(ui.__mem_func__(self.ShowWhisperDialog), whisperButton)
			whisperButton.Show()
			whisperButton.name = name

			self.whisperButtonList.insert(0, whisperButton)
			self.__ArrangeWhisperButton()

			return whisperButton

	def __DestroyWhisperButton(self, button):
		button.SetEvent(0)
		self.whisperButtonList.remove(button)
		self.__ArrangeWhisperButton()

	def HideAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Hide()

	if app.__BL_SOUL_ROULETTE__:
		def Roulette_Open(self, price):
			if self.wndMiniGameRoulette:
				self.wndMiniGameRoulette.Show(price)
		def Roulette_Close(self):
			if self.wndMiniGameRoulette:
				self.wndMiniGameRoulette.Hide()
		def Roulette_TurnWheel(self, spin, i):
			if self.wndMiniGameRoulette:
				self.wndMiniGameRoulette.TurnWheel(spin, i)
		def Roulette_SetIcons(self, i, vnum, count):
			if self.wndMiniGameRoulette:
				self.wndMiniGameRoulette.SetSlotItem(i, vnum, count)

	def ShowAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Show()

	def __CheckGameMaster(self, name):
		if not self.listGMName.has_key(name):
			return
		if self.whisperDialogDict.has_key(name):
			dlg = self.whisperDialogDict[name]
			dlg.SetGameMasterLook()

	def RegisterGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return
		self.listGMName[name] = "GM"

	def IsGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return True
		else:
			return False

	if app.ENABLE_EVENT_MANAGER:
		def MakeEventIcon(self):
			if self.wndEventIcon == None:
				self.wndEventIcon = uiEventCalendar.MovableImage()
				self.wndEventIcon.Show()
		def MakeEventCalendar(self):
			if self.wndEventManager == None:
				self.wndEventManager = uiEventCalendar.EventCalendarWindow()
		def OpenEventCalendar(self):
			self.MakeEventCalendar()
			if self.wndEventManager.IsShow():
				self.wndEventManager.Close()
			else:
				self.wndEventManager.Open()
		def AppendEvent(self, dayIndex, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3, startRealTime, endRealTime, isAlreadyStart):
			self.MakeEventCalendar()
			if self.wndEventManager:
				self.wndEventManager.AppendEvent(dayIndex, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3)

			self.MakeEventIcon()
			self.wndEventIcon.AppendEvent(eventIndex,startRealTime, endRealTime, isAlreadyStart)

	#####################################################################################

	#####################################################################################
	### Guild Building ###

	def BUILD_OpenWindow(self):
		self.wndGuildBuilding = uiGuild.BuildGuildBuildingWindow()
		self.wndGuildBuilding.Open()
		self.wndGuildBuilding.wnds = self.__HideWindows()
		self.wndGuildBuilding.SetCloseEvent(ui.__mem_func__(self.BUILD_CloseWindow))

	def BUILD_CloseWindow(self):
		self.__ShowWindows(self.wndGuildBuilding.wnds)
		self.wndGuildBuilding = None

	def BUILD_OnUpdate(self):
		if not self.wndGuildBuilding:
			return

		if self.wndGuildBuilding.IsPositioningMode():
			import background
			x, y, z = background.GetPickingPoint()
			self.wndGuildBuilding.SetBuildingPosition(x, y, z)
			
	def BUILD_OnMouseLeftButtonDown(self):
		if not self.wndGuildBuilding:
			return

		# GUILD_BUILDING
		if self.wndGuildBuilding.IsPositioningMode():
			self.wndGuildBuilding.SettleCurrentPosition()
			return True
		elif self.wndGuildBuilding.IsPreviewMode():
			pass
		else:
			return True
		# END_OF_GUILD_BUILDING
		return False

	def BUILD_OnMouseLeftButtonUp(self):
		if not self.wndGuildBuilding:
			return

		if not self.wndGuildBuilding.IsPreviewMode():
			return True

		return False

	def BULID_EnterGuildArea(self, areaID):
		# GUILD_BUILDING
		mainCharacterName = player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()

		if mainCharacterName != masterName:
			return

		if areaID != player.GetGuildID():
			return
		# END_OF_GUILD_BUILDING

		self.wndGameButton.ShowBuildButton()

	def BULID_ExitGuildArea(self, areaID):
		self.wndGameButton.HideBuildButton()

	if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
		def OpenPrivateShopSearch(self, type):
			self.wndPrivateShopSearch.Open(type)
			
		def RefreshShopSearch(self):
			self.wndPrivateShopSearch.RefreshMe()
			self.wndPrivateShopSearch.RefreshList()	
		
		def RefreshRequest(self):
			self.wndPrivateShopSearch.RefreshRequest()
	
	def IsPickUpItem(self):
		return self.wndInventory.IsPickUpItem()

	if constInfo.ENABLE_SHOW_CHEST_DROP:
		def MakeChestDrop(self):
			import uiChestDrop
			self.dlgChestDrop = uiChestDrop.ChestDropWindow()
			self.dlgChestDrop.SetItemToolTip(self.tooltipItem)	

	#####################################################################################

	def IsEditLineFocus(self):
		if self.ChatWindow.chatLine.IsFocus():
			return 1

		if self.ChatWindow.chatToLine.IsFocus():
			return 1

		return 0

	def EmptyFunction(self):
		pass

	def GetInventoryPageIndex(self):
		if self.wndInventory:
			return self.wndInventory.GetInventoryPageIndex()
		else:
			return -1

		def RankingClearData(self):
			if self.wndRanking:
				self.wndRanking.ClearData()

		def RankingAddRank(self, position, level, points, name, realPosition):
			if self.wndRanking:
				self.wndRanking.AddRank(position, name, points, level, realPosition)

		def RankingRefresh(self):
			if self.wndRanking:
				self.wndRanking.RefreshList()
				self.wndRanking.OnScroll()

	if app.WJ_ENABLE_TRADABLE_ICON:
		def SetOnTopWindow(self, onTopWnd):
			self.onTopWindow = onTopWnd

		def GetOnTopWindow(self):
			return self.onTopWindow

		def RefreshMarkInventoryBag(self):
			self.wndInventory.RefreshMarkSlots()

			if app.BL_MAILBOX:
				if self.wndDragonSoul and self.wndDragonSoul.IsShow():
					self.wndDragonSoul.RefreshBagSlotWindow()

	if app.ENABLE_NEW_FISHING_SYSTEM:
		def OnFishingStart(self, have, need):
			if self.wndFishingWindow and not self.wndFishingWindow.IsShow():
				self.wndFishingWindow.OnOpen(have, need)

		def OnFishingStop(self):
			if self.wndFishingWindow and self.wndFishingWindow.IsShow():
				self.wndFishingWindow.OnClose()

		def OnFishingCatch(self, have):
			if self.wndFishingWindow and self.wndFishingWindow.IsShow():
				self.wndFishingWindow.OnCatch(have)

		def OnFishingCatchFailed(self):
			if self.wndFishingWindow and self.wndFishingWindow.IsShow():
				self.wndFishingWindow.OnCatchFailed()


	if app.INGAME_WIKI:
		def ToggleWikiNew(self):
			import net
			net.ToggleWikiWindow()

	if app.ENABLE_DSS_ACTIVE_EFFECT_BUTTON:
		def UseDSSButtonEffect(self, enable):
			if self.wndTaskBar:
				self.wndTaskBar.UseDSSButtonEffect(enable)

	if app.GUILD_WAR_COUNTER:
		def __MakeGuildWar(self):
			uiGuildWar.MAIN_VID = player.GetName()
			uiGuildWar.CURRENT_VID = ""
			if self.wndGuildWar == None:
				self.wndGuildWar = uiGuildWar.GuildWarStatic()

		def OpenGuildWarStatics(self):
			self.__MakeGuildWar()
			if self.wndGuildWar.IsShow():
				self.wndGuildWar.Hide()
			else:
				self.wndGuildWar.SetCenterPosition()
				self.wndGuildWar.Open()
		def SetStaticsStatus(self):
			if self.wndGuildWar:
				self.wndGuildWar.SetStaticsStatus()
		def GuildWarStaticsUpdate(self):
			if self.wndGuildWar:
				self.wndGuildWar.Update()
		def GuildWarStaticsClear(self):
			if self.wndGuildWar:
				self.wndGuildWar.Clear()
		def GuildWarStaticsSpecial(self, pid, sub_index):
			if self.wndGuildWar:
				self.wndGuildWar.GuildWarStaticsSpecial(pid, sub_index)
		if app.__IMPROVED_GUILD_WAR__:
			def GuildWarStaticSetGuildID(self, firstID, secondID, iMaxPlayer, iMaxScore, flags):
				self.__MakeGuildWar()
				if self.wndGuildWar:
					self.wndGuildWar.SetGuildID(int(firstID), int(secondID), int(iMaxPlayer), int(iMaxScore), int(flags))
		else:
			def GuildWarStaticSetGuildID(self, firstID, secondID):
				self.__MakeGuildWar()
				if self.wndGuildWar:
					self.wndGuildWar.SetGuildID(int(firstID), int(secondID))
		def GuildWarStaticSetUser(self, id0, user0, id1, user1, observer):
			if self.wndGuildWar:
				self.wndGuildWar.SetUser(id0, user0, id1, user1, observer)

		def GuildWarStaticSetScore(self, id0, id1, score):
			if self.wndGuildWar:
				self.wndGuildWar.SetScore(id0, id1, score)

		def UpdateObserverCount(self, observer):
			if self.wndGuildWar:
				self.wndGuildWar.UpdateObserverCount(observer)

		def MakeCSMessage(self):
			if self.wndGuildWarCSMsg == None:
				self.wndGuildWarCSMsg = uiGuildWar.MessageQueue()
				self.wndGuildWarCSMsg.Show()

		#def AddCSMessage(self, killerName, killerRace, victimName, victimRace):
			#self.MakeCSMessage()
			#if self.wndGuildWarCSMsg:
				#self.wndGuildWarCSMsg.OnMessage(killerName, killerRace, victimName, victimRace)
				
		def __MakeGuildWarLog(self):
			uiGuildWar.MAIN_VID = player.GetName()
			uiGuildWar.CURRENT_VID = ""
			if self.wndGuildWarLog == None:
				self.wndGuildWarLog = uiGuildWar.GuildWarStaticLog()
				self.wndGuildWarLog.SetCenterPosition()
				self.wndGuildWarLog.SetTop()
		def OpenGuildWarLog(self):
			self.__MakeGuildWarLog()
			if self.wndGuildWarLog:
				if self.wndGuildWarLog.IsShow():
					self.wndGuildWarLog.Hide()
				else:
					self.wndGuildWarLog.Open()

		def GuildWarStatisticsEvent(self):
			self.__MakeGuildWarLog()
			if self.wndGuildWarLog:
				self.wndGuildWarLog.RunEvent()
				
	if app.ENABLE_RENEWAL_PVP:
		def MakePvPWindow(self):
			if self.wndPvP == None:
				self.wndPvP = uiPvP.PvPWindow()
		def OpenPvPFirst(self, playerName, playerVID):
			self.MakePvPWindow()
			self.wndPvP.OpenFirst(playerName, playerVID)
		def OpenPvPSecond(self, playerName, playerVID, data):
			pvpData = {}
			if len(data) > 0:
				try:
					dataSplit = data.split("#")
					if len(dataSplit) == 0:
						return
					del dataSplit[0]
					for j in xrange(len(dataSplit)):
						if j == player.PVP_BET:
							pvpData[player.PVP_BET] = long(dataSplit[j])
						else:
							if dataSplit[j] == "1":
								pvpData[j] = True
							else:
								pvpData[j] = False
				except:
					pass
			self.MakePvPWindow()
			self.wndPvP.OpenSecond(playerName, playerVID, pvpData)

	if app.ENABLE_ANTI_MULTIPLE_FARM:
		def ToggleAntiMultipleFarmWindow(self):
			if not self.wndAntiMultipleFarm:
				return
			
			if anti_multiple_farm.GetAntiFarmPlayerCount() <= anti_multiple_farm.MULTIPLE_FARM_MAX_ACCOUNT:
				try:
					self.wndPopupDialog.SetText(localeInfo.ANTI_MULTIPLE_FARM_MESSAGE.format(anti_multiple_farm.MULTIPLE_FARM_MAX_ACCOUNT+1))
					self.wndPopupDialog.Open()
				except:
					self.wndPopupDialog = uiCommon.PopupDialog()
					self.wndPopupDialog.SetText(localeInfo.ANTI_MULTIPLE_FARM_MESSAGE.format(anti_multiple_farm.MULTIPLE_FARM_MAX_ACCOUNT+1))
					self.wndPopupDialog.Open()
				return
			
			isShow = self.wndAntiMultipleFarm.IsShow()
			self.wndAntiMultipleFarm.Close() if isShow else self.wndAntiMultipleFarm.Open()
		
		def SendAntiFarmReload(self):
			if self.wndTaskBar:
				self.wndTaskBar.ReloadAntiMultipleFarmState()
			
			if self.wndAntiMultipleFarm.IsShow():
				self.wndAntiMultipleFarm.OnRefreshData()

				if self.wndAntiMultipleFarm.page_manage_mode != self.wndAntiMultipleFarm.VIEW_MODE:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ANTI_MULTIPLE_FARM_REFRESHED)
		
		def RegistItemGive(self, itemVnum, itemCount):
			if not self.wndGiveItem:
				return
			
			self.wndGiveItem.Open(itemVnum, itemCount)


	if app.BL_MAILBOX:
		def MailBoxProcess(self, type, data):
			if not self.mail_box:
				return
				
			self.mail_box.MailBoxProcess( type, data )
			
		def MiniMapMailProcess(self, type, data):
			if not self.wndMiniMap:
				return
				
			self.wndMiniMap.MiniMapMailProcess(type, data)

		def MarkUnusableDSInvenSlotOnTopWnd(self, onTopWnd, index, window):
			if onTopWnd == player.ON_TOP_WND_MAILBOX and self.mail_box and self.mail_box.CantPostItemSlot(index, window):
				return True
				
			return False

	if app.ENABLE_GUILD_REQUEST:
		def MakeGuildRequest(self):
			if self.wndGuildRequest == None:
				self.wndGuildRequest = uiGuildRequest.GuildRequestWindow()
		def OpenGuildRequest(self):
			self.MakeGuildRequest()
			if self.wndGuildRequest.IsShow():
				self.wndGuildRequest.Close()
			else:
				self.wndGuildRequest.Open()
		def GuildRequestLoadName(self, tabIndex):
			self.MakeGuildRequest()
			self.wndGuildRequest.GuildRequestLoadName(int(tabIndex))
		def GuildRequestLoadPage(self, tabIndex, pageIndex, maxPage):
			self.MakeGuildRequest()
			self.wndGuildRequest.GuildRequestLoadPage(int(tabIndex), int(pageIndex), int(maxPage))
		def GuildRequestSetItem(self, index, g_id, name, level, ladder_point, membercount, maxmember, isRequest):
			self.MakeGuildRequest()
			self.wndGuildRequest.GuildRequestSetItem(index, g_id, name, level, ladder_point, membercount, maxmember, isRequest)
		def GuildRequestSetRequest(self, index, pid, name, level, race, skillIndex):
			self.MakeGuildRequest()
			self.wndGuildRequest.GuildRequestSetRequest(index, pid, name, level, race, skillIndex)	
	
if __name__ == "__main__":

	import app
	import wndMgr
	import systemSetting
	import mouseModule
	import grp
	import ui
	import localeInfo

	app.SetMouseHandler(mouseModule.mouseController)
	app.SetHairColorEnable(True)
	wndMgr.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetScreenSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	app.Create(localeInfo.APP_TITLE, systemSetting.GetWidth(), systemSetting.GetHeight(), 1)
	mouseModule.mouseController.Create()

	class TestGame(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)

			localeInfo.LoadLocaleData()
			player.SetItemData(0, 27001, 10)
			player.SetItemData(1, 27004, 10)

			self.interface = Interface()
			self.interface.MakeInterface()
			self.interface.ShowDefaultWindows()
			self.interface.RefreshInventory()
			#self.interface.OpenCubeWindow()

		def __del__(self):
			ui.Window.__del__(self)

		def OnUpdate(self):
			app.UpdateGame()

		def OnRender(self):
			app.RenderGame()
			grp.PopState()
			grp.SetInterfaceRenderState()

	game = TestGame()
	game.SetSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	game.Show()

	app.Loop()
