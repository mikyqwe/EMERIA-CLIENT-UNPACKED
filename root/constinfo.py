import app
import localeInfo

# EXTRA BEGIN
# loads 5 (B,M,G,P,F) skills .mse
ENABLE_NEW_LEVELSKILL_SYSTEM = 0
# don't set a random channel when you open the client
ENABLE_RANDOM_CHANNEL_SEL = 0
# don't remove id&pass if the login attempt fails
ENABLE_CLEAN_DATA_IF_FAIL_LOGIN = 0
# ctrl+v will now work
ENABLE_PASTE_FEATURE = 1
# display all the bonuses added by a stone instead of the first one
ENABLE_FULLSTONE_DETAILS = 1
# enable successfulness % in the refine dialog
ENABLE_REFINE_PCT = 0
# extra ui features
EXTRA_UI_FEATURE = 1
#
ENABLE_SHOW_CHEST_DROP=1
ULTIMATE_TOOLTIP_MAX_CLICK=25
def IsNewChest(itemVnum):
	if 27987 == itemVnum:
		return True
	elif 50255 == itemVnum:
		return True
	return False
NEW_678TH_SKILL_ENABLE = 1
# EXTRA END

INPUT_IGNORE = 0
SelectJob = {
	'QID' : 0,
	'QCMD' : '',
}

ENABLE_EXPANDED_MONEY_TASKBAR = 1

BIO_DICT = []
BIO_CHANGED = 0
if app.ENABLE_HUNTING_SYSTEM:
	HUNTING_MAIN_UI_SHOW = 0
	HUNTING_MINI_UI_SHOW = 0
	HUNTING_BUTTON_FLASH = 0
	HUNTING_BUTTON_IS_FLASH = 0
	
DROP_GUI_CHECK = 0
ENABLE_NEW_DROP_ITEM = 1
Element_ID = 0
#Interface Login/Select
ACCOUNT_NAME = "NoName"
WOLF_MAN = "DISABLED"
WOLF_WOMEN = "DISABLED"

if app.ENABLE_SPECIAL_STORAGE_SYSTEM:
	IsInventoryOpened = False
	IsSpecialStorageOpened = False

	SpecialStorageCategory = -1

if app.ENABLE_SEND_TARGET_INFO:
	MONSTER_INFO_DATA = {}

# enable save account
ENABLE_SAVE_ACCOUNT = True
if ENABLE_SAVE_ACCOUNT:
	class SAB:
		ST_CACHE, ST_FILE, ST_REGISTRY = xrange(3)
		slotCount = 5
		storeType = ST_REGISTRY # 0 cache, 1 file, 2 registry
		btnName = {
			"Save": "SaveAccountButton_Save_%02d",
			"Access": "SaveAccountButton_Access_%02d",
			"Remove": "SaveAccountButton_Remove_%02d",
		}
		accData = {}
		regPath = r"SOFTWARE\Metin2"
		regName = "slot%02d_%s"
		regValueId = "id"
		regValuePwd = "pwd"
		fileExt = ".do.not.share.it.txt"
def CreateSABDataFolder(filePath):
	import os
	folderPath = os.path.split(filePath)[0]
	if not os.path.exists(folderPath):
		os.makedirs(folderPath)
def IsExistSABDataFile(filePath):
	import os
	return os.path.exists(filePath)
def GetSABDataFile(idx):
	import os
	filePath = "%s\\Metin2\\" % os.getenv('appdata')
	filePath += SAB.regName % (idx, SAB.regValueId)
	filePath += SAB.fileExt
	return filePath
def DelJsonSABData(idx):
	import os
	filePath = GetSABDataFile(idx)
	if IsExistSABDataFile(filePath):
		os.remove(filePath)
def GetJsonSABData(idx):
	(id, pwd) = ("", "")
	filePath = GetSABDataFile(idx)
	if not IsExistSABDataFile(filePath):
		return (id, pwd)
	with old_open(filePath) as data_file:
		try:
			import json
			(id, pwd) = json.load(data_file)
			id = str(id) # unicode to ascii
			pwd = str(pwd) # unicode to ascii
		except ValueError:
			pass
	return (id, pwd)
def SetJsonSABData(idx, slotData):
	filePath = GetSABDataFile(idx)
	CreateSABDataFolder(filePath)
	with old_open(filePath, "w") as data_file:
		import json
		json.dump(slotData, data_file)
def DelWinRegKeyValue(keyPath, keyName):
	try:
		import _winreg
		_winreg.CreateKey(_winreg.HKEY_CURRENT_USER, keyPath)
		_tmpKey = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, keyPath, 0, _winreg.KEY_WRITE)
		_winreg.DeleteValue(_tmpKey, keyName)
		_winreg.CloseKey(_tmpKey)
		return True
	except WindowsError:
		return False
def GetWinRegKeyValue(keyPath, keyName):
	try:
		import _winreg
		_tmpKey = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, keyPath, 0, _winreg.KEY_READ)
		keyValue, keyType = _winreg.QueryValueEx(_tmpKey, keyName)
		_winreg.CloseKey(_tmpKey)
		return str(keyValue) # unicode to ascii
	except WindowsError:
		return None
def SetWinRegKeyValue(keyPath, keyName, keyValue):
	try:
		import _winreg
		_winreg.CreateKey(_winreg.HKEY_CURRENT_USER, keyPath)
		_tmpKey = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, keyPath, 0, _winreg.KEY_WRITE)
		_winreg.SetValueEx(_tmpKey, keyName, 0, _winreg.REG_SZ, keyValue)
		_winreg.CloseKey(_tmpKey)
		return True
	except WindowsError:
		return False
# classic minmax def
def minmax(tmin, tmid, tmax):
	if tmid < tmin:
		return tmin
	elif tmid > tmax:
		return tmax
	return tmid
# EXTRA END

# option
IN_GAME_SHOP_ENABLE = 1
CONSOLE_ENABLE = 0

PVPMODE_ENABLE = 1
PVPMODE_TEST_ENABLE = 0
PVPMODE_ACCELKEY_ENABLE = 1
PVPMODE_ACCELKEY_DELAY = 0.5
PVPMODE_PROTECTED_LEVEL = 15

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

HIGH_PRICE = 500000
MIDDLE_PRICE = 50000
ERROR_METIN_STONE = 28960
SUB2_LOADING_ENABLE = 1
EXPANDED_COMBO_ENABLE = 1
CONVERT_EMPIRE_LANGUAGE_ENABLE = 0
USE_ITEM_WEAPON_TABLE_ATTACK_BONUS = 0
ADD_DEF_BONUS_ENABLE = 0
LOGIN_COUNT_LIMIT_ENABLE = 0

USE_SKILL_EFFECT_UPGRADE_ENABLE = 1

VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = 1
GUILD_MONEY_PER_GSP = 100
GUILD_WAR_TYPE_SELECT_ENABLE = 1
TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE = 10

HAIR_COLOR_ENABLE = 1
ARMOR_SPECULAR_ENABLE = 1
WEAPON_SPECULAR_ENABLE = 1
SEQUENCE_PACKET_ENABLE = 1
KEEP_ACCOUNT_CONNETION_ENABLE = 1
MINIMAP_POSITIONINFO_ENABLE = 1

isItemQuestionDialog = 0

def ConvertMoneyText(text, powers = dict(k = 10**3, m = 10**6, b = 10**9)):
	match = re.search(r'(\d+)({:s}+)?'.format('+|'.join(powers.keys())), text, re.I)
	if match:
		moneyValue, suffixName = match.groups()
		moneyValue = int(moneyValue)
		if not suffixName:
			return moneyValue

		return moneyValue * (powers[suffixName[0]] ** len(suffixName))

	return 0

if app.__CHAT_SETTINGS__:
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

	import chat
	OPTION_CHECKBOX_TALKING = 1
	OPTION_CHECKBOX_PARTY = 2
	OPTION_CHECKBOX_GUILD = 3
	OPTION_CHECKBOX_SHOUT = 4
	OPTION_CHECKBOX_INFO = 5
	OPTION_CHECKBOX_NOTICE = 6
	OPTION_CHECKBOX_DICE = 7
	OPTION_CHECKBOX_EXP_INFO = 8
	OPTION_CHECKBOX_ITEM_INFO = 9
	OPTION_CHECKBOX_MONEY_INFO = 10
	OPTION_CHECKBOX_FILTER = 11

	OPTION_CHECKBOX_FLAG_EN = 12
	OPTION_CHECKBOX_FLAG_DE = 13
	OPTION_CHECKBOX_FLAG_TR = 14
	OPTION_CHECKBOX_FLAG_PT = 15
	OPTION_CHECKBOX_FLAG_ES = 16
	OPTION_CHECKBOX_FLAG_FR = 17
	OPTION_CHECKBOX_FLAG_RO = 18
	OPTION_CHECKBOX_FLAG_PL = 19
	OPTION_CHECKBOX_FLAG_IT = 20
	OPTION_CHECKBOX_FLAG_CZ = 21
	OPTION_CHECKBOX_FLAG_HU = 22
	OPTION_MAX = 23

	OPTION_CHECKBOX_MODE = {
		OPTION_CHECKBOX_TALKING : [[chat.CHAT_TYPE_TALKING], "TEST"],
		OPTION_CHECKBOX_INFO : [[chat.CHAT_TYPE_INFO], "TEST"],
		OPTION_CHECKBOX_NOTICE : [[chat.CHAT_TYPE_NOTICE,chat.CHAT_TYPE_BIG_NOTICE], "TEST"],
		OPTION_CHECKBOX_PARTY : [[chat.CHAT_TYPE_PARTY], "TEST"],
		OPTION_CHECKBOX_GUILD : [[chat.CHAT_TYPE_GUILD], "TEST"],
		OPTION_CHECKBOX_SHOUT : [[chat.CHAT_TYPE_SHOUT], "TEST"],
		OPTION_CHECKBOX_DICE : [[chat.CHAT_TYPE_DICE_INFO], "TEST"],
		OPTION_CHECKBOX_EXP_INFO : [[chat.CHAT_TYPE_EXP_INFO], "TEST"],
		OPTION_CHECKBOX_ITEM_INFO : [[chat.CHAT_TYPE_ITEM_INFO], "TEST"],
		OPTION_CHECKBOX_MONEY_INFO : [[chat.CHAT_TYPE_MONEY_INFO], "TEST"],
	}

	cacheChat = {}
	def CreateEmptyList(index):
		list = [1] * OPTION_MAX
		list[0] = str(index)
		list[OPTION_CHECKBOX_FILTER] = 0
		for langIndex in range(OPTION_CHECKBOX_FLAG_EN, OPTION_MAX):
			list[langIndex] = 0
		return list
	
	def SaveChatData():
		global cacheChat
		if len(cacheChat) == 0:
			return
		
		#import dbg
		#dbg.TraceError("--------------------------------------------")
		#dbg.TraceError(" ")
		#dbg.TraceError(str(cacheChat))
		#dbg.TraceError(" ")
		#dbg.TraceError("--------------------------------------------")
		
		MAIN_FILE = "lib/chatConfig"
		PLAYER_FILE = MAIN_FILE+"/"+player.GetName()+".chat"

		try:
			file = open(PLAYER_FILE, "w+")
			for key, data in cacheChat.items():
				data = cacheChat[key]
				text = ""
				for x in xrange(OPTION_MAX):
					text+=str(data[x])+"#"
				file.write(text+"\n")
			file.close()
		except:
			pass

	def LoadChatNewEmpty(index):
		global cacheChat
		cacheChat[index] = CreateEmptyList(index)
		SaveChatData()

	def LoadChatEmpty():
		global cacheChat
		cacheChat = {
			0: ['0', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			1: ['Empire', 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			2: ['Yang', 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			3: ['Exp', 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			4: ['Server', 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		}
		#cacheChat[0] = CreateEmptyList(0)
		SaveChatData()

	def RemoveChat(index):
		global cacheChat
		if cacheChat.has_key(index):
			del cacheChat[index]
			SaveChatData()

	def LoadChatData():
		global cacheChat
		cacheChat = {}
		MAIN_FILE = "lib/chatConfig"
		PLAYER_FILE = MAIN_FILE+"/"+player.GetName()+".chat"
		CheckDirectory(MAIN_FILE)
		if CheckFile(PLAYER_FILE):
			lines = open(PLAYER_FILE, "r").readlines()
			if len(lines) > 0:

				index = 0
				for line in lines:
					lineSplit = line.split("#")

					if len(lineSplit)==0 or OPTION_MAX != len(lineSplit)-1:
						LoadChatEmpty()
					else:
						list = [1] * OPTION_MAX
						for j in xrange(len(lineSplit)-1):
							if j == 0:
								list[j] = str(lineSplit[j])
							else:
								list[j] = int(lineSplit[j])
						cacheChat[index] = list
					index+=1
			else:
				LoadChatEmpty()
		else:
			LoadChatEmpty()


if app.ENABLE_WIKI:
	_main_wiki_instance = None
	_listbox_wiki_instance = None
	def SetMainParent(instance):
		global _main_wiki_instance
		if _main_wiki_instance:
			del _main_wiki_instance
		_main_wiki_instance = instance
	def GetMainParent():
		global _main_wiki_instance
		return _main_wiki_instance
	def SetListBox(instance):
		global _listbox_wiki_instance
		if _listbox_wiki_instance:
			del _listbox_wiki_instance
		_listbox_wiki_instance = instance
	def GetListBox():
		global _listbox_wiki_instance
		return _listbox_wiki_instance
	def IS_SET(value, flag):
		return (value & flag) == flag


def GET_ITEM_QUESTION_DIALOG_STATUS():
	global isItemQuestionDialog
	return isItemQuestionDialog

def SET_ITEM_QUESTION_DIALOG_STATUS(flag):
	global isItemQuestionDialog
	isItemQuestionDialog = flag

import app
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
import app

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

ACCESSORY_MATERIAL_LIST = [50623, 50624, 50625, 50626, 50627, 50628, 50629, 50630, 50631, 50632, 50633, 50634, 50635, 50636, 50637, 50638, 50639]
JewelAccessoryInfos = [
		# jewel		wrist	neck	ear
		[ 50634,	14420,	16220,	17220 ],
		[ 50635,	14500,	16500,	17500 ],
		[ 50636,	14520,	16520,	17520 ],
		[ 50637,	14540,	16540,	17540 ],
		[ 50638,	14560,	16560,	17560 ],
		[ 50639,	14570,	16570,	17570 ],
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

def GET_BELT_MATERIAL_VNUM(vnum, subType = 0):
	return 18900

##################################################################

def IS_AUTO_POTION(itemVnum):
	return IS_AUTO_POTION_HP(itemVnum) or IS_AUTO_POTION_SP(itemVnum)

def IS_AUTO_POTION_HP(itemVnum):
	if 72723 <= itemVnum and 72726 >= itemVnum:
		return 1
	elif itemVnum >= 76021 and itemVnum <= 76022:
		return 1
	elif itemVnum == 79012:
		return 1

	return 0

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

def IS_BLEND_POTION(itemVnum):
	if itemVnum >= 50821 and itemVnum <= 50826:
		return 1
	elif itemVnum >= 950821 and itemVnum <= 951002:
		return 1
	elif itemVnum >= 27863 and itemVnum <= 27878:
		return 1
	elif itemVnum == 51002:
		return 1

	return 0

def IS_EXTENDED_BLEND_POTION(itemVnum):
	if itemVnum >= 950821 and itemVnum <= 950826: # Dews
		return 1
	elif itemVnum == 951002: # Cristal Energy
		return 1
	elif itemVnum >= 939017 and itemVnum <= 939020: # Dragon God Medals
		return 1
	elif itemVnum == 939024 or itemVnum == 939025: # Critical & Penetration
		return 1
	elif itemVnum == 927209 or itemVnum == 927212: # Attack Speed & Move Speed
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
		