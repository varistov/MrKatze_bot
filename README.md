# butter_bot
I manage your telegram groups. I use [TLG_JoinCaptchaBot](https://github.com/J-Rios/TLG_JoinCaptchaBot) for captchas.

## Features:
- bot protection: verify new users with captchas, auto kick spamming bots

- log protection: let me manage your invitation links; bots can not even join your group

- notes: add notes for your user

- connect: manage your group settings in private

- auto-delete: I do not spam your group, messages are automatically deleted


# Log Protection

*You probably never saw a log protection like that before(I didnt).*

*Any usual bot-protection solution verifies "users" after they joined your group. Any bad bot can dump your whole group history before it fails the verification.*

__This solution verifies users before they can join your group!__

- Set your group to private
- Activate Log Protection with ```/protection```
- Tell users to ask me for an invitation link in private chat
- I will create an invitation link for the user if he passes the captcha
- I revoke the invitation link after a timeout, or after the user joined your group
- Only the verified user can join your group. If another user uses the generated link, I will kick him and revoke the link
### Installation:

Note: Use Python 3 to install and run the Bot, Python 2 support could be broken.

To generate Captchas, the Bot uses [multicolor_captcha_generator library](https://github.com/J-Rios/multicolor_captcha_generator), wich uses Pillow to generate the images.

1. Install Pillow prerequisites:
```
apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
```

2. Get the project and install JoinCaptchaBot requirements:
```
git clone --recurse-submodules https://github.com/v1nc/butter_bot/
pip install -r butter_bot/requirements.txt
```

3. Go to project sources and give execution permission to usage scripts:
```
cd butter_bot/sources
chmod +x run status kill
```

4. Specify Telegram Bot account Token (get it from @BotFather) in "constants.py" file:
```
Change 'TOKEN' : 'XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
```
5. Edit `OWNER` and `OWNER_NAME` to match your account details!
### Usage:

To ease usage, a run, status and kill scripts has been provided.

- Launch the Bot:
```
./run
```

- Check if the script is running:
```
./status
```

- Stop the Bot:
```
./kill
```

### Testing:

You can use telethon for automate testing. Only rudimentary logic gets tested, please extend it :p

1. Get API_ID and API_HASH from my.telegram.org and export them:
```
export API_ID=your_api_id
export API_HASH=your_api_hash
```

2. Run ```tests/test.py``` to register a test bot, create a group and setup admin permissions

3. Copy bot token from ```tests/bot_data.json``` to ```sources/constants.py```,run bot for tests and perhaps allow bot in group
(Todo: make this more comfortable)

4. Run ```tests/test.py``` again to run the tests.
