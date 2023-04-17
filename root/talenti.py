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

SPECIAL_STAT_1_DESC = "Aumenta la probabilita di successo +%d%%."
SPECIAL_STAT_2_DESC = "Velocita movimento +%d%%. Velocita attacco +%d%%."
SPECIAL_STAT_3_DESC = "Aumento HP +%d. Forte contro mostri +%d%%."
SPECIAL_STAT_4_DESC = "Velocita di movimento +%d. Possibilita di colpo critico +%d%%."
SPECIAL_STAT_5_DESC = "Aumenta probabilita di droppare un oggetto +%d%%. e YANG maggiorato del +%d%%."
SPECIAL_STAT_6_DESC = "Forte vs Guerrieri +%d%%. Forte vs Ninja +%d%%. Forte vs Sura +%d%%. Forte vs Shamani +%d%%."


SPECIAL_STAT_1_LONG_DESC = "Aumenta la fortuna generale, principalmente negli upgrade. Una delle abilita piu importanti."
SPECIAL_STAT_2_LONG_DESC = "Aumenta la velocita di movimento e di attacco."
SPECIAL_STAT_3_LONG_DESC = "Aumenta la tua vita e la tua abilita nel fronteggiare mostri."
SPECIAL_STAT_4_LONG_DESC = "Aumenta il tuo attacco e la capacita di effettuare un colpo critico."
SPECIAL_STAT_5_LONG_DESC = "Aumenta la possibilita di droppare un oggetto e ricevi piu yang dai mostri."
SPECIAL_STAT_6_LONG_DESC = "Aumenta la tua capacita in duello contro tutte le razze."

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