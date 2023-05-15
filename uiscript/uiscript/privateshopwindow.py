import uiScriptLocale
import app

ROOT = "d:/ymir work/ui/game/myshop_deco/"

BOARD_WIDTH = 188
BOARD_HEIGHT = 111 + 28 * 4

window = {
	"name" : "PrivateShopWindow",

	"style" : ("movable", "float", "animate",),

	"x" : (SCREEN_WIDTH / 2) - (BOARD_WIDTH / 2),
	"y" : (SCREEN_HEIGHT / 2) - (BOARD_HEIGHT / 2),

	"width" : 185,
	"height" : 227,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 185,
			"height" : 227,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : 170,
					"color" : "yellow",

					"children" :
					(
						{ "name" : "TitleName", "type" : "text", "x" : 82, "y" : 3, "text" : "Magazzino", "text_horizontal_align" : "center" },
					),
				},

				{
					"name" : "BlackBoard",
					"type" : "thinboard_circle",

					"x" : 10,
					"y" : 37,

					"width" : 165,
					"height" : 171,

					"children" :
					(
						{
							"name" : "RemoteShopButton",
							"type" : "button",

							"x" : 8,
							"y" : 4,

							"text" : "Offline-Shop",

							"default_image" : "d:/ymir work/ui/game/myshop_deco/public_store_001.dds",
							"over_image" : "d:/ymir work/ui/game/myshop_deco/public_store_002.dds",
							"down_image" : "d:/ymir work/ui/game/myshop_deco/public_store_003.dds",
						},

						{
							"name" : "SearchShopButton",
							"type" : "button",

							"x" : 8,
							"y" : 4 + 28,

							"text" : "Search-Shop",

							"default_image" : "d:/ymir work/ui/game/myshop_deco/public_store_001.dds",
							"over_image" : "d:/ymir work/ui/game/myshop_deco/public_store_002.dds",
							"down_image" : "d:/ymir work/ui/game/myshop_deco/public_store_003.dds",
						},
					)
				},
			),
		},
	)
}
