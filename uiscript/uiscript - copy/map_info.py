import localeInfo

ROOT_PATH = "d:/ymir work/ui/game/dungeontimer/"
MOB_NAME = "devil_"
SUB = 1

FILE = "sub"
if SUB ==0:
	FILE = "png"

window = {
	"name" : "DevilFloorInfo",

	"x" : SCREEN_WIDTH - 136,
	"y" : 0,

	"width" : 136,
	"height" : 161,

	"children" :
	(
		{
			"name" : "FloorInfoBG",
			"type" : "image",
			"x" : 0,
			"y" : 0,
			"image" : ROOT_PATH+MOB_NAME+"back."+FILE,
		},
		{
			"name" : "CoolTime",
			"type" : "expanded_image",
			"x" : 8,
			"y" : 18,
			"image" : ROOT_PATH+MOB_NAME+"timer."+FILE,
		},

		{ "name":"LeftTime", "type":"text", "x":72, "y":75, "text" : "11:11", "text_horizontal_align":"center" },
		{ "name":"CurrentFloor", "type":"text", "x":72, "y":50, "text" : "1", "text_horizontal_align":"center", "r" : 1.0, "g" : 0.831, "b" : 0.043, "a" : 1.0, "fontsize":"LARGE"},
	),
}
