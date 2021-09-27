from riotwatcher import LolWatcher, ApiError
'''
This file contains all the necessary information to build up the Riot API application.
Data structrue that contains it varies but they are mostly dictionaries. 
'''
# API_KEY and initializing the LoLWatcher instance w
API_KEY = ''
WATCHER = LolWatcher(API_KEY)

# Getting league's latest info 
latest_league_info = WATCHER.data_dragon.versions_for_region(MY_REGION)['n']['champion']

# Getting champion information 
static_champ_list = WATCHER.data_dragon.champions(latest_league_info, False, 'en_US')
champ_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict[row['key']] = row['id']

# Getting Item Info
req1 = requests.get(
    'http://ddragon.leagueoflegends.com/cdn/11.1.1/data/en_US/item.json')
item_dict = req1.json()['data']

# Getting Summoner Spell Info
req2 = requests.get(
    'http://ddragon.leagueoflegends.com/cdn/11.1.1/data/en_US/summoner.json')
summoner_spell_dict = req1.json()['data']

# Getting Runes
req3 = requests.get(
    'http://ddragon.leagueoflegends.com/cdn/11.1.1/data/en_US/runesReforged.json')
runes_info = req3.json()
perk_dict = {}
for major in runes_info:
    runes = major['slots']
    for rune in runes:
        runes_list = rune["runes"]
        for item in runes_list:
            perk_dict[item["id"]] = item["key"]

# Dictionary that converts summoner spell id to its actual name 
summoner_spell_id_to_name = {}
summoner_spell_id_to_name[1] = "Cleanse"
summoner_spell_id_to_name[3] = "Exhaust"
summoner_spell_id_to_name[4] = "Flash"
summoner_spell_id_to_name[6] = "Ghost"
summoner_spell_id_to_name[7] = "Heal"
summoner_spell_id_to_name[11] = "Smite"
summoner_spell_id_to_name[12] = "Teleport"
summoner_spell_id_to_name[13] = "Clarity"
summoner_spell_id_to_name[14] = "Ignite"
summoner_spell_id_to_name[21] = "Barrier"

# Dictionary that converts a tuple to one of roles 
role_dict = defaultdict(lambda: 'NONE')
role_dict[('DUO_CARRY', 'BOTTOM')] = 'ADC'
role_dict[('DUO_SUPPORT', 'NONE')] = 'SUPPORT'
role_dict[('SOLO', 'TOP')] = 'TOP'
role_dict[('NONE', 'JUNGLE')] = 'JUNGLE'
role_dict[('SOLO', 'BOTTOM')] = 'ADC'

#Dictionary that converts a tuple to one of roles 
position = defaultdict(lambda: "BUG")
position[("MID", "SOLO")] = "MID"
position[("TOP", "SOLO")] = "TOP"
position[("JUNGLE", "NONE")] = "JUN"
position[("BOTTOM", "DUO_CARRY")] = "ADC"
position[("BOTTOM", "DUO_SUPPORT")] = "SUP"

#Time shift info by server 
time_shifts_by_server = {
    "oc1": -46800,
    "jp1": -43200,
    "kr": -39600,
    "ru": -28800,
    "eun1": -21600,
    "tr1": -18000,
    "euw1": -10800,
    "br1": -3600,
    "la2": 0,
    "la1": 7200,
    "na1": 10800,
    "ph": 43200,
    "id1": 43200,
    "vn": 46800,
    "sg": 50400,
    "th": 54000,
    "tw": 57600,
}

#Dictionary that converts to time stamp of each season's start
time_stamp_by_season = {
    "11": 1609920000,
    "10": 1578477600,
    "9": 1547020800,
    "8": 1515571200,
    "7": 1484121600,
}

#Dictionary that converts chamption to its most popular role 
champion_to_role = {}
champion_to_role['Aatrox'] = "TOP"
champion_to_role['Ahri'] = "MID"
champion_to_role['Akali'] = "MID"
champion_to_role['Alistar'] = "SUP"
champion_to_role['Amumu'] = "JUN"
champion_to_role['Anivia'] = "MID"
champion_to_role['Annie'] = "MID"
champion_to_role['Aphelios'] = "ADC"
champion_to_role['Ashe'] = "ADC"
champion_to_role['AurelionSol'] = "MID"
champion_to_role['Azir'] = "MID"
champion_to_role['Bard'] = "SUP"
champion_to_role['Blitzcrank'] = "SUP"
champion_to_role['Brand'] = "SUP"
champion_to_role['Braum'] = "SUP"
champion_to_role['Caitlyn'] = "ADC"
champion_to_role['Camille'] = "TOP"
champion_to_role['Cassiopeia'] = "MID"
champion_to_role['Chogath'] = "TOP"
champion_to_role['Corki'] = "MID"
champion_to_role['Darius'] = "TOP"
champion_to_role['Diana'] = "MID"
champion_to_role['Draven'] = "ADC"
champion_to_role['DrMundo'] = "TOP"
champion_to_role['Ekko'] = "JUN"
champion_to_role['Elise'] = "JUN"
champion_to_role['Evelynn'] = "JUN"
champion_to_role['Ezreal'] = 'ADC'
champion_to_role['Fiddlesticks'] = "JUN"
champion_to_role['Fiora'] = "TOP"
champion_to_role['Fizz'] = "MID"
champion_to_role['Galio'] = "MID"
champion_to_role['Gangplank'] = "TOP"
champion_to_role['Garen'] = "TOP"
champion_to_role['Gnar'] = "TOP"
champion_to_role['Gragas'] = "TOP"
champion_to_role['Graves'] = "JUN"
champion_to_role['Hecarim'] = "JUN"
champion_to_role['Heimerdinger'] = "TOP"
champion_to_role['Illaoi'] = "TOP"
champion_to_role['Irelia'] = "TOP"
champion_to_role['Ivern'] = "JUN"
champion_to_role['Janna'] = "SUP"
champion_to_role['JarvanIV'] = "JUN"
champion_to_role['Jax'] = "TOP"
champion_to_role['Jayce'] = "TOP"
champion_to_role['Jhin'] = "ADC"
champion_to_role['Jinx'] = "ADC"
champion_to_role['Kaisa'] = "ADC"
champion_to_role['Kalista'] = "ADC"
champion_to_role['Karma'] = "SUP"
champion_to_role['Karthus'] = "JUN"
champion_to_role['Kassadin'] = "MID"
champion_to_role['Katarina'] = "MID"
champion_to_role['Kayle'] = "TOP"
champion_to_role['Kayn'] = "JUN"
champion_to_role['Kennen'] = "TOP"
champion_to_role['Khazix'] = "JUN"
champion_to_role['Kindred'] = "JUN"
champion_to_role['Kled'] = "TOP"
champion_to_role['KogMaw'] = "ADC"
champion_to_role['Leblanc'] = "MID"
champion_to_role['LeeSin'] = "JUN"
champion_to_role['Leona'] = "SUP"
champion_to_role['Lillia'] = "JUN"
champion_to_role['Lissandra'] = "MID"
champion_to_role['Lucian'] = "BOT"
champion_to_role['Lulu'] = "SUP"
champion_to_role['Lux'] = "SUP"
champion_to_role['Malphite'] = "TOP"
champion_to_role['Malzahar'] = "MID"
champion_to_role['Maokai'] = "SUP"
champion_to_role['MasterYi'] = "JUN"
champion_to_role['MissFortune'] = "ADC"
champion_to_role['MonkeyKing'] = "TOP"
champion_to_role['Mordekaiser'] = "TOP"
champion_to_role['Morgana'] = "SUP"
champion_to_role['Nami'] = "SUP"
champion_to_role['Nasus'] = "TOP"
champion_to_role['Nautilus'] = "SUP"
champion_to_role['Neeko'] = "MID"
champion_to_role['Nidalee'] = "JUN"
champion_to_role['Nocturne'] = "JUN"
champion_to_role['Nunu'] = "JUN"
champion_to_role['Olaf'] = "JUN"
champion_to_role['Orianna'] = "MID"
champion_to_role['Ornn'] = "TOP"
champion_to_role['Pantheon'] = "SUP"
champion_to_role['Poppy'] = "TOP"
champion_to_role['Pyke'] = "SUP"
champion_to_role['Qiyana'] = "MID"
champion_to_role['Quinn'] = "TOP"
champion_to_role['Rakan'] = "SUP"
champion_to_role['Rammus'] = "JUN"
champion_to_role['RekSai'] = "JUN"
champion_to_role['Rell'] = "SUP"
champion_to_role['Renekton'] = "TOP"
champion_to_role['Rengar'] = "TOP"
champion_to_role['Riven'] = "TOP"
champion_to_role['Rumble'] = "TOP"
champion_to_role['Ryze'] = "MID"
champion_to_role['Samira'] = "ADC"
champion_to_role['Sejuani'] = "JUN"
champion_to_role['Senna'] = "SUP"
champion_to_role['Seraphine'] = "SUP"
champion_to_role['Sett'] = "TOP"
champion_to_role['Shaco'] = "SUP"
champion_to_role['Shen'] = "TOP"
champion_to_role['Shyvana'] = "JUN"
champion_to_role['Singed'] = "TOP"
champion_to_role['Sion'] = "TOP"
champion_to_role['Sivir'] = "ADC"
champion_to_role['Skarner'] = "JUN"
champion_to_role['Sona'] = "SUP"
champion_to_role['Soraka'] = "SUP"
champion_to_role['Swain'] = "SUP"
champion_to_role['Sylas'] = "MID"
champion_to_role['Syndra'] = "MID"
champion_to_role['TahmKench'] = "SUP"
champion_to_role['Taliyah'] = "JUN"
champion_to_role['Talon'] = "MID"
champion_to_role['Taric'] = "SUP"
champion_to_role['Teemo'] = "TOP"
champion_to_role['Thresh'] = "SUP"
champion_to_role['Tristana'] = "ADC"
champion_to_role['Trundle'] = "JG"
champion_to_role['Tryndamere'] = "TOP"
champion_to_role['TwistedFate'] = "MID"
champion_to_role['Twitch'] = "ADC"
champion_to_role['Udyr'] = "JUN"
champion_to_role['Urgot'] = "TOP"
champion_to_role['Varus'] = "ADC"
champion_to_role['Vayne'] = "ADC"
champion_to_role['Veigar'] = "MID"
champion_to_role['Velkoz'] = "SUP"
champion_to_role['Vi'] = "JUN"
champion_to_role['Viktor'] = "MID"
champion_to_role['Vladimir'] = "MID"
champion_to_role['Volibear'] = "TOP"
champion_to_role['Warwick'] = "JUN"
champion_to_role['Xayah'] = "ADC"
champion_to_role['Xerath'] = "SUP"
champion_to_role['XinZhao'] = "JUN"
champion_to_role['Yasuo'] = "MID"
champion_to_role['Yone'] = "MID"
champion_to_role['Yorick'] = "TOP"
champion_to_role['Yuumi'] = "SUP"
champion_to_role['Zac'] = "JUN"
champion_to_role['Zed'] = "MID"
champion_to_role['Ziggs'] = "MID"
champion_to_role['Zilean'] = "SUP"
champion_to_role['Zoe'] = "MID"
champion_to_role['Zyra'] = "SUP"
champion_to_role['Viego'] = "JUG"

region_to_name = {}
region_to_name["euw1"] = "EUW"
region_to_name["eun1"] = "EUN"
region_to_name["oc1"] = "OCE"
region_to_name["br1"] = "BR"
region_to_name["la1"] = "LAS"
region_to_name["la2"] = "LAN"
region_to_name["ru"] = "RUS"
region_to_name["tr1"] = "TUR"
region_to_name["kr"] = "KR"
region_to_name["na1"] = "NA"