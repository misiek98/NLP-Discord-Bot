import pandas as pd

# %% read overviewed file

df_after_overview = pd.read_csv(
    ('./processed_data/non_stream_requests/'
     'non_stream_messages_after_overview.csv'),
    sep=';'
)

# %% read series names to increase number of samples
series_names = []

with open('./processed_data/other_data/series_names.txt', 'r',
          encoding='utf8') as file:
    for series in file:
        series_names.append(series.strip())

# %%

list_of_stream_messages = df_after_overview[
    df_after_overview['CATEGORY_ID'] == 0
].MESSAGE.to_list()

list_of_non_stream_messages = df_after_overview[
    df_after_overview['CATEGORY_ID'] == 1
].MESSAGE.to_list()

with open('./processed_data/stream_requests/streamRequests.txt', 'r',
          encoding='utf8') as file:
    for line in file:
        list_of_stream_messages.append(line.strip())

# %% Inscrease number of samples with new series names

expanded_list_of_stream_messages = []
expanded_list_of_non_stream_messages = []

for message in list_of_stream_messages:
    if ('f1' in message):
        for series in series_names:
            expanded_list_of_stream_messages.append(
                message.replace('f1', series)
            )
    elif ('f2' in message):
        for series in series_names:
            expanded_list_of_stream_messages.append(
                message.replace('f2', series)
            )
    else:
        expanded_list_of_stream_messages.append(message)

for message in list_of_non_stream_messages:
    if ('f1' in message):
        for series in series_names:
            expanded_list_of_non_stream_messages.append(
                message.replace('f1', series)
            )
    elif ('f2' in message):
        for series in series_names:
            expanded_list_of_non_stream_messages.append(
                message.replace('f2', series)
            )
    else:
        expanded_list_of_non_stream_messages.append(message)

# %%

df_stream = pd.DataFrame(
    data=expanded_list_of_stream_messages,
    columns=['MESSAGE']
)
df_nonstream = pd.DataFrame(
    data=expanded_list_of_non_stream_messages,
    columns=['MESSAGE']
)

df_stream['CATEGORY_ID'] = 0
df_nonstream['CATEGORY_ID'] = 1

extended_messages = pd.concat(
    [df_stream, df_nonstream],
    ignore_index=True
)

extended_messages.to_csv(
    'C:/Users/Misiek/Desktop/Python/new_bot/data/extendedMessages.csv',
    sep=';', encoding='utf8'
)
