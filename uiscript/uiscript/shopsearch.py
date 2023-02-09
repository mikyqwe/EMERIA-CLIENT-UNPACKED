import uiScriptLocale
import localeInfo

IMAGE_ROOT = "d:/ymir work/ui/shop/"

WINDOW_WIDTH = 760
WINDOW_HEIGHT = 440

window = {
	"name" : "ShopSearch",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float", "animate",),

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_brown",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT,

			"children" :
			(
				## TitleBar
				{"name" : "TitleBar","type" : "titlebar","style" : ("attach",),"x" : 8,"y" : 8,"width" : WINDOW_WIDTH - 15,"color" : "gray",
					"children" :
					(
						{ 
							"name":"TitleName", "type":"text", "x" : (WINDOW_WIDTH - 15) / 2, "y":4, "text":"Cerca Oggetti", "text_horizontal_align":"center" 
						},
					),
				},

				{
					"name" : "ThiniSearch",
					"type" : "thinboard_circle",
					
					"x" : 165,
					"y" : 30,

        			"width" : 585,
        			"height" : 370,
				},
				{
					"name" : "Animation_Board",
					"type" : "thinboard_circle",
					
					"x" : 165,
					"y" : 30,

        			"width" : 585,
        			"height" : 370,
					"children" :
					(
						{
							"name" : "SearchAnim",
							"type" : "ani_image",
							
							"x" : 175,
							"y" : 190,
							
							"delay" : 6,
						},
					),
					
				},
				{
					"name" : "CategBoard",
					"type" : "thinboard_circle",
					
					"x" : 10,
					"y" : 30,

        			"width" : 150,
        			"height" : 370,
				},
				{
					"name" : "Pagefoot",
					"type" : "thinboard_circle",
					
					"x" : 10,
					"y" : 400,

        			"width" : WINDOW_WIDTH - 20,
        			"height" : 30,
				},
				{
					"name" : "SearchText",
					"type" : "text",

					"x" : 55,
					"y" : 38,

					"text" : "Ricerca Esatta",
					"color" : 0xFFFEE3AE,
				},
				{
					"name" : "ItemNameSlot",
					"type" : "image",
					"x" : 12,
					"y" : 55,
					"image" : IMAGE_ROOT+"insert.png",
					"children" :
					(
						{
							"name" : "ItemNameValue",
							"type" : "editline",
							"x" : 3,
							"y" : 3,
							"width" : 136,
							"height" : 15,
							"input_limit" : 20,
							"text" : "",
						},
					),
				},
				{
					"name" : "Separator",
					"type" : "image",
					"x" : 12,
					"y" : 105,
					"image" : IMAGE_ROOT+"separator.png",
				},
				{
					"name" : "CategoriesText",
					"type" : "text",

					"x" : 60,
					"y" : 85,

					"text" : "Categorie",
					"color" : 0xFFFEE3AE,
				},
				{
					"name" : "search_button",
					"type" : "button",

					"x" : 25,
					"y" : 407,
					"text" : "Cerca",

					"default_image" : IMAGE_ROOT + "button_01_brown.png",
					"over_image" : IMAGE_ROOT + "button_02_brown.png",
					"down_image" : IMAGE_ROOT + "button_03_brown.png",
				},
	
				{
					"name" : "FilterButton",
					"type" : "button",

					"x" : 130,
					"y" : 30,
					"tooltip_text" : "Filtro",

					"default_image" : IMAGE_ROOT + "btn_back_down.dds",
					"over_image" : IMAGE_ROOT + "btn_back_normal.dds",
					"down_image" : IMAGE_ROOT + "btn_back_over.dds",
				},
				{
					"name" : "Scrollbar","type" : "scrollbar_search","x" : 159,"y" : 105, "size" : 265,
				},
	
			),
		},
	),
}