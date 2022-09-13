import pytz
from datetime import date, timedelta, datetime
import time

def is_dst(dt, timezone="America/Chicago"):
    if dt is None:
        dt = datetime.utcnow()
    timezone = pytz.timezone(timezone)
    timezone_aware_date = timezone.localize(dt, is_dst=None)
    return timezone_aware_date.tzinfo._dst.seconds != 0 

def get_current_week():
    today = datetime.now()
    
    if(is_dst(today)):
        hour_diff = 5
    else:
        hour_diff = 6

    today = (today - timedelta(hours=hour_diff)).strftime("%d-%m-%Y")
    
    today = datetime.strptime(today, "%d-%m-%Y")
    print(today)

    if(today >= datetime.strptime("13-09-2022", "%d-%m-%Y") and today < datetime.strptime("20-09-2022", "%d-%m-%Y")):
        return 2
    elif(today >= datetime.strptime("20-09-2022", "%d-%m-%Y") and today < datetime.strptime("27-09-2022", "%d-%m-%Y")):
        return 3
    elif(today >= datetime.strptime("27-09-2022", "%d-%m-%Y") and today < datetime.strptime("04-10-2022", "%d-%m-%Y")):
        return 4
    elif(today >= datetime.strptime("04-10-2022", "%d-%m-%Y") and today < datetime.strptime("11-10-2022", "%d-%m-%Y")):
        return 5
    elif(today >= datetime.strptime("11-10-2022", "%d-%m-%Y") and today < datetime.strptime("18-10-2022", "%d-%m-%Y")):
        return 6
    elif(today >= datetime.strptime("18-10-2022", "%d-%m-%Y") and today < datetime.strptime("25-10-2022", "%d-%m-%Y")):
        return 7
    elif(today >= datetime.strptime("25-10-2022", "%d-%m-%Y") and today < datetime.strptime("01-11-2022", "%d-%m-%Y")):
        return 8
    elif(today >= datetime.strptime("01-11-2022", "%d-%m-%Y") and today < datetime.strptime("08-11-2022", "%d-%m-%Y")):
        return 9
    elif(today >= datetime.strptime("08-11-2022", "%d-%m-%Y") and today < datetime.strptime("15-11-2022", "%d-%m-%Y")):
        return 10
    elif(today >= datetime.strptime("15-11-2022", "%d-%m-%Y") and today < datetime.strptime("22-11-2022", "%d-%m-%Y")):
        return 11
    elif(today >= datetime.strptime("22-11-2022", "%d-%m-%Y") and today < datetime.strptime("29-11-2022", "%d-%m-%Y")):
        return 12
    elif(today >= datetime.strptime("29-11-2022", "%d-%m-%Y") and today < datetime.strptime("06-12-2022", "%d-%m-%Y")):
        return 13
    elif(today >= datetime.strptime("06-12-2022", "%d-%m-%Y") and today < datetime.strptime("13-12-2022", "%d-%m-%Y")):
        return 14
    elif(today >= datetime.strptime("13-12-2022", "%d-%m-%Y") and today < datetime.strptime("20-12-2022", "%d-%m-%Y")):
        return 15
    elif(today >= datetime.strptime("20-12-2022", "%d-%m-%Y") and today < datetime.strptime("27-12-2022", "%d-%m-%Y")):
        return 16
    elif(today >= datetime.strptime("27-12-2022", "%d-%m-%Y") and today < datetime.strptime("03-01-2023", "%d-%m-%Y")):
        return 17
    elif(today >= datetime.strptime("03-01-2023", "%d-%m-%Y") and today < datetime.strptime("10-01-2023", "%d-%m-%Y")):
        return 18
    else:
        return 1


def week_to_date_range(week_num):

    if(week_num == 2):
        first_date = datetime.strptime("13-09-2022", "%d-%m-%Y")
        second_date = datetime.strptime("20-09-2022", "%d-%m-%Y")
    elif(week_num == 3):
        first_date = datetime.strptime("20-09-2022", "%d-%m-%Y")
        second_date = datetime.strptime("27-09-2022", "%d-%m-%Y")
    elif(week_num == 4):
        first_date = datetime.strptime("27-09-2022", "%d-%m-%Y")
        second_date = datetime.strptime("04-10-2022", "%d-%m-%Y")
    elif(week_num == 5):
        first_date = datetime.strptime("04-10-2022", "%d-%m-%Y")
        second_date = datetime.strptime("11-10-2022", "%d-%m-%Y")
    elif(week_num == 6):
        first_date = datetime.strptime("11-10-2022", "%d-%m-%Y")
        second_date = datetime.strptime("18-10-2022", "%d-%m-%Y")
    elif(week_num == 7):
        first_date = datetime.strptime("18-10-2022", "%d-%m-%Y")
        second_date = datetime.strptime("25-10-2022", "%d-%m-%Y")                                
    elif(week_num == 8):
        first_date = datetime.strptime("25-10-2022", "%d-%m-%Y")
        second_date = datetime.strptime("01-11-2022", "%d-%m-%Y")
    elif(week_num == 9):
        first_date = datetime.strptime("01-11-2022", "%d-%m-%Y")
        second_date = datetime.strptime("08-11-2022", "%d-%m-%Y")
    elif(week_num == 10):
        first_date = datetime.strptime("08-11-2022", "%d-%m-%Y")
        second_date = datetime.strptime("15-11-2022", "%d-%m-%Y")
    elif(week_num == 11):
        first_date = datetime.strptime("15-11-2022", "%d-%m-%Y")
        second_date = datetime.strptime("22-11-2022", "%d-%m-%Y")
    elif(week_num == 12):
        first_date = datetime.strptime("22-11-2022", "%d-%m-%Y")
        second_date = datetime.strptime("29-11-2022", "%d-%m-%Y") 
    elif(week_num == 13):
        first_date = datetime.strptime("29-11-2022", "%d-%m-%Y")
        second_date = datetime.strptime("06-12-2022", "%d-%m-%Y")
    elif(week_num == 14):
        first_date = datetime.strptime("06-12-2022", "%d-%m-%Y")
        second_date = datetime.strptime("13-12-2022", "%d-%m-%Y")
    elif(week_num == 15):
        first_date = datetime.strptime("13-12-2022", "%d-%m-%Y")
        second_date = datetime.strptime("20-12-2022", "%d-%m-%Y")
    elif(week_num == 16):
        first_date = datetime.strptime("20-12-2022", "%d-%m-%Y")
        second_date = datetime.strptime("27-12-2022", "%d-%m-%Y")
    elif(week_num == 17):
        first_date = datetime.strptime("27-12-2022", "%d-%m-%Y")
        second_date = datetime.strptime("03-01-2023", "%d-%m-%Y")
    elif(week_num == 18):
        first_date = datetime.strptime("03-01-2023", "%d-%m-%Y")
        second_date = datetime.strptime("10-01-2023", "%d-%m-%Y")                  
    else:
        first_date = datetime.strptime("06-09-2022", "%d-%m-%Y")
        second_date = datetime.strptime("13-09-2022", "%d-%m-%Y")      

    print(first_date)
    print(second_date)
    result = ""

    if(is_dst(datetime.now())):
        hour_diff = 17
    else:
        hour_diff = 18

    while first_date <= second_date:
        if week_num == 16 and first_date.weekday() == 5:   #0 == Monday
            return (first_date + timedelta(hours=hour_diff)).strftime("%d-%m-%Y %H:%M:%S")
        elif first_date.weekday() == 6:   #0 == Monday
            return (first_date + timedelta(hours=hour_diff)).strftime("%d-%m-%Y %H:%M:%S")    
        first_date += timedelta(days=1)




