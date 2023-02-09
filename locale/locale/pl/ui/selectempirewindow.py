window = {
	"name" : "SelectEmpireWindow",
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
			"x_scale" : float(SCREEN_WIDTH) / 1280.0,
			"y_scale" : float(SCREEN_HEIGHT) / 720.0,
			"image" : "create_kiro/empire/background.tga",
			"children" :
			(
				{
					"name" : "background", 
					"type" : "expanded_image",
					"x" : 220,
					"y" : -10,
					"horizontal_align" : "center",
					"vertical_align" : "center",
					"image" : "create_kiro/empire/map.tga",
					"children" :
					(
						{
							"name" : "shinsoo", 
							"type" : "expanded_image",
							"x" : 95,
							"y" : 263,
							"image" : "create_kiro/empire/shinsoo.tga",
						},
						{
							"name" : "jinno", 
							"type" : "expanded_image",
							"x" : 390,
							"y" : 100,
							"image" : "create_kiro/empire/jinno.tga",
						},
						{
							"name" : "sonyong", 
							"type" : "expanded_image",
							"x" : 70,
							"y" : 65,
							"image" : "create_kiro/empire/sonyong.tga",
						},
					),
				},
				{
					"name" : "empirename", 
					"type" : "expanded_image",
					"x" : 157,
					"y" : -235,
					"horizontal_align" : "left",
					"vertical_align" : "center",
					"image" : "create_kiro/empire/shinsoo_2.tga",
				},
				{
					"name" : "board", 
					"type" : "expanded_image",
					"x" : 70,
					"y" : -20,
					"horizontal_align" : "left",
					"vertical_align" : "center",
					"image" : "create_kiro/empire/board.tga",
					"children" :
					(
						{
							"name" : "desc", 
							"type" : "expanded_image",
							"x" : 9,
							"y" : 15,
							"horizontal_align" : "center",
							"vertical_align" : "center",
							"image" : "create_kiro/empire/jinno_1.tga",
						},
					),
				},
				{
					"name" : "empire",
					"type" : "image",
					"x" : 0,
					"y" : 60,
					"horizontal_align" : "center",
					"vertical_align" : "bottom",
					"image" : "create_kiro/empire/jinno_0.tga",
				},
				{
					"name" : "select_button",
					"type" : "button",
					"x" : 320,
					"y" : 75,
					"horizontal_align" : "right",
					"vertical_align" : "bottom",
					"default_image" : "create_kiro/empire/select_0.tga",
					"over_image" :  "create_kiro/empire/select_1.tga",
					"down_image" : "create_kiro/empire/select_2.tga",
				},
			),
		},
	),
}
