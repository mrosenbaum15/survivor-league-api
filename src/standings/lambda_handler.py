import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('survivor-league-db')

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

def get_standings():
    try: 
        resp = table.query(KeyConditionExpression= Key('type').eq('userinfo'))
        users = resp["Items"]

        print(resp)
        
        i = 0
        longest_start_streak_arr = []
        most_correct_arr = []
        for user in users:
            name = user['name']
            username = user['username']
            start_streak = int(user['start_streak'])
            total_correct = int(user['total_correct'])
            is_start_streak_alive = user['is_start_streak_alive']

            user_longest_obj = {username: [start_streak, is_start_streak_alive, username]}
            user_most_obj = {username: total_correct}

            if(i == 0):
                longest_start_streak_arr.append(user_longest_obj)
                most_correct_arr.append(user_most_obj)
                i += 1
                continue
            
            print(longest_start_streak_arr)
            j = 1
            for item in longest_start_streak_arr:
                other_vals = next(iter(item.values()))
                if(start_streak > other_vals[0]):
                    longest_start_streak_arr.insert(j-1, user_longest_obj)  
                    break
                elif(start_streak == other_vals[0]):
                    if(not is_start_streak_alive):
                        longest_start_streak_arr.insert(j, user_longest_obj)
                    else:
                        longest_start_streak_arr.insert(j-1, user_longest_obj)    
                    break
                j += 1 
            
            k = 1
            for item in most_correct_arr:
                if(total_correct >= next(iter(item.values()))):
                    most_correct_arr.insert(k-1, user_most_obj)     
                    break
                k += 1
                

            i += 1


        return {
            'longest_start_streak': longest_start_streak_arr,
            'most_correct': most_correct_arr
        }
    except Exception as e:
        raise Exception("Unable to get standings with error: " + str(e))

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

def lambda_handler(event, context):
    print(event)
    
    if(event["path"] == "/standings"):
        print("GETTING STANDINGS")
        standings_val = get_standings()

    return {
        "statusCode": 200,
        "body": json.dumps(standings_val),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": '*'
            }
        }    


