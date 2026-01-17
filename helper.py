from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import nltk

# Download vader if not present
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer

extractor = URLExtract()

# ---------------- STATS ----------------
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

# ---------------- BUSY USERS ----------------
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2)\
            .reset_index()\
            .rename(columns={'index':'name','user':'percent'})
    return x, df

# ---------------- WORD CLOUD ----------------
def create_wordcloud(selected_user, df):
    with open('stop_hinglish.txt','r') as f:
        stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[(df['user'] != 'group_notification') & 
              (df['message'] != '<Media omitted>\n')]

    def remove_stop_words(message):
        return " ".join([w for w in message.lower().split() if w not in stop_words])

    text = temp['message'].apply(remove_stop_words).str.cat(sep=" ")

    if text.strip() == "":
        text = "No Data"

    wc = WordCloud(width=500,height=500,background_color='white')
    return wc.generate(text)

# ---------------- MOST COMMON WORDS ----------------
def most_common_words(selected_user, df):
    with open('stop_hinglish.txt','r') as f:
        stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[(df['user'] != 'group_notification') & 
              (df['message'] != '<Media omitted>\n')]

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    counter = Counter(words).most_common(20)

    return pd.DataFrame(counter, columns=['word','count'])

#emoji
def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    return pd.DataFrame(Counter(emojis).most_common(), columns=['emoji','count'])


#timeline
def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df.groupby('only_date').count()['message'].reset_index()
#activity map
def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df.pivot_table(index='day_name', columns='period',
                          values='message', aggfunc='count').fillna(0)

#message sentiment analysis
analyzer = SentimentIntensityAnalyzer()  # Create once and reuse

def score_message(message):
    # Use the global analyzer
    score = analyzer.polarity_scores(message)
    compound = score['compound']

    important_words = ['urgent','important','call me','deadline','meeting','pay','asap','alert']

    if any(w in message.lower() for w in important_words):
        return "Important", score
    elif compound >= 0.5:
        return "Happy", score
    elif compound <= -0.5:
        return "Sad", score
    elif -0.1 < compound < 0.1:
        return "Normal", score
    else:
        return "Statement", score
