import uiScriptLocale

LOCALE_PATH = uiScriptLocale.WINDOWS_PATH
ROOT_PATH = "d:/ymir work/ui/public/"

window = {
	"name" : "ManualSwitchbot",

	"x" : 300,
	"y" : 100,

	"style" : ("movable", "float",),

	"width" : 256,
	"height" : 375,

	"children" :
	(
								
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 236,
			"height" : 375,
			
			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6,
					"y" : 6,

					"width" : 224,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":120, "y":3, "text":uiScriptLocale.SWITCHER_TITLE, "text_horizontal_align":"center", },
					),
				},

				## Equipment Slot
				{
					"name" : "Switcher_Base",
					"type" : "image",

					"x" : 13,
					"y" : 38,
					
					"image" : ROOT_PATH + "bonus.tga",					

					"children" :
					(

						{
							"name" : "switchslot",
							"type" : "slot",

							"x" : 3,
							"y" : 3,

							"width" : 170,
							"height" : 145,

							"slot" : (
										{"index":0, "x":51, "y":16, "width":32, "height":96},
										{"index":1, "x":140, "y":72, "width":32, "height":32},
									),
						},
					),
				},
				{ 
					"name":"Skill_Active_Title_Bar", 
					"type":"horizontalbar", 
					"x":13, 
					"y":198, 
					"width":210,
					"children" :
					(
						{ "name":"Active_Skill_Point_Value", "type":"text", "x":110, "y":1, "text":uiScriptLocale.SWITCHER_BONUS, "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
					),
				},
				## bonus1
				{
					"name" : "character_board",
					"type" : "thinboard",

					"x" : 13,
					"y" : 220,

					"width" : 210,
					"height" : 30 ,
					"children" :
					(
						{
							"name" : "bonus1",
							"type" : "text",

							"x" : 0,
							"y" : 0,
							"r":0.6911,
							"g":0.8754,
							"b":0.7068,
							"a":1.0,

							"text" : "",

							"all_align" : "center",
						},
					),
				},
				## bonus2
				{
					"name" : "character_board",
					"type" : "thinboard",

					"x" : 13,
					"y" : 255,

					"width" : 210,
					"height" : 30 ,
					"children" :
					(
						{
							"name" : "bonus2",
							"type" : "text",

							"x" : 0 ,
							"y" : 0,
							"r":0.6911,
							"g":0.8754,
							"b":0.7068,
							"a":1.0,

							"text" : "",

							"all_align" : "center",
						},
					),
				},
				## bonus3
				{
					"name" : "character_board",
					"type" : "thinboard",

					"x" : 13,
					"y" : 290,

					"width" : 210,
					"height" : 30 ,
					"children" :
					(
						{
							"name" : "bonus3",
							"type" : "text",

							"x" : 0 ,
							"y" : 0,
							"r":0.6911,
							"g":0.8754,
							"b":0.7068,
							"a":1.0,

							"text" : "",

							"all_align" : "center",
						},
					),
				},
				{
					"name" : "gira_bonus",
					"type" : "button",

					"x" : 80,
					"y" : 340,

					"text" : uiScriptLocale.SWITCHER_CHANGEBONUS,

					"default_image" : ROOT_PATH + "Large_Button_01.sub",
					"over_image" : ROOT_PATH + "Large_Button_02.sub",
					"down_image" : ROOT_PATH + "Large_Button_03.sub",
				},
			),
		},
	),
}