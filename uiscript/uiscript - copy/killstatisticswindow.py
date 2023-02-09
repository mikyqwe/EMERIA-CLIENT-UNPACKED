import uiScriptLocale

LOCALE_PATH = uiScriptLocale.WINDOWS_PATH

window = {
	"name" : "CharacterDetailsWindow",
	"style" : ("float",),
	
	"x" : 274,
	"y" : (SCREEN_HEIGHT - 398) / 2,

	"width" : 200,
	"height" : 364+27+27,
	
	"children" :
	(
		{
			"name" : "MainBoard",
			"type" : "board",
			"style" : ("attach","ltr"),
			
			"x" : 0,
			"y" : 0,

			"width" : 200,
			"height" : 364+27+27,
			
			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 6,
					"y" : 7,

					"width" : 200 - 13,
					
					"children" :
					(
						{ "name" : "TitleName", "type" : "text", "x" : 0, "y" : 0, "text": uiScriptLocale.KILL_STATISTICS_TITLE, "all_align":"center" },
					),
				},
				
				{ 
					"name" : "pvp_title", "type":"horizontalbar", "x":15, "y":32, "width":169, 
					"children" : ( { "name" : "pvp_title_bar", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_PVP_TITLE, "all_align" : "center", }, ),
				},
				
				{
					"name" : "jinno_title_bg", "type" : "thinboard_circle", "x" : 15, "y" : 50+27*0, "width" : 120, "height" : 24,
					
					"children" : ( 
						{ "name" : "jinno_text", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_JINNO, "color": 0xff007bff, "all_align" : "center", },
					),
				},
				{
					"name" : "jinno_kills_bg", "type" : "thinboard_circle", "x" : 15+120+2, "y" : 50+20*0, "width" : 169-120-2, "height" : 24,
					
					"children" : ( 
						{ "name" : "jinno_kills", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
					),
				},	

				{
					"name" : "shinsoo_title_bg", "type" : "thinboard_circle", "x" : 15, "y" : 50+27*1, "width" : 120, "height" : 24,
					
					"children" : ( 
						{ "name" : "shinsoo_text", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_SHINSOO, "color" : 0xffff1723, "all_align" : "center", },
					),
				},
				{
					"name" : "shinsoo_kills_bg", "type" : "thinboard_circle", "x" : 15+120+2, "y" : 50+27*1, "width" : 169-120-2, "height" : 24,
					
					"children" : ( 
						{ "name" : "shinsoo_kills", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
					),
				},		

				{
					"name" : "chunjo_title_bg", "type" : "thinboard_circle", "x" : 15, "y" : 50+27*2, "width" : 120, "height" : 24,
					
					"children" : ( 
						{ "name" : "chunjo_text", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_CHUNJO, "color": 0xffffd903, "all_align" : "center", },
					),
				},
				{
					"name" : "chunjo_kills_bg", "type" : "thinboard_circle", "x" : 15+120+2, "y" : 50+27*2, "width" : 169-120-2, "height" : 24,
					
					"children" : ( 
						{ "name" : "chunjo_kills", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
					),
				},	

				{
					"name" : "total_title_bg", "type" : "thinboard_circle", "x" : 15, "y" : 50+27*3, "width" : 120, "height" : 24,
					
					"children" : ( 
						{ "name" : "total_text", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_TOTAL, "all_align" : "center", },
					),
				},
				{
					"name" : "total_kills_bg", "type" : "thinboard_circle", "x" : 15+120+2, "y" : 50+27*3, "width" : 169-120-2, "height" : 24,
					
					"children" : ( 
						{ "name" : "total_kills", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
					),
				},	

				{
					"name" : "totald_title_bg", "type" : "thinboard_circle", "x" : 15, "y" : 50+27*4, "width" : 120, "height" : 24,
					
					"children" : ( 
						{ "name" : "total_text", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_TOTAL_D, "all_align" : "center", },
					),
				},
				{
					"name" : "total_deaths_bg", "type" : "thinboard_circle", "x" : 15+120+2, "y" : 50+27*4, "width" : 169-120-2, "height" : 24,
					
					"children" : ( 
						{ "name" : "total_deaths", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
					),
				},		

				{
					"name" : "kd_title_bg", "type" : "thinboard_circle", "x" : 15, "y" : 50+27*5, "width" : 120, "height" : 24,
					
					"children" : ( 
						{ "name" : "kd_text", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_KD, "all_align" : "center", },
					),
				},
				{
					"name" : "kd_bg", "type" : "thinboard_circle", "x" : 15+120+2, "y" : 50+27*5, "width" : 169-120-2, "height" : 24,
					
					"children" : ( 
						{ "name" : "kd", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
					),
				},	

				{ 
					"name" : "duels_title", "type":"horizontalbar", "x":15, "y":50+27*6+9, "width":169, 
					"children" : ( { "name" : "duels_title_bar", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_PVPD_TITLE, "all_align" : "center", }, ),
				},
				
				{
					"name" : "duels_t_title_bg", "type" : "thinboard_circle", "x" : 15, "y" : 50+27*7, "width" : 120, "height" : 24,
					
					"children" : ( 
						{ "name" : "duels_t_text", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_DUELS_TOTAL, "all_align" : "center", },
					),
				},
				{
					"name" : "duels_t_bg", "type" : "thinboard_circle", "x" : 15+120+2, "y" : 50+27*7, "width" : 169-120-2, "height" : 24,
					
					"children" : ( 
						{ "name" : "duels_t", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
					),
				},					
				
				{
					"name" : "duels_w_title_bg", "type" : "thinboard_circle", "x" : 15, "y" : 50+27*8, "width" : 120, "height" : 24,
					
					"children" : ( 
						{ "name" : "duels_w_text", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_DUELS_W, "all_align" : "center", },
					),
				},
				{
					"name" : "duels_w_bg", "type" : "thinboard_circle", "x" : 15+120+2, "y" : 50+27*8, "width" : 169-120-2, "height" : 24,
					
					"children" : ( 
						{ "name" : "duels_w", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
					),
				},					
				{
					"name" : "duels_l_title_bg", "type" : "thinboard_circle", "x" : 15, "y" : 50+27*9, "width" : 120, "height" : 24,
					
					"children" : ( 
						{ "name" : "duels_l_text", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_DUELS_L, "all_align" : "center", },
					),
				},
				{
					"name" : "duels_l_bg", "type" : "thinboard_circle", "x" : 15+120+2, "y" : 50+27*9, "width" : 169-120-2, "height" : 24,
					
					"children" : ( 
						{ "name" : "duels_l", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
					),
				},

				{ 
					"name" : "pvm_title", "type":"horizontalbar", "x":15, "y":50+27*10+9, "width":169, 
					"children" : ( { "name" : "pvm_title_bar", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_PVM_TITLE, "all_align" : "center", }, ),
				},
				{
					"name" : "bosses_title_bg", "type" : "thinboard_circle", "x" : 15, "y" : 50+27*11, "width" : 120, "height" : 24,
					
					"children" : ( 
						{ "name" : "bosses_text", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_BOSSES, "all_align" : "center", },
					),
				},
				{
					"name" : "bosses_kills_bg", "type" : "thinboard_circle", "x" : 15+120+2, "y" : 50+27*11, "width" : 169-120-2, "height" : 24,
					
					"children" : ( 
						{ "name" : "bosses_kills", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
					),
				},	
				{
					"name" : "stones_title_bg", "type" : "thinboard_circle", "x" : 15, "y" : 50+27*12, "width" : 120, "height" : 24,
					
					"children" : ( 
						{ "name" : "stones_text", "type" : "text", "x" : 0, "y" : 0, "text" : uiScriptLocale.KILL_STATISTICS_STONES, "all_align" : "center", },
					),
				},
				{
					"name" : "stones_kills_bg", "type" : "thinboard_circle", "x" : 15+120+2, "y" : 50+27*12, "width" : 169-120-2, "height" : 24,
					
					"children" : ( 
						{ "name" : "stones_kills", "type" : "text", "x" : 0, "y" : 0, "text" : "0", "all_align" : "center", },
					),
				},					
			),
		},
	),
}