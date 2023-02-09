import ui, net, guild, playerSettingModule, localeInfo, uiCommon

IMG_DIRECTORY = "d:/ymir work/ui/game/guild_request/"

class QuestionDialogRequest(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.CreateWindow()
	def __del__(self):
		ui.ScriptWindow.__del__(self)
	def Destroy(self):
		self.textLine = None
		self.removeButton = None
		self.cancelButton = None
		self.ClearDictionary()
	def CreateWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog_request.py")

			self.board = self.GetChild("board")
			self.textLine = self.GetChild("message")
			self.acceptButton = self.GetChild("accept")
			self.removeButton = self.GetChild("remove")
			self.cancelButton = self.GetChild("cancel")
		except:
			import exception
			exception.Abort("uiGuildRequest.QuestionDialogRequest.CreateWindow")
	def SetText(self, text):
		self.textLine.SetText(text)
		width = self.textLine.GetTextSize()[0]
		if width > self.board.GetWidth():
			self.SetWidth(width+10)
	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()
	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()
	def Close(self):
		self.Hide()
	def OnPressEscapeKey(self):
		self.Close()
		return TRUE

class GuildRequestWindow(ui.BoardWithTitleBar):
	class requestItem(ui.Button):
		def __del__(self):
			ui.Button.__del__(self)
		def Destroy(self):
			if self.questiondialog != None:
				self.OnCloseQuestinDialog()
			self.children = {}
			self.g_id = -1
		def __init__(self):
			ui.Button.__init__(self)
			self.questiondialog = None
			self.Destroy()
		def isMyGuild(self):
			return self.g_id == guild.GetGuildID()
		def SetImage(self, tabIndex):
			if tabIndex <= 3:
				if self.isMyGuild():
					self.SetUpVisual(IMG_DIRECTORY+"item_0_1.tga")
				else:
					self.SetUpVisual(IMG_DIRECTORY+"item_0_0.tga")
				self.SetOverVisual(IMG_DIRECTORY+"item_0_1.tga")
				self.SetDownVisual(IMG_DIRECTORY+"item_0_1.tga")
			else:
				self.SetUpVisual(IMG_DIRECTORY+"item_1_0.tga")
				self.SetOverVisual(IMG_DIRECTORY+"item_1_1.tga")
				self.SetDownVisual(IMG_DIRECTORY+"item_1_1.tga")
		def raceToText(self, race):
			get_race_index = {
				playerSettingModule.RACE_WARRIOR_M	: 0,
				playerSettingModule.RACE_ASSASSIN_W	: 1,
				playerSettingModule.RACE_SURA_M		: 2,
				playerSettingModule.RACE_SHAMAN_W	: 3,
				playerSettingModule.RACE_WARRIOR_W	: 0,
				playerSettingModule.RACE_ASSASSIN_M	: 1,
				playerSettingModule.RACE_SURA_W		: 2,
				playerSettingModule.RACE_SHAMAN_M	: 3,
			}
			character_names = [
				localeInfo.TOOLTIP_WARRIOR,
				localeInfo.TOOLTIP_ASSASSIN,
				localeInfo.TOOLTIP_SURA,
				localeInfo.TOOLTIP_SHAMAN
			]
			if get_race_index.has_key(race):
				return character_names[get_race_index[race]]
			return character_names[0]
		def skillIndexToText(self, race, skillIndex):
			get_race_index = {
				playerSettingModule.RACE_WARRIOR_M	: 0,
				playerSettingModule.RACE_ASSASSIN_W	: 1,
				playerSettingModule.RACE_SURA_M		: 2,
				playerSettingModule.RACE_SHAMAN_W	: 3,
				playerSettingModule.RACE_WARRIOR_W	: 0,
				playerSettingModule.RACE_ASSASSIN_M	: 1,
				playerSettingModule.RACE_SURA_W		: 2,
				playerSettingModule.RACE_SHAMAN_M	: 3,
			}
			SKILL_GROUP_NAME_DICT = {
				playerSettingModule.JOB_WARRIOR	: { 1 : localeInfo.SKILL_GROUP_WARRIOR_1,	2 : localeInfo.SKILL_GROUP_WARRIOR_2, },
				playerSettingModule.JOB_ASSASSIN	: { 1 : localeInfo.SKILL_GROUP_ASSASSIN_1,	2 : localeInfo.SKILL_GROUP_ASSASSIN_2, },
				playerSettingModule.JOB_SURA		: { 1 : localeInfo.SKILL_GROUP_SURA_1,		2 : localeInfo.SKILL_GROUP_SURA_2, },
				playerSettingModule.JOB_SHAMAN		: { 1 : localeInfo.SKILL_GROUP_SHAMAN_1,	2 : localeInfo.SKILL_GROUP_SHAMAN_2, },
			}
			try:
				return SKILL_GROUP_NAME_DICT[get_race_index[race]][skillIndex]
			except:
				return localeInfo.GUILD_REQUEST_NONE_SKILL
		def LoadRequest(self, index, pid, name, level, race, skillIndex):
			textList = [
				[str(index),25],
				[str(name),115],
				[str(level),207],
				[self.raceToText(race),287],
				[self.skillIndexToText(race,skillIndex),392],
			]
			for textL in textList:
				index = textList.index(textL)
				text = ui.TextLine()
				text.SetParent(self)
				text.SetPosition(textL[1]-5,3)
				text.SetText(textL[0])
				text.SetHorizontalAlignCenter()
				text.Show()
				self.children["text%d"%index] = text
			self.SAFE_SetEvent(self.SetMasterRequest, name, pid)
		def LoadPage(self, index, g_id, name, level, ladder_point, membercount, maxmember, isRequest):
			self.g_id = g_id
			textList = [
				[str(index),25],
				[str(name),115],
				[str(level),207],
				[str(ladder_point),272],
				[str(membercount)+"/"+str(maxmember),342],
				#["",410],
			]
			for textL in textList:
				index = textList.index(textL)
				text = ui.TextLine()
				text.SetParent(self)
				text.SetPosition(textL[1]-5,3)
				text.SetText(textL[0])
				text.SetHorizontalAlignCenter()
				text.Show()
				self.children["text%d"%index] = text
			if not self.isMyGuild():
				event = lambda index = g_id, request = isRequest : ui.__mem_func__(self.SetSendRequest)(index, request)
				self.children["request"] = ui.CheckBoxNew(self, 393, 1, event)
				self.children["request"].SetCheck(isRequest)
		def SetMasterRequest(self, playerName, playerID):
			if self.questiondialog != None:
				self.OnCloseQuestinDialog()
			questiondialog = QuestionDialogRequest()
			questiondialog.SetText(localeInfo.GUILD_REQUEST_MASTER_REQUEST % playerName)
			questiondialog.acceptButton.SAFE_SetEvent(self.SendRequest, playerID, 2)
			questiondialog.removeButton.SAFE_SetEvent(self.SendRequest, playerID, 3)
			questiondialog.cancelButton.SAFE_SetEvent(self.OnCloseQuestinDialog)
			questiondialog.Open()
			self.questiondialog = questiondialog
		def SetSendRequest(self, g_id, isRequest):
			if self.questiondialog != None:
				self.OnCloseQuestinDialog()
			questiondialog = uiCommon.QuestionDialog()
			if isRequest:
				questiondialog.SetText(localeInfo.GUILD_REQUEST_REMOVE_REQUEST)
				questiondialog.acceptButton.SAFE_SetEvent(self.SendRequest, g_id, 1)
			else:
				questiondialog.textLine.SetText(localeInfo.GUILD_REQUEST_SEND_REQUEST)
				questiondialog.acceptButton.SAFE_SetEvent(self.SendRequest, g_id, 0)
			questiondialog.cancelButton.SAFE_SetEvent(self.OnCloseQuestinDialog)
			questiondialog.Open()
			self.questiondialog = questiondialog
		def SendRequest(self, first, second):
			net.SendGuildRequest(first, second)
			self.OnCloseQuestinDialog()
		def OnCloseQuestinDialog(self):
			if self.questiondialog != None:
				self.questiondialog.Close()
				self.questiondialog = None

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)
	def Destroy(self):
		if self.children.has_key("listBox"):
			self.children["listBox"].RemoveAllItems()
			self.children["listBox"]=None
		self.children = {}
		self.radioBtns = []
		self.tabIndex = 0
		self.perPage = 0
		self.currentPage = 0
		self.pageCount = 0
		self.maxPage = 0
		self.isFirst = False

	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.children = {}
		self.Destroy()
		self._LoadWindow()

	def _LoadWindow(self):
		self.SetSize(473, 375)

		self.SetCloseEvent(self.Close)
		self.SetTitleName("Guild Request Window")
		self.AddFlag("movable")
		self.AddFlag("attach")
		self.AddFlag("float")
		self.SetCenterPosition()

		self.perPage = 8
		self.currentPage = 1
		self.pageCount = 1

		board = ui.ImageBox()
		board.SetParent(self)
		board.AddFlag("not_pick")
		board.SetPosition(15,55)
		board.LoadImage(IMG_DIRECTORY+"board.tga")
		board.Show()
		self.children["board"] = board

		listBox = ui.ListBoxEx()
		listBox.SetParent(board)
		listBox.SetSize(board.GetWidth()-(2*4),board.GetHeight()-(2*26))
		listBox.SetPosition(4,26)
		listBox.SetItemSize(435,21)
		listBox.SetItemStep(25)
		listBox.SetViewItemCount(8)
		listBox.Show()
		self.children["listBox"] = listBox

		self.loadingImageRotation = 0
		loadingImage = ui.ExpandedImageBox()
		loadingImage.SetParent(listBox)
		loadingImage.LoadImage(IMG_DIRECTORY+"load_.tga")
		loadingImage.SetPosition((listBox.GetWidth()/2)-loadingImage.GetWidth() + 15, (listBox.GetHeight()/2)-loadingImage.GetHeight())
		loadingImage.Show()
		self.children["loadingImage"] = loadingImage

		searchNameBtn = ui.Button()
		searchNameBtn.SetParent(self)
		searchNameBtn.SetUpVisual(IMG_DIRECTORY+"search_name_0.tga")
		searchNameBtn.SetOverVisual(IMG_DIRECTORY+"search_name_1.tga")
		searchNameBtn.SetDownVisual(IMG_DIRECTORY+"search_name_2.tga")
		searchNameBtn.SetPosition(15+board.GetWidth()-searchNameBtn.GetWidth(),33)
		searchNameBtn.SAFE_SetEvent(self.SearchWithName)
		searchNameBtn.Show()
		self.children["searchNameBtn"] = searchNameBtn

		editLineImg = ui.ImageBox()
		editLineImg.SetParent(self)
		editLineImg.LoadImage(IMG_DIRECTORY+"editline.tga")
		editLineImg.SetPosition(15+board.GetWidth()-searchNameBtn.GetWidth()-5-editLineImg.GetWidth(),33)
		editLineImg.Show()
		self.children["editLineImg"] = editLineImg

		editLine = ui.EditLine()
		editLine.SetParent(editLineImg)
		editLine.SetPosition(2,3)
		editLine.SetSize(editLineImg.GetWidth(),editLineImg.GetHeight())
		editLine.SetInfoMessage(localeInfo.GUILD_REQUEST_GUILD_NAME)
		editLine.SetMax(15)
		editLine.Show()
		self.children["editLine"] = editLine

		refreshBtn = ui.Button()
		refreshBtn.SetParent(self)
		refreshBtn.SetUpVisual(IMG_DIRECTORY+"refresh_0.tga")
		refreshBtn.SetOverVisual(IMG_DIRECTORY+"refresh_1.tga")
		refreshBtn.SetDownVisual(IMG_DIRECTORY+"refresh_2.tga")
		refreshBtn.SetPosition(15+board.GetWidth()-refreshBtn.GetWidth(),55+board.GetHeight()+5)
		refreshBtn.SAFE_SetEvent(self.RefreshButton)
		refreshBtn.Show()
		self.children["refreshBtn"] = refreshBtn

		tabImage = ui.ImageBox()
		tabImage.SetParent(self)
		tabImage.LoadImage(IMG_DIRECTORY+"tab_0.tga")
		tabImage.SetPosition(3,55+board.GetHeight()+5+refreshBtn.GetHeight()+2)
		tabImage.Show()
		self.children["tabImage"] = tabImage

		backLastBtn = ui.Button()
		backLastBtn.SetParent(self.children["board"] )
		backLastBtn.SetUpVisual(IMG_DIRECTORY+"back_last_0.tga")
		backLastBtn.SetOverVisual(IMG_DIRECTORY+"back_last_1.tga")
		backLastBtn.SetDownVisual(IMG_DIRECTORY+"back_last_1.tga")
		backLastBtn.SetPosition(75,228)
		backLastBtn.Show()
		self.children["backLastBtn"] = backLastBtn
		
		backBtn = ui.Button()
		backBtn.SetParent(self.children["board"])
		backBtn.SetUpVisual(IMG_DIRECTORY+"back_btn_0.tga")
		backBtn.SetOverVisual(IMG_DIRECTORY+"back_btn_1.tga")
		backBtn.SetDownVisual(IMG_DIRECTORY+"back_btn_1.tga")
		backBtn.SetPosition(75+22,228)
		backBtn.Show()
		self.children["backBtn"] = backBtn

		nextBtn = ui.Button()
		nextBtn.SetParent(self.children["board"] )
		nextBtn.SetUpVisual(IMG_DIRECTORY+"next_btn_0.tga")
		nextBtn.SetOverVisual(IMG_DIRECTORY+"next_btn_1.tga")
		nextBtn.SetDownVisual(IMG_DIRECTORY+"next_btn_1.tga")
		nextBtn.SetPosition(75+22+241,228)
		nextBtn.Show()
		self.children["nextBtn"] = nextBtn

		nextLastBtn = ui.Button()
		nextLastBtn.SetParent(self.children["board"] )
		nextLastBtn.SetUpVisual(IMG_DIRECTORY+"next_last_0.tga")
		nextLastBtn.SetOverVisual(IMG_DIRECTORY+"next_last_1.tga")
		nextLastBtn.SetDownVisual(IMG_DIRECTORY+"next_last_1.tga")
		nextLastBtn.SetPosition(75+22+241+22,228)
		nextLastBtn.Show()
		self.children["nextLastBtn"] = nextLastBtn

		for j in xrange(5):
			tabBtn = ui.RadioButton()
			tabBtn.SetParent(tabImage)
			tabBtn.SetUpVisual(IMG_DIRECTORY+"btn.tga")
			tabBtn.SetOverVisual(IMG_DIRECTORY+"btn.tga")
			tabBtn.SetDownVisual(IMG_DIRECTORY+"btn.tga")
			tabBtn.SetPosition(10+(j*16)+(j*tabBtn.GetWidth()), 9)
			tabBtn.SAFE_SetEvent(self.SetTabBtn,j)
			tabBtn.Show()
			self.radioBtns.append(tabBtn)

			pageBtn = ui.Button()
			pageBtn.SetParent(self.children["board"])
			pageBtn.SetUpVisual(IMG_DIRECTORY+"page_btn_0.tga")
			pageBtn.SetOverVisual(IMG_DIRECTORY+"page_btn_1.tga")
			pageBtn.SetDownVisual(IMG_DIRECTORY+"page_btn_1.tga")
			pageBtn.SetPosition(75+22+29+(j*40),227)
			pageBtn.Show()
			self.children["pageBtn%d"%j] = pageBtn

	def OnUpdate(self):
		self.loadingImageRotation+=10
		if self.children.has_key("loadingImage"):
			if self.children["loadingImage"].IsShow():
				self.children["loadingImage"].SetRotation(self.loadingImageRotation)

	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			btn=buttonList[buttonIndex]
		except IndexError:
			return
		for eachButton in buttonList:
			eachButton.SetUp()
		btn.Down()

	def RefreshBoardTitle(self):
		if self.tabIndex <= 3:
			textList = [
				[localeInfo.GUILD_REQUEST_POSITION,25],
				[localeInfo.GUILD_REQUEST_GUILD_NAME,115],
				[localeInfo.GUILD_REQUEST_LEVEL,205],
				[localeInfo.GUILD_REQUEST_RANK,270],
				[localeInfo.GUILD_REQUEST_MEMBER,340],
				[localeInfo.GUILD_REQUEST_REQUEST,410],
			]
		else:
			textList = [
				[localeInfo.GUILD_REQUEST_POSITION,25],
				[localeInfo.GUILD_REQUEST_PLAYER_NAME,115],
				[localeInfo.GUILD_REQUEST_LEVEL,205],
				[localeInfo.GUILD_REQUEST_CLASS,285],
				[localeInfo.GUILD_REQUEST_SUB_CLASS,390],
			]

		for j in xrange(6):
			if self.children.has_key("titleText%d"%j):
				self.children["titleText%d"%j] = None

		for text in textList:
			index = textList.index(text)
			titleText = ui.TextLine()
			titleText.SetParent(self.children["board"])
			titleText.SetPosition(text[1],5)
			titleText.SetText(text[0])
			titleText.SetHorizontalAlignCenter()
			titleText.Show()
			self.children["titleText%d"%index] = titleText

	def RefreshTabSetting(self):
		self.children["editLine"].SetText("")
		if self.tabIndex <= 3:
			self.children["editLineImg"].Show()
			self.children["searchNameBtn"].Show()
			self.children["refreshBtn"].Show()
		else:
			self.children["editLineImg"].Hide()
			self.children["searchNameBtn"].Hide()
			self.children["refreshBtn"].Hide()

	def SetTabBtn(self, index, needPacket = True):
		self.tabIndex = index
		self.__ClickRadioButton(self.radioBtns, index)
		self.children["tabImage"].LoadImage(IMG_DIRECTORY+"tab_%d.tga"%int(index))
		self.RefreshBoardTitle()
		self.RefreshTabSetting()

		if needPacket:
			self.SendRequest(self.tabIndex, 1)

	def Open(self):
		if self.isFirst == False:
			self.isFirst = True
			self.SetTabBtn(0)
		self.Show()

	def SearchWithName(self):
		text = self.children["editLine"].GetText()
		if text.isspace() or text == "" or text == " ":
			return
		self.SendRequest(self.tabIndex,0,text)

	def RefreshButton(self):
		self.SetTabBtn(self.tabIndex)

	def SendRequest(self, tabIndex, pageIndex, name = ""):
		self.children["loadingImage"].Show()
		self.children["listBox"].RemoveAllItems()

		if name == "":
			net.SendGuildRequestPage(tabIndex, pageIndex)
		else:
			net.SendGuildRequestName(tabIndex, name)

	def SetPageStatus(self, flag):
		if flag:
			self.children["backLastBtn"].Show()
			self.children["backBtn"].Show()
			self.children["nextBtn"].Show()
			self.children["nextLastBtn"].Show()
			for j in xrange(5):
				self.children["pageBtn%d"%j].Show()
		else:
			self.children["backLastBtn"].Hide()
			self.children["backBtn"].Hide()
			self.children["nextBtn"].Hide()
			self.children["nextLastBtn"].Hide()
			for j in xrange(5):
				self.children["pageBtn%d"%j].Hide()
	
	def GuildRequestLoadName(self, tabIndex):
		self.children["listBox"].RemoveAllItems()
		self.children["loadingImage"].Hide()
		self.SetTabBtn(tabIndex, False)
		self.SetPageStatus(False)

	def GuildRequestLoadPage(self, tabIndex, pageIndex, maxPage):
		self.children["listBox"].RemoveAllItems()
		self.children["loadingImage"].Hide()
		self.SetTabBtn(tabIndex, False)
		self.SetPageStatus(True)
		self.CalculatePage(pageIndex, maxPage)

	def CalculatePage(self, pageIndex, maxPage):
		self.currentPage = pageIndex
		self.maxPage = maxPage

		btns = {
			"backLastBtn":"back_last_%d",
			"backBtn":"back_btn_%d",
			"nextBtn":"next_btn_%d",
			"nextLastBtn":"next_last_%d",
			"pageBtn0":"page_btn_%d",
			"pageBtn1":"page_btn_%d",
			"pageBtn2":"page_btn_%d",
			"pageBtn3":"page_btn_%d",
			"pageBtn4":"page_btn_%d",
		}

		buttonCount = (self.currentPage%5)
		pageBtnIndex = (self.currentPage % 5)
		if pageBtnIndex <= 0:
			pageBtnIndex = 4
		else:
			pageBtnIndex-=1
		pageStartIndex = self.currentPage - pageBtnIndex

		if self.currentPage > 5:
			file = btns["backLastBtn"] % 0
			self.children["backLastBtn"].SetUpVisual(IMG_DIRECTORY+file+".tga")
			file = btns["backLastBtn"] % 1
			self.children["backLastBtn"].SetOverVisual(IMG_DIRECTORY+file+".tga")
			self.children["backLastBtn"].SetDownVisual(IMG_DIRECTORY+file+".tga")
			self.children["backLastBtn"].SAFE_SetEvent(self.SetPageBtn,1)
			
		else:
			file = btns["backLastBtn"] % 0
			self.children["backLastBtn"].SetUpVisual(IMG_DIRECTORY+file+".tga")
			self.children["backLastBtn"].SetOverVisual(IMG_DIRECTORY+file+".tga")
			self.children["backLastBtn"].SetDownVisual(IMG_DIRECTORY+file+".tga")
			self.children["backLastBtn"].eventFunc = None

		if self.maxPage-pageStartIndex > 5:
			file = btns["nextLastBtn"] % 0
			self.children["nextLastBtn"].SetUpVisual(IMG_DIRECTORY+file+".tga")
			file = btns["nextLastBtn"] % 1
			self.children["nextLastBtn"].SetOverVisual(IMG_DIRECTORY+file+".tga")
			self.children["nextLastBtn"].SetDownVisual(IMG_DIRECTORY+file+".tga")
			self.children["nextLastBtn"].SAFE_SetEvent(self.SetPageBtn,self.maxPage)

		else:
			file = btns["nextLastBtn"] % 0
			self.children["nextLastBtn"].SetUpVisual(IMG_DIRECTORY+file+".tga")
			self.children["nextLastBtn"].SetOverVisual(IMG_DIRECTORY+file+".tga")
			self.children["nextLastBtn"].SetDownVisual(IMG_DIRECTORY+file+".tga")
			self.children["nextLastBtn"].eventFunc = None

		if pageStartIndex > 5:
			file = btns["backBtn"] % 0
			self.children["backBtn"].SetUpVisual(IMG_DIRECTORY+file+".tga")
			file = btns["backBtn"] % 1
			self.children["backBtn"].SetOverVisual(IMG_DIRECTORY+file+".tga")
			self.children["backBtn"].SetDownVisual(IMG_DIRECTORY+file+".tga")
			self.children["backBtn"].SAFE_SetEvent(self.SetPageBtn,pageStartIndex-5)
		else:
			file = btns["backBtn"] % 0
			self.children["backBtn"].SetUpVisual(IMG_DIRECTORY+file+".tga")
			self.children["backBtn"].SetOverVisual(IMG_DIRECTORY+file+".tga")
			self.children["backBtn"].SetDownVisual(IMG_DIRECTORY+file+".tga")
			self.children["backBtn"].eventFunc = None

		if pageStartIndex+5 <= self.maxPage:
			file = btns["nextBtn"] % 0
			self.children["nextBtn"].SetUpVisual(IMG_DIRECTORY+file+".tga")
			file = btns["nextBtn"] % 1
			self.children["nextBtn"].SetOverVisual(IMG_DIRECTORY+file+".tga")
			self.children["nextBtn"].SetDownVisual(IMG_DIRECTORY+file+".tga")
			self.children["nextBtn"].SAFE_SetEvent(self.SetPageBtn,pageStartIndex+5)
		else:
			file = btns["nextBtn"] % 0
			self.children["nextBtn"].SetUpVisual(IMG_DIRECTORY+file+".tga")
			self.children["nextBtn"].SetOverVisual(IMG_DIRECTORY+file+".tga")
			self.children["nextBtn"].SetDownVisual(IMG_DIRECTORY+file+".tga")
			self.children["nextBtn"].eventFunc = None

		for j in xrange(5):
			self.children["pageBtn%d"%j].Hide()

		for j in xrange(5):
			if pageStartIndex+j > self.maxPage:
				continue

			if j == pageBtnIndex:
				file = btns["pageBtn%d"%j] % 0
				self.children["pageBtn%d"%j].SetUpVisual(IMG_DIRECTORY+file+".tga")
				self.children["pageBtn%d"%j].SetOverVisual(IMG_DIRECTORY+file+".tga")
				self.children["pageBtn%d"%j].SetDownVisual(IMG_DIRECTORY+file+".tga")
			else:
				file = btns["pageBtn%d"%j] % 1
				self.children["pageBtn%d"%j].SetUpVisual(IMG_DIRECTORY+file+".tga")
				file = btns["pageBtn%d"%j] % 0
				self.children["pageBtn%d"%j].SetOverVisual(IMG_DIRECTORY+file+".tga")
				self.children["pageBtn%d"%j].SetDownVisual(IMG_DIRECTORY+file+".tga")

			self.children["pageBtn%d"%j].SAFE_SetEvent(self.SetPageBtn,pageStartIndex+j)
			self.children["pageBtn%d"%j].SetText(str(pageStartIndex+j))
			self.children["pageBtn%d"%j].Show()

	def SetPageBtn(self, index):
		self.SendRequest(self.tabIndex, index)

	def GuildRequestSetItem(self, index, g_id, name, level, ladder_point, membercount, maxmember, isRequest):
		wnd = self.requestItem()
		wnd.LoadPage(index, g_id, name, level, ladder_point, membercount, maxmember, isRequest)
		wnd.SetImage(self.tabIndex)
		self.children["listBox"].AppendItem(wnd)

	def GuildRequestSetRequest(self, index, pid, name, level, race, skillIndex):
		wnd = self.requestItem()
		wnd.LoadRequest(index, pid, name, level, race, skillIndex)
		wnd.SetImage(self.tabIndex)
		self.children["listBox"].AppendItem(wnd)

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True
