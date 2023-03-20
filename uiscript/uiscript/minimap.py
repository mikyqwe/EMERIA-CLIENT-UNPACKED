ROOT = "d:/ymir work/ui/minimap/"
import uiScriptLocale
import app

window = {
	"name" : "MiniMap",

	"x" : SCREEN_WIDTH - 136,
	"y" : 0,

	"width" : 136,
	"height" : 137,

	"children" :
	(
		## OpenWindow
		{
			"name" : "OpenWindow",
			"type" : "window",

			"x" : 0,
			"y" : 0,

			"width" : 136,
			"height" : 137,

			"children" :
			(
				{
					"name" : "OpenWindowBGI",
					"type" : "image",
					"x" : 0,
					"y" : 0,
					"image" : ROOT + "minimap.sub",
				},
				## DUNGEON_INFO
				
				## MiniMapWindow
				{
					"name" : "MiniMapWindow",
					"type" : "window",

					"x" : 4,
					"y" : 5,

					"width" : 128,
					"height" : 128,
				},
				{
					"name" : "BiologButton",
					"type" : "button",
					"x" : 50,
					"y" : 118,
					"default_image" : "d:/ymir work/ui/minimap/biolog.tga",
					"over_image" : "d:/ymir work/ui/minimap/biolog_over.tga",
					"down_image" : "d:/ymir work/ui/minimap/biolog_down.tga",
					"tooltip_text": "|cffF4B418Biolog",
				},
				{
					"name" : "DungeonInfoShowButton",
					"type" : "button",

					"x" : 26,
					"y" : 114,

					"default_image" : "d:/ymir work/ui/game/dungeon_info/minimap/" + "minimap_dungeon_info_default.tga",
					"over_image" : "d:/ymir work/ui/game/dungeon_info/minimap/" + "minimap_dungeon_info_over.tga",
					"down_image" : "d:/ymir work/ui/game/dungeon_info/minimap/" + "minimap_dungeon_info_down.tga",
				},
				## HUNTING_BUTTON
				# {
					# "name" : "HuntingButton",
					# "type" : "button",
					# "x" : 75,
					# "y" : 118,
					# "default_image" : "d:/ymir work/ui/minimap/hunter.tga",
					# "over_image" : "d:/ymir work/ui/minimap/hunter_over.tga",
					# "down_image" : "d:/ymir work/ui/minimap/hunter_down.tga",
					# "tooltip_text" : "|cffF4B418Taglie",
				# },
				# ## RANKING_BUTTON
				# {
					# "name" : "RankingsButton",
					# "type" : "button",
					# "x" : 112,
					# "y" : 45,
					# "default_image" : "d:/ymir work/ui/minimap/rank.tga",
					# "over_image" : "d:/ymir work/ui/minimap/rank_over.tga",
					# "down_image" : "d:/ymir work/ui/minimap/rank_down.tga",
					# "tooltip_text" : "|cffF4B418Rank",
				# },
				## ScaleUpButton
				{
					"name" : "ScaleUpButton",
					"type" : "button",

					"x" : 101,
					"y" : 116,

					"default_image" : ROOT + "minimap_scaleup_default.sub",
					"over_image" : ROOT + "minimap_scaleup_over.sub",
					"down_image" : ROOT + "minimap_scaleup_down.sub",
				},
				## ScaleDownButton
				{
					"name" : "ScaleDownButton",
					"type" : "button",

					"x" : 115,
					"y" : 103,

					"default_image" : ROOT + "minimap_scaledown_default.sub",
					"over_image" : ROOT + "minimap_scaledown_over.sub",
					"down_image" : ROOT + "minimap_scaledown_down.sub",
				},
				# {
					# "name" : "Evenimente",
					# "type" : "button",

					# "x" : -45,
					# "y" : 12,

					# "tooltip_text" : "Calendarul Evenimentelor",

					# "default_image" : "butoane/calendar1.tga",
					# "over_image" : "butoane/calendar2.tga",
					# "down_image" : "butoane/calendar1.tga",
				# },
				## MiniMapHideButton
				{
					"name" : "MiniMapHideButton",
					"type" : "button",

					"x" : 111,
					"y" : 6,

					"default_image" : ROOT + "minimap_close_default.sub",
					"over_image" : ROOT + "minimap_close_over.sub",
					"down_image" : ROOT + "minimap_close_down.sub",
				},
				## AtlasShowButton
				{
					"name" : "AtlasShowButton",
					"type" : "button",

					"x" : 12,
					"y" : 12,

					"default_image" : ROOT + "atlas_open_default.sub",
					"over_image" : ROOT + "atlas_open_over.sub",
					"down_image" : ROOT + "atlas_open_down.sub",
				},
				## ch buttons
				{
					"name" : "ch_button_0",
					"type" : "button",

					"x" : -2,
					"y" : 36,


					"default_image" : "btn/discord/ch1.png",
					"over_image" : "btn/discord/ch1_over.png",
					"down_image" : "btn/discord/ch1_down.png",
					"tooltip_text": "|cffF4B418CH 1",
				},
				{
					"name" : "ch_button_1",
					"type" : "button",

					"x" : -6,
					"y" : 56,


					"default_image" : "btn/discord/ch2.png",
					"over_image" : "btn/discord/ch2_over.png",
					"down_image" : "btn/discord/ch2_down.png",
					"tooltip_text": "|cffF4B418CH 2",
				},
				{
					"name" : "ch_button_2",
					"type" : "button",

					"x" : -4,
					"y" : 76,

					"default_image" : "btn/discord/ch3.png",
					"over_image" : "btn/discord/ch3_over.png",
					"down_image" : "btn/discord/ch3_down.png",
					"tooltip_text": "|cffF4B418CH 3",
				},
				{
					"name" : "ch_button_3",
					"type" : "button",

					"x" : 3,
					"y" : 96,

					"default_image" : "btn/discord/ch4.png",
					"over_image" : "btn/discord/ch4_over.png",
					"down_image" : "btn/discord/ch4_down.png",
					"tooltip_text": "|cffF4B418CH 4",
				 },
				## Discord Button
				{
					"name" : "Discord",
					"type" : "button",

					"x" : 75,
					"y" : 118,

					"default_image" : "btn/discord/d_open_default.png",
					"over_image" : "btn/discord/d_open_over.png",
					"down_image" : "btn/discord/d_open_down.png",
					"tooltip_text" : "Discord",
				},
				## Wiki
				{
					"name" : "Wiki",
					"type" : "button",

					"x" : 56,
					"y" : 1,

					"default_image" : "d:/ymir work/ui/minimap/wiki.tga",
					"over_image" : "d:/ymir work/ui/minimap/wiki1.tga",
					"down_image" : "d:/ymir work/ui/minimap/wiki2.tga",
				},				
				## ServerInfo
				{
					"name" : "ServerInfo",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70,
					"y" : 140,

					"text" : "",
				},
				## MailBox
				{
					"name" : "MailBoxButton",
					"type" : "button",

					"x" : 110,
					"y" : 30,

					"default_image" : "d:/ymir work/ui/game/mailbox/post_minimap.sub",
					"over_image" : "d:/ymir work/ui/game/mailbox/post_minimap.sub",
					"down_image" : "d:/ymir work/ui/game/mailbox/post_minimap.sub",
				},
				{
					"name" : "MailBoxEffect",
					"type" : "ani_image",
						
					"x" : 110,
					"y" : 30,
						
					"delay" : 6,

					"images" :
					(
						"d:/ymir work/ui/game/mailbox/minimap_flash/2.sub",
						"d:/ymir work/ui/game/mailbox/minimap_flash/3.sub",
						"d:/ymir work/ui/game/mailbox/minimap_flash/4.sub",
						"d:/ymir work/ui/game/mailbox/minimap_flash/5.sub",
						"d:/ymir work/ui/game/mailbox/minimap_flash/4.sub",
						"d:/ymir work/ui/game/mailbox/minimap_flash/3.sub",
						"d:/ymir work/ui/game/mailbox/minimap_flash/2.sub",
						"d:/ymir work/ui/game/mailbox/minimap_flash/1.sub",
						"d:/ymir work/ui/game/mailbox/minimap_flash/1.sub",
						"d:/ymir work/ui/game/mailbox/minimap_flash/1.sub",
						"d:/ymir work/ui/game/mailbox/minimap_flash/1.sub",
						"d:/ymir work/ui/game/mailbox/minimap_flash/1.sub",
					),
				},
				# ## PlayerCount
				# {
					# "name" : "PlayerCount",
					# "type" : "text",
					
					# "text_horizontal_align" : "center",

					# "outline" : 1,

					# "x" : 70,
					# "y" : 173,

					# "text" : "",
				# },
				# ## ShopCount
				# {
					# "name" : "ShopCount",
					# "type" : "text",
					
					# "text_horizontal_align" : "center",

					# "outline" : 1,

					# "x" : 70,
					# "y" : 186,

					# "text" : "",
				# },				
				## PositionInfo
				{
					"name" : "PositionInfo",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70,
					"y" : 160,

					"text" : "",
				},
				## RenderInfo
				{
					"name" : "RenderInfo",
					"type" : "text",
					
					"text_horizontal_align" : "center",	

					"outline" : 1,

					"x" : 95,
					"y" : 160,

					"text" : "",
				},
				## ObserverCount
				{
					"name" : "ObserverCount",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70,
					"y" : 180,

					"text" : "",
				},
				
			),
		},
		{
			"name" : "CloseWindow",
			"type" : "window",

			"x" : 0,
			"y" : 0,

			"width" : 132,
			"height" : 48,

			"children" :
			(
				## ShowButton
				{
					"name" : "MiniMapShowButton",
					"type" : "button",

					"x" : 100,
					"y" : 4,

					"default_image" : ROOT + "minimap_open_default.sub",
					"over_image" : ROOT + "minimap_open_default.sub",
					"down_image" : ROOT + "minimap_open_default.sub",
				},
			),
		},
	),
}