import uiScriptLocale

window = {
	"name" : "TaskBarS",
	"x" : 0,
	"y" : SCREEN_HEIGHT - 130,
	"width" : 120,
	"height" :  90,
	"children" : 
	(
		{
			"name" : "little_bar",
			"type" : "image",
			"x" : 0,
			"y" : 26,
			"image" : "btn/round_bar.png",
			"children" :
			(
				{
					"name" : "new_button_1",
					"type" : "button",
					"x" : 6,
					"y" : 5,
					"tooltip_text" : "Pickup",
					"default_image" : "btn/normal/btn 1_normal.png",
					"over_image" : "btn/hover/btn 1_hover.png",
					"down_image" : "btn/normal/btn 1_normal.png",
				},
				{
					"name" : "new_button_2",
					"type" : "button",
					"x" : 28,
					"y" : 4,
					"tooltip_text" : "Sfere",
					"default_image" : "btn/normal/btn 2_normal.png",
					"over_image" : "btn/hover/btn 2_hover.png",
					"down_image" : "btn/normal/btn 2_normal.png",
				},
				{
					"name" : "new_button_3",
					"type" : "button",
					"x" : 28+21,
					"y" : 10,
					"tooltip_text" : "Guardaroba",
					"default_image" : "btn/normal/btn 3_normal.png",
					"over_image" : "btn/hover/btn 3_hover.png",
					"down_image" : "btn/normal/btn 3_normal.png",
				},
				{
					"name" : "new_button_4",
					"type" : "button",
					"x" : 28+21+17,
					"y" : 12+12,
					"tooltip_text" : "Teleporter",
					"default_image" : "btn/normal/btn 4_normal.png",
					"over_image" : "btn/hover/btn 4_hover.png",
					"down_image" : "btn/normal/btn 4_normal.png",
				},
				{
					"name" : "new_button_5",
					"type" : "button",
					"x" : 28+21+17+13,
					"y" : 12+12+15,
					"tooltip_text" : "Switcher",
					"default_image" : "btn/normal/btn 5_normal.png",
					"over_image" : "btn/hover/btn 5_hover.png",
					"down_image" : "btn/normal/btn 5_normal.png",
				},
			),
		},
	),
}