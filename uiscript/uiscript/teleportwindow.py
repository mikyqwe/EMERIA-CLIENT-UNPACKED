import uiScriptLocale

ANY_WIDTH		= 900
ANY_HEIGHT	= 599
	
window = {
	"name" : "TeleportSystem",
	"style" : ("movable", "float", "animate",),
	
	"x" : SCREEN_WIDTH - 376 -200 -146 -245,	
	"y" : SCREEN_HEIGHT - 37 - 580,				

	"width" : ANY_WIDTH,
	"height" : ANY_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "window",

			"x" : 0,
			"y" : 0,

			"width" : ANY_WIDTH,
			"height" : ANY_HEIGHT,
			
			"children" :
			(
				{ "name" : "MentaL", "type" : "expanded_image", "style" : ("attach",), "x" : 0, "y" : 0, "image" : "d:/ymir work/ui/mappa.tga" },
				
				{ 
					"name" : "CloseButton", 
					"type" : "button", 
					"x" : ANY_WIDTH -10-10, 
					"y" : 15, 
					"tooltip_text" : "Chiudi", 
					"default_image" : "d:/ymir work/ui/public/close_button_01.sub",	
					"over_image" : "d:/ymir work/ui/public/close_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/close_button_03.sub",
				},
				{ 
					"name" : "CapitaleButton",
					"type" : "button", 
					"x" : ANY_WIDTH -700, 
					"y" : 86, 
					"default_image" : "d:/ymir work/ui/click_a.tga",
					"over_image" : "d:/ymir work/ui/click_h.tga",
					"down_image" : "d:/ymir work/ui/click_n.tga",
				},
				{ 
					"name" : "ValleButton",
					"type" : "button", 
					"x" : ANY_WIDTH -700, 
					"y" : 222, 
					"default_image" : "d:/ymir work/ui/click_a.tga",
					"over_image" : "d:/ymir work/ui/click_h.tga",
					"down_image" : "d:/ymir work/ui/click_n.tga",
				},
				{ 
					"name" : "CovoButton",
					"type" : "button", 
					"x" : ANY_WIDTH -800, 
					"y" : 340, 
					"default_image" : "d:/ymir work/ui/click_a.tga",
					"over_image" : "d:/ymir work/ui/click_h.tga",
					"down_image" : "d:/ymir work/ui/click_n.tga",
				},
				{ 
					"name" : "MonteButton",
					"type" : "button", 
					"x" : ANY_WIDTH -640, 
					"y" : 300, 
					"default_image" : "d:/ymir work/ui/click_a.tga",
					"over_image" : "d:/ymir work/ui/click_h.tga",
					"down_image" : "d:/ymir work/ui/click_n.tga",
				},
				{ 
					"name" : "GrottaButton",
					"type" : "button", 
					"x" : ANY_WIDTH -580, 
					"y" : 215, 
					"default_image" : "d:/ymir work/ui/click_a.tga",
					"over_image" : "d:/ymir work/ui/click_h.tga",
					"down_image" : "d:/ymir work/ui/click_n.tga",
				},
				{ 
					"name" : "DesertoButton",
					"type" : "button", 
					"x" : ANY_WIDTH -580, 
					"y" : 148, 
					"default_image" : "d:/ymir work/ui/click_a.tga",
					"over_image" : "d:/ymir work/ui/click_h.tga",
					"down_image" : "d:/ymir work/ui/click_n.tga",
				},
				{ 
					"name" : "CapoButton",
					"type" : "button", 
					"x" : ANY_WIDTH -590, 
					"y" : 77, 
					"default_image" : "d:/ymir work/ui/click_a.tga",
					"over_image" : "d:/ymir work/ui/click_h.tga",
					"down_image" : "d:/ymir work/ui/click_n.tga",
				},
				{ 
					"name" : "BoscoButton",
					"type" : "button", 
					"x" : ANY_WIDTH -490, 
					"y" : 73, 
					"default_image" : "d:/ymir work/ui/click_a.tga",
					"over_image" : "d:/ymir work/ui/click_h.tga",
					"down_image" : "d:/ymir work/ui/click_n.tga",
				},
				{ 
					"name" : "FantasmaButton",
					"type" : "button", 
					"x" : ANY_WIDTH -460, 
					"y" : 170, 
					"default_image" : "d:/ymir work/ui/click_a.tga",
					"over_image" : "d:/ymir work/ui/click_h.tga",
					"down_image" : "d:/ymir work/ui/click_n.tga",
				},
				{ 
					"name" : "FuocoButton",
					"type" : "button", 
					"x" : ANY_WIDTH -470, 
					"y" : 276, 
					"default_image" : "d:/ymir work/ui/click_a.tga",
					"over_image" : "d:/ymir work/ui/click_h.tga",
					"down_image" : "d:/ymir work/ui/click_n.tga",
				},
				#{ 
					#"name" : "TonantiButton",
					#"type" : "button", 
					#"x" : ANY_WIDTH -125, 
					#"y" : 212, 
					#"default_image" : "d:/ymir work/ui/click_a.tga",
					#"over_image" : "d:/ymir work/ui/click_h.tga",
					#"down_image" : "d:/ymir work/ui/click_n.tga",
				#},
				{ 
					"name" : "TorreButton",
					"type" : "button", 
					"x" : ANY_WIDTH -280, 
					"y" : 258, 
					"default_image" : "d:/ymir work/ui/click_a.tga",
					"over_image" : "d:/ymir work/ui/click_h.tga",
					"down_image" : "d:/ymir work/ui/click_n.tga",
				},
				{ 
					"name" : "EruzioneButton",
					"type" : "button", 
					"x" : ANY_WIDTH -320, 
					"y" : 378, 
					"default_image" : "d:/ymir work/ui/click_a.tga",
					"over_image" : "d:/ymir work/ui/click_h.tga",
					"down_image" : "d:/ymir work/ui/click_n.tga",
				},
			), ## End of board window children			
		},
	),
}
