from calendar import day_name, month
import re
import pandas as pd

def preprocess(data):

    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s[AP]M)?\s-\s'
    
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    
 
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    
   
    def parse_date(date_str):
        date_str = date_str.replace('\u202f', ' ')
        for fmt in ('%m/%d/%y, %I:%M %p - ', '%m/%d/%Y, %I:%M %p - '):
            try:
                return pd.to_datetime(date_str, format=fmt)
            except ValueError:
                continue
        return pd.NaT
    df['date'] = df['message_date'].apply(parse_date)
    df.drop(columns=['message_date'], inplace=True)
    
    
    users = []
    cleaned_messages = []
    
    for message in df['user_message']:
       
        entry = re.split(r'([\w\W]+?):\s', message)
        
        if entry[1:]:  
            users.append(entry[1])
            cleaned_messages.append(entry[2])
        else:  
            users.append('group_notification')
            cleaned_messages.append(entry[0])
            
    
    df['user'] = users
    df['message'] = cleaned_messages
    df.drop(columns=['user_message'], inplace=True)
    
   
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['month_num']=df['date'].dt.month
    df['day_name']=df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str(0))
        elif hour == 0:
            period.append(str(24) + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    
    df['period'] = period
    return df