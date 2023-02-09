import localeInfo


MAINBOARD_WIDTH = 515
MAINBOARD_HEIGHT = 560

LEFTBOARD_WIDTH = 291
LEFTBOARD_HEIGHT = 370
LEFTBOARD_X = 13
LEFTBOARD_Y = 36

window = {
	"name" : "GuildWarStaticWindow",
	"style" : ("movable", "float", "animate",),

	"x" : 0,
	"y" : 0,

	"width" : MAINBOARD_WIDTH,
	"height" : MAINBOARD_HEIGHT,

	"children" :
	(
		{
        	"name" : "RightThinboard",
        	"type" : "image",
        	"style" : ("not_pick",),
        	"x" : 10,
        	"y" : 10,
        	"image" : "d:/ymir work/ui/game/guild_war/right_thin.tga",
			"alpha" : 0.7,
        	"children" :
        	(
        		{
        			"name" : "RightTitle",
        			"type" : "image",
        			"style" : ("not_pick",),
        			"x" : 12,
        			"y" : 150,
        			"image" : "d:/ymir work/ui/game/guild_war/right_title.tga",
					"alpha" : 0.7,
        			"children":
        			(
        				{
        					"name" : "king_icon",
        					"type" : "image",
        					"style" : ("not_pick",),
        					"x" : 5,
        					"y" : 2,
        					"image" : "d:/ymir work/ui/game/guild_war/king_icon.tga",
							"alpha" : 0.7,
        				},
        				{
        					"name" : "name_field",
        					"type" : "text",
        					"style" : ("not_pick",),
        					"x" : 75,
        					"y" : -5,
        					"text" : localeInfo.GUILDWAR_STATIC_NAME,
        					"vertical_align":"center",
        				},
        				{
        					"name" : "kill_field",
        					"type" : "text",
        					"style" : ("not_pick",),
        					"x" : 165,
        					"y" : -5,
        					"fontname":"Tahoma:11",
        					"text" : localeInfo.GUILDWAR_STATIC_KILL,
        					"vertical_align":"center",
        					
        				},
        				{
        					"name" : "dead_field",
        					"type" : "text",
        					"style" : ("not_pick",),
        					"x" : 215,
        					"y" : -5,
        					"fontname":"Tahoma:11",
        					"text" : localeInfo.GUILDWAR_STATIC_DEAD,
        					"vertical_align":"center",
        
        				},
        				{
        					"name" : "dmg_field",
        					"type" : "text",
        					"style" : ("not_pick",),
        					"x" : 255,
        					"y" : -5,
        					"fontname":"Tahoma:11",
        					"text" : localeInfo.GUILDWAR_STATIC_DMG,
        					"vertical_align":"center"
        				},
        				{
        					"name" : "guild_field",
        					"type" : "text",
        					"style" : ("not_pick",),
        					"x" : 355,
        					"y" : -5,
        					"fontname":"Tahoma:11",
        					"text" : localeInfo.GUILDWAR_STATIC_GUILD,
        					"vertical_align":"center"
        				},
        				{
        					"name" : "camera_field",
        					"type" : "text",
        					"style" : ("not_pick",),
        					"x" : 410,
        					"y" : -5,
        					"fontname":"Tahoma:11",
        					"text" : localeInfo.GUILDWAR_STATIC_CAMERA,
        					"vertical_align":"center"
        				},
        			),
        		},
        
        		{
        			"name" : "RightMenu",
        			"type" : "image",
        			"style" : ("not_pick",),
        			"x" : 12,
        			"y" :150+26,
        			"image" : "d:/ymir work/ui/game/guild_war/right_list.tga",
					"alpha" : 0.7,
        			"children":
        			(
        				{
        					"name" : "ListBoxNEW",
        					"type" : "listboxex",
        					"style" : ("not_pick",),
        					"x" : 0,
        					"y" : 0,
        					"width" : 400,
        					"height" : 38*9,
        					#"viewcount" : 4,
        				},
        			),
        		},
        
        		{
        			"name" : "back_btn",
        			"type" : "button",
        			"x" : 170,
        			"y" :470,
        			"default_image" : "d:/ymir work/ui/public/small_button_01.sub",
        			"over_image" : "d:/ymir work/ui/public/small_button_02.sub",
        			"down_image" : "d:/ymir work/ui/public/small_button_03.sub",
        			"text":"<<",
					"alpha" : 0.5,
        		},
        
        		{
        			"name" : "RightMenu",
        			"type" : "slotbar",
        			"style" : ("not_pick",),
        			"x" : 170+5+40,
        			"y" : 470,
        			"width" : 40,
        			"height" : 18,
        			"children":
        			(
        				{
        					"name" : "page_text",
        					"type" : "text",
        					"x" : 12,
        					"y" : -5,
        					"text" : "1/1",
        					"vertical_align":"center"
        				},
        			),
        		},
        
        		{
        			"name" : "next_btn",
        			"type" : "button",
        			"x" : 170+5+40+5+40,
        			"y" :470,
        			"default_image" : "d:/ymir work/ui/public/small_button_01.sub",
        			"over_image" : "d:/ymir work/ui/public/small_button_02.sub",
        			"down_image" : "d:/ymir work/ui/public/small_button_03.sub",
        			"text":">>",
					"alpha" : 0.5,
        		},
        
        		{ "name" : "mark_0", "type" : "mark", "x" : 85, "y" : 5 },
        		{
        			"name" : "guild_0_name",
        			"type" : "text",
        			"style" : ("not_pick",),
        			"x" : 85,
        			"y" : 25,
        			"fontname":"Comic Sans MS:20",
        			"text" : "Noname(0)",
        			"text_horizontal_align":"center",
        		},
        
        		{
        			"name" : "guild_0_score",
        			"type" : "text",
        			"style" : ("not_pick",),
        			"x" : 180,
        			"y" : 20,
        			"fontname":"Comic Sans MS:30",
        			"text" : "0",
        			"text_horizontal_align":"center",
        		},
        
        		{
        			"name" : "score_img",
        			"type" : "image",
        			"style" : ("not_pick",),
        			"x" : 210,
        			"y" : 5,
        			"image":"d:/ymir work/ui/public/battle/banner_active.sub",
					"alpha" : 0.7,
        		},
        
        		{
        			"name" : "guild_1_score",
        			"type" : "text",
        			"style" : ("not_pick",),
        			"x" : 295,
        			"y" : 20,
        			"fontname":"Comic Sans MS:30",
        			"text" : "0",
        			"text_horizontal_align":"center",
        		},
        
        		{ "name" : "mark_1", "type" : "mark", "x" : 390, "y" : 5 },
        		{
        			"name" : "guild_1_name",
        			"type" : "text",
        			"style" : ("not_pick",),
        			"x" : 390,
        			"y" : 25,
        			"fontname":"Comic Sans MS:20",
        			"text" : "Noname(0)",
        			"text_horizontal_align":"center",
        		},
        
        		{
        			"name" : "against",
        			"type" : "text",
        			"style" : ("not_pick",),
        			"x" : 240,
        			"y" : 70,
        			"fontname":"Comic Sans MS:17",
        			"text" : "-",
        			"text_horizontal_align":"center",
        		},
        		
        		{
        			"name" : "observer",
        			"type" : "text",
        			"style" : ("not_pick",),
        			"x" : 210,
        			"y" : 90,
        			"fontname":"Comic Sans MS:17",
        			"text" : "-",
        			"text_horizontal_align":"left",
        		},
        
        	),
        },
	),
}

