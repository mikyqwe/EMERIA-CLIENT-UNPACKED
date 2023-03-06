import uiScriptLocale

window = {
	"name" : "MembersOnlineWindow",

	"x" : SCREEN_WIDTH - 170 - 30,
	"y" : SCREEN_HEIGHT - 400 - 50,

	"style" : ("movable", "float", "animate",),

	"width" : 170,
	"height" : 300,

	"children" :
	(

		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : 170,
			"height" : 300,
			"title" : "Membri Online",
		},

		{
			"name" : "ScrollBar",
			"type" : "scrollbar",

			"x" : 30,
			"y" : 40,
			"size" : 220,
			"horizontal_align" : "right",
		},

		{
			"name" : "invite",
			"type" : "button",

			"x" : 15,
			"y" : 265,

			"width" : 41,
			"height" : 21,

			"text" : "Invitã",

			"default_image" : "d:/ymir work/ui/public/small_button_01.sub",
			"over_image" : "d:/ymir work/ui/public/small_button_02.sub",
			"down_image" : "d:/ymir work/ui/public/small_button_03.sub",
		},
		{
			"name" : "aggiorna",
			"type" : "button",

			"x" : 75,
			"y" : 265,

			"width" : 41,
			"height" : 21,

			"text" : "Actualizaþi",

			"default_image" : "d:/ymir work/ui/public/small_button_01.sub",
			"over_image" : "d:/ymir work/ui/public/small_button_02.sub",
			"down_image" : "d:/ymir work/ui/public/small_button_03.sub",
		},
	)
}
