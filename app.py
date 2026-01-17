from email.mime import message
import streamlit as st
import helper
import preprocessor
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

# Persist the analysis view state so the UI doesn't reset when interacting
if "show_analysis" not in st.session_state:
    st.session_state.show_analysis = False

uploaded_file = st.sidebar.file_uploader("Choose a file")


if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # Preprocess and display
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        st.session_state.show_analysis = True

    if st.session_state.show_analysis:
        # FIXED LINE: We now catch THREE variables instead of two
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        st.subheader("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Messages", num_messages)
        with col2:
            st.metric("Total Words", words)
        with col3:
            st.metric("Media Shared", num_media_messages)
        with col4:
            st.metric("Links Shared", num_links)
        st.divider()

        # monthly timeline
        st.subheader("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.divider()

        # Activity map
        st.subheader("Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Most Busy Day", helper.week_activity_map(selected_user, df).idxmax())
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.metric("Most Busy Month", helper.month_activity_map(selected_user, df).idxmax())
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        st.divider()

        if selected_user == 'Overall':
            st.subheader("Most Busy Users")
            x, new_df = helper.most_busy_users(df)
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='lightblue')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
            st.divider()

        # WordCloud
        st.subheader("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis('off')
        st.pyplot(fig)
        st.divider()

        # Most common words
        st.subheader("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df['word'], most_common_df['count'], color='lightblue')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.divider()

        # Emoji Analysis
        st.subheader("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        if not emoji_df.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df.head(20))
            with col2:
                fig, ax = plt.subplots()
                top5 = emoji_df.head(5)
                ax.pie(
                    top5['count'],
                    labels=top5['emoji'],
                    autopct="%0.2f%%",
                    startangle=90,
                    textprops={'fontsize': 16}
                )
                ax.set_title("Top 5 Emojis Used")
                st.pyplot(fig)
        else:
            st.write("No emojis found")
        st.divider()

        # Weekly Activity Heatmap
        st.subheader("Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        st.divider()

        # --- Message Sentiment Inspector (With Search Functionality) ---
        st.title("Message Sentiment ")
        # 1. Prepare the data (Filter out system messages)
        if selected_user != 'Overall':
            df_view = df[df['user'] == selected_user]
        else:
            df_view = df
        df_view = df_view[df_view['message'] != '<Media omitted>\n']
        df_view = df_view[df_view['user'] != 'group_notification']
        # 2. Add a Search Box
        search_query = st.text_input("Search for a specific message:")
        # 3. Filter the options based on the search
        all_messages = df_view['message'].unique()
        if search_query:
            # Only keep messages that contain the search text (case insensitive)
            filtered_messages = [msg for msg in all_messages if search_query.lower() in msg.lower()]
        else:
            # If search is empty, show all messages
            filtered_messages = all_messages
        # 4. Display the Dropdown
        if len(filtered_messages) > 0:
            selected_message = st.selectbox("Select a message to analyze:", filtered_messages)
            if st.button("Analyze This Message"):
                label, scores = helper.score_message(selected_message)
                st.header(f"Sentiment: {label}")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Positive", scores['pos'])
                with col2:
                    st.metric("Negative", scores['neg'])
                with col3:
                    st.metric("Neutral", scores['neu'])
                with col4:
                    st.metric("Compound", scores['compound'])
        else:
            st.info("Upload your WhatsApp chat export to see the analysis.")
        


