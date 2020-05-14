from telethon.sync import TelegramClient
from telethon import functions, types
import sys
try:
	from secrets import SECRETS
except Exception as e:
	print("not")
	exit(1)
if len(sys.argv) > 1:
	with TelegramClient(SECRETS["API_NAME"], SECRETS["API_ID"], SECRETS["API_HASH"]) as client:
	    try:
	    	result = client(functions.messages.CheckChatInviteRequest(hash=sys.argv[1]))
	    	if not result.chat.deactivated:
	    		print("valid")
	    		sys.exit(0)
	    	else:
	    		print("not")
	    except Exception as e:
	    	print("not")
	    	sys.exit(1)
else:
	print("please specify invite hash!")
	sys.exit(1)