import app
import localeInfo
app.ServerName = None

SRV1 = {
	#"name":"Emeria",
	"name":"Emeria",
	"host":"37.46.83.134",
	#"host":"130.193.10.18",
	"auth1":30001,
	"ch1":30003,
	"ch2":40007,
	"ch3":30011,
	"ch4":30015,
	"ch5":30019,
	"ch6":30023,

}

SRV2 = {
	#"name":"Emeria",
	"name":"Emeria",
	"host":"51.91.150.235",
	#"host":"37.46.85.245",
	"auth1":30776,
	"ch1":29001,
	"ch2":29101,
	"ch3":29201,
	"ch4":29301,
	"ch5":29401,
	"ch6":29501,

}

STATE_NONE = -1

STATE_DICT = {
	0 : "....",
	1 : "NORM",
	2 : "BUSY",
	3 : "FULL"
}

SERVER1_CHANNEL_DICT = {
	1:{"key":11,"name":"Channel 1","ip":SRV1["host"],"tcp_port":SRV1["ch1"],"udp_port":SRV1["ch1"],"state":STATE_NONE,},
	2:{"key":12,"name":"Channel 2","ip":SRV1["host"],"tcp_port":SRV1["ch2"],"udp_port":SRV1["ch2"],"state":STATE_NONE,},
	3:{"key":13,"name":"Channel 3","ip":SRV1["host"],"tcp_port":SRV1["ch3"],"udp_port":SRV1["ch3"],"state":STATE_NONE,},
	4:{"key":14,"name":"Channel 4","ip":SRV1["host"],"tcp_port":SRV1["ch4"],"udp_port":SRV1["ch4"],"state":STATE_NONE,},
	5:{"key":15,"name":"Channel 5","ip":SRV1["host"],"tcp_port":SRV1["ch5"],"udp_port":SRV1["ch5"],"state":STATE_NONE,},
	6:{"key":16,"name":"Channel 6","ip":SRV1["host"],"tcp_port":SRV1["ch6"],"udp_port":SRV1["ch6"],"state":STATE_NONE,},

}

SERVER1_CHANNEL_DICT_A = {
	1:{"key":11,"name":"Channel 1","ip":SRV2["host"],"tcp_port":SRV2["ch1"],"udp_port":SRV2["ch1"],"state":STATE_NONE,},
	2:{"key":12,"name":"Channel 2","ip":SRV2["host"],"tcp_port":SRV2["ch2"],"udp_port":SRV2["ch2"],"state":STATE_NONE,},
	3:{"key":13,"name":"Channel 3","ip":SRV2["host"],"tcp_port":SRV2["ch3"],"udp_port":SRV2["ch3"],"state":STATE_NONE,},
	4:{"key":14,"name":"Channel 4","ip":SRV2["host"],"tcp_port":SRV2["ch4"],"udp_port":SRV2["ch4"],"state":STATE_NONE,},
	5:{"key":15,"name":"Channel 5","ip":SRV2["host"],"tcp_port":SRV2["ch5"],"udp_port":SRV2["ch5"],"state":STATE_NONE,},
	6:{"key":16,"name":"Channel 6","ip":SRV2["host"],"tcp_port":SRV2["ch6"],"udp_port":SRV2["ch6"],"state":STATE_NONE,},

}

REGION_NAME_DICT = {
	0 : SRV1["name"],
}

REGION_NAME_DICT_A = {
	0 : SRV2["name"],
}

REGION_AUTH_SERVER_DICT = {
	0 : {
		1 : { "ip":SRV1["host"], "port":SRV1["auth1"], },
		2 : { "ip":SRV1["host"], "port":SRV1["auth1"], },
		3 : { "ip":SRV1["host"], "port":SRV1["auth1"], },
	}
}

REGION_AUTH_SERVER_DICT_A = {
	0 : {
		1 : { "ip":SRV2["host"], "port":SRV2["auth1"], },
		2 : { "ip":SRV2["host"], "port":SRV2["auth1"], },
		3 : { "ip":SRV2["host"], "port":SRV2["auth1"], },
	}
}

REGION_DICT = {
	0 : {
		1 : { "name" :SRV1["name"], "channel" : SERVER1_CHANNEL_DICT, },
	},
}

REGION_DICT_A = {
	0 : {
		1 : { "name" :SRV2["name"], "channel" : SERVER1_CHANNEL_DICT_A, },
	},
}

MARKADDR_DICT = {
	10 : { "ip" : SRV1["host"], "tcp_port" : SRV1["ch1"], "mark" : "10.tga", "symbol_path" : "10", },
}

MARKADDR_DICT_A = {
	10 : { "ip" : SRV2["host"], "tcp_port" : SRV2["ch1"], "mark" : "10.tga", "symbol_path" : "10", },
}
