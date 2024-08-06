import utility

def analyze_over(over, detailed=False):
    deliveries=over.get("deliveries")
    score=0
    wickets=0

    for delivery_no, delivery in enumerate(deliveries):
        runs=delivery.get("runs")
        score=score + runs.get("total",0)

        wicket=delivery.get("wickets",[])
        wickets=wickets + len(wicket)

        if detailed:
            print(f"    {delivery_no+1}: {score}/{wickets}")

    return score, wickets

def analyze_innings(innings, detailed=False):
    overs=innings.get("overs")

    score=0
    wickets=0 

    for over_no, over in enumerate(overs):
        score_in_over, wickets_in_over = analyze_over(over)
        score = score + score_in_over
        wickets = wickets + wickets_in_over

        if detailed:
            print(f"{over_no+1}: {score}/{wickets}\n\n")
    
    innings =  innings.get("team","Unknwon")

    return score, wickets, innings

def get_match_summary(match):
    match_info = match.get('info',{})
    date_of_match = match_info.get('dates',[])[0]
    match_type_number=match_info.get('match_type_number',0)
    teams=match_info.get("teams",[])
    outcome=match_info.get("outcome",{})
    winner=outcome.get("winner","Unknown")

    return match_type_number, date_of_match, teams, winner


def analyze_match(match, detailed=False):
    innings=match.get("innings",[])

    first_innings=innings[0]
    second_innings=innings[1]

    first_innings_score, first_innings_wickets, first_innings_batting = analyze_innings(first_innings)
    second_innings_score, second_innings_wickets, second_innings_batting = analyze_innings(second_innings)

    match_info = match.get('info',{})
    date_of_match = match_info.get('dates',[])[0]
    match_type_number=match_info.get('match_type_number',0)

    outcome=match_info.get("outcome",{})
    winner=outcome.get("winner","Unknown")

    if detailed:
        print(f"{match_type_number } {date_of_match} {first_innings_batting}: {first_innings_score}/{first_innings_wickets} : {second_innings_batting} {second_innings_score}/{second_innings_wickets}  W:{winner}")


def is_player_playing_in_match(player,match):
    info=match.get("info",{})
    players=info.get("players")

    for team in players:
        players_in_team = players.get(team)
        for player_in_team in players_in_team:
            #print(player_in_team)
            if player == player_in_team:
                return True
    
    return False


def analyze_batsman_in_match(player, match):


    played_in_match=False
    runs_scored=0
    count_of_sixes=0
    count_of_fours=0
    count_of_outs=0
    balls_faced=0

    if is_player_playing_in_match(player,match):
        played_in_match=True
        innings=match.get("innings",[])
        for inning in innings:
            overs=inning.get("overs")
            for over in overs:
                deliveries=over.get("deliveries")
                for delivery in deliveries:
                    batter=delivery.get("batter")
                    if player == batter:
                        balls_faced=balls_faced+1
                        runs=delivery.get("runs",{}).get("batter",0)
                        runs_scored=runs_scored+runs
                        if runs==6:
                            count_of_sixes = count_of_sixes+1
                        elif runs == 4:
                            count_of_fours = count_of_fours +1

                    wickets=delivery.get("wickets",[])
                    for wicket in wickets:
                        if wicket.get("player_out")==player:
                            count_of_outs = count_of_outs+1
        
 #       print(f' {player} {runs_scored} ({balls_faced}) fours:{count_of_fours} sixes:{count_of_sixes} out:{count_of_outs}')
 #   else:
 #       print(f' {player} not playing in this match')

    return {
            'played_in_match':played_in_match,
            'player':player,
            'runs_scored':runs_scored,
            'balls_faced':balls_faced,
            'count_of_fours':count_of_fours,
            'count_of_sixes':count_of_sixes,
            'count_of_outs':count_of_outs
        }




    return
import traceback 

def analyze_batsman(name, matches):
    for match_type_number in sorted(matches):
        try:
            match=matches.get(match_type_number)
            player_summary_in_match = analyze_batsman_in_match(name,match)
            if player_summary_in_match.get("played_in_match"):
                   match_type_number, date_of_match, teams, winner = get_match_summary(match)
                   print(f" {match_type_number } {date_of_match} {teams}: {winner} {player_summary_in_match.get("player")} {player_summary_in_match.get("runs_scored")} ({player_summary_in_match.get("balls_faced")}) fours:{player_summary_in_match.get("count_of_fours")} sixes:{player_summary_in_match.get("count_of_sixes")} out:{player_summary_in_match.get("count_of_sixes")}" )
 
        except Exception as e:
            print(f"Skipping  match {match_type_number} due to {e}")
            traceback.print_exc()

        
def analyze_all_matches(matches):
    for match_type_number in sorted(matches):
        try:
            match=matches.get(match_type_number)
            analyze_match(match,True)
        except:
            print(f"Skipping  match {match_type_number}")


def get_matches(mode="test"):
 
    config=utility.get_config()
    data_path= config.get("data_path",{}).get(mode,"")
    
    file_name=data_path + "/all.json"

    matches=utility.read_file_if_exists(file_name)

    if matches is None:
        matches=utility.read_all_files_and_save(data_path+"/odis_male_json",file_name)
   
    matches_to_be_sorted = {}
    for match_idx, match_id in enumerate(matches):
        try:
            match=matches.get(match_id)
            match_info = match.get('info',{})
            match_type_number=match_info.get('match_type_number',0)
            matches_to_be_sorted[match_type_number]= match
        except:
            print(f"Skipping  match {match_id}")

    return matches_to_be_sorted

import time


config = utility.get_config()
mode = config.get("mode","test")

tic = time.perf_counter()
matches=get_matches(mode)
#analyze_all_matches(matches)
toc = time.perf_counter()
print(f"Loaded matches in {toc - tic:0.4f} seconds")

tic = time.perf_counter()

for i in range(1, 2):
    analyze_batsman("V Kohli", matches)
    analyze_batsman("MS Dhoni", matches)
    analyze_batsman("RG Sharma", matches)
    analyze_batsman("DA Miller", matches)
    analyze_batsman("AB de Villiers", matches)
    i = i+1

toc = time.perf_counter()
print(f"Analyzed players in {toc - tic:0.4f} seconds")

