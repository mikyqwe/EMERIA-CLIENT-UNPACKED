import chr
import grp
import app
import net
import snd
import wndMgr
import event
import systemSetting
import localeInfo
#localeInfo = _localeInfo.localeInfo()

import constInfo
import ui
import networkModule
import math
import snd
import musicInfo
import playerSettingModule
import uiScriptLocale
import uiToolTip

LOCALE_PATH = "uiscript/"+uiScriptLocale.CODEPAGE+"_"

MAN			= 0
WOMAN		= 1
SHAPE0		= 0
SHAPE1		= 1
PAGE_COUNT	= 2
SLOT_COUNT	= 4
BASE_CHR_ID	= 3

class CreateCharacterWindow(ui.Window):

	SLOT_ROTATION = [135.0, 225.0, 315.0, 45.0]

	current_slot = 0
	races = {
		0 : [0, "Warrior"],
		1 : [5, "Assassin"],
		2 : [2, "Sura"],
		3 : [7, "Shaman"],
		4 : [4, "Warrior"],
		5 : [1, "Assassin"],
		6 : [6, "Sura"],
		7 : [3, "Shaman"],
	}
	
	START_STAT =	(  ## CON INT STR DEX
						[ 4, 3, 6, 3, ], ## Warrior
						[ 3, 3, 4, 6, ], ## Assassin
						[ 3, 5, 5, 3, ], ## Sura
						[ 4, 6, 3, 3, ], ## Shaman
						[ 4, 3, 6, 3, ], ## Warrior
						[ 3, 3, 4, 6, ], ## Assassin
						[ 3, 5, 5, 3, ], ## Sura
						[ 4, 6, 3, 3, ], ## Shaman
					)

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

			grp.RestoreViewport()
			grp.PopState()
			grp.SetInterfaceRenderState()

	def __init__(self, stream):
		print "NEW CREATE WINDOW ----------------------------------------------------------------------------"
		ui.Window.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_CREATE, self)

		self.stream=stream

	def __del__(self):
		print "---------------------------------------------------------------------------- DELETE CREATE WINDOW"

		net.SetPhaseWindow(net.PHASE_WINDOW_CREATE, 0)
		ui.Window.__del__(self)

	def Open(self):
		print "OPEN CREATE WINDOW ----------------------------------------------------------------------------"

		# playerSettingModule.LoadGameData("INIT")

		self.reservingRaceIndex = -1
		self.reservingShapeIndex = -1
		self.reservingStartTime = 0
		self.stat = [0, 0, 0, 0]
	
		self.gender = 0
		self.shape = 0
		self.slot = -1
		self.shapeList = [
			[0, 0, 0, 0],
			[0, 0, 0, 0]]

		self.descIndex = 0

		try:
			dlgBoard = ui.ScriptWindow()
			pythonScriptLoader = ui.PythonScriptLoader()
			pythonScriptLoader.LoadScriptFile(dlgBoard, "uiscript/intro_charcreate.py")

		except:
			import exception
			exception.Abort("CreateCharacterWindow.Open.LoadObject")

		try:
			getChild = dlgBoard.GetChild

			self.btn_create = getChild("CreateCharacterButton")
			self.btn_close = getChild("ExitButton")
			# self.btn_left = getChild("btn_left")
			# self.btn_right = getChild("btn_right")
			# self.text_race = getChild("text_race")

			self.raceButtonList = []
			self.raceButtonList.append(getChild("CharacterWarrior"))
			self.raceButtonList.append(getChild("CharacterAssassin"))
			self.raceButtonList.append(getChild("CharacterSura"))
			self.raceButtonList.append(getChild("CharacterShaman"))

			self.genderButtonList = []
			self.genderButtonList.append(getChild("SelectGenre0"))
			self.genderButtonList.append(getChild("SelectGenre1"))

			self.shapeButtonList = []
			self.shapeButtonList.append(getChild("SelectSkin0"))
			self.shapeButtonList.append(getChild("SelectSkin1"))

			self.edit_charactername = getChild("InputName")

			self.window_content = getChild("middle_window")

		except:
			import exception
			exception.Abort("CreateCharacterWindow.Open.BindObject")

		self.dlgBoard = dlgBoard
		self.btn_create.SetEvent(ui.__mem_func__(self.CreateCharacter))
		self.btn_close.SetEvent(ui.__mem_func__(self.CancelCreate))
		# self.btn_left.SetEvent(ui.__mem_func__(self.__DecreaseSlotIndex))
		# self.btn_right.SetEvent(ui.__mem_func__(self.__IncreaseSlotIndex))

		self.raceButtonList[0].SetEvent(ui.__mem_func__(self.__SetCharacter), 0)
		self.raceButtonList[1].SetEvent(ui.__mem_func__(self.__SetCharacter), 1)
		self.raceButtonList[2].SetEvent(ui.__mem_func__(self.__SetCharacter), 2)
		self.raceButtonList[3].SetEvent(ui.__mem_func__(self.__SetCharacter), 3)

		self.genderButtonList[0].SetEvent(ui.__mem_func__(self.__SelectGender), MAN)
		self.genderButtonList[1].SetEvent(ui.__mem_func__(self.__SelectGender), WOMAN)

		self.shapeButtonList[0].SetEvent(ui.__mem_func__(self.__SelectShape), SHAPE0)
		self.shapeButtonList[1].SetEvent(ui.__mem_func__(self.__SelectShape), SHAPE1)
		
		
		self.edit_charactername.SetReturnEvent(ui.__mem_func__(self.CreateCharacter))
		self.edit_charactername.SetEscapeEvent(ui.__mem_func__(self.CancelCreate))

		self.chrRenderer = self.CharacterRenderer()
		self.chrRenderer.SetParent(self.window_content)
		self.chrRenderer.Show()

		self.edit_charactername.SetText("")

		self.EnableWindow()
		self.setCharacter()

		app.SetCamera(500.0, 10.0, 180.0, 95.0)

		self.__SelectGender(app.GetRandom(MAN, WOMAN))
		self.__SelectShape(0)
		self.current_slot = 0
		self.__SetCharacter(0)
		# self.setCharacter()

		self.dlgBoard.Show()
		self.Show()

		if musicInfo.createMusic != "":
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("BGM/"+musicInfo.createMusic)

		if constInfo.ENABLE_INTRO_ANIMATION == 1:
			self.CreateAnimateBackground()
			
		app.ShowCursor()

    
	def CreateAnimateBackground(self):
		self.AnimationImage = ui.AniImageBox()
		self.AnimationImage.SetParent(self.dlgBoard.GetChild("video_layer"))
		self.AnimationImage.SetDelay(2)
		for x in xrange(89):
			self.AnimationImage.AppendImageScale("d:/ymir work/ui/intro/animation/char_und_select/frame_%d.sub" % (x), float(wndMgr.GetScreenWidth()) / 1920.0, float(wndMgr.GetScreenHeight()) / 1080.0)
			self.AnimationImage.Show()
			
	def setCharacter(self):
		chr.DeleteInstance(0)
		chr.CreateInstance(0)
		chr.SelectInstance(0)
		chr.SetVirtualID(0)
		if(self.gender == MAN):
			chr.SetRace(self.races[self.current_slot][0])
		else:
			chr.SetRace(self.races[self.current_slot + 4][0])
		chr.SetArmor(0)
		chr.SetHair(0)
		chr.Refresh()
		chr.SetRotation(0.0)
		chr.Show()
		chr.ChangeShape(self.shape)
		chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
		chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)

	def Close(self):
		print "---------------------------------------------------------------------------- CLOSE CREATE WINDOW"

		self.edit_charactername.Enable()
		self.dlgBoard.ClearDictionary()
		self.stream=0
		self.shapeButtonList = []
		self.genderButtonList = []

		if musicInfo.createMusic != "":
			snd.FadeOutMusic("BGM/"+musicInfo.createMusic)

		for id in xrange(BASE_CHR_ID + SLOT_COUNT * PAGE_COUNT):
			chr.DeleteInstance(id)

		self.dlgBoard.Hide()
		self.Hide()

		app.HideCursor()
		event.Destroy()

	def EnableWindow(self):
		self.reservingRaceIndex = -1
		self.reservingShapeIndex = -1
		self.btn_create.Enable()
		self.btn_close.Enable()
		# self.btn_left.Enable()
		# self.btn_right.Enable()

		self.edit_charactername.SetFocus()
		self.edit_charactername.Enable()

		for page in xrange(PAGE_COUNT):
			for slot in xrange(SLOT_COUNT):
				chr_id = self.__GetSlotChrID(page, slot)
				chr.SelectInstance(chr_id)
				chr.BlendLoopMotion(chr.MOTION_INTRO_WAIT, 0.1)

	def DisableWindow(self):
		self.btn_create.Disable()
		self.btn_close.Disable()
		# self.btn_left.Disable()
		# self.btn_right.Disable()
		self.edit_charactername.Disable()

		self.btn_create.SetUp()

	## Manage Character
	def __GetSlotChrID(self, page, slot):
		return BASE_CHR_ID + page * SLOT_COUNT + slot

	def __MakeCharacter(self, page, slot, race):

		chr_id = self.__GetSlotChrID(page, slot)

		chr.CreateInstance(chr_id)
		chr.SelectInstance(chr_id)
		chr.SetVirtualID(chr_id)

		chr.SetRace(race)
		chr.SetArmor(0)
		chr.SetHair(0)

		chr.Refresh()
		chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
		chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)

		chr.SetRotation(0.0)
		chr.Hide()

	def __SelectGender(self, gender):		
		for button in self.genderButtonList:
			button.SetUp()

		self.genderButtonList[gender].Down()

		self.gender = gender
		self.setCharacter()

	def __SelectShape(self, shape):
		self.shapeList[self.gender][self.slot] = shape

		for button in self.shapeButtonList:
			button.SetUp()

		self.shapeButtonList[shape].Down()
		self.shape = shape
		self.setCharacter()

	def GetSlotIndex(self):
		return self.slot

	def __SelectSlot(self, slot):

		if slot < 0:
			return

		if slot >= SLOT_COUNT:
			return		

		if self.slot == slot:
			return

		self.slot = slot

		if self.IsShow():
			snd.PlaySound("sound/ui/click.wav")

	def CreateCharacter(self):

		if -1 != self.reservingRaceIndex:
			return

		textName = self.edit_charactername.GetText()
		if FALSE == self.__CheckCreateCharacter(textName):
			return

		if musicInfo.selectMusic != "":
			snd.FadeLimitOutMusic("BGM/"+musicInfo.selectMusic, systemSetting.GetMusicVolume()*0.05)

		self.DisableWindow()

		
		chr_id = self.__GetSlotChrID(self.gender, self.slot)

		chr.SelectInstance(chr_id)

		self.reservingRaceIndex = chr.GetRace()

		self.reservingShapeIndex = self.shapeList[self.gender][self.slot]
		self.reservingStartTime = app.GetTime()

		chr.PushOnceMotion(chr.MOTION_INTRO_SELECTED)

	def CancelCreate(self):
		self.stream.SetSelectCharacterPhase()


	def changeSlot(self, value):
		self.current_slot = (self.current_slot + value) % 4
		if self.current_slot < 0:
			self.current_slot = 3
		self.setCharacter()

	def __SetCharacter(self, value):
		for idx in xrange(4):
			if idx != value:
				self.raceButtonList[idx].SetUp()
			else:
				self.raceButtonList[idx].Down()

		self.current_slot = value
		self.setCharacter()

	def __DecreaseSlotIndex(self):
		self.changeSlot(-1)

	def __IncreaseSlotIndex(self):
		self.changeSlot(1)

	def PrevDescriptionPage(self):
		if TRUE == event.IsWait(self.descIndex):
			if event.GetVisibleStartLine(self.descIndex)-5 >= 0:
				event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex)-5)
				event.Skip(self.descIndex)
		else:
			event.Skip(self.descIndex)

	def NextDescriptionPage(self):
		if TRUE == event.IsWait(self.descIndex):
			event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex)+5)
			event.Skip(self.descIndex)
		else:
			event.Skip(self.descIndex)

	def __CheckCreateCharacter(self, name):
		if len(name) == 0:
			self.PopupMessage(localeInfo.CREATE_INPUT_NAME, self.EnableWindow)
			return FALSE

		if name.find(localeInfo.CREATE_GM_NAME)!=-1:
			self.PopupMessage(localeInfo.CREATE_ERROR_GM_NAME, self.EnableWindow)
			return FALSE

		if net.IsInsultIn(name):
			self.PopupMessage(localeInfo.CREATE_ERROR_INSULT_NAME, self.EnableWindow)
			return FALSE

		return TRUE

	## Event
	def OnCreateSuccess(self):
		self.stream.SetSelectCharacterPhase()

	def OnCreateFailure(self, type):
		if 1 == type:
			self.PopupMessage(localeInfo.CREATE_EXIST_SAME_NAME, self.EnableWindow)
		else:
			self.PopupMessage(localeInfo.CREATE_FAILURE, self.EnableWindow)

	def OnKeyDown(self, key):

		if key == 2:
			self.__SelectSlot(0)
		if key == 3:
			self.__SelectSlot(1)
		if key == 4:
			self.__SelectSlot(2)
		if key == 5:
			self.__SelectSlot(3)

		if 203 == key:
			self.__DecreaseSlotIndex()
		if 205 == key:
			self.__IncreaseSlotIndex()

		if 59 == key:
			self.__SelectGender(MAN_PAGE)
		if 60 == key:
			self.__SelectGender(WOMAN_PAGE)

		return TRUE

	def OnUpdate(self):
		chr.Update()

		###########################################################
		if -1 != self.reservingRaceIndex:
			if app.GetTime() - self.reservingStartTime >= 1.5:

				chrSlot=self.stream.GetCharacterSlot()
				textName = self.edit_charactername.GetText()
				raceIndex = self.reservingRaceIndex
				shapeIndex = self.reservingShapeIndex

				startStat = self.START_STAT[self.reservingRaceIndex]
				statCon = self.stat[0] - startStat[0]
				statInt = self.stat[1] - startStat[1]
				statStr = self.stat[2] - startStat[2]
				statDex = self.stat[3] - startStat[3]

				net.SendCreateCharacterPacket(chrSlot, textName, raceIndex, shapeIndex, statCon, statInt, statStr, statDex)

				self.reservingRaceIndex = -1

		###########################################################	

	def EmptyFunc(self):
		pass

	def PopupMessage(self, msg, func=0):
		if not func:
			func=self.EmptyFunc

		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)

	def OnPressExitKey(self):
		self.CancelCreate()
		return TRUE

	def OverInStatButton(self, stat):
		if not self.STAT_DESCRIPTION.has_key(stat):
			return

		self.toolTip.ClearToolTip()
		self.toolTip.AppendTextLine(self.STAT_DESCRIPTION[stat])
		self.toolTip.Show()

	def OverOutStatButton(self):
		self.toolTip.Hide()
