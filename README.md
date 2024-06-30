## Why I create this project?

When I found out I had to finish the Second Classroom, I thought it would be very crazy, so I decided to develop this
project to finish the Second Classroom. In my mind, it can gather information about my school -- because I want to let it
solve the problem of my school, and some day I will let it be able to be used in every area. I think it will be very
interesting.

## Badges

[![codebeat badge](https://codebeat.co/badges/3b87724b-fee1-43d4-8eba-a08c6a744881)](https://codebeat.co/projects/github-com-mryan2005-sspu-bot-main)

## which system can use it?
| System  | Can use it? |
|:-------:|:-----------:|
| Windows |     Yes     |
|  Linux  |     Yes     |
|  MacOS  |     No      |

## How to use it?

### on Docker

firstly, you need create a setting file named `settings.json` in the settings folder which is in the data folder.
then, you need to write the following code in the `settings.json` file:

```json
{
  "url": "the url of forum which you want to send the message to",
  "token": "token",
  "weixinUsername": "your Weixin Official Account username",
  "weixinPassword": "your Weixin Official Account password"
}
```

then, you need to run the following code in the terminal:

```shell
docker build -t sspu-bot .
```

Pay attention to this thing: you need to add the settings.json file to the data folder of the container.
then, you need to run the following code in the terminal:

```shell
docker run -d --name sspu-bot sspu-bot
```

or run this following code:

```shell
docker pull ghcr.io/mryan2005/sspu-bot:latest
```

Pay attention to this thing: you need to add the settings.json file to the data folder of the container.
then, you need to run the following code in the terminal:

```shell
docker run -d --name sspu-bot ghcr.io/mryan2005/sspu-bot:latest
```
finally, you need to run the following code in the terminal:

```shell
docker logs sspu-bot
```

then, you can see the logs of the bot.
you should wait it to finish the login process, and then you can use it.
if you see the 1.png file in the root folder, it means you have to scan the QR code to log in.

### on Desktop

firstly, you should install the python3.9, pip, gockodriver and firefox.
then, you need create a setting file named `settings.json` in the settings folder which is in the data folder.
Additionally, you need to write the following code in the `settings.json` file:

```json
{
  "url": "the url which you want to send the message to",
  "token": "token",
  "weixinUsername": "your Weixin Official Account username",
  "weixinPassword": "your Weixin Official Account password"
}
```

finally, you need to run the following code in the terminal:

```shell
pip install -r requirements.txt
python main.py
```

## Contact Me
[Email](mailto:SSPUBot@mryan2005.top)
