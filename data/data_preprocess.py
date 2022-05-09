import pandas as pd

# %% process series names

list_of_series_names = []

with open('./data/raw_data/other_data/series_names.txt',
          'r', encoding='utf8') as file:
    for line in file:
        list_of_series_names.append(line.strip())

# drop non-series elements
list_of_series_names = list_of_series_names[2:-2]
list_of_series_names = [series.lower() for series in list_of_series_names]

# save processed series names to file:
with open('./data/processed_data/other_data/series_names.txt',
          'a', encoding='utf8') as file:
    for series in list_of_series_names:
        file.write(series + '\n')

# %% Stream requests

list_of_stream_messages = []

with open('./data/raw_data/stream_requests/streamRequests.txt',
          'r', encoding='utf8') as file:
    for line in file:
        list_of_stream_messages.append(line.strip())

list_of_stream_messages = set(list_of_stream_messages)

for stream_message in list_of_stream_messages:
    with open('./data/processed_data/stream_requests/streamRequests.txt',
              'a', encoding='utf8') as file:
        file.write(stream_message + '\n')


# %% non-stream messages

list_of_files = ['./data/raw_data/non_stream_requests/textMessages_sample_1.txt',
                 './data/raw_data/non_stream_requests/textMessages_sample_2.txt',
                 './data/raw_data/non_stream_requests/textMessages_sample_3.txt']

list_of_messages = []

for filename in list_of_files:
    with open(filename, 'r', encoding='utf8') as file:
        for line in file:
            if (line.startswith('0')):
                list_of_messages.append(line.strip())

# replace ',' with ';' between prediction and message if necessary
for idx, message in enumerate(list_of_messages):
    if (',' in message[:13]):
        msg = list(message)
        msg[msg[:13].index(',')] = ';'
        list_of_messages[idx] = ''.join(msg)

list_of_messages = [data.split(';') for data in list_of_messages]
df_non_stream_messages = pd.DataFrame(list_of_messages)

# drop every columns except first and second if exist
df_non_stream_messages = df_non_stream_messages.drop(
    labels=[number for number in range(2, df_non_stream_messages.shape[1])],
    axis=1,
    errors='ignore'
)

df_non_stream_messages.columns = ['pred', 'MESSAGE']

# drop missing elements from 'MESSAGE' column
df_non_stream_messages = df_non_stream_messages[
    df_non_stream_messages['MESSAGE'].str.len() > 0
]

# Change the variable type from str to float and round to
# 3 decimal places
df_non_stream_messages['pred'] = df_non_stream_messages['pred'].apply(
    lambda x: float(x)
)
df_non_stream_messages['PREDICTION'] = df_non_stream_messages['pred'].apply(
    lambda x: round(x, 3)
)

# Split the messages into categories
df_non_stream_messages['CATEGORY'] = pd.cut(
    df_non_stream_messages['PREDICTION'], [0, 0.2, 1]
)
df_non_stream_messages['CATEGORY_ID'] = pd.factorize(
    values=df_non_stream_messages['CATEGORY'], sort=True
)[0]

df_non_stream_messages['MESSAGE'] = df_non_stream_messages['MESSAGE'].apply(
    lambda x: x.lower()
)

# drop unused columns
df_non_stream_messages = df_non_stream_messages.drop(
    labels=['pred', 'CATEGORY'],
    axis=1
)

# detect duplicates rows for the MESSAGE column
duplicateDFRow = df_non_stream_messages[
    df_non_stream_messages.duplicated(['MESSAGE'])]

# remove duplicates rows for the MESSAGE column
df = df_non_stream_messages.drop_duplicates(subset=['MESSAGE'])

# save .csv file to overview
df.to_csv(path_or_buf=('./data/raw_data/non_stream_requests/'
          'negTextMessages_to_overview.csv'), sep=';')
