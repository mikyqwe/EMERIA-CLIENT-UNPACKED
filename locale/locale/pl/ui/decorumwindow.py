import uiScriptLocale
import colorInfo

ROOT = "d:/ymir work/ui/universalelements/decorum/"

window = {
	"name" : "DecorumWindow",
	"x" : - 370 - 75,
	"y" : 50,
	"style" : ("float",),
	"width" : 230,
	"height" : 370 + 75,
	"children" :
	(
		{
			"name" : "board",
			"type" : "prettyboard",
			"x" : 0,
			"y" : 0,
			"width" : 230,
			"height" : 370 + 75,
			 "children" :
			 (
				## legue mark
				{
					"name" : "LegueMark",
					"type" : "image",
					"x" : 5,
					"y" : 5,
					"image" : ROOT + "universalelements_legue_diamond4.sub", 
				},
				
				## legue mark
				{
					"name" : "CloseBotton",
					"type" : "button",
					"x" : 5,
					"y" : 5,
					
					"default_image" : "d:/ymir work/ui/public/close_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/close_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/close_button_03.sub",
					
					"tooltip_text" : uiScriptLocale.CLOSE,
				},
				
				## legue name
				{
					"name" : "LegueName",
					"type" : "image",
					"x" : 95,
					"y" : 42,
					"image" : ROOT + "universalelements_decorum_gauge.sub", 
					
					"children" :
					(
						{"name" : "LegueNameValue", "type" : "text", "x" : 4, "y" : -2, "all_align" : "center", "text" : "",},
					),
				},
				
				## char name
				{
					"name" : "PgName",
					"type" : "image",
					"x" : 95,
					"y" : 20,
					"image" : ROOT + "universalelements_decorum_gauge.sub", 
					
					"children" :
					(
						{"name" : "PgNameValue", "type" : "text", "x" : 4, "y" : -2, "all_align" : "center", "text" : "",},
					),
				},
				
				## decorum
				{
					"name" : "DecorumGauge",
					"type" : "image",
					"x" : 80,
					"y" : 65,
					"image" : ROOT + "universalelements_decorum_gauge.sub", 
					
					"children" :
					(
						{"name" : "DecorumValue", "type" : "text", "x" : 4, "y" : -2, "all_align" : "center","text" : "",},
					),
				},
				
				## decored duell
				{
					"name":"DecoredDuelBar", "type":"horizontalbar", "x":15, "y":105, "width":200,
					"children" :
					(
						{ "name":"DecoredDuelName", "type":"text", "x":8, "y":1, "text":uiScriptLocale.DECORUM_DUEL, },
						{ "name":"DecoredDuelFull", "type":"expanded_image", "x":0, "y":15, "image" : ROOT + "universalelements_decorum_rate_full.sub",},
						{ "name":"DecoredDuelEmpty", "type":"image", "x":0, "y":15, "image" : ROOT + "universalelements_decorum_rate_empty.sub",
							"children" : ({"name" : "DecorumDuelRate", "type" : "text", "x" : 179, "y" : 3, "text" : "85%"},),
						},
						{"name" : "DecorumDuelText", "type" : "text", "x" : 10, "y" : 35, "text" : "",},
					),
				},
				
				## decored arena 2v2
				{
					"name":"DecoredArena1Bar", "type":"horizontalbar", "x":15, "y":160, "width":200,
					"children" :
					(
						{ "name":"DecoredArena1Name", "type":"text", "x":8, "y":1, "text":uiScriptLocale.DECORUM_ARENA1, },
						{ "name":"DecoredArena1Full", "type":"expanded_image", "x":0, "y":15, "image" : ROOT + "universalelements_decorum_rate_full.sub",},
						{ "name":"DecoredArena1Empty", "type":"image", "x":0, "y":15, "image" : ROOT + "universalelements_decorum_rate_empty.sub",
							"children" : ({"name" : "DecorumArena1Rate", "type" : "text", "x" : 179, "y" : 3, "text" : "100%"},),
						},
						{"name" : "DecorumArena1Text", "type" : "text", "x" : 10, "y" : 35, "text" : "",},
					),
				},
				
				## decored arena 3v3
				{
					"name":"DecoredArena2Bar", "type":"horizontalbar", "x":15, "y":215, "width":200,
					"children" :
					(
						{ "name":"DecoredArena2Name", "type":"text", "x":8, "y":1, "text":uiScriptLocale.DECORUM_ARENA2, },
						{ "name":"DecoredArena2Full", "type":"expanded_image", "x":0, "y":15, "image" : ROOT + "universalelements_decorum_rate_full.sub",},
						{ "name":"DecoredArena2Empty", "type":"image", "x":0, "y":15, "image" : ROOT + "universalelements_decorum_rate_empty.sub",
							"children" : ({"name" : "DecorumArena2Rate", "type" : "text", "x" : 179, "y" : 3, "text" : "0%"},),
						},
						{"name" : "DecorumArena2Text", "type" : "text", "x" : 10, "y" : 35, "text" : "0%",},
					),
				},
				
				## decored arena 5v5
				{
					"name":"DecoredArena3Bar", "type":"horizontalbar", "x":15, "y":270, "width":200,
					"children" :
					(
						{ "name":"DecoredArena3Name", "type":"text", "x":8, "y":1, "text":uiScriptLocale.DECORUM_ARENA3, },
						{ "name":"DecoredArena3Full", "type":"expanded_image", "x":0, "y":15, "image" : ROOT + "universalelements_decorum_rate_full.sub",},
						{ "name":"DecoredArena3Empty", "type":"image", "x":0, "y":15, "image" : ROOT + "universalelements_decorum_rate_empty.sub",
							"children" : ({"name" : "DecorumArena3Rate", "type" : "text", "x" : 179, "y" : 3, "text" : ""},),
						},
						{"name" : "DecorumArena3Text", "type" : "text", "x" : 10, "y" : 35, "text" : "Vinte 4534 / Fatte 4564",},
					),
				},
				
				## promotion / demotion
				{
					"name":"DecoredGeneralBar", "type":"horizontalbar", "x":15, "y":325, "width":200,
					"children" :
					(
						{ "name":"DecoredPromotionName", "type":"text", "x":8, "y":1, "text":uiScriptLocale.DECORUM_GENERAL, },
						{"name" : "DecorumPromotionText", "type" : "text", "x" : 10, "y" : 17, "text":uiScriptLocale.DECORUM_PROMOTION,},
						{"name" : "DecorumDemotionText", "type" : "text", "x" : 10, "y" : 32, "text":uiScriptLocale.DECORUM_DEMOTION,},
						{"name" : "DecorumKillsText", "type" : "text", "x" : 120, "y" : 17, "text":uiScriptLocale.DECORED_KILLS,},
						{"name" : "DecorumDeathText", "type" : "text", "x" : 120, "y" : 32, "text":uiScriptLocale.DECORED_DEATH,},
					),
				},
				
				## block
				{
					"name":"BlockBar", "type":"horizontalbar", "x":15, "y":300 + 75, "width":200,
					"children" :
					(
						{ "name":"BlockBarName", "type":"text", "x":8, "y":3, "text":uiScriptLocale.DECORUM_BLOCK, },
					),
				},
				
				{"name" : "Duel", "type" : "text", "x" : 30 + 0, "y" : 320 + 75, "text" : uiScriptLocale.DECORUM_BLOCK_DUEL,},
				{"name" : "DuelCheckBox", "type" : "checkBox_classic", "x" : 20 + 0, "y" : 335 + 75, "image" : "d:/ymir work/ui/public/Parameter_Slot_00.sub",},
				
				{"name" : "Arena1", "type" : "text", "x" : 30 + 50 * 1, "y" : 320 + 75, "text" : uiScriptLocale.DECORUM_BLOCK_ARENA1,},
				{"name" : "Arena1CheckBox", "type" : "checkBox_classic", "x" : 20 + 50 * 1, "y" : 335 + 75, "image" : "d:/ymir work/ui/public/Parameter_Slot_00.sub",},
				
				{"name" : "Arena2", "type" : "text", "x" : 30 + 50 * 2, "y" : 320 + 75, "text" : uiScriptLocale.DECORUM_BLOCK_ARENA2,},
				{"name" : "Arena2CheckBox", "type" : "checkBox_classic", "x" : 20 + 50 * 2, "y" : 335 + 75, "image" : "d:/ymir work/ui/public/Parameter_Slot_00.sub",},
				
				{"name" : "Arena3", "type" : "text", "x" : 30 + 50 * 3, "y" : 320 + 75, "text" : uiScriptLocale.DECORUM_BLOCK_ARENA3,},
				{"name" : "Arena3CheckBox", "type" : "checkBox_classic", "x" : 20 + 50 * 3, "y" : 335 + 75, "image" : "d:/ymir work/ui/public/Parameter_Slot_00.sub",},
			),
		},
	),
}