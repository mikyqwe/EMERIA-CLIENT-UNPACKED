import uiScriptLocale
SPACE_BONUS_INVENTORY = 130
window = {
	"name" : "SystemInventoryWindow",
	"x" : SCREEN_WIDTH - 176 - SPACE_BONUS_INVENTORY + 37 - 150,
	"y" : SCREEN_HEIGHT - 37 - 565,
	"width" : 150,
	"height" : 45*8,

	"type" : "image",
	"image" : "d:/ymir work/ui/game/belt_inventory/bg.tga",
	

	"children" :
	(
		{
			"name" : "ExpandBtn",
			"type" : "button",

			"x" : 2,
			"y" : 15,

			"default_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_normal.tga",
			"over_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_over.tga",
			"down_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_down.tga",
			"disable_image" : "d:/ymir work/ui/game/belt_inventory/btn_expand_disabled.tga",
		},

		
		{
			"name" : "SystemInventoryLayer",

			"x" : 5,
			"y" : 0,

			"width" : 150,
			"height" : 45*8,

			"children" :
			(
				{
					"name" : "MinimizeBtn",
					"type" : "button",

					"x" : 2,
					"y" : 15,

					"width" : 10,

					"default_image" : "d:/ymir work/ui/game/belt_inventory/btn_minimize_normal.tga",
					"over_image" : "d:/ymir work/ui/game/belt_inventory/btn_minimize_over.tga",
					"down_image" : "d:/ymir work/ui/game/belt_inventory/btn_minimize_down.tga",
					"disable_image" : "d:/ymir work/ui/game/belt_inventory/btn_minimize_disabled.tga",
				},

				{
					"name" : "SystemInventoryBoard",
					"type" : "board",
					"style" : ("attach", "float"),

					"x" : 10,
					"y" : 0,

					"width" : 51,
					"height" : 45*8,
					
					"children" :
					(
						{
							"name" : "RaktarGomb",
							"type" : "button",

							"x": 7+7-3,
							"y" : 5+26+58-15-70-2+4+16.5,
							"default_image": "d:/ymir work/ui/sidebarinventory/buy_switch_item_button_default.tga",
							"over_image" : "d:/ymir work/ui/sidebarinventory/buy_switch_item_button_over.tga",
							"down_image" : "d:/ymir work/ui/sidebarinventory/buy_switch_item_button_default.tga", 
							"tooltip_text" : "Switcher",
						},
						{
							"name" : "OfflineShopButton",
							"type" : "button",

							"x": 7+7-3,
							"y" : 5+26+58-15-70-2+4+16.5+45,

							"default_image" :"d:/ymir work/ui/sidebarinventory/shirt_default.tga", 
							"over_image" :"d:/ymir work/ui/sidebarinventory/shirt_over.tga", 
							"down_image" :"d:/ymir work/ui/sidebarinventory/shirt_default.tga",
							"tooltip_text" : "Equipment",
						}, 
						{
							"name" : "biolog",
							"type" : "button",
		 
							"x": 7+7-3,
							"y" : 5+26+58-15-70-2+4+16.5+45+45,
		 
							"default_image" :"d:/ymir work/ui/sidebarinventory/bonus_default.tga", 
							"over_image" :"d:/ymir work/ui/sidebarinventory/bonus_over.tga", 
							"down_image" :"d:/ymir work/ui/sidebarinventory/bonus_default.tga",
							"tooltip_text" : "Bonus",
						},
						{
							"name" : "OkeyCardButton",
							"type" : "button",

							"x": 7+7-3,
							"y" : 5+26+58-15-70-2+4+16.5+45+90,

							"default_image" :"d:/ymir work/ui/sidebarinventory/map_default.tga", 
							"over_image" :"d:/ymir work/ui/sidebarinventory/map_over.tga", 
							"down_image" :"d:/ymir work/ui/sidebarinventory/map_default.tga",
							"tooltip_text" : "Map",
						}, 	
						{
							"name" : "special",
							"type" : "button",
		 
							"x": 7+7-3,
							"y" : 5+26+58-15-70-2+4+16.5+45+135,
		 
							"default_image" :"d:/ymir work/ui/sidebarinventory/sky_default.tga", 
							"over_image" :"d:/ymir work/ui/sidebarinventory/sky_over.tga", 
							"down_image" :"d:/ymir work/ui/sidebarinventory/sky_default.tga", 
							"tooltip_text" :"Sky",
						},
						{
							"name" : "clickbattlepasschoose",
							"type" : "button",
		 
							"x": 7+7-3,
							"y" : 5+26+58-15-70-2+4+16.5+45+180,
		 
							"default_image" :"d:/ymir work/ui/sidebarinventory/pick_default.tga", 
							"over_image" :"d:/ymir work/ui/sidebarinventory/pick_over.tga", 
							"down_image" :"d:/ymir work/ui/sidebarinventory/pick_default.tga",
							"tooltip_text" : "Pick Up",
						},
						{
							"name" : "bonus",
							"type" : "button",
		 
							"x": 7+7-3,
							"y" : 5+26+58-15-70-2+4+16.5+45+225,
									 
							"default_image" :"d:/ymir work/ui/sidebarinventory/screen_default.tga", 
							"over_image" :"d:/ymir work/ui/sidebarinventory/screen_over.tga", 
							"down_image" :"d:/ymir work/ui/sidebarinventory/screen_default.tga", 
							"tooltip_text" :"Dragon Soul",
						},	
					)
				},
			)
		},
	),
}