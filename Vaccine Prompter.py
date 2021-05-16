import requests
from fake_useragent import UserAgent
import json
import pandas as pd
from datetime import datetime, timedelta
from playsound import playsound
import multiprocessing
from configparser import ConfigParser
import sched, time

# TO GET THE STATE ID
# https://cdn-api.co-vin.in/api/v2/admin/location/states


# TO GET THE DISTRICT ID
# https://cdn-api.co-vin.in/api/v2/admin/location/districts/{state_id}

def check_availibilty(sc):
    
    temp_user_agent = UserAgent()
    browser_header = {'User-Agent': temp_user_agent.random}
    
    presentday = datetime.now()
    tomorrow = presentday + timedelta(1)
    date = tomorrow.strftime('%d-%m-%Y')
    print("looping for date {}".format(date))
    
    configur = ConfigParser()
    configur.read('config.ini')
    pincode = configur.get('location','pincode')
    district_id = configur.get('location','district')
    
    request_url_pincode = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}".format(pincode, date)
    request_url_disrict_id = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}".format(district_id, date)
    
    
    response = requests.get(request_url_disrict_id, headers=browser_header)
    resp_json = json.loads(response.text)['sessions']
    
    df = pd.DataFrame(resp_json)
    df_min_age_limit = df['min_age_limit']
    df_availabilty = df['available_capacity_dose1']
    for key, value in df_availabilty.iteritems():
        if df_min_age_limit[key] == 18 and value > 0:
            print(key, value)
            playsound('Coldplay - Fix You.mp3')
            # Might as well play a song :p
            p = multiprocessing.Process(target=playsound, args=("Coldplay - Fix You.mp3",))
            p.start()
            input("press ENTER to stop playback")
            p.terminate()
    
    s.enter(4, 1, check_availibilty, (sc,))

s = sched.scheduler(time.time, time.sleep)
s.enter(0, 1, check_availibilty, (s,))
s.run()



