import app
import constInfo

MAP_TRENT02 = "MAP_TRENT02" # 임시
MAP_WL = "MAP_WL" # 임시
MAP_NUSLUCK = "MAP_NUSLUCK" # 임시
MAP_TREE2 = "Bosco Rosso"

BLEND_POTION_NO_TIME = "Durata casuale"
BLEND_POTION_NO_INFO = "BLEND_POTION_NO_INFO"

APP_TITLE = "Emeria ~ Official"

GUILD_HEADQUARTER = "Main Building"
GUILD_FACILITY = "Facility"
GUILD_OBJECT = "Object"
GUILD_MEMBER_COUNT_INFINITY = "INFINITY"

LOGIN_FAILURE_WEB_BLOCK = "BLOCK_LOGIN(WEB)"
LOGIN_FAILURE_BLOCK_LOGIN = "BLOCK_LOGIN"
CHANNEL_NOTIFY_FULL = "CHANNEL_NOTIFY_FULL"

GUILD_BUILDING_LIST_TXT = app.GetLocalePath() + "/GuildBuildingList.txt"

GUILD_MARK_MIN_LEVEL = "1"
GUILD_MARK_NOT_ENOUGH_LEVEL = "길드레벨 3이상 부터 가능합니다."

ERROR_MARK_UPLOAD_NEED_RECONNECT = "UploadMark: Reconnect to game"
ERROR_MARK_CHECK_NEED_RECONNECT = "CheckMark: Reconnect to game"

VIRTUAL_KEY_ALPHABET_LOWERS  = r"[1234567890]/qwertyuiop\=asdfghjkl;`'zxcvbnm.,"
VIRTUAL_KEY_ALPHABET_UPPERS  = r'{1234567890}?QWERTYUIOP|+ASDFGHJKL:~"ZXCVBNM<>'
VIRTUAL_KEY_SYMBOLS    = '!@#$%^&*()_+|{}:"<>?~'
VIRTUAL_KEY_NUMBERS    = "1234567890-=\[];',./`"
VIRTUAL_KEY_SYMBOLS_BR    = '!@#$%^&*()_+|{}:"<>?~蓀呻郵悠壬蛭衝銜'

__IS_ENGLISH	= "ENGLISH" == app.GetLocaleServiceName()
__IS_HONGKONG	= "HONGKONG" == app.GetLocaleServiceName()
__IS_NEWCIBN	= "locale/newcibn" == app.GetLocalePath()
__IS_EUROPE		= "EUROPE" == app.GetLocaleServiceName()
__IS_CANADA		= "locale/ca" == app.GetLocalePath()
__IS_BRAZIL		= "locale/br" == app.GetLocalePath()
__IS_SINGAPORE	= "locale/sg" == app.GetLocalePath()
__IS_VIETNAM	= "locale/vn" == app.GetLocalePath()
__IS_ARABIC		= "locale/ae" == app.GetLocalePath()
__IS_CIBN10		= "locale/cibn10" == app.GetLocalePath()
__IS_WE_KOREA	= "locale/we_korea" == app.GetLocalePath()
__IS_TAIWAN		= "locale/taiwan" == app.GetLocalePath()
__IS_JAPAN		= "locale/japan" == app.GetLocalePath()
LOGIN_FAILURE_WRONG_SOCIALID = "ASDF"
LOGIN_FAILURE_SHUTDOWN_TIME = "ASDF"

if __IS_CANADA:
	__IS_EUROPE = True

def IsYMIR():
	return "locale/ymir" == app.GetLocalePath()

def IsJAPAN():
	return "locale/japan" == app.GetLocalePath()

def IsENGLISH():
	global __IS_ENGLISH
	return __IS_ENGLISH

def IsHONGKONG():
	global __IS_HONGKONG
	return __IS_HONGKONG

def IsTAIWAN():
	return "locale/taiwan" == app.GetLocalePath()

def IsNEWCIBN():
	return "locale/newcibn" == app.GetLocalePath()

def IsCIBN10():
	global __IS_CIBN10
	return __IS_CIBN10

def IsEUROPE():
	global __IS_EUROPE
	return __IS_EUROPE

def IsCANADA():
	global __IS_CANADA
	return __IS_CANADA

def IsBRAZIL():
	global __IS_BRAZIL
	return __IS_BRAZIL

def IsVIETNAM():
	global __IS_VIETNAM
	return __IS_VIETNAM

def IsSINGAPORE():
	global __IS_SINGAPORE
	return __IS_SINGAPORE

def IsARABIC():
	global __IS_ARABIC
	return __IS_ARABIC

def IsWE_KOREA():
	return "locale/we_korea" == app.GetLocalePath()

# SUPPORT_NEW_KOREA_SERVER
def LoadLocaleData():
	app.LoadLocaleData(app.GetLocalePath())

def IsCHEONMA():
	return IsYMIR()		# 이제 YMIR 로케일은 무조건 천마서버임. 천마서버가 문을 닫기 전까지 변할 일 없음.

# END_OF_SUPPORT_NEW_KOREA_SERVER

def mapping(**kwargs): return kwargs

def SNA(text):
	def f(x):
		return text
	return f

def SA(text):
	def f(x):
		return text % x
	return f
	
def FormatTime(time):
	m, s = divmod(time, 60)
	h, m = divmod(m, 60)
	return "%02d:%02d:%02d" % (h, m, s)	

## PET_SKILL_INFO FNCS BEGIN
def SAN(text):
	def f(x):
		return text % x
	return f

def SAA(text):
	def f(x):
		return text % x
	return f
## PET_SKILL_INFO FNCS END

def LoadLocaleFile(srcFileName, localeDict):

	funcDict = {"SA":SA, "SNA":SNA, "SAA":SAA, "SAN":SAN}

	lineIndex = 1

	try:
		lines = open(srcFileName, "r").readlines()
	except IOError:
		import dbg
		dbg.LogBox("LoadLocaleError(%(srcFileName)s)" % locals())
		app.Abort()

	for line in lines:
		try:
			tokens = line[:-1].split("\t")
			if len(tokens) == 2:
				localeDict[tokens[0]] = tokens[1]
			elif len(tokens) >= 3:
				type = tokens[2].strip()
				if type:
					localeDict[tokens[0]] = funcDict[type](tokens[1])
				else:
					localeDict[tokens[0]] = tokens[1]
			else:
				raise RuntimeError, "Unknown TokenSize"

			lineIndex += 1
		except:
			import dbg
			dbg.LogBox("%s: line(%d): %s" % (srcFileName, lineIndex, line), "Error")
			raise



all = ["locale","error"]

FN_GM_MARK = "%s/effect/gm.mse"	% app.GetLocalePath()
LOCALE_FILE_NAME = "%s/locale_game.txt" % app.GetLocalePath()

constInfo.IN_GAME_SHOP_ENABLE = 1

LoadLocaleFile(LOCALE_FILE_NAME, locals())

########################################################################################################
## NOTE : 아이템을 버릴때 "무엇을/를 버리시겠습니까?" 문자열의 조사 선택을 위한 코드
dictSingleWord = {
	"m":1, "n":1, "r":1, "M":1, "N":1, "R":1, "l":1, "L":1, "1":1, "3":1, "6":1, "7":1, "8":1, "0":1,
}


locale = mapping(
)


def CutMoneyString(sourceText, startIndex, endIndex, insertingText, backText):

	sourceLength = len(sourceText)

	if sourceLength < startIndex:
		return backText

	text = sourceText[max(0, sourceLength-endIndex):sourceLength-startIndex]

	if not text:
		return backText

	if int(text) <= 0:
		return backText

	text = str(int(text))

	if backText:
		backText = " " + backText

	return text + insertingText + backText

def GetMapNameByID(id):
	# Shinsoo
	if id == 1:
		return MAP_A1
	elif id == 3:
		return MAP_A3
	elif id == 4:
		return MAP_AG
	elif id == 5:
		return MAP_MONKEY_EZ
	elif id == 6:
		return MAP_AG2
	# Chunjo
	elif id == 21:
		return MAP_B1
	elif id == 23:
		return MAP_B3
	elif id == 24:
		return MAP_BG
	elif id == 25:
		return MAP_MONKEY_EZ
	elif id == 26:
		return MAP_BG2
	# Chunjo
	elif id == 41:
		return MAP_C1
	elif id == 43:
		return MAP_C3
	elif id == 44:
		return MAP_CG
	elif id == 45:
		return MAP_MONKEY_EZ
	elif id == 46:
		return MAP_CG2
	#Neutrals
	elif id == 61:
		return MAP_SNOW
	elif id == 62:
		return MAP_FLAME
	elif id == 63:
		return MAP_DESERT
	elif id == 64:
		return MAP_A2
	elif id == 65:
		return MAP_TEMPLE
	elif id == 66:
		return MAP_SKELTOWER
	elif id == 67:
		return MAP_TREE
	elif id == 68:
		return MAP_TRENT02
	elif id == 69:
		return MAP_WL
	elif id == 70:
		return MAP_NUSLUCK
	
	elif id == 71:
		return MAP_SPIDER2
	elif id == 72:
		return MAP_SKIPIA
	elif id == 73:
		return MAP_SKIPIA2
	elif id == 81:
		return MAP_WEDDING
		
	elif id == 104:
		return MAP_SPIDER
	elif id == 107:
		return MAP_MONKEY_EZ
	elif id == 108:
		return MAP_MONKEY_MD
	elif id == 109:
		return MAP_MONKEY_HD
		
	elif id == 112:
		return MAP_DUEL
	elif id == 208:
		return MAP_SKIPIABOSS
	elif id == 216:
		return MAP_DC
	elif id == 217:
		return MAP_SPIDER3
	elif id == 351:
		return MAP_RAZADOR
	elif id == 355:
		return MAP_GOLD

	return "Mape name not found."

def SecondToDHM(time):
	if time < 60:
		if IsARABIC():
			return "%.2f %s" % (time, SECOND)
		else:
			return "0" + MINUTE

	second = int(time % 60)
	minute = int((time / 60) % 60)
	hour = int((time / 60) / 60) % 24
	day = int(int((time / 60) / 60) / 24)

	text = ""

	if day > 0:
		text += str(day) + DAY
		text += " "

	if hour > 0:
		text += str(hour) + HOUR
		text += " "

	if minute > 0:
		text += str(minute) + MINUTE

	return text

def SecondToHM(time):

	if time < 60:
		if IsARABIC():
			return "%.2f %s" % (time, SECOND)
		else:
			return "0" + MINUTE

	second = int(time % 60)
	minute = int((time / 60) % 60)
	hour = int((time / 60) / 60)

	text = ""

	if hour > 0:
		text += str(hour) + HOUR
		if hour > 0:
			text += " "

	if minute > 0:
		text += str(minute) + MINUTE

	return text


def GetAlignmentTitleName(alignment):
	if alignment >= 12000:
		return TITLE_NAME_LIST[0]
	elif alignment >= 8000:
		return TITLE_NAME_LIST[1]
	elif alignment >= 4000:
		return TITLE_NAME_LIST[2]
	elif alignment >= 1000:
		return TITLE_NAME_LIST[3]
	elif alignment >= 0:
		return TITLE_NAME_LIST[4]
	elif alignment > -4000:
		return TITLE_NAME_LIST[5]
	elif alignment > -8000:
		return TITLE_NAME_LIST[6]
	elif alignment > -12000:
		return TITLE_NAME_LIST[7]

	return TITLE_NAME_LIST[8]

OPTION_PVPMODE_MESSAGE_DICT = {
	0 : PVP_MODE_NORMAL,
	1 : PVP_MODE_REVENGE,
	2 : PVP_MODE_KILL,
	3 : PVP_MODE_PROTECT,
	4 : PVP_MODE_GUILD,
}

error = mapping(
	CREATE_WINDOW = GAME_INIT_ERROR_MAIN_WINDOW,
	CREATE_CURSOR = GAME_INIT_ERROR_CURSOR,
	CREATE_NETWORK = GAME_INIT_ERROR_NETWORK,
	CREATE_ITEM_PROTO = GAME_INIT_ERROR_ITEM_PROTO,
	CREATE_MOB_PROTO = GAME_INIT_ERROR_MOB_PROTO,
	CREATE_NO_DIRECTX = GAME_INIT_ERROR_DIRECTX,
	CREATE_DEVICE = GAME_INIT_ERROR_GRAPHICS_NOT_EXIST,
	CREATE_NO_APPROPRIATE_DEVICE = GAME_INIT_ERROR_GRAPHICS_BAD_PERFORMANCE,
	CREATE_FORMAT = GAME_INIT_ERROR_GRAPHICS_NOT_SUPPORT_32BIT,
	NO_ERROR = ""
)


GUILDWAR_NORMAL_DESCLIST = [GUILD_WAR_USE_NORMAL_MAP, GUILD_WAR_LIMIT_30MIN, GUILD_WAR_WIN_CHECK_SCORE]
GUILDWAR_WARP_DESCLIST = [GUILD_WAR_USE_BATTLE_MAP, GUILD_WAR_WIN_WIPE_OUT_GUILD, GUILD_WAR_REWARD_POTION]
GUILDWAR_CTF_DESCLIST = [GUILD_WAR_USE_BATTLE_MAP, GUILD_WAR_WIN_TAKE_AWAY_FLAG1, GUILD_WAR_WIN_TAKE_AWAY_FLAG2, GUILD_WAR_REWARD_POTION]

MINIMAP_ZONE_NAME_DICT = {
	"metin2_map_a1"  : MAP_A1,
	"map_a2"         : MAP_A2,
	"metin2_map_a3"  : MAP_A3,
	"metin2_map_b1"  : MAP_B1,
	"map_b2"         : MAP_B2,
	"metin2_map_b3"  : MAP_B3,
	"metin2_map_c1"  : MAP_C1,
	"map_c2"         : MAP_C2,
	"metin2_map_c3"  : MAP_C3,
	"map_n_snowm_01" : MAP_SNOW,
	"metin2_map_n_flame_01" : MAP_FLAME,
	"metin2_map_n_desert_01" : MAP_DESERT,
	"metin2_map_milgyo" : MAP_TEMPLE,
	"metin2_map_spiderdungeon" : MAP_SPIDER,
	"metin2_map_deviltower1" : MAP_SKELTOWER,
	"metin2_map_guild_01" : MAP_AG,
	"metin2_map_guild_02" : MAP_BG,
	"metin2_map_guild_03" : MAP_CG,
	"metin2_map_trent" : MAP_TREE,
	"metin2_map_trent02" : MAP_TREE2,
	"season1/metin2_map_WL_01" : MAP_WL,
	"season1/metin2_map_nusluck01" : MAP_NUSLUCK,
    "Metin2_map_CapeDragonHead" : MAP_CAPE,
    "metin2_map_Mt_Thunder" : MAP_THUNDER,
    "metin2_map_dawnmistwood" : MAP_DAWN,
    "metin2_map_BayBlackSand" : MAP_BAY,
	"mental_lobby_1x1" : MAP_LOBBY,
	"plechito_pyramide_dungeon" : MAP_PIRAMIDE,
	"plechito_desert_map_01" : MAP_PLEC_DESERT,
	"plechito_shark_dungeon"  : MAP_DAWNMIST_DUNGEON_01,
}



JOBINFO_TITLE = [
	[JOB_WARRIOR0, JOB_WARRIOR1, JOB_WARRIOR2,],
	[JOB_ASSASSIN0, JOB_ASSASSIN1, JOB_ASSASSIN2,],
	[JOB_SURA0, JOB_SURA1, JOB_SURA2,],
	[JOB_SHAMAN0, JOB_SHAMAN1, JOB_SHAMAN2,],
]
if app.ENABLE_WOLFMAN_CHARACTER:
	JOBINFO_TITLE += [[JOB_WOLFMAN0,JOB_WOLFMAN1,JOB_WOLFMAN2,],]

JOBINFO_DATA_LIST = [
	[
		["타고난 용맹과 굽히지 않는 무사의",
		"기개를 사람들은 일컬어 [용자]라고",
		"부른다. 어떠한 위기에서도 그들은 ",
		"뒤로 물러서지 않으며, 다치고 움직",
		"이기 힘든 동료를 위해 단신으로",
		"적들과 마주 싸우기도 한다. 이들은",
		"잘 단련된 근육과 힘, 강력한 공격력",
		"으로 전장 최선두에서 공격진으로",
		"활약한다.                      ",],
		["가장 일반적인 공격형 무사로, ",
		"적접전에 따른 직접 공격으로 전장",
		"에서 활약한다. 군직 특성상 근력을",
		"메인으로 스텟 포인트를 투자하되, ",
		"적접전에 따른 생명력 / 방어력",
		"확보를 위해 체력을 올린다. 또한",
		"공격의 정확성을 높이기 위해 민첩",
		"에도 포인트를 투자할 필요가 있다.",],
		["상당 수준의 정신력을 이용하는",
		"중/근거리 접전형 무사로, 각 기술",
		"하나하나의 높은 공격력으로 전장에서",
		"활약한다. 군직 특성상 근력을 메인",
		"으로 스탯 포인트를 투자하되, ",
		"중/근거리 공격의 정확성과 명중률을",
		"위해 민첩을 올린다. 또한 접전 시 ",
		"적 공격에 따른 생명력 / 방어력",
		"확보를 위해 체력에도 포인트를",
		"투자할 필요가 있다.        ",],
	],
	[
		["자객은 어떠한 상황에서도 자신의",
		"몸을 숨기고 은밀한 어둠의 임무를",
		"수행하면서 전장의 후위를 지원하는",
		"자들이다. 이들은 아주 빠르고 신속",
		"하며, 비할 데 없이 과감하고 절제된",
		"행동으로 적의 급소에 치명타를 날리",
		"되, 전장에선 적진을 향해 무수한",
		"화살을 내뿜으며 자신의 용맹을",
		"선보인다.                   "],
		["두손 단검을 주무기로 다루며, 신속",
		"하게 치고 빠지는 자객 특유의 움직임",
		"으로 전장에서 활약한다. 군직 특성상",
		"민첩을 메인으로 스텟 포인트를 투자",
		"하되, 근력을 올려 공격력을 높인다.",
		"또한 근접전에 따른 생명력/방어력 ",
		"상승을 위해 체력에도 포인트를",
		"투자할 필요가 있다.          ",],
		["활을 주무기로 다루며, 긴 시야와",
		"사정거리에 따른 원거리 공격으로",
		"전장에서 활약한다. 군직 특성상",
		"공격 성공률의 증가를 위해 민첩을",
		"메인으로 올려야 하며, 원거리",
		"공격의 데미지 증가를 위해 근력을",
		"올릴 필요가 있다. 또한 적들에게",
		"포위되었을 시, 적 공격에 버티기",
		"위한 생명력/방어력 상승을 위해",
		"체력에도 포인트를 투자할 필요가",
		"있다.                        ", ],
	],
	[
		["수라는 [독은 독으로]의 속성으로",
		"창설된 특수 속성의 군직이다. ",
		"그들은 전장에서 적들의 사기를 저하",
		"시키고, 악마의 힘을 실은 마탄으로",
		"적의 영혼과 육신을 짓뭉갠다. 때로",
		"이들은 자신의 검과 갑옷에 어둠의",
		"힘을 실어, 전장에서 무사 못지 않은",
		"공격력을 발휘하기도 하는데, 적들을",
		"죽여대는그 모습이 워낙에 끔찍해",
		"사람들은 수라를 일컬어 [마신]이라",
		"부르기를 주저 앉는다."],
		["환무군의 수라는 악마의 씨에서",
		"얻어지는 마력을 무기나 방어구에",
		"실어 무사 못지 않은 전투력으로",
		"전장에서 활약한다. 군직 특성상",
		"지능이 높아질수록 착용 장비에",
		"실리는 마력의 위력이 증대되므로,",
		"지능과 근력을 메인으로 스탯",
		"포인트를 투자하되, 접전에 따른",
		"생명력/방어력 확보를 위해 체력을",
		"올린다. 또한 공격의 정확성과",
		"회피를 위해서 민첩에도 포인트를",
		"투자할 필요가 있다.           ",],
		["흑마군의 수라들은 각종 어둠의",
		"주문과 악마의 마법으로 전장에서",
		"활약한다. 군직 특성상 마법 공격이",
		"주이므로 지능을 메인으로 스텟",
		"포인트를 투자하되, 원거리 마법",
		"공격의 정확성을 위해 민첩을 올린다.",
		"또한 포위 되었을시, 적 공격에 따른",
		"생명력 / 방어력 확보를 위해 체력에도",
		"포인트를 투자할 필요가 있다.    ",],
	],
	[
		["무당은 용신과 자연, 두 고대의",
		"힘을 다룰 수 있는 유일한 직종이다.",
		"그들은 후방에서 아군을 보조하고",
		"다친 동료의 부상을 회복 시키며",
		"떨어진 사기를 상승시킨다. 그들은",
		"아군의 수면과 휴식을 방해하는 자를 ",
		"절대 용서하지 않으며, 그런 자들",
		"에게는 한 점 주저 없이 주문을",
		"터트려 그 비겁함을 엄히 징계한다.",],
		["천룡군의 무당들은 각종 부적술과",
		"보조주문에 능하며, 적의 직 / 간접",
		"공격으로부터 아군을 지킨다. 군직",
		"특성상 마법 능력이 주이므로 지능을",
		"메인으로 스텟 포인트를 투자하되,",
		"포위되었을 시, 적 공격에 따른",
		"생명력 / 방어력 확보를 위해 체력을",
		"올린다. 또한 원거리 마법 공격의",
		"정확성을 위에 민첩에도 포인트를",
		"투자할 필요가 있다.           ",],
		["광뢰군의 무당들은 자연의 힘을",
		"빌려 아군을 회복하고, 뇌신의 ",
		"힘으로 밀집한 적들에게 큰 충격을",
		"입힐 수 있는 이들이다. 군직의",
		"특성상 마법 능력이 주이므로 지능을",
		"메인으로 스텟 포인트를 투자하되,",
		"포위되었을시, 적 공격에 따른",
		"생명력 / 방어력 확보를 위해 체력을",
		"올린다. 또한 원거리 마법 공격의",
		"정확성을 위에 민첩에도 포인트를",
		"투자할 필요가 있다.             "],
	],
]

if app.ENABLE_DUNGEON_INFO_SYSTEM:
	def GetMiniMapZoneNameByIdx(idx):
		if idx in MINIMAP_ZONE_NAME_DICT_BY_IDX and idx != 0:
			return MINIMAP_ZONE_NAME_DICT_BY_IDX[idx]
		return MAP_NONE

if app.ENABLE_DUNGEON_INFO_SYSTEM:
	MINIMAP_ZONE_NAME_DICT_BY_IDX = {
		0 : "",
		1 : MAP_A1,
		3 : MAP_A3,
		4 : MAP_GUILD_01,
		5 : MAP_MONKEY_DUNGEON_11,
		6 : GUILD_VILLAGE_01,
		21 : MAP_B1,
		23 : MAP_B3,
		24 : MAP_GUILD_02,
		25 : MAP_MONKEY_DUNGEON_12,
		26 : GUILD_VILLAGE_02,
		41 : MAP_C1,
		43 : MAP_C3,
		44 : MAP_GUILD_03,
		45 : MAP_MONKEY_DUNGEON_13,
		46 : GUILD_VILLAGE_03,
		61 : MAP_N_SNOWM_01,
		62 : MAP_N_FLAME_01,
		63 : MAP_N_DESERT_01,
		64 : MAP_N_THREEWAY,
		65 : MAP_MILGYO,
		66 : MAP_DEVILTOWER1,
		67 : MAP_TRENT,
		68 : MAP_TRENT02,
		69 : MAP_WL_01,
		70 : MAP_NUSLUCK01,
		71 : MAP_SPIDERDUNGEON_02,
		72 : MAP_SKIPIA_DUNGEON_01,
		73 : MAP_SKIPIA_DUNGEON_02,
		74 : MAP_N_SNOWM_02,
		75 : MAP_N_FLAME_02,
		76 : MAP_N_DESERT_02,
		77 : MAP_A2_1,
		78 : MAP_MILGYO_A,
		79 : MAP_TRENT_A,
		80 : MAP_TRENT02_A,
		81 : MAP_WEDDING_01,
		91 : MAP_E,
		92 : MAP_E,
		93 : MAP_E,
		103 : MAP_T1,
		104 : MAP_SPIDERDUNGEON,
		105 : MAP_T2,
		107 : MAP_MONKEY_DUNGEON,
		108 : MAP_MONKEY_DUNGEON2,
		109 : MAP_MONKEY_DUNGEON3,
		110 : MAP_T3,
		111 : MAP_T4,
		112 : MAP_DUEL,
		113 : MAP_OXEVENT,
		114 : MAP_SUNGZI,
		118 : MAP_SUNGZI_FLAME_HILL_01,
		119 : MAP_SUNGZI_FLAME_HILL_02,
		120 : MAP_SUNGZI_FLAME_HILL_03,
		121 : MAP_SUNGZI_SNOW,
		122 : MAP_SUNGZI_SNOW_PASS01,
		123 : MAP_SUNGZI_SNOW_PASS02,
		124 : MAP_SUNGZI_SNOW_PASS03,
		125 : MAP_SUNGZI_DESERT_01,
		126 : MAP_SUNGZI_DESERT_HILL_01,
		127 : MAP_SUNGZI_DESERT_HILL_02,
		128 : MAP_SUNGZI_DESERT_HILL_03,
		130 : GUILD_WAR1,
		131 : GUILD_WAR2,
		132 : GUILD_WAR3,
		133 : GUILD_WAR4,
		180 : METIN_TEST,
		181 : MAP_EMPIREWAR01,
		182 : MAP_EMPIREWAR02,
		183 : MAP_EMPIREWAR03,
		184 : MAP_SKIPIA_DUNGEON_011,
		185 : MAP_SKIPIA_DUNGEON_021,
		186 : MAP_SKIPIA_DUNGEON_012,
		187 : MAP_SKIPIA_DUNGEON_022,
		188 : MAP_SKIPIA_DUNGEON_013,
		189 : MAP_SKIPIA_DUNGEON_023,
		193 : MAP_SPIDERDUNGEON_02_1,
		194 : MAP_HOLYPLACE_FLAME,
		195 : MAP_PATHWAY_FLAME_01,
		196 : MAP_PATHWAY_FLAME_02,
		197 : MAP_PATHWAY_FLAME_03,
		198 : MAP_HOLYPLACE_ICE,
		199 : MAP_PATHWAY_ICE_01,
		200 : MAP_PATHWAY_ICE_02,
		201 : MAP_PATHWAY_ICE_03,
		202 : MAP_HOLYPLACE_DESERT,
		203 : MAP_PATHWAY_DESERT_01,
		204 : MAP_PATHWAY_DESERT_02,
		205 : MAP_PATHWAY_DESERT_03,
		208 : MAP_SKIPIA_DUNGEON_BOSS,
		209 : MAP_SKIPIA_DUNGEON_BOSS_1,
		210 : MAP_SKIPIA_DUNGEON_BOSS_2,
		211 : MAP_SKIPIA_DUNGEON_BOSS_3,
		212 : MAP_M_MELEY,
		216 : MAP_DEVILCATACOMB,
		217 : MAP_SPIDERDUNGEON_03,
		301 : MAP_CAPEDRAGONHEAD,
		302 : MAP_DAWNMISTWOOD,
		303 : MAP_BAYBLACKSAND,
		304 : MAP_MT_THUNDER,
		351 : MAP_N_FLAME_DUNGEON_01,
		352 : MAP_N_SNOW_DUNGEON_01,
		355 : MAP_GOLD,
		358 : MAP_DEFENSE_WAVE,
		359 : MAP_DEFENSE_WAVE_PORT,
		360 : MAP_MISTS_OF_ISLAND,
		361 : MAP_MINIBOSS_01,
		362 : MAP_MINIBOSS_02,
		363 : MAP_BOSS_LABYRINTH,
		364 : MAP_BOSS_CRACK_SKIPIA,
		365 : MAP_BOSS_CRACK_FLAME,
		366 : MAP_BOSS_CRACK_SNOW,
		367 : MAP_BOSS_CRACK_DAWNMIST,
		368 : MAP_BOSS_AWAKEN_SKIPIA,
		369 : MAP_BOSS_AWAKEN_FLAME,
		370 : MAP_BOSS_AWAKEN_SNOW,
		371 : MAP_BOSS_AWAKEN_DAWNMIST,
		372 : MAP_GUILD_PVE,
		373 : MAP_EASTPLAIN_01,
		374 : MAP_EMPIRECASTLE,
		375 : MAP_BATTLE_ROYALE,
		376 : MAP_EASTPLAIN_02,
		377 : MAP_EASTPLAIN_03,
		378 : MAP_ELEMENTAL_DUNGEON,
		379 : MAP_ELEMENTAL_DUNGEON,
		380 : MAP_ELEMENTAL_DUNGEON,
		381 : MAP_ELEMENTAL_DUNGEON,
		382 : MAP_MAZE_DUNGEON_01,
		383 : MAP_MAZE_DUNGEON_02,
		384 : MAP_MAZE_DUNGEON_03,
		385 : MAP_SNAKE_VALLEY,
		386 : MAP_SUNGMAHEE_TOWER_WAIT,
		387 : MAP_SUNGMAHEE_TOWER_DUNGEON,
		390 : MAP_SNAKE_TEMPLE_1,
		391 : MAP_SNAKE_TEMPLE_2,
		392 : MAP_PRIVATE_SHOP_MAP,
		396 : MAP_FARMING_DUNGEON,
		358 : MAP_PIRAMIDE,
	}
	#if background.IsMapInfoByMapName("metin2_map_dawnmist_dungeon_01"):
	MINIMAP_ZONE_NAME_DICT_BY_IDX[359] = MAP_DAWNMIST_DUNGEON_01
	#if background.IsMapInfoByMapName("metin2_map_Mt_Th_dungeon_01"):
	MINIMAP_ZONE_NAME_DICT_BY_IDX[354] = MAP_MT_TH_DUNGEON_01
	#if background.IsMapInfoByMapName("metin2_map_n_flame_dragon"):
	MINIMAP_ZONE_NAME_DICT_BY_IDX[356] = MAP_LOBBY
	#if background.IsMapInfoByMapName("metin2_map_battlefied"):
	MINIMAP_ZONE_NAME_DICT_BY_IDX[212] = MAP_M_MELEY
	#if background.IsMapInfoByMapName("metin2_map_battlefied"):
	MINIMAP_ZONE_NAME_DICT_BY_IDX[357] = MAP_BATTLE_FIELD
	#if background.IsMapInfoByMapName("metin2_12zi_stage"):
	MINIMAP_ZONE_NAME_DICT_BY_IDX[355] = MAP_GOLD
	#if background.IsMapInfoByMapName("metin2_12zi_stage"):
	MINIMAP_ZONE_NAME_DICT_BY_IDX[358] = MAP_PIRAMIDE
	#if background.IsMapInfoByMapName("metin2_12zi_stage"):
	MINIMAP_ZONE_NAME_DICT_BY_IDX[109] = MAP_MONKEY_DUNGEON3

WHISPER_ERROR = {
	1 : CANNOT_WHISPER_NOT_LOGON,
	2 : CANNOT_WHISPER_DEST_REFUSE,
	3 : CANNOT_WHISPER_SELF_REFUSE,
}

NOTIFY_MESSAGE = {
	"CANNOT_EQUIP_SHOP" : CANNOT_EQUIP_IN_SHOP,
	"CANNOT_EQUIP_EXCHANGE" : CANNOT_EQUIP_IN_EXCHANGE,
}


ATTACK_ERROR_TAIL_DICT = {
	"IN_SAFE" : CANNOT_ATTACK_SELF_IN_SAFE,
	"DEST_IN_SAFE" : CANNOT_ATTACK_DEST_IN_SAFE,
}

SHOT_ERROR_TAIL_DICT = {
	"EMPTY_ARROW" : CANNOT_SHOOT_EMPTY_ARROW,
	"IN_SAFE" : CANNOT_SHOOT_SELF_IN_SAFE,
	"DEST_IN_SAFE" : CANNOT_SHOOT_DEST_IN_SAFE,
}

USE_SKILL_ERROR_TAIL_DICT = {
	"IN_SAFE" : CANNOT_SKILL_SELF_IN_SAFE,
	"NEED_TARGET" : CANNOT_SKILL_NEED_TARGET,
	"NEED_EMPTY_BOTTLE" : CANNOT_SKILL_NEED_EMPTY_BOTTLE,
	"NEED_POISON_BOTTLE" : CANNOT_SKILL_NEED_POISON_BOTTLE,
	"REMOVE_FISHING_ROD" : CANNOT_SKILL_REMOVE_FISHING_ROD,
	"NOT_YET_LEARN" : CANNOT_SKILL_NOT_YET_LEARN,
	"NOT_MATCHABLE_WEAPON" : CANNOT_SKILL_NOT_MATCHABLE_WEAPON,
	"WAIT_COOLTIME" : CANNOT_SKILL_WAIT_COOLTIME,
	"NOT_ENOUGH_HP" : CANNOT_SKILL_NOT_ENOUGH_HP,
	"NOT_ENOUGH_SP" : CANNOT_SKILL_NOT_ENOUGH_SP,
	"CANNOT_USE_SELF" : CANNOT_SKILL_USE_SELF,
	"ONLY_FOR_ALLIANCE" : CANNOT_SKILL_ONLY_FOR_ALLIANCE,
	"CANNOT_ATTACK_ENEMY_IN_SAFE_AREA" : CANNOT_SKILL_DEST_IN_SAFE,
	"CANNOT_APPROACH" : CANNOT_SKILL_APPROACH,
	"CANNOT_ATTACK" : CANNOT_SKILL_ATTACK,
	"ONLY_FOR_CORPSE" : CANNOT_SKILL_ONLY_FOR_CORPSE,
	"EQUIP_FISHING_ROD" : CANNOT_SKILL_EQUIP_FISHING_ROD,
	"NOT_HORSE_SKILL" : CANNOT_SKILL_NOT_HORSE_SKILL,
	"HAVE_TO_RIDE" : CANNOT_SKILL_HAVE_TO_RIDE,
}

LEVEL_LIST=["", HORSE_LEVEL1, HORSE_LEVEL2, HORSE_LEVEL3]

HEALTH_LIST=[
	HORSE_HEALTH0,
	HORSE_HEALTH1,
	HORSE_HEALTH2,
	HORSE_HEALTH3,
]


USE_SKILL_ERROR_CHAT_DICT = {
	"NEED_EMPTY_BOTTLE" : SKILL_NEED_EMPTY_BOTTLE,
	"NEED_POISON_BOTTLE" : SKILL_NEED_POISON_BOTTLE,
	"ONLY_FOR_GUILD_WAR" : SKILL_ONLY_FOR_GUILD_WAR,
	"ONLY_FOR_GUILD_WAR_RANKED" : "Puoi usare la skill sono nella Ranked Mode",
}

SHOP_ERROR_DICT = {
	"NOT_ENOUGH_MONEY" : SHOP_NOT_ENOUGH_MONEY,
	"SOLDOUT" : SHOP_SOLDOUT,
	"INVENTORY_FULL" : SHOP_INVENTORY_FULL,
	"INVALID_POS" : SHOP_INVALID_POS,
	"NOT_ENOUGH_MONEY_EX" : SHOP_NOT_ENOUGH_MONEY_EX,
}

if app.ENABLE_MULTISHOP:
	SHOP_ERROR_DICT.update({
		"NOT_ENOUGH_ITEM" : SHOP_NOT_ENOUGH_ITEM,
	})

STAT_MINUS_DESCRIPTION = {
	"HTH-" : STAT_MINUS_CON,
	"INT-" : STAT_MINUS_INT,
	"STR-" : STAT_MINUS_STR,
	"DEX-" : STAT_MINUS_DEX,
}

MODE_NAME_LIST = ( PVP_OPTION_NORMAL, PVP_OPTION_REVENGE, PVP_OPTION_KILL, PVP_OPTION_PROTECT, )
TITLE_NAME_LIST = ( PVP_LEVEL0, PVP_LEVEL1, PVP_LEVEL2, PVP_LEVEL3, PVP_LEVEL4, PVP_LEVEL5, PVP_LEVEL6, PVP_LEVEL7, PVP_LEVEL8, )

def GetLetterImageName():
	return "season1/icon/scroll_close.tga"
def GetLetterOpenImageName():
	return "season1/icon/scroll_open.tga"
def GetLetterCloseImageName():
	return "season1/icon/scroll_close.tga"

def DO_YOU_SELL_ITEM(sellItemName, sellItemCount, sellItemPrice):
	if sellItemCount > 1 :
		return DO_YOU_SELL_ITEM2 % (sellItemName, sellItemCount, NumberToMoneyString(sellItemPrice) )
	else:
		return DO_YOU_SELL_ITEM1 % (sellItemName, NumberToMoneyString(sellItemPrice) )

def DO_YOU_BUY_ITEM(buyItemName, buyItemCount, buyItemPrice) :
	if buyItemCount > 1 :
		return DO_YOU_BUY_ITEM2 % ( buyItemName, buyItemCount, buyItemPrice )
	else:
		return DO_YOU_BUY_ITEM1 % ( buyItemName, buyItemPrice )
		
def REFINE_FAILURE_CAN_NOT_ATTACH(attachedItemName) :
	return REFINE_FAILURE_CAN_NOT_ATTACH0 % (attachedItemName)

def REFINE_FAILURE_NO_SOCKET(attachedItemName) :
	return REFINE_FAILURE_NO_SOCKET0 % (attachedItemName)

def REFINE_FAILURE_NO_GOLD_SOCKET(attachedItemName) :
	return REFINE_FAILURE_NO_GOLD_SOCKET0 % (attachedItemName)
	
def HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, dropItemCount) :
	if dropItemCount > 1 :
		return HOW_MANY_ITEM_DO_YOU_DROP2 % (dropItemName, dropItemCount)
	else :	
		return HOW_MANY_ITEM_DO_YOU_DROP1 % (dropItemName)
def HOW_MANY_ITEM_DO_YOU_DROP_NEW(dropItemName, dropItemCount, sellprice) :
	if dropItemCount > 1 :
		return HOW_MANY_ITEM_DO_YOU_DROP_NEW2 % (dropItemName, dropItemCount, sellprice)
	else :
		return HOW_MANY_ITEM_DO_YOU_DROP_NEW1 % (dropItemName, sellprice)
def FISHING_NOTIFY(isFish, fishName) :
	if isFish :
		return FISHING_NOTIFY1 % ( fishName )
	else :
		return FISHING_NOTIFY2 % ( fishName )

def FISHING_SUCCESS(isFish, fishName) :
	if isFish :
		return FISHING_SUCCESS1 % (fishName)
	else :
		return FISHING_SUCCESS2 % (fishName)
		
if app.ENABLE_MULTISHOP:
	def NumberToWithItemString(n,c):
		if n <= 0:
			return "0 %s" % (c)
		return "%s %s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]), c)
		
def NumberToMoneyString(n) :
	if n <= 0 :
		return "0 %s" % (MONETARY_UNIT0)

	return "%s %s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]), MONETARY_UNIT0) 

def NumberToSecondaryCoinString(n) :
	if n <= 0 :
		return "0 %s" % (MONETARY_UNIT_JUN)

	return "%s %s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]), MONETARY_UNIT_JUN) 

def PrettyNumber(n):
	if n <= 0:
		return "0"

	return "%s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]))

def NumberToString(n) :
	if n <= 0 :
		return "0"

	return "%s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]))


def NumberToMoneyStringNEW(n) :
	if n <= 0 :
		return "0"
	return "%s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]))


def surever(time):
	m, s = divmod(time, 60)
	h, m = divmod(m, 60)
	return "%02d:%02d:%02d" % (h, m, s)

if app.ENABLE_OFFLINE_SHOP_SYSTEM:
	def NumberToDisplayedCount(n):
		if n <= 0 :
			return "0 %s" % (MONETARY_UNIT_DISPLAYED_COUNT)

		return "%s %s" % ('.'.join([ i - 3 < 0 and str(n)[:i] or str(n)[i - 3 : i] for i in range(len(str(n)) % 3, len(str(n)) + 1, 3) if i ]), MONETARY_UNIT_DISPLAYED_COUNT)

def NumberToString2(n) :
	return "%s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ])) 

if app.ENABLE_CHEQUE_SYSTEM:
	def DO_YOU_BUY_ITEM_NEW(buyItemName, buyItemCount, buyItemPrice, buyItemCheque) :
		if buyItemCheque > 0:
			if buyItemCount > 1 :
				return DO_YOU_BUY_ITEM4 % ( buyItemName, buyItemCount, buyItemCheque, buyItemPrice )
			else:
				return DO_YOU_BUY_ITEM3 % ( buyItemName, buyItemCheque, buyItemPrice )
		else:
			if buyItemCount > 1 :
				return DO_YOU_BUY_ITEM2 % ( buyItemName, buyItemCount, buyItemPrice )
			else:
				return DO_YOU_BUY_ITEM1 % ( buyItemName, buyItemPrice )
	
	def NumberToChequeString(n) :
		if n <= 0 :
			return "0 %s" % (CHEQUE_SYSTEM_UNIT_WON)
		cheque = str(n)
		return "%s %s" % (cheque, CHEQUE_SYSTEM_UNIT_WON)

	def NumberToCheque(n) :
		if n <= 0 :
			return "0"
		cheque = str(n)
		return "%s" % (cheque)

	def NumberToMoney(n) :
		if n <= 0 :
			return "0"

		return "%s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]))

def MoneyFormat(n):
	return "%s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ])) 

def NumberWithPoint(n) :
	if n <= 0 :
		return "0"

	return "%s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]))
	
def SecondToMS(time):
	if time < 60:
		return "%d%s" % (time, SECOND)

	second = int(time % 60)
	minute = int((time / 60) % 60)

	text = ""

	if minute > 0:
		text += str(minute) + MINUTE
		if minute > 0:
			text += " "

	if second > 0:
		text += str(second) + SECOND

	return text
	
if app.ENABLE_MAINTENANCE_SYSTEM:
	def SecondToDHMS(time, ignoreSecTime = -1, useShortName = TRUE):
		text = ""
		if time < 0:
			time *= -1
			text = "-"

		second = int(time % 60)
		minute = int((time / 60) % 60)
		hour = int(((time / 60) / 60) % 24)
		day = int(((time / 60) / 60) / 24)

		if ignoreSecTime > 0 and time >= ignoreSecTime:
			second = 0

		if day > 0:
			if day == 1:
				text += str(day) + " d "
			else:
				text += str(day) + " d "

		if hour > 0:
			text += str(hour) + " "
			if useShortName == TRUE:
				text += "H. "
			else:
				if hour == 1:
					text += "Ora "
				else:
					text += "Ore "

		if minute > 0:
			text += str(minute) + " "
			if useShortName == TRUE:
				text += "Min. "
			else:
				if minute == 1:
					text += "Minut "
				else:
					text += "Minute "

		if second > 0 or (day == 0 and hour == 0 and minute == 0):
			text += str(second) + " "
			if useShortName == TRUE:
				text += "Sec. "
			else:
				if second == 1:
					text += "Secunda "
				else:
					text += "Secunde "

		return text[:-1]