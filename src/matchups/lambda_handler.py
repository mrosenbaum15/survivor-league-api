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
        return resp["Items"][0]["matchups"], resp["Items"][0]["deadlines"]
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
        matchups, deadlines = get_all_matchups()
        return_body = {
            "matchups": matchups,
            "deadlines": deadlines
        }
        return {
            "statusCode": 200,
            "body": json.dumps(return_body),
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



