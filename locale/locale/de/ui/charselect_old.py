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

import ui
import uiScriptLocale
import networkModule
import musicInfo
import playerSettingModule

####################################
# 빠른 실행을 위한 모듈 로딩 분담
####################################
import uiCommon
import uiMapNameShower
import uiAffectShower
import uiPlayerGauge
import uiCharacter
import uiTarget
import consoleModule

# interface module이 문제야...
import interfaceModule
import uiTaskBar
import uiInventory

###################################

LEAVE_BUTTON_FOR_POTAL = False
NOT_NEED_DELETE_CODE = False
ENABLE_ENGNUM_DELETE_CODE = False

if localeInfo.IsJAPAN():
	NOT_NEED_DELETE_CODE = True
elif localeInfo.IsHONGKONG():
	ENABLE_ENGNUM_DELETE_CODE = True
elif localeInfo.IsNEWCIBN() or localeInfo.IsCIBN10():
	ENABLE_ENGNUM_DELETE_CODE = True
elif localeInfo.IsEUROPE():
	ENABLE_ENGNUM_DELETE_CODE = True

###################################


	



class SelectCharacterWindow(ui.Window):
	
	class CharacterRenderer(ui.Window):
		def OnRender(self):
			grp.ClearDepthBuffer()
			grp.SetGameRenderState()
			grp.PushState()
			grp.SetOmniLight()
			
			screenWidth = wndMgr.GetScreenWidth()
			screenHeight = wndMgr.GetScreenHeight()
			newScreenWidth = float(screenWidth - 270)
			newScreenHeight = float(screenHeight)

			#Yakup ayar startIndex
			if screenHeight<601:
				grp.SetViewport(250.0/screenWidth, 0.0, newScreenWidth/screenWidth, 1.0)
			elif screenHeight>601 and screenHeight<801:
				grp.SetViewport(255.15/screenWidth, 0.0, newScreenWidth/screenWidth, 1.0)
			elif screenHeight>801 and screenHeight<1200:
				grp.SetViewport(270.15/screenWidth, 0.0, newScreenWidth/screenWidth, 1.0)
			else:
				grp.SetViewport(270.0/screenWidth, 0.0, newScreenWidth/screenWidth, 1.0)
			#Frozen ayar endIndex

			app.SetCenterPosition(0.0, 0.0, 0.0)
			
			app.SetCamera(1795.0, 15.0, 180.0, 120.0)
			#else if screenHeight>1200 and screenHeight<800;
				
			#app.SetCamera(500.0, 10.0, 180.0, 95.0)
			grp.SetPerspective(10.0, newScreenWidth/newScreenHeight, 1000.0, 3000.0)
			
			(x, y) = app.GetCursorPosition()
			grp.SetCursorPosition(x, y)
			chr.Deform()
			chr.Render()
			grp.RestoreViewport()
			grp.PopState()
			grp.SetInterfaceRenderState()
			
			
	# SLOT4
	#SLOT_ROTATION = ( 140.0, 260.0, 20.0 )
	#SLOT_COUNT = 3
	if app.ENABLE_PLAYER_PER_ACCOUNT5:
		SLOT_ROTATION = [135.0, 207.0, 279.0, 351.0, 63.0]
		SLOT_COUNT = 5
		# SLOT_ROTATION = [135.0, 180.0, 225.0, 270.0, 315.0, 360.0, 45.0, 90.0]
		# SLOT_COUNT = 8
		# SLOT_ROTATION = [135.0, 157.5, 180.0, 202.5, 225.0, 247.5, 270.0, 292.5, 315.0, 337.5, 360.0, 382.5, 45.0, 67.5, 90.0, 112.5]
		# SLOT_COUNT = 16
	else:
		SLOT_ROTATION = [135.0, 225.0, 315.0, 45.0]
		SLOT_COUNT = 4
	if app.ENABLE_WOLFMAN_CHARACTER:
		CHARACTER_TYPE_COUNT = 5
	else:
		CHARACTER_TYPE_COUNT = 4

	EMPIRE_NAME = {
		net.EMPIRE_A : localeInfo.EMPIRE_A,
		net.EMPIRE_B : localeInfo.EMPIRE_B,
		net.EMPIRE_C : localeInfo.EMPIRE_C
	}

	

	def __init__(self, stream):
		ui.Window.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_SELECT, self)

		self.stream=stream
		self.slot = self.stream.GetCharacterSlot()

		self.openLoadingFlag = False
		self.startIndex = -1
		self.startReservingTime = 0


		self.dlgBoard = 0
		self.changeNameFlag = False
		self.nameInputBoard = None
		self.sendedChangeNamePacket = False

		self.startIndex = -1
		self.isLoad = 0

	def __del__(self):
		ui.Window.__del__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_SELECT, 0)

	def Open(self):
		# if not self.__LoadBoardDialog(uiScriptLocale.LOCALE_UISCRIPT_PATH + "selectcharacterwindow.py"):
		if not self.__LoadBoardDialog("uiscript/selectcharacterwindow.py"):
			import dbg
			dbg.TraceError("SelectCharacterWindow.Open - __LoadScript Error")
			return

		if not self.__LoadQuestionDialog("uiscript/questiondialog.py"):
			return

		self.InitCharacterBoard()

		self.btnStart.Enable()
		self.btnCreate.Enable()
		self.btnDelete.Enable()
		self.btnExit.Enable()
		self.btnLeft.Enable()
		self.btnRight.Enable()

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

		self.character_rotation = 0.0
		
		
		
		self.SetFocus()
		app.ShowCursor()

	def Close(self):
		if musicInfo.selectMusic != "":
			snd.FadeOutMusic("BGM/"+musicInfo.selectMusic)

		self.stream.popupWindow.Close()

		if self.dlgBoard:
			self.dlgBoard.ClearDictionary()

		self.dlgBoard = None
		self.btnStart = None
		self.btnCreate = None
		self.btnDelete = None
		self.btnExit = None
		self.btnLeft = None
		self.btnRight = None
		self.backGround = None

		self.dlgQuestion.ClearDictionary()
		self.dlgQuestion = None
		self.dlgQuestionText = None
		self.dlgQuestionAcceptButton = None
		self.dlgQuestionCancelButton = None
		self.privateInputBoard = None
		self.nameInputBoard = None

		for i in xrange(self.SLOT_COUNT):
			chr.DeleteInstance(i)

		self.Hide()
		self.KillFocus()

		app.HideCursor()

	def Refresh(self):
		if not self.isLoad:
			return

		# SLOT4
		indexArray = range(self.SLOT_COUNT-1, -1, -1)
		for index in indexArray:
			id=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_ID)
			race=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_RACE)
			form=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_FORM)
			name=net.GetAccountCharacterSlotDataString(index, net.ACCOUNT_CHARACTER_SLOT_NAME)
			hair=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_HAIR)
			acce = 0
			if app.ENABLE_ACCE_COSTUME_SYSTEM:
				acce = net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_ACCE)

			if id:
				self.MakeCharacter(index, id, name, race, form, hair, acce)
				self.SelectSlot(index)

		self.SelectSlot(self.slot)
		self.__CharacterRotationLoop()

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

			self.btnStart		= GetObject("start_button")
			self.btnCreate		= GetObject("create_button")
			self.btnDelete		= GetObject("delete_button")
			self.btnExit		= GetObject("exit_button")

			self.CharacterName	= GetObject("character_name_value")
			self.PlayTime		= GetObject("character_play_time_value")
			

			self.btnLeft = GetObject("left_button")
			self.btnRight = GetObject("right_button")

			self.backGround = GetObject("BackGround")
			# self.backGround.Hide()

		except:
			import exception
			exception.Abort("SelectCharacterWindow.LoadBoardDialog.BindObject")


		self.btnStart.SetEvent(ui.__mem_func__(self.StartGame))
		self.btnCreate.SetEvent(ui.__mem_func__(self.CreateCharacter))
		self.btnExit.SetEvent(ui.__mem_func__(self.ExitSelect))



		if NOT_NEED_DELETE_CODE:
			self.btnDelete.SetEvent(ui.__mem_func__(self.PopupDeleteQuestion))
		else:
			self.btnDelete.SetEvent(ui.__mem_func__(self.InputPrivateCode))

		self.btnLeft.SetEvent(ui.__mem_func__(self.DecreaseSlotIndex))
		self.btnRight.SetEvent(ui.__mem_func__(self.IncreaseSlotIndex))

		self.chrRenderer = self.CharacterRenderer()
		self.chrRenderer.SetParent(self.backGround)
		self.chrRenderer.Show()

		return 1

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
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			chr.SetAcce(acce)

		chr.Refresh()
		chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
		chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)

		distance = 50.0
		rotRadian = 82.0
		
		x = distance*math.sin(rotRadian) + distance*math.cos(rotRadian)
		y = distance*math.cos(rotRadian) - distance*math.sin(rotRadian)
		
		chr.SetPixelPosition(int(x), int(y), 30)
		
		chr.SetRotation(0.0)
		chr.Hide()

	## Manage Character
	def StartGame(self):

		if net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_ID) == 0:
			self.PopupMessage(localeInfo.EMPTY_CHAR_SLOT_PLAY)
			return
	
		if self.sendedChangeNamePacket:
			return

		if self.changeNameFlag:
			self.OpenChangeNameDialog()
			return

		if -1 != self.startIndex:
			return

		if musicInfo.selectMusic != "":
			snd.FadeLimitOutMusic("BGM/"+musicInfo.selectMusic, systemSetting.GetMusicVolume()*0.05)

		self.btnStart.SetUp()
		self.btnCreate.SetUp()
		self.btnDelete.SetUp()
		self.btnExit.SetUp()
		self.btnLeft.SetUp()
		self.btnRight.SetUp()

		self.btnStart.Disable()
		self.btnCreate.Disable()
		self.btnDelete.Disable()
		self.btnExit.Disable()
		self.btnLeft.Disable()
		self.btnRight.Disable()
		self.dlgQuestion.Hide()

		self.stream.SetCharacterSlot(self.slot)

		self.startIndex = self.slot
		self.startReservingTime = app.GetTime()

		if chr.HasInstance(self.slot):
			chr.SelectInstance(self.slot)
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
		self.sendedChangeNamePacket = False
		self.PopupMessage(localeInfo.SELECT_CHANGED_NAME)

	def AcceptInputName(self):
		changeName = self.nameInputBoard.GetText()
		if not changeName:
			return

		self.sendedChangeNamePacket = True
		net.SendChangeNamePacket(self.nameInputBoard.slot, changeName)
		return self.CancelInputName()

	def CancelInputName(self):
		self.nameInputBoard.Close()
		self.nameInputBoard = None
		return True

	def OnCreateFailure(self, type):
		self.sendedChangeNamePacket = False
		if 0 == type:
			self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_STRANGE_NAME)
		elif 1 == type:
			self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_ALREADY_EXIST_NAME)
		elif 100 == type:
			self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_STRANGE_INDEX)

	def CreateCharacter(self):
		id = self.GetCharacterSlotID(self.slot)
		if 0==id:
			self.stream.SetCharacterSlot(self.slot)

			EMPIRE_MODE = 1

			if EMPIRE_MODE:
				if self.__AreAllSlotEmpty():
					self.stream.SetReselectEmpirePhase()
				else:
					self.stream.SetCreateCharacterPhase()

			else:
				self.stream.SetCreateCharacterPhase()
		else:
			self.PopupMessage(localeInfo.CHAR_SLOT_ALREADY_USED)

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
		return True

	def CancelInputPrivateCode(self):
		self.privateInputBoard = None
		return True

	def OnDeleteSuccess(self, slot):
		self.PopupMessage(localeInfo.SELECT_DELETED)
		self.DeleteCharacter(slot)

	def OnDeleteFailure(self):
		self.PopupMessage(localeInfo.SELECT_CAN_NOT_DELETE)

	def DeleteCharacter(self, index):
		chr.DeleteInstance(index)
		self.SelectSlot(self.slot)

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

	def DecreaseSlotIndex(self):
		slotIndex = (self.GetSlotIndex() - 1 + self.SLOT_COUNT) % self.SLOT_COUNT
		self.SelectSlot(slotIndex)

	def IncreaseSlotIndex(self):
		slotIndex = (self.GetSlotIndex() + 1) % self.SLOT_COUNT
		self.SelectSlot(slotIndex)

	def SelectSlot(self, index):
		self.character_rotation = 0.0
	
		if index < 0:
			return
		if index >= self.SLOT_COUNT:
			return

		self.slot = index

		chr.SelectInstance(self.slot)
		chr.Show()
		
		id=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_ID)
		if 0 != id:

			playTime=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_PLAYTIME)
			level=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_LEVEL)
			race=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_RACE)
			name=net.GetAccountCharacterSlotDataString(self.slot, net.ACCOUNT_CHARACTER_SLOT_NAME)
			guildID=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_GUILD_ID)
			self.changeNameFlag=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_CHANGE_NAME_FLAG)

			job = chr.RaceToJob(race)

			self.dlgBoard.GetChild("character_level_text").SetText("|cFF00FF00|H|h[%d]|cFF00FF00|H|h"%level)
			self.CharacterName.SetText(name)

			self.__UpdateNamePosition()
			
			self.PlayTime.SetText(str(playTime))
			self.__CharacterRotationLoop()

		else:

			self.InitCharacterBoard()
		
		for i in xrange(self.SLOT_COUNT):
			if i == self.slot or not chr.HasInstance(i):
				continue
			chr.SelectInstance(i)
			chr.Hide()

	def InitCharacterBoard(self):
		self.CharacterName.SetText("")
		self.dlgBoard.GetChild("character_level_text").SetText("")
		self.PlayTime.SetText("")

		
	def __UpdateNamePosition(self):
		GetObject=self.dlgBoard.GetChild
		level_txt = GetObject("character_level_text")
		
		name = self.CharacterName.GetText()
		level = level_txt.GetText()
		
		
		x_level,y_level = self.CharacterName.GetLocalPosition()
		
		x_level -= len(name) * 3
		x_level -= (len(level) - 28 ) * 6
		
		level_txt.SetPosition(x_level,y_level)
		
		# import dbg
		# dbg.TraceError("x %d , y %d  , text [%s]"%(x_level,y_level,level))
		
		
		
	## Event
	def OnKeyDown(self, key):

		if 1 == key:
			self.ExitSelect()
		for i in xrange(self.SLOT_COUNT):
			if 2+i == key:
				self.SelectSlot(i)

		if 28 == key:

			id = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_ID)
			if 0 == id:
				self.CreateCharacter()

			else:
				self.StartGame()

		if 203 == key:
			self.slot = (self.GetSlotIndex() - 1 + self.SLOT_COUNT) % self.SLOT_COUNT
			self.SelectSlot(self.slot)
		if 205 == key:
			self.slot = (self.GetSlotIndex() + 1) % self.SLOT_COUNT
			self.SelectSlot(self.slot)

		return True

	def OnUpdate(self):
		chr.Update()
		
		self.__CharacterRotationLoop()
		#######################################################
		if -1 != self.startIndex:

			## Temporary
			## BackGroundLoading이 지원 될때까지 임시로..
			if True:
				if False == self.openLoadingFlag:
					chrSlot=self.stream.GetCharacterSlot()
					net.DirectEnter(chrSlot)
					self.openLoadingFlag = True

					playTime=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_PLAYTIME)

					import player
					player.SetPlayTime(playTime)
					import chat
					chat.Clear() ## 들어갈때 Chat 을 초기화. 임시 Pos.
			## Temporary
		#######################################################
	
	
	
	
	def EmptyFunc(self):
		pass

		
	def __CharacterRotationLoop(self):
		if not chr.HasInstance(self.slot):
			return
		
		else:
			chr.SelectInstance(self.slot)
			self.character_rotation += 0.25
			
			if self.character_rotation > 360.0:
				self.character_rotation-= 360.0
			chr.SetRotation(self.character_rotation)
		
	def PopupMessage(self, msg, func=0):
		if not func:
			func=self.EmptyFunc

		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)

	def OnPressExitKey(self):
		self.ExitSelect()
		return True

