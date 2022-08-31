import json
import boto3
from boto3.dynamodb.conditions import Key

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

def setup_new_user(username, fullname):
    try:
        table.put_item(
            Item={
                'type': 'userinfo',
                'id': username,
                'username': username,
                'name': fullname,
                'user_picked_teams':  {"Team": "","Team": "","Team": "","Team": "","Team": "","Team": "","Team": "","Team": "","Team": "","Team": "","Team": "","Team": "","Team": "","Team": "","Team": "","Team": "","Team": "","Team": ""},
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

# submit_user_pick(string username, string team, int week #)
# submit user's pick for a given week
#   if week is before current week or team already used, reject
#   safest way is to take user info, get the user's entire info via a scan. 
#   Then write to id = 'username', username (global secondary index) = <username>
#         update user_picked_teams[week #] = <team>: null
#         write user entire user object back as an item 





def lambda_handler(event, context):
    print(event)
    body = json.loads(event["body"])
    
    if(event["path"] == "/setup-new-user"):
        print("Setting up new user")
        setup_new_user(body["username"], body["fullname"])

    return {
        "statusCode": 201,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": '*'
            }
        }    


