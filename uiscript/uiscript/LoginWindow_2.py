import uiScriptLocale

window = {

	"x" : 0,
	"y" : 0,

	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" :
	(
		{
			"name" : "BackGround",
			"type" : "expanded_image",
			"x" : 0,
			"y" : 0,
			"image" : "d:/locale/it/improveload/bg2.png",
			"x_scale" : float(SCREEN_WIDTH) / 1920.0,
			"y_scale" : float(SCREEN_HEIGHT) / 1080.0,
		},
		{
			"name" : "AnimBackGround",
			"type" : "ani_image",
			"x" : SCREEN_WIDTH/2 - 300,
			"y" : SCREEN_HEIGHT/2 - 300,
			"delay" : 6,
			"images":
			(
				"dunno_/z1.tga",
				"dunno_/z2.tga",		
				"dunno_/z3.tga",
				"dunno_/z3.tga",
			),
		},
	),
}
