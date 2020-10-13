import asyncio
import threading
import time
import schedule
from commands import _birthdayMessage

GUILD_ID = 760615522130984980
CHANNEL_ID = 760615523145875494

schedule_stop = threading.Event()


def timer():
	while not schedule_stop.is_set():
		schedule.run_pending()
		time.sleep(1)


schedule_thread = threading.Thread(target = timer)
schedule_thread.start()


async def send_morning_announcement(client):
	# TODO: Access guild ids and channel ids from database and loop through, running sendbirthdaymessage for each one
	# TODO: delete all messages in channel before sending new morning announcement
	await _birthdayMessage.send_birthday_message(client, GUILD_ID, CHANNEL_ID)


async def schedule_announcement(client):
	schedule.every().day.at("08:00").do(
		asyncio.run_coroutine_threadsafe, send_morning_announcement(client), client.loop)
