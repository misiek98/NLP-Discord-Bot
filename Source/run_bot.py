from discord.ext import commands
import tensorflow

from cogs.db_methods import DBMethods
from cogs.msg_processing import MessagePreparator
from cogs.other_methods import current_time, load_config

config = load_config(
    r'C:\Users\Misiek\Desktop\Python\raceday\Source\config.json')

model = tensorflow.keras.models.load_model(config['pathToModel'])

db_conn = DBMethods()
msg_manager = MessagePreparator()

users = db_conn.get_data(
    column_name='user_id, user_role',
    table_name='discord_users'
)
team_members = [
    user.user_id
    for user in users
    if user.user_role != 'Member'
    if user.user_role != 'BOT'
]
bots = [
    user.user_id
    for user in users
    if user.user_role == 'BOT'
]
users = [
    user.user_id
    for user in users
    if user.user_role == 'Member'
]

channels = db_conn.get_data(
    column_name='channel_id, is_evaluated',
    table_name='discord_channels'
)
channels = [
    channel.channel_id
    for channel in channels
    if channel.is_evaluated
]

client = commands.Bot(command_prefix='.')


@ client.event
async def on_message(message):
    channel_id = message.channel.id
    user_id = message.author.id
    msg = message.content

    msg_lower_letters = msg_manager.lower_letters(
        msg=msg
    )
    msg_without_special_characters = msg_manager.drop_special_characters(
        msg=msg_lower_letters
    )
    seq = msg_manager.prepare_sequence(
        msg=msg_without_special_characters
    )

    X = tensorflow.keras.preprocessing.sequence.pad_sequences(
        sequences=[seq],
        maxlen=15,
        padding='post'
    )

    prediction = round(float(model.predict(X)[0][0]), 4)

    if (user_id not in bots):
        db_conn.add_message(
            channel_id=channel_id,
            user_id=user_id,
            message_time=current_time(),
            message_content=message.content,
            prediction=prediction
        )

    if (user_id not in users and
            user_id not in team_members and
            user_id not in bots):
        users.append(user_id)
        db_conn.add_user(
            nickname=message.author.name,
            user_id=user_id,
            ban_time=0.
        )

    if (user_id in users and
            channel_id in channels and
            prediction <= config['predTolerance']):

        if (db_conn.get_user_ban_time(user_id) < current_time()):
            db_conn.update_ban_time(user_id=user_id)
            await message.reply(config['message'])
        else:
            await message.author.send(config['message'])

client.run(config['token'])
