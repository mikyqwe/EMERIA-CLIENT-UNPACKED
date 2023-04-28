#! /usr/bin/env python
__author__		= 'VegaS'
__date__		= '2020-02-04'
__name__		= 'IntroLoading Renewal'
__version__		= '3.8'

import ui
import uiScriptLocale
import net
import app
import player
import background
import wndMgr
import constInfo
import playerSettingModule
import colorInfo
import chrmgr
import localeInfo
import emotion
import os
import playerLoad


##################################
## loadingFunctions
##################################
NAME_COLOR_DICT = {
	chrmgr.NAMECOLOR_PC : colorInfo.CHR_NAME_RGB_PC,
	chrmgr.NAMECOLOR_NPC : colorInfo.CHR_NAME_RGB_NPC,
	chrmgr.NAMECOLOR_MOB : colorInfo.CHR_NAME_RGB_MOB,
	#chrmgr.NAMECOLOR_BOSS : colorInfo.CHR_NAME_RGB_BOSS,
	chrmgr.NAMECOLOR_PVP : colorInfo.CHR_NAME_RGB_PVP,
	chrmgr.NAMECOLOR_PK : colorInfo.CHR_NAME_RGB_PK,
	chrmgr.NAMECOLOR_PARTY : colorInfo.CHR_NAME_RGB_PARTY,
	chrmgr.NAMECOLOR_WARP : colorInfo.CHR_NAME_RGB_WARP,
	chrmgr.NAMECOLOR_WAYPOINT : colorInfo.CHR_NAME_RGB_WAYPOINT,
	chrmgr.NAMECOLOR_METIN : colorInfo.CHR_NAME_RGB_METIN,
	#chrmgr.NAMECOLOR_OFFLINESHOP : colorInfo.CHR_NAME_RGB_OFFLINESHOP,		
	#chrmgr.NAMECOLOR_METIN : colorInfo.CHR_NAME_RGB_METIN,	
	chrmgr.NAMECOLOR_EMPIRE_MOB : colorInfo.CHR_NAME_RGB_EMPIRE_MOB,
	chrmgr.NAMECOLOR_EMPIRE_NPC : colorInfo.CHR_NAME_RGB_EMPIRE_NPC,
	chrmgr.NAMECOLOR_EMPIRE_PC+1 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_A,
	chrmgr.NAMECOLOR_EMPIRE_PC+2 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_B,
	chrmgr.NAMECOLOR_EMPIRE_PC+3 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_C,
}

TITLE_COLOR_DICT = (
	colorInfo.TITLE_RGB_GOOD_4,
	colorInfo.TITLE_RGB_GOOD_3,
	colorInfo.TITLE_RGB_GOOD_2,
	colorInfo.TITLE_RGB_GOOD_1,
	colorInfo.TITLE_RGB_NORMAL,
	colorInfo.TITLE_RGB_EVIL_1,
	colorInfo.TITLE_RGB_EVIL_2,
	colorInfo.TITLE_RGB_EVIL_3,
	colorInfo.TITLE_RGB_EVIL_4,
)

def __main__():
	## RegisterColor
	for nameIndex, nameColor in NAME_COLOR_DICT.items():
		chrmgr.RegisterNameColor(nameIndex, *nameColor)

	for titleIndex, titleColor in enumerate(TITLE_COLOR_DICT):
		chrmgr.RegisterTitleColor(titleIndex, *titleColor)
		
	## RegisterTitleName	
	for titleIndex, titleName in enumerate(localeInfo.TITLE_NAME_LIST):
		chrmgr.RegisterTitleName(titleIndex, titleName)
		
	## RegisterEmotionIcon	
	emotion.RegisterEmotionIcons()
	
	#if app.ENABLE_SPECIAL_STATS_SYSTEM:
	#	talenti.RegisterSpecialStasIcons()
		
	## RegisterDungeonMapName	
	dungeonMapNameList = ("metin2_map_spiderdungeon", "metin2_map_monkeydungeon", "metin2_map_monkeydungeon_02", "metin2_map_monkeydungeon_03", "metin2_map_deviltower1")
	for dungeonMapName in dungeonMapNameList:
		background.RegisterDungeonMapName(dungeonMapName)
		
	## LoadGuildBuilding	
	playerSettingModule.LoadGuildBuildingList(localeInfo.GUILD_BUILDING_LIST_TXT)
	
	## Race Height
	playerSettingModule.LoadRaceHeight()
	
	## HIDE_SPECIAL_CHAT
	try:
		fileName = 'lib/hide_special_chat.inf'
		if os.path.exists(fileName):
			with open(fileName) as file:
				line = file.readline()
				if line:
					tokens = line.split()
					if tokens[0].isdigit():
						constInfo.HIDE_SPECIAL_CHAT = int(tokens[0])
	except:
		pass

##################################
## LoadingWindow
##################################
class LoadingWindow(ui.ScriptWindow):
	def __init__(self, stream):
		ui.Window.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_LOAD, self)

		self.stream = stream
		self.loadingImage = 0
		self.playerX, self.playerY = (0, 0)

	def __del__(self):
		net.SetPhaseWindow(net.PHASE_WINDOW_LOAD, 0)
		ui.Window.__del__(self)

	def Open(self):
		# ui.PythonScriptLoader().LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "LoadingWindow.py")
		try:
			ui.PythonScriptLoader().LoadScriptFile(self, "uiscript/LoginWindow_2.py")
		except:
			import exception
			exception.Abort("LodingWindow.Open - LoadScriptFile Error")
		try:
			self.loadingImage = self.GetChild("BackGround")
			self.loadingAniImage = self.GetChild("AnimBackGround")
		except:
			pass
		self.loadingImage.Hide()
		self.loadingAniImage.Hide()

		if constInfo.INTROSELECT_LOGIN:
			self.loadingAniImage.Hide()
			self.loadingImage.Show()
			constInfo.INTROSELECT_LOGIN = False
		else:
			self.loadingImage.Hide()
			self.loadingAniImage.Show()


		net.SendSelectCharacterPacket(self.stream.GetCharacterSlot())
		app.SetFrameSkip(0)
		self.Show()

	def Close(self):
		app.SetFrameSkip(1)
		self.Hide()

	def OnPressEscapeKey(self):
		app.SetFrameSkip(1)
		self.stream.SetLoginPhase()
		return True

	def DEBUG_LoadData(self, playerX, playerY):
		self.LoadData(playerX, playerY)

	def LoadData(self, playerX, playerY):
		playerLoad.RegisterSkill(net.GetMainActorRace(), net.GetMainActorSkillGroup(), net.GetMainActorEmpire())
		
		background.SetViewDistanceSet(background.DISTANCE0, 25600)
		background.SelectViewDistanceNum(background.DISTANCE0)
		app.SetGlobalCenterPosition(playerX, playerY)
		net.StartGame()