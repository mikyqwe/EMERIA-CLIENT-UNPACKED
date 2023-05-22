import ui
import localeInfo
import chr
import item
import app
import skill
import player
import uiToolTip
import math
import constInfo
import constInfo
import grp
from collections import OrderedDict

# WEDDING
class LovePointImage(ui.ExpandedImageBox):

	FILE_PATH = "d:/ymir work/ui/pattern/LovePoint/"
	FILE_DICT = {
		0 : FILE_PATH + "01.dds",
		1 : FILE_PATH + "02.dds",
		2 : FILE_PATH + "02.dds",
		3 : FILE_PATH + "03.dds",
		4 : FILE_PATH + "04.dds",
		5 : FILE_PATH + "05.dds",
	}

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		self.loverName = ""
		self.lovePoint = 0

		self.toolTip = uiToolTip.ToolTip(100)
		self.toolTip.HideToolTip()

	def __del__(self):
		ui.ExpandedImageBox.__del__(self)

	def SetLoverInfo(self, name, lovePoint):
		self.loverName = name
		self.lovePoint = lovePoint
		self.__Refresh()

	def OnUpdateLovePoint(self, lovePoint):
		self.lovePoint = lovePoint
		self.__Refresh()

	def __Refresh(self):
		self.lovePoint = max(0, self.lovePoint)
		self.lovePoint = min(100, self.lovePoint)

		if 0 == self.lovePoint:
			loveGrade = 0
		else:
			loveGrade = self.lovePoint / 25 + 1
		fileName = self.FILE_DICT.get(loveGrade, self.FILE_PATH+"00.dds")

		try:
			self.LoadImage(fileName)
		except:
			import dbg
			dbg.TraceError("LovePointImage.SetLoverInfo(lovePoint=%d) - LoadError %s" % (self.lovePoint, fileName))

		self.SetScale(0.7, 0.7)

		self.toolTip.ClearToolTip()
		self.toolTip.SetTitle(self.loverName)
		self.toolTip.AppendTextLine(localeInfo.AFF_LOVE_POINT % (self.lovePoint))
		self.toolTip.ResizeToolTip()

	def OnMouseOverIn(self):
		self.toolTip.ShowToolTip()

	def OnMouseOverOut(self):
		self.toolTip.HideToolTip()
# END_OF_WEDDING


class HorseImage(ui.ExpandedImageBox):

	FILE_PATH = "d:/ymir work/ui/pattern/HorseState/"

	FILE_DICT = {
		00 : FILE_PATH+"00.dds",
		01 : FILE_PATH+"00.dds",
		02 : FILE_PATH+"00.dds",
		03 : FILE_PATH+"00.dds",
		10 : FILE_PATH+"10.dds",
		11 : FILE_PATH+"11.dds",
		12 : FILE_PATH+"12.dds",
		13 : FILE_PATH+"13.dds",
		20 : FILE_PATH+"20.dds",
		21 : FILE_PATH+"21.dds",
		22 : FILE_PATH+"22.dds",
		23 : FILE_PATH+"23.dds",
		30 : FILE_PATH+"30.dds",
		31 : FILE_PATH+"31.dds",
		32 : FILE_PATH+"32.dds",
		33 : FILE_PATH+"33.dds",
	}

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)
		self.toolTip = uiToolTip.ToolTip(100)
		self.toolTip.HideToolTip()

	def __GetHorseGrade(self, level):
		if 0 == level:
			return 0

		return (level-1)/10 + 1

	def SetState(self, level, health, battery):
		self.toolTip.ClearToolTip()

		if level>0:

			try:
				grade = self.__GetHorseGrade(level)
				self.__AppendText(localeInfo.LEVEL_LIST[grade])
			except IndexError:
				return

			try:
				healthName=localeInfo.HEALTH_LIST[health]
				if len(healthName)>0:
					self.__AppendText(healthName)
			except IndexError:
				return

			if health>0:
				if battery==0:
					self.__AppendText(localeInfo.NEEFD_REST)

			try:
				fileName=self.FILE_DICT[health*10+battery]
			except KeyError:
				pass

			try:
				self.LoadImage(fileName)
			except:
				pass

		self.SetScale(0.7, 0.7)

	def __AppendText(self, text):
		self.toolTip.AppendTextLine(text)
		self.toolTip.ResizeToolTip()


	def OnMouseOverIn(self):
		self.toolTip.ShowToolTip()

	def OnMouseOverOut(self):
		self.toolTip.HideToolTip()


# AUTO_POTION
class AutoPotionImage(ui.ExpandedImageBox):

	FILE_PATH_HP = "d:/ymir work/ui/pattern/auto_hpgauge/"
	FILE_PATH_SP = "d:/ymir work/ui/pattern/auto_spgauge/"

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		self.loverName = ""
		self.lovePoint = 0
		self.potionType = player.AUTO_POTION_TYPE_HP
		self.filePath = ""

		self.toolTip = uiToolTip.ToolTip(100)
		self.toolTip.HideToolTip()

	def __del__(self):
		ui.ExpandedImageBox.__del__(self)

	def SetPotionType(self, type):
		self.potionType = type

		if player.AUTO_POTION_TYPE_HP == type:
			self.filePath = self.FILE_PATH_HP
		elif player.AUTO_POTION_TYPE_SP == type:
			self.filePath = self.FILE_PATH_SP


	def OnUpdateAutoPotionImage(self):
		self.__Refresh()

	def __Refresh(self):

		isActivated, currentAmount, totalAmount, slotIndex = player.GetAutoPotionInfo(self.potionType)

		amountPercent = (float(currentAmount) / totalAmount) * 100.0
		grade = math.ceil(amountPercent / 20)

		if 5.0 > amountPercent:
			grade = 0

		if 80.0 < amountPercent:
			grade = 4
			if 90.0 < amountPercent:
				grade = 5

		fmt = self.filePath + "%.2d.dds"
		fileName = fmt % grade

		try:
			self.LoadImage(fileName)
		except:
			import dbg
			dbg.TraceError("AutoPotionImage.__Refresh(potionType=%d) - LoadError %s" % (self.potionType, fileName))

		self.SetScale(0.7, 0.7)

		self.toolTip.ClearToolTip()

		if player.AUTO_POTION_TYPE_HP == type:
			self.toolTip.SetTitle(localeInfo.TOOLTIP_AUTO_POTION_HP)
		else:
			self.toolTip.SetTitle(localeInfo.TOOLTIP_AUTO_POTION_SP)

		self.toolTip.AppendTextLine(localeInfo.TOOLTIP_AUTO_POTION_REST	% (amountPercent))
		self.toolTip.ResizeToolTip()

	def OnMouseOverIn(self):
		self.toolTip.ShowToolTip()

	def OnMouseOverOut(self):
		self.toolTip.HideToolTip()
# END_OF_AUTO_POTION


class AffectImage(ui.ExpandedImageBox):

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		self.toolTipText = None
		self.isSkillAffect = True
		self.description = None
		self.endTime = 0
		self.affect = None
		self.isClocked = True
		
		self.itemImage = None

	def SetAffect(self, affect):
		self.affect = affect

	def GetAffect(self):
		return self.affect
		
	def SetItemImage(self, fileName):
		if not self.itemImage:
			self.itemImage = ui.ExpandedImageBox()
			self.itemImage.SetParent(self)
			self.itemImage.AddFlag("not_pick")
			self.itemImage.SetWindowHorizontalAlignCenter()
			self.itemImage.SetWindowVerticalAlignCenter()
			
		self.itemImage.LoadImage(fileName)
		self.itemImage.SetScale(0.65, 0.65)
		self.itemImage.Show()

	def SetToolTipText(self, text, x = 0, y = -19):

		if not self.toolTipText:
			textLine = ui.TextLine()
			textLine.SetParent(self)
			textLine.SetSize(0, 0)
			textLine.SetOutline()
			textLine.Hide()
			self.toolTipText = textLine

		self.toolTipText.SetText(text)
		w, h = self.toolTipText.GetTextSize()
		self.toolTipText.SetPosition(max(0, x + self.GetWidth()/2 - w/2), y)

	def SetDescription(self, description):
		self.description = description

	def SetDuration(self, duration):
		self.endTime = 0
		if duration > 0:
			self.endTime = app.GetGlobalTimeStamp() + duration

	def UpdateAutoPotionDescription(self):

		potionType = 0
		if self.affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY:
			potionType = player.AUTO_POTION_TYPE_HP
		else:
			potionType = player.AUTO_POTION_TYPE_SP

		isActivated, currentAmount, totalAmount, slotIndex = player.GetAutoPotionInfo(potionType)
		amountPercent = 0.0

		try:
			amountPercent = (float(currentAmount) / totalAmount) * 100.0
		except:
			amountPercent = 100.0

		self.SetToolTipText(self.description % amountPercent, 0, 40)

	def SetClock(self, isClocked):
		self.isClocked = isClocked

	def UpdateDescription(self):
		if not self.isClocked:
			self.__UpdateDescription2()
			return

		if not self.description:
			return

		toolTip = self.description
		if self.endTime > 0:
			if self.endTime - app.GetGlobalTimeStamp() < 86400*365: #If time is less than a year, display					
				leftTime = localeInfo.SecondToDHM(self.endTime - app.GetGlobalTimeStamp())
				toolTip += " (%s : %s)" % (localeInfo.LEFT_TIME, leftTime)
			else:
				toolTip += " (%s)" % localeInfo.NEVER_EXPIRES_DURATION
			
		self.SetToolTipText(toolTip, 0, 40)
		
	#?????? ??? ???? ??? ??
	def __UpdateDescription2(self):
		if not self.description:
			return

		toolTip = self.description
		self.SetToolTipText(toolTip, 0, 40)

	def SetSkillAffectFlag(self, flag):
		self.isSkillAffect = flag

	def IsSkillAffect(self):
		return self.isSkillAffect

	def OnMouseOverIn(self):
		if self.toolTipText:
			self.toolTipText.Show()

	def OnMouseOverOut(self):
		if self.toolTipText:
			self.toolTipText.Hide()

class AffectShower(ui.Window):

	MALL_DESC_IDX_START = 1000
	BLEND_IDX_START = 2000
	WATER_IDX_START = 2200
	SITE_IDX_START = 2400
	MONSTER_IDX_START = 2600
	IMAGE_STEP = 25
	AFFECT_MAX_NUM = 32

	INFINITE_AFFECT_DURATION = 0x1FFFFFFF

	AFFECT_DATA_DICT =	{
			chr.AFFECT_POISON : (localeInfo.SKILL_TOXICDIE, "d:/ymir work/ui/skill/common/affect/otrava.tga"),
			chr.AFFECT_SLOW : (localeInfo.SKILL_SLOW, "d:/ymir work/ui/skill/common/affect/incetinire.tga"),
			chr.AFFECT_STUN : (localeInfo.SKILL_STUN, "d:/ymir work/ui/skill/common/affect/stun.tga"),

			chr.AFFECT_ATT_SPEED_POTION : (localeInfo.SKILL_INC_ATKSPD, "d:/ymir work/ui/skill/common/affect/Increase_Attack_Speed.sub"),
			chr.AFFECT_MOV_SPEED_POTION : (localeInfo.SKILL_INC_MOVSPD, "d:/ymir work/ui/skill/common/affect/Increase_Move_Speed.sub"),
			chr.AFFECT_FISH_MIND : (localeInfo.SKILL_FISHMIND, "d:/ymir work/ui/skill/common/affect/fishmind.sub"),

			chr.AFFECT_JEONGWI : (localeInfo.SKILL_JEONGWI, "d:/ymir work/ui/skill/warrior/jeongwi_03.sub",),
			chr.AFFECT_GEOMGYEONG : (localeInfo.SKILL_GEOMGYEONG, "d:/ymir work/ui/skill/warrior/geomgyeong_03.sub",),
			chr.AFFECT_CHEONGEUN : (localeInfo.SKILL_CHEONGEUN, "d:/ymir work/ui/skill/warrior/cheongeun_03.sub",),
			chr.AFFECT_GYEONGGONG : (localeInfo.SKILL_GYEONGGONG, "d:/ymir work/ui/skill/assassin/gyeonggong_03.sub",),
			chr.AFFECT_EUNHYEONG : (localeInfo.SKILL_EUNHYEONG, "d:/ymir work/ui/skill/assassin/eunhyeong_03.sub",),
			chr.AFFECT_GWIGEOM : (localeInfo.SKILL_GWIGEOM, "d:/ymir work/ui/skill/sura/gwigeom_03.sub",),
			chr.AFFECT_GONGPO : (localeInfo.SKILL_GONGPO, "d:/ymir work/ui/skill/sura/gongpo_03.sub",),
			chr.AFFECT_JUMAGAP : (localeInfo.SKILL_JUMAGAP, "d:/ymir work/ui/skill/sura/jumagap_03.sub"),
			chr.AFFECT_HOSIN : (localeInfo.SKILL_HOSIN, "d:/ymir work/ui/skill/shaman/hosin_03.sub",),
			chr.AFFECT_BOHO : (localeInfo.SKILL_BOHO, "d:/ymir work/ui/skill/shaman/boho_03.sub",),
			chr.AFFECT_KWAESOK : (localeInfo.SKILL_KWAESOK, "d:/ymir work/ui/skill/shaman/kwaesok_03.sub",),
			chr.AFFECT_HEUKSIN : (localeInfo.SKILL_HEUKSIN, "d:/ymir work/ui/skill/sura/heuksin_03.sub",),
			chr.AFFECT_MUYEONG : (localeInfo.SKILL_MUYEONG, "d:/ymir work/ui/skill/sura/muyeong_03.sub",),
			chr.AFFECT_GICHEON : (localeInfo.SKILL_GICHEON, "d:/ymir work/ui/skill/shaman/gicheon_03.sub",),
			chr.AFFECT_JEUNGRYEOK : (localeInfo.SKILL_JEUNGRYEOK, "d:/ymir work/ui/skill/shaman/jeungryeok_03.sub",),
			chr.AFFECT_PABEOP : (localeInfo.SKILL_PABEOP, "d:/ymir work/ui/skill/sura/pabeop_03.sub",),
			chr.AFFECT_FALLEN_CHEONGEUN : (localeInfo.SKILL_CHEONGEUN, "d:/ymir work/ui/skill/warrior/cheongeun_03.sub",),
			28 : (localeInfo.SKILL_FIRE, "d:/ymir work/ui/skill/sura/hwayeom_03.sub",),
			chr.AFFECT_CHINA_FIREWORK : (localeInfo.SKILL_POWERFUL_STRIKE, "d:/ymir work/ui/skill/common/affect/powerfulstrike.sub",),

			#64 - END
			chr.NEW_AFFECT_EXP_BONUS : (localeInfo.TOOLTIP_MALL_EXPBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/exp_bonus.sub",),

			chr.NEW_AFFECT_ITEM_BONUS : (localeInfo.TOOLTIP_MALL_ITEMBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/item_bonus.sub",),
			chr.NEW_AFFECT_SAFEBOX : (localeInfo.TOOLTIP_MALL_SAFEBOX, "d:/ymir work/ui/skill/common/affect/safebox.sub",),
			chr.NEW_AFFECT_AUTOLOOT : (localeInfo.TOOLTIP_MALL_AUTOLOOT, "d:/ymir work/ui/skill/common/affect/autoloot.sub",),
			chr.NEW_AFFECT_FISH_MIND : (localeInfo.TOOLTIP_MALL_FISH_MIND, "d:/ymir work/ui/skill/common/affect/fishmind.sub",),
			chr.NEW_AFFECT_MARRIAGE_FAST : (localeInfo.TOOLTIP_MALL_MARRIAGE_FAST, "d:/ymir work/ui/skill/common/affect/marriage_fast.sub",),
			chr.NEW_AFFECT_GOLD_BONUS : (localeInfo.TOOLTIP_MALL_GOLDBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/gold_bonus.sub",),

			chr.NEW_AFFECT_NO_DEATH_PENALTY : (localeInfo.TOOLTIP_APPLY_NO_DEATH_PENALTY, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
			chr.NEW_AFFECT_SKILL_BOOK_BONUS : (localeInfo.TOOLTIP_APPLY_SKILL_BOOK_BONUS, "d:/ymir work/ui/skill/common/affect/citit.tga"),
			chr.NEW_AFFECT_SKILL_BOOK_NO_DELAY : (localeInfo.TOOLTIP_APPLY_SKILL_BOOK_NO_DELAY, "d:/ymir work/ui/skill/common/affect/exo.tga"),

			chr.NEW_AFFECT_AUTO_HP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/skill/common/affect/red.tga"),
			chr.NEW_AFFECT_AUTO_SP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/skill/common/affect/blue.tga"),
			#chr.NEW_AFFECT_AUTO_HP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
			#chr.NEW_AFFECT_AUTO_SP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/skill/common/affect/gold_bonus.sub"),

			MALL_DESC_IDX_START+player.POINT_MALL_ATTBONUS : (localeInfo.TOOLTIP_MALL_ATTBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/att_bonus.sub",),
			MALL_DESC_IDX_START+player.POINT_MALL_DEFBONUS : (localeInfo.TOOLTIP_MALL_DEFBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/def_bonus.sub",),
			MALL_DESC_IDX_START+player.POINT_MALL_EXPBONUS : (localeInfo.TOOLTIP_MALL_EXPBONUS, "d:/ymir work/ui/skill/common/affect/exp.tga",),
			MALL_DESC_IDX_START+player.POINT_MALL_ITEMBONUS : (localeInfo.TOOLTIP_MALL_ITEMBONUS, "d:/ymir work/ui/skill/common/affect/Manusile_Talharului.tga",),
			MALL_DESC_IDX_START+player.POINT_MALL_GOLDBONUS : (localeInfo.TOOLTIP_MALL_GOLDBONUS, "d:/ymir work/ui/skill/common/affect/Medalia_Norocului.tga",),
			MALL_DESC_IDX_START+player.POINT_CRITICAL_PCT : (localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,"d:/ymir work/ui/skill/common/affect/critical.sub"),
			MALL_DESC_IDX_START+player.POINT_PENETRATE_PCT : (localeInfo.TOOLTIP_APPLY_PENETRATE_PCT, "d:/ymir work/ui/skill/common/affect/patrunzatoare.tga"),
			MALL_DESC_IDX_START+player.POINT_MAX_HP_PCT : (localeInfo.TOOLTIP_MAX_HP_PCT, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
			MALL_DESC_IDX_START+player.POINT_MAX_SP_PCT : (localeInfo.TOOLTIP_MAX_SP_PCT, "d:/ymir work/ui/skill/common/affect/maxpm.tga"),

			621 : ( localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,	"icon/item/50821.tga",),
			622 : ( localeInfo.TOOLTIP_APPLY_PENETRATE_PCT,	"icon/item/50822.tga",),
			623 : ( localeInfo.TOOLTIP_ATT_SPEED,				"icon/item/50823.tga",),
			624 : ( localeInfo.TOOLTIP_RESIST_MAGIC,			"icon/item/50824.tga",),
			625 : ( localeInfo.TOOLTIP_ATT_GRADE,				"icon/item/50825.tga",),
			626 : ( localeInfo.TOOLTIP_DEF_GRADE,				"icon/item/50826.tga",),

			BLEND_IDX_START + 53 : ( localeInfo.TOOLTIP_APPLY_ATTBONUS_MONSTER,				"icon/item/2200541.png",),
			BLEND_IDX_START + 12 : ( localeInfo.TOOLTIP_SKILL_DEFEND_BONUS,				"icon/item/2200542.png",),
			BLEND_IDX_START + 12 : ( localeInfo.TOOLTIP_NORMAL_HIT_DEFEND_BONUS,				"icon/item/2200544.png",),
			BLEND_IDX_START + 60 : ( localeInfo.TOOLTIP_NORMAL_HIT_DEFEND_BONUS,				"icon/item/2200546.png",),
			BLEND_IDX_START + 43 : ( localeInfo.TOOLTIP_APPLY_ATTBONUS_HUMAN,				"icon/item/2200547.png",),
			BLEND_IDX_START + 12 : ( localeInfo.TOOLTIP_NORMAL_HIT_DAMAGE_BONUS,				"icon/item/50183.tga",),
			
			WATER_IDX_START + 41 : 	( localeInfo.TOOLTIP_APPLY_PENETRATE_PCT,		"icon/item/50813.tga",),
			WATER_IDX_START + 40 : 	( localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,		"icon/item/50814.tga",),
			WATER_IDX_START + 95 : 	( localeInfo.TOOLTIP_ATT_GRADE,					"icon/item/50817.tga",),
			WATER_IDX_START + 96 : 	( localeInfo.TOOLTIP_DEF_GRADE,					"icon/item/50818.tga",),
			WATER_IDX_START + 77 : 	( localeInfo.TOOLTIP_MAGIC_DEF_GRADE,			"icon/item/50819.tga",),
			WATER_IDX_START + 17 :	( localeInfo.TOOLTIP_ATT_SPEED,					"icon/item/50820.tga",),	
			
			SITE_IDX_START + player.POINT_MAX_HP_PCT 			: (localeInfo.TOOLTIP_MAX_HP_PCT, 				"icon/item/71027.tga",),
			SITE_IDX_START + player.POINT_MAX_SP_PCT 			: (localeInfo.TOOLTIP_MAX_SP_PCT, 					"icon/item/71029.tga",),
			SITE_IDX_START + 93 								: (localeInfo.TOOLTIP_MALL_ATTBONUS_STATIC, 		"icon/item/71028.tga",),
			SITE_IDX_START + player.POINT_MALL_DEFBONUS 		: (localeInfo.TOOLTIP_MALL_DEFBONUS_STATIC, 	"icon/item/71030.tga",),
			SITE_IDX_START + player.POINT_CRITICAL_PCT 			: (localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,			"icon/item/71044.tga"),
			SITE_IDX_START + player.POINT_PENETRATE_PCT 		: (localeInfo.TOOLTIP_APPLY_PENETRATE_PCT,		"icon/item/71045.tga"),
			SITE_IDX_START + 43 								: (localeInfo.TOOLTIP_APPLY_ATTBONUS_HUMAN,			"icon/item/51002.tga",),


	}
	if app.ENABLE_DRAGON_SOUL_SYSTEM:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_DRAGON_SOUL_DECK1] = (localeInfo.TOOLTIP_DRAGON_SOUL_DECK1, "d:/ymir work/ui/dragonsoul/buff_ds_sky1.tga")
		AFFECT_DATA_DICT[chr.NEW_AFFECT_DRAGON_SOUL_DECK2] = (localeInfo.TOOLTIP_DRAGON_SOUL_DECK2, "d:/ymir work/ui/dragonsoul/buff_ds_land1.tga")

	def __init__(self):
		ui.Window.__init__(self)

		self.serverPlayTime=0
		self.clientPlayTime=0

		self.lastUpdateTime=0
		self.affectImageDict={}
		self.skillAffectDict={}
		self.horseImage=None
		self.lovePointImage=None
		self.autoPotionImageHP = AutoPotionImage()
		self.autoPotionImageSP = AutoPotionImage()
		self.SetPosition(10, 10)
		self.Show()

	def ClearAllAffects(self):
		self.horseImage=None
		self.lovePointImage=None
		self.affectImageDict={}
		self.__ArrangeImageList()

	def ClearAffects(self):
		self.living_affectImageDict=OrderedDict()
		for key, image in self.affectImageDict.items():
			if not image.IsSkillAffect():
				self.living_affectImageDict[key] = image
		self.affectImageDict = self.living_affectImageDict
		self.__ArrangeImageList()

	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):
		if type < 500:
			if type < 120:
				self.skillAffectDict[type] = app.GetGlobalTimeStamp() + duration

				i = 0
				affectIdx = player.SkillIndexToAffectIndex(type)
				while affectIdx != 0:
					i += 1
					if self.affectImageDict.has_key(affectIdx):
						self.affectImageDict[affectIdx].SetDuration(duration)
					affectIdx = player.SkillIndexToAffectIndex(type, i)

		if type == chr.NEW_AFFECT_MALL:
			if pointIdx == 116 or pointIdx == 117 or pointIdx == 118:
				affect = self.MALL_DESC_IDX_START + pointIdx
			else:
				affect = self.SITE_IDX_START + pointIdx

		if type == 510:
			affect = self.SITE_IDX_START + pointIdx
		elif type == 531:
			affect = self.BLEND_IDX_START + pointIdx
		elif type == 516:
			affect = self.WATER_IDX_START + pointIdx
		else:
			affect = type

		if self.affectImageDict.has_key(affect):
			return

		if not self.AFFECT_DATA_DICT.has_key(affect):
			return

		if affect == chr.NEW_AFFECT_NO_DEATH_PENALTY or\
		   affect == chr.NEW_AFFECT_SKILL_BOOK_BONUS or\
		   affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY or\
		   affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY or\
		   affect == chr.NEW_AFFECT_SKILL_BOOK_NO_DELAY:
			duration = 0

		affectData = self.AFFECT_DATA_DICT[affect]
		description = affectData[0]
		filename = affectData[1]

		if pointIdx == player.POINT_MALL_ITEMBONUS or\
		   pointIdx == player.POINT_MALL_GOLDBONUS:
			value = 1 + float(value) / 100.0

		if affect != chr.NEW_AFFECT_AUTO_SP_RECOVERY and affect != chr.NEW_AFFECT_AUTO_HP_RECOVERY:
			description = description(float(value))

		image = AffectImage()
		image.SetParent(self)

		image.LoadImage(filename)
		image.SetDescription(description)
		image.SetDuration(duration)
		image.SetAffect(affect)
		if affect == chr.NEW_AFFECT_EXP_BONUS_EURO_FREE or\
			affect == chr.NEW_AFFECT_EXP_BONUS_EURO_FREE_UNDER_15 or\
			self.INFINITE_AFFECT_DURATION < duration:
			image.SetClock(False)
			image.UpdateDescription()
		elif affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY or affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY:
			image.UpdateAutoPotionDescription()
		else:
			image.UpdateDescription()

		image.SetScale(0.7, 0.7)
		image.SetSkillAffectFlag(False)
		image.Show()
		self.affectImageDict[affect] = image
		self.__ArrangeImageList()

	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		if type == 510:
			affect = self.SITE_IDX_START + pointIdx		

		if type == chr.NEW_AFFECT_MALL:
			if pointIdx == 116 or pointIdx == 117 or pointIdx == 118:
				affect = self.MALL_DESC_IDX_START + pointIdx

		elif type == 531:
			affect = self.BLEND_IDX_START + pointIdx
		elif type == 516:
			affect = self.WATER_IDX_START + pointIdx	
		else:
			affect = type


		self.__RemoveAffect(affect)
		self.__ArrangeImageList()

	def SetAffect(self, affect):
		self.__AppendAffect(affect)
		self.__ArrangeImageList()

	def ResetAffect(self, affect):
		self.__RemoveAffect(affect)
		self.__ArrangeImageList()

	def SetLoverInfo(self, name, lovePoint):
		image = LovePointImage()
		image.SetParent(self)
		image.SetLoverInfo(name, lovePoint)
		self.lovePointImage = image
		self.__ArrangeImageList()

	def ShowLoverState(self):
		if self.lovePointImage:
			self.lovePointImage.Show()
			self.__ArrangeImageList()

	def HideLoverState(self):
		if self.lovePointImage:
			self.lovePointImage.Hide()
			self.__ArrangeImageList()

	def ClearLoverState(self):
		self.lovePointImage = None
		self.__ArrangeImageList()

	def OnUpdateLovePoint(self, lovePoint):
		if self.lovePointImage:
			self.lovePointImage.OnUpdateLovePoint(lovePoint)

	def SetHorseState(self, level, health, battery):
		if level==0:
			self.horseImage=None
			self.__ArrangeImageList()
		else:
			image = HorseImage()
			image.SetParent(self)
			image.SetState(level, health, battery)
			image.Show()

			self.horseImage=image
			self.__ArrangeImageList()

	def SetPlayTime(self, playTime):
		self.serverPlayTime = playTime
		self.clientPlayTime = app.GetTime()

	def __AppendAffect(self, affect):

		if self.affectImageDict.has_key(affect):
			return

		try:
			affectData = self.AFFECT_DATA_DICT[affect]
		except KeyError:
			return

		name = affectData[0]
		filename = affectData[1]

		skillIndex = player.AffectIndexToSkillIndex(affect)
		if 0 != skillIndex:
			name = skill.GetSkillName(skillIndex)

		image = AffectImage()
		image.SetParent(self)
		image.SetSkillAffectFlag(True)
		image.SetDescription(name)

		endTime = 0
		if self.skillAffectDict.has_key(skillIndex):
			endTime = self.skillAffectDict[skillIndex]
			image.SetDuration(endTime - app.GetGlobalTimeStamp())

		try:
			image.LoadImage(filename)
		except:
			pass

		#image.SetToolTipText(name, 0, 40)
		image.SetScale(0.7, 0.7)
		image.Show()
		self.affectImageDict[affect] = image

	def __RemoveAffect(self, affect):
		"""
		if affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY:
			self.autoPotionImageSP.Hide()

		if affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY:
			self.autoPotionImageHP.Hide()
		"""

		if not self.affectImageDict.has_key(affect):
			return

		del self.affectImageDict[affect]

		self.__ArrangeImageList()

	def __ArrangeImageList(self):
		width = len(self.affectImageDict) * self.IMAGE_STEP

		if self.lovePointImage:
			width += self.IMAGE_STEP

		if self.horseImage:
			width += self.IMAGE_STEP

		self.SetSize(width, 26)

		xPos = 0
		yPos = 0
		AffectCount = 0


		if self.lovePointImage:
			if self.lovePointImage.IsShow():
				self.lovePointImage.SetPosition(xPos, 0)
				xPos += self.IMAGE_STEP
				if constInfo.SHOW_AFFECT_TOOLTIP:
					AffectCount += 1

		if self.horseImage:
			self.horseImage.SetPosition(xPos, 0)
			xPos += self.IMAGE_STEP
			if constInfo.SHOW_AFFECT_TOOLTIP:
				AffectCount += 1

		for image in self.affectImageDict.values():
			image.SetPosition(xPos, yPos)
			AffectCount += 1
			xPos += self.IMAGE_STEP

			# if constInfo.SHOW_AFFECT_TOOLTIP:
			if AffectCount % 7 == 0:
				yPos += self.IMAGE_STEP
				xPos = 0

				self.SetSize(10 * self.IMAGE_STEP, yPos + self.IMAGE_STEP)

	def OnUpdate(self):
		try:
			if app.GetGlobalTime() - self.lastUpdateTime > 500:
			#if 0 < app.GetGlobalTime():
				self.lastUpdateTime = app.GetGlobalTime()

				for image in self.affectImageDict.values():
					if image.GetAffect() == chr.NEW_AFFECT_AUTO_HP_RECOVERY or image.GetAffect() == chr.NEW_AFFECT_AUTO_SP_RECOVERY:
						image.UpdateAutoPotionDescription()
						continue

					image.UpdateDescription()

		except Exception, e:
			print "AffectShower::OnUpdate error : ", e

