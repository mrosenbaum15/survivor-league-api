import json
from datetime import datetime, timedelta
import boto3
from boto3.dynamodb.conditions import Key
from src.utils.utils import get_current_week, week_to_date_range, is_dst

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('survivor-league-db')


# setup_new_user(string username, string fullname)
# after registration, add empty user
    # pk = 'userinfo' (fixed), sk = None
    # req_body:
    # Item {
    #   id: 'userinfo',  
    #   username: <username>,
    #   name: <fullname>,
    #   user_picked_teams : {"": null, "": null, "": null, "": , "": null, "": null, "": null, "": null, "": null, "": null, "": null, "": null, "": null, "": null, "": null, "": null, "": null, "": null},
    #   start_streak: 0,
    #   is_start_streak_alive: true,
    #   latest_streak: 0,
    #   total_correct: 0,
    #   latest_week: 0 
    # }

def setup_new_user(body):
    username = body["username"]
    fullname= body["fullname"]

    print(username + fullname)
    try:
        table.put_item(
            Item={
                'type': 'userinfo',
                'id': username,
                'username': username,
                'name': fullname,
                'user_picked_teams':  [{"Team": ""},{"Team": ""},{"Team": ""},{"Team": ""},{"Team": ""},{"Team": ""},{"Team": ""},{"Team": ""},{"Team": ""},{"Team": ""},{"Team": ""},{"Team": ""},{"Team": ""},{"Team": ""},{"Team": ""},{"Team": ""},{"Team": ""},{"Team": ""}],
                'start_streak': 0,
                'is_start_streak_alive': True,
                'latest_streak': 0,
                'total_correct': 0,
                'latest_week': 0
            }
        )
    except Exception as e:
        raise Exception("Unable to create new user with error: " + str(e))
        

# get_curr_user_info(string username, string fullname)
# return all relevant info about a user
    # pk = 'userinfo' (fixed), sk = None
    # resp_body:
    # Item {
    #   id: 'userinfo',
    #   username: <username>,
    #   name: <fullname>,
    #   user_picked_teams : {"Rams": true, "Browns": true, "Broncos": true, "Cowboys": true, "Buccaneers": true, "Steelers": true, "Cardinals": true, "Chiefs": true, "Colts": true, "Bills": true, "Titans": false, "Texans": false, "Dolphins": true, "Chargers": true, "Niners": true, "Eagles": true, "Patriots": true, "Packers": null},
    #   start_streak: int,
    #   is_start_streak_alive: bool
    #   latest_streak: int
    #   total_correct: int,
    #   latest_week: int,
    # }

def get_curr_user_info(username):

    try:
        resp = table.query(KeyConditionExpression= Key('type').eq('userinfo') & Key('id').eq(username))
        userinfo = resp["Items"][0]

        return {
            "username": userinfo["username"],
            "fullname": userinfo["name"],
            "start_streak": int(userinfo['start_streak']),
            "total_correct": int(userinfo['total_correct']),
            "is_start_streak_alive": userinfo['is_start_streak_alive'],
            "user_picked_teams": userinfo["user_picked_teams"]
        }
    except Exception as e:
        raise Exception("Unable to get user info with error: " + str(e))

        
def get_curr_user_info_standings(username):

    try:
        resp = table.query(KeyConditionExpression= Key('type').eq('userinfo') & Key('id').eq(username))
        userinfo = resp["Items"][0]
        
        week_num = get_current_week()
        sunday_of_curr_week = week_to_date_range(week_num)
        
        print("DONE WITH SUNDAY OF CURR WEEK")
        today = datetime.now()

        print(sunday_of_curr_week)
        print(type(sunday_of_curr_week))

        target_date = datetime.strptime(sunday_of_curr_week, '%d-%m-%Y %H:%M:%S')

        print(target_date)
        print(type(target_date))
        
        print(today)
        print(type(today))

        user_picks = []
        if(today < target_date and week_num > 1):
            user_picks = userinfo["user_picked_teams"][0:(week_num-1)]
        elif(today >= target_date and week_num == 1):
            user_picks.append(userinfo["user_picked_teams"][0])                          
        elif(today >= target_date):
            user_picks = userinfo["user_picked_teams"][0:week_num]                    
        
        print(user_picks)
        return {
            "username": userinfo["username"],
            "fullname": userinfo["name"],
            "start_streak": int(userinfo['start_streak']),
            "total_correct": int(userinfo['total_correct']),
            "is_start_streak_alive": userinfo['is_start_streak_alive'],
            "user_picked_teams": user_picks
        }
    except Exception as e:
        raise Exception("Unable to get user info with error: " + str(e))        

# submit_user_pick(string username, string team, int week #)
# submit user's pick for a given week
#   if week is before current week or team already used, reject
#   safest way is to take user info, get the user's entire info via a scan. 
#   Then write to id = 'username', username (global secondary index) = <username>
#         update user_picked_teams[week #] = <team>: null
#         write user entire user object back as an item 

def get_all_users(week_num):
    try:

        week_num = get_current_week()
        sunday_of_curr_week = week_to_date_range(week_num)
        
        print("DONE WITH SUNDAY OF CURR WEEK")
        today = datetime.now()

        print(sunday_of_curr_week)
        print(type(sunday_of_curr_week))

        target_date = datetime.strptime(sunday_of_curr_week, '%d-%m-%Y %H:%M:%S')

        print(target_date)
        print(type(target_date))
        
        print(today)
        print(type(today))

        # user_picks = []
        # if(today < target_date and week_num > 1):
        #     user_picks = userinfo["user_picked_teams"][0:(week_num-2)]            
        # elif(today >= target_date):
        #     user_picks = userinfo["user_picked_teams"][0:(week_num-1)]                    
        
        resp = table.query(KeyConditionExpression= Key('type').eq('userinfo'))
        userinfo = resp["Items"]

        print(userinfo)
        
        user_return = []
        for user in userinfo:
            user_return.append({user['id']: user['user_picked_teams'][int(week_num)-1]})
        return user_return
    except Exception as e:
        raise Exception("Unable to get user info with error: " + str(e))




def lambda_handler(event, context):
    print(event)
    
    if(event["path"] == "/setup-new-user"):
        print("Setting up new user")
        code = setup_new_user(json.loads(event["body"]))
        return {
            "statusCode": 201,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": '*'
            }
        }    

    elif(event["path"] == "/userinfo"):
        print("Getting user info")
        user = get_curr_user_info(event["queryStringParameters"]["user"])
        return {
            "statusCode": 200,
            "body": json.dumps(user, sort_keys=True),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": '*'
                }
            }    

    elif(event["path"] == "/user-info-standings"):
        print("Getting user info for standings")
        user = get_curr_user_info_standings(event["queryStringParameters"]["user"])
        return {
            "statusCode": 200,
            "body": json.dumps(user, sort_keys=True),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": '*'
                }
            }                

    elif(event["path"] == "/all-users"):
        print("Getting user info for Current Week")
        users = get_all_users(event["queryStringParameters"]["week_num"])
        return {
            "statusCode": 200,
            "body": json.dumps(users, sort_keys=True),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": '*'
                }
            }                


