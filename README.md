![logobackground](https://user-images.githubusercontent.com/76869717/167440861-87d785fb-f400-407d-9b1e-2d7f6597e14a.png)

## About RaceDay.watch
[RaceDay.watch](https://raceday.watch/#sessions) is a site that provides many motorsport events around the world, including start times and official sources for live streaming and TV broadcasts. The site also has its own Discord -> [join now](https://discord.gg/WAh6AD4)!

We are receiving a lot of questions on Discord text channels about where to watch a particular race. In order to automate and quickly respond, I created a bot that would classify messages. If a message is classified as a stream request, the bot will send a reply to that message with a redirect to the **streaming** channel and to [RaceDay.watch](https://raceday.watch/#sessions). If the user asks another such question in a short period of time (30 minutes by default), an identical respond will be sent as a private message.
Originally, the bot was based on an *if statement* - if a message contained such words: *stream* or a *link* and a *question mark*, the message was considered to be a stream request. It was generating a lot of problems, for example when someone asked if there were any problems with the quality of transmission or high delay. Therefore, I decided to use an intelligent bot based on Recurrent Neural Networks.

## Workflow

The work began by manually collecting streaming request messages (about 120 samples). Then, about 400 samples of different messages were collected during the weekend (when traffic is higher than usual). A test model was prepared from all the data, which then classified the subsequent messages.
After collecting more data (more than 8000 samples), the data was standardized, repetitions were discarded, and sent for manual review to verify that the classification was correct and as much noise as possible was removed. After verification, the data were prepared for the model and the model itself.

Noted that there was a large spread of data with about 150 stream requests and over 7500 different messages. Also noted that the majority of the stream requests was related to F1 or F2. RaceDay.watch contains over 1000 different racing series, so as part of the data augmentation, all occurring F1 and F2 words were replaced with the names of unique series. As a result, the set containing over 250,000 samples was created from a relatively small dataset, 60,000 of them were streaming requests.

The data was processed with the pandas library and several models were created using the TensorFlow library. The best one was selected.

## Accuracy

The model achieves about 96% success rate, and when tested on real data (during busy weekends) it performed decently and classified messages correctly.

![msg](https://user-images.githubusercontent.com/76869717/167444441-8cdff46a-bcae-45aa-b00a-2636375dcab2.png)

## Future work

Also noted that new words that the model has never seen appear very quickly. Therefore, it may be necessary to prepare a new model every now and then.\
The next stage of the project will be dockerizing and putting it on an external server.

## Installation

- Create an instance of PostreSQL database (/Schema/db_schema.sql).
- Enter the token for your bot and other data (/Source/config.json)
- Run the bot (/Source/run_bot.py).
