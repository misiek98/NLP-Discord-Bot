import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    'postgresql://postgres:password@localhost:5432/test_raceday')

# Channels
df = pd.read_csv(
    (r"C:\Users\Misiek\Desktop\Python\raceday\data\processed_data"
     "\other_data\server_channels.csv"),
    sep=';'
)
df = df.drop('Unnamed: 0', axis=1)
df.columns = ['channel_name', 'channel_id', 'is_evaluated']

df.to_sql(
    name='discord_channels',
    con=engine,
    schema='streamer',
    index=False,
    if_exists='append'
)

# Messages
df_mess = pd.read_csv(
    r'C:\Users\Misiek\Desktop\Python\raceday\data\processed_data\messages.csv',
    sep=';'
)

df_mess = df_mess.drop(
    labels='Unnamed: 0',
    axis=1
)
df_mess['CATEGORY_ID'] = df_mess['CATEGORY_ID'].apply(
    lambda cat_id: float(cat_id)
)
df_mess.insert(
    loc=0,
    column='channel_id',
    value=0
)
df_mess.insert(
    loc=1,
    column='user_id',
    value=0
)
df_mess.insert(
    loc=2,
    column='message_time',
    value=0
)
df_mess.columns = ['channel_id', 'user_id',
                   'message_time', 'message_content', 'prediction']

df_mess.to_sql(
    name='discord_messages',
    con=engine,
    schema='streamer',
    index=False,
    if_exists='append'
)

# Users
df_users = pd.read_csv(
    (r"C:\Users\Misiek\Desktop\Python\raceday\data\processed_data\other_data"
     r"\team_members.csv"),
    sep=';'
)

df_users = df_users.drop(
    labels='Unnamed: 0',
    axis=1
)
df_users['ban_time'] = 0
df_users.columns = ['user_nickname', 'user_id', 'user_role', 'ban_time']

df_users.to_sql(
    name='discord_users',
    con=engine,
    schema='streamer',
    index=False,
    if_exists='append'
)
