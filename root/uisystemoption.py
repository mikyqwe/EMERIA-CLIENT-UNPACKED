import dbg
import ui
import snd
import systemSetting
import net
import chat
import app
import localeInfo
import constInfo
import chrmgr
import player
import musicInfo
import grp

import uiSelectMusic
import background

MUSIC_FILENAME_MAX_LEN = 25

blockMode = 0

class OptionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load()
		self.RefreshHideMode()
		self.RefreshHideMode2()

		if app.ENABLE_DOG_MODE:
			self.RefreshDogMode()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		print " -------------------------------------- DELETE SYSTEM OPTION DIALOG"

	def __Initialize(self):
		self.tilingMode = 0
		self.titleBar = 0
		self.changeMusicButton = 0
		self.selectMusicFile = 0
		self.ctrlMusicVolume = 0
		self.ctrlSoundVolume = 0
		self.musicListDlg = 0
		self.tilingApplyButton = 0
		self.cameraModeButtonList = []
		self.fogModeButtonList = []
		self.tilingModeButtonList = []
		self.ctrlShadowQuality = 0
		self.hideModeButtonList = []
		self.hideMode2ButtonList = []
		if app.ENABLE_DOG_MODE:
			self.dogModeButtonList = []
		if app.ENABLE_FOV_OPTION:
			self.fovController = None
			self.fovResetButton = None
			self.fovValueText = None
		if app.__BL_GRAPHIC_ON_OFF__:
			self.effectOnOffButtonList = []
		#	self.privateshopOnOffButtonList = []
			self.itemdropOnOffButtonList = []
			self.petOnOffButtonList = []
			self.npcnameOnOffButtonList = []
			self.effectApplyButton = None
			#self.privateshopApplyButton = None
			self.itemdropApplyButton = None

	def Destroy(self):
		self.ClearDictionary()

		self.__Initialize()
		print " -------------------------------------- DESTROY SYSTEM OPTION DIALOG"

	def __Load_LoadScript(self, fileName):
		try:
			pyScriptLoader = ui.PythonScriptLoader()
			pyScriptLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("System.OptionDialog.__Load_LoadScript")

	def __Load_BindObject(self):
		try:
			GetObject = self.GetChild
			self.titleBar = GetObject("titlebar")
			self.selectMusicFile = GetObject("bgm_file")
			self.changeMusicButton = GetObject("bgm_button")
			self.ctrlMusicVolume = GetObject("music_volume_controller")
			self.ctrlSoundVolume = GetObject("sound_volume_controller")
			self.cameraModeButtonList.append(GetObject("camera_short"))
			self.cameraModeButtonList.append(GetObject("camera_long"))
			if app.ENABLE_DOG_MODE:
				self.dogModeButtonList.append(GetObject("dog_mode_open"))
				self.dogModeButtonList.append(GetObject("dog_mode_close"))
			self.fogModeButtonList.append(GetObject("fog_level0"))
			self.fogModeButtonList.append(GetObject("fog_level1"))
			self.fogModeButtonList.append(GetObject("fog_level2"))
			self.tilingModeButtonList.append(GetObject("tiling_cpu"))
			self.tilingModeButtonList.append(GetObject("tiling_gpu"))
			self.tilingApplyButton=GetObject("tiling_apply")
			for i in xrange(7):
				self.hideModeButtonList.append(GetObject("hidemode_%d" % i))
			for i in xrange(4):
				self.hideMode2ButtonList.append(GetObject("hide2mode_%d" % i))
				
			if app.__BL_GRAPHIC_ON_OFF__:
				for i in range(5):
					self.effectOnOffButtonList.append(GetObject("effect_level{}".format(i + 1)))
					#self.privateshopOnOffButtonList.append(GetObject("privateShop_level{}".format(i + 1)))
					self.itemdropOnOffButtonList.append(GetObject("dropItem_level{}".format(i + 1)))

				self.petOnOffButtonList.append(GetObject("pet_on"))
				self.petOnOffButtonList.append(GetObject("pet_off"))

				self.npcnameOnOffButtonList.append(GetObject("npcName_on"))
				self.npcnameOnOffButtonList.append(GetObject("npcName_off"))

				self.effectApplyButton = GetObject("effect_apply")
				#self.privateshopApplyButton = GetObject("privateShop_apply")
				self.itemdropApplyButton = GetObject("dropItem_apply")
			#self.ctrlShadowQuality = GetObject("shadow_bar")
			if app.ENABLE_FOV_OPTION:
				self.fovController = GetObject("fov_controller")
				self.fovController.SetButtonVisual("d:/ymir work/ui/game/windows/",\
					"sliderbar_cursor_button.tga",\
					"sliderbar_cursor_button.tga",\
					"sliderbar_cursor_button.tga")
				self.fovController.SetBackgroundVisual("d:/ymir work/ui/game/windows/sliderbar_small.tga")
				self.fovResetButton = GetObject("fov_reset_button")
				self.fovValueText = GetObject("fov_value_text")
		except:
			import exception
			exception.Abort("OptionDialog.__Load_BindObject")

	def __Load(self):
		self.__Load_LoadScript("uiscript/systemoptiondialog.py")
		self.__Load_BindObject()

		self.SetCenterPosition()

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

		self.ctrlMusicVolume.SetSliderPos(float(systemSetting.GetMusicVolume()))
		self.ctrlMusicVolume.SetEvent(ui.__mem_func__(self.OnChangeMusicVolume))

		self.ctrlSoundVolume.SetSliderPos(float(systemSetting.GetSoundVolume()) / 5.0)
		self.ctrlSoundVolume.SetEvent(ui.__mem_func__(self.OnChangeSoundVolume))

#		self.ctrlShadowQuality.SetSliderPos(float(systemSetting.GetShadowLevel()) / 5.0)
#		self.ctrlShadowQuality.SetEvent(ui.__mem_func__(self.OnChangeShadowQuality))

		if app.ENABLE_FOV_OPTION:
			if self.fovController:
				self.fovController.SetSliderPos(float(systemSetting.GetFOV()) / float(app.MAX_CAMERA_PERSPECTIVE))
				self.fovController.SetEvent(ui.__mem_func__(self.__OnChangeFOV))

			if self.fovValueText:
				self.fovValueText.SetText(str(int(systemSetting.GetFOV())))

			if self.fovResetButton:
				self.fovResetButton.SetEvent(ui.__mem_func__(self.__OnClickFOVResetButton))


		self.changeMusicButton.SAFE_SetEvent(self.__OnClickChangeMusicButton)

		self.cameraModeButtonList[0].SAFE_SetEvent(self.__OnClickCameraModeShortButton)
		self.cameraModeButtonList[1].SAFE_SetEvent(self.__OnClickCameraModeLongButton)

		if app.ENABLE_DOG_MODE:
			self.dogModeButtonList[0].SAFE_SetEvent(self.__OnClickDogButton)
			self.dogModeButtonList[1].SAFE_SetEvent(self.__OffClickDogButton)

		self.fogModeButtonList[0].SAFE_SetEvent(self.__OnClickFogModeLevel0Button)
		self.fogModeButtonList[1].SAFE_SetEvent(self.__OnClickFogModeLevel1Button)
		self.fogModeButtonList[2].SAFE_SetEvent(self.__OnClickFogModeLevel2Button)

		self.tilingModeButtonList[0].SAFE_SetEvent(self.__OnClickTilingModeCPUButton)
		self.tilingModeButtonList[1].SAFE_SetEvent(self.__OnClickTilingModeGPUButton)
		
		for i in xrange(7):
			self.hideModeButtonList[i].SetToggleUpEvent(self.__OnClickHideOptionUp, i)
			self.hideModeButtonList[i].SetToggleDownEvent(self.__OnClickHideOptionDown, i)
		for i in xrange(4):
			self.hideMode2ButtonList[i].SetToggleUpEvent(self.__OnClickHideOptionUp2, i)
			self.hideMode2ButtonList[i].SetToggleDownEvent(self.__OnClickHideOptionDown2, i)
		
		if app.__BL_GRAPHIC_ON_OFF__:
			for i, btn in enumerate(self.effectOnOffButtonList):
				btn.SAFE_SetEvent(self.__OnClickEffectOnOffButton, i)
			#for i, btn in enumerate(self.privateshopOnOffButtonList):
				#btn.SAFE_SetEvent(self.__OnClickPrivateShopOnOffButton, i)
			for i, btn in enumerate(self.itemdropOnOffButtonList):
				btn.SAFE_SetEvent(self.__OnClickItemDropOnOffButton, i)

			self.petOnOffButtonList[0].SAFE_SetEvent(self.__OnClickPetOnOffButton, 0)
			self.petOnOffButtonList[1].SAFE_SetEvent(self.__OnClickPetOnOffButton, 1)

			self.npcnameOnOffButtonList[0].SAFE_SetEvent(self.__OnClickNPCNameOnOffButton, 0)
			self.npcnameOnOffButtonList[1].SAFE_SetEvent(self.__OnClickNPCNameOnOffButton, 1)

			self.effectApplyButton.SAFE_SetEvent(self.__OnClickApplyEffectOnOffButton)
			#self.privateshopApplyButton.SAFE_SetEvent(self.__OnClickApplyPrivateShopOnOffButton)
			self.itemdropApplyButton.SAFE_SetEvent(self.__OnClickApplyItemDropOnOffButton)

			self.__ClickRadioButton(self.effectOnOffButtonList, grp.GetEffectOnOffLevel())
			#self.__ClickRadioButton(self.privateshopOnOffButtonList, grp.GetPrivateShopOnOffLevel())
			self.__ClickRadioButton(self.itemdropOnOffButtonList, grp.GetDropItemOnOffLevel())
			self.__ClickRadioButton(self.petOnOffButtonList, grp.GetPetOnOffStatus())
			self.__ClickRadioButton(self.npcnameOnOffButtonList, grp.GetNPCNameOnOffStatus())

		self.tilingApplyButton.SAFE_SetEvent(self.__OnClickTilingApplyButton)

		self.__SetCurTilingMode()

		self.__ClickRadioButton(self.fogModeButtonList, constInfo.GET_FOG_LEVEL_INDEX())
		self.__ClickRadioButton(self.cameraModeButtonList, constInfo.GET_CAMERA_MAX_DISTANCE_INDEX())

		if musicInfo.fieldMusic==musicInfo.METIN2THEMA:
			self.selectMusicFile.SetText(uiSelectMusic.DEFAULT_THEMA)
		else:
			self.selectMusicFile.SetText(musicInfo.fieldMusic[:MUSIC_FILENAME_MAX_LEN])

	def __OnClickTilingModeCPUButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_1)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_2)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_3)
		self.__SetTilingMode(0)

	def __OnClickTilingModeGPUButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_1)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_2)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_3)
		self.__SetTilingMode(1)

	def __OnClickTilingApplyButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_TILING_EXIT)
		if 0==self.tilingMode:
			background.EnableSoftwareTiling(1)
		else:
			background.EnableSoftwareTiling(0)

		net.ExitGame()

	def __OnClickChangeMusicButton(self):
		if not self.musicListDlg:

			self.musicListDlg=uiSelectMusic.FileListDialog()
			self.musicListDlg.SAFE_SetSelectEvent(self.__OnChangeMusic)

		self.musicListDlg.Open()


	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			selButton=buttonList[buttonIndex]
		except IndexError:
			return

		for eachButton in buttonList:
			eachButton.SetUp()

		selButton.Down()


	def __SetTilingMode(self, index):
		self.__ClickRadioButton(self.tilingModeButtonList, index)
		self.tilingMode=index

	def __SetCameraMode(self, index):
		constInfo.SET_CAMERA_MAX_DISTANCE_INDEX(index)
		self.__ClickRadioButton(self.cameraModeButtonList, index)

	def __SetFogLevel(self, index):
		constInfo.SET_FOG_LEVEL_INDEX(index)
		self.__ClickRadioButton(self.fogModeButtonList, index)

	def __OnClickCameraModeShortButton(self):
		self.__SetCameraMode(0)

	def __OnClickCameraModeLongButton(self):
		self.__SetCameraMode(1)

	def __OnClickFogModeLevel0Button(self):
		self.__SetFogLevel(0)

	def __OnClickFogModeLevel1Button(self):
		self.__SetFogLevel(1)

	def __OnClickFogModeLevel2Button(self):
		self.__SetFogLevel(2)

	if app.__BL_GRAPHIC_ON_OFF__:
		def __OnClickEffectOnOffButton(self, i):
			self.__ClickRadioButton(self.effectOnOffButtonList, i)

		#def __OnClickPrivateShopOnOffButton(self, i):
		#	self.__ClickRadioButton(self.privateshopOnOffButtonList, i)

		def __OnClickItemDropOnOffButton(self, i):
			self.__ClickRadioButton(self.itemdropOnOffButtonList, i)

		def __OnClickPetOnOffButton(self, i):
			self.__ClickRadioButton(self.petOnOffButtonList, i)
			grp.SetPetOnOffStatus(i)

		def __OnClickNPCNameOnOffButton(self, i):
			self.__ClickRadioButton(self.npcnameOnOffButtonList, i)
			grp.SetNPCNameOnOffStatus(i)

		def __OnClickApplyEffectOnOffButton(self):
			for i, btn in enumerate(self.effectOnOffButtonList):
				if btn.IsDown():
					grp.SetEffectOnOffLevel(i)
					break
		
		#def __OnClickApplyPrivateShopOnOffButton(self):
			#for i, btn in enumerate(self.privateshopOnOffButtonList):
			#	if btn.IsDown():
				#	grp.SetPrivateShopOnOffLevel(i)
				#	break

		def __OnClickApplyItemDropOnOffButton(self):
			for i, btn in enumerate(self.itemdropOnOffButtonList):
				if btn.IsDown():
					grp.SetDropItemOnOffLevel(i)
					break

	def __OnChangeMusic(self, fileName):
		self.selectMusicFile.SetText(fileName[:MUSIC_FILENAME_MAX_LEN])

		if musicInfo.fieldMusic != "":
			snd.FadeOutMusic("BGM/"+ musicInfo.fieldMusic)

		if fileName==uiSelectMusic.DEFAULT_THEMA:
			musicInfo.fieldMusic=musicInfo.METIN2THEMA
		else:
			musicInfo.fieldMusic=fileName

		musicInfo.SaveLastPlayFieldMusic()

		if musicInfo.fieldMusic != "":
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	if app.ENABLE_FOV_OPTION:
		def __OnChangeFOV(self):
			pos = self.fovController.GetSliderPos()
			systemSetting.SetFOV(pos * float(app.MAX_CAMERA_PERSPECTIVE))

			if self.fovValueText:
				self.fovValueText.SetText(str(int(systemSetting.GetFOV())))

		def __OnClickFOVResetButton(self):
			self.fovController.SetSliderPos(float(app.DEFAULT_CAMERA_PERSPECTIVE) / float(app.MAX_CAMERA_PERSPECTIVE))
			systemSetting.SetFOV(float(app.DEFAULT_CAMERA_PERSPECTIVE))

			if self.fovValueText:
				self.fovValueText.SetText(str(int(systemSetting.GetFOV())))

	def OnChangeMusicVolume(self):
		pos = self.ctrlMusicVolume.GetSliderPos()
		snd.SetMusicVolume(pos * net.GetFieldMusicVolume())
		systemSetting.SetMusicVolume(pos)

	def OnChangeSoundVolume(self):
		pos = self.ctrlSoundVolume.GetSliderPos()
		snd.SetSoundVolumef(pos)
		systemSetting.SetSoundVolumef(pos)

	def OnChangeShadowQuality(self):
		pos = self.ctrlShadowQuality.GetSliderPos()
		systemSetting.SetShadowLevel(int(pos / 0.2))

	def OnCloseInputDialog(self):
		self.inputDialog.Close()
		self.inputDialog = None
		return True

	def OnCloseQuestionDialog(self):
		self.questionDialog.Close()
		self.questionDialog = None
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Show(self):
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.__SetCurTilingMode()
		self.Hide()

	def __SetCurTilingMode(self):
		if background.IsSoftwareTiling():
			self.__SetTilingMode(0)
		else:
			self.__SetTilingMode(1)

	def __NotifyChatLine(self, text):
		chat.AppendChat(chat.CHAT_TYPE_INFO, text)

	def RefreshHideMode(self):
		(b1, b2, b3, b4, b5, b6, b7) = systemSetting.GetHideModeStatus()
		if b1:
			self.hideModeButtonList[0].Down()
		else:
			self.hideModeButtonList[0].SetUp()
		
		if b2:
			self.hideModeButtonList[1].Down()
		else:
			self.hideModeButtonList[1].SetUp()
		
		if b3:
			self.hideModeButtonList[2].Down()
		else:
			self.hideModeButtonList[2].SetUp()
		
		if b4:
			self.hideModeButtonList[3].Down()
		else:
			self.hideModeButtonList[3].SetUp()
		
		if b5:
			self.hideModeButtonList[4].Down()
			uiprivateshopbuilder.UpdateADBoard()
		else:
			self.hideModeButtonList[4].SetUp()
		
		if b6:
			self.hideModeButtonList[5].Down()
		else:
			self.hideModeButtonList[5].SetUp()
		
		if b7:
			self.hideModeButtonList[6].Down()
		else:
			self.hideModeButtonList[6].SetUp()

	def __OnClickHideOptionUp(self, arg):
		systemSetting.SetHideModeStatus(arg, 0)

	def __OnClickHideOptionDown(self, arg):
		systemSetting.SetHideModeStatus(arg, 1)
		if arg == 4:
			uiprivateshopbuilder.UpdateADBoard()

	def RefreshHideMode2(self):
		(b1, b2, b3, b4) = systemSetting.GetHideModeStatus2()
		if b1:
			self.hideMode2ButtonList[0].Down()
		else:
			self.hideMode2ButtonList[0].SetUp()
		
		if b2:
			self.hideMode2ButtonList[1].Down()
		else:
			self.hideMode2ButtonList[1].SetUp()
		
		if b3:
			self.hideMode2ButtonList[2].Down()
		else:
			self.hideMode2ButtonList[2].SetUp()
		
		if b4:
			self.hideMode2ButtonList[3].Down()
		else:
			self.hideMode2ButtonList[3].SetUp()

	def __OnClickHideOptionUp2(self, arg):
		systemSetting.SetHideModeStatus2(arg, 0)

	def __OnClickHideOptionDown2(self, arg):
		systemSetting.SetHideModeStatus2(arg, 1)
		
	if app.ENABLE_DOG_MODE:
		def __OnClickDogButton(self):
			systemSetting.SetDogMode(True)
			self.RefreshDogMode()

		def __OffClickDogButton(self):
			systemSetting.SetDogMode(False)
			self.RefreshDogMode()

		def RefreshDogMode(self):
			if systemSetting.GetDogMode():
				self.dogModeButtonList[0].Down()
				self.dogModeButtonList[1].SetUp()
			else:
				self.dogModeButtonList[0].SetUp()
				self.dogModeButtonList[1].Down()