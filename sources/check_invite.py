from telethon.sync import TelegramClient
from telethon import functions, types
import sys
try:
	from secrets import SECRETS
except Exception as e:
	print("secrets")
	exit(1)
if len(sys.argv) > 1:
	try:
		with TelegramClient(SECRETS["API_NAME"], SECRETS["API_ID"], SECRETS["API_HASH"]) as client:
			result = client(functions.messages.CheckChatInviteRequest(hash=sys.argv[1]))
			print("valid")
	except InviteHashExpiredError as ex:
			print("not")
			sys.exit(1)
	except Exception as e:
			print("telethon error")
			sys.exit(1)
else:
	print("please specify invite hash!")
	sys.exit(1)