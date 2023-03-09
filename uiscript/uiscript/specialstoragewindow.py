import uiScriptLocale
import app

window = {
	"name" : "SpecialStorageWindow",

	"x" : SCREEN_WIDTH - 500,
	"y" : SCREEN_HEIGHT - 37 - 565,

	"style" : ("movable", "float", "animate",),

	"width" : 184,
	"height" : 350 + 32 + 30,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 184,
			"height" : 350 + 32 + 30,

			"children" :
			(
				## Separate
				#{
				#	"name" : "SeparateBaseImage",
				#	"type" : "image",
				#	"style" : ("attach",),
				#
				#	"x" : 8,
				#	"y" : 8,
				#
				#	"image" : "d:/ymir work/ui/pattern/titlebar_inv_refresh_baseframe.tga",
				#
				#	"children" :
				#	(
				#		## Separate Button (38 x 24)
				#		{
				#			"name" : "SeparateButton",
				#			"type" : "button",
				#
				#			"x" : 11,
				#			"y" : 3,
				#
				#			"tooltip_text" : "Sort Inventory",
				#
				#			"default_image" : "d:/ymir work/ui/game/inventory/refresh_small_button_01.sub",
				#			"over_image" : "d:/ymir work/ui/game/inventory/refresh_small_button_02.sub",
				#			"down_image" : "d:/ymir work/ui/game/inventory/refresh_small_button_03.sub",
				#			"disable_image" : "d:/ymir work/ui/game/inventory/refresh_small_button_04.sub",
				#		},
				#	),
				#},

				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8 ,#+ 38, ## 38 is the width of the new sort button -> Move the titlebard to the right
					"y" : 8,

					"width" : 169 ,#- 38, ## 38 is the width of the new sort button -> Decrease the width of the titlebar
					"color" : "gray",

					"children" :
					(
						# Without Sort Inventory Button
						# { "name" : "TitleName", "type" : "text", "x" : 84, "y" : 4, "text" : "Storages", "text_horizontal_align" : "center", "horizontal_align" : "center" },

						# With Sort Inventory Button
						{ "name" : "TitleName", "type" : "text", "x" : -4, "y" : 4, "text" : "Depozit", "text_horizontal_align" : "center", "horizontal_align" : "center" },
					),
				},

				## Item Slot
				{
					"name" : "ItemSlot",
					"type" : "grid_table",

					"x" : 12,
					"y" : 34,

					"start_index" : 0,

					"x_count" : 5,
					"y_count" : 9,

					"x_step" : 32,
					"y_step" : 32,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub",
				},

				{
					"name" : "Inventory_Tab_01",
					"type" : "radio_button",

					"x" : 16,
					"y" : 295 + 32,

					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",

					"children" :
					(
						{
							"name" : "Inventory_Tab_01_Print",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "I",
						},
					),
				},
				{
					"name" : "Inventory_Tab_02",
					"type" : "radio_button",

					"x" : 16 + 40,
					"y" : 295 + 32,

					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",

					"children" :
					(
						{
							"name" : "Inventory_Tab_02_Print",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "II",
						},
					),
				},
				{
					"name" : "Inventory_Tab_03",
					"type" : "radio_button",

					"x" : 16 + 40 + 40,
					"y" : 295 + 32,

					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",

					"children" :
					(
						{
							"name" : "Inventory_Tab_03_Print",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "III",
						},
					),
				},
				{
					"name" : "Inventory_Tab_04",
					"type" : "radio_button",

					"x" : 16 + 40 + 40 + 40,
					"y" : 295 + 32,

					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",

					"children" :
					(
						{
							"name" : "Inventory_Tab_04_Print",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "IV",
						},
					),
				},

				{
					"name" : "Category_Tab_01",
					"type" : "radio_button",

					"x" : 12,
					"y" : 295 + 32 + 35,

					"tooltip_text" : "|cffF4B418Libri",

					"default_image" : "d:/ymir work/ui/special_storage_buttons/skillbook_inventory_button.tga",
					"over_image" : "d:/ymir work/ui/special_storage_buttons/skillbook_inventory_button_over.tga",
					"down_image" : "d:/ymir work/ui/special_storage_buttons/skillbook_inventory_button_down.tga",
				},

				{
					"name" : "Category_Tab_02",
					"type" : "radio_button",

					"x" : 12 + 40,
					"y" : 295 + 32 + 35,

					"tooltip_text" : "|cffF4B418Item-Up",

					"default_image" : "d:/ymir work/ui/special_storage_buttons/upgrade_inventory_button.tga",
					"over_image" : "d:/ymir work/ui/special_storage_buttons/upgrade_inventory_button_over.tga",
					"down_image" : "d:/ymir work/ui/special_storage_buttons/upgrade_inventory_button_down.tga",
				},

				{
					"name" : "Category_Tab_03",
					"type" : "radio_button",

					"x" : 12 + 40 + 40,
					"y" : 295 + 32 + 35,

					"tooltip_text" : "|cffF4B418Pietre",

					"default_image" : "d:/ymir work/ui/special_storage_buttons/ghoststone_inventory_button.tga",
					"over_image" : "d:/ymir work/ui/special_storage_buttons/ghoststone_inventory_button_over.tga",
					"down_image" : "d:/ymir work/ui/special_storage_buttons/ghoststone_inventory_button_down.tga",
				},

				{
					"name" : "Category_Tab_04",
					"type" : "radio_button",

					"x" : 12 + 40 + 40 + 40,
					"y" : 295 + 32 + 35,

					"tooltip_text" : "|cffF4B418Generico",

					"default_image" : "d:/ymir work/ui/special_storage_buttons/general_inventory_button.tga",
					"over_image" : "d:/ymir work/ui/special_storage_buttons/general_inventory_button_over.tga",
					"down_image" : "d:/ymir work/ui/special_storage_buttons/general_inventory_button_down.tga",
				},
			),
		},
	),
}
