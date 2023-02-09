import uiScriptLocale

window = {
	"name" : "InputDialog",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float", "animate",),

	"width" : 230,
	"height" : 260,

	"children" :
	(
		{
			"name" : "Board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : 230,
			"height" : 260,

			"title" : uiScriptLocale.GUILD_WAR_DECLARE,

			"children" :
			(
				## Input Slot
				{
					"name" : "InputName",
					"type" : "text",

					"x" : 15,
					"y" : 40,

					"text" : uiScriptLocale.GUILD_WAR_ENEMY,
				},
				{
					"name" : "InputSlot",
					"type" : "slotbar",

					"x" : 80,
					"y" : 37,
					"width" : 130,
					"height" : 18,

					"children" :
					(
						{
							"name" : "InputValue",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"width" : 90,
							"height" : 18,

							"input_limit" : 12,
						},
					),
				},
				## Input Slot
				{
					"name" : "GameType", "x" : 15, "y" : 65, "width" : 65+45*4, "height" : 20,
					
					"children" :
					(
						{"name" : "GameTypeLabel", "type" : "text", "x" : 0, "y" : 3, "text" : "Modalita'",},
						{
							"name" : "GuardianButton",
							"type" : "radio_button",

							"x" : 65,
							"y" : 0,

							"text" : "Guardiano",

							"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
						},
						{
							"name" : "DeathMatchButton",
							"type" : "radio_button",

							"x" : 65+65*1,
							"y" : 0,

							"text" : "DeathMatch",
							
							"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
						},
					),
				},
				## Input Slot 2
				{
					"name" : "GameType2", "x" : 15, "y" : 95, "width" : 77+45*4, "height" : 20,
					
					"children" :
					(
						{"name" : "GameTypeLabel2", "type" : "text", "x" : 0, "y" : 3, "text" : "Tipo",},
						{
							"name" : "FriendlyButton",
							"type" : "radio_button",

							"x" : 65,
							"y" : 0,

							"text" : "Amichevole",

							"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
						},
						{
							"name" : "RankedButton",
							"type" : "radio_button",

							"x" : 65+65*1,
							"y" : 0,

							"text" : "Classificata",
							
							"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
						},
					),
				},
				## Input Slot 3
				{
					"name" : "GameType3", "x" : 15, "y" : 125, "width" : 89+45*4, "height" : 45,
					
					"children" :
					(
						{"name" : "GameTypeLabel3", "type" : "text", "x" : 0, "y" : 10, "text" : "Mappa",},
						{
							"name" : "DeathlandButton",
							"type" : "radio_button",

							"x" : 65,
							"y" : 0,

							"text" : "Deathland",

							"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
						},
						{
							"name" : "MassacroButton",
							"type" : "radio_button",

							"x" : 65+65*1,
							"y" : 0,

							"text" : "Massacro",
							
							"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
						},
						{
							"name" : "SangueButton",
							"type" : "radio_button",

							"x" : 65,
							"y" : 25,

							"text" : "Sangue",
							
							"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
						},
						{
							"name" : "EstinzioneButton",
							"type" : "radio_button",

							"x" : 65+65*1,
							"y" : 25,

							"text" : "Estinzione",
							
							"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
						},
					),
				},
				## Input Slot 4
				{
					"name" : "GameType4", "x" : 15, "y" : 175, "width" : 65+45*4, "height" : 20,
					
					"children" :
					(
						{"name" : "GameTypeLabel4", "type" : "text", "x" : 0, "y" : 3, "text" : "Players",},
						{
							"name" : "threeButton",
							"type" : "radio_button",

							"x" : 65,
							"y" : 0,

							"text" : "3v3",

							"default_image" : "d:/ymir work/ui/public/small_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/small_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/small_button_03.sub",
						},
						{
							"name" : "sixButton",
							"type" : "radio_button",

							"x" : 65+45*1,
							"y" : 0,

							"text" : "6v6",
							
							"default_image" : "d:/ymir work/ui/public/small_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/small_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/small_button_03.sub",
						},
						{
							"name" : "tenButton",
							"type" : "radio_button",

							"x" : 65+45*2,
							"y" : 0,

							"text" : "12v12",

							"default_image" : "d:/ymir work/ui/public/small_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/small_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/small_button_03.sub",
						},
					),
				},
				## Button
				{
					"name" : "AcceptButton",
					"type" : "button",

					"x" : - 61 - 5 + 30,
					"y" : 225,
					"horizontal_align" : "center",

					"text" : uiScriptLocale.OK,

					"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
				},
				{
					"name" : "CancelButton",
					"type" : "button",

					"x" : 5 + 30,
					"y" : 225,
					"horizontal_align" : "center",

					"text" : uiScriptLocale.CANCEL,

					"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
				},
			),
		},
	),
}
