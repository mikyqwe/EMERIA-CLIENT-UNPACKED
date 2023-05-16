import uiScriptLocale
import app

BOARD_ADD_X = 0
BOARD_ADD_X += 50 # won
BOARD_ADD_X += 26 # wonexchange

BOARD_X = SCREEN_WIDTH - (140 + BOARD_ADD_X)
BOARD_WIDTH = (140 + BOARD_ADD_X)
BOARD_HEIGHT = 40

window = {
	"name" : "ExpandedMoneyTaskbar",

	"x" : BOARD_X,
	"y" : SCREEN_HEIGHT - 65,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"style" : ("float",),

	"children" :
	[
		{
			"name" : "ExpanedMoneyTaskBar_Board",
			"type" : "board",

			"x" : 0, "y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"children" :
			[
				## Print
				{
					"name":"Money_Icon",
					"type":"image",

					"x":-66 + BOARD_ADD_X, "y":10,

					"image":"d:/ymir work/ui/game/windows/money_icon.sub",
				},
				{
					"name":"Money_Slot",
					"type":"button",

					"x":-47 + BOARD_ADD_X, "y":9,

					#"horizontal_align":"center",

					"default_image" : "d:/ymir work/ui/game/windows/test.tga",
					"over_image" : "d:/ymir work/ui/game/windows/test.tga",
					"down_image" : "d:/ymir work/ui/game/windows/test.tga",

					"children" :
					(
						{
							"name" : "Money",
							"type" : "text",

							"x" : 3, "y" : 3,

							"horizontal_align" : "right",
							"text_horizontal_align" : "right",

							"text" : "9.999.999.999",
						},
					),
				},
			],
		},
	],
}

# window["children"][0]["children"] += [
	# {
		# "name":"Cheque_Icon",
		# "type":"image",

		# "x": BOARD_ADD_X - 27, "y": 10,

		# "image":"d:/ymir work/ui/game/windows/cheque_icon.sub",
	# },
	# {
		# "name":"Cheque_Slot",
		# "type":"button",

		# "x": BOARD_ADD_X - 8, "y":10,

		# "default_image" : "d:/ymir work/ui/public/cheque_slot.sub",
		# "over_image" : "d:/ymir work/ui/public/cheque_slot.sub",
		# "down_image" : "d:/ymir work/ui/public/cheque_slot.sub",

		# "children" :
		# (
			# {
				# "name" : "Cheque",
				# "type" : "text",

				# "x" : 3, "y" : 3,

				# "horizontal_align" : "right",
				# "text_horizontal_align" : "right",

				# "text" : "99",
			# },
		# ),
	# },
# ]

# window["children"][0]["children"] += [
	# {
		# "name":"ExchangeButtonBase",
		# "type":"image",

		# "x":BOARD_ADD_X - 126+60, "y":8,

		# "image":"d:/ymir work/ui/pattern/titlebar_minimize_baseframe.tga",
		# "children":
		# (
			# {
				# "name":"ExchangeButton", "type":"button",
				# "x":3, "y":3,
				# "tooltip_text" : uiScriptLocale.WONEXCHANGE_TITLE,
				# "default_image" : "d:/ymir work/ui/game/wonexchange/exchange_btn_normal_01.sub",
				# "over_image" : "d:/ymir work/ui/game/wonexchange/exchange_btn_over_01.sub",
				# "down_image" : "d:/ymir work/ui/game/wonexchange/exchange_btn_down_01.sub",
			# },
		# )
	# },
# ]
