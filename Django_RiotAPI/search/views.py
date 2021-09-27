from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from riotwatcher import LolWatcher, ApiError
from pathlib import Path
from collections import defaultdict
from django.conf import settings
from collections import defaultdict
from .models import *
# Create your views here.

###case 
def update_summoner_role_freq(summoner, role):
    switch (role) {
     case "TOP": {
        summoner.Top_played += 1
        break;
        }
    case "MID": {
        summoner.Mid_played += 1
        break;
        }
    case "JUN": {
        summoner.Jun_played += 1
        break;
        }
    case "SUP": {
        summoner.Sup_played += 1
        break;
        }
    default: {
        summoner.Adc_played += 1
        break;
        }
    }
    summoner.save()

def determine_role(match):
    champion = data.champ_dict[str(match['champion'])]
    role = match['role']
    lane = match['lane']
    entry = (lane, role)
    game_result = data.position[entry]
    if game_result != "BUG":
        return game_result
    else:
        return champion_to_role[champion]


def determine_role_part(participant):
    champion = settings.CHAMP_DICT[str(participant['championId'])]
    role = participant['timeline']['role']
    lane = participant['timeline']['lane']
    entry = (lane, role)
    game_result = settings.POSITION[entry]
    dictionary = settings.champion_to_role
    if game_result != "BUG":
        return game_result
    else:
        return dictionary[champion]

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

def show_region_specific_page(request):
    region = region_to_name[request.session['region']]
    return render(request, 'base.html', {'region': region})

def time_stamp(region):
    shift = settings.TIME_SHIFTS[region]
    start = 1000 * (settings.PATCHES["11"] + shift)
    return start


def ranked(user_name, region):
    me = settings.WATCHER.summoner.by_name(region, user_name)
    my_ranked_stats = settings.WATCHER.league.by_summoner(region, me['id'])
    flex_rank = None
    solo_rank = None
    ranked = {}
    for rank_info in my_ranked_stats:
        if rank_info["queueType"] == "RANKED_FLEX_SR":
            flex_rank = rank_info
        else:
            solo_rank = rank_info
    if solo_rank:
        solo_rank_info = {}
        solo_rank_info["summoner_name"] = solo_rank["summonerName"]
        solo_rank_info["wins"] = solo_rank["wins"]
        solo_rank_info["losses"] = solo_rank["losses"]
        solo_rank_info["win_ratio"] = round(
            100 * solo_rank_info["wins"]/(solo_rank_info["losses"] + solo_rank_info["wins"]))
        solo_rank_info["lp"] = solo_rank["leaguePoints"]
        solo_rank_info["tier"] = solo_rank["tier"]
        solo_rank_info["rank"] = solo_rank["rank"]
        solo_rank_info["link"] = "https://riotapi-media.s3-us-west-1.amazonaws.com/images/" + \
            solo_rank["tier"] + solo_rank["rank"] + ".png"
        ranked['solo'] = solo_rank_info
    if flex_rank:
        flex_rank_info = {}
        flex_rank_info["summoner_name"] = flex_rank["summonerName"]
        flex_rank_info["wins"] = flex_rank["wins"]
        flex_rank_info["losses"] = flex_rank["losses"]
        flex_rank_info["win_ratio"] = round(
            100 * flex_rank_info["wins"]/(flex_rank_info["losses"] + flex_rank_info["wins"]))
        flex_rank_info["lp"] = flex_rank["leaguePoints"]
        flex_rank_info["tier"] = flex_rank["tier"]
        flex_rank_info["rank"] = flex_rank["rank"]
        flex_rank_info["link"] = "https://riotapi-media.s3-us-west-1.amazonaws.com/images/" + \
            flex_rank["tier"] + flex_rank["rank"] + ".png"
        ranked['flex'] = flex_rank_info
    else:
        ranked['flex'] = {}
    return ranked


def update(user_name, region):
    queue_dict = defaultdict(list)
    me = settings.WATCHER.summoner.by_name(region, user_name)
    my_matches = settings.WATCHER.match.matchlist_by_account(
        region, me['accountId'])
    start = time_stamp(region)
    user = Summoner.objects.get(Name=me["name"], Searched="True")
    index = 0
    print(user.Most_recent)
    for match in my_matches['matches']:
        print(match['gameId'])
        if index == 0:
            temp = match['gameId']
            index += 1
        if int(match['timestamp']) < start:
            print("for loop broken(timestamp")
            break
        if match['gameId'] <= user.Most_recent:
            print("for loop broken(Most_recent)")
            break
        game_type = match['queue']
        role = determine_role(match)
        user.Num_played += 1
        update_summoner_role_freq(user, role)
        ##user.save()
        queue_dict[str(game_type)].append(match) ###may be able to change defaultdict to dict with two keys
    user.Most_recent = temp
    user.save()
    sort_game_type(queue_dict["420"], region, user, "Solo")
    sort_game_type(queue_dict["440"], region, user, "Flex")
    sort_game_type(queue_dict["430"], region, user, "Normal")
    sort_game_type(queue_dict["700"], region, user, "Clash")
    rank = ranked(user_name, region)
    game_result = {}
    game_result['solo'] = rank['solo']
    game_result['flex'] = rank['flex']
    game_result['summoner'] = user
    return game_result

def initial_search(me, region):
    queue_dict = defaultdict(list)
    my_matches = settings.WATCHER.match.matchlist_by_account(
        region, me['accountId'])
    start = time_stamp(region)
    user = Summoner(Name=me["name"], Searched="True")
    index = 0 
    for i in range(len(my_matches['matches'])): ### the most recent game comes first 
        match = my_matches[i]
        if i == 0 :
            user.Most_recent = match['gameId']
        if int(match['timestamp']) < start:
            print("for loop broken")
            break 
        game_type = match['queue']
        role = determine_role(match)
        user.Num_played += 1
        update_user_role_freq(user, role)
        queue_dict[str(game_type)].append(match)
    sort_game_type(queue_dict["420"], region, user, "Ranked Solo")
    sort_game_type(queue_dict["440"], region, user, "Ranked Flex")
    sort_game_type(queue_dict["430"], region, user, "Normal")
    sort_game_type(queue_dict["700"], region, user, "Clash")
    rank = ranked(user_name, region)
    game_result = {}
    game_result['solo'] = rank['solo']
    game_result['flex'] = rank['flex']
    game_result['summoner'] = user
    return game_result

def summoner_spell_link(spell):
    amazon = "https://riotapi-media.s3-us-west-1.amazonaws.com/Summoner_Spells/"
    end = ".png"
    return amazon + spell + end


def champ_link(champ):
    amazon = "https://riotapi-media.s3-us-west-1.amazonaws.com/tiles/"
    end = "_0.jpg"
    return amazon + champ + end


def item_link(item):
    amazon = "https://riotapi-media.s3-us-west-1.amazonaws.com/item/"
    end = ".png"
    return amazon + item + end


def perk_link(perk):
    amazon = "https://riotapi-media.s3-us-west-1.amazonaws.com/Mastery/"
    end = ".png"
    return amazon + str(perk) + end

### switch
def largest_multi_kill(kill):
    if kill == 1:
        return "    "
    elif kill == 2:
        return "Double Kill"
    elif kill == 3:
        return "Triple Kill"
    elif kill == 4:
        return "Quadra Kill"
    elif kill == 5:
        return "Penta Kill"
    else:
        return "      "


def win(boolean):
    if boolean == "False":
        return "Defeat"
    else:
        return "Victory"

def generate_match_model(game):
    champion_id = game['champion']
    champion = data.champ_dict[str(game['champion'])]
    match_detail = data.WATCHER.match.by_id(region, game['gameId'])
    identities = match_detail['participantIdentities']
    gameDuration = match_detail['gameDuration']
    match = Match(
            Match_id=game['gameId'],
            Min_played=int(gameDuration) // 60,
            Sec_played=int(gameDuration) % 60,
            Queue_type=game_type,
            Summoner=user,
            Result=""
    )
    return match
def generate_match_champion_model(participant, index):
    if int(gameDuration) // 60 < 4:
        game_result = "Remake"
    else:
        game_result = win(str(participant['stats']['win']))
    match_plus_champion = Match_Champion(
        Role=role,
        Position=index,
        Win=game_result,
        Summoner_name=identities[index]["player"]["summonerName"],
        Queue_type=game_type,
        Damage_dealt=participant['stats']['totalDamageDealtToChampions'],
        Perk0=perk_link(
            data.perk_dict[participant['stats']['perk0']]),
        Perk1=perk_link(
            data.perk_dict[participant['stats']['perk1']]),
        Perk2=perk_link(
            data.perk_dict[participant['stats']['perk2']]),
        Perk3=perk_link(
            data.perk_dict[participant['stats']['perk3']]),
        Perk4=perk_link(
            data.perk_dict[participant['stats']['perk4']]),
        Perk5=perk_link(
            data.perk_dict[participant['stats']['perk5']]),
        Item0=item_link(str(participant['stats']['item0'])),
        Item1=item_link(str(participant['stats']['item1'])),
        Item2=item_link(str(participant['stats']['item2'])),
        Item3=item_link(str(participant['stats']['item3'])),
        Item4=item_link(str(participant['stats']['item4'])),
        Item5=item_link(str(participant['stats']['item5'])),
        Item6=item_link(str(participant['stats']['item6'])),
        Champion_link=champ_link(settings.CHAMP_DICT[str(
            participant['championId'])]),
        Match_id=game['gameId'],
        Min_played=int(gameDuration) // 60,
        Sec_played=int(gameDuration) % 60,
        Champion=data.champ_dict[str(
            participant['championId'])],
        Spell1=summoner_spell_link(data.summoner_spell_dict[int(
            participant['spell1Id'])]),
        Spell2=summoner_spell_link(
            data.summoner_spell_dict[int(participant['spell2Id'])]),
        Kills=participant['stats']['kills'],
        Deaths=participant['stats']['deaths'],
        Assists=participant['stats']['assists'],
        LargestMultiKill=largest_multi_kill(
            participant['stats']['largestMultiKill']),
        Champ_level=participant['stats']['champLevel'],
        Vision_ward=int(participant['stats']['visionWardsBoughtInGame']))
    match_plus_champion.save()
    match_plus_champion.finish()
def sort_game_type(games, region, user, game_type):
    for game in games:
        match = generate_match_model(game)
        match.save()
        i = 0
        participants = match_detail['participants']
        for participant in participants:
            role = determine_role_part(participant)
            if int(gameDuration) // 60 < 4:
                game_result = "Remake"
            else:
                game_result = win(str(participant['stats']['win']))
            temp = Match_Champion(
                Role=role,
                Position=i,
                Win=game_result,
                Summoner_name=identities[i]["player"]["summonerName"],
                Queue_type=game_type,
                Damage_dealt=participant['stats']['totalDamageDealtToChampions'],
                Perk0=perk_link(
                    data.perk_dict[participant['stats']['perk0']]),
                Perk1=perk_link(
                    data.perk_dict[participant['stats']['perk1']]),
                Perk2=perk_link(
                    data.perk_dict[participant['stats']['perk2']]),
                Perk3=perk_link(
                    data.perk_dict[participant['stats']['perk3']]),
                Perk4=perk_link(
                    data.perk_dict[participant['stats']['perk4']]),
                Perk5=perk_link(
                    data.perk_dict[participant['stats']['perk5']]),
                Item0=item_link(str(participant['stats']['item0'])),
                Item1=item_link(str(participant['stats']['item1'])),
                Item2=item_link(str(participant['stats']['item2'])),
                Item3=item_link(str(participant['stats']['item3'])),
                Item4=item_link(str(participant['stats']['item4'])),
                Item5=item_link(str(participant['stats']['item5'])),
                Item6=item_link(str(participant['stats']['item6'])),
                Champion_link=champ_link(settings.CHAMP_DICT[str(
                    participant['championId'])]),
                Match_id=game['gameId'],
                Min_played=int(gameDuration) // 60,
                Sec_played=int(gameDuration) % 60,
                Champion=settings.CHAMP_DICT[str(
                    participant['championId'])],
                Spell1=summoner_spell_link(settings.SUMMONER_DICT[int(
                    participant['spell1Id'])]),
                Spell2=summoner_spell_link(
                    settings.SUMMONER_DICT[int(participant['spell2Id'])]),
                Kills=participant['stats']['kills'],
                Deaths=participant['stats']['deaths'],
                Assists=participant['stats']['assists'],
                LargestMultiKill=largest_multi_kill(
                    participant['stats']['largestMultiKill']),
                Champ_level=participant['stats']['champLevel'],
                Vision_ward=int(participant['stats']['visionWardsBoughtInGame']))
            temp.save()
            temp.finish()
            if participant['championId'] == champion_id:
                right = participant
                match.Main = temp
                temp.Summoner = user
                temp.save()
            else:
                summoner_queryset = Summoner.objects.filter(
                    Name=identities[i]['player']['summonerName'])
                if summoner_queryset.count() == 0:
                    summoner_temp = Summoner(
                        Name=identities[i]['player']['summonerName'])
                    summoner_temp.save()
                else:
                    summoner_temp = Summoner.objects.get(
                        Name=identities[i]['player']['summonerName'])
                temp.Summoner = summoner_temp
                temp.save()

            if(i < 5):
                match.Team1.add(temp)
                match.save()
            else:
                match.Team2.add(temp)
                match.save()
            match.save()
            i += 1
        champion_queryset = Champion.objects.filter(
            Summoner=user, Name=champion)
        if champion_queryset.count() == 0:
            temp1 = Champion(Name=champion, Img_link="https://riotapi-media.s3-us-west-1.amazonaws.com/tiles/" +
                             champion + "_0.jpg", Summoner=user, Queue_type=game_type)
            temp1.Mins_played += int(gameDuration) / 60
            temp1.save()
            temp1.change(right)
        else:
            temp1 = Champion.objects.get(
                Summoner=user, Name=champion)
            temp1.change(right)
            temp1.Mins_played += int(gameDuration) / 60
            temp1.save()


def search(request):
    try:
        id = request.GET.get('id')  # summoner ID
    except:
        id = None
    region = request.session['region']
    if id:
        template = "game_result.html"
        me = settings.WATCHER.summoner.by_name(region, id)
        name = me['name']
        # Check if this summoner has been searched 
        if Summoner.objects.filter(Name=name, Searched="True").count() != 0:
            print("update!")
            game_result = update(id, region)
        else: # this summoner has never been searched 
            print("New!")
            game_result = initial_search(id, region)
        rank = game_result['solo']
        flex = game_result['flex']
        summoner = game_result['summoner']
        all_matches = Match.objects.filter(Summoner=summoner)
        matches = Match.objects.filter(Summoner=summoner)[:10]
        solo = Champion.objects.filter(
            Summoner=summoner, Queue_type="Ranked Solo")[:5]
        solo_array = []
        for champion in solo:
            solo_array.append(champion)
            champion.finish()
        solo_array = sorted(
            solo_array, key=lambda x: x.Num_played, reverse=True)
        return render(request, template, {'solo': solo_array, 'rank': rank, 'flex': flex, 'matches': matches, 'all_matches': all_matches})
    else:
        solo_array = []
        template = "game_result.html"
        queryset = None
        display = []
        request.session['current_category'] = ""
        return render(request, template, {'solo': solo_array, 'rank': rank, 'region': region})
