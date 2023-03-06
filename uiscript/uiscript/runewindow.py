import uiScriptLocale
import item

NEW_EQUIPMENT_START_INDEX = item.NEW_EQUIPMENT_SLOT_START

window = {
	"name" : "RuneWindow",

	## 600 - (width + 오른쪽으로 부터 띄우기 24 px)
	"x" : SCREEN_WIDTH - 175 - 295,
	"y" : SCREEN_HEIGHT - 37 - 575,

	"style" : ("movable", "float", "animate",),

	"width" : 295,
	"height" : 195 + 47 + 42,

	"children" :
	(
		## Inventory, Equipment Slots
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 295,
			"height" : 195 + 47 + 42,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : 285,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":150, "y":3, "text": "Mozaic de rune", "text_horizontal_align":"center" },
					),
				},
				

				## Equipment Slot
				{
					"name" : "Equipment_Base",
					"type" : "image",

					"x" : 10,
					"y" : 33,

					"image" : "d:/ymir work/ui/bg_runes.jpg",

					"children" :
					(

						{
							"name" : "RuneSlot",
							"type" : "slot",

							"x" : 3,
							"y" : 3,

							"width" : 295,
							"height" : 195 + 47 + 42,

							"slot" : (
										#	EQ_RUNE = WHITE
										{"index":NEW_EQUIPMENT_START_INDEX+9, "x":120, "y":14, "width":32, "height":32},
										{"index":NEW_EQUIPMENT_START_INDEX+10, "x":48, "y":56, "width":32, "height":32},
										{"index":NEW_EQUIPMENT_START_INDEX+11, "x":188, "y":147, "width":32, "height":32},
										{"index":NEW_EQUIPMENT_START_INDEX+12, "x":48, "y":146, "width":32, "height":32},
										{"index":NEW_EQUIPMENT_START_INDEX+13, "x":120, "y":188, "width":32, "height":32},
										{"index":NEW_EQUIPMENT_START_INDEX+14, "x":188, "y":56, "width":32, "height":32},
									),
						},
                    ),
                },
			),
		},
	),
}

