import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message':messages, 'message_date': dates})
    df[['Date1', 'Time1']] = df.message_date.str.split(pat='-',expand=True)
    df.drop('Time1', inplace=True, axis=1)
    df[['Date', 'Time']] = df.Date1.str.split(pat=',',expand=True)
    df.drop('Date1', inplace=True, axis=1)
    df.drop('message_date', inplace=True, axis=1)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['Author'] = users
    df['Message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    
    df['Date_Time'] = df['Date'] + " " + df['Time']
    df['Date_Time'] = pd.to_datetime(df['Date_Time'])
    
    df['Only_Date'] = df['Date_Time'].dt.date
    df['Year'] = df['Date_Time'].dt.year
    df['Month_Num'] = df['Date_Time'].dt.month
    df['Month'] = df['Date_Time'].dt.month_name()
    df['Day'] = df['Date_Time'].dt.day
    df['Day_Name'] = df['Date_Time'].dt.day_name()
    df['Hour'] = df['Date_Time'].dt.hour
    df['Minute'] = df['Date_Time'].dt.minute


    period = []
    for hour in df[['Day_Name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['Period'] = period

    return df