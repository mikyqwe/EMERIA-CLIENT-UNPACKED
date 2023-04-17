import ui
import uiScriptLocale
import wndMgr
import player
import miniMap
import localeInfo
import net
import app
import colorInfo
import constInfo
import background
import playersettingmodule
import item
import uiToolTip
import grp
import chr
import uiCommon
import chat
from _weakref import proxy

class MapTextToolTip(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)

		textLine = ui.TextLine()
		textLine.SetParent(self)
		#if not app.ENABLE_ATLAS_BOSS:
		textLine.SetHorizontalAlignCenter()
			
		textLine.SetOutline()
		#if not app.ENABLE_ATLAS_BOSS:
		#textLine.SetHorizontalAlignRight()
		#else:
			#textLine.SetHorizontalAlignLeft()
			
		textLine.Show()
		self.textLine = textLine

		if app.ENABLE_ATLAS_BOSS:
			textLine2 = ui.TextLine()
			textLine2.SetParent(self)
			textLine2.SetOutline()
			textLine2.SetHorizontalAlignLeft()
			textLine2.Show()
			self.textLine2 = textLine2

	def __del__(self):
		ui.Window.__del__(self)

	def SetText(self, text):
		self.textLine.SetText(text)

	if app.ENABLE_ATLAS_BOSS:
		def SetText2(self, text):
			self.textLine2.SetText(text)

		def ShowText2(self):
			self.textLine2.Show()

		def HideText2(self):
			self.textLine2.Hide()

	def SetTooltipPosition(self, PosX, PosY):
		if app.ENABLE_ATLAS_BOSS:
			PosY -= 24
		
		if localeInfo.IsARABIC():
			w, h = self.textLine.GetTextSize()
			self.textLine.SetPosition(PosX - w - 5, PosY)
			if app.ENABLE_ATLAS_BOSS:
				self.textLine2.SetPosition(PosX - w - 5, PosY + 10)
		else:
			self.textLine.SetPosition(PosX - 5, PosY)
			if app.ENABLE_ATLAS_BOSS:
				self.textLine2.SetPosition(PosX - 5, PosY + 10)

	def SetTextColor(self, TextColor):
		self.textLine.SetPackedFontColor(TextColor)
		if app.ENABLE_ATLAS_BOSS:
			self.textLine2.SetPackedFontColor(TextColor)

	def GetTextSize(self):
		return self.textLine.GetTextSize()

class AtlasWindow(ui.ScriptWindow):
	BOSS_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)

	class AtlasRenderer(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.AddFlag("not_pick")

		def OnUpdate(self):
			miniMap.UpdateAtlas()

		def OnRender(self):
			(x, y) = self.GetGlobalPosition()
			fx = float(x)
			fy = float(y)
			miniMap.RenderAtlas(fx, fy)

		def HideAtlas(self):
			miniMap.HideAtlas()

		def ShowAtlas(self):
			miniMap.ShowAtlas()

	def __init__(self):
		self.tooltipInfo = MapTextToolTip()
		self.tooltipInfo.Hide()
		self.infoGuildMark = ui.MarkBox()
		self.infoGuildMark.Hide()
		self.AtlasMainWindow = None
		self.mapName = ""
		self.board = 0

		ui.ScriptWindow.__init__(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def SetMapName(self, mapName):
		if 949==app.GetDefaultCodePage():
			try:
				self.board.SetTitleName(localeInfo.MINIMAP_ZONE_NAME_DICT[mapName])
			except:
				pass

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/AtlasWindow.py")
		except:
			import exception
			exception.Abort("AtlasWindow.LoadWindow.LoadScript")

		try:
			self.board = self.GetChild("board")

		except:
			import exception
			exception.Abort("AtlasWindow.LoadWindow.BindObject")

		self.AtlasMainWindow = self.AtlasRenderer()
		self.board.SetCloseEvent(self.Hide)
		self.AtlasMainWindow.SetParent(self.board)
		self.AtlasMainWindow.SetPosition(7, 30)
		self.tooltipInfo.SetParent(self.board)
		self.infoGuildMark.SetParent(self.board)
		self.SetPosition(wndMgr.GetScreenWidth() - 136 - 256 - 10, 0)
		self.Hide()

		miniMap.RegisterAtlasWindow(self)

	def Destroy(self):
		miniMap.UnregisterAtlasWindow()
		self.ClearDictionary()
		self.AtlasMainWindow = None
		self.tooltipAtlasClose = 0
		self.tooltipInfo = None
		self.infoGuildMark = None
		self.board = None


	def OnCancelQuestion(self):
		if self.questionDialog == None:
			return
		elif not self.questionDialog.IsShow():
			return
		
		self.questionDialog.iPosX = 0
		self.questionDialog.iPosY = 0
		self.questionDialog.Close()

	def OnAcceptQuestion(self):
		if self.questionDialog == None:
			return
		
		net.SendChatPacket("/gotoxy %d %d" % (self.questionDialog.iPosX, self.questionDialog.iPosY))
		self.OnCancelQuestion()

	def OnMoveWindow(self, x, y):
		self.OnCancelQuestion()

	def EventMouseLeftButtonUp(self):
		(mouseX, mouseY) = wndMgr.GetMousePosition()
		if app.ENABLE_ATLAS_BOSS:
			(bFind, sName, iPosX, iPosY, dwTextColor, dwGuildID, time) = miniMap.GetAtlasInfo(mouseX, mouseY)
		else:
			(bFind, sName, iPosX, iPosY, dwTextColor, dwGuildID) = miniMap.GetAtlasInfo(mouseX, mouseY)
		
		if self.questionDialog.IsShow():
			self.questionDialog.SetTop()
		
		if False == bFind:
			return 1
		
		self.questionDialog.SetText1(localeInfo.ATLASINFO_QUESTIONDIALOG1 % (sName))
		self.questionDialog.SetText2(localeInfo.ATLASINFO_QUESTIONDIALOG2)
		self.questionDialog.iPosX = iPosX
		self.questionDialog.iPosY = iPosY
		self.questionDialog.SetWidth(170 + len(sName * 5))
		self.questionDialog.Open()
		return 1

	def OnUpdate(self):

		if not self.tooltipInfo:
			return

		if not self.infoGuildMark:
			return

		self.infoGuildMark.Hide()
		self.tooltipInfo.Hide()

		if False == self.board.IsIn():
			return

		(mouseX, mouseY) = wndMgr.GetMousePosition()
		if app.ENABLE_ATLAS_BOSS:
			(bFind, sName, iPosX, iPosY, dwTextColor, dwGuildID, time) = miniMap.GetAtlasInfo(mouseX, mouseY)
		else:
			(bFind, sName, iPosX, iPosY, dwTextColor, dwGuildID) = miniMap.GetAtlasInfo(mouseX, mouseY)

		if False == bFind:
			return

		if "empty_guild_area" == sName:
			sName = localeInfo.GUILD_EMPTY_AREA

		if localeInfo.IsARABIC() and sName[-1].isalnum():
			self.tooltipInfo.SetText("(%s)%d, %d" % (sName, iPosX, iPosY))
			if app.ENABLE_ATLAS_BOSS:
				self.tooltipInfo.SetText2(localeInfo.MINIMAP_BOSS_RESPAWN_TIME % (time / 60))
		else:
			self.tooltipInfo.SetText("%s(%d, %d)" % (sName, iPosX, iPosY))
			if app.ENABLE_ATLAS_BOSS:
				self.tooltipInfo.SetText2(localeInfo.MINIMAP_BOSS_RESPAWN_TIME % (time / 60))

		(x, y) = self.GetGlobalPosition()
		self.tooltipInfo.SetTooltipPosition(mouseX - x, mouseY - y)
		if app.ENABLE_ATLAS_BOSS:
			if time > 0:
				self.tooltipInfo.SetTextColor(self.BOSS_COLOR)
				self.tooltipInfo.ShowText2()
			else:
				self.tooltipInfo.SetTextColor(dwTextColor)
				self.tooltipInfo.HideText2()
		else:
			self.tooltipInfo.SetTextColor(dwTextColor)
		self.tooltipInfo.Show()
		self.tooltipInfo.SetTop()

		if 0 != dwGuildID:
			textWidth, textHeight = self.tooltipInfo.GetTextSize()
			self.infoGuildMark.SetIndex(dwGuildID)
			self.infoGuildMark.SetPosition(mouseX - x - textWidth - 18 - 5, mouseY - y)
			self.infoGuildMark.Show()

	def Hide(self):
		if self.AtlasMainWindow:
			self.AtlasMainWindow.HideAtlas()
			self.AtlasMainWindow.Hide()
		ui.ScriptWindow.Hide(self)

	def Show(self):
		if self.AtlasMainWindow:
			(bGet, iSizeX, iSizeY) = miniMap.GetAtlasSize()
			if bGet:
				self.SetSize(iSizeX + 15, iSizeY + 38)

				if localeInfo.IsARABIC():
					self.board.SetPosition(iSizeX+15, 0)

				self.board.SetSize(iSizeX + 15, iSizeY + 38)
				#self.AtlasMainWindow.SetSize(iSizeX, iSizeY)
				self.AtlasMainWindow.ShowAtlas()
				self.AtlasMainWindow.Show()
		ui.ScriptWindow.Show(self)

	def SetCenterPositionAdjust(self, x, y):
		self.SetPosition((wndMgr.GetScreenWidth() - self.GetWidth()) / 2 + x, (wndMgr.GetScreenHeight() - self.GetHeight()) / 2 + y)

	def OnPressEscapeKey(self):
		self.Hide()
		return True

def __RegisterMiniMapColor(type, rgb):
	miniMap.RegisterColor(type, rgb[0], rgb[1], rgb[2])

class MiniMap(ui.ScriptWindow):

	CANNOT_SEE_INFO_MAP_DICT = {
		"metin2_map_monkeydungeon" : False,
		"metin2_map_monkeydungeon_02" : False,
		"metin2_map_monkeydungeon_03" : False,
		"metin2_map_devilsCatacomb" : False,
	}

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__Initialize()

		miniMap.Create()
		miniMap.SetScale(2.0)
		self.interface = None

		self.AtlasWindow = AtlasWindow()
		self.AtlasWindow.LoadWindow()
		self.AtlasWindow.Hide()

		self.tooltipMiniMapOpen = MapTextToolTip()
		self.tooltipMiniMapOpen.SetText(localeInfo.MINIMAP)
		self.tooltipMiniMapOpen.Show()
		self.tooltipMiniMapClose = MapTextToolTip()
		self.tooltipMiniMapClose.SetText(localeInfo.UI_CLOSE)
		self.tooltipMiniMapClose.Show()
		self.tooltipScaleUp = MapTextToolTip()
		self.tooltipScaleUp.SetText(localeInfo.MINIMAP_INC_SCALE)
		self.tooltipScaleUp.Show()
		self.tooltipScaleDown = MapTextToolTip()
		self.tooltipScaleDown.SetText(localeInfo.MINIMAP_DEC_SCALE)
		self.tooltipScaleDown.Show()
		self.tooltipAtlasOpen = MapTextToolTip()
		self.tooltipAtlasOpen.SetText(localeInfo.MINIMAP_SHOW_AREAMAP)
		self.tooltipAtlasOpen.Show()
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			self.tooltipDungeonInfoOpen = MapTextToolTip()
			self.tooltipDungeonInfoOpen.SetText("|cffF4B418Informazioni Dungeon")
			self.tooltipDungeonInfoOpen.Show()
		self.tooltipInfo = MapTextToolTip()
		self.tooltipInfo.Show()

		if miniMap.IsAtlas():
			self.tooltipAtlasOpen.SetText(localeInfo.MINIMAP_SHOW_AREAMAP)
		else:
			self.tooltipAtlasOpen.SetText(localeInfo.MINIMAP_CAN_NOT_SHOW_AREAMAP)

		self.tooltipInfo = MapTextToolTip()
		self.tooltipInfo.Show()

		self.mapName = ""

		self.isLoaded = 0
		self.canSeeInfo = True

		# AUTOBAN
		self.imprisonmentDuration = 0
		self.imprisonmentEndTime = 0
		self.imprisonmentEndTimeText = ""
		# END_OF_AUTOBAN

	def SetInterface(self, interface):
		self.interface = proxy(interface)

	def OpenBio(self):
		if self.interface:
			self.interface.wndBio.OpenWindow()

	def OpenHunt(self):
		if self.interface:
			self.interface.ToggleHuntingWindow()

	def __del__(self):
		miniMap.Destroy()
		ui.ScriptWindow.__del__(self)
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			self.interface = None

	def __Initialize(self):
		self.positionInfo = 0
		self.observerCount = 0
		self.renderInfo = 0
		self.OpenWindow = 0
		self.CloseWindow = 0
		self.ScaleUpButton = 0
		self.ScaleDownButton = 0
		self.MiniMapHideButton = 0
		self.MiniMapShowButton = 0
		self.AtlasShowButton = 0
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			self.DungeonInfoShowButton = 0
		self.tooltipMiniMapOpen = 0
		self.tooltipMiniMapClose = 0
		self.tooltipScaleUp = 0
		self.tooltipScaleDown = 0
		self.tooltipAtlasOpen = 0
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			self.tooltipDungeonInfoOpen = 0
		self.tooltipInfo = None
		self.serverInfo = None
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			self.interface = None

	def SetMapName(self, mapName):
		self.mapName=mapName
		self.AtlasWindow.SetMapName(mapName)

		if self.CANNOT_SEE_INFO_MAP_DICT.has_key(mapName):
			self.canSeeInfo = False
			self.HideMiniMap()
			self.tooltipMiniMapOpen.SetText(localeInfo.MINIMAP_CANNOT_SEE)
		else:
			self.canSeeInfo = True
			self.ShowMiniMap()
			self.tooltipMiniMapOpen.SetText(localeInfo.MINIMAP)

	# AUTOBAN
	def SetImprisonmentDuration(self, duration):
		self.imprisonmentDuration = duration
		self.imprisonmentEndTime = app.GetGlobalTimeStamp() + duration

		self.__UpdateImprisonmentDurationText()

	def __UpdateImprisonmentDurationText(self):
		restTime = max(self.imprisonmentEndTime - app.GetGlobalTimeStamp(), 0)

		imprisonmentEndTimeText = localeInfo.SecondToDHM(restTime)
		if imprisonmentEndTimeText != self.imprisonmentEndTimeText:
			self.imprisonmentEndTimeText = imprisonmentEndTimeText
			self.serverInfo.SetText("%s: %s" % (uiScriptLocale.AUTOBAN_QUIZ_REST_TIME, self.imprisonmentEndTimeText))
	# END_OF_AUTOBAN

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			if localeInfo.IsARABIC():
				pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "Minimap.py")
			else:
				pyScrLoader.LoadScriptFile(self, "UIScript/MiniMap.py")
		except:
			import exception
			exception.Abort("MiniMap.LoadWindow.LoadScript")

		try:
			self.OpenWindow = self.GetChild("OpenWindow")
			self.MiniMapWindow = self.GetChild("MiniMapWindow")
			self.ScaleUpButton = self.GetChild("ScaleUpButton")
			self.ScaleDownButton = self.GetChild("ScaleDownButton")
			self.MiniMapHideButton = self.GetChild("MiniMapHideButton")
			self.AtlasShowButton = self.GetChild("AtlasShowButton")
			self.CloseWindow = self.GetChild("CloseWindow")
			self.MiniMapShowButton = self.GetChild("MiniMapShowButton")
			self.positionInfo = self.GetChild("PositionInfo")
			self.observerCount = self.GetChild("ObserverCount")
			self.renderInfo = self.GetChild("RenderInfo")
			self.serverInfo = self.GetChild("ServerInfo")
			self.siteDiscord = self.GetChild("Discord")
			self.siteWiki = self.GetChild("Wiki")
			if app.ENABLE_RTT_STATISTICS:
				self.rttTextLine = self.GetChild("RTTTextLine")
				self.pktLossTextLine = self.GetChild("PacketLossTextLine")
			if app.ENABLE_DUNGEON_INFO_SYSTEM:
				self.DungeonInfoShowButton = self.GetChild("DungeonInfoShowButton")
			self.biologinfo = self.GetChild("BiologButton")
			self.biologinfo.SetEvent(self.OpenBio)
			self.huntginfo = self.GetChild("HuntingButton")
			self.huntginfo.SetEvent(self.OpenHunt)
		except:
			import exception
			exception.Abort("MiniMap.LoadWindow.Bind")

		if constInfo.MINIMAP_POSITIONINFO_ENABLE==0:
			self.positionInfo.Hide()

		self.serverInfo.SetText(net.GetServerInfo())
		self.ScaleUpButton.SetEvent(ui.__mem_func__(self.ScaleUp))
		self.ScaleDownButton.SetEvent(ui.__mem_func__(self.ScaleDown))
		self.MiniMapHideButton.SetEvent(ui.__mem_func__(self.HideMiniMap))
		self.MiniMapShowButton.SetEvent(ui.__mem_func__(self.ShowMiniMap))
		self.siteDiscord.SetEvent(ui.__mem_func__(self.discord))
		self.siteWiki.SetEvent(ui.__mem_func__(self.wiki))
			
		if miniMap.IsAtlas():
			self.AtlasShowButton.SetEvent(ui.__mem_func__(self.ShowAtlas))
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			self.DungeonInfoShowButton.SetEvent(ui.__mem_func__(self.ShowDungeonInfo))

		(ButtonPosX, ButtonPosY) = self.MiniMapShowButton.GetGlobalPosition()
		self.tooltipMiniMapOpen.SetTooltipPosition(ButtonPosX, ButtonPosY)

		(ButtonPosX, ButtonPosY) = self.MiniMapHideButton.GetGlobalPosition()
		self.tooltipMiniMapClose.SetTooltipPosition(ButtonPosX, ButtonPosY)

		(ButtonPosX, ButtonPosY) = self.ScaleUpButton.GetGlobalPosition()
		self.tooltipScaleUp.SetTooltipPosition(ButtonPosX, ButtonPosY)

		(ButtonPosX, ButtonPosY) = self.ScaleDownButton.GetGlobalPosition()
		self.tooltipScaleDown.SetTooltipPosition(ButtonPosX, ButtonPosY)

		(ButtonPosX, ButtonPosY) = self.AtlasShowButton.GetGlobalPosition()
		self.tooltipAtlasOpen.SetTooltipPosition(ButtonPosX, ButtonPosY)

		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			(ButtonPosX, ButtonPosY) = self.DungeonInfoShowButton.GetGlobalPosition()
			self.tooltipDungeonInfoOpen.SetTooltipPosition(ButtonPosX, ButtonPosY)

		self.ShowMiniMap()

	def Destroy(self):
		self.HideMiniMap()

		self.AtlasWindow.Destroy()
		self.AtlasWindow = None

		self.ClearDictionary()

		self.__Initialize()

	def UpdateObserverCount(self, observerCount):
		if observerCount>0:
			self.observerCount.Show()
		elif observerCount<=0:
			self.observerCount.Hide()

		self.observerCount.SetText(localeInfo.MINIMAP_OBSERVER_COUNT % observerCount)

	def protect_maps(self):
		protect_list = [
			"season99/new_map_ox",
			"maps_dungeon/devils_zone",
			"maps_dungeon/dt_zone",
			"maps_vegas/wedding_zone",
			"maps_dungeon/spider_3",  
			"maps_vegas/duel_zone",
		]
		if str(background.GetCurrentMapName()) in protect_list:
			return TRUE
		return FALSE    

	def change_ch(self, arg):
		if self.protect_maps():
			chat.AppendChat(1, "Non puoi cambiare CH in questa mappa.")
			return	
		elif time.clock() >= constInfo.change_time:
			net.SetServerInfo("Zayos - Channel %d" % int(arg+1))
			net.SendChatPacket("/ch %d" % int(arg+1))
			constInfo.change_time = time.clock() + 3
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Devi aspettare un attimo per cambiare channel.")

	def OnUpdate(self):
		(x, y, z) = player.GetMainCharacterPosition()
		miniMap.Update(x, y)

		if self.positionInfo:
			self.positionInfo.SetText("(%.0f, %.0f)" % (x/100, y/100))

# FPS RENDER
		nRenderFPS=app.GetRenderFPS()
		fps="%3d"%(nRenderFPS)	
		if self.positionInfo:
			self.renderInfo.SetText(uiScriptLocale.AEON_PERFORMANCE+ " " + str(fps))		
# FPS RENDER

		if app.ENABLE_RTT_STATISTICS:
			if self.rttTextLine and self.pktLossTextLine:
				rtt = app.GetRTT()
				pktLossPct = app.GetPacketLossPct()

				if rtt > 300:
					self.rttTextLine.SetFontColor((255.00 / 255), (0.00 / 255), (0.00 / 255)) # r, g, b
				elif rtt > 100 and rtt < 300:
					self.rttTextLine.SetFontColor((255.00 / 255), (255.00 / 255), (0.00 / 255)) # r, g, b
				else:
					self.rttTextLine.SetFontColor((0.00 / 255), (255.00 / 255), (0.00 / 255)) # r, g, b

				self.rttTextLine.SetText("Ping: %s%dms" % ("+" if rtt > 999 else "", 999 if rtt > 999 else rtt))
				self.pktLossTextLine.SetText("(%.2f%% pkt loss)" % (pktLossPct))

		if self.tooltipInfo:
			if True == self.MiniMapWindow.IsIn():
				(mouseX, mouseY) = wndMgr.GetMousePosition()
				(bFind, sName, iPosX, iPosY, dwTextColor) = miniMap.GetInfo(mouseX, mouseY)
				if bFind == 0:
					self.tooltipInfo.Hide()
				elif not self.canSeeInfo:
					self.tooltipInfo.SetText("%s(%s)" % (sName, localeInfo.UI_POS_UNKNOWN))
					self.tooltipInfo.SetTooltipPosition(mouseX - 5, mouseY)
					self.tooltipInfo.SetTextColor(dwTextColor)
					self.tooltipInfo.Show()
				else:
					if localeInfo.IsARABIC() and sName[-1].isalnum():
						self.tooltipInfo.SetText("(%s)%d, %d" % (sName, iPosX, iPosY))
					else:
						self.tooltipInfo.SetText("%s(%d, %d)" % (sName, iPosX, iPosY))
					self.tooltipInfo.SetTooltipPosition(mouseX - 5, mouseY)
					self.tooltipInfo.SetTextColor(dwTextColor)
					self.tooltipInfo.Show()
			else:
				self.tooltipInfo.Hide()

			# AUTOBAN
			if self.imprisonmentDuration:
				self.__UpdateImprisonmentDurationText()
			# END_OF_AUTOBAN

		if self.MiniMapShowButton:
			if True == self.MiniMapShowButton.IsIn():
				self.tooltipMiniMapOpen.Show()
			else:
				self.tooltipMiniMapOpen.Hide()

		if self.MiniMapHideButton:
			if True == self.MiniMapHideButton.IsIn():
				self.tooltipMiniMapClose.Show()
			else:
				self.tooltipMiniMapClose.Hide()

		if self.ScaleUpButton:
			if True == self.ScaleUpButton.IsIn():
				self.tooltipScaleUp.Show()
			else:
				self.tooltipScaleUp.Hide()

		if self.ScaleDownButton:
			if True == self.ScaleDownButton.IsIn():
				self.tooltipScaleDown.Show()
			else:
				self.tooltipScaleDown.Hide()

		if self.AtlasShowButton:
			if True == self.AtlasShowButton.IsIn():
				self.tooltipAtlasOpen.Show()
			else:
				self.tooltipAtlasOpen.Hide()
				
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			if self.DungeonInfoShowButton:
				if True == self.DungeonInfoShowButton.IsIn():
					self.tooltipDungeonInfoOpen.Show()
				else:
					self.tooltipDungeonInfoOpen.Hide()	

	def OnRender(self):
		(x, y) = self.GetGlobalPosition()
		fx = float(x)
		fy = float(y)
		miniMap.Render(fx + 4.0, fy + 5.0)

	def Close(self):
		self.HideMiniMap()

	def HideMiniMap(self):
		miniMap.Hide()
		self.OpenWindow.Hide()
		self.CloseWindow.Show()

	def ShowMiniMap(self):
		if not self.canSeeInfo:
			return

		miniMap.Show()
		self.OpenWindow.Show()
		self.CloseWindow.Hide()

	def isShowMiniMap(self):
		return miniMap.isShow()

	def ScaleUp(self):
		miniMap.ScaleUp()

	def ScaleDown(self):
		miniMap.ScaleDown()

	def ShowAtlas(self):
		if not miniMap.IsAtlas():
			return
		if not self.AtlasWindow.IsShow():
			self.AtlasWindow.Show()

	def discord(self):
		import os
		o="https://discord.com/invite/smKRtQdUem"
		os.startfile(o)

	def wiki(self):
		if self.interface:
			self.interface.OpenWikiWindow()
			# self.interface.ShowItemFinder()

	def ToggleAtlasWindow(self):
		if not miniMap.IsAtlas():
			return
		if self.AtlasWindow.IsShow():
			self.AtlasWindow.Hide()
		else:
			self.AtlasWindow.Show()
			
	if app.ENABLE_DUNGEON_INFO_SYSTEM:
		def ShowDungeonInfo(self):
			self.interface.ToggleDungeonInfoWindow()

		def BindInterfaceClass(self, interface):
			from _weakref import proxy
			self.interface = proxy(interface)
