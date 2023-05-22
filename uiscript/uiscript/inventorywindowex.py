import uiScriptLocale
import item
import app

import player
EQUIPMENT_START_INDEX = player.EQUIPMENT_SLOT_START
SPACE_BONUS_INVENTORY = 0 # Da verificare
IMAGE_QUARESMA = "d:/ymir work/ui/public/Parameter_Slot_01.sub"
COSTUME_START_INDEX = item.COSTUME_SLOT_START
NEW_EQUIPMENT_START_INDEX = item.NEW_EQUIPMENT_SLOT_START

window = {
	"name" : "InventoryWindow",

	## 600 - (width + 오른쪽으로 부터 띄우기 24 px)
	"x" : SCREEN_WIDTH - 176,
	"y" : SCREEN_HEIGHT - 37 - 565,

	"style" : ("movable", "float",),

	"width" : 176,
	"height" : 565,

	"children" :
	(
		## Inventory, Equipment Slots
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
						{ "name":"TitleName", "type":"text", "x": -4, "y":3, "text":uiScriptLocale.INVENTORY_TITLE, "text_horizontal_align":"center", "horizontal_align" : "center" },
						#{ "name":"TitleName", "type":"text", "x": -4, "y":3, "text":uiScriptLocale.INVENTORY_TITLE, "text_horizontal_align":"center", "horizontal_align" : "center" },
					),
				},			

				## Equipment Slot
				{
					"name" : "Equipment_Base",
					"type" : "expanded_image",

					"x" : 10,
					"y" : 33,

					"image" : "invent/inventar1.png",

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
									{"index":EQUIPMENT_START_INDEX+0, "x":39, "y":37, "width":32, "height":64},#body armor
									{"index":EQUIPMENT_START_INDEX+1, "x":39, "y":2, "width":32, "height":32},#head
									{"index":EQUIPMENT_START_INDEX+2, "x":39, "y":145, "width":32, "height":32},#boots
									{"index":EQUIPMENT_START_INDEX+3, "x":75, "y":67, "width":32, "height":32},#barclet
									{"index":EQUIPMENT_START_INDEX+4, "x":3, "y":3, "width":32, "height":96},#weapon
									{"index":EQUIPMENT_START_INDEX+5, "x":114, "y":68, "width":32, "height":32},#neck
									{"index":EQUIPMENT_START_INDEX+6, "x":114, "y":36, "width":32, "height":32},#earring
									{"index":EQUIPMENT_START_INDEX+9, "x":114, "y":2, "width":32, "height":32},#arrow
									{"index":EQUIPMENT_START_INDEX+10, "x":75, "y":35, "width":32, "height":32},#shield
									{"index": COSTUME_START_INDEX+4, "x":39, "y":106, "width":32, "height":32},#belt
									
									),
						},
						
						# ALCHIMIE
						{
							"name" : "DSSButton",
							"type" : "button",

							"x" : 115,
							"y" : 108,

							"tooltip_text" : uiScriptLocale.TASKBAR_DRAGON_SOUL,

							"default_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_01.tga",
							"over_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_02.tga",
							"down_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_03.tga",
						},

						## LagerButton
						{
							"name" : "LagerButton",
							"type" : "button",

							"x" : 118,
							"y" : 147,

							"tooltip_text" : uiScriptLocale.LAGER_TITLE,

							"default_image" : "d:/ymir work/ui/game/taskbar/mall_button_01.tga",
							"over_image" : "d:/ymir work/ui/game/taskbar/mall_button_02.tga",
							"down_image" : "d:/ymir work/ui/game/taskbar/mall_button_03.tga",
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


				# Equipment Secondary Page
				{
					"name" : "Equipment_Page_Secondary",
					"type" : "expanded_image",

					"x" : 10,
					"y" : 33,

					"image" : "invent/inventar2.png",
					
					"children" :
					(
						{
							"name" : "Equipment_Slot_Secondary",
							"type" : "slot",

							"x" : 0,
							"y" : 0,

							"width" : 155,
							"height" : 187,

							"slot" : (
										{"index":EQUIPMENT_START_INDEX+7, "x":10, "y":21, "width":32, "height":32},#unique_1
										{"index":EQUIPMENT_START_INDEX+8, "x":62, "y":21, "width":32, "height":32},#unique_2
										{"index":205, "x":62 + 50, "y":21, "width":32, "height":32},#aura
										{"index":206, "x":35, "y":75, "width":32, "height":32},#ring_new
										{"index":207, "x":86, "y":75, "width":32, "height":32},#ring_new
										{"index":208, "x":86, "y":129, "width":32, "height":32},#ring_new
										{"index":209, "x":35, "y":129, "width":32, "height":32},#ring_new
										
									),
						},
					),
				},
				
				
				# Equipment Cosmetics Page
				{
					"name" : "Equipment_Page_Cosmetics",
					"type" : "expanded_image",

					"x" : 10,
					"y" : 33,

					"image" : "invent/inventar3.png",
					
					"children" :
					(
						{
							"name" : "Equipment_Slot_Cosmetics",
							"type" : "slot",

							"x" : 0,
							"y" : 0,

							"width" : 155,
							"height" : 187,

							"slot" : (
										{"index": COSTUME_START_INDEX+0, "x": 108-52+7, "y": 6+45+51-35, "width": 32, "height": 64 },#costume_body
										{"index": COSTUME_START_INDEX+1, "x": 108-52+7, "y": 6+45-11, "width": 32, "height": 32 },#costume_hair
										{"index": COSTUME_START_INDEX+3, "x": 108+3, "y": 114-102+20, "width": 32, "height": 32 },#sash
										{"index": COSTUME_START_INDEX+2, "x": 108+3, "y": 114-102+76, "width": 32, "height": 32 },#mount
										{"index": 217, "x": 108+3, "y": 114-102+112, "width": 32, "height": 32 },#pet
									
										{"index":COSTUME_START_INDEX+5, "x":13, "y":13+58-9, "width":32, "height":32},#weapon costume
									
									),
						},

					),
				},

				# Equipment Cosmetics Page
				{
					"name" : "Equipment_Page_Talismans",
					"type" : "expanded_image",

					"x" : 10,
					"y" : 33,

					"image" : "invent/inventar4.png",
					
					"children" :
					(
						{
							"name" : "talizmaneffect1",
							"type" : "slot",
							"x" : 2+11+114-20+7-9,
							"y" : 106+2-70+9-7,
							"width" : 0,
							"height" : 0,
							"slot" : ( {"index":0, "x":0, "y":0, "width":32, "height":32}, ),
						},
						{
							"name" : "talizmaneffect2",
							"type" : "slot",
							"x" : 2+11-9,
							"y" : 106+2-70+9-7,
							"width" : 0,
							"height" : 0,
							"slot" : ( {"index":0, "x":0, "y":0, "width":32, "height":32}, ),
						},
						{
							"name" : "talizmaneffect3",
							"type" : "slot",
							"x" : 2+11+114-20+7-9,
							"y" : 106+2-7,
							"width" : 0,
							"height" : 0,
							"slot" : ( {"index":0, "x":0, "y":0, "width":32, "height":32}, ),
						},
						{
							"name" : "talizmaneffect4",
							"type" : "slot",
							"x" : 2+11-9,
							"y" : 106+2-7,
							"width" : 0,
							"height" : 0,
							"slot" : ( {"index":0, "x":0, "y":0, "width":32, "height":32}, ),
						},
						{
							"name" : "talizmaneffect5",
							"type" : "slot",
							"x" : 2+11+57-6-9,
							"y" : 106+2-110+13-7,
							"width" : 0,
							"height" : 0,
							"slot" : ( {"index":0, "x":0, "y":0, "width":32, "height":32}, ),
						},
						{
							"name" : "talizmaneffect6",
							"type" : "slot",
							"x" : 2+11+57-6-9,
							"y" : 106+2+43-7-7,
							"width" : 0,
							"height" : 0,
							"slot" : ( {"index":0, "x":0, "y":0, "width":32, "height":32}, ),
						},
						{
							"name" : "Equipment_Slot_Talismans",
							"type" : "slot",

							"x" : 0,
							"y" : 0,

							"width" : 155,
							"height" : 187,

							"slot" : (
										{"index":210, "x":2+11+114-20+7, "y":106+2-70+9, "width":32, "height":32},#fire talisman
										{"index":211, "x":2+11, "y":106+2-70+9, "width":32, "height":32},#wind talisman
										{"index":212, "x":2+11+114-20+7, "y":106+2, "width":32, "height":32},#dark talisman
										{"index":213, "x":2+11, "y":106+2, "width":32, "height":32},#earth talisman
										{"index":214, "x":2+11+57-6, "y":106+2-110+13, "width":32, "height":32},#ice talisman
										{"index":215, "x":2+11+57-6, "y":106+2+43-7, "width":32, "height":32},#lighting talisman
									),
							"children" :
							(
								{
									"name" : "talisman_info_btn",
									"type" : "button",
									"x" : ((155 - 17) / 2)+2,
									"y" : ((187 - 17) / 2),
									"default_image" : "d:/ymir work/ui/pattern/q_mark_01.tga",
									"over_image" : "d:/ymir work/ui/pattern/q_mark_02.tga",
									"down_image" : "d:/ymir work/ui/pattern/q_mark_01.tga",
								},
							),
						},

					),
				},
				{
					"name" : "Inventory_Tab_01",
					"type" : "radio_button",

					"x" : 13,
					"y" : 33 + 191,

					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
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

					#"x" : 10 + 78,
					"x" : 10 + 39,
					"y" : 33 + 191,

					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
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
				
				{
					"name" : "Inventory_Tab_03",
					"type" : "radio_button",

					"x" : 10 + 39 + 39,
					"y" : 33 + 191,

					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
					
					"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_3,

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

					"x" : 10 + 39 + 39 + 39,
					"y" : 33 + 191,

					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
					"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_4,
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

				#{
				#	"name":"cover_open_0",
				#	"type":"button",
				#	"vertical_align":"bottom",
				#	
				#	"x":8,
				#	"y":339 - 42,
				#
				#	"default_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#	"over_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#	"down_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#},
				#{
				#	"name":"cover_close_0",
				#	"type":"image",
				#	"vertical_align":"bottom",
				#	
				#	"x":8,
				#	"y":339 - 42,
				#
				#	"image":"d:/ymir work/ui/ex_inven_cover_button_close.sub",
				#},
				#{
				#	"name":"cover_open_1",
				#	"type":"button",
				#	"vertical_align":"bottom",
				#	
				#	"x":8,
				#	"y":339 - 42 - 32,
				#
				#	"default_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#	"over_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#	"down_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#},
				#{
				#	"name":"cover_close_1",
				#	"type":"image",
				#	"vertical_align":"bottom",
				#	
				#	"x":8,
				#	"y":339 - 42 - 32,
				#
				#	"image":"d:/ymir work/ui/ex_inven_cover_button_close.sub",
				#},
				#{
				#	"name":"cover_open_2",
				#	"type":"button",
				#	"vertical_align":"bottom",
				#	
				#	"x":8,
				#	"y":339 - 42 - 64,
				#
				#	"default_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#	"over_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#	"down_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#},
				#{
				#	"name":"cover_close_2",
				#	"type":"image",
				#	"vertical_align":"bottom",
				#	
				#	"x":8,
				#	"y":339 - 42 - 64,
				#
				#	"image":"d:/ymir work/ui/ex_inven_cover_button_close.sub",
				#},
				#{
				#	"name":"cover_open_3",
				#	"type":"button",
				#	"vertical_align":"bottom",
				#	
				#	"x":8,
				#	"y":339 - 42 - 96,
				#
				#	"default_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#	"over_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#	"down_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#},
				#{
				#	"name":"cover_close_3",
				#	"type":"image",
				#	"vertical_align":"bottom",
				#	
				#	"x":8,
				#	"y":339 - 42 - 96,
				#
				#	"image":"d:/ymir work/ui/ex_inven_cover_button_close.sub",
				#},
				#{
				#	"name":"cover_open_4",
				#	"type":"button",
				#	"vertical_align":"bottom",
				#	
				#	"x":8,
				#	"y":339 - 42 - 128,
				#
				#	"default_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#	"over_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#	"down_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#},
				#{
				#	"name":"cover_close_4",
				#	"type":"image",
				#	"vertical_align":"bottom",
				#	
				#	"x":8,
				#	"y":339 - 42 - 128,
				#
				#	"image":"d:/ymir work/ui/ex_inven_cover_button_close.sub",
				#},
				#{
				#	"name":"cover_open_5",
				#	"type":"button",
				#	"vertical_align":"bottom",
				#	
				#	"x":8,
				#	"y":339 - 42 - 160,
				#
				#	"default_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#	"over_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#	"down_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#},
				#{
				#	"name":"cover_close_5",
				#	"type":"image",
				#	"vertical_align":"bottom",
				#	
				#	"x":8,
				#	"y":339 - 42 - 160,
				#
				#	"image":"d:/ymir work/ui/ex_inven_cover_button_close.sub",
				#},
				#{
				#	"name":"cover_open_6",
				#	"type":"button",
				#	"vertical_align":"bottom",
				#	
				#	"x":8,
				#	"y":339 - 42 - 192,
				#
				#	"default_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#	"over_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#	"down_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#},
				#{
				#	"name":"cover_close_6",
				#	"type":"image",
				#	"vertical_align":"bottom",
				#	
				#	"x":8,
				#	"y":339 - 42 - 192,
				#
				#	"image":"d:/ymir work/ui/ex_inven_cover_button_close.sub",
				#},
				#{
				#	"name":"cover_open_7",
				#	"type":"button",
				#	"vertical_align":"bottom",
				#	
				#	"x":8,
				#	"y":339 - 42 - 224,
				#
				#	"default_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#	"over_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#	"down_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#},
				#{
				#	"name":"cover_close_7",
				#	"type":"image",
				#	"vertical_align":"bottom",
				#	
				#	"x":8,
				#	"y":339 - 42 - 224,
				#
				#	"image":"d:/ymir work/ui/ex_inven_cover_button_close.sub",
				#},
				#{
				#	"name":"cover_open_8",
				#	"type":"button",
				#	"vertical_align":"bottom",
				#	
				#	"x":8,
				#	"y":339 - 42 - 256,
				#
				#	"default_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#	"over_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#	"down_image":"d:/ymir work/ui/ex_inven_cover_button_open.sub",
				#},
				#{
				#	"name":"cover_close_8",
				#	"type":"image",
				#	"vertical_align":"bottom",
				#	
				#	"x":8,
				#	"y":339 - 42 - 256,
				#
				#	"image":"d:/ymir work/ui/ex_inven_cover_button_close.sub",
				#},

				## Print
				{
					"name":"Money_Icon",
					"type":"image",
					"vertical_align":"bottom",
					
					"x":57,
					"y":26,

					"image":"d:/ymir work/ui/game/windows/money_icon.sub",
				},
				{
					"name":"Money_Slot",
					"type":"button",

					"x":8,
					"y":28,

					"horizontal_align":"center",
					"vertical_align":"center",

					"default_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
					"over_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",
					"down_image" : "d:/ymir work/ui/public/parameter_slot_05.sub",

					"children" :
					(
						{
							"name" : "Money",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"x":-18,
							"y":2,

							"horizontal_align" : "right",
							"text_horizontal_align" : "right",

							"text" : "1.999.999.999",
						},	
					),
				},				
				# {
					# "name":"Cheque_Icon",
					# "type":"image",
					# "vertical_align":"bottom",
					
					# "x":10,
					# "y":26,

					# "image":"d:/ymir work/ui/game/windows/cheque_icon.sub",
				# },
				{
					"name":"Cheque_Slot",
					"type":"button",

					"x":28,
					"y":28,

					#"horizontal_align":"center",
					"vertical_align":"bottom",

					#"default_image" : "d:/ymir work/ui/public/cheque_slot.sub",
					#"over_image" : "d:/ymir work/ui/public/cheque_slot.sub",
					#"down_image" : "d:/ymir work/ui/public/cheque_slot.sub",

					"children" :
					(
						{
							"name" : "Cheque",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"horizontal_align" : "right",
							"text_horizontal_align" : "right",

							#"text" : "99",
						},
					),
				},
			),
		},
	
		{
			"name" : "BoardGlobal",
			"type" : "window",
			"style" : ("attach",),
			
			"x" : -16,
			"y" : -32,
			
			#"vertical_align":"center",
			
			"width" : 32,
			#"height" : 160,
			"height" : 543,
			"children" :
			(
				{
					"name" : "PaginationOne",
					"type" : "radio_button",
					"x" : 1,
					"y" : 66,
					
					"default_image" : "invent/button_1_norm.png",
					"over_image" : "invent/button_1_norm.png",
					"down_image" : "invent/button_1.png",
				},
				{
					"name" : "PaginationTwo",
					"type" : "radio_button",
					"x" : 1,
					"y" : 66+22,
					
					"default_image" : "invent/button_2_norm.png",
					"over_image" : "invent/button_2_norm.png",
					"down_image" : "invent/button_2.png",
				},
				{
					"name" : "PaginationThree",
					"type" : "radio_button",
					"x" : 1,
					"y" : 66+22+22,
					
					"default_image" : "invent/button_3_norm.png",
					"over_image" : "invent/button_3_norm.png",
					"down_image" : "invent/button_3.png",
				},
				{
					"name" : "PaginationFourth",
					"type" : "radio_button",
					"x" : 1,
					"y" : 66+22+22+22,
					
					"default_image" : "invent/button_4_norm.png",
					"over_image" : "invent/button_4_norm.png",
					"down_image" : "invent/button_4.png",
				},
				# {
					# "name" : "beltbuttonshit",
					# "type" : "button",
					# "x" : 1,
					# "y" : 65+22+22+22+70,
					
					# "default_image" : "invent/button_c_normal.png",
					# "over_image" : "invent/button_c_normal.png",
					# "down_image" : "invent/button_c.png",
					# "text" : "B",
				# },
				#{
				#	"name" : "systembuttonshit",
				#	"type" : "button",
				#	"x" : 7,
				#	"y" : 65+22+22+22+70+22,
				#	
				#	"default_image" : "invent/button_c_normal.png",
				#	"over_image" : "invent/button_c_normal.png",
				#	"down_image" : "invent/button_c.png",
				#	"text" : "S",
				#},		
			),	
		},
	),
}