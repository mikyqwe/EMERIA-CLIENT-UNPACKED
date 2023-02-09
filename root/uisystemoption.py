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
import uiCommon

import uiSelectMusic
import background
from _weakref import proxy

MUSIC_FILENAME_MAX_LEN = 25

blockMode = 0

class OptionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load()

		if app.ENABLE_ENB_MODE:
			self.RefreshENBModeStatus()

		if app.ENABLE_ENB_MODE:
			self.questionDialog = None		

		if app.ENABLE_FOG_FIX:
			self.RefreshFogMode()
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
		if app.ENABLE_ENB_MODE:
			self.enbModeStatusButtonList = []
		self.ctrlShadowQuality = 0
		if app.ENABLE_FOV_OPTION:
			self.fovController = None
			self.fovResetButton = None
			self.fovValueText = None
		if app.ENABLE_DOG_MODE:
			self.dogModeButtonList = []
	def Destroy(self):
		self.ClearDictionary()

		self.__Initialize()
		print " -------------------------------------- DESTROY SYSTEM OPTION DIALOG"
		
	# if app.ENABLE_FPS:
		# self.fps = None
		# self.fpsInfo = None
		# self.currentSelectFPS = 0		

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
			if app.ENABLE_FOG_FIX:
				self.fogModeButtonList.append(GetObject("fog_on"))
				self.fogModeButtonList.append(GetObject("fog_off"))
			else:
				self.fogModeButtonList.append(GetObject("fog_level0"))
				self.fogModeButtonList.append(GetObject("fog_level1"))
				self.fogModeButtonList.append(GetObject("fog_level2"))
			self.tilingModeButtonList.append(GetObject("tiling_cpu"))
			self.tilingModeButtonList.append(GetObject("tiling_gpu"))
			self.tilingApplyButton=GetObject("tiling_apply")
			if app.ENABLE_ENB_MODE:
				self.enbModeStatusButtonList.append(GetObject("enbMode_on"))
				self.enbModeStatusButtonList.append(GetObject("enbMode_off"))
			self.ctrlShadowQuality = GetObject("shadow_bar")
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

		self.ctrlShadowQuality.SetSliderPos(float(systemSetting.GetShadowLevel()) / 5.0)
		self.ctrlShadowQuality.SetEvent(ui.__mem_func__(self.OnChangeShadowQuality))

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

		if app.ENABLE_FOG_FIX:
			self.fogModeButtonList[0].SAFE_SetEvent(self.__OnClickFogModeOn)
			self.fogModeButtonList[1].SAFE_SetEvent(self.__OnClickFogModeOff)
		else:
			self.fogModeButtonList[0].SAFE_SetEvent(self.__OnClickFogModeLevel0Button)
			self.fogModeButtonList[1].SAFE_SetEvent(self.__OnClickFogModeLevel1Button)
			self.fogModeButtonList[2].SAFE_SetEvent(self.__OnClickFogModeLevel2Button)

		self.tilingModeButtonList[0].SAFE_SetEvent(self.__OnClickTilingModeCPUButton)
		self.tilingModeButtonList[1].SAFE_SetEvent(self.__OnClickTilingModeGPUButton)

		if app.ENABLE_ENB_MODE:
			self.enbModeStatusButtonList[0].SAFE_SetEvent(self.__OnClickENBModeStatusButton, 1) # on
			self.enbModeStatusButtonList[1].SAFE_SetEvent(self.__OnClickENBModeStatusButton, 0) # off

		self.tilingApplyButton.SAFE_SetEvent(self.__OnClickTilingApplyButton)

		self.__SetCurTilingMode()

		if app.ENABLE_ENB_MODE:
			self.__ClickRadioButton(self.enbModeStatusButtonList, systemSetting.IsENBModeStatus())

		if not app.ENABLE_FOG_FIX:
			self.__ClickRadioButton(self.fogModeButtonList, constInfo.GET_FOG_LEVEL_INDEX())
		self.__ClickRadioButton(self.cameraModeButtonList, constInfo.GET_CAMERA_MAX_DISTANCE_INDEX())

		if musicInfo.fieldMusic==musicInfo.METIN2THEMA:
			self.selectMusicFile.SetText(uiSelectMusic.DEFAULT_THEMA)
		else:
			self.selectMusicFile.SetText(musicInfo.fieldMusic[:MUSIC_FILENAME_MAX_LEN])

		if app.ENABLE_FPS:
			self.GetChild("fps_change_btn").SetEvent(ui.__mem_func__(self.ChangeFPS))
			self.currentSelectFPS = systemSetting.GetFPS()
			systemSetting.SetFPS(systemSetting.GetFPS())
			self.fpsInfo = {
				0: "30 FPS - (PVM++)",
				1: "60 FPS - (PVM)",
				2: "90 FPS",
				3: "120 FPS",
				4: "144 FPS - (PVP)",
				5: "180 FPS",
				6: "220 FPS",
			}
			self.fps = ui.ComboBoxImage(self.GetChild("board"),"d:/ymir work/ui/pattern/select_image.tga",30,275)
			self.fps.SetCurrentItem(self.fpsInfo[self.currentSelectFPS])
			self.fps.SetParent(self.GetChild("board"))
			for index, data in self.fpsInfo.iteritems():
				self.fps.InsertItem(index, data)
			self.fps.SetEvent(lambda x, point=proxy(self): point.__ClickFPS(x))
			self.fps.Show()

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

		def __OnClickAutoHideModeOffButton(self):
			self.__ClickRadioButton(self.autoHideModeButtonList, 1)
			constInfo.AUTO_HIDE_OPTION = False

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

	if app.ENABLE_FPS:
		def __ClickFPS(self,fps):
			self.currentSelectFPS = fps
			self.fps.SetCurrentItem(self.fpsInfo[fps])
			self.fps.CloseListBox()
		def ChangeFPS(self):
			systemSetting.SetFPS(self.currentSelectFPS)


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

	def OnChangeMusicVolume(self):
		pos = self.ctrlMusicVolume.GetSliderPos()
		snd.SetMusicVolume(pos * net.GetFieldMusicVolume())
		systemSetting.SetMusicVolume(pos)

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


	if app.ENABLE_ENB_MODE:
		def __OnClickENBModeStatusButton(self, flag):
			self.__ClickRadioButton(self.enbModeStatusButtonList, flag)
			self.ConfirmENBSelect(flag)
			self.RefreshENBModeStatus()

		def RefreshENBModeStatus(self):
			if systemSetting.IsENBModeStatus():
				self.enbModeStatusButtonList[1].SetUp()
				self.enbModeStatusButtonList[0].Down()
			else:
				self.enbModeStatusButtonList[1].Down()
				self.enbModeStatusButtonList[0].SetUp()

		def ConfirmENBSelect(self, flag):
			questionDialog = uiCommon.QuestionDialog2()
			questionDialog.SetText1(localeInfo.RESTART_CLIENT_DO_YOU_ACCEPT_1)
			questionDialog.SetText2(localeInfo.RESTART_CLIENT_DO_YOU_ACCEPT_2)
			questionDialog.SetAcceptEvent(lambda arg = flag: self.OnAcceptENBQuestionDialog(arg))
			questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			questionDialog.SetWidth(450)
			questionDialog.Open()
			self.questionDialog = questionDialog

		def OnAcceptENBQuestionDialog(self, flag):
			self.OnCloseQuestionDialog()

			systemSetting.SetENBModeStatusFlag(flag)

			if flag == 1:
				value = 1
			else:
				value = 0

			idxCurMode = "EnableProxyLibrary=%d" % (value)
			f = []
			getLine = 2

			import os
			if os.path.exists("enbconvertor.ini"):
				idx = open("enbconvertor.ini", "r")

				for it in idx:
					f.append(it)
				# idx.close()

				while len(f) < int(getLine):
					f.append("")

				f[int(getLine)-1] = str(idxCurMode)
				idx = open("enbconvertor.ini", "w")

				for it in f:
					idx.write(it)
					if (len(it) > 0 and it[-1:] != "\n") or len(it) == 0:
						idx.write("\n")

				# idx.close()
			else:
				return

			app.Exit()

	def OnChangeSoundVolume(self):
		pos = self.ctrlSoundVolume.GetSliderPos()
		snd.SetSoundVolumef(pos)
		systemSetting.SetSoundVolumef(pos)

	def OnChangeShadowQuality(self):
		pos = self.ctrlShadowQuality.GetSliderPos()
		systemSetting.SetShadowLevel(int(pos / 0.2))

	if app.ENABLE_FOG_FIX:
		def __OnClickFogModeOn(self):
			systemSetting.SetFogMode(True)
			background.SetEnvironmentFog(True)
			self.RefreshFogMode()
			
		def __OnClickFogModeOff(self):
			systemSetting.SetFogMode(False)
			background.SetEnvironmentFog(False)
			self.RefreshFogMode()
			
		def RefreshFogMode(self):
			if systemSetting.IsFogMode():
				self.fogModeButtonList[0].Down()
				self.fogModeButtonList[1].SetUp()
			else:
				self.fogModeButtonList[0].SetUp()
				self.fogModeButtonList[1].Down()

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
		if app.ENABLE_ENB_MODE:
			if self.questionDialog:
				self.OnCloseQuestionDialog()

	def __SetCurTilingMode(self):
		if background.IsSoftwareTiling():
			self.__SetTilingMode(0)
		else:
			self.__SetTilingMode(1)

	def __NotifyChatLine(self, text):
		chat.AppendChat(chat.CHAT_TYPE_INFO, text)
		
	def LanguageButton(self):
		import multi
		MultiDialog = multi.MultiLanguage()
		MultiDialog.Show()
		self.Close()

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