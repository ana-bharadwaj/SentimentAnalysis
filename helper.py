from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


extract= URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    #Fetiching the number of messages
    num_messages = df.shape[0]

    #Fetching the number of words
    words = []

    for message in df['messages']:
        words.extend(message.split())

    #Fetching the media messages
    num_media_messages = df[df['messages'] == '<Media omitted>\n'].shape[0]

    #Fetching the links in messages
    links = []
    for message in df['messages']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def fetch_most_busy_users(df):
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts() * 100) / df.shape[0], 2).reset_index().rename(
        columns={'index': 'Name', 'user': 'Percentage'})
    return x, df

def create_wordcloud(selected_user, df):
    f = open('Hinglish.txt', 'r')
    stopwords = f.read()

    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    # Removing group notifications
    temp = df[df['users'] != 'group notifications']

    # Removing media omitted
    temp = temp[temp['messages'] != "<Media omitted>\n"]

    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stopwords:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=300, min_font_size = 10, background_color = 'white')

    temp['messages'] = temp['messages'].apply(remove_stop_words)

    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    #Importing stopwords
    f = open('Hinglish.txt', 'r')
    stopwords = f.read()

    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    #Removing group notifications
    temp = df[df['users'] != 'group notifications']

    #Removing media omitted
    temp = temp[temp['messages'] != "<Media omitted>\n"]

    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stopwords:
                words.extend(message.split())

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_counter(selected_user, df):

    if selected_user != "Overall":
        df = df[df['users'] == selected_user]


    emojis = []

    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user, df):

    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['Year', 'month_num', 'Month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):

    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('datetimeline').count()['messages'].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):

    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    week_activity = df['day_name'].value_counts()

    return week_activity

def month_activity_map(selected_user, df):

    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    month_activity = df['Month'].value_counts()

    return month_activity

def activity_heatmap(selected_user, df):

    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period',values='messages', aggfunc='count').fillna(0)

    return user_heatmap