import json
import traceback
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('survivor-league-db')

def get_standings():
    resp = table.query(KeyConditionExpression= Key('type').eq('userinfo'))
    users = resp['Items']
    
    i = 0
    longest_start_streak_arr = []
    most_correct_arr = []
    for user in users:
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
            elif(j == len(longest_start_streak_arr)):
                longest_start_streak_arr.append(user_longest_obj)
                break
            j += 1 

        k = 1
        for item in most_correct_arr:
            if(total_correct >= next(iter(item.values()))):
                most_correct_arr.insert(k-1, user_most_obj)     
                break
            elif(k == len(most_correct_arr)):
                most_correct_arr.append(user_most_obj)
                break
            k += 1
            

        i += 1


    return {
        'longest_start_streak': longest_start_streak_arr,
        'most_correct': most_correct_arr
    }

def lambda_handler(event, context):
    try:    
        if(event['path'] == '/standings'):
            standings_val = get_standings()

        return {
            'statusCode': 200,
            'body': json.dumps(standings_val),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
                }
            }    
    except Exception as e:
        traceback.print_exc()
        response_data = {
            'statusCode': 500,
            'error': 'Error running standings API: ' + str(e)
        }
        return response_data

