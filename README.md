# butter_bot
This bot manages telegram groups. Uses [TLG_JoinCaptchaBot](https://github.com/J-Rios/TLG_JoinCaptchaBot) for captchas.

### Installation:

Note: Use Python 3 to install and run the Bot, Python 2 support could be broken.

To generate Captchas, the Bot uses [multicolor_captcha_generator library](https://github.com/J-Rios/multicolor_captcha_generator), wich uses Pillow to generate the images.

1. Install Pillow prerequisites:
```
apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
```

2. Get the project and install JoinCaptchaBot requirements:
```
git clone --recurse-submodules https://github.com/J-Rios/TLG_JoinCaptchaBot
pip install -r TLG_JoinCaptchaBot/requirements.txt
```

3. Go to project sources and give execution permission to usage scripts:
```
cd TLG_JoinCaptchaBot/sources
chmod +x run status kill
```

4. Specify Telegram Bot account Token (get it from @BotFather) in "constants.py" file:
```
Change 'TOKEN' : 'XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
```

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
