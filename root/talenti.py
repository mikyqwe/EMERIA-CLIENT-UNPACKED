import localeInfo
import player
import chrmgr
import chr

SPECIAL_STAT_1 = 1
SPECIAL_STAT_2 = 2
SPECIAL_STAT_3 = 3
SPECIAL_STAT_4 = 4
SPECIAL_STAT_5 = 5
SPECIAL_STAT_6 = 6

SPECIAL_STAT_1_DESC = "Creºte ºansa de succes +%d%%."
SPECIAL_STAT_2_DESC = "Vitezã de miºcare +%d%%. Vitezã de atac +%d%%."
SPECIAL_STAT_3_DESC = "Max. PV +%d. Puternic împotriva monºtrilor +%d%%."
SPECIAL_STAT_4_DESC = "Vitezã de miºcare +%d. ªansa unei lovituri critice +%d%%."
SPECIAL_STAT_5_DESC = "Mãreºte ºansa de a dropa un item +%d%%. iar YANG a crescut cu +%d%%."
SPECIAL_STAT_6_DESC = "Tare vs Razboinic +%d%%. Tare vs Ninja +%d%%. Tare vs Sura +%d%%. tare vs Shaman +%d%%."


SPECIAL_STAT_1_LONG_DESC = "Cre?te norocul general la upgrade-uri. Una dintre cele mai importante aptitudini."
SPECIAL_STAT_2_LONG_DESC = "Mãre?te viteza de miscare ?i viteza de atac."
SPECIAL_STAT_3_LONG_DESC = "Cre?te-?i PV ?i capacitatea de a te lupta cu mon?tri."
SPECIAL_STAT_4_LONG_DESC = "Î?i mãre?te puterea de atac ?i loviturã criticã."
SPECIAL_STAT_5_LONG_DESC = "Mãre?te ?ansa de a dropa un item ?i de a ob?ine mai mult yang de la mon?tri."
SPECIAL_STAT_6_LONG_DESC = "Cre?te-?i capacitatea de duel împotriva tuturor raselor."

SPECIALSTATS_DICT = {
	SPECIAL_STAT_1 :		{"name": localeInfo.SPECIAL_STAT_1, "desc": SPECIAL_STAT_1_DESC, "longdesc" : SPECIAL_STAT_1_LONG_DESC},
	SPECIAL_STAT_2 :		{"name": localeInfo.SPECIAL_STAT_2, "desc": SPECIAL_STAT_2_DESC, "longdesc" : SPECIAL_STAT_2_LONG_DESC},
	SPECIAL_STAT_3 :		{"name": localeInfo.SPECIAL_STAT_3, "desc": SPECIAL_STAT_3_DESC, "longdesc" : SPECIAL_STAT_3_LONG_DESC},
	SPECIAL_STAT_4 :		{"name": localeInfo.SPECIAL_STAT_4, "desc": SPECIAL_STAT_4_DESC, "longdesc" : SPECIAL_STAT_4_LONG_DESC},
	SPECIAL_STAT_5 :		{"name": localeInfo.SPECIAL_STAT_5, "desc": SPECIAL_STAT_5_DESC, "longdesc" : SPECIAL_STAT_5_LONG_DESC},
	SPECIAL_STAT_6 :		{"name": localeInfo.SPECIAL_STAT_6, "desc": SPECIAL_STAT_6_DESC, "longdesc" : SPECIAL_STAT_6_LONG_DESC},
}

ICON_DICT = {
	SPECIAL_STAT_1	: 	"d:/ymir work/ui/talenti/fortuna_stat.sub",
	SPECIAL_STAT_2	:	"d:/ymir work/ui/talenti/agilita_stat.sub",
	SPECIAL_STAT_3	:	"d:/ymir work/ui/talenti/carisma_stat.sub",
	SPECIAL_STAT_4	:	"d:/ymir work/ui/talenti/tenacia_stat.sub",
	SPECIAL_STAT_5	:	"d:/ymir work/ui/talenti/avidita_stat.sub",
	SPECIAL_STAT_6	:	"d:/ymir work/ui/talenti/ferocia_stat.sub"
}

SPECIALSTATS_SKILL_DICT = {
	1 : [1],
	2 : [2, 1],
	3 : [100, 1],
	4 : [10, 1],
	5 : [1, 2],
	6 : [1, 1, 1, 1]
	
}

def getParamInfo(slotIndex, skillLevel):
	return tuple([skillLevel * i for i in SPECIALSTATS_SKILL_DICT[slotIndex]])
	
	
def RegisterSpecialStasIcons():
	for key, val in ICON_DICT.items():
		player.RegisterSpecialStatIcon(key, val)