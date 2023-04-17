import uiScriptLocale

MAINBOARD_WIDTH = 247
MAINBOARD_HEIGHT = 405

IMG_DIR = "d:/ymir work/ui/game/characterdetails/"

window = {
	"name" : "CharacterDetailsWindow",
	"style" : ("float","animate",),
	"x" : 274,
	"y" : (SCREEN_HEIGHT - 398) / 2,
	"width" : MAINBOARD_WIDTH,
	"height" : MAINBOARD_HEIGHT,
	"children" :
	(
		{
			"name" : "MainBoard",
			"type" : "board",
			"x" : 0,
			"y" : 0,
			"width" : MAINBOARD_WIDTH,
			"height" : MAINBOARD_HEIGHT,
			"children" :
			(
				{
					"name" : "bonus_button",
					"type" : "radio_button",
					"x" : 16,
					"y" : 10,
					"text" : "Riepilogo Bonus",
					"default_image" :IMG_DIR+"btn_0.tga",
					"over_image" :IMG_DIR+"btn_0.tga",
					"down_image" :IMG_DIR+"btn_1.tga",
				},
				{
					"name" : "stat_button",
					"type" : "radio_button",
					"x" : 130,
					"y" : 10,
					"text" : "Statistiche",
					"default_image" :IMG_DIR+"btn_0.tga",
					"over_image" :IMG_DIR+"btn_0.tga",
					"down_image" :IMG_DIR+"btn_1.tga",
				},
				{
					"name" : "bonus_window",
					"type" : "image",
					"x" : 10,
					"y" : 10+25,
					"image" :IMG_DIR+"bonus_bg.tga",
				},
				{
					"name" : "stat_window",
					"type" : "image",
					"x" : 10,
					"y" : 10+25,
					"image" :IMG_DIR+"log_bg.tga",
				},
			),
		},
	),
}
