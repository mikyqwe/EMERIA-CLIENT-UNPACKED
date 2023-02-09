import os
import localeInfo
#import os.path

STATE_NONE = "Offline"
STATE_DICT = {
	0 : "OFFLINE",
	1 : "ONLINE",
	2 : "ONLINE",
	3 : "ONLINE"
}

SRV1 = {
	"name":"Elendosfiles",
	"host":"WRITE_THE_IP_HERE",
	"auth":11213,
	"ch1":13101,
	"ch2":14070,
	"ch3":15070,
	"ch4":16070,
}


SRV_LIST = (
	(
		(
			SRV1["name"],SRV1["auth"],
			(SRV1["host"],SRV1["ch1"], "10.tga", "10"),		#[1][0, 1, 2, 3]
			[
				("CH1",SRV1["host"],SRV1["ch1"],SRV1["ch1"],0),   #[2][0][0, 1, 2, 3]
				("CH2",SRV1["host"],SRV1["ch2"],SRV1["ch2"],0),
				("CH3",SRV1["host"],SRV1["ch3"],SRV1["ch3"],0),
				("CH4",SRV1["host"],SRV1["ch4"],SRV1["ch4"],0),
			]
		),
	),
)

# SRV_LIST = {
	# {"name":"Channel 1","ip":SRV1["host"],"tcp_port":SRV1["ch1"],"udp_port":SRV1["ch1"],"state":STATE_NONE,},
	# {"name":"Channel 2","ip":SRV1["host"],"tcp_port":SRV1["ch2"],"udp_port":SRV1["ch2"],"state":STATE_NONE,},
	# {"name":"Channel 3","ip":SRV1["host"],"tcp_port":SRV1["ch3"],"udp_port":SRV1["ch3"],"state":STATE_NONE,},
	# {"name":"Channel 4","ip":SRV1["host"],"tcp_port":SRV1["ch4"],"udp_port":SRV1["ch4"],"state":STATE_NONE,},
# }

# MARKADDR_DICT = {
	# 10 : { "ip" : SRV1["host"], "tcp_port" : SRV1["ch1"], "mark" : "10.tga", "symbol_path" : "10", },
	# 11 : { "ip" : SRV1["host"], "tcp_port" : SRV1["ch2"], "mark" : "10.tga", "symbol_path" : "11", },
	# 12 : { "ip" : SRV1["host"], "tcp_port" : SRV1["ch3"], "mark" : "10.tga", "symbol_path" : "12", },
	# 13 : { "ip" : SRV1["host"], "tcp_port" : SRV1["ch4"], "mark" : "10.tga", "symbol_path" : "13", },
# }

SERVER_STATE_TABLE = {}