import ui, player, net, app, guild, math, uiCommon, chr, constInfo, systemSetting, time
import localeInfo

from _weakref import proxy
import grp
import uiGuildWarData
CURRENT_LOG_WINDOW=None
OWN_GUILD_TEXT_COLOR = "FFFFF1"
LOSER_GUILD_TEXT_COLOR = "FF3D00"

MY_GUILD_ID = -1
MAIN_VID = ""
CURRENT_VID = ""

class GuildWarStatic(ui.ScriptWindow):

	class rankListBoxItem(ui.Window):
		def __lt__(self, other):
			return (self.kill >= other.kill and self.dead <= other.dead and self.skill_dmg >= other.skill_dmg and self.online >= other.online and self.spy <= other.spy)
		def __del__(self):
			ui.Window.__del__(self)
		def Destroy(self):
			self.children = {}
			self.spyDialog = None
			(self.name,self.level,self.race,self.empire,self.is_leader,self.kill,self.dead,self.skill_dmg,self.guild_id, self.spy, self.online) = ("",0,0,0,0,0,0,0,0,0,0)
			self.Index=0
			self.isMe=0
			self.pid=0

		def __init__(self, pid, isMe):
			ui.Window.__init__(self)
			self.children = {}
			self.Index= 0
			self.pid = int(pid)
			self.isMe=isMe
			self.spyDialog = None
			(self.name,self.level,self.race,self.empire,self.is_leader,self.kill,self.dead,self.skill_dmg,self.guild_id, self.spy, self.online) = guild.StaticsPIDToData(self.pid, self.isMe)
			self.InitItem()


		def InitItem(self):
			global MY_GUILD_ID

			if self.isMe and self.is_leader:
				MY_GUILD_ID = self.guild_id

			playerRank = ui.TextLine()
			playerRank.SetParent(self)
			playerRank.SetPosition(15, 3)
			playerRank.SetHorizontalAlignCenter()
			playerRank.AddFlag("not_pick")
			playerRank.SetText("%d" % self.Index)
			playerRank.Show()
			self.children["playerRank"] = playerRank

			playerStatus = ui.ImageBox()
			playerStatus.SetParent(self)
			playerStatus.SetPosition(30, 3)
			playerStatus.AddFlag("not_pick")
			if self.online:
				playerStatus.LoadImage("d:/ymir work/ui/game/guild_war/online.tga")
			else:
				playerStatus.LoadImage("d:/ymir work/ui/game/guild_war/offline.tga")
			playerStatus.SetAlpha(0.7)
			playerStatus.Show()
			self.children["playerStatus"] = playerStatus

			playerRace = ui.ImageBox()
			playerRace.SetParent(self)
			playerRace.SetPosition(30+12+3, 3)
			playerRace.AddFlag("not_pick")
			playerRace.LoadImage("d:/ymir work/ui/game/ronark/race_"+str(constInfo.raceToJob(self.race))+".tga")
			playerRace.SetAlpha(0.7)
			playerRace.Show()
			self.children["playerRace"] = playerRace

			playerText = ui.TextLine()
			playerText.SetParent(self)
			playerText.SetPosition(30+12+3+16+5, 4)
			playerText.AddFlag("not_pick")
			playerText.SetText("%s[%d]" % (self.name,self.level))
			playerText.SetHorizontalAlignLeft()
			playerText.Show()
			self.children["playerText"] = playerText

			if self.is_leader:
				playerLeader = ui.ImageBox()
				playerLeader.SetParent(self)
				playerLeader.AddFlag("not_pick")
				playerLeader.SetPosition(30+12+3+16+5+playerText.GetTextSize()[0]+5, 4)
				playerLeader.LoadImage("d:/ymir work/ui/game/guild_war/king_icon.tga")
				playerLeader.SetAlpha(0.7)
				playerLeader.Show()
				self.children["playerLeader"] = playerLeader
			else:
				if MY_GUILD_ID == self.guild_id and self.spy == False:
					playerSpy = ui.Button()
					playerSpy.SetParent(self)
					playerSpy.SetPosition(30+12+3+16+5+playerText.GetTextSize()[0]+5, 4)
					playerSpy.SetUpVisual("d:/ymir work/ui/game/guild_war/remove_btn_0.tga")
					playerSpy.SetOverVisual("d:/ymir work/ui/game/guild_war/remove_btn_1.tga")
					playerSpy.SetDownVisual("d:/ymir work/ui/game/guild_war/remove_btn_2.tga")
					playerSpy.SAFE_SetEvent(self.__ClickOutSpy)
					playerSpy.SetAlpha(0.5)
					playerSpy.Show()
					self.children["playerSpy"] = playerSpy

			playerKill = ui.TextLine()
			playerKill.SetParent(self)
			playerKill.AddFlag("not_pick")
			playerKill.SetPosition(180, 4)
			playerKill.SetHorizontalAlignCenter()
			playerKill.SetText("%s" % localeInfo.NumberToMoneyStringNEW(self.kill))
			playerKill.Show()
			self.children["playerKill"] = playerKill

			playerDead = ui.TextLine()
			playerDead.SetParent(self)
			playerDead.AddFlag("not_pick")
			playerDead.SetPosition(220, 4)
			playerDead.SetHorizontalAlignCenter()
			playerDead.SetText("%s" % localeInfo.NumberToMoneyStringNEW(self.dead))
			playerDead.Show()
			self.children["playerDead"] = playerDead

			playerDmg = ui.TextLine()
			playerDmg.SetParent(self)
			playerDmg.AddFlag("not_pick")
			playerDmg.SetPosition(270, 4)
			playerDmg.SetHorizontalAlignCenter()
			playerDmg.SetText("%s"%localeInfo.NumberToMoneyStringNEW(self.skill_dmg))
			playerDmg.Show()
			self.children["playerDmg"] = playerDmg

			playerGuild = ui.TextLine()
			playerGuild.SetParent(self)
			playerGuild.AddFlag("not_pick")
			playerGuild.SetPosition(360, 4)
			playerGuild.SetHorizontalAlignCenter()
			playerGuild.SetText("%s" % guild.GetGuildName(self.guild_id))
			playerGuild.Show()
			self.children["playerGuild"] = playerGuild

			global MAIN_VID
			if not self.isMe and self.spy == False and self.name != MAIN_VID and player.IsObserverMode():
				playerCamera = ui.Button()
				playerCamera.SetParent(self)
				playerCamera.SetPosition(415, 4)
				playerCamera.SetUpVisual("d:/ymir work/ui/game/mailbox/post_block_button_default.sub")
				playerCamera.SetOverVisual("d:/ymir work/ui/game/mailbox/post_write_confirm_over.sub")
				playerCamera.SetDownVisual("d:/ymir work/ui/game/mailbox/post_write_confirm_down.sub")
				playerCamera.SetAlpha(0.5)
				playerCamera.SAFE_SetEvent(self.__ClickCamera)
				self.children["playerCamera"] = playerCamera
			self.SetOnlineStatus()
			self.ChangeColor()

		def ChangeColor(self):
			color = 0
			if self.spy:
				color = 0xffff0000
			elif self.isMe:
				color = 0xffffcc00
			elif self.Index == 1:
				color = 0xffffcc00
			elif self.Index == 2:
				color = 0xffB0C4DE
			elif self.Index == 3:
				color = 0xff8B4513

			if color != 0:
				self.children["playerRank"].SetPackedFontColor(color)
				self.children["playerText"].SetPackedFontColor(color)
				self.children["playerKill"].SetPackedFontColor(color)
				self.children["playerDead"].SetPackedFontColor(color)
				self.children["playerDmg"].SetPackedFontColor(color)
				self.children["playerGuild"].SetPackedFontColor(color)

		def SetOnlineStatus(self):
			if self.online:
				self.children["playerStatus"].LoadImage("d:/ymir work/ui/game/guild_war/online.tga")
				if self.children.has_key("playerCamera"):
					self.children["playerCamera"].Show()
			else:
				self.children["playerStatus"].LoadImage("d:/ymir work/ui/game/guild_war/offline.tga")
				if self.children.has_key("playerCamera"):
					self.children["playerCamera"].Hide()

		def __ClickOutSpy(self):
			if self.spyDialog == None:
				self.spyDialog = uiCommon.QuestionDialog()
			self.spyDialog.SetText(localeInfo.GUILDWAR_STATIC_SPY_ASK%self.name)
			self.spyDialog.SetAcceptText(localeInfo.UI_ACCEPT)
			self.spyDialog.SetCancelText(localeInfo.UI_DENY)
			self.spyDialog.SetAcceptEvent(lambda arg=1: self.__AnswerSpyPlayer(arg))
			self.spyDialog.SetCancelEvent(lambda arg=0: self.__AnswerSpyPlayer(arg))
			self.spyDialog.Open()

		def __ClickCamera(self):
			interface = constInfo.GetInterfaceInstance()
			if interface != None:
				if interface.wndGuildWar:
					interface.wndGuildWar.SetCameraMode(self.name)

		def __AnswerSpyPlayer(self, status):
			if status:
				net.SendChatPacket("/guild_war_static spy %s %d"%(self.name,self.pid))
			self.spyDialog.Close()

		def Update(self, index):
			(self.name,self.level,self.race,self.empire,self.is_leader,self.kill,self.dead,self.skill_dmg,self.guild_id,self.spy, self.online) = guild.StaticsPIDToData(self.pid, self.isMe)
			if index == 1:
				self.children["playerKill"].SetText("%s" %localeInfo.NumberToMoneyStringNEW(self.kill))
				self.children["playerDead"].SetText("%s" %localeInfo.NumberToMoneyStringNEW(self.dead))
			elif index == 2:
				self.children["playerDmg"].SetText("%s" %localeInfo.NumberToMoneyStringNEW(self.skill_dmg))
			elif index == 4:
				self.ChangeColor()
				if self.children.has_key("playerSpy"):
					self.children["playerSpy"].Hide()
			elif index == 5:
				self.SetOnlineStatus()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.loadingImageRotation=0
		self.lastItem = None
		self.rankListBoxEx = None
		self.loadingImage = None
		self.staticListLoaded = False
		self.start = 1
		self.end = 1
		self.observerCount=0

		self.perPage = 10
		self.currentPage = 1
		self.pageCount = 1
		self.isStillCantHide=True

		self.firstGuildText = None
		self.secondGuildText = None
		self.warInfo = None

		self.firstID =-1
		self.secondID =-1

		self.Initializition()
	
	def Destroy(self):
		self.Clear()
		self.loadingImageRotation=0
		self.loadingImage = None
		self.staticListLoaded = False
		self.start = 0
		self.observerCount=0
		self.end = 0
		self.perPage = 0
		self.currentPage = 0
		self.pageCount = 0
		self.isStillCantHide=0
		self.firstGuildText = None
		self.secondGuildText = None
		self.warInfo = None

		self.firstID =0
		self.secondID =0

	def Initializition(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/guildwar_static.py")
			self.rankListBoxEx = self.GetChild("ListBoxNEW")
			self.GetChild("next_btn").SAFE_SetEvent(self.NextPage)
			self.GetChild("back_btn").SAFE_SetEvent(self.PrevPage)
		except:
			import exception
			exception.Abort("EventInfo.LoadDialog.LoadScript")

		self.rankListBoxEx.SetViewItemCount(10)
		self.rankListBoxEx.SetItemStep(26)
		self.rankListBoxEx.SetItemSize(550,26)

		self.loadingImage = ui.ExpandedImageBox()
		self.loadingImage.SetParent(self.rankListBoxEx)
		self.loadingImage.AddFlag("not_pick")
		self.loadingImage.LoadImage("d:/ymir work/ui/load_.tga")
		self.loadingImage.SetPosition(self.rankListBoxEx.GetWidth()/2-70,self.rankListBoxEx.GetHeight()/2)
		self.loadingImage.Show()

		self.firstGuildText = ui.MultiTextLine()
		self.firstGuildText.SetParent(self.GetChild("RightThinboard"))
		self.firstGuildText.SetTextType("horizontal#center")
		self.firstGuildText.SetTextRange(20)
		self.firstGuildText.SetPosition(93,55)
		self.firstGuildText.Show()

		self.secondGuildText = ui.MultiTextLine()
		self.secondGuildText.SetParent(self.GetChild("RightThinboard"))
		self.secondGuildText.SetTextType("horizontal#center")
		self.secondGuildText.SetTextRange(20)
		self.secondGuildText.SetPosition(380,55)
		self.secondGuildText.Show()
		
		self.warInfo = ui.MultiTextLine()
		self.warInfo.SetParent(self.GetChild("RightThinboard"))
		self.warInfo.SetTextType("horizontal#center")
		self.warInfo.SetTextRange(20)
		self.warInfo.SetPosition(240,110)
		self.warInfo.Show()

	def OnPressEscapeKey(self):
		self.Hide()
		return True

	def Open(self):
		self.isStillCantHide = True
		if self.staticListLoaded == False:
			self.SetCenterPosition()
			self.SetTop()
			self.loadingImage.Show()
			net.SendChatPacket("/guild_war_static load")
		#self.SetStaticsStatus()
		#self.Update()
		self.Show()

	def Clear(self):
		if self.lastItem:
			self.lastItem.Hide()
			self.lastItem.Destroy()
			self.lastItem=None
		if self.rankListBoxEx:
			self.rankListBoxEx.RemoveAllItems()

	def SetStaticsStatus(self):
		self.staticListLoaded = True
		self.loadingImage.Hide()

	def SetCameraMode(self, name):
		global CURRENT_VID
		global MAIN_VID

		if CURRENT_VID == name:
			self.ExitCameraMode()
			return

		data = self.rankListBoxEx.itemList
		newRank = None
		for rank in data:
			if rank.name == CURRENT_VID:
				if rank.children.has_key("playerCamera"):
					rank.children["playerCamera"].SetUpVisual("d:/ymir work/ui/game/mailbox/post_block_button_default.sub")
					rank.children["playerCamera"].SetOverVisual("d:/ymir work/ui/game/mailbox/post_write_confirm_over.sub")
					rank.children["playerCamera"].SetDownVisual("d:/ymir work/ui/game/mailbox/post_write_confirm_down.sub")
			elif rank.name == name:
				newRank = rank

		if newRank != None:
			if newRank.online == False:
				self.ExitCameraMode()
				return
			
			if newRank.children.has_key("playerCamera"):
				if chr.SetMainInstance(name,MAIN_VID, True):
					CURRENT_VID = name

					newRank.children["playerCamera"].SetUpVisual("d:/ymir work/ui/game/mailbox/post_write_confirm_down.sub")
					newRank.children["playerCamera"].SetOverVisual("d:/ymir work/ui/game/mailbox/post_write_confirm_over.sub")
					newRank.children["playerCamera"].SetDownVisual("d:/ymir work/ui/game/mailbox/post_block_button_default.sub")

					interface = constInfo.GetInterfaceInstance()
					if interface != None:
						if interface.wndGameButton:
							interface.wndGameButton.UpdateCameraMode()
				#player.SetCameraMode(True)
		else:
			self.ExitCameraMode()

	def ExitCameraMode(self):
		global MAIN_VID
		global CURRENT_VID
		if MAIN_VID != "":

			data = self.rankListBoxEx.itemList
			for rank in data:
				if rank.name == CURRENT_VID:
					if rank.children.has_key("playerCamera"):
						rank.children["playerCamera"].SetUpVisual("d:/ymir work/ui/game/mailbox/post_block_button_default.sub")
						rank.children["playerCamera"].SetOverVisual("d:/ymir work/ui/game/mailbox/post_write_confirm_over.sub")
						rank.children["playerCamera"].SetDownVisual("d:/ymir work/ui/game/mailbox/post_write_confirm_down.sub")

			CURRENT_VID = ""
			chr.SetMainInstance(MAIN_VID,MAIN_VID, False)

		interface = constInfo.GetInterfaceInstance()
		if interface != None:
			if interface.wndGameButton:
				interface.wndGameButton.UpdateCameraMode()

	def CreateSelfLastItem(self):
		global MY_GUILD_ID
		MY_GUILD_ID = -1
		PID = guild.StaticsNameToPID(player.GetName())
		if PID != -1:
			if self.lastItem == None:
				self.lastItem = self.rankListBoxItem(PID, True)
				self.lastItem.SetParent(self.rankListBoxEx)
				self.lastItem.SetPosition(0,26*10)
				self.lastItem.Show()

	def SortAfterCheck(self, listbox):
		data = self.rankListBoxEx.itemList
		lastIndex=-1
		for rank in data:
			index = data.index(rank)
			if rank.name == player.GetName():
				lastIndex = index+1
			rank.children["playerRank"].Index = index+1
			rank.children["playerRank"].SetText("%d"%(index+1))
			rank.ChangeColor()

		if self.lastItem:
			if lastIndex != -1:
				self.lastItem.children["playerRank"].SetText("%d"%lastIndex)
				self.lastItem.Index = lastIndex

	def GuildWarStaticsSpecial(self, pid, sub_index):
		if self.staticListLoaded == False:
			return
		pid = int(pid)
		isAlreadyHave = False

		global CURRENT_VID
		for rank in self.rankListBoxEx.itemList:
			if rank.pid == pid:
				rank.Update(sub_index)
				isAlreadyHave=True
			
			if rank.name == CURRENT_VID and rank.online == False:
				self.ExitCameraMode()

		if self.lastItem:
			if self.lastItem.pid == pid:
				self.lastItem.Update(sub_index)
				isAlreadyHave=True

		if not isAlreadyHave:
			resultItem = self.rankListBoxItem(pid, False)
			self.rankListBoxEx.AppendItem(resultItem)
			self.UpdatePageCount()

		if not sub_index >= 4 and sub_index <= 6:
			self.rankListBoxEx.itemList.sort()
			self.rankListBoxEx.SetBasePos(0)
			self.SortAfterCheck(self.rankListBoxEx)

		self.UpdateMultiText()

	def UpdatePageCount(self):
		self.pageCount = int(math.ceil(float(guild.StaticsSize()) / float(self.perPage)))
		if self.pageCount == 0:
			self.pageCount = 1
		self.GetChild("page_text").SetText("%d/%d"%(self.currentPage,self.pageCount))
		self.start = (self.currentPage - 1) * self.perPage
		self.end = ((self.currentPage - 1) * self.perPage) + self.perPage
		if self.pageCount == 1:
			self.GetChild("next_btn").Hide()
			self.GetChild("back_btn").Hide()
		else:
			self.GetChild("next_btn").Show()
			self.GetChild("back_btn").Show()
		if self.end >= guild.StaticsSize():
			self.end = guild.StaticsSize()

	def Update(self):
		if self.staticListLoaded == False:
			return
		self.UpdatePageCount()
		self.CreateSelfLastItem()
		for j in range(self.start,self.end):
			pid = guild.StaticsIndexToPID(j)
			if pid != -1:
				resultItem = self.rankListBoxItem(pid, False)
				self.rankListBoxEx.AppendItem(resultItem)

		self.rankListBoxEx.itemList.sort()
		self.rankListBoxEx.SetBasePos(0)
		self.SortAfterCheck(self.rankListBoxEx)

		self.UpdateMultiText()

	def OnUpdate(self):
		if self.loadingImage:
			if self.loadingImage.IsShow():
				self.loadingImage.SetRotation(self.loadingImageRotation)
				self.loadingImageRotation+=10

		if not app.IsPressed(app.DIK_TAB) and self.isStillCantHide:
			self.isStillCantHide=False
			self.Hide()

	def NextPage(self):
		if self.currentPage < self.pageCount:
			self.currentPage += 1
			self.Clear()
			self.Update()

	def PrevPage(self):
		if self.currentPage > 1:
			self.currentPage -= 1
			self.Clear()
			self.Update()

	def GetGuildLeaderName(self, check_guild_id):
		leaderName = "-"
		onlineCount = 0
		offlineCount = 0
		spyCount = 0
		totalKill = 0
		totalDead = 0
		totalDmg = 0
		guildEmpire = 0
		#raceList = [0,0,0,0,0] # wolfman
		raceList = [0,0,0,0]
		for j in xrange(guild.StaticsSize()):
			(name,level,race,empire,is_leader,kill,dead,skill_dmg,guild_id, spy, online) = guild.StaticsPIDToData(guild.StaticsIndexToPID(j), False)
			if guild_id == check_guild_id:
				if is_leader:
					leaderName = name

				if online:
					onlineCount+=1
					raceList[constInfo.raceToJob(race)]+=1
				else:
					offlineCount+=1

				if spy:
					spyCount+=1

				totalKill+=kill
				totalDead+=dead
				totalDmg+=skill_dmg
				guildEmpire = empire
		return (leaderName, onlineCount, offlineCount, spyCount, totalKill, totalDead, totalDmg, guildEmpire, raceList)

	if app.__IMPROVED_GUILD_WAR__:
		def SetGuildID(self, firstID, secondID, iMaxPlayer, iMaxScore, flags):
			(self.firstID,self.secondID) =(firstID,secondID)

			text = ""
			if not constInfo.IS_SET(flags, 1<<1):
				self.GetChild("observer").Hide()
				self.warInfo.SetPosition(240,90)
				text+= localeInfo.GULDWAR_STATIC_CANT_OBSERVER
				text+="\n"

			text+= localeInfo.GULDWAR_STATIC_MAXPLAYER % iMaxPlayer
			text+="\n"
			text+= localeInfo.GULDWAR_STATIC_MAXSCORE % iMaxScore
			self.warInfo.SetText(text)
	else:
		def SetGuildID(self, firstID, secondID):
			(self.firstID,self.secondID) =(firstID,secondID)
			self.warInfo.SetText("")

	def SetUser(self, id0, user0, id1, user1, observer):
		self.GetChild("mark_0").SetIndex(id0)
		self.GetChild("guild_0_name").SetText("%s(%d)"%(guild.GetGuildName(id0),user0))
		
		self.GetChild("mark_1").SetIndex(id1)
		self.GetChild("guild_1_name").SetText("%s(%d)"%(guild.GetGuildName(id1),user1))
		self.GetChild("observer").SetText(localeInfo.RONARK_OBSERVER%observer)

	def SetScore(self, id0, id1, score):
		if self.firstID == id0:
			self.GetChild("guild_0_score").SetText(str(score))
		elif self.secondID == id0:
			self.GetChild("guild_1_score").SetText(str(score))

		score1 = int(self.GetChild("guild_0_score").GetText())
		score2 = int(self.GetChild("guild_1_score").GetText())
		lastScore = 0
		if score1 > score2:
			lastScore = score1-score2
			self.GetChild("guild_0_score").SetPackedFontColor(0xff50b409)
			self.GetChild("guild_1_score").SetPackedFontColor(0xffea150a)
		elif score2 > score1:
			lastScore = score2-score1
			self.GetChild("guild_0_score").SetPackedFontColor(0xffea150a)
			self.GetChild("guild_1_score").SetPackedFontColor(0xff50b409)

		self.GetChild("against").SetText(localeInfo.GULDWAR_STATIC_AGAINST %lastScore)

	def UpdateObserverCount(self, observer):
		self.observerCount = int(observer)
		self.UpdateMultiText()
	
	def UpdateMultiText(self):
		guild_id  = [[self.firstID,self.firstGuildText],[self.secondID,self.secondGuildText]]
		data = []

		for guild in guild_id:
			guild[1].SetText("")
			if guild[0] == -1:
				continue
			item = []
			multi_text = ""

			(leaderName, onlineCount, offlineCount, spyCount, totalKill, totalDead, totalDmg, guildEmpire, raceList)  = self.GetGuildLeaderName(guild[0])
			if leaderName != "-":
				#multi_text += "|Eempire_%d|e"%guildEmpire
				#multi_text += "|Eking|e "+str(leaderName)+"\n"
				#multi_text += "|Eonline|eOnline: %d\t"%onlineCount
				#multi_text += "|Eoffline|eOffline: %d\t"%offlineCount
				#multi_text += "Spy: %d\n"%spyCount
				multi_text += localeInfo.GUILDWAR_STATIC_TOTAL_INFO+"\n"
				#multi_text += "Kill: %s\t"%(localeInfo.NumberToMoneyStringNEW(totalKill))
				multi_text += "%s: %s\t"%(localeInfo.GUILDWAR_STATIC_DEAD,(localeInfo.NumberToMoneyStringNEW(totalDead)))
				multi_text += "%s: %s\n"%(localeInfo.GUILDWAR_STATIC_DMG,(localeInfo.NumberToMoneyStringNEW(totalDmg)))

				item.append(guild[0])
				item.append(totalKill)
				item.append(onlineCount)
				data.append(item)

				c = 0
				for raceCount in raceList:
					multi_text += "|Erace_%d|e: %d\t"%(c,raceCount)
					c+=1
			#else:
			#	multi_text = "-"

			if multi_text != "":
				guild[1].SetText(multi_text)

		if len(data) > 1:
			interface = constInfo.GetInterfaceInstance()
			if interface != None:

				# Score
				interface.OnRecvGuildWarPoint(data[0][0],data[1][0],data[0][1])
				interface.OnRecvGuildWarPoint(data[1][0],data[0][0],data[1][1])
				self.SetScore(data[0][0],data[1][0],data[0][1])
				self.SetScore(data[1][0],data[0][0],data[1][1])

				# Member
				interface.UpdateMemberCount(data[0][0],data[0][2],data[1][0],data[1][2])
				self.SetUser(data[0][0],data[0][2],data[1][0],data[1][2],self.observerCount)
				interface.wndMiniMap.UpdateObserverCount(self.observerCount)


DROP_MESSAGE_TIME = 4
DROP_MAX_STACK = 13

class CSMessageObject(ui.Bar):
	def __init__(self, data):
		ui.Bar.__init__(self)
		self.children = []
		self.endTime = time.clock() + DROP_MESSAGE_TIME
		self.SetSize(250, 25)
		self.SetColor(0x77000000)
		#self.Initialize(data)

	def __del__(self):
		ui.Bar.__del__(self)

	def Destroy(self):
		self.children = []
		self.endTime = 0

	# def Initialize(self, data):
		# killerName = ui.TextLine()
		# killerName.SetParent(self)
		# killerName.SetPosition(25, 3)

		# text = "|Erace_%d|e\t%s"%(constInfo.raceToJob(data[1]),data[0])
		# killerName.SetText(text)
		# killerName.SetOutline()
		# killerName.SetFeather(False)
		# killerName.SetPackedFontColor(0xff00e5ee)
		# killerName.Show()
		# self.children.append(killerName)

		#killerRace = ui.ExpandedImageBox()
		#killerRace.SetParent(self)		
		#try:
		#	killerRace.LoadImage(FACE_IMAGE_DICT[int(data[1])])
		#except:
		#	killerRace.Hide()
		#killerRace.SetPosition(0, 5)
		#killerRace.SetScale(0.3, 0.3)
		#killerRace.Show()
		#self.children.append(killerRace)

		# victimName = ui.TextLine()
		# victimName.SetParent(self)
		# victimName.SetPosition(155, 3)
		# text = "|Erace_%d|e\t%s"%(constInfo.raceToJob(data[3]),data[2])
		# victimName.SetText(text)
		# victimName.SetOutline()
		# victimName.SetFeather(False)
		# victimName.SetPackedFontColor(0xffff0000)
		# victimName.Show()
		# self.children.append(victimName)

		#victimRace = ui.ExpandedImageBox()
		#victimRace.SetParent(self)		
		#try:
		#	victimRace.LoadImage(FACE_IMAGE_DICT[int(data[3])])
		#except:
		#	victimRace.Hide()
		#victimRace.SetPosition(135, 5)
		#victimRace.SetScale(0.3, 0.3)
		#victimRace.Show()
		#self.children.append(victimRace)

	def isTimeout(self):
		lastTime = max(0, self.endTime - time.clock())
		if 0 == lastTime:
			return True
		return False

class MessageQueue(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)
		self.stack = []
		self.lastClock = 0
		self.timeDiff = 0.5
		self.nextY = 0
		self.__Reset()

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.stack = []

		self.lastClock = 0
		self.timeDiff = 0.5
		self.nextY = 0

	def OnMessage(self, killerName, killerRace, victimName, victimRace):
		data = [killerName, killerRace, victimName, victimRace]
		#message = CSMessageObject(data)
		message.SetParent(self)
		message.Hide()

		count = len(self.stack)

		if count == DROP_MAX_STACK:
			self.stack.remove(self.stack[0])

		self.stack.append(message)
		self.__Render()

	def __Reset(self):
		self.SetPosition(systemSetting.GetWidth()- 250, -200)
		self.Show()

	def __Render(self):
		for it in self.stack:
			if it.isTimeout():
				it.Destroy()
				self.stack.remove(it)
		stack = list(self.stack)
		stack.reverse()
		self.nextY = 408
		for it in stack:
			it.SetPosition(0, self.nextY)
			if not it.IsShow():
				it.Show()
			self.nextY += 27

	def OnUpdate(self):
		if len(self.stack) > 0:
			if (app.GetTime() - self.lastClock) >= self.timeDiff:
				self.lastClock = app.GetTime()
				self.__Render()


class GuildWarStaticLog(ui.BoardWithTitleBar):

	class GuildWarListItem(ui.ThinBoardCircle):
		def __del__(self):
			ui.ThinBoardCircle.__del__(self)
		def Destroy(self):
			self.ResetData()
		def SetParent(self, parent):
			ui.ThinBoardCircle.SetParent(self, parent)
			self.parent=proxy(parent)
		def OnMouseLeftButtonDown(self):
			if self.parent.selItem == self:
				self.parent.SelectItem(None)
				return
			self.parent.SelectItem(self)
		def OnSelectedRender(self):
			self.OnMouseOverIn()
			self.isSelected=True
		def UnSelectedRender(self):
			self.isSelected=False
			self.OnMouseOverOut()
		def OnMouseOverIn(self):
			if self.isSelected == False:
				self.SetColor(self.BOARD_COLOR_IN)
		def OnMouseOverOut(self):
			if self.isSelected == False:
				self.SetColor(self.BOARD_COLOR_OUT)

		def ResetData(self):
			self.warID = 0
			self.parent=None
			self.children = {}
			self.isSelected = False
		def __init__(self, warID):
			ui.ThinBoardCircle.__init__(self)
			self.ResetData()
			self.warID = warID

			self._Load()

		def _Load(self):
			if app.__IMPROVED_GUILD_WAR__:
				(dwID, dwGuildFrom, dwGuildTo, dwTime, bType, iMaxPlayer, iMaxScore, flags, winner, guild1_name, guild2_name, date) = guild.WarStatisticsInfo(self.warID, False)
			else:
				(dwID, dwGuildFrom, dwGuildTo, dwTime, bType, winner, guild1_name, guild2_name, date) = guild.WarStatisticsInfo(self.warID, False)
			if dwID != 0:
				global OWN_GUILD_TEXT_COLOR
				global LOSER_GUILD_TEXT_COLOR
				myGuildID = guild.GetGuildID()

				text = ui.TextLine()
				text.AddFlag("not_pick")
				text.SetParent(self)
				text.SetHorizontalAlignCenter()
				text.SetPosition(115,6)
				text_ptr = ""

				if dwGuildFrom == winner:
					text_ptr+="|Eking|e"

				if myGuildID != dwGuildFrom and myGuildID != dwGuildTo:
					text_ptr+="%s vs %s"%(guild1_name, guild2_name)
				elif myGuildID == dwGuildFrom:
					color = OWN_GUILD_TEXT_COLOR
					if winner != myGuildID and winner != -1:
						color = LOSER_GUILD_TEXT_COLOR
					text_ptr+="|cFF%s%s|h|r vs %s"%(color,guild1_name, guild2_name)
				elif myGuildID == dwGuildTo:
					color = OWN_GUILD_TEXT_COLOR
					if winner != myGuildID and winner != -1:
						color = LOSER_GUILD_TEXT_COLOR
					text_ptr+="%s vs |cFF%s%s|h|r"%(guild1_name, color, guild2_name)

				if dwGuildTo == winner:
					text_ptr+="|Eking|e"

				#text_ptr +=str(dwID)
				text.SetText(text_ptr)
				text.Show()
				self.children["text"]=text

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)
	
	def ResetData(self):
		self.children={}
		self.btnList = []
		self.warIDList = []
		self.btnStep = 0
		self.loadingImageRotation = 0
		self.perPage = 7
		self.currentPage = 1
		self.selectedWarID=-1
		self.pageCount = 1
		self.isLoadInfo = False
		self.isLoadData = False
		self.nextEvent = None
	def Destroy(self):
		self.ResetData()
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.AddFlag("float")
		self.AddFlag("movable")
		self.ResetData()
		self._LoadWindow()

	def _LoadRightStatistics(self):
		statistics = [\
			[localeInfo.GUILD_LOG_STATISTICS,"NAME"],\
			[localeInfo.GUILD_LOG_LEADER,"LEADER"],\
			[localeInfo.GUILD_LOG_TOTAL_PLAYER,"PLAYER"],\
			[localeInfo.GUILD_LOG_TOTAL_KILL,"KILL"],\
			[localeInfo.GUILD_LOG_TOTAL_DEAD,"DEAD"],\
			[localeInfo.GUILD_LOG_TOTAL_DMG,"DAMAGE"],\
			[localeInfo.GUILD_LOG_TOTAL_ONLINE,"ONLINE"],\
			[localeInfo.GUILD_LOG_TOTAL_OFFLINE,"OFFLINE"],\
			[localeInfo.GUILD_LOG_TOTAL_SPY,"SPY"],\
		]

		self.children["warstatisticsWallChildren"] = []
		wall = self.children["warstatisticsWall"]
		for j in xrange(len(statistics)):
			statisticsItem = ui.TextLine()
			statisticsItem.SetParent(wall)
			if j == 0:
				statisticsItem.SetPosition(50,6)
			else:
				statisticsItem.SetPosition(50,9+(20*j))
			statisticsItem.SetHorizontalAlignCenter()
			statisticsItem.SetText(statistics[j][0])
			statisticsItem.Show()
			self.children["warstatisticsWallChildren"].append(statisticsItem)

		for j in xrange(2):
			for i in xrange(len(statistics)):
				statisticsReal = ui.TextLine()
				statisticsReal.SetParent(wall)
				if j == 0:
					if i == 0:
						statisticsReal.SetPosition(140,6)
					else:
						statisticsReal.SetPosition(140,9+(20*i))
				else:
					if i == 0:
						statisticsReal.SetPosition(225,6)
					else:
						statisticsReal.SetPosition(225,9+(20*i))
				statisticsReal.SetHorizontalAlignCenter()
				statisticsReal.Show()
				self.children["GUILD_%d_%s"%(j,statistics[i][1])] = statisticsReal

		statisticsDate = ui.TextLine()
		statisticsDate.SetParent(wall)
		statisticsDate.SetPosition(10,9+(20*len(statistics))+2)
		statisticsDate.SetHorizontalAlignLeft()
		statisticsDate.SetText("-")
		statisticsDate.Show()
		self.children["GUILD_DATE"]=statisticsDate

		realStatistics = ui.Button()
		realStatistics.SetParent(wall)
		realStatistics.SetPosition(150,9+(20*len(statistics)))
		realStatistics.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		realStatistics.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		realStatistics.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		realStatistics.SetText(localeInfo.GUILDWAR_STATIC_SEE)
		realStatistics.SAFE_SetEvent(self.ClickOpenStatistics)
		realStatistics.Show()
		self.children["realStatistics"]=realStatistics


	def _LoadWindow(self):
		self.SetSize(550,310)

		blackWall = ui.ThinBoardCircle()
		blackWall.AddFlag("not_pick")
		blackWall.SetParent(self)
		blackWall.SetPosition(10,33)
		blackWall.SetSize(self.GetWidth()-15-5,self.GetHeight()-20-24)
		blackWall.Show()
		self.children["blackWall"] = blackWall

		btnWall = ui.ThinBoardCircle()
		btnWall.AddFlag("attach")
		btnWall.SetParent(self)
		btnWall.SetPosition(10+5,33+5)
		btnWall.SetSize(self.GetWidth()-15-5-10,30)
		btnWall.Show()
		self.children["btnWall"] = btnWall

		warListWall = ui.ThinBoardCircle()
		warListWall.AddFlag("attach")
		warListWall.SetParent(self)
		warListWall.SetPosition(10+5,33+5+35)
		warListWall.SetSize((self.GetWidth()-15-5-30)/2-15,self.GetHeight()-20-24-55-35)
		warListWall.Show()
		self.children["warListWall"] = warListWall

		warListBox = ui.ListBoxEx()
		warListBox.AddFlag("attach")
		warListBox.SetParent(warListWall)
		warListBox.SetPosition(0,0)
		warListBox.SetSize(warListWall.GetWidth(),warListWall.GetHeight())
		warListBox.SetItemSize(warListWall.GetWidth(),25)
		warListBox.SetItemStep(25)
		warListBox.SetViewItemCount(7)
		warListBox.SetSelectEvent(ui.__mem_func__(self.SelectWar))
		warListBox.SetGuildLogStatistics()
		warListBox.Show()
		self.children["warListBox"] = warListBox

		warListWallLoading = ui.ExpandedImageBox()
		warListWallLoading.AddFlag("not_pick")
		warListWallLoading.SetParent(warListWall)
		warListWallLoading.LoadImage("d:/ymir work/ui/load_.tga")
		warListWallLoading.SetPosition((warListWall.GetWidth()/2)-(warListWallLoading.GetWidth()/2),(warListWall.GetHeight()/2)-(warListWallLoading.GetHeight()/2))
		warListWallLoading.Show()
		self.children["warListWallLoading"] = warListWallLoading

		warstatisticsWall = ui.ThinBoardCircle()
		warstatisticsWall.AddFlag("not_pick")
		warstatisticsWall.SetParent(self)
		warstatisticsWall.SetPosition(((self.GetWidth()-15-5-30)/2-10)+10+5,33+5+35)
		warstatisticsWall.SetSize((self.GetWidth()-15-5-10)/2+10,self.GetHeight()-20-24-55)
		warstatisticsWall.Show()
		self.children["warstatisticsWall"] = warstatisticsWall

		wallShitsThings = []
		wallShits = [\
			[ 1,25+(20*8),100,0, 1],\
			[ 1,25+(20*8),(warstatisticsWall.GetWidth()/2)-1+50,0, 1],\
			[ warstatisticsWall.GetWidth(),1,0,25, 0],\
			[ warstatisticsWall.GetWidth(),1,0,25+(20*1), 0],\
			[ warstatisticsWall.GetWidth(),1,0,25+(20*2), 0],\
			[ warstatisticsWall.GetWidth(),1,0,25+(20*3), 0],\
			[ warstatisticsWall.GetWidth(),1,0,25+(20*4), 0],\
			[ warstatisticsWall.GetWidth(),1,0,25+(20*5), 0],\
			[ warstatisticsWall.GetWidth(),1,0,25+(20*6), 0],\
			[ warstatisticsWall.GetWidth(),1,0,25+(20*7), 0],\
			[ warstatisticsWall.GetWidth(),1,0,25+(20*8), 0],\
		]
		for block in wallShits:
			j = ui.ThinBoardCircle()
			j.AddFlag("not_pick")
			j.SetParent(warstatisticsWall)
			j.SetSize(block[0],block[1])
			j.SetPosition(block[2],block[3])
			j.SetLoopStep = block[4]
			#LINE-AFFECT
			#j.increaseLoop = 0
			#j.increaseLoopStep = 0
			#j.LoopStep = False
			j.Show()
			wallShitsThings.append(j)
		self.children["warstatisticsWallShits"] = wallShitsThings

		warstatisticsWallLoading = ui.ExpandedImageBox()
		warstatisticsWallLoading.AddFlag("not_pick")
		warstatisticsWallLoading.SetParent(warstatisticsWall)
		warstatisticsWallLoading.LoadImage("d:/ymir work/ui/load_.tga")
		warstatisticsWallLoading.SetPosition((warListWall.GetWidth()/2)-(warstatisticsWallLoading.GetWidth()/2)+70,(warListWall.GetHeight()/2)-(warstatisticsWallLoading.GetHeight()/2)-15)
		#warstatisticsWallLoading.Show()
		self.children["staLoad"] = warstatisticsWallLoading

		mainWarsBtn = ui.RadioButton()
		mainWarsBtn.SetParent(btnWall)
		mainWarsBtn.SetPosition(3,5)
		mainWarsBtn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		mainWarsBtn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		mainWarsBtn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		mainWarsBtn.SetText(localeInfo.GUILD_MAIN_WAR)
		mainWarsBtn.SAFE_SetEvent(self.ClickStatisticsButton,0)
		mainWarsBtn.Show()
		self.btnList.append(mainWarsBtn)

		X_LEN = mainWarsBtn.GetWidth()

		winnerWarsBtn = ui.RadioButton()
		winnerWarsBtn.SetParent(btnWall)
		winnerWarsBtn.SetPosition(3+X_LEN+3,5)
		winnerWarsBtn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		winnerWarsBtn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		winnerWarsBtn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		winnerWarsBtn.SetText(localeInfo.GUILD_WINNING_WAR)
		winnerWarsBtn.SAFE_SetEvent(self.ClickStatisticsButton,1)
		winnerWarsBtn.Show()
		self.btnList.append(winnerWarsBtn)

		drawWarsBtn = ui.RadioButton()
		drawWarsBtn.SetParent(btnWall)
		drawWarsBtn.SetPosition(3+X_LEN+3+X_LEN+3,5)
		drawWarsBtn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		drawWarsBtn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		drawWarsBtn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		drawWarsBtn.SetText(localeInfo.GUILD_DRAW_WAR)
		drawWarsBtn.SAFE_SetEvent(self.ClickStatisticsButton,2)
		drawWarsBtn.Show()
		self.btnList.append(drawWarsBtn)

		#global MY_GUILD_ID
		#if MY_GUILD_ID != -1:
		ourWarsBtn = ui.RadioButton()
		ourWarsBtn.SetParent(btnWall)
		ourWarsBtn.SetPosition(3+X_LEN+3+X_LEN+3+X_LEN+3,5)
		ourWarsBtn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		ourWarsBtn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		ourWarsBtn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		ourWarsBtn.SetText(localeInfo.GUILD_MY_WARS)
		ourWarsBtn.SAFE_SetEvent(self.ClickStatisticsButton,3)
		ourWarsBtn.Show()
		self.btnList.append(ourWarsBtn)

		backBtn = ui.Button()
		backBtn.SetParent(self)
		backBtn.SetUpVisual("d:/ymir work/ui/public/small_button_01.sub")
		backBtn.SetOverVisual("d:/ymir work/ui/public/small_button_02.sub")
		backBtn.SetDownVisual("d:/ymir work/ui/public/small_button_03.sub")
		backBtn.SAFE_SetEvent(self.PrevPage)
		backBtn.SetText("<<")
		#backBtn.Show()
		self.children["backBtn"]=backBtn

		x, y = warListWall.GetLocalPosition()
		
		pageBar = ui.SlotBar()
		pageBar.SetParent(self)
		pageBar.SetSize(backBtn.GetWidth(),backBtn.GetHeight())
		pageBar.SetPosition((warListWall.GetWidth()/2)-(pageBar.GetWidth()/2),y+warListWall.GetHeight()+5)
		pageBar.Show()
		self.children["pageBar"]=pageBar

		pageText = ui.TextLine()
		pageText.SetParent(pageBar)
		pageText.SetPosition(22,5)
		pageText.SetText("1/1")
		pageText.SetHorizontalAlignCenter()
		pageText.Show()
		self.children["pageText"]=pageText

		nextBtn = ui.Button()
		nextBtn.SetParent(self)
		nextBtn.SetUpVisual("d:/ymir work/ui/public/small_button_01.sub")
		nextBtn.SetOverVisual("d:/ymir work/ui/public/small_button_02.sub")
		nextBtn.SetDownVisual("d:/ymir work/ui/public/small_button_03.sub")
		nextBtn.SetPosition(((warListWall.GetWidth()/2)-(nextBtn.GetWidth()/2)+(nextBtn.GetWidth()/2))+(pageBar.GetWidth()/2)+5,y+warListWall.GetHeight()+7)
		backBtn.SetPosition(((warListWall.GetWidth()/2)-(backBtn.GetWidth()/2)-(backBtn.GetWidth()/2))-(pageBar.GetWidth()/2)-5,y+warListWall.GetHeight()+7)
		nextBtn.SetText(">>")
		nextBtn.SAFE_SetEvent(self.NextPage)
		#nextBtn.Show()
		self.children["nextBtn"]=nextBtn

		self._LoadRightStatistics()
		self.ClickStatisticsButton(0)

	def NextPage(self):
		if self.currentPage < self.pageCount:
			self.currentPage += 1
		self.RefreshStatistics()

	def PrevPage(self):
		if self.currentPage > 1:
			self.currentPage -= 1
		self.RefreshStatistics()

	def SelectWar(self, button):
		if button == None:
			return
		self.selectedWarID = button.warID
		self.RefrestRightStatistics()

	def RefrestRightStatistics(self):
		self.ClearRightStatistics()
		self.children["staLoad"].Show()
		self.nextEvent = self.LoadButtonRightStatistics
	
		if guild.WarStatisticsDataSize(self.selectedWarID) == 0:
			if uiGuildWarData.LoadData(self.selectedWarID) == False:
				net.SendChatPacket("/guild_war_static data %d"%self.selectedWarID)
				return
	
			if guild.WarStatisticsDataSize(self.selectedWarID) == 0:
				net.SendChatPacket("/guild_war_static data %d"%self.selectedWarID)
				return

		self.LoadButtonRightStatistics()

	def ClickOpenStatistics(self):
		global CURRENT_LOG_WINDOW
		if CURRENT_LOG_WINDOW != None:
			CURRENT_LOG_WINDOW.Hide()
			CURRENT_LOG_WINDOW.Destroy()
			CURRENT_LOG_WINDOW=None

		CURRENT_LOG_WINDOW = GuildWarStaticXLog(self.selectedWarID)
		CURRENT_LOG_WINDOW.SetCenterPosition()
		CURRENT_LOG_WINDOW.SetTop()
		CURRENT_LOG_WINDOW.Open()

	def LoadButtonRightStatistics(self):
		self.ClearRightStatistics()

		if guild.WarStatisticsDataSize(self.selectedWarID) == 0:
			if uiGuildWarData.LoadData(self.selectedWarID) == False:
				self.ClearRightStatistics()
				return

		if app.__IMPROVED_GUILD_WAR__:
			(dwID, dwGuildFrom, dwGuildTo, dwTime, bType, iMaxPlayer, iMaxScore, flags, winner, guild1_name, guild2_name, date) = guild.WarStatisticsInfo(self.selectedWarID, False)
		else:
			(dwID, dwGuildFrom, dwGuildTo, dwTime, bType, winner, guild1_name, guild2_name, date) = guild.WarStatisticsInfo(self.selectedWarID, False)
		guildList = [[dwGuildFrom,guild1_name], [dwGuildTo,guild2_name]]
		for j in xrange(len(guildList)):
			(leaderName, onlineCount, offlineCount, spyCount, totalKill, totalDead, totalDmg, guildEmpire, raceList) = uiGuildWarData.GetWarStatistics(self.selectedWarID, guildList[j][0])
			self.children["GUILD_%d_NAME"%j].SetText(guildList[j][1])
			self.children["GUILD_%d_LEADER"%j].SetText(leaderName)
			self.children["GUILD_%d_PLAYER"%j].SetText(str(onlineCount+offlineCount))
			self.children["GUILD_%d_KILL"%j].SetText(str(totalKill))
			self.children["GUILD_%d_DEAD"%j].SetText(str(totalDead))
			self.children["GUILD_%d_DAMAGE"%j].SetText(str(totalDmg))
			self.children["GUILD_%d_ONLINE"%j].SetText(str(onlineCount))
			self.children["GUILD_%d_OFFLINE"%j].SetText(str(offlineCount))
			self.children["GUILD_%d_SPY"%j].SetText(str(spyCount))

		self.children["GUILD_DATE"].SetText(str(date))
		self.children["realStatistics"].Show()

	def ClearRightStatistics(self):
		self.children["staLoad"].Hide()
		self.nextEvent = None
		statistics = [\
			[localeInfo.GUILD_LOG_STATISTICS,"NAME"],\
			[localeInfo.GUILD_LOG_LEADER,"LEADER"],\
			[localeInfo.GUILD_LOG_TOTAL_PLAYER,"PLAYER"],\
			[localeInfo.GUILD_LOG_TOTAL_KILL,"KILL"],\
			[localeInfo.GUILD_LOG_TOTAL_DEAD,"DEAD"],\
			[localeInfo.GUILD_LOG_TOTAL_DMG,"DAMAGE"],\
			[localeInfo.GUILD_LOG_TOTAL_ONLINE,"ONLINE"],\
			[localeInfo.GUILD_LOG_TOTAL_OFFLINE,"OFFLINE"],\
			[localeInfo.GUILD_LOG_TOTAL_SPY,"SPY"],\
		]
		for j in xrange(2):
			for i in xrange(len(statistics)):
				self.children["GUILD_%d_%s"%(j,statistics[i][1])].SetText("-")
		self.children["GUILD_DATE"].SetText("-")
		self.children["realStatistics"].Hide()

	def RunEvent(self):
		if self.nextEvent != None:
			self.nextEvent()

	def LoadButtonIndexInfo(self):
		self.nextEvent = None
		self.children["warListWallLoading"].Hide()
		warIDList = []

		myGuildID = guild.GetGuildID()

		for j in xrange(guild.WarStatisticsInfoSize()):
			if app.__IMPROVED_GUILD_WAR__:
				(dwID, dwGuildFrom, dwGuildTo, dwTime, bType, iMaxPlayer, iMaxScore, flags, winner, guild1_name, guild2_name, date) = guild.WarStatisticsInfo(j, True)
			else:
				(dwID, dwGuildFrom, dwGuildTo, dwTime, bType, winner, guild1_name, guild2_name, date) = guild.WarStatisticsInfo(j, True)
			if self.btnStep == 0:
				warIDList.append(dwID)
			elif self.btnStep == 1:
				if winner > 0:
					warIDList.append(dwID)
			elif self.btnStep == 2:
				if winner <= 0:
					warIDList.append(dwID)
			elif self.btnStep == 3:
				if dwGuildFrom == myGuildID or dwGuildTo == myGuildID:
					warIDList.append(dwID)

		warIDList.reverse()

		self.pageCount = int(math.ceil(float(len(warIDList)) / float(self.perPage)))

		if self.pageCount > 1 and self.currentPage < self.pageCount:
			self.children["nextBtn"].Show()
		else:
			self.children["nextBtn"].Hide()

		if self.currentPage == 1:
			self.children["backBtn"].Hide()
		else:
			self.children["backBtn"].Show()

		self.children["pageText"].SetText("%d/%d"%(self.currentPage,self.pageCount))
		start = (self.currentPage - 1) * self.perPage
		end = ((self.currentPage - 1) * self.perPage) + self.perPage
		currentPageDict = warIDList[start:end]
		for war in currentPageDict:
			warItem = self.GuildWarListItem(int(war))
			warItem.Show()
			self.children["warListBox"].AppendItem(warItem)

	def Open(self):
		self.RefreshStatistics()
		self.Show()
		self.SetTop()
		
	def RefreshStatistics(self):
		self.selectedWarID = -1
		self.ClearRightStatistics()
		self.children["warListBox"].RemoveAllItems()
		self.nextEvent = self.LoadButtonIndexInfo
		self.children["warListWallLoading"].Show()

		#if guild.WarStatisticsInfoSize() == 0:
		net.SendChatPacket("/guild_war_static info")
		#	return

		#self.LoadButtonIndexInfo()

	def ClickStatisticsButton(self, index):
		self.btnStep = index
		self.__ClickRadioButton(self.btnList,self.btnStep)
		self.currentPage=1
		self.RefreshStatistics()

	def OnUpdate(self):
		self.loadingImageRotation+=10
		if self.children.has_key("staLoad"):
			if self.children["staLoad"].IsShow():
				self.children["staLoad"].SetRotation(self.loadingImageRotation)
		if self.children.has_key("warListWallLoading"):
			if self.children["warListWallLoading"].IsShow():
				self.children["warListWallLoading"].SetRotation(self.loadingImageRotation)

	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			warButton=buttonList[buttonIndex]
		except IndexError:
			return
		for eachButton in buttonList:
			eachButton.SetUp()
		warButton.Down()

	def OnPressEscapeKey(self):
		self.Hide()
		return True


class GuildWarStaticXLog(ui.ScriptWindow):

	class rankListBoxItem(ui.Window):
		def __lt__(self, other):
			return (self.kill >= other.kill and self.dead <= other.dead and self.skill_dmg >= other.skill_dmg and self.online >= other.online and self.spy <= other.spy)
		def __del__(self):
			ui.Window.__del__(self)
		def Destroy(self):
			self.children = {}
			(self.name,self.level,self.race,self.empire,self.is_leader,self.kill,self.dead,self.skill_dmg,self.guild_id, self.spy, self.online, self.pid) = ("",0,0,0,0,0,0,0,0,0,0,0)
			self.Index=0
			self.pid=0

		def __init__(self, warID, index):
			ui.Window.__init__(self)
			self.children = {}
			self.Index=0
			self.warID = int(warID)
			self.loopIndex = int(index)
			(self.name,self.level,self.race,self.empire,self.is_leader,self.kill,self.dead,self.skill_dmg,self.guild_id, self.spy, self.online, self.pid) = guild.WarStatisticsData(self.warID, self.loopIndex)
			self.InitItem()

		def InitItem(self):
			playerRank = ui.TextLine()
			playerRank.SetParent(self)
			playerRank.SetPosition(15, 3)
			playerRank.SetHorizontalAlignCenter()
			playerRank.AddFlag("not_pick")
			playerRank.SetText("%d" % self.Index)
			playerRank.Show()
			self.children["playerRank"] = playerRank

			playerRace = ui.ImageBox()
			playerRace.SetParent(self)
			playerRace.SetPosition(30+12+3-16, 4)
			playerRace.AddFlag("not_pick")
			playerRace.LoadImage("d:/ymir work/ui/game/ronark/race_"+str(constInfo.raceToJob(self.race))+".tga")
			playerRace.SetAlpha(0.7)
			playerRace.Show()
			self.children["playerRace"] = playerRace

			playerText = ui.TextLine()
			playerText.SetParent(self)
			playerText.SetPosition(30+12+3+5, 4)
			playerText.AddFlag("not_pick")
			playerText.SetText("%s[%d]" % (self.name,self.level))
			playerText.SetHorizontalAlignLeft()
			playerText.Show()
			self.children["playerText"] = playerText

			if self.is_leader:
				playerLeader = ui.ImageBox()
				playerLeader.SetParent(self)
				playerLeader.AddFlag("not_pick")
				playerLeader.SetPosition(30+12+3+5+playerText.GetTextSize()[0]+5, 4)
				playerLeader.LoadImage("d:/ymir work/ui/game/guild_war/king_icon.tga")
				playerLeader.SetAlpha(0.7)
				playerLeader.Show()
				self.children["playerLeader"] = playerLeader

			playerKill = ui.TextLine()
			playerKill.SetParent(self)
			playerKill.AddFlag("not_pick")
			playerKill.SetPosition(180, 4)
			playerKill.SetHorizontalAlignCenter()
			playerKill.SetText("%s" % localeInfo.NumberToMoneyStringNEW(self.kill))
			playerKill.Show()
			self.children["playerKill"] = playerKill

			playerDead = ui.TextLine()
			playerDead.SetParent(self)
			playerDead.AddFlag("not_pick")
			playerDead.SetPosition(220, 4)
			playerDead.SetHorizontalAlignCenter()
			playerDead.SetText("%s" % localeInfo.NumberToMoneyStringNEW(self.dead))
			playerDead.Show()
			self.children["playerDead"] = playerDead

			playerDmg = ui.TextLine()
			playerDmg.SetParent(self)
			playerDmg.AddFlag("not_pick")
			playerDmg.SetPosition(270, 4)
			playerDmg.SetHorizontalAlignCenter()
			playerDmg.SetText("%s"%localeInfo.NumberToMoneyStringNEW(self.skill_dmg))
			playerDmg.Show()
			self.children["playerDmg"] = playerDmg

			if app.__IMPROVED_GUILD_WAR__:
				(dwID, dwGuildFrom, dwGuildTo, dwTime, bType, iMaxPlayer, iMaxScore, flags, winner, guild1_name, guild2_name, date) = guild.WarStatisticsInfo(self.warID, False)
			else:
				(dwID, dwGuildFrom, dwGuildTo, dwTime, bType, winner, guild1_name, guild2_name, date) = guild.WarStatisticsInfo(self.warID, False)

			playerGuild = ui.TextLine()
			playerGuild.SetParent(self)
			playerGuild.AddFlag("not_pick")
			playerGuild.SetPosition(360, 4)
			playerGuild.SetHorizontalAlignCenter()
			if self.guild_id == dwGuildFrom:
				playerGuild.SetText(guild1_name)
			elif self.guild_id == dwGuildTo:
				playerGuild.SetText(guild2_name)
			else:
				playerGuild.SetText("Noname")
			playerGuild.Show()
			self.children["playerGuild"] = playerGuild

			self.ChangeColor()

		def ChangeColor(self):
			color = 0
			if self.spy:
				color = 0xffff0000
			elif self.Index == 1:
				color = 0xffffcc00
			elif self.Index == 2:
				color = 0xffB0C4DE
			elif self.Index == 3:
				color = 0xff8B4513

			if color != 0:
				self.children["playerRank"].SetPackedFontColor(color)
				self.children["playerText"].SetPackedFontColor(color)
				self.children["playerKill"].SetPackedFontColor(color)
				self.children["playerDead"].SetPackedFontColor(color)
				self.children["playerDmg"].SetPackedFontColor(color)
				self.children["playerGuild"].SetPackedFontColor(color)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __init__(self, warID):
		ui.ScriptWindow.__init__(self)

		self.rankListBoxEx = None
		self.start = 1
		self.end = 1
		self.observerCount=0

		self.perPage = 8
		self.currentPage = 1
		self.pageCount = 1
		self.isStillCantHide=True

		self.firstGuildText = None
		self.secondGuildText = None
		self.warInfo = None

		self.warID = int(warID)

		self.Initializition()
	
	def Destroy(self):
		self.Clear()
		self.start = 0
		self.observerCount=0
		self.end = 0
		self.perPage = 0
		self.currentPage = 0
		self.pageCount = 0
		self.isStillCantHide=0
		self.firstGuildText = None
		self.secondGuildText = None
		self.warInfo = None

	def Initializition(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/guildwar_static_log.py")
			self.rankListBoxEx = self.GetChild("ListBoxNEW")
			self.GetChild("next_btn").SAFE_SetEvent(self.NextPage)
			self.GetChild("back_btn").SAFE_SetEvent(self.PrevPage)
		except:
			import exception
			exception.Abort("EventInfo.LoadDialog.LoadScript")

		self.rankListBoxEx.SetViewItemCount(10)
		self.rankListBoxEx.SetItemStep(26)
		self.rankListBoxEx.SetItemSize(550,26)

		self.firstGuildText = ui.MultiTextLine()
		self.firstGuildText.SetParent(self.GetChild("RightThinboard"))
		self.firstGuildText.SetTextType("horizontal#center")
		self.firstGuildText.SetTextRange(20)
		self.firstGuildText.SetPosition(93,55)
		self.firstGuildText.Show()

		self.secondGuildText = ui.MultiTextLine()
		self.secondGuildText.SetParent(self.GetChild("RightThinboard"))
		self.secondGuildText.SetTextType("horizontal#center")
		self.secondGuildText.SetTextRange(20)
		self.secondGuildText.SetPosition(380,55)
		self.secondGuildText.Show()

		self.warInfo = ui.MultiTextLine()
		self.warInfo.SetParent(self.GetChild("RightThinboard"))
		self.warInfo.SetTextType("horizontal#center")
		self.warInfo.SetTextRange(20)
		self.warInfo.SetPosition(240,95)
		self.warInfo.Show()

	def OnPressEscapeKey(self):
		self.Hide()
		return True

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Update()
		self.Show()

	def Clear(self):
		if self.rankListBoxEx:
			self.rankListBoxEx.RemoveAllItems()

	def SortAfterCheck(self, listbox):
		data = self.rankListBoxEx.itemList
		for rank in data:
			index = data.index(rank)
			rank.children["playerRank"].Index = index+1
			rank.children["playerRank"].SetText("%d"%(index+1))
			rank.ChangeColor()

	def UpdatePageCount(self):
		self.pageCount = int(math.ceil(float(guild.WarStatisticsDataSize(self.warID)) / float(self.perPage)))
		if self.pageCount == 0:
			self.pageCount = 1
		self.GetChild("page_text").SetText("%d/%d"%(self.currentPage,self.pageCount))
		self.start = (self.currentPage - 1) * self.perPage
		self.end = ((self.currentPage - 1) * self.perPage) + self.perPage
		if self.pageCount == 1:
			self.GetChild("next_btn").Hide()
			self.GetChild("back_btn").Hide()
		else:
			self.GetChild("next_btn").Show()
			self.GetChild("back_btn").Show()

		if self.end >= guild.WarStatisticsDataSize(self.warID):
			self.end = guild.WarStatisticsDataSize(self.warID)

	def Update(self):
		self.UpdatePageCount()
		for j in range(self.start,self.end):
			resultItem = self.rankListBoxItem(self.warID, j)
			self.rankListBoxEx.AppendItem(resultItem)

		self.rankListBoxEx.itemList.sort()
		self.rankListBoxEx.SetBasePos(0)
		self.SortAfterCheck(self.rankListBoxEx)
		self.UpdateMultiText()

	def NextPage(self):
		if self.currentPage < self.pageCount:
			self.currentPage += 1
			self.Clear()
			self.Update()

	def PrevPage(self):
		if self.currentPage > 1:
			self.currentPage -= 1
			self.Clear()
			self.Update()

	def UpdateMultiText(self):
		if app.__IMPROVED_GUILD_WAR__:
			(dwID, dwGuildFrom, dwGuildTo, dwTime, bType, iMaxPlayer, iMaxScore, flags, winner, guild1_name, guild2_name, date) = guild.WarStatisticsInfo(self.warID, False)

			text = ""
			text+= localeInfo.GULDWAR_STATIC_MAXPLAYER % iMaxPlayer
			text+="\n"
			text+= localeInfo.GULDWAR_STATIC_MAXSCORE % iMaxScore
			self.warInfo.SetText(text)
		else:
			(dwID, dwGuildFrom, dwGuildTo, dwTime, bType, winner, guild1_name, guild2_name, date) = guild.WarStatisticsInfo(self.warID, False)

		guild_id  = [[dwGuildFrom,self.firstGuildText],[dwGuildTo,self.secondGuildText]]
		data = []
		for guildX in guild_id:
			guildX[1].SetText("")
			if guildX[0] == -1:
				continue
			item = []
			multi_text = ""
			(leaderName, onlineCount, offlineCount, spyCount, totalKill, totalDead, totalDmg, guildEmpire, raceList)  = uiGuildWarData.GetWarStatistics(self.warID,guildX[0])
			if leaderName != "-":
				multi_text += localeInfo.GUILDWAR_STATIC_TOTAL_INFO+"\n"
				multi_text += "%s: %s\t"%(localeInfo.GUILDWAR_STATIC_DEAD,(localeInfo.NumberToMoneyStringNEW(totalDead)))
				multi_text += "%s: %s\n"%(localeInfo.GUILDWAR_STATIC_DMG,(localeInfo.NumberToMoneyStringNEW(totalDmg)))

				item.append(guildX[0])
				item.append(totalKill)
				item.append(onlineCount)
				data.append(item)

				c = 0
				for raceCount in raceList:
					multi_text += "|Erace_%d|e: %d\t"%(c,raceCount)
					c+=1

			if multi_text != "":
				guildX[1].SetText(multi_text)

		if len(data) > 1:
			self.GetChild("guild_0_score").SetText(str(data[0][1]))
			self.GetChild("guild_1_score").SetText(str(data[1][1]))


		self.GetChild("mark_0").SetIndex(dwGuildFrom)
		self.GetChild("guild_0_name").SetText("%s"%guild1_name)

		self.GetChild("mark_1").SetIndex(dwGuildTo)
		self.GetChild("guild_1_name").SetText("%s"%guild2_name)
		
		self.SetScore()

	def SetScore(self):
		score1 = int(self.GetChild("guild_0_score").GetText())
		score2 = int(self.GetChild("guild_1_score").GetText())
		lastScore = 0
		if score1 > score2:
			lastScore = score1-score2
			self.GetChild("guild_0_score").SetPackedFontColor(0xff50b409)
			self.GetChild("guild_1_score").SetPackedFontColor(0xffea150a)
		elif score2 > score1:
			lastScore = score2-score1
			self.GetChild("guild_0_score").SetPackedFontColor(0xffea150a)
			self.GetChild("guild_1_score").SetPackedFontColor(0xff50b409)
		self.GetChild("against").SetText(localeInfo.GULDWAR_STATIC_AGAINST %lastScore)

