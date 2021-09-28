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
API_KEY = 'RGAPI-7ab293e7-9951-4edb-8039-ae08a67df3d0'
WATCHER = LolWatcher(API_KEY)
def NA(request):
    request.session['region'] = "na1"
    return render(request, 'base.html',
                  {'region': "NA"})
def update_summoner_role_freq(summoner, role):
    if role == "TOP":
        summoner.Top_played += 1
    elif role == "MID":
        summoner.Mid_played += 1
    elif role == "JUN":
        summoner.Jun_played += 1
    elif role == "SUP":
        summoner.Sup_played += 1
    else:
        summoner.Adc_played += 1
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
    champion = data.champ_dict[str(participant['championId'])]
    role = participant['timeline']['role']
    lane = participant['timeline']['lane']
    entry = (lane, role)
    game_result = data.position[entry]
    if game_result != "BUG":
        return game_result
    else:
        return data.champion_to_role[champion]

def show_region_specific_page(request):
    region = region_to_name[request.session['region']]
    return render(request, 'base.html', {'region': region})

def time_stamp(region):
    shift = data.time_shifts_by_server[region]
    start = 1000 * (data.season["11"] + shift)
    return start

def generate_rank_info(rank):
    solo_rank_info = {}
    solo_rank_info["summoner_name"] = rank["summonerName"]
    solo_rank_info["wins"] = rank["wins"]
    solo_rank_info["losses"] = rank["losses"]
    solo_rank_info["win_ratio"] = round(
        100 * solo_rank_info["wins"]/(solo_rank_info["losses"] + solo_rank_info["wins"]))
    solo_rank_info["lp"] = rank["leaguePoints"]
    solo_rank_info["tier"] = rank["tier"]
    solo_rank_info["rank"] = rank["rank"]
    solo_rank_info["link"] = "https://riotapi-media.s3-us-west-1.amazonaws.com/images/" + \
        rank["tier"] + rank["rank"] + ".png"
    return solo_rank_info

def ranked(user_name, region):
    me = data.WATCHER.summoner.by_name(region, user_name)
    my_ranked_stats = data.WATCHER.league.by_summoner(region, me['id'])
    flex_rank = None
    solo_rank = None
    ranked = {}
    for rank_info in my_ranked_stats:
        if rank_info["queueType"] == "RANKED_FLEX_SR":
            flex_rank = rank_info
        else:
            solo_rank = rank_info
    if solo_rank:
        solo_rank_info = generate_rank_info(solo_rank)
        ranked['solo'] = solo_rank_info
    if flex_rank:
        flex_rank_info = generate_rank_info(flex_rank)
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
    game_result['region'] = region
    return game_result

def initial_search(me, region):
    queue_dict = defaultdict(list)
    print(me)
    my_matches = WATCHER.match.matchlist_by_account(
        region, me)
    start = time_stamp(region)
    user = Summoner(Name=me["name"], Searched="True")
    index = 0 
    for i in range(len(my_matches['matches'])): ### the most recent game comes first 
        match = my_matches[i]
        if i == 0 :
            user.Most_recent = match['gameId']
        if int(match['timestamp']) < start:
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
    game_result['region'] = region
    return game_result

def to_link(item, group):
    amazon = "https://riotapi-media.s3-us-west-1.amazonaws.com/"
    middle = type_to_txt[group]
    end = type_to_file_type[group]
    return amazon + middle + "/" + end 

### switch
def largest_multi_kill(kill):
    return data.kils_numeric_to_english[kill]

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
def generate_match_champion_model(participant, identities, game):
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
        Perk0=to_link(
            data.perk_dict[participant['stats']['perk0']], perk),
        Perk1=to_link(
            data.perk_dict[participant['stats']['perk1']], perk),
        Perk2=to_link(
            data.perk_dict[participant['stats']['perk2']], perk),
        Perk3=to_link(
            data.perk_dict[participant['stats']['perk3']], perk),
        Perk4=to_link(
            data.perk_dict[participant['stats']['perk4']], perk),
        Perk5=tok_link(
            data.perk_dict[participant['stats']['perk5']]),
        Item0=to_link(str(participant['stats']['item0']), item),
        Item1=to_link(str(participant['stats']['item1']), item),
        Item2=to_link(str(participant['stats']['item2']), item),
        Item3=to_link(str(participant['stats']['item3']), item),
        Item4=to_link(str(participant['stats']['item4']), item),
        Item5=to_link(str(participant['stats']['item5']), item),
        Item6=to_link(str(participant['stats']['item6']), item),
        Champion_link=to_link(settings.CHAMP_DICT[str(
            participant['championId'])], champ),
        Match_id=game['gameId'],
        Min_played=int(gameDuration) // 60,
        Sec_played=int(gameDuration) % 60,
        Champion=data.champ_dict[str(
            participant['championId'])],
        Spell1=to_link(data.summoner_spell_dict[int(
            participant['spell1Id'])], spell),
        Spell2=to_link(
            data.summoner_spell_dict[int(participant['spell2Id'])], spell),
        Kills=participant['stats']['kills'],
        Deaths=participant['stats']['deaths'],
        Assists=participant['stats']['assists'],
        LargestMultiKill=largest_multi_kill(
            participant['stats']['largestMultiKill']),
        Champ_level=participant['stats']['champLevel'],
        Vision_ward=int(participant['stats']['visionWardsBoughtInGame']))
    match_plus_champion.save()
    match_plus_champion.finish()
    return match_plus_champion

def modify_or_create_summoner(participants, champion_id, match_champion_model, match, index):
    if participant['championId'] == champion_id:
        match.Main = match_champion_model
        match_champion_model.Summoner = user
        match_champion_model.save()
        return participant
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
            match_champion_model.Summoner = summoner_temp
            match_champion_model.save()

        if(index < 5):
            match.Team1.add(match_champion_model)
            match.save()
        else:
            match.Team2.add(match_champion_model)
            match.save()
        match.save()
        return None
 
def create_or_modify_champion_model(user, champion, right, game_duration, game_type):
    champion_queryset = Champion.objects.filter(
        Summoner=user, Name=champion)
    if champion_queryset.count() == 0:
        champion_model = Champion(Name=champion, Img_link="https://riotapi-media.s3-us-west-1.amazonaws.com/tiles/" +
            champion + "_0.jpg", Summoner=user, Queue_type=game_type)
        champion_model.Mins_played += int(game_duration) / 60
        champion_model.save()
        champion_model.change(right)
    else:
        champion_model = Champion.objects.get(
            Summoner=user, Name=champion)
        champion_model.change(right)
        champion_model.Mins_played += int(game_duration) / 60
        champion_model.save()

def sort_game_type(games, region, user, game_type):
    for game in games:
        match = generate_match_model(game)
        match_detail = data.WATCHER.match.by_id(region, game['gameId'])
        game_duration = match_detail['gameDuration']
        champion = data.champ_dict[str(game['champion'])]
        champion_id= game['champion']
        identities = match_detail['participantIdentities']
        match.save()
        i = 0
        participants = match_detail['participants']
        for participant in participants:
            role = determine_role_part(participant)
            if int(game_duration) // 60 < 4:
                game_result = "Remake"
            else:
                game_result = win(str(participant['stats']['win']))
            match_champion_model = generate_match_champion_model(participant, identities, game)
            result = modify_or_create_summoner(participant, champion_id, match_champion_model, match, i)
            i += 1
            if result != None:
                right = result 
        create_or_modify_champion_model(user, champion, right, game_duration)

def generate_invalid_dataset(region):
    solo_array = []
    rank = []
    return {'solo' : solo_array, 'rank':rank, 'region':region}

def generate_valid_dataset(game_result):
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
    return {'solo' : solo_array, 'rank':rank, 'flex':flex, 'matches': matches, 'all_matches': all_matches}

def search(request):
    try:
        id = request.GET.get('id')  # summoner ID
    except:
        id = None
    region = request.session['region']
    template = "result.html"
    if id:
        print("id")
        print(id)
        me = WATCHER.summoner.by_name(region, id)
        print("me in init")
        print(me)
        name = me['id']
        # Check if this summoner has been searched 
        if Summoner.objects.filter(Name=name, Searched="True").count() != 0:
            game_result = update(name, region)
        else: # this summoner has never been searched 
            game_result = initial_search(name, region)
        dataset = generate_valid_dataset(game_result)
        return render(request, template, dataset)
    else:
        request.session['current_category'] = ""
        dataset = generate_invalid_dataset(region)
        return render(request, template, dataset)
