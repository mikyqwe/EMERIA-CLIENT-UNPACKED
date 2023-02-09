import uiScriptLocale
import item
import app
import localeInfo

LOCALE_PATH = "d:/ymir work/ui/rankingboard/"
GOLD_COLOR	= 0xFFFEE3AE
ROOT_PATH = "d:/ymir work/ui/public/"

window = {
	"name" : "GuildWindow_GuildRankingPageNonGuild",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float", "animate",),
	
	"width" : 517,
	"height" : 356,

	"children" :
	(
		{
			"name" : "Board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : 517,
			"height" : 356,

			"title" : "Classifica Gilde/Player",
			"children" :
			(
				###Guild/Players Radio Button
				{
					"name" : "guild_button",
					"type" : "radio_button",

					"x" : 380 + 6,
					"y" : 5 + 28,

					"text" : "Gilde",

					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
				{
					"name" : "players_button",
					"type" : "radio_button",

					"x" : 440 + 6,
					"y" : 5 + 28,

					"text" : "Players",

					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
				###
				## ItemNameEditLine
				{
					"name" : "ItemNameSlot",
					"type" : "image",
					"x" : 0 + 6,
					"y" : 5 + 28,
					"image" : LOCALE_PATH+"private_leftSlotImg.sub",
					"children" :
					(
					##EditLine
						{
							"name" : "ItemNameValue",
							"type" : "editline",
							"x" : 2,
							"y" : 3,
							"width" : 136,
							"height" : 15,
							"input_limit" : 18,
							"text" : "",
						},
					),
				},
				## FindButton
				{
					"name" : "RefreshBtn",
					"type" : "button",

					"x" : 190 + 6,
					"y" : 5 + 28,

					"text" : "Aggiorna",


					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},		
				## RefreshButton
				{
					"name" : "SearchButton",
					"type" : "button",

					"x" : 125 + 6,
					"y" : 5 + 28,

					"text" : "Cerca",


					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
				##Lines "Non gli assorbenti :)"
				{
					"name" : "top_line",
					"type" : "line",

					"x" : -2 + 6,
					"y" : 27 + 28,

					"width" : 506,
					"height" : 0,

					"color" : 0xffAAA6A1,
				},
				{
					"name" : "right_line",
					"type" : "line",

					"x" : -2 + 6,
					"y" : 30 + 28,

					"width" : 0,
					"height" : 240,

					"color" : 0xffAAA6A1,
				},
				{
					"name" : "left_line",
					"type" : "line",

					"x" : 504 + 6,
					"y" : 30 + 28,

					"width" : 0,
					"height" : 240,

					"color" : 0xffAAA6A1,
				},
				{
					"name" : "bottom_line",
					"type" : "line",

					"x" : -2 + 6,
					"y" : 270 + 28,

					"width" : 506,
					"height" : 0,

					"color" : 0xffAAA6A1,
				},
				#######
				## tab_menu_01
				{
					"name" : "ItemTypeImg",
					"type" : "expanded_image",
					"x" : 0 + 6,
					"y" : 30 + 28,
					"width" : 10,
					"image" : "d:/ymir work/ui/tab_menu_01.tga",
					"x_scale" : 1.145, 
					"y_scale" : 1.0,
					"children" :
					(
						## Text
						{ "name" : "ResultNameText1", "type" : "text", "x" : 10, "y" : 4,  "text" : "#  Nome", },
						{ "name" : "ResultNameText2", "type" : "text", "x" : 107, "y" : 4, "text" : "", },
						{ "name" : "ResultNameText3", "type" : "text", "x" : 203, "y" : 4, "text" : "W  -  L", },
						{ "name" : "ResultNameText4", "type" : "text", "x" : 282, "y" : 4, "text" : "Trofei", },
						{ "name" : "ResultNameText5", "type" : "text", "x" : 395, "y" : 4, "text" : "Miglior Giocatore", },
						{ "name" : "ResultNameText6", "type" : "text", "x" : 441, "y" : 4, "text" : "Gilda", },
					),
				},
				## Pag2Button
				{
					"name" : "pagetwoButton",
					"type" : "radio_button",

					"x" : 435 + 6,
					"y" : 280 + 28,

					"text" : "Pagina 2",


					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
				###
				## Pag1Button
				{
					"name" : "pageoneButton",
					"type" : "radio_button",

					"x" : -2 + 6,
					"y" : 280 + 28,

					"text" : "Pagina 1",


					"default_image" : ROOT_PATH + "Middle_Button_01.sub",
					"over_image" : ROOT_PATH + "Middle_Button_02.sub",
					"down_image" : ROOT_PATH + "Middle_Button_03.sub",
				},
				###
			),
		},
	),
}