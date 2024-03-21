import pandas as pd
import re
def preprocess(data):
    pattern = '\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s[ap]m\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message_date data type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%y/%m/%d, %I:%M %p - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(':\s', message)
        if entry[1:]:
            users.append(entry[0])
            messages.append(entry[1])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages

    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df