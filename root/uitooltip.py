import dbg
import player
import item
import grp
import wndMgr
import skill
import shop
import exchange
import grpText
import safebox
import localeInfo
import app
import background
import nonplayer
import chr
import chat
if app.BL_MAILBOX:
	import mail
import ui
import mouseModule
import constInfo
if app.ENABLE_ACCE_COSTUME_SYSTEM:
	import acce

if app.RENDER_TARGET:
	import renderTarget
	
SOCKET_REALTIME_INDEX = 2

WARP_SCROLLS = [22011, 22000, 22010]

DESC_DEFAULT_MAX_COLS = 26
DESC_WESTERN_MAX_COLS = 35
DESC_WESTERN_MAX_WIDTH = 220


def chop(n):
	return round(n - 0.5, 1)

if app.INGAME_WIKI:
	def GET_AFFECT_STRING(affType, affValue):
		if 0 == affType:
			return None
		
		try:
			affectString = ItemToolTip.AFFECT_DICT[affType]
			if type(affectString) != str:
				return affectString(affValue)

			if affectString.find("%d") != -1:
				return affectString % affValue
			else:
				return affectString
		except KeyError:
			return "UNKNOWN_TYPE[%s] %s" % (affType, affValue)
	
	
def pointop(n):
	t = int(n)
	if t / 10 < 1:
		return "0."+n
	else:		
		return n[0:len(n)-1]+"."+n[len(n)-1:]

def SplitDescription(desc, limit):
	total_tokens = desc.split()
	line_tokens = []
	line_len = 0
	lines = []
	for token in total_tokens:
		if "|" in token:
			sep_pos = token.find("|")
			line_tokens.append(token[:sep_pos])

			lines.append(" ".join(line_tokens))
			line_len = len(token) - (sep_pos + 1)
			line_tokens = [token[sep_pos+1:]]
		else:
			line_len += len(token)
			if len(line_tokens) + line_len > limit:
				lines.append(" ".join(line_tokens))
				line_len = len(token)
				line_tokens = [token]
			else:
				line_tokens.append(token)

	if line_tokens:
		lines.append(" ".join(line_tokens))

	return lines


PetVnum = {
	53001 : 34001,
	53003 : 34001,
	53004 : 34002,
	53005 : 34002,
	53010 : 34008,
	53011 : 34007,
	53012 : 34005,
	53013 : 34006,
	53017 : 34016,
	53025 : 34024,
	53256 : 34066,
	53242 : 34066,
	53243 : 34066,
	53244 : 34067,
	53245 : 34068,
	53246 : 34069,
	53247 : 34070,
	53248 : 34071,
	53249 : 34072,
	53250 : 34084,
	53251 : 34085,
	55701 : 34041,
	55702 : 34045,
	55703 : 34049,
	55704 : 34053,
	55705 : 34036,
	55706 : 34064,
	55707 : 34073,
	55708 : 34075,
	55709 : 34080,
	55710 : 34082,
	55711 : 34095,
	53263 : 34093,
	53264 : 34094,
	53282 : 34114,
	53283 : 34115,
	53026 : 34008,
	53027 : 34008,
	53028 : 34008,
	53029 : 34094,
	53030 : 34094,
	53031 : 34094,
	53252 : 34085,
	53253 : 34085,
	53248 : 34084,
	53249 : 34084
	#halloween
	, 48301 : 34100,
	48311 : 34100,
	48321 : 34100
	#end hallowee
	#patch3
	, 49010 : 34116
	#end patch3
	#patch4
	, 49050 : 34117
	#end patch4
	, 60101 : 34118
	, 60102 : 34118
	, 60103 : 34119
	, 60104 : 34119
}
###################################################################################################
## ToolTip
##
##   NOTE : ����� Item�� Skill�� ������� Ưȭ ���ѵξ���
##          ������ �״��� �ǹ̰� ���� ����
##
class ToolTip(ui.ThinBoard):

	TOOL_TIP_WIDTH = 190
	TOOL_TIP_HEIGHT = 10

	TEXT_LINE_HEIGHT = 17

	TITLE_COLOR = grp.GenerateColor(0.9490, 0.9058, 0.7568, 1.0)
	SPECIAL_TITLE_COLOR = grp.GenerateColor(1.0, 0.7843, 0.0, 1.0)
	NORMAL_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	FROZEN_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	FROZEN_2_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	FONT_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	PRICE_COLOR = 0xffFFB96D
	CHANGELOOK_ITEMNAME_COLOR = 0xffBCE55C
	HIGH_PRICE_COLOR = SPECIAL_TITLE_COLOR
	MIDDLE_PRICE_COLOR = grp.GenerateColor(0.85, 0.85, 0.85, 1.0)
	LOW_PRICE_COLOR = grp.GenerateColor(0.7, 0.7, 0.7, 1.0)
	WON_PRICE_COLOR = grp.GenerateColor(0.11, 0.56, 1.0, 1.0)
	PRICE_INFO_COLOR = grp.GenerateColor(1.0, 0.88, 0.0, 1.0)
	ENABLE_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	DISABLE_COLOR = grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0)

	NEGATIVE_COLOR = grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0)
	POSITIVE_COLOR = grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0)
	SPECIAL_POSITIVE_COLOR = grp.GenerateColor(0.6911, 0.8754, 0.7068, 1.0)
	SPECIAL_POSITIVE_COLOR2 = grp.GenerateColor(0.8824, 0.9804, 0.8824, 1.0)
	if app.ENABLE_6_7_BONUS_NEW_SYSTEM:
		ATTR_6TH_7TH_COLOR = 0xffffff9a
	ITEM_BUFF_LEVEL_COLOR = 0xffffd300
	ITEM_BUFF_TYPE_COLOR = 0xfffc9c3a
	ITEM_BUFF_RATE_COLOR = 0xff40e0d0
	ITEM_BUFF_DURATION_COLOR = 0xffadff00
	ITEM_BUFF_USAGE_COLOR = 0xffffffff	
	CONDITION_COLOR = 0xffBEB47D
	CAN_LEVEL_UP_COLOR = 0xff8EC292
	CANNOT_LEVEL_UP_COLOR = DISABLE_COLOR
	NEED_SKILL_POINT_COLOR = 0xff9A9CDB

	def __init__(self, width = TOOL_TIP_WIDTH, isPickable=False):
		ui.ThinBoard.__init__(self, "TOP_MOST")

		if isPickable:
			pass
		else:
			self.AddFlag("not_pick")

		self.AddFlag("float")

		self.followFlag = True
		self.toolTipWidth = width

		self.xPos = -1
		self.yPos = -1

		self.defFontName = localeInfo.UI_DEF_FONT
		self.ClearToolTip()
		if app.__COMPARE_TOOLTIP__:
			self.CompareTooltip = None
			self.IsCompare = False
	def __del__(self):
		ui.ThinBoard.__del__(self)
		if app.__COMPARE_TOOLTIP__ and self.CompareTooltip:
			del self.CompareTooltip
	def ClearToolTip(self):
		self.toolTipHeight = 12
		self.childrenList = []

	def SetFollow(self, flag):
		self.followFlag = flag

	def SetDefaultFontName(self, fontName):
		self.defFontName = fontName

	def AppendSpace(self, size):
		self.toolTipHeight += size
		self.ResizeToolTip()
		
	if app.INGAME_WIKI:
		def SetThinBoardSize(self, width, height = 12):
			self.toolTipWidth = width 
			self.toolTipHeight = height


	def AppendHorizontalLine(self):

		for i in xrange(2):
			horizontalLine = ui.Line()
			horizontalLine.SetParent(self)
			horizontalLine.SetPosition(0, self.toolTipHeight + 3 + i)
			horizontalLine.SetWindowHorizontalAlignCenter()
			horizontalLine.SetSize(150, 0)
			horizontalLine.Show()

			if 0 == i:
				horizontalLine.SetColor(0xff555555)
			else:
				horizontalLine.SetColor(0xff000000)

			self.childrenList.append(horizontalLine)

		self.toolTipHeight += 11
		self.ResizeToolTip()

	if app.ENABLE_DUNGEON_INFO_SYSTEM:
		def TextAlignHorizonalCenter(self):
			for child in self.childrenList:
				(x, y) = child.GetLocalPosition()
				try:
					if child.GetText() != "":
						child.SetPosition(self.toolTipWidth / 2, y)
				except:
					pass

			self.ResizeToolTip()

	def AlignHorizonalCenter(self):
		for child in self.childrenList:
			(x, y)=child.GetLocalPosition()
			child.SetPosition(self.toolTipWidth/2, y)

		self.ResizeToolTip()

	def AutoAppendTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.Show()

		if centerAlign:
			textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()

		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)

		(textWidth, textHeight)=textLine.GetTextSize()

		textWidth += 40
		textHeight += 5

		if self.toolTipWidth < textWidth:
			self.toolTipWidth = textWidth

		self.toolTipHeight += textHeight

		return textLine

	def AutoAppendNewTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(FALSE)
		textLine.Show()
		if localeInfo.IsARABIC():
			textLine.SetHorizontalAlignRight()
		
		textLine.SetPosition(15, self.toolTipHeight)
		
		self.childrenList.append(textLine)
		(textWidth, textHeight) = textLine.GetTextSize()
		textWidth += 30
		textHeight += 10
		if self.toolTipWidth < textWidth:
			self.toolTipWidth = textWidth
		
		self.toolTipHeight += textHeight
		self.ResizeToolTipText(textWidth, self.toolTipHeight)
		return textLine

	def AppendTextLine(self, text, color = FONT_COLOR, centerAlign = TRUE, text2 = ""):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(FALSE)
		textLine.Show()

		if text2 != "":
			textLine2 = ui.TextLine()
			textLine2.SetParent(textLine)
			textLine2.SetFontName(self.defFontName)
			textLine2.SetPackedFontColor(self.HIGH_PRICE_COLOR)
			textLine2.SetText(text2)
			textLine2.SetOutline()
			textLine2.SetFeather(FALSE)
			textLine2.Show()

		if centerAlign:
			textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()

			if text2 != "":
				w, h = textLine.GetTextSize()
				w2, h2 = textLine2.GetTextSize()
				textLine2.SetPosition(w / 2 + w2 / 2 + 3, 0)
				textLine2.SetHorizontalAlignCenter()
		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)
		if text2 != "":
			self.childrenList.append(textLine2)

		self.toolTipHeight += self.TEXT_LINE_HEIGHT
		self.ResizeToolTip()

		return textLine

	def AppendDescription(self, desc, limit, color = FONT_COLOR):
		if localeInfo.IsEUROPE():
			self.__AppendDescription_WesternLanguage(desc, color)
		else:
			self.__AppendDescription_EasternLanguage(desc, limit, color)

	def __AppendDescription_EasternLanguage(self, description, characterLimitation, color=FONT_COLOR):
		length = len(description)
		if 0 == length:
			return

		lineCount = grpText.GetSplitingTextLineCount(description, characterLimitation)
		for i in xrange(lineCount):
			if 0 == i:
				self.AppendSpace(5)
			self.AppendTextLine(grpText.GetSplitingTextLine(description, characterLimitation, i), color)

	def __AppendDescription_WesternLanguage(self, desc, color=FONT_COLOR):
		lines = SplitDescription(desc, DESC_WESTERN_MAX_COLS)
		if not lines:
			return

		self.AppendSpace(5)
		for line in lines:
			self.AppendTextLine(line, color)


	def ResizeToolTip(self):
		self.SetSize(self.toolTipWidth, self.TOOL_TIP_HEIGHT + self.toolTipHeight)

	def ResizeToolTipText(self, x, y):
		self.SetSize(x, y)

	def SetTitle(self, name):
		self.AppendTextLine(name, self.TITLE_COLOR)

	if app.BL_MAILBOX:
		def SetThinBoardSize(self, width, height=12):
			self.toolTipWidth = width
			self.toolTipHeight = height

	def GetLimitTextLineColor(self, curValue, limitValue):
		if curValue < limitValue:
			return self.DISABLE_COLOR

		return self.ENABLE_COLOR

	def GetChangeTextLineColor(self, value, isSpecial=False):
		if value > 0:
			if isSpecial:
				return self.SPECIAL_POSITIVE_COLOR
			else:
				return self.POSITIVE_COLOR

		if 0 == value:
			return self.NORMAL_COLOR

		return self.NEGATIVE_COLOR

	def SetToolTipPosition(self, x = -1, y = -1):
		self.xPos = x
		self.yPos = y

	def ShowToolTip(self):
		self.SetTop()
		self.Show()

		self.OnUpdate()

	def HideToolTip(self):
		self.Hide()
		if app.__COMPARE_TOOLTIP__ and self.CompareTooltip:
			for_check = ItemToolTip()
			if constInfo.automatic_check == 0:
				constInfo.automatic_check = 1
			constInfo.Compared = 0
			self.CompareTooltip.Hide()

	def OnUpdate(self):

		if not self.followFlag:
			return

		x = 0
		y = 0
		width = self.GetWidth()
		height = self.toolTipHeight

		if -1 == self.xPos and -1 == self.yPos:

			(mouseX, mouseY) = wndMgr.GetMousePosition()

			if mouseY < wndMgr.GetScreenHeight() - 300:
				y = mouseY + 40
			else:
				y = mouseY - height - 30

			x = mouseX - width/2

		else:

			x = self.xPos - width/2
			y = self.yPos - height

		x = max(x, 0)
		y = max(y, 0)
		x = min(x + width/2, wndMgr.GetScreenWidth() - width/2) - width/2
		y = min(y + self.GetHeight(), wndMgr.GetScreenHeight()) - self.GetHeight()

		parentWindow = self.GetParentProxy()
		if parentWindow:
			(gx, gy) = parentWindow.GetGlobalPosition()
			x -= gx
			y -= gy
		if app.__COMPARE_TOOLTIP__:
			if self.IsCompare:
				return
			if self.CompareTooltip:
				val = [0] * 2
				if x < self.CompareTooltip.GetWidth():
					val[0] = self.GetWidth()
				else:
					val[0] = -self.CompareTooltip.GetWidth()
				CompareHeight = wndMgr.GetScreenHeight() - self.CompareTooltip.GetHeight()
				if y > CompareHeight:
					val[1] = CompareHeight - y
				elif y < 0:
					val[1] = 0 - y
				self.CompareTooltip.SetPosition(x + val[0], y + val[1])
		self.SetPosition(x, y)

class ItemToolTip(ToolTip):

	if app.RENDER_TARGET:
		automatic = 1
		#confiuger by yourself
		#how to configure
		#item_vnum : model_vnum
		if app.RENDER_TARGET:
			MountRender = {
				71127:20117,
				52062:20213,
				71127:20117,
				71128:20118,
			}
			
			PetRender = {
				53005:34004,
				55704:34053,
				55703:34049,
			}
		ModelPreviewBoard = None
		ModelPreview = None
		ModelPreviewText = None


	if app.ENABLE_SEND_TARGET_INFO:
		isStone = False
		isBook = False
		isBook2 = False

	CHARACTER_NAMES = (
		localeInfo.TOOLTIP_WARRIOR,
		localeInfo.TOOLTIP_ASSASSIN,
		localeInfo.TOOLTIP_SURA,
		localeInfo.TOOLTIP_SHAMAN
	)
	if app.ENABLE_WOLFMAN_CHARACTER:
		CHARACTER_NAMES += (
			localeInfo.TOOLTIP_WOLFMAN,
		)

	CHARACTER_COUNT = len(CHARACTER_NAMES)
	WEAR_NAMES = (
		localeInfo.TOOLTIP_ARMOR,
		localeInfo.TOOLTIP_HELMET,
		localeInfo.TOOLTIP_SHOES,
		localeInfo.TOOLTIP_WRISTLET,
		localeInfo.TOOLTIP_WEAPON,
		localeInfo.TOOLTIP_NECK,
		localeInfo.TOOLTIP_EAR,
		localeInfo.TOOLTIP_UNIQUE,
		localeInfo.TOOLTIP_SHIELD,
		localeInfo.TOOLTIP_ARROW,
	)
	WEAR_COUNT = len(WEAR_NAMES)

	AFFECT_DICT = {
		item.APPLY_MAX_HP : localeInfo.TOOLTIP_MAX_HP,
		item.APPLY_MAX_SP : localeInfo.TOOLTIP_MAX_SP,
		item.APPLY_CON : localeInfo.TOOLTIP_CON,
		item.APPLY_INT : localeInfo.TOOLTIP_INT,
		item.APPLY_STR : localeInfo.TOOLTIP_STR,
		item.APPLY_DEX : localeInfo.TOOLTIP_DEX,
		item.APPLY_ATT_SPEED : localeInfo.TOOLTIP_ATT_SPEED,
		item.APPLY_MOV_SPEED : localeInfo.TOOLTIP_MOV_SPEED,
		item.APPLY_CAST_SPEED : localeInfo.TOOLTIP_CAST_SPEED,
		item.APPLY_HP_REGEN : localeInfo.TOOLTIP_HP_REGEN,
		item.APPLY_SP_REGEN : localeInfo.TOOLTIP_SP_REGEN,
		item.APPLY_POISON_PCT : localeInfo.TOOLTIP_APPLY_POISON_PCT,
		item.APPLY_STUN_PCT : localeInfo.TOOLTIP_APPLY_STUN_PCT,
		item.APPLY_SLOW_PCT : localeInfo.TOOLTIP_APPLY_SLOW_PCT,
		item.APPLY_CRITICAL_PCT : localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,
		item.APPLY_PENETRATE_PCT : localeInfo.TOOLTIP_APPLY_PENETRATE_PCT,

		item.APPLY_ATTBONUS_WARRIOR : localeInfo.TOOLTIP_APPLY_ATTBONUS_WARRIOR,
		item.APPLY_ATTBONUS_ASSASSIN : localeInfo.TOOLTIP_APPLY_ATTBONUS_ASSASSIN,
		item.APPLY_ATTBONUS_SURA : localeInfo.TOOLTIP_APPLY_ATTBONUS_SURA,
		item.APPLY_ATTBONUS_SHAMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_SHAMAN,
		item.APPLY_ATTBONUS_MONSTER : localeInfo.TOOLTIP_APPLY_ATTBONUS_MONSTER,

		item.APPLY_ATTBONUS_HUMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_HUMAN,
		item.APPLY_ATTBONUS_ANIMAL : localeInfo.TOOLTIP_APPLY_ATTBONUS_ANIMAL,
		item.APPLY_ATTBONUS_ORC : localeInfo.TOOLTIP_APPLY_ATTBONUS_ORC,
		item.APPLY_ATTBONUS_MILGYO : localeInfo.TOOLTIP_APPLY_ATTBONUS_MILGYO,
		item.APPLY_ATTBONUS_UNDEAD : localeInfo.TOOLTIP_APPLY_ATTBONUS_UNDEAD,
		item.APPLY_ATTBONUS_DEVIL : localeInfo.TOOLTIP_APPLY_ATTBONUS_DEVIL,
		item.APPLY_ATTBONUS_BOSS : localeInfo.TOOLTIP_ATTBONUS_BOSS,
		item.APPLY_ATTBONUS_METIN : localeInfo.TOOLTIP_ATTBONUS_METIN,
		item.APPLY_STEAL_HP : localeInfo.TOOLTIP_APPLY_STEAL_HP,
		item.APPLY_STEAL_SP : localeInfo.TOOLTIP_APPLY_STEAL_SP,
		item.APPLY_MANA_BURN_PCT : localeInfo.TOOLTIP_APPLY_MANA_BURN_PCT,
		item.APPLY_DAMAGE_SP_RECOVER : localeInfo.TOOLTIP_APPLY_DAMAGE_SP_RECOVER,
		item.APPLY_BLOCK : localeInfo.TOOLTIP_APPLY_BLOCK,
		item.APPLY_DODGE : localeInfo.TOOLTIP_APPLY_DODGE,
		item.APPLY_RESIST_SWORD : localeInfo.TOOLTIP_APPLY_RESIST_SWORD,
		item.APPLY_RESIST_TWOHAND : localeInfo.TOOLTIP_APPLY_RESIST_TWOHAND,
		item.APPLY_RESIST_DAGGER : localeInfo.TOOLTIP_APPLY_RESIST_DAGGER,
		item.APPLY_RESIST_BELL : localeInfo.TOOLTIP_APPLY_RESIST_BELL,
		item.APPLY_RESIST_FAN : localeInfo.TOOLTIP_APPLY_RESIST_FAN,
		item.APPLY_RESIST_BOW : localeInfo.TOOLTIP_RESIST_BOW,
		item.APPLY_RESIST_FIRE : localeInfo.TOOLTIP_RESIST_FIRE,
		item.APPLY_RESIST_ELEC : localeInfo.TOOLTIP_RESIST_ELEC,
		item.APPLY_RESIST_MAGIC : localeInfo.TOOLTIP_RESIST_MAGIC,
		item.APPLY_RESIST_WIND : localeInfo.TOOLTIP_APPLY_RESIST_WIND,
		item.APPLY_REFLECT_MELEE : localeInfo.TOOLTIP_APPLY_REFLECT_MELEE,
		item.APPLY_REFLECT_CURSE : localeInfo.TOOLTIP_APPLY_REFLECT_CURSE,
		item.APPLY_POISON_REDUCE : localeInfo.TOOLTIP_APPLY_POISON_REDUCE,
		item.APPLY_KILL_SP_RECOVER : localeInfo.TOOLTIP_APPLY_KILL_SP_RECOVER,
		item.APPLY_EXP_DOUBLE_BONUS : localeInfo.TOOLTIP_APPLY_EXP_DOUBLE_BONUS,
		item.APPLY_GOLD_DOUBLE_BONUS : localeInfo.TOOLTIP_APPLY_GOLD_DOUBLE_BONUS,
		item.APPLY_ITEM_DROP_BONUS : localeInfo.TOOLTIP_APPLY_ITEM_DROP_BONUS,
		item.APPLY_POTION_BONUS : localeInfo.TOOLTIP_APPLY_POTION_BONUS,
		item.APPLY_KILL_HP_RECOVER : localeInfo.TOOLTIP_APPLY_KILL_HP_RECOVER,
		item.APPLY_IMMUNE_STUN : localeInfo.TOOLTIP_APPLY_IMMUNE_STUN,
		item.APPLY_IMMUNE_SLOW : localeInfo.TOOLTIP_APPLY_IMMUNE_SLOW,
		item.APPLY_IMMUNE_FALL : localeInfo.TOOLTIP_APPLY_IMMUNE_FALL,
		item.APPLY_BOW_DISTANCE : localeInfo.TOOLTIP_BOW_DISTANCE,
		item.APPLY_DEF_GRADE_BONUS : localeInfo.TOOLTIP_DEF_GRADE,
		item.APPLY_ATT_GRADE_BONUS : localeInfo.TOOLTIP_ATT_GRADE,
		item.APPLY_MAGIC_ATT_GRADE : localeInfo.TOOLTIP_MAGIC_ATT_GRADE,
		item.APPLY_MAGIC_DEF_GRADE : localeInfo.TOOLTIP_MAGIC_DEF_GRADE,
		item.APPLY_MAX_STAMINA : localeInfo.TOOLTIP_MAX_STAMINA,
		item.APPLY_MALL_ATTBONUS : localeInfo.TOOLTIP_MALL_ATTBONUS,
		item.APPLY_MALL_DEFBONUS : localeInfo.TOOLTIP_MALL_DEFBONUS,
		item.APPLY_MALL_EXPBONUS : localeInfo.TOOLTIP_MALL_EXPBONUS,
		item.APPLY_MALL_ITEMBONUS : localeInfo.TOOLTIP_MALL_ITEMBONUS,
		item.APPLY_MALL_GOLDBONUS : localeInfo.TOOLTIP_MALL_GOLDBONUS,
		item.APPLY_SKILL_DAMAGE_BONUS : localeInfo.TOOLTIP_SKILL_DAMAGE_BONUS,
		item.APPLY_NORMAL_HIT_DAMAGE_BONUS : localeInfo.TOOLTIP_NORMAL_HIT_DAMAGE_BONUS,
		item.APPLY_SKILL_DEFEND_BONUS : localeInfo.TOOLTIP_SKILL_DEFEND_BONUS,
		item.APPLY_NORMAL_HIT_DEFEND_BONUS : localeInfo.TOOLTIP_NORMAL_HIT_DEFEND_BONUS,
		item.APPLY_PC_BANG_EXP_BONUS : localeInfo.TOOLTIP_MALL_EXPBONUS_P_STATIC,
		item.APPLY_PC_BANG_DROP_BONUS : localeInfo.TOOLTIP_MALL_ITEMBONUS_P_STATIC,
		item.APPLY_RESIST_WARRIOR : localeInfo.TOOLTIP_APPLY_RESIST_WARRIOR,
		item.APPLY_RESIST_ASSASSIN : localeInfo.TOOLTIP_APPLY_RESIST_ASSASSIN,
		item.APPLY_RESIST_SURA : localeInfo.TOOLTIP_APPLY_RESIST_SURA,
		item.APPLY_RESIST_SHAMAN : localeInfo.TOOLTIP_APPLY_RESIST_SHAMAN,
		item.APPLY_MAX_HP_PCT : localeInfo.TOOLTIP_APPLY_MAX_HP_PCT,
		item.APPLY_MAX_SP_PCT : localeInfo.TOOLTIP_APPLY_MAX_SP_PCT,
		item.APPLY_ENERGY : localeInfo.TOOLTIP_ENERGY,
		item.APPLY_COSTUME_ATTR_BONUS : localeInfo.TOOLTIP_COSTUME_ATTR_BONUS,

		item.APPLY_MAGIC_ATTBONUS_PER : localeInfo.TOOLTIP_MAGIC_ATTBONUS_PER,
		item.APPLY_MELEE_MAGIC_ATTBONUS_PER : localeInfo.TOOLTIP_MELEE_MAGIC_ATTBONUS_PER,
		item.APPLY_RESIST_ICE : localeInfo.TOOLTIP_RESIST_ICE,
		item.APPLY_RESIST_EARTH : localeInfo.TOOLTIP_RESIST_EARTH,
		item.APPLY_RESIST_DARK : localeInfo.TOOLTIP_RESIST_DARK,
		item.APPLY_ANTI_CRITICAL_PCT : localeInfo.TOOLTIP_ANTI_CRITICAL_PCT,
		item.APPLY_ANTI_PENETRATE_PCT : localeInfo.TOOLTIP_ANTI_PENETRATE_PCT,
	}
	if app.ENABLE_WOLFMAN_CHARACTER:
		AFFECT_DICT.update({
			item.APPLY_BLEEDING_PCT : localeInfo.TOOLTIP_APPLY_BLEEDING_PCT,
			item.APPLY_BLEEDING_REDUCE : localeInfo.TOOLTIP_APPLY_BLEEDING_REDUCE,
			item.APPLY_ATTBONUS_WOLFMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_WOLFMAN,
			item.APPLY_RESIST_CLAW : localeInfo.TOOLTIP_APPLY_RESIST_CLAW,
			item.APPLY_RESIST_WOLFMAN : localeInfo.TOOLTIP_APPLY_RESIST_WOLFMAN,
		})

	if app.ENABLE_MAGIC_REDUCTION_SYSTEM:
		AFFECT_DICT.update({
			item.APPLY_RESIST_MAGIC_REDUCTION : localeInfo.TOOLTIP_RESIST_MAGIC_REDUCTION,
		})

	if app.ENABLE_NEW_TALISMAN_GF:
		AFFECT_DICT.update({
			item.APPLY_ATTBONUS_ELEC : localeInfo.TOOLTIP_APPLY_ATTBONUS_ELEC,
			item.APPLY_ATTBONUS_FIRE : localeInfo.TOOLTIP_APPLY_ATTBONUS_FIRE,
			item.APPLY_ATTBONUS_ICE : localeInfo.TOOLTIP_APPLY_ATTBONUS_ICE,
			item.APPLY_ATTBONUS_WIND : localeInfo.TOOLTIP_APPLY_ATTBONUS_WIND,
			item.APPLY_ATTBONUS_EARTH : localeInfo.TOOLTIP_APPLY_ATTBONUS_EARTH,
			item.APPLY_ATTBONUS_DARK : localeInfo.TOOLTIP_APPLY_ATTBONUS_DARK,
			item.APPLY_RESIST_HUMAN : localeInfo.TOOLTIP_APPLY_RESIST_HUMAN,
			item.APPLY_RESIST_SWORD_REDUCTION : localeInfo.TOOLTIP_APPLY_RESIST_SWORD_REDUCTION,
			item.APPLY_RESIST_TWOHAND_REDUCTION: localeInfo.TOOLTIP_APPLY_RESIST_TWOHAND_REDUCTION,
			item.APPLY_RESIST_DAGGER_REDUCTION : localeInfo.TOOLTIP_APPLY_RESIST_DAGGER_REDUCTION,
			item.APPLY_RESIST_BELL_REDUCTION : localeInfo.TOOLTIP_APPLY_RESIST_BELL_REDUCTION,
			item.APPLY_RESIST_FAN_REDUCTION : localeInfo.TOOLTIP_APPLY_RESIST_FAN_REDUCTION,
			item.APPLY_RESIST_BOW_REDUCTION : localeInfo.TOOLTIP_APPLY_RESIST_BOW_REDUCTION,
			item.APPLY_ATTBONUS_ZODIAC : localeInfo.TOOLTIP_APPLY_ATTBONUS_ZODIAC,
			item.APPLY_ATTBONUS_DESERT : localeInfo.TOOLTIP_APPLY_ATTBONUS_DESERT,
			item.APPLY_ATTBONUS_INSECT : localeInfo.TOOLTIP_APPLY_ATTBONUS_INSECT,
			
		})

	if app.ENABLE_WOLFMAN_CHARACTER and app.ENABLE_NEW_TALISMAN_GF:
		AFFECT_DICT.update({
			item.APPLY_RESIST_CLAW_REDUCTION : localeInfo.TOOLTIP_APPLY_RESIST_CLAW_REDUCTION,
		})

	ATTRIBUTE_NEED_WIDTH = {
		23 : 230,
		24 : 230,
		25 : 230,
		26 : 220,
		27 : 210,

		35 : 210,
		36 : 210,
		37 : 210,
		38 : 210,
		39 : 210,
		40 : 210,
		41 : 210,

		42 : 220,
		43 : 230,
		45 : 230,
	}

	ANTI_FLAG_DICT = {
		0 : item.ITEM_ANTIFLAG_WARRIOR,
		1 : item.ITEM_ANTIFLAG_ASSASSIN,
		2 : item.ITEM_ANTIFLAG_SURA,
		3 : item.ITEM_ANTIFLAG_SHAMAN,
	}
	if app.ENABLE_WOLFMAN_CHARACTER:
		ANTI_FLAG_DICT.update({
			4 : item.ITEM_ANTIFLAG_WOLFMAN,
		})

	FONT_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)

	def __init__(self, *args, **kwargs):
		ToolTip.__init__(self, *args, **kwargs)
		self.itemVnum = 0
		self.isShopItem = False
		# BEGIN_OFFLINE_SHOP
		self.isOfflineShopItem = False
		# END_OF_OFFLINE_SHOP
		# ������ ������ ǥ���� �� ���� ĳ���Ͱ� ������ �� ���� �������̶�� ������ Disable Color�� ���� (�̹� �׷��� �۵��ϰ� ������ ���� �� �ʿ䰡 �־)
		self.bCannotUseItemForceSetDisableColor = True

	if app.RENDER_TARGET:

		def GetAutomatic(self):
			return constInfo.automatic_check

		def CanViewRendering(self):
			race = player.GetRace()
			job = chr.RaceToJob(race)
			if not self.ANTI_FLAG_DICT.has_key(job):
				return False
			if item.IsAntiFlag(self.ANTI_FLAG_DICT[job]):
				return False
			sex = chr.RaceToSex(race)
			MALE = 1
			FEMALE = 0
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and sex == MALE:
				return False
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and sex == FEMALE:
				return False
			return True
		def CanViewRenderingSex(self):
			race = player.GetRace()
			sex = chr.RaceToSex(race)
			MALE = 1
			FEMALE = 0
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and sex == MALE:
				return False
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and sex == FEMALE:
				return False
			return True

	def __del__(self):
		ToolTip.__del__(self)

	def SetCannotUseItemForceSetDisableColor(self, enable):
		self.bCannotUseItemForceSetDisableColor = enable

	def CanEquip(self):
		if not item.IsEquipmentVID(self.itemVnum):
			return True

		race = player.GetRace()
		job = chr.RaceToJob(race)
		if not self.ANTI_FLAG_DICT.has_key(job):
			return False

		if item.IsAntiFlag(self.ANTI_FLAG_DICT[job]):
			return False

		sex = chr.RaceToSex(race)

		MALE = 1
		FEMALE = 0

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and sex == MALE:
			return False

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and sex == FEMALE:
			return False

		for i in xrange(item.LIMIT_MAX_NUM):
			(limitType, limitValue) = item.GetLimit(i)

			if item.LIMIT_LEVEL == limitType:
				if player.GetStatus(player.LEVEL) < limitValue:
					return False
			"""
			elif item.LIMIT_STR == limitType:
				if player.GetStatus(player.ST) < limitValue:
					return False
			elif item.LIMIT_DEX == limitType:
				if player.GetStatus(player.DX) < limitValue:
					return False
			elif item.LIMIT_INT == limitType:
				if player.GetStatus(player.IQ) < limitValue:
					return False
			elif item.LIMIT_CON == limitType:
				if player.GetStatus(player.HT) < limitValue:
					return False
			"""

		return True

	def AppendTextLine(self, text, color = FONT_COLOR, centerAlign = TRUE, text2 = ""):
		if not self.CanEquip() and self.bCannotUseItemForceSetDisableColor:
			color = self.DISABLE_COLOR

		return ToolTip.AppendTextLine(self, text, color, centerAlign, text2)

	if app.__COMPARE_TOOLTIP__:
		def SetCompareItem(self, itemVnum):
			slotIndex = item.GetCompareIndex(itemVnum)
			if slotIndex and (player.GetItemIndex(slotIndex) > 0):
				if not self.CompareTooltip:
					self.CompareTooltip = ItemToolTip()
					self.CompareTooltip.IsCompare = True

				automatic_check = self.GetAutomatic()
				if automatic_check == 1:
					constInfo.automatic_check = 0
				constInfo.Compared = 1
				self.CompareTooltip.SetInventoryItem(slotIndex, player.INVENTORY, False)
				self.CompareTooltip.AutoAppendTextLine("Attualmente Equipaggiato", 0xffADFF2F)
				self.CompareTooltip.ResizeToolTip()
	

	def ClearToolTip(self):
		self.isShopItem = False
		self.toolTipWidth = self.TOOL_TIP_WIDTH
		ToolTip.ClearToolTip(self)
		# BEGIN_OFFLINE_SHOP
		self.isOfflineShopItem = False
		# END_OF_OFFLINE_SHOP

	def SetInventoryItem(self, slotIndex, window_type = player.INVENTORY, CompareItem = True):
		itemVnum = player.GetItemIndex(window_type, slotIndex)
		
		if 0 == itemVnum:
			return

		self.ClearToolTip()
		if shop.IsOpen():
			# BEGIN_OFFLINE_SHOP
			if not shop.IsPrivateShop() or not shop.IsOfflineShop():
			# END_OF_OFFLINE_SHOP
				item.SelectItem(itemVnum)
				self.AppendSellingPrice(player.GetISellItemPrice(window_type, slotIndex))

		metinSlot = [player.GetItemMetinSocket(window_type, slotIndex, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
		attrSlot = [player.GetItemAttribute(window_type, slotIndex, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

		if app.ENABLE_CHANGELOOK_SYSTEM:
			if app.RENDER_TARGET:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 0, 0, 0, player.INVENTORY, slotIndex)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, player.INVENTORY, slotIndex)
		else:
			if app.RENDER_TARGET:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 0)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot)

		if app.__COMPARE_TOOLTIP__ and app.IsPressed(app.DIK_LALT) and not slotIndex >= player.EQUIPMENT_SLOT_START and CompareItem:
			self.SetCompareItem(itemVnum)
		
		if app.GAMEMASTER_ITEMVAULE_TOOLTIP and chr.IsGameMaster():
			self.AppendTextLine("Value item %s" % (str(itemVnum)), self.SPECIAL_TITLE_COLOR)

	if app.ENABLE_OFFLINE_SHOP_SYSTEM:
		def SetOfflineShopBuilderItem(self, invenType, invenPos, offlineShopIndex):
			itemVnum = player.GetItemIndex(invenType, invenPos)

			if itemVnum == 0:
				return
			item.SelectItem(itemVnum)

			self.ClearToolTip()

			if app.ENABLE_CHEQUE_SYSTEM:
				self.AppendSellInfoText()

				self.AppendSellingChequePrice(shop.GetOfflineShopItemCheque(invenType, invenPos))

			self.AppendSellingPrice(shop.GetOfflineShopItemPrice2(invenType, invenPos))

			metinSlot = []

			# import chat

			# chat.AppendChat(7, "invenType %d invenPos: %d" % (invenType, invenPos))

			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(player.GetItemMetinSocket(invenType, invenPos, i))

			attrSlot = []

			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(player.GetItemAttribute(invenType, invenPos, i))

			if app.RENDER_TARGET:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 1)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot)

		def SetOfflineShopItem(self, slotIndex):
			itemVnum = shop.GetOfflineShopItemID(slotIndex)
			if itemVnum == 0:
				return
			price = shop.GetOfflineShopItemPrice(slotIndex)
			if app.ENABLE_CHEQUE_SYSTEM:
				cheque = shop.GetOfflineShopItemCheque(slotIndex)
			self.ClearToolTip()
			self.isOfflineShopItem = True
			metinSlot = []
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(shop.GetOfflineShopItemMetinSocket(slotIndex, i))

			attrSlot = []
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(shop.GetOfflineShopItemAttribute(slotIndex, i))
			if app.ENABLE_CHANGELOOK_SYSTEM:
				transmutation = shop.GetOfflineShopItemTransmutation(slotIndex)
				if not transmutation:
					if app.RENDER_TARGET:
						self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 1)
					else:
						self.AddItemData(itemVnum, metinSlot, attrSlot)
				else:
					if app.RENDER_TARGET:
						self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 1, 0, 0, player.INVENTORY, -1, transmutation)
					else:
						self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, player.INVENTORY, -1, transmutation)
			else:
				if app.RENDER_TARGET:
					self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 1)
				else:
					self.AddItemData(itemVnum, metinSlot, attrSlot)

			if app.ENABLE_CHEQUE_SYSTEM:
				self.AppendSellInfoText()
				self.AppendSellingChequePrice(cheque)
			self.AppendPrice(price)
			status, who = shop.GetOfflineShopItemStatus(slotIndex)
			if status:
				self.AppendItemBuyer(who)


	def SetShopItem(self, slotIndex):
		itemVnum = shop.GetItemID(slotIndex)
		if 0 == itemVnum:
			return

		price = shop.GetItemPrice(slotIndex)
		if app.ENABLE_CHEQUE_SYSTEM:
			cheque = shop.GetItemCheque(slotIndex)
		self.ClearToolTip()
		self.isShopItem = True

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(shop.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(shop.GetItemAttribute(slotIndex, i))
		if app.ENABLE_CHANGELOOK_SYSTEM:
			transmutation = shop.GetItemTransmutation(slotIndex)
			if not transmutation:
				if app.RENDER_TARGET:
					self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 1)
				else:
					self.AddItemData(itemVnum, metinSlot, attrSlot)
			else:
				if app.RENDER_TARGET:
					self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 1, 0, 0, player.INVENTORY, -1, transmutation)
				else:
					self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, player.INVENTORY, -1, transmutation)
		else:
			if app.RENDER_TARGET:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 1)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot)
		if app.ENABLE_CHEQUE_SYSTEM:
			self.AppendSellInfoText()
			if shop.IsPrivateShop():
				self.AppendSellingChequePrice(cheque)
		
		if app.ENABLE_MULTISHOP:
			import dbg
			dbg.TraceError("%s %d"%(shop.GetBuyWithItem(slotIndex),shop.GetBuyWithItemCount(slotIndex)))
			if shop.GetBuyWithItem(slotIndex) != 0:
				self.AppendPriceTextLine(shop.GetBuyWithItemCount(slotIndex), shop.GetBuyWithItem(slotIndex))
			else:
				self.AppendPrice(price)
		else:
			self.AppendPrice(price)
		if app.__COMPARE_TOOLTIP__ and shop.IsOpen() and not shop.IsMainPlayerPrivateShop():
			self.SetCompareItem(itemVnum)	

		
			
	if app.ENABLE_SEND_TARGET_INFO:
		def SetItemToolTipStone(self, itemVnum):
			self.itemVnum = itemVnum
			item.SelectItem(itemVnum)
			itemType = item.GetItemType()

			itemDesc = item.GetItemDescription()
			itemSummary = item.GetItemSummary()
			attrSlot = 0
			self.__AdjustMaxWidth(attrSlot, itemDesc)
			itemName = item.GetItemName()
			realName = itemName[:itemName.find("+")]
			self.SetTitle(realName + " +0 - +4")

			## Description ###
			self.AppendDescription(itemDesc, 26)
			self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)

			if item.ITEM_TYPE_METIN == itemType:
				self.AppendMetinInformation()
				self.AppendMetinWearInformation()

			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)

				if item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
					self.AppendRealTimeStartFirstUseLastTime(item, metinSlot, i)

				elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
					self.AppendTimerBasedOnWearLastTime(metinSlot)

			self.ShowToolTip()
	def SetShopItemBySecondaryCoin(self, slotIndex):
		itemVnum = shop.GetItemID(slotIndex)
		if 0 == itemVnum:
			return

		price = shop.GetItemPrice(slotIndex)
		self.ClearToolTip()
		self.isShopItem = True

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(shop.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(shop.GetItemAttribute(slotIndex, i))

		if app.ENABLE_CHANGELOOK_SYSTEM:
			transmutation = shop.GetItemTransmutation(slotIndex)
			if not transmutation:
				if app.RENDER_TARGET:
					self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 1)
				else:
					self.AddItemData(itemVnum, metinSlot, attrSlot)
			else:
				if app.RENDER_TARGET:
					self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 1, 0, 0, player.INVENTORY, -1, transmutation)
				else:
					self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, player.INVENTORY, -1, transmutation)
		else:
			if app.RENDER_TARGET:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 1)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot)
		self.AppendPriceBySecondaryCoin(price)

	def SetExchangeOwnerItem(self, slotIndex):
		itemVnum = exchange.GetItemVnumFromSelf(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(exchange.GetItemMetinSocketFromSelf(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(exchange.GetItemAttributeFromSelf(slotIndex, i))
		if app.__COMPARE_TOOLTIP__:
			self.SetCompareItem(itemVnum)
		automatic = self.GetAutomatic()
		if app.ENABLE_CHANGELOOK_SYSTEM:
			transmutation = exchange.GetItemTransmutation(slotIndex, True)
			if not transmutation:
				if app.RENDER_TARGET:
					self.AddItemData(itemVnum, metinSlot, attrSlot, 1, automatic)
				else:
					self.AddItemData(itemVnum, metinSlot, attrSlot)
			else:
				if app.RENDER_TARGET:
					self.AddItemData(itemVnum, metinSlot, attrSlot, 1, automatic, 0, 0, player.INVENTORY, -1, transmutation)
				else:
					self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, player.INVENTORY, -1, transmutation)
		else:
			if app.RENDER_TARGET:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 1, automatic)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot)

	def SetExchangeTargetItem(self, slotIndex):
		itemVnum = exchange.GetItemVnumFromTarget(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(exchange.GetItemMetinSocketFromTarget(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(exchange.GetItemAttributeFromTarget(slotIndex, i))
		if app.__COMPARE_TOOLTIP__:
			self.SetCompareItem(itemVnum)
		automatic = self.GetAutomatic()
		if app.ENABLE_CHANGELOOK_SYSTEM:
			transmutation = exchange.GetItemTransmutation(slotIndex, False)
			if not transmutation:
				if app.RENDER_TARGET:
					self.AddItemData(itemVnum, metinSlot, attrSlot, 1, automatic)
				else:
					self.AddItemData(itemVnum, metinSlot, attrSlot)
			else:
				if app.RENDER_TARGET:
					self.AddItemData(itemVnum, metinSlot, attrSlot, 1, automatic, 0, 0, player.INVENTORY, -1, transmutation)
				else:
					self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, player.INVENTORY, -1, transmutation)
		else:
			if app.RENDER_TARGET:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 1, automatic)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot)
		if app.__COMPARE_TOOLTIP__:
			self.SetCompareItem(itemVnum)
	def SetPrivateShopBuilderItem(self, invenType, invenPos, privateShopSlotIndex):
		itemVnum = player.GetItemIndex(invenType, invenPos)
		if 0 == itemVnum:
			return

		item.SelectItem(itemVnum)
		self.ClearToolTip()
		if app.ENABLE_CHEQUE_SYSTEM:
			self.AppendSellInfoText()
			self.AppendSellingChequePrice(shop.GetPrivateShopItemCheque(invenType, invenPos))
		self.AppendSellingPrice(shop.GetPrivateShopItemPrice(invenType, invenPos))

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(invenPos, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(invenPos, i))

			if app.ENABLE_CHANGELOOK_SYSTEM:
				if app.RENDER_TARGET:
					self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 1, 0, 0, invenType, invenPos)
				else:
					self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, invenType, invenPos)
			else:
				if app.RENDER_TARGET:
					self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 1)
				else:
					self.AddItemData(itemVnum, metinSlot, attrSlot)

	if app.ENABLE_CHEQUE_SYSTEM:
		def AppendSellingChequePrice(self, cheque):
			self.AppendTextLine(localeInfo.NumberToChequeString(cheque), self.WON_PRICE_COLOR)
			self.AppendSpace(5)
		
		def AppendSellInfoText(self):
			self.AppendTextLine(localeInfo.CHEQUE_SYSTEM_SELL_PRICE, self.PRICE_INFO_COLOR)
			self.AppendSpace(5)


	def SetSafeBoxItem(self, slotIndex):
		itemVnum = safebox.GetItemID(slotIndex)
		if 0 == itemVnum:
			return
		self.ClearToolTip()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(safebox.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(safebox.GetItemAttribute(slotIndex, i))
		if app.__COMPARE_TOOLTIP__:
			self.SetCompareItem(itemVnum)
		automatic = self.GetAutomatic()
		if app.ENABLE_CHANGELOOK_SYSTEM:
			if app.RENDER_TARGET:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 1, automatic, safebox.GetItemFlags(slotIndex), 0, player.SAFEBOX, slotIndex)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot, safebox.GetItemFlags(slotIndex), 0, player.SAFEBOX, slotIndex)
		else:
			if app.RENDER_TARGET:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 1, automatic, safebox.GetItemFlags(slotIndex))
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot, safebox.GetItemFlags(slotIndex))
		# if app.__COMPARE_TOOLTIP__:
			# self.SetCompareItem(itemVnum)
	def SetMallItem(self, slotIndex):
		itemVnum = safebox.GetMallItemID(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(safebox.GetMallItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(safebox.GetMallItemAttribute(slotIndex, i))

		if app.ENABLE_CHANGELOOK_SYSTEM:
			if app.RENDER_TARGET:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 1, 0, 0, player.MALL, slotIndex)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, player.MALL, slotIndex)
		else:
			if app.RENDER_TARGET:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 1)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot)
		if app.__COMPARE_TOOLTIP__:
			self.SetCompareItem(itemVnum)
	def SetItemToolTip(self, itemVnum):
		self.ClearToolTip()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(0)
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append((0, 0))
		
		if app.RENDER_TARGET:
			self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 0)
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot)

	if app.BL_MAILBOX:
		def SetMailBoxItem(self, index):
			item_data = mail.GetMailItemData(index)
			if None == item_data:
				return

			(vnum, count) = item_data

			self.ClearToolTip()
			metinSlot = []
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(mail.GetMailItemMetinSocket(index, i))
			attrSlot = []
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(mail.GetMailItemAttribute(index, i))

			self.AddItemData(vnum, metinSlot, attrSlot)

			#if app.BL_TRANSMUTATION_SYSTEM:
			#	changelookvnum = mail.GetItemChangeLookVnum( index )
			#	self.AppendChangeLookInfoItemVnum(changelookvnum)


	def __AppendAttackSpeedInfo(self, item):
		atkSpd = item.GetValue(0)

		if atkSpd < 80:
			stSpd = localeInfo.TOOLTIP_ITEM_VERY_FAST
		elif atkSpd <= 95:
			stSpd = localeInfo.TOOLTIP_ITEM_FAST
		elif atkSpd <= 105:
			stSpd = localeInfo.TOOLTIP_ITEM_NORMAL
		elif atkSpd <= 120:
			stSpd = localeInfo.TOOLTIP_ITEM_SLOW
		else:
			stSpd = localeInfo.TOOLTIP_ITEM_VERY_SLOW

		self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_SPEED % stSpd, self.NORMAL_COLOR)

	def __AppendAttackGradeInfo(self):
		atkGrade = item.GetValue(1)
		self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_GRADE % atkGrade, self.GetChangeTextLineColor(atkGrade))

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def CalcAcceValue(self, value, abs):
			if not value:
				return 0
			
			valueCalc = int((round(value * abs) / 100) - .5) + int(int((round(value * abs) / 100) - .5) > 0)
			if valueCalc <= 0 and value > 0:
				value = 1
			else:
				value = valueCalc
			
			return value

	def __AppendAttackPowerInfo(self, itemAbsChance = 0):
		minPower = item.GetValue(3)
		maxPower = item.GetValue(4)
		addPower = item.GetValue(5)
		
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if itemAbsChance:
				minPower = self.CalcAcceValue(minPower, itemAbsChance)
				maxPower = self.CalcAcceValue(maxPower, itemAbsChance)
				addPower = self.CalcAcceValue(addPower, itemAbsChance)
		
		if maxPower > minPower:
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_POWER % (minPower + addPower, maxPower + addPower), self.POSITIVE_COLOR)
		else:
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_POWER_ONE_ARG % (minPower + addPower), self.POSITIVE_COLOR)

	def __AppendMagicAttackInfo(self, itemAbsChance = 0):
		minMagicAttackPower = item.GetValue(1)
		maxMagicAttackPower = item.GetValue(2)
		addPower = item.GetValue(5)
		
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if itemAbsChance:
				minMagicAttackPower = self.CalcAcceValue(minMagicAttackPower, itemAbsChance)
				maxMagicAttackPower = self.CalcAcceValue(maxMagicAttackPower, itemAbsChance)
				addPower = self.CalcAcceValue(addPower, itemAbsChance)
		
		if minMagicAttackPower > 0 or maxMagicAttackPower > 0:
			if maxMagicAttackPower > minMagicAttackPower:
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_MAGIC_ATT_POWER % (minMagicAttackPower + addPower, maxMagicAttackPower + addPower), self.POSITIVE_COLOR)
			else:
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_MAGIC_ATT_POWER_ONE_ARG % (minMagicAttackPower + addPower), self.POSITIVE_COLOR)

	def __AppendMagicDefenceInfo(self, itemAbsChance = 0):
		magicDefencePower = item.GetValue(0)
		
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			if itemAbsChance:
				magicDefencePower = self.CalcAcceValue(magicDefencePower, itemAbsChance)
		
		if magicDefencePower > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_MAGIC_DEF_POWER % magicDefencePower, self.GetChangeTextLineColor(magicDefencePower))

	def __AppendAttributeInformation(self, attrSlot, itemAbsChance = 0, itemVnum = 0):
		if 0 != attrSlot:
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				type = attrSlot[i][0]
				value = attrSlot[i][1]
				if len(attrSlot[i]) > 2:
					frozen = attrSlot[i][2]
				else:
					frozen = False

				if 0 == value:
					continue
				
				affectString = self.__GetAffectString(type, value)
				if app.ENABLE_ACCE_COSTUME_SYSTEM:
					if item.GetItemType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_ACCE and itemAbsChance:
						value = self.CalcAcceValue(value, itemAbsChance)
						affectString = self.__GetAffectString(type, value)
				if affectString:
					affectColor = self.__GetAttributeColor(i, value)
					if frozen:
						self.AppendTextLine("["+affectString+"]", self.FROZEN_2_COLOR)
					else:
						self.AppendTextLine(affectString, affectColor)

			#if app.ENABLE_6_7_BONUS_NEW_SYSTEM:
			#	if self.__GetCheck67Bonus():
					#if self.__GetAttributeText67Bonus(attrSlot) == 5:
					#	self.AppendTextLine(localeInfo.ATTR_6TH_7TH_POSSIBILITY,self.ATTR_6TH_7TH_COLOR)

	if app.ENABLE_6_7_BONUS_NEW_SYSTEM:
		def __GetCheck67Bonus(self):
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			if ((itemType == item.ITEM_TYPE_ARMOR and itemSubType != item.ARMOR_TALISMAN) or itemType == item.ITEM_TYPE_WEAPON):
				return True

			return False

		def __GetAttributeText67Bonus(self,attrSlot):
			count = 0
			
			if 0 == attrSlot:
				return count
			
			for q in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				type = attrSlot[q][0]
				value = attrSlot[q][1]
				if type != 0:
					count += 1
			
			return count

	def __GetAttributeColor(self, index, value):
		if value > 0:
			if index >= player.ATTRIBUTE_SLOT_RARE_START and index < player.ATTRIBUTE_SLOT_RARE_END:
				if app.ENABLE_6_7_BONUS_NEW_SYSTEM:
					if self.__GetCheck67Bonus():
						return self.ATTR_6TH_7TH_COLOR
				return self.SPECIAL_POSITIVE_COLOR2
			else:
				return self.SPECIAL_POSITIVE_COLOR
		elif value == 0:
			return self.NORMAL_COLOR
		else:
			return self.NEGATIVE_COLOR

	def __IsPolymorphItem(self, itemVnum):
		if itemVnum >= 70103 and itemVnum <= 70106:
			return 1
		return 0

	def __SetPolymorphItemTitle(self, monsterVnum):
		if localeInfo.IsVIETNAM():
			itemName =item.GetItemName()
			itemName+=" "
			itemName+=nonplayer.GetMonsterName(monsterVnum)
		else:
			itemName =nonplayer.GetMonsterName(monsterVnum)
			itemName+=" "
			itemName+=item.GetItemName()
		self.SetTitle(itemName)

	def __SetNormalItemTitle(self):
		if app.ENABLE_SEND_TARGET_INFO:
			if self.isStone:
				itemName = item.GetItemName()
				realName = itemName[:itemName.find("+")]
				self.SetTitle(realName + " +0 - +4")
			else:
				self.SetTitle(item.GetItemName())
		else:
			self.SetTitle(item.GetItemName())

	def __SetSpecialItemTitle(self):
		self.AppendTextLine(item.GetItemName(), self.SPECIAL_TITLE_COLOR)

	def __SetItemTitle(self, itemVnum, metinSlot, attrSlot):
		if localeInfo.IsCANADA():
			if 72726 == itemVnum or 72730 == itemVnum:
				self.AppendTextLine(item.GetItemName(), grp.GenerateColor(1.0, 0.7843, 0.0, 1.0))
				return

		if self.__IsPolymorphItem(itemVnum):
			self.__SetPolymorphItemTitle(metinSlot[0])
		else:
			if self.__IsAttr(attrSlot):
				self.__SetSpecialItemTitle()
				return

			self.__SetNormalItemTitle()

	def __IsAttr(self, attrSlot):
		if not attrSlot:
			return False

		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			type = attrSlot[i][0]
			if 0 != type:
				return True

		return False

	def AddRefineItemData(self, itemVnum, metinSlot, attrSlot = 0):
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlotData=metinSlot[i]
			if self.GetMetinItemIndex(metinSlotData) == constInfo.ERROR_METIN_STONE:
				metinSlot[i]=player.METIN_SOCKET_TYPE_SILVER
		#if app.RENDER_TARGET:
		#	self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 1)
		#else:
		self.AddItemData(itemVnum, metinSlot, attrSlot)

	def AddItemData_Offline(self, itemVnum, itemDesc, itemSummary, metinSlot, attrSlot):
		self.__AdjustMaxWidth(attrSlot, itemDesc)
		self.__SetItemTitle(itemVnum, metinSlot, attrSlot)

		if self.__IsHair(itemVnum):
			self.__AppendHairIcon(itemVnum)

		### Description ###
		self.AppendDescription(itemDesc, 26)
		self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)
 
	def check_sigillo(self, item_vnum):
		for x in range(55701,55710):
			if x == item_vnum:
				return TRUE	
		if item_vnum == 55801:
			return TRUE
		return FALSE

	def AddItemData(self, itemVnum, metinSlot, attrSlot = 0, preview = 0, automatic = 0, flags = 0, unbindTime = 0, window_type = player.INVENTORY, slotIndex = -1, transmutation = -1):
		self.itemVnum = itemVnum
		item.SelectItem(itemVnum)
		itemType = item.GetItemType()
		itemSubType = item.GetItemSubType()

		if 50026 == itemVnum:
			if 0 != metinSlot:
				name = item.GetItemName()
				if metinSlot[0] > 0:
					name += " "
					name += localeInfo.NumberToMoneyString(metinSlot[0])
				self.SetTitle(name)
				self.__AppendSealInformation(window_type, slotIndex) ## cyh itemseal 2013 11 11
				self.ShowToolTip()
			return

		### Skill Book ###
		if app.ENABLE_SEND_TARGET_INFO:
			if 50300 == itemVnum and not self.isBook:
				if 0 != metinSlot and not self.isBook:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILLBOOK_NAME, 1)
					self.ShowToolTip()
				elif self.isBook:
					self.SetTitle(item.GetItemName())
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					self.ShowToolTip()					
				return
			elif 70037 == itemVnum :
				if 0 != metinSlot and not self.isBook2:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					self.ShowToolTip()
				elif self.isBook2:
					self.SetTitle(item.GetItemName())
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					self.ShowToolTip()					
				return
			elif 70055 == itemVnum:
				if 0 != metinSlot:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					self.ShowToolTip()
				return
		else:
			if 50300 == itemVnum:
				if 0 != metinSlot:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILLBOOK_NAME, 1)
					self.ShowToolTip()
				return
			elif 70037 == itemVnum:
				if 0 != metinSlot:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					self.ShowToolTip()
				return
			elif 70055 == itemVnum:
				if 0 != metinSlot:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					self.ShowToolTip()
				return
		###########################################################################################


		itemDesc = item.GetItemDescription()
		itemSummary = item.GetItemSummary()

		isCostumeItem = 0
		isCostumeHair = 0
		isCostumeBody = 0
		isCostumeAura = 0
		if app.ENABLE_MOUNT_COSTUME_SYSTEM:
			isCostumeMount = 0
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			isCostumeAcce = 0
		if app.ENABLE_WEAPON_COSTUME_SYSTEM:
			isCostumeWeapon = 0

		if app.ENABLE_COSTUME_SYSTEM:
			if item.ITEM_TYPE_COSTUME == itemType:
				isCostumeItem = 1
				isCostumeHair = item.COSTUME_TYPE_HAIR == itemSubType
				isCostumeBody = item.COSTUME_TYPE_BODY == itemSubType
				isCostumeAura = item.COSTUME_TYPE_AURA == itemSubType
				if app.ENABLE_MOUNT_COSTUME_SYSTEM:
					isCostumeMount = item.COSTUME_TYPE_MOUNT == itemSubType
				if app.ENABLE_ACCE_COSTUME_SYSTEM:
					isCostumeAcce = item.COSTUME_TYPE_ACCE == itemSubType
				if app.ENABLE_WEAPON_COSTUME_SYSTEM:
					isCostumeWeapon = item.COSTUME_TYPE_WEAPON == itemSubType

				#dbg.TraceError("IS_COSTUME_ITEM! body(%d) hair(%d)" % (isCostumeBody, isCostumeHair))

		self.__AdjustMaxWidth(attrSlot, itemDesc)
		if app.RENDER_TARGET:
			self.__ModelPreviewClose()
		self.__SetItemTitle(itemVnum, metinSlot, attrSlot)

		### Hair Preview Image ###
		if self.__IsHair(itemVnum):
			self.__AppendHairIcon(itemVnum)

		### Description ###
		self.AppendDescription(itemDesc, 26)
		self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)
        
		if self.check_sigillo(itemVnum) or itemVnum == 55002:
			if attrSlot[0][1] != 0:
				self.AppendSpace(5)
				self.AppendTextLine("Livello: "+str(metinSlot[1]), self.NORMAL_COLOR)
				self.AppendTextLine("HP: +"+pointop(str(attrSlot[0][1]))+"%", self.SPECIAL_POSITIVE_COLOR)
				self.AppendTextLine("DEX: +"+pointop(str(attrSlot[1][1]))+"%", self.SPECIAL_POSITIVE_COLOR)
				self.AppendTextLine("SP: +"+pointop(str(attrSlot[2][1]))+"%", self.SPECIAL_POSITIVE_COLOR)
				self.AppendSpace(5)
				if itemVnum != 55002:
					days = (int(attrSlot[3][1])/60)/24
					hours = (int(attrSlot[3][1]) - (days*60*24)) / 60
					mins = int(attrSlot[3][1]) - (days*60*24) - (hours*60)
					self.AppendTextLine("Durata: %d Giorni %d Ore %d Minuti" % (days, hours, mins), self.SPECIAL_POSITIVE_COLOR)
				else:
					value_pet_name = str(metinSlot[0])
					pet_name_type = ["Monkey", "Spider", "Razador", "Nemere", "Dragon", "Meley"]
					value_pet_evo = str(metinSlot[2])
					petname_box = ["Cucciolo", "Selvaggio", "Coraggioso", "Eroico"]
					self.AppendTextLine("Pet : %s, %s" % ((pet_name_type[int(value_pet_name)-1]), (petname_box[int(value_pet_evo)])))

		### Weapon ###	
		if item.ITEM_TYPE_WEAPON == itemType:

			self.__AppendLimitInformation()

			self.AppendSpace(5)

			## ��ä�� ��� ������ ���� ǥ���Ѵ�.
			if item.WEAPON_FAN == itemSubType:
				self.__AppendMagicAttackInfo()
				self.__AppendAttackPowerInfo()

			else:
				self.__AppendAttackPowerInfo()
				self.__AppendMagicAttackInfo()

			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)
			if app.ENABLE_CHANGELOOK_SYSTEM:
				self.AppendTransmutation(window_type, slotIndex, transmutation)

			self.AppendWearableInformation()
			if app.ENABLE_NEW_ARROW_SYSTEM:
				if itemSubType != item.WEAPON_UNLIMITED_ARROW:
					self.__AppendMetinSlotInfo(metinSlot)
				else:
					bHasRealtimeFlag = 0
					for i in xrange(item.LIMIT_MAX_NUM):
						(limitType, limitValue) = item.GetLimit(i)
						if item.LIMIT_REAL_TIME == limitType:
							bHasRealtimeFlag = 1
					
					if bHasRealtimeFlag == 1:
						self.AppendMallItemLastTime(metinSlot[0])
			else:
				self.__AppendMetinSlotInfo(metinSlot)
			if app.RENDER_TARGET:
				if preview != 0:
					transmutation_weap = player.GetItemTransmutation(slotIndex)
					if item.WEAPON_SWORD == itemSubType:
						if player.GetRace() != 7 and player.GetRace() != 3:
							if not transmutation_weap:
								self.__ModelPreview(itemVnum, 3, player.GetRace(), automatic)
							else:
								itemVnum = player.GetItemTransmutation(window_type, slotIndex)
								self.__ModelPreview(itemVnum, 3, player.GetRace(), automatic)
					
					if item.WEAPON_DAGGER == itemSubType:
						if player.GetRace() == 5 or player.GetRace() == 1:
							if not transmutation_weap:
								self.__ModelPreview(itemVnum, 3, player.GetRace(), automatic)
							else:
								itemVnum = player.GetItemTransmutation(window_type, slotIndex)
								self.__ModelPreview(itemVnum, 3, player.GetRace(), automatic)
					
					if item.WEAPON_BOW == itemSubType:
						if player.GetRace() == 5 or player.GetRace() == 1:
							if not transmutation_weap:
								self.__ModelPreview(itemVnum, 3, player.GetRace(), automatic)
							else:
								itemVnum = player.GetItemTransmutation(window_type, slotIndex)
								self.__ModelPreview(itemVnum, 3, player.GetRace(), automatic)
					
					if item.WEAPON_BELL == itemSubType:
						if player.GetRace() == 7 or player.GetRace() == 3:
							if not transmutation_weap:
								self.__ModelPreview(itemVnum, 3, player.GetRace(), automatic)
							else:
								itemVnum = player.GetItemTransmutation(window_type, slotIndex)
								self.__ModelPreview(itemVnum, 3, player.GetRace(), automatic)
					
					if item.WEAPON_FAN == itemSubType:
						if player.GetRace() == 7 or player.GetRace() == 3:
							if not transmutation_weap:
								self.__ModelPreview(itemVnum, 3, player.GetRace(), automatic)
							else:
								itemVnum = player.GetItemTransmutation(window_type, slotIndex)
								self.__ModelPreview(itemVnum, 3, player.GetRace(), automatic)
					
					if item.WEAPON_TWO_HANDED == itemSubType:	
						if player.GetRace() == 4 or player.GetRace() == 0:
							if not transmutation_weap:
								self.__ModelPreview(itemVnum, 3, player.GetRace(), automatic)
							else:
								itemVnum = player.GetItemTransmutation(window_type, slotIndex)
								self.__ModelPreview(itemVnum, 3, player.GetRace(), automatic)

		### Armor ###
		elif item.ITEM_TYPE_ARMOR == itemType:
			self.__AppendLimitInformation()

			## ����
			defGrade = item.GetValue(1)
			defBonus = item.GetValue(5)*2 ## ���� ǥ�� �߸� �Ǵ� ������ ����
			if defGrade > 0:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade+defBonus), self.GetChangeTextLineColor(defGrade))

			self.__AppendMagicDefenceInfo()
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)
			if app.ENABLE_CHANGELOOK_SYSTEM:
				self.AppendTransmutation(window_type, slotIndex, transmutation)
			self.AppendWearableInformation()

			if app.RENDER_TARGET:
				if preview != 0 and itemSubType == item.ARMOR_BODY:
					transmutation_arm = player.GetItemTransmutation(slotIndex)
					if item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR) == False:
						if player.GetRace() == 4 or player.GetRace() == 0:
							if not transmutation_arm:
								self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
							else:
								itemVnum = player.GetItemTransmutation(window_type, slotIndex)
								self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
						
					if item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN) == False:
						if player.GetRace() == 5 or player.GetRace() == 1:
							if not transmutation_arm:
								self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
							else:
								itemVnum = player.GetItemTransmutation(window_type, slotIndex)
								self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
						
					if item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA) == False:
						if player.GetRace() == 6 or player.GetRace() == 2:
							if not transmutation_arm:
								self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
							else:
								itemVnum = player.GetItemTransmutation(window_type, slotIndex)
								self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
					
					if item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN) == False:
						if player.GetRace() == 7 or player.GetRace() == 3:
							if not transmutation_arm:
								self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic) 
							else:
								itemVnum = player.GetItemTransmutation(window_type, slotIndex)
								self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)

			if itemSubType in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
				self.__AppendAccessoryMetinSlotInfo(metinSlot, constInfo.GET_ACCESSORY_MATERIAL_VNUM(itemVnum, itemSubType))
			else:
				self.__AppendMetinSlotInfo(metinSlot)

		### Ring Slot Item (Not UNIQUE) ###
		elif item.ITEM_TYPE_RING == itemType:
			self.__AppendLimitInformation()
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)

			#���� ���� �ý��� �����ؼ� ���� ��ȹ ����
			#self.__AppendAccessoryMetinSlotInfo(metinSlot, 99001)


		### Belt Item ###
		elif item.ITEM_TYPE_BELT == itemType:
			self.__AppendLimitInformation()
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)

			self.__AppendAccessoryMetinSlotInfo(metinSlot, constInfo.GET_BELT_MATERIAL_VNUM(itemVnum))

		### Rune Item ###
		elif item.ITEM_TYPE_RUNE == itemType or item.ITEM_TYPE_RUNE_RED == itemType or item.ITEM_TYPE_RUNE_BLUE == itemType or item.ITEM_TYPE_RUNE_BLACK == itemType or item.ITEM_TYPE_RUNE_YELLOW == itemType or item.ITEM_TYPE_RUNE_GREEN == itemType:
			self.__AppendLimitInformation()
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)

		elif itemVnum in self.MountRender or itemVnum in self.PetRender:
			if itemVnum in self.MountRender:
				self.__ModelPreview(itemVnum, 9, self.MountRender[itemVnum], automatic)
			else:
				self.__ModelPreview(itemVnum, 9, self.PetRender[itemVnum], automatic)

		## �ڽ��� ������ ##
		elif 0 != isCostumeItem:
			self.__AppendLimitInformation()

			if app.RENDER_TARGET:
				if preview != 0:
					transmutation_cost = player.GetItemTransmutation(window_type, slotIndex)
					if itemSubType == item.COSTUME_TYPE_BODY:
						if item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR) == False and (player.GetRace() == 4 or player.GetRace() == 0):
							if(item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and chr.RaceToSex(player.GetRace()) == 0):
								if not transmutation_cost:
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
								else:
									itemVnum = player.GetItemTransmutation(window_type, slotIndex)
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
							if(item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and chr.RaceToSex(player.GetRace()) == 1):
								if not transmutation_cost:
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
								else:
									itemVnum = player.GetItemTransmutation(window_type, slotIndex)
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
							if (item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) == False and item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) == False):
								if not transmutation_cost:
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
								else:
									itemVnum = player.GetItemTransmutation(window_type, slotIndex)
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
						elif item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN) == False and (player.GetRace() == 5 or player.GetRace() == 1):
							if(item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and chr.RaceToSex(player.GetRace()) == 0):
								if not transmutation_cost:
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
								else:
									itemVnum = player.GetItemTransmutation(window_type, slotIndex)
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
							if(item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and chr.RaceToSex(player.GetRace()) == 1):
								if not transmutation_cost:
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
								else:
									itemVnum = player.GetItemTransmutation(window_type, slotIndex)
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
							if (item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) == False and item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) == False):
								if not transmutation_cost:
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
								else:
									itemVnum = player.GetItemTransmutation(window_type, slotIndex)
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
						elif item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA) == False and (player.GetRace() == 2 or player.GetRace() == 6):
							if(item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and chr.RaceToSex(player.GetRace()) == 0):
								if not transmutation_cost:
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
								else:
									itemVnum = player.GetItemTransmutation(window_type, slotIndex)
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
							if(item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and chr.RaceToSex(player.GetRace()) == 1):
								if not transmutation_cost:
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
								else:
									itemVnum = player.GetItemTransmutation(window_type, slotIndex)
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
							if (item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) == False and item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) == False):
								if not transmutation_cost:
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
								else:
									itemVnum = player.GetItemTransmutation(window_type, slotIndex)
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
						elif item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN) == False and (player.GetRace() == 7 or player.GetRace() == 3):
							if(item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and chr.RaceToSex(player.GetRace()) == 0):
								if not transmutation_cost:
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
								else:
									itemVnum = player.GetItemTransmutation(window_type, slotIndex)
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
							if(item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and chr.RaceToSex(player.GetRace()) == 1):
								if not transmutation_cost:
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
								else:
									itemVnum = player.GetItemTransmutation(window_type, slotIndex)
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
							if (item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) == False and item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) == False):
								if not transmutation_cost:
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
								else:
									itemVnum = player.GetItemTransmutation(window_type, slotIndex)
									self.__ModelPreview(itemVnum, 2, player.GetRace(), automatic)
						item.SelectItem(self.itemVnum)
					
					elif itemSubType == item.COSTUME_TYPE_HAIR: #Hair 
						if item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR) == False and (player.GetRace() == 4 or player.GetRace() == 0):
							if(item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and chr.RaceToSex(player.GetRace()) == 0):
								if not transmutation_cost:
									item.SelectItem(self.itemVnum)
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
								else:
									item.SelectItem(player.GetItemTransmutation(window_type, slotIndex))
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
							if(item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and chr.RaceToSex(player.GetRace()) == 1):
								if not transmutation_cost:
									item.SelectItem(self.itemVnum)
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
								else:
									item.SelectItem(player.GetItemTransmutation(window_type, slotIndex))
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
							if (item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) == False and item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) == False):
								if not transmutation_cost:
									item.SelectItem(self.itemVnum)
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
								else:
									item.SelectItem(player.GetItemTransmutation(window_type, slotIndex))
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
						if item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN) == False and (player.GetRace() == 5 or player.GetRace() == 1):
							if(item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and chr.RaceToSex(player.GetRace()) == 0):
								if not transmutation_cost:
									item.SelectItem(self.itemVnum)
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
								else:
									item.SelectItem(player.GetItemTransmutation(window_type, slotIndex))
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
							if(item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and chr.RaceToSex(player.GetRace()) == 1):
								if not transmutation_cost:
									item.SelectItem(self.itemVnum)
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
								else:
									item.SelectItem(player.GetItemTransmutation(window_type, slotIndex))
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
							if (item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) == False and item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) == False):
								if not transmutation_cost:
									item.SelectItem(self.itemVnum)
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
								else:
									item.SelectItem(player.GetItemTransmutation(window_type, slotIndex))
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
						if item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA) == False and (player.GetRace() == 2 or player.GetRace() == 6):
							if(item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and chr.RaceToSex(player.GetRace()) == 0):
								if not transmutation_cost:
									item.SelectItem(self.itemVnum)
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
								else:
									item.SelectItem(player.GetItemTransmutation(window_type, slotIndex))
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
							if(item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and chr.RaceToSex(player.GetRace()) == 1):
								if not transmutation_cost:
									item.SelectItem(self.itemVnum)
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
								else:
									item.SelectItem(player.GetItemTransmutation(window_type, slotIndex))
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
							if (item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) == False and item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) == False):
								if not transmutation_cost:
									item.SelectItem(self.itemVnum)
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
								else:
									item.SelectItem(player.GetItemTransmutation(window_type, slotIndex))
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
						elif item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN) == False and (player.GetRace() == 7 or player.GetRace() == 3):
							if(item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and chr.RaceToSex(player.GetRace()) == 0):
								if not transmutation_cost:
									item.SelectItem(self.itemVnum)
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
								else:
									item.SelectItem(player.GetItemTransmutation(window_type, slotIndex))
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
							if(item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and chr.RaceToSex(player.GetRace()) == 1):
								if not transmutation_cost:
									item.SelectItem(self.itemVnum)
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
								else:
									item.SelectItem(player.GetItemTransmutation(window_type, slotIndex))
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
							if (item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) == False and item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) == False):
								if not transmutation_cost:
									item.SelectItem(self.itemVnum)
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
								else:
									item.SelectItem(player.GetItemTransmutation(window_type, slotIndex))
									self.__ModelPreview(item.GetValue(3), 1, player.GetRace(), automatic)
						item.SelectItem(self.itemVnum)

					elif itemSubType == item.COSTUME_TYPE_WEAPON:
						if item.GetValue(3) == 0:
							if player.GetRace() != 7 and player.GetRace() != 3:
								if not transmutation_cost:
									self.__ModelPreview(itemVnum, 3, player.GetRace(), automatic)
								else:
									self.__ModelPreview(transmutation_cost, 3, player.GetRace(), automatic)
						if item.GetValue(3) == 1:
							if player.GetRace() == 5 or player.GetRace() == 1:
								if not transmutation_cost:
									self.__ModelPreview(itemVnum, 3, player.GetRace(), automatic)
								else:
									self.__ModelPreview(transmutation_cost, 3, player.GetRace(), automatic)
						if item.GetValue(3) == 2:
							if player.GetRace() == 5 or player.GetRace() == 1:
								if not transmutation_cost:
									self.__ModelPreview(itemVnum, 3, player.GetRace(), automatic)
								else:
									self.__ModelPreview(transmutation_cost, 3, player.GetRace(), automatic)
						if item.GetValue(3) == 3:
							if player.GetRace() == 0 or player.GetRace() == 4:
								if not transmutation_cost:
									self.__ModelPreview(itemVnum, 3, player.GetRace(), automatic)
								else:
									self.__ModelPreview(transmutation_cost, 3, player.GetRace(), automatic)
						if item.GetValue(3) == 4:
							if player.GetRace() == 7 or player.GetRace() == 3:
								if not transmutation_cost:
									self.__ModelPreview(itemVnum, 3, player.GetRace(), automatic)
								else:
									self.__ModelPreview(transmutation_cost, 3, player.GetRace(), automatic)

						if item.GetValue(3) == 5:
							if player.GetRace() == 7 or player.GetRace() == 3:
								if not transmutation_cost:
									self.__ModelPreview(itemVnum, 3, player.GetRace(), automatic)
								else:
									self.__ModelPreview(transmutation_cost, 3, player.GetRace(), automatic)
						item.SelectItem(self.itemVnum)

					elif itemSubType == item.COSTUME_TYPE_ACCE:
						self.__ModelPreview(itemVnum, 4, player.GetRace(), automatic)

					# elif itemSubType == item.COSTUME_TYPE_AURA:
						# self.__ModelPreview(itemVnum, 5, player.GetRace(), automatic)

			if 0 != isCostumeAura:
				self.AppendTextLine(localeInfo.AURA_TOOLTIP_LEVEL%(metinSlot[0],metinSlot[1]),self.CHANGELOOK_ITEMNAME_COLOR)
				self.AppendTextLine(localeInfo.AURA_TOOLTIP_ABS%float(self.GetAbsorb(metinSlot[1])),self.CHANGELOOK_ITEMNAME_COLOR)
				self.AppendTextLine(localeInfo.AURA_TOOLTIP_EXP%metinSlot[2],self.CHANGELOOK_ITEMNAME_COLOR)
				self.__AppendAttributeInformation(attrSlot)
				
			elif app.ENABLE_ACCE_COSTUME_SYSTEM:
				if isCostumeAcce:
					## ABSORPTION RATE
					absChance = int(metinSlot[acce.ABSORPTION_SOCKET])
					self.AppendTextLine(localeInfo.ACCE_ABSORB_CHANCE % (absChance), self.CONDITION_COLOR)
					## END ABSOPRTION RATE
					
					itemAbsorbedVnum = int(metinSlot[acce.ABSORBED_SOCKET])
					if itemAbsorbedVnum:
						## ATTACK / DEFENCE
						item.SelectItem(itemAbsorbedVnum)
						if item.GetItemType() == item.ITEM_TYPE_WEAPON:
							if item.GetItemSubType() == item.WEAPON_FAN:
								self.__AppendMagicAttackInfo(metinSlot[acce.ABSORPTION_SOCKET])
								item.SelectItem(itemAbsorbedVnum)
								self.__AppendAttackPowerInfo(metinSlot[acce.ABSORPTION_SOCKET])
							else:
								self.__AppendAttackPowerInfo(metinSlot[acce.ABSORPTION_SOCKET])
								item.SelectItem(itemAbsorbedVnum)
								self.__AppendMagicAttackInfo(metinSlot[acce.ABSORPTION_SOCKET])
						elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
							defGrade = item.GetValue(1)
							defBonus = item.GetValue(5) * 2
							defGrade = self.CalcAcceValue(defGrade, metinSlot[acce.ABSORPTION_SOCKET])
							defBonus = self.CalcAcceValue(defBonus, metinSlot[acce.ABSORPTION_SOCKET])
							
							if defGrade > 0:
								self.AppendSpace(5)
								self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus), self.GetChangeTextLineColor(defGrade))
							
							item.SelectItem(itemAbsorbedVnum)
							self.__AppendMagicDefenceInfo(metinSlot[acce.ABSORPTION_SOCKET])
						## END ATTACK / DEFENCE
						
						## EFFECT
						item.SelectItem(itemAbsorbedVnum)
						for i in xrange(item.ITEM_APPLY_MAX_NUM):
							(affectType, affectValue) = item.GetAffect(i)
							affectValue = self.CalcAcceValue(affectValue, metinSlot[acce.ABSORPTION_SOCKET])
							affectString = self.__GetAffectString(affectType, affectValue)
							if affectString and affectValue > 0:
								self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))
							
							item.SelectItem(itemAbsorbedVnum)
						# END EFFECT
						
						item.SelectItem(itemVnum)
						## ATTR
						self.__AppendAttributeInformation(attrSlot, metinSlot[acce.ABSORPTION_SOCKET])
						# END ATTR
					else:
						# ATTR
						self.__AppendAttributeInformation(attrSlot)
						# END ATTR
				else:
					self.__AppendAffectInformation()
					self.__AppendAttributeInformation(attrSlot)
			else:
				self.__AppendAffectInformation()
				self.__AppendAttributeInformation(attrSlot)
			if app.ENABLE_CHANGELOOK_SYSTEM:
				self.AppendTransmutation(window_type, slotIndex, transmutation)			
			self.AppendWearableInformation()
			bHasRealtimeFlag = 0
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_REAL_TIME == limitType:
					bHasRealtimeFlag = 1
			
			if bHasRealtimeFlag == 1:
				self.AppendMallItemLastTime(metinSlot[0])

		## Rod ##
		elif item.ITEM_TYPE_ROD == itemType:

			if 0 != metinSlot:
				curLevel = item.GetValue(0) / 10
				curEXP = metinSlot[0]
				maxEXP = item.GetValue(2)
				self.__AppendLimitInformation()
				self.__AppendRodInformation(curLevel, curEXP, maxEXP)

		## Pick ##
		elif item.ITEM_TYPE_PICK == itemType:

			if 0 != metinSlot:
				curLevel = item.GetValue(0) / 10
				curEXP = metinSlot[0]
				maxEXP = item.GetValue(2)
				self.__AppendLimitInformation()
				self.__AppendPickInformation(curLevel, curEXP, maxEXP)

		## Lottery ##
		elif item.ITEM_TYPE_LOTTERY == itemType:
			if 0 != metinSlot:

				ticketNumber = int(metinSlot[0])
				stepNumber = int(metinSlot[1])

				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_LOTTERY_STEP_NUMBER % (stepNumber), self.NORMAL_COLOR)
				self.AppendTextLine(localeInfo.TOOLTIP_LOTTO_NUMBER % (ticketNumber), self.NORMAL_COLOR);

		### Metin ###
		elif item.ITEM_TYPE_METIN == itemType:
			self.AppendMetinInformation()
			self.AppendMetinWearInformation()

		### Fish ###
		elif item.ITEM_TYPE_FISH == itemType:
			if 0 != metinSlot:
				self.__AppendFishInfo(metinSlot[0])

		## item.ITEM_TYPE_BLEND
		elif item.ITEM_TYPE_BLEND == itemType:
			self.__AppendLimitInformation()

			if metinSlot:
				affectType = metinSlot[0]
				affectValue = metinSlot[1]
				time = metinSlot[2]
				self.AppendSpace(5)
				affectText = self.__GetAffectString(affectType, affectValue)

				self.AppendTextLine(affectText, self.NORMAL_COLOR)

				if time > 0:
					minute = (time / 60)
					second = (time % 60)
					timeString = localeInfo.TOOLTIP_POTION_TIME

					if minute > 0:
						timeString += str(minute) + localeInfo.TOOLTIP_POTION_MIN
					if second > 0:
						timeString += " " + str(second) + localeInfo.TOOLTIP_POTION_SEC

					self.AppendTextLine(timeString)
				else:
					self.AppendTextLine(localeInfo.BLEND_POTION_NO_TIME)
			else:
				self.AppendTextLine("BLEND_POTION_NO_INFO")
		elif item.ITEM_TYPE_UNIQUE == itemType:
			if 0 != metinSlot:
				bHasRealtimeFlag = 0

				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1

				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])
				else:
					time = metinSlot[SOCKET_REALTIME_INDEX]

					if 1 == item.GetValue(2): ## �ǽð� �̿� Flag / ���� ���ص� �ش�
						self.AppendMallItemLastTime(time)
					else:
						self.AppendUniqueItemLastTime(time)

		### Use ###
		elif item.ITEM_TYPE_USE == itemType:
			self.__AppendLimitInformation()

			if app.ENABLE_REAL_TIME_ENCHANT:
				if itemSubType == item.USE_CHANGE_ATTRIBUTE or itemSubType == item.USE_ADD_ATTRIBUTE:
					if 0 != metinSlot:
						for i in xrange(item.LIMIT_MAX_NUM):
							(limitType, limitValue) = item.GetLimit(i)
							if item.LIMIT_REAL_TIME == limitType:
								self.AppendMallItemLastTime(metinSlot[0])
								break

			if item.USE_POTION == itemSubType or item.USE_POTION_NODELAY == itemSubType:
				self.__AppendPotionInformation()

			elif item.USE_ABILITY_UP == itemSubType:
				self.__AppendAbilityPotionInformation()


			## ���� ������
			if 27989 == itemVnum or 76006 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TOOLTIP_REST_USABLE_COUNT % (6 - useCount), self.NORMAL_COLOR)

			## �̺�Ʈ ������
			elif 50004 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TOOLTIP_REST_USABLE_COUNT % (10 - useCount), self.NORMAL_COLOR)

			## �ڵ�����
			elif constInfo.IS_AUTO_POTION(itemVnum):
				if 0 != metinSlot:
					## 0: Ȱ��ȭ, 1: ��뷮, 2: �ѷ�
					isActivated = int(metinSlot[0])
					usedAmount = float(metinSlot[1])
					totalAmount = float(metinSlot[2])

					if 0 == totalAmount:
						totalAmount = 1

					self.AppendSpace(5)

					if 0 != isActivated:
						self.AppendTextLine("(%s)" % (localeInfo.TOOLTIP_AUTO_POTION_USING), self.SPECIAL_POSITIVE_COLOR)
						self.AppendSpace(5)

					self.AppendTextLine(localeInfo.TOOLTIP_AUTO_POTION_REST, self.POSITIVE_COLOR)

			## ��ȯ ����
			elif itemVnum in WARP_SCROLLS:
				if 0 != metinSlot:
					xPos = int(metinSlot[0])
					yPos = int(metinSlot[1])

					if xPos != 0 and yPos != 0:
						(mapName, xBase, yBase) = background.GlobalPositionToMapInfo(xPos, yPos)

						localeMapName=localeInfo.MINIMAP_ZONE_NAME_DICT.get(mapName, "")

						self.AppendSpace(5)

						if localeMapName!="":
							self.AppendTextLine(localeInfo.TOOLTIP_MEMORIZED_POSITION % (localeMapName, int(xPos-xBase)/100, int(yPos-yBase)/100), self.NORMAL_COLOR)
						else:
							self.AppendTextLine(localeInfo.TOOLTIP_MEMORIZED_POSITION_ERROR % (int(xPos)/100, int(yPos)/100), self.NORMAL_COLOR)
							dbg.TraceError("NOT_EXIST_IN_MINIMAP_ZONE_NAME_DICT: %s" % mapName)

			if 79000 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine("Livello Buff: [M]" , self.ITEM_BUFF_LEVEL_COLOR)
					self.AppendTextLine("Tipo di Buff: Benedizione" , self.ITEM_BUFF_TYPE_COLOR)			
					self.AppendTextLine("Percentuale: 24" , self.ITEM_BUFF_RATE_COLOR)			
					self.AppendTextLine("Durata Buff: 250 s" , self.ITEM_BUFF_DURATION_COLOR)	
					self.AppendTextLine("Buff Rimasti: %s "  %(80 - useCount), self.ITEM_BUFF_USAGE_COLOR)					
	
					
			if 79001 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine("Livello Buff: [G]" , self.ITEM_BUFF_LEVEL_COLOR)
					self.AppendTextLine("Tipo di Buff: Benedizione" , self.ITEM_BUFF_TYPE_COLOR)			
					self.AppendTextLine("Percentuale: 29" , self.ITEM_BUFF_RATE_COLOR)			
					self.AppendTextLine("Durata Buff: 350 s" , self.ITEM_BUFF_DURATION_COLOR)	
					self.AppendTextLine("Buff Rimasti: %s "  %(100 - useCount), self.ITEM_BUFF_USAGE_COLOR)					
					
			if 79002 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine("Livello Buff: [P]" , self.ITEM_BUFF_LEVEL_COLOR)
					self.AppendTextLine("Tipo di Buff: Benedizione" , self.ITEM_BUFF_TYPE_COLOR)			
					self.AppendTextLine("Percentuale: 35" , self.ITEM_BUFF_RATE_COLOR)			
					self.AppendTextLine("Durata Buff: 500 s" , self.ITEM_BUFF_DURATION_COLOR)	
					self.AppendTextLine("Buff Rimasti: %s "  %(120 - useCount), self.ITEM_BUFF_USAGE_COLOR)					
	
			if 79003 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine("Livello Buff: [M]" , self.ITEM_BUFF_LEVEL_COLOR)
					self.AppendTextLine("Tipo di Buff: Aiuto del drago" , self.ITEM_BUFF_TYPE_COLOR)			
					self.AppendTextLine("Percentuale: 24" , self.ITEM_BUFF_RATE_COLOR)			
					self.AppendTextLine("Durata Buff: 250 s" , self.ITEM_BUFF_DURATION_COLOR)	
					self.AppendTextLine("Buff Rimasti: %s "  %(80 - useCount), self.ITEM_BUFF_USAGE_COLOR)					
	
					
			if 79004 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine("Livello Buff: [G]" , self.ITEM_BUFF_LEVEL_COLOR)
					self.AppendTextLine("Tipo di Buff: Aiuto del drago" , self.ITEM_BUFF_TYPE_COLOR)			
					self.AppendTextLine("Percentuale: 29" , self.ITEM_BUFF_RATE_COLOR)			
					self.AppendTextLine("Durata Buff: 350 s" , self.ITEM_BUFF_DURATION_COLOR)	
					self.AppendTextLine("Buff Rimasti: %s "  %(100 - useCount), self.ITEM_BUFF_USAGE_COLOR)					
					
			if 79005 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine("Livello Buff: [P]" , self.ITEM_BUFF_LEVEL_COLOR)
					self.AppendTextLine("Tipo di Buff: Aiuto del drago" , self.ITEM_BUFF_TYPE_COLOR)			
					self.AppendTextLine("Percentuale: 35" , self.ITEM_BUFF_RATE_COLOR)			
					self.AppendTextLine("Durata Buff: 500 s" , self.ITEM_BUFF_DURATION_COLOR)	
					self.AppendTextLine("Buff Rimasti: %s "  %(120 - useCount), self.ITEM_BUFF_USAGE_COLOR)					

			if 79006 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine("Livello Buff: [M]" , self.ITEM_BUFF_LEVEL_COLOR)
					self.AppendTextLine("Tipo di Buff: Riflessione" , self.ITEM_BUFF_TYPE_COLOR)			
					self.AppendTextLine("Percentuale: 21" , self.ITEM_BUFF_RATE_COLOR)			
					self.AppendTextLine("Durata Buff: 250 s" , self.ITEM_BUFF_DURATION_COLOR)	
					self.AppendTextLine("Buff Rimasti: %s "  %(80 - useCount), self.ITEM_BUFF_USAGE_COLOR)					
	
					
			if 79007 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine("Livello Buff: [G]" , self.ITEM_BUFF_LEVEL_COLOR)
					self.AppendTextLine("Tipo di Buff: Riflessione" , self.ITEM_BUFF_TYPE_COLOR)			
					self.AppendTextLine("Percentuale: 31" , self.ITEM_BUFF_RATE_COLOR)			
					self.AppendTextLine("Durata Buff: 350 s" , self.ITEM_BUFF_DURATION_COLOR)	
					self.AppendTextLine("Buff Rimasti: %s "  %(100 - useCount), self.ITEM_BUFF_USAGE_COLOR)					
					
			if 79008 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine("Livello Buff: [P]" , self.ITEM_BUFF_LEVEL_COLOR)
					self.AppendTextLine("Tipo di Buff: Riflessione" , self.ITEM_BUFF_TYPE_COLOR)			
					self.AppendTextLine("Percentuale: 45" , self.ITEM_BUFF_RATE_COLOR)			
					self.AppendTextLine("Durata Buff: 500 s" , self.ITEM_BUFF_DURATION_COLOR)	
					self.AppendTextLine("Buff Rimasti: %s "  %(120 - useCount), self.ITEM_BUFF_USAGE_COLOR)										

			#####
			if item.USE_SPECIAL == itemSubType:
				bHasRealtimeFlag = 0
				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1

				## �ִٸ� ���� ������ ǥ����. ex) ���� �ð� : 6�� 6�ð� 58��
				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])
				else:
					# ... �̰�... �������� �̷� �ð� üũ �ȵǾ� �ִµ�...
					# �� �̷��� �ִ��� ������ ���ϳ� �׳� ����...
					if 0 != metinSlot:
						time = metinSlot[SOCKET_REALTIME_INDEX]

						## �ǽð� �̿� Flag
						if 1 == item.GetValue(2):
							self.AppendMallItemLastTime(time)

			elif item.USE_TIME_CHARGE_PER == itemSubType:
				bHasRealtimeFlag = 0
				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1
				if metinSlot[2]:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_PER(metinSlot[2]))
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_PER(item.GetValue(0)))

				## �ִٸ� ���� ������ ǥ����. ex) ���� �ð� : 6�� 6�ð� 58��
				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])

			elif item.USE_TIME_CHARGE_FIX == itemSubType:
				bHasRealtimeFlag = 0
				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1
				if metinSlot[2]:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_FIX(metinSlot[2]))
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_FIX(item.GetValue(0)))

				## �ִٸ� ���� ������ ǥ����. ex) ���� �ð� : 6�� 6�ð� 58��
				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])

		elif item.ITEM_TYPE_QUEST == itemType:
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)

				if item.LIMIT_REAL_TIME == limitType:
					self.AppendMallItemLastTime(metinSlot[0])
		elif item.ITEM_TYPE_DS == itemType:
			self.AppendTextLine(self.__DragonSoulInfoString(itemVnum))
			self.__AppendAttributeInformation(attrSlot)
		else:
			self.__AppendLimitInformation()

		for i in xrange(item.LIMIT_MAX_NUM):
			(limitType, limitValue) = item.GetLimit(i)
			#dbg.TraceError("LimitType : %d, limitValue : %d" % (limitType, limitValue))

			if item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
				self.AppendRealTimeStartFirstUseLastTime(item, metinSlot, i)
				#dbg.TraceError("2) REAL_TIME_START_FIRST_USE flag On ")

			elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
				self.AppendTimerBasedOnWearLastTime(metinSlot)
				#dbg.TraceError("1) REAL_TIME flag On ")

			itemPrice = item.GetISellItemPrice()
			itemCount = player.GetItemCount(window_type, slotIndex)
			itemPriceCount = itemPrice * itemCount

		if app.ENABLE_SELL_ITEM:
			if self.IsSellItems(itemVnum, itemPrice):
				if item.GetItemType() == item.ITEM_TYPE_WEAPON or item.GetItemType() == item.ITEM_TYPE_ARMOR:
				# Skip showing the item price information for weapons and armor
					pass
				else:
					self.AppendSpace(5)
					self.AppendTextLine("|Ekey_shift|e"+" + |Ekey_x|e"+" + "+"|Ekey_srclick|e - Vendita Rapida",grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0),False)
					if itemCount > 1:
						self.AppendTextLine(localeInfo.SELL_PRICE_INFO_PCS % localeInfo.NumberToMoneyString(itemPrice), self.SPECIAL_TITLE_COLOR)
						self.AppendTextLine(localeInfo.SELL_PRICE_INFO_ALL % localeInfo.NumberToMoneyString(itemPriceCount), self.SPECIAL_TITLE_COLOR)
					else:
						self.AppendTextLine(localeInfo.NumberToMoneyString(itemPrice), self.SPECIAL_TITLE_COLOR)


		if itemVnum == 58500: #qui cambi colori scritta Frozen
			self.AppendSpace(5)
			self.AppendTextLine("Slot Congenlamento: %d" % (int(metinSlot[0])+1), self.FROZEN_COLOR)
			
		if itemVnum == 58501 or itemVnum == 58502:
			self.AppendSpace(5)
			self.AppendTextLine("Slot Scongenlamento: %d" % (int(metinSlot[0])+1), self.FROZEN_COLOR)

		self.__AppendSealInformation(window_type, slotIndex) ## cyh itemseal 2013 11 11

		self.AppendAntiflagInformation()

		if slotIndex != -1 and ((itemType == item.ITEM_TYPE_COSTUME and itemSubType != item.COSTUME_TYPE_AURA) or itemType == item.ITEM_TYPE_WEAPON or (itemType == item.ITEM_TYPE_ARMOR and itemSubType == item.ARMOR_BODY) or itemVnum in self.PetRender or itemVnum in self.MountRender) and not automatic and not constInfo.Compared:
			self.__RenderTargetPreviewInfo()

		if app.ENABLE_MOUNT_COSTUME_SYSTEM and (itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_MOUNT):
			self.MountItemInfo()

		self.ShowToolTip()

	def AppendAntiflagInformation(self):
		antiFlagDict = {
			"|Eanti_drop|e"	 : item.ITEM_ANTIFLAG_DROP,
			"|Eanti_sell|e"	 : item.ITEM_ANTIFLAG_SELL,
			"|Eanti_shop|e"	 : item.ITEM_ANTIFLAG_MYSHOP,
			"|Eanti_safebox|e"	 : item.ITEM_ANTIFLAG_SAFEBOX,
			#"|antiflag/anti_safebox|e" : item.ITEM_ANTIFLAG_GIVE,
			#"|antiflag/anti_safebox|e" : item.ITEM_ANTIFLAG_STACK,
		}
		#antiFlagDict2 = {
		#	"|antiflag/anti_drop|e"	 : item.ITEM_ANTIFLAG_EMPIRE_A,
		#	"|antiflag/anti_sell|e"	 : item.ITEM_ANTIFLAG_EMPIRE_B,
		#	"|antiflag/anti_shop|e"	 : item.ITEM_ANTIFLAG_EMPIRE_R,
		#}
		antiFlagNames = [name for name, flag in antiFlagDict.iteritems() if item.IsAntiFlag(flag)]
		if antiFlagNames:
			self.AppendSpace(5)
			textLine1 = self.AppendTextLine(localeInfo.NOT_POSSIBLE, self.DISABLE_COLOR)
			textLine1.SetFeather()
			self.AppendSpace(5)
			textLine2 = self.AppendTextLine('{}'.format(' '.join(antiFlagNames)), self.DISABLE_COLOR)
			textLine2.SetFeather()
		#antiFlagNames2 = [name for name, flag in antiFlagDict2.iteritems() if item.IsAntiFlag(flag)]
		#if antiFlagNames2:
		#	self.AppendSpace(5)
		#	textLine3 = self.AppendTextLine(localeInfo.NOT_POSSIBLE_EQUIP, self.DISABLE_COLOR)
		#	textLine3.SetFeather()
		#	self.AppendSpace(5)
		#	textLine4 = self.AppendTextLine('{}'.format(' '.join(antiFlagNames2)), self.DISABLE_COLOR)
		#	textLine4.SetFeather()

	if constInfo.ENABLE_AURA_SYSTEM:
		def GetAbsorb(self, level):
			new_level = str(level)
			if len(new_level) == 1:
				return "0.%d"%level
			elif len(new_level) == 2:
				return "%d.%d"%(int(new_level[0]),int(new_level[1]))
			elif len(new_level) == 3:
				return "%d%d.%d"%(int(new_level[0]),int(new_level[1]),int(new_level[2]))

		def SetAuraAbsorb(self, a_pos, i_pos):
			self.ClearToolTip()#clean old shit
			aura_vnum = player.GetItemIndex(player.INVENTORY, a_pos)
			if not aura_vnum:
				return
			equip_vnum = player.GetItemIndex(player.INVENTORY, i_pos)
			if not equip_vnum:
				return
			item.SelectItem(aura_vnum)
			if item.GetItemType() != item.ITEM_TYPE_COSTUME and item.GetItemSubType() != item.COSTUME_TYPE_AURA:
				return
			self.SetTitle(item.GetItemName())
			metinSlot = [player.GetItemMetinSocket(player.INVENTORY, a_pos, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
			#attrSlot = [player.GetItemAttribute(player.INVENTORY, a_pos, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
			#AURA_LEVEL = 0
			#AURA_SUB_LEVEL = 1
			#AURA_EXP = 2
			self.AppendTextLine(localeInfo.AURA_TOOLTIP_LEVEL%(metinSlot[0],metinSlot[1]),self.CHANGELOOK_ITEMNAME_COLOR)
			self.AppendTextLine(localeInfo.AURA_TOOLTIP_ABS%float(self.GetAbsorb(metinSlot[1])),self.CHANGELOOK_ITEMNAME_COLOR)
			self.AppendTextLine(localeInfo.AURA_TOOLTIP_EXP%metinSlot[2],self.CHANGELOOK_ITEMNAME_COLOR)
			item.SelectItem(equip_vnum)
			if item.GetItemSubType() in (item.ARMOR_FOOTS, item.ARMOR_SHIELD, item.ARMOR_HEAD):
				defGradeCalc = item.GetValue(5) * 2 + item.GetValue(1)
				defGrade = defGradeCalc * metinSlot[1] / 1000
				if defGrade <= 0:
					defGrade = 1
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade), self.GetChangeTextLineColor(defGrade))
			for g in xrange(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(g)
				affectValue = affectValue * metinSlot[1] / 1000
				if affectValue <= 0:
					if affectType != 0:
						affectValue = 1
					else:
						affectValue = 0
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString:
					affectColor = self.GetChangeTextLineColor(affectValue)
					self.AppendTextLine(affectString, affectColor)
			attrSlot = []
			for w in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(player.GetItemAttribute(i_pos, w))
			if 0 != attrSlot:
				for q in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
					if q >= 7:
						continue
					else:
						type = attrSlot[q][0]
						value = attrSlot[q][1]
						if 0 == value:
							continue
						value = value * metinSlot[1] / 1000
						if value <= 0:
							if type != 0:
								value = 1
							else:
								value = 0
						affectString = self.__GetAffectString(type, value)
						if affectString:
							affectColor = self.__GetAttributeColor(q, value)
							self.AppendTextLine(affectString, affectColor)
			self.AppendWearableInformation()
			self.ShowToolTip()

	if app.ENABLE_SELL_ITEM:
		def IsSellItems(self, itemVnum, itemPrice):
			item.SelectItem(itemVnum)
			
			# if item.GetItemType() == item.ITEM_TYPE_WEAPON or item.GetItemType() == item.ITEM_TYPE_ARMOR:
				# return True
				
			if itemPrice > 1:
				return True
				
			return False


	def __DragonSoulInfoString (self, dwVnum):
		step = (dwVnum / 100) % 10
		refine = (dwVnum / 10) % 10
		if 0 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL1 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		elif 1 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL2 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		elif 2 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL3 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		elif 3 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL4 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		elif 4 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL5 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		else:
			return ""

	if app.ENABLE_MULTISHOP:
		def AppendPriceTextLine(self, price, priceVnum):
			item.SelectItem(priceVnum)
			windowBack = ui.Window()
			windowBack.SetParent(self)

			textLine = ui.TextLine()
			textLine.SetParent(windowBack)
			textLine.SetFontName(self.defFontName)
			textLine.SetPackedFontColor(self.FONT_COLOR)
			textLine.SetText("%sx" % (localeInfo.TOOLTIP_BUYPRICE % int(price)))
			textLine.SetOutline()
			textLine.SetFeather(False)
			textLine.SetPosition(0, 10)
			textLine.Show()

			itemImage = ui.ImageBox()
			itemImage.SetParent(windowBack)
			itemImage.LoadImage(item.GetIconImageFileName())
			itemImage.SetPosition(textLine.GetTextSize()[0] + 2, 0)
			itemImage.Show()

			textLineName = ui.TextLine()
			textLineName.SetParent(windowBack)
			textLineName.SetFontName(self.defFontName)
			textLineName.SetPackedFontColor(self.FONT_COLOR)
			textLineName.SetText("%s" % item.GetItemName())
			textLineName.SetOutline()
			textLineName.SetFeather(False)
			textLineName.SetPosition(textLine.GetTextSize()[0] + itemImage.GetWidth() + 4, 10)
			textLineName.Show()

			windowBack.SetPosition(0, self.toolTipHeight)
			windowBack.SetSize(textLine.GetTextSize()[0] + itemImage.GetWidth() + textLineName.GetTextSize()[0] + 6, 32)
			windowBack.SetWindowHorizontalAlignCenter()
			windowBack.Show()

			self.toolTipHeight += itemImage.GetHeight()

			self.childrenList.append(textLine)
			self.childrenList.append(textLineName)
			self.childrenList.append(itemImage)
			self.childrenList.append(windowBack)
			self.ResizeToolTip()

	## ����ΰ�?
	def __IsHair(self, itemVnum):
		return (self.__IsOldHair(itemVnum) or
			self.__IsNewHair(itemVnum) or
			self.__IsNewHair2(itemVnum) or
			self.__IsNewHair3(itemVnum) or
			self.__IsCostumeHair(itemVnum)
			)

	def __IsOldHair(self, itemVnum):
		return itemVnum > 73000 and itemVnum < 74000

	def __IsNewHair(self, itemVnum):
		return itemVnum > 74000 and itemVnum < 75000

	def __IsNewHair2(self, itemVnum):
		return itemVnum > 75000 and itemVnum < 76000

	def __IsNewHair3(self, itemVnum):
		return ((74012 < itemVnum and itemVnum < 74022) or
			(74262 < itemVnum and itemVnum < 74272) or
			(74512 < itemVnum and itemVnum < 74522) or
			(74544 < itemVnum and itemVnum < 74560) or
			(74762 < itemVnum and itemVnum < 74772) or
			(45000 < itemVnum and itemVnum < 47000))

	def __IsCostumeHair(self, itemVnum):
		return app.ENABLE_COSTUME_SYSTEM and self.__IsNewHair3(itemVnum - 100000)

	if app.ENABLE_MOUNT_COSTUME_SYSTEM:
		def MountItemInfo(self):
			self.AppendTextLine("|Ekey_ctrl|e + |Ekey_g|e" + " " + localeInfo.MOUNT_M, self.CONDITION_COLOR)
			self.AppendTextLine("|Ekey_ctrl|e + |Ekey_b|e" + " " + localeInfo.MOUNT_B, self.CONDITION_COLOR)

	if app.RENDER_TARGET:
		def __RenderTargetPreviewInfo(self):
			self.AppendTextLine("|Ekey_x|e" + " " + localeInfo.RENDER_TARGET, self.CONDITION_COLOR)

		def __ModelPreview(self, Vnum, test, model, automatic):
			if (not automatic and (not app.IsPressed(app.DIK_X) or app.IsPressed(app.DIK_LALT))) or constInfo.Compared:
				return

			# chat.AppendChat(1, "talisman_6 slot : equipped vnum: %d" % player.GetItemIndex(item.EQUIPMENT_TALISMAN_6))

			RENDER_TARGET_INDEX = 1
			
			self.ModelPreviewBoard = ui.ThinBoard()
			self.ModelPreviewBoard.SetParent(self)
			self.ModelPreviewBoard.SetSize(190+10, 210+30)
			self.ModelPreviewBoard.SetPosition(-202, 0)
			self.ModelPreviewBoard.Show()
	
			self.ModelPreview = ui.RenderTarget()
			self.ModelPreview.SetParent(self.ModelPreviewBoard)
			self.ModelPreview.SetSize(190, 210)
			self.ModelPreview.SetPosition(5, 22)
			self.ModelPreview.SetRenderTarget(RENDER_TARGET_INDEX)
			self.ModelPreview.Show()
	
			self.ModelPreviewText = ui.TextLine()
			self.ModelPreviewText.SetParent(self.ModelPreviewBoard)
			self.ModelPreviewText.SetFontName(self.defFontName)
			self.ModelPreviewText.SetPackedFontColor(grp.GenerateColor(0.8824, 0.9804, 0.8824, 1.0))
			self.ModelPreviewText.SetPosition(0, 5)
			self.ModelPreviewText.SetText("Anteprima")
			self.ModelPreviewText.SetOutline()
			self.ModelPreviewText.SetFeather(False)
			self.ModelPreviewText.SetWindowHorizontalAlignCenter()
			self.ModelPreviewText.SetHorizontalAlignCenter()
			self.ModelPreviewText.Show()
			renderTarget.SetBackground(RENDER_TARGET_INDEX, "d:/ymir work/ui/game/myshop_deco/model_view_bg.sub")
			renderTarget.SetVisibility(RENDER_TARGET_INDEX, True)
			renderTarget.SelectModel(RENDER_TARGET_INDEX, model)
			renderTarget.ChangeEffect(RENDER_TARGET_INDEX, model)

			if test == 1: #HAIR

				#Show Body-Costume/Armor
				if (player.GetItemIndex(item.COSTUME_SLOT_BODY) > 0):
					itemTransmutedVnum = player.GetItemTransmutation(item.COSTUME_SLOT_BODY)
					if not itemTransmutedVnum:
						itemTransmutedVnum = player.GetItemIndex(item.COSTUME_SLOT_BODY)
					renderTarget.SetArmor(RENDER_TARGET_INDEX, itemTransmutedVnum)
				elif (player.GetItemIndex(item.COSTUME_SLOT_BODY) < 1):
					itemTransmutedVnum = player.GetItemTransmutation(item.EQUIPMENT_BODY)
					if not itemTransmutedVnum:
						itemTransmutedVnum = player.GetItemIndex(item.EQUIPMENT_BODY)
					renderTarget.SetArmor(RENDER_TARGET_INDEX, itemTransmutedVnum)
				#End of Show Body-Costume/Armor

				#Show Weapon-Costume/Weapon
				if (player.GetItemIndex(item.COSTUME_SLOT_WEAPON) > 0):
					itemTransmutedVnum = player.GetItemTransmutation(item.COSTUME_SLOT_WEAPON)
					if not itemTransmutedVnum:
						itemTransmutedVnum = player.GetItemIndex(item.COSTUME_SLOT_WEAPON)
					renderTarget.SetWeapon(RENDER_TARGET_INDEX, itemTransmutedVnum)
				elif (player.GetItemIndex(item.COSTUME_SLOT_WEAPON) < 1):
					itemTransmutedVnum = player.GetItemTransmutation(item.EQUIPMENT_WEAPON)
					if not itemTransmutedVnum:
						itemTransmutedVnum = player.GetItemIndex(item.EQUIPMENT_WEAPON)
					renderTarget.SetWeapon(RENDER_TARGET_INDEX, itemTransmutedVnum)
				#End of Show Weapon-Costume/Weapon

				#Show Sash
				if (player.GetItemIndex(item.COSTUME_SLOT_ACCE)):
					renderTarget.SetAcce(RENDER_TARGET_INDEX,  player.GetItemIndex(item.COSTUME_SLOT_ACCE))
				#End of Show Sash

				#Show Aura
				# if (player.GetItemIndex(item.COSTUME_SLOT_AURA)):
					# renderTarget.SetAura(RENDER_TARGET_INDEX,  player.GetItemIndex(item.COSTUME_SLOT_AURA))
				#End of Show Aura

				renderTarget.SetHair(RENDER_TARGET_INDEX, Vnum)

			elif test == 2: #ARMOR
				renderTarget.SetArmor(RENDER_TARGET_INDEX, Vnum)
				#Show Hair-Costume
				if (player.GetItemIndex(item.COSTUME_SLOT_HAIR) > 0):
					itemTransmutedVnum = player.GetItemTransmutation(item.COSTUME_SLOT_HAIR)
					if not itemTransmutedVnum:
						itemTransmutedVnum = player.GetItemIndex(item.COSTUME_SLOT_HAIR)
					item.SelectItem(itemTransmutedVnum)
					renderTarget.SetHair(RENDER_TARGET_INDEX, item.GetValue(3))
				#End of Show Hair-Costume

				#Show Weapon-Costume/Weapon
				if (player.GetItemIndex(item.COSTUME_SLOT_WEAPON) > 0):
					itemTransmutedVnum = player.GetItemTransmutation(item.COSTUME_SLOT_WEAPON)
					if not itemTransmutedVnum:
						itemTransmutedVnum = player.GetItemIndex(item.COSTUME_SLOT_WEAPON)
					renderTarget.SetWeapon(RENDER_TARGET_INDEX, itemTransmutedVnum)
				elif (player.GetItemIndex(item.COSTUME_SLOT_WEAPON) < 1):
					itemTransmutedVnum = player.GetItemTransmutation(item.EQUIPMENT_WEAPON)
					if not itemTransmutedVnum:
						itemTransmutedVnum = player.GetItemIndex(item.EQUIPMENT_WEAPON)
					renderTarget.SetWeapon(RENDER_TARGET_INDEX, itemTransmutedVnum)
				#End of Show Weapon-Costume/Weapon

				#Show Sash
				if (player.GetItemIndex(item.COSTUME_SLOT_ACCE)):
					renderTarget.SetAcce(RENDER_TARGET_INDEX,  player.GetItemIndex(item.COSTUME_SLOT_ACCE))
				# End of Show Sash
				# Show Aura
				# if (player.GetItemIndex(item.COSTUME_SLOT_AURA)):
					# renderTarget.SetAura(RENDER_TARGET_INDEX,  player.GetItemIndex(item.COSTUME_SLOT_AURA))
				#End of Show Aura

			elif test == 3: #WEAPON
				#Show Body-Costume/Armor
				if (player.GetItemIndex(item.COSTUME_SLOT_BODY) > 0):
					itemTransmutedVnum = player.GetItemTransmutation(item.COSTUME_SLOT_BODY)
					if not itemTransmutedVnum:
						itemTransmutedVnum = player.GetItemIndex(item.COSTUME_SLOT_BODY)
					renderTarget.SetArmor(RENDER_TARGET_INDEX, itemTransmutedVnum)
				elif (player.GetItemIndex(item.COSTUME_SLOT_BODY) < 1):
					itemTransmutedVnum = player.GetItemTransmutation(item.EQUIPMENT_BODY)
					if not itemTransmutedVnum:
						itemTransmutedVnum = player.GetItemIndex(item.EQUIPMENT_BODY)
					renderTarget.SetArmor(RENDER_TARGET_INDEX, itemTransmutedVnum)
				#End of Show Body-Costume/Armor

				#Show Hair-Costume
				if (player.GetItemIndex(item.COSTUME_SLOT_HAIR) > 0):
					itemTransmutedVnum = player.GetItemTransmutation(item.COSTUME_SLOT_HAIR)
					if not itemTransmutedVnum:
						itemTransmutedVnum = player.GetItemIndex(item.COSTUME_SLOT_HAIR)
					item.SelectItem(itemTransmutedVnum)
					renderTarget.SetHair(RENDER_TARGET_INDEX, item.GetValue(3))
				#End of Show Hair-Costume

				#Show Sash
				if (player.GetItemIndex(item.COSTUME_SLOT_ACCE)):
					renderTarget.SetAcce(RENDER_TARGET_INDEX,  player.GetItemIndex(item.COSTUME_SLOT_ACCE))
				#End of Show Sash
				#Show Aura
				# if (player.GetItemIndex(item.COSTUME_SLOT_AURA)):
					# renderTarget.SetAura(RENDER_TARGET_INDEX,  player.GetItemIndex(item.COSTUME_SLOT_AURA))
				#End of Show Aura

				renderTarget.SetWeapon(RENDER_TARGET_INDEX, Vnum)

			elif test == 4: #SASH
				#Show Body-Costume/Armor
				if (player.GetItemIndex(item.COSTUME_SLOT_BODY) > 0):
					itemTransmutedVnum = player.GetItemTransmutation(item.COSTUME_SLOT_BODY)
					if not itemTransmutedVnum:
						itemTransmutedVnum = player.GetItemIndex(item.COSTUME_SLOT_BODY)
					renderTarget.SetArmor(RENDER_TARGET_INDEX, itemTransmutedVnum)
				elif (player.GetItemIndex(item.COSTUME_SLOT_BODY) < 1):
					itemTransmutedVnum = player.GetItemTransmutation(item.EQUIPMENT_BODY)
					if not itemTransmutedVnum:
						itemTransmutedVnum = player.GetItemIndex(item.EQUIPMENT_BODY)
					renderTarget.SetArmor(RENDER_TARGET_INDEX, itemTransmutedVnum)
				#End of Show Body-Costume/Armor

				#Show Hair-Costume
				if (player.GetItemIndex(item.COSTUME_SLOT_HAIR) > 0):
					itemTransmutedVnum = player.GetItemTransmutation(item.COSTUME_SLOT_HAIR)
					if not itemTransmutedVnum:
						itemTransmutedVnum = player.GetItemIndex(item.COSTUME_SLOT_HAIR)
					item.SelectItem(itemTransmutedVnum)
					renderTarget.SetHair(RENDER_TARGET_INDEX, item.GetValue(3))
				#End of Show Hair-Costume

				#Show Weapon-Costume/Weapon
				if (player.GetItemIndex(item.COSTUME_SLOT_WEAPON) > 0):
					itemTransmutedVnum = player.GetItemTransmutation(item.COSTUME_SLOT_WEAPON)
					if not itemTransmutedVnum:
						itemTransmutedVnum = player.GetItemIndex(item.COSTUME_SLOT_WEAPON)
					renderTarget.SetWeapon(RENDER_TARGET_INDEX, itemTransmutedVnum)
				elif (player.GetItemIndex(item.COSTUME_SLOT_WEAPON) < 1):
					itemTransmutedVnum = player.GetItemTransmutation(item.EQUIPMENT_WEAPON)
					if not itemTransmutedVnum:
						itemTransmutedVnum = player.GetItemIndex(item.EQUIPMENT_WEAPON)
					renderTarget.SetWeapon(RENDER_TARGET_INDEX, itemTransmutedVnum)
				#End of Show Weapon-Costume/Weapon

				#Show Aura
				# if (player.GetItemIndex(item.COSTUME_SLOT_AURA)):
					# renderTarget.SetAura(RENDER_TARGET_INDEX,  player.GetItemIndex(item.COSTUME_SLOT_AURA))
				#End of Show Aura
				renderTarget.SetAcce(RENDER_TARGET_INDEX, Vnum)

			#elif test == 5: #AURA
			#	#Show Body-Costume/Armor
			#	if (player.GetItemIndex(item.COSTUME_SLOT_BODY) > 0):
			#		itemTransmutedVnum = player.GetItemTransmutation(item.COSTUME_SLOT_BODY)
			#		if not itemTransmutedVnum:
			#			itemTransmutedVnum = player.GetItemIndex(item.COSTUME_SLOT_BODY)
			#		renderTarget.SetArmor(RENDER_TARGET_INDEX, itemTransmutedVnum)
			#	elif (player.GetItemIndex(item.COSTUME_SLOT_BODY) < 1):
			#		itemTransmutedVnum = player.GetItemTransmutation(item.EQUIPMENT_BODY)
			#		if not itemTransmutedVnum:
			#			itemTransmutedVnum = player.GetItemIndex(item.EQUIPMENT_BODY)
			#		renderTarget.SetArmor(RENDER_TARGET_INDEX, itemTransmutedVnum)
			#	#End of Show Body-Costume/Armor
			#
			#	#Show Hair-Costume
			#	if (player.GetItemIndex(item.COSTUME_SLOT_HAIR) > 0):
			#		itemTransmutedVnum = player.GetItemTransmutation(item.COSTUME_SLOT_HAIR)
			#		if not itemTransmutedVnum:
			#			itemTransmutedVnum = player.GetItemIndex(item.COSTUME_SLOT_HAIR)
			#		item.SelectItem(itemTransmutedVnum)
			#		renderTarget.SetHair(RENDER_TARGET_INDEX, item.GetValue(3))
			#	#End of Show Hair-Costume
			#
			#	#Show Weapon-Costume/Weapon
			#	if (player.GetItemIndex(item.COSTUME_SLOT_WEAPON) > 0):
			#		itemTransmutedVnum = player.GetItemTransmutation(item.COSTUME_SLOT_WEAPON)
			#		if not itemTransmutedVnum:
			#			itemTransmutedVnum = player.GetItemIndex(item.COSTUME_SLOT_WEAPON)
			#		renderTarget.SetWeapon(RENDER_TARGET_INDEX, itemTransmutedVnum)
			#	elif (player.GetItemIndex(item.COSTUME_SLOT_WEAPON) < 1):
			#		itemTransmutedVnum = player.GetItemTransmutation(item.EQUIPMENT_WEAPON)
			#		if not itemTransmutedVnum:
			#			itemTransmutedVnum = player.GetItemIndex(item.EQUIPMENT_WEAPON)
			#		renderTarget.SetWeapon(RENDER_TARGET_INDEX, itemTransmutedVnum)
			#	#End of Show Weapon-Costume/Weapon
			#
			#	#Show Sash
			#	if (player.GetItemIndex(item.COSTUME_SLOT_ACCE)):
			#		renderTarget.SetAcce(RENDER_TARGET_INDEX,  player.GetItemIndex(item.COSTUME_SLOT_ACCE))
			#	#End of Show Sash
			#	renderTarget.SetAura(RENDER_TARGET_INDEX, Vnum)

			elif test == 9:
				renderTarget.SelectModel(RENDER_TARGET_INDEX, model)

		def __ModelPreviewClose(self):
			RENDER_TARGET_INDEX = 1
			
			if self.ModelPreviewBoard:
				self.ModelPreviewBoard.Hide()
				self.ModelPreview.Hide()
				self.ModelPreviewText.Hide()
	
				self.ModelPreviewBoard = None
				self.ModelPreview = None
				self.ModelPreviewText = None
	
				renderTarget.SetVisibility(RENDER_TARGET_INDEX, False)


		def __ItemGetRace(self):
			race = 0
	
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN) and item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA) and item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN):
				race = 9
			elif item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR) and item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA) and item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN):
				race = 1
			elif item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR) and item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN) and item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN):
				race = 2
			elif item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR) and item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN) and item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA):
				race = 3
	
			sex = chr.RaceToSex(player.GetRace())
			MALE = 1
			FEMALE = 0
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and sex == MALE:
				race = player.GetRace() + 4
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and sex == FEMALE:
				race = player.GetRace()
			if race == 0:
				race = player.GetRace()
			if race == 9:
				race = 0
			return race

	def __AppendHairIcon(self, itemVnum):
		itemImage = ui.ImageBox()
		itemImage.SetParent(self)
		itemImage.Show()

		if self.__IsOldHair(itemVnum):
			itemImage.LoadImage("d:/ymir work/item/quest/"+str(itemVnum)+".tga")
		elif self.__IsNewHair3(itemVnum):
			itemImage.LoadImage("icon/hair/%d.sub" % (itemVnum))
		elif self.__IsNewHair(itemVnum): # ���� ��� ��ȣ�� ������Ѽ� ����Ѵ�. ���ο� �������� 1000��ŭ ��ȣ�� �þ���.
			itemImage.LoadImage("d:/ymir work/item/quest/"+str(itemVnum-1000)+".tga")
		elif self.__IsNewHair2(itemVnum):
			itemImage.LoadImage("icon/hair/%d.sub" % (itemVnum))
#		elif self.__IsCostumeHair(itemVnum):
#			itemImage.LoadImage("icon/hair/%d.sub" % (itemVnum - 100000))

		itemImage.SetPosition(itemImage.GetWidth()/2, self.toolTipHeight)
		self.toolTipHeight += itemImage.GetHeight()
		#self.toolTipWidth += itemImage.GetWidth()/2
		self.childrenList.append(itemImage)
		self.ResizeToolTip()

	## ����� ū Description �� ��� ���� ����� �����Ѵ�
	def __AdjustMaxWidth(self, attrSlot, desc):
		newToolTipWidth = self.toolTipWidth
		newToolTipWidth = max(self.__AdjustAttrMaxWidth(attrSlot), newToolTipWidth)
		newToolTipWidth = max(self.__AdjustDescMaxWidth(desc), newToolTipWidth)
		if newToolTipWidth > self.toolTipWidth:
			self.toolTipWidth = newToolTipWidth
			self.ResizeToolTip()

	def __AdjustAttrMaxWidth(self, attrSlot):
		if 0 == attrSlot:
			return self.toolTipWidth

		maxWidth = self.toolTipWidth
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			type = attrSlot[i][0]
			value = attrSlot[i][1]
			if self.ATTRIBUTE_NEED_WIDTH.has_key(type):
				if value > 0:
					maxWidth = max(self.ATTRIBUTE_NEED_WIDTH[type], maxWidth)

					# ATTR_CHANGE_TOOLTIP_WIDTH
					#self.toolTipWidth = max(self.ATTRIBUTE_NEED_WIDTH[type], self.toolTipWidth)
					#self.ResizeToolTip()
					# END_OF_ATTR_CHANGE_TOOLTIP_WIDTH

		return maxWidth

	def __AdjustDescMaxWidth(self, desc):
		if len(desc) < DESC_DEFAULT_MAX_COLS:
			return self.toolTipWidth

		return DESC_WESTERN_MAX_WIDTH

	def __SetSkillBookToolTip(self, skillIndex, bookName, skillGrade):
		skillName = skill.GetSkillName(skillIndex)

		if not skillName:
			return

		if localeInfo.IsVIETNAM():
			itemName = bookName + " " + skillName
		else:
			itemName = skillName + " " + bookName
		self.SetTitle(itemName)

	def __AppendPickInformation(self, curLevel, curEXP, maxEXP):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_PICK_LEVEL % (curLevel), self.NORMAL_COLOR)
		self.AppendTextLine(localeInfo.TOOLTIP_PICK_EXP % (curEXP, maxEXP), self.NORMAL_COLOR)

		if curEXP == maxEXP:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE1, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE2, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE3, self.NORMAL_COLOR)


	def __AppendRodInformation(self, curLevel, curEXP, maxEXP):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_LEVEL % (curLevel), self.NORMAL_COLOR)
		self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_EXP % (curEXP, maxEXP), self.NORMAL_COLOR)

		if curEXP == maxEXP:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_UPGRADE1, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_UPGRADE2, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_UPGRADE3, self.NORMAL_COLOR)

	def __AppendLimitInformation(self):

		appendSpace = False

		for i in xrange(item.LIMIT_MAX_NUM):

			(limitType, limitValue) = item.GetLimit(i)

			if limitValue > 0:
				if False == appendSpace:
					self.AppendSpace(5)
					appendSpace = True

			else:
				continue

			if item.LIMIT_LEVEL == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.LEVEL), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_LEVEL % (limitValue), color)
			"""
			elif item.LIMIT_STR == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.ST), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_STR % (limitValue), color)
			elif item.LIMIT_DEX == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.DX), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_DEX % (limitValue), color)
			elif item.LIMIT_INT == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.IQ), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_INT % (limitValue), color)
			elif item.LIMIT_CON == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.HT), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_CON % (limitValue), color)
			"""

	## cyh itemseal 2013 11 11
	def __AppendSealInformation(self, window_type, slotIndex):
		if not app.ENABLE_SOULBIND_SYSTEM:
			return

		itemSealDate = player.GetItemSealDate(window_type, slotIndex)
		if itemSealDate == item.GetDefaultSealDate():
			return

		if itemSealDate == item.GetUnlimitedSealDate():
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_SEALED, self.NEGATIVE_COLOR)

		elif itemSealDate > 0:
			self.AppendSpace(5)
			hours, minutes = player.GetItemUnSealLeftTime(window_type, slotIndex)
			self.AppendTextLine(localeInfo.TOOLTIP_UNSEAL_LEFT_TIME % (hours, minutes), self.NEGATIVE_COLOR)

	def __GetAffectString(self, affectType, affectValue):
		if 0 == affectType:
			return None

		if 0 == affectValue:
			return None

		try:
			return self.AFFECT_DICT[affectType](affectValue)
		except TypeError:
			return "UNKNOWN_VALUE[%s] %s" % (affectType, affectValue)
		except KeyError:
			return "UNKNOWN_TYPE[%s] %s" % (affectType, affectValue)

	def __AppendAffectInformation(self):
		for i in xrange(item.ITEM_APPLY_MAX_NUM):

			(affectType, affectValue) = item.GetAffect(i)

			affectString = self.__GetAffectString(affectType, affectValue)
			if affectString:
				self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

	def AppendWearableInformation(self):

		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_ITEM_WEARABLE_JOB, self.NORMAL_COLOR)

		flagList = (
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN))
		if app.ENABLE_WOLFMAN_CHARACTER:
			flagList += (not item.IsAntiFlag(item.ITEM_ANTIFLAG_WOLFMAN),)
		characterNames = ""
		for i in xrange(self.CHARACTER_COUNT):

			name = self.CHARACTER_NAMES[i]
			flag = flagList[i]

			if flag:
				characterNames += " "
				characterNames += name

		textLine = self.AppendTextLine(characterNames, self.NORMAL_COLOR, True)
		textLine.SetFeather()

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
			textLine = self.AppendTextLine(localeInfo.FOR_FEMALE, self.NORMAL_COLOR, True)
			textLine.SetFeather()

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
			textLine = self.AppendTextLine(localeInfo.FOR_MALE, self.NORMAL_COLOR, True)
			textLine.SetFeather()

	def __AppendPotionInformation(self):
		self.AppendSpace(5)

		healHP = item.GetValue(0)
		healSP = item.GetValue(1)
		healStatus = item.GetValue(2)
		healPercentageHP = item.GetValue(3)
		healPercentageSP = item.GetValue(4)

		if healHP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_HP_POINT % healHP, self.GetChangeTextLineColor(healHP))
		if healSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_SP_POINT % healSP, self.GetChangeTextLineColor(healSP))
		if healStatus != 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_CURE)
		if healPercentageHP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_HP_PERCENT % healPercentageHP, self.GetChangeTextLineColor(healPercentageHP))
		if healPercentageSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_SP_PERCENT % healPercentageSP, self.GetChangeTextLineColor(healPercentageSP))

	def __AppendAbilityPotionInformation(self):

		self.AppendSpace(5)

		abilityType = item.GetValue(0)
		time = item.GetValue(1)
		point = item.GetValue(2)

		if abilityType == item.APPLY_ATT_SPEED:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_ATTACK_SPEED % point, self.GetChangeTextLineColor(point))
		elif abilityType == item.APPLY_MOV_SPEED:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_MOVING_SPEED % point, self.GetChangeTextLineColor(point))

		if time > 0:
			minute = (time / 60)
			second = (time % 60)
			timeString = localeInfo.TOOLTIP_POTION_TIME

			if minute > 0:
				timeString += str(minute) + localeInfo.TOOLTIP_POTION_MIN
			if second > 0:
				timeString += " " + str(second) + localeInfo.TOOLTIP_POTION_SEC

			self.AppendTextLine(timeString)

	if app.ENABLE_OFFLINE_SHOP_SYSTEM:
		def AppendItemBuyer(self, itemBuyer):
			self.AppendSpace(5)
			self.AppendTextLine('Bought by: %s' % itemBuyer, self.DISABLE_COLOR)

	def GetPriceColor(self, price):
		if price>=constInfo.HIGH_PRICE:
			return self.HIGH_PRICE_COLOR
		if price>=constInfo.MIDDLE_PRICE:
			return self.MIDDLE_PRICE_COLOR
		else:
			return self.LOW_PRICE_COLOR


	def AppendPrice(self, price):
		if app.ENABLE_CHEQUE_SYSTEM:
			self.AppendTextLine(localeInfo.NumberToMoneyString(price), self.GetPriceColor(price))
			#self.AppendTextLine(localeInfo.TOOLTIP_BUYPRICE , self.SHOP_ITEM_COLOR)
		else:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_BUYPRICE  % (localeInfo.NumberToMoneyString(price)), self.GetPriceColor(price))
		
	def AppendPriceBySecondaryCoin(self, price):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_BUYPRICE  % (localeInfo.NumberToSecondaryCoinString(price)), self.GetPriceColor(price))

	def AppendSellingPrice(self, price):
		if item.IsAntiFlag(item.ITEM_ANTIFLAG_SELL):			
			self.AppendTextLine(localeInfo.TOOLTIP_ANTI_SELL, self.DISABLE_COLOR)
			self.AppendSpace(5)
		else:
			self.AppendTextLine(localeInfo.TOOLTIP_SELLPRICE % (localeInfo.NumberToMoneyString(price)), self.GetPriceColor(price))
			self.AppendSpace(5)

	def AppendMetinInformation(self):
		if constInfo.ENABLE_FULLSTONE_DETAILS:
			for i in xrange(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString:
					self.AppendSpace(5)
					self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

	def AppendMetinWearInformation(self):

		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_SOCKET_REFINABLE_ITEM, self.NORMAL_COLOR)

		flagList = (item.IsWearableFlag(item.WEARABLE_BODY),
					item.IsWearableFlag(item.WEARABLE_HEAD),
					item.IsWearableFlag(item.WEARABLE_FOOTS),
					item.IsWearableFlag(item.WEARABLE_WRIST),
					item.IsWearableFlag(item.WEARABLE_WEAPON),
					item.IsWearableFlag(item.WEARABLE_NECK),
					item.IsWearableFlag(item.WEARABLE_EAR),
					item.IsWearableFlag(item.WEARABLE_UNIQUE),
					item.IsWearableFlag(item.WEARABLE_SHIELD),
					item.IsWearableFlag(item.WEARABLE_ARROW))

		wearNames = ""
		for i in xrange(self.WEAR_COUNT):

			name = self.WEAR_NAMES[i]
			flag = flagList[i]

			if flag:
				wearNames += "  "
				wearNames += name

		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
		textLine.SetHorizontalAlignCenter()
		textLine.SetPackedFontColor(self.NORMAL_COLOR)
		textLine.SetText(wearNames)
		textLine.Show()
		self.childrenList.append(textLine)

		self.toolTipHeight += self.TEXT_LINE_HEIGHT
		self.ResizeToolTip()

	def GetMetinSocketType(self, number):
		if player.METIN_SOCKET_TYPE_NONE == number:
			return player.METIN_SOCKET_TYPE_NONE
		elif player.METIN_SOCKET_TYPE_SILVER == number:
			return player.METIN_SOCKET_TYPE_SILVER
		elif player.METIN_SOCKET_TYPE_GOLD == number:
			return player.METIN_SOCKET_TYPE_GOLD
		else:
			item.SelectItem(number)
			if item.METIN_NORMAL == item.GetItemSubType():
				return player.METIN_SOCKET_TYPE_SILVER
			elif item.METIN_GOLD == item.GetItemSubType():
				return player.METIN_SOCKET_TYPE_GOLD
			elif "USE_PUT_INTO_ACCESSORY_SOCKET" == item.GetUseType(number):
				return player.METIN_SOCKET_TYPE_SILVER
			elif "USE_PUT_INTO_RING_SOCKET" == item.GetUseType(number):
				return player.METIN_SOCKET_TYPE_SILVER
			elif "USE_PUT_INTO_BELT_SOCKET" == item.GetUseType(number):
				return player.METIN_SOCKET_TYPE_SILVER

		return player.METIN_SOCKET_TYPE_NONE

	def GetMetinItemIndex(self, number):
		if player.METIN_SOCKET_TYPE_SILVER == number:
			return 0
		if player.METIN_SOCKET_TYPE_GOLD == number:
			return 0

		return number

	def __AppendAccessoryMetinSlotInfo(self, metinSlot, mtrlVnum):
		ACCESSORY_SOCKET_MAX_SIZE = 3

		cur=min(metinSlot[0], ACCESSORY_SOCKET_MAX_SIZE)
		end=min(metinSlot[1], ACCESSORY_SOCKET_MAX_SIZE)

		affectType1, affectValue1 = item.GetAffect(0)
		affectList1=[0, max(1, affectValue1*10/100), max(2, affectValue1*20/100), max(3, affectValue1*40/100)]

		affectType2, affectValue2 = item.GetAffect(1)
		affectList2=[0, max(1, affectValue2*10/100), max(2, affectValue2*20/100), max(3, affectValue2*40/100)]

		affectType3, affectValue3 = item.GetAffect(2)
		affectList3=[0, max(1, affectValue3*10/100), max(2, affectValue3*20/100), max(3, affectValue3*40/100)]

		mtrlPos=0
		mtrlList=[mtrlVnum]*cur+[player.METIN_SOCKET_TYPE_SILVER]*(end-cur)
		for mtrl in mtrlList:
			affectString1 = self.__GetAffectString(affectType1, affectList1[mtrlPos+1]-affectList1[mtrlPos])
			affectString2 = self.__GetAffectString(affectType2, affectList2[mtrlPos+1]-affectList2[mtrlPos])
			affectString3 = self.__GetAffectString(affectType3, affectList3[mtrlPos+1]-affectList3[mtrlPos])

			leftTime = 0
			if cur == mtrlPos+1:
				leftTime=metinSlot[2]

			self.__AppendMetinSlotInfo_AppendMetinSocketData(mtrlPos, mtrl, affectString1, affectString2, affectString3, leftTime)
			mtrlPos+=1

	def __AppendMetinSlotInfo(self, metinSlot):
		if self.__AppendMetinSlotInfo_IsEmptySlotList(metinSlot):
			return

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			self.__AppendMetinSlotInfo_AppendMetinSocketData(i, metinSlot[i])

	def __AppendMetinSlotInfo_IsEmptySlotList(self, metinSlot):
		if 0 == metinSlot:
			return 1

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlotData=metinSlot[i]
			if 0 != self.GetMetinSocketType(metinSlotData):
				if 0 != self.GetMetinItemIndex(metinSlotData):
					return 0

		return 1

	def __AppendMetinSlotInfo_AppendMetinSocketData(self, index, metinSlotData, custumAffectString="", custumAffectString2="", custumAffectString3="", leftTime=0):

		slotType = self.GetMetinSocketType(metinSlotData)
		itemIndex = self.GetMetinItemIndex(metinSlotData)

		if 0 == slotType:
			return

		self.AppendSpace(5)

		slotImage = ui.ImageBox()
		slotImage.SetParent(self)
		slotImage.Show()

		## Name
		nameTextLine = ui.TextLine()
		nameTextLine.SetParent(self)
		nameTextLine.SetFontName(self.defFontName)
		nameTextLine.SetPackedFontColor(self.NORMAL_COLOR)
		nameTextLine.SetOutline()
		nameTextLine.SetFeather()
		nameTextLine.Show()

		self.childrenList.append(nameTextLine)

		if player.METIN_SOCKET_TYPE_SILVER == slotType:
			slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_silver.sub")
		elif player.METIN_SOCKET_TYPE_GOLD == slotType:
			slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_gold.sub")

		self.childrenList.append(slotImage)

		if localeInfo.IsARABIC():
			slotImage.SetPosition(self.toolTipWidth - slotImage.GetWidth() - 9, self.toolTipHeight-1)
			nameTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 2)
		else:
			slotImage.SetPosition(9, self.toolTipHeight-1)
			nameTextLine.SetPosition(50, self.toolTipHeight + 2)

		metinImage = ui.ImageBox()
		metinImage.SetParent(self)
		metinImage.Show()
		self.childrenList.append(metinImage)

		if itemIndex:

			item.SelectItem(itemIndex)

			## Image
			try:
				metinImage.LoadImage(item.GetIconImageFileName())
			except:
				dbg.TraceError("ItemToolTip.__AppendMetinSocketData() - Failed to find image file %d:%s" %
					(itemIndex, item.GetIconImageFileName())
				)

			nameTextLine.SetText(item.GetItemName())

			## Affect
			affectTextLine = ui.TextLine()
			affectTextLine.SetParent(self)
			affectTextLine.SetFontName(self.defFontName)
			affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
			affectTextLine.SetOutline()
			affectTextLine.SetFeather()
			affectTextLine.Show()

			if localeInfo.IsARABIC():
				metinImage.SetPosition(self.toolTipWidth - metinImage.GetWidth() - 10, self.toolTipHeight)
				affectTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 16 + 2)
			else:
				metinImage.SetPosition(10, self.toolTipHeight)
				affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2)

			if custumAffectString:
				affectTextLine.SetText(custumAffectString)
			elif itemIndex!=constInfo.ERROR_METIN_STONE:
				affectType, affectValue = item.GetAffect(0)
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString:
					affectTextLine.SetText(affectString)
			else:
				affectTextLine.SetText(localeInfo.TOOLTIP_APPLY_NOAFFECT)

			self.childrenList.append(affectTextLine)

			if constInfo.ENABLE_FULLSTONE_DETAILS and (not custumAffectString2) and (itemIndex!=constInfo.ERROR_METIN_STONE):
				custumAffectString2 = self.__GetAffectString(*item.GetAffect(1))

			if custumAffectString2:
				affectTextLine = ui.TextLine()
				affectTextLine.SetParent(self)
				affectTextLine.SetFontName(self.defFontName)
				affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
				affectTextLine.SetOutline()
				affectTextLine.SetFeather()
				affectTextLine.Show()
				affectTextLine.SetText(custumAffectString2)
				self.childrenList.append(affectTextLine)
				self.toolTipHeight += 16 + 2

			if constInfo.ENABLE_FULLSTONE_DETAILS and (not custumAffectString3) and (itemIndex!=constInfo.ERROR_METIN_STONE):
				custumAffectString3 = self.__GetAffectString(*item.GetAffect(2))

			if custumAffectString3:
				affectTextLine = ui.TextLine()
				affectTextLine.SetParent(self)
				affectTextLine.SetFontName(self.defFontName)
				affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
				affectTextLine.SetOutline()
				affectTextLine.SetFeather()
				affectTextLine.Show()
				affectTextLine.SetText(custumAffectString3)
				self.childrenList.append(affectTextLine)
				self.toolTipHeight += 16 + 2

			if 0 != leftTime:
				timeText = (localeInfo.LEFT_TIME + " : " + localeInfo.SecondToDHM(leftTime))

				timeTextLine = ui.TextLine()
				timeTextLine.SetParent(self)
				timeTextLine.SetFontName(self.defFontName)
				timeTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				timeTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
				timeTextLine.SetOutline()
				timeTextLine.SetFeather()
				timeTextLine.Show()
				timeTextLine.SetText(timeText)
				self.childrenList.append(timeTextLine)
				self.toolTipHeight += 16 + 2

		else:
			nameTextLine.SetText(localeInfo.TOOLTIP_SOCKET_EMPTY)

		self.toolTipHeight += 35
		self.ResizeToolTip()

	def __AppendFishInfo(self, size):
		if size > 0:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_FISH_LEN % (float(size) / 100.0), self.NORMAL_COLOR)

	def AppendUniqueItemLastTime(self, restMin):
		if restMin > 0:
			restSecond = restMin*60
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.LEFT_TIME + " : " + localeInfo.SecondToHM(restSecond), self.NORMAL_COLOR)

	def AppendMallItemLastTime(self, endTime):
		if endTime > 0:
			leftSec = max(0, endTime - app.GetGlobalTimeStamp())
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.LEFT_TIME + " : " + localeInfo.SecondToDHM(leftSec), self.NORMAL_COLOR)

	def AppendTimerBasedOnWearLastTime(self, metinSlot):
		if 0 == metinSlot[0]:
			self.AppendSpace(5)
			#self.AppendTextLine(localeInfo.CANNOT_USE, self.DISABLE_COLOR)
		else:
			endTime = app.GetGlobalTimeStamp() + metinSlot[0]
			self.AppendMallItemLastTime(endTime)

	def AppendRealTimeStartFirstUseLastTime(self, item, metinSlot, limitIndex):
		useCount = metinSlot[1]
		endTime = metinSlot[0]

		# �� ���̶� ����ߴٸ� Socket0�� ���� �ð�(2012�� 3�� 1�� 13�� 01�� ����..) �� ��������.
		# ������� �ʾҴٸ� Socket0�� �̿밡�ɽð�(�̸��׸� 600 ���� ��. �ʴ���)�� ������� �� �ְ�, 0�̶�� Limit Value�� �ִ� �̿밡�ɽð��� ����Ѵ�.
		if 0 == useCount:
			if 0 == endTime:
				(limitType, limitValue) = item.GetLimit(limitIndex)
				endTime = limitValue

			endTime += app.GetGlobalTimeStamp()

		self.AppendMallItemLastTime(endTime)

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def SetAcceResultItem(self, slotIndex, window_type = player.INVENTORY):
			(itemVnum, MinAbs, MaxAbs) = acce.GetResultItem()
			if not itemVnum:
				return
			
			self.ClearToolTip()
			
			metinSlot = [player.GetItemMetinSocket(window_type, slotIndex, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
			attrSlot = [player.GetItemAttribute(window_type, slotIndex, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
			
			item.SelectItem(itemVnum)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			if itemType != item.ITEM_TYPE_COSTUME and itemSubType != item.COSTUME_TYPE_ACCE:
				return
			
			absChance = MaxAbs
			itemDesc = item.GetItemDescription()
			self.__AdjustMaxWidth(attrSlot, itemDesc)
			self.__SetItemTitle(itemVnum, metinSlot, attrSlot)
			self.AppendDescription(itemDesc, 26)
			self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
			self.__AppendLimitInformation()
			
			## ABSORPTION RATE
			if MinAbs == MaxAbs:
				self.AppendTextLine(localeInfo.ACCE_ABSORB_CHANCE % (MinAbs), self.CONDITION_COLOR)
			else:
				self.AppendTextLine(localeInfo.ACCE_ABSORB_CHANCE2 % (MinAbs, MaxAbs), self.CONDITION_COLOR)
			## END ABSOPRTION RATE
			
			itemAbsorbedVnum = int(metinSlot[acce.ABSORBED_SOCKET])
			if itemAbsorbedVnum:
				## ATTACK / DEFENCE
				item.SelectItem(itemAbsorbedVnum)
				if item.GetItemType() == item.ITEM_TYPE_WEAPON:
					if item.GetItemSubType() == item.WEAPON_FAN:
						self.__AppendMagicAttackInfo(absChance)
						item.SelectItem(itemAbsorbedVnum)
						self.__AppendAttackPowerInfo(absChance)
					else:
						self.__AppendAttackPowerInfo(absChance)
						item.SelectItem(itemAbsorbedVnum)
						self.__AppendMagicAttackInfo(absChance)
				elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
					defGrade = item.GetValue(1)
					defBonus = item.GetValue(5) * 2
					defGrade = self.CalcAcceValue(defGrade, absChance)
					defBonus = self.CalcAcceValue(defBonus, absChance)
					
					if defGrade > 0:
						self.AppendSpace(5)
						self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus), self.GetChangeTextLineColor(defGrade))
					
					item.SelectItem(itemAbsorbedVnum)
					self.__AppendMagicDefenceInfo(absChance)
				## END ATTACK / DEFENCE
				
				## EFFECT
				item.SelectItem(itemAbsorbedVnum)
				for i in xrange(item.ITEM_APPLY_MAX_NUM):
					(affectType, affectValue) = item.GetAffect(i)
					affectValue = self.CalcAcceValue(affectValue, absChance)
					affectString = self.__GetAffectString(affectType, affectValue)
					if affectString and affectValue > 0:
						self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))
					
					item.SelectItem(itemAbsorbedVnum)
				# END EFFECT
				
			item.SelectItem(itemVnum)
			## ATTR
			self.__AppendAttributeInformation(attrSlot, MaxAbs)
			# END ATTR
			
			self.AppendWearableInformation()
			self.ShowToolTip()

		def SetAcceResultAbsItem(self, slotIndex1, slotIndex2, window_type = player.INVENTORY):
			itemVnumAcce = player.GetItemIndex(window_type, slotIndex1)
			itemVnumTarget = player.GetItemIndex(window_type, slotIndex2)
			if not itemVnumAcce or not itemVnumTarget:
				return
			
			self.ClearToolTip()
			
			item.SelectItem(itemVnumAcce)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			if itemType != item.ITEM_TYPE_COSTUME and itemSubType != item.COSTUME_TYPE_ACCE:
				return
			
			metinSlot = [player.GetItemMetinSocket(window_type, slotIndex1, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
			attrSlot = [player.GetItemAttribute(window_type, slotIndex2, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
			
			itemDesc = item.GetItemDescription()
			self.__AdjustMaxWidth(attrSlot, itemDesc)
			self.__SetItemTitle(itemVnumAcce, metinSlot, attrSlot)
			self.AppendDescription(itemDesc, 26)
			self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
			item.SelectItem(itemVnumAcce)
			self.__AppendLimitInformation()
			
			## ABSORPTION RATE
			self.AppendTextLine(localeInfo.ACCE_ABSORB_CHANCE % (metinSlot[acce.ABSORPTION_SOCKET]), self.CONDITION_COLOR)
			## END ABSOPRTION RATE
			
			## ATTACK / DEFENCE
			itemAbsorbedVnum = itemVnumTarget
			item.SelectItem(itemAbsorbedVnum)
			if item.GetItemType() == item.ITEM_TYPE_WEAPON:
				if item.GetItemSubType() == item.WEAPON_FAN:
					self.__AppendMagicAttackInfo(metinSlot[acce.ABSORPTION_SOCKET])
					item.SelectItem(itemAbsorbedVnum)
					self.__AppendAttackPowerInfo(metinSlot[acce.ABSORPTION_SOCKET])
				else:
					self.__AppendAttackPowerInfo(metinSlot[acce.ABSORPTION_SOCKET])
					item.SelectItem(itemAbsorbedVnum)
					self.__AppendMagicAttackInfo(metinSlot[acce.ABSORPTION_SOCKET])
			elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
				defGrade = item.GetValue(1)
				defBonus = item.GetValue(5) * 2
				defGrade = self.CalcAcceValue(defGrade, metinSlot[acce.ABSORPTION_SOCKET])
				defBonus = self.CalcAcceValue(defBonus, metinSlot[acce.ABSORPTION_SOCKET])
				
				if defGrade > 0:
					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus), self.GetChangeTextLineColor(defGrade))
				
				item.SelectItem(itemAbsorbedVnum)
				self.__AppendMagicDefenceInfo(metinSlot[acce.ABSORPTION_SOCKET])
			## END ATTACK / DEFENCE
			
			## EFFECT
			item.SelectItem(itemAbsorbedVnum)
			for i in xrange(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)
				affectValue = self.CalcAcceValue(affectValue, metinSlot[acce.ABSORPTION_SOCKET])
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString and affectValue > 0:
					self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))
				
				item.SelectItem(itemAbsorbedVnum)
			## END EFFECT
			
			## ATTR
			item.SelectItem(itemAbsorbedVnum)
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				type = attrSlot[i][0]
				value = attrSlot[i][1]
				if not value:
					continue
				
				value = self.CalcAcceValue(value, metinSlot[acce.ABSORPTION_SOCKET])
				affectString = self.__GetAffectString(type, value, 1)
				if affectString and value > 0:
					affectColor = self.__GetAttributeColor(i, value)
					self.AppendTextLine(affectString, affectColor)
				
				item.SelectItem(itemAbsorbedVnum)
			## END ATTR
			
			## WEARABLE
			item.SelectItem(itemVnumAcce)
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_WEARABLE_JOB, self.NORMAL_COLOR)
			
			item.SelectItem(itemVnumAcce)
			flagList = (
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN)
			)
			
			if app.ENABLE_WOLFMAN_CHARACTER:
				flagList += (not item.IsAntiFlag(item.ITEM_ANTIFLAG_WOLFMAN),)
			
			characterNames = ""
			for i in xrange(self.CHARACTER_COUNT):
				name = self.CHARACTER_NAMES[i]
				flag = flagList[i]
				if flag:
					characterNames += " "
					characterNames += name
			
			textLine = self.AppendTextLine(characterNames, self.NORMAL_COLOR, True)
			textLine.SetFeather()
			
			item.SelectItem(itemVnumAcce)
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
				textLine = self.AppendTextLine(localeInfo.FOR_FEMALE, self.NORMAL_COLOR, True)
				textLine.SetFeather()
			
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
				textLine = self.AppendTextLine(localeInfo.FOR_MALE, self.NORMAL_COLOR, True)
				textLine.SetFeather()
			## END WEARABLE	
			self.ShowToolTip()
			
	if app.ENABLE_CHANGELOOK_SYSTEM:
		def AppendTransmutation(self, window_type, slotIndex, transmutation):
			itemVnum = 0
			if transmutation == -1:
				if window_type == player.INVENTORY:
					itemVnum = player.GetItemTransmutation(window_type, slotIndex)
				elif window_type == player.SAFEBOX:
					itemVnum = safebox.GetItemTransmutation(slotIndex)
			else:
				itemVnum = transmutation
			
			if not itemVnum:
				return
			
			item.SelectItem(itemVnum)
			itemName = item.GetItemName()
			if not itemName or itemName == "":

				return
			
			self.AppendSpace(5)
			title = "[ " + localeInfo.CHANGE_LOOK_TITLE + " ]"
			self.AppendTextLine(title, self.NORMAL_COLOR)
			textLine = self.AppendTextLine(itemName, self.CONDITION_COLOR, True)
			textLine.SetFeather()
			

class HyperlinkItemToolTip(ItemToolTip):
	def __init__(self):
		ItemToolTip.__init__(self, isPickable=True)

	def SetHyperlinkItem(self, tokens):
		minTokenCount = 3 + player.METIN_SOCKET_MAX_NUM
		if app.ENABLE_CHANGELOOK_SYSTEM:
			minTokenCount += 1
		maxTokenCount = minTokenCount + 3 * player.ATTRIBUTE_SLOT_MAX_NUM
		if tokens and len(tokens) >= minTokenCount and len(tokens) <= maxTokenCount:
			head, vnum, flag = tokens[:3]
			itemVnum = int(vnum, 16)
			metinSlot = [int(metin, 16) for metin in tokens[3:3+player.METIN_SOCKET_MAX_NUM]]

			rests = tokens[3+player.METIN_SOCKET_MAX_NUM:]
			transmutation = 0
			if app.ENABLE_CHANGELOOK_SYSTEM:
				cur_index = 3 + player.METIN_SOCKET_MAX_NUM
				rests = tokens[cur_index+1:]
				cnv = [int(cnv, 16) for cnv in tokens[cur_index:cur_index+1]]
				transmutation = int(cnv[0])
			if rests:
				attrSlot = []
				
				rests.reverse()
				while rests:
					key = int(rests.pop(), 16)
					
					if rests:
						val = int(rests.pop())
						froz = int(rests.pop())
						attrSlot.append((key, val, froz))

				attrSlot += [(0, 0, 0)] * (player.ATTRIBUTE_SLOT_MAX_NUM - len(attrSlot))
			else:
				attrSlot = [(0, 0, 0)] * player.ATTRIBUTE_SLOT_MAX_NUM

			self.ClearToolTip()
			if app.ENABLE_CHANGELOOK_SYSTEM:
				if not transmutation:
					if app.RENDER_TARGET:
						self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 1)
					else:
						self.AddItemData(itemVnum, metinSlot, attrSlot)
				else:
					if app.RENDER_TARGET:
						self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 1, 0, 0, player.INVENTORY, -1, transmutation)
					else:
						self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, player.INVENTORY, -1, transmutation)
			else:
				if app.RENDER_TARGET:
					self.AddItemData(itemVnum, metinSlot, attrSlot, 1, 1)
				else:
					self.AddItemData(itemVnum, metinSlot, attrSlot)

			ItemToolTip.OnUpdate(self)

	def OnUpdate(self):
		pass

	def OnMouseLeftButtonDown(self):
		self.Hide()

if app.ENABLE_SPECIAL_STATS_SYSTEM:
	class SpecialStatsToolTip(ToolTip):

		def __init__(self):
			ToolTip.__init__(self, 200)
			self.skillLevel = { 1 : 0,
								2 : 0,
								3 : 0,
								4 : 0,
								5 : 0,
								6 : 0
							  }
			
		def __del__(self):
			ToolTip.__del__(self)
			
		def UpdateSkillLevel(self, skillIndex, level):
			self.skillLevel[skillIndex] = level
			

		def AppendSkillLevel(self, skill):
			self.AutoAppendTextLine("Livello Skill:%d" % self.skillLevel[skill], grp.GenerateColor(1, 0.4705, 0, 1.0))
			
		def AppendSkillDesc(self, desc, isNextLevel = False):
			if isNextLevel:
				self.AutoAppendTextLine("Prossimo Livello", grp.GenerateColor(0, 0.4980, 1, 1.0))
				self.AppendDescription( desc, 26, grp.GenerateColor(0.1333, 0.5450, 0.1333, 1.0))
			else:
				self.AppendDescription( desc, 26)
			
		def GetStatLevel(self, skillIndex):
			return self.skillLevel[skillIndex]
			

class SkillToolTip(ToolTip):

	POINT_NAME_DICT = {
		player.LEVEL : localeInfo.SKILL_TOOLTIP_LEVEL,
		player.IQ : localeInfo.SKILL_TOOLTIP_INT,
	}

	SKILL_TOOL_TIP_WIDTH = 200
	PARTY_SKILL_TOOL_TIP_WIDTH = 340

	PARTY_SKILL_EXPERIENCE_AFFECT_LIST = (	( 2, 2,  10,),
											( 8, 3,  20,),
											(14, 4,  30,),
											(22, 5,  45,),
											(28, 6,  60,),
											(34, 7,  80,),
											(38, 8, 100,), )

	PARTY_SKILL_PLUS_GRADE_AFFECT_LIST = (	( 4, 2, 1, 0,),
											(10, 3, 2, 0,),
											(16, 4, 2, 1,),
											(24, 5, 2, 2,), )

	PARTY_SKILL_ATTACKER_AFFECT_LIST = (	( 36, 3, ),
											( 26, 1, ),
											( 32, 2, ), )

	SKILL_GRADE_NAME = {	player.SKILL_GRADE_MASTER : localeInfo.SKILL_GRADE_NAME_MASTER,
							player.SKILL_GRADE_GRAND_MASTER : localeInfo.SKILL_GRADE_NAME_GRAND_MASTER,
							player.SKILL_GRADE_PERFECT_MASTER : localeInfo.SKILL_GRADE_NAME_PERFECT_MASTER, }

	AFFECT_NAME_DICT =	{
							"HP" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_POWER,
							"ATT_GRADE" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_GRADE,
							"DEF_GRADE" : localeInfo.TOOLTIP_SKILL_AFFECT_DEF_GRADE,
							"ATT_SPEED" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_SPEED,
							"MOV_SPEED" : localeInfo.TOOLTIP_SKILL_AFFECT_MOV_SPEED,
							"DODGE" : localeInfo.TOOLTIP_SKILL_AFFECT_DODGE,
							"RESIST_NORMAL" : localeInfo.TOOLTIP_SKILL_AFFECT_RESIST_NORMAL,
							"REFLECT_MELEE" : localeInfo.TOOLTIP_SKILL_AFFECT_REFLECT_MELEE,
						}
	AFFECT_APPEND_TEXT_DICT =	{
									"DODGE" : "%",
									"RESIST_NORMAL" : "%",
									"REFLECT_MELEE" : "%",
								}

	def __init__(self):
		ToolTip.__init__(self, self.SKILL_TOOL_TIP_WIDTH)
	def __del__(self):
		ToolTip.__del__(self)

	def SetSkill(self, skillIndex, skillLevel = -1):

		if 0 == skillIndex:
			return

		if skill.SKILL_TYPE_GUILD == skill.GetSkillType(skillIndex):

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendGuildSkillData(skillIndex, skillLevel)

		else:

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			skillGrade = player.GetSkillGrade(slotIndex)
			skillLevel = player.GetSkillLevel(slotIndex)
			skillCurrentPercentage = player.GetSkillCurrentEfficientPercentage(slotIndex)
			skillNextPercentage = player.GetSkillNextEfficientPercentage(slotIndex)

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendSkillDataNew(slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage)
			self.AppendSkillRequirement(skillIndex, skillLevel)

		self.ShowToolTip()

	def SetSkillNew(self, slotIndex, skillIndex, skillGrade, skillLevel):

		if 0 == skillIndex:
			return

		if player.SKILL_INDEX_TONGSOL == skillIndex:

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			skillLevel = player.GetSkillLevel(slotIndex)

			self.AppendDefaultData(skillIndex)
			self.AppendPartySkillData(skillGrade, skillLevel)

		elif player.SKILL_INDEX_RIDING == skillIndex:

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			self.AppendSupportSkillDefaultData(skillIndex, skillGrade, skillLevel, 30)

		elif player.SKILL_INDEX_SUMMON == skillIndex:

			maxLevel = 10

			self.ClearToolTip()
			self.__SetSkillTitle(skillIndex, skillGrade)

			## Description
			description = skill.GetSkillDescription(skillIndex)
			self.AppendDescription(description, 25)

			if skillLevel == 10:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (skillLevel*10), self.NORMAL_COLOR)

			else:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
				self.__AppendSummonDescription(skillLevel, self.NORMAL_COLOR)

				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel+1), self.NEGATIVE_COLOR)
				self.__AppendSummonDescription(skillLevel+1, self.NEGATIVE_COLOR)

		elif skill.SKILL_TYPE_GUILD == skill.GetSkillType(skillIndex):

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendGuildSkillData(skillIndex, skillLevel)

		else:

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			slotIndex = player.GetSkillSlotIndex(skillIndex)

			skillCurrentPercentage = player.GetSkillCurrentEfficientPercentage(slotIndex)
			skillNextPercentage = player.GetSkillNextEfficientPercentage(slotIndex)

			self.AppendDefaultData(skillIndex, skillGrade)
			self.AppendSkillConditionData(skillIndex)
			self.AppendSkillDataNew(slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage)
			self.AppendSkillRequirement(skillIndex, skillLevel)

		self.ShowToolTip()

	def __SetSkillTitle(self, skillIndex, skillGrade):
		self.SetTitle(skill.GetSkillName(skillIndex, skillGrade))
		self.__AppendSkillGradeName(skillIndex, skillGrade)

	def __AppendSkillGradeName(self, skillIndex, skillGrade):
		if self.SKILL_GRADE_NAME.has_key(skillGrade):
			self.AppendSpace(5)
			self.AppendTextLine(self.SKILL_GRADE_NAME[skillGrade] % (skill.GetSkillName(skillIndex, 0)), self.CAN_LEVEL_UP_COLOR)

	def SetSkillOnlyName(self, slotIndex, skillIndex, skillGrade):
		if 0 == skillIndex:
			return

		slotIndex = player.GetSkillSlotIndex(skillIndex)

		self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
		self.ResizeToolTip()

		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)
		self.AppendDefaultData(skillIndex, skillGrade)
		self.AppendSkillConditionData(skillIndex)
		self.ShowToolTip()

	def AppendDefaultData(self, skillIndex, skillGrade = 0):
		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)

		## Level Limit
		levelLimit = skill.GetSkillLevelLimit(skillIndex)
		if levelLimit > 0:

			color = self.NORMAL_COLOR
			if player.GetStatus(player.LEVEL) < levelLimit:
				color = self.NEGATIVE_COLOR

			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_LEVEL % (levelLimit), color)

		## Description
		description = skill.GetSkillDescription(skillIndex)
		self.AppendDescription(description, 25)

	def AppendSupportSkillDefaultData(self, skillIndex, skillGrade, skillLevel, maxLevel):
		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)

		## Description
		description = skill.GetSkillDescription(skillIndex)
		self.AppendDescription(description, 25)

		if 1 == skillGrade:
			skillLevel += 19
		elif 2 == skillGrade:
			skillLevel += 29
		elif 3 == skillGrade:
			skillLevel = 40

		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_WITH_MAX % (skillLevel, maxLevel), self.NORMAL_COLOR)

	def AppendSkillConditionData(self, skillIndex):
		conditionDataCount = skill.GetSkillConditionDescriptionCount(skillIndex)
		if conditionDataCount > 0:
			self.AppendSpace(5)
			for i in xrange(conditionDataCount):
				self.AppendTextLine(skill.GetSkillConditionDescription(skillIndex, i), self.CONDITION_COLOR)

	def AppendGuildSkillData(self, skillIndex, skillLevel):
		skillMaxLevel = 7
		skillCurrentPercentage = float(skillLevel) / float(skillMaxLevel)
		skillNextPercentage = float(skillLevel+1) / float(skillMaxLevel)
		## Current Level
		if skillLevel > 0:
			if self.HasSkillLevelDescription(skillIndex, skillLevel):
				self.AppendSpace(5)
				if skillLevel == skillMaxLevel:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)

				#####

				for i in xrange(skill.GetSkillAffectDescriptionCount(skillIndex)):
					self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillCurrentPercentage), self.ENABLE_COLOR)

				## Cooltime
				coolTime = skill.GetSkillCoolTime(skillIndex, skillCurrentPercentage)
				if coolTime > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), self.ENABLE_COLOR)

				## SP
				needGSP = skill.GetSkillNeedSP(skillIndex, skillCurrentPercentage)
				if needGSP > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_NEED_GSP % (needGSP), self.ENABLE_COLOR)

		## Next Level
		if skillLevel < skillMaxLevel:
			if self.HasSkillLevelDescription(skillIndex, skillLevel+1):
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skillMaxLevel), self.DISABLE_COLOR)

				#####

				for i in xrange(skill.GetSkillAffectDescriptionCount(skillIndex)):
					self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillNextPercentage), self.DISABLE_COLOR)

				## Cooltime
				coolTime = skill.GetSkillCoolTime(skillIndex, skillNextPercentage)
				if coolTime > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), self.DISABLE_COLOR)

				## SP
				needGSP = skill.GetSkillNeedSP(skillIndex, skillNextPercentage)
				if needGSP > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_NEED_GSP % (needGSP), self.DISABLE_COLOR)

	def AppendSkillDataNew(self, slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage):

		self.skillMaxLevelStartDict = { 0 : 17, 1 : 7, 2 : 10, }
		self.skillMaxLevelEndDict = { 0 : 20, 1 : 10, 2 : 10, }

		skillLevelUpPoint = 1
		realSkillGrade = player.GetSkillGrade(slotIndex)
		skillMaxLevelStart = self.skillMaxLevelStartDict.get(realSkillGrade, 15)
		skillMaxLevelEnd = self.skillMaxLevelEndDict.get(realSkillGrade, 20)

		## Current Level
		if skillLevel > 0:
			if self.HasSkillLevelDescription(skillIndex, skillLevel):
				self.AppendSpace(5)
				if skillGrade == skill.SKILL_GRADE_COUNT:
					pass
				elif skillLevel == skillMaxLevelEnd:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
				self.AppendSkillLevelDescriptionNew(skillIndex, skillCurrentPercentage, self.ENABLE_COLOR)

		## Next Level
		if skillGrade != skill.SKILL_GRADE_COUNT:
			if skillLevel < skillMaxLevelEnd:
				if self.HasSkillLevelDescription(skillIndex, skillLevel+skillLevelUpPoint):
					self.AppendSpace(5)
					## HP����, ����ȸ�� ������ų�� ���
					if skillIndex == 141 or skillIndex == 142:
						self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_3 % (skillLevel+1), self.DISABLE_COLOR)
					else:
						self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skillMaxLevelEnd), self.DISABLE_COLOR)
					self.AppendSkillLevelDescriptionNew(skillIndex, skillNextPercentage, self.DISABLE_COLOR)

	def AppendSkillLevelDescriptionNew(self, skillIndex, skillPercentage, color):

		affectDataCount = skill.GetNewAffectDataCount(skillIndex)
		if affectDataCount > 0:
			for i in xrange(affectDataCount):
				type, minValue, maxValue = skill.GetNewAffectData(skillIndex, i, skillPercentage)

				if not self.AFFECT_NAME_DICT.has_key(type):
					continue

				minValue = int(minValue)
				maxValue = int(maxValue)
				affectText = self.AFFECT_NAME_DICT[type]

				if "HP" == type:
					if minValue < 0 and maxValue < 0:
						minValue *= -1
						maxValue *= -1

					else:
						affectText = localeInfo.TOOLTIP_SKILL_AFFECT_HEAL

				affectText += str(minValue)
				if minValue != maxValue:
					affectText += " - " + str(maxValue)
				affectText += self.AFFECT_APPEND_TEXT_DICT.get(type, "")

				#import debugInfo
				#if debugInfo.IsDebugMode():
				#	affectText = "!!" + affectText

				self.AppendTextLine(affectText, color)

		else:
			for i in xrange(skill.GetSkillAffectDescriptionCount(skillIndex)):
				self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillPercentage), color)


		## Duration
		duration = skill.GetDuration(skillIndex, skillPercentage)
		if duration > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_SKILL_DURATION % (duration), color)

		## Cooltime
		coolTime = skill.GetSkillCoolTime(skillIndex, skillPercentage)
		if coolTime > 0:
			basic_cast_speed = 100
			cd_s = player.GetStatus(player.CASTING_SPEED)
			cool_down = "%s" % (coolTime*basic_cast_speed/cd_s)
			self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + cool_down, color)

		## SP
		needSP = skill.GetSkillNeedSP(skillIndex, skillPercentage)
		if needSP != 0:
			continuationSP = skill.GetSkillContinuationSP(skillIndex, skillPercentage)

			if skill.IsUseHPSkill(skillIndex):
				self.AppendNeedHP(needSP, continuationSP, color)
			else:
				self.AppendNeedSP(needSP, continuationSP, color)

	def AppendSkillRequirement(self, skillIndex, skillLevel):

		skillMaxLevel = skill.GetSkillMaxLevel(skillIndex)

		if skillLevel >= skillMaxLevel:
			return

		isAppendHorizontalLine = False

		## Requirement
		if skill.IsSkillRequirement(skillIndex):

			if not isAppendHorizontalLine:
				isAppendHorizontalLine = True
				self.AppendHorizontalLine()

			requireSkillName, requireSkillLevel = skill.GetSkillRequirementData(skillIndex)

			color = self.CANNOT_LEVEL_UP_COLOR
			if skill.CheckRequirementSueccess(skillIndex):
				color = self.CAN_LEVEL_UP_COLOR
			self.AppendTextLine(localeInfo.TOOLTIP_REQUIREMENT_SKILL_LEVEL % (requireSkillName, requireSkillLevel), color)

		## Require Stat
		requireStatCount = skill.GetSkillRequireStatCount(skillIndex)
		if requireStatCount > 0:

			for i in xrange(requireStatCount):
				type, level = skill.GetSkillRequireStatData(skillIndex, i)
				if self.POINT_NAME_DICT.has_key(type):

					if not isAppendHorizontalLine:
						isAppendHorizontalLine = True
						self.AppendHorizontalLine()

					name = self.POINT_NAME_DICT[type]
					color = self.CANNOT_LEVEL_UP_COLOR
					if player.GetStatus(type) >= level:
						color = self.CAN_LEVEL_UP_COLOR
					self.AppendTextLine(localeInfo.TOOLTIP_REQUIREMENT_STAT_LEVEL % (name, level), color)

	def HasSkillLevelDescription(self, skillIndex, skillLevel):
		if skill.GetSkillAffectDescriptionCount(skillIndex) > 0:
			return True
		if skill.GetSkillCoolTime(skillIndex, skillLevel) > 0:
			return True
		if skill.GetSkillNeedSP(skillIndex, skillLevel) > 0:
			return True

		return False

	def AppendMasterAffectDescription(self, index, desc, color):
		self.AppendTextLine(desc, color)

	def AppendNextAffectDescription(self, index, desc):
		self.AppendTextLine(desc, self.DISABLE_COLOR)

	def AppendNeedHP(self, needSP, continuationSP, color):

		self.AppendTextLine(localeInfo.TOOLTIP_NEED_HP % (needSP), color)

		if continuationSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_HP_PER_SEC % (continuationSP), color)

	def AppendNeedSP(self, needSP, continuationSP, color):

		if -1 == needSP:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_ALL_SP, color)

		else:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_SP % (needSP), color)

		if continuationSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_SP_PER_SEC % (continuationSP), color)

	def AppendPartySkillData(self, skillGrade, skillLevel):
		def fix001(vl):
			return vl.replace("%,0f", "%.0f")

		if 1 == skillGrade:
			skillLevel += 19
		elif 2 == skillGrade:
			skillLevel += 29
		elif 3 == skillGrade:
			skillLevel =  40

		if skillLevel <= 0:
			return

		skillIndex = player.SKILL_INDEX_TONGSOL
		slotIndex = player.GetSkillSlotIndex(skillIndex)
		skillPower = player.GetSkillCurrentEfficientPercentage(slotIndex)
		if localeInfo.IsBRAZIL():
			k = skillPower
		else:
			k = player.GetSkillLevel(skillIndex) / 100.0
		self.AppendSpace(5)
		self.AutoAppendTextLine(localeInfo.TOOLTIP_PARTY_SKILL_LEVEL % skillLevel, self.NORMAL_COLOR)

		if skillLevel>=10:
			self.AutoAppendTextLine(fix001(localeInfo.PARTY_SKILL_ATTACKER) % chop( 10 + 60 * k ))

		if skillLevel>=20:
			self.AutoAppendTextLine(fix001(localeInfo.PARTY_SKILL_BERSERKER) 	% chop(1 + 5 * k))
			self.AutoAppendTextLine(fix001(localeInfo.PARTY_SKILL_TANKER) 	% chop(50 + 1450 * k))

		if skillLevel>=25:
			self.AutoAppendTextLine(fix001(localeInfo.PARTY_SKILL_BUFFER) % chop(5 + 45 * k ))

		if skillLevel>=35:
			self.AutoAppendTextLine(fix001(localeInfo.PARTY_SKILL_SKILL_MASTER) % chop(25 + 600 * k ))

		if skillLevel>=40:
			self.AutoAppendTextLine(fix001(localeInfo.PARTY_SKILL_DEFENDER) % chop( 5 + 30 * k ))

		self.AlignHorizonalCenter()

	def __AppendSummonDescription(self, skillLevel, color):
		if skillLevel > 1:
			self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (skillLevel * 10), color)
		elif 1 == skillLevel:
			self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (15), color)
		elif 0 == skillLevel:
			self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (10), color)
			
if __name__ == "__main__":
	import app
	import wndMgr
	import systemSetting
	import mouseModule
	import grp
	import ui

	#wndMgr.SetOutlineFlag(True)

	app.SetMouseHandler(mouseModule.mouseController)
	app.SetHairColorEnable(True)
	wndMgr.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetScreenSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	app.Create("METIN2 CLOSED BETA", systemSetting.GetWidth(), systemSetting.GetHeight(), 1)
	mouseModule.mouseController.Create()

	toolTip = ItemToolTip()
	toolTip.ClearToolTip()
	#toolTip.AppendTextLine("Test")
	desc = "Item descriptions:|increase of width of display to 35 digits per row AND installation of function that the displayed words are not broken up in two parts, but instead if one word is too long to be displayed in this row, this word will start in the next row."
	summ = ""

	toolTip.AddItemData_Offline(10, desc, summ, 0, 0)
	toolTip.Show()

	app.Loop()

if app.ENABLE_DECORUM:
	class HyperlinkArenaToolTip(ToolTip):
		def __init__(self):
			ToolTip.__init__(self, isPickable = True)

		def SetHyperlinkArenaStart(self, tokens):
			if not tokens or len(tokens) < 4:
				return
			
			arenaType = int(tokens[2])
			teamSize = int(tokens[3])
			maxXL = 0
			maxXR = 0
			
			minTokenCount = 4 + teamSize * 2
			
			if len(tokens) < minTokenCount:
				return
					
			names = ["Team A", "Team B"]
			for i in xrange(teamSize): 
				names.append(tokens[4 + i])
				names.append(tokens[4 + i + teamSize])
			
			
			for i in xrange(len(names)):
				txt = ui.TextLine()
				txt.SetText(names[i])
				if i % 2 == 0:
					maxXL = max(maxXL, txt.GetTextSize()[0])
				else:
					maxXR = max(maxXR, txt.GetTextSize()[0])
					
			self.ClearToolTip()
			
			self.SetTootlipName(arenaType)
			self.AppendSpace(5)
			self.BuildTooltip(names, maxXL, maxXR)

			self.ShowToolTip()
			ToolTip.OnUpdate(self)
			
		def SetHyperlinkArenaEnd(self, tokens):
			if not tokens or len(tokens) < 4:
				return
			
			arenaType = int(tokens[2])
			teamSize = int(tokens[3])
			maxXL = 0
			maxXR = 0
			
			minTokenCount = 4 + teamSize * 5
			
			if len(tokens) < minTokenCount:
				return
				
			teamA = ["Team A", uiScriptLocale.DECORUM_END_STATS]
			teamB = ["Team B", uiScriptLocale.DECORUM_END_STATS]
			
			rests = tokens[4:]
			rests.reverse()
			while rests:
				name = rests.pop()
				kill = rests.pop()
				death = rests.pop()
				dmgD = int(rests.pop(), 16) / 1000.0
				dmgT = int(rests.pop(), 16) / 1000.0
				
				if len(teamA) < (teamSize + 1) * 2:
					teamA.append(name)
					teamA.append("[%s / %s] (%.2fk / %.2fk)" % (kill, death, dmgD, dmgT))
				else:
					teamB.append(name)
					teamB.append("[%s / %s] (%.2fk / %.2fk)" % (kill, death, dmgD, dmgT))
					
			for i in xrange(len(teamA)):
				txt = ui.TextLine()
				txt.SetText(teamA[i])
				if i % 2 == 0:
					maxXL = max(maxXL, txt.GetTextSize()[0])
				else:
					maxXR = max(maxXR, txt.GetTextSize()[0])
					
			for i in xrange(len(teamB)):
				txt = ui.TextLine()
				txt.SetText(teamB[i])
				if i % 2 == 0:
					maxXL = max(maxXL, txt.GetTextSize()[0])
				else:
					maxXR = max(maxXR, txt.GetTextSize()[0])
					
			self.ClearToolTip()
					
			self.SetTootlipName(arenaType)
			self.AppendSpace(5)
			self.BuildTooltip(teamA, maxXL, maxXR)
			self.AppendSpace(5)
			self.BuildTooltip(teamB, maxXL, maxXR)

			self.ShowToolTip()
			ToolTip.OnUpdate(self)
					
			
		def SetTootlipName(self, type):
			arenaTypeName = (uiScriptLocale.DECORUM_BLOCK_ARENA1, uiScriptLocale.DECORUM_BLOCK_ARENA2, uiScriptLocale.DECORUM_BLOCK_ARENA3)
			nameString = uiScriptLocale.DECORUM_ARENA_NAME % arenaTypeName[type]
			
			self.AppendTextLine(nameString, self.SPECIAL_TITLE_COLOR)
			self.AppendSpace(5)
			
		def BuildTooltip(self, token, xl, xr):
			for i in xrange(0, len(token) - 1, 2):
				name1 = token[i]
				name2 = token[i + 1]
					
				txt = ui.TextLine()
				txt.SetText(name1)
				while txt.GetTextSize()[0] < xl + 30:
					name1 += " "
					txt.SetText(name1)
				txt.SetText(name2)
				while txt.GetTextSize()[0] < xr:
					name2 += " "
					txt.SetText(name2)
			
				if i == 0:
					self.AppendTextLine(name1 + name2, self.TITLE_COLOR)
				elif i % 1 == 1:
					self.AppendTextLine(name1 + name2, self.NORMAL_COLOR)	
				else:
					self.AppendTextLine(name1 + name2, self.CONDITION_COLOR)
		
		def OnUpdate(self):
			pass

		def OnMouseLeftButtonDown(self):
			self.Hide()
