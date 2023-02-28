import uiScriptLocale

MAIN_PATH = "d:/ymir work/ui/intro_elendos/"
COMMON_PATH = "d:/ymir work/ui/intro_elendos/common/"
BUTTON_PATH = "d:/ymir work/ui/intro_elendos/button/"


LEFT_WINDOW_X = -403
RIGHT_WINDOW_X = 403
ROTATE_BUTTON_Y = 600
ROTATE_BUTTON_LEFT_X = -200
ROTATE_BUTTON_RIGHT_X = 200

if SCREEN_HEIGHT < 1000:
	ROTATE_BUTTON_Y = 480

if SCREEN_WIDTH < 1200:
	LEFT_WINDOW_X = -350
	RIGHT_WINDOW_X = 350
	ROTATE_BUTTON_LEFT_X = -140
	ROTATE_BUTTON_RIGHT_X = 140

window = {
    "name" : "SelectCharacterWindow",
    "x" : 0, "y" : 0,
    "width" : SCREEN_WIDTH, "height" : SCREEN_HEIGHT,
    "children" : (
        {
            "name" : "BackgroundImage", "type" : "expanded_image",
            "x" : 0, "y" : 0,
            "x_scale" : float(SCREEN_WIDTH) / 1920.0, "y_scale" : float(SCREEN_HEIGHT) / 1080.0,
            "image" : MAIN_PATH + "background_char.jpg",
        },
		{ "name" : "video_layer",  "type" : "window", "x" : 0, "y" : 0, "width" : SCREEN_WIDTH, "height" : SCREEN_HEIGHT, },
        {
            "name" : "middle_window", "type" : "window",
            "x" : 0, "y" : 0,  "horizontal_align" : "center", "vertical_align" : "center",
            "width" : 460, "height" : 650,
            # "children" : (
				# {
					# "name" : "RotateLeftButton", "type" : "button",
					# "x" : ROTATE_BUTTON_LEFT_X, "y" : ROTATE_BUTTON_Y, "horizontal_align" : "center",
					# "default_image" : BUTTON_PATH + "button_rotate_left_normal.sub",
					# "over_image" : BUTTON_PATH + "button_rotate_left_hover.sub",
					# "down_image" : BUTTON_PATH + "button_rotate_left_down.sub",
				# },
				# {
					# "name" : "RotateRightButton", "type" : "button",
					# "x" : ROTATE_BUTTON_RIGHT_X, "y" : ROTATE_BUTTON_Y, "horizontal_align" : "center",
					# "default_image" : BUTTON_PATH + "button_rotate_right_normal.sub",
					# "over_image" : BUTTON_PATH + "button_rotate_right_hover.sub",
					# "down_image" : BUTTON_PATH + "button_rotate_right_down.sub",
				# },
            # ),
        },
        {
            "name" : "left_window", "type" : "window",
            "x" : LEFT_WINDOW_X, "y" : 0,  "horizontal_align" : "center", "vertical_align" : "center",
            "width" : 330, "height" : 500,
            "children" : (
				{
					"name" : "CharacterSlotTitleBar", "type" : "image",
					"x" : 0, "y" : 0, "image" : MAIN_PATH + "char_left_titlebar.tga",
					"children" : (
						{ "name" : "CharacterSlotTitleBarText", "type" : "text", "x" : 65, "y" : 29, "color" : 0xff9a8b70, "fontsize" : "LARGE", "text" : "Select Class" },
					),
				},
				{
					"name" : "CharacterWarrior", "type" : "radio_button",
					"x" : 0, "y" : 68 + 75 * 0, "horizontal_align" : "center",
					"default_image" : COMMON_PATH + "character_slot_normal.sub",
					"over_image" : COMMON_PATH + "character_slot_hover.sub",
					"down_image" : COMMON_PATH + "character_slot_down.sub",
					"children" : (
						{ "name" : "CharacterSlot0_Icon", "type" : "image", "x" : 15, "y" : 18, "image" : COMMON_PATH + "character_icon_warrior.sub" },
						{ "name" : "CharacterSlot0_Text1", "type" : "text", "x" : 80, "y" : 20, "fontsize" : "LARGE", "color" : 0xffbeaa87, "text" : "Warrior" },
						{ "name" : "CharacterSlot0_Text2", "type" : "text", "x" : 80, "y" : 35, "color" : 0xff6f6f6f, "text" : "Body | Mental" },
					),
				},
				{
					"name" : "CharacterAssassin", "type" : "radio_button",
					"x" : 0, "y" : 68 + 75 * 1, "horizontal_align" : "center",
					"default_image" : COMMON_PATH + "character_slot_normal.sub",
					"over_image" : COMMON_PATH + "character_slot_hover.sub",
					"down_image" : COMMON_PATH + "character_slot_down.sub",
					"children" : (
						{ "name" : "CharacterSlot1_Icon", "type" : "image", "x" : 15, "y" : 18, "image" : COMMON_PATH + "character_icon_assassin.sub" },
						{ "name" : "CharacterSlot1_Text1", "type" : "text", "x" : 80, "y" : 20, "fontsize" : "LARGE", "color" : 0xffbeaa87, "text" : "Ninja" },
						{ "name" : "CharacterSlot1_Text2", "type" : "text", "x" : 80, "y" : 35, "color" : 0xff6f6f6f, "text" : "Assassin | Archer" },
					),
				},
				{
					"name" : "CharacterSura", "type" : "radio_button",
					"x" : 0, "y" : 68 + 75 * 2, "horizontal_align" : "center",
					"default_image" : COMMON_PATH + "character_slot_normal.sub",
					"over_image" : COMMON_PATH + "character_slot_hover.sub",
					"down_image" : COMMON_PATH + "character_slot_down.sub",
					"children" : (
						{ "name" : "CharacterSlot2_Icon", "type" : "image", "x" : 15, "y" : 18, "image" : COMMON_PATH + "character_icon_sura.sub" },
						{ "name" : "CharacterSlot2_Text1", "type" : "text", "x" : 80, "y" : 20, "fontsize" : "LARGE", "color" : 0xffbeaa87, "text" : "Sura" },
						{ "name" : "CharacterSlot2_Text2", "type" : "text", "x" : 80, "y" : 35, "color" : 0xff6f6f6f, "text" : "Black Magic | Weapon" },
					),
				},
				{
					"name" : "CharacterShaman", "type" : "radio_button",
					"x" : 0, "y" : 68 + 75 * 3, "horizontal_align" : "center",
					"default_image" : COMMON_PATH + "character_slot_normal.sub",
					"over_image" : COMMON_PATH + "character_slot_hover.sub",
					"down_image" : COMMON_PATH + "character_slot_down.sub",
					"children" : (
						{ "name" : "CharacterSlot3_Icon", "type" : "image", "x" : 15, "y" : 18, "image" : COMMON_PATH + "character_icon_shaman.sub" },
						{ "name" : "CharacterSlot3_Text1", "type" : "text", "x" : 80, "y" : 20, "fontsize" : "LARGE", "color" : 0xffbeaa87, "text" : "Shaman" },
						{ "name" : "CharacterSlot3_Text2", "type" : "text", "x" : 80, "y" : 35, "color" : 0xff6f6f6f, "text" : "Dragon | Healer" },
					),
				},
            ),
        },
        {
            "name" : "right_window", "type" : "window",
            "x" : RIGHT_WINDOW_X, "y" : 0,  "horizontal_align" : "center", "vertical_align" : "center",
            "width" : 330, "height" : 500,
            "children" : (
				{
					"name" : "ContainerCustomization", "type" : "image",
					"x" : 0, "y" : 0,
					"image" : MAIN_PATH + "char_create_board.tga",
					"children" : (
						{ "name" : "TitleTextContainerCustomization", "type" : "text", "x" : 65, "y" : 29, "color" : 0xff9a8b70, "fontsize" : "LARGE", "text" : "Costumization" },
						
						
						{ "name" : "SelectGenreText", "type" : "text", "x" : -77, "y" : -11, "all_align" : "center", "color" : 0xff9a8b70, "fontsize" : "LARGE", "text" : "Select Genre" },
						
						{
							"name" : "SelectGenre0", "type" : "radio_button",
							"x" : 35, "y" : 142,
							"default_image" : BUTTON_PATH + "button_gender_male_normal.sub",
							"over_image" : BUTTON_PATH + "button_gender_male_hover.sub",
							"down_image" : BUTTON_PATH + "button_gender_male_down.sub",
						},
						{
							"name" : "SelectGenre1", "type" : "radio_button",
							"x" : 95, "y" : 142,
							"default_image" : BUTTON_PATH + "button_gender_female_normal.sub",
							"over_image" : BUTTON_PATH + "button_gender_female_hover.sub",
							"down_image" : BUTTON_PATH + "button_gender_female_down.sub",
						},
						
						{ "name" : "SelectSkinText", "type" : "text", "x" : 77, "y" : -11, "all_align" : "center", "color" : 0xff9a8b70, "fontsize" : "LARGE", "text" : "Select Skin"},
						
						{
							"name" : "SelectSkin0", "type" : "radio_button",
							"x" : 193, "y" : 142,
							"default_image" : BUTTON_PATH + "button_skin_1_normal.sub",
							"over_image" : BUTTON_PATH + "button_skin_1_hover.sub",
							"down_image" : BUTTON_PATH + "button_skin_1_down.sub",
						},
						{
							"name" : "SelectSkin1", "type" : "radio_button",
							"x" : 253, "y" : 142,
							"default_image" : BUTTON_PATH + "button_skin_2_normal.sub",
							"over_image" : BUTTON_PATH + "button_skin_2_hover.sub",
							"down_image" : BUTTON_PATH + "button_skin_2_down.sub",
						},
					),
				},
				
				
				{
					"name" : "ContainerCharacterName", "type" : "image",
					"x" : 0, "y" :226,
					"image" : MAIN_PATH + "char_create_board.tga",
					"children" : (
						{ "name" : "TitleTextCharacterName", "type" : "text", "x" : 65, "y" : 29, "color" : 0xff9a8b70, "fontsize" : "LARGE", "text" : "Character Name" },
						
						{
							"name" : "InputSlotName", "type" : "image",
							"x" : 35, "y" : 84,
							"image" : COMMON_PATH + "input_large.sub",
							"children" :
							(
								{
									"name" : "InputName", "type" : "editline",
									"input_limit" : 24, "text" : "Enter Character Name...",
									"x" : 13, "y" : 13, "width" : 250, "height" : 14,
								},
							),
						},
						{
							"name" : "CreateCharacterButton", "type" : "button",
							"x" : 35, "y" : 148,
							"default_image" : BUTTON_PATH + "button_char_create_normal.sub",
							"over_image" : BUTTON_PATH + "button_char_create_hover.sub",
							"down_image" : BUTTON_PATH + "button_char_create_down.sub",
						},
					),
				},
				
				{
					"name" : "ExitButton", "type" : "button",
					"x" : 0, "y" : 459, "horizontal_align" : "center",
					"default_image" : BUTTON_PATH + "button_back_normal.sub",
					"over_image" : BUTTON_PATH + "button_back_hover.sub",
					"down_image" : BUTTON_PATH + "button_back_down.sub",
				},
            ),
        },
    ),
}