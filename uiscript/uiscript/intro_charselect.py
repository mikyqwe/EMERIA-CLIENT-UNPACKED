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
            "children" : (
				{
					"name" : "RotateLeftButton", "type" : "button",
					"x" : ROTATE_BUTTON_LEFT_X, "y" : ROTATE_BUTTON_Y, "horizontal_align" : "center",
					"default_image" : BUTTON_PATH + "button_rotate_left_normal.sub",
					"over_image" : BUTTON_PATH + "button_rotate_left_hover.sub",
					"down_image" : BUTTON_PATH + "button_rotate_left_down.sub",
				},
				{
					"name" : "RotateRightButton", "type" : "button",
					"x" : ROTATE_BUTTON_RIGHT_X, "y" : ROTATE_BUTTON_Y, "horizontal_align" : "center",
					"default_image" : BUTTON_PATH + "button_rotate_right_normal.sub",
					"over_image" : BUTTON_PATH + "button_rotate_right_hover.sub",
					"down_image" : BUTTON_PATH + "button_rotate_right_down.sub",
				},
            ),
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
						{ "name" : "CharacterSlotTitleBarText", "type" : "text", "x" : 65, "y" : 29, "color" : 0xff9a8b70, "fontsize" : "LARGE", "text" : "Select Your Character" },
					),
				},
				{
					"name" : "CharacterSlotEmpty", "type" : "button",
					"x" : 0, "y" : 0, "horizontal_align" : "center",
					"default_image" : COMMON_PATH + "character_slot_normal.sub",
					"over_image" : COMMON_PATH + "character_slot_hover.sub",
					"down_image" : COMMON_PATH + "character_slot_down.sub",
					"children" : (
						{ "name" : "CharacterSlot0_Icon", "type" : "image", "x" : 15, "y" : 18, "image" : COMMON_PATH + "character_icon_empty.sub" },
						{ "name" : "CharacterSlot0_Text1", "type" : "text", "x" : 80, "y" : 27, "fontsize" : "LARGE", "color" : 0xffbeaa87, "text" : "Create Character" },
					),
				},
				{
					"name" : "CharacterSlot0", "type" : "radio_button",
					"x" : 0, "y" : 0, "horizontal_align" : "center",
					"default_image" : COMMON_PATH + "character_slot_normal.sub",
					"over_image" : COMMON_PATH + "character_slot_hover.sub",
					"down_image" : COMMON_PATH + "character_slot_down.sub",
					"children" : (
						{ "name" : "CharacterSlot0_Icon", "type" : "image", "x" : 15, "y" : 18, "image" : COMMON_PATH + "character_icon_empty.sub" },
						{ "name" : "CharacterSlot0_Text1", "type" : "text", "x" : 80, "y" : 20, "fontsize" : "LARGE", "color" : 0xffbeaa87, "text" : "Lv. 167 - Elendos" },
						{ "name" : "CharacterSlot0_Text2", "type" : "text", "x" : 80, "y" : 35, "color" : 0xff6f6f6f, "text" : "Tal von Seungryong" },
					),
				},
				{
					"name" : "CharacterSlot1", "type" : "radio_button",
					"x" : 0, "y" : 0, "horizontal_align" : "center",
					"default_image" : COMMON_PATH + "character_slot_normal.sub",
					"over_image" : COMMON_PATH + "character_slot_hover.sub",
					"down_image" : COMMON_PATH + "character_slot_down.sub",
					"children" : (
						{ "name" : "CharacterSlot1_Icon", "type" : "image", "x" : 15, "y" : 18, "image" : COMMON_PATH + "character_icon_empty.sub" },
						{ "name" : "CharacterSlot1_Text1", "type" : "text", "x" : 80, "y" : 20, "fontsize" : "LARGE", "color" : 0xffbeaa87, "text" : "Lv. 55 - Aslan" },
						{ "name" : "CharacterSlot1_Text2", "type" : "text", "x" : 80, "y" : 35, "color" : 0xff6f6f6f, "text" : "Yongbi Wüste" },
					),
				},
				{
					"name" : "CharacterSlot2", "type" : "radio_button",
					"x" : 0, "y" : 0, "horizontal_align" : "center",
					"default_image" : COMMON_PATH + "character_slot_normal.sub",
					"over_image" : COMMON_PATH + "character_slot_hover.sub",
					"down_image" : COMMON_PATH + "character_slot_down.sub",
					"children" : (
						{ "name" : "CharacterSlot2_Icon", "type" : "image", "x" : 15, "y" : 18, "image" : COMMON_PATH + "character_icon_empty.sub" },
						{ "name" : "CharacterSlot2_Text1", "type" : "text", "x" : 80, "y" : 20, "fontsize" : "LARGE", "color" : 0xffbeaa87, "text" : "Lv. 27 - Miepsen" },
						{ "name" : "CharacterSlot2_Text2", "type" : "text", "x" : 80, "y" : 35, "color" : 0xff6f6f6f, "text" : "Feuerland" },
					),
				},
				{
					"name" : "CharacterSlot3", "type" : "radio_button",
					"x" : 0, "y" : 0, "horizontal_align" : "center",
					"default_image" : COMMON_PATH + "character_slot_normal.sub",
					"over_image" : COMMON_PATH + "character_slot_hover.sub",
					"down_image" : COMMON_PATH + "character_slot_down.sub",
					"children" : (
						{ "name" : "CharacterSlot3_Icon", "type" : "image", "x" : 15, "y" : 18, "image" : COMMON_PATH + "character_icon_empty.sub" },
						{ "name" : "CharacterSlot3_Text1", "type" : "text", "x" : 80, "y" : 20, "fontsize" : "LARGE", "color" : 0xffbeaa87, "text" : "Lv. 77 - Zarex" },
						{ "name" : "CharacterSlot3_Text2", "type" : "text", "x" : 80, "y" : 35, "color" : 0xff6f6f6f, "text" : "Chunjo - Map 1" },
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
					"name" : "ContainerCharacterDetails", "type" : "image",
					"x" : 0, "y" : 0,
					"image" : MAIN_PATH + "char_select_board.tga",
					"children" : (
						{ "name" : "TitleTextCharacterDetails", "type" : "text", "x" : 65, "y" : 29, "color" : 0xff9a8b70, "fontsize" : "LARGE", "text" : "Character Details" },
						
						# GENERAL INFO # ########################################################################################################################################################
						
						{ "name" : "CharacterDetailsTextName", "type" : "text", "x" : 37, "y" : 83, "color" : 0xff9a8b70, "fontsize" : "LARGE", "text" : "Name" },
						{ "name" : "CharacterDetailsTextLevel", "type" : "text", "x" : 37, "y" : 117, "color" : 0xff9a8b70, "fontsize" : "LARGE", "text" : "Level" },
						{ "name" : "CharacterDetailsTextGuild", "type" : "text", "x" : 37, "y" : 150, "color" : 0xff9a8b70, "fontsize" : "LARGE", "text" : "Guild" },
						{ "name" : "CharacterDetailsTextPlaytime", "type" : "text", "x" : 37, "y" : 183, "color" : 0xff9a8b70, "fontsize" : "LARGE", "text" : "Playtime" },
						
						{ 
							"name" : "CharacterDetailsInputName", "type" : "image", "x" : 132, "y" : 83 - 5, "image" : COMMON_PATH + "input_middle.sub", 
							"children" : ( { "name" : "CharacterDetailsInputNameText", "type" : "text", "x" : 0, "y" : 0, "all_align" : "center", "color" : 0xff9a8b70, "text" : "Elendos" }, ),
						},
						{ 
							"name" : "CharacterDetailsInputLevel", "type" : "image", "x" : 132, "y" : 117 - 5, "image" : COMMON_PATH + "input_middle.sub",
							"children" : ( { "name" : "CharacterDetailsInputLevelText", "type" : "text", "x" : 0, "y" : 0, "all_align" : "center", "color" : 0xff9a8b70, "text" : "Lv. 180" }, ),
						},
						{ 
							"name" : "CharacterDetailsInputGuild", "type" : "image", "x" : 132, "y" : 150 - 5, "image" : COMMON_PATH + "input_middle.sub",
							"children" : ( { "name" : "CharacterDetailsInputGuildText", "type" : "text", "x" : 0, "y" : 0, "all_align" : "center", "color" : 0xff9a8b70, "text" : "Elendosfiles" }, ),
						},
						{ 
							"name" : "CharacterDetailsInputPlaytime", "type" : "image", "x" : 132, "y" : 183 - 5, "image" : COMMON_PATH + "input_middle.sub",
							"children" : ( { "name" : "CharacterDetailsInputPlaytimeText", "type" : "text", "x" : 0, "y" : 0, "all_align" : "center", "color" : 0xff9a8b70, "text" : "274Std. 22Min." }, ),
						},
						
						# STATUS INFO # ########################################################################################################################################################
						
						{ "name" : "CharacterDetailsTextHP", "type" : "text", "x" : 37, "y" : 237, "color" : 0xff9a8b70, "fontsize" : "LARGE", "text" : "HP" },
						{ "name" : "CharacterDetailsTextINT", "type" : "text", "x" : 37, "y" : 270, "color" : 0xff9a8b70, "fontsize" : "LARGE", "text" : "INT" },
						{ "name" : "CharacterDetailsTextSTR", "type" : "text", "x" : 37, "y" : 303, "color" : 0xff9a8b70, "fontsize" : "LARGE", "text" : "STR" },
						{ "name" : "CharacterDetailsTextDEX", "type" : "text", "x" : 37, "y" : 336, "color" : 0xff9a8b70, "fontsize" : "LARGE", "text" : "DEX" },
						
						{
							"name" : "HPGaugeBG", "type" : "image",
							"x" : 71, "y" : 239, "image" : COMMON_PATH + "gauge_empty.sub",
							"children": ( { "name" : "HPGauge", "type" : "expanded_image", "x" : 0, "y" : 0, "image" : COMMON_PATH + "gauge_full.sub", }, ),
						},
						{
							"name" : "INTGaugeBG", "type" : "image",
							"x" : 71, "y" : 272, "image" : COMMON_PATH + "gauge_empty.sub",
							"children": ( { "name" : "INTGauge", "type" : "expanded_image", "x" : 0, "y" : 0, "image" : COMMON_PATH + "gauge_full.sub", }, ),
						},
						{
							"name" : "STRGaugeBG", "type" : "image",
							"x" : 71, "y" : 305, "image" : COMMON_PATH + "gauge_empty.sub",
							"children": ( { "name" : "STRGauge", "type" : "expanded_image", "x" : 0, "y" : 0, "image" : COMMON_PATH + "gauge_full.sub", }, ),
						},
						{
							"name" : "DEXGaugeBG", "type" : "image",
							"x" : 71, "y" : 338, "image" : COMMON_PATH + "gauge_empty.sub",
							"children": ( { "name" : "DEXGauge", "type" : "expanded_image", "x" : 0, "y" : 0, "image" : COMMON_PATH + "gauge_full.sub", }, ),
						},
						{ 
							"name" : "CharacterDetailsInputHP", "type" : "image", "x" : 242, "y" : 237 - 5, "image" : COMMON_PATH + "input_small.sub", 
							"children" : ( { "name" : "CharacterDetailsInputHPText", "type" : "text", "x" : 0, "y" : 0, "all_align" : "center", "color" : 0xff9a8b70, "text" : "88" }, ),
						},
						{ 
							"name" : "CharacterDetailsInputINT", "type" : "image", "x" : 242, "y" : 270 - 5, "image" : COMMON_PATH + "input_small.sub",
							"children" : ( { "name" : "CharacterDetailsInputINTText", "type" : "text", "x" : 0, "y" : 0, "all_align" : "center", "color" : 0xff9a8b70, "text" : "95" }, ),
						},
						{ 
							"name" : "CharacterDetailsInputSTR", "type" : "image", "x" : 242, "y" : 303 - 5, "image" : COMMON_PATH + "input_small.sub",
							"children" : ( { "name" : "CharacterDetailsInputSTRText", "type" : "text", "x" : 0, "y" : 0, "all_align" : "center", "color" : 0xff9a8b70, "text" : "102" }, ),
						},
						{ 
							"name" : "CharacterDetailsInputDEX", "type" : "image", "x" : 242, "y" : 336 - 5, "image" : COMMON_PATH + "input_small.sub",
							"children" : ( { "name" : "CharacterDetailsInputDEXText", "type" : "text", "x" : 0, "y" : 0, "all_align" : "center", "color" : 0xff9a8b70, "text" : "42" }, ),
						},
						
						# PLAY BUTTON # ########################################################################################################################################################
						{
							"name" : "PlayButton", "type" : "button",
							"x" : 33, "y" : 383,
							"default_image" : BUTTON_PATH + "button_play_normal.sub",
							"over_image" : BUTTON_PATH + "button_play_hover.sub",
							"down_image" : BUTTON_PATH + "button_play_down.sub",
						},
					),
				},
				{
					"name" : "DeleteButton", "type" : "button",
					"x" : 7, "y" : 459,
					"default_image" : BUTTON_PATH + "button_delchar_normal.sub",
					"over_image" : BUTTON_PATH + "button_delchar_hover.sub",
					"down_image" : BUTTON_PATH + "button_delchar_down.sub",
				},
				{
					"name" : "ExitButton", "type" : "button",
					"x" : 185, "y" : 459,
					"default_image" : BUTTON_PATH + "button_exit_normal.sub",
					"over_image" : BUTTON_PATH + "button_exit_hover.sub",
					"down_image" : BUTTON_PATH + "button_exit_down.sub",
				},
            ),
        },
    ),
}