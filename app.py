import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import numpy as np
from collections import Counter
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a File")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)


    #Fetching unique users
    user_list = df['users'].unique().tolist()

    user_list.remove('group notifications')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analaysis For", user_list)

    if st.sidebar.button("Show Analysis"):
        #Numerical Shows
        num_messages, words, num_media_messages, num_links =  helper.fetch_stats(selected_user, df)
        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media")
            st.title(num_media_messages)

        with col4:
            st.header("Total Link Shared")
            st.title(num_links)

        #Timeline
        st.title("Timeline")
        col1, col2 = st.columns(2)

        with col1:
            st.title("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['messages'], color='red')
            fig.patch.set_facecolor('xkcd:mint green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.title("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['datetimeline'], daily_timeline['messages'], color='red')
            fig.patch.set_facecolor('xkcd:mint green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #Activity Map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.title("Weekly Map")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            fig.patch.set_facecolor('xkcd:mint green')
            ax.bar(busy_day.index, busy_day.values, color='orange')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with col2:
            st.title("Monthly Map")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            fig.patch.set_facecolor('xkcd:mint green')
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation=45)
            st.pyplot(fig)



        #Finding the Engaging Performance.
        if selected_user == "Overall":
            st.title('Most Engaging User')
            x, new_df = helper.fetch_most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='blue')
                fig.patch.set_facecolor('xkcd:mint green')
                plt.xticks(rotation=45)
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        #WordCloud Appearance
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('xkcd:mint green')
        ax.imshow(df_wc)
        st.pyplot(fig)

        #Most Common Words
        st.title('Most Common words')
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('xkcd:mint green')
        ax.barh(most_common_df[0], most_common_df[1], color='red')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        #Emoji Analysis
        st.title('Emoji Analysis')
        emoji_df = helper.emoji_counter(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            fig.patch.set_facecolor('xkcd:mint green')
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)

        # Activity Heatmap
        st.title('Activity Heatmap')
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('xkcd:mint green')
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

