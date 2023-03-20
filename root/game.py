import os
import app
import dbg
import grp
import item
import background
import chr
import chrmgr
import player
import snd
import chat
import teleport_system
import textTail
import snd
import net
import effect
import wndMgr
import fly
import systemSetting
import uiPopup
import time
import quest
import guild
import uifastequip
import skill
import messenger
import localeInfo
import constInfo
import exchange
import ime
import uiScriptLocale
import ui
import uiCommon
import uiPhaseCurtain
import uiMapNameShower
import uiAffectShower
import uiPlayerGauge
import uiCharacter
import uiTarget
import safebox
if app.ENABLE_DEFENSAWESHIP:
	import uiShipMastHP
# PRIVATE_SHOP_PRICE_LIST
import uiPrivateShopBuilder
# END_OF_PRIVATE_SHOP_PRICE_LIST

import mouseModule
import consoleModule
import localeInfo

import playerSettingModule
import interfaceModule
if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
	from uispecialStorage import SpecialStorageWindow
import musicInfo
import debugInfo
import uipetsystem
import skybox_system
import stringCommander
import uimarbleshop
import binascii
#Mental Bonus
import uiBonusPage
###################

from _weakref import proxy
# BEGIN_OFFLINE_SHOP
if app.ENABLE_OFFLINE_SHOP_SYSTEM:
	import uiOfflineShopBuilder
	import uiOfflineShop
# END_OF_OFFLINE_SHOP								  

# TEXTTAIL_LIVINGTIME_CONTROL
#if localeInfo.IsJAPAN():
#	app.SetTextTailLivingTime(8.0)
# END_OF_TEXTTAIL_LIVINGTIME_CONTROL

# SCREENSHOT_CWDSAVE
SCREENSHOT_CWDSAVE = False
SCREENSHOT_DIR = None
if app.GUILD_WAR_COUNTER:
	import uiGuildWarData
	
if localeInfo.IsEUROPE():
	SCREENSHOT_CWDSAVE = True

if localeInfo.IsCIBN10():
	SCREENSHOT_CWDSAVE = False
	SCREENSHOT_DIR = "YT2W"

cameraDistance = 1550.0
cameraPitch = 27.0
cameraRotation = 0.0
cameraHeight = 100.0

testAlignment = 0
# PROFESSIONAL_BIOLOG_SYSTEM
if app.ENABLE_BIOLOG_SYSTEM:
	import uiprofessionalbiolog
# END_OF_PROFESSIONAL_BIOLOG_SYSTEM	
class GameWindow(ui.ScriptWindow):
	def __init__(self, stream):
		if constInfo.ENABLE_MULTI_RANKING:
			self.rankingWindow =None
		ui.ScriptWindow.__init__(self, "GAME")
		import dailygift
		self.wnddailygift = dailygift.DailyGift() 
		self.SetWindowName("game")
		if constInfo.ENABLE_NEW_DROP_ITEM:
			self.itemDropQuestionDialog=None
		net.SetPhaseWindow(net.PHASE_WINDOW_GAME, self)
		player.SetGameWindow(self)
		if app.ENABLE_DEFENSAWESHIP:
			self.wndShipMastHP = uiShipMastHP.ShipMastHP()
			self.wndShipMastHP.Close()

		self.quickSlotPageIndex = 0
		self.lastPKModeSendedTime = 0
		self.pressNumber = None

		self.guildWarQuestionDialog = None
		self.interface = None
		self.targetBoard = None
		if app.ENABLE_SHIP_DEFENSE:
			self.allyTargetBoard = None
		self.console = None
		self.mapNameShower = None
		self.affectShower = None
		self.playerGauge = None
		self.stream=stream
		self.interface = interfaceModule.Interface()
		if app.ENABLE_GUILD_REQUEST:
			constInfo.SetInterfaceInstance(self.interface)
		if app.ENABLE_EVENT_MANAGER:
			constInfo.SetInterfaceInstance(self.interface)
		constInfo.SetInterfaceInstance(self.interface)
		self.interface.SetStream(self.stream)
		self.interface.MakeInterface()
		self.interface.ShowDefaultWindows()
		self.interface.Bind(self)
		self.stream.isAutoSelect = 0

		self.curtain = uiPhaseCurtain.PhaseCurtain()
		self.curtain.speed = 0.03
		self.curtain.Hide()
		self.teleportsystem = teleport_system.teleportwindow()
		self.skyboxsystem = skybox_system.MentaLGui()
		
		self.interface.wndMiniMap.SAFE_SetHideEvent(self.__HideSpecial)
		self.interface.wndMiniMap.SAFE_SetShowEvent(self.__ShowSpecial)

		if app.ENABLE_SHIP_DEFENSE:
			self.allyTargetBoard = uiTarget.AllianceTargetBoard()
			self.allyTargetBoard.Hide()
			self.interface.SetAllianceTargetBoard(self.allyTargetBoard)

		self.targetBoard = uiTarget.TargetBoard()
		self.targetBoard.SetWhisperEvent(ui.__mem_func__(self.interface.OpenWhisperDialog))
		self.targetBoard.Hide()
		if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
			self.uispecialStorage = SpecialStorageWindow()
			self.uispecialStorage.Hide()
		self.petmain = uipetsystem.PetSystemMain()
		self.petmini = uipetsystem.PetSystemMini()
		self.console = consoleModule.ConsoleWindow()
		self.console.BindGameClass(self)
		self.console.SetConsoleSize(wndMgr.GetScreenWidth(), 200)
		self.console.Hide()

		self.mapNameShower = uiMapNameShower.MapNameShower()
		self.affectShower = uiAffectShower.AffectShower()
		self.wndMarbleShop = uimarbleshop.MarbleShopWindow()				
		self.playerGauge = uiPlayerGauge.PlayerGauge(self)
		self.playerGauge.Hide()      

		#wj 2014.1.2. ESC키를 누를 시 우선적으로 DropQuestionDialog를 끄도록 만들었다. 하지만 처음에 itemDropQuestionDialog가 선언되어 있지 않아 ERROR가 발생하여 init에서 선언과 동시에 초기화 시킴.
		self.itemDropQuestionDialog = None

		self.__SetQuickSlotMode()

		self.__ServerCommand_Build()
		self.__ProcessPreservedServerCommand()
		self.isCameraMoving = False
		self.cameraMovementProgress = 0.0
		
		self.pingLine = None
		if app.ENABLE_PINGTIME:
			self.pingLine = ui.TextLine()
			self.pingLine.SetFontName(localeInfo.UI_DEF_FONT)
#			self.pingLine.SetFontColor(1.0,1.0,1.0)
			self.pingLine.SetPosition((wndMgr.GetScreenWidth() - 180) / 2, 160)		
		
		self.timeLine = ui.TextLine()
		self.timeLine.SetFontName(localeInfo.UI_DEF_FONT)
		self.timeLine.SetPosition((wndMgr.GetScreenWidth() - 83) / 1, 150)
		
		import uiPickupFilter
		self.PickupFilter = uiPickupFilter.PickupFilter()
		self.PickupFilter.Hide()

	if app.ENABLE_KILL_STATISTICS:
		def ReceiveKillStatisticsPacket(self, j, sh, ch, t, td, dw, dl, b, st):
			constInfo.KILL_STATISTICS_DATA = [int(j), int(sh), int(ch), int(t), int(td), int(dw), int(dl), int(b), int(st),]

	def __del__(self):
		player.SetGameWindow(0)
		net.ClearPhaseWindow(net.PHASE_WINDOW_GAME, self)
		ui.ScriptWindow.__del__(self)
	
	def	__EnablePickUpItem(self):
		if self.PickupFilter.IsShow():
			self.PickupFilter.Hide()
		else:
			self.PickupFilter.Show()
			self.PickupFilter.SetCenterPosition()
			self.PickupFilter.SetTop()
			
	if app.INGAME_WIKI:
		def ToggleWikiWindow(self):
			if not self.wndWiki:
				return
			
			if self.wndWiki.IsShow():
				self.wndWiki.Hide()
			else:
				self.wndWiki.Show()
				self.wndWiki.SetTop()


	def Open(self):
		app.SetFrameSkip(1)
		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		#self.daily_reward = ui.Button()
		#self.daily_reward.SetParent(self)
		#self.daily_reward.SetPosition(wndMgr.GetScreenWidth()-188,80)
		#self.daily_reward.SetUpVisual("icon/giftsystem/prize1.png")
		#self.daily_reward.SetOverVisual("icon/giftsystem/prize2.png")
		#self.daily_reward.SetDownVisual("icon/giftsystem/prize3.png")
		#self.daily_reward.SetToolTipText("Ricompensa")
		#self.daily_reward.SetEvent(lambda : self.ManagerGiftSystem("Show|"))
		#self.daily_reward.FlashEx()
		#self.daily_reward.Show()

		self._timeLine_hide = False
		
		self.__BuildKeyDict()
		self.__BuildDebugInfo()
		
		self.quickSlotPageIndex = 0
		self.PickingCharacterIndex = -1
		self.PickingItemIndex = -1
		self.consoleEnable = False
		self.isShowDebugInfo = False
		self.ShowNameFlag = False
		## Battlepass
		self.battlepass_button = ui.Button()
		self.battlepass_button.SetParent(self)
		self.battlepass_button.SetPosition(wndMgr.GetScreenWidth()-116,175)
		self.battlepass_button.SetUpVisual("d:/ymir work/battle_pass/open_battlepass1.tga")
		self.battlepass_button.SetOverVisual("d:/ymir work/battle_pass/open_battlepass2.tga")
		self.battlepass_button.SetDownVisual("d:/ymir work/battle_pass/open_battlepass3.tga")
		self.battlepass_button.SetEvent(lambda : net.SendChatPacket("/open_battlepass"))

		self.enableXMasBoom = False
		self.startTimeXMasBoom = 0.0
		self.indexXMasBoom = 0

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight

		app.SetCamera(cameraDistance, cameraPitch, cameraRotation, cameraHeight)

		constInfo.SET_DEFAULT_CAMERA_MAX_DISTANCE()
		constInfo.SET_DEFAULT_CHRNAME_COLOR()
		constInfo.SET_DEFAULT_FOG_LEVEL()
		constInfo.SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE()
		constInfo.SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS()
		constInfo.SET_DEFAULT_USE_SKILL_EFFECT_ENABLE()

		# TWO_HANDED_WEAPON_ATTACK_SPEED_UP
		constInfo.SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE()
		# END_OF_TWO_HANDED_WEAPON_ATTACK_SPEED_UP

		import event
		event.SetLeftTimeString(localeInfo.UI_LEFT_TIME)

		textTail.EnablePKTitle(constInfo.PVPMODE_ENABLE)

		if constInfo.PVPMODE_TEST_ENABLE:
			self.testPKMode = ui.TextLine()
			self.testPKMode.SetFontName(localeInfo.UI_DEF_FONT)
			self.testPKMode.SetPosition(0, 15)
			self.testPKMode.SetWindowHorizontalAlignCenter()
			self.testPKMode.SetHorizontalAlignCenter()
			self.testPKMode.SetFeather()
			self.testPKMode.SetOutline()
			self.testPKMode.Show()

			self.testAlignment = ui.TextLine()
			self.testAlignment.SetFontName(localeInfo.UI_DEF_FONT)
			self.testAlignment.SetPosition(0, 35)
			self.testAlignment.SetWindowHorizontalAlignCenter()
			self.testAlignment.SetHorizontalAlignCenter()
			self.testAlignment.SetFeather()
			self.testAlignment.SetOutline()
			self.testAlignment.Show()

		self.__BuildKeyDict()
		self.__BuildDebugInfo()

		# PRIVATE_SHOP_PRICE_LIST
		uiPrivateShopBuilder.Clear()
		# END_OF_PRIVATE_SHOP_PRICE_LIST
		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			uiOfflineShopBuilder.Clear()
		# END_OF_PRIVATE_SHOP_PRICE_LIST
		# UNKNOWN_UPDATE
		exchange.InitTrading()
		# END_OF_UNKNOWN_UPDATE


		## Sound
		snd.SetMusicVolume(systemSetting.GetMusicVolume()*net.GetFieldMusicVolume())
		snd.SetSoundVolume(systemSetting.GetSoundVolume())

		netFieldMusicFileName = net.GetFieldMusicFileName()
		if netFieldMusicFileName:
			snd.FadeInMusic("BGM/" + netFieldMusicFileName)
		elif musicInfo.fieldMusic != "":
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

		self.__SetQuickSlotMode()
		self.__SelectQuickPage(self.quickSlotPageIndex)

		self.SetFocus()
		self.Show()
		app.ShowCursor()

		net.SendEnterGamePacket()
		if app.ENABLE_DEFENSAWESHIP:
			if background.GetCurrentMapName() == "defensawe_hydra":
				self.__ShipMastHPShow()

		curLang = systemSetting.GetTransLangKey()
		if curLang not in constInfo.AVAILABLE_LANGUAGES:
			localeName = app.GetLocaleName()
			if localeName in constInfo.AVAILABLE_LANGUAGES:
				systemSetting.SetTransLangKey(localeName)
			else:
				langKey = list(constInfo.AVAILABLE_LANGUAGES)[0]
				systemSetting.SetTransLangKey(langKey)

		# START_GAME_ERROR_EXIT
		try:
			self.StartGame()
		except:
			import exception
			exception.Abort("GameWindow.Open")
		# END_OF_START_GAME_ERROR_EXIT

		# NPC가 큐브시스템으로 만들 수 있는 아이템들의 목록을 캐싱
		# ex) cubeInformation[20383] = [ {"rewordVNUM": 72723, "rewordCount": 1, "materialInfo": "101,1&102,2", "price": 999 }, ... ]
		self.cubeInformation = {}
		self.currentCubeNPC = 0
		self.isCameraMoving = True
		self.cameraMovementProgress = 0.0

		if app.INGAME_WIKI:
			import inGameWiki
			self.wndWiki = inGameWiki.InGameWiki()
			self.interface.dlgSystem.wikiWnd = proxy(self.wndWiki)

		if app.ENABLE_FOG_FIX:
			if systemSetting.IsFogMode():
				background.SetEnvironmentFog(True)
			else:
				background.SetEnvironmentFog(False)	

		#Mental Bonus
		self.BonusPageBoard = None
		##############
		
		if app.ENABLE_CHAT_COLOR_SYSTEM:
			if systemSetting.GetChatColor():
				systemSetting.SetChatColor(True)
				if not self.open_colors:
					return
				if constInfo.chat_color_page_open == 0:
					return False
				if arg == 1:
					constInfo.chat_color = "|cFFff1a1a|H|h"
				if arg == 2:
					constInfo.chat_color = "|cFF00ffe4|H|h"
				if arg == 3:
					constInfo.chat_color = "|cFF33ff33|H|h"
				if arg == 4:
					constInfo.chat_color = "|cFFFFF200|H|h"
				if arg == 5:
					constInfo.chat_color = "|cFFFF62FF|H|h"
				if arg == 6:
					constInfo.chat_color = "|cFFFF7F27|H|h"
				if arg == 7:
					constInfo.chat_color = "|cFFff9966|H|h"
				if arg == 8:
					constInfo.chat_color = "|cFFbf80ff|H|h"
			else:
				if constInfo.chat_color_page_open == 0:
					return False
		
	def Close(self):
		self.Hide()
		if app.ENABLE_DEFENSAWESHIP:
			if self.wndShipMastHP:
				self.wndShipMastHP.Close()
				self.wndShipMastHP=0
		constInfo.py_Flag.clear()

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight
		(cameraDistance, cameraPitch, cameraRotation, cameraHeight) = app.GetCamera()

		if musicInfo.fieldMusic != "":
			snd.FadeOutMusic("BGM/"+ musicInfo.fieldMusic)

		self.onPressKeyDict = None
		self.onClickKeyDict = None

		chat.Close()
		snd.StopAllSound()
		grp.InitScreenEffect()
		chr.Destroy()
		textTail.Clear()
		quest.Clear()
		background.Destroy()
		guild.Destroy()
		messenger.Destroy()
		skill.ClearSkillData()
		wndMgr.Unlock()
		systemSetting.SaveConfig()
		mouseModule.mouseController.DeattachObject()

		# if self.rankingWindow:
			# self.rankingWindow.Hide()
			# self.rankingWindow = None

		if self.guildWarQuestionDialog:
			self.guildWarQuestionDialog.Close()

		self.guildNameBoard = None
		self.partyRequestQuestionDialog = None
		self.partyInviteQuestionDialog = None
		self.guildInviteQuestionDialog = None
		self.guildWarQuestionDialog = None
		self.messengerAddFriendQuestion = None
		if app.INGAME_WIKI:
			if self.wndWiki:
				self.wndWiki.Hide()
				self.wndWiki = None
		# UNKNOWN_UPDATE
		self.itemDropQuestionDialog = None
		# END_OF_UNKNOWN_UPDATE

		# QUEST_CONFIRM
		self.confirmDialog = None
		# END_OF_QUEST_CONFIRM
		self.PrintCoord = None
		self.FrameRate = None
		self.Pitch = None
		self.Splat = None
		self.TextureNum = None
		self.ObjectNum = None
		self.ViewDistance = None
		self.PrintMousePos = None

		self.ClearDictionary()
		self.petmain.Close()
		self.petmini.Close()
		self.teleportsystem.Close()
		self.skyboxsystem.Close()

		self.playerGauge = None
		self.mapNameShower = None
		self.affectShower = None
		
		self.PickupFilter.Hide()
		self.PickupFilter=0

		if self.console:
			self.console.BindGameClass(0)
			self.console.Close()
			self.console=None
            

		if self.targetBoard:
			self.targetBoard.Destroy()
			self.targetBoard = None

		if app.ENABLE_SHIP_DEFENSE:
			if self.allyTargetBoard:
				self.allyTargetBoard.Destroy()
				self.allyTargetBoard = None
			
		if self.wndMarbleShop:
			self.wndMarbleShop.Hide()

		if self.interface:
			self.interface.HideAllWindows()
			self.interface.Close()
			self.interface=None

		if app.ENABLE_PINGTIME:
			self.pingLine = None

		player.ClearSkillDict()
		player.ResetCameraRotation()

		self.KillFocus()
		if app.ENABLE_GUILD_REQUEST:
			constInfo.SetInterfaceInstance(None)

		if app.ENABLE_EVENT_MANAGER:
			constInfo.SetInterfaceInstance(None)
		constInfo.SetInterfaceInstance(None)
		app.HideCursor()

		#Mental Bonus
		self.BonusPageBoard = None
		###########
		print "---------------------------------------------------------------------------- CLOSE GAME WINDOW"

	def __HideSpecial(self):
		if app.ENABLE_PINGTIME:
			self.pingLine.Hide()
		self._timeLine_hide = True
		self._timeLine_off()
		
	def __ShowSpecial(self):
		if app.ENABLE_PINGTIME:
			self.pingLine.Show()
		self._timeLine_hide = False
		
	def __BuildKeyDict(self):
		onPressKeyDict = {}

		##PressKey 는 누르고 있는 동안 계속 적용되는 키이다.

		## 숫자 단축키 퀵슬롯에 이용된다.(이후 숫자들도 퀵 슬롯용 예약)
		## F12 는 클라 디버그용 키이므로 쓰지 않는 게 좋다.
		onPressKeyDict[app.DIK_1]	= lambda : self.__PressNumKey(1)
		onPressKeyDict[app.DIK_2]	= lambda : self.__PressNumKey(2)
		onPressKeyDict[app.DIK_3]	= lambda : self.__PressNumKey(3)
		onPressKeyDict[app.DIK_4]	= lambda : self.__PressNumKey(4)
		onPressKeyDict[app.DIK_5]	= lambda : self.__PressNumKey(5)
		onPressKeyDict[app.DIK_6]	= lambda : self.__PressNumKey(6)
		onPressKeyDict[app.DIK_7]	= lambda : self.__PressNumKey(7)
		onPressKeyDict[app.DIK_8]	= lambda : self.__PressNumKey(8)
		onPressKeyDict[app.DIK_9]	= lambda : self.__PressNumKey(9)
		onPressKeyDict[app.DIK_F1]	= lambda : self.__PressQuickSlot(4)
		onPressKeyDict[app.DIK_F2]	= lambda : self.__PressQuickSlot(5)
		onPressKeyDict[app.DIK_F3]	= lambda : self.__PressQuickSlot(6)
		onPressKeyDict[app.DIK_F4]	= lambda : self.__PressQuickSlot(7)
		onPressKeyDict[app.DIK_F5]	= lambda : net.ToggleWikiWindow()
		onPressKeyDict[app.DIK_F5]	= lambda : self.interface.ToggleWikiNew()
		onPressKeyDict[app.DIK_F6]	= lambda : self.interface.ToggleSwitchbotWindow()
		onPressKeyDict[app.DIK_F7]	= lambda : self.interface.wndBio.OpenWindow()
		onPressKeyDict[app.DIK_F11]	= lambda : self.interface.wndFastEquip.Show()
		onPressKeyDict[app.DIK_F12]	= lambda : self.interface.OpenRanking()
			
		if app.GUILD_WAR_COUNTER:
			if background.GetCurrentMapName() == "metin2_map_t3":
				onPressKeyDict[app.DIK_TAB]	= lambda : self.OpenGuildWarStatics()
		
		onPressKeyDict[app.DIK_F8]	= lambda : self.__EnablePickUpItem()
		
		if app.ENABLE_DECORUM:
			onPressKeyDict[app.DIK_F9]	= lambda : self.__PressF9Key()
		onPressKeyDict[app.DIK_O]	= lambda : self.interface.ToggleDragonSoulWindowWithNoInfo()
		if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
			onPressKeyDict[app.DIK_U]		= lambda : self.interface.ToggleKeySpecialStorageWindow()

		onPressKeyDict[app.DIK_LALT]		= lambda : self.ShowName()
		onPressKeyDict[app.DIK_X]		= lambda : self.fuck_buttons()
		onPressKeyDict[app.DIK_LCONTROL]	= lambda : self.ShowMouseImage()
		onPressKeyDict[app.DIK_SYSRQ]		= lambda : self.SaveScreen()
		onPressKeyDict[app.DIK_SPACE]		= lambda : self.StartAttack()
		#onPressKeyDict[app.DIK_F11]	= lambda : self.OpenMarbleShop()
		#onPressKeyDict[app.DIK_F12]	= lambda : self.OpenRanking()
		#캐릭터 이동키
		onPressKeyDict[app.DIK_UP]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_DOWN]		= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_LEFT]		= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_RIGHT]		= lambda : self.MoveRight()
		onPressKeyDict[app.DIK_W]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_S]			= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_A]			= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_D]			= lambda : self.MoveRight()

		onPressKeyDict[app.DIK_E]			= lambda: app.RotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_R]			= lambda: app.ZoomCamera(app.CAMERA_TO_NEGATIVE)
		#onPressKeyDict[app.DIK_F]			= lambda: app.ZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_T]			= lambda: app.PitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_G]			= self.__PressGKey
		onPressKeyDict[app.DIK_Q]			= self.__PressQKey

		onPressKeyDict[app.DIK_NUMPAD9]		= lambda: app.MovieResetCamera()
		onPressKeyDict[app.DIK_NUMPAD4]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD6]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_PGUP]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_PGDN]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_NUMPAD8]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD2]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_GRAVE]		= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_Z]			= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_C]			= lambda state = "STATUS": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_V]			= lambda state = "SKILL": self.interface.ToggleCharacterWindow(state)
		#onPressKeyDict[app.DIK_B]			= lambda state = "EMOTICON": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_N]			= lambda state = "QUEST": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_I]			= lambda : self.interface.ToggleInventoryWindow()
		onPressKeyDict[app.DIK_O]			= lambda : self.interface.ToggleDragonSoulWindowWithNoInfo()
		onPressKeyDict[app.DIK_M]			= lambda : self.interface.PressMKey()
		#onPressKeyDict[app.DIK_H]			= lambda : self.interface.OpenHelpWindow()
		onPressKeyDict[app.DIK_ADD]			= lambda : self.interface.MiniMapScaleUp()
		onPressKeyDict[app.DIK_SUBTRACT]	= lambda : self.interface.MiniMapScaleDown()
		onPressKeyDict[app.DIK_L]			= lambda : self.interface.ToggleChatLogWindow()
		# onPressKeyDict[app.DIK_COMMA]		= lambda : self.ShowConsole()		# "`" key
		onPressKeyDict[app.DIK_LSHIFT]		= lambda : self.__SetQuickPageMode()

		onPressKeyDict[app.DIK_J]			= lambda : self.__PressJKey()
		onPressKeyDict[app.DIK_H]			= lambda : self.__PressHKey()
		onPressKeyDict[app.DIK_B]			= lambda : self.__PressBKey()
		onPressKeyDict[app.DIK_F]			= lambda : self.__PressFKey()
		
		
		self.onPressKeyDict = onPressKeyDict

		onClickKeyDict = {}
		onClickKeyDict[app.DIK_UP] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_DOWN] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_LEFT] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_RIGHT] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_SPACE] = lambda : self.EndAttack()

		onClickKeyDict[app.DIK_W] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_S] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_A] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_D] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_Q] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_E] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_R] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_F] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_T] = lambda: app.PitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_G] = lambda: self.__ReleaseGKey()
		onClickKeyDict[app.DIK_NUMPAD4] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD6] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGUP] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGDN] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD8] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD2] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_LALT] = lambda: self.HideName()
		onClickKeyDict[app.DIK_LCONTROL] = lambda: self.HideMouseImage()
		onClickKeyDict[app.DIK_LSHIFT] = lambda: self.__SetQuickSlotMode()
		onClickKeyDict[app.DIK_P] = lambda: self.OpenPetMainGui()
		

		#if constInfo.PVPMODE_ACCELKEY_ENABLE:
		#	onClickKeyDict[app.DIK_B] = lambda: self.ChangePKMode()

		self.onClickKeyDict=onClickKeyDict

	if constInfo.ENABLE_MULTI_RANKING:
		def OpenRanking(self):
			if self.rankingWindow ==None:
				import uirank
				self.rankingWindow = uirank.RankingGUI()
			self.rankingWindow.Open()
		def RankLevel(self, index, name, empire, value):
			constInfo.SetFlag("rank_level_name_%d"%index,name)
			constInfo.SetFlag("rank_level_empire_%d"%index,empire)
			constInfo.SetFlag("rank_level_value_%d"%index,value)
		def RankDestroyedStone(self, index, name, empire, value):
			constInfo.SetFlag("rank_stone_name_%d"%index,name)
			constInfo.SetFlag("rank_stone_empire_%d"%index,empire)
			constInfo.SetFlag("rank_stone_value_%d"%index,value)
		def RankKillMonster(self, index, name, empire, value):
			constInfo.SetFlag("rank_monster_name_%d"%index,name)
			constInfo.SetFlag("rank_monster_empire_%d"%index,empire)
			constInfo.SetFlag("rank_monster_value_%d"%index,value)
		def RankKillBoss(self, index, name, empire, value):
			constInfo.SetFlag("rank_boss_name_%d"%index,name)
			constInfo.SetFlag("rank_boss_empire_%d"%index,empire)
			constInfo.SetFlag("rank_boss_value_%d"%index,value)
		def RankCompletedDungeon(self, index, name, empire, value):
			constInfo.SetFlag("rank_dungeon_name_%d"%index,name)
			constInfo.SetFlag("rank_dungeon_empire_%d"%index,empire)
			constInfo.SetFlag("rank_dungeon_value_%d"%index,value)
		def RankPlaytime(self, index, name, empire, value):
			constInfo.SetFlag("rank_playtime_name_%d"%index,name)
			constInfo.SetFlag("rank_playtime_empire_%d"%index,empire)
			constInfo.SetFlag("rank_playtime_value_%d"%index,value)
		def RankGold(self, index, name, empire, value):
			constInfo.SetFlag("rank_gold_name_%d"%index,name)
			constInfo.SetFlag("rank_gold_empire_%d"%index,empire)
			constInfo.SetFlag("rank_gold_value_%d"%index,value)
		def RankGaya(self, index, name, empire, value):
			constInfo.SetFlag("rank_gaya_name_%d"%index,name)
			constInfo.SetFlag("rank_gaya_empire_%d"%index,empire)
			constInfo.SetFlag("rank_gaya_value_%d"%index,value)
		def RankCaughtFishes(self, index, name, empire, value):
			constInfo.SetFlag("rank_fish_name_%d"%index,name)
			constInfo.SetFlag("rank_fish_empire_%d"%index,empire)
			constInfo.SetFlag("rank_fish_value_%d"%index,value)
		def RankOpenedChest(self, index, name, empire, value):
			constInfo.SetFlag("rank_chest_name_%d"%index,name)
			constInfo.SetFlag("rank_chest_empire_%d"%index,empire)
			constInfo.SetFlag("rank_chest_value_%d"%index,value)


	if app.ENABLE_EVENT_MANAGER:
		def AppendEvent(self, dayIndex, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3, startRealTime, endRealTime, isAlreadyStart):
			self.interface.AppendEvent(int(dayIndex), int(eventIndex), str(startTime), str(endTime), int(empireFlag), int(channelFlag), int(value0), int(value1), int(value2), int(value3), int(startRealTime), int(endRealTime), int(isAlreadyStart))

	if app.ENABLE_DECORUM:
		def __PressF9Key(self):
			self.interface.ToggleDecorumStat()

	if app.ENABLE_NEW_FISHING_SYSTEM:
		def OnFishingStart(self, have, need):
			if self.interface:
				self.interface.OnFishingStart(have, need)

		def OnFishingStop(self):
			if self.interface:
				self.interface.OnFishingStop()

		def OnFishingCatch(self, have):
			if self.interface:
				self.interface.OnFishingCatch(have)

		def OnFishingCatchFailed(self):
			if self.interface:
				self.interface.OnFishingCatchFailed()

	def __PressNumKey(self,num):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):

			if num >= 1 and num <= 9:
				if(chrmgr.IsPossibleEmoticon(-1)):
					chrmgr.SetEmoticon(-1,int(num)-1)
					net.SendEmoticon(int(num)-1)
		else:
			if num >= 1 and num <= 4:
				self.pressNumber(num-1)

	def __ClickBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			return
		else:
			if constInfo.PVPMODE_ACCELKEY_ENABLE:
				self.ChangePKMode()


	def	__PressJKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if player.IsMountingHorse():
				net.SendChatPacket("/unmount")
			# BEGIN_OFFLINE_SHOP
			elif not uiPrivateShopBuilder.IsBuildingPrivateShop() or not uiOfflineShopBuilder.IsBuildingOfflineShop():
			# END_OF_OFFLINE_SHOP
				if not uiPrivateShopBuilder.IsBuildingPrivateShop():
					for i in xrange(player.INVENTORY_PAGE_SIZE):
						if player.GetItemIndex(i) in (71114, 71116, 71118, 71120):
							net.SendItemUsePacket(i)
							break
	def	__PressHKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_ride")
		else:
			self.interface.OpenHelpWindow()

	def	__PressBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_back")
		else:
			state = "EMOTICON"
			self.interface.ToggleCharacterWindow(state)

	def	__PressFKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_feed")
		else:
			app.ZoomCamera(app.CAMERA_TO_POSITIVE)

	def __PressGKey2(self):
		net.SendChatPacket("/ride")

	def __PressGKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/ride")
		else:
			if self.ShowNameFlag:
				self.interface.ToggleGuildWindow()
			else:
				app.PitchCamera(app.CAMERA_TO_POSITIVE)

	def	__ReleaseGKey(self):
		app.PitchCamera(app.CAMERA_STOP)
		

	def __PressQKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if 0==interfaceModule.IsQBHide:
				interfaceModule.IsQBHide = 1
				self.interface.HideAllQuestButton()
			else:
				interfaceModule.IsQBHide = 0
				self.interface.ShowAllQuestButton()
		else:
			app.RotateCamera(app.CAMERA_TO_NEGATIVE)

	def __SetQuickSlotMode(self):
		self.pressNumber=ui.__mem_func__(self.__PressQuickSlot)

	def __SetQuickPageMode(self):
		self.pressNumber=ui.__mem_func__(self.__SelectQuickPage)

	def __PressQuickSlot(self, localSlotIndex):
		if localeInfo.IsARABIC():
			if 0 <= localSlotIndex and localSlotIndex < 4:
				player.RequestUseLocalQuickSlot(3-localSlotIndex)
			else:
				player.RequestUseLocalQuickSlot(11-localSlotIndex)
		else:
			player.RequestUseLocalQuickSlot(localSlotIndex)

	def __SelectQuickPage(self, pageIndex):
		self.quickSlotPageIndex = pageIndex
		player.SetQuickPage(pageIndex)

	def ToggleDebugInfo(self):
		self.isShowDebugInfo = not self.isShowDebugInfo

		if self.isShowDebugInfo:
			self.PrintCoord.Show()
			self.FrameRate.Show()
			self.Pitch.Show()
			self.Splat.Show()
			self.TextureNum.Show()
			self.ObjectNum.Show()
			self.ViewDistance.Show()
			self.PrintMousePos.Show()
		else:
			self.PrintCoord.Hide()
			self.FrameRate.Hide()
			self.Pitch.Hide()
			self.Splat.Hide()
			self.TextureNum.Hide()
			self.ObjectNum.Hide()
			self.ViewDistance.Hide()
			self.PrintMousePos.Hide()

	def __BuildDebugInfo(self):
		## Character Position Coordinate
		self.PrintCoord = ui.TextLine()
		self.PrintCoord.SetFontName(localeInfo.UI_DEF_FONT)
		self.PrintCoord.SetPosition(wndMgr.GetScreenWidth() - 270, 0)

		## Frame Rate
		self.FrameRate = ui.TextLine()
		self.FrameRate.SetFontName(localeInfo.UI_DEF_FONT)
		self.FrameRate.SetPosition(wndMgr.GetScreenWidth() - 270, 20)

		## Camera Pitch
		self.Pitch = ui.TextLine()
		self.Pitch.SetFontName(localeInfo.UI_DEF_FONT)
		self.Pitch.SetPosition(wndMgr.GetScreenWidth() - 270, 40)

		## Splat
		self.Splat = ui.TextLine()
		self.Splat.SetFontName(localeInfo.UI_DEF_FONT)
		self.Splat.SetPosition(wndMgr.GetScreenWidth() - 270, 60)

		##
		self.PrintMousePos = ui.TextLine()
		self.PrintMousePos.SetFontName(localeInfo.UI_DEF_FONT)
		self.PrintMousePos.SetPosition(wndMgr.GetScreenWidth() - 270, 80)

		# TextureNum
		self.TextureNum = ui.TextLine()
		self.TextureNum.SetFontName(localeInfo.UI_DEF_FONT)
		self.TextureNum.SetPosition(wndMgr.GetScreenWidth() - 270, 100)

		# 오브젝트 그리는 개수
		self.ObjectNum = ui.TextLine()
		self.ObjectNum.SetFontName(localeInfo.UI_DEF_FONT)
		self.ObjectNum.SetPosition(wndMgr.GetScreenWidth() - 270, 120)

		# 시야거리
		self.ViewDistance = ui.TextLine()
		self.ViewDistance.SetFontName(localeInfo.UI_DEF_FONT)
		self.ViewDistance.SetPosition(0, 0)

		if app.ENABLE_PINGTIME:
			self.pingLine.SetWindowHorizontalAlignCenter()
			self.pingLine.SetHorizontalAlignCenter()
			self.pingLine.SetFeather()
			self.pingLine.SetOutline()
			self.pingLine.Show()


	def __NotifyError(self, msg):
		chat.AppendChat(chat.CHAT_TYPE_INFO, msg)

	def ChangePKMode(self):

		if not app.IsPressed(app.DIK_LCONTROL):
			return

		if player.GetStatus(player.LEVEL)<constInfo.PVPMODE_PROTECTED_LEVEL:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_PROTECT % (constInfo.PVPMODE_PROTECTED_LEVEL))
			return

		curTime = app.GetTime()
		if curTime - self.lastPKModeSendedTime < constInfo.PVPMODE_ACCELKEY_DELAY:
			return

		self.lastPKModeSendedTime = curTime

		curPKMode = player.GetPKMode()
		nextPKMode = curPKMode + 1
		if nextPKMode == player.PK_MODE_PROTECT:
			if 0 == player.GetGuildID():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
				nextPKMode = 0
			else:
				nextPKMode = player.PK_MODE_GUILD

		elif nextPKMode == player.PK_MODE_MAX_NUM:
			nextPKMode = 0

		net.SendChatPacket("/PKMode " + str(nextPKMode))
		print "/PKMode " + str(nextPKMode)

	def OnChangePKMode(self):

		self.interface.OnChangePKMode()

		try:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_MESSAGE_DICT[player.GetPKMode()])
		except KeyError:
			print "UNKNOWN PVPMode[%d]" % (player.GetPKMode())

		if constInfo.PVPMODE_TEST_ENABLE:
			curPKMode = player.GetPKMode()
			alignment, grade = chr.testGetPKData()
			self.pkModeNameDict = { 0 : "PEACE", 1 : "REVENGE", 2 : "FREE", 3 : "PROTECT", }
			self.testPKMode.SetText("Current PK Mode : " + self.pkModeNameDict.get(curPKMode, "UNKNOWN"))
			self.testAlignment.SetText("Current Alignment : " + str(alignment) + " (" + localeInfo.TITLE_NAME_LIST[grade] + ")")

	###############################################################################################
	###############################################################################################
	## Game Callback Functions

	if app.ENABLE_MAP_LOCATION_APP_NAME:
		def SetApplicationText(self):
			mapName = background.GetCurrentMapName()
			if mapName in localeInfo.MINIMAP_ZONE_NAME_DICT:
				app.SetText(localeInfo.APP_TITLE + " | " + localeInfo.MINIMAP_ZONE_NAME_DICT[mapName])

	# Start
	def StartGame(self):
		self.RefreshInventory()
		self.RefreshEquipment()
		self.RefreshCharacter()
		self.RefreshSkill()

	# Refresh
	def CheckGameButton(self):
		if self.interface:
			self.interface.CheckGameButton()

	def RefreshAlignment(self):
		self.interface.RefreshAlignment()
		
	if app.WJ_SHOW_ALL_CHANNEL:
		def BINARY_OnChannelPacket(self, channel):
			serverName = "|cffFDBA31Emeria"
			text =localeInfo.TEXT_CHANNEL % serverName
			if channel == 99:
				text+= "Dungeon"
			elif channel == 98:
				text+= " general"
			else:
				text+= ""+str(channel)
			net.SetServerInfo(text)
			if self.interface:
				self.interface.wndMiniMap.serverInfo.SetText(net.GetServerInfo())

	def RefreshStatus(self):
		self.CheckGameButton()

		if self.interface:
			self.interface.RefreshStatus()

		if self.playerGauge:
			self.playerGauge.RefreshGauge()

	def RefreshStamina(self):
		self.interface.RefreshStamina()

	def RefreshSkill(self):
		self.CheckGameButton()
		if self.interface:
			self.interface.RefreshSkill()

	def RefreshQuest(self):
		self.interface.RefreshQuest()

	def RefreshMessenger(self):
		self.interface.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.interface.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.interface.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.interface.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.interface.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.interface.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.interface.RefreshGuildGradePage()

	def RefreshMobile(self):
		if self.interface:
			self.interface.RefreshMobile()

	def OnMobileAuthority(self):
		self.interface.OnMobileAuthority()

	def OnBlockMode(self, mode):
		self.interface.OnBlockMode(mode)

	def OpenQuestWindow(self, skin, idx):
		if constInfo.INPUT_IGNORE == 1:
			return
		else:
			self.interface.OpenQuestWindow(skin, idx)

		if constInfo.INPUT_IGNORE == 1:
			return


	def AskGuildName(self):

		guildNameBoard = uiCommon.InputDialog()
		guildNameBoard.SetTitle(localeInfo.GUILD_NAME)
		guildNameBoard.SetAcceptEvent(ui.__mem_func__(self.ConfirmGuildName))
		guildNameBoard.SetCancelEvent(ui.__mem_func__(self.CancelGuildName))
		guildNameBoard.Open()

		self.guildNameBoard = guildNameBoard

	def ConfirmGuildName(self):
		guildName = self.guildNameBoard.GetText()
		if not guildName:
			return

		if net.IsInsultIn(guildName):
			self.PopupMessage(localeInfo.GUILD_CREATE_ERROR_INSULT_NAME)
			return

		net.SendAnswerMakeGuildPacket(guildName)
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return True

	def CancelGuildName(self):
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return True

	## Refine
	def PopupMessage(self, msg):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, 0, localeInfo.UI_OK)

	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type=0):
		self.interface.OpenRefineDialog(targetItemPos, nextGradeItemVnum, cost, prob, type)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.interface.AppendMaterialToRefineDialog(vnum, count)

	def RunUseSkillEvent(self, slotIndex, coolTime):
		self.interface.OnUseSkill(slotIndex, coolTime)

	def ClearAffects(self):
		self.affectShower.ClearAffects()

	def SetAffect(self, affect):
		self.affectShower.SetAffect(affect)

	def ResetAffect(self, affect):
		self.affectShower.ResetAffect(affect)

	if app.ENABLE_ANTI_MULTIPLE_FARM:
		def BINARY_RecvAntiFarmReload(self):
			if not self.interface:
				return
			self.interface.SendAntiFarmReload()


	# UNKNOWN_UPDATE
	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):
		#import chat
		#chat.AppendChat(1, "add type: %d point: %d"%(type, pointIdx))
		
		if type == None:
			return
		else:
			self.affectShower.BINARY_NEW_AddAffect(type, pointIdx, value, duration)
			if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
				self.interface.DragonSoulActivate(type - chr.NEW_AFFECT_DRAGON_SOUL_DECK1)
			elif chr.NEW_AFFECT_DRAGON_SOUL_QUALIFIED == type:
				self.BINARY_DragonSoulGiveQuilification()
			elif chr.AFFECT_POISON == type or 209 == type:
				self.playerGauge.RefreshGuageColor("lime")
				self.interface.HPPoisonEffectShow()
				self.interface.PartyPoisonGuageShow()

	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		#import chat
		#chat.AppendChat(1, "remove type: %d point: %d"%(type, pointIdx))
		
		if type == None:
			return
		else:
			self.affectShower.BINARY_NEW_RemoveAffect(type, pointIdx)
			if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
				self.interface.DragonSoulDeactivate()
			elif chr.AFFECT_POISON == type or 209 == type:
				self.playerGauge.RefreshGuageColor("red")
				self.interface.HPPoisonEffectHide()
				self.interface.PartyPoisonGuageHide()

	if app.ENABLE_AFFECT_FIX:
		def RefreshAffectWindow(self):
			self.affectShower.BINARY_NEW_RefreshAffect()
	# END_OF_UNKNOWN_UPDATE

	def ActivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnActivateSkill(slotIndex)

	def DeactivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnDeactivateSkill(slotIndex)

	def RefreshEquipment(self):
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshInventory(self):
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshCharacter(self):
		if self.interface:
			self.interface.RefreshCharacter()

	if app.RENEWAL_DEAD_PACKET:
		def OnGameOver(self, d_time):
			self.CloseTargetBoard()
			self.OpenRestartDialog(d_time)
	else:
		def OnGameOver(self):
			self.CloseTargetBoard()
			self.OpenRestartDialog()

	if app.RENEWAL_DEAD_PACKET:
		def OpenRestartDialog(self, d_time):
			self.interface.OpenRestartDialog(d_time)
	else:
		def OpenRestartDialog(self):
			self.interface.OpenRestartDialog()

	def ChangeCurrentSkill(self, skillSlotNumber):
		self.interface.OnChangeCurrentSkill(skillSlotNumber)

	## TargetBoard
	def SetPCTargetBoard(self, vid, name):
		self.targetBoard.Open(vid, name)

		if app.IsPressed(app.DIK_LCONTROL):

			if not player.IsSameEmpire(vid):
				return

			if player.IsMainCharacterIndex(vid):
				return
			elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(vid):
				return

			self.interface.OpenWhisperDialog(name)

	def RefreshTargetBoardByVID(self, vid):
		self.targetBoard.RefreshByVID(vid)

	def RefreshTargetBoardByName(self, name):
		self.targetBoard.RefreshByName(name)
		self.interface.UpdateWhisperButtons(name)

	def __RefreshTargetBoard(self):
		self.targetBoard.Refresh()

	if app.ENABLE_VIEW_ELEMENT:
		def SetHPTargetBoard(self, vid, hpPercentage, bElement):
			if vid != self.targetBoard.GetTargetVID():
				self.targetBoard.ResetTargetBoard()
				self.targetBoard.SetEnemyVID(vid)
			
			self.targetBoard.SetHP(hpPercentage)
			self.targetBoard.SetElementImage(bElement)
			self.targetBoard.Show()
	
	def SetMountTargetBoard(self, vid):
		if vid != self.targetBoard.GetTargetVID():
			self.targetBoard.SetMount(vid)

	if app.ENABLE_SHIP_DEFENSE:
		def SetHPAllianceTargetBoard(self, vid, hp, hpMax):
			if self.interface.IsHideUiMode == True:
				return

			if not vid:
				self.allyTargetBoard.Close()
				return

			if vid != self.allyTargetBoard.GetTargetVID():
				self.allyTargetBoard.ResetTargetBoard()
				self.allyTargetBoard.SetTarget(vid)

			self.allyTargetBoard.SetHP(hp, hpMax)
			self.allyTargetBoard.Show()

	def CloseTargetBoardIfDifferent(self, vid, hpPercentage):
		if vid != self.targetBoard.GetTargetVID():
			self.targetBoard.Close()
		else:
			self.targetBoard.SetNewHP(hpPercentage)

	def CloseTargetBoard(self):
		self.targetBoard.Close()

	## View Equipment
	def OpenEquipmentDialog(self, vid):
		self.interface.OpenEquipmentDialog(vid)

	def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
		self.interface.SetEquipmentDialogItem(vid, slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		self.interface.SetEquipmentDialogSocket(vid, slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		self.interface.SetEquipmentDialogAttr(vid, slotIndex, attrIndex, type, value)
		
	if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
		def BINARY_SET_LANG_AND_EMPIRE_FLAG(self, name, language, empire):
			self.interface.SetInterfaceFlag(name, language, empire)

	# SHOW_LOCAL_MAP_NAME
	def ShowMapName(self, mapName, x, y):

		if self.mapNameShower:
			self.mapNameShower.ShowMapName(mapName, x, y)

		if self.interface:
			self.interface.SetMapName(mapName)
	# END_OF_SHOW_LOCAL_MAP_NAME

	if app.ENABLE_HUNTING_SYSTEM:
		def BINARY_OpenHuntingWindowMain(self, level, monster, cur_count, dest_count, money_min, money_max, exp_min, exp_max, race_item, race_item_count):
			if self.interface:
				self.interface.OpenHuntingWindowMain(level, monster, cur_count, dest_count, money_min, money_max, exp_min, exp_max, race_item, race_item_count)
		
		def BINARY_OpenHuntingWindowSelect(self, level, type, monster, count, money_min, money_max, exp_min, exp_max, race_item, race_item_count):
			if self.interface:
				self.interface.OpenHuntingWindowSelect(level, type ,monster, count, money_min, money_max, exp_min, exp_max, race_item, race_item_count)
				
		def BINARY_OpenHuntingWindowReward(self, level, reward, reward_count, random_reward, random_reward_count, money, exp):
			if self.interface:
				self.interface.OpenHuntingWindowReward(level, reward, reward_count, random_reward, random_reward_count, money, exp)
				
		def BINARY_UpdateHuntingMission(self, count):
			if self.interface:
				self.interface.UpdateHuntingMission(count)
				
		def BINARY_HuntingReciveRandomItem(self, window, item_vnum, item_count):
			if self.interface:
				if window == 0:
					self.interface.HuntingSetRandomItemsMain(item_vnum, item_count)
				if window == 1:
					self.interface.HuntingSetRandomItemsSelect(item_vnum, item_count)


	def BINARY_OpenAtlasWindow(self):
		self.interface.BINARY_OpenAtlasWindow()

	## Chat
	if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
		def OnRecvWhisper(self, mode, name, line, language, empire):
			if mode == chat.WHISPER_TYPE_GM:
				self.interface.RegisterGameMasterName(name)
			chat.AppendWhisper(mode, name, line)
			self.interface.RecvWhisper(name, language, empire)
	else:
		def OnRecvWhisper(self, mode, name, line):
			if mode == chat.WHISPER_TYPE_GM:
				self.interface.RegisterGameMasterName(name)
			chat.AppendWhisper(mode, name, line)
			self.interface.RecvWhisper(name)

	def OnRecvWhisperSystemMessage(self, mode, name, line):
		chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, line)
		self.interface.RecvWhisper(name)

	def OnRecvWhisperError(self, mode, name, line):
		if localeInfo.WHISPER_ERROR.has_key(mode):
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, localeInfo.WHISPER_ERROR[mode](name))
		else:
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, "Whisper Unknown Error(mode=%d, name=%s)" % (mode, name))
		self.interface.RecvWhisper(name)

	def RecvWhisper(self, name):
		self.interface.RecvWhisper(name)

	def OnPickMoney(self, money):
		if app.ENABLE_CHATTING_WINDOW_RENEWAL:
			chat.AppendChat(chat.CHAT_TYPE_MONEY_INFO, localeInfo.GAME_PICK_MONEY % (money))
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_PICK_MONEY % (money))

	if app.ENABLE_CHEQUE_SYSTEM:
		def OnPickCheque(self, cheque):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHEQUE_SYSTEM_PICK_WON % (cheque))


	def OnShopError(self, type):
		try:
			self.PopupMessage(localeInfo.SHOP_ERROR_DICT[type])
		except KeyError:
			self.PopupMessage(localeInfo.SHOP_ERROR_UNKNOWN % (type))

	def OnSafeBoxError(self):
		self.PopupMessage(localeInfo.SAFEBOX_ERROR)

	def OnFishingSuccess(self, isFish, fishName):
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.FISHING_SUCCESS(isFish, fishName), 2000)

	# ADD_FISHING_MESSAGE
	def OnFishingNotifyUnknown(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_UNKNOWN)

	def OnFishingWrongPlace(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_WRONG_PLACE)
	# END_OF_ADD_FISHING_MESSAGE

	def OnFishingNotify(self, isFish, fishName):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_NOTIFY(isFish, fishName))

	def OnFishingFailure(self):
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.FISHING_FAILURE, 2000)

	def OnCannotPickItem(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_PICK_ITEM)

	# MINING
	def OnCannotMining(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_MINING)
	# END_OF_MINING

	def OnCannotUseSkill(self, vid, type):
		if localeInfo.USE_SKILL_ERROR_TAIL_DICT.has_key(type):
			textTail.RegisterInfoTail(vid, localeInfo.USE_SKILL_ERROR_TAIL_DICT[type])

		if localeInfo.USE_SKILL_ERROR_CHAT_DICT.has_key(type):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_SKILL_ERROR_CHAT_DICT[type])

	def	OnCannotShotError(self, vid, type):
		textTail.RegisterInfoTail(vid, localeInfo.SHOT_ERROR_TAIL_DICT.get(type, localeInfo.SHOT_ERROR_UNKNOWN % (type)))

	## PointReset
	def StartPointReset(self):
		self.interface.OpenPointResetDialog()

	## Shop
	def StartShop(self, vid):
		if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
			if(vid == constInfo.MARKED_SHOP_VID):
				background.DeletePrivateShopPos()
				constInfo.MARKED_SHOP_VID = 0

		self.interface.OpenShopDialog(vid)

	def EndShop(self):
		self.interface.CloseShopDialog()

	def RefreshShop(self):
		self.interface.RefreshShopDialog()


	if app.ENABLE_OFFLINE_SHOP_SYSTEM:
		def StartOfflineShop(self, vid):
			self.interface.OpenOfflineShopDialog(vid)

		def LoadInfoShopOffline(self, vid, time, map_index, x, y):
			self.interface.OpenOfflineShopEditMode(vid, time, map_index, x, y)

		def EndOfflineShop(self):
			self.interface.CloseOfflineShopDialog()

		def RefreshOfflineShop(self):
			self.interface.RefreshOfflineShopDialog()
			self.interface.RefreshOfflineShopEditMode()

	def SetShopSellingPrice(self, Price):
		pass

	## Exchange
	def StartExchange(self):
		self.interface.StartExchange()

	def EndExchange(self):
		self.interface.EndExchange()

	def RefreshExchange(self):
		self.interface.RefreshExchange()

	## Party
	def RecvPartyInviteQuestion(self, leaderVID, leaderName):
		partyInviteQuestionDialog = uiCommon.QuestionDialog()
		partyInviteQuestionDialog.SetText(leaderName + localeInfo.PARTY_DO_YOU_JOIN)
		partyInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerPartyInvite(arg))
		partyInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerPartyInvite(arg))
		partyInviteQuestionDialog.Open()
		partyInviteQuestionDialog.partyLeaderVID = leaderVID
		self.partyInviteQuestionDialog = partyInviteQuestionDialog

	def AnswerPartyInvite(self, answer):

		if not self.partyInviteQuestionDialog:
			return

		partyLeaderVID = self.partyInviteQuestionDialog.partyLeaderVID

		distance = player.GetCharacterDistance(partyLeaderVID)
		if distance < 0.0 or distance > 5000:
			answer = False

		net.SendPartyInviteAnswerPacket(partyLeaderVID, answer)

		self.partyInviteQuestionDialog.Close()
		self.partyInviteQuestionDialog = None

	def AddPartyMember(self, pid, name):
		self.interface.AddPartyMember(pid, name)

	def UpdatePartyMemberInfo(self, pid):
		self.interface.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.interface.RemovePartyMember(pid)
		self.__RefreshTargetBoard()

	def LinkPartyMember(self, pid, vid):
		self.interface.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.interface.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.interface.UnlinkAllPartyMember()

	def ExitParty(self):
		self.interface.ExitParty()
		self.RefreshTargetBoardByVID(self.targetBoard.GetTargetVID())

	def ChangePartyParameter(self, distributionMode):
		self.interface.ChangePartyParameter(distributionMode)

	## Messenger
	def OnMessengerAddFriendQuestion(self, name):
		messengerAddFriendQuestion = uiCommon.QuestionDialog2()
		messengerAddFriendQuestion.SetText1(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_1 % (name))
		messengerAddFriendQuestion.SetText2(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_2)
		messengerAddFriendQuestion.SetAcceptEvent(ui.__mem_func__(self.OnAcceptAddFriend))
		messengerAddFriendQuestion.SetCancelEvent(ui.__mem_func__(self.OnDenyAddFriend))
		messengerAddFriendQuestion.Open()
		messengerAddFriendQuestion.name = name
		self.messengerAddFriendQuestion = messengerAddFriendQuestion

	def OnAcceptAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		net.SendChatPacket("/messenger_auth y " + name)
		self.OnCloseAddFriendQuestionDialog()
		return True

	def OnDenyAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		net.SendChatPacket("/messenger_auth n " + name)
		self.OnCloseAddFriendQuestionDialog()
		return True

	def OnCloseAddFriendQuestionDialog(self):
		self.messengerAddFriendQuestion.Close()
		self.messengerAddFriendQuestion = None
		return True

	## SafeBox
	def OpenSafeboxWindow(self, size):
		self.interface.OpenSafeboxWindow(size)

	def RefreshSafebox(self):
		self.interface.RefreshSafebox()

	def RefreshSafeboxMoney(self):
		self.interface.RefreshSafeboxMoney()

	# ITEM_MALL
	def OpenMallWindow(self, size):
		self.interface.OpenMallWindow(size)

	def RefreshMall(self):
		self.interface.RefreshMall()
	# END_OF_ITEM_MALL

	## Guild
	def RecvGuildInviteQuestion(self, guildID, guildName):
		guildInviteQuestionDialog = uiCommon.QuestionDialog()
		guildInviteQuestionDialog.SetText(guildName + localeInfo.GUILD_DO_YOU_JOIN)
		guildInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.Open()
		guildInviteQuestionDialog.guildID = guildID
		self.guildInviteQuestionDialog = guildInviteQuestionDialog

	def AnswerGuildInvite(self, answer):

		if not self.guildInviteQuestionDialog:
			return

		guildLeaderVID = self.guildInviteQuestionDialog.guildID
		net.SendGuildInviteAnswerPacket(guildLeaderVID, answer)

		self.guildInviteQuestionDialog.Close()
		self.guildInviteQuestionDialog = None


	def DeleteGuild(self):
		self.interface.DeleteGuild()

	## Clock
	def ShowClock(self, second):
		self.interface.ShowClock(second)

	def HideClock(self):
		self.interface.HideClock()

	## Emotion
	def BINARY_ActEmotion(self, emotionIndex):
		if self.interface.wndCharacter:
			self.interface.wndCharacter.ActEmotion(emotionIndex)

	###############################################################################################
	###############################################################################################
	## Keyboard Functions

	def CheckFocus(self):
		if False == self.IsFocus():
			if True == self.interface.IsOpenChat():
				self.interface.ToggleChat()

			self.SetFocus()

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

	def ShowConsole(self):
		if debugInfo.IsDebugMode() or True == self.consoleEnable:
			player.EndKeyWalkingImmediately()
			self.console.OpenWindow()

	def fuck_buttons(self):
		self.ShowNameFlag = False
		self.playerGauge.DisableShowAlways()
		player.SetQuickPage(self.quickSlotPageIndex)

	def ShowName(self):
		self.ShowNameFlag = True
		self.playerGauge.EnableShowAlways()
		player.SetQuickPage(self.quickSlotPageIndex+1)

	# ADD_ALWAYS_SHOW_NAME
	def __IsShowName(self):
		x = systemSetting.IsAlwaysShowName()
		return x == 1 or x == 3 or self.ShowNameFlag
	# END_OF_ADD_ALWAYS_SHOW_NAME

	def HideName(self):
		self.ShowNameFlag = False
		self.playerGauge.DisableShowAlways()
		player.SetQuickPage(self.quickSlotPageIndex)

	def ShowMouseImage(self):
		self.interface.ShowMouseImage()

	def HideMouseImage(self):
		self.interface.HideMouseImage()

	def StartAttack(self):
		player.SetAttackKeyState(True)

	def EndAttack(self):
		player.SetAttackKeyState(False)

	def MoveUp(self):
		player.SetSingleDIKKeyState(app.DIK_UP, True)

	def MoveDown(self):
		player.SetSingleDIKKeyState(app.DIK_DOWN, True)

	def MoveLeft(self):
		player.SetSingleDIKKeyState(app.DIK_LEFT, True)

	def MoveRight(self):
		player.SetSingleDIKKeyState(app.DIK_RIGHT, True)

	def StopUp(self):
		player.SetSingleDIKKeyState(app.DIK_UP, False)

	def StopDown(self):
		player.SetSingleDIKKeyState(app.DIK_DOWN, False)

	def StopLeft(self):
		player.SetSingleDIKKeyState(app.DIK_LEFT, False)

	def StopRight(self):
		player.SetSingleDIKKeyState(app.DIK_RIGHT, False)

	def PickUpItem(self):
		if systemSetting.GetPickupMode():
			player.PickCloseItemVector()
		else:
			player.PickCloseItem()

	###############################################################################################
	###############################################################################################
	## Event Handler

	def OnKeyDown(self, key):
		if self.interface.wndWeb and self.interface.wndWeb.IsShow():
			return

		if key == app.DIK_ESC:
			self.RequestDropItem(False)
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		try:
			self.onPressKeyDict[key]()
		except KeyError:
			pass
		except:
			raise
		
		return True
		
		constInfo.SET_ITEM_DROP_QUESTION_DIALOG_STATUS(0)

	def OnKeyUp(self, key):
		if key == None:
			return
		
		try:
			self.onClickKeyDict[key]()
		except:
			pass
		
		return True

	def OnMouseLeftButtonDown(self):
		if self.interface.BUILD_OnMouseLeftButtonDown():
			return

		if mouseModule.mouseController.isAttached():
			self.CheckFocus()
		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				return
			else:
				self.CheckFocus()
				player.SetMouseState(player.MBT_LEFT, player.MBS_PRESS);

		return True

	def OnMouseLeftButtonUp(self):

		if self.interface.BUILD_OnMouseLeftButtonUp():
			return

		if mouseModule.mouseController.isAttached():

			attachedType = mouseModule.mouseController.GetAttachedType()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
			attachedItemSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()

			## QuickSlot
			if player.SLOT_TYPE_QUICK_SLOT == attachedType:
				player.RequestDeleteGlobalQuickSlot(attachedItemSlotPos)

			## Inventory
			elif player.SLOT_TYPE_INVENTORY == attachedType:

				if player.ITEM_MONEY == attachedItemIndex:
					self.__PutMoney(attachedType, attachedItemCount, self.PickingCharacterIndex)
				else:
					self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			## DragonSoul
			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			## Special Storage
			elif app.ENABLE_SPECIAL_STORAGE_SYSTEM:
				if player.SLOT_TYPE_SKILLBOOK_INVENTORY == attachedType or\
					player.SLOT_TYPE_UPPITEM_INVENTORY == attachedType or\
					player.SLOT_TYPE_GHOSTSTONE_INVENTORY == attachedType or\
					player.SLOT_TYPE_GENERAL_INVENTORY == attachedType:
					self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			mouseModule.mouseController.DeattachObject()

		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				if app.IsPressed(app.DIK_LALT):
					link = chat.GetLinkFromHyperlink(hyperlink)
					ime.PasteString(link)
				else:
					
					self.interface.MakeHyperlinkTooltip(hyperlink)
				return
			else:
				player.SetMouseState(player.MBT_LEFT, player.MBS_CLICK)

		#player.EndMouseWalking()
		return True

	def __PutItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, dstChrID):
		if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
			if player.SLOT_TYPE_INVENTORY == attachedType or\
				player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType or\
				player.SLOT_TYPE_SKILLBOOK_INVENTORY == attachedType or\
				player.SLOT_TYPE_UPPITEM_INVENTORY == attachedType or\
				player.SLOT_TYPE_GHOSTSTONE_INVENTORY == attachedType or\
				player.SLOT_TYPE_GENERAL_INVENTORY == attachedType:

				attachedInvenType = player.SlotTypeToInvenType(attachedType)

				if True == chr.HasInstance(self.PickingCharacterIndex) and player.GetMainCharacterIndex() != dstChrID:
					if player.IsEquipmentSlot(attachedItemSlotPos) and\
						player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedType and\
						player.SLOT_TYPE_SKILLBOOK_INVENTORY != attachedType and\
						player.SLOT_TYPE_UPPITEM_INVENTORY != attachedType and\
						player.SLOT_TYPE_GHOSTSTONE_INVENTORY != attachedType and\
						player.SLOT_TYPE_GENERAL_INVENTORY != attachedType:
						self.stream.popupWindow.Close()
						self.stream.popupWindow.Open(localeInfo.EXCHANGE_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)
					else:
						if chr.IsNPC(dstChrID):
							if app.ENABLE_REFINE_RENEWAL:
								constInfo.AUTO_REFINE_TYPE = 2
								constInfo.AUTO_REFINE_DATA["NPC"][0] = dstChrID
								constInfo.AUTO_REFINE_DATA["NPC"][1] = attachedInvenType
								constInfo.AUTO_REFINE_DATA["NPC"][2] = attachedItemSlotPos
								constInfo.AUTO_REFINE_DATA["NPC"][3] = attachedItemCount
							net.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
							net.SendExchangeStartPacket(dstChrID)
							net.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
						else:
							net.SendExchangeStartPacket(dstChrID)
							net.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
				else:
					self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)
		else:
			if player.SLOT_TYPE_INVENTORY == attachedType or player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				attachedInvenType = player.SlotTypeToInvenType(attachedType)
				if True == chr.HasInstance(self.PickingCharacterIndex) and player.GetMainCharacterIndex() != dstChrID:
					if player.IsEquipmentSlot(attachedItemSlotPos) and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedType:
						self.stream.popupWindow.Close()
						self.stream.popupWindow.Open(localeInfo.EXCHANGE_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)
					else:
						if chr.IsNPC(dstChrID):
								net.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
						else:
							net.SendExchangeStartPacket(dstChrID)
							net.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
				else:
					self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)

	def __PutMoney(self, attachedType, attachedMoney, dstChrID):
		if True == chr.HasInstance(dstChrID) and player.GetMainCharacterIndex() != dstChrID:
			net.SendExchangeStartPacket(dstChrID)
			net.SendExchangeElkAddPacket(attachedMoney)
		else:
			self.__DropMoney(attachedType, attachedMoney)

	def __DropMoney(self, attachedType, attachedMoney):
		# PRIVATESHOP_DISABLE_ITEM_DROP - 개인상점 열고 있는 동안 아이템 버림 방지
		if uiPrivateShopBuilder.IsBuildingPrivateShop():												
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return
		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			if (uiOfflineShopBuilder.IsBuildingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return

		if (uiOfflineShop.IsEditingOfflineShop()):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return
		# END_OF_OFFLINE_SHOP			
		# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

		if attachedMoney>=1000:
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.DROP_MONEY_FAILURE_1000_OVER, 0, localeInfo.UI_OK)
			return

		itemDropQuestionDialog = uiCommon.QuestionDialog()
		itemDropQuestionDialog.SetText(localeInfo.DO_YOU_DROP_MONEY % (attachedMoney))
		itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
		itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
		itemDropQuestionDialog.Open()
		itemDropQuestionDialog.dropType = attachedType
		itemDropQuestionDialog.dropCount = attachedMoney
		itemDropQuestionDialog.dropNumber = player.ITEM_MONEY
		self.itemDropQuestionDialog = itemDropQuestionDialog

	if constInfo.ENABLE_NEW_DROP_ITEM:
		def __DropItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount):
			if player.SLOT_TYPE_INVENTORY == attachedType and player.IsEquipmentSlot(attachedItemSlotPos):
				self.stream.popupWindow.Close()
				self.stream.popupWindow.Open(localeInfo.DROP_ITEM_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)
			elif safebox.isOpen() and app.ENABLE_CHECK_SAFEBOX_IS_OPEN:
					self.stream.popupWindow.Close()
					self.stream.popupWindow.Open(localeInfo.DROP_ITEM_FAILURE_SAFEBOX, 0, localeInfo.UI_OK)
			else:
				constInfo.DROP_GUI_CHECK = 1
				if self.itemDropQuestionDialog ==None:
					self.itemDropQuestionDialog = uiCommon.QuestionDialogItemNew(self.interface.tooltipItem)

				if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
					if attachedType == player.SLOT_TYPE_SKILLBOOK_INVENTORY:
						self.itemDropQuestionDialog.dropType = player.SKILLBOOK_INVENTORY
					elif attachedType == player.SLOT_TYPE_UPPITEM_INVENTORY:
						self.itemDropQuestionDialog.dropType = player.UPPITEM_INVENTORY
					elif attachedType == player.SLOT_TYPE_GHOSTSTONE_INVENTORY:
						self.itemDropQuestionDialog.dropType = player.GHOSTSTONE_INVENTORY
					elif attachedType == player.SLOT_TYPE_GENERAL_INVENTORY:
						self.itemDropQuestionDialog.dropType = player.GENERAL_INVENTORY
					elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:#DS
						self.itemDropQuestionDialog.dropType = player.DRAGON_SOUL_INVENTORY
					else:
						self.itemDropQuestionDialog.dropType = player.INVENTORY
				else:
					if player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
						self.itemDropQuestionDialog.dropType = player.DRAGON_SOUL_INVENTORY
					else:
						self.itemDropQuestionDialog.dropType = player.INVENTORY

				self.itemDropQuestionDialog.dropNumber = attachedItemSlotPos
				self.itemDropQuestionDialog.dropCount = attachedItemCount
				self.itemDropQuestionDialog.Open()
	else:
		def __DropItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount):
			# PRIVATESHOP_DISABLE_ITEM_DROP - 개인상점 열고 있는 동안 아이템 버림 방지
			if uiPrivateShopBuilder.IsBuildingPrivateShop():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return
			# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
			# BEGIN_OFFLINE_SHOP
			if app.ENABLE_OFFLINE_SHOP_SYSTEM:
				if (uiOfflineShopBuilder.IsBuildingOfflineShop()):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
					return

				if (uiOfflineShop.IsEditingOfflineShop()):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
					return
			# END_OF_OFFLINE_SHOP
			if player.SLOT_TYPE_INVENTORY == attachedType and player.IsEquipmentSlot(attachedItemSlotPos):
				self.stream.popupWindow.Close()
				self.stream.popupWindow.Open(localeInfo.DROP_ITEM_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)

			else:
				if player.SLOT_TYPE_INVENTORY == attachedType:
					dropItemIndex = player.GetItemIndex(attachedItemSlotPos)

					item.SelectItem(dropItemIndex)
					dropItemName = item.GetItemName()

					## Question Text
					questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

					## Dialog
					itemDropQuestionDialog = uiCommon.QuestionDialog()
					itemDropQuestionDialog.SetText(questionText)
					itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
					itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
					itemDropQuestionDialog.Open()
					itemDropQuestionDialog.dropType = attachedType
					itemDropQuestionDialog.dropNumber = attachedItemSlotPos
					itemDropQuestionDialog.dropCount = attachedItemCount
					self.itemDropQuestionDialog = itemDropQuestionDialog

					constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
				elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
					dropItemIndex = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, attachedItemSlotPos)

					item.SelectItem(dropItemIndex)
					dropItemName = item.GetItemName()

					## Question Text
					questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

					## Dialog
					itemDropQuestionDialog = uiCommon.QuestionDialog()
					itemDropQuestionDialog.SetText(questionText)
					itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
					itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
					itemDropQuestionDialog.Open()
					itemDropQuestionDialog.dropType = attachedType
					itemDropQuestionDialog.dropNumber = attachedItemSlotPos
					itemDropQuestionDialog.dropCount = attachedItemCount
					self.itemDropQuestionDialog = itemDropQuestionDialog

					constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
				elif app.ENABLE_SPECIAL_STORAGE_SYSTEM:
					if player.SLOT_TYPE_SKILLBOOK_INVENTORY == attachedType or\
						player.SLOT_TYPE_UPPITEM_INVENTORY == attachedType or\
						player.SLOT_TYPE_GHOSTSTONE_INVENTORY == attachedType or\
						player.SLOT_TYPE_GENERAL_INVENTORY == attachedType:

						dropItemIndex = player.GetItemIndex(player.SlotTypeToInvenType(attachedType), attachedItemSlotPos)

						item.SelectItem(dropItemIndex)
						dropItemName = item.GetItemName()

						## Question Text
						questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

						## Dialog
						itemDropQuestionDialog = uiCommon.QuestionDialog()
						itemDropQuestionDialog.SetText(questionText)
						itemDropQuestionDialog.SetAcceptEvent(lambda arg = True: self.RequestDropItem(arg))
						itemDropQuestionDialog.SetCancelEvent(lambda arg = False: self.RequestDropItem(arg))
						itemDropQuestionDialog.Open()
						itemDropQuestionDialog.dropType = attachedType
						itemDropQuestionDialog.dropNumber = attachedItemSlotPos
						itemDropQuestionDialog.dropCount = attachedItemCount
						self.itemDropQuestionDialog = itemDropQuestionDialog

						constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def RequestDropItem(self, answer):
		if not self.itemDropQuestionDialog:
			return

		if answer:
			dropType = self.itemDropQuestionDialog.dropType
			dropCount = self.itemDropQuestionDialog.dropCount
			dropNumber = self.itemDropQuestionDialog.dropNumber

			if player.SLOT_TYPE_INVENTORY == dropType:
				if dropNumber == player.ITEM_MONEY:
					net.SendGoldDropPacketNew(dropCount)
					snd.PlaySound("sound/ui/money.wav")
				else:
					# PRIVATESHOP_DISABLE_ITEM_DROP
					self.__SendDropItemPacket(dropNumber, dropCount)
					# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType:
					# PRIVATESHOP_DISABLE_ITEM_DROP
					self.__SendDropItemPacket(dropNumber, dropCount, player.DRAGON_SOUL_INVENTORY)
					# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
			elif app.ENABLE_SPECIAL_STORAGE_SYSTEM:
				if player.SLOT_TYPE_SKILLBOOK_INVENTORY == dropType or\
					player.SLOT_TYPE_UPPITEM_INVENTORY == dropType or\
					player.SLOT_TYPE_GHOSTSTONE_INVENTORY == dropType or\
					player.SLOT_TYPE_GENERAL_INVENTORY == dropType:
					# PRIVATESHOP_DISABLE_ITEM_DROP
					self.__SendDropItemPacket(dropNumber, dropCount, player.SlotTypeToInvenType(dropType))
					# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
	
		self.itemDropQuestionDialog.Close()
		self.itemDropQuestionDialog = None

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	# PRIVATESHOP_DISABLE_ITEM_DROP
	def __SendDropItemPacket(self, itemVNum, itemCount, itemInvenType = player.INVENTORY):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return
		# BEGIN_OFFLINE_SHOP
		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			if (uiOfflineShopBuilder.IsBuildingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return

			if (uiOfflineShop.IsEditingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return
		net.SendItemDropPacketNew(itemInvenType, itemVNum, itemCount)
	# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
	def __SendDestroyItemPacket(self, itemVNum, itemCount, itemInvenType = player.INVENTORY):
#	def __SendDestroyItemPacket(self, itemVNum, itemInvenType = player.INVENTORY):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return
		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			if (uiOfflineShopBuilder.IsBuildingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return

			if (uiOfflineShop.IsEditingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return
		net.SendItemDestroyPacket(itemInvenType, itemVNum, itemCount)
	def __SendSellItemPacket(self, itemVNum, itemCount, itemInvenType = player.INVENTORY):
#	def __SendSellItemPacket(self, itemVNum, itemInvenType = player.INVENTORY):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return
		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			if (uiOfflineShopBuilder.IsBuildingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return

			if (uiOfflineShop.IsEditingOfflineShop()):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
				return
		net.SendItemSellPacket(itemInvenType, itemVNum, itemCount)
	def OnMouseRightButtonDown(self):

		self.CheckFocus()

		if True == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			player.SetMouseState(player.MBT_RIGHT, player.MBS_PRESS)

		return True

	def OnMouseRightButtonUp(self):
		if True == mouseModule.mouseController.isAttached():
			return True

		player.SetMouseState(player.MBT_RIGHT, player.MBS_CLICK)
		return True

	def OnMouseMiddleButtonDown(self):
		player.SetMouseMiddleButtonState(player.MBS_PRESS)

	def OnMouseMiddleButtonUp(self):
		player.SetMouseMiddleButtonState(player.MBS_CLICK)

	def Lerp(self, a, b, t):
		return (1 - t) * a + t * b

	def __bioClear(self):
		constInfo.BIO_DICT = []
		self.interface.wndBio.ClearBio()

	def __bioUpdate(self, v1,v2,v3,v4):
		#chat.AppendChat(0, "BioUpdate")
		for frontmodifier in range(len(constInfo.BIO_DICT)):
				constInfo.BIO_DICT[frontmodifier]["STATE"] = 0
				constInfo.BIO_DICT[frontmodifier]["STATUS"] = 0		

		counter = 0
		for x in constInfo.BIO_DICT:
			if x["LEVEL"] == int(v1): ##60 -> Counter: 3
				x["COUNT"] = int(v2)
				x["STATE"] = int(v3)
				x["STATUS"] = 1
				x["LAST_TRY"] = int(v4)
				#chat.AppendChat(0, "%s %s %s %s" % (v1,v2,v3,v4))
				break
				
			counter += 1
		
		if counter > 0:
			for backmodifier in range(counter):
				constInfo.BIO_DICT[backmodifier]["STATE"] = 0
				constInfo.BIO_DICT[backmodifier]["STATUS"] = 2
				
		self.interface.wndBio.UpdateBio()

	def __bioData(self, v1,v2,v3,v4,v5,v6,v7,v8,v9):
		data =	{
				"LEVEL": int(v1),
				"STATUS": 0, ## 0: Not ready | 1: In Progress | 2: Completed
				"STATE": 0, ## H?y van k?z?
				"ITEMS": [int(v2),int(v3),int(v4)],
				"NEED_COUNT": int(v5),
				"COUNT": 0,
				"LAST_TRY": 0, ##time
				"PERCENT": int(v6), ## success percent
				"LIMIT_TIME": int(v7), ##in seconds
				"BONUS": [int(v8), int(v9)] ## bonus
			}		
		
		#chat.AppendChat(0, "Data:" + str(v1))
		constInfo.BIO_DICT.append(data)

	def OnUpdate(self):
		app.UpdateGame()
		
		self.wnddailygift.OnUpdate()		
		if self.interface.IsPickUpItem():
			self.PickUpItem()

		if self.mapNameShower.IsShow():
			self.mapNameShower.Update()

		if self.isShowDebugInfo:
			self.UpdateDebugInfo()

		if self.enableXMasBoom:
			self.__XMasBoom_Update()

		if self.isCameraMoving == True:
			self.cameraMovementProgress += 0.01
			startLoc = [5827.0, 90.0, 200.0]
			global cameraDistance, cameraPitch, cameraRotation, cameraHeight
			(ucameraDistance, ucameraPitch, ucameraRotation, ucameraHeight) = app.GetCamera()
			dist = self.Lerp(startLoc[0], cameraDistance, self.cameraMovementProgress)
			put = self.Lerp(startLoc[1], cameraPitch, self.cameraMovementProgress)
			rot = self.Lerp(startLoc[2], cameraRotation, self.cameraMovementProgress)
			app.SetCamera(dist, put, rot, ucameraHeight)
			if self.cameraMovementProgress >= 1:
				self.isCameraMoving = False
				self.cameraMovementProgress = 0.0

		if constInfo.need_open_pickup_filter:
			constInfo.need_open_pickup_filter=0
			self.__EnablePickUpItem()
		if systemSetting.GetPickupAutoMode():
			self.PickUpItem()

		if constInfo.status_battle_pass == 1:
			self.battlepass_button.Show()
		else:
			self.battlepass_button.Hide()	
			
		self.interface.wndBio.OnUpdate()	
		self.interface.BUILD_OnUpdate()
		
		if app.ENABLE_PINGTIME:
			nPing = app.GetPingTime()
			self.pingLine.SetText("PING: %s ~" % (nPing))
##Mental Time
		localtime2 = localtime = time.strftime("%S")
		#if localtime == "00":
		#		self.__DayMode__Auto_Update1()
		#if localtime == "30":
		#		self.__DayMode__Auto_Update1()
		localtime = localtime = time.strftime("|cffC6E2FF%H:%M:%S")
		
		if not self._timeLine_hide:
			self._timeLine_on(localtime)
	
	def _timeLine_on(self, localtime):
		self.timeLine.SetText(localtime)
		self.timeLine.Show()
		self.timeLine.SetFontColor(8.0,7.0,7.0)
	def	_timeLine_off(self):
		self.timeLine.Hide()


	def UpdateDebugInfo(self):
		#
		# 캐릭터 좌표 및 FPS 출력
		(x, y, z) = player.GetMainCharacterPosition()
		nUpdateTime = app.GetUpdateTime()
		nUpdateFPS = app.GetUpdateFPS()
		nRenderFPS = app.GetRenderFPS()
		nFaceCount = app.GetFaceCount()
		fFaceSpeed = app.GetFaceSpeed()
		nST=background.GetRenderShadowTime()
		(fAveRT, nCurRT) =  app.GetRenderTime()
		(iNum, fFogStart, fFogEnd, fFarCilp) = background.GetDistanceSetInfo()
		(iPatch, iSplat, fSplatRatio, sTextureNum) = background.GetRenderedSplatNum()
		if iPatch == 0:
			iPatch = 1

		#(dwRenderedThing, dwRenderedCRC) = background.GetRenderedGraphicThingInstanceNum()

		self.PrintCoord.SetText("Coordinate: %.2f %.2f %.2f ATM: %d" % (x, y, z, app.GetAvailableTextureMemory()/(1024*1024)))
		xMouse, yMouse = wndMgr.GetMousePosition()
		self.PrintMousePos.SetText("MousePosition: %d %d" % (xMouse, yMouse))

		self.FrameRate.SetText("UFPS: %3d UT: %3d FS %.2f" % (nUpdateFPS, nUpdateTime, fFaceSpeed))

		if fAveRT>1.0:
			self.Pitch.SetText("RFPS: %3d RT:%.2f(%3d) FC: %d(%.2f) " % (nRenderFPS, fAveRT, nCurRT, nFaceCount, nFaceCount/fAveRT))

		self.Splat.SetText("PATCH: %d SPLAT: %d BAD(%.2f)" % (iPatch, iSplat, fSplatRatio))
		#self.Pitch.SetText("Pitch: %.2f" % (app.GetCameraPitch())
		#self.TextureNum.SetText("TN : %s" % (sTextureNum))
		#self.ObjectNum.SetText("GTI : %d, CRC : %d" % (dwRenderedThing, dwRenderedCRC))
		self.ViewDistance.SetText("Num : %d, FS : %f, FE : %f, FC : %f" % (iNum, fFogStart, fFogEnd, fFarCilp))

	def OnRender(self):
		app.RenderGame()

		if self.console.Console.collision:
			background.RenderCollision()
			chr.RenderCollision()

		(x, y) = app.GetCursorPosition()

		########################
		# Picking
		########################
		textTail.UpdateAllTextTail()

		if True == wndMgr.IsPickedWindow(self.hWnd):

			self.PickingCharacterIndex = chr.Pick()

			if -1 != self.PickingCharacterIndex:
				textTail.ShowCharacterTextTail(self.PickingCharacterIndex)
			if 0 != self.targetBoard.GetTargetVID():
				textTail.ShowCharacterTextTail(self.targetBoard.GetTargetVID())

			# ADD_ALWAYS_SHOW_NAME
			if not self.__IsShowName():
				self.PickingItemIndex = item.Pick()
				if -1 != self.PickingItemIndex:
					textTail.ShowItemTextTail(self.PickingItemIndex)
			# END_OF_ADD_ALWAYS_SHOW_NAME

		## Show all name in the range

		# ADD_ALWAYS_SHOW_NAME
		if self.__IsShowName():
			textTail.ShowAllTextTail()
			self.PickingItemIndex = textTail.Pick(x, y)
		# END_OF_ADD_ALWAYS_SHOW_NAME
		if app.ENABLE_SHOPNAMES_RANGE:
			if systemSetting.IsShowSalesText():
				uiPrivateShopBuilder.UpdateADBoard()
				uiOfflineShopBuilder.UpdateADBoard()


		textTail.UpdateShowingTextTail()
		textTail.ArrangeTextTail()
		if -1 != self.PickingItemIndex:
			textTail.SelectItemName(self.PickingItemIndex)

		grp.PopState()
		grp.SetInterfaceRenderState()

		textTail.Render()
		textTail.HideAllTextTail()

	def OnPressEscapeKey(self):
		if app.TARGET == app.GetCursor():
			app.SetCursor(app.NORMAL)

		elif True == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			self.interface.OpenSystemDialog()

		return True

	def OnIMEReturn(self):
		if app.IsPressed(app.DIK_LSHIFT):
			self.interface.OpenWhisperDialogWithoutTarget()
		else:
			self.interface.ToggleChat()
		return True

	def OnPressExitKey(self):
		self.interface.ToggleSystemDialog()
		return True

	## BINARY CALLBACK
	######################################################################################

	# EXCHANGE
	if app.WJ_ENABLE_TRADABLE_ICON:
		def BINARY_AddItemToExchange(self, inven_type, inven_pos, display_pos):
			if inven_type == player.INVENTORY:
				self.interface.CantTradableItemExchange(display_pos, inven_pos)
	# END_OF_EXCHANGE

	# WEDDING
	def BINARY_LoverInfo(self, name, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnAddLover(name, lovePoint)
		if self.affectShower:
			self.affectShower.SetLoverInfo(name, lovePoint)

	def BINARY_UpdateLovePoint(self, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnUpdateLovePoint(lovePoint)
		if self.affectShower:
			self.affectShower.OnUpdateLovePoint(lovePoint)
	# END_OF_WEDDING
	if app.ENABLE_SEND_TARGET_INFO:
		def BINARY_AddTargetMonsterDropInfo(self, raceNum, itemVnum, itemCount, rarity = 0):
			if not raceNum in constInfo.MONSTER_INFO_DATA:
				constInfo.MONSTER_INFO_DATA.update({raceNum : {}})
				constInfo.MONSTER_INFO_DATA[raceNum].update({"items" : []})
			curList = constInfo.MONSTER_INFO_DATA[raceNum]["items"]

			isUpgradeable = False
			isMetin = False
			item.SelectItem(itemVnum)
			if item.GetItemType() == item.ITEM_TYPE_WEAPON or item.GetItemType() == item.ITEM_TYPE_ARMOR:
				isUpgradeable = True
			elif item.GetItemType() == item.ITEM_TYPE_METIN:
				isMetin = True

			for curItem in curList:
				if isUpgradeable:
					if curItem.has_key("vnum_list") and curItem["vnum_list"][0] / 10 * 10 == itemVnum / 10 * 10:
						if not (itemVnum in curItem["vnum_list"]):
							curItem["vnum_list"].append(itemVnum)
						return
				elif isMetin:
					if curItem.has_key("vnum_list"):
						baseVnum = curItem["vnum_list"][0]
					if curItem.has_key("vnum_list") and (baseVnum - baseVnum%1000) == (itemVnum - itemVnum%1000):
						if not (itemVnum in curItem["vnum_list"]):
							curItem["vnum_list"].append(itemVnum)
						return
				else:
					if curItem.has_key("vnum") and curItem["vnum"] == itemVnum and curItem["count"] == itemCount:
						return

			if isUpgradeable or isMetin:
				curList.append({"vnum_list":[itemVnum], "count":itemCount, "rarity":rarity})
			else:
				curList.append({"vnum":itemVnum, "count":itemCount, "rarity":rarity})

		def BINARY_RefreshTargetMonsterDropInfo(self, raceNum):
			self.targetBoard.RefreshMonsterInfoBoard()

	# QUEST_CONFIRM
	def BINARY_OnQuestConfirm(self, msg, timeout, pid):
		confirmDialog = uiCommon.QuestionDialogWithTimeLimit()
		confirmDialog.Open(msg, timeout)
		confirmDialog.SetAcceptEvent(lambda answer=True, pid=pid: net.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		confirmDialog.SetCancelEvent(lambda answer=False, pid=pid: net.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		self.confirmDialog = confirmDialog
    # END_OF_QUEST_CONFIRM

    # GIFT command
	def Gift_Show(self):
		self.interface.ShowGift()

	# CUBE
	def BINARY_Cube_Open(self, npcVNUM):
		self.currentCubeNPC = npcVNUM

		self.interface.OpenCubeWindow()


		if npcVNUM not in self.cubeInformation:
			net.SendChatPacket("/cube r_info")
		else:
			cubeInfoList = self.cubeInformation[npcVNUM]

			i = 0
			for cubeInfo in cubeInfoList:
				self.interface.wndCube.AddCubeResultItem(cubeInfo["vnum"], cubeInfo["count"])

				j = 0
				for materialList in cubeInfo["materialList"]:
					for materialInfo in materialList:
						itemVnum, itemCount = materialInfo
						self.interface.wndCube.AddMaterialInfo(i, j, itemVnum, itemCount)
					j = j + 1

				i = i + 1

			self.interface.wndCube.Refresh()

	def BINARY_Cube_Close(self):
		self.interface.CloseCubeWindow()

	# 제작에 필요한 골드, 예상되는 완성품의 VNUM과 개수 정보 update
	def BINARY_Cube_UpdateInfo(self, gold, itemVnum, count):
		self.interface.UpdateCubeInfo(gold, itemVnum, count)

	def BINARY_Cube_Succeed(self, itemVnum, count):
		print "큐브 제작 성공"
		self.interface.SucceedCubeWork(itemVnum, count)
		pass

	def BINARY_Cube_Failed(self):
		print "큐브 제작 실패"
		self.interface.FailedCubeWork()
		pass

	def BINARY_Cube_ResultList(self, npcVNUM, listText):
		# ResultList Text Format : 72723,1/72725,1/72730.1/50001,5  이런식으로 "/" 문자로 구분된 리스트를 줌
		#print listText

		if npcVNUM == 0:
			npcVNUM = self.currentCubeNPC

		self.cubeInformation[npcVNUM] = []

		try:
			for eachInfoText in listText.split("/"):
				eachInfo = eachInfoText.split(",")
				itemVnum	= int(eachInfo[0])
				itemCount	= int(eachInfo[1])

				self.cubeInformation[npcVNUM].append({"vnum": itemVnum, "count": itemCount})
				self.interface.wndCube.AddCubeResultItem(itemVnum, itemCount)

			resultCount = len(self.cubeInformation[npcVNUM])
			requestCount = 7
			modCount = resultCount % requestCount
			splitCount = resultCount / requestCount
			for i in xrange(splitCount):
				#print("/cube r_info %d %d" % (i * requestCount, requestCount))
				net.SendChatPacket("/cube r_info %d %d" % (i * requestCount, requestCount))

			if 0 < modCount:
				#print("/cube r_info %d %d" % (splitCount * requestCount, modCount))
				net.SendChatPacket("/cube r_info %d %d" % (splitCount * requestCount, modCount))

		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

		pass

	def BINARY_Cube_MaterialInfo(self, startIndex, listCount, listText):
		# Material Text Format : 125,1|126,2|127,2|123,5&555,5&555,4/120000
		try:
			#print listText

			if 3 > len(listText):
				dbg.TraceError("Wrong Cube Material Infomation")
				return 0



			eachResultList = listText.split("@")

			cubeInfo = self.cubeInformation[self.currentCubeNPC]

			itemIndex = 0
			for eachResultText in eachResultList:
				cubeInfo[startIndex + itemIndex]["materialList"] = [[], [], [], [], []]
				materialList = cubeInfo[startIndex + itemIndex]["materialList"]

				gold = 0
				splitResult = eachResultText.split("/")
				if 1 < len(splitResult):
					gold = int(splitResult[1])

				#print "splitResult : ", splitResult
				eachMaterialList = splitResult[0].split("&")

				i = 0
				for eachMaterialText in eachMaterialList:
					complicatedList = eachMaterialText.split("|")

					if 0 < len(complicatedList):
						for complicatedText in complicatedList:
							(itemVnum, itemCount) = complicatedText.split(",")
							itemVnum = int(itemVnum)
							itemCount = int(itemCount)
							self.interface.wndCube.AddMaterialInfo(itemIndex + startIndex, i, itemVnum, itemCount)

							materialList[i].append((itemVnum, itemCount))

					else:
						itemVnum, itemCount = eachMaterialText.split(",")
						itemVnum = int(itemVnum)
						itemCount = int(itemCount)
						self.interface.wndCube.AddMaterialInfo(itemIndex + startIndex, i, itemVnum, itemCount)

						materialList[i].append((itemVnum, itemCount))

					i = i + 1



				itemIndex = itemIndex + 1

			self.interface.wndCube.Refresh()


		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

		pass

	# END_OF_CUBE

	# 용혼석
	def BINARY_Highlight_Item(self, inven_type, inven_pos):
		if self.interface:
			self.interface.Highlight_Item(inven_type, inven_pos)

	def BINARY_DragonSoulGiveQuilification(self):
		self.interface.DragonSoulGiveQuilification()

	def BINARY_DragonSoulRefineWindow_Open(self):
		self.interface.OpenDragonSoulRefineWindow()

	def BINARY_DragonSoulRefineWindow_RefineFail(self, reason, inven_type, inven_pos):
		self.interface.FailDragonSoulRefine(reason, inven_type, inven_pos)

	def BINARY_DragonSoulRefineWindow_RefineSucceed(self, inven_type, inven_pos):
		self.interface.SucceedDragonSoulRefine(inven_type, inven_pos)

	# END of DRAGON SOUL REFINE WINDOW

	def BINARY_SetBigMessage(self, message):
		self.interface.bigBoard.SetTip(message)

	def BINARY_SetMissionMessage(self, message):
		self.interface.missionBoard.SetMission(message)


	def BINARY_SetTipMessage(self, message):
		self.interface.tipBoard.SetTip(message)

	if app.ENABLE_DUNGEON_INFO_SYSTEM:
		def BINARY_DungeonInfoOpen(self):
			if self.interface:
				self.interface.DungeonInfoOpen()

		def BINARY_DungeonRankingRefresh(self):
			if self.interface:
				self.interface.DungeonRankingRefresh()

		def BINARY_DungeonInfoReload(self, onReset):
			if self.interface:
				self.interface.DungeonInfoReload(onReset)

	def BINARY_AppendNotifyMessage(self, type):
		if not type in localeInfo.NOTIFY_MESSAGE:
			return
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.NOTIFY_MESSAGE[type])

	def BINARY_Guild_EnterGuildArea(self, areaID):
		self.interface.BULID_EnterGuildArea(areaID)

	def BINARY_Guild_ExitGuildArea(self, areaID):
		self.interface.BULID_ExitGuildArea(areaID)

	def BINARY_GuildWar_OnSendDeclare(self, guildID):
		pass

	def BINARY_GuildWar_OnRecvDeclare(self, guildID, warType, maxPlayer, maxScore, warFlags, customMapIdx):
		if app.ENABLE_GENERAL_IN_GUILD:
			self.__GuildWar_OpenAskDialog(guildID, warType, maxPlayer, maxScore, warFlags, customMapIdx)
		else:
			mainCharacterName = player.GetMainCharacterName()
			masterName = guild.GetGuildMasterName()
			if mainCharacterName == masterName:
				self.__GuildWar_OpenAskDialog(guildID, warType, maxPlayer, maxScore, warFlags, customMapIdx)

	def BINARY_GuildWar_OnRecvPoint(self, gainGuildID, opponentGuildID, point):
		self.interface.OnRecvGuildWarPoint(gainGuildID, opponentGuildID, point)

	if app.__IMPROVED_GUILD_WAR__:
		def BINARY_GuildWar_OnStart(self, guildSelf, guildOpp, iMaxPlayer, iMaxScore, flags):
			self.interface.OnStartGuildWar(guildSelf, guildOpp)
			if app.GUILD_WAR_COUNTER:
				self.interface.GuildWarStaticSetGuildID(guildSelf, guildOpp,iMaxPlayer, iMaxScore, flags)
	else:
		def BINARY_GuildWar_OnStart(self, guildSelf, guildOpp):
			self.interface.OnStartGuildWar(guildSelf, guildOpp)
			if app.GUILD_WAR_COUNTER:
				self.interface.GuildWarStaticSetGuildID(guildSelf, guildOpp)

	def BINARY_GuildWar_OnEnd(self, guildSelf, guildOpp):
		self.interface.OnEndGuildWar(guildSelf, guildOpp)

	def BINARY_BettingGuildWar_SetObserverMode(self, isEnable):
		self.interface.BINARY_SetObserverMode(isEnable)

	def BINARY_BettingGuildWar_UpdateObserverCount(self, observerCount):
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	def __GuildWar_UpdateMemberCount(self, guildID1, memberCount1, guildID2, memberCount2, observerCount):
		guildID1 = int(guildID1)
		guildID2 = int(guildID2)
		memberCount1 = int(memberCount1)
		memberCount2 = int(memberCount2)
		observerCount = int(observerCount)

		self.interface.UpdateMemberCount(guildID1, memberCount1, guildID2, memberCount2)
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)
		
	def __GuildWar_OpenAskDialog(self, guildID, warType, maxPlayer, maxScore, warFlags, customMapIdx):

		guildName = guild.GetGuildName(guildID)

		# REMOVED_GUILD_BUG_FIX
		if "Noname" == guildName:
			return
		# END_OF_REMOVED_GUILD_BUG_FIX

		import uiGuild
		questionDialog = uiGuild.AcceptGuildWarDialog()
		questionDialog.SAFE_SetAcceptEvent(self.__GuildWar_OnAccept)
		questionDialog.SAFE_SetCancelEvent(self.__GuildWar_OnDecline)
		questionDialog.Open(guildName, warType, maxPlayer, maxScore, warFlags, customMapIdx)

		self.guildWarQuestionDialog = questionDialog

	# PROFESSIONAL_BIOLOG_SYSTEM
	if app.ENABLE_BIOLOG_SYSTEM:
		def BINARY_Biolog_Update(self, pLeftTime, pCountActual, pCountNeed, pVnum):
			uiprofessionalbiolog.BIOLOG_BINARY_LOADED["time"][0] = int(pLeftTime) + app.GetGlobalTimeStamp()
			uiprofessionalbiolog.BIOLOG_BINARY_LOADED["countActual"][0] = str(pCountActual)	
			uiprofessionalbiolog.BIOLOG_BINARY_LOADED["countNeed"][0] = str(pCountNeed)
			uiprofessionalbiolog.BIOLOG_BINARY_LOADED["vnum"][0] = int(pVnum)

		def BINARY_Biolog_SendMessage(self, pMessage):
			if str(pMessage) != "":
				self.wndBiologMessage = uiCommon.PopupDialog()
				self.wndBiologMessage.SetWidth(350)
				self.wndBiologMessage.SetText((str(pMessage).replace("$"," ")))
				self.wndBiologMessage.Show()
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, "Error, i could not initialize message from server!")

		def BINARY_Biolog_PopUp(self, iRewardType, iRewardItem, iBonusName_1, iBonusValue_1, iBonusName_2, iBonusValue_2):
			self.wndBiologSlider = uiprofessionalbiolog.Biolog_FinishSlider()
			self.wndBiologSlider.BINARY_BiologPopUp_Load([str(iRewardType), int(iRewardItem), str(iBonusName_1), int(iBonusValue_1), str(iBonusName_2), int(iBonusValue_2)])
			self.wndBiologSlider.Show()

		def BINARY_Biolog_SelectReward(self, iTypeWindow, iRewardType, iBonusName_1, iBonusValue_1, iBonusName_2, iBonusValue_2, iBonusName_3, iBonusValue_3):
			self.wndBiologSelectReward = uiprofessionalbiolog.Biolog_SelectReward()
			self.wndBiologSelectReward.Open_SelectRewardType([int(iTypeWindow), str(iRewardType), str(iBonusName_1), int(iBonusValue_1), str(iBonusName_2), int(iBonusValue_2), str(iBonusName_3), int(iBonusValue_3)])
			self.wndBiologSelectReward.SetTitle((str(iRewardType).replace("$"," ")))
			self.wndBiologSelectReward.SetCenterPosition()
			self.wndBiologSelectReward.SetTop()
			self.wndBiologSelectReward.Show()
	# END_OF_PROFESSIONAL_BIOLOG_SYSTEM

	if app.ENABLE_DECORUM:
		def BINARY_RecvDecorumBase(self, vid, decorum, legue, promotion, demotion, block):
			self.interface.SetDecorumBase(vid, decorum, legue, promotion, demotion, block)
				
		def BINARY_RecvDecorumBattle(self, vid, type, done, won):
			self.interface.SetDecorumBattle(vid, type, done, won)
				
		def BINARY_RecvDecorumKD(self, vid, kill, death):
			self.interface.SetDecorumKD(vid, kill, death)
				
		def __OnArenaConfirm(self, arenaID, arenaType):
			arenaTypeName = (uiScriptLocale.DECORUM_BLOCK_ARENA1, uiScriptLocale.DECORUM_BLOCK_ARENA2, uiScriptLocale.DECORUM_BLOCK_ARENA3)
			askString = uiScriptLocale.DECORUM_ACCEPT_ARENA % arenaTypeName[int(arenaType)]
			answerString = "/decorum_arena_accept %s" % arenaID
			
			confirmDialog = uiCommon.QuestionDialogWithTimeLimit()
			confirmDialog.Open(askString, 15)
			confirmDialog.SetAcceptEvent(lambda arenaID=arenaID: net.SendChatPacket(answerString) or self.confirmDialog.Hide())
			confirmDialog.SetCancelEvent(lambda: self.confirmDialog.Hide())
			self.confirmDialog = confirmDialog

	if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
		def OpenPrivateShopSearch(self, type):
			if self.interface:
				self.interface.OpenPrivateShopSearch(type)
		
		def RefreshShopSearch(self):
			# self.interface.RefreshShopSearch()
			self.interface.ShopSearchReady()
			
		def BuyShopSearch(self):
			self.interface.ShopSearchBuyDone()
			self.PopupMessage(localeInfo.PRIVATESHOPSEARCH_BUY_SUCCESS)


	def __GuildWar_CloseAskDialog(self):
		if self.guildWarQuestionDialog:
			self.guildWarQuestionDialog.Close()
			self.guildWarQuestionDialog = None

	def __GuildWar_OnAccept(self):
		warType = self.guildWarQuestionDialog.GetWarType()
		guildName = self.guildWarQuestionDialog.GetGuildName()
		maxScore = self.guildWarQuestionDialog.GetMaxScore()
		maxPlayer = self.guildWarQuestionDialog.GetMaxPlayerCount()
		warFlags = self.guildWarQuestionDialog.GetWarFlags()
		warCustomMapIdx = self.guildWarQuestionDialog.GetCustomMapIdx()

		net.SendChatPacket("/war %s %s %s %s %s %s" % (str(guildName), str(warType), str(maxPlayer), str(maxScore), str(warFlags), str(warCustomMapIdx)))
		self.__GuildWar_CloseAskDialog()

		return 1
        
	def __SendInvite(self, vid):
		chat.AppendChat(1, str(vid))
		net.SendPartyInvitePacket(vid)
		
	def __GuildWar_OnDecline(self):

		guildName = self.guildWarQuestionDialog.GetGuildName()

		net.SendChatPacket("/nowar " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1

	## BINARY CALLBACK
	######################################################################################

	def __ServerCommand_Build(self):
		serverCommandList={
			"ConsoleEnable"			: self.__Console_Enable,
			"DayMode"				: self.__DayMode_Update,
			"refreshinven"            : self.Update_inventory_ref,
			"PRESERVE_DayMode"		: self.__PRESERVE_DayMode_Update,
			"CloseRestartWindow"	: self.__RestartDialog_Close,
			"OpenPrivateShop"		: self.__PrivateShop_Open,
			"PartyHealReady"		: self.PartyHealReady,
			"update_envanter_lazim"   : self.Update_inventory_lazim,
			"ShowMeSafeboxPassword"	: self.AskSafeboxPassword,
			"spop"               	: self.__ShowPopup,
			"CloseSafebox"			: self.CommandCloseSafebox,
			"GET_INPUT_BEGIN" 	: self.GetInputBegin,
			"GET_INPUT_END" 	: self.GetInputEnd,

			"ReportLogin"			: self.ReportLogin,
			"Report"				: self.Report,
			"getinputbegin"                 : self.__Inputget1, 
			"getinputend"                   : self.__Inputget2,

			"GUILDSTORAGE"			: self._GuildStorageCMD,
			"GUILDSTORAGE_ADDITEM"	: self._GuildStorageAddItem,
			"GUILDSTORAGE_ADDITEMSLOT" : self._GuildStorageAddItemSlot,
			"GUILDSTORAGE_ADDMEMBER" : self._GuildStorageAddMemberToList,
			"GUILDSTORAGE_ADDTEMPSLOT" : self._GuildStorageTempSlotsAdd,
			"GUILDSTORAGE_ADDLOG"		: self._GuildStorageAddLog,
			"getinputbegin"			: self.__Inputget1,
			"getinputend"			: self.__Inputget2,
			
			# ITEM_MALL
			"CloseMall"				: self.CommandCloseMall,
			"ShowMeMallPassword"	: self.AskMallPassword,
			"item_mall"				: self.__ItemMall_Open,
			# END_OF_ITEM_MALL

			"RefineSuceeded"		: self.RefineSuceededMessage,
			"RefineFailed"			: self.RefineFailedMessage,
			"xmas_snow"				: self.__XMasSnow_Enable,
			"xmas_boom"				: self.__XMasBoom_Enable,
			"xmas_song"				: self.__XMasSong_Enable,
			"xmas_tree"				: self.__XMasTree_Enable,
			"newyear_boom"			: self.__XMasBoom_Enable,
			"PartyRequest"			: self.__PartyRequestQuestion,
			"PartyRequestDenied"	: self.__PartyRequestDenied,
			"horse_state"			: self.__Horse_UpdateState,
			"hide_horse_state"		: self.__Horse_HideState,   
			"PetEvolution"			: self.SetPetEvolution,
			"PetName"				: self.SetPetName,
			"PetLevel"				: self.SetPetLevel,
			"PetDuration"			: self.SetPetDuration,
			"PetBonus"				: self.SetPetBonus,
			"PetSkill"				: self.SetPetskill,
			"PetIcon"				: self.SetPetIcon,
			#"PetInvSlot"			: self.SetPetPosInv,
			"PetExp"				: self.SetPetExp,
			"PetUnsummon"			: self.PetUnsummon,
			#"PetActiveVnum"			: self.PetActive,
			"OpenPetIncubator"		: self.OpenPetIncubator,
			"test_server"			: self.__EnableTestServerFlag,
			"mall"					: self.__InGameShop_Show,
			"welcome"               : self.welcome_quest,
			# PROFESSIONAL_BIOLOG_SYSTEM
#			"BINARY_Biolog_Update"	:	self.BINARY_Biolog_Update,
#			"BINARY_Biolog_SendMessage"	:	self.BINARY_Biolog_SendMessage,	
#			"BINARY_Biolog_PopUp"	:	self.BINARY_Biolog_PopUp,
#			"BINARY_Biolog_SelectReward"	:	self.BINARY_Biolog_SelectReward,
			# END_OF_PROFESSIONAL_BIOLOG_SYSTEM				
			"getinputbegin"			: self.__Input_Get_Vegas_1,
			"getinputend"			: self.__Input_Get_Vegas_2,
			"getinput"				: self.__Input_Get_Vegas_3,
			"SELECT_JOB"			: self.SelectJob,

			# WEDDING
			"lover_login"			: self.__LoginLover,
			"lover_logout"			: self.__LogoutLover,
			"lover_near"			: self.__LoverNear,
			"lover_far"				: self.__LoverFar,
			"lover_divorce"			: self.__LoverDivorce,
			"PlayMusic"				: self.__PlayMusic,
			# END_OF_WEDDING
			# "RemoveItemFromList"					: self.interface.ShopSearchRemoveItem,

			"searched_item"				: self.SitemFinder,
			"searched_item_count"		: self.SitemFinderCounter,

			# PRIVATE_SHOP_PRICE_LIST
			"MyShopPriceList"		: self.__PrivateShop_PriceList,
			# END_OF_PRIVATE_SHOP_PRICE_LIST
			
			### Battle Pass
			"missions_bp"	:self.SMissionsBP,
			"info_missions_bp"	:self.SInfoMissions,
			"size_missions_bp"	:self.SizeMissions,
			"rewards_missions_bp"	:self.SRewardsMissions,
			"final_reward"	:self.SFinalRewards,
			"show_battlepass"	:self.interface.ShowBoardBpass,
			"status_battlepass"	:self.SBattlePass,
			"battlepass_status"	:self.SBattlePass2,
			### Battle Pass END

			"bioUpdate"	:	self.__bioUpdate,
			"bioClear"	:	self.__bioClear,
			"bioData"	:	self.__bioData,
			"openBio"	:	self.interface.wndBio.OpenWindow,
			"OpenHunt"	:	self.interface.ToggleHuntingWindow,
			
			"RefreshSStat"		: self.RefreshSpecialStats,
		
			"ManagerGiftSystem"		: self.ManagerGiftSystem,
		}

		if app.ENABLE_DECORUM:
			serverCommandList.update({
				"DecorumRandomArena"	:self.__OnArenaConfirm,
			})
			
		serverCommandList.update({ "/ride"	:self.__PressGKey2, })
	
		if app.ENABLE_HUNTING_SYSTEM:
			serverCommandList["HuntingButtonFlash"] = self.SetHuntingButtonFlash

		if app.ENABLE_CHEQUE_SYSTEM:
			serverCommandList.update({"MyShopPriceListNew"		: self.__PrivateShop_PriceListNew,})

		if app.ENABLE_OVER_KILL:
			serverCommandList["SingleKillSound"]    = self.__CommandSingleKillSound
		if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
			serverCommandList["auto_stack_storage"]	= self.interface.AutoStackStorage
		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			serverCommandList["COSTUME_HIDE_CLEAR"] = self.COSTUME_HIDE_CLEAR
			serverCommandList["COSTUME_HIDE_LIST"] 	= self.COSTUME_HIDE_LIST
			serverCommandList["COSTUME_HIDE_LOAD"] 	= self.COSTUME_HIDE_LOAD
		if app.ENABLE_EXPRESSING_EMOTION:	
			serverCommandList["SERVER_EMOTIONS_CLEAR"] 				= self.SERVER_EMOTIONS_CLEAR
			serverCommandList["SERVER_EMOTIONS_ADD"] 				= self.SERVER_EMOTIONS_ADD
			serverCommandList["SERVER_EMOTIONS_LOAD"] 				= self.SERVER_EMOTIONS_LOAD		
		if constInfo.ENABLE_AURA_SYSTEM:
			serverCommandList.update({"AuraMessage" : self.GetAuraInfo})      
		if app.ENABLE_6_7_BONUS_NEW_SYSTEM:
			serverCommandList["OpenSkillbookCombinationDialog"] = self.OpenSkillbookCombinationDialog
			serverCommandList["OpenAttr67BonusNew"] 			= self.OpenAttr67BonusNew
		if app.GUILD_WAR_COUNTER:
			serverCommandList.update({"OpenGuildStatisticsLog" : self.interface.OpenGuildWarLog})
		if app.ENABLE_RENEWAL_PVP:
			serverCommandList.update({"OpenPvPWindow" : self.interface.OpenPvPSecond})
			
		if app.WORLD_BOSS_YUMA:
			serverCommandList["SendWorldbossNotification"] = self.WorldbossNotficiation
		
		if app.ENABLE_ANTI_EXP:
			serverCommandList.update({"SetAntiExp" : self.SetAntiExp})
		if app.ENABLE_GUILD_REQUEST:
			serverCommandList.update({"OpenGuildRequest" : self.interface.OpenGuildRequest})
		serverCommandList.update({"RefreshDungeonFloor" : self.RefreshDungeonFloor })
		serverCommandList.update({"RefreshDungeonTimer" : self.RefreshDungeonTimer })

		serverCommandList.update({"PetInvSlotOld" : self.PetInvSlotOld})
		if app.ENABLE_DEFENSAWESHIP:
			serverCommandList.update({"gethydrahp" : self.__HydraGetHp })
		self.serverCommander=stringCommander.Analyzer()
		if app.ENABLE_MULTI_LANGUAGE_SYSTEM:
			serverCommandList["BINARY_SET_LANG_AND_EMPIRE_FLAG"] = self.BINARY_SET_LANG_AND_EMPIRE_FLAG
		for serverCommandItem in serverCommandList.items():
			self.serverCommander.SAFE_RegisterCallBack(
				serverCommandItem[0], serverCommandItem[1]
			)

	if app.ENABLE_OVER_KILL:
		def __CommandSingleKillSound(self):
			snd.PlaySound("sound/effect/over_kill/single_kill.waw")

	if constInfo.ENABLE_AURA_SYSTEM:
		def GetAuraInfo(self, arg):
			v = int(arg)
			if v == 4:
				self.interface.auraAbs.Show()
			elif v == 5:
				self.interface.auraUpgrade.Show()
			elif v == 69:
				self.interface.auraEXP.Show()
			else:
				if self.interface.auraAbs.IsShow():
					self.interface.auraAbs.GetGameInfo(v)
				elif self.interface.auraUpgrade.IsShow():
					self.interface.auraUpgrade.GetGameInfo(v)
				elif self.interface.auraEXP.IsShow():
					self.interface.auraEXP.GetGameInfo(v)

	if app.ENABLE_CUBE_RENEWAL_WORLDARD:
		def BINARY_CUBE_RENEWAL_OPEN(self):
			if self.interface:
				self.interface.BINARY_CUBE_RENEWAL_OPEN()

	if app.ENABLE_6_7_BONUS_NEW_SYSTEM:
		def OpenSkillbookCombinationDialog(self):
			self.interface.OpenSkillbookCombinationDialog()

		def OpenAttr67BonusNew(self):
			self.interface.OpenAttr67BonusNew()

		def BINARY_BONUS_67_NEW_FRAGMENT_GET(self, vnum):
			self.interface.AddMaterialSlot(vnum)

	# def ManagerGiftSystem(self, cmd):
		# cmd = cmd.split("|")
		# if cmd[0] == "Show":
			# self.PopupMessage("Le ricompense saranno disponibili a breve!")
			# #self.wnddailygift.Show()
		# elif cmd[0] == "DeleteRewards":
			# self.wnddailygift.DeleteRewards()
		# elif cmd[0] == "SetDailyReward":
			# self.wnddailygift.SetDailyReward(cmd[1]) # numero de la recompensa
		# elif cmd[0] == "SetTime":
			# self.wnddailygift.SetTime(cmd[1]) # tiempo en numeros grandes
		# elif cmd[0] == "SetReward":
			# self.wnddailygift.SetReward(cmd[1], cmd[2]) #hacer un array con los items
		# elif cmd[0] == "SetRewardDone":
			# self.wnddailygift.SetRewardDone()
			
	def ManagerGiftSystem(self, cmd):
		cmd = cmd.split("|")
		if cmd[0] == "Show":
			self.wnddailygift.Show()
		elif cmd[0] == "DeleteRewards":
			self.wnddailygift.DeleteRewards()
		elif cmd[0] == "SetDailyReward":
			self.wnddailygift.SetDailyReward(cmd[1]) # numero de la recompensa
		elif cmd[0] == "SetTime":
			self.wnddailygift.SetTime(cmd[1]) # tiempo en numeros grandes
		elif cmd[0] == "SetReward":
			self.wnddailygift.SetReward(cmd[1], cmd[2]) #hacer un array con los items
		elif cmd[0] == "SetRewardDone":
			self.wnddailygift.SetRewardDone()

	if app.ENABLE_GUILD_REQUEST:
		def GuildRequestLoadName(self, tabIndex):
			self.interface.GuildRequestLoadName(int(tabIndex))
		def GuildRequestLoadPage(self, tabIndex, pageIndex, maxPage):
			self.interface.GuildRequestLoadPage(int(tabIndex), int(pageIndex), int(maxPage))
		def GuildRequestSetItem(self, index, g_id, name, level, ladder_point, membercount, maxmember, isRequest):
			self.interface.GuildRequestSetItem(int(index), int(g_id), str(name), int(level), int(ladder_point), int(membercount), int(maxmember), int(isRequest))
		def GuildRequestSetRequest(self, index, pid, name, level, race, skillIndex):
			self.interface.GuildRequestSetRequest(int(index), int(pid), str(name), int(level), int(race), int(skillIndex))

	if app.ENABLE_HUNTING_SYSTEM:
		def SetHuntingButtonFlash(self):
			if constInfo.HUNTING_MAIN_UI_SHOW == 0:
				constInfo.HUNTING_BUTTON_FLASH = 1

	def BINARY_ServerCommand_Run(self, line):
		#dbg.TraceError(line)
		try:
			#print " BINARY_ServerCommand_Run", line
			return self.serverCommander.Run(line)
		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

	def __ProcessPreservedServerCommand(self):
		try:
			command = net.GetPreservedServerCommand()
			while command:
				print " __ProcessPreservedServerCommand", command
				self.serverCommander.Run(command)
				command = net.GetPreservedServerCommand()
		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

	def ReportLogin(self, id):
		constInfo.ReportLogin = int(id)
		
	def Report(self):
		net.SendQuestInputStringPacket(constInfo.ReportEntered)
		
	def __Inputget1(self):
		constInfo.INPUT = 1 

	def __Inputget2(self):
		constInfo.INPUT = 0

	def PartyHealReady(self):
		self.interface.PartyHealReady()

	if app.GUILD_RANK_SYSTEM:
		def BINARY_GUILD_RANK_OPEN(self):
			self.interface.OpenGuildRanking()

	if app.__BL_RANKING__:
		def BINARY_RANK_OPEN(self):
			self.interface.OpenPlayerRanking()

	def AskSafeboxPassword(self):
		self.interface.AskSafeboxPassword()

	if app.__BL_SOUL_ROULETTE__:
		def BINARY_ROULETTE_OPEN(self, price):
			if self.interface:
				self.interface.Roulette_Open(price)
		def BINARY_ROULETTE_CLOSE(self):
			if self.interface:
				self.interface.Roulette_Close()
		def BINARY_ROULETTE_TURN(self, spin, idx):
			if self.interface:
				self.interface.Roulette_TurnWheel(spin, idx)
		def BINARY_ROULETTE_ICON(self, idx, vnum, count):
			if self.interface:
				self.interface.Roulette_SetIcons(idx, vnum, count)

	def RefreshDungeonTimer(self, Floor,Time):
		if self.interface:
			if self.interface.wndMiniMap:
				self.interface.wndMiniMap.HideMiniMap()
				self.interface.wndMiniMap.Hide()
			self.interface.MakeDungeonTimerWindow()
			if self.interface.wndDungeonTimer:
				self.interface.wndDungeonTimer.RefreshDungeonTimer(Time, Floor)
	def RefreshDungeonFloor(self, Floor2):
		if self.interface:
			if self.interface.wndMiniMap:
				self.interface.wndMiniMap.HideMiniMap()
				self.interface.wndMiniMap.Hide()
			self.interface.MakeDungeonTimerWindow()
			if self.interface.wndDungeonTimer:
				self.interface.wndDungeonTimer.RefreshDungeonFloor(Floor2)

	def GetSearchedItemData(self, row, seller_name,seller_vid, item_vnum, item_count, item_refine, item_price, item_level,sockets,attrs,item_pos,transmutation):
		self.PrivateShopSearch.LoadItems(row, seller_name,seller_vid, item_vnum, item_count, item_refine, item_price, item_level,sockets,attrs,item_pos, transmutation)

	def CreateSearchedItemList(self):
		self.interface.ShopSearchReady()

	# ITEM_MALL
	def AskMallPassword(self):
		self.interface.AskMallPassword()

	def __ItemMall_Open(self):
		self.interface.OpenItemMall();

	def CommandCloseMall(self):
		self.interface.CommandCloseMall()
	# END_OF_ITEM_MALL

  	## Worldboss ##
	if app.WORLD_BOSS_YUMA:				
		def WorldbossNotficiation(self, szString):
			if self.interface:
				szString = szString.replace("_", " ")
				self.interface.WorldbossNotification(szString)

	def RefineSuceededMessage(self):
		self.PopupMessage(localeInfo.REFINE_SUCCESS)
		snd.PlaySound("sound/ui/make_soket.wav")
		if app.ENABLE_REFINE_RENEWAL:
			self.interface.CheckRefineDialog(False)

	def RefineFailedMessage(self):
		self.PopupMessage(localeInfo.REFINE_FAILURE)
		snd.PlaySound("sound/ui/jaeryun_fail.wav")
		if app.ENABLE_REFINE_RENEWAL:
			self.interface.CheckRefineDialog(True)

	def CommandCloseSafebox(self):
		self.interface.CommandCloseSafebox()

	# PRIVATE_SHOP_PRICE_LIST
	def __PrivateShop_PriceList(self, itemVNum, itemPrice):
			uiPrivateShopBuilder.SetPrivateShopItemPrice(itemVNum, itemPrice)
	# END_OF_PRIVATE_SHOP_PRICE_LIST
			
	
	def SetPetEvolution(self, evo):
		petname = ["Cucciolo", "Selvaggio", "Coraggioso", "Eroico"]
		self.petmain.SetEvolveName(petname[int(evo)])
	
	def SetPetName(self, name):
		if len(name) > 1 and name != "":
			self.petmini.Show()
		self.petmain.SetName(name)
	
	def SetPetLevel(self, level):
		self.petmain.SetLevel(level)
	
	def SetPetDuration(self, dur, durt):
		if int(durt) > 0:
			self.petmini.SetDuration(dur, durt)
		self.petmain.SetDuration(dur, durt)
	
	def SetPetBonus(self, hp, dif, sp):
		self.petmain.SetHp(hp)
		self.petmain.SetDef(dif)
		self.petmain.SetSp(sp)
		
	def SetPetskill(self, slot, idx, lv):
		if int(lv) > 0:
			self.petmini.SetSkill(slot, idx, lv)
		self.petmain.SetSkill(slot, idx, lv)
		self.affectShower.BINARY_NEW_AddAffect(5400+int(idx),int(constInfo.LASTAFFECT_POINT)+1,int(constInfo.LASTAFFECT_VALUE)+1, 0)
		if int(slot)==0:
			constInfo.SKILL_PET1=5400+int(idx)
		if int(slot)==1:
			constInfo.SKILL_PET2=5400+int(idx)
		if int(slot)==2:
			constInfo.SKILL_PET3=5400+int(idx)

	def SetPetPos(self, pos):
		constInfo.PetPosInv = int(pos)

	def SetPetIcon(self, vnum):
		if int(vnum) > 0:
			self.petmini.SetImageSlot(vnum)
		self.petmain.SetImageSlot(vnum)
		constInfo.PetOfficialVnum = int(vnum)
		
	def SetPetExp(self, exp, expi, exptot):
		if int(exptot) > 0:
			self.petmini.SetExperience(exp, expi, exptot)
		self.petmain.SetExperience(exp, expi, exptot)

	def PetInvSlotOld(self, vnum):
		constInfo.PetVnum = int(vnum)
		self.interface.wndInventory.RefreshItemSlot()

	def PetUnsummon(self):
		self.petmini.SetDefaultInfo()
		self.petmini.Close()
		self.petmain.SetDefaultInfo()
		self.affectShower.BINARY_NEW_RemoveAffect(int(constInfo.SKILL_PET1),0)
		self.affectShower.BINARY_NEW_RemoveAffect(int(constInfo.SKILL_PET2),0)
		self.affectShower.BINARY_NEW_RemoveAffect(int(constInfo.SKILL_PET3),0)
		constInfo.SKILL_PET1 = 0
		constInfo.SKILL_PET2 = 0
		constInfo.SKILL_PET3 = 0
		constInfo.PetOfficialVnum = 0
	
	def OpenPetMainGui(self):
		if constInfo.PET_MAIN == 0:
			self.petmain.Show()
			self.petmain.SetTop()
			constInfo.PET_MAIN = 1
		else:
			self.petmain.Close()

	def OpenPetIncubator(self, pet_new = 0):
		import uipetincubatrice
		self.petinc = uipetincubatrice.PetSystemIncubator(pet_new)
		self.petinc.Show()
		self.petinc.SetTop()
		
	def OpenPetMini(self):
		self.petmini.Show()
		self.petmini.SetTop()
		
	def OpenPetFeed(self):
		
		self.feedwind = uipetfeed.PetFeedWindow()
		self.feedwind.Show()
		self.feedwind.SetTop()

	def Gift_Show(self):
		if constInfo.PET_MAIN == 0:
			self.petmain.Show()
			constInfo.PET_MAIN =1
			self.petmain.SetTop()
		else:
			self.petmain.Hide()
			constInfo.PET_MAIN =0    
 
	if app.ENABLE_CHEQUE_SYSTEM:
		def __PrivateShop_PriceListNew(self, itemVNum, itemPrice, itemCheque):
			uiPrivateShopBuilder.SetPrivateShopItemPrice(itemVNum, itemPrice)
			uiPrivateShopBuilder.SetPrivateShopItemCheque(itemVNum, itemCheque)
 
	if app.ENABLE_SPECIAL_STATS_SYSTEM:
		def RefreshSpecialStats(self, s1, s2, s3, s4, s5, s6):
			statskills = [s1, s2, s3, s4, s5, s6]
			for x in range(1, len(statskills)+1):
				self.interface.RefreshSpecialStatsSkill(x, int(statskills[x-1]))

	def __Horse_HideState(self):
		self.affectShower.SetHorseState(0, 0, 0)

	def __Horse_UpdateState(self, level, health, battery):
		self.affectShower.SetHorseState(int(level), int(health), int(battery))

	def __IsXMasMap(self):
		mapDict = ( "metin2_map_n_flame_01",
					"metin2_map_n_desert_01",
					"metin2_map_spiderdungeon",
					"metin2_map_deviltower1",
					"plechito_pyramide_dungeon",)

		if background.GetCurrentMapName() in mapDict:
			return False

		return True

	def __XMasSnow_Enable(self, mode):

		self.__XMasSong_Enable(mode)

		if "1"==mode:

			if not self.__IsXMasMap():
				return

			print "XMAS_SNOW ON"
			background.EnableSnow(1)

		else:
			print "XMAS_SNOW OFF"
			background.EnableSnow(0)

	def __XMasBoom_Enable(self, mode):
		if "1"==mode:

			if not self.__IsXMasMap():
				return

			print "XMAS_BOOM ON"
			self.__DayMode_Update("dark")
			self.enableXMasBoom = True
			self.startTimeXMasBoom = app.GetTime()
		else:
			print "XMAS_BOOM OFF"
			self.__DayMode_Update("light")
			self.enableXMasBoom = False

	def __XMasTree_Enable(self, grade):

		print "XMAS_TREE ", grade
		background.SetXMasTree(int(grade))

	def __XMasSong_Enable(self, mode):
		if "1"==mode:
			print "XMAS_SONG ON"

			XMAS_BGM = "xmas.mp3"

			if app.IsExistFile("BGM/" + XMAS_BGM)==1:
				if musicInfo.fieldMusic != "":
					snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

				musicInfo.fieldMusic=XMAS_BGM
				snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

		else:
			print "XMAS_SONG OFF"

			if musicInfo.fieldMusic != "":
				snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

			musicInfo.fieldMusic=musicInfo.METIN2THEMA
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	def __RestartDialog_Close(self):
		self.interface.CloseRestartDialog()

	def __Console_Enable(self):
		constInfo.CONSOLE_ENABLE = True
		self.consoleEnable = True
		app.EnableSpecialCameraMode()
		ui.EnablePaste(True)

	## PrivateShop
	def __PrivateShop_Open(self):
		self.interface.OpenPrivateShopInputNameDialog()

	def BINARY_PrivateShop_Appear(self, vid, text):
		self.interface.AppearPrivateShop(vid, text)

	def BINARY_PrivateShop_Disappear(self, vid):
		self.interface.DisappearPrivateShop(vid)

	if app.ENABLE_OFFLINE_SHOP_SYSTEM:
		def BINARY_OfflineShop_OpenOfflineShop(self):
			if self.interface:
				self.interface.OpenOfflineShopInputNameDialog()

		def BINARY_OfflineShop_CloseOfflineShopBuilderWindow(self):
			self.interface.CloseOfflineShopBuilder()

		def BINARY_OfflineShop_Appear(self, vid, text):
			if chr.GetInstanceType(vid) == chr.INSTANCE_TYPE_NPC:
				self.interface.AppearOfflineShop(vid, text)

		def BINARY_OfflineShop_Disappear(self, vid):
			if chr.GetInstanceType(vid) == chr.INSTANCE_TYPE_NPC:
				self.interface.DisappearOfflineShop(vid)

		# def BINARY_OfflineShop_UpdateOnlinePlayerCount(self, playerCount):
			# if self.interface:
				# self.interface.wndMiniMap.UpdateOnlinePlayerCount(playerCount)

		# def BINARY_OfflineShop_UpdateOnlineShopCount(self, shopCount):
			# if self.interface:
				# self.interface.wndMiniMap.UpdateOnlineShopCount(shopCount)

	## DayMode
	def __PRESERVE_DayMode_Update(self, mode):
		if "light"==mode:
			background.SetEnvironmentData(0)
		elif "dark"==mode:

			if not self.__IsXMasMap():
				return

			background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
			background.SetEnvironmentData(1)

	def __DayMode_Update(self, mode):
		if "light"==mode:
			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToLight)
		elif "dark"==mode:

			if not self.__IsXMasMap():
				return

			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToDark)

	def __DayMode_OnCompleteChangeToLight(self):
		background.SetEnvironmentData(0)
		self.curtain.FadeIn()

	def __DayMode_OnCompleteChangeToDark(self):
		background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
		background.SetEnvironmentData(1)
		self.curtain.FadeIn()

	if app.ENABLE_MAINTENANCE_SYSTEM:
		def BINARY_ShowMaintenanceSign(self, timeLeft, duration):
			self.interface.ShowMaintenanceSign(timeLeft, duration)

		def BINARY_HideMaintenanceSign(self):
			self.interface.HideMaintenanceSign()

	## XMasBoom
	def __XMasBoom_Update(self):

		self.BOOM_DATA_LIST = ( (2, 5), (5, 2), (7, 3), (10, 3), (20, 5) )
		if self.indexXMasBoom >= len(self.BOOM_DATA_LIST):
			return

		boomTime = self.BOOM_DATA_LIST[self.indexXMasBoom][0]
		boomCount = self.BOOM_DATA_LIST[self.indexXMasBoom][1]

		if app.GetTime() - self.startTimeXMasBoom > boomTime:

			self.indexXMasBoom += 1

			for i in xrange(boomCount):
				self.__XMasBoom_Boom()

	def __XMasBoom_Boom(self):
		x, y, z = player.GetMainCharacterPosition()
		randX = app.GetRandom(-150, 150)
		randY = app.GetRandom(-150, 150)

		snd.PlaySound3D(x+randX, -y+randY, z, "sound/common/etc/salute.mp3")

	def __PartyRequestQuestion(self, vid):
		vid = int(vid)
		partyRequestQuestionDialog = uiCommon.QuestionDialog()
		partyRequestQuestionDialog.SetText(chr.GetNameByVID(vid) + localeInfo.PARTY_DO_YOU_ACCEPT)
		partyRequestQuestionDialog.SetAcceptText(localeInfo.UI_ACCEPT)
		partyRequestQuestionDialog.SetCancelText(localeInfo.UI_DENY)
		partyRequestQuestionDialog.SetAcceptEvent(lambda arg=True: self.__AnswerPartyRequest(arg))
		partyRequestQuestionDialog.SetCancelEvent(lambda arg=False: self.__AnswerPartyRequest(arg))
		partyRequestQuestionDialog.Open()
		partyRequestQuestionDialog.vid = vid
		self.partyRequestQuestionDialog = partyRequestQuestionDialog

	def __AnswerPartyRequest(self, answer):
		if not self.partyRequestQuestionDialog:
			return

		vid = self.partyRequestQuestionDialog.vid

		if answer:
			net.SendChatPacket("/party_request_accept " + str(vid))
		else:
			net.SendChatPacket("/party_request_deny " + str(vid))

		self.partyRequestQuestionDialog.Close()
		self.partyRequestQuestionDialog = None

	def __PartyRequestDenied(self):
		self.PopupMessage(localeInfo.PARTY_REQUEST_DENIED)

	def __EnableTestServerFlag(self):
		app.EnableTestServerFlag()

	if app.BL_KILL_BAR:
		def AddKillInfo(self, killer, victim, killer_race, victim_race, weapon_type):
			if self.interface:
				self.interface.AddKillInfo(killer, victim, killer_race, victim_race, weapon_type)

	def __InGameShop_Show(self, url):
		if constInfo.IN_GAME_SHOP_ENABLE:
			self.interface.OpenWebWindow(url)

	# WEDDING
	def __LoginLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLoginLover()

	def __LogoutLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogoutLover()
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverNear(self):
		if self.affectShower:
			self.affectShower.ShowLoverState()

	def __LoverFar(self):
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverDivorce(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.ClearLoverInfo()
		if self.affectShower:
			self.affectShower.ClearLoverState()

	def SitemFinder(self, i, item, mob, i_vnum, count, prob, actives, mob_vnum):
		mob = str(mob).replace("_", " ")
		item = str(item).replace("_", " ")
		self.interface.AppendInfoFinder(int(i), str(mob), int(prob), int(actives), int(i_vnum), int(count), str(item))
		constInfo.finder_items[int(i)]={"iMobVnum":mob_vnum}
		constInfo.finder_items_v[int(i)]={"iItemVnum":i_vnum}

	def SitemFinderCounter(self, count):
		constInfo.finder_counts = int(count)

	def __PlayMusic(self, flag, filename):
		flag = int(flag)
		if flag:
			snd.FadeOutAllMusic()
			musicInfo.SaveLastPlayFieldMusic()
			snd.FadeInMusic("BGM/" + filename)
		else:
			snd.FadeOutAllMusic()
			musicInfo.LoadLastPlayFieldMusic()
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)
	# END_OF_WEDDING

	def	OpenMarbleShop(self):
		if self.wndMarbleShop.IsShow():
			self.wndMarbleShop.Hide()
		else:
			self.wndMarbleShop.Show()

	if app.ENABLE_CHANGELOOK_SYSTEM:
		def ActChangeLook(self, iAct):
			if self.interface:
				self.interface.ActChangeLook(iAct)

		def AlertChangeLook(self):
			self.PopupMessage(localeInfo.CHANGE_LOOK_DEL_ITEM)


	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def COSTUME_HIDE_CLEAR(self):
			self.interface.costume_hide_clear()
		def COSTUME_HIDE_LIST(self,slot,index):
			self.interface.costume_hide_list(slot,index)
		def COSTUME_HIDE_LOAD(self):
			self.interface.costume_hide_load()

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def ActAcce(self, iAct, bWindow):
			if self.interface:
				self.interface.ActAcce(iAct, bWindow)

		def AlertAcce(self, bWindow):
			snd.PlaySound("sound/ui/make_soket.wav")
			if bWindow:
				self.PopupMessage(localeInfo.ACCE_DEL_SERVEITEM)
			else:
				self.PopupMessage(localeInfo.ACCE_DEL_ABSORDITEM)

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
	
	# Mental Bonus
	def __BonusPage(self):
		
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
	# Mental Bonus END
	if app.SKILL_COOLTIME_UPDATE:
		def	SkillClearCoolTime(self, slotIndex):
			self.interface.SkillClearCoolTime(slotIndex)
	
	if app.ENABLE_EXTEND_INVEN_SYSTEM:	
		def Update_inventory_ref(self):
			if self.interface:
				self.interface.SetInventoryPageKilit()
				
		def Update_inventory_lazim(self, lazim):
			self.wndPopupDialog = uiCommon.PopupDialog()
			self.wndPopupDialog.SetText(lazim + " " + localeInfo.ENVANTER_ANAH_LAZIM)
			self.wndPopupDialog.Open()
			
	def __ShowPopup(self, arg):
		self.pop = uiPopup.PopupMsg()
		data = arg.split("|")
		self.pop.SetType(int(data[0]))
		self.pop.SetMsg(data[1])
		self.pop.Show()
		
	if app.ENABLE_SWITCHBOT:
		def RefreshSwitchbotWindow(self):
			self.interface.RefreshSwitchbotWindow()
			
		def RefreshSwitchbotItem(self, slot):
			self.interface.RefreshSwitchbotItem(slot)
			
	if app.ENABLE_EXPRESSING_EMOTION:	
		def SERVER_EMOTIONS_CLEAR(self):
			self.interface.ClearEmotionsNew()

		def SERVER_EMOTIONS_ADD(self,id_emotion,time_emotion):
			self.interface.AddEmotionsNew(int(id_emotion),int(time_emotion))
			
		def SERVER_EMOTIONS_LOAD(self):
			self.interface.RefreshEmotionsNew()

	if constInfo.ENABLE_SHOW_CHEST_DROP:
		def BINARY_AddChestDropInfo(self, chestVnum, pageIndex, slotIndex, itemVnum, itemCount):
			if self.interface:
				if self.interface.dlgChestDrop:
					self.interface.dlgChestDrop.AddChestDropItem(chestVnum, pageIndex, slotIndex, itemVnum, itemCount)
		def BINARY_RefreshChestDropInfo(self, chestVnum, sub):
			if self.interface:
				if self.interface.dlgChestDrop:
					self.interface.dlgChestDrop.RefreshItems(chestVnum, sub)

	def SMissionsBP(self, i, type, vnum, counts):
		constInfo.missions_bp[int(i)]={"iType":type, "iVnum":vnum, "iCount":counts}
	
	def SInfoMissions(self, i, counts, status, nume, image):
		nume = str(nume).replace("#", " ")
		constInfo.info_missions_bp[int(i)]={"iCounts":counts, "iStatus":status, "Name":nume, "Image":image}

	def SRewardsMissions(self, i, vnum1, vnum2, vnum3, count1, count2, count3):
		constInfo.rewards_bp[int(i)]={"iVnum1":vnum1, "iVnum2":vnum2, "iVnum3":vnum3,"iCount1":count1, "iCount2":count2, "iCount3":count3}
	
	def SizeMissions(self, size):
		constInfo.size_battle_pass = int(size)
		
	def SBattlePass(self, status):
		constInfo.status_battle_pass = int(status)
		
	def SBattlePass2(self, status):
		constInfo.battle_status_pass = int(status)

	def SFinalRewards(self, vnum1, vnum2, vnum3, count1, count2, count3):
		constInfo.final_rewards = [int(vnum1),int(vnum2),int(vnum3),int(count1),int(count2),int(count3)]
	
	def __Input_Get_Vegas_1(self):
		constInfo.INPUT_IGNORE = 1

	def __Input_Get_Vegas_2(self):
		constInfo.INPUT_IGNORE = 0

	def __Input_Get_Vegas_3(self):
		net.SendQuestInputStringPacket("1")

	def SelectJob(self, cmd):
		import uiselectjob
		cmd = cmd.split('#')	
		if cmd[0] == 'QID':
			constInfo.SelectJob['QID'] = int(cmd[1])
		elif cmd[0] == 'INPUT':
			constInfo.INPUT_IGNORE = int(cmd[1])
		elif cmd[0] == 'SEND':
			net.SendQuestInputStringPacket(str(constInfo.SelectJob['QCMD']))
			constInfo.SelectJob['QCMD'] = ''
		elif cmd[0] == 'OPEN':
			self.job_select = uiselectjob.JobSelectWindow()
			self.job_select.Open()	
		elif cmd[0] == 'CLOSE':
			self.job_select = uiselectjob.JobSelectWindow()
			self.job_select.RealClose()	

	def GetInputStart(self):
		constInfo.INPUT_IGNORE = 1

	def GetInputStop(self):
		constInfo.INPUT_IGNORE = 0	
		
	def GetInputBegin(self):
		constInfo.INPUT_IGNORE = 1
		
	def GetInputEnd(self):
		constInfo.INPUT_IGNORE = 0

	#welcome_QUEST
	def welcome_quest(self):
		snd.PlaySound("sound/ui/welcome.wav")
	#END_OF welcome_QUEST
	
	if app.GUILD_WAR_COUNTER:
		def OpenGuildWarStatics(self):
			self.interface.OpenGuildWarStatics()
		def SetStaticsStatus(self):
			self.interface.SetStaticsStatus()
		def GuildWarStaticsUpdate(self):
			self.interface.GuildWarStaticsUpdate()
		def GuildWarStaticsClear(self):
			self.interface.GuildWarStaticsClear()
		def GuildWarStaticsSpecial(self, pid, sub_index):
			self.interface.GuildWarStaticsSpecial(pid, sub_index)
		def GuildWarUpdateUserCount(self, id0, user0, id1, user1, observer):
			self.interface.UpdateMemberCount(int(id0), int(user0), int(id1), int(user1))
			self.interface.wndMiniMap.UpdateObserverCount(int(observer))
			self.interface.GuildWarStaticSetUser(int(id0), int(user0), int(id1), int(user1), int(observer))
		def UpdateObserverCount(self, observer):
			self.interface.UpdateObserverCount(observer)
		#def AddCSMessage(self, killerName, killerRace, victimName, victimRace):
			#self.interface.AddCSMessage(str(killerName), int(killerRace), str(victimName), int(victimRace))
		def GuildWarStatisticsSave(self, saveType, warID):
			uiGuildWarData.Save(saveType, warID)
		def GuildWarStatisticsEvent(self):
			self.interface.GuildWarStatisticsEvent()

	if app.ENABLE_GUILD_ONLINE_LIST:
		def GuildListRemove(self):
			self.interface.GuildListRemove()
		def GuildListSetData(self,guildID, guildName, masterOnline):
			self.interface.GuildListSetData(int(guildID), str(guildName), int(masterOnline))

	if app.ENABLE_ANTI_EXP:
		def SetAntiExp(self, flag):
			flag = int(flag)
			if self.interface:
				ptr = [self.interface.wndInventory,self.interface.wndCharacter]
				for gui in ptr:
					if gui:
						if flag:
							if gui.IsChild("AntiExp"):
								guiptr = gui.GetChild("AntiExp")
								guiptr.SetUpVisual("d:/ymir work/ui/anti_exp/anti_exp.tga")
								guiptr.SetOverVisual("d:/ymir work/ui/anti_exp/exp.tga")
								guiptr.SetDownVisual("d:/ymir work/ui/anti_exp/exp.tga")
								guiptr.Show()
								if gui.IsChild("RestExp_Value"):
									gui.GetChild("RestExp_Value").Hide()
								if gui.IsChild("Exp_Value"):
									gui.GetChild("Exp_Value").Hide()
								for j in range(1,5):
									if gui.IsChild("EXPGauge_0%d"%j):
										gui.GetChild("EXPGauge_0%d"%j).SetDiffuseColor(63,0,0,1)
						else:
							if gui.IsChild("AntiExp"):
								guiptr = gui.GetChild("AntiExp")
								guiptr.SetUpVisual("d:/ymir work/ui/anti_exp/exp.tga")
								guiptr.SetOverVisual("d:/ymir work/ui/anti_exp/anti_exp.tga")
								guiptr.SetDownVisual("d:/ymir work/ui/anti_exp/anti_exp.tga")
								guiptr.Show()
								if gui.IsChild("RestExp_Value"):
									gui.GetChild("RestExp_Value").Show()
								if gui.IsChild("Exp_Value"):
									gui.GetChild("Exp_Value").Show()
								for j in range(1,5):
									if gui.IsChild("EXPGauge_0%d"%j):
										gui.GetChild("EXPGauge_0%d"%j).SetDiffuseColor(201,160,51,1)

	if app.ENABLE_DEFENSAWESHIP:
		def __ShipMastHPShow(self):
			if self.wndShipMastHP:
				self.wndShipMastHP.Open(10000000, 10000000)

		def __HydraGetHp(self, curPoint):
			if self.wndShipMastHP:
				new = int(curPoint)
				self.wndShipMastHP.SetShipMastHP(new, 10000000)
				
	def _GuildStorageCMD(self, command):
		cmd = command.split("/")
		
		if cmd[0] == "OPEN":
			self.interface.GuildStorageWindow.Open(int(cmd[1]))
		elif cmd[0] == "REFRESH":
			self.interface.GuildStorageWindow.RefreshSlots()
		elif cmd[0] == "REFRESH_MONEY":
			self.interface.GuildStorageWindow.SetMoney(cmd[1])
		elif cmd[0] == "REFRESH_MEMBERS":
			self.interface.GuildStorageWindow.Adminpanel["board"].RefreshMembers()
		elif cmd[0] == "CLEAR_TEMPSLOTS":
			constInfo.GUILDSTORAGE["tempslots"] = {"TAB0" : {},"TAB1" : {},"TAB2" : {}}
		elif cmd[0] == "COMPARE_TEMPSLOTS":
			for i in range(3):
				if constInfo.GUILDSTORAGE["tempslots"]["TAB"+str(i)] != constInfo.GUILDSTORAGE["slots"]["TAB"+str(i)]:
					constInfo.GUILDSTORAGE["slots"]["TAB"+str(i)] = {}
					constInfo.GUILDSTORAGE["slots"]["TAB"+str(i)] = constInfo.GUILDSTORAGE["tempslots"]["TAB"+str(i)]
					self.interface.GuildStorageWindow.RefreshSlots()
		elif cmd[0] == "QID":
			self.GuildStorageQID(cmd[1])
		elif cmd[0] == "QUESTCMD":
			self._GuildStorageQuestCMD()
		elif cmd[0] == "MEMBER_COMPLETE":
			constInfo.GUILDSTORAGE["members"] = {}
			self.interface.GuildStorageWindow.ClearMembers()
			import event
			constInfo.GUILDSTORAGE["questCMD"] = "GETMEMBERLIST"
			event.QuestButtonClick(int(constInfo.GUILDSTORAGE["qid"]))
				
	def _GuildStorageAddItemSlot(self, slot, tab ,itemVnum, count, socket0, socket1, socket2, socket3, socket4, socket5, attrtype0,attrvalue0, attrtype1,attrvalue1, attrtype2, attrvalue2, attrtype3, attrvalue3, attrtype4, attrvalue4, attrtype5, attrvalue5, attrtype6, attrvalue6):
		self.interface.GuildStorageWindow.AddItemSlot(slot, tab ,itemVnum, count, socket0, socket1, socket2, socket3, socket4, socket5, attrtype0,attrvalue0, attrtype1,attrvalue1, attrtype2, attrvalue2, attrtype3, attrvalue3, attrtype4, attrvalue4, attrtype5, attrvalue5, attrtype6, attrvalue6)
	
	def _GuildStorageAddItem(self, slot ,itemVnum, count, socket0, socket1, socket2, socket3, socket4, socket5, attrtype0,attrvalue0, attrtype1,attrvalue1, attrtype2, attrvalue2, attrtype3, attrvalue3, attrtype4, attrvalue4, attrtype5, attrvalue5, attrtype6, attrvalue6):
		slotsWidth = 15
		slotsHeight = 8
		slot = int(slot)
		if slot <= 120:
			constInfo.GUILDSTORAGE["slots"]["TAB0"][slot] = [int(itemVnum),int(count), int(socket0), int(socket1), int(socket2), int(socket3), int(socket4), int(socket5), int(attrtype0),int(attrvalue0), int(attrtype1),int(attrvalue1), int(attrtype2), int(attrvalue2), int(attrtype3), int(attrvalue3), int(attrtype4), int(attrvalue4), int(attrtype5), int(attrvalue5), int(attrtype6), int(attrvalue6)]
		elif slot > 120 and slot <= 240:
			constInfo.GUILDSTORAGE["slots"]["TAB1"][slot-120] = [int(itemVnum),int(count), int(socket0), int(socket1), int(socket2), int(socket3), int(socket4), int(socket5), int(attrtype0),int(attrvalue0), int(attrtype1),int(attrvalue1), int(attrtype2), int(attrvalue2), int(attrtype3), int(attrvalue3), int(attrtype4), int(attrvalue4), int(attrtype5), int(attrvalue5), int(attrtype6), int(attrvalue6)]
		elif slot > 240 and slot <= 360:
			constInfo.GUILDSTORAGE["slots"]["TAB2"][slot-240] = [int(itemVnum),int(count), int(socket0), int(socket1), int(socket2), int(socket3), int(socket4), int(socket5), int(attrtype0),int(attrvalue0), int(attrtype1),int(attrvalue1), int(attrtype2), int(attrvalue2), int(attrtype3), int(attrvalue3), int(attrtype4), int(attrvalue4), int(attrtype5), int(attrvalue5), int(attrtype6), int(attrvalue6)]
	
	def _GuildStorageTempSlotsAdd(self,slot ,itemVnum, count, socket0, socket1, socket2, socket3, socket4, socket5, attrtype0,attrvalue0, attrtype1,attrvalue1, attrtype2, attrvalue2, attrtype3, attrvalue3, attrtype4, attrvalue4, attrtype5, attrvalue5, attrtype6, attrvalue6):
		slot = int(slot)
		if slot <= 120:
			constInfo.GUILDSTORAGE["tempslots"]["TAB0"][slot] = [int(itemVnum),int(count), int(socket0), int(socket1), int(socket2), int(socket3), int(socket4), int(socket5), int(attrtype0),int(attrvalue0), int(attrtype1),int(attrvalue1), int(attrtype2), int(attrvalue2), int(attrtype3), int(attrvalue3), int(attrtype4), int(attrvalue4), int(attrtype5), int(attrvalue5), int(attrtype6), int(attrvalue6)]
		elif slot > 120 and slot <= 240:
			constInfo.GUILDSTORAGE["tempslots"]["TAB1"][slot-120] = [int(itemVnum),int(count), int(socket0), int(socket1), int(socket2), int(socket3), int(socket4), int(socket5), int(attrtype0),int(attrvalue0), int(attrtype1),int(attrvalue1), int(attrtype2), int(attrvalue2), int(attrtype3), int(attrvalue3), int(attrtype4), int(attrvalue4), int(attrtype5), int(attrvalue5), int(attrtype6), int(attrvalue6)]
		elif slot > 240 and slot <= 360:
			constInfo.GUILDSTORAGE["tempslots"]["TAB2"][slot-240] = [int(itemVnum),int(count), int(socket0), int(socket1), int(socket2), int(socket3), int(socket4), int(socket5), int(attrtype0),int(attrvalue0), int(attrtype1),int(attrvalue1), int(attrtype2), int(attrvalue2), int(attrtype3), int(attrvalue3), int(attrtype4), int(attrvalue4), int(attrtype5), int(attrvalue5), int(attrtype6), int(attrvalue6)]
		
	def _GuildStorageAddLog(self,id,name,date,type,do,desc):
		self.interface.GuildStorageWindow.LogsInsert(id,name,date,type,do,desc)
		constInfo.GUILDSTORAGE["logs"][int(id)] = [name,date,type,do,desc]
		
	def _GuildStorageQuestCMD(self):
		net.SendQuestInputStringPacket(str(constInfo.GUILDSTORAGE["questCMD"]))
		constInfo.GUILDSTORAGE["questCMD"] = "NULL#"
	
	def GuildStorageQID(self, qid):
		constInfo.GUILDSTORAGE["qid"] = int(qid)
		
	def _GuildStorageAddMemberToList(self,memberId,member,authority0,authority1,authority2,authority3):
		constInfo.GUILDSTORAGE["members"]["member"+memberId] = [member,int(authority0),int(authority1),int(authority2),int(authority3)]

	def __Inputget1(self):
		constInfo.INPUT_IGNORE = 1

	def __Inputget2(self):
		constInfo.INPUT_IGNORE = 0

	if app.BL_MAILBOX:
		def MailBoxProcess(self, type, data):
			if self.interface:
				self.interface.MailBoxProcess( type, data )

		
class WaitingDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.eventTimeOver = lambda *arg: None
		self.eventExit = lambda *arg: None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/WarteSchleife.py")

		except:
			import exception
			exception.Abort("WaitingDialog.LoadDialog.BindObject")

	def Open(self, waitTime):
		curTime = time.clock()
		self.endTime = curTime + waitTime

		self.Show()		

	def Close(self):
		self.Hide()

	def Destroy(self):
		self.Hide()

	def SAFE_SetTimeOverEvent(self, event):
		self.eventTimeOver = ui.__mem_func__(event)

	def SAFE_SetExitEvent(self, event):
		self.eventExit = ui.__mem_func__(event)
		
	def OnUpdate(self):
		lastTime = max(0, self.endTime - time.clock())
		if 0 == lastTime:
			self.Close()
			self.eventTimeOver()
		else:
			return
		
	def OnPressExitKey(self):
		self.Close()
		return TRUE