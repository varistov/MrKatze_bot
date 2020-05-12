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

## read about installation & usage in the [wiki](https://github.com/v1nc/butter_bot/wiki)
