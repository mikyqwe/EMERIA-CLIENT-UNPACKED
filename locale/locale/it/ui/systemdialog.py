import uiScriptLocale

ROOT = "d:/ymir work/ui/public/"

window = {
	"name" : "SystemDialog",
	"style" : ("float", "animate",),

	"x" : (SCREEN_WIDTH  - 200) /2,
	"y" : (SCREEN_HEIGHT - 288) /2,

	"width" : 200,
	"height" : 280+75,		##

	"children" :
	(
		{
			"name" : "board",
			"type" : "thinboard",

			"x" : 0,
			"y" : 0,

			"width" : 200,
			"height" : 280+75,

			"children" :
			(
				{
					"name" : "mall_button",
					"type" : "button",

					"x" : 10,
					"y" : 57,

					"text" : uiScriptLocale.SYSTEM_MALL,
					"text_color" : 0xffF8BF24,

					"default_image" : ROOT + "XLarge_Button_02.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_02.sub",
				},

				{
					"name" : "system_option_button",
					"type" : "button",

					"x" : 10,
					"y" : 87,

					"text" : uiScriptLocale.SYSTEMOPTION_TITLE,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "game_option_button",
					"type" : "button",

					"x" : 10,
					"y" : 117,

					"text" : uiScriptLocale.GAMEOPTION_TITLE,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},

				{
					"name" : "language_button",
					"type" : "button",

					"x" : 32,
					"y" : 300,
					"tooltip_text" : uiScriptLocale.CHANGE_LANGUAGE,
					#"text" : "Cambia Lingua",
					#"text_color" : 0xffF8BF24,

					"default_image" : ROOT + "global1.tga",
					"over_image" : ROOT + "global2.tga",
					"down_image" : ROOT + "global3.tga",
				},
				{
				
					"name" : "RafinarieMain",
					"type" : "thinboard",
					"style" : ("attach",),
					
					"x" : -45,
					"y" : -70,
		
					"width" : 280+200-32-115-40,
					"height" : 62,	
					"children" :
					(
						{ "name":"SmartText0", "type":"text", "x":0, "y":3, "text" : "L'utilizzo di software illegali su Zayos viene", "horizontal_align":"center", "text_horizontal_align":"center" },
						{ "name":"RewardText", "type":"text", "x":0, "y":14, "text" : "sanzionato con un ban hardware definitivo.", "horizontal_align":"center", "text_horizontal_align":"center" },
						{ "name":"RewardText", "type":"text", "x":0, "y":14+11, "text" : "Per favore, cerca di utilizzare sempre un linguaggio rispettoso.", "horizontal_align":"center", "text_horizontal_align":"center" },
						{ "name":"RewardText", "type":"text", "x":0, "y":14+11+11, "text" : "Se hai bisogno di aiuto, unisciti al nostro server Discord!", "horizontal_align":"center", "text_horizontal_align":"center" },
						{ "name":"RewardText", "type":"text", "x":0, "y":14+11+11+11, "text" : "E' consigliato giocare a una risoluzione superiore a 800x600.", "horizontal_align":"center", "text_horizontal_align":"center" },
					)
				},				
                {
                    "name" : "change_ch_button",
                    "type" : "button",


                    "x" : 84,
                    "y" : 300,

					"tooltip_text" : uiScriptLocale.CHANGE_CHH,
                    #"text" : "Cambia Canale",
					#"text_color" : 0xffF8BF24,

					"default_image" : ROOT + "ch_norm.tga",
					"over_image" : ROOT + "ch_over.tga",
					"down_image" : ROOT + "ch_down.tga",
                },				

				{
					"name" : "change_button",
					"type" : "button",

					"x" : 10,
					"y" : 147,

					"text" : uiScriptLocale.SYSTEM_CHANGE,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "logout_button",
					"type" : "button",

					"x" : 10,
					"y" : 177,

					"text" : uiScriptLocale.SYSTEM_LOGOUT,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},	
	
				{
					"name" : "exit_button",
					"type" : "button",

					"x" : 10,
					"y" : 217,

					"text" : uiScriptLocale.SYSTEM_EXIT,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "help_button",
					"type" : "button",

					"x" : 10,
					"y" : 17,

					"text" : uiScriptLocale.SYSTEM_HELP,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
				{
					"name" : "helptwo_button",
					"type" : "button",

					"x" : 135,
					"y" : 300,
					"tooltip_text" : uiScriptLocale.CHANGE_REPORT,
					#"text" : uiScriptLocale.SYSTEM_REPORT,
					#"text_color" : 0xffDA3511,
					
					"default_image" : ROOT + "report_norm.tga",
					"over_image" : ROOT + "report_over.tga",
					"down_image" : ROOT + "report_down.tga",
				},
				{
					"name" : "cancel_button",
					"type" : "button",

					"x" : 10,
					"y" : 251,

					"text" : uiScriptLocale.CANCEL,

					"default_image" : ROOT + "XLarge_Button_01.sub",
					"over_image" : ROOT + "XLarge_Button_02.sub",
					"down_image" : ROOT + "XLarge_Button_03.sub",
				},
			),
		},
	),
}
