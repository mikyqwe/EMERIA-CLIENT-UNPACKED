import uiScriptLocale
import app

ROOT = "d:/ymir work/ui/game/myshop_deco/"

BOARD_WIDTH = 188
BOARD_HEIGHT = 111 + 28 * 4

window = {
	"name" : "InventoryMenu",

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
							"name" : "SafeBox",
							"type" : "button",

							"x" : 8,
							"y" : 4,

							"text" : "Magazzino",

							"default_image" : "d:/ymir work/ui/game/myshop_deco/public_store_001.dds",
							"over_image" : "d:/ymir work/ui/game/myshop_deco/public_store_002.dds",
							"down_image" : "d:/ymir work/ui/game/myshop_deco/public_store_003.dds",
						},

						{
							"name" : "ItemShop",
							"type" : "button",

							"x" : 8,
							"y" : 4 + 28,

							"text" : "Item-Shop",

							"default_image" : "d:/ymir work/ui/game/myshop_deco/public_store_001.dds",
							"over_image" : "d:/ymir work/ui/game/myshop_deco/public_store_002.dds",
							"down_image" : "d:/ymir work/ui/game/myshop_deco/public_store_003.dds",
						},

						# {
							# "name" : "SkillBook_Storage",
							# "type" : "button",

							# "x" : 8,
							# "y" : 4 + 28 + 28,

							# "text" : "Libri",

							# "default_image" : "d:/ymir work/ui/game/myshop_deco/public_store_001.dds",
							# "over_image" : "d:/ymir work/ui/game/myshop_deco/public_store_002.dds",
							# "down_image" : "d:/ymir work/ui/game/myshop_deco/public_store_003.dds",
						# },
						# {
							# "name" : "UppItem_Storage",
							# "type" : "button",
							# "x" : 8,
							# "y" : 4 + 28 + 28 + 28,

							# "text" : "Item Up",

							# "default_image" : "d:/ymir work/ui/game/myshop_deco/public_store_001.dds",
							# "over_image" : "d:/ymir work/ui/game/myshop_deco/public_store_002.dds",
							# "down_image" : "d:/ymir work/ui/game/myshop_deco/public_store_003.dds",
						# },
						# {
							# "name" : "GhostStone_Storage",
							# "type" : "button",

							# "x" : 8,
							# "y" : 4 + 28 + 28 + 28 + 28,

							# "text" : "Pietre",

							# "default_image" : "d:/ymir work/ui/game/myshop_deco/public_store_001.dds",
							# "over_image" : "d:/ymir work/ui/game/myshop_deco/public_store_002.dds",
							# "down_image" : "d:/ymir work/ui/game/myshop_deco/public_store_003.dds",
						# },
						{
							"name" : "General_Storage",
							"type" : "button",

							"x" : 8,
							"y" : 4 + 28 + 28,

							"text" : "Generale",

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
