ROOT_PATH = "d:/ymir work/ui/game/biolog/"

window = {
	"name" : "BiologWindow",
	"style" : ("movable", "float","animate",),

	"x" : 0,
	"y" : 0,

	"width" : 255,
	"height" : 485,

	"children" :
	(
		{
			"name": "Board",
			"type": "image",
			
			"style" : ("attach",),
			
			"width": 255,
			"height": 485,
			
			"x": 0,
			"y": 0,
			
			"image" : "d:/ymir work/ui/cw/bio/empty_board.tga",
			#"image" : "d:/ymir work/ui/cw/bio/board_full.tga",

			# "title" : "Cercetarile Biologului",

			"children" :
			(

				{
					"name" : "CloseButton",
					"type" : "button",
					"x" : 230,
					"y" : 8,
					"default_image" : "d:/ymir work/ui/cw/bio/close_normal.tga",
					"over_image" : "d:/ymir work/ui/cw/bio/close_over.tga",
					"down_image" :"d:/ymir work/ui/cw/bio/close_down.tga",
				},

				{
					"name" : "info",
					"type" : "image",
					
					"x" : 203,
					"y" : 102,
					
					"image" : "d:/ymir work/ui/cw/bio/info.tga",
				},

				{
					"name" : "ShopButton",
					"type" : "button",
					"x" : 190,
					"y" : 59,
					"default_image" : "d:/ymir work/ui/cw/bio/shop_normal.tga",
					"over_image" : "d:/ymir work/ui/cw/bio/shop_over.tga",
					"down_image" : "d:/ymir work/ui/cw/bio/shop_down.tga",
				},

				{
					"name" : "gaugeText", 
					"type" : "text",
					
					"text_horizontal_align" : "center",
					
					"x" : 129,
					"y" : 309,
					
					"text" : "Timp Ramas : 6 ore 5 minute 30 secunde",
				},
				{
					"name" : "titlename", 
					"type" : "text",
					
					"text_horizontal_align" : "center",
					
					"x" : 130,
					"y" : 9,
					
					"text" : "Cercetarile Biologului",
				},
				{
					"name" : "namebio", 
					"type" : "text",
					
					"text_horizontal_align" : "center",
					
					"x" : 143,
					"y" : 64,
					
					"text" : "Biologul Chaegirab",
				},

				{
					"name" : "CurrentBiologName", 
					"type" : "text",
					
					"text_horizontal_align" : "center",
					
					"x" : 125,
					"y" : 104,
					
					"text" : "Dinti de Ork",
				},

				{
					"name" : "SelectThing", 
					"type" : "text",
					
					"text_horizontal_align" : "center",
					
					"x" : 128,
					"y" : 336,
					
					"text" : "Selecteaza Bonus",
				},

				{
					"name" : "ani_slot0",
					"type" : "ani_image",
					"style" : ("attach",),
					
					"x" : 99,
					"y" : 121,
					
					"delay" : 6,

					"images" :
					(
						"d:/ymir work/ui/cw/bio/glow/slot_glow_1.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_2.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_3.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_4.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_5.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_5.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_4.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_3.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_2.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_1.tga",		
					),
				},

				{
					"name" : "ItemSlotBack",
					"type" : "image",
					
					"x" : 107,
					"y" : 130,
					
					"image" : "d:/ymir work/ui/cw/bio/slot.tga",
					
					"children" :
					(
						{
							"name" : "ItemSlotBiolog",
							"type" : "slot",
		
							"x" : 3,
							"y" : 3,
		
							"width" : 32,
							"height" : 32,

							"slot":
							(
								{ "index": 0, "x": 0,"y": 0, "width":32, "height":32 },
							),
						},
					),
				},

				{
					"name" : "ani_slot0",
					"type" : "ani_image",
					"style" : ("attach",),
					
					"x" : 67 - 8,
					"y" : 180 - 9,
					
					"delay" : 6,

					"images" :
					(
						"d:/ymir work/ui/cw/bio/glow/slot_glow_1.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_2.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_3.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_4.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_5.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_5.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_4.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_3.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_2.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_1.tga",		
					),
				},

				{
					"name" : "ItemSlotImageReset",
					"type" : "image",
					
					"x" : 67,
					"y" : 180,
					
					"image" : "d:/ymir work/ui/cw/bio/slot.tga",
					
					"children" :
					(
						{
							"name" : "ItemSlotReset",
							"type" : "slot",
		
							"x" : 3,
							"y" : 3,
		
							"width" : 32,
							"height" : 32,

							"slot":
							(
								{ "index": 0, "x": 0,"y": 0, "width":32, "height":32 },
							),
						},
					),
				},

				{
					"name" : "ani_slot0",
					"type" : "ani_image",
					"style" : ("attach",),
					
					"x" : 146 - 8,
					"y" : 180 - 9,
					
					"delay" : 6,

					"images" :
					(
						"d:/ymir work/ui/cw/bio/glow/slot_glow_1.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_2.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_3.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_4.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_5.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_5.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_4.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_3.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_2.tga",		
						"d:/ymir work/ui/cw/bio/glow/slot_glow_1.tga",		
					),
				},

				{
					"name" : "ItemSlotImagePercent",
					"type" : "image",
					
					"x" : 146,
					"y" : 180,
					
					"image" : "d:/ymir work/ui/cw/bio/slot.tga",
					
					"children" :
					(
						{
							"name" : "ItemSlotPercent",
							"type" : "slot",
		
							"x" : 3,
							"y" : 3,
		
							"width" : 32,
							"height" : 32,

							"slot":
							(
								{ "index": 0, "x": 0,"y": 0, "width":32, "height":32 },
							),
						},
					),
				},

				{
					"name" : "ToggleReset",
					"type" : "toggle_button",
		
					"x" : 79,
					"y" : 220,
		
					"default_image" : "d:/ymir work/ui/cw/bio/checkbox.tga",
					"over_image" : "d:/ymir work/ui/cw/bio/checkbox2.tga",
					"down_image" : "d:/ymir work/ui/cw/bio/checkbox2.tga",
				},

				{
					"name" : "ToggleChance",
					"type" : "toggle_button",
		
					"x" : 158,
					"y" : 220,
		
					"default_image" : "d:/ymir work/ui/cw/bio/checkbox.tga",
					"over_image" : "d:/ymir work/ui/cw/bio/checkbox2.tga",
					"down_image" : "d:/ymir work/ui/cw/bio/checkbox2.tga",
				},

				{
					"name" : "DeliverButton",
					"type" : "button",
					"x" : 82,
					"y" : 247,

					"text" : "Livreaza",

					"default_image" : "d:/ymir work/ui/cw/bio/button_normal.tga",
					"over_image" : "d:/ymir work/ui/cw/bio/button_over.tga",
					"down_image" :"d:/ymir work/ui/cw/bio/button_down.tga",
				},

				{
					"name" : "bonusBoard0",
					"type" : "image",
					
					"x" : 33,
					"y" : 363,
					
					"image" : "d:/ymir work/ui/cw/bio/bonusBoard.tga",
					
					"children" :
					(

						{
							"name" : "selectBonus0",
							"type" : "button",

							"x" : 160,
							"y" : -1,

							"default_image" : "d:/ymir work/ui/cw/bio/select_normal.tga",
							"over_image" : "d:/ymir work/ui/cw/bio/select_down.tga",
							"down_image" : "d:/ymir work/ui/cw/bio/select_hover.tga",
						},

						{
							"name" : "selectText0", 
							"type" : "text",

							"text_horizontal_align" : "center",

							"x" : 80,
							"y" : 3,

							"text" : "-",
						},
					),
				},

				{
					"name" : "bonusBoard1",
					"type" : "image",
					
					"x" : 33,
					"y" : 386,
					
					"image" : "d:/ymir work/ui/cw/bio/bonusBoard.tga",
					
					"children" :
					(

						{
							"name" : "selectBonus1",
							"type" : "button",

							"x" : 160,
							"y" : -1,

							"default_image" : "d:/ymir work/ui/cw/bio/select_normal.tga",
							"over_image" : "d:/ymir work/ui/cw/bio/select_down.tga",
							"down_image" : "d:/ymir work/ui/cw/bio/select_hover.tga",
						},						
						{
							"name" : "selectText1", 
							"type" : "text",
							
							"text_horizontal_align" : "center",
							
							"x" : 80,
							"y" : 3,
							
							"text" : "-",
						},
					),
				},
				{
					"name" : "bonusBoard2",
					"type" : "image",
					
					"x" : 33,
					"y" : 386 + 23,
					
					"image" : "d:/ymir work/ui/cw/bio/bonusBoard.tga",
					
					"children" :
					(

						{
							"name" : "selectBonus2",
							"type" : "button",

							"x" : 160,
							"y" : -1,

							"default_image" : "d:/ymir work/ui/cw/bio/select_normal.tga",
							"over_image" : "d:/ymir work/ui/cw/bio/select_down.tga",
							"down_image" : "d:/ymir work/ui/cw/bio/select_hover.tga",
						},

						{
							"name" : "selectText2", 
							"type" : "text",
							
							"text_horizontal_align" : "center",
							
							"x" : 80,
							"y" : 3,
							
							"text" : "-",
						},
					),
				},
				{
					"name" : "bonusBoard3",
					"type" : "image",
					
					"x" : 33,
					"y" : 386 + 46,
					
					"image" : "d:/ymir work/ui/cw/bio/bonusBoard.tga",
					
					"children" :
					(

						{
							"name" : "selectBonus3",
							"type" : "button",

							"x" : 160,
							"y" : -1,

							"default_image" : "d:/ymir work/ui/cw/bio/select_normal.tga",
							"over_image" : "d:/ymir work/ui/cw/bio/select_down.tga",
							"down_image" : "d:/ymir work/ui/cw/bio/select_hover.tga",
						},

						{
							"name" : "selectText3", 
							"type" : "text",
							
							"text_horizontal_align" : "center",
							
							"x" : 80,
							"y" : 3,
							
							"text" : "-",
						},
					),
				},
				{
					"name" : "GaugeBackground",
					"type" : "image",
					
					"x" : 32,
					"y" : 275,
					
					"image" : "d:/ymir work/ui/cw/bio/loadbar.tga",
					
					"children" :
					(
						{
							"name" : "CoolTime",
							"type" : "expanded_image",
							"x" : 23,
							"y" : 8,
							"image" : "d:/ymir work/ui/cw/bio/loadbarfull.tga",
						},
					),
				},
			),
		},
	),
}
