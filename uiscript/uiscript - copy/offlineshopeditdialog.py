import uiScriptLocale
window = {
	"name": "OfflineShopEditDialog",
	"x": SCREEN_WIDTH - 400,
	"y": 10,
	"style": ("movable", "float"),
	"width": 280,
	"height": 328+10,
	"children":
	(
		{
			"name": "board",
			"type": "board",
			"style": ("attach",),
			"x": 0,
			"y": 0,
			"width": 280,
			"height": 328+10,
			"children":
			(
				{
					"name": "TitleBar",
					"type": "titlebar",
					"style": ("attach",),
					"x": 8,
					"y": 8,
					"width": 265,
					"color": "gray",
					"children":
					(
						{
							"name": "TitleName",
							"type": "text",
							"x": 135,
							"y": 4,
							"text": uiScriptLocale.SHOP_TITLE,
							"text_horizontal_align": "center"
						},
					)
				},
				{
					"name": "ItemSlot",
					"type": "grid_table",
					"x": 12,
					"y": 34+13,
					"start_index": 0,
					"x_count": 8,
					"y_count": 8,
					"x_step": 32,
					"y_step": 32,
					"image": "d:/ymir work/ui/public/Slot_Base.sub"
				},
				{
					"name": "TimeLeft",
					"type": "text",
					"x": (280 / 2) - 90,
					"y": 328 - 15,
					"text": "Time Left: 0 Seconds",
				},
				{
					"name": "LocationText",
					"type": "text",
					"x": 15,
					"y": 33,
					"text": "No Shop Online / Not In This Core",
				},
				# {
					# 'name': 'Seen',
					# 'type': 'button',
					# 'x': 150,
					# 'y': 295,
					# 'text': "Görüntülenme",
					# 'default_image': 'd:/ymir work/ui/public/parameter_slot_04.sub',
					# 'over_image': 'd:/ymir work/ui/public/parameter_slot_04.sub',
					# 'down_image': 'd:/ymir work/ui/public/parameter_slot_04.sub',

					# "children" :
					# (
						# {
							# "name" : "SeenText",
							# "type" : "text",

							# "x" : 3,
							# "y" : 3,

							# "width" : 30,
							# "height" : 18,
						# },
					# ),
				# },
			)
		},
	)
}
