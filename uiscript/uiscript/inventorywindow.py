import uiScriptLocale

EQUIPMENT_START_INDEX = 90

window = {
	"name" : "InventoryWindow",

	## 600 - (width + 오른쪽으로 부터 띄우기 24 px)
	"x" : SCREEN_WIDTH - 176 - 200,
	"y" : SCREEN_HEIGHT - 37 - 565,

	"style" : ("movable", "float", "animate",),

	"width" : 176,
	"height" : 565,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 176,
			"height" : 565,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : 161,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":77, "y":3, "text":uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_2, "text_horizontal_align":"center" },
					),
				},

				## Equipment Slot
				{
					"name" : "Equipment_Base",
					"type" : "image",

					"x" : 10,
					"y" : 33,

					"image" : "d:/ymir work/ui/game/windows/equipment_base.sub",

					"children" :
					(

						{
							"name" : "EquipmentSlot",
							"type" : "slot",

							"x" : 3,
							"y" : 3,

							"width" : 150,
							"height" : 182,

							"slot" : (
										{"index":EQUIPMENT_START_INDEX+0, "x":39, "y":37, "width":32, "height":64},
										{"index":EQUIPMENT_START_INDEX+1, "x":39, "y":2, "width":32, "height":32},
										{"index":EQUIPMENT_START_INDEX+2, "x":39, "y":145, "width":32, "height":32},
										{"index":EQUIPMENT_START_INDEX+3, "x":75, "y":67, "width":32, "height":32},
										{"index":EQUIPMENT_START_INDEX+4, "x":3, "y":3, "width":32, "height":96},
										{"index":EQUIPMENT_START_INDEX+5, "x":114, "y":84, "width":32, "height":32},
										{"index":EQUIPMENT_START_INDEX+6, "x":114, "y":52, "width":32, "height":32},
										{"index":EQUIPMENT_START_INDEX+7, "x":2, "y":113, "width":32, "height":32},
										{"index":EQUIPMENT_START_INDEX+8, "x":75, "y":113, "width":32, "height":32},
										{"index":EQUIPMENT_START_INDEX+9, "x":114, "y":1, "width":32, "height":32},
										{"index":EQUIPMENT_START_INDEX+10, "x":75, "y":35, "width":32, "height":32},
									),
						},

						{
							"name" : "Equipment_Tab_01",
							"type" : "radio_button",

							"x" : 86,
							"y" : 161,

							"default_image" : "d:/ymir work/ui/game/windows/tab_button_small_01.sub",
							"over_image" : "d:/ymir work/ui/game/windows/tab_button_small_02.sub",
							"down_image" : "d:/ymir work/ui/game/windows/tab_button_small_03.sub",

							"children" :
							(
								{
									"name" : "Equipment_Tab_01_Print",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : "I",
								},
							),
						},
						{
							"name" : "Equipment_Tab_02",
							"type" : "radio_button",

							"x" : 86 + 32,
							"y" : 161,

							"default_image" : "d:/ymir work/ui/game/windows/tab_button_small_01.sub",
							"over_image" : "d:/ymir work/ui/game/windows/tab_button_small_02.sub",
							"down_image" : "d:/ymir work/ui/game/windows/tab_button_small_03.sub",

							"children" :
							(
								{
									"name" : "Equipment_Tab_02_Print",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : "II",
								},
							),
						},

					),
				},

				{
					"name" : "Inventory_Tab_01",
					"type" : "radio_button",

					"x" : 10,
					"y" : 33 + 191,

					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_02.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_03.sub",
					"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_1,

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

					"x" : 10 + 78,
					"y" : 33 + 191,

					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_02.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_03.sub",
					"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_2,

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
				
					###############################################################################################
					# RANDOMMINIMIEREN
					##Minimieren Button
					{
						"name" : "MinimierenButton",
						"type" : "button",

						"x" : 161 + SPACE_BONUS_INVENTORY - 30,
						"y" : 10,

						"default_image" : "d:/ymir work/ui/public/minimize_button_01.sub",
						"over_image" : "d:/ymir work/ui/public/minimize_button_02.sub",
						"down_image" : "d:/ymir work/ui/public/minimize_button_03.sub",
						"tooltip_text" : "Minimieren",
					},
					###################################################
					###################################################
					###################################################
					#############Bonustabelle############
					#Defensive Bonustabelle
					{
						"name" : "Defensiv",
						"type" : "horizontalbar",

						"x" : 176 - 7,
						"y" : 33,
						"width" : 125,

						"children" :
						(
							{
								"name" : "bonus_text_1",
								"type" : "text",
								"x" : 0,
								"y" : 0,
								"all_align" : "center",
								"text" : "Defensiv",
							},
						),
					},
					########################################
					{
						"name" : "Schwert",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 55,
						"text" : "Schwert:"
					},
					{
						"name" : "Schwert_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 55 - 2,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_1",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					########################################
					{
						"name" : "2Hand",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75,
						"text" : "Zweihander:"
					},
					{
						"name" : "2Hand_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 - 2,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_2",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					########################################
					{
						"name" : "Dolch",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20,
						"text" : "Dolche:"
					},
					{
						"name" : "Dolch_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_3",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					########################################
					{
						"name" : "Pfeilwiderstand",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20 + 20,
						"text" : "Pfeilwiderstand:"
					},
					{
						"name" : "Pfeilwiderstand_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2 + 20,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_4",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					########################################

					{
						"name" : "Glocke",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20,
						"text" : "Glocke:"
					},
					{
						"name" : "Glocke_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2 + 20 + 20,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_5",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					########################################
					{
						"name" : "Faecher",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20 + 20,
						"text" : "Faecher:"
					},
					{
						"name" : "Faecher_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2 + 20 + 20 + 20,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_6",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					########################################
					{
						"name" : "Magiewiederstand",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20 + 20 + 20,
						"text" : "Magiewiederst.:"
					},
					{
						"name" : "Magiewiederstand_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2 + 20 + 20 + 20 + 20,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_7",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					########################################
					{
						"name" : "Giftwiederstand",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20 + 20 + 20 + 20,
						"text" : "Giftwiederst.:"
					},
					{
						"name" : "Giftwiederstand_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2 + 20 + 20 + 20 + 20 + 20,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_8",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					########################################
					{
						"name" : "Krieger",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"text" : "Krieger:"
					},
					{
						"name" : "Krieger_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2 + 20 + 20 + 20 + 20 + 20 + 20,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_9",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					########################################
					{
						"name" : "Ninja",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"text" : "Ninja:"
					},
					{
						"name" : "Ninja_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_10",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					########################################
					{
						"name" : "Sura",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"text" : "Sura:"
					},
					{
						"name" : "Sura_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_11",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					########################################
					{
						"name" : "Schamane",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"text" : "Schamane:"
					},
					{
						"name" : "Schamane_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_12",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					###################################################
					#Offensive Bonus Tabelle
					{
						"name" : "Offensive",
						"type" : "horizontalbar",

						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"width" : 125,

						"children" :
						(
							{
								"name" : "bonus_text_2",
								"type" : "text",
								"x" : 0,
								"y" : 0,
								"all_align" : "center",
								"text" : "Offensive",
							},
						),
					},
					########################################
					{
						"name" : "Krit",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"text" : "Krit. Treffer:"
					},
					{
						"name" : "Krit_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_13",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					###################################################
					{
						"name" : "DB",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"text" : "DB. Treffer:"
					},
					{
						"name" : "DB_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_14",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					###################################################
					{
						"name" : "DSS",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"text" : "DSS:"
					},
					{
						"name" : "DSS_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_15",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					###################################################
					{
						"name" : "FKS",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"text" : "FKS:"
					},
					{
						"name" : "FKS_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_16",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					###################################################
					{
						"name" : "Halbmenschen",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"text" : "Halbmenschen:"
					},
					{
						"name" : "Halbmenschen_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_17",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					###################################################
					{
						"name" : "Untote",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"text" : "Untote:"
					},
					{
						"name" : "Untote_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_18",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					###################################################
					{
						"name" : "Teufel",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"text" : "Teufel:"
					},
					{
						"name" : "Teufel_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_19",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					###################################################
					{
						"name" : "KriegerO",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"text" : "Krieger:"
					},
					{
						"name" : "KriegerO_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_20",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					###################################################
					{
						"name" : "NinjaO",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"text" : "Ninja:"
					},
					{
						"name" : "NinjaO_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_21",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					###################################################
					{
						"name" : "SuraO",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"text" : "Sura:"
					},
					{
						"name" : "SuraO_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_22",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					###################################################
					{
						"name" : "SchamaneO",
						"type" : "text",
						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"text" : "Schamane:"
					},
					{
						"name" : "SchamaneO_info",
						"type" : "image",
						"x" : 176 + SPACE_BONUS_INVENTORY - 65,
						"y" : 75 + 20 - 2 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"image" : IMAGE_QUARESMA,
						"children" :
						(
							{
								"name" : "bonus_23",
								"type" : "text",
								"x" : 26,
								"y" : 3,
								"text" : "999",
								"r" : 1.0,
								"g" : 1.0,
								"b" : 1.0,
								"a" : 1.0,
								"text_horizontal_align":"center"
							},
						),
					},
					{
						"name" : "SERVER_NAME",
						"type" : "horizontalbar",

						"x" : 176 - 5,
						"y" : 75 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20 + 20,
						"width" : 125,

						"children" :
						(
							{
								"name" : "bonus_text_3",
								"type" : "text",
								"x" : 0,
								"y" : 0,
								"r" : 1.0,
								"g" : 0.0,
								"b" : 0.0,
								"a" : 1.0,
								"all_align" : "center",
								"text" : "Exception2",
							},
						),
					}, 

					# RANDOMMINIMIEREN
					###############################################################################################

				## Item Slot
				{
					"name" : "ItemSlot",
					"type" : "grid_table",

					"x" : 8,
					"y" : 246,

					"start_index" : 0,
					"x_count" : 5,
					"y_count" : 9,
					"x_step" : 32,
					"y_step" : 32,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub"
				},

				## Print
				{
					"name":"Money_Slot",
					"type":"button",

					"x":8,
					"y":28,

					"horizontal_align":"center",
					"vertical_align":"bottom",

					"default_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
					"over_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
					"down_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",

					"children" :
					(
						{
							"name":"Money_Icon",
							"type":"image",

							"x":-18,
							"y":20,

							"image":"d:/ymir work/ui/game/windows/money_icon.sub",
						},

						{
							"name" : "Money",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"horizontal_align" : "right",
							"text_horizontal_align" : "right",

							"text" : "123456789",
						},
					),
				},

			),
		},
	),
}
