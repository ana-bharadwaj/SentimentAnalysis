import re
import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)\s'

    pattern2 = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)\s-\s'

    pattern3 = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    if re.match(pattern2, data):
        messages = re.split(pattern2, data)[1:]
        dates = re.findall(pattern2, data)
    else:
        messages = re.split(pattern3, data)[1:]
        dates = re.findall(pattern3, data)


    df = pd.DataFrame({'username': messages, 'date': dates})

    df['date'] = df['date'].map(lambda x: x.rstrip(' - '))

    df['date'] = pd.to_datetime(df['date'], dayfirst = True,errors='coerce')


    users = []
    messages = []

    for message in df['username']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group notifications')
            messages.append(entry[0])

    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['username'], inplace=True)

    df['Year'] = df['date'].dt.year
    df['Month'] = df['date'].dt.month_name()
    df['Day'] = df['date'].dt.day
    df['Hour'] = df['date'].dt.hour
    df['Minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['datetimeline'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()

    period = []
    for hour in df[['day_name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period

    return df