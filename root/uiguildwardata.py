import os
import guild
import constInfo

DATA_DIRECTORY = "lib/guild_statistics/data"
MAIN_DIRECTORY = "lib/guild_statistics"
FILE_EXTENSION = ".gw"

def LoadData(warID):
	if guild.WarStatisticsDataSize(warID) > 0:
		return True
	else:
		constInfo.CheckDirectory(MAIN_DIRECTORY)
		constInfo.CheckDirectory(DATA_DIRECTORY)

		dataFile = DATA_DIRECTORY+"/"+str(warID)+FILE_EXTENSION
		if constInfo.CheckFile(dataFile):
			lines = open(dataFile, "r").readlines()
			if len(lines) > 0:
				guild.WarStatisticsDataRemove(int(warID))
				for line in lines:
					line = constInfo.decodeMessage(line,31)
					splitText = line.split("!")
					if len(splitText) != 12:
						continue
					(name, level, race, empire, is_leader, kill, dead, skill_dmg, guild_id, spy, online, pid) = tuple(splitText)
					guild.WarStatisticsDataSet(int(warID), str(name), int(level), int(race), int(empire), int(is_leader), int(kill), int(dead), int(skill_dmg), int(guild_id), int(spy), int(online), int(pid))
				return True
			return False
	return False

def Save(saveType, warID):
	if saveType == 9:
		constInfo.CheckDirectory(MAIN_DIRECTORY)
		constInfo.CheckDirectory(DATA_DIRECTORY)
		file = open(DATA_DIRECTORY+"/"+str(warID)+FILE_EXTENSION, "w+")
		for j in xrange(guild.WarStatisticsDataSize(int(warID))):
			try:
				text = "%s!%d!%d!%d!%d!%d!%d!%d!%d!%d!%d!%d" % tuple(guild.WarStatisticsData(int(warID),j))
				text = constInfo.encodeMessage(text,31)
				file.write(text+"\n")
			except:
				pass
		file.close()

def GetWarStatistics(check_war_id, g_id):
	leaderName,onlineCount, offlineCount, guildEmpire, spyCount, totalKill,totalDead, totalDmg, raceList = ("-",0,0,0,0,0,0,0,[0,0,0,0])
	for j in xrange(guild.WarStatisticsDataSize(check_war_id)):
		(name,level,race,empire,is_leader,kill,dead,skill_dmg,guild_id, spy, online, pid) = guild.WarStatisticsData(check_war_id, j)
		if guild_id != g_id:
			continue
		if is_leader:
			leaderName = name
		if online:
			onlineCount+=1
			
		else:
			offlineCount+=1

		raceList[constInfo.raceToJob(race)]+=1

		if spy:
			spyCount+=1
		totalKill+=kill
		totalDead+=dead
		totalDmg+=skill_dmg
	return (leaderName, onlineCount, offlineCount, spyCount, totalKill, totalDead, totalDmg, guildEmpire, raceList)
