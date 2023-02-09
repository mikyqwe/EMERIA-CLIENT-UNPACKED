import uiScriptLocale

TEMPORARY_X = +43
BUTTON_TEMPORARY_X = 5
PVP_X = -10
ROOT_PATH = "d:/ymir work/ui/public/"
LINE_LABEL_X 	= 25
LINE_DATA_X 	= 90
LINE_STEP	= 0
SMALL_BUTTON_WIDTH 	= 45
MIDDLE_BUTTON_WIDTH 	= 65
window = {
	"name" : "EfsunGor",
	"x" : 0,
	"y" : 0,
	"style" : ("movable", "float",),
	"width" : 350-50,
	"height" : 200,
	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach", "ignore_size",),
			"x" : 0,
			"y" : 0,
			"horizontal_align" : "center",
			"vertical_align" : "center",
			"width" : 350-50,
			"height" : 210,
			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),
					"x" : 6,
					"y" : 6,
					"width" : 340-50,
					"color" : "yellow",
					"children" :
					(
						{
							"name" : "TitleName",
							"type" : "text",
							"x" : 0,
							"y" : 3,
							"horizontal_align" : "center",
							"text_horizontal_align" : "center",
							"text":"Impostazioni Filtro Pick-UP",
						},
					),
				},

				{"name" : "PickupMode","type" : "text","multi_line" : 1,"x" : LINE_LABEL_X,"y" : 50+2,"text" : "Modalita'",},
				{"name" : "mode_old","type" : "toggle_button","x" : LINE_DATA_X,"y" : 50,"text" : "Normale","default_image" : ROOT_PATH + "middle_button_01.sub","over_image" : ROOT_PATH + "middle_button_02.sub","down_image" : ROOT_PATH + "middle_button_03.sub",},
				{"name" : "mode_fast","type" : "toggle_button","x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,"y" : 50,"text" : "Veloce","default_image" : ROOT_PATH + "middle_button_01.sub","over_image" : ROOT_PATH + "middle_button_02.sub","down_image" : ROOT_PATH + "middle_button_03.sub",},

				{"name" : "PickupAutoMode","type" : "text","multi_line" : 1,"x" : LINE_LABEL_X,"y" : 75+2,"text" : "Automatico:",},
				{"name" : "mode_auto_deactive","type" : "toggle_button","x" : LINE_DATA_X,"y" : 75,"text" : "Off","default_image" : ROOT_PATH + "middle_button_01.sub","over_image" : ROOT_PATH + "middle_button_02.sub","down_image" : ROOT_PATH + "middle_button_03.sub",},
				{"name" : "mode_auto_active","type" : "toggle_button","x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,"y" : 75,"text" : "On","default_image" : ROOT_PATH + "middle_button_01.sub","over_image" : ROOT_PATH + "middle_button_02.sub","down_image" : ROOT_PATH + "middle_button_03.sub",},


				{"name" : "PickUpFilter","type" : "text","multi_line" : 1,"x" : LINE_LABEL_X,"y" : 100+2,"text" : "Filtri:",},
				{"name" : "filter_weapon","type" : "toggle_button","x" : LINE_DATA_X,"y" : 100,"text" : "Armi","default_image" : ROOT_PATH + "middle_button_01.sub","over_image" : ROOT_PATH + "middle_button_02.sub","down_image" : ROOT_PATH + "middle_button_03.sub",},
				{"name" : "filter_armor","type" : "toggle_button","x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,"y" : 100,"text" : "Armature","default_image" : ROOT_PATH + "middle_button_01.sub","over_image" : ROOT_PATH + "middle_button_02.sub","down_image" : ROOT_PATH + "middle_button_03.sub",},
				{"name" : "filter_ear","type" : "toggle_button","x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*2,"y" : 100,"text" : "Orecchini","default_image" : ROOT_PATH + "middle_button_01.sub","over_image" : ROOT_PATH + "middle_button_02.sub","down_image" : ROOT_PATH + "middle_button_03.sub",},
				{"name" : "filter_neck","type" : "toggle_button","x" : LINE_DATA_X,"y" : 125,"text" : "Collane","default_image" : ROOT_PATH + "middle_button_01.sub","over_image" : ROOT_PATH + "middle_button_02.sub","down_image" : ROOT_PATH + "middle_button_03.sub",},
				{"name" : "filter_foots","type" : "toggle_button","x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,"y" : 125,"text" : "Scarpe","default_image" : ROOT_PATH + "middle_button_01.sub","over_image" : ROOT_PATH + "middle_button_02.sub","down_image" : ROOT_PATH + "middle_button_03.sub",},
				{"name" : "filter_shield","type" : "toggle_button","x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*2,"y" : 125,"text" : "Scudi","default_image" : ROOT_PATH + "middle_button_01.sub","over_image" : ROOT_PATH + "middle_button_02.sub","down_image" : ROOT_PATH + "middle_button_03.sub",},
				{"name" : "filter_head","type" : "toggle_button","x" : 90,"y" : 175,"text" : "Elmi","default_image" : ROOT_PATH + "middle_button_01.sub","over_image" : ROOT_PATH + "middle_button_02.sub","down_image" : ROOT_PATH + "middle_button_03.sub",},
				{"name" : "filter_wrist","type" : "toggle_button","x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*2,"y" : 150,"text" : "Bracciali","default_image" : ROOT_PATH + "middle_button_01.sub","over_image" : ROOT_PATH + "middle_button_02.sub","down_image" : ROOT_PATH + "middle_button_03.sub",},
				{"name" : "filter_book","type" : "toggle_button","x" : LINE_DATA_X,"y" : 150,"text" : "Libri","default_image" : ROOT_PATH + "middle_button_01.sub","over_image" : ROOT_PATH + "middle_button_02.sub","down_image" : ROOT_PATH + "middle_button_03.sub",},
				{"name" : "filter_stone","type" : "toggle_button","x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH,"y" : 150,"text" : "Pietre","default_image" : ROOT_PATH + "middle_button_01.sub","over_image" : ROOT_PATH + "middle_button_02.sub","down_image" : ROOT_PATH + "middle_button_03.sub",},
				{"name" : "filter_etc","type" : "toggle_button","x" : LINE_DATA_X+MIDDLE_BUTTON_WIDTH*2,"y" : 150,"text" : "Generico","default_image" : ROOT_PATH + "middle_button_01.sub","over_image" : ROOT_PATH + "middle_button_02.sub","down_image" : ROOT_PATH + "middle_button_03.sub",},
			),
		},
	),
}
