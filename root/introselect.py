import chr
import grp
import app
import math
import wndMgr
import snd
import net
import systemSetting
import localeInfo
import chr

import constInfo
import ui
import uiScriptLocale
import networkModule
import musicInfo
import playerSettingModule

####################################
# ???? ?????? ???? ??? ?¥å? ?¬Õ?
####################################
import uiCommon                    
import uiMapNameShower             
import uiAffectShower              
import uiPlayerGauge               
import uiCharacter                 
import uiTarget                    
import consoleModule               

# interface module?? ??????...
import interfaceModule
import uiTaskBar                   
import uiInventory

###################################

LEAVE_BUTTON_FOR_POTAL = FALSE
NOT_NEED_DELETE_CODE = FALSE
ENABLE_ENGNUM_DELETE_CODE = FALSE

if localeInfo.IsJAPAN():
	NOT_NEED_DELETE_CODE = TRUE
elif localeInfo.IsHONGKONG():
	ENABLE_ENGNUM_DELETE_CODE = TRUE
elif localeInfo.IsNEWCIBN() or localeInfo.IsCIBN10():
	ENABLE_ENGNUM_DELETE_CODE = TRUE
elif localeInfo.IsEUROPE():
	ENABLE_ENGNUM_DELETE_CODE = TRUE

###################################

ROTATE_SPEED = 2.5
MAX_STATUS_POINTS = 90

COMMON_PATH = "d:/ymir work/ui/intro_elendos/common/"
CHAR_ICON_DICT = {
	0 : COMMON_PATH + "character_icon_warrior.sub", 
	1 : COMMON_PATH + "character_icon_assassin.sub", 
	2 : COMMON_PATH + "character_icon_sura.sub", 
	3 : COMMON_PATH + "character_icon_shaman.sub", 
	4 : COMMON_PATH + "character_icon_warrior.sub", 
	5 : COMMON_PATH + "character_icon_assassin.sub", 
	6 : COMMON_PATH + "character_icon_sura.sub", 
	7 : COMMON_PATH + "character_icon_shaman.sub", 
}

MAP_NAME_DICT = {
	0 : "",
	1 : "Shinsoo - Yongan (Map1)",
	3 : "Shinsoo - Yayang (Map2)",
	4 : "Shinsoo - Jungrang (Guildzone)",
	6 : "Shinsoo - Miryang (Guildzone 2)",
	21 : "Chunjo - Joan (Map1)",
	23 : "Chunjo - Bokjung (Map2)",
	24 : "Chunjo - Waryong (Guildzone)",
	116 : "Chunjo - Songpa (Guildzone 2)",
	41 : "Jinno - Pyungmoo (Map1)",
	43 : "Jinno - Bakra (Map2)",
	44 : "Jinno - Imha (Guildzone)",
	46 : "Jinno - Daeyami (Guildzone 2)",
	5 : "Hasun Dong - (Monkey Dungeon Beginner)",
	25 : "Hasun Dong - (Monkey Dungeon Beginner)",
	45 : "Hasun Dong - (Monkey Dungeon Beginner)",
	107 : "Hasun Dong - (Monkey Dungeon Beginner)",
	108 : "Jungsun Dong - (Monkey Dungeon Normally)",
	109 : "Sangsun Dong - (Monkey Dungeon Expert)",
	61 : "Mount Sohan (Iceland)",
	62 : "Doyyumhwaji (Fireland)",
	63 : "Yongbi Desert",
	64 : "Valley of Seungryong - (Orctal)",
	65 : "Hwang Temple",
	67 : "Lungsam - (Ghost forest)",
	68 : "Lungsam - (Red forest)",
	69 : "Snakefiield",
	70 : "Valley of Giants",
	81 : "Wedding Place",
	103 : "Guild War",
	105 : "Guild War",
	110 : "Guild War",
	111 : "Guild War",
	112 : "PvP-Area",
	113 : "OX Map - (Event)",
	120 : "Empire War - (Event)",
	121 : "Empire War - (Event)",
	122 : "Empire War - (Event)",
	123 : "Empire War - (Event)",
	124 : "Empire War - (Event)",
	125 : "Empire War - (Event)",
	126 : "Empire War - (Event)",
	127 : "Empire War - (Event)",
	128 : "Empire War - (Event)",
	351 : "Red Dragon Fortress - (Dungeon)",
	216 : "Devils Catacomb - (Dungeon)",
	352 : "Nemeres Warte - (Dungeon)",
	319 : "Hydra Ship defence - (Dungeon)",
	320 : "Hydra Entrance - (Entrance)",
	356 : "Land of Giants - (Normal Map)",
	400 : "Spider Baroness - (Dungeon)",
	401 : "Cape of the Dragon - (Normal Map)",
	402 : "Thunder Mountains - (Normal Map)",
	403 : "Gautama Cliff - (Normal Map)",
	404 : "Nephrite Bay - (Normal Map)",
	405 : "Enchanted Forest - (Normal Map)",
	66 : "Demon Tower - (Dungeon)",
	71 : "Spider Dungeon - (01)",
	104 : "Spider Dungeon - (02)",
	217 : "Spider Dungeon - (03)",
	72 : "Grotto of Exile - (1)",
	73 : "Grotto of Exile - (2)",
	409 : "Grotto of Exile - (Dragon Room)",
	242 : "Event Map - (Event)",
	223 : "Halloween Dungeon - (Event Map)",
	358 : "Demon Tower - (2)",
	37 : "Halloween Dungeon - (Dungeon)",
	212 : "Meleys Hoard - (Guild Dungeon)",
	77 : "Chamber of Wisdom - (Dungeon)",
	76 : "Deep underwater Shark Cave - (Dungeon)",
	334 : "Trade Mile - (Trading Map)",
	243 : "Spider Dungeon - (04)",
	350 : "Spider Dungeon - (05)",
	50 : "Sommer Map - (Event)",
	57 : "Sands of Suffering - (Level / Farmmap)",
	240 : "Demon Dungeon - (Dungeon)",
	245 : "Nephrite Cave - (Dungeon)",
	318 : "Orcmaze - (Dungeon)",
	325 : "Worldboss - (Dragon)",
	241 : "Mushroom Garden - (Dungeon)",
	54 : "Magic Trolls Cave - (Dungeon)",
	58 : "World Boss - (Diamond Dragon)",
	368 : "World Boss - (Snake)",
	152 : "Gamemaster - (Island)",
	270 : "Green Island - (Level / Farmmap)",
	271 : "White Dragon Cave - (Level / Farmmap)",
	272 : "White Dragon Cave - (Boss Room)",
	273 : "Heaven Island - (Level / Farmmap)",
	274 : "VIP Map - (01)",
	275 : "VIP Map - (02)",
	75 : "Ancient Pyramid - (Dungeon)",
	144 : "Shadow Tower - (Dungeon)",
	145 : "Shadow Tower - (Entrance)",
	150 : "Scorpion Ruins - (Dungeon)",
	147 : "Ancient Jungle - (Dungeon)",
	153 : "Lava Fields - (Level / Farmmap)",
	154 : "Valley of the Water - (Level / Farmmap)",
	134 : "Crafting and Dungeon Area - (Neutral Area)",
	27 : "Slime Cave - (Dungeon)",
	263 : "Elendosfiles PvP Map - (Global PvP)",
	156 : "Andun Catacombs (Level /Farmmap)",
	157 : "Seelen Dungeon - (Dungeon)",
}


class SelectCharacterWindow(ui.Window):

	SLOT_COUNT = 4
	CHARACTER_TYPE_COUNT = 4


	EMPIRE_NAME = { 
		net.EMPIRE_A : localeInfo.EMPIRE_A, 
		net.EMPIRE_B : localeInfo.EMPIRE_B, 
		net.EMPIRE_C : localeInfo.EMPIRE_C 
	}
	
	class CharacterRenderer(ui.Window):
		def OnRender(self):
			grp.ClearDepthBuffer()

			grp.SetGameRenderState()
			grp.PushState()
			grp.SetOmniLight()
			
			screenWidth = float(wndMgr.GetScreenWidth() / 2)
			screenHeight = float(wndMgr.GetScreenHeight())

			grp.SetViewport(0.25, 0.0, 0.5, 1.0) 

			app.SetCenterPosition(0.0, 0.0, 0.0)
			app.SetCamera(1550.0, 15.0, 180.0, 95.0)
			grp.SetPerspective(15.0, screenWidth/screenHeight, 1000.0, 3000.0)

			(x, y) = app.GetCursorPosition()
			grp.SetCursorPosition(x, y)

			chr.Deform()
			chr.Render()
			for i in xrange(5):#slotcount = 5
				chr.SelectInstance(i)
				chr.RenderAllAttachingEffect()

			grp.RestoreViewport()
			grp.PopState()
			grp.SetInterfaceRenderState()

	def __init__(self, stream):
		ui.Window.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_SELECT, self)

		self.stream=stream
		self.slot = self.stream.GetCharacterSlot()
		self.rotation = 0.0
		
		self.openLoadingFlag = FALSE
		self.startIndex = -1
		self.startReservingTime = 0

		self.characterInfoDict = {}
		self.characterSlotsDict = {}
		self.flagDict = {}
		self.curRotation = []
		self.destRotation = []

		self.curNameAlpha = []
		self.destNameAlpha = []
		for i in xrange(self.CHARACTER_TYPE_COUNT):
			self.curNameAlpha.append(0.0)
			self.destNameAlpha.append(0.0)

		self.curGauge = [0.0, 0.0, 0.0, 0.0]
		self.destGauge = [0.0, 0.0, 0.0, 0.0]

		self.dlgBoard = 0
		self.changeNameFlag = FALSE
		self.nameInputBoard = None
		self.sendedChangeNamePacket = FALSE

		self.startIndex = -1
		self.isLoad = 0

	def __del__(self):
		ui.Window.__del__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_SELECT, 0)

	def Open(self):
		if not self.__LoadBoardDialog("uiscript/intro_charselect.py"):
			import dbg
			dbg.TraceError("SelectCharacterWindow.Open - __LoadScript Error")
			return

		if not self.__LoadQuestionDialog("uiscript/questiondialog.py"):
			return

		# playerSettingModule.LoadGameData("INIT")

		self.SetFocus()
		self.InitCharacterBoard()

		self.dlgBoard.Show()
		self.SetWindowName("SelectCharacterWindow")
		self.Show()

		if self.slot>=0:
			self.SelectSlot(self.slot)

		if musicInfo.selectMusic != "":
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("BGM/"+musicInfo.selectMusic)

		app.SetCenterPosition(0.0, 0.0, 0.0)
		app.SetCamera(1550.0, 15.0, 180.0, 95.0)

		self.isLoad=1
		self.Refresh()

		if self.stream.isAutoSelect:
			chrSlot=self.stream.GetCharacterSlot()
			self.SelectSlot(chrSlot)
			self.StartGame()

		self.HideAllFlag()
        
        
		app.ShowCursor()

	def Close(self):
		if musicInfo.selectMusic != "":
			snd.FadeOutMusic("BGM/"+musicInfo.selectMusic)

		self.stream.popupWindow.Close()

		if self.dlgBoard:
			self.dlgBoard.ClearDictionary()

		self.dlgQuestion.ClearDictionary()
		self.dlgQuestion = None
		self.dlgQuestionText = None
		self.dlgQuestionAcceptButton = None
		self.dlgQuestionCancelButton = None
		self.privateInputBoard = None
		self.nameInputBoard = None

		chr.DeleteInstance(0)
		chr.DeleteInstance(1)
		chr.DeleteInstance(2)
		chr.DeleteInstance(3)

		self.Hide()
		self.KillFocus()

		app.HideCursor()
		
	def HideAllFlag(self):
		for flag in self.flagDict.values():
			flag.Hide()

	def Refresh(self):
		if not self.isLoad:
			return

		# SLOT4
		indexArray = (3, 2, 1, 0)
		for index in indexArray:
			playTime=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_PLAYTIME)
			id=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_ID)
			race=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_RACE)
			form=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_FORM)
			name=net.GetAccountCharacterSlotDataString(index, net.ACCOUNT_CHARACTER_SLOT_NAME)
			level=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_LEVEL)
			hair=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_HAIR)
			acce=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_ACCE)
			guildName=net.GetAccountCharacterSlotDataString(self.slot, net.ACCOUNT_CHARACTER_SLOT_GUILD_NAME)
			#weapon=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_WEAPON)
			#mapindex=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_MAPINDEX)
			
			if id:
				self.characterInfoDict[index] = {"empty" : False, "race" : race, "name" : str(name), "level" : level}
				self.MakeCharacter(index, id, name, race, form, hair, acce)
				self.SelectSlot(index)
			else:
				self.characterInfoDict[index] = {"empty" : True, "name" : "", "level" : 0}
				
		self.CreateCharacterSlots()
		self.SelectSlot(self.slot)

	def CreateCharacterSlots(self):
		indexArray = (0, 1, 2, 3)
		self.active_characters = 0
		self.characterSlotsDict = {}
		arrange_y = 68
		self.dlgBoard.GetChild("CharacterSlotEmpty").Hide()
		for index in indexArray:
			if self.characterInfoDict[index]["empty"] == False:
				self.dlgBoard.GetChild("CharacterSlot%d" % index).Show()
				self.dlgBoard.GetChild("CharacterSlot%d" % index).SetPosition(0, arrange_y)
				self.dlgBoard.GetChild("CharacterSlot%d_Icon" % index).LoadImage(CHAR_ICON_DICT[self.characterInfoDict[index]["race"]])
				self.dlgBoard.GetChild("CharacterSlot%d_Text1" % index).SetText("Lv.%d - %s" % (self.characterInfoDict[index]["level"], self.characterInfoDict[index]["name"]))
				#if MAP_NAME_DICT.has_key(self.characterInfoDict[index]["mapindex"]):
					#self.dlgBoard.GetChild("CharacterSlot%d_Text2" % index).SetText(MAP_NAME_DICT[self.characterInfoDict[index]["mapindex"]])
				#else:
				self.dlgBoard.GetChild("CharacterSlot%d_Text2" % index).SetText("")
				self.characterSlotsDict[index] = self.dlgBoard.GetChild("CharacterSlot%d" % index)
				self.dlgBoard.GetChild("CharacterSlot%d" % index).SetEvent(ui.__mem_func__(self.SelectSlot), index)
				self.active_characters += 1
				arrange_y += 75
			else:
				self.dlgBoard.GetChild("CharacterSlot%d" % index).Hide()
				
		if self.active_characters < 4:
			self.dlgBoard.GetChild("CharacterSlotEmpty").SetPosition(0, arrange_y)
			self.dlgBoard.GetChild("CharacterSlotEmpty").Show()

	
	def GetCharacterSlotID(self, slotIndex):
		return net.GetAccountCharacterSlotDataInteger(slotIndex, net.ACCOUNT_CHARACTER_SLOT_ID)

	def __LoadQuestionDialog(self, fileName):
		self.dlgQuestion = ui.ScriptWindow()

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self.dlgQuestion, fileName)
		except:
			import exception
			exception.Abort("SelectCharacterWindow.LoadQuestionDialog.LoadScript")

		try:
			GetObject=self.dlgQuestion.GetChild
			self.dlgQuestionText=GetObject("message")
			self.dlgQuestionAcceptButton=GetObject("accept")
			self.dlgQuestionCancelButton=GetObject("cancel")
		except:
			import exception
			exception.Abort("SelectCharacterWindow.LoadQuestionDialog.BindObject")

		self.dlgQuestionText.SetText(localeInfo.SELECT_DO_YOU_DELETE_REALLY)
		self.dlgQuestionAcceptButton.SetEvent(ui.__mem_func__(self.RequestDeleteCharacter))
		self.dlgQuestionCancelButton.SetEvent(ui.__mem_func__(self.dlgQuestion.Hide))
		return 1

	def __LoadBoardDialog(self, fileName):
		self.dlgBoard = ui.ScriptWindow()

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self.dlgBoard, fileName)
		except:
			import exception
			exception.Abort("SelectCharacterWindow.LoadBoardDialog.LoadScript")

		try:
			GetObject=self.dlgBoard.GetChild

			self.btn_start		= GetObject("PlayButton")
			# self.btn_create		= GetObject("btn_create")
			self.btn_delete		= GetObject("DeleteButton")
			self.btn_close		= GetObject("ExitButton")
			

			self.text_name			= GetObject("CharacterDetailsInputNameText")
			self.text_level			= GetObject("CharacterDetailsInputLevelText")
			self.text_guild			= GetObject("CharacterDetailsInputGuildText")
			self.text_playtime		= GetObject("CharacterDetailsInputPlaytimeText")
			
			self.text_hp			= GetObject("CharacterDetailsInputHPText")
			self.text_int			= GetObject("CharacterDetailsInputINTText")
			self.text_str			= GetObject("CharacterDetailsInputSTRText")
			self.text_dex			= GetObject("CharacterDetailsInputDEXText")
			self.gauge_hp			= GetObject("HPGauge")
			self.gauge_int			= GetObject("INTGauge")
			self.gauge_str			= GetObject("STRGauge")
			self.gauge_dex			= GetObject("DEXGauge")

			# self.btn_left = GetObject("btn_left")
			# self.btn_right = GetObject("btn_right")

			self.left_window = GetObject("left_window")
			self.middle_window = GetObject("middle_window")
			self.right_window = GetObject("right_window")

		except:
			import exception
			exception.Abort("SelectCharacterWindow.LoadBoardDialog.BindObject")

		self.btn_start.SetEvent(ui.__mem_func__(self.StartGame))
		# self.btn_create.SetEvent(ui.__mem_func__(self.CreateCharacter))
		self.btn_close.SetEvent(ui.__mem_func__(self.ExitSelect))
		self.btn_delete.SetEvent(ui.__mem_func__(self.InputPrivateCode))

		self.dlgBoard.GetChild("CharacterSlotEmpty").SetEvent(ui.__mem_func__(self.CreateCharacter))
			
		# self.btn_left.SetEvent(ui.__mem_func__(self.changeSlot), -1)
		# self.btn_right.SetEvent(ui.__mem_func__(self.changeSlot), 1)

		self.chrRenderer = self.CharacterRenderer()
		self.chrRenderer.SetParent(self.middle_window)
		self.chrRenderer.Show()
		
		if constInfo.ENABLE_INTRO_ANIMATION == 1:
			self.CreateAnimateBackground()
			
		return 1
    
	def CreateAnimateBackground(self):
		self.AnimationImage = ui.AniImageBox()
		self.AnimationImage.SetParent(self.dlgBoard.GetChild("video_layer"))
		self.AnimationImage.SetDelay(2)
		for x in xrange(89):
			self.AnimationImage.AppendImageScale("d:/ymir work/ui/intro/animation/char_und_select/frame_%d.sub" % (x), float(wndMgr.GetScreenWidth()) / 1920.0, float(wndMgr.GetScreenHeight()) / 1080.0)
			self.AnimationImage.Show()
			
	def SameLoginDisconnect(self):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(localeInfo.LOGIN_FAILURE_SAMELOGIN, self.ExitSelect, localeInfo.UI_OK)
        #self.stream.popupWindow.Open(localeInfo.LOGIN_FAILURE_ALREAY, app.Exit, localeInfo.UI_OK)
        
	def MakeCharacter(self, index, id, name, race, form, hair, acce):
		if 0 == id:
			return

		chr.CreateInstance(index)
		chr.SelectInstance(index)
		chr.SetVirtualID(index)
		chr.SetNameString(name)

		chr.SetRace(race)
		chr.SetArmor(form)
		chr.SetHair(hair)
		#if weapon != 0:
			#chr.ChangeWeapon(weapon)
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			chr.SetAcce(acce)

		chr.Refresh()
		#if weapon == 0:
			#chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
			#chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)

		chr.SetRotation(0.0)

	## Manage Character
	def StartGame(self):

		if self.sendedChangeNamePacket:
			return

		if self.changeNameFlag:
			self.OpenChangeNameDialog()
			return

		if -1 != self.startIndex:
			return

		if musicInfo.selectMusic != "":
			snd.FadeLimitOutMusic("BGM/"+musicInfo.selectMusic, systemSetting.GetMusicVolume()*0.05)

		self.dlgQuestion.Hide()

		self.stream.SetCharacterSlot(self.slot)

		self.startIndex = self.slot
		self.startReservingTime = app.GetTime()

		chr.PushOnceMotion(chr.MOTION_INTRO_SELECTED, 0.1)

	def OpenChangeNameDialog(self):
		import uiCommon
		nameInputBoard = uiCommon.InputDialogWithDescription()
		nameInputBoard.SetTitle(localeInfo.SELECT_CHANGE_NAME_TITLE)
		nameInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputName))
		nameInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputName))
		nameInputBoard.SetMaxLength(chr.PLAYER_NAME_MAX_LEN)
		nameInputBoard.SetBoardWidth(200)
		nameInputBoard.SetDescription(localeInfo.SELECT_INPUT_CHANGING_NAME)
		nameInputBoard.Open()
		nameInputBoard.slot = self.slot
		self.nameInputBoard = nameInputBoard

	def OnChangeName(self, id, name):
		self.SelectSlot(id)
		self.sendedChangeNamePacket = FALSE
		self.PopupMessage(localeInfo.SELECT_CHANGED_NAME)

	def AcceptInputName(self):
		changeName = self.nameInputBoard.GetText()
		if not changeName:
			return

		self.sendedChangeNamePacket = TRUE
		net.SendChangeNamePacket(self.nameInputBoard.slot, changeName)
		return self.CancelInputName()

	def CancelInputName(self):
		self.nameInputBoard.Close()
		self.nameInputBoard = None
		return TRUE

	def OnCreateFailure(self, type):
		self.sendedChangeNamePacket = FALSE
		if 0 == type:
			self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_STRANGE_NAME)
		elif 1 == type:
			self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_ALREADY_EXIST_NAME)
		elif 100 == type:
			self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_STRANGE_INDEX)

	def CreateCharacter(self):
		#id = self.GetCharacterSlotID(self.slot)
		if 4 > self.active_characters:
			self.stream.SetCharacterSlot(self.active_characters)

			EMPIRE_MODE = 1

			if EMPIRE_MODE:
				if self.__AreAllSlotEmpty():
					self.stream.SetReselectEmpirePhase()
				else:
					self.stream.SetCreateCharacterPhase()

			else:
				self.stream.SetCreateCharacterPhase()

	def __AreAllSlotEmpty(self):
		for iSlot in xrange(self.SLOT_COUNT):
			if 0!=net.GetAccountCharacterSlotDataInteger(iSlot, net.ACCOUNT_CHARACTER_SLOT_ID):
				return 0
		return 1

	def PopupDeleteQuestion(self):
		id = self.GetCharacterSlotID(self.slot)
		if 0 == id:
			return

		self.dlgQuestion.Show()
		self.dlgQuestion.SetTop()

	def RequestDeleteCharacter(self):
		self.dlgQuestion.Hide()

		id = self.GetCharacterSlotID(self.slot)
		if 0 == id:
			self.PopupMessage(localeInfo.SELECT_EMPTY_SLOT)
			return

		net.SendDestroyCharacterPacket(self.slot, "1234567")
		self.PopupMessage(localeInfo.SELECT_DELEING)

	def InputPrivateCode(self):
		
		import uiCommon
		privateInputBoard = uiCommon.InputDialogWithDescription()
		privateInputBoard.SetTitle(localeInfo.INPUT_PRIVATE_CODE_DIALOG_TITLE)
		privateInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrivateCode))
		privateInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrivateCode))

		if ENABLE_ENGNUM_DELETE_CODE:
			pass
		else:
			privateInputBoard.SetNumberMode()

		privateInputBoard.SetSecretMode()
		privateInputBoard.SetMaxLength(7)
			
		privateInputBoard.SetBoardWidth(250)
		privateInputBoard.SetDescription(localeInfo.INPUT_PRIVATE_CODE_DIALOG_DESCRIPTION)
		privateInputBoard.Open()
		self.privateInputBoard = privateInputBoard

	def AcceptInputPrivateCode(self):
		privateCode = self.privateInputBoard.GetText()
		if not privateCode:
			return

		id = self.GetCharacterSlotID(self.slot)
		if 0 == id:
			self.PopupMessage(localeInfo.SELECT_EMPTY_SLOT)
			return

		net.SendDestroyCharacterPacket(self.slot, privateCode)
		self.PopupMessage(localeInfo.SELECT_DELEING)

		self.CancelInputPrivateCode()
		return TRUE

	def CancelInputPrivateCode(self):
		self.privateInputBoard = None
		return TRUE

	def OnDeleteSuccess(self, slot):
		self.PopupMessage(localeInfo.SELECT_DELETED)
		self.slot = slot
		self.SelectSlot(self.slot)
		self.Refresh()

	def OnDeleteFailure(self):
		self.PopupMessage(localeInfo.SELECT_CAN_NOT_DELETE)

	def ExitSelect(self):
		self.dlgQuestion.Hide()
	
		if LEAVE_BUTTON_FOR_POTAL:
			if app.loggined:
				self.stream.SetPhaseWindow(0)
			else:
				self.stream.setloginphase()
		else:
			self.stream.SetLoginPhase()

		self.Hide()

	def GetSlotIndex(self):
		return self.slot

	def changeSlot(self, value):
		self.slot = (self.slot + value) % 4
		if self.slot < 0:
			self.slot = 0
		self.SelectSlot(self.slot)

	def SelectSlot(self, index):
		if index < 0:
			return
		if index >= self.SLOT_COUNT:
			return

		chr.DeleteInstance(0)
		chr.DeleteInstance(1)
		chr.DeleteInstance(2)
		chr.DeleteInstance(3)

		self.slot = index
		self.rotation = 0.0
				
		chr.SelectInstance(self.slot)

		id=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_ID)
		if 0 != id:

			indexArray = (3, 2, 1, 0)
			for idx in indexArray:
				if self.characterSlotsDict.has_key(idx):
					if idx != self.slot:
						self.characterSlotsDict[idx].SetUp()
					else:
						self.characterSlotsDict[idx].Down()
				
			# self.btn_start.Show()
			# self.btn_delete.Show()
			# self.btn_create.Hide()

			self.right_window.Show()
			self.dlgBoard.GetChild("RotateLeftButton").Show()
			self.dlgBoard.GetChild("RotateRightButton").Show()
	
			name=net.GetAccountCharacterSlotDataString(self.slot, net.ACCOUNT_CHARACTER_SLOT_NAME)
			race=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_RACE)
			form=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_FORM)
			hair=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_HAIR)
			acce=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_ACCE)
			#weapon=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_WEAPON)
			
			playtime=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_PLAYTIME)
			level=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_LEVEL)
			guildname=net.GetAccountCharacterSlotDataString(self.slot, net.ACCOUNT_CHARACTER_SLOT_GUILD_NAME)
			
			
			hp=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_HTH)
			int=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_INT)
			st=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_STR)
			dex=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_DEX)
			
			self.text_name.SetText(name)
			self.text_level.SetText("Lv. %d" % level)
			self.text_guild.SetText(guildname)
			self.text_playtime.SetText(localeInfo.PlayerTimeTextIntroSel(playtime))
			self.text_hp.SetText(str(hp))
			self.text_int.SetText(str(int))
			self.text_str.SetText(str(st))
			self.text_dex.SetText(str(dex))
			self.gauge_hp.SetPercentage(hp, MAX_STATUS_POINTS)
			self.gauge_int.SetPercentage(int, MAX_STATUS_POINTS)
			self.gauge_str.SetPercentage(st, MAX_STATUS_POINTS)
			self.gauge_dex.SetPercentage(dex, MAX_STATUS_POINTS)
			
		if id:
			self.MakeCharacter(self.slot, id, name, race, form, hair, acce)
		else:
			self.InitCharacterBoard()

	def InitCharacterBoard(self):
		self.right_window.Hide()
		self.dlgBoard.GetChild("RotateLeftButton").Hide()
		self.dlgBoard.GetChild("RotateRightButton").Hide()
		# self.btn_start.Hide()
		# self.btn_delete.Hide()
		# self.btn_create.Show()
		# self.text_charactername.SetText("")
		# self.text_guild.SetText("")
		# self.text_playtime.SetText("")

	## Event
	def OnKeyDown(self, key):
		
		if 1 == key:
			self.ExitSelect()
		if 2 == key:
			self.SelectSlot(0)
		if 3 == key:
			self.SelectSlot(1)
		if 4 == key:
			self.SelectSlot(2)
		if 5 == key:
			self.SelectSlot(3)

		if 28 == key:

			id = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_ID)
			if 0 == id:
				self.CreateCharacter()

			else:
				self.StartGame()

		# if 203 == key:
			# self.changeSlot(-1)
		# if 205 == key:
			# self.changeSlot(1)

		if 30 == key:
			self.RotationProgress(1)
		
		if 32 == key:
			self.RotationProgress(2)
			
		return TRUE

	def RotationProgress(self, key = 0):
		if self.dlgBoard.GetChild("RotateLeftButton").IsDown():
			self.rotation -= ROTATE_SPEED
			chr.SetRotation(self.rotation)
			
		if self.dlgBoard.GetChild("RotateRightButton").IsDown():
			self.rotation += ROTATE_SPEED
			chr.SetRotation(self.rotation)
		
		if key == 1:
			self.rotation -= 45.0
			chr.SetRotation(self.rotation)
		
		if key == 2:
			self.rotation += 45.0
			chr.SetRotation(self.rotation)
		

	def OnUpdate(self):
		chr.Update()
		self.RotationProgress()
		for i in xrange(self.SLOT_COUNT):

			if FALSE == chr.HasInstance(i):
				continue

			chr.SelectInstance(i)
			
		chr.EffectUpdate()

		#######################################################
		if -1 != self.startIndex:

			## Temporary
			## BackGroundLoading?? ???? ??????? ??¡À?..
			if True:
				if FALSE == self.openLoadingFlag:
					chrSlot=self.stream.GetCharacterSlot()
					net.DirectEnter(chrSlot)
					self.openLoadingFlag = TRUE

					playTime=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_PLAYTIME)

					import player
					player.SetPlayTime(playTime)
					import chat
					chat.Clear() ## ????? Chat ?? ????. ??? Pos.
			## Temporary
		#######################################################

	def EmptyFunc(self):
		pass

	def PopupMessage(self, msg, func=0):
		if not func:
			func=self.EmptyFunc

		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)

	def OnPressExitKey(self):
		self.ExitSelect()
		return TRUE

