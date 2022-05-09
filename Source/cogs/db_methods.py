from datetime import datetime

import psycopg2
import psycopg2.extras

from .other_methods import load_config

config = load_config(
    r'C:\Users\Misiek\Desktop\Python\raceday\Source\config.json')


class DBMethods():
    """
    A bunch of functions that allow you to connect to a database and 
    make some operations (e.g. add a new users or messages, get an
    information about user's ban time).

    Available methods:
    get_data,
    add_user,
    get_user_ban_time,
    update_ban_time,
    add_message.
    """

    __db = psycopg2.connect(
        dbname=config['dbname'],
        user=config['user'],
        password=config['password'],
        host=config['host'],
        cursor_factory=psycopg2.extras.NamedTupleCursor
    )

    __db.autocommit = True
    schema_name = config['schema']

    @classmethod
    def get_data(cls, column_name: str, table_name: str) -> list:
        """
        Function get_data allows to download any column(s) from 
        database.

        Parameters
        ----------
        column_name: str
            A name of the database column(s) from which you want to 
            download data. For more than one column, use comma as 
            separator (just like in SQL syntax).
        table_name: str
            A name of a table from where you want to get data.

        Returns
        -------
        list
        """
        with cls.__db.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT {column_name}
                FROM {cls.schema_name}.{table_name}
                """
            )
            return cursor.fetchall()

    @classmethod
    def add_user(cls, nickname: str, user_id: int,
                 ban_time: int, user_rank='Member') -> None:
        """
        Function add_user adds a new user to our database.

        Parameters
        ----------
        nickname : str
            User's Discord nickname.
        user_id : int
            User's Discord id.
        ban_time : int
            0 by default. If user's message is classified as stream
            request, then the ban_time value is updated to current 
            timestamp.
        user_rank : str
            Discord's role (set by Admins). Default's role is Member.
        """
        with cls.__db.cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO {cls.schema_name}.discord_users
                (user_nickname, user_id, user_role, ban_time)
                VALUES (%s, %s, %s, %s)
                """, (nickname, user_id, user_rank, ban_time)
            )

    @classmethod
    def get_user_ban_time(cls, user_id: int) -> int:
        """
        Function get_user_ban_time returns the value of user's ban_time. 

        Parameters
        ----------
        user_id : int
            User's Discord id.

        Returns
        -------
        int
        """
        with cls.__db.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT ban_time
                FROM {cls.schema_name}.discord_users
                WHERE user_id = {user_id}
                """
            )
            return cursor.fetchall()[0][0]

    @classmethod
    def update_ban_time(cls, user_id: int) -> None:
        """
        Function update_ban_time allows to update user's ban_time.

        Parameters
        ----------
        user_id : int
            User's Discord id.
        """
        ban = int(datetime.timestamp(datetime.now()) + config['banTime'])
        with cls.__db.cursor() as cursor:
            cursor.execute(
                f"""
                UPDATE {cls.schema_name}.discord_users
                SET ban_time = {ban}
                WHERE user_id = {user_id};
                """
            )

    @classmethod
    def add_message(cls, channel_id: int, user_id: int, message_time: int,
                    message_content: str, prediction: float) -> None:
        """
        Function add_message adds a new message to our database.

        Parameters
        ----------
        channel_id : int
            Channel's Discord id where message has been sent.
        user_id : int
            User's Discord id.
        message_time : int
            The time when message was sent. Stored as timestamp.
        message_content : str
            Content of the message.
        prediction : float
            Prediction contains an information about message class. It's
            an information for our DL model.
        """
        with cls.__db.cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO {cls.schema_name}.discord_messages 
                (channel_id, user_id, message_time, 
                 message_content, prediction)
                VALUES (%s, %s, %s, %s, %s)
                """, (channel_id, user_id, message_time,
                      message_content, prediction)
            )
