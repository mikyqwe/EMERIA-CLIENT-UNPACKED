import ui
import uiScriptLocale
import app
import net
import dbg
import snd
import player
import mouseModule
import wndMgr
import skill
import grp
import playerSettingModule
import quest
import localeInfo
import uiToolTip
import constInfo
import emotion
if app.ENABLE_NEW_DETAILS_GUI:
	import uiCharacterDetails
if app.ENABLE_QUEST_RENEWAL:
	import math, uiQuest
if app.ENABLE_SPECIAL_STATS_SYSTEM:
	import talenti
import chr
import playerLoad
SHOW_ONLY_ACTIVE_SKILL = FALSE
SHOW_LIMIT_SUPPORT_SKILL_LIST = []
HIDE_SUPPORT_SKILL_POINT = FALSE

if localeInfo.IsYMIR():
	SHOW_LIMIT_SUPPORT_SKILL_LIST = [121, 122, 123, 124, 126, 127, 129, 128, 131, 137, 138, 139, 140,141,142]
	if not localeInfo.IsCHEONMA():
		HIDE_SUPPORT_SKILL_POINT = TRUE 
		SHOW_LIMIT_SUPPORT_SKILL_LIST = [121, 122, 123, 124, 126, 127, 129, 128, 131, 137, 138, 139, 140,141,142]
elif localeInfo.IsJAPAN() or   (localeInfo.IsEUROPE() and app.GetLocalePath() != "locale/ca") and (localeInfo.IsEUROPE() and app.GetLocalePath() != "locale/br"):
	HIDE_SUPPORT_SKILL_POINT = TRUE	
	SHOW_LIMIT_SUPPORT_SKILL_LIST = [121, 122, 123, 124, 126, 127, 129, 128, 131, 137, 138, 139, 140]
else:
	HIDE_SUPPORT_SKILL_POINT = TRUE

FACE_IMAGE_DICT = {
	playerSettingModule.RACE_WARRIOR_M	: "icon/face/warrior_m.tga",
	playerSettingModule.RACE_WARRIOR_W	: "icon/face/warrior_w.tga",
	playerSettingModule.RACE_ASSASSIN_M	: "icon/face/assassin_m.tga",
	playerSettingModule.RACE_ASSASSIN_W	: "icon/face/assassin_w.tga",
	playerSettingModule.RACE_SURA_M		: "icon/face/sura_m.tga",
	playerSettingModule.RACE_SURA_W		: "icon/face/sura_w.tga",
	playerSettingModule.RACE_SHAMAN_M	: "icon/face/shaman_m.tga",
	playerSettingModule.RACE_SHAMAN_W	: "icon/face/shaman_w.tga",
}

if app.ENABLE_QUEST_RENEWAL:
	quest_slot_listbar = {
		"name" : "Quest_Slot",
		"type" : "listbar",

		"x" : 0,
		"y" : 0,

		"width" : 210,
		"height" : 20,

		"text" : "Quest title",
		"align" : "left",

		"horizontal_align" : "left",
		"vertical_align" : "left",
		"text_horizontal_align" : "left",
		"all_align" : "left",

		"text_height": 40
	}

	quest_lable_expend_img_path_dict = {
		0: "d:/ymir work/ui/quest_re/tabcolor_1_main.tga",
		1: "d:/ymir work/ui/quest_re/tabcolor_2_sub.tga",
		2: "d:/ymir work/ui/quest_re/tabcolor_3_levelup.tga",
		3: "d:/ymir work/ui/quest_re/tabcolor_4_event.tga",
		4: "d:/ymir work/ui/quest_re/tabcolor_5_collection.tga",
		5: "d:/ymir work/ui/quest_re/tabcolor_6_system.tga",
		6: "d:/ymir work/ui/quest_re/tabcolor_7_scroll.tga",
		7: "d:/ymir work/ui/quest_re/tabcolor_8_daily.tga"
	}

	quest_label_dict = {
		0 : localeInfo.QUEST_CATEGORY_00,
		1 : localeInfo.QUEST_CATEGORY_01,
		2 : localeInfo.QUEST_CATEGORY_02,
		3 : localeInfo.QUEST_CATEGORY_03,
		4 : localeInfo.QUEST_CATEGORY_04,
		5 : localeInfo.QUEST_CATEGORY_05,
		6 : localeInfo.QUEST_CATEGORY_06,
		7 : localeInfo.QUEST_CATEGORY_07,
	}

class CharacterWindow(ui.ScriptWindow):
	if app.ENABLE_NEW_DETAILS_GUI:
		chDetailsWnd = None
		isOpenedDetailsWnd = False

	ACTIVE_PAGE_SLOT_COUNT = 8
	SUPPORT_PAGE_SLOT_COUNT = 12

	PAGE_SLOT_COUNT = 12
	PAGE_HORSE = 2

	SKILL_GROUP_NAME_DICT = {
		playerSettingModule.JOB_WARRIOR	: { 1 : localeInfo.SKILL_GROUP_WARRIOR_1,	2 : localeInfo.SKILL_GROUP_WARRIOR_2, 	3 : localeInfo.SKILL_GROUP_PERKS, },
		playerSettingModule.JOB_ASSASSIN	: { 1 : localeInfo.SKILL_GROUP_ASSASSIN_1,	2 : localeInfo.SKILL_GROUP_ASSASSIN_2,	3 : localeInfo.SKILL_GROUP_PERKS, },
		playerSettingModule.JOB_SURA		: { 1 : localeInfo.SKILL_GROUP_SURA_1,		2 : localeInfo.SKILL_GROUP_SURA_2,		3 : localeInfo.SKILL_GROUP_PERKS, },
		playerSettingModule.JOB_SHAMAN		: { 1 : localeInfo.SKILL_GROUP_SHAMAN_1,	2 : localeInfo.SKILL_GROUP_SHAMAN_2,	3 : localeInfo.SKILL_GROUP_PERKS, },
	}

	STAT_DESCRIPTION =	{
		"HTH" : localeInfo.STAT_TOOLTIP_CON,
		"INT" : localeInfo.STAT_TOOLTIP_INT,
		"STR" : localeInfo.STAT_TOOLTIP_STR,
		"DEX" : localeInfo.STAT_TOOLTIP_DEX,
	}


	STAT_MINUS_DESCRIPTION = localeInfo.STAT_MINUS_DESCRIPTION
	if app.ENABLE_QUEST_RENEWAL:
		MAX_QUEST_PAGE_HEIGHT = 293.5
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		if app.ENABLE_QUEST_RENEWAL:
			self.isQuestCategoryLoad = False
		self.state = "STATUS"
		self.isLoaded = 0

		self.toolTipSkill = 0
				
		self.__Initialize()
		self.__LoadWindow()

		self.statusPlusCommandDict={
			"HTH" : "/stat_val ht ",
			"INT" : "/stat_val iq ",
			"STR" : "/stat_val st ",
			"DEX" : "/stat_val dx ",
		}

		self.statusMinusCommandDict={
			"HTH-" : "/stat- ht",
			"INT-" : "/stat- iq",
			"STR-" : "/stat- st",
			"DEX-" : "/stat- dx",
		}

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __Initialize(self):
		self.refreshToolTip = 0
		self.curSelectedSkillGroup = 0
		self.canUseHorseSkill = -1

		self.toolTip = None
		self.toolTipJob = None
		self.toolTipAlignment = None
		self.toolTipSkill = None

		self.faceImage = None
		self.statusPlusLabel = None
		self.statusPlusValue = None
		self.activeSlot = None
		self.tabDict = None
		self.tabButtonDict = None
		self.pageDict = None
		self.titleBarDict = None
		self.statusPlusButtonDict = None
		self.statusMinusButtonDict = None

		if app.ENABLE_NEW_DETAILS_GUI:
			self.ExpandBtn = None
			self.MinimizeBtn = None
			self.chDetailsWnd = None
			self.isOpenedDetailsWnd = False

		self.skillPageDict = None
		if app.ENABLE_QUEST_RENEWAL:
			self.questScrollBar = None
			self.questLastScrollPosition = 0
			self.questPage = None
			self.questTitleBar = None
			self.questSlotList = []
			self.questCategory = {}
			self.questCategoryList = []

			self.questColorList = {
				"green" : 0xFF83C055,
				"blue": 0xFF45678D,
				"golden": 0xFFCAB62F,
				"default_title": 0xFFCEC6B5
			}

			self.questOpenedCategories = []
			self.questMaxOpenedCategories = 1

			self.questClicked = []
			self.questIndexMap = {}
			self.questCounterList = []
			self.questClockList = []
			self.questSeparatorList = []

			self.displayY = 0
			self.baseCutY = 0
			self.questCategoryRenderPos = []

			self.questSlideWnd = {}
			self.questSlideWndNewKey = 0
		else:
			self.questShowingStartIndex = 0
			self.questScrollBar = None
			self.questSlot = None
			self.questNameList = None
			self.questLastTimeList = None
			self.questLastCountList = None
		self.skillGroupButton = ()
		self.skillGroupButtonP = ()

		self.activeSlot = None
		self.activeSkillPointValue = None
		self.supportSkillPointValue = None
		self.skillGroupButton1 = None
		self.skillGroupButton2 = None
		self.skillGroupButton3 = None
		self.skillGroupButtonP1 = None
		self.skillGroupButtonP2 = None
		self.skillGroupButtonP3 = None
		self.activeSkillGroupName = None

		self.guildNameSlot = None
		self.guildNameValue = None
		self.characterNameSlot = None
		self.characterNameValue = None

		self.emotionToolTip = None
		self.soloEmotionSlot = None
		self.dualEmotionSlot = None
		if app.ENABLE_EXPRESSING_EMOTION:
			self.specialEmotionSlot = None
			self.emotionTimeIdx = 0
			self.specialEmotionList = []
			self.specialEmotionListTime = {}
		
		if app.ENABLE_SPECIAL_STATS_SYSTEM:
			self.talentiSlotGrid = None
			self.talentiSlotGridInfo = None
			self.talentToolTip = None

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)

		if app.ENABLE_NEW_DETAILS_GUI:
			self.__InitCharacterDetailsUIButton()
			if self.chDetailsWnd and self.isOpenedDetailsWnd:
				self.chDetailsWnd.Show()

	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)	
		
	def __BindObject(self):
		self.toolTip = uiToolTip.ToolTip()
		self.toolTipJob = uiToolTip.ToolTip()
		self.toolTipAlignment = uiToolTip.ToolTip(130)		

		self.faceImage = self.GetChild("Face_Image")

		faceSlot=self.GetChild("Face_Slot")
		if 949 == app.GetDefaultCodePage():
			faceSlot.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowJobToolTip)
			faceSlot.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideJobToolTip)

		self.statusPlusLabel = self.GetChild("Status_Plus_Label")
		self.statusPlusValue = self.GetChild("Status_Plus_Value")		

		self.characterNameSlot = self.GetChild("Character_Name_Slot")			
		self.characterNameValue = self.GetChild("Character_Name")
		self.guildNameSlot = self.GetChild("Guild_Name_Slot")
		self.guildNameValue = self.GetChild("Guild_Name")
		self.characterNameSlot.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowAlignmentToolTip)
		self.characterNameSlot.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideAlignmentToolTip)

		self.activeSlot = self.GetChild("Skill_Active_Slot")
		self.activeSkillPointValue = self.GetChild("Active_Skill_Point_Value")
		self.supportSkillPointValue = self.GetChild("Support_Skill_Point_Value")
		self.skillGroupButton1 = self.GetChild("Skill_Group_Button_1")
		self.skillGroupButton2 = self.GetChild("Skill_Group_Button_2")
		self.skillGroupButton3 = self.GetChild("Skill_Group_Button_3")
		self.skillGroupButtonP1 = self.GetChild("Skill_Group_Button_1_P")
		self.skillGroupButtonP2 = self.GetChild("Skill_Group_Button_2_P")
		self.skillGroupButtonP3 = self.GetChild("Skill_Group_Button_3_P")
		self.activeSkillGroupName = self.GetChild("Active_Skill_Group_Name")
		if app.ENABLE_QUEST_RENEWAL:
			self.questScrollBar = self.GetChild("Quest_ScrollBar")
			self.questPage = self.GetChild("Quest_Page")
			self.questTitleBar = self.GetChild("Quest_TitleBar")
			self.quest_page_board_window = self.GetChild("quest_page_board_window")
			self.quest_object_board_window = self.GetChild("quest_object_board_window")		
				
		if app.ENABLE_SPECIAL_STATS_SYSTEM:
			self.tabDict = {
				"STATUS"	: self.GetChild("Tab_01"),
				"SKILL"		: self.GetChild("Tab_02"),
				"EMOTICON"	: self.GetChild("Tab_03"),
				"QUEST"		: self.GetChild("Tab_04"),
				# "TALENTI"	: self.GetChild("Tab_05"),
			}

			self.tabButtonDict = {
				"STATUS"	: self.GetChild("Tab_Button_01"),
				"SKILL"		: self.GetChild("Tab_Button_02"),
				"EMOTICON"	: self.GetChild("Tab_Button_03"),
				"QUEST"		: self.GetChild("Tab_Button_04"),
				# "TALENTI"	: self.GetChild("Tab_Button_05"),
			}

			self.pageDict = {
				"STATUS"	: self.GetChild("Character_Page"),
				"SKILL"		: self.GetChild("Skill_Page"),
				"EMOTICON"	: self.GetChild("Emoticon_Page"),
				"QUEST"		: self.GetChild("Quest_Page"),
				"TALENTI"	: self.GetChild("Talenti_Page"),
			}

			self.titleBarDict = {
				"STATUS"	: self.GetChild("Character_TitleBar"),
				"SKILL"		: self.GetChild("Skill_TitleBar"),
				"EMOTICON"	: self.GetChild("Emoticon_TitleBar"),
				"QUEST"		: self.GetChild("Quest_TitleBar"),
				"TALENTI"	: self.GetChild("Talenti_TitleBar"),
			}
		else:
			self.tabDict = {
				"STATUS"	: self.GetChild("Tab_01"),
				"SKILL"		: self.GetChild("Tab_02"),
				"EMOTICON"	: self.GetChild("Tab_03"),
				"QUEST"		: self.GetChild("Tab_04"),
			}

			self.tabButtonDict = {
				"STATUS"	: self.GetChild("Tab_Button_01"),
				"SKILL"		: self.GetChild("Tab_Button_02"),
				"EMOTICON"	: self.GetChild("Tab_Button_03"),
				"QUEST"		: self.GetChild("Tab_Button_04"),
			}

			self.pageDict = {
				"STATUS"	: self.GetChild("Character_Page"),
				"SKILL"		: self.GetChild("Skill_Page"),
				"EMOTICON"	: self.GetChild("Emoticon_Page"),
				"QUEST"		: self.GetChild("Quest_Page"),
			}

			self.titleBarDict = {
				"STATUS"	: self.GetChild("Character_TitleBar"),
				"SKILL"		: self.GetChild("Skill_TitleBar"),
				"EMOTICON"	: self.GetChild("Emoticon_TitleBar"),
				"QUEST"		: self.GetChild("Quest_TitleBar"),
			}

		self.statusPlusButtonDict = {
			"HTH"		: self.GetChild("HTH_Plus"),
			"INT"		: self.GetChild("INT_Plus"),
			"STR"		: self.GetChild("STR_Plus"),
			"DEX"		: self.GetChild("DEX_Plus"),
		}

		self.dunno = {
			"Vitalita"	: self.GetChild("HTH_Slot"),
			"Intelligenza"	: self.GetChild("INT_Slot"),
			"Forza"	: self.GetChild("STR_Slot"),
			"Destrezza"	: self.GetChild("DEX_Slot"),
		}

		self.statusMinusButtonDict = {
			"HTH-"		: self.GetChild("HTH_Minus"),
			"INT-"		: self.GetChild("INT_Minus"),
			"STR-"		: self.GetChild("STR_Minus"),
			"DEX-"		: self.GetChild("DEX_Minus"),
		}

		self.skillPageDict = {
			"ACTIVE" : self.GetChild("Skill_Active_Slot"),
			"SUPPORT" : self.GetChild("Skill_ETC_Slot"),
			"HORSE" : self.GetChild("Skill_Active_Slot"),
		}

		self.skillPageStatDict = {
			"SUPPORT"	: player.SKILL_SUPPORT,
			"ACTIVE"	: player.SKILL_ACTIVE,
			"HORSE"		: player.SKILL_HORSE,
		}

		self.skillGroupButton = (
			self.GetChild("Skill_Group_Button_1"),
			self.GetChild("Skill_Group_Button_2"),
			# self.GetChild("Skill_Group_Button_3"),
		)
		
		self.skillGroupButtonP = (
			self.GetChild("Skill_Group_Button_1_P"),
			self.GetChild("Skill_Group_Button_2_P"),
			# self.GetChild("Skill_Group_Button_3_P"),
		)

		
		
		if app.ENABLE_SPECIAL_STATS_SYSTEM:
			## Talenti
			self.talentiSlotGrid = self.GetChild("SkillTalentiSlot")
			self.talentiSlotGridInfo = self.GetChild("TalentiInfoSlot")
			self.talentiLongDescT = self.GetChild("talento_tld")
			self.talentiLongDesc = self.GetChild("talento_ld")
			self.talentiLongDescSlot = self.GetChild("TalentiInfoSlot")
			self.talentiPrevButton = self.GetChild("talenti_prev_button")
			self.talentiNextButton = self.GetChild("talenti_next_button")
			self.talentiLongDescIndex = 0
			
			self.__SetTalentiSlot()
			
			##End Talenti

		global SHOW_ONLY_ACTIVE_SKILL
		global HIDE_SUPPORT_SKILL_POINT
		if SHOW_ONLY_ACTIVE_SKILL or HIDE_SUPPORT_SKILL_POINT:	
			self.GetChild("Support_Skill_Point_Label").Hide()

		self.soloEmotionSlot = self.GetChild("SoloEmotionSlot")
		self.dualEmotionSlot = self.GetChild("DualEmotionSlot")
		if app.ENABLE_EXPRESSING_EMOTION:
			self.specialEmotionSlot = self.GetChild("SpecialEmotionSlot")
		self.__SetEmotionSlot()

		if app.ENABLE_QUEST_RENEWAL:
			self.questScrollBar.SetParent(self.quest_page_board_window)
			for i in xrange(quest.QUEST_CATEGORY_MAX_NUM):
				self.questCategory = ui.SubTitleBar()
				self.questCategory.SetParent(self.questPage)
				self.questCategory.MakeSubTitleBar(210, "red")
				self.questCategory.SetText(quest_label_dict[i])
				self.questCategory.SetSize(210, 16)
				self.questCategory.SetPosition(13, 0)
				self.questCategoryList.append(self.questCategory)

				self.questCategoryRenderPos.append(0)

			self.questScrollBar.SetParent(self.questPage)
			self.RearrangeQuestCategories(xrange(quest.QUEST_CATEGORY_MAX_NUM))
		else:
			self.questShowingStartIndex = 0
			self.questScrollBar = self.GetChild("Quest_ScrollBar")
			self.questScrollBar.SetScrollEvent(ui.__mem_func__(self.OnQuestScroll))
			self.questSlot = self.GetChild("Quest_Slot")
			for i in xrange(quest.QUEST_MAX_NUM):
				self.questSlot.HideSlotBaseImage(i)
				self.questSlot.SetCoverButton(i,\
					"d:/ymir work/ui/game/quest/slot_button_01.sub",\
					"d:/ymir work/ui/game/quest/slot_button_02.sub",\
					"d:/ymir work/ui/game/quest/slot_button_03.sub",\
					"d:/ymir work/ui/game/quest/slot_button_03.sub", True)

			self.questNameList = []
			self.questLastTimeList = []
			self.questLastCountList = []

			for i in xrange(quest.QUEST_MAX_NUM):
				self.questNameList.append(self.GetChild("Quest_Name_0" + str(i)))
				self.questLastTimeList.append(self.GetChild("Quest_LastTime_0" + str(i)))
				self.questLastCountList.append(self.GetChild("Quest_LastCount_0" + str(i)))

		if app.ENABLE_NEW_DETAILS_GUI:
			MainBoard = self.GetChild("board")
			self.ExpandBtn = ui.MakeButton(MainBoard, 240, 120, "", "d:/ymir work/ui/game/belt_inventory/", "btn_minimize_normal.tga", "btn_minimize_over.tga", "btn_minimize_down.tga")
			self.ExpandBtn.SetEvent(ui.__mem_func__(self.__ClickExpandButton))
			self.MinimizeBtn = ui.MakeButton(MainBoard, 240, 120, "", "d:/ymir work/ui/game/belt_inventory/", "btn_expand_normal.tga", "btn_expand_over.tga", "btn_expand_down.tga")
			self.MinimizeBtn.SetEvent(ui.__mem_func__(self.__ClickMinimizeButton))

		if app.ENABLE_ANTI_EXP:
			self.GetChild("AntiExp").SetEvent(ui.__mem_func__(self.__ClickAntiExp))

		self.skillGroupButton3.SetEvent(ui.__mem_func__(self.__ClickPerksButton))

		for i in xrange(len(self.skillGroupButtonP)):
			self.skillGroupButtonP[i].SetEvent(lambda arg=i: self.__SelectSkillGroup_P(arg))

	if app.ENABLE_ANTI_EXP:
		def __ClickAntiExp(self):
			net.SendChatPacket("/anti_exp")

	if app.ENABLE_SPECIAL_STATS_SYSTEM:
		def __SelectSkillGroup_P(self, arg):
			self.__SelectSkillGroup(arg)
			self.SetState("SKILL")

		def __ClickPerksButton(self):
			self.SetState("TALENTI")

			for btn in self.skillGroupButton:
				btn.SetUp()
			for btn_2 in self.skillGroupButtonP:
				btn_2.SetUp()
			self.skillGroupButton3.Down()
			self.skillGroupButtonP3.Down()
			self.curSelectedSkillGroup = 3

		def __SetTalentiSlot(self):
			
			self.talentToolTip = uiToolTip.SpecialStatsToolTip()
			
			slot = self.talentiSlotGrid
			slot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			slot.SetSelectItemSlotEvent(ui.__mem_func__(self.OnSelectTalento))
			slot.SetOverInItemEvent(ui.__mem_func__(self.__OverInSpecialStat))
			slot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutSpecialStat))
			slot.AppendSlotButton("d:/ymir work/ui/game/windows/btn_plus_up.sub",\
											"d:/ymir work/ui/game/windows/btn_plus_over.sub",\
											"d:/ymir work/ui/game/windows/btn_plus_down.sub")
												
			for slotIdx, datadict in talenti.SPECIALSTATS_DICT.items():
				slot.SetSpecialStatSlot(slotIdx, slotIdx)
				slot.SetSlotCountNew(slotIdx, 0, 0)
				slot.SetCoverButton(slotIdx)
				
				
			####Long Desc
			
			slot = self.talentiLongDescSlot
			slot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			
			self.talentiPrevButton.SetEvent(ui.__mem_func__(self.OnPrevTalentInfo))
			self.talentiNextButton.SetEvent(ui.__mem_func__(self.OnNextTalentInfo))
			
			self.UpdateTalentInfo(self.talentiLongDescIndex+1)
			
		

		def OnSelectTalento(self, slotIndex):
			self.talentiLongDescIndex = slotIndex-1
			self.UpdateTalentInfo(slotIndex)
		
		def UpdateTalentInfo(self, page):
			self.talentiLongDescT.SetText(talenti.SPECIALSTATS_DICT[page]["name"])
			self.talentiLongDesc.ClearAll()
			self.talentiLongDesc.SetText(talenti.SPECIALSTATS_DICT[page]["longdesc"])
			self.talentiLongDescSlot.ClearSlot(1)
			self.talentiLongDescSlot.SetSpecialStatSlot(1, page)
			self.talentiLongDescSlot.SetCoverButton(1)
		
		def OnNextTalentInfo(self):
			self.talentiLongDescIndex += 1
			nextPage = self.talentiLongDescIndex % 6
			self.UpdateTalentInfo(nextPage+1)
			
		def OnPrevTalentInfo(self):
			if(self.talentiLongDescIndex == 0):
				self.talentiLongDescIndex = 6
			self.talentiLongDescIndex -= 1
			prevPage = self.talentiLongDescIndex % 6
			self.UpdateTalentInfo(prevPage+1)
				
		def RefreshTalentSlot(self, slotIndex, level):
		
			self.talentToolTip.UpdateSkillLevel(slotIndex, level)
			
			slot = self.talentiSlotGrid
			slot.ClearSlot(slotIndex)
			slot.SetSpecialStatSlot(slotIndex, slotIndex)
			slot.SetSlotCountNew(slotIndex, 0, level)
			slot.SetCoverButton(slotIndex)
	
	
		def __OverInSpecialStat(self, slotIndex):
			if not slotIndex in talenti.SPECIALSTATS_DICT:
				return
				
			self.talentToolTip.ClearToolTip()
			self.talentToolTip.SetTitle(talenti.SPECIALSTATS_DICT[slotIndex]["name"])
			self.talentToolTip.AppendSkillLevel(slotIndex)
			
			talentoLevel = self.talentToolTip.GetStatLevel(slotIndex)
			
			self.talentToolTip.AppendSkillDesc((talenti.SPECIALSTATS_DICT[slotIndex]["desc"] % (talenti.getParamInfo(slotIndex, talentoLevel))))
			if talentoLevel < 10:
				self.talentToolTip.AppendSkillDesc((talenti.SPECIALSTATS_DICT[slotIndex]["desc"] % (talenti.getParamInfo(slotIndex, talentoLevel+1))), True)
			
			self.talentToolTip.AlignHorizonalCenter()
			self.talentToolTip.ShowToolTip()
		
		def __OverOutSpecialStat(self):
			if self.talentToolTip:
				self.talentToolTip.HideToolTip()
				

	def __SetSkillSlotEvent(self):
		for skillPageValue in self.skillPageDict.itervalues():
			skillPageValue.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			skillPageValue.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectSkill))
			skillPageValue.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
			skillPageValue.SetUnselectItemSlotEvent(ui.__mem_func__(self.ClickSkillSlot))
			skillPageValue.SetUseSlotEvent(ui.__mem_func__(self.ClickSkillSlot))
			skillPageValue.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			skillPageValue.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			skillPageValue.SetPressedSlotButtonEvent(ui.__mem_func__(self.OnPressedSlotButton))
			skillPageValue.AppendSlotButton("d:/ymir work/ui/game/windows/btn_plus_up.sub",\
											"d:/ymir work/ui/game/windows/btn_plus_over.sub",\
											"d:/ymir work/ui/game/windows/btn_plus_down.sub")

	if app.ENABLE_EXPRESSING_EMOTION:
		def RefreshEmotion(self):
			self.__SetEmotionSlot()

		def ClearEmotionsNew(self):
			self.specialEmotionList = []
			self.specialEmotionListTime = {}

			for i in xrange(app.SLOT_EMOTION_START,app.SLOT_EMOTION_END+1):
				self.specialEmotionSlot.ClearSlot(i)

		def AddEmotionsNew(self, id_emotion, time_emotion):
			self.specialEmotionList.append([id_emotion,time_emotion+app.GetGlobalTimeStamp()])

		def SetTime(self, time):
			time_collect = time - app.GetGlobalTimeStamp()

			if time_collect < 0:
				time_collect = 0

			return self.__FormatTime(time_collect)

		def __FormatTime(self, time):
			m, s = divmod(time, 60)
			h, m = divmod(m, 60)
			return "%1d:%02d:%02d" % (h, m, s)	

	def __SetEmotionSlot(self):

		self.emotionToolTip = uiToolTip.ToolTip()

		slots_new = None 

		if app.ENABLE_EXPRESSING_EMOTION:	
			slots_new = (self.soloEmotionSlot, self.dualEmotionSlot, self.specialEmotionSlot)
		else:
			slots_new = (self.soloEmotionSlot, self.dualEmotionSlot)

		for slot in slots_new:
			slot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			slot.SetSelectItemSlotEvent(ui.__mem_func__(self.__SelectEmotion))
			slot.SetUnselectItemSlotEvent(ui.__mem_func__(self.__ClickEmotionSlot))
			slot.SetUseSlotEvent(ui.__mem_func__(self.__ClickEmotionSlot))
			slot.SetOverInItemEvent(ui.__mem_func__(self.__OverInEmotion))
			slot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutEmotion))
			slot.AppendSlotButton("d:/ymir work/ui/game/windows/btn_plus_up.sub",\
											"d:/ymir work/ui/game/windows/btn_plus_over.sub",\
											"d:/ymir work/ui/game/windows/btn_plus_down.sub")

		for slotIdx, datadict in emotion.EMOTION_DICT.items():
			emotionIdx = slotIdx

			slot = self.soloEmotionSlot

			if app.ENABLE_EXPRESSING_EMOTION:	
				if slotIdx > 50 and slotIdx < 54:
					slot = self.dualEmotionSlot
			else:
				if slotIdx > 50:
					slot = self.dualEmotionSlot

			slot.SetEmotionSlot(slotIdx, emotionIdx)
			slot.SetCoverButton(slotIdx)

		if app.ENABLE_EXPRESSING_EMOTION:
			if len(self.specialEmotionList) > 0:
				for i in xrange(0,len(self.specialEmotionList)):
					slotIdx = app.SLOT_EMOTION_START+i #Slot
					emotionIdx = self.specialEmotionList[i][0] #Emotion

					if slotIdx >= app.SLOT_EMOTION_START:
						slot = self.specialEmotionSlot

					self.specialEmotionListTime[i] = self.specialEmotionList[i][1]

					slot.SetEmotionSlot(slotIdx, emotionIdx)
					slot.SetCoverButton(slotIdx)

	def __SelectEmotion(self, slotIndex):
		if not slotIndex in emotion.EMOTION_DICT:
			return

		if app.IsPressed(app.DIK_LCONTROL):
			player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_EMOTION, slotIndex)
			return

		mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_EMOTION, slotIndex, slotIndex)

	def __ClickEmotionSlot(self, slotIndex):
		print "click emotion"

		if app.ENABLE_EXPRESSING_EMOTION:
			if not slotIndex in emotion.EMOTION_DICT and slotIndex < app.SLOT_EMOTION_START:
				return
		else:
			if not slotIndex in emotion.EMOTION_DICT:
				return

		print "check acting"
		if player.IsActingEmotion():
			return

		if app.ENABLE_EXPRESSING_EMOTION:
			command = ""
			if slotIndex < app.SLOT_EMOTION_START:
				command = emotion.EMOTION_DICT[slotIndex]["command"]
			print "command", command

		else:
			command = emotion.EMOTION_DICT[slotIndex]["command"]
			print "command", command

		if app.ENABLE_EXPRESSING_EMOTION:
			if slotIndex > 50 and slotIndex < 54:
				vid = player.GetTargetVID()

				if 0 == vid or vid == player.GetMainCharacterIndex() or chr.IsNPC(vid) or chr.IsEnemy(vid):
					import chat
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.EMOTION_CHOOSE_ONE)
					return

				command += " " + chr.GetNameByVID(vid)
		else:
			if slotIndex > 50:
				vid = player.GetTargetVID()

				if 0 == vid or vid == player.GetMainCharacterIndex() or chr.IsNPC(vid) or chr.IsEnemy(vid):
					import chat
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.EMOTION_CHOOSE_ONE)
					return

				command += " " + chr.GetNameByVID(vid)

		if app.ENABLE_EXPRESSING_EMOTION:		
			if slotIndex >= app.SLOT_EMOTION_START:
				emotionIdx = self.specialEmotionList[slotIndex-app.SLOT_EMOTION_START][0] #Emotion

				if emotionIdx >= app.SLOT_EMOTION_START: #Emotion
					command = emotion.command_emotion[emotionIdx]["command"]			

				if emotionIdx > app.SLOT_EMOTION_START+4: #Emoticon
					command = int(emotion.command_emotion[emotionIdx]["command"])
					num = command+1

					import chrmgr
					if(chrmgr.IsPossibleEmoticon(-1)):				
						chrmgr.SetEmoticon(-1,int(num)-1)
						net.SendEmoticon(int(num)-1)

				else:
					print "send_command", command
					net.SendChatPacket(command)
			else:
				print "send_command", command
				net.SendChatPacket(command)
		else:
			print "send_command", command
			net.SendChatPacket(command)

	def ActEmotion(self, emotionIndex):
		self.__ClickEmotionSlot(emotionIndex)

	def __OverInEmotion(self, slotIndex):
		if self.emotionToolTip:

			if app.ENABLE_EXPRESSING_EMOTION:
				if not slotIndex in emotion.EMOTION_DICT and slotIndex < app.SLOT_EMOTION_START:
					return
			else:
				if not slotIndex in emotion.EMOTION_DICT:
					return


			self.emotionToolTip.ClearToolTip()

			if app.ENABLE_EXPRESSING_EMOTION:
				if slotIndex < app.SLOT_EMOTION_START:
					self.emotionToolTip.SetTitle(emotion.EMOTION_DICT[slotIndex]["name"])
				else:
					emotionIdx = self.specialEmotionList[slotIndex-app.SLOT_EMOTION_START][0] #Emotion
					self.emotionToolTip.SetTitle(emotion.command_emotion[emotionIdx]["name"])

				if slotIndex >= app.SLOT_EMOTION_START:
					self.emotionTimeIdx = self.specialEmotionListTime[slotIndex-app.SLOT_EMOTION_START] #Time
					self.emotionToolTip.AppendTextLine("%s"%self.emotionTimeIdx)
			else:
				self.emotionToolTip.SetTitle(emotion.EMOTION_DICT[slotIndex]["name"])

			self.emotionToolTip.AlignHorizonalCenter()
			self.emotionToolTip.ShowToolTip()

	def __OverOutEmotion(self):
		if self.emotionToolTip:
			self.emotionToolTip.HideToolTip()

	def __BindEvent(self):
		for i in xrange(len(self.skillGroupButton)):
			self.skillGroupButton[i].SetEvent(lambda arg=i: self.__SelectSkillGroup(arg))

		self.RefreshQuest()
		self.__HideJobToolTip()

		for (tabKey, tabButton) in self.tabButtonDict.items():
			tabButton.SetEvent(ui.__mem_func__(self.__OnClickTabButton), tabKey)

		for (statusPlusKey, statusPlusButton) in self.statusPlusButtonDict.items():
			statusPlusButton.SAFE_SetEvent(self.__OnClickStatusPlusButton, statusPlusKey)
			statusPlusButton.ShowToolTip = lambda arg=statusPlusKey: self.__OverInStatButton(arg)
			statusPlusButton.HideToolTip = lambda arg=statusPlusKey: self.__OverOutStatButton()

		for (statusTT, statusTTI) in self.dunno.items():
			statusTTI.OnMouseOverIn = lambda arg = statusTT: self.__OverInStatusTT(arg)
			statusTTI.OnMouseOverOut = lambda arg=statusTT: self.__OverOutStatusTT()

		for (statusMinusKey, statusMinusButton) in self.statusMinusButtonDict.items():
			statusMinusButton.SAFE_SetEvent(self.__OnClickStatusMinusButton, statusMinusKey)
			statusMinusButton.ShowToolTip = lambda arg=statusMinusKey: self.__OverInStatMinusButton(arg)
			statusMinusButton.HideToolTip = lambda arg=statusMinusKey: self.__OverOutStatMinusButton()

		for titleBarValue in self.titleBarDict.itervalues():
			titleBarValue.SetCloseEvent(ui.__mem_func__(self.Close))

		if app.ENABLE_QUEST_RENEWAL:
			self.questTitleBar.SetCloseEvent(ui.__mem_func__(self.Close))
			self.questScrollBar.SetScrollEvent(ui.__mem_func__(self.__OnScrollQuest))

			for i in xrange(quest.QUEST_CATEGORY_MAX_NUM):
				self.questCategoryList[i].SetEvent(ui.__mem_func__(self.__OnClickQuestCategoryButton), i)
		else:
			self.questSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.__SelectQuest))

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			if localeInfo.IsARABIC() or localeInfo.IsVIETNAM() or localeInfo.IsJAPAN():
				self.__LoadScript(uiScriptLocale.LOCALE_UISCRIPT_PATH + "CharacterWindow.py")
			else:
				self.__LoadScript("UIScript/CharacterWindow.py")
				
			self.__BindObject()
			self.__BindEvent()
		except:
			import exception
			exception.Abort("CharacterWindow.__LoadWindow")

		#self.tabButtonDict["EMOTICON"].Disable()
		self.SetState("STATUS")

	def Destroy(self):
		self.ClearDictionary()
		self.Close()
		self.__Initialize()
		if app.ENABLE_NEW_DETAILS_GUI:
			if self.chDetailsWnd:
				self.ExpandBtn = None
				self.MinimizeBtn = None
				self.chDetailsWnd.Destroy()
				self.chDetailsWnd=None

	def Close(self):
		if app.ENABLE_NEW_DETAILS_GUI:
			if self.chDetailsWnd:
				self.isOpenedDetailsWnd = self.chDetailsWnd.IsShow()
				self.chDetailsWnd.Close()
		if self.toolTipSkill != None:
			self.toolTipSkill.Hide()
		if app.ENABLE_QUEST_RENEWAL:
			if self.questSlideWndNewKey > 0:
				if self.questSlideWnd[self.questSlideWndNewKey-1] is not None:
					self.questSlideWnd[self.questSlideWndNewKey-1].CloseSelf()
		self.Hide()

	def SetSkillToolTip(self, toolTipSkill):
		self.toolTipSkill = toolTipSkill

	def __OnClickStatusPlusButton(self, statusKey):
		cmd = self.statusPlusCommandDict[statusKey]

		if app.IsPressed(app.DIK_LCONTROL):
			cmd = cmd + "10"
		else:
			cmd = cmd + "1"
			
		net.SendChatPacket(cmd)

	def __OnClickStatusMinusButton(self, statusKey):
		try:
			statusMinusCommand=self.statusMinusCommandDict[statusKey]
			net.SendChatPacket(statusMinusCommand)
		except KeyError, msg:
			dbg.TraceError("CharacterWindow.__OnClickStatusMinusButton KeyError: %s", msg)


	def __OnClickTabButton(self, stateKey):
		self.SetState(stateKey)

	def SetState(self, stateKey):
		if self.curSelectedSkillGroup == 3 and stateKey == "SKILL":
			stateKey = "TALENTI"
		self.state = stateKey
		if app.ENABLE_QUEST_RENEWAL:
			if stateKey != "QUEST":
				self.questPage.Hide()
				if self.questSlideWndNewKey > 0:
					if self.questSlideWnd[self.questSlideWndNewKey-1] is not None:
						self.questSlideWnd[self.questSlideWndNewKey-1].CloseSelf()
			else:
				self.__LoadQuestCategory()

		if stateKey == "TALENTI":
			for (tabKey, tabButton) in self.tabButtonDict.items():
				if "SKILL"!=tabKey:
					tabButton.SetUp()
		else:
			for (tabKey, tabButton) in self.tabButtonDict.items():
				if stateKey!=tabKey:
					tabButton.SetUp()


		# if stateKey != "TALENTI":
		for tabValue in self.tabDict.itervalues():
			tabValue.Hide()

		for pageValue in self.pageDict.itervalues():
			pageValue.Hide()

		for titleBarValue in self.titleBarDict.itervalues():
			titleBarValue.Hide()

		if stateKey == "TALENTI":
			self.tabDict["SKILL"].Show()
		else:
			self.tabDict[stateKey].Show()

		self.pageDict[stateKey].Show()
		self.titleBarDict[stateKey].Show()
		

	def GetState(self):
		return self.state

	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			if self.GetState() == "STATUS":
				self.SetState("SKILL")
			elif self.GetState() == "SKILL":
				self.SetState("EMOTICON")
			elif self.GetState() == "EMOTICON":
				self.SetState("QUEST")
		else:
			if self.GetState() == "SKILL":
				self.SetState("STATUS")
			elif self.GetState() == "EMOTICON":
				self.SetState("SKILL")
			elif self.GetState() == "QUEST":
				self.SetState("EMOTICON")

	def __GetTotalAtkText(self):
		minAtk=player.GetStatus(player.ATT_MIN)
		maxAtk=player.GetStatus(player.ATT_MAX)
		atkBonus=player.GetStatus(player.ATT_BONUS)
		attackerBonus=player.GetStatus(player.ATTACKER_BONUS)

		if minAtk==maxAtk:
			return "%d" % (minAtk+atkBonus+attackerBonus)
		else:
			return "%d-%d" % (minAtk+atkBonus+attackerBonus, maxAtk+atkBonus+attackerBonus)

	def __GetTotalMagAtkText(self):
		minMagAtk=player.GetStatus(player.MAG_ATT)+player.GetStatus(player.MIN_MAGIC_WEP)
		maxMagAtk=player.GetStatus(player.MAG_ATT)+player.GetStatus(player.MAX_MAGIC_WEP)

		if minMagAtk==maxMagAtk:
			return "%d" % (minMagAtk)
		else:
			return "%d-%d" % (minMagAtk, maxMagAtk)

	def __GetTotalDefText(self):
		defValue=player.GetStatus(player.DEF_GRADE)
		if constInfo.ADD_DEF_BONUS_ENABLE:
			defValue+=player.GetStatus(player.DEF_BONUS)
		return "%d" % (defValue)

	def RefreshStatus(self):
		if self.isLoaded==0:
			return

		try:
			self.GetChild("Level_Value").SetText(str(player.GetStatus(player.LEVEL)))
			self.GetChild("Exp_Value").SetText(str(player.GetEXP()))
			self.GetChild("RestExp_Value").SetText(str(player.GetStatus(player.NEXT_EXP) - player.GetStatus(player.EXP)))
			self.GetChild("HP_Value").SetText(str(player.GetStatus(player.HP)) + '/' + str(player.GetStatus(player.MAX_HP)))
			self.GetChild("SP_Value").SetText(str(player.GetStatus(player.SP)) + '/' + str(player.GetStatus(player.MAX_SP)))

			self.GetChild("STR_Value").SetText(str(player.GetStatus(player.ST)))
			self.GetChild("DEX_Value").SetText(str(player.GetStatus(player.DX)))
			self.GetChild("HTH_Value").SetText(str(player.GetStatus(player.HT)))
			self.GetChild("INT_Value").SetText(str(player.GetStatus(player.IQ)))

			self.GetChild("ATT_Value").SetText(self.__GetTotalAtkText())
			self.GetChild("DEF_Value").SetText(self.__GetTotalDefText())

			self.GetChild("MATT_Value").SetText(self.__GetTotalMagAtkText())
			#self.GetChild("MATT_Value").SetText(str(player.GetStatus(player.MAG_ATT)))

			self.GetChild("MDEF_Value").SetText(str(player.GetStatus(player.MAG_DEF)))
			self.GetChild("ASPD_Value").SetText(str(player.GetStatus(player.ATT_SPEED)))
			self.GetChild("MSPD_Value").SetText(str(player.GetStatus(player.MOVING_SPEED)))
			self.GetChild("CSPD_Value").SetText(str(player.GetStatus(player.CASTING_SPEED)))
			self.GetChild("ER_Value").SetText(str(player.GetStatus(player.EVADE_RATE)))

		except:
			#import exception
			#exception.Abort("CharacterWindow.RefreshStatus.BindObject")
			## ������ ƨ�� ����
			pass

		self.__RefreshStatusPlusButtonList()
		self.__RefreshStatusMinusButtonList()
		self.RefreshAlignment()

		if self.refreshToolTip:
			self.refreshToolTip()

		if app.ENABLE_NEW_DETAILS_GUI:
			if self.chDetailsWnd:
				if self.chDetailsWnd.IsShow():
					self.chDetailsWnd.Refresh()

	def __RefreshStatusPlusButtonList(self):
		if self.isLoaded==0:
			return

		statusPlusPoint=player.GetStatus(player.STAT)

		if statusPlusPoint>0:
			self.statusPlusValue.SetText(str(statusPlusPoint))
			self.statusPlusLabel.Show()
			self.ShowStatusPlusButtonList()
		else:
			self.statusPlusValue.SetText(str(0))
			self.statusPlusLabel.Hide()
			self.HideStatusPlusButtonList()

	def __RefreshStatusMinusButtonList(self):
		if self.isLoaded==0:
			return

		statusMinusPoint=self.__GetStatMinusPoint()

		if statusMinusPoint>0:
			self.__ShowStatusMinusButtonList()
		else:
			self.__HideStatusMinusButtonList()

	def RefreshAlignment(self):
		point, grade = player.GetAlignmentData()

		import colorInfo
		COLOR_DICT = {	0 : colorInfo.TITLE_RGB_GOOD_4,
						1 : colorInfo.TITLE_RGB_GOOD_3,
						2 : colorInfo.TITLE_RGB_GOOD_2,
						3 : colorInfo.TITLE_RGB_GOOD_1,
						4 : colorInfo.TITLE_RGB_NORMAL,
						5 : colorInfo.TITLE_RGB_EVIL_1,
						6 : colorInfo.TITLE_RGB_EVIL_2,
						7 : colorInfo.TITLE_RGB_EVIL_3,
						8 : colorInfo.TITLE_RGB_EVIL_4, }
		colorList = COLOR_DICT.get(grade, colorInfo.TITLE_RGB_NORMAL)
		gradeColor = ui.GenerateColor(colorList[0], colorList[1], colorList[2])

		self.toolTipAlignment.ClearToolTip()
		self.toolTipAlignment.AutoAppendTextLine(localeInfo.TITLE_NAME_LIST[grade], gradeColor)
		self.toolTipAlignment.AutoAppendTextLine(localeInfo.ALIGNMENT_NAME + str(point))
		self.toolTipAlignment.AlignHorizonalCenter()

	def __ShowStatusMinusButtonList(self):
		for (stateMinusKey, statusMinusButton) in self.statusMinusButtonDict.items():
			statusMinusButton.Show()

	def __HideStatusMinusButtonList(self):
		for (stateMinusKey, statusMinusButton) in self.statusMinusButtonDict.items():
			statusMinusButton.Hide()

	def ShowStatusPlusButtonList(self):
		for (statePlusKey, statusPlusButton) in self.statusPlusButtonDict.items():
			statusPlusButton.Show()

	def HideStatusPlusButtonList(self):
		for (statePlusKey, statusPlusButton) in self.statusPlusButtonDict.items():
			statusPlusButton.Hide()

	def ShowStatusHizliPlusButtonList(self):
		for (statePlusKey, statusHizliPlusButton) in self.statusHizliPlusButtonDict.items():
			statusHizliPlusButton.Show()

	def HideStatusHizliPlusButtonList(self):
		for (statePlusKey, statusHizliPlusButton) in self.statusHizliPlusButtonDict.items():
			statusHizliPlusButton.Hide()

	def SelectSkill(self, skillSlotIndex):

		mouseController = mouseModule.mouseController

		if FALSE == mouseController.isAttached():

			srcSlotIndex = self.__RealSkillSlotToSourceSlot(skillSlotIndex)
			selectedSkillIndex = player.GetSkillIndex(srcSlotIndex)

			if skill.CanUseSkill(selectedSkillIndex):

				if app.IsPressed(app.DIK_LCONTROL):

					player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_SKILL, srcSlotIndex)
					return

				mouseController.AttachObject(self, player.SLOT_TYPE_SKILL, srcSlotIndex, selectedSkillIndex)

		else:

			mouseController.DeattachObject()

	def SelectEmptySlot(self, SlotIndex):
		mouseModule.mouseController.DeattachObject()

	## ToolTip
	def OverInItem(self, slotNumber):

		if mouseModule.mouseController.isAttached():
			return

		if 0 == self.toolTipSkill:
			return

		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotNumber)
		skillIndex = player.GetSkillIndex(srcSlotIndex)
		skillLevel = player.GetSkillLevel(srcSlotIndex)
		skillGrade = player.GetSkillGrade(srcSlotIndex)
		skillType = skill.GetSkillType(skillIndex)

		## ACTIVE
		if skill.SKILL_TYPE_ACTIVE == skillType:
			overInSkillGrade = self.__GetSkillGradeFromSlot(slotNumber)

			if overInSkillGrade == skill.SKILL_GRADE_COUNT-1 and skillGrade == skill.SKILL_GRADE_COUNT:
				self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, skillGrade, skillLevel)
			elif overInSkillGrade == skillGrade:
				self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, overInSkillGrade, skillLevel)
			else:
				self.toolTipSkill.SetSkillOnlyName(srcSlotIndex, skillIndex, overInSkillGrade)

		else:
			self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, skillGrade, skillLevel)

	def OverOutItem(self):
		if 0 != self.toolTipSkill:
			self.toolTipSkill.HideToolTip()

	## Quest
	def __SelectQuest(self, slotIndex):
		if app.ENABLE_QUEST_RENEWAL:
			questIndex = self.questIndexMap[slotIndex]

			if not questIndex in self.questClicked:
				self.questClicked.append(questIndex)
		else:
			questIndex = quest.GetQuestIndex(self.questShowingStartIndex + slotIndex)

		import event
		event.QuestButtonClick(-2147483648 + questIndex)

	def RefreshQuest(self):
		if app.ENABLE_QUEST_RENEWAL:
			if self.isLoaded == 0 or self.state != "QUEST":
				return

			for cat in self.questOpenedCategories:
				self.RefreshQuestCategory(cat)

			self.RefreshQuestCategoriesCount()
		else:
			if self.isLoaded==0:
				return

			self.OnQuestScroll()

			questCount = quest.GetQuestCount()
			questRange = range(quest.QUEST_MAX_NUM)

			if questCount > quest.QUEST_MAX_NUM:
				self.questScrollBar.Show()
			else:
				self.questScrollBar.Hide()

			for i in questRange[:questCount]:
				(questName, questIcon, questCounterName, questCounterValue) = quest.GetQuestData(self.questShowingStartIndex + i)

				self.questNameList[i].SetText(questName)
				self.questNameList[i].Show()
				self.questLastCountList[i].Show()
				self.questLastTimeList[i].Show()

				if len(questCounterName) > 0:
					self.questLastCountList[i].SetText("%s : %d" % (questCounterName, questCounterValue))
				else:
					self.questLastCountList[i].SetText("")

				## Icon
				self.questSlot.SetSlot(i, i, 1, 1, questIcon)

			for i in questRange[questCount:]:
				self.questNameList[i].Hide()
				self.questLastTimeList[i].Hide()
				self.questLastCountList[i].Hide()
				self.questSlot.ClearSlot(i)
				self.questSlot.HideSlotBaseImage(i)

			self.__UpdateQuestClock()

	def __UpdateQuestClock(self):
		if "QUEST" == self.state:
			if app.ENABLE_QUEST_RENEWAL:
				for clock in self.questClockList:
					clockText = localeInfo.QUEST_UNLIMITED_TIME

					if clock.GetProperty("idx"):
						(lastName, lastTime) = quest.GetQuestLastTime(clock.GetProperty("idx"))

						if len(lastName) > 0:
							if lastTime <= 0:
								clockText = localeInfo.QUEST_TIMEOVER
							else:
								questLastMinute = lastTime / 60
								questLastSecond = lastTime % 60

								clockText = lastName + " : "

								if questLastMinute > 0:
									clockText += str(questLastMinute) + localeInfo.QUEST_MIN
									if questLastSecond > 0:
										clockText += " "

								if questLastSecond > 0:
									clockText += str(questLastSecond) + localeInfo.QUEST_SEC

					clock.SetText(clockText)
			else:
				# QUEST_LIMIT_COUNT_BUG_FIX
				for i in xrange(min(quest.GetQuestCount(), quest.QUEST_MAX_NUM)):
				# END_OF_QUEST_LIMIT_COUNT_BUG_FIX
					(lastName, lastTime) = quest.GetQuestLastTime(i + self.questShowingStartIndex)

					clockText = localeInfo.QUEST_UNLIMITED_TIME
					if len(lastName) > 0:

						if lastTime <= 0:
							clockText = localeInfo.QUEST_TIMEOVER
						else:
							questLastMinute = lastTime / 60
							questLastSecond = lastTime % 60

							clockText = lastName + " : "

							if questLastMinute > 0:
								clockText += str(questLastMinute) + localeInfo.QUEST_MIN
								if questLastSecond > 0:
									clockText += " "

							if questLastSecond > 0:
								clockText += str(questLastSecond) + localeInfo.QUEST_SEC

					self.questLastTimeList[i].SetText(clockText)

	def __GetStatMinusPoint(self):
		POINT_STAT_RESET_COUNT = 112
		return player.GetStatus(POINT_STAT_RESET_COUNT)

	def __OverInStatMinusButton(self, stat):
		try:
			self.__ShowStatToolTip(self.STAT_MINUS_DESCRIPTION[stat] % self.__GetStatMinusPoint())
		except KeyError:
			pass

		self.refreshToolTip = lambda arg=stat: self.__OverInStatMinusButton(arg) 

	def __OverOutStatMinusButton(self):
		self.__HideStatToolTip()
		self.refreshToolTip = 0

	def __OverInStatusTT(self, arg):
		try:
			self.__ShowStatToolTip(arg)
		except KeyError:
			pass

	def __OverOutStatusTT(self):
		self.__HideStatToolTip()

	def __OverInStatButton(self, stat):	
		try:
			self.__ShowStatToolTip("|Ekey_ctrl|e"+" + "+"|Ekey_lclick|e - Adaug� +10",grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0),False)
		except KeyError:
			pass

	def __OverOutStatButton(self):
		self.__HideStatToolTip()

	def __ShowStatToolTip(self, statDesc, statDesc2 = False, arg2 = False):
		if self.toolTip != None:
			self.toolTip.ClearToolTip()
			self.toolTip.AppendTextLine(statDesc)
		
		if arg2 == True:
			self.toolTip.AppendTextLine(statDesc2)
			
		self.toolTip.Show()
			

	def __HideStatToolTip(self):
		if self.toolTip != None:
			self.toolTip.Hide()

	def OnPressEscapeKey(self):
		if app.ENABLE_QUEST_RENEWAL:
			if self.questSlideWndNewKey > 0:
				if self.questSlideWnd[self.questSlideWndNewKey-1] is not None:
					self.questSlideWnd[self.questSlideWndNewKey-1].OnPressEscapeKey()	
		self.Close()
		return TRUE

	def OnUpdate(self):
		if self.chDetailsWnd:
			x, y = self.GetGlobalPosition()
			self.chDetailsWnd.AdjustPosition(x, y)
		self.__UpdateQuestClock()
		if app.ENABLE_EXPRESSING_EMOTION:
			if "EMOTICON" == self.state:
				if len(self.specialEmotionList) > 0:
					for i in xrange(0,len(self.specialEmotionList)):
						self.specialEmotionListTime[i] = self.SetTime(self.specialEmotionList[i][1])

	## Skill Process
	def __RefreshSkillPage(self, name, slotCount):
		global SHOW_LIMIT_SUPPORT_SKILL_LIST

		skillPage = self.skillPageDict[name]

		startSlotIndex = skillPage.GetStartIndex()
		if "ACTIVE" == name:
			if self.PAGE_HORSE == self.curSelectedSkillGroup:
				startSlotIndex += slotCount

		getSkillType=skill.GetSkillType
		getSkillIndex=player.GetSkillIndex
		getSkillGrade=player.GetSkillGrade
		getSkillLevel=player.GetSkillLevel
		getSkillLevelUpPoint=skill.GetSkillLevelUpPoint
		getSkillMaxLevel=skill.GetSkillMaxLevel
		for i in xrange(slotCount+1):

			slotIndex = i + startSlotIndex
			skillIndex = getSkillIndex(slotIndex)

			for j in xrange(skill.SKILL_GRADE_COUNT):
				skillPage.ClearSlot(self.__GetRealSkillSlot(j, i))

			if 0 == skillIndex:
				continue

			skillGrade = getSkillGrade(slotIndex)
			skillLevel = getSkillLevel(slotIndex)
			skillType = getSkillType(skillIndex)

			## �¸� ��ų ���� ó��
			if player.SKILL_INDEX_RIDING == skillIndex:
				if 1 == skillGrade:
					skillLevel += 19
				elif 2 == skillGrade:
					skillLevel += 29
				elif 3 == skillGrade:
					skillLevel = 40

				skillPage.SetSkillSlotNew(slotIndex, skillIndex, max(skillLevel-1, 0), skillLevel)
				skillPage.SetSlotCount(slotIndex, skillLevel)

			## ACTIVE
			elif skill.SKILL_TYPE_ACTIVE == skillType:
				for j in xrange(skill.SKILL_GRADE_COUNT):
					realSlotIndex = self.__GetRealSkillSlot(j, slotIndex)
					skillPage.SetSkillSlotNew(realSlotIndex, skillIndex, j, skillLevel)
					skillPage.SetCoverButton(realSlotIndex)

					if (skillGrade == skill.SKILL_GRADE_COUNT) and j == (skill.SKILL_GRADE_COUNT-1):
						skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)
					elif (not self.__CanUseSkillNow()) or (skillGrade != j):
						skillPage.SetSlotCount(realSlotIndex, 0)
						skillPage.DisableCoverButton(realSlotIndex)
						skillPage.DeactivateSlot(realSlotIndex)
					else:
						skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)

					if player.IsSkillActive(slotIndex) and (skillGrade == j): # fix
						skillPage.ActivateSlot(realSlotIndex)
			## �׿�
			else:
				if not SHOW_LIMIT_SUPPORT_SKILL_LIST or skillIndex in SHOW_LIMIT_SUPPORT_SKILL_LIST:
					realSlotIndex = self.__GetETCSkillRealSlotIndex(slotIndex)
					skillPage.SetSkillSlot(realSlotIndex, skillIndex, skillLevel)
					skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)

					if skill.CanUseSkill(skillIndex):
						skillPage.SetCoverButton(realSlotIndex)

			skillPage.RefreshSlot()
			self.__RestoreSlotCoolTime(skillPage)

	def RefreshSkill(self):

		if self.isLoaded==0:
			return

		if self.__IsChangedHorseRidingSkillLevel():
			self.RefreshCharacter()
			return


		global SHOW_ONLY_ACTIVE_SKILL
		if SHOW_ONLY_ACTIVE_SKILL:
			self.__RefreshSkillPage("ACTIVE", self.ACTIVE_PAGE_SLOT_COUNT)
		else:
			self.__RefreshSkillPage("ACTIVE", self.ACTIVE_PAGE_SLOT_COUNT)
			self.__RefreshSkillPage("SUPPORT", self.SUPPORT_PAGE_SLOT_COUNT)

		self.RefreshSkillPlusButtonList()

	def __RestoreSlotCoolTime(self, skillPage):
		restoreType = skill.SKILL_TYPE_NONE
		if self.PAGE_HORSE == self.curSelectedSkillGroup:
			restoreType = skill.SKILL_TYPE_HORSE
		else:
			restoreType = skill.SKILL_TYPE_ACTIVE
		
		skillPage.RestoreSlotCoolTime(restoreType)

	def CanShowPlusButton(self, skillIndex, skillLevel, curStatPoint):

		## ��ų�� ������
		if 0 == skillIndex:
			return FALSE

		## ������ ������ �����Ѵٸ�
		if not skill.CanLevelUpSkill(skillIndex, skillLevel):
			return FALSE

		return TRUE

	def __RefreshSkillPlusButton(self, name):
		global HIDE_SUPPORT_SKILL_POINT
		if HIDE_SUPPORT_SKILL_POINT and "SUPPORT" == name:
			return

		slotWindow = self.skillPageDict[name]
		slotWindow.HideAllSlotButton()

		slotStatType = self.skillPageStatDict[name]
		if 0 == slotStatType:
			return

		statPoint = player.GetStatus(slotStatType)
		startSlotIndex = slotWindow.GetStartIndex()
		if "HORSE" == name:
			startSlotIndex += self.ACTIVE_PAGE_SLOT_COUNT

		if statPoint > 0:
			for i in xrange(self.PAGE_SLOT_COUNT):
				slotIndex = i + startSlotIndex
				skillIndex = player.GetSkillIndex(slotIndex)
				skillGrade = player.GetSkillGrade(slotIndex)
				skillLevel = player.GetSkillLevel(slotIndex)

				if skillIndex == 0:
					continue
				if skillGrade != 0:
					continue

				if name == "HORSE":
					if player.GetStatus(player.LEVEL) >= skill.GetSkillLevelLimit(skillIndex):
						if skillLevel < 20:
							slotWindow.ShowSlotButton(self.__GetETCSkillRealSlotIndex(slotIndex))

				else:
					if "SUPPORT" == name:						
						if not SHOW_LIMIT_SUPPORT_SKILL_LIST or skillIndex in SHOW_LIMIT_SUPPORT_SKILL_LIST:
							if self.CanShowPlusButton(skillIndex, skillLevel, statPoint):
								slotWindow.ShowSlotButton(slotIndex)
					else:
						if self.CanShowPlusButton(skillIndex, skillLevel, statPoint):
							slotWindow.ShowSlotButton(slotIndex)
					

	def RefreshSkillPlusButtonList(self):

		if self.isLoaded==0:
			return

		self.RefreshSkillPlusPointLabel()

		if not self.__CanUseSkillNow():
			return

		try:
			if self.PAGE_HORSE == self.curSelectedSkillGroup:
				self.__RefreshSkillPlusButton("HORSE")
			else:
				self.__RefreshSkillPlusButton("ACTIVE")

			self.__RefreshSkillPlusButton("SUPPORT")

		except:
			import exception
			exception.Abort("CharacterWindow.RefreshSkillPlusButtonList.BindObject")

	def RefreshSkillPlusPointLabel(self):
		if self.isLoaded==0:
			return

		if self.PAGE_HORSE == self.curSelectedSkillGroup:
			activeStatPoint = player.GetStatus(player.SKILL_HORSE)
			self.activeSkillPointValue.SetText(str(activeStatPoint))

		else:
			activeStatPoint = player.GetStatus(player.SKILL_ACTIVE)
			self.activeSkillPointValue.SetText(str(activeStatPoint))

		supportStatPoint = max(0, player.GetStatus(player.SKILL_SUPPORT))
		self.supportSkillPointValue.SetText(str(supportStatPoint))

	## Skill Level Up Button
	def OnPressedSlotButton(self, slotNumber):
		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotNumber)

		skillIndex = player.GetSkillIndex(srcSlotIndex)
		curLevel = player.GetSkillLevel(srcSlotIndex)
		maxLevel = skill.GetSkillMaxLevel(skillIndex)

		net.SendChatPacket("/skillup " + str(skillIndex))

	## Use Skill
	def ClickSkillSlot(self, slotIndex):

		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotIndex)
		skillIndex = player.GetSkillIndex(srcSlotIndex)
		skillType = skill.GetSkillType(skillIndex)

		if not self.__CanUseSkillNow():
			if skill.SKILL_TYPE_ACTIVE == skillType:
				return

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				if skill.CanUseSkill(skillIndex):
					player.ClickSkillSlot(srcSlotIndex)
					return

		mouseModule.mouseController.DeattachObject()

	## FIXME : ��ų�� ��������� ���� ��ȣ�� ������ �ش� ������ ã�Ƽ� ������Ʈ �Ѵ�.
	##         �ſ� ���ո�. ���� ��ü�� �����ؾ� �ҵ�.
	def OnUseSkill(self, slotIndex, coolTime):

		skillIndex = player.GetSkillIndex(slotIndex)
		skillType = skill.GetSkillType(skillIndex)

		## ACTIVE
		if skill.SKILL_TYPE_ACTIVE == skillType:
			skillGrade = player.GetSkillGrade(slotIndex)
			slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)
		## ETC
		else:
			slotIndex = self.__GetETCSkillRealSlotIndex(slotIndex)

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				slotWindow.StoreSlotCoolTime(skillType, slotIndex, coolTime)
				self.__RestoreSlotCoolTime(slotWindow)
				return

	def OnActivateSkill(self, slotIndex):
		skillGrade = player.GetSkillGrade(slotIndex)
		slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)
		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				if app.ENABLE_ACCE_COSTUME_SYSTEM:
					slotWindow.ActivateSlotOld(slotIndex)
				else:
					slotWindow.ActivateSlot(slotIndex)
				
				return

	def OnDeactivateSkill(self, slotIndex):
		skillGrade = player.GetSkillGrade(slotIndex)
		slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)
		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				if app.ENABLE_ACCE_COSTUME_SYSTEM:
					slotWindow.DeactivateSlotOld(slotIndex)
				else:
					slotWindow.DeactivateSlot(slotIndex)
				
				return

	def __ShowJobToolTip(self):
		self.toolTipJob.ShowToolTip()

	if app.SKILL_COOLTIME_UPDATE:
		def SkillClearCoolTime(self, slotIndex):
			slotIndex = self.__GetRealSkillSlot(player.GetSkillGrade(slotIndex), slotIndex)
			for slotWindow in self.skillPageDict.values():
				if slotWindow.HasSlot(slotIndex):
					slotWindow.SetSlotCoolTime(slotIndex, 0)

	def __HideJobToolTip(self):
		self.toolTipJob.HideToolTip()

	def __SetJobText(self, mainJob, subJob):
		if player.GetStatus(player.LEVEL)<5:
			subJob=0

		if 949 == app.GetDefaultCodePage():
			self.toolTipJob.ClearToolTip()

			try:
				jobInfoTitle=localeInfo.JOBINFO_TITLE[mainJob][subJob]
				jobInfoData=localeInfo.JOBINFO_DATA_LIST[mainJob][subJob]
			except IndexError:
				print "uiCharacter.CharacterWindow.__SetJobText(mainJob=%d, subJob=%d)" % (mainJob, subJob)
				return

			self.toolTipJob.AutoAppendTextLine(jobInfoTitle)
			self.toolTipJob.AppendSpace(5)

			for jobInfoDataLine in jobInfoData:
				self.toolTipJob.AutoAppendTextLine(jobInfoDataLine)

			self.toolTipJob.AlignHorizonalCenter()

	def __ShowAlignmentToolTip(self):
		if self.toolTipAlignment != None:#ifbd
			self.toolTipAlignment.ShowToolTip()

	def __HideAlignmentToolTip(self):
		if self.toolTipAlignment != None:
			self.toolTipAlignment.HideToolTip()

	def RefreshCharacter(self):
		if self.isLoaded==0:
			return

		## Name
		try:
			characterName = player.GetName()
			guildName = player.GetGuildName()
			self.characterNameValue.SetText(characterName)
			self.guildNameValue.SetText(guildName)
			if not guildName:
				if localeInfo.IsARABIC():
					self.characterNameSlot.SetPosition(190, 34)
				else:
					self.characterNameSlot.SetPosition(109, 34)

				self.guildNameSlot.Hide()
			else:
				if localeInfo.IsJAPAN():
					self.characterNameSlot.SetPosition(143, 34)
				else:
					self.characterNameSlot.SetPosition(153, 34)
				self.guildNameSlot.Show()
		except:
			import exception
			exception.Abort("CharacterWindow.RefreshCharacter.BindObject")

		race = net.GetMainActorRace()
		group = net.GetMainActorSkillGroup()
		empire = net.GetMainActorEmpire()

		## Job Text
		job = chr.RaceToJob(race)
		self.__SetJobText(job, group)

		## FaceImage
		try:
			faceImageName = FACE_IMAGE_DICT[race]

			try:
				self.faceImage.LoadImage(faceImageName)
			except:
				print "CharacterWindow.RefreshCharacter(race=%d, faceImageName=%s)" % (race, faceImageName)
				self.faceImage.Hide()

		except KeyError:
			self.faceImage.Hide()

		## GroupName
		self.__SetSkillGroupName(race, group)

		## Skill
		if 0 == group:
			self.__SelectSkillGroup(0)

		else:
			self.__SetSkillSlotData(race, group, empire)

			if self.__CanUseHorseSkill():
				self.__SelectSkillGroup(0)
		
		if app.ENABLE_NEW_DETAILS_GUI:
			if self.chDetailsWnd:
				if self.chDetailsWnd.IsShow():
					self.chDetailsWnd.Refresh()

	def __SetSkillGroupName_P(self, race, group):

		job = chr.RaceToJob(race)

		if not self.SKILL_GROUP_NAME_DICT.has_key(job):
			return

		nameList = self.SKILL_GROUP_NAME_DICT[job]

		if 0 == group:
			self.skillGroupButtonP1.SetText(nameList[1])
			self.skillGroupButtonP2.SetText(nameList[2])
			self.skillGroupButtonP3.SetText(nameList[3])
			self.skillGroupButtonP1.Show()
			self.skillGroupButtonP2.Show()
			self.skillGroupButtonP3.Show()
			self.activeSkillGroupName.Hide()

		else:
			if self.__CanUseHorseSkill():
				self.activeSkillGroupName.Hide()
				self.skillGroupButtonP1.SetText(nameList.get(group, "Noname"))
				self.skillGroupButtonP2.SetText(localeInfo.SKILL_GROUP_HORSE)
				self.skillGroupButtonP3.SetText(localeInfo.SKILL_GROUP_PERKS)
				self.skillGroupButtonP1.Show()
				self.skillGroupButtonP2.Show()
				self.skillGroupButtonP3.Show()


	def __SetSkillGroupName(self, race, group):

		job = chr.RaceToJob(race)

		if not self.SKILL_GROUP_NAME_DICT.has_key(job):
			return

		nameList = self.SKILL_GROUP_NAME_DICT[job]

		if 0 == group:
			self.skillGroupButton1.SetText(nameList[1])
			self.skillGroupButton2.SetText(nameList[2])
			self.skillGroupButton3.SetText(nameList[3])
			self.skillGroupButton1.Show()
			self.skillGroupButton2.Show()
			self.skillGroupButton3.Show()
			self.activeSkillGroupName.Hide()

		else:

			if self.__CanUseHorseSkill():
				self.activeSkillGroupName.Hide()
				self.skillGroupButton1.SetText(nameList.get(group, "Noname"))
				self.skillGroupButton2.SetText(localeInfo.SKILL_GROUP_HORSE)
				self.skillGroupButton3.SetText(localeInfo.SKILL_GROUP_PERKS)
				self.skillGroupButton1.Show()
				self.skillGroupButton2.Show()
				self.skillGroupButton3.Show()

			else:
				self.activeSkillGroupName.SetText(nameList.get(group, "Noname"))
				self.activeSkillGroupName.Show()
				self.skillGroupButton1.Hide()
				self.skillGroupButton2.Hide()
				self.skillGroupButton3.Hide()

	def __SetSkillSlotData(self, race, group, empire=0):

		## SkillIndex
		playerLoad.RegisterSkill(race, group, empire)

		## Event
		self.__SetSkillSlotEvent()

		## Refresh
		self.RefreshSkill()

	def __SelectSkillGroup(self, index):
		for btn in self.skillGroupButton:
			btn.SetUp()
		self.skillGroupButton3.SetUp()
		self.skillGroupButtonP3.SetUp()
		self.skillGroupButton[index].Down()

		if self.__CanUseHorseSkill():
			if 0 == index:
				index = net.GetMainActorSkillGroup()-1
			elif 1 == index:
				index = self.PAGE_HORSE
		self.curSelectedSkillGroup = index
		self.__SetSkillSlotData(net.GetMainActorRace(), index+1, net.GetMainActorEmpire())

	def __CanUseSkillNow(self):
		if 0 == net.GetMainActorSkillGroup():
			return FALSE

		return TRUE

	def __CanUseHorseSkill(self):

		slotIndex = player.GetSkillSlotIndex(player.SKILL_INDEX_RIDING)

		if not slotIndex:
			return FALSE

		grade = player.GetSkillGrade(slotIndex)
		level = player.GetSkillLevel(slotIndex)
		if level < 0:
			level *= -1
		if grade >= 1 and level >= 1:
			return TRUE

		return FALSE

	def __IsChangedHorseRidingSkillLevel(self):
		ret = FALSE

		if -1 == self.canUseHorseSkill:
			self.canUseHorseSkill = self.__CanUseHorseSkill()

		if self.canUseHorseSkill != self.__CanUseHorseSkill():
			ret = TRUE

		self.canUseHorseSkill = self.__CanUseHorseSkill()
		return ret

	def __GetRealSkillSlot(self, skillGrade, skillSlot):
		return skillSlot + min(skill.SKILL_GRADE_COUNT-1, skillGrade)*skill.SKILL_GRADE_STEP_COUNT

	def __GetETCSkillRealSlotIndex(self, skillSlot):
		if skillSlot > 100:
			return skillSlot
		return skillSlot % self.ACTIVE_PAGE_SLOT_COUNT

	def __RealSkillSlotToSourceSlot(self, realSkillSlot):
		if realSkillSlot > 100:
			return realSkillSlot
		if self.PAGE_HORSE == self.curSelectedSkillGroup:
			return realSkillSlot + self.ACTIVE_PAGE_SLOT_COUNT
		return realSkillSlot % skill.SKILL_GRADE_STEP_COUNT

	def __GetSkillGradeFromSlot(self, skillSlot):
		return int(skillSlot / skill.SKILL_GRADE_STEP_COUNT)

	def SelectSkillGroup(self, index):
		self.__SelectSkillGroup(index)

	def OnQuestScroll(self):
		questCount = quest.GetQuestCount()
		scrollLineCount = max(0, questCount - quest.QUEST_MAX_NUM)
		startIndex = int(scrollLineCount * self.questScrollBar.GetPos())

		if startIndex != self.questShowingStartIndex:
			self.questShowingStartIndex = startIndex
			self.RefreshQuest()

	if app.ENABLE_QUEST_RENEWAL:
		def __OnScrollQuest(self):
			if self.state != "QUEST":
				return

			curPos = self.questScrollBar.GetPos()
			if math.fabs(curPos - self.questLastScrollPosition) >= 0.001:
				self.RerenderQuestPage()
				self.questLastScrollPosition = curPos

		def ResetQuestScroll(self):
			self.questScrollBar.Hide()

			if self.questScrollBar.GetPos() != 0:
				self.questScrollBar.SetPos(0)

		def RerenderQuestPage(self):
			overflowingY = self.displayY - self.MAX_QUEST_PAGE_HEIGHT
			if overflowingY < 0:
				overflowingY = 0

			self.baseCutY = math.ceil(overflowingY * self.questScrollBar.GetPos())
			self.displayY = 0
			self.RearrangeQuestCategories(xrange(quest.QUEST_CATEGORY_MAX_NUM))
			self.RefreshQuestCategory()

			if overflowingY > 0:
				if (len(self.questOpenedCategories)) == 0:
					self.ResetQuestScroll()
				else:
					self.questScrollBar.Show()
			else:
				self.ResetQuestScroll()

		def __LoadQuestCategory(self):
			self.questPage.Show()

			if self.isLoaded == 0:
				return

			for i in xrange(quest.QUEST_CATEGORY_MAX_NUM):
				category = self.questCategoryList[i]

				categoryName = category.GetProperty("name")
				if not categoryName:
					category.SetProperty("name", category.GetText())
					categoryName = category.GetText()

				questCount = self.GetQuestCountInCategory(i)
				self.questCategoryList[i].SetTextAlignLeft(categoryName + " (" + str(questCount) + ")")
				self.questCategoryList[i].SetTextColor(self.GetQuestCategoryColor(i))
				self.questCategoryList[i].SetQuestLabel(quest_lable_expend_img_path_dict[i], self.GetQuestCountInCategory(i))
				self.questCategoryList[i].Show()

			self.RefreshQuestCategory()
			if self.isQuestCategoryLoad == False:
				self.questScrollBar.Hide()
			else:
				self.RerenderQuestPage()

			self.isQuestCategoryLoad = True

		def GetQuestCategoryColor(self, category):
			return self.questColorList["default_title"]

		def GetQuestProperties(self, questName):
			findString = {
				"*" : "blue",
				"&" : "green",
				"~" : "golden"
			}

			if questName[0] in findString:
				return (questName[1:], findString[questName[0]])

			return (questName, None)

		def IsQuestCategoryOpen(self, category):
			return (category in self.questOpenedCategories)

		def ToggleCategory(self, category):
			if self.IsQuestCategoryOpen(category):
				self.CloseQuestCategory(category)
			else:
				self.OpenQuestCategory(category)

		def RearrangeQuestCategories(self, categoryRange):
			i = 0
			for i in categoryRange:
				if (self.displayY - self.baseCutY) >= 0 and (self.displayY - self.baseCutY) < self.MAX_QUEST_PAGE_HEIGHT - 20:
					self.questCategoryList[i].SetPosition(13, (self.displayY - self.baseCutY) + 10)
					self.questCategoryList[i].Show()
				else:
					self.questCategoryList[i].Hide()

				self.displayY += 20
				self.questCategoryRenderPos[i] = self.displayY

		def CloseQuestCategory(self, category):
			self.questCategoryList[category].CloseCategory(self.GetQuestCountInCategory(category))

			if category in self.questOpenedCategories:
				self.questOpenedCategories.remove(category)

			for currentSlot in self.questSlotList:
				if currentSlot.GetProperty("category") == category:
					currentSlot.Hide()
					self.displayY -= currentSlot.GetHeight()

			self.RerenderQuestPage()

		def OpenQuestCategory(self, category):
			if self.GetQuestCountInCategory(category) == 0:
				return

			while len(self.questOpenedCategories) >= self.questMaxOpenedCategories:
				openedCategories = self.questOpenedCategories.pop()
				self.CloseQuestCategory(openedCategories)

			self.questCategoryList[category].OpenCategory(self.GetQuestCountInCategory(category))
			self.questOpenedCategories.append(category)
			self.RefreshQuestCategory(category)
			self.RerenderQuestPage()

		def RefreshQuestCategory(self, category = -1):
			if self.isLoaded == 0 or self.state != "QUEST":
				return

			categories = []
			if category == -1:
				categories = self.questOpenedCategories
			elif not category in self.questOpenedCategories:
				self.OpenQuestCategory(category)
				return
			else:
				categories.append(category)

			for currentCategory in categories:
				self.displayY = self.questCategoryRenderPos[currentCategory]

				self.LoadCategory(currentCategory)
				self.RearrangeQuestCategories(xrange(currentCategory + 1, quest.QUEST_CATEGORY_MAX_NUM))

		def RefreshQuestCategoriesCount(self):
			for category in xrange(quest.QUEST_CATEGORY_MAX_NUM):
				categoryName = self.questCategoryList[category].GetProperty("name")
				questCount = self.GetQuestCountInCategory(category)
				self.questCategoryList[category].SetTextAlignLeft(categoryName + " (" + str(questCount) + ")")

		def RefreshQuest(self):
			if self.isLoaded == 0 or self.state != "QUEST":
				return

			for category in self.questOpenedCategories:
				self.RefreshQuestCategory(category)

			self.RefreshQuestCategoriesCount()

		def CreateQuestSlot(self, name):
			for questSlot in self.questSlotList:
				if questSlot.GetWindowName() == name:
					return questSlot

			pyScrLoader = ui.PythonScriptLoader()
			slot = ui.ListBar()
			pyScrLoader.LoadElementListBar(slot, quest_slot_listbar, self.questPage)

			slot.SetParent(self.quest_page_board_window)
			slot.SetWindowName(name)
			slot.Hide()
			self.questSlotList.append(slot)
			return slot

		def SetQuest(self, slot, questID, questName, questCounterName, questCounterValue):
			(name, color) = self.GetQuestProperties(questName)
			slot.SetTextAlignLeft(name, 20)
			if color:
				slot.SetTextColor(self.questColorList[color])
			slot.SetEvent(ui.__mem_func__(self.__SelectQuest), questID)
			slot.SetWindowHorizontalAlignLeft()
			slot.Show()

		def LoadCategory(self, category):
			self.questIndexMap = {}
			self.questCounterList = []
			self.questClockList = []
			self.questSeparatorList = []

			for questSlot in self.questSlotList:
				questSlot.Hide()

			questCount = 0
			for questIdx in self.GetQuestsInCategory(category):
				questCount += 1
				(questID, questIndex, questName, questCategory, _, questCounterName, questCounterValue) = questIdx
				(lastName, lastTime) = quest.GetQuestLastTime(questID)

				slot = self.CreateQuestSlot("QuestSlotList_" + str(questCategory) + "_" + str(questID))

				slot.SetPosition(0, (self.displayY - self.baseCutY))
				slot.SetParent(self.quest_page_board_window)
				baseDisplayY = self.displayY

				## -- Quest Counter
				hasCounter = False
				if questCounterName != "":
					self.displayY += 15

					counter = ui.TextLine()
					counter.SetParent(slot)
					counter.SetPosition(20, 20 - 2.5)
					counter.SetText(questCounterName + ": " + str(questCounterValue))
					counter.Show()

					self.questCounterList.append(counter)
					hasCounter = True
				## -- Quest Counter

				## -- Quest Clock
				self.displayY += 15

				clockText = localeInfo.QUEST_UNLIMITED_TIME
				if len(lastName) > 0:
					if lastTime <= 0:
						clockText = localeInfo.QUEST_TIMEOVER
					else:
						questLastMinute = lastTime / 60
						questLastSecond = lastTime % 60

						clockText = lastName + " : "

						if questLastMinute > 0:
							clockText += str(questLastMinute) + localeInfo.QUEST_MIN
							if questLastSecond > 0:
								clockText += " "

						if questLastSecond > 0:
							clockText += str(questLastSecond) + localeInfo.QUEST_SEC

				clock = ui.TextLine()
				clock.SetParent(slot)
				clock.SetPosition(20, 20 + (int(hasCounter) * 14) - 2.5)
				clock.SetText(clockText)
				clock.SetProperty("idx", questID)
				self.questClockList.append(clock)
				clock.Show()
				## -- Quest Clock

				## -- Quest Separator
				self.displayY += 5
				if questCount < self.GetQuestCountInCategory(category):
					seperator = ui.ImageBox()
					seperator.SetParent(slot)
					seperator.SetPosition(4, 20 + (int(hasCounter) * 14 - 2.5) + 15)
					seperator.LoadImage("d:/ymir work/ui/quest_re/quest_list_line_01.tga")
					seperator.Show()
					self.questSeparatorList.append(seperator)
				## -- Quest Separator

				slot.SetProperty("category", questCategory)

				if questIndex in self.questClicked:
					slot.OnClickEvent()

				if (baseDisplayY - self.baseCutY) + 2 >= 0 and (baseDisplayY - self.baseCutY) + 2 < self.MAX_QUEST_PAGE_HEIGHT - 30:
					self.questIndexMap[questID] = questIndex
					self.SetQuest(slot, questID, questName, questCounterName, questCounterValue)

				self.displayY += 15

			newList = []
			for questSlot in self.questSlotList:
				if questSlot.IsShow():
					newList.append(questSlot)

			self.questSlotList = newList

		def __OnClickQuestCategoryButton(self, category):
			self.ToggleCategory(category)

		def GetQuestsInCategory(self, category, retCount = False):
			questList = []
			count = 0
			for i in xrange(quest.GetQuestCount()):
				(questIndex, questName, questCategory, questIcon, questCounterName, questCounterValue) = quest.GetQuestData(i)
				if questCategory == category:
					count += 1
					questList.append((i, questIndex, questName, questCategory, questIcon, questCounterName, questCounterValue))

			if retCount:
				return count

			return questList

		def GetQuestCountInCategory(self, category):
			return self.GetQuestsInCategory(category, True)
			
	if app.ENABLE_NEW_DETAILS_GUI:
		def __InitCharacterDetailsUIButton(self):
			self.ExpandBtn.Show()
			self.MinimizeBtn.Hide()
		def __ClickExpandButton(self):
			if not self.chDetailsWnd:
				self.chDetailsWnd = uiCharacterDetails.CharacterDetailsUI()
			self.chDetailsWnd.Show()
			self.ExpandBtn.Hide()
			self.MinimizeBtn.Show()
		def __ClickMinimizeButton(self):
			self.chDetailsWnd.Hide()
			self.MinimizeBtn.Hide()
			self.ExpandBtn.Show()