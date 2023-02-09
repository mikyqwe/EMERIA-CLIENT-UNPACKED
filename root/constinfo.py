import app
if app.ENABLE_CHAT_COLOR_SYSTEM:
	chat_color_page_open = 0
	chat_color = ""
if app.WORLD_BOSS_YUMA:
	WORLD_BOSS_TEXT_POSITION = [0, 0, 0 ,0 ,0]
if app.ENABLE_EVENT_MANAGER:
	_interface_instance = None
	def GetInterfaceInstance():
		global _interface_instance
		return _interface_instance
	def SetInterfaceInstance(instance):
		global _interface_instance
		if _interface_instance:
			del _interface_instance
		_interface_instance = instance

if app.ENABLE_GUILD_REQUEST:
	_interface_instance = None
	def GetInterfaceInstance():
		global _interface_instance
		return _interface_instance
	def SetInterfaceInstance(instance):
		global _interface_instance
		if _interface_instance:
			del _interface_instance
		_interface_instance = instance


if app.ENABLE_COSTUME_SWITCHBOT:
	BONUS_SWITCHER = 0
	
	def IS_SWITCHER(itemVnum,):
		if itemVnum == 70063:
			return 1
		elif itemVnum == 70064:
			return 1
		return 0
		
	AVG_DMG_WARNING = 40 #se hai trovato bonus danni medi over 40 ti da un avviso
	SK_DMG_WARNING = 15 #se hai trovato bonus danni abi over 15 ti da un avviso
automatic_check = 1
Compared = 0

INTROSELECT_LOGIN = False

BIO_DICT = []
BIO_CHANGED = 0
if app.ENABLE_HUNTING_SYSTEM:
	HUNTING_MAIN_UI_SHOW = 0
	HUNTING_MINI_UI_SHOW = 0
	HUNTING_BUTTON_FLASH = 0
	HUNTING_BUTTON_IS_FLASH = 0

finder_counts = 0
finder_items = {}
finder_items_v = {}
OVER_IN = False

if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
	IsInventoryOpened = False
	IsSpecialStorageOpened = False

	SpecialStorageCategory = -1

need_open_pickup_filter = 0

if app.WON_EXCHANGE:
	WHEEL_TO_SCROLL_MIN = 5
	WHEEL_TO_SCROLL_MAX = 40
	WHEEL_TO_SCROLL_DEFAULT = 13
	WHEEL_VALUE = WHEEL_TO_SCROLL_DEFAULT

	def WHEEL_TO_SCROLL(wheel, custom = None):
		return -wheel * ((custom if custom else WHEEL_VALUE) / WHEEL_TO_SCROLL_MIN)

	def WHEEL_TO_SCROLL_SLOW(wheel):
		return -wheel * max(1, WHEEL_VALUE / WHEEL_TO_SCROLL_DEFAULT)

	def WHEEL_TO_SCROLL_PX(wheel):
		return -wheel * WHEEL_VALUE
if app.GUILD_WAR_COUNTER:
	import os
	def CheckDirectory(directory):
		try:
			os.makedirs(directory)
		except:
			pass
	def CheckFile(directory):
		if os.path.exists(directory):
			return True
		return False
	def RemoveFile(directory):
		if os.path.exists(directory):
		  os.remove(directory)
	def encodeMessage(message, keycode):
		ciphertext = ""
		alphabet = "!'^+%&/()=?_/*abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUWXYZ0123456789"
		for letter in message:
			if letter in alphabet:
				keyLetter = ((alphabet.index(letter)) + keycode) % len(alphabet)
				cipherLetter = alphabet[keyLetter]
				ciphertext = ciphertext + cipherLetter
			else:
				cipherLetter = letter
				ciphertext = ciphertext + cipherLetter
		return ciphertext

	def decodeMessage(message, keycode):
		ciphertext = ""
		alphabet = "!'^+%&/()=?_/*abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUWXYZ0123456789"
		for letter in message:
			if letter in alphabet:
				keyLetter = ((alphabet.index(letter)) - keycode) % len(alphabet)
				cipherLetter = alphabet[keyLetter]
				ciphertext = ciphertext + cipherLetter
			else:
				cipherLetter = letter
				ciphertext = ciphertext + cipherLetter
		return ciphertext

PetPosInv = 0
PetVnum = 0
PetOfficialVnum = 0
DROP_GUI_CHECK = 0
Element_ID = 0
FEQO = 0

HIDE_SPECIAL_CHAT = 1

ENABLE_BUFF_DISABLE = True

if app.ENABLE_HIDE_COSTUME_SYSTEM:
	hide_buttons = 1

ENABLE_MULTI_RANKING=0
py_Flag = {}
def GetFlag(flagname):
	global py_Flag
	return py_Flag.get(flagname, 0)
def SetFlag(flagname,value):
	global py_Flag
	py_Flag[flagname] = value
ENABLE_SHOW_CHEST_DROP=1
ULTIMATE_TOOLTIP_MAX_CLICK=25
def IsNewChest(itemVnum):
	if 27987 == itemVnum:
		return True
	elif 50255 == itemVnum:
		return True
	return False
   
KILL_STATISTICS_DATA = [0, 0, 0, 0, 0, 0, 0, 0, 0,]
MAX_DUNGEON = 4 # IMPORTANT
dungeonInfo = []
dungeonInfoCooldown = []
dungeon_qf_index = 0 # for questindex
DungeonWarp = "" # for cmd
ENABLE_AURA_SYSTEM=1
SHOPNAMES_RANGE = 5000						# The range to see the shop name, previous this will be calculated in base of range bar.
ENABLE_NEW_DROP_ITEM = 1
# Showing description of item in refine window.
ENABLE_REFINE_ITEM_DESCRIPTION = 1
# EXTRA BEGIN
# loads 5 (B,M,G,P,F) skills .mse
ENABLE_NEW_LEVELSKILL_SYSTEM = 0
# don't set a random channel when you open the client
ENABLE_RANDOM_CHANNEL_SEL = 0
# don't remove id&pass if the login attempt fails
ENABLE_CLEAN_DATA_IF_FAIL_LOGIN = 0
# ctrl+v will now work
ENABLE_PASTE_FEATURE = 0
# display all the bonuses added by a stone instead of the first one
ENABLE_FULLSTONE_DETAILS = 1
# enable successfulness % in the refine dialog
ENABLE_REFINE_PCT = 1
ENABLE_EXPANDED_MONEY_TASKBAR = 1
# extra ui features
EXTRA_UI_FEATURE = 1
NEW_678TH_SKILL_ENABLE = 1
Yang = 1
# EXTRA END
if app.ENABLE_REFINE_RENEWAL:
	IS_AUTO_REFINE = False
	AUTO_REFINE_TYPE = 0
	AUTO_REFINE_DATA = {
		"ITEM" : [-1, -1],
		"NPC" : [0, -1, -1, 0]
	}
	
INPUT_IGNORE = 0
SelectJob = {
	'QID' : 0,
	'QCMD' : '',
}

AVAILABLE_LANGUAGES = {
	'de': {
		'name':'german', 
		'encoding':'cp1252'
	},
	'en': {
		'name':'english', 
		'encoding':'cp1252'
	},
	'es': {
		'name':'spanish', 
		'encoding':'cp1252'
	},
	'it': {
		'name':'italian', 
		'encoding':'cp1252'
	},
	'fr': {
		'name':'french', 
		'encoding':'cp1252'
	},
	# 'pt': {
	# 	'name':'portuguese', 
	# 	'encoding':'cp1252'
	# },
	# 'tr': {
	# 	'name':'turkish', 
	# 	'encoding':'cp1253'
	# },
	'pl': {
		'name':'polish', 
		'encoding':'cp1250'
	},
	'tr': {
		'name':'turkish', 
		'encoding':'cp1254'
	},
	# 'nl': {
	# 	'name':'dutch', 
	# 	'encoding':'cp1252'
	# },
	# 'ru': {
	# 	'name':'russian', 
	# 	'encoding':'cp1250'
	# },
	# 'hu': {
	# 	'name':'hungarian', 
	# 	'encoding':'cp1250'
	# },
	'ro': {
		'name':'romanian', 
		'encoding':'cp1250'
	},
	# 'ja': {
	# 	'name':'japanese',
	# 	'encoding':'cp932'
	# },
}

## Battle Pass
missions_bp = {}
info_missions_bp = {}
rewards_bp = {}
size_battle_pass = 0
status_battle_pass = 0
battle_status_pass = 0
final_rewards = []
## Battle Pass

cheque = 0

change_time = 0
# option
IN_GAME_SHOP_ENABLE = 1
CONSOLE_ENABLE = 0
Chitra = ''
TELEPORT_SYSTEM_GUI = 0
SKYBOX_GUI = 0
FAST_PAGE = 1
FAST_EQUIP = 0
envanter = 0
canShowRankingGuild = 0
ME_KEY = 0
PVPMODE_ENABLE = 1
ACCOUNT_NAME = "NoName"
WOLF_MAN = "DISABLED"
WOLF_WOMEN = "DISABLED"
PVPMODE_TEST_ENABLE = 0
PVPMODE_ACCELKEY_ENABLE = 1
PVPMODE_ACCELKEY_DELAY = 0.5
PVPMODE_PROTECTED_LEVEL = 15
if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
	MARKED_SHOP_VID	= 0
FOG_LEVEL0 = 4800.0
FOG_LEVEL1 = 9600.0
FOG_LEVEL2 = 12800.0
FOG_LEVEL = FOG_LEVEL0
FOG_LEVEL_LIST=[FOG_LEVEL0, FOG_LEVEL1, FOG_LEVEL2]
CAMERA_MAX_DISTANCE_SHORT = 2500.0
CAMERA_MAX_DISTANCE_LONG = 3500.0
CAMERA_MAX_DISTANCE_LIST=[CAMERA_MAX_DISTANCE_SHORT, CAMERA_MAX_DISTANCE_LONG]
CAMERA_MAX_DISTANCE = CAMERA_MAX_DISTANCE_SHORT

CHRNAME_COLOR_INDEX = 0

ENVIRONMENT_NIGHT="d:/ymir work/environment/moonlight04.msenv"

ReportLogin = 0
ReportEntered = ""
INPUT = 0

# constant
HIGH_PRICE = 500000
PET_EVOLUTION = 0
PET_LEVEL = 0
PET_MAIN = 0
FEEDWIND = 0
SKILL_PET3 = 0
SKILL_PET2 = 0
SKILL_PET1 = 0
LASTAFFECT_POINT = 0
LASTAFFECT_VALUE = 0
EVOLUTION = 0

MIDDLE_PRICE = 50000
ERROR_METIN_STONE = 28960
SUB2_LOADING_ENABLE = 1
EXPANDED_COMBO_ENABLE = 1
CONVERT_EMPIRE_LANGUAGE_ENABLE = 1
USE_ITEM_WEAPON_TABLE_ATTACK_BONUS = 0
ADD_DEF_BONUS_ENABLE = 1
LOGIN_COUNT_LIMIT_ENABLE = 0

USE_SKILL_EFFECT_UPGRADE_ENABLE = 1

VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = 1
GUILD_MONEY_PER_GSP = 100
GUILD_WAR_TYPE_SELECT_ENABLE = 1
TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE = 0

HAIR_COLOR_ENABLE = 1
ARMOR_SPECULAR_ENABLE = 1
WEAPON_SPECULAR_ENABLE = 1
SEQUENCE_PACKET_ENABLE = 1
KEEP_ACCOUNT_CONNETION_ENABLE = 1
MINIMAP_POSITIONINFO_ENABLE = 0
CONVERT_EMPIRE_LANGUAGE_ENABLE = 0
USE_ITEM_WEAPON_TABLE_ATTACK_BONUS = 0
ADD_DEF_BONUS_ENABLE = 0
LOGIN_COUNT_LIMIT_ENABLE = 0
PVPMODE_PROTECTED_LEVEL = 15
TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE = 10

isItemQuestionDialog = 0

GUILDSTORAGE = {
	"slots" : {"TAB0" : {},"TAB1" : {},"TAB2" : {}},
	"tempslots" : {"TAB0" : {},"TAB1" : {},"TAB2" : {}},
	"qid"	: 0,
	"questCMD" : "",
	"members": {},
	"logs" : {},
}

def GET_ITEM_QUESTION_DIALOG_STATUS():
	global isItemQuestionDialog
	return isItemQuestionDialog

def SET_ITEM_QUESTION_DIALOG_STATUS(flag):
	global isItemQuestionDialog
	isItemQuestionDialog = flag

import app
if app.ENABLE_SEND_TARGET_INFO:
	MONSTER_INFO_DATA = {}

import net

########################

def SET_DEFAULT_FOG_LEVEL():
	global FOG_LEVEL
	app.SetMinFog(FOG_LEVEL)

def SET_FOG_LEVEL_INDEX(index):
	global FOG_LEVEL
	global FOG_LEVEL_LIST
	try:
		FOG_LEVEL=FOG_LEVEL_LIST[index]
	except IndexError:
		FOG_LEVEL=FOG_LEVEL_LIST[0]
	app.SetMinFog(FOG_LEVEL)

def GET_FOG_LEVEL_INDEX():
	global FOG_LEVEL
	global FOG_LEVEL_LIST
	return FOG_LEVEL_LIST.index(FOG_LEVEL)

########################

def SET_DEFAULT_CAMERA_MAX_DISTANCE():
	global CAMERA_MAX_DISTANCE
	app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE)

def SET_CAMERA_MAX_DISTANCE_INDEX(index):
	global CAMERA_MAX_DISTANCE
	global CAMERA_MAX_DISTANCE_LIST
	try:
		CAMERA_MAX_DISTANCE=CAMERA_MAX_DISTANCE_LIST[index]
	except:
		CAMERA_MAX_DISTANCE=CAMERA_MAX_DISTANCE_LIST[0]

	app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE)

def GET_CAMERA_MAX_DISTANCE_INDEX():
	global CAMERA_MAX_DISTANCE
	global CAMERA_MAX_DISTANCE_LIST
	return CAMERA_MAX_DISTANCE_LIST.index(CAMERA_MAX_DISTANCE)

########################

import chrmgr
import player

def SET_DEFAULT_CHRNAME_COLOR():
	global CHRNAME_COLOR_INDEX
	chrmgr.SetEmpireNameMode(CHRNAME_COLOR_INDEX)

def SET_CHRNAME_COLOR_INDEX(index):
	global CHRNAME_COLOR_INDEX
	CHRNAME_COLOR_INDEX=index
	chrmgr.SetEmpireNameMode(index)

def GET_CHRNAME_COLOR_INDEX():
	global CHRNAME_COLOR_INDEX
	return CHRNAME_COLOR_INDEX

def SET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD(index):
	global VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD
	VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = index

def GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD():
	global VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD
	return VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD

def SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE():
	global CONVERT_EMPIRE_LANGUAGE_ENABLE
	net.SetEmpireLanguageMode(CONVERT_EMPIRE_LANGUAGE_ENABLE)

def SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS():
	global USE_ITEM_WEAPON_TABLE_ATTACK_BONUS
	player.SetWeaponAttackBonusFlag(USE_ITEM_WEAPON_TABLE_ATTACK_BONUS)

def SET_DEFAULT_USE_SKILL_EFFECT_ENABLE():
	global USE_SKILL_EFFECT_UPGRADE_ENABLE
	app.SetSkillEffectUpgradeEnable(USE_SKILL_EFFECT_UPGRADE_ENABLE)

def SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE():
	global TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE
	app.SetTwoHandedWeaponAttSpeedDecreaseValue(TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE)

########################
import item

ACCESSORY_MATERIAL_LIST = [50623, 50624, 50625, 50626, 50627, 50628, 50629, 50630, 50631, 50632, 50633, 50634, 50635, 50636, 50637, 50638, 50639]#, 50640, 50641, 50642]
JewelAccessoryInfos = [
		# jewel		wrist	neck	ear
		[ 50634,	14420,	16220,	17220 ],
		[ 50635,	14500,	16500,	17500 ],
		[ 50636,	14520,	16520,	17520 ],
		[ 50637,	82520,	82530,	82540 ],
		[ 50638,	14560,	82640,	82630 ],
		[ 50639,	82610,	82600,	82590 ],


		#[ 50640,	82520,	82530,	82540 ],
		#[ 50641,	14560,	82640,	82630 ],
		#[ 50642,	82610,	82600,	82590 ],
	]
def GET_ACCESSORY_MATERIAL_VNUM(vnum, subType):
	ret = vnum
	item_base = (vnum / 10) * 10
	for info in JewelAccessoryInfos:
		if item.ARMOR_WRIST == subType:
			if info[1] == item_base:
				return info[0]
		elif item.ARMOR_NECK == subType:
			if info[2] == item_base:
				return info[0]
		elif item.ARMOR_EAR == subType:
			if info[3] == item_base:
				return info[0]

	if vnum >= 16210 and vnum <= 16219:
		return 50625

	if item.ARMOR_WRIST == subType:
		WRIST_ITEM_VNUM_BASE = 14000
		ret -= WRIST_ITEM_VNUM_BASE
	elif item.ARMOR_NECK == subType:
		NECK_ITEM_VNUM_BASE = 16000
		ret -= NECK_ITEM_VNUM_BASE
	elif item.ARMOR_EAR == subType:
		EAR_ITEM_VNUM_BASE = 17000
		ret -= EAR_ITEM_VNUM_BASE

	type = ret/20

	if type<0 or type>=len(ACCESSORY_MATERIAL_LIST):
		type = (ret-170) / 20
		if type<0 or type>=len(ACCESSORY_MATERIAL_LIST):
			return 0

	return ACCESSORY_MATERIAL_LIST[type]

##################################################################
## 새로 추가된 '벨트' 아이템 타입과, 벨트의 소켓에 꽂을 아이템 관련..
## 벨트의 소켓시스템은 악세서리와 동일하기 때문에, 위 악세서리 관련 하드코딩처럼 이런식으로 할 수밖에 없다..

def GET_BELT_MATERIAL_VNUM(vnum, subType = 0):
	# 현재는 모든 벨트에는 하나의 아이템(#18900)만 삽입 가능
	return 18900

##################################################################
## 자동물약 (HP: #72723 ~ #72726, SP: #72727 ~ #72730)

# 해당 vnum이 자동물약인가?
def IS_AUTO_POTION(itemVnum):
	return IS_AUTO_POTION_HP(itemVnum) or IS_AUTO_POTION_SP(itemVnum) or IS_N_PET(itemVnum)

def IS_N_PET(itemVnum):
	pet_vnums = [53234, 53013, 53005, 53011, 53012, 53231, 53218, 53220, 53014]
	if itemVnum in pet_vnums:
		return 1
	return 0

# 해당 vnum이 HP 자동물약인가?
def IS_AUTO_POTION_HP(itemVnum):
	if 72723 <= itemVnum and 72726 >= itemVnum:
		return 1
	elif itemVnum >= 76021 and itemVnum <= 76022:		## 새로 들어간 선물용 화룡의 축복
		return 1
	elif itemVnum == 79012:
		return 1

	return 0

# 해당 vnum이 SP 자동물약인가?
def IS_AUTO_POTION_SP(itemVnum):
	if 72727 <= itemVnum and 72730 >= itemVnum:
		return 1
	elif itemVnum >= 76004 and itemVnum <= 76005:		## 새로 들어간 선물용 수룡의 축복
		return 1
	elif itemVnum == 79013:
		return 1
	elif itemVnum >= 55701 and itemVnum <= 55710: #pets effetto
		return 1
				
	return 0
	
_interface_instance = None
def GetInterfaceInstance():
	global _interface_instance
	return _interface_instance
def SetInterfaceInstance(instance):
	global _interface_instance
	if _interface_instance:
		del _interface_instance
	_interface_instance = instance
def raceToJob(race):
	if race == 0 or race == 4:#warrior
		return 0
	elif race == 1 or race == 5:#assassin
		return 1
	elif race == 2 or race == 6:#sura
		return 2
	elif race == 3 or race == 7:#shaman
		return 3
	return 0
def IS_SET(value, flag):
	return (value & flag) == flag
def SET_BIT(value, bit):
	return value | (bit)
def REMOVE_BIT(value, bit):
	return value & ~(bit)
def getFlagValue(value):
	return 1 << value
	
def COUNT_SPECIFY_ITEM(itemVnum):
	finalCount = 0
	
	for i in xrange(player.INVENTORY_PAGE_SIZE*player.INVENTORY_PAGE_COUNT):
		if player.GetItemIndex(i) == itemVnum:
			finalCount = finalCount + player.GetItemCount(i)
			
	return finalCount


def WriteLineInFile(fname, linenum, s):
	import os
	farr = []
	if os.path.exists(fname):
		f = open(fname, "r")
		for line in f:
			farr.append(line)
		f.close()
	while len(farr) < int(linenum):
		farr.append("")
	farr[int(linenum)-1] = str(s)
	f = open(fname, "w")
	for line in farr:
		f.write(line)
		if (len(line) > 0 and line[-1:] != "\n") or len(line) == 0:
			f.write("\n")
	f.close()

def ReadLineInFile(fname, linenum):
	import os
	if not os.path.exists(fname):
		return ""
	f = open(fname, "r")
	farr = []
	for line in f:
		farr.append(line)
	f.close()
	if len(farr) >= int(linenum):
		ret = farr[int(linenum)-1]
		if ret[-1:] == "\n":
			return ret[:-1]
		else:
			return ret
	else:
		return ""

