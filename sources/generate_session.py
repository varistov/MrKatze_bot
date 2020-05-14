from telethon.sync import TelegramClient
from telethon import functions, types
try:
	from secrets import SECRETS
except Exception as e:
	print("not")
	exit(1)
with TelegramClient(SECRETS["API_NAME"], SECRETS["API_ID"], SECRETS["API_HASH"]) as client:
    print("success")