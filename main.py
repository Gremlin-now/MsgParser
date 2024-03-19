from pyrogram import Client, filters
import string


parser = Client(name="UsParser")

bot_api_id = 28521388
bot_api_hash = "2584676d9fd234256457b0f82854484f"
app = Client(name="MsgHandler",
             bot_token="1219428556:AAEKo1FxUBZD75RfJHEoGFeD6v1TNV2qmag",
             api_id=bot_api_id, api_hash=bot_api_hash)

targets = ["peepoSwamp"]
archive_msgs = []


async def searcher(user_msg):
    array_of_pairs = []
    table = str.maketrans("", "", string.punctuation)
    key_word = user_msg.text.lower().translate(table).split()
    for msg_from_history in archive_msgs:
        if msg_from_history.text is not None:
            words_array_msg_from_archive_msgs = (msg_from_history
                                            .text
                                            .lower()
                                            .translate(table)
                                            .split())
        else:
            if msg_from_history.caption is not None:
                words_array_msg_from_archive_msgs = (msg_from_history
                                                     .caption
                                                     .lower()
                                                     .translate(table)
                                                     .split())
            else:
                continue
        tmp = list(set(words_array_msg_from_archive_msgs) & set(key_word))
        if len(tmp) > 0:
            array_of_pairs.append([len(tmp), msg_from_history])
    return sorted(array_of_pairs, key=lambda x: x[0], reverse=True)

async def main():
    async with parser:
        for target in targets:
            async for msg in parser.get_chat_history(chat_id=target):
                archive_msgs.append(msg)
    print(len(archive_msgs))

@app.on_message(filters.text)
async def display_suitable_msgs(client, msg):
    print(msg.chat.id, " : ", msg.text)
    for i in await searcher(msg):
        try:
            await client.forward_messages(from_chat_id=i[1].chat.username, chat_id=msg.chat.id, message_ids=i[1].id)
        except:
            print(i[1])

@parser.on_message(filters.chat(targets))
async def add_in_archive_new_msgs(client, msg):
    archive_msgs.append(msg)
    print(len(archive_msgs))

parser.run(main())
parser.run()
app.run()