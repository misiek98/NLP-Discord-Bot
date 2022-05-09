CREATE SCHEMA streamer;

CREATE TABLE streamer.discord_users (
user_nickname VARCHAR,
user_id BIGINT UNIQUE PRIMARY KEY,
user_role VARCHAR,
ban_time INT);

CREATE TABLE streamer.discord_messages (
id SERIAL PRIMARY KEY,
channel_id BIGINT,
user_id BIGINT,
message_time INT,
message_content VARCHAR,
prediction REAL);

CREATE TABLE streamer.discord_channels (
channel_name VARCHAR,
channel_id BIGINT UNIQUE PRIMARY KEY,
is_evaluated BOOLEAN);