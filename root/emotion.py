import localeInfo
import player
import chrmgr
import chr
import app

EMOTION_CLAP = 1
EMOTION_CONGRATULATION = 2
EMOTION_FORGIVE = 3
EMOTION_ANGRY = 4
EMOTION_ATTRACTIVE = 5
EMOTION_SAD = 6
EMOTION_SHY = 7
EMOTION_CHEERUP = 8
EMOTION_BANTER = 9
EMOTION_JOY = 10
EMOTION_CHEERS_1 = 11
EMOTION_CHEERS_2 = 12
EMOTION_DANCE_1 = 13
EMOTION_DANCE_2 = 14
EMOTION_DANCE_3 = 15
EMOTION_DANCE_4 = 16
EMOTION_DANCE_5 = 17
EMOTION_DANCE_6 = 18
EMOTION_KISS = 51
EMOTION_FRENCH_KISS = 52
EMOTION_SLAP = 53

if app.ENABLE_EXPRESSING_EMOTION:
	EMOTICON_NEXT = 12
	EMOTION_PUSHUP 	= app.SLOT_EMOTION_START
	EMOTION_DANCE_7 = app.SLOT_EMOTION_START+1
	EMOTION_EXERCISE = app.SLOT_EMOTION_START+2
	EMOTION_DOZE = app.SLOT_EMOTION_START+3
	EMOTION_SELFIE = app.SLOT_EMOTION_START+4
	EMOTION_CHARGING = app.SLOT_EMOTION_START+5
	EMOTION_NOSAY = app.SLOT_EMOTION_START+6
	EMOTION_WEATHER_1 = app.SLOT_EMOTION_START+7
	EMOTION_WEATHER_2 = app.SLOT_EMOTION_START+8
	EMOTION_WEATHER_3 = app.SLOT_EMOTION_START+9
	EMOTION_HUNGRY = app.SLOT_EMOTION_START+10
	EMOTION_SIREN = app.SLOT_EMOTION_START+11
	EMOTION_ALCOHOL = app.SLOT_EMOTION_START+12
	EMOTION_CALL = app.SLOT_EMOTION_START+13
	EMOTION_CELEBRATION = app.SLOT_EMOTION_START+14
	EMOTION_LETTER = app.SLOT_EMOTION_START+15
	EMOTION_BUSY = app.SLOT_EMOTION_START+16
	EMOTION_WHIRL = app.SLOT_EMOTION_START+17

EMOTION_DICT = {
	EMOTION_CLAP :			{"name": localeInfo.EMOTION_CLAP, 		"command":"/clap"},
	EMOTION_DANCE_1 :		{"name": localeInfo.EMOTION_DANCE_1, 	"command":"/dance1"},
	EMOTION_DANCE_2 :		{"name": localeInfo.EMOTION_DANCE_2, 	"command":"/dance2"},
	EMOTION_DANCE_3 :		{"name": localeInfo.EMOTION_DANCE_3, 	"command":"/dance3"},
	EMOTION_DANCE_4 :		{"name": localeInfo.EMOTION_DANCE_4, 	"command":"/dance4"},
	EMOTION_DANCE_5 :		{"name": localeInfo.EMOTION_DANCE_5, 	"command":"/dance5"},
	EMOTION_DANCE_6 :		{"name": localeInfo.EMOTION_DANCE_6, 	"command":"/dance6"},
	EMOTION_CONGRATULATION :	{"name": localeInfo.EMOTION_CONGRATULATION,	"command":"/congratulation"},
	EMOTION_FORGIVE :		{"name": localeInfo.EMOTION_FORGIVE, 	"command":"/forgive"},
	EMOTION_ANGRY :			{"name": localeInfo.EMOTION_ANGRY, 		"command":"/angry"},
	EMOTION_ATTRACTIVE :		{"name": localeInfo.EMOTION_ATTRACTIVE, 	"command":"/attractive"},
	EMOTION_SAD :			{"name": localeInfo.EMOTION_SAD, 		"command":"/sad"},
	EMOTION_SHY :			{"name": localeInfo.EMOTION_SHY, 		"command":"/shy"},
	EMOTION_CHEERUP :		{"name": localeInfo.EMOTION_CHEERUP, 	"command":"/cheerup"},
	EMOTION_BANTER :		{"name": localeInfo.EMOTION_BANTER, 	"command":"/banter"},
	EMOTION_JOY :			{"name": localeInfo.EMOTION_JOY, 		"command":"/joy"},
	EMOTION_CHEERS_1 :		{"name": localeInfo.EMOTION_CHEERS_1, 	"command":"/cheer1"},
	EMOTION_CHEERS_2 :		{"name": localeInfo.EMOTION_CHEERS_2, 	"command":"/cheer2"},
	EMOTION_KISS :			{"name": localeInfo.EMOTION_CLAP_KISS, 	"command":"/kiss"},
	EMOTION_FRENCH_KISS :		{"name": localeInfo.EMOTION_FRENCH_KISS, 	"command":"/french_kiss"},
	EMOTION_SLAP :			{"name": localeInfo.EMOTION_SLAP, 		"command":"/slap"},
}

if app.ENABLE_EXPRESSING_EMOTION:
	command_emotion = {
		EMOTION_PUSHUP : {"name": localeInfo.EMOTION_PUSH_UP, "command":"/pushup"},
		EMOTION_DANCE_7 : {"name": localeInfo.EMOTION_DANCE_7, "command":"/dance_7"},
		EMOTION_EXERCISE : {"name": localeInfo.EMOTION_EXERCISE, "command":"/exercise"},
		EMOTION_DOZE : {"name": localeInfo.EMOTION_DOZE, "command":"/doze"},
		EMOTION_SELFIE : {"name": localeInfo.EMOTION_SELFIE, "command":"/selfie"},
		EMOTION_CHARGING : {"name": localeInfo.EMOTION_CHARGING, "command":EMOTICON_NEXT},
		EMOTION_NOSAY : {"name": localeInfo.EMOTION_NOSAY, "command":EMOTICON_NEXT+1},
		EMOTION_WEATHER_1 : {"name": localeInfo.EMOTION_WEATHER_1, "command":EMOTICON_NEXT+2},
		EMOTION_WEATHER_2 : {"name": localeInfo.EMOTION_WEATHER_2, "command":EMOTICON_NEXT+3},
		EMOTION_WEATHER_3 : {"name": localeInfo.EMOTION_WEATHER_3, "command":EMOTICON_NEXT+4},
		EMOTION_HUNGRY : {"name": localeInfo.EMOTION_HUNGRY, "command":EMOTICON_NEXT+5},
		EMOTION_SIREN : {"name": localeInfo.EMOTION_SIREN, "command":EMOTICON_NEXT+6},
		EMOTION_ALCOHOL : {"name": localeInfo.EMOTION_ALCOHOL, "command":EMOTICON_NEXT+7},
		EMOTION_CALL : {"name": localeInfo.EMOTION_CALL, "command":EMOTICON_NEXT+8},
		EMOTION_CELEBRATION : {"name": localeInfo.EMOTION_CELEBRATION, "command":EMOTICON_NEXT+9},
		EMOTION_LETTER : {"name": localeInfo.EMOTION_LETTER, "command":EMOTICON_NEXT+10},
		EMOTION_BUSY : {"name": localeInfo.EMOTION_BUSY, "command":EMOTICON_NEXT+11},
		EMOTION_WHIRL : {"name": localeInfo.EMOTION_WHIRL, "command":EMOTICON_NEXT+12},
	}

ICON_DICT = {
	EMOTION_CLAP 		: 	"d:/ymir work/ui/game/windows/emotion_clap.sub",
	EMOTION_CHEERS_1	:	"d:/ymir work/ui/game/windows/emotion_cheers_1.sub",
	EMOTION_CHEERS_2	:	"d:/ymir work/ui/game/windows/emotion_cheers_2.sub",

	EMOTION_DANCE_1		:	"icon/action/dance1.tga",
	EMOTION_DANCE_2		:	"icon/action/dance2.tga",

	EMOTION_CONGRATULATION	:	"icon/action/congratulation.tga",
	EMOTION_FORGIVE		:	"icon/action/forgive.tga",
	EMOTION_ANGRY		:	"icon/action/angry.tga",
	EMOTION_ATTRACTIVE	:	"icon/action/attractive.tga",
	EMOTION_SAD		:	"icon/action/sad.tga",
	EMOTION_SHY		:	"icon/action/shy.tga",
	EMOTION_CHEERUP		:	"icon/action/cheerup.tga",
	EMOTION_BANTER		:	"icon/action/banter.tga",
	EMOTION_JOY		:	"icon/action/joy.tga",
	EMOTION_DANCE_1		:	"icon/action/dance1.tga",
	EMOTION_DANCE_2		:	"icon/action/dance2.tga",
	EMOTION_DANCE_3		:	"icon/action/dance3.tga",
	EMOTION_DANCE_4		:	"icon/action/dance4.tga",
	EMOTION_DANCE_5		:	"icon/action/dance5.tga",
	EMOTION_DANCE_6		:	"icon/action/dance6.tga",

	EMOTION_KISS		:	"d:/ymir work/ui/game/windows/emotion_kiss.sub",
	EMOTION_FRENCH_KISS	:	"d:/ymir work/ui/game/windows/emotion_french_kiss.sub",
	EMOTION_SLAP		:	"d:/ymir work/ui/game/windows/emotion_slap.sub",
}

if app.ENABLE_EXPRESSING_EMOTION:
	ICON_DICT[EMOTION_PUSHUP] = "d:/ymir work/ui/action/pushup.tga"
	ICON_DICT[EMOTION_DANCE_7] =	"d:/ymir work/ui/action/dance7.tga"
	ICON_DICT[EMOTION_EXERCISE]	 ="d:/ymir work/ui/action/exercise.tga"
	ICON_DICT[EMOTION_DOZE]	 ="d:/ymir work/ui/action/doze.tga"
	ICON_DICT[EMOTION_SELFIE]	 ="d:/ymir work/ui/action/selfie.tga"
	ICON_DICT[EMOTION_CHARGING]	 =	"d:/ymir work/ui/action/charging.tga"
	ICON_DICT[EMOTION_NOSAY] ="d:/ymir work/ui/action/nosay.tga"
	ICON_DICT[EMOTION_WEATHER_1] ="d:/ymir work/ui/action/weather1.tga"
	ICON_DICT[EMOTION_WEATHER_2] ="d:/ymir work/ui/action/weather2.tga"
	ICON_DICT[EMOTION_WEATHER_3] ="d:/ymir work/ui/action/weather3.tga"
	ICON_DICT[EMOTION_HUNGRY] ="d:/ymir work/ui/action/hungry.tga"
	ICON_DICT[EMOTION_SIREN] ="d:/ymir work/ui/action/siren.tga"
	ICON_DICT[EMOTION_ALCOHOL] ="d:/ymir work/ui/action/alcohol.tga"
	ICON_DICT[EMOTION_CALL] ="d:/ymir work/ui/action/call.tga"
	ICON_DICT[EMOTION_CELEBRATION] ="d:/ymir work/ui/action/celebration.tga"
	ICON_DICT[EMOTION_LETTER] ="d:/ymir work/ui/action/letter.tga"
	ICON_DICT[EMOTION_BUSY] ="d:/ymir work/ui/action/busy.tga"
	ICON_DICT[EMOTION_WHIRL] ="d:/ymir work/ui/action/whirl.tga"

ANI_DICT = {
	chr.MOTION_CLAP :			"clap.msa",
	chr.MOTION_CHEERS_1 :			"cheers_1.msa",
	chr.MOTION_CHEERS_2 :			"cheers_2.msa",
	chr.MOTION_DANCE_1 :			"dance_1.msa",
	chr.MOTION_DANCE_2 :			"dance_2.msa",
	chr.MOTION_DANCE_3 :			"dance_3.msa",
	chr.MOTION_DANCE_4 :			"dance_4.msa",
	chr.MOTION_DANCE_5 :			"dance_5.msa",
	chr.MOTION_DANCE_6 :			"dance_6.msa",
	chr.MOTION_CONGRATULATION :		"congratulation.msa",
	chr.MOTION_FORGIVE :			"forgive.msa",
	chr.MOTION_ANGRY :			"angry.msa",
	chr.MOTION_ATTRACTIVE :			"attractive.msa",
	chr.MOTION_SAD :			"sad.msa",
	chr.MOTION_SHY :			"shy.msa",
	chr.MOTION_CHEERUP :			"cheerup.msa",
	chr.MOTION_BANTER :			"banter.msa",
	chr.MOTION_JOY :			"joy.msa",
	chr.MOTION_FRENCH_KISS_WITH_WARRIOR :	"french_kiss_with_warrior.msa",
	chr.MOTION_FRENCH_KISS_WITH_ASSASSIN :	"french_kiss_with_assassin.msa",
	chr.MOTION_FRENCH_KISS_WITH_SURA :	"french_kiss_with_sura.msa",
	chr.MOTION_FRENCH_KISS_WITH_SHAMAN :	"french_kiss_with_shaman.msa",
	chr.MOTION_KISS_WITH_WARRIOR :		"kiss_with_warrior.msa",
	chr.MOTION_KISS_WITH_ASSASSIN :		"kiss_with_assassin.msa",
	chr.MOTION_KISS_WITH_SURA :		"kiss_with_sura.msa",
	chr.MOTION_KISS_WITH_SHAMAN :		"kiss_with_shaman.msa",
	chr.MOTION_SLAP_HIT_WITH_WARRIOR :	"slap_hit.msa",
	chr.MOTION_SLAP_HIT_WITH_ASSASSIN :	"slap_hit.msa",
	chr.MOTION_SLAP_HIT_WITH_SURA :		"slap_hit.msa",
	chr.MOTION_SLAP_HIT_WITH_SHAMAN :	"slap_hit.msa",
	chr.MOTION_SLAP_HURT_WITH_WARRIOR :	"slap_hurt.msa",
	chr.MOTION_SLAP_HURT_WITH_ASSASSIN :	"slap_hurt.msa",
	chr.MOTION_SLAP_HURT_WITH_SURA :	"slap_hurt.msa",
	chr.MOTION_SLAP_HURT_WITH_SHAMAN :	"slap_hurt.msa",
}

if app.ENABLE_WOLFMAN_CHARACTER:
	ANI_DICT.update({
		chr.MOTION_FRENCH_KISS_WITH_WOLFMAN :	"french_kiss_with_wolfman.msa",
		chr.MOTION_KISS_WITH_WOLFMAN :			"kiss_with_wolfman.msa",
		chr.MOTION_SLAP_HIT_WITH_WOLFMAN :		"slap_hit.msa",
		chr.MOTION_SLAP_HURT_WITH_WOLFMAN :		"slap_hurt.msa",
	})

if app.ENABLE_EXPRESSING_EMOTION:
	ANI_DICT[chr.MOTION_PUSHUP] = "pushup.msa"
	ANI_DICT[chr.MOTION_PUSHUP] =	"pushup.msa"
	ANI_DICT[chr.MOTION_DANCE_7] =	"dance_7.msa"
	ANI_DICT[chr.MOTION_EXERCISE] ="exercise.msa"
	ANI_DICT[chr.MOTION_DOZE] =	"doze.msa"
	ANI_DICT[chr.MOTION_SELFIE ] =	"selfie.msa"

def RegisterEmotionIcons():
	for key, val in ICON_DICT.items():
		player.RegisterEmotionIcon(key, val)

