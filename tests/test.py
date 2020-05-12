#base on work by Bibo-Joshi: https://gist.github.com/Bibo-Joshi/75f135edf1ca3530decf4c2ae06bd699

import asyncio
import itertools
import json
import os
import re
import urllib.parse
import itertools
import random
import string
import json
import sys
import time
from telethon import TelegramClient
from telethon.utils import get_input_peer
from telethon.tl.functions.messages import (AddChatUserRequest, CreateChatRequest,
											MigrateChatRequest)
from telethon.tl.functions.channels import InviteToChannelRequest
sys.path.append('../sources/')
from tsjson import TSjson
from telegram import Bot

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
session_file = os.path.basename(__file__) + '.session'

BOT_FATHER = '@BotFather'

loop = asyncio.get_event_loop()


async def send_message_check_reply(conv, text, reply):
	await conv.send_message(text)
	msg = await conv.get_response()
	if not reply in msg.text:
		#print('Partial Error: "{}" not found in "{}"'.format(reply, msg.text))
		raise AssertionError
	await asyncio.sleep(1)
	return msg


async def send_file_check_reply(conv, file, reply):
	await conv.send_file(file)
	msg = await conv.get_response()
	if not reply in msg.text:
		print('Error: "{}" not found in "{}"'.format(reply, msg.text))
		raise AssertionError
	await asyncio.sleep(1)
	return msg


async def click_check_edit(conv, msg, text_filter, edit):
	for button in itertools.chain.from_iterable(msg.buttons):
		if text_filter in button.text:
			await button.click()
			edited_msg = await conv.get_edit()
			if not edit in edited_msg.text:
				print('Error: "{}" not found in "{}"'.format(edit, edited_msg.text))
				raise AssertionError
			await asyncio.sleep(1)
			return edited_msg
	else:
		return await click_check_edit(conv, msg, '»', edit)


async def create_bot(client, name, username):
	print('Creating bot')
	async with client.conversation(BOT_FATHER) as conv:
		await send_message_check_reply(conv, '/newbot', 'Please choose a name for your bot.')
		await send_message_check_reply(conv, name, 'Now let\'s choose a username for your bot.')
		msg = await send_message_check_reply(conv, username,
											 'Done! Congratulations on your new bot.')

		token_search = re.search(r'`(.+)`', msg.text)
		assert token_search
		token = token_search.group(1)
		assert token

		return token


async def set_description(client, username, description):
	print('Setting description')
	async with client.conversation(BOT_FATHER) as conv:
		await send_message_check_reply(conv, '/setdescription', 'Choose a bot')
		await send_message_check_reply(conv, username, 'Send me the new description for the bot.')
		await send_message_check_reply(conv, description, 'Success!')


async def set_about_text(client, username, about_text):
	print('Setting about_text')
	async with client.conversation(BOT_FATHER) as conv:
		await send_message_check_reply(conv, '/setabouttext', 'Choose a bot')
		await send_message_check_reply(conv, username, 'Send me the new \'About\' text.')
		await send_message_check_reply(conv, about_text, 'Success!')


async def set_join_groups(client, username, join_groups):
	print('Setting join groups')
	async with client.conversation(BOT_FATHER) as conv:
		await send_message_check_reply(conv, '/setjoingroups', 'Choose a bot')
		await send_message_check_reply(conv, username, 'Current status is')
		await send_message_check_reply(conv, join_groups, 'Success!')


async def create_super_group(client, username, group_title):
	print('Creating new super group.')
	r = CreateChatRequest(users=[username], title=group_title)
	result = await client(r)
	await asyncio.sleep(1)
	group_id = result.updates[-1].peer.chat_id
	r = MigrateChatRequest(group_id)
	result = await client(r)
	await asyncio.sleep(1)
	return result.updates[0].channel_id


async def add_to_group(client, group, username):
	print('Adding to group')
	r = InviteToChannelRequest(group, [username])
	await client(r)
	await asyncio.sleep(1)


async def make_group_admin(client, group, username):
	print('Making group admin')
	await client.edit_admin(group, username, add_admins=True, is_admin=True)
	await asyncio.sleep(1)


async def new_bot(client,
				  name,
				  username,
				  description=None,
				  about_text=None,
				  group_id=None,
				  group_name=None,
				  group_admin=None,
				  channel_id=None,
				  inline_placeholder=None,
				  game_title=None,
				  game_description=None,
				  game_photo=None,
				  game_animation=None,
				  game_short_name=None,
				  sticker_set_name=None,
				  animated_sticker_set_name=None,
				  sticker_set_title=None,
				  animated_sticker_set_title=None,
				  sticker=None,
				  animated_sticker=None,
				  sticker_emoji=None,
				  token=None,
				  payment_provider_token=None):
	print('Creating bot')

	# Create the bot
	if token is None:
		token = await create_bot(client, name, username)

	# Allow the bot to talk to us
	await client.send_message(username, '/start')

	username = '@' + username

	# Set texts in case a user stumbles upon the bot
	if description:
		await set_description(client, username, description)
	if about_text:
		await set_about_text(client, username, about_text)

	# Make sure the new bot can join groups
	if group_id or channel_id:
		await set_join_groups(client, username, 'Enable')

	# Add it to the developer group
	if group_id:
		await add_to_group(client, group_id, username)

	if group_name:
		new_group_id = await create_super_group(client, username, group_name)
	else:
		new_group_id = group_id

	# Make it admin in the group
	if group_admin:
		if group_id:
			await make_group_admin(client, group_id, username)
		if new_group_id:
			await make_group_admin(client, new_group_id, username)

	return token, payment_provider_token, new_group_id


def print_bot(name, username, token, payment_provider_token, super_group_id):
	print()
	print('-' * 80)
	print('Name:', name)
	print('Username: @{}'.format(username))
	print('Link: https://t.me/{}'.format(username))

	data = {
		'token': token,
		'payment_provider_token': payment_provider_token,
		'name': name,
		'username': username,
		'super_group_id': super_group_id,
	}

	print(json.dumps(data, indent=4))

def randomString(stringLength):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(stringLength))


async def setup_bot(client):
	tag = randomString(5)
	name = 'ButterBot Testing Bot [{}]'.format(tag)
	username = 'bbt_{}_bot'.format(tag)
	description = ('This bot is only for running tests for butter_bot'
				   ' and has no actual functionality.')

	token, payment_provider_token, super_group_id = await new_bot(
		client,
		name=name,
		username=username,
		description=description,
		about_text=description,
		# Pass a group id, if there is a group set up for the bot
		# group_id=-1001493296829,
		# Pass a group name to create a new super group
		group_name='>>> telegram.Bot(test) @{}'.format(username),
		group_admin=True,
		channel_id=1062610360,
		inline_placeholder='This bot is only for running tests.',
		game_title='Python-telegram-bot test game',
		game_description='A no-op test game, for python-telegram-bot bot framework testing.',
		game_photo='tests/data/game.png',
		game_animation='tests/data/game.gif',
		game_short_name='test_game',
		sticker_set_name='test_by_{}'.format(username),
		animated_sticker_set_name='animated_test_by_{}'.format(username),
		sticker_set_title='Test',
		animated_sticker_set_title='Animated Test',
		sticker='tests/data/telegram_sticker.png',
		animated_sticker='tests/data/telegram_animated_sticker.tgs',
		sticker_emoji='😄'
	)
	print_bot(name, username, token, payment_provider_token, super_group_id)
	return {"name": name, "username": username, "token": token, "ppt": payment_provider_token, "super_group_id": super_group_id}



###real time tests start here####
async def run_tests(client, super_group_id):
	#read en language file
	json_lang_file = TSjson("../sources/language/en.json")
	json_lang_texts = json_lang_file.read()
	TEXT = {}
	TEXT["en"] = json_lang_texts

	#test command outputs(only some logic!)
	await test_start(client,super_group_id,TEXT)
	await test_set_welcome_msg(client,super_group_id,TEXT)
	await test_protection(client,super_group_id,TEXT)
	await test_notes(client,super_group_id,TEXT)
	await test_questions(client,super_group_id,TEXT)
	await test_enable_toggle(client, super_group_id,TEXT)
	await test_trigger_delete_welcome(client, super_group_id, TEXT)
	await test_trigger_delete_notes(client, super_group_id, TEXT)

async def test_start(client,sgi,TEXT):
	async with client.conversation(sgi) as conv:
		await send_message_check_reply(conv, '/start', TEXT["en"]["START"])

async def test_set_welcome_msg(client,sgi,TEXT):
	async with client.conversation(sgi) as conv:
		random_message = randomString(20)
		await send_message_check_reply(conv, '/set_welcome_msg {}'.format(random_message), random_message)
		await send_message_check_reply(conv, '/welcome_msg', random_message)

async def test_protection(client,sgi,TEXT):
	async with client.conversation(sgi) as conv:
		try:
			await send_message_check_reply(conv, '/protection', TEXT["en"]["CHANNEL_PROTECTION_ON"])
		except Exception as e:
			await send_message_check_reply(conv, '/protection', TEXT["en"]["CHANNEL_PROTECTION_ON"])

async def test_notes(client,sgi,TEXT):
	async with client.conversation(sgi) as conv:
		random_note = randomString(20)
		random_message = randomString(20)
		await send_message_check_reply(conv, '/add_note {} {}'.format(random_note, random_message), TEXT["en"]["TRIGGER_ADD"])
		await send_message_check_reply(conv, '/notes', random_note)
		await send_message_check_reply(conv, '#{}'.format(random_note), random_message)
		await send_message_check_reply(conv, '/delete_note {}'.format(random_note), TEXT["en"]["TRIGGER_DELETE"])
		try:
			await send_message_check_reply(conv, '/notes', random_note)
			raise NoteNotDeletedError

		except AssertionError as e:
			pass

async def test_questions(client,sgi,TEXT):
	async with client.conversation(sgi) as conv:
		random_note = randomString(20)
		await send_message_check_reply(conv, '/add_question {0}|{0}|{0}|{0}|{0}'.format(random_note), TEXT["en"]["QUESTION_ADD"])
		await send_message_check_reply(conv, '/questions', random_note)
		await send_message_check_reply(conv, '/delete_question {}'.format(random_note), TEXT["en"]["QUESTION_DELETE"])
		try:
			await send_message_check_reply(conv, '/questions', random_note)
			raise QuestionNotDeletedError

		except AssertionError as e:
			pass

async def test_enable_toggle(client,sgi,TEXT):
	async with client.conversation(sgi) as conv:
		try:
			await send_message_check_reply(conv, '/enable', TEXT["en"]["ENABLE"])
		except AssertionError as e:
			await send_message_check_reply(conv, '/enable', TEXT["en"]["ALREADY_ENABLE"])
			await send_message_check_reply(conv, '/disable', TEXT["en"]["DISABLE"])
			await send_message_check_reply(conv, '/enable', TEXT["en"]["ENABLE"])
		await send_message_check_reply(conv, '/enable', TEXT["en"]["ALREADY_ENABLE"])
		await send_message_check_reply(conv, '/disable', TEXT["en"]["DISABLE"])
		await send_message_check_reply(conv, '/disable', TEXT["en"]["ALREADY_DISABLE"])

async def test_trigger_delete_welcome(client,sgi,TEXT):
	async with client.conversation(sgi) as conv:
		try:
			await send_message_check_reply(conv, '/trigger_delete_welcome', TEXT["en"]["DELETE_WELCOME_ON"])
			await send_message_check_reply(conv, '/trigger_delete_welcome' , TEXT["en"]["DELETE_WELCOME_OFF"])
		except AssertionError as e:
			await send_message_check_reply(conv, '/trigger_delete_welcome' , TEXT["en"]["DELETE_WELCOME_ON"])
			await send_message_check_reply(conv, '/trigger_delete_welcome' , TEXT["en"]["DELETE_WELCOME_OFF"])
		

async def test_trigger_delete_notes(client,sgi,TEXT):
	async with client.conversation(sgi) as conv:
		try:
			await send_message_check_reply(conv, '/trigger_delete_notes', TEXT["en"]["DELETE_NOTES_ON"])
			await send_message_check_reply(conv, '/trigger_delete_notes' , TEXT["en"]["DELETE_NOTES_OFF"])
		except AssertionError as e:
			await send_message_check_reply(conv, '/trigger_delete_notes' , TEXT["en"]["DELETE_NOTES_ON"])
			await send_message_check_reply(conv, '/trigger_delete_notes' , TEXT["en"]["DELETE_NOTES_OFF"])


###real time tests end here###


def setup_real_bot(token):
	os.system("bash setup_bot.sh {}".format(token))

async def main():
	async with TelegramClient(session_file, api_id, api_hash) as client:
		# Fill session cache with chats that we can see
		# We need this since otherwise we don't know the access
		# hash of the group and channel
		await client.get_dialogs()
		os.system("mkdir data")
		bot_data = {}
		first_run = False
		try :
			with open('data/bot_data.json') as json_file:
				data = json.load(json_file)
		except Exception as e:
			data = await setup_bot(client)
			first_run = True
		print(data)
		if not "super_group_id" in data:
			data = await setup_bot(client)
			first_run = True
		with open('data/bot_data.json', 'w') as outfile:
			json.dump(data, outfile)
		#setup_real_bot(data["token"])
		#print("sleep so bot can start")
		#time.sleep(10)
		#await run_tests(client,data["super_group_id"])
		if first_run:
			print("please start bot with created token and restart this script!")
			sys.exit(0)
		else:
			await run_tests(client,data["super_group_id"])
			print("All tests finished!")

if __name__ == '__main__':
	import logging

	logging.basicConfig(level=logging.INFO)

	loop.run_until_complete(main())
