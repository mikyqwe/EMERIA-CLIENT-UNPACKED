import uiScriptLocale

window = {
	"name" : "SplitItemDialog",

	"x" : 100,
	"y" : 100,

	"style" : ("movable", "float", "animate",),

	"width" : 170,
	"height" : 110,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : 170,
			"height" : 110,

			"title" : uiScriptLocale.PICK_MONEY_TITLE,

			"children" :
			(

				## Money Slot
				{
					"name" : "money_slot",
					"type" : "image",

					"x" : 20,
					"y" : 34,

					"image" : "d:/ymir work/ui/public/Parameter_Slot_02.sub",

					"children" :
					(
						{
							"name" : "split_value",
							"type" : "editline",

							"x" : 3,
							"y" : 2,

							"width" : 60,
							"height" : 18,

							"input_limit" : 3,
							"only_number" : 1,

							"text" : "1",
						},
						{
							"name" : "max_value",
							"type" : "text",

							"x" : 63,
							"y" : 3,

							"text" : "/ 200",
						},
					),
				},

				## Split checkbox
				{
					"name" : "split_checkbox",
					"type" : "checkbox",

					"x" : 200 / 2 - 61 - 5 - 14,
					"y" : 58,

					"checked" : False,

					"text" : "Split Item",
				},

				## Button
				{
					"name" : "accept_button",
					"type" : "button",

					"x" : 200 / 2 - 61 - 5 - 15,
					"y" : 58 + 20,

					"text" : uiScriptLocale.OK,

					"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
				},
				{
					"name" : "cancel_button",
					"type" : "button",

					"x" : 200 / 2 + 5 - 15,
					"y" : 58 + 20,

					"text" : uiScriptLocale.CANCEL,

					"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
				},
			),
		},
	),
}
