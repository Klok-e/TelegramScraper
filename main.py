from telethon import TelegramClient, sync
import json
import datetime
import asyncio


def create_client():
    api_id = 000000 # your api_id
    api_hash = 'your_hash'
    return TelegramClient('scrape', api_id, api_hash).start()


async def get_messages(client, *args, **kwargs):
    messages = []
    async for x in client.iter_messages(*args, **kwargs):
        messages.append(x)
    return messages


def main():
    loop = asyncio.get_event_loop()

    my_group_name = "Итши -18-1"

    messages = []
    with create_client() as client:
        dialogs = client.get_dialogs()

        groups = []
        for dialog in dialogs:
            if my_group_name == dialog.name:
                groups.append(dialog)
        del dialogs

        for group in groups:
            messages.extend(loop.run_until_complete(get_messages(client, group.entity)))

            """
            for msg in msgs:
                # help(msg)
                ent = client.get_entity(msg.sender)
                # help(ent)
                messages.append(((msg.date.second, msg.date.minute, msg.date.hour, msg.date.day, msg.date.month,
                                  msg.date.year), msg.raw_text, ent.username, ent.id, ent.first_name, ent.last_name))
                print(messages[len(messages) - 1])
            """

        data = []
        for msg in messages:
            ent = client.get_entity(msg.sender)
            data.append(((msg.date.second, msg.date.minute, msg.date.hour, msg.date.day, msg.date.month,
                          msg.date.year), msg.raw_text, ent.username, ent.id, ent.first_name, ent.last_name))
            #print(data[len(data) - 1])

        data.sort(key=lambda x: datetime.datetime(second=x[0][0], minute=x[0][1], hour=x[0][2],
                                                  day=x[0][3], month=x[0][4], year=x[0][5]), reverse=True)

    file = open("scraped_information.json", "w")
    json.dump(data, file)
    file.close()


if __name__ == "__main__":
    main()
