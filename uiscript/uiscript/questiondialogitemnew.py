import uiScriptLocale

window = {
	"name" : "QuestionDialog",
	"style" : ("movable", "float", "animate",),

	"x" : SCREEN_WIDTH/2 - 125,
	"y" : SCREEN_HEIGHT/2 - 52,

	"width" : 280,
	"height" : 200,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"x" : 0,
			"y" : 0,
			"width" : 280,
			"height" : 200,
			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"x" : 6,
					"y" : 6,
					"width" : 270,
					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":125, "y":3, "text" : "Alege o op�iune", "text_horizontal_align":"center" },
					),
				},
				{
					"name":"PreviewImage",
					"type":"image",
					"x":20,
					"y":40,
					"image" : "preview.tga",
					"children" :
					(
						{
							"name":"Item",
							"type":"expanded_image",
							"x":50,
							"y":15,
							"image":"icon/item/00270.tga",
						},
						{ "name":"ItemName", "type":"text", "x":67, "y":115, "text" : "ItemName", "text_horizontal_align":"center" },
					),
				},
				{
					"name" : "drop",
					"type" : "button",
					"x" : 170,
					"y" : 40,
					"text" : "Arunc�",
					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
				{
					"name" : "destroy",
					"type" : "button",
					"x" : 170,
					"y" : 70,
					"text" : "Distruge",
					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
				# {
					# "name" : "sell",
					# "type" : "button",
					# "x" : 170,
					# "y" : 100,
					# "text" : "Vinde",
					# "default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					# "over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					# "down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				# },
				{
					"name" : "cancel",
					"type" : "button",
					"x" : 170,
					"y" : 140,
					"text" : "�nchide",
					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
			),
		},
	),
}