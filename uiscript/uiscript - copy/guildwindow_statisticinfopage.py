import uiScriptLocale

SMALL_VALUE_FILE = "d:/ymir work/ui/public/Parameter_Slot_01.sub"
LARGE_VALUE_FILE = "d:/ymir work/ui/public/Parameter_Slot_03.sub"
XLARGE_VALUE_FILE = "d:/ymir work/ui/public/Parameter_Slot_04.sub"

window = {
	"name" : "GuildWindow_GuildStatisticPage",

	"x" : 8,
	"y" : 30,

	"width" : 505,
	"height" : 298,

	"children" :
	(

		## Guild Info Title
		{
			"name":"Guild_Info_Title_Bar", "type":"horizontalbar", "x":5, "y":10, "width":167,
			"children" :
			(
				{ "name":"Guild_Info_Point_Value", "type":"text", "x":8, "y":3, "text":"Danni Effettuati/Ricevuti", },

				## DamageDone
				{
					"name" : "GuildDamageDone", "type" : "text", "x" : 3, "y" : 31, "text" : "Danno Effettuato",
					"children" :
					(
						{
							"name" : "GuildNameSlot",
							"type" : "image",
							"x" : 100,
							"y" : -2,
							"image" : LARGE_VALUE_FILE,
							"children" :
							(
								{"name" : "GuildDamageDoneValue", "type":"text", "text":"0", "x":0, "y":0, "all_align":"center"},
							),
						},
					),
				},

				## DamageReceived
				{
					"name" : "GuildDamageReceived", "type" : "text", "x" : 3, "y" : 57, "text" : "Danno Ricevuto",
					"children" :
					(
						{
							"name" : "GuildDamageReceivedSlot",
							"type" : "image",
							"x" : 100,
							"y" : -2,
							"image" : LARGE_VALUE_FILE,
							"children" :
							(
								{"name" : "GuildDamageReceivedValue", "type":"text", "text":"0", "x":0, "y":0, "all_align":"center"},
							),
						},
					),
				},

				## Kills/Deaths
				{
					"name" : "GuildKillsDeaths", "type" : "text", "x" : 3, "y" : 93, "text" : "Ratio",
					"children" :
					(
						{
							"name" : "GuildKillsDeathsSlot",
							"type" : "slotbar",
							"x" : 100,
							"y" : -2,
							"width" : 45,
							"height" : 17,
							"children" :
							(
								{"name" : "GuildKillDeathsValue", "type":"text", "text":"30", "x":0, "y":0, "all_align":"center"},
							),
						},
					),
				},

				## Wins
				{
					"name" : "GuildWins", "type" : "text", "x" : 3, "y" : 119, "text" : "Wins",
					"children" :
					(
						{
							"name" : "WinsSlot",
							"type" : "image",
							"x" : 100,
							"y" : -2,
							"image" : LARGE_VALUE_FILE,
							"children" :
							(
								{"name" : "WinsValue", "type":"text", "text":"10000000", "x":0, "y":0, "all_align":"center"},
							),
						},
					),
				},

				## Loses
				{
					"name" : "GuildLoses", "type" : "text", "x" : 3, "y" : 145, "text" : "Loses",
					"children" :
					(
						{
							"name" : "LosesSlot",
							"type" : "image",
							"x" : 70,
							"y" : -2,
							"image" : LARGE_VALUE_FILE,
							"children" :
							(
								{"name" : "LosesValue", "type":"text", "text":"123123123123", "x":0, "y":0, "all_align":"center"},
							),
						},
					),
				},

				## BestPlayer
				{
					"name" : "GuildBestPlayer", "type" : "text", "x" : 3, "y" : 171, "text" : "BestPlayer",
					"children" :
					(
						{
							"name" : "GuildBestPlayer",
							"type" : "image",
							"x" : 70,
							"y" : -2,
							"image" : LARGE_VALUE_FILE,
							"children" :
							(
								{"name" : "GuildBestPlayerValue", "type":"text", "text":"30 / 32", "x":0, "y":0, "all_align":"center"},
							),
						},
					),
				},

				## BestPlayerKills
				{
					"name" : "GuildBestPlayerKills", "type" : "text", "x" : 3, "y" : 197, "text" : "BestPlayerKills",
					"children" :
					(
						{
							"name" : "GuildBestPlayerKillsSlot",
							"type" : "image",
							"x" : 108,
							"y" : -2,
							"image" : SMALL_VALUE_FILE,
							"children" :
							(
								{"name" : "GuildBestPlayerKillsValue", "type":"text", "text":"53", "x":0, "y":0, "all_align":"center"},
							),
						},
					),
				},

				## BestPlayerDeaths
				{
					"name" : "GuildBestPlayerDeaths", "type" : "text", "x" : 3, "y" : 233, "text" : "BestPlayerDeaths",
					"children" :
					(
						{
							"name" : "GuildBestPlayerDeathsSlot",
							"type" : "image",
							"x" : 100,
							"y" : -2,
							"image" : LARGE_VALUE_FILE,
							"children" :
							(
								{"name" : "GuildBestPlayerDeathsValue", "type":"text", "text":"9999999", "x":0, "y":0, "all_align":"center"},
							),
						},
					),
				},
			),
		},

		###############################################################################################################

		## Ranking Title Bar
		{
			"name":"Ranking_Title_Bar", "type":"horizontalbar", "x":218, "y":10, "width":167,
			"children" :
			(

				{ "name":"Guild_Ranking_Title", "type":"text", "x":8, "y":3, "text":"Posizione e trofei", },	
				
				{
					"name" : "GuildPosition", "type" : "text", "x" : 3, "y" : 31, "text" : "Posizione",
					"children" :
					(
						{
							"name" : "GuildNameSlot",
							"type" : "image",
							"x" : 50,
							"y" : -2,
							"image" : LARGE_VALUE_FILE,
							"children" :
							(
								{"name" : "PositionValue", "type":"text", "text":"0", "x":0, "y":0, "all_align":"center"},
							),
						},
					),
				},			

				{
					"name" : "Trophies", "type" : "text", "x" : 3, "y" : 57, "text" : "Trofei",
					"children" :
					(
						{
							"name" : "GuildNameSlot",
							"type" : "image",
							"x" : 50,
							"y" : -2,
							"image" : LARGE_VALUE_FILE,
							"children" :
							(
								{"name" : "ThropiesValue", "type":"text", "text":"0", "x":0, "y":0, "all_align":"center"},
							),
						},
					),
				},
				
			),
		},
		
		##IMAGE
		{
			"name" : "Image1",
			"type" : "image",
			"x" : 250 + 110,
			"y" : 7,
			"image" : "d:/ymir work/ui/boardimage/test3.tga",
		},
	),
}
