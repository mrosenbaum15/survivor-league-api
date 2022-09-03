import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('survivor-league-db')

# set_weekly_game_results(dict team_1_result, dict team_2_result, int week#)
# each game result will have their own item for each week
    # item 1: pk = 'result', sk = 1, results = {"team1": boolean, "team2": boolean}
    # item 2: pk = 'result', sk = 2, results = {"team1": boolean, "team2": boolean}
# admin: enter each week's results from front-end (show match-up, win/loss/tie), on backend have object as such for Bears vs Packers:
# start with:
    # pk = 'result' (fixed), sk = 1 (int for week #, dynamic ?)
    # req_body (individual object):
    #    {
    #      "Bears": True, 
    #      "Packers": False,
    #       ... all 30 teams repesented, null means no result yet
    #    }
    # params: week (0 < x < 19), matchup result (bool win = T, loss/tie = F)
# then do a scan where pk = 'username' 
# for each user... update with put_item
#   if latest_week >= week #, RETURN
#   else:
#       set current user's picked team for the given week
#       if (user didn't select a team) key(Item[user_picked_teams][week #]) == "" OR user selected a LOSS:
#           is_start_streak_alive = False
#           latest_streak = 0
#       else if user was currect
#           if is_start_streak_alive:
#               start_streak++
#           latest_streak++
#           total_correct++
#           

# get_standings()
# scan where pk = 'username' 
#   example return value: 
#        {
#           "longest_start_streak": ["Rosey": 15, "Brad": 13, "Swill": 5],
#           "most_correct": ["Rosey": 15, "Swill": 14, "Brad": 13]
#        }
            
#   push first user into new dict: 
#   for each user after: 
#       for each in longest_start_streak
#           if start_streak >= other_start_streak:
#               insert before
#           else:
#               continue to next user;
#           
#           if most_correct >= other_most_correct:
#               insert before
#           else:
#               continue to next user:     
#
#        


# get_other_user_info()
# on the standings page, only allow users to see up to a given week
#      need backend to determine current week
#      pk = 'username', sk = None
#      query the DB table using pk and 'username' = <username>
#      return:
#       Item {
#           id: 'userinfo',  
#           username: <username>,
#           fullname: <fullname> 
#           other_user_picked_teams : user_picked_teams[0:curr week # - 1]
#           other_user_start_streak: user_start_streak,
#           other_is_start_streak_alive: is_start_streak_alive,
#           other_latest_streak: latest_streak,
#           other_total_correct: total_curect,
#           other_latest_week: 0 
#       }


# get_all_matchups()
# return all matchups - get every matchup for all 18 weeks
    # pk = 'matchup' (fixed), sk = None
    # resp_body (list of list of strings):
    # [
    #   [
    #    "Chicago Bears vs Minnesota Vikings,
    #    "Dallas Cowboys vs New York Giants"
    #   ],
    #   [
    #    "Chicago Bears vs Green Bay Packers,
    #    "Dallas Cowboys vs Philadelphia Eagles"
    #   ]
    # ]

def get_all_matchups():
    try:
        resp = table.query(KeyConditionExpression= Key('type').eq('matchup') &  Key('id').eq('all'))
        return resp["Items"][0]["matchups"]
    except Exception as e:
        raise Exception("Unable to get matchups with error: " + str(e))

# submit_user_pick(string username, string team, int week #)
# submit user's pick for a given week
#   if week is before current week or team already used, reject
#   safest way is to take user info, get the user's entire info via a scan. 
#   Then write to id = 'username', username (global secondary index) = <username>
#         update user_picked_teams[week #] = <team>: null
#         write user entire user object back as an item 

def submit_user_pick(body):
    username = body["username"]
    week_num = body["weekNum"]
    team = body["pick"].strip()

    try:
        resp = table.query(KeyConditionExpression= Key('type').eq('userinfo') & Key('id').eq(username))
        curr_user = resp["Items"][0]

        curr_user["user_picked_teams"][week_num-1] = {team: ""}

        table.put_item(
            Item=curr_user
        )
    except Exception as e:
        raise Exception("Unable to submit pick with error: " + str(e))




def lambda_handler(event, context):
    print(event)
    print("RETURNING 200")
    
    matchups = []
    if(event["path"] == "/get-all-matchups"):
        print("GETTING ALL MATCHUPS")
        matchups = get_all_matchups()
        return {
            "statusCode": 200,
            "body": json.dumps(matchups),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": '*'
            }
        }    


    elif(event["path"] == "/submit-pick"):
        print("SUBMITTING PICK")
        submit_user_pick(json.loads(event["body"]))
        return {
            "statusCode": 201,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": '*'
            }
        }    

    
    print(json.dumps(matchups))



